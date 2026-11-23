"""Pre-RS1 compatibility probes for Release 15's authored Plan 72 seam.

This is a source-scoped rehearsal with miniature authored records, not an
assertion that the frozen Release 15 branch has these files or that its
release-plan branch was cut. Preserve the original real-tree traversal tests.
"""
import tempfile
import unittest
from pathlib import Path

import gap_relationships as goal_links
from project_delivery import deliveries_for_goal, frozen_releases_for_issue, load_delivery
from records import release_branch_errors
from relationships import RecordRef, RelationshipError
from test_project_delivery import GAP, PILLAR, PLAN, RELEASE
from vision_subject import SECTIONS


BRANCH_HEAD = (
    "## Branches\n\n"
    "| Repository | Branch | Role | Cut at | State |\n"
    "| --- | --- | --- | --- | --- |\n"
)
RELEASE_ROW = (
    "| astrid-dev | `release/15/main` | release | " + "a" * 40 + " | open |\n"
)
PLAN_ROW = (
    "| astrid-dev | `release/15/plan-72` | plan 72 | not yet cut | open |\n"
)
AUTHORED_BRIEF = RELEASE.replace(
    "## Publication", BRANCH_HEAD + RELEASE_ROW + PLAN_ROW + "\n## Publication"
)


class Release15SourceSeamTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.write("vision/pillars/shared.md",
                   PILLAR.replace("## Aspirations", f"## {SECTIONS[2]}"))
        self.write("vision/gaps/CA-001-finish-work.md",
                   GAP.replace("**Aspiration:**", "**Goal:**")
                   if hasattr(goal_links, "parse_gap_goals") else GAP)
        self.write("plans/72-demo/plan.md", PLAN)
        self.write("releases/15.md", AUTHORED_BRIEF)

    def write(self, relative, body):
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")

    def test_astrid_dev_release_and_uncut_plan_rows_are_structurally_valid(self):
        # The branch table is an authored record, not a branch-existence check.
        self.assertEqual(release_branch_errors(AUTHORED_BRIEF, "15", ("72",)), [])

    def test_missing_plan_branch_row_cannot_justify_included_plan(self):
        incomplete = AUTHORED_BRIEF.replace(PLAN_ROW, "")
        errors = release_branch_errors(incomplete, "15", ("72",))
        self.assertTrue(
            any("Included plan 72 has no" in error for error in errors), errors
        )

    def test_plan_row_requires_a_release_row_in_same_repository(self):
        incomplete = AUTHORED_BRIEF.replace(RELEASE_ROW, "")
        errors = release_branch_errors(incomplete, "15", ("72",))
        self.assertTrue(
            any("no release row" in error and "astrid-dev" in error
                for error in errors), errors
        )

    def test_release_membership_without_authored_plan_is_rejected(self):
        # The older release baseline lacks the Plan72 authored pack. It must
        # not be represented as a valid full traversal merely from a row.
        (self.root / "plans/72-demo/plan.md").unlink()
        with self.assertRaisesRegex(RelationshipError, "unknown folder"):
            load_delivery(self.root)

    def test_authored_membership_and_frozen_issue_are_independent(self):
        graph = load_delivery(self.root)
        goal = RecordRef("goal", "pillar:shared/finish-work")
        deliveries = deliveries_for_goal(graph, goal)
        self.assertEqual(
            [(path.project.id, path.release.id) for path in deliveries],
            [("72", "15")],
        )
        self.assertEqual(
            frozen_releases_for_issue(graph, 123), (RecordRef("release", "15"),)
        )
        self.write(
            "releases/15.md",
            AUTHORED_BRIEF.replace(
                "- [Plan 72](../plans/72-demo/plan.md) — demonstrable result",
                "None yet",
            ),
        )
        without_membership = load_delivery(self.root)
        self.assertEqual(deliveries_for_goal(without_membership, goal), ())
        self.assertEqual(
            frozen_releases_for_issue(without_membership, 123),
            (RecordRef("release", "15"),),
        )


if __name__ == "__main__":
    unittest.main()
