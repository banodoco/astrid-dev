"""Plan 72 source-ownership tests; preserve canonical Plan 48/53 parsers.

A candidate review input, not an accepted RS1 decision or release integration.
"""
import tempfile
import unittest
from pathlib import Path

import gap_relationships as goal_links
from check_docs import GAP_NAME
from export_public_vision import GAP_ID
from project_contract import plan_gap_ids, plan_gap_links
from project_delivery import GAP_FILE, load_delivery
from relationships import RecordRef, RelationshipError
from test_project_delivery import GAP, PLAN, PILLAR, RELEASE
from vision_subject import SECTIONS


class SourceOwnershipTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.write("vision/pillars/shared.md",
                   PILLAR.replace("## Aspirations", f"## {SECTIONS[2]}"))
        self.write("vision/gaps/CA-001-finish-work.md",
                   GAP.replace("**Aspiration:**", "**Goal:**")
                   if hasattr(goal_links, "parse_gap_goals") else GAP)
        self.write("plans/72-demo/plan.md", PLAN)
        self.write("releases/15.md", RELEASE)

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def test_canonical_project_source_owns_roles_ids_and_hrefs(self):
        text = (
            "**Vision gaps:** [One](../../vision/gaps/CA-001-finish-work.md) "
            "(primary); [Two](../../vision/gaps/CA-002-follow-on.md) "
            "(supporting).\n")
        self.assertEqual(plan_gap_links(text), [
            ("CA-001", "primary", "../../vision/gaps/CA-001-finish-work.md"),
            ("CA-002", "supporting", "../../vision/gaps/CA-002-follow-on.md"),
        ])
        self.assertEqual(plan_gap_ids(text), ["CA-001", "CA-002"])

    def test_enabler_has_no_project_gap_links(self):
        for kind in ("Foundational", "Communication"):
            with self.subTest(kind=kind):
                line = f"**Vision role:** {kind} enabler — project support\n"
                self.assertEqual(plan_gap_links(line), [])
                self.assertEqual(plan_gap_ids(line), [])

    def test_invalid_gap_roles_stay_owned_by_canonical_parser(self):
        base = ("**Vision gaps:** [One](../../vision/gaps/CA-001-finish-work.md)")
        for line in (
            base + " (supporting) (primary)",
            base + " (supporting)",
            base + " (primary); [Two](../../vision/gaps/CA-002-other.md) (primary)",
        ):
            with self.subTest(line=line), self.assertRaises(ValueError):
                plan_gap_links(line)

    def test_two_gap_project_delivery_preserves_source_roles(self):
        second = GAP.replace("# CA-001 —", "# CA-002 —")
        if hasattr(goal_links, "parse_gap_goals"):
            second = second.replace("**Aspiration:**", "**Goal:**")
        self.write("vision/gaps/CA-002-follow-on.md", second)
        self.write("plans/72-demo/plan.md", PLAN.replace(
            " (primary)\n\n## Outcome",
            " (primary); [CA-002](../../vision/gaps/CA-002-follow-on.md) "
            "(supporting)\n\n## Outcome"))
        graph = load_delivery(self.root)
        links = graph.outgoing(RecordRef("project", "72"), "addresses")
        self.assertEqual(
            {(x.target.id, x.role, x.source_path) for x in links},
            {("CA-001", "primary", "plans/72-demo/plan.md"),
             ("CA-002", "supporting", "plans/72-demo/plan.md")})

    def test_gap_filename_identity_matches_existing_canonical_readers(self):
        # Characterize existing independently owned source contracts before
        # deciding whether a shared helper is smaller than deliberate reuse.
        for name, expected in (
            ("CA-001-finish-work.md", "CA-001"),
            ("F-008-portable-generation.md", "F-008"),
            ("LS-004-composable.md", "LS-004"),
        ):
            with self.subTest(name=name):
                for rule in (GAP_NAME, GAP_ID, GAP_FILE):
                    self.assertEqual(rule.fullmatch(name).group(1), expected)
        for name in (
            "CA-001.md", "CA-001-Upper.md", "CA-001-bad.txt",
            "CA-01-too-short.md", "ca-001-lowercase.md",
        ):
            with self.subTest(name=name):
                for rule in (GAP_NAME, GAP_ID, GAP_FILE):
                    self.assertIsNone(rule.fullmatch(name))

    def test_wrong_gap_heading_refuses_with_canonical_provenance(self):
        self.write("vision/gaps/CA-001-finish-work.md",
                   GAP.replace("# CA-001 —", "# CA-002 —"))
        with self.assertRaises(RelationshipError) as caught:
            load_delivery(self.root)
        message = str(caught.exception)
        for expected in (
            "vision/gaps/CA-001-finish-work.md", "gap:CA-001", "CA-002"
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, message)

    def test_second_gap_source_with_same_id_refuses_both_paths(self):
        self.write("vision/gaps/CA-001-another-source.md", GAP)
        with self.assertRaises(RelationshipError) as caught:
            load_delivery(self.root)
        message = str(caught.exception)
        for expected in (
            "gap:CA-001", "vision/gaps/CA-001-another-source.md",
            "vision/gaps/CA-001-finish-work.md"
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, message)


if __name__ == "__main__":
    unittest.main()
