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
BEGIN = '<!-- plans:top10:start -->'
END = '<!-- plans:top10:end -->'
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


def preview(rows: list[list[str]]) -> str:
    selected = [r for r in rows if r[2] in VISIBLE][:10]
    output = [HEADER, DIVIDER]
    for row in selected:
        cells = list(row)
        cells[6] = cells[6].replace('](', '](plans/', 1)
        output.append('| ' + ' | '.join(cells) + ' |')
    return '\n'.join(output)


def replace_preview(text: str, rendered: str) -> str:
    if text.count(BEGIN) != 1 or text.count(END) != 1:
        raise ValueError('README needs exactly one top-ten marker pair')
    a, b = text.index(BEGIN) + len(BEGIN), text.index(END)
    if a >= b:
        raise ValueError('README top-ten markers out of order')
    return text[:a] + '\n' + rendered + '\n' + text[b:]


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


def check(root: Path, sync: bool = False) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        rows = catalog_rows(read(root, CATALOG))
    except (OSError, ValueError, IndexError) as exc:
        return [f'plan catalog: {exc}'], []

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

    try:
        current = read(root, README)
        expected = replace_preview(current, preview(rows))
        if current != expected:
            if sync:
                (root / README).write_text(expected, encoding='utf-8')
            else:
                errors.append('README top ten is stale; run python3 scripts/check_docs.py --sync')
    except (OSError, ValueError) as exc:
        errors.append(f'README preview: {exc}')

    gaps = sorted((root / 'visions/gaps').glob('*.md'))
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
    # The archive is a pointer, never a second status table.
    if '| Project | Status |' in read(root, Path('ARCHIVE.md')):
        errors.append('ARCHIVE.md contains a duplicate plan registry')

    mandatory = [README, CATALOG, Path('ARCHIVE.md'), Path('AGENTS.md'),
                 Path('templates/project/plan.md'), Path('docs/project-format.md')]
    mandatory += [p.relative_to(root) for p in (root / 'visions').rglob('*.md')]
    mandatory += sorted(actual)
    # Include the actual agent entrypoint, domain map and project templates:
    # broken guidance links should fail the same CI as broken plan links.
    mandatory += [p.relative_to(root) for p in (root / 'skills').rglob('*.md')]
    mandatory += [p.relative_to(root) for p in (root / 'templates/project').glob('*.md')]
    for path in sorted(set(mandatory)):
        errors.extend(local_links(root, path))
    # Older task/evidence documents may have legacy references; don't fail this
    # catalog migration on those. Their references can be audited separately.
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sync', action='store_true', help='regenerate README summary from plans/index.md')
    args = parser.parse_args()
    errors, warnings = check(ROOT, args.sync)
    for issue in warnings:
        print(f'WARN {issue}')
    for issue in errors:
        print(f'ERROR {issue}')
    if errors:
        print(f'Document validation failed with {len(errors)} error(s).')
        return 1
    print('Documentation structure, plan catalog, README excerpt and managed local links: OK')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
