#!/usr/bin/env python3
"""Print the current documentation and public-vision errors for the repo and fixtures."""
from __future__ import annotations

import json
import shutil
import tempfile
import contextlib
import io
from pathlib import Path

import astrid_dev

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / "fixtures"
REVISION = "0000000000000000000000000000000000000000"


def _copy_tree(destination: Path) -> None:
    ignored = shutil.ignore_patterns(".git", ".otto", "__pycache__", "fixtures")
    shutil.copytree(ROOT, destination, ignore=ignored, dirs_exist_ok=True)


def _errors(root: Path) -> list[str]:
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        astrid_dev.main(["check"], root=root)
    return [line.removeprefix("ERROR ").split(": ", 1)[1]
            for line in output.getvalue().splitlines()]


@contextlib.contextmanager
def _overlay(root: Path, overlay: dict[str, str]):
    """Apply one fixture and restore every touched path on exit."""
    previous: dict[Path, bytes | None] = {}
    created_dirs: set[Path] = set()
    try:
        for relative, contents in overlay.items():
            target = root / relative
            if target not in previous:
                previous[target] = target.read_bytes() if target.is_file() else None
            missing = []
            parent = target.parent
            while parent != root and not parent.exists():
                missing.append(parent)
                parent = parent.parent
            target.parent.mkdir(parents=True, exist_ok=True)
            created_dirs.update(missing)
            target.write_text(contents, encoding="utf-8")
        yield
    finally:
        for target, contents in reversed(list(previous.items())):
            if contents is None:
                target.unlink(missing_ok=True)
            else:
                target.write_bytes(contents)
        for directory in sorted(created_dirs, key=lambda path: len(path.parts), reverse=True):
            try:
                directory.rmdir()
            except OSError:
                pass


def collect() -> list[str]:
    output = [f"real: {error}" for error in _errors(ROOT)]
    with tempfile.TemporaryDirectory(prefix="astrid-golden-") as directory:
        root = Path(directory) / "repo"
        _copy_tree(root)
        for overlay_path in sorted(FIXTURES.glob("*/overlay.json")):
            fixture = overlay_path.parent
            overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
            with _overlay(root, overlay):
                output.extend(f"{fixture.name}: {error}" for error in _errors(root))
    return sorted(output)


def main() -> int:
    for error in collect():
        print(error)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
