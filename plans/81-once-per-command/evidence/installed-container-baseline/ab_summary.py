"""Summary for the A/B run: medians per arm per group, ratio, after-arm stage table. Used by ab_run.py and rebuild_ab_summary.py."""
import json, statistics
from pathlib import Path

def summarize(records, OUT, SETTING, LOAD_MAX, ARMS, SAMPLES):
    OUT = Path(OUT)
    groups = [("same", None), ("changed", None), ("timeline", None)]
    from datetime import datetime, timezone
    summary = {"setting": SETTING, "when_utc": datetime.now(timezone.utc).isoformat(), "load_max": LOAD_MAX,
               "arms": {a: {"launcher": v["launcher"], "generate_extra": v.get("generate_extra", [])} for a, v in ARMS.items()},
               "groups": {}, "records": records}
    for group, _ in groups:
        g = {}
        for arm in ARMS:
            rs = [r for r in records if r["group"] == group and r["arm"] == arm and not r["name"].endswith("-warmup")]
            ok = [r for r in rs if r["ok"]]; w = [r["wall_seconds"] for r in ok]
            g[arm] = {"runs": len(rs), "succeeded": len(ok), "median_wall_seconds": round(statistics.median(w), 3) if w else None,
                      "min": min(w, default=None), "max": max(w, default=None), "walls": w,
                      "load_before_1m": [round(r["load_before"][0], 2) for r in rs], "load_after_1m": [round(r["load_after"][0], 2) for r in rs]}
        b, a = g["before"]["median_wall_seconds"], g["after"]["median_wall_seconds"]
        g["ratio_after_over_before"] = round(a / b, 3) if a and b else None
        g["percent_change"] = round((a / b - 1) * 100, 1) if a and b else None
        summary["groups"][group] = g
    # after-arm stage table (candidate --timings): median seconds per stage per generate group
    stages = {}
    for group in ("same", "changed"):
        rows = [r["timings"] for r in records if r["group"] == group and r["arm"] == "after" and not r["name"].endswith("-warmup") and r["ok"] and r["timings"]]
        names = {}
        for t in rows:
            for s in t: names.setdefault((s["stage"], s.get("parent")), []).append((s["seconds"], s.get("total_seconds", s["seconds"])))
        stages[group] = [{"stage": n, "parent": p, "occurrences_seen": len(v), "median_seconds": round(statistics.median(x[0] for x in v), 4),
                          "median_total_seconds": round(statistics.median(x[1] for x in v), 4)}
                         for (n, p), v in sorted(names.items(), key=lambda kv: -statistics.median(x[1] for x in kv[1]))]
    summary["after_stage_table"] = stages
    (OUT / "summary-ab.json").write_text(json.dumps(summary, indent=2))
    print("\nSETTING:", SETTING)
    print(f"{'group':10s} {'before median s':>16s} {'after median s':>15s} {'after/before':>13s} {'change':>8s}  ok(b/a)  load1 before-cmd range (b | a)")
    for group, g in summary["groups"].items():
        lb = g["before"]["load_before_1m"]; la = g["after"]["load_before_1m"]
        print(f"{group:10s} {g['before']['median_wall_seconds']!s:>16s} {g['after']['median_wall_seconds']!s:>15s} "
              f"{g['ratio_after_over_before']!s:>13s} {str(g['percent_change']) + '%':>8s}  {g['before']['succeeded']}/{g['after']['succeeded']}  "
              f"{min(lb):.2f}-{max(lb):.2f} | {min(la):.2f}-{max(la):.2f}")
    for group, rows in stages.items():
        print(f"\nafter-arm stages, {group} (median of {SAMPLES}; top 14 by total seconds):")
        for r in rows[:14]: print(f"  {r['median_total_seconds']:8.3f} s total  {r['median_seconds']:8.3f} s self  {r['stage']}  (in: {r['parent']})")
    print(f"\nWrote {OUT / 'summary-ab.json'}")
    return summary
