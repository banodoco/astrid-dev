#!/usr/bin/env python3
"""Compare a release page's Branches table with GitHub, or list its branches and heads.

Hand-run by the release manager; it is not part of `astrid_dev.py check`.
Ancestry needs a clone (`--clone repository=path`, after a fetch) or GH_TOKEN;
without either, a row is "not verified", never passed or failed.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import urllib.error
from dataclasses import dataclass, field
from pathlib import Path

from contribution_api import request
from records import BRANCH_FIRST_RELEASE, BRANCH_REPOSITORIES, release_branch_errors, release_brief
from otto.markdown import section_by_heading as section, split_table_row

OWNER = "banodoco"
NOT_CUT = "not yet cut"


class NotVerified(Exception):
    """An ancestry question this run cannot answer: no clone or token, or a commit missing from the clone."""


@dataclass
class Report:
    rows: list[dict] = field(default_factory=list)
    flagged: list[str] = field(default_factory=list)
    unverified: list[str] = field(default_factory=list)


def repo_url(repo: str) -> str:
    return f"https://github.com/{OWNER}/{repo}"


def ls_remote(url: str, pattern: str) -> dict[str, str]:
    """Return {ref: sha} for the remote refs matching pattern."""
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
    result = subprocess.run(["git", "ls-remote", url, pattern], capture_output=True, text=True,
                            timeout=120, env=env)
    if result.returncode != 0:
        raise ValueError(f"could not read {url}: {result.stderr.strip() or 'git ls-remote failed'}")
    refs = {}
    for line in result.stdout.splitlines():
        sha, ref = line.split("\t", 1)
        refs[ref] = sha
    return refs


def release_rows(text: str, number: int) -> list[dict]:
    """The Branches rows, after the structure check records.py makes."""
    plans = [plan["number"] for plan in release_brief(text, strict=False)["plans"]]
    errors = release_branch_errors(text, str(number), plans)
    if errors:
        raise ValueError("Branches table is malformed: " + "; ".join(errors))
    lines = [line.strip() for line in section(text, "Branches").splitlines() if line.strip().startswith("|")]
    rows = []
    for line in lines[2:]:
        repo, branch_cell, role, cut, state = split_table_row(line)
        rows.append({"repo": repo, "branch": branch_cell.strip("`"), "role": role, "cut": cut, "state": state})
    return rows


def read_heads(rows: list[dict], remote) -> None:
    """Set row["head"] from one exact ls-remote per row; None means the branch is missing."""
    for row in rows:
        ref = f"refs/heads/{row['branch']}"
        row["head"] = remote(repo_url(row["repo"]), ref).get(ref)


def short(sha: str | None, empty: str = "missing") -> str:
    return sha[:8] if sha else empty


def clone_ancestor(path: Path, ancestor: str, descendant: str) -> bool:
    for sha in (ancestor, descendant):
        present = subprocess.run(["git", "-C", str(path), "cat-file", "-e", sha + "^{commit}"], capture_output=True)
        if present.returncode != 0:
            raise NotVerified(f"{sha[:8]} is not in the clone at {path}; fetch it first")
    done = subprocess.run(["git", "-C", str(path), "merge-base", "--is-ancestor", ancestor, descendant],
                          capture_output=True)
    if done.returncode not in (0, 1):
        raise NotVerified(f"git merge-base failed in {path}")
    return done.returncode == 0


def api_ancestor(api, repo: str, ancestor: str, descendant: str) -> bool:
    """GitHub's compare status: "ahead" or "identical" means the base is an ancestor of the head."""
    try:
        data = api("GET", f"/repos/{OWNER}/{repo}/compare/{ancestor}...{descendant}")
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            raise ValueError(f"{ancestor[:8]} or {descendant[:8]} is not a commit in {repo}") from exc
        raise NotVerified(f"GitHub compare failed for {repo}: HTTP {exc.code}") from exc
    status = data.get("status") if isinstance(data, dict) else None
    if status in ("ahead", "identical"):
        return True
    if status in ("behind", "diverged"):
        return False
    raise NotVerified(f"unexpected compare status {status!r} for {repo}")


def ancestor_check(clones: dict[str, Path], api):
    """Answer ancestry from a clone when one is given, else from the API, else not at all."""
    def check(repo: str, ancestor: str, descendant: str) -> bool:
        if repo in clones:
            return clone_ancestor(clones[repo], ancestor, descendant)
        if api is not None:
            return api_ancestor(api, repo, ancestor, descendant)
        raise NotVerified("no --clone for this repository and no GH_TOKEN")
    return check


def api_issue_exists(api):
    """An issue-existence oracle over the GitHub API; 404 is False, anything else unanswerable."""
    def exists(number: int) -> bool:
        try:
            api("GET", f"/repos/{OWNER}/astrid-dev/issues/{number}")
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return False
            raise NotVerified(f"GitHub issue lookup failed: HTTP {exc.code}") from exc
        return True
    return exists


