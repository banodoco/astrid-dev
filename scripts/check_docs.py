"""Validate Astrid Dev's documentation index and local links (stdlib only)."""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

from gap_relationships import parse_gap_relationships
import lifecycle
from project_contract import PLAN_FOLDER, plan_gap_ids
from records import (PLACEHOLDERS_ACTIVE_OWNER, heading_present,
                     is_placeholder, key_value_lines, read_text, section as record_section,
                     split_table_row)
from vision_subject import parse_subject

ROOT = Path(__file__).resolve().parents[1]
CATALOG = Path('plans/index.md')
README = Path('README.md')
LINK = re.compile(r'(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)')
GAP_NAME = re.compile(r'([A-Z]{1,3}-\d{3})-[a-z0-9-]+\.md')


def read(root: Path, path: Path) -> str:
    return read_text(root, path)


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
        if row[2] in lifecycle.requiring("named-owner") and is_placeholder(row[3], PLACEHOLDERS_ACTIVE_OWNER, trim=None)
    ]



def obsolete_template_paths(root: Path) -> list[str]:
    """Reject stale project paths in Markdown, including GitHub's absolute form links."""
    issues: list[str] = []
    for path in root.rglob("*.md"):
        if ".git" not in path.relative_to(root).parts and "strategy/projects/" in read(root, path.relative_to(root)):
            issues.append(f"{path.relative_to(root)}: obsolete strategy/projects path; use plans/")
    for obsolete in ("templates/bug-issue.md", "templates/bug-pr.md", "templates/review-submission.md"):
        if (root / obsolete).exists():
            issues.append(f"{obsolete}: obsolete duplicate or ungrouped template")
    return issues

ROUTE_PLAN = re.compile(r"\[Plan (\d{2})\]\(\.\./\.\./plans/([0-9]{2}-[a-z0-9-]+)/plan\.md\)")
def gap_section(text: str, title: str) -> str | None:
    return record_section(text, title, missing='none', boundary=r'^## ', strip=True)


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
    route_status = re.compile(lifecycle.route_pattern())
    for line in body:
        for match in route_status.finditer(line):
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


LEDGER = Path('docs/ledger')
LEDGER_NAME = re.compile(r'(\d{4}-\d{2}-\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*\.md')
LEDGER_KINDS = {'papercut', 'issue', 'idea', 'fix'}
LEDGER_FIELDS = ('Date', 'Kind', 'Source', 'Resolved by')


def ledger_entry_errors(name: str, text: str, entries: set[str]) -> list[str]:
    """One ledger entry file: name, header fields, kind, date and references."""
    match = LEDGER_NAME.fullmatch(name)
    if not match:
        return [f'docs/ledger/{name}: file name must be YYYY-MM-DD-<short-slug>.md']
    label = f'docs/ledger/{name}'
    header, _, body = text.partition('\n\n')
    fields: dict[str, str] = {}
    for key, sep, value in key_value_lines(header):
        if not sep or key.strip() not in LEDGER_FIELDS or key.strip() in fields:
            return [f'{label}: header must be exactly Date, Kind, Source and Resolved by lines, then a blank line']
        fields[key.strip()] = value
    errors = [f'{label}: missing header field {f}:' for f in LEDGER_FIELDS if not fields.get(f)]
    if fields.get('Kind') and fields['Kind'] not in LEDGER_KINDS:
        errors.append(f'{label}: Kind must be one of {", ".join(sorted(LEDGER_KINDS))}')
    if fields.get('Date') and fields['Date'] != match.group(1):
        errors.append(f'{label}: Date must match the file name prefix {match.group(1)}')
    if not body.strip():
        errors.append(f'{label}: needs entry text after the header')
    refs = [(fields.get('Resolved by', '—'), 'Resolved by')]
    refs += [(m.group(1).strip(), 'Follows') for m in re.finditer(r'^Follows:(.*)$', body, re.M)]
    for ref, field in refs:
        if ref in ('', '—'):
            continue
        target = ref[:-3] if ref.endswith('.md') else ref
        if target + '.md' not in entries or target + '.md' == name:
            errors.append(f'{label}: {field} names no existing entry: {ref}')
    return errors


def ledger_errors(root: Path) -> list[str]:
    folder = root / LEDGER
    files = sorted(p for p in folder.glob('*.md') if p.name != 'README.md')
    entries = {p.name for p in files}
    errors: list[str] = []
    for file in files:
        errors.extend(ledger_entry_errors(file.name, read(root, file.relative_to(root)), entries))
    return errors


STRATEGY = Path('strategy.md')
STRATEGY_HEADER = '| Release | Highlight | Plans | Why this order |'
STRATEGY_SECTIONS = ('## Focus now', '## Sequence', '## Not now', '## Decisions')
RELEASE_ROW = re.compile(r'\[Release ([1-9]\d*) \((draft|final)\)\]\(releases/([1-9]\d*)\.md\)')
RELEASE_PLAN = re.compile(r'\[Plan (\d+)\]\(\.\./plans/([0-9]{2}-[a-z0-9-]+)/plan\.md\)')
STRATEGY_PLAN = re.compile(r'\[Plan (\d+)\]\(plans/([0-9]{2}-[a-z0-9-]+)/plan\.md\)')
RELEASE_SECTIONS = ('Highlight', 'Intent', 'Approach', 'Included plans', 'Publication')


def release_section(body: str, name: str) -> str:
    return record_section(body, name, missing='empty', boundary=r'^## ', strip=True) or ''


