#!/usr/bin/env python3
"""Route PRs to review without approving, merging or executing contributor code.

Uses trusted code in pull_request_target with only issues:write. The PR title,
body and file list are data; all authorization checks use the live main catalog.
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
from pathlib import Path

from check_docs import PLAN_LINK, catalog_rows
from contribution_api import catalog, changed_files, ensure_review_label, request
from project_contract import PLAN_FOLDER

LABEL = "needs-review"
PROJECT = re.compile(r"^Project:\s*strategy/projects/(" + PLAN_FOLDER.pattern + r")/plan\.md\s*$", re.I | re.M)
ROUTE = re.compile(r"^Review request:\s*(scope|implementation|completion)\s*$", re.I | re.M)
COMPLETION = re.compile(r"^#{2,3}\s+Completion assessment\s*[—:-]\s*Plan\s+(\d{2,})\s*$", re.I | re.M)


def parse_intent(body: str) -> tuple[str, str] | None:
    projects, routes = PROJECT.findall(body), ROUTE.findall(body)
    if not projects and not routes:
        return None
    if len(projects) != 1 or len(routes) != 1:
        raise ValueError("review PR must declare exactly one Project and Review request")
    return projects[0], routes[0].lower()


def classify(pr: dict, repo: str, main_catalog: str, files: list[dict]) -> str | None:
    """Determine a review queue lane, never an approval or scope acceptance."""
    intent = parse_intent(pr.get("body") or "")
    if intent is None:
        return None
    folder, route = intent
    user, base = pr.get("user") or {}, pr.get("base") or {}
    if (pr.get("state") != "open" or pr.get("draft") or
            base.get("ref") != "main" or
            (base.get("repo") or {}).get("full_name") != repo or
            user.get("type") != "User"):
        return None
    changes = {f.get("filename"): f.get("status") for f in files}
    found = [row for row in catalog_rows(main_catalog)
             if PLAN_LINK.fullmatch(row[6]).group(1) == folder + "/plan.md"]
    if route == "scope":
        if not found:
            necessary = {f"strategy/projects/{folder}/{filename}" for filename in ("plan.md", "inputs.md", "tasks.md")}
            if not all(changes.get(p) == "added" for p in necessary):
                return None
            if changes.get("strategy/projects/index.md") not in ("modified", "added"):
                return None
        elif f"strategy/projects/{folder}/plan.md" not in changes and "strategy/projects/index.md" not in changes:
            return None
        return "scope"
    if len(found) != 1 or found[0][3].casefold() != ("@" + user.get("login", "")).casefold():
        return None
    if route == "completion":
        if changes.get("strategy/projects/index.md") != "modified":
            return None
        if COMPLETION.findall(pr.get("body") or "") != [folder.split("-", 1)[0]]:
            return None
    return route


def route_event(event: dict, repo: str) -> str:
    number = (event.get("pull_request") or {}).get("number")
    if not isinstance(number, int):
        raise ValueError("no PR number")
    pr = request("GET", f"/repos/{repo}/pulls/{number}")
    main = request("GET", f"/repos/{repo}/git/ref/heads/main")["object"]["sha"]
    lane = classify(pr, repo, catalog(repo, main), changed_files(repo, number))
    labeled = LABEL in {label.get("name") for label in pr.get("labels", [])}
    if not lane:
        if labeled:
            # A changed PR body or lost ownership must not leave a stale
            # bot-managed review request in the queue.
            request("DELETE", f"/repos/{repo}/issues/{number}/labels/{LABEL}")
            return "Removed stale review-intake label; request no longer eligible"
        return "Not an eligible project review submission"
    if labeled:
        return f"Already queued for {lane} review"
    ensure_review_label(repo, LABEL)
    request("POST", f"/repos/{repo}/issues/{number}/labels", {"labels": [LABEL]})
    request("POST", f"/repos/{repo}/issues/{number}/comments", {"body":
        f"Accepted into the **{lane} review queue**, not approved for merge. "
        "A reviewer still examines the actual scope/code, exact candidate, model "
        "provenance, focused checks, negative cases and required integration authority. "
        f"See [the contribution guide](https://github.com/{repo}/blob/main/docs/contribution-workflow.md)."})
    return f"Queued PR #{number} for {lane} review"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", required=True, type=Path)
    args = parser.parse_args()
    try:
        event = json.loads(args.event.read_text(encoding="utf-8"))
        repo = os.environ["GITHUB_REPOSITORY"]
        if (event.get("repository") or {}).get("full_name") != repo:
            raise ValueError("event repository does not match trusted workflow")
        print(route_event(event, repo))
    except (ValueError, OSError, KeyError) as exc:
        print(f"Review intake failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
