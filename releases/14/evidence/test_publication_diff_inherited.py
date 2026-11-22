"""Regressions for live inherited-red approval proofs."""
import importlib.util
import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest import mock

FILE = Path(__file__).with_name("publication_diff.py")
spec = importlib.util.spec_from_file_location("r14_inherited", FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestInheritedApprovalProofs(unittest.TestCase):
    def test_xfail_is_red_for_inventory_validation(self):
        self.assertIn("XFAIL", mod.INHERITED_RED_STATUSES)

    def test_partial_baseline_rejects_approval_for_green_or_wrong_exact_job(self):
        approved = [{"repo": "agent", "workflow": "CI", "job": "unit shard 1", "id": "x", "status": "FAIL"}]
        green = [{"repo": "agent", "workflow": "CI", "job": "unit shard 1", "id": "x", "status": "PASS"}]
        self.assertTrue(mod.validate_inherited_failures({"approved_prior": approved, "current": approved}, green, partial_baseline=True))
        other_job = [dict(approved[0], job="unit shard 2")]
        self.assertTrue(mod.validate_inherited_failures({"approved_prior": approved, "current": approved}, other_job, partial_baseline=True))

    def test_baseline_proof_uses_r13_job_and_id_from_comparison_rows(self):
        rows = [{"product":"agent", "workflow":"CI", "job":"unit shard 2", "id":"renamed", "r13_job":"unit shard 1", "r13_id":"old", "r13":"FAIL", "candidate":"FAIL"}]
        actual = mod.inherited_baseline_rows(rows)
        self.assertEqual(actual, [{"repo":"agent", "workflow":"CI", "job":"unit shard 1", "id":"old", "status":"FAIL"}])

    def test_live_cli_requires_manifest_digest_anchor_even_allow_growth(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); manifest=root/'m.json'; inv=root/'i.json'
            manifest.write_text('{}')
            inv.write_text(json.dumps({"schema_version":1,"sealed_prior":[],"current":[]}))
            rc=mod.main(["--manifest",str(manifest),"--inherited-red",str(inv),"--out",str(root/'out'),"--allow-growth"])
            self.assertEqual(rc,2)

    def test_validator_partial_mode_preserves_legacy_strict_contract(self):
        inventory={"approved_prior":[],"current":[]}
        baseline=[{"repo":"agent","workflow":"CI","job":"unit shard 1","id":"new","status":"FAIL"}]
        self.assertTrue(mod.validate_inherited_failures(inventory,baseline))
        self.assertEqual(mod.validate_inherited_failures(inventory,baseline,partial_baseline=True),[])

    def test_partial_baseline_counts_exact_identity_and_ignores_approved_status(self):
        approved = [{"repo":"agent","workflow":"CI","job":"unit shard 1","id":"x","status":"FAIL","count":3}]
        baseline = [{"repo":"agent","workflow":"CI","job":"unit shard 1","id":"x","status":"XFAIL","count":3}]
        self.assertEqual(mod.validate_inherited_failures({"approved_prior":approved,"current":approved},baseline,partial_baseline=True), [])
        baseline[0]["job"] = "unit shard 2"
        self.assertTrue(mod.validate_inherited_failures({"approved_prior":approved,"current":approved},baseline,partial_baseline=True))

    def test_resolve_committed_anchor_uses_safe_rev_parse_and_full_commit(self):
        completed = [mock.Mock(stdout="a" * 40 + "\n", returncode=0),
                     mock.Mock(stdout="", returncode=0),
                     mock.Mock(stdout=json.dumps({"schema_version":1,"sealed_prior":[{"x":1}],"current":[]}), returncode=0)]
        with mock.patch.object(mod.subprocess, "run", side_effect=completed) as run:
            commit, inventory = mod.resolve_inherited_base("HEAD")
        self.assertEqual(commit, "a" * 40)
        self.assertEqual(inventory["sealed_prior"], [{"x":1}])
        self.assertIn("--end-of-options", run.call_args_list[0].args[0])
        self.assertIn(commit + ":releases/14/evidence/inherited-red.json", run.call_args_list[2].args[0])

    def test_growth_uses_committed_current_even_if_both_working_lists_grew(self):
        entry = {"repo": "agent", "workflow": "CI", "job": "unit shard 1", "id": "tests/a.py::case"}
        working = {"schema_version": 1, "sealed_prior": [entry], "current": [entry]}
        committed = {**working, "current": []}
        with mock.patch.object(mod, "resolve_inherited_base", return_value=("a" * 40, committed)):
            approved, problems, anchor = mod.anchored_inherited_red_counts({}, working, "HEAD", False)
            self.assertFalse(approved)
            self.assertIn("exceeds committed current ceiling", problems[0])
            approved, problems, _ = mod.anchored_inherited_red_counts({}, working, "HEAD", True)
        self.assertEqual(approved, Counter({tuple(entry.values()): 1}))
        self.assertFalse(problems)
        self.assertIn("a" * 40, anchor)

    def test_sealed_prior_digest_rejects_a_rewritten_local_list(self):
        sealed = {"schema_version": 1, "sealed_prior": [], "current": []}
        manifest = {"inherited_red_sealed_sha256": mod.sealed_prior_digest(sealed)}
        entry = {"repo": "agent", "workflow": "CI", "job": "unit shard 1", "id": "tests/a.py::case"}
        with self.assertRaisesRegex(ValueError, "does not match canonical sealed_prior"):
            mod.anchored_inherited_red_counts(manifest, {**sealed, "sealed_prior": [entry]}, None, True)

    def test_baseline_proofs_ignore_grouped_job_skip_and_use_original_native_identity(self):
        rows = [
            {"product":"agent","workflow":"CI","job":"new shard","r13_job":"old shard","id":"new","r13_id":"old","r13":"FAIL","candidate":"FAIL","kind":"test"},
            {"product":"agent","workflow":"CI","job":"old shard","id":mod.UNATTRIBUTED_SKIP_ID,"r13":"SKIP","candidate":"SKIP","kind":"job"},
        ]
        self.assertEqual(mod.inherited_baseline_rows(rows), [{"repo":"agent","workflow":"CI","job":"old shard","id":"old","status":"FAIL"}])

    def test_live_main_rejects_inventory_entry_not_red_in_exact_baseline(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); log=root/'job.log'; log.write_text("PASSED tests/a.py::green\n")
            row={"repo":"agent","workflow":"CI","job":"unit shard 1","id":"tests/a.py::green"}
            inventory={"schema_version":1,"sealed_prior":[row],"current":[row]}
            inv=root/'inventory.json'; inv.write_text(json.dumps(inventory))
            manifest=root/'manifest.json'; manifest.write_text(json.dumps({"inherited_red_sealed_sha256":mod.sealed_prior_digest(inventory)}))
            job={"id":1,"name":"unit shard 1","conclusion":"success","log":str(log)}
            records={p:{"baseline":{},"candidate":{}} for p in mod.REPO}
            records["agent"]["baseline"]["CI"]={"id":1,"conclusion":"success","jobs":[job]}
            records["agent"]["candidate"]["CI"]={"id":2,"conclusion":"success","jobs":[dict(job,id=2)]}
            with mock.patch.object(mod,"collect_runs",return_value=records), mock.patch.object(mod,"check_canonical_baseline_diff",return_value=[]):
                rc=mod.main(["--manifest",str(manifest),"--inherited-red",str(inv),"--out",str(root/'out')])
            self.assertEqual(rc,1)
            self.assertIn("approved ID not actually red in baseline",(root/'out'/'report.md').read_text())

    def test_live_main_rejects_r13_pass_r14_fail_even_when_candidate_is_approved(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); base_log=root/'r13.log'; base_log.write_text("PASSED tests/a.py::case\n")
            candidate_log=root/'r14.log'; candidate_log.write_text("FAILED tests/a.py::case - regression\n")
            row={"repo":"agent","workflow":"CI","job":"unit shard 1","id":"tests/a.py::case"}
            inventory={"schema_version":1,"sealed_prior":[row],"current":[row]}
            inv=root/'inventory.json'; inv.write_text(json.dumps(inventory))
            manifest=root/'manifest.json'; manifest.write_text(json.dumps({"inherited_red_sealed_sha256":mod.sealed_prior_digest(inventory)}))
            job={"id":1,"name":"unit shard 1","conclusion":"success","log":str(base_log)}
            records={p:{"baseline":{},"candidate":{}} for p in mod.REPO}
            records["agent"]["baseline"]["CI"]={"id":1,"conclusion":"success","jobs":[job]}
            records["agent"]["candidate"]["CI"]={"id":2,"conclusion":"success","jobs":[dict(job,id=2,log=str(candidate_log))]}
            with mock.patch.object(mod,"collect_runs",return_value=records), mock.patch.object(mod,"check_canonical_baseline_diff",return_value=[]):
                rc=mod.main(["--manifest",str(manifest),"--inherited-red",str(inv),"--out",str(root/'out')])
            self.assertEqual(rc,1)
            report=(root/'out'/'report.md').read_text()
            self.assertIn("approved ID not actually red in baseline",report)

    def test_all_pytest_summaries_in_one_step_are_retained(self):
        log="===== short test summary info =====\nPASSED tests/a.py::first\n== 1 passed in 1s ==\n===== short test summary info =====\nFAILED tests/b.py::second - failure\n== 1 failed in 1s ==\n"
        self.assertEqual(mod.parse_pytest(log),{"tests/a.py::first":"PASS","tests/b.py::second":"FAIL"})


if __name__ == "__main__":
    unittest.main()
