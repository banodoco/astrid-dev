"""Explicit fallback keeps receipt and qualification safeguards intact."""
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

from ab_summary import rebuild
from test_ab_qualification import records

ROOT = Path(__file__).resolve().parent


class AttestationSwitch(unittest.TestCase):
    def driver(self, directory, mode, *, invalid_receipt=False):
        arm = {"launcher": "/fake", "home": str(directory), "tmp": str(directory),
               "door_port": 1234, "current": "/fake/current", "manifest": "/fake/manifest"}
        env = {"IB": str(directory), "EVIDENCE_DIR": str(directory), "COMFY_URL": "fake",
               "MEDIA_PNG": "fake", "ARMS_JSON": json.dumps({"before": arm}), "SAMPLES": "1",
               "ASTRID_AB_ATTEST": mode}
        calls = []
        def run(args, **kwargs):
            calls.append(args)
            if any(str(arg).endswith("runtime_attestation.py") for arg in args):
                if mode == "off":
                    raise AssertionError("off must bypass listener attestation")
                Path(args[-1]).write_text(json.dumps({"port": 1234, "address_hex": "a", "socket_table": "tcp",
                    "socket_inode": 1, "pid": 2, "start_ticks": 3, "exe": "x", "cwd": "x",
                    "selected_version": "x", "manifest_shas": {}, "scope": "test"}))
                return subprocess.CompletedProcess(args, 0, "", "")
            payload = {"ok": True}
            if args[1:3] == ["generate", "image"] and not invalid_receipt:
                payload["kernel_task_id"] = f"task-{len(calls)}"
            if args[1:3] == ["timelines", "edit"]:
                payload["data"] = {"status": "accepted", "accepted_revision_id": f"revision-{len(calls)}"}
            return subprocess.CompletedProcess(args, 0, json.dumps(payload), "")
        with patch.dict(os.environ, env, clear=True), patch("subprocess.run", side_effect=run), \
             patch("os.getloadavg", return_value=(0.5, 0, 0)), patch("fcntl.flock"), \
             contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            try:
                runpy.run_path(str(ROOT / "ab_run.py"), run_name="__main__")
            except SystemExit:
                pass
        return calls

    def test_off_records_mode_and_does_not_call_listener(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            calls = self.driver(d, "off")
            self.assertTrue(calls)
            marker = json.loads((d / "records.jsonl").read_text().splitlines()[-1])
            self.assertTrue(marker["records_complete"])
            self.assertEqual(marker["attestation"], "off")
            self.assertEqual(marker["qualification_schema"], 3)
            summary = json.loads((d / "summary-ab.json").read_text())
            self.assertEqual(summary["attestation"], "off")

    def test_on_records_mode_and_checks_listener(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            calls = self.driver(d, "on")
            self.assertTrue(any(any(str(arg).endswith("runtime_attestation.py") for arg in call) for call in calls))
            marker = json.loads((d / "records.jsonl").read_text().splitlines()[-1])
            self.assertEqual(marker["attestation"], "on")
            self.assertEqual(marker["qualification_schema"], 2)
            self.assertEqual(json.loads((d / "summary-ab.json").read_text())["attestation"], "on")

    def test_off_still_rejects_invalid_generation_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            self.driver(d, "off", invalid_receipt=True)
            last = json.loads((d / "records.jsonl").read_text().splitlines()[-1])
            self.assertFalse(last["ok"])
            self.assertTrue(last["error"])
            self.assertFalse((d / "summary-ab.json").exists())

    def test_wrapper_rejects_invalid_switch(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(["bash", str(ROOT / "run-ab-installed.sh")],
                                    env=dict(os.environ, IB=tmp, ASTRID_AB_ATTEST="false"),
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("ASTRID_AB_ATTEST", result.stdout + result.stderr)

    def test_driver_rejects_invalid_switch_before_commands(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            self.assertEqual(self.driver(d, "false"), [])
            self.assertFalse((d / "records.jsonl").exists())

    def test_off_still_checks_selected_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            program = root / "program"
            version = program / "versions" / "one"
            version.mkdir(parents=True)
            (program / "current").write_text("one\n")
            (version / "manifest.json").write_text((ROOT / "manifest-candidate.json").read_text())
            launcher = program / "run-astrid"
            launcher.write_text("#!/bin/sh\nexit 0\n")
            launcher.chmod(0o755)
            fakebin = root / "bin"
            fakebin.mkdir()
            curl = fakebin / "curl"
            curl.write_text('#!/bin/sh\n: > "$3"\n')
            curl.chmod(0o755)
            out = root / "evidence"
            env = dict(os.environ, IB=tmp, EVIDENCE_DIR=str(out), ARMS="before", ASTRID_AB_ATTEST="off",
                       PATH=f'{fakebin}:{os.environ["PATH"]}')
            result = subprocess.run(["bash", str(ROOT / "run-ab-installed.sh")], env=env, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("arm: installed", result.stdout + result.stderr)
            self.assertFalse((out / "astrid-version-before.txt").exists())

    def test_rebuild_old_schema_is_on_and_off_schema_is_explicit(self):
        rows = records()
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            marker = {"records_complete": True, "count": len(rows), "arms": ["before", "after", "vc48"],
                      "samples": 5, "qualification_schema": 2, "load_max": 1.0}
            def write():
                (d / "records.jsonl").write_text("\n".join(json.dumps(r) for r in [*rows, marker]) + "\n")
            write()
            old = rebuild(d)
            self.assertEqual(old["attestation"], "on")
            self.assertFalse(old["qualification"]["passed"])
            self.assertTrue(any("listener attestation" in r for r in old["qualification"]["reasons"]))
            marker.update(qualification_schema=3, attestation="off")
            write()
            new = rebuild(d)
            self.assertEqual(new["attestation"], "off")
            self.assertTrue(new["qualification"]["passed"])
            rows[0].pop("kernel_task_id")
            write()
            self.assertFalse(rebuild(d)["qualification"]["passed"])

            for value in ("on", "invalid", None):
                marker["attestation"] = value
                write()
                with self.subTest(value=value), self.assertRaises(ValueError):
                    rebuild(d)
            marker.update(qualification_schema=2, attestation="off")
            write()
            with self.assertRaises(ValueError):
                rebuild(d)


if __name__ == "__main__":
    unittest.main()
