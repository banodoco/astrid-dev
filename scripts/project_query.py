"""Read-only project selection over canonical Dev records (no additional store).

Keep the optional strategy target separate from actual release membership.
The project reader, lifecycle vocabulary and release grouping remain owners;
this is the Dev query/projection adapter, not an additional record format.
"""
from __future__ import annotations

import json
from pathlib import Path

import lifecycle
from records import (PLACEHOLDERS_ACTIVE_OWNER, project_target_milestone,
                     projects, release_brief, strategy_milestones)


def _version_key(value):
    return tuple(int(part) for part in value.split("."))


def load_projects(root: Path, *, briefs=None):
    from views import release_membership
    root = Path(root)
    if briefs is None:
        briefs = [release_brief(path.read_text(encoding="utf-8"))
                  for path in sorted((root / "releases").glob("[0-9]*.md")) if path.stem.isdigit()]
    membership = {}
    for milestone, group in release_membership(briefs).items():
        for brief in group:
            for plan in brief["plans"]:
                membership.setdefault(plan["folder"], []).append({
                    "number": int(brief["number"]), "state": brief["state"], "milestone": milestone,
                })
    strategy_path = root / "strategy.md"
    allowed = strategy_milestones(strategy_path.read_text(encoding="utf-8")) if strategy_path.is_file() else ()
    result = []
    for name, goal, status, owner, estimate, waiting, link in projects(root):
        folder = link.rsplit("(", 1)[1].removesuffix("/plan.md)")
        path = root / "plans" / folder / "plan.md"
        explicit = project_target_milestone(path.read_text(encoding="utf-8"))
        if explicit is not None and explicit not in allowed:
            raise ValueError(f"plans/{folder}/plan.md: Target milestone {explicit} has no authored strategy milestone")
        allocations = sorted(membership.get(folder, []), key=lambda row: row["number"])
        drafts = [row for row in allocations if row["state"] == "Draft"]
        # Open work may span several briefs. The latest draft is its
        # outstanding delivery horizon; finalized membership is history.
        inferred = drafts[-1]["milestone"] if drafts and status not in lifecycle.terminal() else None
        target = explicit or inferred
        late = bool(explicit and any(_version_key(row["milestone"]) > _version_key(explicit) for row in drafts))
        result.append({
            "id": int(folder.split("-", 1)[0]), "folder": folder, "project": name,
            "goal": goal, "status": status, "owner": owner, "estimate": estimate,
            "waiting_on": waiting, "target_milestone": target, "explicit_target": explicit,
            "target_source": "explicit" if explicit else "release" if inferred else None,
            "releases": allocations, "draft_releases": [row["number"] for row in drafts],
            "late_allocation": late,
        })
    return result


def filter_projects(rows, *, pending=False, statuses=(), milestone=None, owner=None,
                    unallocated=False, release=None, search=None, late=False):
    """All selected predicates are intersected; order remains catalog priority."""
    def matches(row):
        if pending and row["status"] in lifecycle.terminal():
            return False
        if statuses and row["status"] not in statuses:
            return False
        if milestone is not None and row["target_milestone"] != (None if milestone == "unassigned" else milestone):
            return False
        if owner is not None:
            actual = row["owner"].strip().casefold()
            wanted = owner.strip().casefold()
            if wanted == "unassigned":
                if actual not in PLACEHOLDERS_ACTIVE_OWNER:
                    return False
            elif wanted == "assigned":
                if actual in PLACEHOLDERS_ACTIVE_OWNER:
                    return False
            elif actual != wanted:
                return False
        if unallocated and row["draft_releases"]:
            return False
        if release is not None and not any(item["number"] == release for item in row["releases"]):
            return False
        if late and not row["late_allocation"]:
            return False
        if search is not None and search.casefold() not in (
            f"{row['id']} {row['folder']} {row['project']} {row['goal']}".casefold()
        ):
            return False
        return True
    return [row for row in rows if matches(row)]


def add_arguments(parser):
    parser.add_argument("--pending", action="store_true", help="All nonterminal project statuses")
    parser.add_argument("--status", choices=lifecycle.names(), action="append", default=[], help="Repeat to select several statuses")
    parser.add_argument("--target-milestone", "--milestone", dest="milestone", help="Effective target, e.g. 0.5; use unassigned for no target")
    parser.add_argument("--owner", help="Exact accountable owner, or assigned/unassigned")
    parser.add_argument("--unallocated", action="store_true", help="Not included in any Draft release")
    parser.add_argument("--release", type=int, help="Included in a specific draft or final numbered release")
    parser.add_argument("--search", help="Case-insensitive project ID, name or goal substring")
    parser.add_argument("--late", action="store_true", help="Explicit target has a later draft allocation")
    parser.add_argument("--json", action="store_true", help="Emit full structured project records")


def run(root, args):
    if args.milestone not in (None, "unassigned"):
        strategy = (root / "strategy.md").read_text(encoding="utf-8")
        if args.milestone not in strategy_milestones(strategy):
            raise ValueError(f"Unknown target milestone {args.milestone!r}")
    rows = filter_projects(load_projects(root), pending=args.pending, statuses=args.status,
                           milestone=args.milestone, owner=args.owner, unallocated=args.unallocated,
                           release=args.release, search=args.search, late=args.late)
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0
    print("| Plan | Project | Status | Owner | Target | Releases |")
    print("| --- | --- | --- | --- | --- | --- |")
    for row in rows:
        target = row["target_milestone"] or "—"
        if row["target_source"] == "release":
            target += " (from release)"
        if row["late_allocation"]:
            target += " (review: later allocation)"
        releases = ", ".join(f"{r['number']} ({r['state']})" for r in row["releases"]) or "—"
        print(f"| [{row['id']}](plans/{row['folder']}/plan.md) | {row['project']} | {row['status']} | {row['owner']} | {target} | {releases} |")
    print(f"\n{len(rows)} projects")
    return 0
