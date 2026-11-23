#!/usr/bin/env python3
"""Gated A/B driver for the installed Astrid baseline (called by run-ab-installed.sh --run).

Setting (printed every time): INSTALLED builds, CPU container, STAND-IN ComfyUI (no real node-info answer, no GPU work),
shared 4-vCPU box. Every timed command is gated: 1-min load < LOAD_MAX before start, shared lock held only while the command
runs. If the gate is not met within LOAD_WAIT_SECONDS the whole run FAILS (exit 3); nothing runs ungated.
Env (all required, set by the wrapper): IB, EVIDENCE_DIR, COMFY_URL, MEDIA_PNG, ARMS_JSON, optional LOAD_MAX, LOAD_WAIT_SECONDS, SAMPLES."""
from ab_summary import summarize
from ab_receipt import generation_error
import fcntl, json, math, os, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

IB = Path(os.environ["IB"]); OUT = Path(os.environ["EVIDENCE_DIR"]); RAW = OUT / "raw"; RAW.mkdir(parents=True, exist_ok=True)
COMFY = os.environ["COMFY_URL"]; MEDIA = os.environ["MEDIA_PNG"]
ARMS = json.loads(os.environ["ARMS_JSON"])   # {"before": {launcher, home, door_port, extra:[...]}, "after": {...}}
LOAD_MAX = float(os.environ.get("LOAD_MAX", "1.0")); WAIT = float(os.environ.get("LOAD_WAIT_SECONDS", "600"))
SAMPLES = int(os.environ.get("SAMPLES", "5"))
ATTEST = os.environ.get("ASTRID_AB_ATTEST", "on")
if ATTEST not in ("on", "off"):
    sys.exit("ASTRID_AB_ATTEST must be on or off")
SETTING = ("installed builds, CPU container, stand-in ComfyUI (not covered: a real ComfyUI's node-info answer, GPU work), "
           "shared 4-vCPU box, --no-wait (times Astrid up to 'task queued')")
STAMP = datetime.now().strftime("%Y%m%d-%H%M%S")
PROJECT = {a: f"ab-{a}-{STAMP}" for a in ARMS}
records = []
if (OUT / "records.jsonl").exists() or (OUT / "summary-ab.json").exists():
    sys.exit("evidence directory already contains A/B records or summary; choose a new directory")
if not ARMS or SAMPLES < 1:
    sys.exit("at least one arm and one sample are required")
if not math.isfinite(LOAD_MAX) or LOAD_MAX <= 0 or not math.isfinite(WAIT) or WAIT < 0:
    sys.exit("LOAD_MAX must be finite and positive and LOAD_WAIT_SECONDS finite and nonnegative")

def arm_env(arm):
    # Do not inherit a prepared connection, endpoint, credential, or other
    # Astrid runtime override from the invoking shell. Each arm owns its port.
    h = ARMS[arm]["home"]; env = {k: v for k, v in os.environ.items() if not k.startswith("ASTRID_")}
    env.update(HOME=h, XDG_DATA_HOME=f"{h}/.local/share", XDG_STATE_HOME=f"{h}/.local/state",
               XDG_CONFIG_HOME=f"{h}/.config", XDG_CACHE_HOME=f"{h}/.cache", TMPDIR=ARMS[arm]["tmp"],
               ASTRID_RUNTIME_DOOR_PORT=str(ARMS[arm]["door_port"]))
    return env

def durable_write(path, data, mode="w"):
    with open(path, mode, encoding="utf-8") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())

def append_record(rec):
    durable_write(OUT / "records.jsonl", json.dumps(rec) + "\n", "a")

def as_text(value):
    if value is None: return ""
    return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else value

