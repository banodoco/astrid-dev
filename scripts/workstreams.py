"""One workstream contract for independently invocable skills and role-owned docs.

The procedure's substance remains in its body. Packaging changes discovery and
ownership, never the required outcome, inputs, execution or completion criteria.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Literal
import re

from document_structure import frontmatter, headings, ordered_bold_fields, section

# These are also the authorized generated-index targets in scripts/views.py.
PARENT_SKILLS = (
    "skills/roles/astrid-dev-lead/SKILL.md",
    "skills/roles/astrid-dev-manage/SKILL.md",
    "skills/roles/astrid-dev-orchestrate/SKILL.md",
)
ROLE_SKILLS = PARENT_SKILLS + ("skills/roles/astrid-dev-worker/SKILL.md",)
START = "<!-- workstreams:start -->"
END = "<!-- workstreams:end -->"
SHARED_START = "<!-- shared-workstreams:start -->"
SHARED_END = "<!-- shared-workstreams:end -->"
CONTRACT_HEADING = "Workstream contract"
CONTRACT_FIELDS = ("Outcome", "When to use", "Inputs", "Procedure", "Completion")


@dataclass(frozen=True)
class Workstream:
    """The common definition, irrespective of how an agent discovers it."""
    path: Path
    kind: Literal["skill", "document"]
    title: str
    description: str
    outcome: str
    when_to_use: str
    inputs: str
    procedure: str
    completion: str
    name: str | None = None


def workstream_files(root: Path) -> tuple[Path, ...]:
    """Find direct role-owned workstream docs, excluding nested guides."""
    return tuple(sorted(path for path in (root / "skills/roles").glob("astrid-dev-*/workstreams/*.md")
                        if path.name != "README.md"))


def shared_skill_files(root: Path) -> tuple[Path, ...]:
    """Find standalone workstreams (skill packages) without following aliases."""
    folder = root / "skills/shared/workstreams"
    return tuple(sorted(path / "SKILL.md" for path in folder.glob("astrid-dev-*")
                        if path.is_dir() and not path.is_symlink()))


def parse_workstream(path: Path) -> Workstream:
    """Parse the same structural contract from a SKILL.md or a role-specific .md.

    Name and parent rules are packaging-specific; the five contract fields are not.
    """
    if path.is_symlink() or not path.is_file():
        raise ValueError("workstream source must be a regular file, not a symlink")
    metadata, body = frontmatter(path.read_text(encoding="utf-8"))
    kind: Literal["skill", "document"] = "skill" if path.name == "SKILL.md" else "document"
    allowed = {"name", "description"} if kind == "skill" else {"description"}
    if set(metadata) != allowed:
        fields = ", ".join(sorted(allowed))
        raise ValueError(f"frontmatter must contain exactly {fields} as single-line fields")
    description = metadata["description"]
    if (not description or len(description) > 240 or description != description.strip()
            or not description.endswith((".", "!", "?"))
            or any(char in description for char in "[]<>|\t\r\n")):
        raise ValueError("description must be one plain-text sentence (max 240 characters) ending in punctuation")
    lines = [line for line in body.splitlines() if line.strip()]
    heading = lines[0] if lines else ""
    if not heading.startswith("# ") or not heading[2:].strip():
        raise ValueError("first body heading must be a nonempty '# <title>'")
    if kind == "document":
        hit = re.fullmatch(r"# Workstream: ([^\[\]]+)", heading)
        if not hit or not hit.group(1).strip():
            raise ValueError("first body heading must be '# Workstream: <title>'")
        title = hit.group(1).strip()
        title = title[0].upper() + title[1:]
    else:
        title = heading[2:].strip()
        if not re.fullmatch(r"astrid-dev-[a-z0-9]+(?:-[a-z0-9]+)*", metadata["name"]):
            raise ValueError("skill name must be an astrid-dev-* identifier")
        if metadata["name"] != path.parent.name:
            raise ValueError(f"skill name must match folder {path.parent.name!r}")
    if not headings(body, 2) or headings(body, 2)[0].strip() != CONTRACT_HEADING:
        raise ValueError("first ## section must be '## Workstream contract'")
    contract_block = section(body, CONTRACT_HEADING)
    contract = ordered_bold_fields(contract_block, CONTRACT_FIELDS)
    # A valid summary alone is not an executable workstream. Require a real
    # procedure below it: a later level-two section or an authored step/list.
    trailing = body.split("## Workstream contract", 1)[1]
    _, _, instructions = trailing.partition("\n\n")
    if not (headings(body, 2)[1:] or re.search(r"(?m)^(?:[0-9]+\. |[-*] )\S", instructions)):

        raise ValueError("workstream requires operational instructions beyond its five-field contract")
    return Workstream(
        path=path, kind=kind, name=metadata.get("name"), title=title,
        description=description, outcome=contract["Outcome"],
        when_to_use=contract["When to use"], inputs=contract["Inputs"],
        procedure=contract["Procedure"], completion=contract["Completion"],
    )


def metadata(path: Path) -> tuple[str, str]:
    """Compatibility wrapper for the generated, role-specific discovery index."""
    workstream = parse_workstream(path)
    return workstream.title, workstream.description


def _markers(text: str, parent: str, start: str = START, end: str = END) -> tuple[str, str]:
    if text.count(start) != 1 or text.count(end) != 1 or text.index(start) > text.index(end):
        raise ValueError(f"{parent}: expected exactly one ordered {start} and {end} pair")
    before, remainder = text.split(start, 1)
    _, after = remainder.split(end, 1)
    return before, after


def render_index(root: Path, parent: str) -> str:
    """Replace only a role's generated role-specific workstream region."""
    text = (root / parent).read_text(encoding="utf-8")
    before, after = _markers(text, parent)
    folder = (root / parent).parent / "workstreams"
    rows = []
    for path in sorted(folder.glob("*.md")):
        if path.name == "README.md":
            continue
        workstream = parse_workstream(path)
        rows.append(f"- [{workstream.title}](workstreams/{path.name}) — {workstream.description}")
    return before + START + "\n" + "\n".join(rows) + "\n" + END + after


