#!/usr/bin/env python3
"""Medians from timing.jsonl written by timed-astrid.py (command wall time only; lock/load wait excluded)."""
import json, statistics, sys
from pathlib import Path
d = Path(sys.argv[1]); rows = [json.loads(l) for l in (d / "timing.jsonl").read_text().splitlines()]
def group(r):
    a = r["args"]
    if a[:2] == ["generate", "image"]:
        return "same" if "red square" in a[2] else "changed" if "blue square" in a[2] else None
    if a[:2] == ["timelines", "edit"]: return "timeline"
    if a[:1] == ["--version"] or a[:2] == ["generate", "defaults"]: return "floor:" + " ".join(a[:2])
    return None
out = {}
for g in ("same", "changed", "timeline") + tuple(sorted({group(r) for r in rows if (group(r) or "").startswith("floor:")})):
    rs = [r for r in rows if group(r) == g]; ok = [r for r in rs if r["exit_code"] == 0]
    w = [r["wall_seconds"] for r in ok]
    out[g] = {"runs": len(rs), "succeeded": len(ok), "median_wall_seconds": round(statistics.median(w), 3) if w else None,
              "min": min(w, default=None), "max": max(w, default=None),
              "load_before_1m": [r["load_before"][0] for r in rs], "load_after_1m": [r["load_after"][0] for r in rs],
              "walls": w, "load_gate_met_all": all(r["load_gate_met"] for r in rs),
              "waited_seconds": [r["waited_seconds"] for r in rs]}
(d / "timing-summary.json").write_text(json.dumps(out, indent=2))
for g, v in out.items():
    print(f"  {g:22s} {v['succeeded']}/{v['runs']} ok  median {v['median_wall_seconds']} s  (min {v['min']}, max {v['max']})  "
          f"load1 before {min(v['load_before_1m'], default=0):.2f}-{max(v['load_before_1m'], default=0):.2f} gate_met={v['load_gate_met_all']}")
