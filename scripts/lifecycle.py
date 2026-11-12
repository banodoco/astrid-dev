"""The project's lifecycle vocabulary and the requirements for entering it."""
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Status:
    name: str
    terminal: bool
    meaning: str
    needs: tuple[str, ...] = ()


STATUSES = (
    Status("queued", False, "planned, not started"),
    Status("active", False, "explicitly started", ("named-owner",)),
    Status("blocked", False, "known impediment"),
    Status("paused", False, "deliberately stopped"),
    Status("done", True, "accepted completion evidence", ("completion-assessment",)),
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
    return tuple(status.name for status in STATUSES if need in status.needs)


def definitions():
    return "; ".join(f"`{status.name}` = {status.meaning}" for status in STATUSES) + "."
