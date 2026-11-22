#!/usr/bin/env python3
"""Gated A/B driver for the installed Astrid baseline (called by run-ab-installed.sh --run).

Setting (printed every time): INSTALLED builds, CPU container, STAND-IN ComfyUI (no real node-info answer, no GPU work),
shared 4-vCPU box. Every timed command is gated: 1-min load < LOAD_MAX before start, shared lock held only while the command
runs. If the gate is not met within LOAD_WAIT_SECONDS the whole run FAILS (exit 3); nothing runs ungated.
Env (all required, set by the wrapper): IB, EVIDENCE_DIR, COMFY_URL, MEDIA_PNG, ARMS_JSON, optional LOAD_MAX, LOAD_WAIT_SECONDS, SAMPLES."""
from ab_summary import summarize
import fcntl, json, os, statistics, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

IB = Path(os.environ["IB"]); OUT = Path(os.environ["EVIDENCE_DIR"]); RAW = OUT / "raw"; RAW.mkdir(parents=True, exist_ok=True)
COMFY = os.environ["COMFY_URL"]; MEDIA = os.environ["MEDIA_PNG"]
ARMS = json.loads(os.environ["ARMS_JSON"])   # {"before": {launcher, home, door_port, extra:[...]}, "after": {...}}
LOAD_MAX = float(os.environ.get("LOAD_MAX", "1.0")); WAIT = float(os.environ.get("LOAD_WAIT_SECONDS", "600"))
SAMPLES = int(os.environ.get("SAMPLES", "5"))
SETTING = ("installed builds, CPU container, stand-in ComfyUI (not covered: a real ComfyUI's node-info answer, GPU work), "
           "shared 4-vCPU box, --no-wait (times Astrid up to 'task queued')")
STAMP = datetime.now().strftime("%Y%m%d-%H%M%S")
PROJECT = {a: f"ab-{a}-{STAMP}" for a in ARMS}
records = []

def arm_env(arm):
    h = ARMS[arm]["home"]; env = dict(os.environ)
    env.update(HOME=h, XDG_DATA_HOME=f"{h}/.local/share", XDG_STATE_HOME=f"{h}/.local/state",
               XDG_CONFIG_HOME=f"{h}/.config", XDG_CACHE_HOME=f"{h}/.cache", TMPDIR=ARMS[arm]["tmp"])
    return env

def untimed(arm, args):
    p = subprocess.run([ARMS[arm]["launcher"], *args], env=arm_env(arm), capture_output=True, text=True, stdin=subprocess.DEVNULL)
    return p

def gated_run(name, group, arm, args):
    """Wait for load < LOAD_MAX, take the lock only for the command, record loads. Fail the run if the gate is never met."""
    deadline = time.monotonic() + WAIT; waited_from = time.monotonic()
    lock = open("/tmp/astrid-timing.lock", "a")
    while True:
        if os.getloadavg()[0] < LOAD_MAX:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)   # polled, so the 10-minute cap covers lock waits too
                if os.getloadavg()[0] < LOAD_MAX: break            # re-check at the moment we own the lock
                fcntl.flock(lock, fcntl.LOCK_UN)
            except BlockingIOError:
                pass
        if time.monotonic() > deadline:
            print(f"FAIL: load gate (<{LOAD_MAX}) not met within {WAIT:.0f}s before {name}; load {os.getloadavg()}. "
                  "Run aborted; nothing was run ungated.", file=sys.stderr)
            (OUT / "FAILED-load-gate.txt").write_text(f"{name} load={os.getloadavg()}\n"); sys.exit(3)
        time.sleep(2)
    try:
        lb = os.getloadavg(); t0 = time.monotonic(); started = datetime.now(timezone.utc).isoformat()
        p = subprocess.run([ARMS[arm]["launcher"], *args], env=arm_env(arm), capture_output=True, text=True,
                           stdin=subprocess.DEVNULL, timeout=900)
        wall = time.monotonic() - t0; la = os.getloadavg()
    finally:
        fcntl.flock(lock, fcntl.LOCK_UN)
    (RAW / f"{name}.stdout").write_text(p.stdout); (RAW / f"{name}.stderr").write_text(p.stderr)
    try: parsed = json.loads(p.stdout)
    except Exception: parsed = None
    rec = {"name": name, "group": group, "arm": arm, "args": args, "started_at": started, "wall_seconds": round(wall, 4),
           "exit_code": p.returncode, "ok": p.returncode == 0 and (parsed is None or parsed.get("ok", True) is not False),
           "load_before": lb, "load_after": la, "gate_wait_seconds": round(time.monotonic() - waited_from - wall, 2),
           "timings": parsed.get("timings") if isinstance(parsed, dict) else None}
    records.append(rec)
    with open(OUT / "records.jsonl", "a") as f: f.write(json.dumps(rec) + "\n")
    print(f"  {name:28s} {rec['wall_seconds']:8.3f} s  exit {p.returncode}  load {lb[0]:.2f} -> {la[0]:.2f}", flush=True)
    return rec

def gen_args(arm, prompt):
    return ["generate", "image", prompt, "--mode", "t2i", "--placement", COMFY, "--project", PROJECT[arm], "--no-wait", "--json",
            *ARMS[arm].get("generate_extra", [])]

def tl_args(arm, k):
    p = PROJECT[arm]
    return ["timelines", "edit", p, "--project", p, "--add-layer", "media", "--layer-asset", MEDIA, "--on", str(3 * k),
            "--for", "3", "--track", "V1", "--id", f"ab-{k}", "--idempotency-key", f"{p}-{k}", "--json"]

print("SETTING:", SETTING, flush=True)
for arm in ARMS:   # setup, not timed
    p = PROJECT[arm]
    for args in (["projects", "create", p, "--name", p, "--select", "--json"],
                 ["timelines", "create", "--project", p, "--slug", p, "--name", p, "--json"]):
        r = untimed(arm, args)
        if r.returncode != 0: sys.exit(f"setup failed on {arm}: {args[:2]}: {r.stdout[-300:]} {r.stderr[-300:]}")

groups = [("same", lambda arm, k: gen_args(arm, "a red square on a plain background")),
          ("changed", lambda arm, k: gen_args(arm, f"a blue square on a plain background, variation {k}")),
          ("timeline", tl_args)]
order = list(ARMS)  # before, after
for group, make in groups:
    print(f"[{group}] warm-up, then {SAMPLES} alternating pairs", flush=True)
    for arm in order: gated_run(f"{group}-{arm}-warmup", group, arm, make(arm, 0)); records[-1]["warmup"] = True
    for k in range(1, SAMPLES + 1):
        for arm in order: gated_run(f"{group}-{arm}-{k}", group, arm, make(arm, k))

summarize(records, OUT, SETTING, LOAD_MAX, ARMS, SAMPLES)
