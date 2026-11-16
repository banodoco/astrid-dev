"""The project's lifecycle vocabulary and the requirements for entering it."""
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Status:
    name: str
    terminal: bool
    meaning: str
    needs: tuple[str, ...] = ()


NAMED_OWNER = "named-owner"
COMPLETION_ASSESSMENT = "completion-assessment"
NEEDS = (NAMED_OWNER, COMPLETION_ASSESSMENT)


STATUSES = (
    Status("queued", False, "planned, not started"),
    Status("active", False, "explicitly started", (NAMED_OWNER,)),
    Status("blocked", False, "known impediment"),
    Status("paused", False, "deliberately stopped"),
    Status("done", True, "accepted completion evidence", (COMPLETION_ASSESSMENT,)),
    Status("cancelled", True, "intentionally abandoned, with reason in the plan"),
)


def names():
    return tuple(status.name for status in STATUSES)


def terminal():
    return tuple(status.name for status in STATUSES if status.terminal)


def phrase():
    values = names()
    return ", ".join(values[:-1]) + " or " + values[-1]


def route_pattern():
    return r"(?i)\b(" + "|".join(re.escape(name) for name in names()) + r")\b"


def requiring(need):
    if need not in NEEDS:
        known = ", ".join(NEEDS)
        raise ValueError(f"unknown lifecycle need {need!r}; known needs: {known}")
    return tuple(status.name for status in STATUSES if need in status.needs)


def definitions():
    return "; ".join(f"`{status.name}` = {status.meaning}" for status in STATUSES) + "."
