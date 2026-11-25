"""Generate standards-compatible skill packages from canonical Markdown sources."""
from __future__ import annotations

from pathlib import Path
import json
import ctypes
import errno
import os
import stat
import sys
from contextlib import contextmanager
import re
import shutil
import tempfile
from urllib.parse import quote, unquote

from agent_documents import AGENT_SOURCE_ROOT, SKILL_PREFIX, AgentDocument, discover_documents
from document_structure import markdown_heading_anchors

OUTPUT = Path(".generated/skills")
MARKER = f".{SKILL_PREFIX}generated"
REPO_LINK = "../../../"
# The angle form is a destination only when it starts one (CommonMark); elsewhere "<" and ">" are ordinary
# characters. Keeping the alternatives disjoint means no input can backtrack exponentially.
_LINK = re.compile(r"(!?\[[^\]\n]*\])\((<[^>\n]*>|(?:\\[^\n]|\((?:\\[^\n]|[^()\\\n])*\)|[^()\\\n])+?)\)")
_SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*:", re.I)
_REFERENCE_DEFINITION = re.compile(r"^([ ]{0,3})\[([^\]\n]+)\]:[ \t]*(.*)$")
_REFERENCE_USE = re.compile(r"(?<!\\)\[([^\]\n]+)\](?:\[([^\]\n]*)\])?")
_REF_TOKEN = re.compile(r"^([ \t]*)(<[^>\n]+>|[^\s\n]+)")
_CODE_SPAN = re.compile(r"(?<!\\)(\x60+)(?!\x60)((?:(?!\n[ \t]*\n).)*?)(?<!\x60)\1(?!\x60)", re.S)
_MARKER_SOURCE = re.compile(re.escape(AGENT_SOURCE_ROOT) + r"/(?:[^/\\\r\n]+/)*([a-z0-9]+(?:-[a-z0-9]+)*)\.md\n\Z")


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
    # Retain list containers across lazy paragraph continuations. A code
    # block in a list starts four columns beyond its innermost item indent;
    # lesser indentation can contain live links and must be validated.
    previous_blank = True
    previous_depth = 0
    indented_context: tuple[int, tuple[tuple[int, int], ...]] | None = None
    list_stack: list[tuple[int, int]] = []  # marker column, content column
    list_quote_depth = 0
    uncertain_quote_container = False
    for index, line in enumerate(lines):
        plain = line.rstrip("\r\n")
        quote = re.match(r"^(?:[ ]{0,3}>[ ]?)+", plain)
        depth = quote.group(0).count(">") if quote else 0
        content = plain[len(quote.group(0)):] if quote else plain
        if not content.strip():
            # An unquoted blank ends a blockquote; a quoted blank retains it.
            if not quote and list_quote_depth:
                list_stack.clear()
                list_quote_depth = 0
                uncertain_quote_container = False
                indented_context = None
            previous_blank = True
            previous_depth = depth
            continue
        if depth != list_quote_depth:
            list_stack.clear()
            uncertain_quote_container = False
            list_quote_depth = depth
        # Expand indentation from the actual column after quote markers.
        # When the separator is a tab, CommonMark consumes one expanded space
        # for marker separation; the remainder contributes to indentation.
        prefix = quote.group(0) if quote else ""
        start_column = len(prefix.expandtabs(4))
        whitespace = content[:len(content) - len(content.lstrip(" \t"))]
        leading = len((prefix + whitespace).expandtabs(4)) - start_column
        if quote and prefix.endswith(">") and content.startswith("\t"):
            leading -= 1
        marker = re.match(r"^([ ]*)([-+*]|\d{1,9}[.)])([ \t]+)", content)
        # Tabs in up to three indentation columns before a quoted list
        # marker are measured at their physical tab stops.
        split_tab_marker = None
        if quote and "\t" in whitespace and leading <= 3:
            split_tab_marker = re.match(r"^([ \t]+)([-+*]|\d{1,9}[.)])([ \t]+)", content)
            marker = marker or split_tab_marker
        if (not marker and quote and prefix.endswith(">") and content.startswith("\t")
                and re.match(r"^(?:[-+*]|\d{1,9}[.)])[ \t]+", content.lstrip(" \t"))):
            # The tab straddles marker whitespace and indentation. Until this
            # quote closes, retain potentially live list content for checking.
            uncertain_quote_container = True
        if marker and (len(marker.group(1)) < 4 or list_stack):
            marker_column = leading if split_tab_marker else len(marker.group(1))
            while list_stack and marker_column < list_stack[-1][1]:
                list_stack.pop()
            marker_end = marker_column + len(marker.group(2))
            content_column = len((prefix + marker.group(0)).expandtabs(4)) - start_column
            if split_tab_marker and prefix.endswith(">") and content.startswith("\t"):
                content_column -= 1
            # CommonMark treats more than four padding columns as one; the
            # remainder is content, often an indented code example.
            if content_column - marker_end > 4:
                content_column = marker_end + 1
            list_stack.append((marker_column, content_column))
        elif previous_blank:
            while list_stack and leading < list_stack[-1][1]:
                list_stack.pop()
        threshold = (list_stack[-1][1] if list_stack else 0) + 4
        indented = leading >= threshold
        context = (depth, tuple(list_stack))
        eligible = result[index] and not marker and indented and not uncertain_quote_container
        starts_block = previous_blank or depth > previous_depth
        if eligible and (indented_context == context or starts_block):
            result[index] = False
            indented_context = context
        else:
            indented_context = None
        previous_blank = False
        previous_depth = depth
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
                (Path(AGENT_SOURCE_ROOT) / doc.relative).as_posix() + "\n",
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
            or package.name != SKILL_PREFIX + match.group(1)):
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


