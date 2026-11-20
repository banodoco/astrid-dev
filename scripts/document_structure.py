"""Small reusable Markdown structure rules, independent of document purpose.

Callers own their section names, allowed fields, and any semantic rules.
The helpers enforce shape and order; they do not judge the quality of prose.
"""
from __future__ import annotations

import re


def headings(text: str, level: int = 2) -> list[str]:
    """Return exact Markdown headings at a chosen level, in source order."""
    if level < 1 or level > 6:
        raise ValueError("heading level must be 1..6")
    return re.findall(rf"^{'#' * level} (.+)$", text, re.M)


def ordered_heading_error(actual: list[str], required: list[str], *, level: int = 2) -> str | None:
    """Give the first missing or out-of-order required heading, allowing extras."""
    cursor = 0
    for item in required:
        try:
            cursor = actual.index(item, cursor) + 1
        except ValueError:
            if item in actual:
                return f"heading '{'#' * level} {item}' is out of order; move it to where the template puts it"
            return f"missing heading '{'#' * level} {item}'; add it where the template puts it"
    return None


def frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Parse the intentionally small, one-line YAML-frontmatter subset we author."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing frontmatter; the first line must be '---'")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration as exc:
        raise ValueError("unclosed frontmatter; add a closing '---'") from exc
    fields: dict[str, str] = {}
    for line in lines[1:end]:
        match = re.fullmatch(r"([a-z][a-z0-9_-]*):[ ]+([^\r\n]+)\r?\n?", line)
        if not match or not match.group(2).strip():
            raise ValueError("frontmatter fields must be nonempty single-line 'key: value' entries")
        key, value = match.group(1), match.group(2)
        if key in fields:
            raise ValueError(f"duplicate frontmatter field {key!r}")
        fields[key] = value
    return fields, "".join(lines[end + 1:])


def section(text: str, name: str, *, level: int = 2) -> str:
    """Find exactly one Markdown section and return the text up to the next peer."""
    marker = "#" * level
    matches = list(re.finditer(rf"^{re.escape(marker)} {re.escape(name)}[ \t]*$", text, re.M))
    if len(matches) != 1:
        raise ValueError(f"expected exactly one '{marker} {name}' section")
    match = matches[0]
    next_peer = re.search(rf"^{re.escape(marker)} (?!#)[^\n]+$", text[match.end():], re.M)
    end = match.end() + next_peer.start() if next_peer else len(text)
    return text[match.end():end].strip()


def ordered_bold_fields(block: str, required: tuple[str, ...]) -> dict[str, str]:
    """Require one substantive, single-line **Label:** value for each field, in order."""
    # The compact contract's first paragraph is its machine-readable interface.
    # Further prose may elaborate within the section without duplicating the fields.
    rows = [line.strip() for line in block.split("\n\n", 1)[0].splitlines() if line.strip()]
    actual: list[str] = []
    values: dict[str, str] = {}
    for line in rows:
        hit = re.fullmatch(r"\*\*([^*:\n]+):\*\* ([^\n]+)", line)
        if not hit:
            raise ValueError("contract must contain only single-line '**Field:** value' entries")
        key, value = hit.group(1), hit.group(2)
        if key in values:
            raise ValueError(f"duplicate contract field {key!r}")
        if len(value.strip()) < 12 or value != value.strip() or value in ("TBD", "TODO"):
            raise ValueError(f"contract field {key!r} needs substantive one-line content")
        actual.append(key)
        values[key] = value
    if actual != list(required):
        raise ValueError(f"contract fields must be {', '.join(required)}, in that order; found {', '.join(actual) or 'none'}")
    return values
