"""A regression is a test that ran and passed on a baseline and fails on the candidate."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(
    "baseline_diff", Path(__file__).resolve().parent.parent / "env" / "baseline-diff.py")
bd = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(bd)

BASE = """\
PASSED tests/a.py::test_ok
PASSED tests/a.py::test_broken_now
FAILED tests/a.py::test_old_red - AssertionError: x
PASSED tests/a.py::test_gone
FAILED tests/b.py::test_param[invalid0-missing inputs: request] - ValueError: a - b
XFAIL tests/b.py::test_known - reason
"""
CAND = """\
PASSED tests/a.py::test_ok
FAILED tests/a.py::test_broken_now - assert 3 == 1
FAILED tests/a.py::test_old_red - AssertionError: x
FAILED tests/c.py::test_new - boom
PASSED tests/b.py::test_param[invalid0-missing inputs: request]
XFAIL tests/b.py::test_known - reason
PASSED tests/d.py::TestX::test_teardown
ERROR tests/d.py::TestX::test_teardown - teardown failed
"""


class BaselineDiffTests(unittest.TestCase):
    def _run(self, base, cand, *extra):
        with tempfile.TemporaryDirectory() as t:
            b, c, out = Path(t, "b.log"), Path(t, "c.log"), Path(t, "out")
            b.write_text(base)
            c.write_text(cand)
            code = bd.main(["--baseline", f"served-11={b}", "--candidate", str(c), "--out", str(out), *extra])
            files = {p.stem: p.read_text().splitlines() for p in out.glob("*.txt")}
            return code, files

    def test_buckets(self):
        code, f = self._run(BASE, CAND)
        self.assertEqual(code, 1)
        self.assertEqual(f["regression"], ["tests/a.py::test_broken_now"])
        self.assertEqual(f["preexisting"], ["tests/a.py::test_old_red"])
        self.assertEqual(f["no-baseline"], ["tests/c.py::test_new", "tests/d.py::TestX::test_teardown"])
        self.assertEqual(f["fixed"], ["tests/b.py::test_param[invalid0-missing inputs: request]"])
        self.assertEqual(f["missing"], ["tests/a.py::test_gone"])

    def test_passing_on_any_baseline_makes_it_a_regression(self):
        with tempfile.TemporaryDirectory() as t:
            r10, main, cand = Path(t, "r10.log"), Path(t, "main.log"), Path(t, "c.log")
            r10.write_text("FAILED tests/a.py::test_x - e\n")
            main.write_text("PASSED tests/a.py::test_x\n")
            cand.write_text("FAILED tests/a.py::test_x - e\n")
            code = bd.main(["--baseline", f"r10={r10}", "--baseline", f"main={main}", "--candidate", str(cand)])
        self.assertEqual(code, 1)

    def test_clean_candidate_exits_zero(self):
        code, f = self._run("PASSED tests/a.py::test_ok\n", "PASSED tests/a.py::test_ok\n")
        self.assertEqual((code, f["regression"]), (0, []))

    def test_log_without_summary_lines_is_bad_input(self):
        code, _ = self._run("1 passed in 0.1s\n", "PASSED tests/a.py::test_ok\n")
        self.assertEqual(code, 2)

JOB = """\
2026-11-24T08:00:00.1Z tests/a.py::test_ok PASSED [ 50%]
2026-11-24T08:00:01.1Z tests/a.py::test_sub SUBFAILED(i=2) [ 90%]
2026-11-24T08:00:02.1Z =========== short test summary info ===========
2026-11-24T08:00:03.1Z PASSED tests/a.py::test_ok
2026-11-24T08:00:03.2Z PASSED tests/a.py::test_sub
2026-11-24T08:00:03.3Z FAILED tests/a.py::test_param[a b - c] - AssertionError: x
2026-11-24T08:00:04.1Z = 2 failed, 2 passed in 3.00s =
"""
INNER = """\
=========== short test summary info ===========
FAILED test_case.py::test_inner - printed by a test that runs pytest
= 1 failed in 0.1s =
=========== short test summary info ===========
PASSED tests/a.py::test_ok
FAILED tests/a.py::test_real - boom
= 1 failed, 1 passed in 9.00s =
"""


class SummarySectionTests(unittest.TestCase):
    def _parse(self, text):
        with tempfile.TemporaryDirectory() as t:
            log = Path(t, "j.log")
            log.write_text(text)
            return bd.parse([str(log)])

    def test_failed_subtests_are_counted_and_timestamps_ignored(self):
        got = self._parse(JOB)
        self.assertEqual(got["tests/a.py::test_sub SUBFAILED(i=2)"], "failed")
        self.assertEqual(got["tests/a.py::test_param[a b - c]"], "failed")
        self.assertEqual(got["tests/a.py::test_ok"], "passed")

    def test_inner_pytest_output_is_not_read(self):
        got = self._parse(INNER)
        self.assertEqual(got, {"tests/a.py::test_ok": "passed", "tests/a.py::test_real": "failed"})

    def test_truncated_log_is_bad_input(self):
        code, _ = BaselineDiffTests._run(self, "PASSED tests/a.py::test_ok\n",
                                         "=== short test summary info ===\nPASSED tests/a.py::test_ok\n")
        self.assertEqual(code, 2)

    def test_new_failing_subtest_of_a_passing_test_is_a_regression(self):
        code, f = BaselineDiffTests._run(self, "PASSED tests/a.py::test_sub\n", JOB)
        self.assertEqual(code, 1)
        self.assertIn("tests/a.py::test_sub SUBFAILED(i=2)", f["regression"])


class FailOnMissingTests(unittest.TestCase):
    def test_missing_only_blocks_with_the_flag(self):
        run = BaselineDiffTests._run
        base, cand = "PASSED tests/a.py::test_ok\nPASSED tests/a.py::test_gone\n", "PASSED tests/a.py::test_ok\n"
        code, f = run(self, base, cand)
        self.assertEqual((code, f["missing"]), (0, ["tests/a.py::test_gone"]))
        code, f = run(self, base, cand, "--fail-on-missing")
        self.assertEqual((code, f["missing"]), (1, ["tests/a.py::test_gone"]))

    def test_nothing_missing_passes_with_the_flag(self):
        code, _ = BaselineDiffTests._run(self, "PASSED tests/a.py::test_ok\n", "PASSED tests/a.py::test_ok\n",
                                         "--fail-on-missing")
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
