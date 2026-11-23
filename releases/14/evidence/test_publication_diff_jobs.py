import importlib.util
import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path

FILE = Path(__file__).with_name("publication_diff.py")
spec = importlib.util.spec_from_file_location("jobs_publication_diff", FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class JobEvaluatorRegressions(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def job(self, name, conclusion, log="", steps=()):
        path = self.root / f"{name}-{len(list(self.root.iterdir()))}.log"
        path.write_text(log)
        return {"name": name, "id": len(list(self.root.iterdir())), "attempt": 1,
                "conclusion": conclusion, "log": str(path), "failed_steps": list(steps), "log_error": None}

    def records(self, product, workflow, before, after):
        result = {key: {"baseline": {}, "candidate": {}} for key in mod.REPO}
        result[product]["baseline"][workflow] = {"id": 1, "sha": "a", "conclusion": "success", "attempt": 1, "jobs": before}
        result[product]["candidate"][workflow] = {"id": 2, "sha": "b", "conclusion": "failure", "attempt": 1, "jobs": after}
        return result

    def evaluate(self, records, manifest=None, **kwargs):
        return mod.evaluate(manifest or {}, records, self.root, {}, **kwargs)

    def test_failed_job_with_red_test_id_also_emits_blocking_job_failure(self):
        log = "FAILED tests/a.py::bad - assertion\n"
        rows, _, problems = self.evaluate(self.records("agent", "CI", [self.job("unit shard 1", "success")],
                                                          [self.job("unit shard 1", "failure", log)]))
        self.assertTrue(any(row["kind"] == "job" and row["candidate"] == "FAIL" for row in rows))
        self.assertTrue(any("[job]" in issue and "BLOCKS" in issue for issue in problems))

    def test_approved_skip_cannot_mask_collection_error(self):
        summary = "===== short test summary info =====\nPASSED tests/a.py::ok\nSKIPPED [1] tests/a.py:3: why\n"
        err = summary + "ERROR tests/new.py - ImportError: boom\n"
        approved = Counter({("agent", "CI", "unit shard 1", "[unattributed skip]"): 1})
        rows, _, problems = self.evaluate(self.records("agent", "CI", [self.job("unit shard 1", "success", summary)],
                                                          [self.job("unit shard 1", "failure", err, ["Run tests"])]), approved_counts=approved)
        self.assertTrue(any("parse" in issue.lower() or "malformed" in issue.lower() for issue in problems))
        self.assertTrue(any(row.get("parse_error") for row in rows))

    def test_skip_groups_keep_location_and_reason_identity(self):
        parser = getattr(mod, "pytest_job_evidence", None)
        self.assertIsNotNone(parser)
        _, skips, errors = parser("SKIPPED [1] tests/a.py:3: old reason\nSKIPPED [1] tests/b.py:8: new reason\n")
        self.assertEqual(skips, Counter({("tests/a.py:3", "old reason"): 1, ("tests/b.py:8", "new reason"): 1}))
        self.assertEqual(errors, [])

    def test_malformed_failed_lines_create_diagnostic_nonapprovable_rows(self):
        parser = getattr(mod, "pytest_job_evidence", None)
        self.assertIsNotNone(parser)
        outcomes, _, errors = parser("FAILED tests/a.py::broken[ - detail\nERROR tests/c.py\n")
        self.assertEqual(outcomes, {})
        self.assertEqual(errors, ["FAILED tests/a.py::broken[ - detail", "ERROR tests/c.py"])

    def test_no_ids_exception_requires_exact_manifest_key_and_reason(self):
        blank = self.records("agent", "CI", [self.job("windows smoke", "success")],
                              [self.job("windows smoke", "success")])
        _, _, problems = self.evaluate(blank)
        self.assertTrue(any("no_ids_expected" in p for p in problems))
        approved = {"no_ids_expected": {"baseline/agent/CI/windows smoke": "smoke-only workflow",
                                        "candidate/agent/CI/windows smoke": "smoke-only workflow"}}
        _, _, problems = self.evaluate(blank, approved)
        self.assertFalse(any("no_ids_expected" in p for p in problems))

    def test_setup_failure_exception_requires_exact_key_and_reason(self):
        records = self.records("agent", "CI", [self.job("unit shard 1", "failure", "", ["Install dependencies"])],
                               [self.job("unit shard 1", "failure", "", ["Install dependencies"])])
        manifest = {"setup_failure_ok": {"baseline/agent/CI/unit shard 1": "dependency installation fails before collection",
                                         "candidate/agent/CI/unit shard 1": "dependency installation fails before collection"}}
        _, jobs, problems = self.evaluate(records, manifest)
        self.assertTrue(all(job["r13_setup"] if "r13_setup" in job else job["candidate_setup"] for job in jobs))
        self.assertFalse(any("complete test ID inventory required" in p for p in problems))

    def test_setup_named_test_step_does_not_qualify_as_setup(self):
        records = self.records("vibecomfy", "ci", [self.job("test", "failure", "", ["Build and test"])],
                               [self.job("test", "failure", "", ["Build and test"])])
        manifest = {"setup_failure_ok": {"baseline/vibecomfy/ci/test": "paired setup failure"},
                    "no_ids_expected": {"candidate/vibecomfy/ci/test": "non-test declaration"}}
        _, _, problems = self.evaluate(records, manifest,
                                       approved_counts={("vibecomfy", "ci", "test", "[job]"): 1})
        self.assertTrue(any("(candidate)" in p and "setup_failure_ok" in p for p in problems))

    def test_changed_unattributed_skip_does_not_match_old_group(self):
        summary = "===== short test summary info =====\nPASSED tests/a.py::test_ok\n"
        total = "\n== 1 passed, 1 skipped in 1s ==\n"
        before = summary + "SKIPPED [1] tests/a.py:3: old reason" + total
        after = summary + "SKIPPED [1] tests/zzz.py:9: brand new skip" + total
        records = self.records("agent", "CI", [self.job("unit shard 1", "success", before)],
                               [self.job("unit shard 1", "success", after)])
        rows, _, problems = self.evaluate(records, approved_counts={
            ("agent", "CI", "unit shard 1", "[unattributed skip]"): 1,
        })
        skips = {row["id"]: (row["r13"], row["candidate"]) for row in rows if row["kind"] == "job"}
        self.assertEqual(skips, {
            "[unattributed skip] tests/a.py:3: old reason": ("SKIP", "MISSING"),
            "[unattributed skip] tests/zzz.py:9: brand new skip": ("MISSING", "SKIP"),
        })
        self.assertTrue(any("no IDs" in problem and "tests/zzz.py:9" in problem for problem in problems))

    def test_setup_exception_uses_exact_tuple_and_any_failed_step(self):
        records = self.records("app", "E2E", [self.job("playwright-chromium", "failure", "", ["Compile widget"])],
                               [self.job("playwright-chromium", "failure", "", ["Arbitrary custom step"])])
        key0 = "baseline/app/E2E/playwright-chromium"
        key1 = "candidate/app/E2E/playwright-chromium"
        manifest = {"setup_failure_ok": {key0: "setup did not reach tests", key1: "setup did not reach tests"}}
        _, jobs, problems = self.evaluate(records, manifest)
        self.assertTrue(all(job["r13_setup"] for job in jobs))
        self.assertFalse(any("native Playwright JSON required" in p or "no_ids_expected" in p for p in problems))
        self.assertIn(key0, manifest["setup_failure_ok"])

    def test_app_and_skipped_jobs_require_no_ids_exception(self):
        records = self.records("app", "E2E", [self.job("playwright-chromium", "skipped")],
                               [self.job("playwright-chromium", "skipped")])
        _, _, problems = self.evaluate(records)
        self.assertGreaterEqual(sum("no_ids_expected" in p for p in problems), 2)
        approved = {"no_ids_expected": {
            "baseline/app/E2E/playwright-chromium": "conditionally skipped",
            "candidate/app/E2E/playwright-chromium": "conditionally skipped",
        }}
        _, _, problems = self.evaluate(records, approved)
        self.assertFalse(any("no_ids_expected" in p for p in problems))

    def test_job_approval_requires_exact_failed_tuple_and_never_approves_new_red(self):
        records = self.records("agent", "CI", [self.job("unit shard 1", "failure")],
                               [self.job("unit shard 1", "failure")])
        approved = Counter({("agent", "CI", "unit shard 1", "[job]"): 1})
        rows, _, problems = self.evaluate(records, approved_counts=approved)
        self.assertTrue(any(r["kind"] == "job" and r["r13"] == r["candidate"] == "FAIL" for r in rows))
        self.assertFalse(any("approved [job]" in p for p in problems))
        moved = self.records("agent", "CI", [self.job("unit shard 1", "success")],
                             [self.job("unit shard 1", "failure")])
        _, _, problems = self.evaluate(moved, approved_counts=approved)
        self.assertTrue(any("exact failed counterpart" in p for p in problems))

    def test_xpass_is_preserved_as_changed_outcome(self):
        report = self.root / "xpass.json"
        report.write_text(json.dumps({"suites": [{"title": "a.spec.ts", "file": "tests/a.spec.ts",
            "specs": [{"title": "known", "tests": [{"projectName": "chromium", "status": "unexpected",
                "expectedStatus": "failed", "results": [{"status": "passed"}]}]}]}]}))
        key = "candidate/E2E/playwright-chromium"
        original = mod.parse_playwright_json
        mod.parse_playwright_json = lambda _path: {"tests/a.spec.ts › known": "XPASS"}
        self.addCleanup(setattr, mod, "parse_playwright_json", original)
        records = self.records("app", "E2E", [self.job("playwright-chromium", "success")],
                               [self.job("playwright-chromium", "success")])
        rows, _, problems = self.evaluate(records, {"no_ids_expected": {
            "baseline/app/E2E/playwright-chromium": "no native test records"}},
            playwright={key: report})
        row = next(r for r in rows if r.get("id") == "tests/a.spec.ts › known")
        self.assertEqual(row["candidate"], "XPASS")
        self.assertEqual(row["classification"], "changed")
        self.assertTrue(any("BLOCKS" in p for p in problems))

    def test_checkout_lanes_accepts_native_vitest_report_without_dropping_occurrences(self):
        report = {"testResults": [{"name": "/work/app/tests/e2e/checkout.test.ts",
            "assertionResults": [
                {"fullName": "checkout > accepts card", "status": "passed"},
                {"fullName": "checkout > accepts card", "status": "passed"},
            ]}]}
        baseline_path = self.root / "checkout-baseline.json"
        candidate_path = self.root / "checkout-candidate.json"
        baseline_path.write_text(json.dumps(report))
        report["testResults"][0]["assertionResults"][1]["status"] = "failed"
        candidate_path.write_text(json.dumps(report))
        rows, _, problems = self.evaluate(self.records("app", "Lanes",
            [self.job("checkout-lanes", "success")], [self.job("checkout-lanes", "failure")]),
            playwright={"baseline/Lanes/checkout-lanes": baseline_path,
                        "candidate/Lanes/checkout-lanes": candidate_path})
        self.assertFalse(any("native Playwright JSON required" in problem for problem in problems))
        outcome_rows = [row for row in rows if row.get("id") == "tests/e2e/checkout.test.ts › checkout > accepts card"]
        self.assertEqual(len(outcome_rows), 2)
        self.assertEqual(Counter((row["r13"], row["candidate"]) for row in outcome_rows),
                         Counter({("PASS", "PASS"): 1, ("PASS", "FAIL"): 1}))

    def test_checkout_vitest_skipped_assertion_is_not_a_pass(self):
        path = self.root / "checkout-skipped.json"
        path.write_text(json.dumps({"testResults": [{"name": "tests/checkout.test.ts", "assertionResults": [
            {"fullName": "card", "status": "pending"}]}]}))
        records = self.records("app", "Lanes", [self.job("checkout-lanes", "success")],
                               [self.job("checkout-lanes", "success")])
        rows, _, _ = self.evaluate(records, playwright={
            "baseline/Lanes/checkout-lanes": path, "candidate/Lanes/checkout-lanes": path})
        row = next(row for row in rows if row["id"] == "tests/checkout.test.ts › card")
        self.assertEqual((row["r13"], row["candidate"]), ("SKIP", "SKIP"))

    def test_known_app_native_job_format_mismatches_are_rejected(self):
        playwright_path = self.root / "wrong-playwright.json"
        playwright_path.write_text(json.dumps({"suites": [{"title": "checkout.test.ts", "file": "tests/checkout.test.ts",
            "specs": [{"title": "card", "tests": [{"status": "expected", "expectedStatus": "passed",
                "results": [{"status": "passed"}]}]}]}]}))
        vitest_path = self.root / "wrong-vitest.json"
        vitest_path.write_text(json.dumps({"testResults": [{"name": "/app/tests/x.test.ts", "assertionResults": [
            {"fullName": "x", "status": "passed"}]}]}))
        checkout_records = self.records("app", "Lanes", [self.job("checkout-lanes", "success")],
                                        [self.job("checkout-lanes", "success")])
        _, _, checkout_problems = self.evaluate(checkout_records, playwright={
            "baseline/Lanes/checkout-lanes": playwright_path, "candidate/Lanes/checkout-lanes": playwright_path})
        self.assertTrue(any("expected native vitest JSON, received playwright" in issue for issue in checkout_problems))
        e2e_records = self.records("app", "E2E", [self.job("playwright-chromium", "success")],
                                   [self.job("playwright-chromium", "success")])
        _, _, e2e_problems = self.evaluate(e2e_records, playwright={
            "baseline/E2E/playwright-chromium": vitest_path, "candidate/E2E/playwright-chromium": vitest_path})
        self.assertTrue(any("expected native playwright JSON, received vitest" in issue for issue in e2e_problems))

    def test_checkout_lanes_skips_reject_supplied_native_input(self):
        path = self.root / "checkout.json"
        path.write_text(json.dumps({"testResults": [{"name": "tests/checkout.test.ts", "assertionResults": [
            {"fullName": "checkout", "status": "passed"}]}]}))
        records = self.records("app", "Lanes", [self.job("checkout-lanes", "skipped")],
                               [self.job("checkout-lanes", "skipped")])
        _, _, problems = self.evaluate(records, {"no_ids_expected": {
            "baseline/app/Lanes/checkout-lanes": "conditionally skipped",
            "candidate/app/Lanes/checkout-lanes": "conditionally skipped"}}, playwright={
            "baseline/Lanes/checkout-lanes": path, "candidate/Lanes/checkout-lanes": path})
        self.assertGreaterEqual(sum("native input supplied for a skipped job" in issue for issue in problems), 2)


    def test_playwright_xpass_or_unexpected_pass_is_changed(self):
        report = self.root / "pw.json"
        report.write_text(json.dumps({"suites": [{"title": "a.spec.ts", "file": "tests/a.spec.ts", "specs": [{"title": "known", "tests": [{"projectName": "chromium", "status": "unexpected", "expectedStatus": "failed", "results": [{"status": "passed"}]}]}]}]}))
        key = "candidate/E2E/playwright-chromium"
        original = mod.parse_playwright_json
        mod.parse_playwright_json = lambda _path: {"tests/a.spec.ts › known": "XPASS"}
        self.addCleanup(setattr, mod, "parse_playwright_json", original)
        rows, _, problems = self.evaluate(self.records("app", "E2E", [self.job("playwright-chromium", "success")],
                                                          [self.job("playwright-chromium", "success")]),
                                          playwright={key: report})
        row = next(row for row in rows if row["id"] == "tests/a.spec.ts › known")
        self.assertEqual(row["candidate"], "XPASS")
        self.assertEqual(row["classification"], "changed")
        self.assertTrue(any("BLOCKS" in p for p in problems))

    def test_pytest_xfail_state_is_preserved_for_comparator(self):
        rows, _, problems = self.evaluate(self.records("agent", "CI",
            [self.job("unit shard 1", "success", "PASSED tests/a.py::known\n")],
            [self.job("unit shard 1", "success", "XFAIL tests/a.py::known - still broken\n")]))
        row = next(row for row in rows if row["id"] == "tests/a.py::known")
        self.assertEqual((row["r13"], row["candidate"], row["classification"]), ("PASS", "XFAIL", "regressed"))
        self.assertTrue(any("XFAIL" in problem and "BLOCKS publish" in problem for problem in problems))


if __name__ == "__main__":
    unittest.main()
