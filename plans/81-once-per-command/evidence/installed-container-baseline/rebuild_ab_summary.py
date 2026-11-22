#!/usr/bin/env python3
"""Rebuild summary-ab.json for a run whose in-memory summary step crashed (ab-run-1): reads the per-command lines printed
by ab_run.py (wall, exit code, 1-min load before -> after; 2 decimals) and raw/<name>.stdout (timings). Usage: rebuild_ab_summary.py EVIDENCE_DIR CONSOLE_LOG"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ab_summary import summarize
d = Path(sys.argv[1]); recs = []
for line in Path(sys.argv[2]).read_text().splitlines():
    m = re.match(r"\s+((same|changed|timeline)-(before|after)-(warmup|\d))\s+([\d.]+) s\s+exit (\d+)\s+load ([\d.]+) -> ([\d.]+)", line)
    if not m: continue
    name, group, arm = m[1], m[2], m[3]
    try: parsed = json.loads((d / "raw" / f"{name}.stdout").read_text())
    except Exception: parsed = None
    recs.append({"name": name, "group": group, "arm": arm, "wall_seconds": float(m[5]), "exit_code": int(m[6]),
                 "ok": int(m[6]) == 0 and (parsed is None or parsed.get("ok", True) is not False),
                 "load_before": [float(m[7])], "load_after": [float(m[8])],
                 "timings": parsed.get("timings") if isinstance(parsed, dict) else None})
SETTING = ("installed builds, CPU container, stand-in ComfyUI (not covered: a real ComfyUI's node-info answer, GPU work), "
           "shared 4-vCPU box, --no-wait (times Astrid up to 'task queued')")
ARMS = {"before": {"launcher": "program/run-astrid"}, "after": {"launcher": "program-after/run-astrid", "generate_extra": ["--timings"]}}
summarize(recs, d, SETTING, 1.0, ARMS, 5)
