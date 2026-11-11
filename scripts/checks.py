"""Registry contract for repository checks."""
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Literal


@dataclass(frozen=True)
class Context:
    root: Path
    base: str | None = None
    event: Path | None = None
    body_file: Path | None = None


@dataclass(frozen=True)
class Check:
    id: str
    trigger: Literal["always", "pr"]
    description: str
    run: Callable[[Context], list[str]]

    def __post_init__(self):
        if not self.id or any(c.isspace() for c in self.id):
            raise ValueError("check id must be a nonempty token")
        if self.trigger not in ("always", "pr"):
            raise ValueError("check trigger must be always or pr")
        if not self.description.strip() or "\n" in self.description or "\r" in self.description:
            raise ValueError("check description must be one nonempty line")
        if not callable(self.run):
            raise ValueError("check must be callable")


# PM-2b registers the existing rules here.
REGISTRY: tuple[Check, ...] = ()
