"""The lock-protected gate reading is the recorded command start load."""
import contextlib
import io
import json
import os
from pathlib import Path
import runpy
import subprocess
import tempfile
import unittest
from unittest.mock import patch


def attested(calls):
    from unittest.mock import Mock
    command = Mock(side_effect=calls)
    def run(args, **kwargs):
        if any(str(arg).endswith("runtime_attestation.py") for arg in args):
            Path(args[-1]).write_text(json.dumps({"port": int(args[-4]), "address_hex": "a", "socket_table": "tcp", "socket_inode": 1, "pid": 2, "start_ticks": 3, "exe": "x", "cwd": "x", "selected_version": "x", "manifest_shas": {}, "scope": "test"}))
            return subprocess.CompletedProcess(args, 0, "", "")
        return command(args, **kwargs)
    run.command = command
    return run


class GateReceipt(unittest.TestCase):
    def test_under_lock_reading_authorizes_and_records_start(self):
        with tempfile.TemporaryDirectory() as tmp:
            arm = {"launcher": "/fake", "home": tmp, "tmp": tmp, "door_port": 1234, "current": "/fake/current", "manifest": "/fake/manifest"}
            env = {"IB": tmp, "EVIDENCE_DIR": tmp, "COMFY_URL": "fake", "MEDIA_PNG": "fake",
                   "ARMS_JSON": json.dumps({"before": arm})}
            # The third reading is after the command; it must not become the start reading.
            loads = iter([(0.99, 0, 0), (0.99, 0, 0), (1.01, 0, 0)])
            def call(args, **kwargs):
                return subprocess.CompletedProcess(args, 0, '{"ok": true}', '')
            with patch.dict(os.environ, env, clear=True), patch("subprocess.run", side_effect=attested(call)), \
                 patch("os.getloadavg", side_effect=lambda: next(loads)), patch("fcntl.flock"), \
                 contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(SystemExit):
                    runpy.run_path(str(Path(__file__).with_name("ab_run.py")), run_name="__main__")
            row = json.loads((Path(tmp) / "records.jsonl").read_text())
            self.assertEqual(row["load_before"][0], 0.99)
            self.assertEqual(row["load_after"][0], 1.01)


    def test_retries_attestation_after_high_under_lock_load(self):
        with tempfile.TemporaryDirectory() as tmp:
            arm = {"launcher": "/fake", "home": tmp, "tmp": tmp, "door_port": 1234,
                   "current": "/fake/current", "manifest": "/fake/manifest"}
            env = {"IB": tmp, "EVIDENCE_DIR": tmp, "COMFY_URL": "fake", "MEDIA_PNG": "fake",
                   "ARMS_JSON": json.dumps({"before": arm})}
            loads = iter([(0.99, 0, 0), (1.01, 0, 0), (0.99, 0, 0), (0.98, 0, 0), (1.01, 0, 0)])
            runner = attested(lambda args, **kwargs: subprocess.CompletedProcess(args, 0, '{"ok": true}', ""))
            with patch.dict(os.environ, env, clear=True), patch("subprocess.run", side_effect=runner), \
                 patch("os.getloadavg", side_effect=lambda: next(loads)), patch("fcntl.flock"), \
                 patch("time.sleep"), contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(SystemExit):
                    runpy.run_path(str(Path(__file__).with_name("ab_run.py")), run_name="__main__")
            raw = Path(tmp) / "raw"
            self.assertTrue((raw / "same-before-warmup.listener-before-1.json").exists())
            self.assertTrue((raw / "same-before-warmup.listener-before-2.json").exists())
            row = json.loads((Path(tmp) / "records.jsonl").read_text())
            self.assertEqual(row["load_before"][0], 0.98)

    def test_duplicate_admissions_fail_qualification_and_keep_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            arms = {name: {"launcher": "/fake", "home": tmp, "tmp": tmp, "door_port": port, "current": "/fake/current", "manifest": "/fake/manifest"}
                    for name, port in (("before", 1234), ("after", 1235))}
            env = {"IB": tmp, "EVIDENCE_DIR": tmp, "COMFY_URL": "fake", "MEDIA_PNG": "fake",
                   "ARMS_JSON": json.dumps(arms), "SAMPLES": "1"}
            revisions = iter(f"revision-{n}" for n in range(4))
            def call(args, **kwargs):
                payload = {"ok": True}
                if args[1:3] == ["generate", "image"]:
                    payload["kernel_task_id"] = "duplicate"
                if args[1:3] == ["timelines", "edit"]:
                    payload["data"] = {"status": "accepted", "accepted_revision_id": next(revisions)}
                return subprocess.CompletedProcess(args, 0, json.dumps(payload), "")
            with patch.dict(os.environ, env, clear=True), patch("subprocess.run", side_effect=attested(call)), \
                 patch("os.getloadavg", return_value=(0.99, 0, 0)), patch("fcntl.flock"), \
                 contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as result:
                    runpy.run_path(str(Path(__file__).with_name("ab_run.py")), run_name="__main__")
            self.assertEqual(result.exception.code, 5)
            summary = json.loads((Path(tmp) / "summary-ab.json").read_text())
            self.assertFalse(summary["qualification"]["passed"])
            self.assertTrue((Path(tmp) / "records.jsonl").exists())
            self.assertTrue((Path(tmp) / "raw" / "timeline-after-1.stdout").exists())


if __name__ == "__main__":
    unittest.main()
