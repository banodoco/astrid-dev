"""Regression cases from the Q1-Q4 publication-diff probe."""
import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest import mock

import publication_diff as mod


SUMMARY = "===== short test summary info =====\n"
JOB_KEY = ("agent", "CI", "unit shard 1")


class TestProbeRegressions(unittest.TestCase):
    def evaluate_pair(self, baseline_log, candidate_log, approved, *, candidate_steps=None, manifest=None, step_names=None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            jobs = []
            for index, log in enumerate((baseline_log, candidate_log), 1):
                path = root / f"{index}.log"
                path.write_text(log)
                jobs.append({"name": "unit shard 1", "id": index, "attempt": 1,
                             "conclusion": "failure", "log": str(path),
                             "failed_steps": (["Run tests"] if index == 1 else candidate_steps or ["Run tests"]),
                             "step_names": step_names or ["Run tests"], "log_error": None})
            records = {repo: {side: {} for side in ("baseline", "candidate")} for repo in mod.REPO}
            for side, run_id, job in (("baseline", 1, jobs[0]), ("candidate", 2, jobs[1])):
                records["agent"][side]["CI"] = {
                    "id": run_id, "sha": str(run_id), "conclusion": "failure",
                    "attempt": 1, "jobs": [job],
                }
            rows, _, problems = mod.evaluate(manifest or {}, records, root, {}, None, None,
                                               approved_counts=approved)
            approved_rows = [dict(zip(mod.INHERITED_RED_FIELDS, key), count=count)
                             for key, count in approved.items()]
            problems += mod.validate_inherited_failures(
                {"approved_prior": approved_rows, "current": approved_rows},
                mod.inherited_baseline_rows(rows), partial_baseline=True)
            problems += mod.check_inherited_red_observations(approved, rows)
            return rows, problems

    def test_q1_xfail_to_fail_under_approved_key_is_new_adversity(self):
        approved = Counter({JOB_KEY + ("tests/a.py::t1",): 1,
                            JOB_KEY + ("tests/a.py::t2",): 1,
                            JOB_KEY + ("[job]",): 1})
        baseline = SUMMARY + "FAILED tests/a.py::t1 - old\nXFAIL tests/a.py::t2 - known\nPASSED tests/a.py::t3\n== 1 failed, 1 xfailed, 1 passed in 1s ==\n"
        candidate = SUMMARY + "FAILED tests/a.py::t1 - old\nFAILED tests/a.py::t2 - now failing\nPASSED tests/a.py::t3\n== 2 failed, 1 passed in 1s ==\n"
        _, problems = self.evaluate_pair(baseline, candidate, approved)
        self.assertTrue(any("tests/a.py::t2" in problem and "FAIL" in problem for problem in problems), problems)

    def test_q2_skip_to_error_under_approved_key_is_new_adversity(self):
        approved = Counter({JOB_KEY + ("tests/a.py::t1",): 1,
                            JOB_KEY + ("tests/a.py::t2",): 1,
                            JOB_KEY + ("[job]",): 1})
        baseline = "tests/a.py::t1 FAILED [ 33%]\ntests/a.py::t2 SKIPPED [ 66%]\ntests/a.py::t3 PASSED [100%]\n"
        candidate = "tests/a.py::t1 FAILED [ 33%]\ntests/a.py::t2 ERROR [ 66%]\ntests/a.py::t3 PASSED [100%]\n"
        _, problems = self.evaluate_pair(baseline, candidate, approved)
        self.assertTrue(any("tests/a.py::t2" in problem and "ERROR" in problem for problem in problems), problems)

    def test_q3_new_non_test_step_failure_is_not_hidden_by_same_test_ids(self):
        approved = Counter({JOB_KEY + ("tests/a.py::t1",): 1, JOB_KEY + ("[job]",): 1})
        log = SUMMARY + "FAILED tests/a.py::t1 - old\nPASSED tests/a.py::t3\n== 1 failed, 1 passed in 1s ==\n"
        _, problems = self.evaluate_pair(log, log + "##[group]Run coverage check\nERROR: coverage below threshold\n", approved, candidate_steps=["Run tests", "Run coverage check"])
        self.assertTrue(any("coverage" in problem.lower() or "step" in problem.lower() for problem in problems), problems)

    def test_r1_step_that_passed_on_r13_and_fails_on_r14_blocks(self):
        approved = Counter({JOB_KEY + ("tests/a.py::t1",): 1, JOB_KEY + ("[job]",): 1})
        log = SUMMARY + "FAILED tests/a.py::t1 - old\nPASSED tests/a.py::t3\n== 1 failed, 1 passed in 1s ==\n"
        _, problems = self.evaluate_pair(log, log, approved,
                                         candidate_steps=["Run tests", "Coverage gate"],
                                         step_names=["Run tests", "Coverage gate"])
        self.assertTrue(any("Coverage gate" in problem for problem in problems), problems)

    def test_new_step_requires_exact_nonempty_exception(self):
        approved = Counter({JOB_KEY + ("tests/a.py::t1",): 1, JOB_KEY + ("[job]",): 1})
        log = SUMMARY + "FAILED tests/a.py::t1 - old\n== 1 failed in 1s ==\n"
        step = "Run coverage check"
        key = "candidate/agent/CI/unit shard 1/" + step
        for exceptions, expected in (({key: "reviewed"}, False), ({key + "x": "reviewed"}, True), ({key: " "}, True)):
            _, problems = self.evaluate_pair(log, log, approved, candidate_steps=["Run tests", step],
                                             manifest={"failed_step_exceptions": exceptions})
            self.assertEqual(bool(problems), expected, problems)

    def test_equal_and_improving_red_statuses_can_consume_approval(self):
        approved = Counter({JOB_KEY + ("tests/a.py::t2",): 1, JOB_KEY + ("[job]",): 1})
        for before, after, expected in (("XFAIL", "SKIPPED", False), ("ERROR", "FAILED", False),
                                        ("FAILED", "ERROR", True)):
            old = f"tests/a.py::t2 {before} [100%]\n"
            new = f"tests/a.py::t2 {after} [100%]\n"
            _, problems = self.evaluate_pair(old, new, approved)
            self.assertEqual(bool(problems), expected, problems)

    def test_q4_parent_summary_survives_nested_pytester_summary(self):
        log = ("tests/a.py::t3 PASSED [100%]\n----- Captured stdout call -----\n"
               "running: python -mpytest --basetemp=/tmp/runpytest-0\n" + SUMMARY +
               "FAILED tests/n.py::brand_new - x\n== 1 failed in 1s ==\n" + SUMMARY +
               "FAILED tests/a.py::t1 - old\nPASSED tests/a.py::t3\n== 1 failed, 1 passed in 1s ==\n")
        evidence, _, errors = mod.pytest_job_evidence(log)
        self.assertEqual(evidence.get("tests/a.py::t1"), "FAIL")
        self.assertTrue("tests/n.py::brand_new" in evidence or errors)

    def test_live_cli_requires_explicit_inherited_base_even_with_manifest_digest(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            inventory = {"schema_version": 1, "sealed_prior": [], "current": []}
            inventory_path = root / "inherited.json"
            inventory_path.write_text(json.dumps(inventory))
            manifest_path = root / "manifest.json"
            manifest_path.write_text(json.dumps({
                "inherited_red_sealed_sha256": mod.sealed_prior_digest(inventory)}))
            records = {repo: {side: {} for side in ("baseline", "candidate")} for repo in mod.REPO}
            with mock.patch.object(mod, "collect_runs", return_value=records), \
                    mock.patch.object(mod, "check_canonical_baseline_diff", return_value=[]):
                result = mod.main(["--manifest", str(manifest_path), "--inherited-red",
                                   str(inventory_path), "--out", str(root / "out")])
            self.assertEqual(result, 2)


if __name__ == "__main__":
    unittest.main()
