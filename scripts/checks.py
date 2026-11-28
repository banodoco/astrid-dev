"""Registry contract for repository checks."""
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Literal
import json
import re
import sys
import subprocess

sys.path.insert(0, str(Path(__file__).resolve().parent))




# Documentation rules retain the legacy order and skip after a bad catalog.
def _catalog(context):
    import lifecycle
    from project_contract import PLAN_FOLDER
    from records import project_fields, project_target_milestone, strategy_milestones, priority_order, section
    root = context.root
    errors = []
    folders = set()
    strategy_path = root / "strategy.md"
    milestones = strategy_milestones(strategy_path.read_text(encoding="utf-8")) if strategy_path.is_file() else ()
    for path in sorted((root / "plans").glob("*/plan.md")):
        folder = path.parent.name
        if not PLAN_FOLDER.fullmatch(folder):
            errors.append(f"plans/{folder}: invalid plan folder name; rename it to the NN-short-name form, like 48-one-record-model")
            continue
        folders.add(folder)
        try:
            text = path.read_text(encoding="utf-8")
            fields = project_fields(text)
            target = project_target_milestone(text)
            if target is not None and target not in milestones:
                errors.append(f"plans/{folder}/plan.md: Target milestone {target} has no authored strategy milestone")
            if fields["Status"] not in lifecycle.names():
                errors.append(f"plans/{folder}/plan.md: invalid status {fields['Status']!r}; use {lifecycle.phrase()}")
        except (ValueError, OSError) as exc:
            errors.append(f"plans/{folder}/plan.md: {exc}")
    priority = root / "plans/priority.md"
    priority_text = priority.read_text(encoding="utf-8") if priority.exists() else None
    order = priority_order(priority_text)
    order_section = section(priority_text or "", "Order")
    order_heading = re.search(r"^## Order\s*$", priority_text or "", re.M)
    first_order_line = (priority_text[:order_heading.start()].count("\n") + 2) if order_heading else 1
    for line_number, line in enumerate(order_section.splitlines(), first_order_line):
        if line.strip() and not re.fullmatch(r"- \d{2,}-[a-z0-9-]+", line):
            errors.append(f"plans/priority.md: invalid line {line_number} under ## Order; fix it to - <folder-id>")
    seen = set()
    for folder in order:
        if folder in seen:
            errors.append(f"plans/priority.md: duplicate {folder} under ## Order; delete one of its lines")
        if folder not in folders:
            errors.append(f"plans/priority.md: unknown {folder} under ## Order (there is no plans/{folder}/plan.md); fix the name or delete the line")
        seen.add(folder)
    return errors


def _catalog_ready(context):
    """True when the plan catalog has no errors; the documentation checks skip otherwise."""
    try:
        return not _catalog(context)
    except (OSError, ValueError, IndexError):
        return False


def _unique_project_numbers(context):
    plans = context.root / "plans"
    by_number = {}
    for folder in plans.iterdir():
        if folder.is_dir() and (match := re.match(r"^(\d{2})-", folder.name)):
            by_number.setdefault(match.group(1), []).append(folder.name)
    return [f"duplicate project number {number}: {', '.join(sorted(folders))}"
            for number, folders in sorted(by_number.items()) if len(folders) > 1]


def _release_documents(context):
    from check_docs import read, release_errors
    from records import git_show
    from release_status import validate_change
    root = context.root
    if not _catalog_ready(context):
        return []
    errors = []
    release_folder = root / 'releases'
    if not (release_folder / 'TEMPLATE.md').is_file():
        errors.append('releases/TEMPLATE.md: missing canonical release template')
    release_docs = {p.name: read(root, p.relative_to(root))
                    for p in release_folder.glob('[0-9]*.md') if p.stem.isdigit()}
    for filename, body in release_docs.items():
        errors.extend(release_errors(filename, body))
        if context.base:
            path = f"releases/{filename}"
            before = git_show(root, context.base, path, missing="none")
            errors.extend(f"{path}: {message}" for message in
                          validate_change(root, int(Path(filename).stem), before, body))
    return errors


