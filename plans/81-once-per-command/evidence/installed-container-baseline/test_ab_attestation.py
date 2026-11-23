"""The driver witnesses listener identity on both sides of each command."""
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
from ab_summary import qualification


class DriverAttestation(unittest.TestCase):
    def test_qualification_rejects_absent_listener_evidence(self):
        rows = [{"name": "same-before-1", "group": "same", "arm": "before",
                 "wall_seconds": 1, "load_before": [0.5], "door_port": 1234}]
        result = qualification(rows, ["before"], 1.0, require_attestation=True)
        self.assertTrue(any("listener attestation" in reason for reason in result["reasons"]))

    def run_driver(self, directory, failure=None):
        arm = {"launcher": "/fake", "home": str(directory), "tmp": str(directory), "door_port": 1234,
               "current": "/fake/current", "manifest": "/fake/manifest"}
        env = {"IB": str(directory), "EVIDENCE_DIR": str(directory), "COMFY_URL": "fake", "MEDIA_PNG": "fake",
               "ARMS_JSON": json.dumps({"before": arm}), "SAMPLES": "1"}
        attestations = []
        commands = []
        def call(args, **kwargs):
            if any(str(arg).endswith("runtime_attestation.py") for arg in args):
                attestations.append(args)
                if failure == "error" and len(attestations) == 2:
                    return subprocess.CompletedProcess(args, 1, "", "selected manifest mismatch")
                identity = {"port": 1234, "address_hex": "0100007F", "socket_table": "tcp",
                            "socket_inode": 10, "pid": 20 if failure == "changed" and len(attestations) == 2 else 19,
                            "start_ticks": 42, "exe": "/fake/exe", "cwd": "/fake",
                            "selected_version": "/fake/version", "manifest_shas": {
                                "agent": "a", "runtime": "b", "vibecomfy": "c", "lifecycle": "d"},
                            "scope": "test"}
                Path(args[-1]).write_text(json.dumps(identity))
                return subprocess.CompletedProcess(args, 0, "", "")
            commands.append(args)
            # After successful setup, stop at the first timed command with an invalid receipt.
            return subprocess.CompletedProcess(args, 0, '{"ok": true}', "")
        with patch.dict(os.environ, env, clear=True), patch("subprocess.run", side_effect=call), \
             patch("os.getloadavg", return_value=(0.5, 0, 0)), patch("fcntl.flock"), \
             contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                runpy.run_path(str(Path(__file__).with_name("ab_run.py")), run_name="__main__")
        return attestations, commands

    def test_success_checks_before_and_after_commands(self):
        with tempfile.TemporaryDirectory() as tmp:
            attestations, commands = self.run_driver(Path(tmp))
            self.assertEqual(len(attestations), 2 * len(commands))
            for call in attestations:
                self.assertEqual(call[-4:-1], ["1234", "/fake/current", "/fake/manifest"])

    def test_attestation_failure_or_changed_identity_fails_with_record(self):
        for failure in ("error", "changed"):
            with self.subTest(failure=failure), tempfile.TemporaryDirectory() as tmp:
                attestations, commands = self.run_driver(Path(tmp), failure)
                self.assertEqual(len(attestations), 2)
                self.assertEqual(len(commands), 1)
                records = [json.loads(line) for line in (Path(tmp) / "records.jsonl").read_text().splitlines()]
                self.assertFalse(records[-1]["ok"])
                self.assertTrue(records[-1]["error"])
                self.assertFalse((Path(tmp) / "summary-ab.json").exists())


if __name__ == "__main__":
    unittest.main()