def listener_attestation(name, arm, phase):
    """Capture the listener identity, without claiming the command contacted it."""
    path = RAW / f"{name}.listener-{phase}.json"
    spec = ARMS[arm]
    try:
        p = subprocess.run([sys.executable, str(Path(__file__).resolve().parent / "runtime_attestation.py"),
                            str(spec["door_port"]), str(spec["current"]), str(spec["manifest"]), str(path)],
                           capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=30)
        durable_write(RAW / f"{name}.listener-{phase}.stderr", p.stderr)
        if p.returncode != 0:
            return None, f"listener {phase} attestation failed (exit {p.returncode})"
        identity = json.loads(path.read_text())
        required = {"port", "address_hex", "socket_table", "socket_inode", "pid", "start_ticks", "exe", "cwd", "selected_version", "manifest_shas", "scope"}
        if not isinstance(identity, dict) or not required <= identity.keys():
            return None, f"listener {phase} attestation is malformed"
        return identity, None
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired) as exc:
        return None, f"listener {phase} attestation failed: {type(exc).__name__}: {exc}"

def command(name, group, arm, args, extra=None, before_evidence=None):
    """Capture output and a durable record even when the process cannot complete."""
    started = datetime.now(timezone.utc).isoformat()
    stdout = stderr = ""; code = None; error = None
    before, error = before_evidence if before_evidence is not None else (listener_attestation(name, arm, "before") if ATTEST == "on" else (None, None))
    after = None; wall = 0.0
    if error is None:
        t0 = time.monotonic()
        try:
            p = subprocess.run([ARMS[arm]["launcher"], *args], env=arm_env(arm), capture_output=True, text=True,
                               stdin=subprocess.DEVNULL, timeout=900)
            stdout, stderr, code = p.stdout, p.stderr, p.returncode
        except subprocess.TimeoutExpired as exc:
            stdout, stderr = as_text(exc.stdout), as_text(exc.stderr)
            error = f"timeout after {exc.timeout} seconds"
        except (OSError, ValueError, KeyError) as exc:
            error = f"{type(exc).__name__}: {exc}"
        wall = time.monotonic() - t0
        if ATTEST == "on":
            after, attestation_error = listener_attestation(name, arm, "after")
            if attestation_error:
                error = f"{error}; {attestation_error}" if error else attestation_error
            elif {k: v for k, v in before.items() if k != "scope"} != {k: v for k, v in after.items() if k != "scope"}:
                error = f"{error}; listener identity changed during command" if error else "listener identity changed during command"
    durable_write(RAW / f"{name}.stdout", stdout)
    durable_write(RAW / f"{name}.stderr", stderr)
    parsed = None
    if error is None:
        try:
            parsed = json.loads(stdout)
        except (ValueError, TypeError) as exc:
            error = f"invalid JSON output: {exc}"
        if error is None and not isinstance(parsed, dict): error = "JSON output is not an object"
        if error is None and parsed.get("ok") is not True: error = "JSON output missing ok=true"
        if error is None and code != 0: error = f"exit code {code}"
        if error is None: error = generation_error(parsed, args)
    rec = {"name": name, "group": group, "arm": arm, "args": args, "started_at": started,
           "wall_seconds": round(wall, 4), "exit_code": code, "ok": error is None,
           "door_port": ARMS[arm].get("door_port"),
           "listener_before": before, "listener_after": after,
           "kernel_task_id": parsed.get("kernel_task_id") if isinstance(parsed, dict) else None,
           "accepted_revision_id": (parsed["data"].get("accepted_revision_id")
                                    if isinstance(parsed, dict) and isinstance(parsed.get("data"), dict) else None),
           "timeline_status": (parsed["data"].get("status")
                               if isinstance(parsed, dict) and isinstance(parsed.get("data"), dict) else None),
           "timings": parsed.get("timings") if isinstance(parsed, dict) else None,
           "collector_span_seconds": parsed.get("collector_span_seconds") if isinstance(parsed, dict) else None}
    if extra: rec.update(extra)
    if error is not None: rec["error"] = error
    return rec

def untimed(name, arm, args):
    rec = command(name, "setup", arm, args)
    durable_write(OUT / "setup-records.jsonl", json.dumps(rec) + "\n", "a")
    if not rec["ok"]:
        append_record(rec)
        sys.exit(f"setup failed on {arm}: {rec['error']}; see {OUT / 'records.jsonl'} and raw output")

