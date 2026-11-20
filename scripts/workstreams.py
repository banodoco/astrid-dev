"""Canonical workstream descriptions and parent-skill discovery views.

Each direct workstreams/*.md file owns its one-line description and H1 title.
Only registered parent SKILL.md files may receive generated content.
"""
from pathlib import Path
import re

# Also the target allowlist for generated workstream views in scripts/views.py.
PARENT_SKILLS = (
    "skills/roles/astrid-dev-lead/SKILL.md",
    "skills/roles/astrid-dev-manage/SKILL.md",
    "skills/roles/astrid-dev-orchestrate/SKILL.md",
)
ROLE_SKILLS = PARENT_SKILLS + ("skills/roles/astrid-dev-worker/SKILL.md",)
START = "<!-- workstreams:start -->"
SHARED_START = "<!-- shared-workstreams:start -->"
SHARED_END = "<!-- shared-workstreams:end -->"
END = "<!-- workstreams:end -->"
TITLE = re.compile(r"^# Workstream: (.+)$")


def workstream_files(root: Path) -> tuple[Path, ...]:
    """Find direct workstream documents, not nested setup guides."""
    return tuple(sorted(path for path in (root / "skills").glob("**/workstreams/*.md")
                        if path.name != "README.md"))


def metadata(path: Path) -> tuple[str, str]:
    """Read the existing workstream title and its single-line discovery description."""
    if path.is_symlink():
        raise ValueError("workstream source must not be a symlink")
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("missing frontmatter; add a first-line '---', one 'description: ...' line and a closing '---'")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("unclosed frontmatter; add a closing '---'") from exc
    fields = lines[1:end]
    if len(fields) != 1 or not fields[0].startswith("description: "):
        raise ValueError("frontmatter must contain exactly one single-line 'description: ...' field")
    description = fields[0][len("description: "):]
    if (not description.strip() or description != description.strip()
            or len(description) > 240 or not description.endswith((".", "!", "?"))
            or any(char in description for char in "[]<>|\t\r\n")):
        raise ValueError("description must be one plain-text sentence (max 240 characters) ending in punctuation")
    heading = next((line for line in lines[end + 1:] if line.strip()), "")
    match = TITLE.fullmatch(heading)
    if not match or not match.group(1).strip() or any(char in match.group(1) for char in "[]"):
        raise ValueError("first body heading must be '# Workstream: <title>'")
    title = match.group(1).strip()
    return title[0].upper() + title[1:], description


def _markers(text: str, parent: str, start: str = START, end: str = END) -> tuple[str, str]:
    if text.count(start) != 1 or text.count(end) != 1 or text.index(start) > text.index(end):
        raise ValueError(f"{parent}: expected exactly one ordered {start} and {end} pair")
    before, remainder = text.split(start, 1)
    _, after = remainder.split(end, 1)
    return before, after


def render_index(root: Path, parent: str) -> str:
    """Replace only the parent skill's generated workstream region."""
    text = (root / parent).read_text(encoding="utf-8")
    before, after = _markers(text, parent)
    folder = (root / parent).parent / "workstreams"
    lines = []
    for path in sorted(folder.glob("*.md")):
        if path.name == "README.md":
            continue
        title, description = metadata(path)
        lines.append(f"- [{title}](workstreams/{path.name}) — {description}")
    return before + START + "\n" + "\n".join(lines) + "\n" + END + after


def render_shared_index(root: Path, parent: str) -> str:
    """List the names of independently invocable workstream skills under a role."""
    text = (root / parent).read_text(encoding="utf-8")
    before, after = _markers(text, parent, SHARED_START, SHARED_END)
    rows = []
    for folder in sorted((root / "skills/shared/workstreams").glob("astrid-dev-*")):
        if folder.is_symlink() or not folder.is_dir():
            continue
        # These identifiers are checked by validate and by the installer.
        rows.append(f"- [{folder.name}](../../shared/workstreams/{folder.name}/SKILL.md)")
    return before + SHARED_START + "\n" + "\n".join(rows) + "\n" + SHARED_END + after


def validate(root: Path) -> list[str]:
    """Always-on CI check, including source-only edits and newly added files."""
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
            title, _ = metadata(path)
            seen = titles.setdefault(parent, set())
            if title in seen:
                errors.append(f"{relative}: duplicate workstream title {title!r} under {parent}")
            seen.add(title)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"{relative}: {exc}")
    # Standalone shared workstreams are skills, not generated parent-index entries.
    shared = root / "skills/shared/workstreams"
    if shared.exists():
        for folder in sorted(shared.iterdir()):
            if not folder.is_dir() or folder.is_symlink() or not folder.name.startswith("astrid-dev-"):
                errors.append(f"{folder.relative_to(root)}: shared workstream must be an astrid-dev-* directory")
                continue
            skill = folder / "SKILL.md"
            if skill.is_symlink() or not skill.is_file():
                errors.append(f"{folder.relative_to(root)}: missing regular SKILL.md")
                continue
            lines = skill.read_text(encoding="utf-8").splitlines()
            if len(lines) < 4 or lines[0] != "---" or "---" not in lines[1:]:
                errors.append(f"{skill.relative_to(root)}: missing YAML frontmatter")
                continue
            end = lines.index("---", 1)
            meta = lines[1:end]
            if meta.count(f"name: {folder.name}") != 1 or len([line for line in meta if line.startswith("name:")]) != 1:
                errors.append(f"{skill.relative_to(root)}: name must match folder {folder.name!r}")
            descriptions = [line.removeprefix("description: ") for line in meta if line.startswith("description: ")]
            if len(descriptions) != 1 or not descriptions[0].strip() or descriptions[0] != descriptions[0].strip():
                errors.append(f"{skill.relative_to(root)}: exactly one nonempty single-line description required")
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
