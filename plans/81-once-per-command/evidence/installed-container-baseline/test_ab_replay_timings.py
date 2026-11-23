"""Replay rejects incomplete timing evidence unless explicitly importing history."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from ab_summary import rebuild, summarize

SCRIPT = Path(__file__).resolve().parent / "ab_summary.py"


def records():
    return [{"name": f"{group}-after-{sample}", "group": group, "arm": "after",
             "ok": True, "exit_code": 0, "wall_seconds": 1.0,
             "args": ["generate", "image", "--timings"] if group != "timeline" else ["timelines", "edit"],
             "timings": [{"stage": "work", "seconds": 0.5}], "collector_span_seconds": 1.0}
            for group in ("same", "changed", "timeline") for sample in ("warmup", 1)]


class ReplayTimings(unittest.TestCase):
    def test_rejects_missing_and_malformed_timing_data(self):
        for field, value in (("timings", None), ("timings", []), ("timings", ["junk"]),
                             ("timings", [{"stage": "x", "seconds": -1}]),
                             ("collector_span_seconds", None), ("collector_span_seconds", float("nan"))):
            data = records()
            data[0][field] = value
            with self.subTest(field=field, value=value), tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises(ValueError):
                    summarize(data, tmp, "test", 1, {"after": {}}, 1, quiet=True)
                self.assertFalse((Path(tmp) / "summary-ab.json").exists())

    def test_timed_rebuild_requires_schema(self):
        data = records()
        marker = {"records_complete": True, "count": len(data), "arms": ["after"], "samples": 1}
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            def write():
                (d / "records.jsonl").write_text("\n".join(json.dumps(r) for r in [*data, marker]) + "\n")
            write()
            missing = subprocess.run([sys.executable, str(SCRIPT), str(d)], capture_output=True, text=True)
            self.assertNotEqual(missing.returncode, 0)
            marker["timing_receipt_schema"] = 1
            write()
            valid = subprocess.run([sys.executable, str(SCRIPT), str(d)], capture_output=True, text=True)
            self.assertEqual(valid.returncode, 0, valid.stderr)

    def test_legacy_rebuild_requires_explicit_metadata(self):
        data = records()
        marker = {"records_complete": True, "count": len(data), "arms": ["after"], "samples": 1}
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "records.jsonl").write_text("\n".join(json.dumps(r) for r in [*data, marker]) + "\n")
            for args in ([], ["--arms", "after"], ["--samples", "1"]):
                result = subprocess.run([sys.executable, str(SCRIPT), str(d), "--legacy-records", *args], capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0, args)
            with self.assertRaises(ValueError):
                rebuild(d, legacy_missing_collector_span=True)

    def test_explicit_legacy_import_discloses_missing_span(self):
        data = records()
        for r in data:
            del r["collector_span_seconds"]
        marker = {"records_complete": True, "count": len(data)}
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "records.jsonl").write_text("\n".join(json.dumps(r) for r in [*data, marker]) + "\n")
            strict = subprocess.run([sys.executable, str(SCRIPT), str(d)], capture_output=True, text=True)
            self.assertNotEqual(strict.returncode, 0)
            legacy = subprocess.run([sys.executable, str(SCRIPT), str(d), "--legacy-records", "--arms", "after", "--samples", "1"], capture_output=True, text=True)
            self.assertEqual(legacy.returncode, 0, legacy.stderr)
            result = json.loads((d / "summary-ab.json").read_text())
            self.assertIn("spans are unverified", result["interpretation"])
            self.assertNotIn("collector_span_seconds", result["records"][0])


if __name__ == "__main__":
    unittest.main()