def gated_run(name, group, arm, args):
    """Wait for load < LOAD_MAX and record every attempted command; abort on failure."""
    deadline = time.monotonic() + WAIT; waited_from = time.monotonic(); attempt = 0
    with open("/tmp/astrid-timing.lock", "a") as lock:
        while True:
            if os.getloadavg()[0] < LOAD_MAX:
                try:
                    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    attempt += 1
                    before_evidence = listener_attestation(name, arm, f"before-{attempt}") if ATTEST == "on" else (None, None)
                    lb = os.getloadavg()
                    if before_evidence[1] is not None or lb[0] < LOAD_MAX: break
                    fcntl.flock(lock, fcntl.LOCK_UN)
                except BlockingIOError:
                    pass
            if time.monotonic() > deadline:
                load = os.getloadavg()
                msg = f"load gate (<{LOAD_MAX}) not met within {WAIT:.0f}s before {name}; load {load}"
                durable_write(OUT / "FAILED-load-gate.txt", msg + "\n")
                append_record({"name": name, "group": group, "arm": arm, "args": args, "door_port": ARMS[arm].get("door_port"), "ok": False, "error": msg})
                print(f"FAIL: {msg}. Run aborted; nothing was run ungated.", file=sys.stderr)
                sys.exit(3)
            time.sleep(2)
        try:
            gate_wait = time.monotonic() - waited_from
            rec = command(name, group, arm, args, {"load_before": lb, "gate_wait_seconds": round(gate_wait, 2)}, before_evidence)
            rec["load_after"] = os.getloadavg()
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)
    records.append(rec)
    append_record(rec)
    print(f"  {name:28s} {rec['wall_seconds']:8.3f} s  exit {rec['exit_code']}  load {lb[0]:.2f} -> {rec['load_after'][0]:.2f}", flush=True)
    if not rec["ok"]:
        sys.exit(f"command failed: {name}: {rec['error']}; see {OUT / 'records.jsonl'} and raw output")
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
    for name, args in (("projects", ["projects", "create", p, "--name", p, "--select", "--json"]),
                       ("timelines", ["timelines", "create", "--project", p, "--slug", p, "--name", p, "--json"])):
        untimed(f"setup-{arm}-{name}", arm, args)

groups = [("same", lambda arm, k: gen_args(arm, "a red square on a plain background")),
          ("changed", lambda arm, k: gen_args(arm, f"a blue square on a plain background, variation {k}")),
          ("timeline", tl_args)]
order = list(ARMS)  # one round per sample, in this order: before, after, vc48
for group, make in groups:
    print(f"[{group}] warm-up, then {SAMPLES} alternating rounds", flush=True)
    for arm in order: gated_run(f"{group}-{arm}-warmup", group, arm, make(arm, 0))
    for k in range(1, SAMPLES + 1):
        for arm in order: gated_run(f"{group}-{arm}-{k}", group, arm, make(arm, k))

append_record({"records_complete": True, "count": len(records), "arms": list(ARMS), "samples": SAMPLES,
               "timing_receipt_schema": 1,
               "qualification_schema": 2 if ATTEST == "on" else 3,
               "attestation": ATTEST,
               "load_max": LOAD_MAX,
               "door_ports": {a: ARMS[a]["door_port"] for a in ARMS},
               "when_utc": datetime.now(timezone.utc).isoformat()})
try:
    summary = summarize(records, OUT, SETTING, LOAD_MAX, ARMS, SAMPLES, require_attestation=ATTEST == "on", attestation=ATTEST)
except Exception as exc:   # the records are already on disk; never lose a run to the summary step
    print(f"SUMMARY FAILED ({type(exc).__name__}: {exc}); records are in {OUT / 'records.jsonl'}; rebuild with: python3 {Path(__file__).resolve().parent}/ab_summary.py {OUT}", file=sys.stderr)
    sys.exit(4)
if not summary["qualification"]["passed"]:
    print("QUALIFICATION FAILED: " + "; ".join(summary["qualification"]["reasons"]), file=sys.stderr)
    sys.exit(5)
