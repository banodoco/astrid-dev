"""Focused tests for first-principles gap boundary review, independent of actual PRs."""
import subprocess
import tempfile
import unittest
from pathlib import Path

from check_gap_boundaries import (
    affected_gaps,
    assess_boundary,
    boundary_signature,
    check_pr,
    needs_boundary_review,
)

ORIGINAL = """# F-005 — An outcome is not yet available

**Applies to:** [Local-first](../principles/local-first-cloud-capable.md) · **Assessment:** Open (evidence under review).

## Desired state

Creators can use remote capabilities without moving their persistent workspace.

## Current state

No integrated end-to-end remote workflow has been qualified.

## Gap

The remote execution boundary lacks a supported, auditable user journey.

## Closure evidence

Run real remote work and return verified editable local artifacts with negative tests.

## Sources and reassessment

See the current plan and product source.
"""

RECEIPT = """## Gap boundary assessment — F-005

Decision: Refine — Express a durable creator outcome independently of the proposed cloud implementation.
Outcome: A local-first creator can delegate selected work without giving up local project ownership.
Existing alternatives: Compared F-003 general creative execution and F-006 durable hosting; Plan 25 is a project, not the gap.
Why this level: The independent user outcome remains important if Plan 25 or its provider choices are replaced.
Independent closure: A real user delegates work and receives editable results with custody, consent, cost and recovery checks.
Primary connection: principle:local-first-cloud-capable — Optional cloud work preserves the local-first promise at the heart of this gap.
Supporting connections: principle:in-the-creators-control — Consenting to transfers and retaining data custody matter but do not define the main outcome.
Evidence: https://github.com/banodoco/astrid-dev/blob/main/plans/25-cloud-assist-v1/plan.md
"""


