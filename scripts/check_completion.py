"""One decision gate: a PR moving a plan to done needs a reviewable completion assessment."""
from __future__ import annotations

import re
from pathlib import Path

from check_docs import read
from project_contract import plan_gap_ids, project_number
from records import (PLAN_CELL, PLACEHOLDERS_COMPLETION, field_match, git_result, git_show,
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


def transitions_to_done(before: dict[str, str], after: dict[str, str]) -> list[str]:
    from lifecycle import requiring
    completion_statuses = requiring("completion-assessment")
    return sorted(f"{folder}/plan.md" for folder, status in after.items()
                  if status in completion_statuses and before.get(folder) != status)


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
            or (re.match(r"^None\s*[—:-]\s*\S", value, re.I) and has_real_reason(value[4:].lstrip(" —:-")))
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


def check_pr(changes: list[str], body: str, root: Path) -> list[str]:
    errors = []
    for path in changes:
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


def project_statuses(root: Path, revision: str | None = None) -> dict[str, str]:
    """Read plan field statuses; an unreadable revision asks for the PR base."""
    from records import projects
    if revision is not None:
        if git_result(root, "cat-file", "-e", f"{revision}^{{commit}}").returncode:
            raise ValueError(f"base revision {revision!r} is not available; fetch the PR base")
    if revision is not None:
        from project_contract import PLAN_FOLDER
        from records import git_output, project_fields
        statuses = {}
        for path in git_output(root, "ls-tree", "-r", "--name-only", revision, "plans/").splitlines():
            parts = Path(path).parts
            if len(parts) != 3 or parts[2] != "plan.md" or not PLAN_FOLDER.fullmatch(parts[1]):
                continue
            try:
                statuses[parts[1]] = project_fields(git_show(root, revision, path))["Status"]
            except ValueError:
                continue
        return statuses
    return {Path(PLAN_CELL.fullmatch(row[6]).group(1)).parent.name: row[2] for row in projects(root)}
