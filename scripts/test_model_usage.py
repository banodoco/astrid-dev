"""Model provenance is recorded during work, not invented during review."""
import json
import tempfile
import unittest
from pathlib import Path
from model_usage import append_record, make_record, read_records, summarize


class ModelUseTests(unittest.TestCase):
    def test_live_append_and_summary(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            item = make_record("N", "implementation", "task-1", "self-reported",
                               model_id="<id>", provider="<provider>", effort="high")
            append_record(root, item)
            rows = read_records(root)
            self.assertEqual(len(rows), 1)
            summary = summarize(rows)
            self.assertIn("Routes used: N for implementation (1 invocation(s))", summary)
            self.assertNotIn("<id>", summary)
            self.assertNotIn("override", summary)
            self.assertIn("Not recorded", summarize([]))
            self.assertEqual((root / "model-usage.jsonl").read_text().count("\n"), 1)

    def test_summary_is_accepted_by_completion_receipt_validator(self):
        from check_completion import assess_completion
        summary = summarize([make_record("N", "implementation", "task-1", "self-reported")])
        self.assertTrue(summary.startswith("Routes used: N for implementation"))
        plan = ("# Result\n\n**Vision role:** Foundational enabler — "
                "not a directly linked gap.\n")
        receipt = (
            "## Completion assessment — Plan 20\n"
            "Evidence: https://github.com/banodoco/astrid-dev/pull/15\n"
            "Completion: Yes — The accepted deliverable was independently checked.\n"
            "Implementation PRs: None — Research-only deliverable with no product code.\n"
            "Integrated candidate: None — No code was changed in this project.\n"
            "Unproven: Remaining environments are explicitly out of scope.\n"
            "Gap impact: None — This enabler has no directly attributed outcome.\n"
            + summary + "\n"
        )
        self.assertEqual(assess_completion("20-example/plan.md", plan, receipt), [])

    def test_verified_claim_requires_receipt(self):
        with self.assertRaisesRegex(ValueError, "requires a source"):
            make_record("S", "review", "task", "runtime-observed")
        self.assertEqual(make_record("S", "review", "task", "runtime-observed",
                                     receipt="run/actual.json")["basis"], "runtime-observed")

    def test_route_is_required_and_checked(self):
        with self.assertRaises(ValueError):
            make_record("Q", "research", "task", "self-reported")
        with self.assertRaises(ValueError):
            make_record("N", "research", "", "self-reported")
        self.assertEqual(make_record("T", "implementation", "copy pass", "self-reported")["route"], "T")

    def test_override_is_summarized_only_when_present(self):
        summary = summarize([
            make_record("X", "review", "t1", "self-reported", override="<name>"),
            make_record("N", "implementation", "t2", "self-reported"),
            make_record("N", "implementation", "t3", "self-reported")])
        self.assertIn("N for implementation (2 invocation(s))", summary)
        self.assertIn("X for review (1 invocation(s), override: <name>)", summary)
        self.assertEqual(summary.count("override"), 1)

    def test_old_record_without_route_is_summarized_safely(self):
        old = {"provider": "p", "model_id": "m", "role": "review", "task": "t",
               "basis": "self-reported"}
        with tempfile.TemporaryDirectory() as t:
            (Path(t) / "model-usage.jsonl").write_text(json.dumps(old) + "\n")
            summary = summarize(read_records(Path(t)))
        self.assertIn("route not recorded for review", summary)
        self.assertNotIn("m/", summary)

    def test_bad_source_is_reported(self):
        with tempfile.TemporaryDirectory() as t:
            (Path(t) / "model-usage.jsonl").write_text("nonsense\n")
            with self.assertRaisesRegex(ValueError, "malformed"):
                read_records(Path(t))


if __name__ == "__main__":
    unittest.main()