def render_shared_index(root: Path, parent: str) -> str:
    """List shared workstreams by name only, without duplicating their descriptions."""
    text = (root / parent).read_text(encoding="utf-8")
    before, after = _markers(text, parent, SHARED_START, SHARED_END)
    rows = []
    for path in shared_skill_files(root):
        workstream = parse_workstream(path)
        rows.append(f"- [{workstream.name}](../../shared/workstreams/{workstream.name}/SKILL.md)")
    return before + SHARED_START + "\n" + "\n".join(rows) + "\n" + SHARED_END + after


def validate(root: Path) -> list[str]:
    """Validate both packages, the common contract, parent registration and views."""
    root = root.resolve()
    errors: list[str] = []
    parents = set(PARENT_SKILLS)
    titles: dict[str, set[str]] = {}
    for path in workstream_files(root):
        relative = path.relative_to(root).as_posix()
        parent = (path.parent.parent / "SKILL.md").relative_to(root).as_posix()
        if parent not in parents:
            errors.append(f"{relative}: unregistered parent {parent}; register its generated view and CI target first")
        try:
            item = parse_workstream(path)
            seen = titles.setdefault(parent, set())
            if item.title in seen:
                errors.append(f"{relative}: duplicate workstream title {item.title!r} under {parent}")
            seen.add(item.title)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"{relative}: {exc}")
    shared = root / "skills/shared/workstreams"
    if shared.exists():
        for folder in sorted(shared.iterdir()):
            if not folder.is_dir() or folder.is_symlink() or not folder.name.startswith("astrid-dev-"):
                errors.append(f"{folder.relative_to(root)}: shared workstream must be an astrid-dev-* directory")
                continue
            skill = folder / "SKILL.md"
            try:
                parse_workstream(skill)
            except (OSError, UnicodeError, ValueError) as exc:
                errors.append(f"{skill.relative_to(root)}: {exc}")
    # Preserve historical Markdown links without installing a second skill.
    # Only these relative directory symlinks are permitted at legacy locations.
    aliases = {f"skills/capabilities/astrid-dev-{name}": f"skills/shared/workstreams/astrid-dev-{name}"
               for name in ("bugfix", "gap", "gpu-validate", "green", "improve", "iterate", "merge", "release")}
    aliases["skills/roles/astrid-dev-plan"] = "skills/shared/workstreams/astrid-dev-plan"
    for legacy, canonical in sorted(aliases.items()):
        source = root / legacy
        if not source.exists() and not source.is_symlink():
            continue
        if not source.is_symlink() or source.resolve() != (root / canonical).resolve():
            errors.append(f"{legacy}: historical link must be a symlink to {canonical}, not another skill copy")
    for parent in ROLE_SKILLS:
        try:
            _markers((root / parent).read_text(encoding="utf-8"), parent, SHARED_START, SHARED_END)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"{parent}: {exc}")
    for parent in PARENT_SKILLS:
        try:
            _markers((root / parent).read_text(encoding="utf-8"), parent)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"{parent}: {exc}")
    return errors
