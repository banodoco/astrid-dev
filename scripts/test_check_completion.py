"""Focused, synthetic tests for the plan-completion decision gate."""
import tempfile
import unittest
from pathlib import Path

from check_completion import assess_completion, check_pr, transitions_to_done
from check_docs import DIVIDER, HEADER

PLAN = ("# Zero-to-first-image\n\n"
        "**Vision gaps:** [Creative execution](../../visions/gaps/F-003-creative-execution.md) (primary).\n\n"
        "## Completion\nA real generated image appears on the timeline with captured recovery evidence.\n")
ENABLER = "# Documentation refactor\n\n**Vision role:** Foundational enabler — no direct gap.\n"
RECEIPT = """## Completion assessment — Plan 20

Evidence: [real task run](https://github.com/banodoco/astrid-agent/actions/runs/123)
Completion: Yes — A real image reached the timeline in the supported environment.
Gap F-003: Partially evidenced — One complete route works, but not all inference backends or machines.
"""


def catalog(status: str) -> str:
    row = f"| First image | Build a flow | {status} | Owner | TBD | — | [Plan 20](20-zero-to-first-image/plan.md) |"
    return HEADER + "\n" + DIVIDER + "\n" + row + "\n"


class CompletionGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        target = self.root / "plans/20-zero-to-first-image"
        target.mkdir(parents=True)
        (target / "plan.md").write_text(PLAN, encoding="utf-8")

    def test_only_new_done_transition_requires_receipt(self):
        self.assertEqual(transitions_to_done(catalog("active"), catalog("done")),
                         ["20-zero-to-first-image/plan.md"])
        self.assertEqual(transitions_to_done(catalog("done"), catalog("done")), [])
        self.assertEqual(transitions_to_done(catalog("queued"), catalog("active")), [])

    def test_missing_receipt_fails(self):
        issues = check_pr(catalog("active"), catalog("done"), "", self.root)
        self.assertEqual(len(issues), 1)
        self.assertIn("missing", issues[0])

    def test_missing_linked_gap_fails(self):
        body = """## Completion assessment — Plan 20
Evidence: https://github.com/example/repo/actions/runs/123
Completion: Yes — The plan completion criteria were tested on the reviewed source.
"""
        issues = check_pr(catalog("active"), catalog("done"), body, self.root)
        self.assertTrue(any("F-003" in issue for issue in issues))

    def test_valid_assessment_passes(self):
        self.assertEqual(check_pr(catalog("active"), catalog("done"), RECEIPT, self.root), [])

    def test_placeholder_evidence_fails(self):
        body = RECEIPT.replace(
            "[real task run](https://github.com/banodoco/astrid-agent/actions/runs/123)",
            "a run happened")
        self.assertTrue(any("Evidence" in error for error in
                            check_pr(catalog("active"), catalog("done"), body, self.root)))

    def test_future_project_ids_and_concise_reasons(self):
        future = RECEIPT.replace("Plan 20", "Plan 100").replace(
            "One complete route works, but not all inference backends or machines.",
            "One route works; others are unproven.")
        self.assertEqual(assess_completion("100-later/plan.md", PLAN, future), [])
        placeholder = RECEIPT.replace(
            "One complete route works, but not all inference backends or machines.", "TBD")
        self.assertTrue(any("F-003" in error for error in
                            assess_completion("20-zero-to-first-image/plan.md", PLAN, placeholder)))

    def test_enabler_needs_explicit_no_gap_impact(self):
        self.assertTrue(assess_completion("21-site/plan.md", ENABLER,
                        """## Completion assessment — Plan 21
Evidence: https://github.com/example/repo/pull/4
Completion: Yes — The existing homepage work passes its stated requirements.
"""))
        self.assertEqual(assess_completion("21-site/plan.md", ENABLER,
                         """## Completion assessment — Plan 21
Evidence: https://github.com/example/repo/pull/4
Completion: Yes — The existing homepage work passes its stated requirements.
Gap impact: None — It is a communication deliverable, not proof that a gap was closed.
"""), [])

    def test_new_catalog_during_migration_is_not_transition(self):
        self.assertEqual(check_pr(None, catalog("done"), "", self.root), [])

    def test_existing_done_is_not_rechecked(self):
        self.assertEqual(check_pr(catalog("done"), catalog("done"), "", self.root), [])


if __name__ == "__main__":
    unittest.main()
