"""Release 14 Playwright expected/actual status regressions."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

FILE = Path(__file__).with_name("publication_diff.py")
spec = importlib.util.spec_from_file_location("r14_playwright_diff", FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestPlaywrightExpectedActual(unittest.TestCase):
    def report(self, status, expected="passed", actual="passed", results=True):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / "playwright.json"
        case = {"projectName": "chromium", "status": status, "expectedStatus": expected}
        if results:
            case["results"] = [] if actual is None else [{"status": actual}]
        path.write_text(json.dumps({"suites": [{"title": "a.spec.ts", "file": "tests/a.spec.ts",
            "specs": [{"title": "case", "tests": [case]}]}]}))
        return path

    def audit(self, path):
        return next(iter(mod.parse_playwright_json_outcomes(path).values()))[0]

    def test_expected_failure_is_xfail_not_pass(self):
        path = self.report("expected", "failed", "failed")
        self.assertEqual(next(iter(mod.parse_playwright_json(path).values())), "XFAIL")
        self.assertEqual(self.audit(path), {"expected": "FAIL", "actual": "FAIL", "status": "XFAIL"})

    def test_unexpected_pass_is_xpass_and_audit_is_not_pass(self):
        path = self.report("unexpected", "failed", "passed")
        self.assertEqual(next(iter(mod.parse_playwright_json(path).values())), "XPASS")
        self.assertEqual(self.audit(path), {"expected": "FAIL", "actual": "PASS", "status": "XPASS"})

    def test_normal_pass_skip_and_flaky(self):
        passed = self.report("expected")
        skipped = self.report("skipped", "skipped", "skipped")
        flaky_results = [{"status": "failed", "retry": 0}, {"status": "passed", "retry": 1}]
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        flaky = Path(temp.name) / "flaky.json"
        flaky.write_text(json.dumps({"suites": [{"title": "a.spec.ts", "file": "tests/a.spec.ts",
            "specs": [{"title": "case", "tests": [{"status": "flaky", "expectedStatus": "passed", "results": flaky_results}]}]}]}))
        self.assertEqual(next(iter(mod.parse_playwright_json(passed).values())), "PASS")
        self.assertEqual(self.audit(passed)["status"], "PASS")
        self.assertEqual(next(iter(mod.parse_playwright_json(skipped).values())), "SKIP")
        self.assertEqual(self.audit(skipped)["status"], "SKIP")
        self.assertEqual(next(iter(mod.parse_playwright_json(flaky).values())), "FAIL")
        self.assertEqual(self.audit(flaky)["status"], "FAIL")
        self.assertEqual(self.audit(flaky)["retries"], flaky_results)

    def test_missing_actual_is_explicit_and_expected_failure_fails_closed(self):
        path = self.report("expected", "failed", None)
        self.assertEqual(self.audit(path), {"expected": "FAIL", "actual": "MISSING", "status": "FAIL"})
        self.assertEqual(next(iter(mod.parse_playwright_json(path).values())), "FAIL")

    def test_malformed_actual_is_rejected(self):
        path = self.report("expected", "passed", "unknown")
        with self.assertRaisesRegex(ValueError, "unknown Playwright result status"):
            mod.parse_playwright_json(path)


if __name__ == "__main__":
    unittest.main()
