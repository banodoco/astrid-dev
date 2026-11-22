#!/usr/bin/env python3
"""Focused checks for reconstructed timing evidence disclosure."""
import tempfile
import unittest

from ab_summary import summarize


class ReconstructionCaveat(unittest.TestCase):
    def test_missing_collector_span_is_disclosed(self):
        records = [{"name": f"{group}-after-{sample}", "group": group, "arm": "after",
                    "ok": True, "exit_code": 0, "wall_seconds": 1.0,
                    "reconstructed": True}
                   for group in ("same", "changed", "timeline") for sample in ("warmup", 1)]
        with tempfile.TemporaryDirectory() as directory:
            result = summarize(records, directory, "historical", 1.0, {"after": {}}, 1, quiet=True)
        self.assertTrue(result["reconstructed"])
        self.assertIn("lack collector span data", result["interpretation"])
        self.assertNotIn("collector_span_seconds", result["records"][0])


if __name__ == "__main__":
    unittest.main()
