#!/usr/bin/env python3
"""Validate Astrid Dev's documentation index and local links (stdlib only)."""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import unquote

from gap_relationships import parse_gap_relationships
from project_contract import PLAN_FOLDER, plan_gap_ids

ROOT = Path(__file__).resolve().parents[1]
CATALOG = Path('plans/index.md')
README = Path('README.md')
HEADER = '| Project | Goal | Status | Owner | Estimate | Waiting on | Plan |'
DIVIDER = '|---|---|---|---|---:|---|---|'
STATUSES = {'queued', 'active', 'blocked', 'paused', 'done', 'cancelled'}
VISIBLE = {'queued', 'active', 'blocked', 'paused'}
LINK = re.compile(r'(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)')
PLAN_LINK = re.compile(r'\[[^\]]+\]\(([^)]+/plan\.md)\)')
GAP_NAME = re.compile(r'([A-Z]{1,3}-\d{3})-[a-z0-9-]+\.md')


def read(root: Path, path: Path) -> str:
    return (root / path).read_text(encoding='utf-8')


def catalog_rows(text: str) -> list[list[str]]:
    """Parse exactly one canonical seven-column Markdown table."""
    lines = text.splitlines()
    heads = [i for i, line in enumerate(lines) if line.strip() == HEADER]
    if len(heads) != 1 or lines[heads[0] + 1].strip() != DIVIDER:
        raise ValueError('plans/index.md needs one canonical plan table')
    rows: list[list[str]] = []
    for line in lines[heads[0] + 2:]:
        if not line.startswith('|'):
            break
        cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
        if len(cells) != 7 or not all(cells):
            raise ValueError(f'malformed plan row: {line}')
        if cells[2] not in STATUSES:
            raise ValueError(f'invalid status {cells[2]!r} in {cells[0]}')
        if not PLAN_LINK.fullmatch(cells[6]):
            raise ValueError(f'plan cell must be a single plan.md link: {cells[6]}')
        rows.append(cells)
    if not rows:
        raise ValueError('plan catalog is empty')
    if any(r[2] in VISIBLE for r in rows[next((i for i, r in enumerate(rows) if r[2] not in VISIBLE), len(rows)):]):
        raise ValueError('done/cancelled rows must follow prioritized nonterminal rows')
    return rows


def local_links(root: Path, path: Path) -> list[str]:
    """Check paths, not GitHub-generated anchor fragments or external URLs."""
    text = read(root, path)
    text = re.sub(r'(?ms)^\s*```.*?^\s*```[^\n]*$', '', text)
    missing = []
    for hit in LINK.finditer(text):
        target = hit.group(1).strip().split(' "', 1)[0].strip('<>')
        if target.startswith(('#', '/', '//')) or re.match(r'^[a-z][\w+.-]*:', target, re.I):
            continue
        target = unquote(target.split('#', 1)[0].split('?', 1)[0])
        if target and not (root / path.parent / target).exists():
            missing.append(f'{path}: missing link target {target}')
    return missing


def unnamed_active_owners(rows: list[list[str]]) -> list[str]:
    """Active work must have one named accountable catalog owner."""
    return [
        f"active project needs a named accountable owner: {row[0]}"
        for row in rows
        if row[2] == 'active' and row[3].strip().lower() in {'unassigned', 'tbd', 'none', '—', '-'}
    ]



def obsolete_template_paths(root: Path) -> list[str]:
    """Reject stale project paths in Markdown, including GitHub's absolute form links."""
    issues: list[str] = []
    for path in root.rglob("*.md"):
        if ".git" not in path.relative_to(root).parts and "strategy/projects/" in path.read_text(encoding="utf-8"):
            issues.append(f"{path.relative_to(root)}: obsolete strategy/projects path; use plans/")
    for obsolete in ("templates/bug-issue.md", "templates/bug-pr.md", "templates/review-submission.md"):
        if (root / obsolete).exists():
            issues.append(f"{obsolete}: obsolete duplicate or ungrouped template")
    return issues

ROUTE_PLAN = re.compile(r"\[Plan (\d{2})\]\(\.\./\.\./plans/([0-9]{2}-[a-z0-9-]+)/plan\.md\)")
ROUTE_STATUS = re.compile(r"\b(active|queued|blocked|paused|done|cancelled)\b", re.I)


def gap_section(text: str, title: str) -> str | None:
    match = re.search(r"^## " + re.escape(title) + r"\s*$", text, re.M)
    if not match:
        return None
    tail = text[match.end():]
    end = re.search(r"^## ", tail, re.M)
    return (tail[:end.start()] if end else tail).strip()


def route_issues(name: str, gap_id: str, text: str, plans: dict[str, str]) -> list[str]:
    """Route to closure: structure and two-way links only, never strategic merit.

    `plans` maps a plan folder name (for example '33-unblock') to its plan.md text.
    """
    issues: list[str] = []
    route = gap_section(text, "Route to closure")
    approach = gap_section(text, "Closure approach")
    if route is None:
        return issues
    if not approach:
        issues.append(f"{name}: Route to closure needs a non-empty Closure approach section before it")
    elif text.index("## Closure approach") > text.index("## Route to closure"):
        issues.append(f"{name}: Closure approach must come before Route to closure")
    rows = [line for line in route.splitlines() if line.startswith("|") and not re.fullmatch(r"\|[\s|:-]+\|", line)]
    body = rows[1:] if rows else []
    if not body:
        issues.append(f"{name}: Route to closure needs at least one step row")
    for line in body:
        for match in ROUTE_STATUS.finditer(line):
            issues.append(f"{name}: route row carries status/ownership word '{match.group(1)}'; the catalog owns it")
        for _, folder in ROUTE_PLAN.findall(line):
            plan = plans.get(folder)
            if plan is None:
                issues.append(f"{name}: route names missing plan {folder}")
                continue
            try:
                declared = plan_gap_ids(plan)
            except ValueError:
                declared = []
            if gap_id not in declared:
                issues.append(f"{name}: routed plan {folder} does not name {gap_id} in its Vision gaps line")
            if not re.search(r"^\*\*Contributes to closure:\*\*.*\b" + re.escape(gap_id) + r"\b", plan, re.M):
                issues.append(f"{name}: routed plan {folder} needs a 'Contributes to closure:' line naming {gap_id}")
    return issues


