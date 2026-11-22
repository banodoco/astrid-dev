"""Isolated native-parser and fail-closed tests; no network or paid calls."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

FILE = Path(__file__).with_name("publication_diff.py")
spec = importlib.util.spec_from_file_location("r14_publication_diff", FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestRealLogParserHardening(unittest.TestCase):
    """Small bounded regressions for downloaded-log formats and adverse merges."""

    def test_pytest_gh_prefix_and_duplicate_node_keep_strongest_adverse(self):
        log = "\n".join([
            "unit shard 8\tRun tests\t2026-11-22T02:24:53.4089686Z FAILED tests/a.py::test_same - assertion",
            "unit shard 8\tRun tests\t2026-11-22T02:24:53.4089686Z ERROR tests/a.py::test_same - fixture",
            "unit shard 8\tRun tests\t2026-11-22T02:24:53.4089686Z PASSED tests/a.py::test_same",
            "PASSED tests/a.py::green",
        ])
        self.assertEqual(mod.parse_pytest(log), {
            "tests/a.py::test_same": "ERROR", "tests/a.py::green": "PASS",
        })

    def test_pytest_adverse_over_green_in_both_progress_and_summary(self):
        log = "tests/a.py::test_case FAILED [ 50%]\nPASSED tests/a.py::test_case\n"
        self.assertEqual(mod.parse_pytest(log), {"tests/a.py::test_case": "FAIL"})

    def test_junit_keeps_failure_and_skip_red(self):
        with tempfile.TemporaryDirectory() as p:
            f = Path(p) / "results.xml"
            f.write_text('<testsuite><testcase classname="suite" name="red"><failure/></testcase>'
                         '<testcase classname="suite" name="skipped"><skipped/></testcase>'
                         '<testcase classname="suite" name="green"/></testsuite>')
            self.assertEqual(mod.parse_junit_xml(f), {
                "suite::red": "FAIL", "suite::skipped": "SKIP", "suite::green": "PASS",
            })

    def test_playwright_numbered_error_summary_recovers_failure_only(self):
        log = "##[error] 1) [chromium] › tests/e2e/a.spec.ts:19:3 › nested › failed title\n"
        self.assertEqual(mod.parse_playwright(log), {
            "tests/e2e/a.spec.ts › [chromium] › nested › failed title": "FAIL",
        })


class TestPlaywrightParserBoundaries(unittest.TestCase):
    def _report(self, tests):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / "pw.json"
        path.write_text(json.dumps({"suites": [{"title": "a.spec.ts", "file": "tests/a.spec.ts", "specs": [{"title": "case", "tests": tests}]}]}))
        return path

    def test_empty_null_and_absent_names_share_default_but_named_default_is_distinct(self):
        f = self._report([
            {"projectName": "", "status": "expected", "results": [{"status": "passed"}]},
            {"projectName": None, "status": "expected", "results": [{"status": "passed"}]},
            {"status": "expected", "results": [{"status": "passed"}]},
            {"projectName": "default", "status": "expected", "results": [{"status": "passed"}]},
        ])
        parsed = mod.parse_playwright_json(f)
        self.assertEqual(parsed["tests/a.spec.ts › [<default>] › case"], ["PASS"] * 3)
        self.assertEqual(parsed["tests/a.spec.ts › [default] › case"], "PASS")

    def test_retry_failure_is_adverse_and_full_native_results_are_exposed(self):
        results = [
            {"status": "failed", "retry": 0, "workerIndex": 1, "error": {"message": "first attempt"}},
            {"status": "passed", "retry": 1, "workerIndex": 2, "duration": 14},
        ]
        f = self._report([{"status": "flaky", "expectedStatus": "passed", "results": results}])
        self.assertEqual(mod.parse_playwright_json(f)["tests/a.spec.ts › [<default>] › case"], "FAIL")
        audit = mod.parse_playwright_json_outcomes(f)["tests/a.spec.ts › [<default>] › case"][0]
        self.assertEqual((audit["expected"], audit["actual"], audit["status"]), ("PASS", "PASS", "FAIL"))
        self.assertEqual(audit["retries"], results)

    def test_skipped_case_stays_skip_even_when_expected_status_is_failed(self):
        f = self._report([{"status": "skipped", "expectedStatus": "failed", "results": []}])
        self.assertEqual(mod.parse_playwright_json(f)["tests/a.spec.ts › [<default>] › case"], "SKIP")
        audit = mod.parse_playwright_json_outcomes(f)["tests/a.spec.ts › [<default>] › case"][0]
        self.assertEqual(audit, {"expected": "FAIL", "actual": "MISSING", "status": "PASS"})

    def test_expected_status_skipped_is_retained_independently(self):
        f = self._report([{"status": "expected", "expectedStatus": "skipped", "results": [{"status": "skipped"}]}])
        audit = mod.parse_playwright_json_outcomes(f)["tests/a.spec.ts › [<default>] › case"][0]
        self.assertEqual(audit, {"expected": "SKIP", "actual": "SKIP", "status": "PASS"})


class TestPublicationDiff(unittest.TestCase):
    def test_playwright_outcomes_retain_expected_and_actual_separately(self):
        with tempfile.TemporaryDirectory() as p:
            f = Path(p) / "pw.json"
            f.write_text(json.dumps({"suites": [{"title": "a.spec.ts", "file": "tests/a.spec.ts", "specs": [{"title": "known failure", "tests": [{"projectName": "chromium", "status": "expected", "expectedStatus": "failed", "results": [{"status": "failed"}]}]}]}]}))
            self.assertEqual(mod.parse_playwright_json_outcomes(f), {
                "tests/a.spec.ts › [chromium] › known failure": [{"expected": "FAIL", "actual": "FAIL", "status": "PASS"}]
            })

    def test_inherited_red_inventory_is_shrink_only_and_requires_real_baseline_red(self):
        baseline = {"repo": "app", "workflow": "E2E", "job": "pw", "id": "tests/a.spec.ts › [chromium] › known failure", "status": "FAIL"}
        valid = {"approved_prior": [baseline], "current": [baseline]}
        self.assertEqual(mod.validate_inherited_failures(valid, [baseline]), [])
        extra = dict(baseline, id="tests/a.spec.ts › [chromium] › invented")
        self.assertTrue(mod.validate_inherited_failures({"approved_prior": [baseline], "current": [baseline, extra]}, [baseline]))
        self.assertTrue(mod.validate_inherited_failures({"approved_prior": [], "current": []}, [baseline]))
        self.assertTrue(mod.validate_inherited_failures({"approved_prior": [baseline], "current": []}, []))

    def test_candidate_reds_must_be_approved_by_current_inventory(self):
        fail = {"repo": "app", "workflow": "E2E", "job": "pw", "id": "failure", "status": "FAIL"}
        prior_only = {"approved_prior": [fail], "current": []}
        self.assertTrue(mod.validate_inherited_failures(prior_only, [fail], [fail]))
        self.assertTrue(mod.validate_inherited_failures({"approved_prior": [], "current": []}, [], [fail]))

    def test_unchanged_skip_and_error_are_red_and_need_current_approval(self):
        for status in ("SKIP", "ERROR"):
            row = {"repo": "app", "workflow": "E2E", "job": "pw", "id": status.lower(), "status": status}
            approved = {"approved_prior": [row], "current": [row]}
            self.assertEqual(mod.validate_inherited_failures(approved, [row], [row]), [])
            self.assertTrue(mod.validate_inherited_failures({"approved_prior": [row], "current": []}, [row], [row]))

    def test_playwright_json_uses_expected_actual_and_default_project(self):
        with tempfile.TemporaryDirectory() as p:
            f = Path(p) / "pw.json"
            f.write_text(json.dumps({"suites": [{"title": "a.spec.ts", "file": "tests/a.spec.ts", "specs": [{"title": "works", "tests": [{"status": "unexpected", "expectedStatus": "passed", "results": [{"status": "failed"}]}]}]}]}))
            result = mod.parse_playwright_json(f)
            self.assertEqual(result, {"tests/a.spec.ts › [<default>] › works": "FAIL"})

    def test_playwright_duplicate_test_identity_preserves_counts(self):
        with tempfile.TemporaryDirectory() as p:
            f = Path(p) / "pw.json"
            f.write_text(json.dumps({"suites": [{"title": "a.spec.ts", "file": "tests/a.spec.ts", "specs": [{"title": "works", "tests": [{"projectName": "chromium", "status": "expected", "results": [{"status": "passed"}]}, {"projectName": "chromium", "status": "expected", "results": [{"status": "passed"}]}]}]}]}))
            self.assertEqual(mod.parse_playwright_json(f), {"tests/a.spec.ts › [chromium] › works": ["PASS", "PASS"]})

    def test_playwright_skip_is_not_a_pass(self):
        with tempfile.TemporaryDirectory() as p:
            f = Path(p) / "pw.json"
            f.write_text(json.dumps({"suites": [{"title": "a.spec.ts", "file": "tests/a.spec.ts", "specs": [{"title": "works", "tests": [{"projectName": "chromium", "status": "skipped"}]}]}]}))
            self.assertEqual(set(mod.parse_playwright_json(f).values()), {"SKIP"})

    def test_setup_failure_and_missing_id_are_visible_per_job_attempt(self):
        with tempfile.TemporaryDirectory() as p:
            a, b = Path(p) / "a.log", Path(p) / "b.log"
            a.write_text("ERROR tests/a.py::test_setup - setup failed\n")
            b.write_text("")
            records = {"agent": {"baseline": {"CI": {"jobs": [{"id": 1, "attempt": 1, "name": "unit shard 1", "conclusion": "failure", "log": str(a)}]}}, "candidate": {"CI": {"jobs": [{"id": 2, "attempt": 2, "name": "unit shard 1", "conclusion": "success", "log": str(b)}]}}}}
            rows, jobs, problems = mod.evaluate({}, records, Path(p), {})
            self.assertEqual(rows[0]["candidate"], "MISSING")
            self.assertEqual(jobs[0].get("candidate_attempt"), 2)
            self.assertTrue(any("test_setup" in issue and "BLOCKS" in issue for issue in problems))

    def test_new_failing_added_id_is_blocking(self):
        with tempfile.TemporaryDirectory() as p:
            a, b = Path(p) / "a.log", Path(p) / "b.log"
            a.write_text("")
            b.write_text("SKIPPED tests/a.py::test_new - skip\nFAILED tests/a.py::test_bad - failure\n")
            records = {"agent": {"baseline": {"CI": {"jobs": [{"id": 1, "name": "unit shard 1", "conclusion": "success", "log": str(a)}]}}, "candidate": {"CI": {"jobs": [{"id": 2, "name": "unit shard 1", "conclusion": "failure", "log": str(b)}]}}}}
            _, _, problems = mod.evaluate({}, records, Path(p), {})
            self.assertTrue(any("test_bad" in issue and "BLOCKS" in issue for issue in problems))
            self.assertTrue(any("test_new" in issue and "BLOCKS" in issue for issue in problems))

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
            f.write_text(json.dumps({"suites": [{"title": "tests/e2e/a.spec.ts", "file": "/work/tests/e2e/a.spec.ts", "suites": [{"title": "editor", "specs": [{"title": "save and reopen", "file": "/work/tests/e2e/a.spec.ts", "tests": [{"projectName": "chromium-desktop", "status": "expected", "results": [{"status": "passed"}]}, {"projectName": "chromium-mobile", "status": "flaky", "results": [{"status": "failed"}]}]}]}]}]}))
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

    def test_junit_xml_is_supported_and_retains_duplicate_cases(self):
        with tempfile.TemporaryDirectory() as p:
            f = Path(p) / "junit.xml"
            f.write_text('<testsuite><testcase classname="tests.a" name="one"/><testcase classname="tests.a" name="one"><failure/></testcase></testsuite>')
            self.assertEqual(mod.parse_junit_xml(f), {"tests.a::one": ["PASS", "FAIL"]})

    def test_evaluate_compares_duplicate_junit_occurrences(self):
        with tempfile.TemporaryDirectory() as p:
            old_report, new_report = Path(p) / "old.xml", Path(p) / "new.xml"
            old_report.write_text('<testsuite><testcase classname="src.a" name="duplicate"/><testcase classname="src.a" name="duplicate"><failure/></testcase></testsuite>')
            new_report.write_text('<testsuite><testcase classname="src.a" name="duplicate"><failure/></testcase><testcase classname="src.a" name="duplicate"/><testcase classname="src.a" name="duplicate"><failure/></testcase></testsuite>')
            log = Path(p) / "vitest.log"
            log.write_text("")
            records = {"app": {"baseline": {"Tests": {"jobs": [{"id": 1, "name": "vitest", "conclusion": "success", "log": str(log)}]}},
                                "candidate": {"Tests": {"jobs": [{"id": 2, "name": "vitest", "conclusion": "success", "log": str(log)}]}}}}
            rows, _, issues = mod.evaluate({}, records, Path(p), {}, junit={"baseline": old_report, "candidate": new_report})
            self.assertEqual([(row["r13"], row["candidate"], row["classification"]) for row in rows], [
                ("FAIL", "FAIL", "same"), ("PASS", "PASS", "same"), ("MISSING", "FAIL", "failing-added"),
            ])
            self.assertTrue(any("added 1 FAIL occurrence(s) BLOCKS publish" in issue for issue in issues))

    def test_playwright_default_project_and_missing_actual_fail_closed(self):
        with tempfile.TemporaryDirectory() as p:
            f = Path(p) / "pw.json"
            f.write_text(json.dumps({"suites": [{"title": "a.spec.ts", "file": "tests/a.spec.ts", "specs": [{"title": "works", "tests": [
                {"status": "expected", "expectedStatus": "failed", "results": [{"status": "failed"}]},
                {"projectName": "default", "status": "expected", "results": [{"status": "failed"}]},
                {"status": "expected", "expectedStatus": "passed", "results": []}
            ]}]}]}))
            result = mod.parse_playwright_json(f)
            self.assertIn("[<default>]", next(iter(result)))
            self.assertTrue(any("[default]" in key for key in result))
            self.assertEqual({s for value in result.values() for s in (value if isinstance(value, list) else [value])}, {"FAIL"})

    def test_duplicate_occurrence_comparison_is_order_independent(self):
        self.assertEqual(mod.multiset_diff(["PASS", "FAIL"], ["FAIL", "PASS"]), {})


class TestPublicationDiffEvaluatorRows(unittest.TestCase):
    def test_job_inventory_attempts_and_approved_red_ceiling(self):
        with tempfile.TemporaryDirectory() as p:
            log = Path(p) / "run.log"
            log.write_text("FAILED tests/a.py::test_bad - assertion\n")
            records = {"agent": {"baseline": {"CI": {"id": 10, "attempt": 1, "jobs": [{"id": 101, "attempt": 1, "name": "unit shard", "conclusion": "failure", "log": str(log)}]}}, "candidate": {"CI": {"id": 20, "attempt": 2, "jobs": [{"id": 202, "attempt": 2, "name": "unit shard", "conclusion": "failure", "log": str(log)}]}}}}
            rows, jobs, problems = mod.evaluate({}, records, Path(p), {}, approved_counts={("agent", "CI", "unit shard", "tests/a.py::test_bad"): 1})
            self.assertEqual(jobs[0]["candidate_attempt"], 2)
            self.assertEqual(rows[0]["candidate"], "FAIL")
            self.assertFalse(any("exceed approval ceiling" in x for x in problems))

    def test_setup_is_job_row_even_with_native_ids_and_no_random_setup_mentions(self):
        with tempfile.TemporaryDirectory() as p:
            bad, good = Path(p) / "bad.log", Path(p) / "good.log"
            bad.write_text("FAILED tests/a.py::test_x - assertion\n")
            good.write_text("setup test passed\nPASSED tests/a.py::test_x\n")
            rec = {"agent": {"baseline": {"CI": {"jobs": [{"id": 1, "name": "unit shard", "conclusion": "failure", "failed_steps": ["Install dependencies"], "log": str(bad)}]}}, "candidate": {"CI": {"jobs": [{"id": 2, "name": "unit shard", "conclusion": "success", "log": str(good)}]}}}}
            rows, _, issues = mod.evaluate({}, rec, Path(p), {})
            self.assertTrue(any(r["id"] == "[job]" and r.get("kind") == "job" for r in rows))
            self.assertFalse(any("setup/collection failure" in x for x in issues))

    def test_candidate_only_and_baseline_only_workflows_are_reported(self):
        with tempfile.TemporaryDirectory() as p:
            log = Path(p) / "x.log"; log.write_text("PASSED tests/a.py::test_x\n")
            rec = {"agent": {"baseline": {"CI": {"jobs": [{"id": 1, "name": "unit shard", "conclusion": "success", "log": str(log)}]}}, "candidate": {"Lanes": {"jobs": [{"id": 2, "attempt": 3, "name": "unit shard", "conclusion": "success", "log": str(log)}]}}}}
            rows, jobs, issues = mod.evaluate({}, rec, Path(p), {})
            self.assertTrue(any("workflow missing" in x for x in issues))
            self.assertTrue(any(j["workflow"] == "Lanes" and j["candidate_job_id"] == 2 for j in jobs))
            self.assertTrue(any(j["workflow"] == "CI" and j["r13_job_id"] == 1 for j in jobs))

class TestReviewedInventory(unittest.TestCase):
    def test_duplicate_allowance_can_shrink_and_never_exceed_prior(self):
        entry = {"repo": "app", "workflow": "Tests", "job": "vitest", "id": "duplicate", "count": 2}
        inventory = {"schema_version": 1, "sealed_prior": [entry], "current": [dict(entry, count=1)]}
        approved, problems = mod.reviewed_inherited_red_counts(inventory)
        self.assertEqual(approved[("app", "Tests", "vitest", "duplicate")], 1)
        self.assertEqual(problems, [])
        inventory["current"] = [dict(entry, count=3)]
        _, problems = mod.reviewed_inherited_red_counts(inventory)
        self.assertTrue(any("exceeds the sealed prior" in problem for problem in problems))

    def test_fixed_requires_removal_and_missing_evidence_cannot_prove_fixed(self):
        key = ("runtime", "CI", "unit", "test")
        row = dict(zip(("product", "workflow", "job", "id"), key))
        for outcome, message in (("PASS", "fixed occurrence"), ("MISSING", "lack R14 evidence")):
            self.assertIn(message, mod.check_inherited_red_observations({key: 1}, [dict(row, candidate=outcome)])[0])
        self.assertEqual(mod.check_inherited_red_observations({}, [dict(row, candidate="PASS")]), [])

    def test_proposal_preserves_status_counts_and_job_binding(self):
        row = {"product": "vibecomfy", "workflow": "ci", "job": "browser-boot", "id": "[job]", "kind": "job",
               "r13": "FAIL", "candidate": "ERROR", "candidate_job": "browser-boot", "candidate_job_id": 11,
               "candidate_run_id": 10, "candidate_attempt": 2}
        proposal = mod.inherited_red_proposal([row, dict(row, r13="PASS", candidate="SKIP")])
        self.assertEqual([entry["classification"] for entry in proposal["reds"]], ["red-on-both", "R14-only"])
        self.assertEqual([entry["occurrence"] for entry in proposal["reds"]], [1, 2])
        self.assertEqual([entry["attempt"] for entry in proposal["reds"]], [2, 2])
        self.assertEqual(proposal["counts"]["vibecomfy"]["r14_red"], 2)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "candidate.json"
            mod.write_inherited_red_candidate_list(output, proposal)
            self.assertEqual(json.loads(output.read_text()), proposal)
            with self.assertRaises(FileExistsError):
                mod.write_inherited_red_candidate_list(output, proposal)
            self.assertEqual(json.loads(output.read_text()), proposal)


class TestFreezeVerdict(unittest.TestCase):
    def test_pytest_outer_summary_excludes_nested_capture_and_retains_other_steps(self):
        log = """##[group]Run first pytest command
