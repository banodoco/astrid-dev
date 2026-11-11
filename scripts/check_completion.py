#!/usr/bin/env python3
"""One decision gate: a PR moving a plan to done needs a reviewable completion assessment."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

from check_docs import CATALOG, PLAN_LINK, ROOT, catalog_rows, read
from project_contract import plan_gap_ids, project_number
from records import (PLACEHOLDERS_COMPLETION, field_match, git_result, git_show,
                     is_placeholder, matching_sections, section_after_match)

SECTION = re.compile(r"^#{2,3}\s+Completion assessment\s*[—:-]\s*Plan\s+(\d{2,})\s*$", re.I | re.M)
GAP_LINE = re.compile(
    r"^Gap\s+([A-Z]{1,3}-\d{3}):\s*"
    r"(Closed|Partially evidenced|Unchanged|Needs recheck)\s*[—:-]\s*(.+)$", re.I | re.M,
)
ROUTE_TOKEN = re.compile(r"(?<![\w/])[NXST](?![\w/])")
EVIDENCE_REF = re.compile(r"https?://[^\s)]+|(?<![\da-f])[0-9a-f]{40}(?![\da-f])", re.I)


def has_real_reason(value: str) -> bool:
    """Reject missing/placeholder decisions; review determines their quality."""
    return not is_placeholder(value, PLACEHOLDERS_COMPLETION)


def plan_statuses(catalog: str) -> dict[str, str]:
    return {PLAN_LINK.fullmatch(row[6]).group(1): row[2] for row in catalog_rows(catalog)}


def transitions_to_done(before: str, after: str) -> list[str]:
    old, new = plan_statuses(before), plan_statuses(after)
    return sorted(path for path, status in new.items() if status == "done" and old.get(path) != "done")


def linked_gaps(plan_text: str) -> set[str]:
    return set(plan_gap_ids(plan_text))


def assessment_section(body: str, plan_id: str) -> tuple[str | None, bool]:
    matches = matching_sections(body, SECTION)
    relevant = [i for i, match in enumerate(matches) if match.group(1) == plan_id]
    if len(relevant) != 1:
        return None, len(relevant) > 1
    i = relevant[0]
    # Stop before the next Markdown heading, not just the next completion receipt.
    return section_after_match(body, matches[i], boundary=r"^#{1,3}\s+\S", strip=False), False


def assess_completion(plan_path: str, plan_text: str, body: str) -> list[str]:
    """Check the PR's *stated* judgment, not the truth of its evidence."""
    plan_id = project_number(plan_path)
    section, duplicates = assessment_section(body, plan_id)
    if duplicates:
        return [f"Plan {plan_id}: duplicate completion assessment sections"]
    if section is None:
        return [f"Plan {plan_id}: missing '## Completion assessment — Plan {plan_id}' in PR description"]

    issues = []
    evidence = field_match(section, "Evidence", flags=re.I | re.M)
    if not evidence or not EVIDENCE_REF.search(evidence.group(1)):
        issues.append(f"Plan {plan_id}: Evidence needs a concrete URL or full 40-character commit SHA")
    conclusion = field_match(section, "Completion", value_pattern=r"(Yes|Met)\s*[—:-]\s*(.+)", flags=re.I | re.M)
    if not conclusion or not has_real_reason(conclusion.group(2)):
        issues.append(f"Plan {plan_id}: Completion needs 'Yes —' and a specific reason")

    # Final review summary is kept in this PR, not a parallel evidence-pack file.
    # CI checks references and explicit limits, not whether a linked test proves the claim.
    def has_reference_or_none(field: str) -> bool:
        hit = field_match(section, field, flags=re.I | re.M)
        if not hit:
            return False
        value = hit.group(1).strip()
        return bool(
            EVIDENCE_REF.search(value)
            or (re.match(r"^None\s*[—:-]\s*\S", value, re.I) and has_real_reason(value[4:]))
        )

    if not has_reference_or_none("Implementation PRs"):
        issues.append(f"Plan {plan_id}: Implementation PRs needs linked PRs or 'None — <reason>'")
    if not has_reference_or_none("Integrated candidate"):
        issues.append(f"Plan {plan_id}: Integrated candidate needs exact source links/SHAs or 'None — <reason>'")
    limitations = field_match(section, "Unproven", flags=re.I | re.M)
    if not limitations or not has_real_reason(limitations.group(1)):
        issues.append(f"Plan {plan_id}: Unproven must state remaining limits or 'None within stated scope'")

    routes = field_match(section, "Routes used", flags=re.I | re.M)
    if not routes:
        issues.append(f"Plan {plan_id}: Routes used must name the route (N, X, S or T) or explain why unknown")
    else:
        value = routes.group(1).strip()
        unknown = re.fullmatch(r"(?:Unknown|Not recorded)\s*[—:-]\s*(.+)", value, re.I)
        if unknown and not has_real_reason(unknown.group(1)):
            issues.append(f"Plan {plan_id}: missing reason for unknown route provenance")
        elif not unknown and not ROUTE_TOKEN.search(value) and not EVIDENCE_REF.search(value):
            issues.append(f"Plan {plan_id}: Routes used needs a route (N, X, S or T), "
                          "'Unknown — <reason>' or a linked evidence reference")

    gaps = linked_gaps(plan_text)
    found: dict[str, str] = {}
    for match in GAP_LINE.finditer(section):
        gap, outcome, reason = match.groups()
        if gap in found:
            issues.append(f"Plan {plan_id}: duplicate assessment for {gap}")
        if not has_real_reason(reason):
            issues.append(f"Plan {plan_id}: {gap} needs an evidence-based explanation")
        found[gap] = outcome.lower()
    for gap in sorted(gaps - found.keys()):
        issues.append(f"Plan {plan_id}: missing gap disposition for {gap}")
    for gap in sorted(found.keys() - gaps):
        issues.append(f"Plan {plan_id}: {gap} is not linked from its plan")
    if not gaps:
        impact = field_match(section, "Gap impact", value_pattern=r"None\s*[—:-]\s*(.+)", flags=re.I | re.M)
        if not impact or not has_real_reason(impact.group(1)):
            issues.append(f"Plan {plan_id}: enabler needs 'Gap impact: None — <reason>'")
    return issues