def _active_plans_in_releases(context):
    from check_docs import read
    from records import active_plan_errors, project_fields, release_brief
    root = context.root
    if not _catalog_ready(context):
        return []
    active = {}
    errors = []
    for path in sorted((root / 'plans').glob('*/plan.md')):
        body = read(root, path.relative_to(root))
        if project_fields(body)['Status'] != 'active':
            continue
        if re.search(r"(?m)^\*\*Run route:\*\* astrid-dev-only\s*$", body):
            inputs = path.parent / 'inputs.md'
            evidence = inputs.read_text(encoding='utf-8') if inputs.is_file() else ''
            pointed = _running_lane_pointer(root, inputs.relative_to(root).as_posix(), evidence)
            if (not pointed
                    and (not re.search(r"(?m)^\*\*Run start:\*\* .+", evidence)
                         or 'owner-authorized' not in
                         next((line for line in evidence.splitlines()
                               if line.startswith('**Run start:**')), ''))):
                errors.append(f"{path.relative_to(root)}: astrid-dev-only active run requires an explicit owner-authorized Run start in inputs.md, or a Run start pointer to a running lane brief")
            continue
        active[path.parent.name[:2]] = path.parent.name
    briefs = [release_brief(read(root, p.relative_to(root)), strict=False)
              for p in sorted((root / 'releases').glob('[0-9]*.md')) if p.stem.isdigit()]
    return [*errors, *active_plan_errors(active, briefs)]


LANE_BRIEF_PATH = re.compile(r"releases/[0-9]+/briefs/[a-z0-9-]+\.md")
LANE_ACTIVE_STATES = ("prepared", "running", "paused")


def _running_lane_pointer(root, inputs, text):
    """True when the inputs.md Run start line links a lane brief whose State is running (contract §3, §5)."""
    from records import is_lane_brief, lane_brief, run_start_briefs
    for target in run_start_briefs(text, inputs):
        brief = root / target
        if LANE_BRIEF_PATH.fullmatch(target) and brief.is_file():
            body = brief.read_text(encoding="utf-8")
            if is_lane_brief(body) and lane_brief(body, target)["state"] == "running":
                return True
    return False


def _lane_brief_files(root):
    """Parsed lane briefs under releases/*/briefs/, keyed by root-relative path; files without **Lane:** are ignored."""
    from records import is_lane_brief, lane_brief
    briefs = {}
    for path in sorted((root / "releases").glob("*/briefs/*.md")):
        text = path.read_text(encoding="utf-8")
        if is_lane_brief(text):
            relative = path.relative_to(root).as_posix()
            briefs[relative] = lane_brief(text, relative)
    return briefs


def _lane_briefs(context):
    from records import LANE_PLAN_FILE, release_brief, run_start_briefs
    root = context.root
    briefs = _lane_brief_files(root)
    errors = []
    lanes = {}
    active = {}
    for relative, brief in briefs.items():
        prefix = f"{relative}: "
        errors.extend(prefix + message for message in brief["errors"])
        number = Path(relative).parts[1]
        stem = Path(relative).stem
        lane = brief["lane"]
        if lane and lane != stem:
            errors.append(prefix + f"**Lane:** {lane} differs from the file name {stem}; the lane slug is the file name without .md")
        if lane:
            lanes.setdefault(lane, []).append(relative)
        if brief["releases"] and str(brief["releases"][0]) != number:
            errors.append(prefix + f"the first **Releases:** number {brief['releases'][0]} differs from the path's release {number}")
        for row in brief["plans"]:
            plan = row["path"]
            if plan is None or not LANE_PLAN_FILE.fullmatch(plan) or not (root / plan).is_file():
                errors.append(prefix + f"Plans and order row {row['label']} does not link an existing plans/<PP>-<slug>/plan.md")
                continue
            folder = Path(plan).parent.name
            release = row["release"]
            if release is not None and release not in brief["releases"]:
                errors.append(prefix + f"{plan}: Release {release} is not in this brief's **Releases:** line")
            if release is not None:
                release_file = root / "releases" / f"{release}.md"
                if not release_file.is_file():
                    errors.append(prefix + f"{plan}: releases/{release}.md does not exist, so the plan is in no Release {release}")
                else:
                    included = {item["folder"] for item in release_brief(release_file.read_text(encoding="utf-8"), strict=False)["plans"]}
                    if folder not in included:
                        errors.append(prefix + f"{plan}: not in releases/{release}.md ## Included plans; list the plan there or fix the Release cell")
            if brief["state"] in LANE_ACTIVE_STATES:
                active.setdefault(folder, []).append(relative)
            if brief["state"] == "done":
                import lifecycle
                from records import project_fields
                status = project_fields((root / plan).read_text(encoding="utf-8")).get("Status")
                if status not in lifecycle.terminal():
                    errors.append(prefix + f"{plan}: Status is {status} while the lane is done; a done lane's plans are done or cancelled, "
                                  "and a plan that moves to another lane or the Lead leaves this brief's Plans and order")
            if brief["state"] in ("running", "paused"):
                inputs = f"plans/{folder}/inputs.md"
                inputs_file = root / inputs
                text = inputs_file.read_text(encoding="utf-8") if inputs_file.is_file() else ""
                if relative not in run_start_briefs(text, inputs):
                    errors.append(prefix + f"{inputs}: the **Run start:** line must link this lane brief ({relative}) while the lane is {brief['state']}")
    for lane, paths in sorted(lanes.items()):
        if len(paths) > 1:
            for relative in paths:
                others = ", ".join(other for other in paths if other != relative)
                errors.append(f"{relative}: lane {lane} is also in {others}; a lane slug names one brief")
    for folder, paths in sorted(active.items()):
        owners = sorted(set(paths))
        if len(owners) > 1:
            errors.append(f"plans/{folder}/plan.md: in more than one active lane brief ({', '.join(owners)}); a plan belongs to one lane")
    return errors


