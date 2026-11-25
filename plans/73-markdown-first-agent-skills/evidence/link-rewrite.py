#!/usr/bin/env python3
"""MSC-6 mechanical step: re-point every relative Markdown link into skills/ at its agent/ home.

Run from a checkout root.  Uses scripts/agent_reference_inventory.py:mapped_target for the
skills/ -> agent/ mapping, so the mapping is the one the inventory already proposes.
  link_rewrite.py            dry run: print counts and every unmapped link
  link_rewrite.py --write    rewrite files in place
Only links inside Markdown files outside skills/ and agent/ are touched; prose, absolute URLs
and links to anything other than skills/ are left alone.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "scripts"))
import agent_reference_inventory as inv  # noqa: E402

LINK = re.compile(r"(?<!\\)(\]\()([^)\s]+)((?:\s+\"[^\"]*\")?\))")


def tracked_markdown() -> list[str]:
    raw = subprocess.check_output(["git", "ls-files", "-z", "--", "*.md"], cwd=ROOT)
    return [p for p in sorted(x.decode() for x in raw.split(b"\0") if x)
            if not p.startswith(("skills/", "agent/"))]


EXTRA = {  # homes recorded in the cutover maps that the inventory's mapper does not know
    "skills/shared/workstreams.md": "agent/README.md",
    "skills/roles/astrid-dev-orchestrate/workstreams/measurement-box/README.md": "agent/guides/measurement-box/README.md",
    "skills/roles/astrid-dev-plan/SKILL.md": "agent/shared/workstreams/plan.md",
    "skills/shared/workstreams/astrid-dev-release/qualification.md": "agent/shared/release-qualification.md",
}


def map_target(path: str) -> str | None:
    """skills/... -> agent/..., or None when neither the inventory nor the cutover maps know a home."""
    return EXTRA.get(path) or inv.mapped_target(path, "path")


def rewrite(text: str, source: str, write: bool):
    changed = unmapped = 0
    bad: list[tuple[str, str]] = []
    base = (ROOT / source).parent

    def sub(match: re.Match) -> str:
        nonlocal changed, unmapped
        raw = match.group(2)
        if re.match(r"^[a-z][a-z0-9+.-]*:", raw, re.I) or raw.startswith("#"):
            return match.group(0)
        target, hash_, anchor = raw.partition("#")
        if not target:
            return match.group(0)
        resolved = Path(os.path.normpath(base / target))
        try:
            rel = resolved.relative_to(ROOT).as_posix()
        except ValueError:
            return match.group(0)
        if not (rel == "skills" or rel.startswith("skills/")):
            return match.group(0)
        home = map_target(rel)
        if home is None:
            unmapped += 1
            bad.append((source, raw))
            return match.group(0)
        new = os.path.relpath(ROOT / home, base).replace(os.sep, "/")
        if target.endswith("/") and not new.endswith("/"):
            new += "/"
        changed += 1
        return match.group(1) + new + (hash_ + anchor) + match.group(3)

    return LINK.sub(sub, text), changed, unmapped, bad


def main() -> int:
    write = "--write" in sys.argv
    total = unmapped_total = files = 0
    all_bad: list[tuple[str, str]] = []
    for path in tracked_markdown():
        text = (ROOT / path).read_text(encoding="utf-8")
        new, changed, unmapped, bad = rewrite(text, path, write)
        total += changed
        unmapped_total += unmapped
        all_bad += bad
        if changed:
            files += 1
            if write and new != text:
                (ROOT / path).write_text(new, encoding="utf-8")
    print(f"{'rewrote' if write else 'would rewrite'} {total} links in {files} files; {unmapped_total} unmapped")
    for source, raw in all_bad:
        print(f"UNMAPPED {source}: {raw}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
