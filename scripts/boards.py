#!/usr/bin/env python3
"""Read-only view of who is where on a release's coordination boards."""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
from datetime import datetime, timezone

from contribution_api import request

REPO = "banodoco/astrid-dev"
QUIET_HOURS, STALE_HOURS = 2, 24
ROW = re.compile(r"^\|[^|]*\|\s*`([^`<>]+)`\s*\|(.*)\|\s*$")
SESSION = re.compile(r"session_[A-Za-z0-9]+")
FROM = re.compile(r"^from_session:\s*(\S+)", re.M)
ANNOUNCE = re.compile(r"^session:\s*(session_[A-Za-z0-9]+)", re.M)


def api(path: str):
    """GET a REST path, with GH_TOKEN if set, else the gh CLI."""
    if os.environ.get("GH_TOKEN") or not shutil.which("gh"):
        return request("GET", path)
    return json.loads(subprocess.run(["gh", "api", path], check=True, capture_output=True, text=True).stdout)


def find_boards(release: str) -> list[dict]:
    q = urllib.parse.quote(f'repo:{REPO} is:issue is:open in:title "board: release {release}"', safe=":")
    found = api(f"/search/issues?q={q}&per_page=100")["items"]
    pat = re.compile(rf"^board: release {re.escape(release)}( .+)?$")
    return sorted((i for i in found if pat.match(i["title"])), key=lambda i: i["number"])


def comments(number: int) -> list[dict]:
    out, page = [], 1
    while True:
        chunk = api(f"/repos/{REPO}/issues/{number}/comments?per_page=100&page={page}")
        out += chunk
        if len(chunk) < 100:
            return out
        page += 1


def parse_table(body: str) -> dict[str, str | None]:
    """Mailbox name -> session id (or None) from the first post's role table."""
    names = {}
    for line in (body or "").splitlines():
        m = ROW.match(line)
        if m and m[1] != "Mailbox name":
            s = SESSION.search(m[2])
            names[m[1]] = s[0] if s else None
    return names


def parse_posts(items: list[dict]) -> dict[str, dict]:
    """from_session name -> {last: ISO time, session: newest self-announced id}."""
    seen: dict[str, dict] = {}
    for c in sorted(items, key=lambda c: c["created_at"]):
        body = c.get("body") or ""
        for name in FROM.findall(body):
            rec = seen.setdefault(name, {"last": None, "session": None})
            rec["last"] = c["created_at"]
            ann = ANNOUNCE.findall(body)
            if ann:
                rec["session"] = ann[-1]
            elif name.startswith("session_"):
                rec["session"] = name
    return seen


def rows_for(board: dict, items: list[dict], now: datetime) -> list[dict]:
    table = parse_table(board.get("body") or "")
    posts = parse_posts(items)
    out = []
    for name in list(table) + [n for n in posts if n not in table]:
        post = posts.get(name, {})
        last = post.get("last")
        age = (now - datetime.fromisoformat(last.replace("Z", "+00:00"))).total_seconds() / 3600 if last else None
        flags = []
        if age is not None and age > QUIET_HOURS:
            flags.append("QUIET")
        if name in table and (age is None or age > STALE_HOURS):
            flags.append("STALE-ROSTER")
        out.append({"board": board["title"], "issue": board["number"], "name": name,
                    "session": post.get("session") or table.get(name), "last_post": last,
                    "age_hours": None if age is None else round(age, 1), "flags": flags})
    return out


def roster(release: str, now: datetime | None = None) -> list[dict]:
    now = now or datetime.now(timezone.utc)
    return [r for b in find_boards(release) for r in rows_for(b, comments(b["number"]), now)]


def render(rows: list[dict]) -> str:
    head = ("BOARD", "#", "NAME", "SESSION", "LAST POST (UTC)", "AGE_H", "FLAGS")
    body = [(r["board"], str(r["issue"]), r["name"], r["session"] or "-",
             (r["last_post"] or "never").replace("T", " ").rstrip("Z"),
             "-" if r["age_hours"] is None else f"{r['age_hours']:.1f}", " ".join(r["flags"])) for r in rows]
    w = [max(len(x[i]) for x in [head] + body) for i in range(len(head))]
    return "\n".join("  ".join(c.ljust(w[i]) for i, c in enumerate(x)).rstrip() for x in [head] + body)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    r = sub.add_parser("roster", help="Who is where on a release's boards")
    r.add_argument("release")
    r.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    rows = roster(args.release)
    print(json.dumps(rows, indent=2) if args.json else render(rows) if rows else f"no open boards for release {args.release}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
