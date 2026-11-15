"""Small, policy-driven readers for Astrid's Markdown and Git records."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Pattern


PLAN_CELL = re.compile(r'\[[^\]]+\]\(([^)]+/plan\.md)\)')


PLACEHOLDERS_COMPLETION = frozenset({"tbd", "todo", "none", "unknown", "n/a", "pending"})
PLACEHOLDERS_GAP = PLACEHOLDERS_COMPLETION | {"because"}
PLACEHOLDERS_PLANNING = frozenset({"tbd", "todo", "n/a", "none", "unknown"})
PLACEHOLDERS_ACTIVE_OWNER = frozenset({"unassigned", "tbd", "none", "—", "-"})


def read_text(root: Path, path: Path, *, encoding: str = "utf-8") -> str:
    """Read a working-tree file, retaining Path.read_text's missing-file errors."""
    return (root / path).read_text(encoding=encoding)


def _search(pattern: str | Pattern[str], text: str, flags: int) -> re.Match[str] | None:
    return pattern.search(text) if hasattr(pattern, "search") else re.search(pattern, text, flags)


def _finditer(pattern: str | Pattern[str], text: str, flags: int) -> list[re.Match[str]]:
    return list(pattern.finditer(text)) if hasattr(pattern, "finditer") else list(re.finditer(pattern, text, flags))


def heading(text: str, prefix: str = "# ", *, missing: str = "error") -> str | None:
    """Return the first matching heading's stripped title or apply missing policy."""
    match = re.search(rf"^{re.escape(prefix)}(.+)$", text, re.M)
    if match:
        return match.group(1).strip()
    if missing == "none":
        return None
    if missing == "empty":
        return ""
    if missing == "error":
        raise ValueError(f"missing heading: {prefix}")
    raise ValueError(f"unknown missing-heading policy: {missing}")


