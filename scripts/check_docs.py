"""Validate Astrid Dev's documentation index and local links (stdlib only)."""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

from gap_relationships import parse_gap_relationships
import lifecycle
from project_contract import PLAN_FOLDER, plan_gap_ids
from project_delivery import GAP_FILE as GAP_NAME
from records import (PLACEHOLDERS_ACTIVE_OWNER, heading_present,
                     is_placeholder, key_value_lines, read_text, release_brief, release_branch_errors, release_fix_issue_errors, BRANCH_FIRST_RELEASE, section as record_section)
from vision_subject import parse_subject

ROOT = Path(__file__).resolve().parents[1]
CATALOG = Path('plans/index.md')
README = Path('README.md')
LINK = re.compile(r'(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)')


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
STRATEGY_SECTIONS = ('## Focus now', '## Versions', '## Not now', '## Decisions')
VERSION_HEADING = re.compile(r'^(#{3,4}) Version (\d+)\.(\d+)\s*$', re.M)
# Not records.named_field_matches: its `\s*` after the label can cross a newline, so an empty
# `**Aim:**` would capture the next line as its value.
VERSION_FIELD = re.compile(r'^\*\*(Aim):\*\*[ \t]*(.*)$', re.M)
VERSION_OPEN = 'Open'


def release_errors(filename: str, body: str) -> list[str]:
    """A release brief is valid as a draft, without publication pins."""
    issues = []
    stem = Path(filename).stem
    brief = release_brief(body, strict=False)
    if not stem.isdigit() or not re.fullmatch(r'[1-9]\d*', brief['number'] or '') or brief['number'] != stem:
        issues.append(f'releases/{filename}: Release must equal the numeric filename')
    if brief['title_number'] != stem:
        issues.append(f'releases/{filename}: title must be # Release {stem} — <title>')
    state = brief['state'] if brief['state'] in ('Draft', 'Final') else None
    if not state:
        issues.append(f'releases/{filename}: State must be Draft or Final')
    sections = brief['sections']
    for name, content in sections.items():
        if not content:
            issues.append(f'releases/{filename}: missing or empty ## {name}')
    highlight = sections['Highlight'].splitlines()
    if highlight and (len(highlight) != 1 or len(highlight[0]) < 15):
        issues.append(f'releases/{filename}: Highlight must be one substantive sentence on one line')
    plans = brief['plan_links']
    none_yet = sections['Included plans'] == 'None yet' and state == 'Draft'
    if not plans and not none_yet:
        issues.append(f'releases/{filename}: Included plans must link project plan.md files')
    if len({folder for _, folder in plans}) != len(plans):
        issues.append(f'releases/{filename}: duplicated included plan')
    if any(number != folder[:2] for number, folder in plans):
        issues.append(f'releases/{filename}: included plan number does not match its link')
    for error in brief['errors']:
        # Preserve the existing no-links diagnostic without adding a duplicate.
        if error.startswith('Included plans') and not plans:
            continue
        issues.append(f'releases/{filename}: {error}')
    if stem.isdigit() and int(stem) >= BRANCH_FIRST_RELEASE:
        issues.extend(f'releases/{filename}: {e}' for e in release_branch_errors(
            body, stem, [number for number, _ in plans]))
        issues.extend(f'releases/{filename}: {e}' for e in release_fix_issue_errors(body, stem))
    if state == 'Final' and brief['issues_present'] and not brief['issues_frozen']:
        issues.append(f'releases/{filename}: Final Issues block must be frozen')
    if state:
        if state == 'Draft':
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
    """Validate authored structure and release kinds, excluding generated regions."""
    errors = []
    for version in [*(f'0.{n}' for n in range(1, 10)), '1.0']:
        start, end = f'<!-- strategy-{version}:start -->', f'<!-- strategy-{version}:end -->'
        if text.count(start) != 1 or text.count(end) != 1 or text.find(start) > text.find(end):
            errors.append(f'strategy.md: needs exactly one ordered {start} and {end} pair')
        else:
            text = text[:text.index(start)] + text[text.index(end) + len(end):]
    errors.extend(f'strategy.md: missing section {name}' for name in STRATEGY_SECTIONS
                  if not heading_present(text, rf'^{re.escape(name)}\s*$'))
    if not re.search(r'^\*\*Last reviewed:\*\* \d{4}-\d{2}-\d{2}', text, re.M):
        errors.append('strategy.md: needs a "**Last reviewed:** YYYY-MM-DD" line')
    if release_docs is not None:
        ordered = sorted(((int(Path(name).stem), release_brief(body, strict=False))
                          for name, body in release_docs.items() if Path(name).stem.isdigit()))
        if sum(brief['kind'] == 'minor' for _, brief in ordered) > 9:
            errors.append('strategy.md: release briefs declare more than nine minor releases')
        if any(brief['kind'] == 'major' and i != len(ordered) - 1
               for i, (_, brief) in enumerate(ordered)):
            errors.append('strategy.md: a major release brief must be last')
    return errors + version_errors(text)


def version_errors(text: str) -> list[str]:
    """Validate one major aim and its nine ordered minor aims or Open values."""
    body = record_section(text, 'Versions', missing='none', boundary=r'^## ', strip=False)
    if body is None:
        return []
    errors = []
    heads = list(VERSION_HEADING.finditer(body))
    blocks = []
    for index, match in enumerate(heads):
        end = heads[index + 1].start() if index + 1 < len(heads) else len(body)
        fields: dict[str, str] = {}
        for name, value in VERSION_FIELD.findall(body[match.end():end]):
            if name in fields:
                errors.append(f"strategy.md: version {match.group(2)}.{match.group(3)}: duplicate field '{name}'")
            fields[name] = value.strip()
        blocks.append((len(match.group(1)), int(match.group(2)), int(match.group(3)), fields))
    majors = [(major, minor) for level, major, minor, _ in blocks if level == 3]
    if not majors:
        return ['strategy.md: Versions needs at least one major version heading (### Version N.0)']
    if len(majors) > 1:
        errors.append('strategy.md: Versions must contain exactly one major version heading')
    current = None
    expected_minor = 1
    for level, major, minor, fields in blocks:
        name = f'{major}.{minor}'
        aim = fields.get('Aim', '')
        if not aim:
            errors.append(f'strategy.md: version {name} needs an "**Aim:**" sentence')
        if level == 3:
            if minor != 0 or major < 1:
                errors.append(f'strategy.md: major version heading must be N.0: {name}')
            if current is not None:
                if expected_minor != 10:
                    errors.append(f'strategy.md: version {current}.0 must contain versions '
                                  f'{current - 1}.1 to {current - 1}.9 in order')
                if major != current + 1:
                    errors.append(f'strategy.md: major version {name} must follow {current}.0')
            if aim == VERSION_OPEN:
                errors.append(f'strategy.md: major version {name} needs a real aim, not "{VERSION_OPEN}"')
            current, expected_minor = major, 1
            continue
        if current is None:
            errors.append(f'strategy.md: version {name} is outside a major version')
            continue
        if major != current - 1 or minor != expected_minor:
            errors.append(f'strategy.md: expected version {current - 1}.{expected_minor} here, found {name}')
        expected_minor = minor + 1
    if current is not None and expected_minor != 10:
        errors.append(f'strategy.md: version {current}.0 must contain versions '
                      f'{current - 1}.1 to {current - 1}.9 in order')
    return errors
