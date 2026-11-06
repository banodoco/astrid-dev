#!/usr/bin/env python3
"""One decision gate: a PR moving a plan to done needs a reviewable completion assessment."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

from check_docs import CATALOG, PLAN_LINK, ROOT, catalog_rows, read

SECTION = re.compile(r"^#{2,3}\s+Completion assessment\s*[—:-]\s*Plan\s+(\d{2})\s*$", re.I | re.M)
GAP_LINK = re.compile(r"\]\(\.\./\.\./visions/gaps/([A-Z]{1,3}-\d{3})-[^)]+\.md\)")
GAP_LINE = re.compile(
    r"^Gap\s+([A-Z]{1,3}-\d{3}):\s*"
    r"(Closed|Partially evidenced|Unchanged|Needs recheck)\s*[—:-]\s*(.+)$", re.I | re.M,
)
EVIDENCE_REF = re.compile(r"https?://[^\s)]+|(?<![\da-f])[0-9a-f]{40}(?![\da-f])", re.I)


def plan_statuses(catalog: str) -> dict[str, str]:
    return {PLAN_LINK.fullmatch(row[6]).group(1): row[2] for row in catalog_rows(catalog)}


def transitions_to_done(before: str, after: str) -> list[str]:
    old, new = plan_statuses(before), plan_statuses(after)
    return sorted(path for path, status in new.items() if status == "done" and old.get(path) != "done")


def linked_gaps(plan_text: str) -> set[str]:
    lines = re.findall(r"^\*\*Vision gaps:\*\*\s*(.+)$", plan_text, re.M)
    if lines:
        return set(GAP_LINK.findall(lines[0]))
    if re.search(r"^\*\*Vision role:\*\*", plan_text, re.M):
        return set()
    raise ValueError("plan must declare Vision gaps or Vision role")


def assessment_section(body: str, plan_id: str) -> tuple[str | None, bool]:
    matches = list(SECTION.finditer(body))
    relevant = [i for i, match in enumerate(matches) if match.group(1) == plan_id]
    if len(relevant) != 1:
        return None, len(relevant) > 1
    i = relevant[0]
    # Stop before the next Markdown heading, not just the next completion receipt.
    start = matches[i].end()
    tail = body[start:]
    end = re.search(r"^#{1,3}\s+\S", tail, re.M)
    return tail[:end.start()] if end else tail, False


def assess_completion(plan_path: str, plan_text: str, body: str) -> list[str]:
    """Check the PR's *stated* judgment, not the truth of its evidence."""
    plan_id = Path(plan_path).parent.name.split("-", 1)[0]
    section, duplicates = assessment_section(body, plan_id)
    if duplicates:
        return [f"Plan {plan_id}: duplicate completion assessment sections"]
    if section is None:
        return [f"Plan {plan_id}: missing '## Completion assessment — Plan {plan_id}' in PR description"]

    issues = []
    evidence = re.search(r"^Evidence:\s*(.+)$", section, re.I | re.M)
    if not evidence or not EVIDENCE_REF.search(evidence.group(1)):
        issues.append(f"Plan {plan_id}: Evidence needs a concrete URL or full 40-character commit SHA")
    conclusion = re.search(r"^Completion:\s*(Yes|Met)\s*[—:-]\s*(.+)$", section, re.I | re.M)
    if not conclusion or len(conclusion.group(2).strip()) < 15:
        issues.append(f"Plan {plan_id}: Completion needs 'Yes —' and a specific reason")

    gaps = linked_gaps(plan_text)
    found: dict[str, str] = {}
    for match in GAP_LINE.finditer(section):
        gap, outcome, reason = match.groups()
        if gap in found:
            issues.append(f"Plan {plan_id}: duplicate assessment for {gap}")
        if len(reason.strip()) < 15:
            issues.append(f"Plan {plan_id}: {gap} needs an evidence-based explanation")
        found[gap] = outcome.lower()
    for gap in sorted(gaps - found.keys()):
        issues.append(f"Plan {plan_id}: missing gap disposition for {gap}")
    for gap in sorted(found.keys() - gaps):
        issues.append(f"Plan {plan_id}: {gap} is not linked from its plan")
    if not gaps and not re.search(r"^Gap impact:\s*None\s*[—:-]\s*.{15,}$", section, re.I | re.M):
        issues.append(f"Plan {plan_id}: enabler needs 'Gap impact: None — <reason>'")
    return issues


def catalog_at_revision(base: str, root: Path) -> str | None:
    """None means the catalog did not exist in the PR base (initial migration)."""
    def git(*args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=False)
    if git("cat-file", "-e", f"{base}^{{commit}}").returncode:
        raise ValueError(f"base revision {base!r} is not available; fetch the PR base")
    if git("cat-file", "-e", f"{base}:{CATALOG}").returncode:
        return None
    result = git("show", f"{base}:{CATALOG}")
    if result.returncode:
        raise ValueError(f"cannot read base catalog: {result.stderr.strip()}")
    return result.stdout


def check_pr(before: str | None, after: str, body: str, root: Path) -> list[str]:
    if before is None:
        print("SKIP completion transition gate: catalog did not exist in PR base")
        return []
    errors = []
    for path in transitions_to_done(before, after):
        plan_path = Path("plans") / path
        try:
            plan = read(root, plan_path)
            errors.extend(assess_completion(path, plan, body))
        except (OSError, ValueError) as exc:
            errors.append(f"{plan_path}: cannot assess completion: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="PR base commit SHA (or local base ref)")
    parser.add_argument("--event", type=Path, help="GitHub PR event JSON")
    parser.add_argument("--body-file", type=Path, help="PR description Markdown (local test)")
    args = parser.parse_args()
    try:
        before = catalog_at_revision(args.base, ROOT)
        if before is None:
            print("SKIP completion transition gate: initial catalog migration")
            return 0
        after = read(ROOT, CATALOG)
        changes = transitions_to_done(before, after)
        if not changes:
            print("No new plan completions; completion gate not required")
            return 0
        if args.body_file:
            body = args.body_file.read_text(encoding="utf-8")
        elif args.event:
            body = json.loads(args.event.read_text(encoding="utf-8")).get("pull_request", {}).get("body") or ""
        else:
            raise ValueError("completion requires --event or --body-file")
        issues = check_pr(before, after, body, ROOT)
    except (OSError, ValueError) as exc:
        print(f"ERROR completion gate: {exc}")
        return 1
    for issue in issues:
        print(f"ERROR {issue}")
    if issues:
        print("Add a completion assessment to the PR description; see AGENTS.md")
        return 1
    print(f"Completion gate passed for {len(changes)} plan(s): {', '.join(changes)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
