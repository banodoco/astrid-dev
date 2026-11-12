"""Registry contract for repository checks."""
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Literal
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))




# Documentation rules retain the legacy order and skip after a bad catalog.
def _catalog(context):
    from check_docs import catalog_rows, read, CATALOG
    try:
        catalog_rows(read(context.root, CATALOG))
    except (OSError, ValueError, IndexError) as exc:
        return [f"plan catalog: {exc}"]
    return []


def _release_documents(context):
    from check_docs import catalog_rows, read, CATALOG, release_errors
    root = context.root
    try:
        rows = catalog_rows(read(root, CATALOG))
    except (OSError, ValueError, IndexError):
        return []
    errors = []
    release_folder = root / 'releases'
    if not (release_folder / 'TEMPLATE.md').is_file():
        errors.append('releases/TEMPLATE.md: missing canonical release template')
    release_docs = {p.name: read(root, p.relative_to(root))
                    for p in release_folder.glob('[0-9]*.md') if p.stem.isdigit()}
    for filename, body in release_docs.items():
        errors.extend(release_errors(filename, body))
    return errors


def _strategy_consistency(context):
    from check_docs import catalog_rows, read, CATALOG, STRATEGY, strategy_errors
    root = context.root
    try:
        rows = catalog_rows(read(root, CATALOG))
    except (OSError, ValueError, IndexError):
        return []
    errors = []
    release_folder = root / 'releases'
    release_docs = {p.name: read(root, p.relative_to(root)) for p in release_folder.glob('[0-9]*.md') if p.stem.isdigit()}
    try:
        errors.extend(strategy_errors(read(root, STRATEGY), release_docs))
    except OSError as exc:
        errors.append(f'strategy.md: {exc}')
    return errors


def _catalog_paths(context):
    from check_docs import catalog_rows, read, CATALOG, PLAN_LINK, PLAN_FOLDER, unnamed_active_owners
    root = context.root
    try:
        rows = catalog_rows(read(root, CATALOG))
    except (OSError, ValueError, IndexError):
        return []
    errors = []
    indexed: set[Path] = set()
    for row in rows:
        dest = PLAN_LINK.fullmatch(row[6]).group(1)
        plan = Path('plans') / dest
        if plan in indexed:
            errors.append(f'duplicate plan catalog entry: {plan}')
        indexed.add(plan)
        if len(plan.parts) != 3 or plan.parts[2] != 'plan.md' or not PLAN_FOLDER.fullmatch(plan.parts[1]):
            errors.append(f'invalid catalog plan path: {plan}')
        if not (root / plan).is_file():
            errors.append(f'catalog plan missing: {plan}')
    errors.extend(unnamed_active_owners(rows))
    actual = set(Path('plans') / p.parent.name / 'plan.md' for p in (root / 'plans').glob('*/plan.md'))
    for missing in sorted(actual - indexed):
        errors.append(f'plan folder absent from catalog: {missing}')
    for extra in sorted(indexed - actual):
        errors.append(f'catalog references non-plan: {extra}')

    return errors


def _gap_structure(context):
    from check_docs import catalog_rows, read, CATALOG, GAP_NAME, parse_gap_relationships, route_issues
    root = context.root
    try:
        rows = catalog_rows(read(root, CATALOG))
    except (OSError, ValueError, IndexError):
        return []
    errors = []
    gaps = sorted((root / 'vision/gaps').glob('*.md'))
    gap_ids = set()
    for file in gaps:
        match = GAP_NAME.fullmatch(file.name)
        if not match:
            errors.append(f'bad gap filename: {file.name}')
            continue
        gap_id = match.group(1)
        if gap_id in gap_ids:
            errors.append(f'duplicate gap ID: {gap_id}')
        gap_ids.add(gap_id)
        text = read(root, file.relative_to(root))
        if not text.startswith(f'# {gap_id} —'):
            errors.append(f'{file.name}: title must start with gap ID')
        for field in ['**Applies to:**', '**Assessment:**', '## Desired state', '## Current state', '## Gap', '## Closure evidence', '## Sources and reassessment']:
            if field not in text:
                errors.append(f'{file.name}: missing {field}')
        applies = next((s for s in text.splitlines() if s.startswith('**Applies to:**')), '')
        try:
            parse_gap_relationships(applies)
        except ValueError as exc:
            errors.append(f'{file.name}: {exc}')
        plan_texts = {p.parent.name: read(root, p.relative_to(root)) for p in (root / 'plans').glob('*/plan.md')}
        errors.extend(route_issues(file.name, gap_id, text, plan_texts))

    return errors


