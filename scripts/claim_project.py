#!/usr/bin/env python3
"""Merge only verified self-claims of unassigned projects after PR CI.

Trusted default-branch code; forked PR content is read as data, never executed.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

from contribution_api import plan_text, request as api, changed_files as files_in_pr
from project_contract import PLAN_FOLDER
from records import project_fields

LOGIN = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37})")


def verify_claim(before: str, after: str, actor: str, folder: str | None = None) -> str | None:
    """Validate a one-line self-claim in the plan's project record."""
    if not LOGIN.fullmatch(actor):
        raise ValueError("invalid author login")
    old_fields, new_fields = project_fields(before), project_fields(after)
    if old_fields["Status"] != "queued":
        raise ValueError("only queued projects may be claimed")
    if old_fields["Owner"] != "Unassigned":
        raise ValueError("project is not unassigned")
    if new_fields["Owner"] != "@" + actor:
        raise ValueError("claimed owner does not match authenticated PR author")
    if any(old_fields[key] != new_fields[key] for key in old_fields if key != "Owner"):
        raise ValueError("claim changed another project field")
    old_lines, new_lines = before.splitlines(keepends=True), after.splitlines(keepends=True)
    if len(old_lines) != len(new_lines):
        raise ValueError("plan line count changed")
    changes = [(a, b) for a, b in zip(old_lines, new_lines) if a != b]
    if len(changes) != 1:
        raise ValueError("only the owner line may change")
    old_raw, new_raw = changes[0]
    old_line, new_line = old_raw.rstrip("\r\n"), new_raw.rstrip("\r\n")
    if (old_line != "**Owner:** Unassigned" or new_line != "**Owner:** @" + actor
            or old_raw[len(old_line):] != new_raw[len(new_line):]):
        raise ValueError("only the owner line may change to the authenticated PR author")
    return folder




def verify_live_claim(base: str, proposed: str, live: str, actor: str,
                      folder: str | None = None) -> str | None:
    """An unrelated main edit must not block a valid claim.

    The candidate must be a one-cell self-claim relative to its PR base.
    For that project, current main must still have the exact original plan.
    GitHub's normal merge handles unrelated project changes.
    """
    verify_claim(base, proposed, actor, folder)
    if base != live:
        raise ValueError("claimed project's live plan changed; rebase or choose another project")
    project_fields(live)
    return folder

def open_pulls(repo: str):
    for page in range(1, 11):
        prs = api("GET", f"/repos/{repo}/pulls?state=open&per_page=100&page={page}")
        yield from prs
        if len(prs) < 100:
            return
    raise ValueError("claim scan exceeded bounded PR list")



def eligible(pr: dict, repo: str, sha: str, files: list[dict]) -> bool:
    user = pr.get("user") or {}
    head = pr.get("head") or {}
    base = pr.get("base") or {}
    return bool(
        pr.get("state") == "open" and not pr.get("draft")
        and head.get("sha") == sha and (head.get("repo") or {}).get("full_name")
        and base.get("ref") == "main"
        and (base.get("repo") or {}).get("full_name") == repo
        and user.get("type") == "User" and LOGIN.fullmatch(user.get("login", ""))
        and len(files) == 1 and files[0].get("status") == "modified"
        and files[0].get("additions") == 1 and files[0].get("deletions") == 1
        and re.fullmatch(r"plans/(" + PLAN_FOLDER.pattern + r")/plan\.md",
                         files[0].get("filename", "")) is not None
    )


def main_has_protection(repo: str) -> bool:
    """Fail closed until rules/branch protection are active on main."""
    return api("GET", f"/repos/{repo}/branches/main").get("protected") is True


def handle_run(repo: str, run: dict) -> list[str]:
    if run.get("event") != "pull_request" or run.get("conclusion") != "success":
        return []
    sha = run.get("head_sha", "")
    if not re.fullmatch(r"[0-9a-f]{40}", sha, re.I):
        return []
    # A privileged GitHub App must never merge on an unprotected default branch.
    # Maintainers must configure a review ruleset and restrict App bypass to PRs.
    if not main_has_protection(repo):
        raise ValueError("main is not protected; claim auto-merge stays disabled")
    merged = []
    for summary in open_pulls(repo):
        if (summary.get("head") or {}).get("sha") != sha:
            continue
        number = summary["number"]
        pr = api("GET", f"/repos/{repo}/pulls/{number}")
        changed = files_in_pr(repo, number)
        if not eligible(pr, repo, sha, changed):
            continue
        login = pr["user"]["login"]
        from_repo, from_ref = pr["head"]["repo"]["full_name"], pr["head"]["sha"]
        base_repo, base_ref = pr["base"]["repo"]["full_name"], pr["base"]["sha"]
        match = re.fullmatch(r"plans/(" + PLAN_FOLDER.pattern + r")/plan\.md",
                             changed[0].get("filename", ""))
        if not match:
            continue
        folder = match.group(1)
        candidate = plan_text(from_repo, from_ref, folder)
        original = plan_text(base_repo, base_ref, folder)
        if candidate is None or original is None:
            continue
        main_ref = api("GET", f"/repos/{repo}/git/ref/heads/main")["object"]["sha"]
        live = plan_text(repo, main_ref, folder)
        if live is None:
            continue
        project = verify_live_claim(original, candidate, live, login, folder)
        if api("GET", f"/repos/{repo}/git/ref/heads/main")["object"]["sha"] != main_ref:
            raise ValueError("main moved during claim validation; rebase the PR")
        fresh = api("GET", f"/repos/{repo}/pulls/{number}")
        if fresh["state"] != "open" or fresh["head"]["sha"] != sha:
            raise ValueError("claim changed during validation")
        api("PUT", f"/repos/{repo}/pulls/{number}/merge",
            {"sha": sha, "merge_method": "squash",
             "commit_title": f"claim(project): {project} by @{login}"})
        merged.append(project or folder)
        # A failed optional message must not undo a valid merge.
        try:
            api("POST", f"/repos/{repo}/issues/{number}/comments", {"body":
                f"Project **{folder}** is claimed by @{login}. "
                f"[Start from its plan](https://github.com/{repo}/blob/main/plans/{folder}/plan.md) "
                f"and [contribution guide](https://github.com/{repo}/blob/main/docs/contribution-workflow.md). "
                "Ownership does not imply scope acceptance, authorization to run, or permission to merge."})
        except Exception as exc:
            print(f"Claim merged, guidance comment failed: {exc}", file=sys.stderr)
    return merged


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", type=Path, required=True)
    args = parser.parse_args()
    event = json.loads(args.event.read_text()).get("workflow_run", {})
    try:
        merged = handle_run(os.environ["GITHUB_REPOSITORY"], event)
    except (ValueError, OSError, KeyError) as exc:
        print(f"Claim not auto-merged: {exc}", file=sys.stderr)
        return 1
    print("Auto-merged claims: " + ", ".join(merged) if merged else "No eligible owner-only claim")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
