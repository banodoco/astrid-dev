"""Generate standards-compatible skill packages from canonical Markdown sources."""
from __future__ import annotations

from pathlib import Path
import json
import os
import re
import shutil
import tempfile
from urllib.parse import quote, unquote

from agent_documents import AgentDocument, discover_documents
from records import markdown_heading_anchors

OUTPUT = Path(".generated/skills")
MARKER = ".astrid-dev-generated"
REPO_LINK = "../../../"
_LINK = re.compile(r"(!?\[[^\]\n]*\])\(((?:\\[^\n]|<[^>\n]*>|\((?:\\[^\n]|[^()\\\n])*\)|[^()\\\n])+?)\)")
_SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*:", re.I)
_REFERENCE_DEFINITION = re.compile(r"^([ ]{0,3})\[([^\]\n]+)\]:[ \t]*(.*)$")
_REFERENCE_USE = re.compile(r"(?<!\\)\[([^\]\n]+)\](?:\[([^\]\n]*)\])?")
_REF_TOKEN = re.compile(r"^([ \t]*)(<[^>\n]+>|[^\s\n]+)")
_CODE_SPAN = re.compile(r"(?<!\\)(\x60+)(?!\x60)((?:(?!\n[ \t]*\n).)*?)(?<!\x60)\1(?!\x60)", re.S)
_MARKER_SOURCE = re.compile(r"agent/(?:[^/\\\r\n]+/)*([a-z0-9]+(?:-[a-z0-9]+)*)\.md\n\Z")


def _active_lines(lines: list[str]) -> list[bool]:
    """Mask fenced code in ordinary, blockquote and simple list containers."""
    result: list[bool] = []
    fence: str | None = None
    size = 0
    quote_depth = 0
    list_indent = 0
    for line in lines:
        plain = line.rstrip("\r\n")
        quotes = re.match(r"^(?:[ ]{0,3}>[ ]?)*", plain).group(0)
        depth = quotes.count(">")
        rest = plain[len(quotes):]
        if fence is not None:
            # A container can end before its unclosed fence; following prose
            # must still be validated, not swallowed by the example.
            indent = len(rest) - len(rest.lstrip(" "))
            if depth < quote_depth or (list_indent and rest.strip() and indent < list_indent):
                fence, size, list_indent = None, 0, 0
            else:
                inner = rest[list_indent:] if list_indent else rest
                result.append(False)
                if re.fullmatch(r"[ ]{0,3}" + re.escape(fence) + "{" + str(size) + r",}[ \t]*", inner):
                    fence, size, list_indent = None, 0, 0
                continue
        item = re.match(r"^([ ]{0,3}(?:[-+*]|\d{1,9}[.)])[ \t]+)", rest)
        prefix = len(item.group(1)) if item else 0
        inner = rest[prefix:]
        opening = re.match(r"^[ ]{0,3}(\x60{3,}|~{3,})", inner)
        if opening:
            fence, size = opening.group(1)[0], len(opening.group(1))
            quote_depth, list_indent = depth, prefix
            result.append(False)
        else:
            result.append(True)
    return result


def _real_anchors(text: str) -> set[str]:
    """Use shared GitHub slug rules without accepting headings in fences."""
    lines = text.splitlines(keepends=True)
    active = _active_lines(lines)
    visible = "".join(
        line if keep else ("\n" if line.endswith("\n") else "")
        for line, keep in zip(lines, active)
    )
    return {anchor for _, _, anchor in markdown_heading_anchors(visible)}


def _ref_key(label: str) -> str:
    return " ".join(label.split()).casefold()


def _mask_code_spans(line: str) -> str:
    # Keep offsets stable so the original source can be rewritten exactly.
    return _CODE_SPAN.sub(lambda match: "".join("\n" if ch == "\n" else "\r" if ch == "\r" else " " for ch in match.group(0)), line)


