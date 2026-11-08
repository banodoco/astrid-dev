#!/usr/bin/env python3
"""Validate Astrid Dev's documentation index and local links (stdlib only)."""
from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path
from urllib.parse import unquote

from gap_relationships import parse_gap_relationships
from project_contract import PLAN_FOLDER, plan_gap_ids

ROOT = Path(__file__).resolve().parents[1]
CATALOG = Path('plans/index.md')
RELEASES = Path('plans/releases.md')
README = Path('README.md')
HEADER = '| Project | Goal | Status | Owner | Estimate | Waiting on | Plan |'
DIVIDER = '|---|---|---|---|---:|---|---|'
RELEASE_HEADER = ('| Release | Version | Kind | Date | App commit | Agent | Runtime | Pinokio | Required '
                  '| Projects | Owner go |')
RELEASE_DIVIDER = '|---|---|---|---|---|---|---|---|---|---|---|'
RELEASE_KINDS = {'patch', 'minor', 'major'}
LEGACY_RELEASE = 9
LEGACY_VERSION = '0.0.9'
STATUSES = {'queued', 'active', 'blocked', 'paused', 'done', 'cancelled'}
VISIBLE = {'queued', 'active', 'blocked', 'paused'}
LINK = re.compile(r'(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)')
PLAN_LINK = re.compile(r'\[[^\]]+\]\(([^)]+/plan\.md)\)')
GAP_NAME = re.compile(r'([A-Z]{1,3}-\d{3})-[a-z0-9-]+\.md')
VERSION = re.compile(r'\d+\.\d+\.\d+')
DATE = re.compile(r'\d{4}-\d{2}-\d{2}')
FULL_SHA = re.compile(r'[0-9a-f]{40}')
PLACEHOLDERS = {'', '—', '-', 'tbd', 'none', 'unassigned'}


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


def next_version(version: str, kind: str) -> str:
    """The successor of a version for a patch, minor or major release."""
    major, minor, patch = (int(part) for part in version.split('.'))
    if kind == 'major':
        return f'{major + 1}.0.0'
    if kind == 'minor':
        return f'{major}.{minor + 1}.0'
    return f'{major}.{minor}.{patch + 1}'


def release_log_rows(text: str) -> list[list[str]]:
    """Parse one canonical eleven-column release table and validate each add-only row in order."""
    lines = text.splitlines()
    heads = [i for i, line in enumerate(lines) if line.strip() == RELEASE_HEADER]
    if len(heads) != 1 or lines[heads[0] + 1].strip() != RELEASE_DIVIDER:
        raise ValueError('plans/releases.md needs one canonical release table')
    rows: list[list[str]] = []
    for line in lines[heads[0] + 2:]:
        if not line.startswith('|'):
            break
        cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
        if len(cells) != 11 or not all(cells):
            raise ValueError(f'malformed release row: {line}')
        rows.append(cells)
    if not rows:
        raise ValueError('release log is empty')
    previous: tuple[int, str] | None = None
    for row in rows:
        release, version, kind, day, app, agent, runtime, pinokio, required, projects, owner = row
        if not release.isdigit():
            raise ValueError(f'release number must be an integer: {release}')
        number = int(release)
        if not VERSION.fullmatch(version):
            raise ValueError(f'Release {number} version must be major.minor.patch: {version}')
        if previous is None:
            if (number, version, kind) != (LEGACY_RELEASE, LEGACY_VERSION, 'legacy'):
                raise ValueError(f'the log must start with the legacy row Release {LEGACY_RELEASE} = {LEGACY_VERSION}')
        else:
            if number != previous[0] + 1:
                raise ValueError(f'release gap: Release {number} follows Release {previous[0]}; '
                                 'release numbers go up by exactly 1')
            if kind not in RELEASE_KINDS:
                raise ValueError(f'Release {number} kind must be patch, minor or major: {kind}')
            expected = next_version(previous[1], kind)
            if version != expected:
                raise ValueError(f'wrong version step: Release {number} is a {kind} after {previous[1]}, '
                                 f'so it must be {expected}, not {version}')
        if not DATE.fullmatch(day):
            raise ValueError(f'Release {number} date must be YYYY-MM-DD: {day}')
        date.fromisoformat(day)
        for name, sha in (('App commit', app), ('Agent', agent), ('Runtime', runtime)):
            if not FULL_SHA.fullmatch(sha):
                raise ValueError(f'Release {number} {name} must be a full 40-character SHA: {sha}')
        if pinokio != '—' and not FULL_SHA.fullmatch(pinokio):
            raise ValueError(f'Release {number} Pinokio must be a full SHA or — when not recorded: {pinokio}')
        if required.lower() in PLACEHOLDERS:
            raise ValueError(f'Release {number} Required must be no or a reason')
        if owner.lower() in PLACEHOLDERS:
            raise ValueError(f'Release {number} has an empty owner go')
        for link in projects.split(','):
            if not PLAN_LINK.fullmatch(link.strip()):
                raise ValueError(f'Release {number} Projects must be plan.md links: {link.strip()}')
        previous = (number, version)
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

def check(root: Path) -> tuple[list[str], list[str]]:
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
    try:
        release_log_rows(read(root, RELEASES))
    except (OSError, ValueError, IndexError) as exc:
        errors.append(f'release log: {exc}')
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
