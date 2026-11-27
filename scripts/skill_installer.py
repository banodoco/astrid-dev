"""Bind Dev's generated skill installer to the shared Otto implementation."""
from __future__ import annotations

# The existing fault-injection targets refer to these shared module objects.
import os
import tempfile
from pathlib import Path

from agent_documents import SKILL_CONFIG
from otto.skills import installer
from otto.skills.installer import (
    CommittedRetargetCleanupError,
    PartialInstallationError,
    default_destinations,
)


def install_packages(root: Path, destinations: list[Path] | None = None,
                     *, dry_run: bool = False) -> list[str]:
    return installer.install_packages(root, SKILL_CONFIG, destinations, dry_run=dry_run)
