"""Bind Dev's skill package builder to the shared Otto implementation."""
from __future__ import annotations

import os  # Shared module object for the existing lock-setup crash injection.
from pathlib import Path

from agent_documents import AgentDocument, SKILL_CONFIG
from otto.skills import builder
from otto.skills.builder import (
    PublicationCommittedError,
    _LINK,
    _build_lock as _otto_build_lock,
    _build_output as _otto_build_output,
    _exchange_paths,
)


OUTPUT = SKILL_CONFIG.output
MARKER = SKILL_CONFIG.marker
REPO_LINK = SKILL_CONFIG.repo_link
_LOCK_CONTENT = SKILL_CONFIG.lock_content


def render_skill(doc: AgentDocument, root: Path) -> str:
    return builder.render_skill(doc, root, config=SKILL_CONFIG)


def expected_packages(root: Path) -> dict[str, tuple[str, str]]:
    return builder.expected_packages(root, SKILL_CONFIG)


def check_packages(root: Path) -> list[str]:
    return builder.check_packages(root, SKILL_CONFIG)


def build_packages(root: Path) -> list[str]:
    return builder.build_packages(root, SKILL_CONFIG)


# Bind the original Otto functions for existing direct test calls. Fault
# injection patches Otto's own globals; the direct calls still reach the
# unpatched implementations, as the original Dev tests require.
def _build_lock(parent: Path):
    return _otto_build_lock(parent, SKILL_CONFIG)


def _build_output(output: Path, expected: dict[str, tuple[str, str]]) -> list[str]:
    return _otto_build_output(output, expected, SKILL_CONFIG)
