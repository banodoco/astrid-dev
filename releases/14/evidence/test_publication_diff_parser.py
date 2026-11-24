"""Focused pytest-log evidence regressions for Release 14 parser fixes."""
import importlib.util
from pathlib import Path
import unittest

FILE = Path(__file__).with_name("publication_diff.py")
spec = importlib.util.spec_from_file_location("r14_parser_evidence", FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestPytestEvidence(unittest.TestCase):
    def test_capture_then_single_outer_summary_is_kept(self):
        log = """---------------- Captured stdout call ----------------
ordinary application output
=========================== short test summary info ===========================
FAILED tests/a.py::test_outer - assertion
== 1 failed in 1s ==
"""
        self.assertEqual(mod.parse_pytest(log), {"tests/a.py::test_outer": "FAIL"})

    def test_progress_and_all_summaries_survive_with_truncation(self):
        log = """tests/a.py::test_first PASSED [ 10%]
tests/a.py::test_second PASSED [ 20%]
=========================== short test summary info ===========================
PASSED tests/a.py::test_first
== 2 passed in 1s ==
=========================== short test summary info ===========================
PASSED tests/b.py::test_later
"""
        self.assertEqual(mod.parse_pytest(log), {
            "tests/a.py::test_first": "PASS", "tests/a.py::test_second": "PASS",
            "tests/b.py::test_later": "PASS",
        })

    def test_malformed_progress_and_collection_failures_are_reported(self):
        log = """tests/a.py::test_bad FAILED [ 50%]
tests/a.py::test_bad[a[b] FAILED [100%]
FAILED tests/no_node.py - collection failed
ERROR tests/also_no_node.py - import failed
"""
        outcomes, _, malformed = mod.pytest_job_evidence(log)
        self.assertEqual(outcomes, {"tests/a.py::test_bad": "FAIL"})
        self.assertEqual(len(malformed), 3)

    def test_grouped_skip_without_file_line_is_retained(self):
        self.assertEqual(mod.pytest_job_evidence(
            "=========================== short test summary info ===========================\n"
            "SKIPPED [2] no usable location: reason\n== 2 skipped in 1s ==\n"
        )[1], {("no usable location", "reason"): 2})

    def test_grouped_skips_already_covered_by_ids_are_not_double_counted(self):
        log = """=========================== short test summary info ===========================
SKIPPED tests/a.py::test_skip - platform
SKIPPED [1] tests/a.py:3: platform
== 1 skipped in 1s ==
"""
        outcomes, groups, _ = mod.pytest_job_evidence(log)
        self.assertEqual(outcomes, {"tests/a.py::test_skip": "SKIP"})
        self.assertEqual(groups, {})

    def test_collection_and_unbalanced_node_failures_are_retained_as_parse_errors(self):
        log = """=========================== short test summary info ===========================
FAILED tests/a.py::test_case[a[b] - assertion
ERROR tests/new.py - ImportError: boom
== 2 failed, 1 error in 1.0s ==
"""
        outcomes, skips, errors = mod.pytest_job_evidence(log)
        self.assertEqual(outcomes, {})
        self.assertEqual(skips, {})
        self.assertEqual(errors, [
            "FAILED tests/a.py::test_case[a[b] - assertion",
            "ERROR tests/new.py - ImportError: boom",
        ])

    def test_all_invocations_in_one_step_are_read(self):
        log = """=========================== short test summary info ===========================
FAILED tests/a.py::test_bad - assertion
== 1 failed in 1s ==
=========================== short test summary info ===========================
PASSED tests/b.py::test_good
== 1 passed in 1s ==
"""
        self.assertEqual(mod.pytest_job_evidence(log), (
            {"tests/a.py::test_bad": "FAIL", "tests/b.py::test_good": "PASS"}, {}, []
        ))

    def test_ordinary_capture_does_not_hide_an_earlier_outer_summary(self):
        log = """tests/a.py::test_first FAILED [100%]
============================= FAILURES =============================
----------------------------- Captured stdout call -----------------------------
ordinary application output
=========================== short test summary info ===========================
FAILED tests/a.py::test_first - assertion
== 1 failed in 1s ==
=========================== short test summary info ===========================
PASSED tests/b.py::test_second
== 1 passed in 1s ==
"""
        self.assertEqual(mod.parse_pytest(log), {
            "tests/a.py::test_first": "FAIL", "tests/b.py::test_second": "PASS",
        })

    def test_early_close_and_bare_failed_are_malformed(self):
        log = """===== short test summary info =====
FAILED tests/a.py::test_case[param]] - assertion
ERROR tests/a.py::bad]name - assertion
FAILED
== 3 failed in 1s ==
"""
        outcomes, _, errors = mod.pytest_job_evidence(log)
        self.assertFalse(outcomes)
        self.assertEqual(errors, log.splitlines()[1:4])

    def test_nested_child_summary_in_captured_output_is_not_outer_evidence(self):
        log = """============================= FAILURES =============================
outer_test
----- Captured stdout call -----
running: /tmp/runpytest-0
=========================== short test summary info ===========================
FAILED tests/child.py::test_child - child failure
== 1 failed, 1 passed in 0.01s ==
=========================== short test summary info ===========================
PASSED tests/outer.py::test_outer
== 1 passed in 1s ==
"""
        self.assertEqual(mod.parse_pytest(log), {"tests/outer.py::test_outer": "PASS"})

    def test_unbound_skip_groups_keep_location_and_reason_identity(self):
        log = """=========================== short test summary info ===========================
SKIPPED [2] tests/a.py:3: old reason
== 2 skipped in 1s ==
=========================== short test summary info ===========================
SKIPPED [1] tests/zzz.py:9: brand new skip
== 1 skipped in 1s ==
"""
        outcomes, skips, errors = mod.pytest_job_evidence(log)
        self.assertEqual(outcomes, {})
        self.assertEqual(skips, {
            ("tests/a.py:3", "old reason"): 2,
            ("tests/zzz.py:9", "brand new skip"): 1,
        })
        self.assertEqual(errors, [])
        self.assertEqual(mod.pytest_job_results(log), ({}, 3))

    def test_progress_only_legacy_api_stays_two_item_tuple(self):
        self.assertEqual(mod.pytest_job_results("PASSED tests/a.py::test_ok\n"),
                         ({"tests/a.py::test_ok": "PASS"}, 0))


if __name__ == "__main__":
    unittest.main()