def _strategy_consistency(context):
    from check_docs import read, STRATEGY, strategy_errors
    root = context.root
    if not _catalog_ready(context):
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
    from check_docs import read, PLAN_FOLDER, unnamed_active_owners
    root = context.root
    if not _catalog_ready(context):
        return []
    from records import projects
    try:
        rows = projects(root)
    except (OSError, ValueError, IndexError):
        return []
    return unnamed_active_owners(rows)


def _gap_structure(context):
    from check_docs import read, GAP_NAME, parse_gap_relationships, route_issues
    from gap_relationships import gap_metadata
    root = context.root
    if not _catalog_ready(context):
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
        for field in ['**Aspiration:**', '**Assessment:**', '## Desired state', '## Current state', '## Gap', '## Closure evidence', '## Sources and reassessment']:
            if field not in text:
                errors.append(f'{file.name}: missing {field}')
        try:
            parse_gap_relationships(gap_metadata(text), root / 'vision')
        except ValueError as exc:
            errors.append(f'{file.name}: {exc}')
        plan_texts = {p.parent.name: read(root, p.relative_to(root)) for p in (root / 'plans').glob('*/plan.md')}
        errors.extend(route_issues(file.name, gap_id, text, plan_texts))

    return errors


def _plan_files(context):
    from check_docs import read, GAP_NAME, plan_gap_ids
    root = context.root
    if not _catalog_ready(context):
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
    from check_docs import read, parse_subject
    root = context.root
    if not _catalog_ready(context):
        return []
    errors = []
    # Do not let pillar and principle docs quietly drift into unrelated prose
    # structures. Both are edited from one authoring template and parsed by
    # the public Vision exporter.
    for folder, prefix in (('pillars', 'Pillar'), ('principles', 'Principle')):
        entries = sorted((root / 'vision' / folder).glob('*.md'))
        if len(entries) != 4:
            errors.append(f'vision/{folder}: expected exactly four canonical elements')
        for file in entries:
            relative = file.relative_to(root)
            try:
                parse_subject(read(root, relative), relative.as_posix())
            except ValueError as exc:
                errors.append(str(exc))
    return errors


def _obsolete_sources(context):
    from check_docs import read
    root = context.root
    if not _catalog_ready(context):
        return []
    errors = []
    for stale in ('AGENTS.md', 'visions', 'vision/vision.md', 'vision/principles.md', 'vision/gaps.md',
                  'skills', 'sync.sh'):
        if ((root / stale).exists()
                or stale in ('skills', 'sync.sh') and (root / stale).is_symlink()):
            errors.append(f'obsolete source must be removed: {stale}')
    return errors


def _canonical_principles(context):
    from check_docs import read
    root = context.root
    if not _catalog_ready(context):
        return []
    errors = []
    expected_principles = {'local-first-cloud-capable', 'open-by-design', 'in-the-creators-control', 'eliminate-needless-technical-wrangling'}
    actual_principles = {p.stem for p in (root / 'vision/principles').glob('*.md')}
    if actual_principles != expected_principles:
        errors.append(f'expected four canonical principle pages, got {sorted(actual_principles)}')
    return errors


