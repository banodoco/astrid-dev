#!/usr/bin/env python3
"""Migrate the hand-written plan catalog into project record files."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

import check_docs
from records import split_table_row

FIELDS = ('Project', 'Goal', 'Status', 'Owner', 'Estimate', 'Waiting on')
PLAN_LINK = re.compile(r'\[[^\]]+\]\(([^)]+/plan\.md)\)')
FIELD_LINE = re.compile(r'^\*\*(Project|Goal|Status|Owner|Estimate|Waiting on):\*\*')


def _table(root: Path, revision: str | None, suffix: str | None) -> list[list[str]]:
    if suffix:
        text = (root / ('plans/index.md' + suffix)).read_text(encoding='utf-8')
    else:
        result = subprocess.run(['git', 'show', f'{revision}:plans/index.md'], cwd=root,
                                check=True, capture_output=True, text=True)
        text = result.stdout
    return check_docs.catalog_rows(text)


def _relative(value: str, folder: str) -> str:
    """Rebase links from plans/index.md to plans/<folder>/plan.md."""
    def replace(match: re.Match[str]) -> str:
        target = match.group(1)
        if re.match(r'^[a-z][a-z0-9+.-]*:', target) or target.startswith(('#', '/')):
            return match.group(0)
        return match.group(0).replace(f']({target})', f'](../{target})')
    return re.sub(r'(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)', replace, value)


def migrate(root: Path, rows: list[list[str]], suffix: str | None = None) -> dict[Path, str]:
    plans_dir = root / 'plans'
    extension = suffix or ''
    folders: list[str] = []
    values_by_folder: dict[str, list[str]] = {}
    for row in rows:
        match = PLAN_LINK.fullmatch(row[6])
        if not match:
            raise ValueError(f'plan cell must be a single plan.md link: {row[6]}')
        folder = Path(match.group(1)).parent.name
        folders.append(folder)
        values_by_folder[folder] = [_relative(value, folder) for value in row[:6]]

    planned: dict[Path, str] = {}
    found: set[str] = set()
    for folder in folders:
        rel = Path('plans') / folder / ('plan.md' + extension)
        path = root / rel
        if not path.is_file():
            raise ValueError(f"missing plan: {rel.as_posix()}")
        found.add(folder)
        text = path.read_text(encoding='utf-8')
        lines = text.splitlines(keepends=True)
        if not lines or not lines[0].startswith('# '):
            raise ValueError(f'{rel.as_posix()}: line 1 is not a title')
        header_end = next((i for i, line in enumerate(lines) if line.startswith('## ')), len(lines))
        block_start, block_end = 2, 14
        labels_in_header = [i for i, line in enumerate(lines[:header_end]) if FIELD_LINE.match(line.rstrip('\r\n'))]
        expected = [f'**{field}:**' for field in FIELDS]
        block_lines = [line.rstrip('\r\n') for line in lines[block_start:block_end:2]]
        block_labels = [FIELD_LINE.match(line).group(1) if FIELD_LINE.match(line) else None
                        for line in block_lines]
        is_block = (block_end <= len(lines) and block_labels == list(FIELDS)
                    and len(lines) >= block_end)
        outside = [i for i in labels_in_header if not (block_start <= i < block_end)]
        if outside:
            raise ValueError(f'{rel.as_posix()}: field label appears outside migration block')
        if not is_block and labels_in_header:
            raise ValueError(f'{rel.as_posix()}: field label appears outside migration block')
        values = values_by_folder[folder]
        block = ''.join(f'**{field}:** {value}\n\n' for field, value in zip(FIELDS, values))
        if is_block:
            new_text = ''.join(lines[:block_start]) + block + ''.join(lines[block_end:])
        else:
            # Card contract requires the title and blank second line.
            if len(lines) < 2 or lines[1].strip():
                raise ValueError(f'{rel.as_posix()}: line 2 must be blank')
            new_text = ''.join(lines[:2]) + block + ''.join(lines[2:])
        planned[rel] = new_text

    for path in plans_dir.glob('*/plan.md' + extension):
        folder = path.parent.name
        if folder not in found:
            raise ValueError(f'folder has no catalog row: plans/{folder}')
    priority = ('# Plan priority\n\nPriority follows this order among open plans.\n'
                'Plans omitted from the list follow the listed plans.\n\n## Order\n' +
                ''.join(f'- {folder}\n' for folder in folders))
    priority_rel = Path('plans/priority.md' + extension)
    planned[priority_rel] = priority
    return planned


def verify(root: Path, rows: list[list[str]], suffix: str | None = None) -> None:
    """Check that record headers reproduce the source table in its row order."""
    extension = suffix or ''
    for row in rows:
        match = PLAN_LINK.fullmatch(row[6])
        if not match:
            raise ValueError(f'plan cell must be a single plan.md link: {row[6]}')
        folder = Path(match.group(1)).parent.name
        path = root / 'plans' / folder / ('plan.md' + extension)
        if not path.is_file():
            raise ValueError(f'missing plan: {path.relative_to(root).as_posix()}')
        text = path.read_text(encoding='utf-8')
        header = text.split('## ', 1)[0]
        actual: dict[str, str] = {}
        for line in header.splitlines():
            found = FIELD_LINE.match(line)
            if found:
                name = found.group(1)
                actual[name] = line[found.end():].strip()
        for field, catalog_value in zip(FIELDS, row[:6]):
            if actual.get(field) != _relative(catalog_value, folder):
                raise ValueError(f'{path.relative_to(root).as_posix()}: {field} does not match catalog')


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--from-ref', required=True)
    parser.add_argument('--suffix')
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        rows = _table(root, args.from_ref, args.suffix)
        planned = migrate(root, rows, args.suffix)
        for rel, text in planned.items():
            path = root / rel
            old = path.read_text(encoding='utf-8') if path.exists() else None
            if args.write:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding='utf-8')
                state = 'unchanged' if old == text else 'written'
                print(f'{rel}: {state}')
            else:
                state = 'no change' if old == text else 'planned'
                print(f'{rel}: {state}')
                if rel.name.startswith('plan.md'):
                    print(''.join(text.splitlines(keepends=True)[2:14]), end='')
                else:
                    print(text, end='' if text.endswith('\n') else '\n')
        if args.verify:
            verify(root, rows, args.suffix)
            print('verify: project records match catalog')
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f'migrate_catalog: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
