"""Isolated native-parser and fail-closed tests; no network or paid calls."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

FILE = Path(__file__).with_name("publication_diff.py")
spec = importlib.util.spec_from_file_location("r14_publication_diff", FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestPublicationDiff(unittest.TestCase):
    def test_pytest_gha_lines_and_expected_failures(self):
        log = "\n".join([
            "2026-11-21T14:00:00.000Z PASSED tests/a.py::test_one",
            "2026-11-21T14:00:00.000Z FAILED tests/a.py::test_two[with space] - assertion",
            "2026-11-21T14:00:00.000Z ERROR tests/a.py::test_three - setup",
            "2026-11-21T14:00:00.000Z XFAIL tests/a.py::test_four",
        ])
        self.assertEqual(mod.parse_pytest(log), {
            "tests/a.py::test_one": "PASS",
            "tests/a.py::test_two[with space]": "FAIL",
            "tests/a.py::test_three": "ERROR",
            "tests/a.py::test_four": "XFAIL",
        })

    def test_id_parser_does_not_strip_param_with_spaces(self):
        self.assertEqual(mod.pytest_id("tests/a.py::test_case[a b c] - reason"), "tests/a.py::test_case[a b c]")
        self.assertIsNone(mod.pytest_id("tests/a.py"))

    def test_playwright_preserves_nested_title_without_line_number(self):
        log = "2026-11-17T12:05:06.9176781Z   ✓  31 tests/e2e/local/direct-journey.spec.ts:839:3 › restarts › it works (1.4s)"
        self.assertEqual(mod.parse_playwright(log), {
            "tests/e2e/local/direct-journey.spec.ts › restarts › it works": "PASS"
        })

    def test_playwright_failed_and_skipped(self):
        log = "  ✘  2 tests/e2e/foo.spec.ts:91:7 › failure (1.2s)\n  -  3 tests/e2e/foo.spec.ts:92:7 › skip"
        self.assertEqual(mod.parse_playwright(log), {
            "tests/e2e/foo.spec.ts › failure": "FAIL", "tests/e2e/foo.spec.ts › skip": "SKIP"
        })

    def test_vitest_requires_assertion_results(self):
        with tempfile.TemporaryDirectory() as p:
            f = Path(p) / "report.json"
            f.write_text(json.dumps({"testResults": [{"name": "src/a.test.ts", "status": "passed"}]}))
            with self.assertRaisesRegex(ValueError, "assertionResults"):
                mod.parse_vitest_json(f)

    def test_vitest_per_id(self):
        with tempfile.TemporaryDirectory() as p:
            f = Path(p) / "report.json"
            f.write_text(json.dumps({"testResults": [{"name": "/x/src/foo.test.ts", "assertionResults": [
                {"fullName": "one > success", "status": "passed"},
                {"fullName": "one > refusal", "status": "failed"},
            ]}]}))
            self.assertEqual(mod.parse_vitest_json(f), {
                "src/foo.test.ts › one > success": "PASS", "src/foo.test.ts › one > refusal": "FAIL",
            })

    def test_frozen_sha_and_run_id_required_before_fetch(self):
        with self.assertRaisesRegex(ValueError, "frozen full SHA"):
            mod.collect_runs({"baseline": {"agent": {"sha": None}}}, Path("/tmp/unused"))

    def test_duplicate_vitest_id_refused(self):
        with tempfile.TemporaryDirectory() as p:
            f = Path(p) / "report.json"
            f.write_text(json.dumps({"testResults": [{"name": "src/a.test.ts", "assertionResults": [
                {"fullName": "duplicate", "status": "passed"},
                {"fullName": "duplicate", "status": "failed"}]}]}))
            with self.assertRaisesRegex(ValueError, "duplicate"):
                mod.parse_vitest_json(f)


if __name__ == "__main__":
    unittest.main()
