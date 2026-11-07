#!/usr/bin/env python3
"""Merge only verified self-claims of unassigned projects after PR CI.

Trusted default-branch code; forked PR content is read as data, never executed.
"""
import argparse
import base64
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from check_docs import CATALOG, PLAN_LINK, catalog_rows

LOGIN = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37})")


def verify_claim(before: str, after: str, actor: str) -> str:
    """Return claimed folder only if exactly one owner cell changed to @actor."""
    if not LOGIN.fullmatch(actor):
        raise ValueError("invalid author login")
    old_lines, new_lines = before.splitlines(keepends=True), after.splitlines(keepends=True)
    if len(old_lines) != len(new_lines):
        raise ValueError("catalog line count changed")
    changes = [(a, b) for a, b in zip(old_lines, new_lines) if a != b]
    if len(changes) != 1:
        raise ValueError("only one owner cell may change")
    a, b = changes[0]
    old, new = a.rstrip("\r\n").split("|"), b.rstrip("\r\n").split("|")
    if len(old) != 9 or len(new) != 9 or any(old[i] != new[i] for i in range(9) if i != 4):
        raise ValueError("claim changed another column or non-project text")
    if old[4].strip() != "Unassigned":
        raise ValueError("project is not unassigned")
    expected = old[4].replace("Unassigned", "@" + actor)
    if new[4] != expected or a[len(a.rstrip("\r\n")):] != b[len(b.rstrip("\r\n")):]:
        raise ValueError("claimed owner does not match authenticated PR author")
    orig, changed = catalog_rows(before), catalog_rows(after)
    diffs = [(x, y) for x, y in zip(orig, changed) if x != y]
    if len(orig) != len(changed) or len(diffs) != 1:
        raise ValueError("claim must modify precisely one indexed project")
    row, updated = diffs[0]
    if row != [v.strip() for v in old[1:8]]:
        raise ValueError("edited row is not in the catalog")
    if row[3] != "Unassigned" or updated[3] != "@" + actor:
        raise ValueError("catalog owner mismatch")
    if any(row[i] != updated[i] for i in range(7) if i != 3):
        raise ValueError("other catalog cells changed")
    return PLAN_LINK.fullmatch(row[6]).group(1).split("/")[0]


def api(method: str, path: str, payload=None):
    root = os.environ.get("GITHUB_API_URL", "https://api.github.com").rstrip("/")
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        root + path, data=data, method=method,
        headers={"Authorization": "Bearer " + os.environ["GH_TOKEN"],
                 "Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28",
                 "User-Agent": "astrid-dev-claim-bot",
                 **({"Content-Type": "application/json"} if data is not None else {})})
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.loads(response.read())


def catalog(repository: str, ref: str) -> str:
    owner, name = repository.split("/", 1)
    query = urllib.parse.quote(ref, safe="")
    result = api("GET", f"/repos/{owner}/{name}/contents/{CATALOG}?ref={query}")
    if result.get("type") != "file" or result.get("encoding") != "base64":
        raise ValueError("expected a plain catalog file")
    return base64.b64decode(result["content"]).decode("utf-8")


def open_pulls(repo: str):
    for page in range(1, 11):
        prs = api("GET", f"/repos/{repo}/pulls?state=open&per_page=100&page={page}")
        yield from prs
        if len(prs) < 100:
            return
    raise ValueError("claim scan exceeded bounded PR list")


def files_in_pr(repo: str, number: int):
    files = []
    for page in range(1, 4):
        page_files = api("GET", f"/repos/{repo}/pulls/{number}/files?per_page=100&page={page}")
        files.extend(page_files)
        if len(page_files) < 100:
            return files
    raise ValueError("claim cannot contain hundreds of changed files")


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
        and len(files) == 1 and files[0].get("filename") == str(CATALOG)
        and files[0].get("status") == "modified"
    )


def handle_run(repo: str, run: dict) -> list[str]:
    if run.get("event") != "pull_request" or run.get("conclusion") != "success":
        return []
    sha = run.get("head_sha", "")
    if not re.fullmatch(r"[0-9a-f]{40}", sha, re.I):
        return []
    merged = []
    for summary in open_pulls(repo):
        if (summary.get("head") or {}).get("sha") != sha:
            continue
        number = summary["number"]
        pr = api("GET", f"/repos/{repo}/pulls/{number}")
        if not eligible(pr, repo, sha, files_in_pr(repo, number)):
            continue
        login = pr["user"]["login"]
        from_repo, from_ref = pr["head"]["repo"]["full_name"], pr["head"]["sha"]
        base_repo, base_ref = pr["base"]["repo"]["full_name"], pr["base"]["sha"]
        candidate = catalog(from_repo, from_ref)
        project = verify_claim(catalog(base_repo, base_ref), candidate, login)
        main_ref = api("GET", f"/repos/{repo}/git/ref/heads/main")["object"]["sha"]
        verify_claim(catalog(repo, main_ref), candidate, login)
        if api("GET", f"/repos/{repo}/git/ref/heads/main")["object"]["sha"] != main_ref:
            raise ValueError("main moved during claim validation; rebase the PR")
        fresh = api("GET", f"/repos/{repo}/pulls/{number}")
        if fresh["state"] != "open" or fresh["head"]["sha"] != sha:
            raise ValueError("claim changed during validation")
        api("PUT", f"/repos/{repo}/pulls/{number}/merge",
            {"sha": sha, "merge_method": "squash",
             "commit_title": f"claim(project): {project} by @{login}"})
        merged.append(project)
        # A failed optional message must not undo a valid merge.
        try:
            api("POST", f"/repos/{repo}/issues/{number}/comments", {"body":
                f"Project **{project}** is claimed by @{login}. "
                f"[Start from its plan](https://github.com/{repo}/blob/main/plans/{project}/plan.md) "
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