tests/a.py::test_run FAILED [100%]
----------------------------- Captured stdout call -----------------------------
=========================== short test summary info ============================
FAILED check_it.py::test_child - intentional failure
1 failed in 0.01s
=========================== short test summary info ============================
PASSED tests/a.py::test_passed
Context from a wrapped assertion
FAILED tests/a.py::test_run - assertion
1 failed, 1 passed in 0.10s
##[group]Run second pytest command
=========================== short test summary info ============================
PASSED tests/b.py::test_other
1 passed in 0.10s
"""
        self.assertEqual(mod.parse_pytest(log), {
            "tests/a.py::test_run": "FAIL", "tests/a.py::test_passed": "PASS", "tests/b.py::test_other": "PASS",
        })

    def test_collector_links_jobs_to_explicit_attempt(self):
        with tempfile.TemporaryDirectory() as directory:
            sha = "a" * 40
            source = {"sha": sha, "workflows": {"ci": 10}, "attempts": {"ci": 2}}
            manifest = {side: {"vibecomfy": source} for side in ("baseline", "candidate")}
            run = {"id": 10, "head_sha": sha, "name": "ci", "status": "completed",
                   "run_attempt": 2, "conclusion": "failure"}
            job = {"name": "browser-boot", "status": "completed", "conclusion": "failure", "id": 20,
                   "run_attempt": 2, "steps": [{"name": "Install browsers", "conclusion": "failure"}]}
            prefix = "/VibeComfy/actions/runs/10/attempts/2"
            receipts = {prefix: run, f"{prefix}/jobs?per_page=100&page=1": {"jobs": [job]}}
            with mock.patch.object(mod, "REPO", {"vibecomfy": "VibeComfy"}), mock.patch.object(
                    mod, "get_json", side_effect=receipts.__getitem__), mock.patch.object(
                    mod, "api", return_value=b"install failed\n") as logs:
                records = mod.collect_runs(manifest, Path(directory))
                for side in manifest:
                    record = records["vibecomfy"][side]["ci"]["jobs"][0]
                    self.assertEqual((record["id"], record["attempt"]), (20, 2))
                    self.assertEqual(record["failed_steps"], ["Install browsers"])
                    self.assertEqual(Path(record["log"]).read_bytes(), b"install failed\n")
                self.assertEqual(logs.call_args_list, [mock.call("/VibeComfy/actions/jobs/20/logs")] * 2)
                job["run_attempt"] = 1
                with self.assertRaisesRegex(ValueError, "another attempt"):
                    mod.collect_runs(manifest, Path(directory))

    def test_cli_blocks_new_skip_and_stale_review_but_accepts_current_review(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            log = root / "job.log"
            log.write_text("installation output\n")
            manifest, inventory, proposal = (root / name for name in ("manifest.json", "approved.json", "proposed.json"))
            manifest.write_text("{}")
            base = {"name": "browser-boot", "id": 1, "attempt": 1, "conclusion": "failure",
                    "failed_steps": ["Install dependencies"], "log": str(log)}
            candidate = dict(base, id=2, attempt=2)
            skipped = dict(base, name="installer", id=3, attempt=2, conclusion="skipped", failed_steps=[])
            records = {product: {"baseline": {}, "candidate": {}} for product in mod.REPO}
            records["vibecomfy"]["baseline"]["ci"] = {"id": 10, "attempt": 1, "conclusion": "failure", "jobs": [base]}
            records["vibecomfy"]["candidate"]["ci"] = {"id": 20, "attempt": 2, "conclusion": "failure",
                                                        "jobs": [candidate, skipped]}
            accepted = [{"repo": "vibecomfy", "workflow": "ci", "job": job, "id": "[job]"}
                        for job in ("browser-boot", "installer")]
            current = dict(schema_version=1, sealed_prior=accepted, current=accepted[:1])
            inventory.write_text(json.dumps(current))
            args = ["--manifest", str(manifest), "--inherited-red", str(inventory), "--out", str(root / "out")]
            with mock.patch.object(mod, "collect_runs", return_value=records), mock.patch.object(
                    mod, "check_canonical_baseline_diff", return_value=[]):
                self.assertEqual(mod.main([*args, "--generate-candidate-list", str(proposal)]), 1)
                self.assertEqual(json.loads(inventory.read_text()), current)
                proposed = json.loads(proposal.read_text())["reds"]
                self.assertEqual([(row["classification"], row["attempt"]) for row in proposed],
                                 [("red-on-both", 2), ("R14-only", 2)])
                current["current"] = accepted
                inventory.write_text(json.dumps(current))
                self.assertEqual(mod.main(args), 0)
                candidate.update(conclusion="success", failed_steps=[])
                self.assertEqual(mod.main(args), 1)
                self.assertIn("fixed occurrence", (root / "out" / "report.md").read_text())
                inventory.write_text(json.dumps(dict(current, current=accepted[1:])))
                self.assertEqual(mod.main(args), 0)

    def test_shard_move_retains_job_binding_and_proves_fixed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            records = {"agent": {"baseline": {"CI": {"jobs": []}}, "candidate": {"CI": {"jobs": []}}}}
            for side, observation, shard, number in (("baseline", "FAILED", 1, 10), ("candidate", "PASSED", 2, 20)):
                for index in (1, 2):
                    log = root / f"{side}-{index}.log"
                    log.write_text(f"{observation} tests/a.py::test_move\n" if index == shard
                                   else "PASSED tests/a.py::test_control\n")
                    records["agent"][side]["CI"]["jobs"].append({
                        "id": number + index, "name": f"unit shard {index}", "log": str(log),
                        "conclusion": "success", "attempt": index,
                    })
            rows, _, problems = mod.evaluate({}, records, root, {})
            self.assertEqual(problems, [])
            moved = next(row for row in rows if row["id"] == "tests/a.py::test_move")
            self.assertEqual((moved["r13_job_id"], moved["candidate_job_id"]), (11, 22))
            self.assertEqual((moved["r13_attempt"], moved["candidate_attempt"]), (1, 2))
            self.assertEqual(moved["classification"], "fixed")

    def test_collapsed_pytest_skips_visible_without_inventing_test_ids(self):
        log = "PASSED tests/a.py::test_pass\nSKIPPED [2] tests/a.py:4: platform"
        self.assertEqual(mod.pytest_job_results(log), ({"tests/a.py::test_pass": "PASS"}, 2))


if __name__ == "__main__":
    unittest.main()