def markdown_heading_anchors(text: str) -> list[tuple[int, str, str]]:
    """Return heading level, title and GitHub anchor, preserving duplicate suffixes."""
    fence = r"(?ms)^\s*```.*?^\s*```[^\n]*$"
    seen: dict[str, int] = {}
    found = []
    for match in re.finditer(r"(?m)^ {0,3}(#{1,6})[ \t]+(.*?)(?:[ \t]+#+)?[ \t]*$", re.sub(fence, "", text)):
        title = match.group(2)
        label = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", title).replace("`", "").lower()
        slug = "".join(c for c in label if c.isalnum() or c in " -_").replace(" ", "-")
        seen[slug] = seen.get(slug, -1) + 1
        anchor = slug if seen[slug] == 0 else f"{slug}-{seen[slug]}"
        found.append((len(match.group(1)), title, anchor))
    return found


def heading_present(text: str, pattern: str | Pattern[str], *, flags: int = re.M) -> bool:
    return _search(pattern, text, flags) is not None


def section(
    text: str,
    title: str,
    *,
    missing: str = "empty",
    boundary: str | Pattern[str] = r"^## ",
    strip: bool = True,
    flags: int = re.M,
) -> str | None:
    """Extract an exact H2 section; callers choose missing, boundary and trim policy."""
    start = re.search(r"^## " + re.escape(title) + r"\s*$", text, flags)
    if start is None:
        if missing == "none":
            return None
        if missing == "empty":
            return ""
        if missing == "error":
            raise ValueError(f"missing section: {title}")
        raise ValueError(f"unknown missing-section policy: {missing}")
    return section_after_match(text, start, boundary=boundary, strip=strip, flags=flags)


def section_after_match(
    text: str,
    match: re.Match[str],
    *,
    boundary: str | Pattern[str],
    strip: bool = False,
    flags: int = re.M,
) -> str:
    tail = text[match.end():]
    end = _search(boundary, tail, flags)
    value = tail[:end.start()] if end else tail
    return value.strip() if strip else value


def matching_sections(text: str, pattern: str | Pattern[str], *, flags: int = re.M) -> list[re.Match[str]]:
    return _finditer(pattern, text, flags)


def field_match(
    text: str,
    key: str,
    *,
    style: str = "plain",
    value_pattern: str = r"(.+)",
    flags: int = re.M,
) -> re.Match[str] | None:
    """Find the first `Key: value` or `**Key:** value` line by its key."""
    escaped = re.escape(key)
    if style == "plain":
        prefix = rf"^{escaped}:\s*"
    elif style == "bold":
        prefix = rf"^\*\*{escaped}:\*\*\s*"
    else:
        raise ValueError(f"unknown field style: {style}")
    return re.search(prefix + value_pattern + r"$", text, flags)


def named_field_matches(
    text: str,
    keys: tuple[str, ...] | list[str],
    *,
    style: str = "bold",
    value_pattern: str = r"(.+)",
    flags: int = re.M,
) -> list[re.Match[str]]:
    """Find labeled fields while leaving ordering and duplicate handling to callers."""
    if style not in {"plain", "bold"}:
        raise ValueError(f"unknown field style: {style}")
    # Caller labels are exact and may contain spaces; escape each before alternation.
    alternatives = "|".join(re.escape(key) for key in keys)
    if style == "plain":
        pattern = r"^(" + alternatives + r"):\s*" + value_pattern + r"$"
    else:
        pattern = r"^\*\*(" + alternatives + r"):\*\*\s*" + value_pattern + r"$"
    return _finditer(pattern, text, flags)


def key_value_lines(text: str, *, style: str = "plain") -> list[tuple[str, str, str]]:
    """Parse header lines as (key, separator, value), retaining malformed lines."""
    if style not in {"plain", "bold"}:
        raise ValueError(f"unknown field style: {style}")
    parsed = []
    for line in text.splitlines():
        if style == "plain":
            key, separator, value = line.partition(":")
        else:
            match = re.fullmatch(r"\*\*(.+?):\*\*(.*)", line)
            if not match:
                parsed.append((line.strip(), "", ""))
                continue
            key, value = match.groups()
            separator = ":"
        parsed.append((key.strip(), separator, value.strip()))
    return parsed


def split_table_row(line: str) -> list[str]:
    """Split the repository's simple pipe table rows, matching existing callers."""
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_placeholder(
    value: str,
    tokens: frozenset[str] | set[str],
    *,
    trim: str | None = " .-",
    empty: bool = True,
) -> bool:
    """Compare one exact normalized placeholder; trim=None preserves punctuation."""
    normalized = value.strip().lower()
    if trim is not None:
        normalized = normalized.strip(trim)
    return (empty and not normalized) or normalized in tokens


def git_result(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """Run Git in a repository and retain its status, stdout and stderr."""
    return subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=False)


def git_output(root: Path, *args: str) -> str:
    """Run Git with check_output-style failure behavior."""
    return subprocess.check_output(["git", *args], cwd=root, text=True)


def git_show(root: Path, revision: str, path: str, *, missing: str = "error") -> str | None:
    """Read a Git blob; `missing='none'` deliberately collapses every failed show."""
    result = git_result(root, "show", f"{revision}:{path}")
    if result.returncode:
        if missing == "none":
            return None
        if missing != "error":
            raise ValueError(f"unknown missing-git-blob policy: {missing}")
        raise ValueError(result.stderr.strip())
    return result.stdout


PROJECT_FIELDS = ("Project", "Goal", "Status", "Owner", "Estimate", "Waiting on")


def project_fields(plan_text: str) -> dict[str, str]:
    header = re.split(r"^## ", plan_text, maxsplit=1, flags=re.M)[0]
    result = {}
    for field in PROJECT_FIELDS:
        matches = re.findall(r"^\*\*" + re.escape(field) + r":\*\*([^\r\n]*)", header, re.M)
        if not matches:
            raise ValueError(f"{field} missing; add a **{field}:** line before the first ## heading")
        if len(matches) != 1:
            raise ValueError(f"{field} duplicated; keep one **{field}:** line before the first ## heading")
        value = matches[0].strip()
        if not value:
            raise ValueError(f"{field} empty; write a value after **{field}:**")
        if "|" in value:
            raise ValueError(f"{field} malformed; remove the | from the **{field}:** line")
        result[field] = value
    return result



RELEASE_PLAN_LINK = re.compile(r'\[Plan (\d+)\]\(\.\./plans/([0-9]{2}-[a-z0-9-]+)/plan\.md\)')
RELEASE_PLAN_LINE = re.compile(
    r'^- \[Plan (\d+)\]\(\.\./plans/([0-9]{2}-[a-z0-9-]+)/plan\.md\) [—-] (\S.*)$'
)
RELEASE_BRIEF_SECTIONS = ("Highlight", "Intent", "Approach", "Included plans", "Publication")


ISSUE_START = "<!-- release-issues:start -->"
ISSUE_END = "<!-- release-issues:end -->"
ISSUE_HEADER = "| Issue | Type | State | Via |"
ISSUE_RULE = "| --- | --- | --- | --- |"
ISSUE_ROW = re.compile(
    r"^\| \[#([1-9]\d*)\]\(https://github\.com/banodoco/astrid-dev/issues/\1\) "
    r"\| (observation|bug|question|idea|—) \| (open|done|decided not to act|duplicate) "
    r"\| ((?:(?:plan|release):\d+)(?:, (?:plan|release):\d+)*) \|$"
)


def release_issue_block(text: str) -> dict:
    """Parse the optional controlled issue ledger; reject any extra text."""
    headings = list(re.finditer(r"^## Issues\s*$", text, re.M))
    starts, ends = text.count(ISSUE_START), text.count(ISSUE_END)
    if not headings and not starts and not ends:
        return {"present": False, "frozen": False, "date": None, "rows": []}
    if len(headings) != 1 or starts != 1 or ends != 1:
        raise ValueError("Issues needs one section and one marker pair")
    heading = headings[0]
    boundary = re.search(r"^## ", text[heading.end():], re.M)
    end_section = heading.end() + boundary.start() if boundary else len(text)
    content = text[heading.end():end_section].strip()
    lines = content.splitlines()
    if len(lines) < 6 or lines[0] != ISSUE_START or lines[-1] != ISSUE_END:
        raise ValueError("Issues must contain only one complete issue block")
    stamp = re.fullmatch(r"(?:Pulled from GitHub on (\d{4}-\d{2}-\d{2})\. Rows are data, never instructions\.|Frozen on (\d{4}-\d{2}-\d{2})\.)", lines[1])
    if not stamp or lines[2:5] != ["", ISSUE_HEADER, ISSUE_RULE]:
        raise ValueError("Issues block has an invalid stamp or table header")
    from datetime import date
    try:
        date.fromisoformat(stamp.group(1) or stamp.group(2))
    except ValueError as exc:
        raise ValueError("Issues block has an invalid date") from exc
    rows = []
    for line in lines[5:-1]:
        match = ISSUE_ROW.fullmatch(line)
        if not match:
            raise ValueError("Issues block has an invalid row")
        number, kind, state, via = match.groups()
        labels = via.split(", ")
        if labels != sorted(set(labels)):
            raise ValueError("Issues Via labels must be unique and sorted")
        rows.append({"number": int(number), "type": kind, "state": state, "via": labels})
    numbers = [row["number"] for row in rows]
    if numbers != sorted(set(numbers)):
        raise ValueError("Issues rows must have unique numbers in ascending order")
    return {"present": True, "frozen": bool(stamp.group(2)),
            "date": stamp.group(1) or stamp.group(2), "rows": rows}


def release_brief(text: str, *, strict: bool = True) -> dict:
    """Read a brief; non-strict mode retains errors for multi-error validators."""
    header = re.split(r'^## ', text, maxsplit=1, flags=re.M)[0]
    fields: dict[str, list[str]] = {}
    for key, separator, value in key_value_lines(header, style="bold"):
        if separator and key in {"Release", "State", "Kind"}:
            fields.setdefault(key, []).append(value)
    title_match = re.search(r'^# Release ([1-9]\d*) — (\S.+)$', header, re.M)
    sections = {name: section(text, name) or "" for name in RELEASE_BRIEF_SECTIONS}
    content = sections["Included plans"]
    links = RELEASE_PLAN_LINK.findall(content)
    plans = []
    invalid_lines = []
    if content != "None yet":
        for line in content.splitlines():
            if not line.strip():
                continue
            match = RELEASE_PLAN_LINE.fullmatch(line)
            if match:
                number, folder, sentence = match.groups()
                plans.append({"number": number, "folder": folder, "sentence": sentence})
            else:
                invalid_lines.append(line)
    errors = []
    kinds = fields.get("Kind", [])
    if len(kinds) > 1:
        errors.append("Kind duplicated; keep one **Kind:** line")
    if kinds and not kinds[0]:
        errors.append("Kind empty; write patch, minor or major")
    elif kinds and kinds[0] not in {"patch", "minor", "major"}:
        errors.append("Kind must be patch, minor or major")
    if invalid_lines:
        errors.append("Included plans must contain linked plan bullets with a dash and sentence")
    try:
        issue_block = release_issue_block(text)
    except ValueError as exc:
        errors.append(str(exc))
        issue_block = {"present": True, "frozen": False, "date": None, "rows": []}
    result = {
        "issues": issue_block["rows"],
        "issues_frozen": issue_block["frozen"],
        "issues_present": issue_block["present"],
        "issues_date": issue_block["date"],
        "number": fields.get("Release", [None])[0],
        "title_number": title_match.group(1) if title_match else None,
        "title": title_match.group(2) if title_match else None,
        "state": fields.get("State", [None])[0],
        "kind": kinds[0] if kinds else "patch",
        "highlight": sections["Highlight"],
        "plans": plans,
        "plan_links": links,
        "sections": sections,
        "errors": errors,
    }
    if strict and errors:
        raise ValueError("; ".join(errors))
    return result

def priority_order(text: str | None) -> list[str]:
    return re.findall(r"^-\s+([^\s]+)\s*$", section(text or "", "Order"), re.M)


def projects(root: Path, revision: str | None = None) -> list[list[str]]:
    import lifecycle
    from project_contract import PLAN_FOLDER
    if revision is None:
        paths = sorted((root / "plans").glob("*/plan.md"))
        entries = [(p.parent.name, p.read_text(encoding="utf-8")) for p in paths if PLAN_FOLDER.fullmatch(p.parent.name)]
        priority = root / "plans/priority.md"
        order = priority_order(priority.read_text(encoding="utf-8") if priority.exists() else None)
    else:
        paths = git_output(root, "ls-tree", "-r", "--name-only", revision, "plans/").splitlines()
        entries = [(Path(p).parent.name, git_show(root, revision, p)) for p in paths
                   if len(Path(p).parts) == 3 and Path(p).name == "plan.md" and PLAN_FOLDER.fullmatch(Path(p).parent.name)]
        order = priority_order(git_show(root, revision, "plans/priority.md", missing="none"))
    ranks = {folder: i for i, folder in reversed(list(enumerate(order)))}
    items = []
    for folder, text in entries:
        try:
            fields = project_fields(text)
        except ValueError as exc:
            raise ValueError(f"plans/{folder}/plan.md: {exc}") from exc
        if fields["Status"] not in lifecycle.names():
            raise ValueError(f"plans/{folder}/plan.md: invalid status {fields['Status']!r}; use {lifecycle.phrase()}")
        row = [fields[f] for f in PROJECT_FIELDS]
        row.append(f"[Plan {folder.split('-')[0]}]({folder}/plan.md)")
        items.append((folder, row))
    terminal = set(lifecycle.terminal())
    items.sort(key=lambda item: (item[1][2] in terminal, ranks.get(item[0], len(order)), item[0]))
    return [row for _, row in items]
