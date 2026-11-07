"""Shared parser for a gap's explicit primary and supporting vision relationships."""
from __future__ import annotations

import re
from pathlib import Path

ENTRY = re.compile(
    r"\[([^\]\n]+)\]\((\.\./(?:pillars/[a-z0-9-]+\.md|principles\.md#[a-z0-9-]+))\)"
    r"\s+\((primary|supporting)\)"
)


def parse_gap_relationships(metadata: str) -> tuple[list[str], str]:
    """Return (all relationship refs, primary relationship ref), strictly validated.

    Keep the same contract for docs CI and the public JSON exporter.
    """
    if not metadata.startswith("**Applies to:**") or "**Assessment:**" not in metadata:
        raise ValueError("expected Applies to and Assessment on the same metadata line")
    raw = metadata.split("**Assessment:**", 1)[0].removeprefix("**Applies to:**").strip()
    raw = raw.removesuffix("·").strip()
    tokens = [token.strip() for token in raw.split("·")]
    if not tokens or any(not token for token in tokens):
        raise ValueError("gap must have clearly separated Applies to entries")
    relationships: list[str] = []
    primary: list[str] = []
    for token in tokens:
        match = ENTRY.fullmatch(token)
        if not match:
            raise ValueError(f"invalid gap relationship or role: {token}")
        _, target, role = match.groups()
        if target.startswith("../pillars/"):
            ref = "pillar:" + Path(target).stem
        else:
            ref = "principle:" + target.partition("#")[2]
        if ref in relationships:
            raise ValueError(f"duplicate gap relationship: {ref}")
        relationships.append(ref)
        if role == "primary":
            primary.append(ref)
    if len(primary) != 1:
        raise ValueError(f"exactly one primary gap relationship required, found {len(primary)}")
    if relationships[0] != primary[0]:
        raise ValueError("put the primary relationship first")
    return relationships, primary[0]
