#!/usr/bin/env python3
"""Driver failure and isolation checks with mocked subprocess and load gate."""
import contextlib
import io
import json
import os
import runpy
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parent / "ab_run.py"


def result(stdout='{"ok": true}', code=0, stderr=""):
    return subprocess.CompletedProcess(["fake"], code, stdout, stderr)


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


class DriverIntegrity(unittest.TestCase):
    def run_driver(self, directory, calls):
        arms = {name: {"launcher": "/fake/launcher", "home": f"/fake/{name}",
                       "tmp": f"/fake/{name}/tmp", "door_port": port, "current": "/fake/current", "manifest": "/fake/manifest"}
                for name, port in (("before", 17340), ("after", 17341))}
        env = {"IB": "/fake", "EVIDENCE_DIR": str(directory), "COMFY_URL": "http://fake",
               "MEDIA_PNG": "/fake/media.png", "ARMS_JSON": json.dumps(arms), "SAMPLES": "1"}
        real_open = open
        def open_for_test(file, *args, **kwargs):
            if str(file) == "/tmp/astrid-timing.lock":
                return contextlib.nullcontext(io.StringIO())
            return real_open(file, *args, **kwargs)
        runner = attested(calls)
        command = runner.command
        with patch.dict(os.environ, env, clear=True), patch("subprocess.run", side_effect=runner), \
             patch("os.getloadavg", return_value=(0.0, 0.0, 0.0)), patch("fcntl.flock"), \
             patch("builtins.open", side_effect=open_for_test), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit):
                runpy.run_path(str(SCRIPT), run_name="__main__")
        return command

    def test_bad_sample_aborts_with_raw_and_failure_record(self):
        failures = [result("bad json"), result("[]"), result("{}"), result('{"ok": false}'),
                    result('{"ok": true}', 1),
                    subprocess.TimeoutExpired(["fake"], 900, output=b"partial", stderr=b"timeout"),
                    FileNotFoundError("launcher missing")]
        for failure in failures:
            with self.subTest(failure=repr(failure)), tempfile.TemporaryDirectory() as tmp:
                d = Path(tmp)
                command = self.run_driver(d, [result(), result(), result(), result(), failure])
                self.assertEqual(command.call_count, 5)
                records = [json.loads(line) for line in (d / "records.jsonl").read_text().splitlines()]
                self.assertEqual(len(records), 1)
                self.assertFalse(records[0]["ok"])
                self.assertTrue(records[0]["error"])
                self.assertFalse((d / "summary-ab.json").exists())
                self.assertTrue((d / "raw" / "same-before-warmup.stdout").exists())
                self.assertTrue((d / "raw" / "same-before-warmup.stderr").exists())
                if isinstance(failure, subprocess.TimeoutExpired):
                    self.assertEqual((d / "raw" / "same-before-warmup.stdout").read_text(), "partial")
                    self.assertEqual((d / "raw" / "same-before-warmup.stderr").read_text(), "timeout")

    def test_setup_uses_distinct_arm_ports_and_aborts_on_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            command = self.run_driver(d, [result(), result(), result("{}")])
            self.assertEqual(command.call_count, 3)
            ports = [call.kwargs["env"]["ASTRID_RUNTIME_DOOR_PORT"] for call in command.call_args_list]
            self.assertEqual(ports, ["17340", "17340", "17341"])
            records = [json.loads(line) for line in (d / "records.jsonl").read_text().splitlines()]
            self.assertEqual(len(records), 1)
            self.assertFalse(records[0]["ok"])
            self.assertFalse((d / "summary-ab.json").exists())


if __name__ == "__main__":
    unittest.main()
