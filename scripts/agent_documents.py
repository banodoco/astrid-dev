"""Canonical Markdown-first agent document discovery and validation.

Only `skill: true` opts a source document into packaging. Directories describe
ownership, not its skill name; the stem supplies a stable astrid-dev-* name.
This source reader intentionally has no knowledge of legacy SKILL.md packages.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import os

from otto.markdown import frontmatter, headings, section


SKILL_PREFIX = "astrid-dev-"
SKILL_NAME_MAX_LENGTH = 64
AGENT_SOURCE_ROOT = "agent"

_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
_SECTION_NAMES = {
    "role": ("Responsibility", "Authority", "Responsibilities", "Handoff"),
    "workstream": ("When to use", "Outcome", "Inputs", "Procedure", "Completion"),
}


def routing_table_headers(text: str) -> tuple[int, ...]:
    """Locate real route-to-model-family tables, not role/mode tables or examples.

    Column names identify the contract; model-family values stay in the authored
    policy. Offsets let generated-view validation distinguish an owned copy from
    another authored table elsewhere in the same document.
    """
    found: list[int] = []
    previous: tuple[int, list[str]] | None = None
    fence: str | None = None
    fence_size = 0
    offset = 0
    family_columns = {"claude", "codex", "model", "models", "family", "model family", "model families"}
    for line in text.splitlines(keepends=True):
        start, offset = offset, offset + len(line)
        plain = line.rstrip("\r\n")
        if fence is not None:
            if re.fullmatch(r"[ ]{0,3}" + re.escape(fence) + "{" + str(fence_size) + r",}[ \t]*", plain):
                fence, fence_size = None, 0
            previous = None
            continue
        opening = re.match(r"^[ ]{0,3}(`{3,}|~{3,})", plain)
        if opening:
            marker = opening.group(1)
            fence, fence_size = marker[0], len(marker)
            previous = None
            continue
        if plain.startswith(("    ", "\t")) or "|" not in plain:
            previous = None
            continue
        cells = [cell.strip() for cell in re.split(r"(?<!\\)\|", plain.strip().strip("|"))]
        if (previous is not None and len(cells) == len(previous[1])
                and all(re.fullmatch(r":?-+:?", cell) for cell in cells)):
            columns = {re.sub(r"[`*_]", "", cell).strip().casefold() for cell in previous[1]}
            if "route" in columns and columns.intersection(family_columns):
                found.append(previous[0])
        previous = (start, cells)
    return tuple(found)


@dataclass(frozen=True)
class AgentDocument:
    path: Path
    relative: Path
    title: str
    description: str
    body: str
    kind: str
    skill: bool

    @property
    def skill_name(self) -> str | None:
        return SKILL_PREFIX + self.path.stem if self.skill else None


def _kind(relative: Path) -> str:
    parts = relative.parts
    if len(parts) == 2 and parts[0] == "roles":
        return "role"
    if ((len(parts) == 3 and parts[0] == "roles")
            or (len(parts) == 3 and parts[:2] == ("shared", "workstreams"))):
        return "workstream"
    return "reference"


def parse_document(root: Path, path: Path) -> AgentDocument:
    """Parse one authored document; reject symlinks and unsupported metadata."""
    root = Path(root).resolve()
    path = Path(path)
    if not path.is_absolute():
        path = root / path
    if path.is_symlink() or not path.is_file():
        raise ValueError("source must be a regular Markdown file, not a symlink")
    # Resolve the source as well as root: /var and /private/var alias on macOS.
    path = path.resolve()
    try:
        relative = path.relative_to(root / AGENT_SOURCE_ROOT)
    except ValueError as exc:
        raise ValueError("source must be under agent/") from exc
    if not relative.parts or ".." in relative.parts or path.suffix != ".md":
        raise ValueError("source must be a regular .md document under agent/")
    if not path.resolve().is_relative_to(root / AGENT_SOURCE_ROOT):
        raise ValueError("source resolves outside agent/")

    metadata, body = frontmatter(path.read_text(encoding="utf-8"))
    if set(metadata) - {"description", "skill"}:
        raise ValueError("only description and optional skill metadata are supported")
    description = metadata.get("description", "")
    if (not description or len(description) > 240
            or description != description.strip()
            or not description.endswith((".", "!", "?"))
            or any(char in description for char in "[]<>|\t\r\n")):
        raise ValueError("description must be one plain-text sentence of at most 240 characters")
    flag = metadata.get("skill", "false")
    if flag not in ("true", "false"):
        raise ValueError("skill must be the literal boolean true or false")
    if flag == "true" and any(part in (".", "..") or any(c in part for c in "\\\r\n")
                              for part in relative.parts[:-1]):
        raise ValueError("skill source directory cannot be represented by an ownership marker")
    if flag == "true" and not _NAME.fullmatch(path.stem):
        raise ValueError("skill filename must be a lowercase kebab-case name")
    if flag == "true":
        skill_name = SKILL_PREFIX + path.stem
        if len(skill_name) > SKILL_NAME_MAX_LENGTH:
            raise ValueError(
                f"{(Path(AGENT_SOURCE_ROOT) / relative).as_posix()}: generated skill name "
                f"'{skill_name}' is {len(skill_name)} characters; limit is {SKILL_NAME_MAX_LENGTH}"
            )

    lines = [line for line in body.splitlines() if line.strip()]
    title = lines[0] if lines else ""
    if not title.startswith("# ") or not title[2:].strip():
        raise ValueError("document must start with a nonempty # title")
    kind = _kind(relative)
    actual = headings(body, 2)
    cursor = 0
    for required in _SECTION_NAMES.get(kind, ()):
        try:
            pos = actual.index(required, cursor)
        except ValueError as exc:
            raise ValueError(f"missing or out-of-order section '## {required}'") from exc
        instructions = section(body, required)
        if not instructions:
            raise ValueError(f"section '## {required}' must contain actual instructions")
        if kind == "workstream" and (len(instructions) < 12 or instructions in ("TBD", "TODO")):
            raise ValueError(f"section '## {required}' needs substantive instructions (at least 12 characters)")
        cursor = pos + 1

    return AgentDocument(path, relative, title[2:].strip(), description,
                         body, kind, flag == "true")


def discover_documents(root: Path) -> tuple[AgentDocument, ...]:
    """Discover all Markdown sources with no manually maintained package list."""
    root = Path(root).resolve()
    agent_root = root / AGENT_SOURCE_ROOT
    # A dangling directory symlink has exists() == False; refuse it before
    # treating an absent agent source tree as an empty, removable package set.
    if agent_root.is_symlink():
        raise ValueError("agent/ must be a real directory")
    if not agent_root.exists():
        return ()
    if not agent_root.is_dir():
        raise ValueError("agent/ must be a real directory")
    documents: list[AgentDocument] = []
    names: dict[str, Path] = {}
    # Refuse incomplete inventories before deriving stale package names.
    def traversal_error(error: OSError) -> None:
        raise error

    paths: list[Path] = []
    for directory, dirs, files in os.walk(agent_root, followlinks=False, onerror=traversal_error):
        for name in dirs + files:
            entry = Path(directory) / name
            if entry.is_symlink() and (name in dirs or not entry.exists()):
                raise ValueError(f"source tree contains a directory or dangling symlink: {entry}")
        paths.extend(Path(directory) / name for name in files if name.endswith(".md"))
    paths.sort()
    for path in paths:
        document = parse_document(root, path)
        name = document.skill_name
        if name is not None:
            if name in names:
                raise ValueError(
                    f"duplicate skill name {name}: {names[name]} and {document.relative}"
                )
            names[name] = document.relative
        documents.append(document)
    titles: dict[str, set[str]] = {}
    for document in documents:
        if (document.kind == "workstream" and
                document.relative.parts[0] == "roles"):
            role = document.relative.parts[1]
            if not (agent_root / "roles" / f"{role}.md").is_file():
                raise ValueError(f"{document.relative}: role {role!r} has no definition")
            title = document.title[0].upper() + document.title[1:]
            seen = titles.setdefault(role, set())
            if title in seen:
                raise ValueError(f"{document.relative}: duplicate workstream title {title!r} under roles/{role}.md")
            seen.add(title)
    return tuple(documents)


def validate_documents(root: Path) -> list[str]:
    """One fail-closed validation entry for repository checks."""
    try:
        discover_documents(root)
    except (OSError, UnicodeError, ValueError) as exc:
        return [f"agent documents: {exc}"]
    return []
