"""Shared project identity and vision-gap declarations; not a second registry."""
from __future__ import annotations
import re
from pathlib import Path

PLAN_FOLDER = re.compile(r"\d{2,}-[a-z0-9-]+")
GAP_LINK = re.compile(r"\]\(\.\./\.\./vision/gaps/([A-Z]{1,3}-\d{3})-[^)]+\.md\)")
VISION_GAPS = re.compile(r"^\*\*Vision gaps:\*\*\s*(.+)$", re.M)
VISION_ROLE = re.compile(r"^\*\*Vision role:\*\*\s*(.+)$", re.M)
VISION_ENABLER_ROLE = re.compile(
    r"^(?:Foundational|Communication) enabler(?:\s*[—–:]\s*\S.*)?$"
)


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
        role = roles[0].strip()
        # A gapless plan must explicitly declare a supported enabler kind;
        # an arbitrary placeholder must not masquerade as delivery evidence.
        if not VISION_ENABLER_ROLE.fullmatch(role):
            raise ValueError(
                f"unsupported Vision role {role!r}; expected explicit "
                "Foundational enabler or Communication enabler")
        return []
    ids = GAP_LINK.findall(gaps[0])
    if not ids:
        raise ValueError("Vision gaps declaration needs a gap document link")
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate gap IDs in plan declaration")
    # Refuse an authored link with both roles; preserve the accepted ordering.
    gap_matches = list(GAP_LINK.finditer(gaps[0]))
    for i, match in enumerate(gap_matches):
        next_start = (gap_matches[i + 1].start()
                      if i + 1 < len(gap_matches) else len(gaps[0]))
        role_text = gaps[0][match.end():next_start]
        if "(primary)" in role_text and "(supporting)" in role_text:
            raise ValueError(f"gap {ids[i]} has contradictory primary/supporting roles")
    # The first linked gap is the one project owns. Other gaps may inform
    # dependencies, but the public vision renders this project only once.
    primary_count = len(re.findall(r"\(primary\)", gaps[0]))
    if primary_count != 1:
        raise ValueError("project must declare exactly one primary vision gap")
    first_link = GAP_LINK.search(gaps[0])
    first_primary = re.search(r"\(primary\)", gaps[0])
    second_link = list(GAP_LINK.finditer(gaps[0]))
    if first_link is None or first_primary is None or first_primary.start() < first_link.end():
        raise ValueError("primary gap must follow the first gap link")
    if len(second_link) > 1 and first_primary.start() > second_link[1].start():
        raise ValueError("primary gap must be the first linked gap")
    return ids