_LOCK_CONTENT = f"{SKILL_PREFIX}skill-build-lock-v1\n".encode("ascii")


@contextmanager
def _build_lock(parent: Path):
    """Nonblocking cooperative lock at a stable, owned, non-symlink path."""
    try:
        import fcntl
    except ImportError as exc:
        raise OSError(errno.ENOTSUP, "skill build locking unavailable") from exc
    if not hasattr(os, "O_NOFOLLOW"):
        raise OSError(errno.ENOTSUP, "safe lock opening unavailable")
    path = parent / ".skills-build.lock"
    flags = os.O_RDWR | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
    # Prepare complete contents before linking the stable lock name. A process
    # death during setup cannot strand a half-written public lock file.
    temp_fd, temp_name = tempfile.mkstemp(prefix=".skills-lock-", dir=parent)
    try:
        with os.fdopen(temp_fd, "wb") as prepared:
            prepared.write(_LOCK_CONTENT)
        try:
            os.link(temp_name, path, follow_symlinks=False)
        except FileExistsError:
            pass
    finally:
        os.unlink(temp_name)
    fd = os.open(path, flags)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid():
            raise ValueError("refusing foreign skill build lock")
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError("another skill build is in progress") from exc
        identity = os.stat(path, follow_symlinks=False)
        if (info.st_dev, info.st_ino) != (identity.st_dev, identity.st_ino):
            raise ValueError("skill build lock changed during acquisition")
        if os.read(fd, len(_LOCK_CONTENT) + 1) != _LOCK_CONTENT:
            raise ValueError("refusing foreign skill build lock")
        yield
    finally:
        os.close(fd)


def _exchange_paths(left: Path, right: Path) -> None:
    """Exchange two existing paths or fail closed if unsupported."""
    libc = ctypes.CDLL(None, use_errno=True)
    if sys.platform == "darwin":
        function = getattr(libc, "renamex_np", None)
        if function is None:
            raise OSError(errno.ENOTSUP, "atomic directory exchange unavailable")
        function.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
        result = function(os.fsencode(left), os.fsencode(right), 2)  # RENAME_SWAP
    elif sys.platform.startswith("linux"):
        function = getattr(libc, "renameat2", None)
        if function is None:
            raise OSError(errno.ENOTSUP, "atomic directory exchange unavailable")
        function.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
        result = function(-100, os.fsencode(left), -100, os.fsencode(right), 2)  # AT_FDCWD, RENAME_EXCHANGE
    else:
        raise OSError(errno.ENOTSUP, "atomic directory exchange unavailable")
    if result != 0:
        code = ctypes.get_errno()
        raise OSError(code, os.strerror(code))


def _probe_exchange(parent: Path) -> None:
    """Verify the actual filesystem supports populated-directory exchange."""
    with tempfile.TemporaryDirectory(prefix=".skills-probe-", dir=parent) as scratch:
        left, right = Path(scratch) / "left", Path(scratch) / "right"
        left.mkdir()
        right.mkdir()
        (left / "old").touch()
        (right / "new").touch()
        _exchange_paths(left, right)
        if not (left / "new").is_file() or not (right / "old").is_file():
            raise OSError(errno.ENOTSUP, "atomic directory exchange probe failed")


class PublicationCommittedError(OSError):
    """Publication succeeded but a later finalization step failed."""


def build_packages(root: Path) -> list[str]:
    """Publish an owned real-directory generation using a capability-gated exchange."""
    published = [False]
    try:
        return _build_packages(root, published)
    except Exception as exc:
        if published[0]:
            raise PublicationCommittedError(
                f"skill generation published; finalization failed: {exc}"
            ) from exc
        raise


def _build_packages(root: Path, published: list[bool]) -> list[str]:
    root = Path(root).resolve()
    output = _output_root(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    with _build_lock(output.parent):
        _output_root(root)  # Refuse a changed or symlinked output path again.
        expected = expected_packages(root)
        if output.exists() and not output.is_dir():
            raise ValueError("generated skills root is not a directory")
        initial_stat = output.stat() if output.exists() else None
        initial_identity = ((initial_stat.st_dev, initial_stat.st_ino) if initial_stat else None)
        existing = {item.name: item for item in output.iterdir()} if output.exists() else {}
        for name, package in sorted(existing.items()):
            _assert_package_dir(package, stale=name not in expected)
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
        _probe_exchange(output.parent)
        with tempfile.TemporaryDirectory(prefix=".skills-build-", dir=output.parent,
                                         ignore_cleanup_errors=True) as scratch:
            stage = Path(scratch) / "skills"
            if output.exists():
                shutil.copytree(output, stage, symlinks=True)
            else:
                stage.mkdir()
            actions = _build_output(stage, expected)
            if not actions and output.exists():
                return actions
            if expected_packages(root) != expected:
                raise RuntimeError("skill sources changed during build; retry")
            _output_root(root)
            current_stat = output.stat() if output.exists() else None
            current_identity = ((current_stat.st_dev, current_stat.st_ino) if current_stat else None)
            if current_identity != initial_identity:
                raise RuntimeError("skill output changed during build; retry")
            for name, package in sorted(existing.items()):
                _assert_package_dir(package, stale=name not in expected)
            # Initial publication creates an empty owned directory without
            # replacing an existing path; subsequent publication exchanges it.
            created = False
            if not output.exists():
                output.mkdir()
                created = True
            try:
                _exchange_paths(output, stage)
                published[0] = True
            except BaseException:
                if created:
                    output.rmdir()
                raise
            return actions
