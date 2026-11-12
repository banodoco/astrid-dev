#!/usr/bin/env python3
"""Require a first-principles PR decision when a gap is added, retired, or redefined.

CI verifies that reasoning is supplied and refers to a concrete source.
A human reviewer must judge whether the reasoning and evidence are good.
Ordinary current-state/assessment/source refreshes don't redefine a gap.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

from check_docs import ROOT
from gap_relationships import parse_gap_relationships
from records import (PLACEHOLDERS_GAP, field_match, git_result, git_show,
                     is_placeholder, matching_sections, read_text,
                     section as record_section, section_after_match)

GAP_PATH = re.compile(r"^(?:visions|vision)/gaps/([A-Z]{1,3}-\d{3})-[a-z0-9-]+\.md$")
SECTION = re.compile(
    r"^#{2,3}\s+Gap boundary assessment\s*[—:-]\s*([A-Z]{1,3}-\d{3})\s*$",
    re.I | re.M,
)
LINK = re.compile(r"https?://[^\s)]+|(?<![\da-f])[0-9a-f]{40}(?![\da-f])", re.I)
ALTERNATIVE = re.compile(r"\b(?:[A-Z]{1,3}-\d{3}|Plan\s+\d{2}|project|none)\b", re.I)


def section(text: str, title: str) -> str:
    return record_section(text, title, missing="empty", boundary=r"^## ", strip=True) or ""


def boundary_signature(text: str) -> tuple[str, ...]:
    """Only semantic outcome boundaries trigger a new rationale.

    Updating assessment, current evidence or citations without redefining
    the outcome does not require a second architecture review.
    """
    title = re.search(r"^# (.+)$", text, re.M)
    applies = re.search(r"^\*\*Applies to:\*\*[ \t]*(.*)$", text, re.M)
    return (
        title.group(1).strip() if title else "",
        re.sub(r"\.\./principles\.md#([a-z0-9-]+)", r"../principles/\1.md", applies.group(1).split("**Assessment:**", 1)[0].strip()) if applies else "",
        section(text, "Desired state"),
        section(text, "Gap"),
        section(text, "Closure evidence"),
    )


def needs_boundary_review(before: str | None, after: str | None) -> bool:
    return before is None or after is None or boundary_signature(before) != boundary_signature(after)


def git(root: Path, *args: str, must_succeed: bool = True) -> subprocess.CompletedProcess[str]:
    result = git_result(root, *args)
    if must_succeed and result.returncode:
        raise ValueError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result


def before_file(root: Path, base: str, path: str) -> str | None:
    return git_show(root, base, path, missing="none")


def after_file(root: Path, path: str) -> str | None:
    file = root / path
    return read_text(root, Path(path)) if file.is_file() else None


def affected_gaps(base: str, root: Path) -> set[str]:
    """Compare stable gap outcomes, not file moves or representation-only links.

    Moving the vision folder or splitting principle pages must not demand 15
    fresh philosophical approval receipts when the underlying outcomes have
    not changed. A real title, relationship, outcome or closure change still
    requires one boundary review per affected ID.
    """
    git(root, "cat-file", "-e", f"{base}^{{commit}}")
    listing = git(root, "ls-tree", "-r", "--name-only", base, "--", "visions/gaps", "vision/gaps")
    old_paths: dict[str, str] = {}
    for path in listing.stdout.splitlines():
        match = GAP_PATH.fullmatch(path)
        if match:
            gap_id = match.group(1)
            if gap_id in old_paths:
                raise ValueError(f"duplicate historical gap ID: {gap_id}")
            old_paths[gap_id] = path

    new_paths: dict[str, str] = {}
    for file in sorted((root / "vision/gaps").glob("*.md")):
        path = file.relative_to(root).as_posix()
        match = GAP_PATH.fullmatch(path)
        if match:
            gap_id = match.group(1)
            if gap_id in new_paths:
                raise ValueError(f"duplicate gap ID: {gap_id}")
            new_paths[gap_id] = path

    required: set[str] = set()
    for gap_id in old_paths.keys() | new_paths.keys():
        old_path, new_path = old_paths.get(gap_id), new_paths.get(gap_id)
        if old_path is None or new_path is None:
            required.add(gap_id)
            continue
        if Path(old_path).name != Path(new_path).name:
            required.add(gap_id)
            continue
        if needs_boundary_review(before_file(root, base, old_path), after_file(root, new_path)):
            required.add(gap_id)
    return required


def has_real_reason(value: str) -> bool:
    """Mechanical placeholder check only; reviewers judge substantive reasoning."""
    return not is_placeholder(value, PLACEHOLDERS_GAP)


def assess_boundary(
    gap_id: str,
    body: str,
    expected: tuple[list[str], str] | None = None,
) -> list[str]:
    matches = matching_sections(body, SECTION)
    selected = [i for i, match in enumerate(matches) if match.group(1).upper() == gap_id]
    if len(selected) != 1:
        if not selected:
            return [f"{gap_id}: missing '## Gap boundary assessment — {gap_id}' in PR description"]
        return [f"{gap_id}: duplicate gap boundary assessment sections"]
    text = section_after_match(body, matches[selected[0]], boundary=r"^#{1,6}\s+\S", strip=True)
    issues = []
    decision = field_match(text, "Decision", value_pattern=r"(New|Refine|Merge|Retire)\s*[—:-]\s*(.+)", flags=re.I | re.M)
    if not decision or not has_real_reason(decision.group(2)):
        issues.append(f"{gap_id}: Decision needs New/Refine/Merge/Retire and a specific rationale")
    for field in ("Outcome", "Existing alternatives", "Why this level", "Independent closure"):
        match = field_match(text, field, flags=re.I | re.M)
        value = match.group(1).strip() if match else ""
        if not has_real_reason(value):
            issues.append(f"{gap_id}: {field} needs explicit first-principles reasoning")
        if field == "Existing alternatives" and value and not ALTERNATIVE.search(value):
            issues.append(f"{gap_id}: Existing alternatives must examine a concrete gap, plan or project (or explain none)")
    # A rationale must identify the actual chosen vision connection and
    # explicitly defend any secondary ones. When a gap still exists, compare
    # the PR prose against its source metadata rather than only checking prose.
    relationships = {}
    for field in ("Primary connection", "Supporting connections"):
        match = field_match(
            text, field, value_pattern=r"(None|(?:(?:pillar|principle):[a-z0-9-]+"
              r"(?:,\s*(?:pillar|principle):[a-z0-9-]+)*))"
              r"\s+[—:-]\s*(.+)", flags=re.I | re.M,
        )
        if not match or not has_real_reason(match.group(2)):
            issues.append(f"{gap_id}: {field} needs explicit links and substantive justification")
            continue
        refs = [] if match.group(1) == "None" else [x.strip() for x in match.group(1).split(",")]
        if field == "Primary connection" and len(refs) != 1 and (expected is not None or refs):
            issues.append(f"{gap_id}: Primary connection must contain exactly one vision ref")
        if field == "Supporting connections" and len(refs) != len(set(refs)):
            issues.append(f"{gap_id}: duplicate supporting connection")
        relationships[field] = refs
    if expected is not None:
        all_links, chosen_primary = expected
        if relationships.get("Primary connection") != [chosen_primary]:
            issues.append(f"{gap_id}: Primary connection differs from gap metadata ({chosen_primary})")
        if set(relationships.get("Supporting connections", [])) != set(all_links) - {chosen_primary}:
            issues.append(f"{gap_id}: Supporting connections differ from gap metadata")
    evidence = field_match(text, "Evidence", flags=re.I | re.M)
    if not evidence or not LINK.search(evidence.group(1)):
        issues.append(f"{gap_id}: Evidence needs a concrete URL or full 40-character source SHA")
    return issues


def check_pr(
    required: set[str],
    body: str,
    expected_by_gap: dict[str, tuple[list[str], str] | None] | None = None,
) -> list[str]:
    issues = []
    for gap_id in sorted(required):
        expected = expected_by_gap.get(gap_id) if expected_by_gap else None
        issues.extend(assess_boundary(gap_id, body, expected=expected))
    return issues


def main() -> int:
    from checks import boundary_main
    return boundary_main()


if __name__ == "__main__":
    raise SystemExit(main())
