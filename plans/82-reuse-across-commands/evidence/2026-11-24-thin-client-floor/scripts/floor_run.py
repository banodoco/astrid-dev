#!/usr/bin/env python3
"""Plan 82 floor run: one warm-up per arm, then SAMPLES alternating rounds; medians.

Arms (all to "task queued", --no-wait):
  A       installed `run-astrid generate image ... --timings` (Part 2b's command, same prompt)
  Cnaive  stub thin client -> stub warm host, literal substitution (floor of the stub)
  Creal   stub thin client -> stub warm host doing the real per-request work in-line
  W       stub thin client -> stub warm host running today's astrid.console.main in-process
  Cping   stub thin client -> stub warm host, no request work (client + IPC floor)
Each timed command is gated on 1-minute load < LOAD_MAX; after each, the queued task is
followed to a terminal state (untimed) so its execution does not overlap the next sample.
Run with env.sh sourced (isolated HOME/XDG). Usage: floor_run.py OUTDIR
"""
import json, os, statistics, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hostreq

OUT = sys.argv[1]; os.makedirs(OUT + "/raw", exist_ok=True)
SAMPLES = int(os.environ.get("SAMPLES", "5")); LOAD_MAX = float(os.environ.get("LOAD_MAX", "1.0"))
PROGRAM = os.environ["PROGRAM"]; VPY = f"{PROGRAM}/versions/{open(PROGRAM + '/current').read().strip()}/py/bin/python"
COMFY = "http://127.0.0.1:18388"; CLIENT = "/root/plan82-floor/scripts/thin_client.py"
ARMS = os.environ.get("ARMS", "A Cnaive Creal W Cping").split()

def argv(arm, k):
    changed = f"a blue square on a plain background, variation {k}"
    if arm == "A":
        return [f"{PROGRAM}/run-astrid", "generate", "image", "a red square on a plain background", "--mode", "t2i",
                "--placement", COMFY, "--project", "floor", "--no-wait", "--json", "--timings"]
    mode = {"Cnaive": "naive", "Creal": "real", "Cfull": "realfull", "W": "product", "Cping": "validation"}[arm]
    return [VPY, "-I", "-S", CLIENT, mode, changed, str(7000 + 10 * k + ARMS.index(arm) + int(os.environ.get("SEED_BASE", "0")))]

def gate():
    t = time.monotonic()
    while os.getloadavg()[0] >= LOAD_MAX and time.monotonic() - t < 240:
        time.sleep(2)
    return os.getloadavg()[0], time.monotonic() - t

def run(arm, k, name):
    load, waited = gate()
    t0 = time.perf_counter()
    p = subprocess.run(argv(arm, k), capture_output=True)
    wall = time.perf_counter() - t0
    open(f"{OUT}/raw/{name}.stdout", "wb").write(p.stdout); open(f"{OUT}/raw/{name}.stderr", "wb").write(p.stderr)
    rec = {"name": name, "arm": arm, "k": k, "wall": wall, "exit": p.returncode, "load_before": load,
           "gate_wait": waited, "load_after": os.getloadavg()[0]}
    try:
        if arm == "A":
            d = json.loads(p.stdout); rec["task_id"] = d.get("kernel_task_id")
            rec["timings"] = d.get("timings"); rec["collector_span_seconds"] = d.get("collector_span_seconds")
        else:
            d = json.loads(p.stderr.decode().splitlines()[0])
            rec["server_seconds"] = d.get("server_seconds"); rec["steps"] = d.get("steps")
            task = d.get("task") or {}
            rec["task_id"] = (task.get("data") or {}).get("task_id") or task.get("task_id")
            if arm == "W": rec["timings"] = d.get("timings")
            if not d.get("ok"): rec["error"] = d.get("error")
    except Exception as exc:  # keep the raw output; mark the record
        rec["parse_error"] = repr(exc)
    if rec.get("task_id"):
        w = hostreq.call({"mode": "wait", "task_id": rec["task_id"]})
        rec["task_final_state"] = w.get("state")
    with open(f"{OUT}/records.jsonl", "a") as f: f.write(json.dumps(rec) + "\n")
    print(f"{name:12s} {wall:7.3f} s exit {p.returncode} load {load:.2f} task {str(rec.get('task_id'))[:8]} "
          f"{rec.get('task_final_state')} server {rec.get('server_seconds') or 0:.3f}", flush=True)
    return rec

recs = []
for arm in ARMS: recs.append(run(arm, 0, f"{arm}-warmup"))
for k in range(1, SAMPLES + 1):
    for arm in ARMS: recs.append(run(arm, k, f"{arm}-{k}"))

summary = {"samples": SAMPLES, "load_max": LOAD_MAX, "arms": {}}
for arm in ARMS:
    rs = [r for r in recs if r["arm"] == arm and r["k"] > 0]
    s = {"walls": [round(r["wall"], 4) for r in rs], "median_wall": round(statistics.median(r["wall"] for r in rs), 4),
         "exits": [r["exit"] for r in rs], "task_states": [r.get("task_final_state") for r in rs]}
    if rs and rs[0].get("server_seconds") is not None:
        s["median_server"] = round(statistics.median(r["server_seconds"] for r in rs), 4)
        steps = {}
        for r in rs:
            for key, v in (r.get("steps") or {}).items(): steps.setdefault(key, []).append(v)
        s["median_steps"] = {key: round(statistics.median(v), 4) for key, v in steps.items()}
    if rs and rs[0].get("timings"):
        stages = {}
        for r in rs:
            per = {}
            for row in r["timings"]: per[row["stage"]] = per.get(row["stage"], 0) + row["seconds"]
            for key, v in per.items(): stages.setdefault(key, []).append(v)
        s["median_stage_self_seconds"] = dict(sorted(((key, round(statistics.median(v + [0] * (len(rs) - len(v))), 4))
                                                      for key, v in stages.items()), key=lambda kv: -kv[1]))
    summary["arms"][arm] = s
json.dump(summary, open(f"{OUT}/summary.json", "w"), indent=1)
for arm, s in summary["arms"].items():
    print(f"{arm:7s} median {s['median_wall']:.3f} s  samples {s['walls']}  states {s['task_states']}")
