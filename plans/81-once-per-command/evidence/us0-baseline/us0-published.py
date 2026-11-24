#!/usr/bin/env python3
"""US-0 "today" baseline for Plan 81, for a PUBLISHED, INSTALLED Astrid with a real ComfyUI.

What it does: creates one scratch project and timeline, then runs
  - 5 `generate image` commands with the SAME prompt,
  - 5 `generate image` commands with CHANGED prompts,
  - 5 timeline edits (one image each),
each as a fresh `astrid` process, timing the whole process with a monotonic clock.
It uses no flag that only newer builds have (no --timings), so it works on what you have
installed today. It records everything it saw and never stops at the first problem:
a failed command is recorded with its exit code and output, and the run goes on.

Needs: Python 3, the installed `astrid` on PATH, a running ComfyUI, one PNG on disk.
It queues 10 real image generations on your ComfyUI (--no-wait: it does not wait for them
to finish) and makes one scratch project; nothing is paid unless your image route is a paid one.

Usage (set the variables, then run it):
    export ASTRID_CMD="$(command -v astrid)"
    export COMFY_URL="http://127.0.0.1:8188"
    export MEDIA_PNG="/absolute/path/to/any-image.png"
    export EVIDENCE_DIR="$HOME/us0-published-$(date +%Y%m%d-%H%M)"
    python3 us0-published.py

Optional: GEN_EXTRA="--mode t2i" (default) to change the generate arguments after the prompt;
PROJECT / TIMELINE to name the scratch project (default: us0-published-<time>).
Then send me the EVIDENCE_DIR folder (zip it); summary.json is the headline.
"""
import json
import os
import platform
import shlex
import statistics
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


def env(name, default=None, required=False):
    value = os.environ.get(name, default)
    if required and not value:
        sys.exit(f"missing environment variable {name}; see the usage at the top of this file")
    return value


ASTRID = env("ASTRID_CMD", required=True)
COMFY = env("COMFY_URL", required=True)
MEDIA = env("MEDIA_PNG", required=True)
OUT = Path(env("EVIDENCE_DIR", required=True))
STAMP = datetime.now().strftime("%Y%m%d-%H%M%S")
PROJECT = env("PROJECT", f"us0-published-{STAMP}")
TIMELINE = env("TIMELINE", PROJECT)
GEN_EXTRA = shlex.split(env("GEN_EXTRA", "--mode t2i"))
RAW = OUT / "raw"
RAW.mkdir(parents=True, exist_ok=True)

if not Path(MEDIA).is_file():
    sys.exit(f"MEDIA_PNG is not a file: {MEDIA}")


def load_average():
    try:
        return os.getloadavg()
    except (AttributeError, OSError):
        return None


def run(name, args):
    """Run one fresh astrid process; record wall time, exit code and raw output."""
    before_load = load_average()
    start = time.monotonic()
    started_at = datetime.now(timezone.utc).isoformat()
    try:
        p = subprocess.run([ASTRID, *args], capture_output=True, text=True, timeout=900)
        code, out, err = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as exc:
        code, out, err = "timeout", exc.stdout or "", exc.stderr or ""
    wall = time.monotonic() - start
    (RAW / f"{name}.stdout").write_text(out if isinstance(out, str) else out.decode("utf-8", "replace"), encoding="utf-8")
    (RAW / f"{name}.stderr").write_text(err if isinstance(err, str) else err.decode("utf-8", "replace"), encoding="utf-8")
    parsed = None
    try:
        parsed = json.loads(out)
    except Exception:
        pass
    return {
        "name": name,
        "args": args,
        "started_at": started_at,
        "wall_seconds": round(wall, 4),
        "exit_code": code,
        "ok": code == 0,
        "load_before": before_load,
        "load_after": load_average(),
        "json": parsed is not None,
        "task_id": find_id(parsed),
        "revision_id": find_key(parsed, ("accepted_revision_id", "revision_id")),
    }


def find_key(value, keys):
    if isinstance(value, dict):
        for k in keys:
            if value.get(k):
                return value[k]
        for v in value.values():
            found = find_key(v, keys)
            if found:
                return found
    elif isinstance(value, list):
        for v in value:
            found = find_key(v, keys)
            if found:
                return found
    return None


def find_id(value):
    return find_key(value, ("kernel_task_id", "task_id", "prompt_id"))


def med(values):
    return round(statistics.median(values), 4) if values else None


rows = []
rows.append(run("project-create", ["projects", "create", PROJECT, "--name", PROJECT, "--select", "--json"]))
rows.append(run("timeline-create", ["timelines", "create", "--project", PROJECT, "--slug", TIMELINE,
                                    "--name", TIMELINE, "--json"]))

groups = {"same": [], "changed": [], "timeline": []}
for i in range(1, 6):
    groups["same"].append(run(
        f"generate-same-{i}",
        ["generate", "image", "a red square on a plain background", *GEN_EXTRA, "--placement", COMFY,
         "--project", PROJECT, "--no-wait", "--json"]))
for i in range(1, 6):
    groups["changed"].append(run(
        f"generate-changed-{i}",
        ["generate", "image", f"a blue square on a plain background, variation {i}", *GEN_EXTRA,
         "--placement", COMFY, "--project", PROJECT, "--no-wait", "--json"]))
for i in range(1, 6):
    groups["timeline"].append(run(
        f"timeline-edit-{i}",
        ["timelines", "edit", TIMELINE, "--project", PROJECT, "--add-layer", "media", "--layer-asset", MEDIA,
         "--on", str(3 * (i - 1)), "--for", "3", "--track", "V1", "--id", f"us0-{i}",
         "--idempotency-key", f"{TIMELINE}-{i}", "--json"]))

summary = {
    "what": "Plan 81 US-0, today's time on a published installed Astrid (no instrumentation flags)",
    "when_utc": datetime.now(timezone.utc).isoformat(),
    "machine": {"platform": platform.platform(), "python": platform.python_version(), "cpus": os.cpu_count()},
    "astrid_cmd": ASTRID,
    "comfy_url": COMFY,
    "groups": {},
    "setup": rows,
}
for group, items in groups.items():
    ok = [r for r in items if r["ok"]]
    ids = [r["task_id"] for r in ok if r["task_id"]]
    summary["groups"][group] = {
        "runs": len(items),
        "succeeded": len(ok),
        "median_wall_seconds": med([r["wall_seconds"] for r in ok]),
        "min_wall_seconds": min((r["wall_seconds"] for r in ok), default=None),
        "max_wall_seconds": max((r["wall_seconds"] for r in ok), default=None),
        "distinct_task_ids": len(set(ids)) if group != "timeline" else None,
        "accepted_revisions": sum(1 for r in ok if r["revision_id"]) if group == "timeline" else None,
        "runs_detail": items,
    }
version = run("astrid-version", ["--version"])
summary["astrid_version_output"] = (RAW / "astrid-version.stdout").read_text(encoding="utf-8").strip()
(OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("US-0 (published install) finished.")
for group, data in summary["groups"].items():
    print(f"  {group:9s} {data['succeeded']}/{data['runs']} ok, median {data['median_wall_seconds']} s "
          f"(min {data['min_wall_seconds']}, max {data['max_wall_seconds']})")
print(f"Evidence: {OUT / 'summary.json'}  (zip the whole folder and send it)")
