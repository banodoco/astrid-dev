"""A zero exit is insufficient when the readiness receipt is invalid."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

READINESS = Path(__file__).resolve().parent / "runtime-readiness.sh"


class RuntimeReadinessJSON(unittest.TestCase):
    def test_invalid_zero_exit_receipts_fail_with_output_preserved(self):
        for response in ("not json", "[]", '{"ok": false}', '{}'):
            with self.subTest(response=response), tempfile.TemporaryDirectory() as tmp:
                d = Path(tmp)
                launcher = d / "launcher"
                launcher.write_text('#!/bin/sh\necho attempt >> "$CALLS"\nprintf "%s\\n" "$RESPONSE"\necho "launcher warning" >&2\n')
                launcher.chmod(0o755)
                sleep = d / "sleep"
                sleep.write_text('#!/bin/sh\nexit 0\n')
                sleep.chmod(0o755)
                log = d / "readiness.log"
                env = dict(os.environ, PATH=f"{d}:{os.environ['PATH']}", CALLS=str(d / "calls"), RESPONSE=response)
                proc = subprocess.run(["bash", "-c", 'source "$1"; runtime_ready "$2" after "$3"',
                                       "bash", str(READINESS), str(launcher), str(log)],
                                      env=env, text=True, capture_output=True)
                self.assertNotEqual(proc.returncode, 0)
                self.assertEqual((d / "calls").read_text().splitlines(), ["attempt"] * 4)
                self.assertIn(response, log.read_text())
                self.assertIn("launcher warning", log.read_text())
                self.assertIn("ok=true", log.read_text())

    def test_valid_receipt_with_stderr_succeeds(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            launcher = d / "launcher"
            launcher.write_text('#!/bin/sh\necho \'{"ok": true}\'\necho warning >&2\n')
            launcher.chmod(0o755)
            proc = subprocess.run(["bash", "-c", 'source "$1"; runtime_ready "$2" after "$3"',
                                   "bash", str(READINESS), str(launcher), str(d / "log")],
                                  text=True, capture_output=True)
            self.assertEqual(proc.returncode, 0)
            self.assertIn("warning", (d / "log.stderr").read_text())


if __name__ == "__main__":
    unittest.main()
