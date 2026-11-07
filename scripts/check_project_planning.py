#!/usr/bin/env python3
"""Mechanically validate decision evidence in new or opted-in project packs.

A PR issue or small fix is NOT a project. Draft project evidence may be pending;
defined scope must show a traceable decision and useful source references.
Human reviewers judge quality, research completeness and proportional challenge.
"""
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

from check_docs import ROOT
from project_contract import PLAN_FOLDER

PLAN = re.compile(r"^strategy/projects/(" + PLAN_FOLDER.pattern + r")/(plan|inputs)\.md$")
LABELS = ("Scope decision", "Prior art", "Approach", "Challenge", "Proof and limits")
FIELD = re.compile(r"^\*\*(Scope decision|Prior art|Approach|Challenge|Proof and limits):\*\*\s*(.+)$", re.M)
REFERENCE = re.compile(
    r"https?://[^\s)]+|(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])|\]\((?:\.\.?/)[^)]+\)", re.I
)
PENDING = re.compile(r"^Pending\s*[—:-]\s*(.+)$", re.I)
ACCEPTED = re.compile(r"^Accepted\s*[—:-]\s*(.+)$", re.I)
CHALLENGE = re.compile(r"^(Reviewed|Not needed)\s*[—:-]\s*(.+)$", re.I)


def planning_block(text: str) -> str | None:
    match = re.search(r"^## Planning evidence\s*$", text, re.M)
    if not match:
        return None
    tail = text[match.end():]
    end = re.search(r"^## \S", tail, re.M)
    return (tail[:end.start()] if end else tail).strip()


def validate_pack(name: str, contents: str) -> list[str]:
    block = planning_block(contents)
    if block is None:
        return [f"{name}: missing '## Planning evidence' in inputs.md"]
    found: dict[str, str] = {}
    issues = []
    for match in FIELD.finditer(block):
        label, value = match.groups()
        if label in found:
            issues.append(f"{name}: duplicate field '{label}'")
        found[label] = value.strip()
    for label in LABELS:
        if label not in found:
            issues.append(f"{name}: missing '{label}' planning evidence")
    if issues:
        return issues

    state = found["Scope decision"]
    pending = PENDING.match(state)
    approved = ACCEPTED.match(state)
    if not (pending or approved):
        issues.append(f"{name}: Scope decision must be Pending or Accepted with a reason")
    if approved and not REFERENCE.search(approved.group(1)):
        issues.append(f"{name}: accepted scope needs a linked or pinned owner decision")
    if pending and not re.search(r"\bNext:\s*\S", pending.group(1), re.I):
        issues.append(f"{name}: pending scope decision needs a next action")

    for label in LABELS[1:]:
        value = found[label]
        placeholder = PENDING.match(value)
        if placeholder:
            if not re.search(r"\bNext:\s*\S", placeholder.group(1), re.I):
                issues.append(f"{name}: pending '{label}' needs a next action")
            if approved:
                issues.append(f"{name}: accepted scope cannot leave '{label}' pending")
        elif value.lower().strip(" .") in {"tbd", "todo", "n/a", "none", "unknown"}:
            issues.append(f"{name}: '{label}' needs a meaningful statement or an explicit pending action")

    if approved:
        if not REFERENCE.search(found["Prior art"]):
            issues.append(f"{name}: accepted Prior art needs a source reference or documented search")
        challenge = CHALLENGE.match(found["Challenge"])
        if not challenge:
            issues.append(f"{name}: Challenge must be 'Reviewed — <source>' or 'Not needed — <reason>'")
        elif challenge.group(1).lower() == "reviewed" and not REFERENCE.search(challenge.group(2)):
            issues.append(f"{name}: Reviewed challenge needs a source reference")
    return issues


def changed_projects(base: str, root: Path) -> set[str]:
    """Check new packs, and older packs that opted in; issues are never included."""
    def git(*args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=False)

    if git("cat-file", "-e", f"{base}^{{commit}}").returncode:
        raise ValueError(f"base revision {base!r} is unavailable")
    changed = git("diff", "--name-only", base, "HEAD", "--", "strategy/projects/")
    if changed.returncode:
        raise ValueError(f"can't compare project changes: {changed.stderr.strip()}")
    selected = set()
    for name in set(path for path in changed.stdout.splitlines() if PLAN.fullmatch(path)):
        match = PLAN.fullmatch(name)
        project = match.group(1)
        path = root / "strategy/projects" / project / "inputs.md"
        if not path.exists():
            continue  # check_docs.py reports missing project files
        previous_plan = git("cat-file", "-e", f"{base}:strategy/projects/{project}/plan.md")
        previous_inputs = git("show", f"{base}:strategy/projects/{project}/inputs.md")
        # A pure migration of existing project folders must not retroactively
        # require the new planning template. Truly new projects still do.
        if previous_plan.returncode != 0:
            legacy = git("cat-file", "-e", f"{base}:plans/{project}/plan.md")
            if legacy.returncode == 0:
                previous_plan = legacy
                previous_inputs = git("show", f"{base}:plans/{project}/inputs.md")
        opted_in = planning_block(path.read_text(encoding="utf-8")) is not None or (
            previous_inputs.returncode == 0 and planning_block(previous_inputs.stdout) is not None
        )
        if previous_plan.returncode != 0 or opted_in:
            selected.add(project)
    return selected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="Fetched PR base commit SHA")
    args = parser.parse_args()
    try:
        names = changed_projects(args.base, ROOT)
        errors = []
        for name in sorted(names):
            errors.extend(validate_pack(name, (ROOT / "plans" / name / "inputs.md").read_text(encoding="utf-8")))
    except (ValueError, OSError) as exc:
        print(f"ERROR project evidence: {exc}")
        return 1
    for error in errors:
        print(f"ERROR {error}")
    if errors:
        print("Fix the project decision record in inputs.md; see the Astrid project template.")
        return 1
    print(f"Project evidence OK for {len(names)} new or opted-in project(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