def _plan_files(context):
    from check_docs import catalog_rows, read, CATALOG, GAP_NAME, plan_gap_ids
    root = context.root
    try:
        rows = catalog_rows(read(root, CATALOG))
    except (OSError, ValueError, IndexError):
        return []
    errors = []
    actual = set(Path('plans') / p.parent.name / 'plan.md' for p in (root / 'plans').glob('*/plan.md'))
    gap_ids = {m.group(1) for p in (root / 'vision/gaps').glob('*.md') if (m := GAP_NAME.fullmatch(p.name))}
    for plan in sorted(actual):
        for name in ('plan.md', 'tasks.md', 'inputs.md'):
            if not (root / plan.parent / name).is_file():
                errors.append(f'{plan.parent}: missing {name}')
        body = read(root, plan)
        try:
            refs = plan_gap_ids(body)
            for gap in refs:
                if gap not in gap_ids:
                    errors.append(f'{plan}: unknown vision gap {gap}')
        except ValueError as exc:
            errors.append(f'{plan}: {exc}')
    return errors


def _subjects(context):
    from check_docs import catalog_rows, read, CATALOG, parse_subject
    root = context.root
    try:
        rows = catalog_rows(read(root, CATALOG))
    except (OSError, ValueError, IndexError):
        return []
    errors = []
    # Do not let pillar and principle docs quietly drift into unrelated prose
    # structures. Both are edited from one authoring template and parsed by
    # the public Vision exporter.
    for folder, prefix in (('pillars', 'Pillar'), ('principles', 'Principle')):
        entries = sorted((root / 'vision' / folder).glob('*.md'))
        if len(entries) != 4:
            errors.append(f'vision/{folder}: expected exactly four canonical subjects')
        for file in entries:
            relative = file.relative_to(root)
            try:
                parse_subject(read(root, relative), relative.as_posix())
            except ValueError as exc:
                errors.append(str(exc))
    return errors


def _obsolete_sources(context):
    from check_docs import catalog_rows, read, CATALOG
    root = context.root
    try:
        rows = catalog_rows(read(root, CATALOG))
    except (OSError, ValueError, IndexError):
        return []
    errors = []
    for stale in ('AGENTS.md', 'visions', 'vision/vision.md', 'vision/principles.md', 'vision/gaps.md'):
        if (root / stale).exists():
            errors.append(f'obsolete source must be removed: {stale}')
    return errors


def _canonical_principles(context):
    from check_docs import catalog_rows, read, CATALOG
    root = context.root
    try:
        rows = catalog_rows(read(root, CATALOG))
    except (OSError, ValueError, IndexError):
        return []
    errors = []
    expected_principles = {'local-first-cloud-capable', 'open-by-design', 'in-the-creators-control', 'eliminate-needless-technical-wrangling'}
    actual_principles = {p.stem for p in (root / 'vision/principles').glob('*.md')}
    if actual_principles != expected_principles:
        errors.append(f'expected four canonical principle pages, got {sorted(actual_principles)}')
    return errors


def _obsolete_templates(context):
    from check_docs import catalog_rows, read, CATALOG, obsolete_template_paths
    root = context.root
    try:
        rows = catalog_rows(read(root, CATALOG))
    except (OSError, ValueError, IndexError):
        return []
    errors = []
    errors.extend(obsolete_template_paths(root))
    return errors


def _ledger(context):
    from check_docs import catalog_rows, read, CATALOG, ledger_errors
    root = context.root
    try:
        rows = catalog_rows(read(root, CATALOG))
    except (OSError, ValueError, IndexError):
        return []
    errors = []
    errors.extend(ledger_errors(root))
    return errors


def _markdown_links(context):
    from check_docs import catalog_rows, read, CATALOG, README, local_links
    root = context.root
    try:
        rows = catalog_rows(read(root, CATALOG))
    except (OSError, ValueError, IndexError):
        return []
    errors = []
    mandatory = [README, CATALOG, Path('vision/README.md'),
                 Path('vision/templates/subject.md'),
                 Path('CONTRIBUTING.md'),
                 Path('templates/project/plan.md'), Path('docs/project-format.md'),
                 Path('docs/contribution-design-principles.md'),
                 Path('docs/contribution-workflow.md'), Path('docs/contribution-automation-setup.md'),
                 Path('templates/product-pr/review.md')]
    # Every Markdown file must be current. No grandfathered dead references.
    # Product evidence and old task cards must either have valid local links
    # or be removed/replaced by their authoritative project source.
    mandatory += [p.relative_to(root) for p in root.rglob("*.md")
                  if ".git" not in p.relative_to(root).parts]
    for path in sorted(set(mandatory)):
        errors.extend(local_links(root, path))

    return errors


def _public_vision(context):
    import export_public_vision
    try:
        page = export_public_vision.build(context.root, '0000000000000000000000000000000000000000')
        expected = export_public_vision.render_readme(context.root, page)
        if (context.root / 'vision/README.md').read_text(encoding='utf-8') != expected:
            return ['public vision content: vision/README.md is stale; run python3 scripts/export_public_vision.py --sync-readme']
        source = (context.root / 'README.md').read_text(encoding='utf-8')
        if source != export_public_vision.render_root_readme(source, page):
            return ['public vision content: README.md vision summary is stale; run python3 scripts/export_public_vision.py --sync-readme']
    except (ValueError, OSError) as exc:
        return [f'public vision content: {exc}']
    return []


