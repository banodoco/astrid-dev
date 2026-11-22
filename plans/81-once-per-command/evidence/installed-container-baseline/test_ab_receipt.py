"""Generation receipts must substantiate successful timed runs."""
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from ab_receipt import generation_error

ROOT = Path(__file__).resolve().parent
ARGS = ["generate", "image", "prompt", "--timings"]
VALID = {"ok": True, "kernel_task_id": "task-1", "collector_span_seconds": 1.0,
         "timings": [{"stage": "other command work", "seconds": 1.0}]}


class ReceiptTests(unittest.TestCase):
    def test_receipt_contract(self):
        self.assertIsNone(generation_error(VALID, ARGS))
        self.assertIsNone(generation_error({"kernel_task_id": "task-1"}, ARGS[:-1]))
        self.assertIsNone(generation_error({}, ["projects", "create"]))
        for field, bad in (("kernel_task_id", None), ("kernel_task_id", ""),
                           ("timings", None), ("timings", []),
                           ("collector_span_seconds", None), ("collector_span_seconds", float("nan")),
                           ("timings", [{"stage": "x", "seconds": "1"}]),
                           ("timings", [{"stage": "x", "seconds": 1, "total_seconds": -1}])):
            with self.subTest(field=field, bad=bad):
                self.assertIsNotNone(generation_error(dict(VALID, **{field: bad}), ARGS))

    def test_driver_records_failure_and_preserves_raw_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            launcher = d / "launcher"
            launcher.write_text('#!/usr/bin/env python3\nimport json, sys\n'
                                'print(json.dumps({"ok": True} if sys.argv[1] != "generate" else '
                                '{"ok": True, "kernel_task_id": "task-1"}))\n')
            launcher.chmod(0o755)
            arm = {"launcher": str(launcher), "home": tmp, "tmp": tmp, "door_port": 1234,
                   "generate_extra": ["--timings"], "current": "/fake/current", "manifest": "/fake/manifest"}
            env = dict(os.environ, IB=tmp, EVIDENCE_DIR=tmp, COMFY_URL="test", MEDIA_PNG="test",
                       ARMS_JSON=json.dumps({"after": arm}), LOAD_MAX="1000000", SAMPLES="1")
            for filename in ("ab_run.py", "ab_summary.py", "ab_receipt.py"):
                shutil.copy(ROOT / filename, d / filename)
            (d / "runtime_attestation.py").write_text(
                'import json, sys\n'
                'json.dump({"port": int(sys.argv[1]), "address_hex": "a", "socket_table": "tcp", '
                '"socket_inode": 1, "pid": 2, "start_ticks": 3, "exe": "x", "cwd": "x", '
                '"selected_version": "x", "manifest_shas": {}, "scope": "test"}, open(sys.argv[4], "w"))\n')
            result = subprocess.run([sys.executable, str(d / "ab_run.py")], env=env, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            record = json.loads((d / "records.jsonl").read_text().splitlines()[-1])
            self.assertFalse(record["ok"])
            self.assertIn("missing requested timings", record["error"])
            self.assertEqual(json.loads((d / "raw" / "same-after-warmup.stdout").read_text())["kernel_task_id"], "task-1")
            self.assertFalse((d / "summary-ab.json").exists())


if __name__ == "__main__":
    unittest.main()
