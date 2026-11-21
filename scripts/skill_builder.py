"""Generate standards-compatible skill packages from canonical Markdown sources."""
from __future__ import annotations

from pathlib import Path
import json
import os
import re
import shutil
from urllib.parse import unquote

from agent_documents import AgentDocument, discover_documents
from records import markdown_heading_anchors

OUTPUT = Path(".generated/skills")
MARKER = ".astrid-dev-generated"
REPO_LINK = "../../../"
_LINK = re.compile(r"(!?\[[^\]\n]+\])\(([^)\n]+)\)")
_SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*:", re.I)


def _rewrite_links(source: AgentDocument, root: Path) -> str:
    """Local Markdown links resolve through the generated package's repo link."""
    fence: str | None = None
    size = 0
    lines = []
    for line in source.body.splitlines(keepends=True):
        trimmed = line.strip()
        if fence:
            if re.fullmatch(re.escape(fence) + "{" + str(size) + r",}[ \t]*", trimmed):
                fence, size = None, 0
            lines.append(line)
            continue
        fence_pattern = r"^(" + re.escape(chr(96)) + r"{3,}|~{3,})"
        start = re.match(fence_pattern, trimmed)
        if start:
            fence, size = start.group(1)[0], len(start.group(1))
            lines.append(line)
            continue

        def replace(match: re.Match[str]) -> str:
            label, raw = match.groups()
            quoted = re.match(r'^(\S+)(\s+"[^"\n]*")?$', raw)
            if quoted is None:
                raise ValueError(f"{source.relative}: unsupported Markdown link {raw!r}")
            address, suffix = quoted.group(1), quoted.group(2) or ""
            if not address:
                return match.group(0)
            if address.startswith("#"):
                # A fragment-only link targets this source's unchanged Markdown body.
                fragment = unquote(address[1:])
                if fragment and fragment not in {
                    anchor for _, _, anchor in markdown_heading_anchors(source.body)
                }:
                    raise ValueError(f"{source.relative}: missing heading in {address}")
                return match.group(0)
            if address.startswith(("/", "//")) or _SCHEME.match(address):
                return match.group(0)
            pathpart, sep, anchor = address.partition("#")
            pathpart, _, query = pathpart.partition("?")
            target = (source.path.parent / unquote(pathpart)).resolve()
            if not target.is_relative_to(root):
                raise ValueError(f"{source.relative}: link escapes checkout: {address}")
            if not target.exists():
                raise ValueError(f"{source.relative}: missing link target: {address}")
            if anchor and target.is_file() and target.suffix.lower() == ".md":
                anchors = {a for _, _, a in markdown_heading_anchors(
                    target.read_text(encoding="utf-8"))}
                if anchor not in anchors:
                    raise ValueError(f"{source.relative}: missing heading in {address}")
            output = "repo/" + target.relative_to(root).as_posix()
            if query:
                output += "?" + query
            if sep:
                output += "#" + anchor
            return label + "(" + output + suffix + ")"

        lines.append(_LINK.sub(replace, line))
    return "".join(lines)


def render_skill(doc: AgentDocument, root: Path) -> str:
    if not doc.skill or doc.skill_name is None:
        raise ValueError(f"{doc.relative}: not opted in as a skill")
    content = _rewrite_links(doc, Path(root).resolve())
    return ("---\n"
            f"name: {doc.skill_name}\n"
            f"description: {json.dumps(doc.description, ensure_ascii=False)}\n"
            "---\n\n" + content.lstrip("\n").rstrip("\n") + "\n")


def expected_packages(root: Path) -> dict[str, tuple[str, str]]:
    root = Path(root).resolve()
    result = {}
    for doc in discover_documents(root):
        if doc.skill:
            result[doc.skill_name] = (
                render_skill(doc, root),
                (Path("agent") / doc.relative).as_posix() + "\n",
            )
    return dict(sorted(result.items()))