def _generated_views(context):
    import views
    errors = views.check(context.root)
    # The legacy public-vision rule owns diagnostics for these two targets.
    legacy_errors = _public_vision(context)
    if legacy_errors:
        errors = [message for message in errors
                  if not message.startswith(('view public-vision ', 'view public-vision:',
                                             'view root-vision-summary ', 'view root-vision-summary:'))]
    return errors


def _body(context):
    if context.body_file:
        return context.body_file.read_text(encoding='utf-8')
    if context.event:
        return json.loads(context.event.read_text(encoding='utf-8')).get('pull_request', {}).get('body') or ''
    return ''


def _completion_impl(context):
    import check_completion as gate
    from check_docs import CATALOG, read
    before = gate.catalog_at_revision(context.base, context.root)
    if before is None:
        return []
    after = read(context.root, CATALOG)
    changes = gate.transitions_to_done(before, after)
    if not changes:
        return []
    body = _body(context)
    errors = gate.check_pr(before, after, body, context.root)
    errors.extend(gate.strategy_errors(gate.changed_paths(context.base, context.root)))
    return errors


def _boundary_impl(context):
    import check_gap_boundaries as gate
    from gap_relationships import parse_gap_relationships
    from records import read_text
    required = gate.affected_gaps(context.base, context.root)
    if not required:
        return []
    body = _body(context)
    expected = {}
    for gap_id in sorted(required):
        paths = list((context.root / 'vision/gaps').glob(gap_id + '-*.md'))
        if len(paths) > 1:
            raise ValueError(f'{gap_id}: duplicate gap files')
        if paths:
            meta = next((line for line in read_text(context.root, paths[0].relative_to(context.root)).splitlines() if line.startswith('**Applies to:**')), '')
            expected[gap_id] = parse_gap_relationships(meta)
        else:
            expected[gap_id] = None
    return gate.check_pr(required, body, expected)


def _planning_impl(context):
    import check_project_planning as gate
    from records import read_text
    names = gate.changed_projects(context.base, context.root)
    errors = []
    for name in sorted(names):
        errors.extend(gate.validate_pack(name, read_text(context.root, Path('plans') / name / 'inputs.md')))
    return errors


def _completion(context):
    try:
        return _completion_impl(context)
    except (OSError, ValueError) as exc:
        return [f"completion gate: {exc}"]


def _boundary(context):
    try:
        return _boundary_impl(context)
    except (OSError, ValueError) as exc:
        return [f"gap boundary gate: {exc}"]


def _planning(context):
    try:
        return _planning_impl(context)
    except (OSError, ValueError) as exc:
        return [f"project evidence: {exc}"]


@dataclass(frozen=True)
class Context:
    root: Path
    base: str | None = None
    event: Path | None = None
    body_file: Path | None = None


@dataclass(frozen=True)
class Check:
    id: str
    trigger: Literal["always", "pr"]
    description: str
    run: Callable[[Context], list[str]]

    def __post_init__(self):
        if not self.id or any(c.isspace() for c in self.id):
            raise ValueError("check id must be a nonempty token")
        if self.trigger not in ("always", "pr"):
            raise ValueError("check trigger must be always or pr")
        if not self.description.strip() or "\n" in self.description or "\r" in self.description:
            raise ValueError("check description must be one nonempty line")
        if not callable(self.run):
            raise ValueError("check must be callable")


REGISTRY: tuple[Check, ...] = (
    Check('plan-catalog', 'always', 'Parse the plan catalog', _catalog),
    Check('release-documents', 'always', 'Validate release documents', _release_documents),
    Check('strategy-consistency', 'always', 'Validate strategy consistency', _strategy_consistency),
    Check('catalog-paths', 'always', 'Validate catalog paths', _catalog_paths),
    Check('gap-structure', 'always', 'Validate gap structure', _gap_structure),
    Check('plan-files', 'always', 'Validate plan files', _plan_files),
    Check('subjects', 'always', 'Validate subjects', _subjects),
    Check('obsolete-sources', 'always', 'Validate obsolete sources', _obsolete_sources),
    Check('canonical-principles', 'always', 'Validate canonical principles', _canonical_principles),
    Check('obsolete-templates', 'always', 'Validate obsolete templates', _obsolete_templates),
    Check('ledger', 'always', 'Validate ledger', _ledger),
    Check('markdown-links', 'always', 'Validate markdown links', _markdown_links),
    Check('public-vision-content', 'always', 'Validate generated public vision summaries', _public_vision),
    Check('generated-views', 'always', 'Validate that each generated view matches its sources', _generated_views),
    Check('completion-assessment', 'pr', 'Require evidence for plans newly marked done', _completion),
    Check('gap-boundary-assessment', 'pr', 'Require a first-principles assessment for redefined gaps', _boundary),
    Check('project-planning-evidence', 'pr', 'Validate planning evidence for new or opted-in projects', _planning),
)