def _obsolete_templates(context):
    from check_docs import read, obsolete_template_paths
    root = context.root
    if not _catalog_ready(context):
        return []
    errors = []
    errors.extend(obsolete_template_paths(root))
    return errors


def _agent_tests(context):
    from agent_tests import validate
    return validate(context.root)


def _ledger(context):
    from check_docs import read, ledger_errors
    root = context.root
    if not _catalog_ready(context):
        return []
    errors = []
    errors.extend(ledger_errors(root))
    return errors


def _markdown_links(context):
    from check_docs import read, CATALOG, README, local_links
    root = context.root
    if not _catalog_ready(context):
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
                  if ".git" not in p.relative_to(root).parts and ".generated" not in p.relative_to(root).parts]
    for path in sorted(set(mandatory)):
        errors.extend(local_links(root, path))

    return errors


def _link_anchors(context):
    """A #fragment into an agent document, template or top-level doc must name a heading there."""
    import posixpath
    from check_docs import LINK, read
    root, fence = context.root, r"(?ms)^\s*```.*?^\s*```[^\n]*$"

    from document_structure import markdown_heading_anchors

    def anchors(relative):
        return {anchor for _, _, anchor in markdown_heading_anchors(read(root, relative))}

    errors = []
    for path in sorted(p.relative_to(root) for p in root.rglob("*.md") if ".git" not in p.relative_to(root).parts and ".generated" not in p.relative_to(root).parts):
        for hit in LINK.finditer(re.sub(fence, "", read(root, path))):
            address, _, fragment = hit.group(1).strip().split(' "', 1)[0].strip("<>").partition("#")
            if not fragment or re.match(r"^([a-z][\w+.-]*:|/)", address, re.I):
                continue
            target = posixpath.normpath((path.parent / (address or path.name)).as_posix())
            if (re.fullmatch(r"(?:agent|templates)/.+\.md|docs/[^/]+\.md", target) and (root / target).is_file()
                    and fragment not in anchors(Path(target))):
                errors.append(f"{path.as_posix()}: link to {target}#{fragment} matches no heading in that file; point the link at a heading that exists")
    return errors


def _public_vision(context):
    import export_public_vision
    try:
        page = export_public_vision.build(context.root, '0000000000000000000000000000000000000000')
    except (ValueError, OSError) as exc:
        return [f'public vision content: {exc}']
    return []



def _workstream_structure(context):
    from agent_documents import validate_documents
    from views import agent_index_errors
    errors = validate_documents(context.root)
    return errors if errors else agent_index_errors(context.root)


def _generated_views(context):
    import views
    declared, errors = views.views_for(context.root)
    errors = [f'shared blocks: {message}' for message in errors]
    if not context.base:
        return errors
    for view in declared:
        try:
            if views.touched(view, context.root, context.base):
                errors.extend(views.check_view(view, context.root))
        except (OSError, ValueError, subprocess.CalledProcessError) as exc:
            errors.append(f'view {view.name}: cannot check {view.target}: {exc}; '
                          f'{view.target} is generated from {", ".join(view.sources)}, so fix any error there, '
                          'then run python3 scripts/astrid_dev.py sync')
    if _catalog(context):
        errors = [message for message in errors if not message.startswith(("view plan-catalog ", "view plan-catalog:"))]
    # The legacy public-vision rule owns diagnostics for these two targets.
    legacy_errors = _public_vision(context)
    if legacy_errors:
        errors = [message for message in errors
                  if not message.startswith(('view public-vision ', 'view public-vision:',
                                             'view root-vision-summary ', 'view root-vision-summary:'))]
    return errors


def _tracked_generated_skills(context):
    """Refuse tracked generated skill output: SKILL.md anywhere, or anything under .generated/."""
    try:
        result = subprocess.run(["git", "-C", str(context.root), "ls-files", "-z"], capture_output=True)
    except OSError as exc:
        return [f"cannot list tracked files with git ls-files: {exc}"]
    if result.returncode != 0:
        if b"not a git repository" in result.stderr:
            return []  # A tree outside git has no tracked files to refuse.
        return [f"cannot list tracked files with git ls-files: {result.stderr.decode('utf-8', 'replace').strip()}"]
    listed = result.stdout
    errors = []
    for raw in listed.split(b"\0"):
        path = raw.decode("utf-8", "surrogateescape")
        parts = path.split("/")
        if not path or not (parts[-1] == "SKILL.md" or parts[0] == ".generated"):
            continue
        errors.append(f"{path}: generated skill packages must not be tracked; "
                      "edit the agent/ source and rebuild with python3 scripts/astrid_dev.py skills build")
    return errors


