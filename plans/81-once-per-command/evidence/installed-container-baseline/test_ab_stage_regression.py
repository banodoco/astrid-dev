"""Regression coverage for command-level stage accounting and summary ratios."""
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from ab_summary import stage_table, summarize


class StageSummaryRegression(unittest.TestCase):
    def test_committed_historical_stage_totals(self):
        path = Path(__file__).resolve().parent / "ab-run-2" / "records.jsonl"
        entries = [json.loads(line) for line in path.read_text().splitlines()]
        self.assertTrue(entries[-1]["records_complete"])
        rows = stage_table(entries[:-1], "after", "same")
        row = next(r for r in rows if (r["stage"], r["parent"]) ==
                   ("pack discovery", "candidate qualification"))
        self.assertEqual(row["occurrences_seen"], 30)
        self.assertEqual(row["median_seconds"], 0.0984)
        self.assertEqual(row["median_command_occurrences"], 6)
        self.assertEqual(row["median_command_seconds"], 0.5958)

    def test_command_totals_include_absent_occurrences_and_do_not_sum_inclusive(self):
        def rec(k, timings):
            return {"name": f"same-after-{k}", "group": "same", "arm": "after", "ok": True, "timings": timings}
        def stage(seconds, total):
            return {"stage": "x", "parent": "p", "seconds": seconds, "total_seconds": total}
        rows = stage_table([rec(1, [stage(.2, 2), stage(.3, 3)]),
                            rec(2, []), rec(3, [stage(.1, 4)])], "after", "same")
        row = rows[0]
        self.assertEqual(row["occurrences_seen"], 3)
        self.assertEqual(row["median_seconds"], .2)
        self.assertEqual(row["median_total_seconds"], 3)
        self.assertEqual(row["median_command_seconds"], .1)
        self.assertEqual(row["median_command_occurrences"], 1)

    def test_summary_prints_command_totals_and_distinct_arm_ratios(self):
        arms = {a: {"generate_extra": ["--timings"]} for a in ("before", "after", "vc48")}
        walls = {"before": 10, "after": 4, "vc48": 7}
        records = []
        for group in ("same", "changed", "timeline"):
            for arm in arms:
                for k in ("warmup", 1, 2, 3, 4, 5):
                    records.append({"name": f"{group}-{arm}-{k}", "group": group, "arm": arm,
                                    "ok": True, "exit_code": 0, "wall_seconds": walls[arm],
                                    "load_before": [.1], "timings": [
                                        {"stage": "x", "seconds": .2}, {"stage": "x", "seconds": .3}]})
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()) as output:
            result = summarize(records, tmp, "fixture", 1., arms, 5)
        self.assertEqual(result["groups"]["same"]["after"]["ratio_vs_before"], .4)
        self.assertEqual(result["groups"]["same"]["vc48"]["ratio_vs_before"], .7)
        self.assertIn("0.500 s exclusive/command", output.getvalue())
        self.assertIn("0.250 s exclusive/occurrence", output.getvalue())


if __name__ == "__main__":
    unittest.main()
