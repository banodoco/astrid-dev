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


def field_matches(text: str, pattern: str | Pattern[str], *, flags: int = re.M) -> list[re.Match[str]]:
    """Return all field matches so callers can retain their duplicate policy."""
    return _finditer(pattern, text, flags)


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


def priority_order(text: str | None) -> list[str]:
    return re.findall(r"^-\s+([^\s]+)\s*$", section(text or "", "Order"), re.M)


def projects(root: Path, revision: str | None = None) -> list[list[str]]:
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
        if fields["Status"] not in {"queued", "active", "blocked", "paused", "done", "cancelled"}:
            raise ValueError(f"plans/{folder}/plan.md: invalid status {fields['Status']!r}; use queued, active, blocked, paused, done or cancelled")
        row = [fields[f] for f in PROJECT_FIELDS]
        row.append(f"[Plan {folder.split('-')[0]}]({folder}/plan.md)")
        items.append((folder, row))
    items.sort(key=lambda item: (item[1][2] in {"done", "cancelled"}, ranks.get(item[0], len(order)), item[0]))
    return [row for _, row in items]