def _body(context):
    if context.body_file:
        return context.body_file.read_text(encoding='utf-8')
    if context.event:
        return json.loads(context.event.read_text(encoding='utf-8')).get('pull_request', {}).get('body') or ''
    return ''


def _completion_impl(context):
    import check_completion as gate
    before = gate.project_statuses(context.root, context.base)
    after = gate.project_statuses(context.root)
    changes = gate.transitions_to_done(before, after)
    if not changes:
        return []
    errors = gate.check_pr(changes, _body(context), context.root)
    return errors

def _boundary_impl(context):
    import check_gap_boundaries as gate
    from gap_relationships import gap_metadata, parse_gap_aspirations
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
            meta = gap_metadata(read_text(context.root, paths[0].relative_to(context.root)))
            expected[gap_id] = parse_gap_aspirations(meta, context.root / 'vision')
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


def _pack_shape_impl(context):
    import pack_shape as gate
    root = context.root
    shape = gate.template_shape(root)
    errors = []
    for name in gate.new_packs(context.base, root):
        errors.extend(gate.shape_errors(name, shape, root))
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


def _pack_shape(context):
    try:
        return _pack_shape_impl(context)
    except (OSError, ValueError) as exc:
        return [f"can't check new packs against the templates: {exc}; if the base revision is missing, fetch the PR base, then run the check again"]


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


def _project_delivery(context: Context) -> list[str]:
    from project_delivery import load_delivery

    try:
        load_delivery(context.root)
    except (ValueError, OSError) as exc:
        return [str(exc)]
    return []


REGISTRY: tuple[Check, ...] = (
    Check('plan-catalog', 'always', 'Parse the plan catalog', _catalog),
    Check('unique-project-numbers', 'always', 'Require unique project numbers', _unique_project_numbers),
    Check('release-documents', 'always', 'Validate release documents', _release_documents),
    Check('active-plans-in-releases', 'always', 'Require every active plan in an unpublished release brief', _active_plans_in_releases),
    Check('lane-briefs', 'always', 'Validate lane briefs: shape, plans, releases, active lanes and Run start pointers', _lane_briefs),
    Check('strategy-consistency', 'always', 'Validate strategy structure and release kinds', _strategy_consistency),
    Check('catalog-paths', 'always', 'Validate catalog paths', _catalog_paths),
    Check('gap-structure', 'always', 'Validate gap structure', _gap_structure),
    Check('plan-files', 'always', 'Validate plan files', _plan_files),
    Check('subjects', 'always', 'Validate subjects', _subjects),
    Check('obsolete-sources', 'always', 'Validate obsolete sources', _obsolete_sources),
    Check('canonical-principles', 'always', 'Validate canonical principles', _canonical_principles),
    Check('obsolete-templates', 'always', 'Validate obsolete templates', _obsolete_templates),
    Check('agent-tests', 'always', 'Validate agent-test cases: fields, sections, covered files, chains and results', _agent_tests),
    Check('ledger', 'always', 'Validate ledger', _ledger),
    Check('markdown-links', 'always', 'Validate markdown links', _markdown_links),
    Check('link-anchors', 'always', 'Validate links to headings in agent documents, templates and top-level docs', _link_anchors),
    Check('public-vision-content', 'always', 'Validate public vision source content', _public_vision),
    Check('workstream-structure', 'always', 'Validate canonical agent contracts, routing ownership and declared indexes', _workstream_structure),
    Check('project-delivery', 'always', 'Validate authored project-delivery relationships', _project_delivery),
    Check('generated-views', 'pr', 'Validate generated views that a pull request changes', _generated_views),
    Check('generated-skills-untracked', 'always', 'Refuse tracked SKILL.md files and .generated/ output', _tracked_generated_skills),
    Check('completion-assessment', 'pr', 'Require evidence for plans newly marked done', _completion),
    Check('gap-boundary-assessment', 'pr', 'Require a first-principles assessment for redefined gaps', _boundary),
    Check('project-planning-evidence', 'pr', 'Validate planning evidence for new or opted-in projects', _planning),
    Check('pack-shape', 'pr', 'Check that new project packs follow the templates', _pack_shape),
)