def _rewrite_links(source: AgentDocument, root: Path) -> str:
    """Validate and rewrite inline and full/collapsed/shortcut reference links."""
    lines = source.body.splitlines(keepends=True)
    active = _active_lines(lines)
    definitions: set[str] = set()
    destinations: dict[int, tuple[int, int, str, str]] = {}
    definition_lines: set[int] = set()

    def rewrite_address(address: str) -> str:
        if not address:
            return address
        # CommonMark backslash escapes apply to ASCII punctuation in destinations.
        address = re.sub(r"\\([!\"#$%&'()*+,\-./:;<=>?@\[\]\\^_`{|}~])", r"\1", address)
        if address.startswith("#"):
            fragment = unquote(address[1:])
            if fragment and fragment not in _real_anchors(source.body):
                raise ValueError(f"{source.relative}: missing heading in {address}")
            return address
        if address.startswith("/"):
            raise ValueError(
                f"{source.relative}: absolute filesystem link is not portable: {address}"
            )
        if address.lower().startswith("file:") or re.match(r"^[A-Za-z]:", address):
            raise ValueError(
                f"{source.relative}: file: or absolute filesystem link is not portable: {address}"
            )
        if _SCHEME.match(address):
            return address
        pathpart, sep, anchor = address.partition("#")
        pathpart, _, query = pathpart.partition("?")
        target = (source.path.parent / unquote(pathpart)).resolve()
        if not target.is_relative_to(root):
            raise ValueError(f"{source.relative}: link escapes checkout: {address}")
        if not target.exists():
            raise ValueError(f"{source.relative}: missing link target: {address}")
        if anchor and target.is_file() and target.suffix.lower() == ".md":
            if unquote(anchor) not in _real_anchors(target.read_text(encoding="utf-8")):
                raise ValueError(f"{source.relative}: missing heading in {address}")
        result = "repo/" + quote(target.relative_to(root).as_posix(), safe="/-._~")
        if query:
            result += "?" + query
        if sep:
            result += "#" + anchor
        return result

    # Definitions may follow uses and may put the destination on an indented
    # next line. Missing definitions cannot silently become plain prose.
    for index, line in enumerate(lines):
        if not active[index]:
            continue
        quote_prefix = re.match(r"^(?:[ ]{0,3}>[ ]?)*", line).group(0)
        definition = _REFERENCE_DEFINITION.match(line[len(quote_prefix):].rstrip("\r\n"))
        if definition is None:
            continue
        key = _ref_key(definition.group(2))
        if not key or key in definitions:
            raise ValueError(f"{source.relative}: invalid or duplicate reference [{key}]")
        raw = definition.group(3)
        if raw.strip():
            destination_line = index
            token = _REF_TOKEN.match(raw)
            if token is None:
                raise ValueError(f"{source.relative}: unsupported reference [{key}]")
            begin = len(quote_prefix) + definition.start(3) + token.start(2)
            finish = len(quote_prefix) + definition.start(3) + token.end(2)
        else:
            destination_line = index + 1
            if (destination_line >= len(lines) or not active[destination_line]
                    or not lines[destination_line].strip()):
                raise ValueError(f"{source.relative}: reference [{key}] has no destination")
            next_line = lines[destination_line]
            next_prefix = re.match(r"^(?:[ ]{0,3}>[ ]?)*", next_line).group(0)
            if next_prefix.count(">") != quote_prefix.count(">"):
                raise ValueError(f"{source.relative}: reference [{key}] has no destination")
            token = _REF_TOKEN.match(next_line[len(next_prefix):])
            if token is None:
                raise ValueError(f"{source.relative}: reference [{key}] has no destination")
            begin, finish = (position + len(next_prefix) for position in token.span(2))
            definition_lines.add(destination_line)
        original = lines[destination_line][begin:finish]
        address = original[1:-1] if original.startswith("<") and original.endswith(">") else original
        if not address:
            raise ValueError(f"{source.relative}: empty reference destination [{key}]")
        definitions.add(key)
        destinations[destination_line] = (begin, finish, original, address)
        definition_lines.add(index)

    masked_lines = _mask_code_spans("".join(line if keep else " " * (len(line.rstrip("\r\n"))) + ("\n" if line.endswith("\n") else "") for line, keep in zip(lines, active))).splitlines(keepends=True)
    for index, line in enumerate(lines):
        if not active[index] or index in definition_lines:
            continue
        masked = masked_lines[index]
        for match in reversed(list(_LINK.finditer(masked))):
            masked = (masked[:match.start()]
                      + " " * (match.end() - match.start())
                      + masked[match.end():])
        checkbox = re.match(r"^\s*(?:[-*+]|\d+[.)])\s+\[([ xX])\]", masked)
        for match in _REFERENCE_USE.finditer(masked):
            if checkbox and checkbox.start(1) - 1 == match.start():
                continue
            if match.group(1).startswith("^"):
                continue  # Footnote syntax is not a Markdown link.
            label = match.group(2) if match.group(2) else match.group(1)
            key = _ref_key(label)
            if key not in definitions:
                raise ValueError(f"{source.relative}: undefined reference [{key}]")

    for index, line in enumerate(lines):
        if not active[index]:
            continue
        masked = masked_lines[index]
        replacements: list[tuple[int, int, str]] = []
        for match in _LINK.finditer(masked):
            actual = _LINK.fullmatch(line[match.start():match.end()])
            assert actual is not None
            label, raw = actual.groups()
            quoted = re.match(r'^(<[^>\n]*>|\S+)(\s+"[^"\n]*")?$', raw)
            if quoted is None:
                raise ValueError(f"{source.relative}: unsupported Markdown link {raw!r}")
            address, suffix = quoted.group(1), quoted.group(2) or ""
            angle = address.startswith("<") and address.endswith(">")
            address = address[1:-1] if angle else address
            rewritten = rewrite_address(address)
            rewritten = f"<{rewritten}>" if angle else rewritten
            replacements.append(
                (match.start(), match.end(),
                 label + "(" + rewritten + suffix + ")")
            )
        if index in destinations:
            begin, finish, token, address = destinations[index]
            rewritten = rewrite_address(address)
            if rewritten != address:
                value = f"<{rewritten}>" if token.startswith("<") else rewritten
                replacements.append((begin, finish, value))
        for begin, finish, value in sorted(replacements, reverse=True):
            line = line[:begin] + value + line[finish:]
        lines[index] = line
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
    source = marker.read_text(encoding="utf-8")
    match = _MARKER_SOURCE.fullmatch(source)
    if (match is None or any(part in (".", "..") for part in source.strip().split("/"))
            or package.name != "astrid-dev-" + match.group(1)):
        raise ValueError(f"invalid ownership marker: {package}")
    # Verify every package's SKILL.md before build_packages can retire anything.
    # A symlink with matching bytes is still foreign content and must be refused.
    skill = package / "SKILL.md"
    if skill.is_symlink():
        raise ValueError(f"{package}: refusing symlinked SKILL.md")
    if skill.exists() and not skill.is_file():
        raise ValueError(f"{package}: SKILL.md must be a regular file")
    if stale and not skill.is_file():
        raise ValueError(f"{package}: stale SKILL.md must be a regular file")
    contents = {path.name for path in package.iterdir()}
    if contents - {MARKER, "SKILL.md", "repo"}:
        raise ValueError(f"unmanaged extra files in {package}: {sorted(contents)}")
    # Even obsolete packages must retain an owned, canonical repo entry.
    # Check every member of every package before retiring any stale package.
    link = package / "repo"
    if not link.is_symlink() or os.readlink(link) != REPO_LINK:
        raise ValueError(f"{package}: expected canonical repo link")


