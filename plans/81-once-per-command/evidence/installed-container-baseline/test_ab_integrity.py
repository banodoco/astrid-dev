#!/usr/bin/env python3
"""Isolated evidence-integrity checks; no installed programs or historical data required."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from ab_summary import summarize

SCRIPT = Path(__file__).resolve().parent / "ab_summary.py"
ARMS = {"before": {}, "after": {}}
SAMPLES = 5


def complete_records():
    return [
        {"name": f"{group}-{arm}-{index}", "group": group, "arm": arm,
         "ok": True, "exit_code": 0, "wall_seconds": float(k + 1),
         "load_before": [0.1], "load_after": [0.1], "timings": None}
        for group in ("same", "changed", "timeline")
        for arm in ARMS
        for k, index in enumerate(["warmup", *range(1, SAMPLES + 1)])
    ]


def marker(records):
    return {"records_complete": True, "count": len(records),
            "arms": list(ARMS), "samples": SAMPLES}


class Integrity(unittest.TestCase):
    def test_summary_requires_every_expected_successful_sample(self):
        valid = complete_records()
        variants = []
        variants.append(valid[:-1])
        variants.append(valid + [valid[-1]])
        failed = [dict(r) for r in valid]
        failed[-1]["ok"] = False
        variants.append(failed)
        bad_warmup = [dict(r) for r in valid]
        bad_warmup[0]["ok"] = False
        variants.append(bad_warmup)
        for records in variants:
            with self.subTest(count=len(records), last=records[-1]), tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises((ValueError, RuntimeError)):
                    summarize(records, tmp, "test", 1.0, ARMS, SAMPLES, quiet=True)
                self.assertFalse((Path(tmp) / "summary-ab.json").exists())

    def test_complete_reconstructed_records_can_be_summarized(self):
        records = [dict(r, reconstructed=True) for r in complete_records()]
        with tempfile.TemporaryDirectory() as tmp:
            result = summarize(records, tmp, "reconstructed from console", 1.0, ARMS, SAMPLES, quiet=True)
            self.assertEqual(result["groups"]["same"]["before"]["succeeded"], SAMPLES)
            self.assertTrue(all(r["reconstructed"] for r in result["records"]))

    def test_cli_rejects_missing_invalid_or_nonfinal_completion_marker(self):
        records = complete_records()
        good = [json.dumps(r) for r in records]
        end = json.dumps(marker(records))
        variants = [good, good + ['{bad json'], good + [json.dumps([]), end],
                    good + [json.dumps(dict(marker(records), count=1))],
                    good + [end, json.dumps(records[0])],
                    good[:-1] + [end]]
        for lines in variants:
            with self.subTest(last=lines[-1]), tempfile.TemporaryDirectory() as tmp:
                d = Path(tmp)
                (d / "records.jsonl").write_text("\n".join(lines) + "\n")
                result = subprocess.run([sys.executable, str(SCRIPT), str(d)], capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertFalse((d / "summary-ab.json").exists())

    def test_cli_accepts_complete_records_with_marker(self):
        records = complete_records()
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "records.jsonl").write_text("\n".join(json.dumps(r) for r in [*records, marker(records)]) + "\n")
            result = subprocess.run([sys.executable, str(SCRIPT), str(d)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            summary = json.loads((d / "summary-ab.json").read_text())
            self.assertEqual(summary["groups"]["same"]["before"]["succeeded"], SAMPLES)


if __name__ == "__main__":
    unittest.main()
