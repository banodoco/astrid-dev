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

    def test_playwright_json_has_stable_project_and_nested_titles(self):
        with tempfile.TemporaryDirectory() as p:
            f = Path(p) / "playwright.json"
            f.write_text(json.dumps({"suites": [{"title": "tests/e2e/a.spec.ts", "file": "/work/tests/e2e/a.spec.ts", "suites": [{"title": "editor", "specs": [{"title": "save and reopen", "file": "/work/tests/e2e/a.spec.ts", "tests": [{"projectName": "chromium-desktop", "status": "expected"}, {"projectName": "chromium-mobile", "status": "flaky"}]}]}]}]}))
            self.assertEqual(mod.parse_playwright_json(f), {
                "tests/e2e/a.spec.ts › [chromium-desktop] › editor › save and reopen": "PASS",
                "tests/e2e/a.spec.ts › [chromium-mobile] › editor › save and reopen": "FAIL",
            })

    def test_playwright_json_requires_native_results(self):
        with tempfile.TemporaryDirectory() as p:
            f = Path(p) / "playwright.json"
            f.write_text(json.dumps({"suites": [{"title": "file", "specs": []}]}))
            with self.assertRaisesRegex(ValueError, "no Playwright per-test records"):
                mod.parse_playwright_json(f)

    def test_e2e_dot_logs_with_no_ids_block_qualification(self):
        with tempfile.TemporaryDirectory() as p:
            a, b = Path(p) / "base.log", Path(p) / "candidate.log"
            a.write_text("   555 passed\n   27 failed\n")
            b.write_text("   552 passed\n   30 failed\n")
            records = {"app": {"baseline": {"E2E": {"jobs": [{"id": 1, "name": "playwright-default", "conclusion": "failure", "log": str(a)}]}},
                               "candidate": {"E2E": {"jobs": [{"id": 2, "name": "playwright-default", "conclusion": "failure", "log": str(b)}]}}}}
            _, _, issues = mod.evaluate({}, records, Path(p), {}, {})
            self.assertTrue(any("complete native Playwright JSON required" in x for x in issues))

    def test_explained_pass_to_fail_remains_blocking(self):
        with tempfile.TemporaryDirectory() as p:
            a, b = Path(p) / "base.log", Path(p) / "candidate.log"
            a.write_text("  ✓  1 tests/e2e/a.spec.ts:10:1 › save works (1s)\n")
            b.write_text("  ✘  1 tests/e2e/a.spec.ts:15:1 › save works (1s)\n")
            manifest = {"dispositions": {"app/Direct Journey/tests/e2e/a.spec.ts › save works": {"reason": "investigation", "source": "https://example.com/evidence"}}}
            records = {"app": {"baseline": {"Direct Journey": {"jobs": [{"id": 1, "name": "direct-journey", "conclusion": "success", "log": str(a)}]}},
                               "candidate": {"Direct Journey": {"jobs": [{"id": 2, "name": "direct-journey", "conclusion": "failure", "log": str(b)}]}}}}
            _, _, issues = mod.evaluate(manifest, records, Path(p), {}, {})
            self.assertTrue(any("BLOCKS publish" in x for x in issues))

    def test_failed_disappearance_needs_reconciled_present_destination(self):
        with tempfile.TemporaryDirectory() as p:
            a, b = Path(p) / "a", Path(p) / "b"
            a.write_text("FAILED tests/a.py::test_old - failure\n")
            b.write_text("PASSED tests/a.py::test_other\n")
            records = {"agent": {"baseline": {"CI": {"jobs": [{"id": 1, "name": "unit shard 1", "conclusion": "failure", "log": str(a)}]}}, "candidate": {"CI": {"jobs": [{"id": 2, "name": "unit shard 1", "conclusion": "failure", "log": str(b)}]}}}}
            _, _, issues = mod.evaluate({}, records, Path(p), {})
            self.assertTrue(any("disappearance requires" in issue for issue in issues))
            manifest = {"test_id_renames": {"agent/CI/tests/a.py::test_old": {"to": "tests/a.py::test_other", "reason": "renamed", "source": "evidence"}}}
            _, _, issues = mod.evaluate(manifest, records, Path(p), {})
            self.assertFalse(any("disappearance requires" in issue for issue in issues))

    def test_candidate_only_job_enumerates_ids_and_blocks_failure(self):
        with tempfile.TemporaryDirectory() as p:
            a, b = Path(p) / "a", Path(p) / "b"
            a.write_text("PASSED tests/a.py::test_old\n")
            b.write_text("PASSED tests/b.py::test_new\nFAILED tests/b.py::test_bad - failure\n")
            records = {"agent": {"baseline": {"CI": {"jobs": [{"id": 1, "name": "unit shard 1", "conclusion": "success", "log": str(a)}]}}, "candidate": {"CI": {"jobs": [{"id": 2, "name": "unit shard 1", "conclusion": "success", "log": str(a)}, {"id": 3, "name": "unit shard 2", "conclusion": "failure", "log": str(b)}]}}}}
            rows, _, issues = mod.evaluate({}, records, Path(p), {})
            self.assertEqual({r["id"] for r in rows if r["job"] == "unit shard 2"}, {"tests/b.py::test_new", "tests/b.py::test_bad"})
            self.assertTrue(any("test_bad" in issue and "BLOCKS" in issue for issue in issues))

    def test_progress_only_ids_are_compared(self):
        with tempfile.TemporaryDirectory() as p:
            a, b = Path(p) / "a", Path(p) / "b"
            a.write_text("tests/x.py::test_vanished PASSED [ 50%]\nPASSED tests/x.py::test_common\n")
            b.write_text("tests/x.py::test_added[param with space] PASSED [ 50%]\nPASSED tests/x.py::test_common\n")
            records = {"agent": {"baseline": {"CI": {"jobs": [{"id": 1, "name": "unit shard 1", "conclusion": "success", "log": str(a)}]}}, "candidate": {"CI": {"jobs": [{"id": 2, "name": "unit shard 1", "conclusion": "success", "log": str(b)}]}}}}
            rows, _, issues = mod.evaluate({}, records, Path(p), {})
            by_id = {row["id"]: row for row in rows}
            self.assertEqual(by_id["tests/x.py::test_vanished"]["candidate"], "MISSING")
            self.assertTrue(any("test_vanished" in issue and "BLOCKS" in issue for issue in issues))
            self.assertEqual(by_id["tests/x.py::test_added[param with space]"]["candidate"], "PASS")
            self.assertEqual(by_id["tests/x.py::test_added[param with space]"]["r13"], "MISSING")

    def test_pytest_summary_wins_over_progress_regardless_of_order(self):
        self.assertEqual(mod.parse_pytest("FAILED tests/a.py::test_one - teardown\ntests/a.py::test_one PASSED [100%]\n"), {"tests/a.py::test_one": "FAIL"})

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