STRATEGY = Path('strategy.md')
STRATEGY_HEADER = '| Order | When | Gap | Plans | What creators get | Waiting on |'
STRATEGY_WHEN = {'Now', 'Next', 'Later'}
STRATEGY_SECTIONS = ('## Focus now', '## Sequence', '## Not now', '## Decisions')
GAP_LINK = re.compile(r'\[[^\]]+\]\((?:\.\./)*vision/gaps/[A-Z]{1,3}-\d{3}-[a-z0-9-]+\.md\)')
ANY_PLAN_LINK = re.compile(r'\[[^\]]+\]\((?:\.\./)*plans/[^)]+/plan\.md\)')


def strategy_errors(text: str) -> list[str]:
    """strategy.md has its sections, a review date and a structured sequence table."""
    errors = [f'strategy.md: missing section {name}' for name in STRATEGY_SECTIONS
              if not re.search(rf'^{re.escape(name)}\s*$', text, re.M)]
    if not re.search(r'^\*\*Last reviewed:\*\* \d{4}-\d{2}-\d{2}', text, re.M):
        errors.append('strategy.md: needs a "**Last reviewed:** YYYY-MM-DD" line')
    lines = text.splitlines()
    heads = [i for i, line in enumerate(lines) if line.strip() == STRATEGY_HEADER]
    if len(heads) != 1:
        return errors + ['strategy.md: needs one sequence table with the canonical header']
    rows = []
    for line in lines[heads[0] + 2:]:
        if not line.startswith('|'):
            break
        rows.append([cell.strip() for cell in line.strip().strip('|').split('|')])
    if not rows:
        errors.append('strategy.md: the sequence table is empty')
    for cells in rows:
        if len(cells) != 6:
            errors.append(f'strategy.md: malformed sequence row: {"|".join(cells)}')
            continue
        order, when, gap, plans, gets, waiting = cells
        label = f'strategy.md row {order}'
        if not order.isdigit():
            errors.append(f'{label}: Order must be a number')
        if when not in STRATEGY_WHEN:
            errors.append(f'{label}: When must be Now, Next or Later')
        if not GAP_LINK.search(gap):
            errors.append(f'{label}: Gap must link a vision/gaps file')
        if not ANY_PLAN_LINK.search(plans) and '(proposed)' not in plans:
            errors.append(f'{label}: Plans must link a plan.md, or say "(proposed)"')
        if not gets or not waiting:
            errors.append(f'{label}: What creators get and Waiting on must be filled')
    return errors


def check(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        rows = catalog_rows(read(root, CATALOG))
    except (OSError, ValueError, IndexError) as exc:
        return [f'plan catalog: {exc}'], []

    try:
        errors.extend(strategy_errors(read(root, STRATEGY)))
    except OSError as exc:
        errors.append(f'strategy.md: {exc}')
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
        text = file.read_text(encoding='utf-8')
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
        plan_texts = {p.parent.name: p.read_text(encoding='utf-8') for p in (root / 'plans').glob('*/plan.md')}
        errors.extend(route_issues(file.name, gap_id, text, plan_texts))

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
    mandatory = [README, CATALOG, Path('vision/README.md'),
                 Path('CONTRIBUTING.md'),
                 Path('templates/project/plan.md'), Path('docs/project-format.md'),
                 Path('docs/contribution-design-principles.md'),
                 Path('docs/contribution-workflow.md'), Path('docs/contribution-automation-setup.md'),
                 Path('templates/product-pr/review.md')]
    for stale in ('AGENTS.md', 'visions', 'vision/vision.md', 'vision/principles.md', 'vision/gaps.md'):
        if (root / stale).exists():
            errors.append(f'obsolete source must be removed: {stale}')
    expected_principles = {'local-first-cloud-capable', 'open-by-design', 'in-the-creators-control', 'eliminate-needless-technical-wrangling'}
    actual_principles = {p.stem for p in (root / 'vision/principles').glob('*.md')}
    if actual_principles != expected_principles:
        errors.append(f'expected four canonical principle pages, got {sorted(actual_principles)}')
    errors.extend(obsolete_template_paths(root))
    # Every Markdown file must be current. No grandfathered dead references.
    # Product evidence and old task cards must either have valid local links
    # or be removed/replaced by their authoritative project source.
    mandatory += [p.relative_to(root) for p in root.rglob("*.md")
                  if ".git" not in p.relative_to(root).parts]
    for path in sorted(set(mandatory)):
        errors.extend(local_links(root, path))

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args()
    errors, warnings = check(ROOT)
    for issue in warnings:
        print(f'WARN {issue}')
    for issue in errors:
        print(f'ERROR {issue}')
    if errors:
        print(f'Document validation failed with {len(errors)} error(s).')
        return 1
    print('Documentation structure, project catalog and every Markdown local link: OK')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
