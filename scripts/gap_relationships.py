"""Resolve each gap to one primary goal and any supporting goals.

The source names goals; the schema-v1 element relationships remain a
projection so existing App builds can keep reading the public feed.
"""
from __future__ import annotations

import re
from pathlib import Path

from records import markdown_heading_anchors
from vision_subject import parse_subject

ENTRY = re.compile(
    r"\[([^\]\n]+)\]\((\.\./(?:pillars|principles)/[a-z0-9-]+\.md)#([^()\s]+)\)"
    r"\s+\((primary|supporting)\)"
)
VISION = Path(__file__).resolve().parents[1] / "vision"


def gap_metadata(text: str) -> str:
    """Reject old, repeated or mixed relationship lines, not just the first one."""
    lines = [line for line in text.splitlines()
             if line.startswith(("**Goal:**", "**Applies to:**"))]
    if len(lines) != 1 or not lines[0].startswith("**Goal:**"):
        raise ValueError("expected exactly one Goal metadata line; Applies to is no longer accepted")
    return lines[0]


def parse_gap_goals(metadata: str, vision_root: Path = VISION) -> tuple[list[str], str]:
    """Return ordered goal refs and the primary, checking their actual headings."""
    if (not metadata.startswith("**Goal:**") or "**Assessment:**" not in metadata
            or "\n" in metadata or "**Applies to:**" in metadata):
        raise ValueError("expected Goal and Assessment on the same metadata line")
    raw = metadata.split("**Assessment:**", 1)[0].removeprefix("**Goal:**").strip()
    tokens = [token.strip() for token in raw.removesuffix("·").strip().split("·")]
    if not tokens or any(not token for token in tokens):
        raise ValueError("gap must have clearly separated Goal entries")
    references: list[str] = []
    primary: list[str] = []
    for token in tokens:
        match = ENTRY.fullmatch(token)
        if not match:
            raise ValueError(f"invalid gap goal or role: {token}")
        label, target, anchor, role = match.groups()
        path = vision_root / target.removeprefix("../")
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise ValueError(f"unknown goal element: {target}") from exc
        subject = parse_subject(text, str(path))
        headings = {fragment: title for level, title, fragment in markdown_heading_anchors(text) if level == 3}
        title = headings.get(anchor)
        goal = next((item for item in subject["goals"] if item["title"] == title), None)
        if goal is None:
            raise ValueError(f"unknown goal anchor: {target}#{anchor}")
        if label != goal["title"]:
            raise ValueError(f"goal link text must be its title: {goal['title']}")
        kind = "pillar" if target.startswith("../pillars/") else "principle"
        ref = f"{kind}:{path.stem}/{goal['id']}"
        if ref in references:
            raise ValueError(f"duplicate gap goal: {ref}")
        references.append(ref)
        if role == "primary":
            primary.append(ref)
    if len(primary) != 1:
        raise ValueError(f"exactly one primary gap goal required, found {len(primary)}")
    if references[0] != primary[0]:
        raise ValueError("put the primary goal first")
    return references, primary[0]


def parse_gap_relationships(metadata: str, vision_root: Path = VISION) -> tuple[list[str], str]:
    """Keep (element refs, primary element) for the schema-v1 consumer contract."""
    goals, primary = parse_gap_goals(metadata, vision_root)
    relationships = list(dict.fromkeys(ref.split("/", 1)[0] for ref in goals))
    return relationships, primary.split("/", 1)[0]