def _check_output(output: Path, expected: dict[str, tuple[str, str]]) -> None:
    if not output.exists():
        if expected:
            raise ValueError("generated skill packages are missing")
        return
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


def check_packages(root: Path) -> list[str]:
    """Report drift without changing generated packages."""
    root = Path(root).resolve()
    try:
        _check_output(_output_root(root), expected_packages(root))
        return []
    except (OSError, UnicodeError, ValueError) as exc:
        return [str(exc)]


def _build_output(output: Path, expected: dict[str, tuple[str, str]]) -> list[str]:
    """Apply changes to a private staged copy of the generated tree."""
    actions = []
    # Validate every existing package before any destructive or corrective write.
    # A foreign package must not leave an earlier owned package half-retired.
    existing = {item.name: item for item in output.iterdir()}
    for name, package in sorted(existing.items()):
        _assert_package_dir(package, stale=name not in expected)
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
            # Verify a refresh may write the existing file, then stage the new
            # bytes before replacement so a failed write cannot truncate it.
            if skill.exists():
                with skill.open("r+", encoding="utf-8"):
                    pass
            staged = None
            try:
                with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=package,
                                                 delete=False) as pending:
                    staged = Path(pending.name)
                    pending.write(content)
                if skill.exists():
                    os.chmod(staged, skill.stat().st_mode & 0o777)
                os.replace(staged, skill)
            finally:
                if staged is not None:
                    staged.unlink(missing_ok=True)
            actions.append(f"updated {name}")
        if (package / MARKER).read_text(encoding="utf-8") != source:
            (package / MARKER).write_text(source, encoding="utf-8")
            actions.append(f"source {name}")
    for extra in sorted(set(existing) - set(expected)):
        target = existing[extra]
        shutil.rmtree(target)
        actions.append(f"retired {extra}")
    _check_output(output, expected)
    return actions


def build_packages(root: Path) -> list[str]:
    """Stage the complete owned tree and restore it if publication fails."""
    root = Path(root).resolve()
    expected = expected_packages(root)
    output = _output_root(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and not output.is_dir():
        raise ValueError("generated skills root is not a directory")
    existing = {item.name: item for item in output.iterdir()} if output.exists() else {}
    for name, package in sorted(existing.items()):
        _assert_package_dir(package, stale=name not in expected)
    # Preserve the existing refusal for read-only active files and check every
    # one before doing any work on the staged copy.
    for name, (content, source) in expected.items():
        package = existing.get(name)
        if package is None:
            continue
        skill = package / "SKILL.md"
        if skill.exists() and skill.read_text(encoding="utf-8") != content:
            with skill.open("r+", encoding="utf-8"):
                pass
        marker = package / MARKER
        if marker.read_text(encoding="utf-8") != source:
            with marker.open("r+", encoding="utf-8"):
                pass
    scratch = Path(tempfile.mkdtemp(prefix=".skills-build-", dir=output.parent))
    stage = scratch / "skills"
    backup = scratch / "previous"
    preserve_backup = False
    try:
        if output.exists():
            shutil.copytree(output, stage, symlinks=True)
        else:
            stage.mkdir()
        actions = _build_output(stage, expected)
        if not actions and output.exists():
            return actions
        had_output = output.exists()
        if had_output:
            os.replace(output, backup)
        try:
            os.replace(stage, output)
        except BaseException:
            if had_output:
                try:
                    os.replace(backup, output)
                except BaseException as rollback_error:
                    # Never remove the only surviving original if restoration
                    # itself fails; report the recovery path to the caller.
                    preserve_backup = True
                    raise RuntimeError(f"package rollback failed; original retained at {backup}") from rollback_error
            raise
        return actions
    finally:
        if not preserve_backup:
            shutil.rmtree(scratch, ignore_errors=True)
