"""The project's lifecycle vocabulary and the requirements for entering it."""
from dataclasses import dataclass


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
    raise NotImplementedError


def terminal():
    raise NotImplementedError


def phrase():
    raise NotImplementedError


def route_pattern():
    raise NotImplementedError


def requiring(need):
    raise NotImplementedError


def definitions():
    raise NotImplementedError
