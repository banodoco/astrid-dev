#!/usr/bin/env python3
"""Validate planning evidence carried with *new* or opted-in Astrid project packs.

Older project packs are grandfathered until they add a planning-evidence section.
Pending drafts are legitimate; accepted scopes must cite actual research, independent
challenge and an attributable owner decision. CI checks structure, not truth.
"""
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

from check_docs import ROOT

PLAN = re.compile(r"^plans/(\d{2}-[a-z0-9-]+)/(plan|inputs)\.md$")
SECTIONS = (
    "Prior art and behavior traced",
    "Reuse and placement decision",
    "Independent simplification challenge",
    "End-state options and owner choice",
    "Assumptions and evidence limits",
)
REF = re.compile(r"https?://[^\s)]+|(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])|\]\((?:\.\.?/)[^)]+\)", re.I)
DECISION = re.compile(r"^\*\*Scope decision:\*\*\s*(Pending|Accepted)\s*[—:-]\s*(.+)$", re.I | re.M)
PENDING = re.compile(r"^Pending\s*[—:-]\s*(.+)$", re.I | re.S)


def subsection(text: str, heading: str) -> str | None:
    match = re.search(r"^### " + re.escape(heading) + r"\s*$", text, re.M)
    if not match:
        return None
    tail = text[match.end():]
    end = re.search(r"^#{2,3}\s+\S", tail, re.M)
    return (tail[:end.start()] if end else tail).strip()


def planning_block(contents: str) -> str | None:
    match = re.search(r"^## Planning evidence\s*$", contents, re.M)
    if not match:
        return None
    tail = contents[match.end():]
    end = re.search(r"^## \S", tail, re.M)
    return (tail[:end.start()] if end else tail).strip()


def pending_issue(value: str, field: str) -> str | None:
    match = PENDING.match(value)
    if not match:
        return None
    details = match.group(1).strip()
    if len(details) < 45 or not re.search(r"\bNext:\s*\S", details, re.I):
        return f"{field}: pending research must explain the missing evidence and a concrete 'Next:' action"
    return ""


def validate_pack(project: str, contents: str) -> list[str]:
    errors = []
    block = planning_block(contents)
    if block is None:
        return [f"{project}: inputs.md needs a '## Planning evidence' section from the project template"]

    decision = DECISION.search(block)
    if not decision:
        errors.append(f"{project}: missing '**Scope decision:** Pending/Accepted — ...' in inputs.md")
        accepted = False
    else:
        state, reason = decision.groups()
        accepted = state.lower() == "accepted"
        if len(reason.strip()) < 45:
            errors.append(f"{project}: Scope decision must identify the decision or why it is pending")
        if accepted and not REF.search(reason):
            errors.append(f"{project}: accepted scope needs an attributable, linked or revision-pinned owner decision")
        if not accepted and (issue := pending_issue("Pending — " + reason, "Scope decision")):
            errors.append(f"{project}: {issue}")

    for heading in SECTIONS:
        value = subsection(block, heading)
        if value is None:
            errors.append(f"{project}: missing '### {heading}' planning evidence")
            continue
        is_pending = pending_issue(value, heading)
        if is_pending is not None:
            if is_pending:
                errors.append(f"{project}: {is_pending}")
            if accepted and heading != "Assumptions and evidence limits":
                errors.append(f"{project}: accepted scope cannot leave '{heading}' pending")
            continue
        if len(value.strip()) < 75:
            errors.append(f"{project}: '{heading}' needs substantive findings, not a placeholder")
        if accepted and heading in (
            "Prior art and behavior traced",
            "Independent simplification challenge",
            "End-state options and owner choice",
        ) and not REF.search(value):
            errors.append(f"{project}: accepted '{heading}' needs a traceable source/reference")
    return errors


def changed_projects(base: str, root: Path) -> set[str]:
    """Review new project folders and edits to opted-in planning evidence.

    Existing projects without a planning-evidence record are not retroactively
    forced through a new gate when receiving unrelated fixes.
    """
    present = subprocess.run(
        ["git", "cat-file", "-e", f"{base}^{{commit}}"],
        cwd=root, capture_output=True, text=True, check=False,
    )
    if present.returncode:
        raise ValueError(f"base revision {base!r} is not available")
    diff = subprocess.run(
        ["git", "diff", "--name-only", base, "HEAD", "--", "plans/"],
        cwd=root, capture_output=True, text=True, check=False,
    )
    if diff.returncode:
        raise ValueError(f"cannot read project diff: {diff.stderr.strip()}")
    selected = set()
    for path in diff.stdout.splitlines():
        match = PLAN.fullmatch(path)
        if not match:
            continue
        project, kind = match.groups()
        base_plan = subprocess.run(
            ["git", "cat-file", "-e", f"{base}:plans/{project}/plan.md"],
            cwd=root, capture_output=True, text=True, check=False,
        )
        new_plan = base_plan.returncode != 0
        inputs_path = root / f"plans/{project}/inputs.md"
        if not inputs_path.is_file():
            continue  # the existing structural validator reports missing files
        if new_plan:
            selected.add(project)
        elif kind == "inputs":
            old = subprocess.run(
                ["git", "show", f"{base}:plans/{project}/inputs.md"],
                cwd=root, capture_output=True, text=True, check=False,
            )
            if planning_block(inputs_path.read_text(encoding="utf-8")) is not None or (
                old.returncode == 0 and planning_block(old.stdout) is not None
            ):
                selected.add(project)
    return selected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="GitHub PR base SHA, fetched locally")
    args = parser.parse_args()
    try:
        projects = changed_projects(args.base, ROOT)
        issues = []
        for name in sorted(projects):
            path = ROOT / "plans" / name / "inputs.md"
            issues.extend(validate_pack(name, path.read_text(encoding="utf-8")))
    except (OSError, ValueError) as exc:
        print(f"ERROR project-planning evidence: {exc}")
        return 1
    for issue in issues:
        print(f"ERROR {issue}")
    if issues:
        print("Preserve prior art, planning decisions and honest pending steps in inputs.md; see astrid-dev-plan.")
        return 1
    print(f"Project planning evidence OK for {len(projects)} new/opted-in project pack(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
