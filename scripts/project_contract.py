"""Shared project identity and vision-gap declarations; not a second registry."""
from __future__ import annotations
import re
from pathlib import Path

PLAN_FOLDER = re.compile(r"\d{2,}-[a-z0-9-]+")
GAP_LINK = re.compile(r"\]\(\.\./\.\./visions/gaps/([A-Z]{1,3}-\d{3})-[^)]+\.md\)")
VISION_GAPS = re.compile(r"^\*\*Vision gaps:\*\*\s*(.+)$", re.M)
VISION_ROLE = re.compile(r"^\*\*Vision role:\*\*\s*(.+)$", re.M)


def project_number(plan_path: str | Path) -> str:
    """Stable numeric ID, including projects >= 100."""
    folder = Path(plan_path).parent.name
    if not PLAN_FOLDER.fullmatch(folder):
        raise ValueError(f"invalid project folder: {folder}")
    return folder.split("-", 1)[0]


def plan_gap_ids(plan_text: str) -> list[str]:
    """The one interpretation used by validation, completion and publishing."""
    gaps, roles = VISION_GAPS.findall(plan_text), VISION_ROLE.findall(plan_text)
    if len(gaps) + len(roles) != 1:
        raise ValueError("expected exactly one Vision gaps or Vision role declaration")
    if roles:
        return []
    ids = GAP_LINK.findall(gaps[0])
    if not ids:
        raise ValueError("Vision gaps declaration needs a gap document link")
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate gap IDs in plan declaration")
    return ids
