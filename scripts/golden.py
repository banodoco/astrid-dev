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


def collect() -> list[str]:
    output = [f"real: {error}" for error in _errors(ROOT)]
    for overlay_path in sorted(FIXTURES.glob("*/overlay.json")):
        fixture = overlay_path.parent
        with tempfile.TemporaryDirectory(prefix="astrid-golden-") as directory:
            root = Path(directory) / "repo"
            _copy_tree(root)
            overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
            for relative, contents in overlay.items():
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(contents, encoding="utf-8")
            output.extend(f"{fixture.name}: {error}" for error in _errors(root))
    return sorted(output)


def main() -> int:
    for error in collect():
        print(error)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
