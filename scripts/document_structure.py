"""Small reusable Markdown structure rules, independent of document purpose.

Callers own their section names, allowed fields, and any semantic rules.
The helpers enforce shape and order; they do not judge the quality of prose.
"""
from __future__ import annotations

import re


def _heading_spans(text: str, level: int) -> list[tuple[str, int, int]]:
    """Find real Markdown headings, not examples inside backtick/tilde fences."""
    if level < 1 or level > 6:
        raise ValueError("heading level must be 1..6")
    found: list[tuple[str, int, int]] = []
    fence: str | None = None
    fence_size = 0
    offset = 0
    for line in text.splitlines(keepends=True):
        plain = line.rstrip("\r\n")
        if fence is not None:
            if re.fullmatch(r"[ ]{0,3}" + re.escape(fence) + "{" + str(fence_size) + r",}[ \t]*", plain):
                fence, fence_size = None, 0
        else:
            opening = re.match(r"^[ ]{0,3}(" + re.escape(chr(96)) + r"{3,}|~{3,})", plain)
            if opening:
                marker = opening.group(1)
                fence, fence_size = marker[0], len(marker)
            else:
                match = re.fullmatch(re.escape("#" * level) + r" (.+)", plain)
                if match:
                    found.append((match.group(1).strip(), offset, offset + len(line)))
        offset += len(line)
    return found


def headings(text: str, level: int = 2) -> list[str]:
    """Return actual Markdown headings at one level, ignoring fenced examples."""
    return [title for title, _, _ in _heading_spans(text, level)]


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
    """Find exactly one real Markdown section, stopping at the next peer."""
    matches = _heading_spans(text, level)
    positions = [i for i, (title, _, _) in enumerate(matches) if title == name]
    if len(positions) != 1:
        raise ValueError(f"expected exactly one '{'#' * level} {name}' section")
    index = positions[0]
    start = matches[index][2]
    end = matches[index + 1][1] if index + 1 < len(matches) else len(text)
    return text[start:end].strip()


def ordered_bold_fields(block: str, required: tuple[str, ...]) -> dict[str, str]:
    """Require one substantive, single-line **Label:** value for each field, in order."""
    # The compact contract's first paragraph is its machine-readable interface.
    # Further prose may elaborate within the section without duplicating the fields.
    first, _, remainder = block.partition("\n\n")
    rows = [line.strip() for line in first.splitlines() if line.strip()]
    # Supporting prose is permitted, but not a second version of any contract
    # field after the first blank line. There is one canonical value per field.
    names = "|".join(re.escape(name) for name in required)
    duplicate = re.search(r"(?m)^\s*\*\*(" + names + r"):\*\*", remainder)
    if duplicate:
        raise ValueError(f"duplicate contract field {duplicate.group(1)!r} after the field block")
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
