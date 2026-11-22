#!/usr/bin/env python3
"""Focused checks for timing values used in stage summaries."""
import unittest

from ab_summary import stage_table


class StageDurations(unittest.TestCase):
    def test_malformed_durations_are_rejected(self):
        for field in ("seconds", "total_seconds"):
            for value in (None, "1.0", True, -1, float("nan"), float("inf")):
                with self.subTest(field=field, value=value):
                    stage = {"stage": "load", "seconds": 1.0, "total_seconds": 2.0}
                    stage[field] = value
                    record = {"name": "same-after-1", "group": "same", "arm": "after",
                              "ok": True, "timings": [stage]}
                    with self.assertRaisesRegex(ValueError, f"invalid {field}"):
                        stage_table([record], "after", "same")

    def test_missing_seconds_is_rejected(self):
        record = {"name": "same-after-1", "group": "same", "arm": "after",
                  "ok": True, "timings": [{"stage": "load"}]}
        with self.assertRaisesRegex(ValueError, "invalid seconds"):
            stage_table([record], "after", "same")


if __name__ == "__main__":
    unittest.main()
