"""Regression checks for Runtime readiness retries without starting an install."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


READINESS = Path(__file__).resolve().parent / "runtime-readiness.sh"


class RuntimeReadiness(unittest.TestCase):
    def test_exhausted_retries_fail_and_keep_last_diagnostic(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            launcher = d / "launcher"
            launcher.write_text('#!/bin/sh\necho attempt >> "$CALLS"\necho "runtime unavailable" >&2\nexit 1\n')
            launcher.chmod(0o755)
            sleep = d / "sleep"
            sleep.write_text('#!/bin/sh\nexit 0\n')
            sleep.chmod(0o755)
            log = d / "readiness.log"
            env = dict(os.environ, PATH=f"{d}:{os.environ['PATH']}", CALLS=str(d / "calls"))
            proc = subprocess.run(
                ["bash", "-c", 'source "$1"; runtime_ready "$2" after "$3"',
                 "bash", str(READINESS), str(launcher), str(log)],
                env=env, text=True, capture_output=True,
            )
            self.assertNotEqual(proc.returncode, 0)
            self.assertEqual((d / "calls").read_text().splitlines(), ["attempt"] * 4)
            self.assertIn("runtime unavailable", log.read_text())
            self.assertIn(str(log), proc.stderr)


if __name__ == "__main__":
    unittest.main()
