"""Supplementary Plan 72 critique: source-bound negative regression probes.

Test-only diagnostic. Before fixes, these cases must fail visibly; the branch
does not grant RS1 acceptance or release integration authority.
"""
import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import gap_relationships as goal_links
from vision_subject import SECTIONS
from project_delivery import load_delivery, main
from relationships import (
    RecordRef, Relationship, RelationshipError, RelationshipIndex,
)
from test_project_delivery import GAP, PLAN, PILLAR, RELEASE


class SupplementaryCritiqueRegressions(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.write("vision/pillars/shared.md",
                   PILLAR.replace("## Aspirations", f"## {SECTIONS[2]}"))
        self.write("vision/gaps/CA-001-finish-work.md",
                   GAP.replace("**Aspiration:**", "**Goal:**")
                   if hasattr(goal_links, "parse_gap_goals") else GAP)
        self.write("plans/72-demo/plan.md", PLAN)
        self.write("releases/15.md", RELEASE)

    def write(self, relative, contents):
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(contents, encoding="utf-8")

    def test_duplicate_included_plans_sections_refuse_in_both_orders(self):
        # records.release_brief used the first H2, so source ordering decided
        # whether a release included the project.
        included = ("## Included plans\n"
                    "- [Plan 72](../plans/72-demo/plan.md) — demonstrable result")
        missing = "## Included plans\nNone yet"
        for sections in ((included, missing), (missing, included)):
            with self.subTest(order=sections):
                text = RELEASE.replace(included, "\n\n".join(sections))
                self.write("releases/15.md", text)
                with self.assertRaisesRegex(RelationshipError, "Included plans"):
                    load_delivery(self.root)

    def test_contradictory_release_h1_headings_refuse(self):
        # records.release_brief selected the first title and authorized
        # release membership despite a second conflicting # Release heading.
        self.write("releases/15.md", RELEASE.replace(
            "# Release 15 — Demo",
            "# Release 15 — Demo\n# Release 16 — Contradictory"))
        with self.assertRaisesRegex(RelationshipError, "[Rr]elease.*[Hh]eading"):
            load_delivery(self.root)

    def test_one_gap_link_cannot_be_primary_and_supporting(self):
        # project_contract.plan_gap_ids counted a single (primary) marker but
        # failed to reject another role marker on the exact same authored link.
        self.write("plans/72-demo/plan.md",
                   PLAN.replace(" (primary)", " (supporting) (primary)"))
        with self.assertRaisesRegex(RelationshipError, "gap.*role|role.*gap"):
            load_delivery(self.root)

    def test_enabler_cannot_have_an_addresses_edge(self):
        # An enabler was exempted from the shared index's primary count,
        # but even an explicit addresses(primary) edge was accepted.
        goal = RecordRef("goal", "pillar:shared/finish-work")
        gap = RecordRef("gap", "CA-001")
        project = RecordRef("project", "72")
        links = [
            Relationship(gap, "measures", goal, "primary",
                         "vision/gaps/CA-001-finish-work.md"),
            Relationship(project, "addresses", gap, "primary",
                         "plans/72-demo/plan.md"),
        ]
        with self.assertRaisesRegex(RelationshipError, "[Ee]nabler"):
            RelationshipIndex([goal, gap, project], links, enablers=[project])

    def test_missing_root_is_not_a_valid_empty_graph(self):
        missing = self.root / "this-root-does-not-exist"
        with self.assertRaisesRegex(RelationshipError, "root"):
            load_delivery(missing)

    def test_cli_check_on_nonexistent_root_refuses(self):
        missing = self.root / "nonexistent"
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            result = main(["check", "--root", str(missing)])
        self.assertEqual(result, 1)
        self.assertIn("root", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
