#!/usr/bin/env python3
"""ASTRID_CMD wrapper: gate on load, hold the shared timing lock only while astrid runs, and
record the command's own wall time (excluding the wait) in $TIMING_LOG (jsonl).
Passes stdout, stderr and the exit code of the real command through unchanged.
Env: REAL_ASTRID (required), TIMING_LOG (required), LOAD_MAX (default 1.0), LOAD_WAIT_SECONDS (default 600)."""
import fcntl, json, os, subprocess, sys, time
from datetime import datetime, timezone

real = os.environ["REAL_ASTRID"]
log = os.environ["TIMING_LOG"]
load_max = float(os.environ.get("LOAD_MAX", "1.0"))
wait_limit = float(os.environ.get("LOAD_WAIT_SECONDS", "600"))

def load1():
    return os.getloadavg()[0]

lock = open("/tmp/astrid-timing.lock", "a")
gate_start = time.monotonic()
gated = True
failed_flag = log + ".gate-failed"  # once the box stayed loaded for the full wait, later commands do not wait again
while load1() >= load_max and not os.path.exists(failed_flag):
    if time.monotonic() - gate_start > wait_limit:
        gated = False  # box stayed loaded: run anyway, flagged in the record
        open(failed_flag, "w").close()
        break
    time.sleep(5)
if os.path.exists(failed_flag): gated = False
fcntl.flock(lock, fcntl.LOCK_EX)
try:
    load_before = os.getloadavg()
    t0 = time.monotonic()
    started = datetime.now(timezone.utc).isoformat()
    p = subprocess.run([real, *sys.argv[1:]], stdin=subprocess.DEVNULL, capture_output=True)
    wall = time.monotonic() - t0
    load_after = os.getloadavg()
finally:
    fcntl.flock(lock, fcntl.LOCK_UN)
with open(log, "a") as f:
    f.write(json.dumps({"args": sys.argv[1:], "started_at": started, "wall_seconds": round(wall, 4),
                        "exit_code": p.returncode, "load_before": load_before, "load_after": load_after,
                        "waited_seconds": round(t0 - gate_start, 2), "load_gate_met": gated}) + "\n")
sys.stdout.buffer.write(p.stdout); sys.stdout.flush()
sys.stderr.buffer.write(p.stderr); sys.stderr.flush()
sys.exit(p.returncode)
