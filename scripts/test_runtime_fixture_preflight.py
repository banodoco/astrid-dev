"""Focused coverage for the Runtime fixture preflight used by cmp-run.sh."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Optional

SCRIPT = Path(__file__).resolve().parents[1] / "env" / "runtime-fixture-preflight.py"
FIXTURES = ("test_verified_host_launch", "test_remote_worker_activation")


class RuntimeFixturePreflightTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.agent = self.root / "agent"
        self.runtime = self.root / "runtime"
        (self.agent / "tests").mkdir(parents=True)
        (self.agent / "tests" / "__init__.py").write_text("", encoding="utf-8")
        (self.runtime / "runtime_protocol").mkdir(parents=True)
        (self.runtime / "runtime_protocol" / "__init__.py").write_text("", encoding="utf-8")
        (self.runtime / "tests").mkdir()
        for name in FIXTURES:
            (self.runtime / "tests" / f"{name}.py").write_text("FIXTURE = True\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_preflight(self, runtime_import_root: Optional[Path] = None) -> subprocess.CompletedProcess:
        env = os.environ.copy()
        env["PYTHONPATH"] = os.pathsep.join(
            str(path) for path in (runtime_import_root or self.runtime, self.agent)
        )
        env["PYTHONNOUSERSITE"] = "1"
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(self.agent), str(self.runtime)],
            cwd=self.root,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_imports_both_fixtures_from_pinned_runtime(self) -> None:
        result = self.run_preflight()
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in FIXTURES:
            self.assertIn(f"Runtime fixture OK: tests.{name}", result.stdout)

    def test_missing_fixture_is_environment_failure(self) -> None:
        (self.runtime / "tests" / f"{FIXTURES[0]}.py").unlink()
        result = self.run_preflight()
        self.assertEqual(result.returncode, 3)
        self.assertIn("ENV: pinned Runtime producer fixtures are missing", result.stderr)

    def test_wrong_runtime_import_origin_is_environment_failure(self) -> None:
        other = self.root / "installed-runtime"
        (other / "runtime_protocol").mkdir(parents=True)
        (other / "runtime_protocol" / "__init__.py").write_text("", encoding="utf-8")
        result = self.run_preflight(other)
        self.assertEqual(result.returncode, 3)
        self.assertIn("ENV: runtime_protocol resolves outside the pinned Runtime checkout", result.stderr)


if __name__ == "__main__":
    unittest.main()