def catalog_at_revision(base: str, root: Path) -> str | None:
    """None means the catalog did not exist in the PR base (initial migration)."""
    def git(*args: str) -> subprocess.CompletedProcess[str]:
        return git_result(root, *args)
    if git("cat-file", "-e", f"{base}^{{commit}}").returncode:
        raise ValueError(f"base revision {base!r} is not available; fetch the PR base")
    if git("cat-file", "-e", f"{base}:{CATALOG}").returncode:
        return None
    try:
        return git_show(root, base, str(CATALOG))
    except ValueError as exc:
        raise ValueError(f"cannot read base catalog: {exc}") from exc


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


STRATEGY = "strategy.md"


def strategy_errors(changed_paths: set[str]) -> list[str]:
    """A completion must update strategy.md so the sequence stays current."""
    if STRATEGY in changed_paths:
        return []
    return [f"{STRATEGY}: a plan completion must update the strategy (its row, and focus or sequence if they changed)"]


def changed_paths(base: str, root: Path) -> set[str]:
    result = git_result(root, "diff", "--name-only", base, "HEAD")
    if result.returncode:
        raise ValueError(f"cannot list changed files: {result.stderr.strip()}")
    return set(result.stdout.split())


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
        issues.extend(strategy_errors(changed_paths(args.base, ROOT)))
    except (OSError, ValueError) as exc:
        print(f"ERROR completion gate: {exc}")
        return 1
    for issue in issues:
        print(f"ERROR {issue}")
    if issues:
        print("Add a completion assessment to the PR description; see skills/astrid-dev/SKILL.md")
        return 1
    print(f"Completion gate passed for {len(changes)} plan(s): {', '.join(changes)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