class GapBoundaryGateTests(unittest.TestCase):
    def test_empty_applies_to_does_not_swallow_next_line(self):
        text = ORIGINAL.replace(
            "**Applies to:** [Local-first](../principles/local-first-cloud-capable.md) · **Assessment:** Open (evidence under review).",
            "**Applies to:**\nThe next line must not become the value. **Assessment:** Open (evidence under review).",
        )
        self.assertEqual(boundary_signature(text)[1], "")

    def test_evidence_only_changes_do_not_require_new_boundary_review(self):
        revised = ORIGINAL.replace("Open (evidence under review)", "Partially evidenced (new tests)")
        revised = revised.replace("No integrated end-to-end remote workflow has been qualified.",
                                  "One prototype path exists, but no complete workflow is qualified.")
        revised += "\nNew source link: https://github.com/example/source\n"
        self.assertFalse(needs_boundary_review(ORIGINAL, revised))

    def test_new_removed_or_semantically_changed_gap_is_reviewed(self):
        self.assertTrue(needs_boundary_review(None, ORIGINAL))
        self.assertTrue(needs_boundary_review(ORIGINAL, None))
        self.assertTrue(needs_boundary_review(
            ORIGINAL, ORIGINAL.replace("An outcome is not yet available", "A better outcome name")))
        self.assertTrue(needs_boundary_review(
            ORIGINAL, ORIGINAL.replace("without moving their persistent workspace",
                                       "and move all their files to the cloud")))
        self.assertTrue(needs_boundary_review(
            ORIGINAL, ORIGINAL.replace("Run real remote work", "Only run a mock workflow")))
        self.assertTrue(boundary_signature(ORIGINAL))

    def test_valid_first_principles_receipt_passes(self):
        self.assertEqual(check_pr({"F-005"}, RECEIPT), [])

    def test_primary_and_supporting_justification_required_and_matched(self):
        expected = {
            "F-005": (
                ["principle:local-first-cloud-capable", "principle:in-the-creators-control"],
                "principle:local-first-cloud-capable",
            )
        }
        self.assertEqual(check_pr({"F-005"}, RECEIPT, expected), [])
        missing = RECEIPT.replace(
            "Primary connection: principle:local-first-cloud-capable — Optional cloud work preserves the local-first promise at the heart of this gap.\n", "")
        self.assertTrue(any("Primary connection" in x for x in check_pr({"F-005"}, missing, expected)))
        wrong = RECEIPT.replace(
            "Primary connection: principle:local-first-cloud-capable",
            "Primary connection: pillar:artistic-ambition")
        self.assertTrue(any("differs" in x for x in check_pr({"F-005"}, wrong, expected)))
        extra = RECEIPT.replace(
            "Supporting connections: principle:in-the-creators-control",
            "Supporting connections: principle:in-the-creators-control, principle:open-by-design")
        self.assertTrue(any("Supporting connections differ" in x for x in
                            check_pr({"F-005"}, extra, expected)))

    def test_requires_each_changed_gap(self):
        issues = check_pr({"F-005", "F-006"}, RECEIPT)
        self.assertTrue(any("F-006" in issue and "missing" in issue for issue in issues))

    def test_rejects_vague_or_missing_alternative_and_proof(self):
        weak = RECEIPT.replace(
            "Compared F-003 general creative execution and F-006 durable hosting; Plan 25 is a project, not the gap.",
            "Other solutions could exist in the future, so this is needed.")
        weak = weak.replace(
            "A real user delegates work and receives editable results with custody, consent, cost and recovery checks.",
            "TBD.")
        issues = assess_boundary("F-005", weak)
        self.assertTrue(any("Existing alternatives" in issue for issue in issues))
        self.assertTrue(any("Independent closure" in issue for issue in issues))

    def test_concise_but_specific_rationale_is_allowed(self):
        succinct = RECEIPT.replace(
            "A real user delegates work and receives editable results with custody, consent, cost and recovery checks.",
            "Demonstrate local custody with an approved remote result.")
        self.assertEqual(assess_boundary("F-005", succinct), [])

    def test_rejects_missing_evidence_and_duplicate_sections(self):
        without = RECEIPT.replace(
            "https://github.com/banodoco/astrid-dev/blob/main/plans/25-cloud-assist-v1/plan.md",
            "my impression")
        self.assertTrue(any("Evidence" in issue for issue in assess_boundary("F-005", without)))
        self.assertTrue(any("duplicate" in issue for issue in
                            assess_boundary("F-005", RECEIPT + "\n" + RECEIPT)))

    def test_detects_renamed_boundaries_from_real_git_diff(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            def git(*args):
                return subprocess.check_output(["git", *args], cwd=root, text=True).strip()
            git("init", "-q")
            git("config", "user.name", "Gap tests")
            git("config", "user.email", "gap-tests@example.com")
            gap = root / "vision/gaps/F-005-test.md"
            gap.parent.mkdir(parents=True)
            gap.write_text(ORIGINAL, encoding="utf-8")
            git("add", ".")
            git("commit", "-qm", "baseline")
            base = git("rev-parse", "HEAD")
            gap.write_text(ORIGINAL.replace("No integrated end-to-end remote workflow",
                                            "A partial remote workflow"), encoding="utf-8")
            git("add", ".")
            git("commit", "-qm", "evidence only")
            self.assertEqual(affected_gaps(base, root), set())
            gap.write_text(ORIGINAL.replace("An outcome is not yet available",
                                            "The desired capability is unproven"), encoding="utf-8")
            git("add", ".")
            git("commit", "-qm", "reframe outcome")
            self.assertEqual(affected_gaps(base, root), {"F-005"})
            added = root / "vision/gaps/F-007-sandbox.md"
            added.write_text(ORIGINAL.replace("F-005", "F-007"), encoding="utf-8")
            git("add", ".")
            git("commit", "-qm", "add gap")
            self.assertEqual(affected_gaps(base, root), {"F-005", "F-007"})


    def test_vision_folder_move_preserves_gap_boundary_without_new_review(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            def git(*args):
                return subprocess.check_output(["git", *args], cwd=root, text=True).strip()
            git("init", "-q")
            git("config", "user.name", "Gap tests")
            git("config", "user.email", "gap-tests@example.com")
            old = root / "visions/gaps/F-005-test.md"
            old.parent.mkdir(parents=True)
            old.write_text(ORIGINAL, encoding="utf-8")
            git("add", ".")
            git("commit", "-qm", "legacy vision location")
            base = git("rev-parse", "HEAD")
            new = root / "vision/gaps/F-005-test.md"
            new.parent.mkdir(parents=True)
            new.write_text(ORIGINAL.replace(
                "../principles/local-first-cloud-capable.md",
                "../principles/local-first-cloud-capable.md"), encoding="utf-8")
            old.unlink()
            git("add", ".")
            git("commit", "-qm", "move only")
            self.assertEqual(affected_gaps(base, root), set())
            new.write_text(new.read_text(encoding="utf-8").replace(
                "without moving their persistent workspace",
                "by moving their persistent workspace"), encoding="utf-8")
            git("add", ".")
            git("commit", "-qm", "material outcome change")
            self.assertEqual(affected_gaps(base, root), {"F-005"})

if __name__ == "__main__":
    unittest.main()
