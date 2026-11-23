#!/usr/bin/env python3
"""Rebuild summary-ab.json for an A/B run from the per-command lines printed by ab_run.py (wall, exit code, 1-min load
before -> after, 2 decimals) plus raw/<name>.stdout (timings). Needed only for runs that predate records.jsonl (ab-run-1).
Usage: rebuild_ab_summary.py EVIDENCE_DIR CONSOLE_LOG [OUT_DIR]   (pure file work, starts nothing)"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ab_summary import summarize

SETTING = ("installed builds, CPU container, stand-in ComfyUI (not covered: a real ComfyUI's node-info answer, GPU work), "
           "shared 4-vCPU box, --no-wait (times Astrid up to 'task queued')")

def records_from_console(d, console):
    recs = []
    for line in Path(console).read_text().splitlines():
        m = re.match(r"\s+((same|changed|timeline)-(before|after|vc48)-(warmup|\d))\s+([\d.]+) s\s+exit (\d+)\s+load ([\d.]+) -> ([\d.]+)", line)
        if not m: continue
        try: parsed = json.loads((Path(d) / "raw" / f"{m[1]}.stdout").read_text())
        except Exception: parsed = None
        recs.append({"name": m[1], "group": m[2], "arm": m[3], "wall_seconds": float(m[5]), "exit_code": int(m[6]),
                     "ok": int(m[6]) == 0 and isinstance(parsed, dict) and parsed.get("ok") is True,
                     "reconstructed": True,
                     "load_before": [float(m[7])], "load_after": [float(m[8])],
                     "args": ["--timings"] if m[3] != "before" and m[2] != "timeline" else [],
                     "timings": parsed.get("timings") if isinstance(parsed, dict) else None})
    return recs

if __name__ == "__main__":
    d = Path(sys.argv[1]); recs = records_from_console(d, sys.argv[2])
    arms = {a: ({"generate_extra": ["--timings"]} if a != "before" else {}) for a in dict.fromkeys(r["arm"] for r in recs)}
    summarize(recs, Path(sys.argv[3]) if len(sys.argv) > 3 else d, "RECONSTRUCTED from console and raw output; " + SETTING, 1.0, arms, 5)
