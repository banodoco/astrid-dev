#!/usr/bin/env python3
"""Arm A only, two installs (base, cand), alternating base,cand,... Adapted from Plan 82 floor_run.py.
One warm-up per build, then SAMPLES alternating rounds; each sample gated on 1-min load < LOAD_MAX for up to
GATE_WAIT s (then it runs anyway and is flagged gate_met=false). Each queued task is followed untimed to a
terminal state before the next sample. Usage: floor_s1.py OUTDIR"""
import json, os, statistics, subprocess, sys, time
S1 = "/home/user/installed-s1"; OUT = sys.argv[1]; os.makedirs(OUT + "/raw", exist_ok=True)
SAMPLES = int(os.environ.get("SAMPLES", "5")); LOAD_MAX = float(os.environ.get("LOAD_MAX", "1.0"))
GATE_WAIT = float(os.environ.get("GATE_WAIT", "240"))
ARMS = ["base", "cand"]; PORT = {"base": 18410, "cand": 18411}; DOOR = {"base": 17410, "cand": 17411}

def env_for(arm):
    H = f"{S1}/{arm}/home"; e = dict(os.environ)
    for k in ("ASTRID_RUNTIME_LAUNCHER","ASTRID_RUNTIME_ENDPOINT","ASTRID_RUNTIME_CREDENTIAL","ASTRID_RUNTIME_DATA_ROOT",
              "ASTRID_PREPARED_CONNECTION","ASTRID_TIMELINE_EVAL_ENDPOINT","ASTRID_TIMELINE_EVAL_CREDENTIAL",
              "ASTRID_TIMELINE_EVAL_REALM_ID","ASTRID_TIMELINE_EVAL_ACTOR_ID"): e.pop(k, None)
    e.update(HOME=H, XDG_DATA_HOME=H + "/.local/share", XDG_STATE_HOME=H + "/.local/state", XDG_CONFIG_HOME=H + "/.config",
             XDG_CACHE_HOME=H + "/.cache", TMPDIR=f"{S1}/{arm}/tmp", ASTRID_RUNTIME_DOOR_PORT=str(DOOR[arm]),
             PYTHONDONTWRITEBYTECODE="1")
    return e

def argv(arm):
    return [f"{S1}/{arm}/program/run-astrid", "generate", "image", "a red square on a plain background", "--mode", "t2i",
            "--placement", f"http://127.0.0.1:{PORT[arm]}", "--project", "floor", "--no-wait", "--json", "--timings"]

def gate():
    t = time.monotonic()
    while os.getloadavg()[0] >= LOAD_MAX and time.monotonic() - t < GATE_WAIT: time.sleep(2)
    return os.getloadavg()[0], time.monotonic() - t

def follow(arm, task_id, limit=180):
    end = time.monotonic() + limit; state = None
    while time.monotonic() < end:
        p = subprocess.run([f"{S1}/{arm}/program/run-astrid", "tasks", "show", task_id, "--project", "floor", "--json"],
                           capture_output=True, env=env_for(arm))
        try: state = json.loads(p.stdout)["data"]["state"]
        except Exception: state = "unreadable"
        if state in ("succeeded", "failed", "cancelled", "rejected", "settled", "completed", "expired"): return state
        time.sleep(1.0)
    return "timeout:" + str(state)

def run(arm, k, name):
    load, waited = gate()
    t0 = time.perf_counter()
    p = subprocess.run(argv(arm), capture_output=True, env=env_for(arm))
    wall = time.perf_counter() - t0
    open(f"{OUT}/raw/{name}.stdout", "wb").write(p.stdout); open(f"{OUT}/raw/{name}.stderr", "wb").write(p.stderr)
    rec = {"name": name, "arm": arm, "k": k, "wall": wall, "exit": p.returncode, "load_before": load,
           "gate_wait": waited, "gate_met": load < LOAD_MAX, "load_after": os.getloadavg()[0]}
    try:
        d = json.loads(p.stdout); rec["task_id"] = d.get("kernel_task_id"); rec["ok"] = d.get("ok")
        rec["timings"] = d.get("timings"); rec["collector_span_seconds"] = d.get("collector_span_seconds")
    except Exception as exc: rec["parse_error"] = repr(exc)
    if rec.get("task_id"): rec["task_final_state"] = follow(arm, rec["task_id"])
    with open(f"{OUT}/records.jsonl", "a") as f: f.write(json.dumps(rec) + "\n")
    print(f"{name:10s} {wall:7.3f} s exit {p.returncode} load {load:.2f} gate_met {rec['gate_met']} waited {waited:.0f}s "
          f"task {str(rec.get('task_id'))[:8]} {rec.get('task_final_state')}", flush=True)
    return rec

recs = []
for arm in ARMS: recs.append(run(arm, 0, f"{arm}-warmup"))
for k in range(1, SAMPLES + 1):
    for arm in ARMS: recs.append(run(arm, k, f"{arm}-{k}"))

summary = {"samples": SAMPLES, "load_max": LOAD_MAX, "gate_wait": GATE_WAIT, "arms": {}}
for arm in ARMS:
    rs = [r for r in recs if r["arm"] == arm and r["k"] > 0]
    s = {"walls": [round(r["wall"], 4) for r in rs], "median_wall": round(statistics.median(r["wall"] for r in rs), 4),
         "loads_before": [round(r["load_before"], 2) for r in rs], "gate_met": [r["gate_met"] for r in rs],
         "exits": [r["exit"] for r in rs], "task_states": [r.get("task_final_state") for r in rs],
         "collector_spans": [round(r.get("collector_span_seconds") or 0, 4) for r in rs]}
    stages = {}
    for r in rs:
        per = {}
        for row in r.get("timings") or []: per[row["stage"]] = per.get(row["stage"], 0) + row["seconds"]
        for key, v in per.items(): stages.setdefault(key, []).append(v)
    s["median_stage_self_seconds"] = dict(sorted(((key, round(statistics.median(v + [0] * (len(rs) - len(v))), 4))
                                                  for key, v in stages.items()), key=lambda kv: -kv[1]))
    summary["arms"][arm] = s
json.dump(summary, open(f"{OUT}/summary.json", "w"), indent=1)
for arm, s in summary["arms"].items(): print(f"{arm:5s} median {s['median_wall']:.3f} s  samples {s['walls']}  states {s['task_states']}")
