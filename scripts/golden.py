#!/usr/bin/env python3
"""Print the current documentation and public-vision errors for the repo and fixtures."""
from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

import check_docs
import export_public_vision

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / "fixtures"
REVISION = "0000000000000000000000000000000000000000"


def _copy_tree(destination: Path) -> None:
    ignored = shutil.ignore_patterns(".git", ".otto", "__pycache__", "fixtures")
    shutil.copytree(ROOT, destination, ignore=ignored, dirs_exist_ok=True)


def _errors(root: Path) -> list[str]:
    errors, _warnings = check_docs.check(root)
    try:
        page = export_public_vision.build(root, REVISION)
        expected_vision = export_public_vision.render_readme(root, page)
        vision = (root / "vision/README.md").read_text(encoding="utf-8")
        if vision != expected_vision:
            raise ValueError("vision/README.md is stale; run python3 scripts/export_public_vision.py --sync-readme")
        source = (root / "README.md").read_text(encoding="utf-8")
        if source != export_public_vision.render_root_readme(source, page):
            raise ValueError("README.md vision summary is stale; run python3 scripts/export_public_vision.py --sync-readme")
    except (ValueError, OSError) as exc:
        errors.append(f"public vision content: {exc}")
    return errors


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
