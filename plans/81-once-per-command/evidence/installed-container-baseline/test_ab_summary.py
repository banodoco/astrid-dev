#!/usr/bin/env python3
"""Pure-file test of the A/B summary code (starts no process, installs nothing).
Run: python3 /root/codex/installed-baseline/test_ab_summary.py"""
import json, tempfile, unittest
from pathlib import Path
from ab_summary import summarize, stage_table, group_summary
from rebuild_ab_summary import records_from_console, SETTING

IB = Path(__file__).resolve().parent
RUN1 = IB / "ab-run-1"

class Summary(unittest.TestCase):
    def test_reproduces_ab_run_1_medians(self):
        saved = json.loads((RUN1 / "summary-ab.json").read_text())
        recs = records_from_console(RUN1, RUN1 / "console.log")
        with tempfile.TemporaryDirectory() as t:
            new = summarize(recs, t, SETTING, 1.0, {"before": {}, "after": {"generate_extra": ["--timings"]}}, 5, quiet=True)
        for group, g in saved["groups"].items():
            for arm in ("before", "after"):
                self.assertEqual(new["groups"][group][arm]["median_wall_seconds"], g[arm]["median_wall_seconds"], (group, arm))
                self.assertEqual(new["groups"][group][arm]["walls"], g[arm]["walls"])
            self.assertEqual(new["groups"][group]["after"]["ratio_vs_before"], g["ratio_after_over_before"])
        self.assertEqual(new["groups"]["same"]["before"]["median_wall_seconds"], 15.007)
        self.assertEqual(new["groups"]["same"]["after"]["median_wall_seconds"], 5.41)
        old = {(r["stage"], r["parent"]): r["median_total_seconds"] for r in saved["after_stage_table"]["same"]}
        cur = {(r["stage"], r["parent"]): r["median_total_seconds"] for r in new["stage_tables"]["after"]["same"]}
        self.assertEqual(old, cur)

    def test_stage_row_without_total_seconds(self):
        recs = [{"name": "same-after-1", "group": "same", "arm": "after", "ok": True, "wall_seconds": 1.0,
                 "timings": [{"stage": "other command work", "seconds": 0.5}, {"stage": "x", "seconds": 0.1, "total_seconds": 0.3, "parent": None}, "junk"]}]
        rows = {r["stage"]: r for r in stage_table(recs, "after", "same")}
        self.assertEqual(rows["other command work"]["median_total_seconds"], 0.5)
        self.assertEqual(rows["x"]["median_total_seconds"], 0.3)

    def test_three_arm_share(self):
        def rec(arm, k, w): return {"name": f"same-{arm}-{k}", "group": "same", "arm": arm, "ok": True, "wall_seconds": w,
                                    "load_before": [0.9], "load_after": [1.0], "timings": None}
        recs = [rec("before", k, 15.0) for k in range(1, 6)] + [rec("after", k, 5.0) for k in range(1, 6)] + [rec("vc48", k, 9.0) for k in range(1, 6)]
        recs += [{"name": "same-before-warmup", "group": "same", "arm": "before", "ok": True, "wall_seconds": 99.0}]  # warm-up excluded
        g = group_summary(recs, ["before", "after", "vc48"], "same")
        self.assertEqual(g["before"]["median_wall_seconds"], 15.0)
        self.assertEqual(g["vc48"]["ratio_vs_before"], 0.6)
        s = g["vibecomfy_fix_share"]
        self.assertEqual((s["total_saving_before_minus_after_s"], s["saving_without_vibecomfy_fix_before_minus_vc48_s"],
                          s["vibecomfy_fix_saving_vc48_minus_after_s"]), (10.0, 6.0, 4.0))
        self.assertEqual((s["vibecomfy_fix_share_of_total_saving"], s["agent_only_share_of_total_saving"]), (0.4, 0.6))

    def test_missing_arm_and_empty(self):
        g = group_summary([], ["before", "after", "vc48"], "timeline")
        self.assertIsNone(g["after"]["median_wall_seconds"]); self.assertIsNone(g["vibecomfy_fix_share"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