def _output_root(root: Path) -> Path:
    root = Path(root).resolve()
    path = root / OUTPUT
    for item in (root / ".generated", path):
        if item.is_symlink():
            raise ValueError(f"{item}: generated output path cannot be a symlink")
    return path


def _assert_package_dir(package: Path, *, stale: bool = False) -> None:
    if package.is_symlink() or not package.is_dir():
        raise ValueError(f"package must be a real directory: {package}")
    marker = package / MARKER
    if not marker.is_file() or marker.is_symlink():
        raise ValueError(f"refusing unmanaged generated package: {package}")
    if not marker.read_text(encoding="utf-8").startswith("agent/"):
        raise ValueError(f"invalid ownership marker: {package}")
    # Verify every package's SKILL.md before build_packages can retire anything.
    # A symlink with matching bytes is still foreign content and must be refused.
    skill = package / "SKILL.md"
    if skill.is_symlink():
        raise ValueError(f"{package}: refusing symlinked SKILL.md")
    if skill.exists() and not skill.is_file():
        raise ValueError(f"{package}: SKILL.md must be a regular file")
    contents = {path.name for path in package.iterdir()}
    if contents - {MARKER, "SKILL.md", "repo"}:
        raise ValueError(f"unmanaged extra files in {package}: {sorted(contents)}")
    if not stale:
        link = package / "repo"
        if not link.is_symlink() or os.readlink(link) != REPO_LINK:
            raise ValueError(f"{package}: expected canonical repo link")


def check_packages(root: Path) -> list[str]:
    """Report drift without changing generated packages."""
    root = Path(root).resolve()
    try:
        expected = expected_packages(root)
        output = _output_root(root)
        if not output.exists():
            return ["generated skill packages are missing"] if expected else []
        if not output.is_dir():
            raise ValueError("generated skills root is not a directory")
        actual = {child.name for child in output.iterdir()}
        if actual != set(expected):
            raise ValueError(f"generated skill names differ: missing={sorted(set(expected)-actual)}, extra={sorted(actual-set(expected))}")
        for name, (content, source) in expected.items():
            package = output / name
            _assert_package_dir(package)
            if (package / "SKILL.md").read_text(encoding="utf-8") != content:
                raise ValueError(f"{name}: generated SKILL.md is stale")
            if (package / MARKER).read_text(encoding="utf-8") != source:
                raise ValueError(f"{name}: ownership/source marker is stale")
        return []
    except (OSError, UnicodeError, ValueError) as exc:
        return [str(exc)]


def build_packages(root: Path) -> list[str]:
    """Refresh owned packages, retiring only package directories with own marker."""
    root = Path(root).resolve()
    expected = expected_packages(root)
    output = _output_root(root)
    output.mkdir(parents=True, exist_ok=True)
    actions = []
    # Validate every existing package before any destructive or corrective write.
    # A foreign package must not leave an earlier owned package half-retired.
    existing = {item.name: item for item in output.iterdir()}
    for name, package in sorted(existing.items()):
        _assert_package_dir(package, stale=name not in expected)
    for extra in sorted(set(existing) - set(expected)):
        target = existing[extra]
        shutil.rmtree(target)
        actions.append(f"retired {extra}")
    for name, (content, source) in expected.items():
        package = output / name
        if package.exists() or package.is_symlink():
            _assert_package_dir(package)
        else:
            package.mkdir()
            (package / MARKER).write_text(source, encoding="utf-8")
            (package / "repo").symlink_to(REPO_LINK, target_is_directory=True)
            actions.append(f"created {name}")
        skill = package / "SKILL.md"
        if skill.is_symlink():
            raise ValueError(f"{name}: refusing symlinked SKILL.md")
        if not skill.is_file() or skill.read_text(encoding="utf-8") != content:
            skill.write_text(content, encoding="utf-8")
            actions.append(f"updated {name}")
        if (package / MARKER).read_text(encoding="utf-8") != source:
            (package / MARKER).write_text(source, encoding="utf-8")
            actions.append(f"source {name}")
    issues = check_packages(root)
    if issues:
        raise ValueError("; ".join(issues))
    return actions