def release_errors(filename: str, body: str) -> list[str]:
    """A release brief is valid as a draft, without publication pins."""
    issues = []
    stem = Path(filename).stem
    match = re.search(r'^\*\*Release:\*\* ([1-9]\d*)$', body, re.M)
    if not stem.isdigit() or not match or match.group(1) != stem:
        issues.append(f'releases/{filename}: Release must equal the numeric filename')
    if not re.search(r'^# Release ' + re.escape(stem) + r' — \S.+$', body, re.M):
        issues.append(f'releases/{filename}: title must be # Release {stem} — <title>')
    state = re.search(r'^\*\*State:\*\* (Draft|Final)$', body, re.M)
    if not state:
        issues.append(f'releases/{filename}: State must be Draft or Final')
    sections = {name: release_section(body, name) for name in RELEASE_SECTIONS}
    for name, content in sections.items():
        if not content:
            issues.append(f'releases/{filename}: missing or empty ## {name}')
    highlight = sections['Highlight'].splitlines()
    if highlight and (len(highlight) != 1 or len(highlight[0]) < 15):
        issues.append(f'releases/{filename}: Highlight must be one substantive sentence on one line')
    plans = RELEASE_PLAN.findall(sections['Included plans'])
    if not plans:
        issues.append(f'releases/{filename}: Included plans must link project plan.md files')
    if len({folder for _, folder in plans}) != len(plans):
        issues.append(f'releases/{filename}: duplicated included plan')
    if any(number != folder[:2] for number, folder in plans):
        issues.append(f'releases/{filename}: included plan number does not match its link')
    if state:
        if state.group(1) == 'Draft':
            if 'Not pinned.' not in sections['Publication']:
                issues.append(f'releases/{filename}: draft publication must say Not pinned.')
        else:
            payload = re.search(r'^\x60{3}json\s*\n(\{.*?\})\s*\n\x60{3}', sections['Publication'], re.S | re.M)
            if not payload:
                issues.append(f'releases/{filename}: final publication needs a JSON payload')
            else:
                try:
                    record = json.loads(payload.group(1))
                    required = {'version', 'kind', 'required', 'app', 'agent', 'runtime', 'runtime_schema_digest', 'tools'}
                    if not isinstance(record, dict) or not required <= record.keys():
                        issues.append(f'releases/{filename}: final payload missing manifest fields')
                except json.JSONDecodeError:
                    issues.append(f'releases/{filename}: invalid JSON publication payload')
    return issues


def strategy_errors(text: str, release_docs: dict[str, str] | None = None) -> list[str]:
    """Validate a release-led strategy against its canonical release briefs."""
    errors = [f'strategy.md: missing section {name}' for name in STRATEGY_SECTIONS
              if not heading_present(text, rf'^{re.escape(name)}\s*$')]
    if not re.search(r'^\*\*Last reviewed:\*\* \d{4}-\d{2}-\d{2}', text, re.M):
        errors.append('strategy.md: needs a "**Last reviewed:** YYYY-MM-DD" line')
    lines = text.splitlines()
    heads = [i for i, line in enumerate(lines) if line.strip() == STRATEGY_HEADER]
    if len(heads) != 1:
        return errors + ['strategy.md: needs one release sequence table with the canonical header']
    rows = []
    for line in lines[heads[0] + 2:]:
        if not line.startswith('|'):
            break
        rows.append(split_table_row(line))
    if not rows:
        errors.append('strategy.md: the release sequence table is empty')
    referenced = set()
    previous = -1
    for cells in rows:
        if len(cells) != 4:
            errors.append(f'strategy.md: malformed sequence row: {"|".join(cells)}')
            continue
        release, highlight, plans, why = cells
        match = RELEASE_ROW.fullmatch(release)
        if not match or match.group(1) != match.group(3):
            errors.append(f'strategy.md: release needs a matching link to releases/<N>.md: {release}')
            continue
        number, state, file_number = match.groups()
        if int(number) <= previous:
            errors.append(f'strategy.md: release {number} must follow ascending order')
        previous = int(number)
        key = f'{file_number}.md'
        if key in referenced:
            errors.append(f'strategy.md: duplicate release {number}')
        referenced.add(key)
        if not highlight or not why:
            errors.append(f'strategy.md: release {number} needs Highlight and Why this order')
        plan_refs = STRATEGY_PLAN.findall(plans)
        if not plan_refs:
            errors.append(f'strategy.md: release {number} needs at least one linked plan')
        if release_docs is not None:
            body = release_docs.get(key)
            if body is None:
                errors.append(f'strategy.md: no release document {key}')
                continue
            actual_state = re.search(r'^\*\*State:\*\* (Draft|Final)$', body, re.M)
            if not actual_state or actual_state.group(1).lower() != state:
                errors.append(f'strategy.md: release {number} state differs from its document')
            if highlight != release_section(body, 'Highlight'):
                errors.append(f'strategy.md: release {number} highlight differs from its document')
            actual_plans = set(RELEASE_PLAN.findall(release_section(body, 'Included plans')))
            if set(plan_refs) != actual_plans or len(plan_refs) != len(actual_plans):
                errors.append(f'strategy.md: release {number} plan links differ from its document')
    if release_docs is not None:
        for missing in sorted(release_docs.keys() - referenced):
            errors.append(f'strategy.md: releases/{missing} has no roadmap row')
    return errors
