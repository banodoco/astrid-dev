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

GAP_PATH = re.compile(r"^strategy/vision/gaps/([A-Z]{1,3}-\d{3})-[a-z0-9-]+\.md$")
SECTION = re.compile(
    r"^#{2,3}\s+Gap boundary assessment\s*[—:-]\s*([A-Z]{1,3}-\d{3})\s*$",
    re.I | re.M,
)
LINK = re.compile(r"https?://[^\s)]+|(?<![\da-f])[0-9a-f]{40}(?![\da-f])", re.I)
ALTERNATIVE = re.compile(r"\b(?:[A-Z]{1,3}-\d{3}|Plan\s+\d{2}|project|none)\b", re.I)


def section(text: str, title: str) -> str:
    match = re.search(r"^## " + re.escape(title) + r"\s*$", text, re.M)
    if not match:
        return ""
    tail = text[match.end():]
    end = re.search(r"^## ", tail, re.M)
    return (tail[:end.start()] if end else tail).strip()


def boundary_signature(text: str) -> tuple[str, ...]:
    """Only semantic outcome boundaries trigger a new rationale.

    Updating assessment, current evidence or citations without redefining
    the outcome does not require a second architecture review.
    """
    title = re.search(r"^# (.+)$", text, re.M)
    applies = re.search(r"^\*\*Applies to:\*\*(.+)$", text, re.M)
    return (
        title.group(1).strip() if title else "",
        applies.group(1).split("**Assessment:**", 1)[0].strip() if applies else "",
        section(text, "Desired state"),
        section(text, "Gap"),
        section(text, "Closure evidence"),
    )


def needs_boundary_review(before: str | None, after: str | None) -> bool:
    return before is None or after is None or boundary_signature(before) != boundary_signature(after)


def git(root: Path, *args: str, must_succeed: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=False)
    if must_succeed and result.returncode:
        raise ValueError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result


def before_file(root: Path, base: str, path: str) -> str | None:
    result = git(root, "show", f"{base}:{path}", must_succeed=False)
    if result.returncode:
        return None
    return result.stdout


def after_file(root: Path, path: str) -> str | None:
    file = root / path
    return file.read_text(encoding="utf-8") if file.is_file() else None


def migration_signature(text: str) -> tuple[str, ...]:
    """Normalize only link-root moves, never wording or closure criteria."""
    return tuple(
        value.replace("../../projects/", "../../plans/")
             .replace("../projects/", "../plans/")
             .replace("strategy/projects/", "plans/")
        for value in boundary_signature(text)
    )


def affected_gaps(base: str, root: Path) -> set[str]:
    """Determine newly created, deleted and materially redefined gaps in the PR."""
    git(root, "cat-file", "-e", f"{base}^{{commit}}")
    changed = git(root, "diff", "--name-status", "--find-renames", base, "HEAD", "--", "strategy/vision/gaps")
    required: set[str] = set()
    for line in changed.stdout.splitlines():
        cells = line.split("\t")
        if len(cells) < 2:
            raise ValueError(f"unexpected git diff name-status row: {line}")
        change = cells[0]
        paths = cells[1:]
        # Renaming a gap or changing its stable identity is always a review event.
        if change.startswith(("R", "C")):
            for path in paths:
                match = GAP_PATH.fullmatch(path)
                if match:
                    required.add(match.group(1))
            continue
        for path in paths:
            match = GAP_PATH.fullmatch(path)
            if not match:
                continue
            old = before_file(root, base, path)
            new = after_file(root, path)
            if old is None and new is not None:
                legacy_path = path.replace("strategy/vision/gaps/", "visions/gaps/", 1)
                legacy = before_file(root, base, legacy_path)
                if legacy is not None and migration_signature(legacy) == migration_signature(new):
                    continue
            if needs_boundary_review(old, new):
                required.add(match.group(1))
    return required


def has_real_reason(value: str) -> bool:
    """Mechanical placeholder check only; reviewers judge substantive reasoning."""
    normalized = value.strip().lower().strip(" .-")
    return bool(normalized) and normalized not in {"tbd", "todo", "n/a", "none", "unknown", "pending", "because"}


def assess_boundary(
    gap_id: str,
    body: str,
    expected: tuple[list[str], str] | None = None,
) -> list[str]:
    matches = list(SECTION.finditer(body))
    selected = [i for i, match in enumerate(matches) if match.group(1).upper() == gap_id]
    if len(selected) != 1:
        if not selected:
            return [f"{gap_id}: missing '## Gap boundary assessment — {gap_id}' in PR description"]
        return [f"{gap_id}: duplicate gap boundary assessment sections"]
    start = matches[selected[0]].end()
    tail = body[start:]
    next_heading = re.search(r"^#{1,6}\s+\S", tail, re.M)
    text = (tail[:next_heading.start()] if next_heading else tail).strip()
    issues = []
    decision = re.search(r"^Decision:\s*(New|Refine|Merge|Retire)\s*[—:-]\s*(.+)$", text, re.I | re.M)
    if not decision or not has_real_reason(decision.group(2)):
        issues.append(f"{gap_id}: Decision needs New/Refine/Merge/Retire and a specific rationale")
    for field in ("Outcome", "Existing alternatives", "Why this level", "Independent closure"):
        match = re.search(r"^" + re.escape(field) + r":\s*(.+)$", text, re.I | re.M)
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
        match = re.search(
            r"^" + re.escape(field)
            + r":\s*(None|(?:(?:pillar|principle):[a-z0-9-]+"
              r"(?:,\s*(?:pillar|principle):[a-z0-9-]+)*))"
              r"\s+[—:-]\s*(.+)$",
            text, re.I | re.M,
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
    evidence = re.search(r"^Evidence:\s*(.+)$", text, re.I | re.M)
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="PR base commit SHA or fetched base ref")
    parser.add_argument("--event", type=Path, help="GitHub pull request event JSON")
    parser.add_argument("--body-file", type=Path, help="Local PR description")
    args = parser.parse_args()
    try:
        required = affected_gaps(args.base, ROOT)
        if not required:
            print("No new or materially redefined gaps; boundary review not required")
            return 0
        if args.body_file:
            body = args.body_file.read_text(encoding="utf-8")
        elif args.event:
            body = json.loads(args.event.read_text(encoding="utf-8")).get("pull_request", {}).get("body") or ""
        else:
            raise ValueError("gap boundary changes require --event or --body-file")
        expected_by_gap = {}
        for gap_id in sorted(required):
            paths = list((ROOT / "strategy/vision/gaps").glob(gap_id + "-*.md"))
            if len(paths) > 1:
                raise ValueError(f"{gap_id}: duplicate gap files")
            if paths:
                metadata = next((line for line in paths[0].read_text(encoding="utf-8").splitlines()
                                 if line.startswith("**Applies to:**")), "")
                expected_by_gap[gap_id] = parse_gap_relationships(metadata)
            else:
                expected_by_gap[gap_id] = None  # a retired gap has no current source mapping
        issues = check_pr(required, body, expected_by_gap)
    except (OSError, ValueError) as exc:
        print(f"ERROR gap boundary gate: {exc}")
        return 1
    for issue in issues:
        print(f"ERROR {issue}")
    if issues:
        print("Add a first-principles gap boundary assessment to the PR description; see strategy/vision/gaps.md")
        return 1
    print(f"Gap boundary gate passed for {len(required)} gap(s): {', '.join(sorted(required))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