def ancestry(report: Report, label: str, check, repo: str, inner: str, outer: str | None,
             what: str, wrong: str) -> None:
    """Record one ancestry claim: flagged when false, not verified when it cannot be answered."""
    if outer is None:
        report.unverified.append(f"{label}: {what} not checked, release main is missing")
        return
    try:
        if not check(repo, inner, outer):
            report.flagged.append(f"{label}: {wrong}")
    except NotVerified as exc:
        report.unverified.append(f"{label}: {what} not verified ({exc})")
    except ValueError as exc:
        report.flagged.append(f"{label}: {exc}")


def verify(text: str, number: int, remote=ls_remote, check=None, issue_exists=None) -> Report:
    """Check the table against the repositories. `remote` and `check` are injectable for tests."""
    rows = release_rows(text, number)
    read_heads(rows, remote)
    check = check or ancestor_check({}, None)
    report = Report(rows=rows)
    for row in rows:
        if row["role"].startswith("fix #"):
            label, issue = f"{row['repo']} {row['branch']}", int(row["role"][5:])
            try:
                if issue_exists is None:
                    raise NotVerified("no GH_TOKEN")
                if not issue_exists(issue):
                    report.flagged.append(f"{label}: issue #{issue} does not exist in {OWNER}/astrid-dev")
            except NotVerified as exc:
                report.unverified.append(f"{label}: issue #{issue} not verified ({exc})")
    heads = {(row["repo"], row["branch"]): row["head"] for row in rows}
    release_main = {row["repo"]: row["head"] for row in rows if row["role"] == "release"}
    for row in rows:
        label = f"{row['repo']} {row['branch']}"
        if row["head"] is None:
            report.flagged.append(f"{label}: branch is missing on GitHub")
            continue
        if row["state"] == "merged":
            ancestry(report, label, check, row["repo"], row["head"], release_main.get(row["repo"]),
                     "merged check", f"marked merged, but head {short(row['head'])} is not in "
                     f"release/{number}/main")
        if row["cut"] == NOT_CUT:
            report.unverified.append(f"{label}: Cut at is {NOT_CUT}")
        else:
            ancestry(report, label, check, row["repo"], row["cut"], row["head"], "Cut at check",
                     f"Cut at {short(row['cut'])} is not an ancestor of the branch head")
    for repo in BRANCH_REPOSITORIES:
        for ref in remote(repo_url(repo), f"refs/heads/release/{number}/*"):
            branch = ref.removeprefix("refs/heads/")
            if (repo, branch) not in heads:
                report.flagged.append(f"{repo} {branch}: exists on GitHub but is not in the Branches table")
    return report


def table(rows: list[dict]) -> str:
    cells = [["Repository", "Branch", "Role", "Cut at", "State", "Head"]]
    for row in rows:
        cut = row["cut"] if row["cut"] == NOT_CUT else short(row["cut"])
        cells.append([row["repo"], row["branch"], row["role"], cut, row["state"], short(row["head"])])
    widths = [max(len(line[i]) for line in cells) for i in range(len(cells[0]))]
    return "\n".join("  ".join(value.ljust(width) for value, width in zip(line, widths)).rstrip()
                     for line in cells)


def parse_clones(values: list[str]) -> dict[str, Path]:
    clones = {}
    for value in values:
        repo, _, path = value.partition("=")
        if repo not in BRANCH_REPOSITORIES or not path:
            raise ValueError(f"--clone must be REPOSITORY=PATH with REPOSITORY one of {', '.join(BRANCH_REPOSITORIES)}")
        clones[repo] = Path(path)
    return clones


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    check_cmd = commands.add_parser("check", help="compare the Branches table with GitHub")
    check_cmd.add_argument("number", type=int)
    check_cmd.add_argument("--clone", action="append", default=[], metavar="REPOSITORY=PATH",
                           help="a local clone for ancestry checks (repeatable)")
    list_cmd = commands.add_parser("list", help="print the release's branches and heads")
    list_cmd.add_argument("number", type=int)
    args = parser.parse_args(argv)
    try:
        if args.number < BRANCH_FIRST_RELEASE:
            raise ValueError(f"Release {args.number} has no Branches table; branches start with Release {BRANCH_FIRST_RELEASE}")
        path = Path(__file__).resolve().parent.parent / "releases" / f"{args.number}.md"
        text = path.read_text(encoding="utf-8")
        if args.command == "list":
            rows = release_rows(text, args.number)
            read_heads(rows, ls_remote)
            print(table(rows))
            return 0
        api = request if os.environ.get("GH_TOKEN") else None
        report = verify(text, args.number, check=ancestor_check(parse_clones(args.clone), api),
                        issue_exists=api_issue_exists(api) if api else None)
        print(table(report.rows))
        print()
        for line in report.flagged:
            print(f"FLAGGED: {line}")
        for line in report.unverified:
            print(f"not verified: {line}")
        print(f"\nChecked {len(report.rows)} rows: {len(report.flagged)} flagged, {len(report.unverified)} not verified.")
        return 1 if report.flagged else 0
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print(f"release branches: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
