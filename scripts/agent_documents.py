"""Canonical Markdown-first agent document discovery and validation.

Only \`skill: true\` opts a source document into packaging. Directories describe
ownership, not its skill name; the stem supplies a stable astrid-dev-* name.
This source reader intentionally has no knowledge of legacy SKILL.md packages.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from document_structure import frontmatter, headings, section


_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
_SECTION_NAMES = {
    "role": ("Responsibility", "Authority", "Responsibilities", "Handoff"),
    "workstream": ("When to use", "Outcome", "Inputs", "Procedure", "Completion"),
}


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
        return "astrid-dev-" + self.path.stem if self.skill else None


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
        relative = path.relative_to(root / "agent")
    except ValueError as exc:
        raise ValueError("source must be under agent/") from exc
    if not relative.parts or ".." in relative.parts or path.suffix != ".md":
        raise ValueError("source must be a regular .md document under agent/")
    if not path.resolve().is_relative_to(root / "agent"):
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
    if flag == "true" and not _NAME.fullmatch(path.stem):
        raise ValueError("skill filename must be a lowercase kebab-case name")

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
        if not section(body, required):
            raise ValueError(f"section '## {required}' must contain actual instructions")
        cursor = pos + 1

    return AgentDocument(path, relative, title[2:].strip(), description,
                         body, kind, flag == "true")


def discover_documents(root: Path) -> tuple[AgentDocument, ...]:
    """Discover all Markdown sources with no manually maintained package list."""
    root = Path(root).resolve()
    agent_root = root / "agent"
    if not agent_root.exists():
        return ()
    if agent_root.is_symlink() or not agent_root.is_dir():
        raise ValueError("agent/ must be a real directory")
    documents: list[AgentDocument] = []
    names: dict[str, Path] = {}
    paths = sorted(agent_root.rglob("*.md"))
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
    for document in documents:
        if (document.kind == "workstream" and
                document.relative.parts[0] == "roles"):
            role = document.relative.parts[1]
            if not (agent_root / "roles" / f"{role}.md").is_file():
                raise ValueError(f"{document.relative}: role {role!r} has no definition")
    return tuple(documents)


def validate_documents(root: Path) -> list[str]:
    """One fail-closed validation entry for repository checks."""
    try:
        discover_documents(root)
    except (OSError, UnicodeError, ValueError) as exc:
        return [f"agent documents: {exc}"]
    return []
