"""F72 source-boundary probes: a Markdown symlink must not import outside facts.

A parsed in-root filename is not a canonical authored source when the underlying
file resolves outside the delivery root. Internal source aliases stay supported.
"""
import tempfile
import unittest
from pathlib import Path

import gap_relationships as goal_links
from project_delivery import deliveries_for_goal, load_delivery
from relationships import RecordRef, RelationshipError
from test_project_delivery import GAP, PILLAR, PLAN, RELEASE
from vision_subject import SECTIONS


class DeliverySourceContainmentTests(unittest.TestCase):
    def setUp(self):
        root_tmp = tempfile.TemporaryDirectory()
        outside_tmp = tempfile.TemporaryDirectory()
        self.addCleanup(root_tmp.cleanup)
        self.addCleanup(outside_tmp.cleanup)
        self.root = Path(root_tmp.name)
        self.outside = Path(outside_tmp.name)
        self.write("vision/pillars/shared.md",
                   PILLAR.replace("## Aspirations", f"## {SECTIONS[2]}"))
        self.write("vision/gaps/CA-001-finish-work.md",
                   GAP.replace("**Aspiration:**", "**Goal:**")
                   if hasattr(goal_links, "parse_gap_goals") else GAP)
        self.write("plans/72-demo/plan.md", PLAN)
        self.write("releases/15.md", RELEASE)

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def externalize(self, relative):
        source = self.root / relative
        outside = self.outside / source.name
        outside.write_bytes(source.read_bytes())
        source.unlink()
        source.symlink_to(outside)

    def assert_external_source_refused(self, relative):
        self.externalize(relative)
        with self.assertRaisesRegex(
            RelationshipError, "outside delivery root"
        ) as failure:
            load_delivery(self.root)
        self.assertIn(relative, str(failure.exception))

    def test_external_pillar_source_cannot_author_goal(self):
        self.assert_external_source_refused("vision/pillars/shared.md")

    def test_external_gap_source_cannot_author_measurement(self):
        self.assert_external_source_refused("vision/gaps/CA-001-finish-work.md")

    def test_external_project_source_cannot_author_addresses(self):
        self.assert_external_source_refused("plans/72-demo/plan.md")

    def test_external_release_source_cannot_author_membership(self):
        self.assert_external_source_refused("releases/15.md")

    def test_internal_source_alias_preserves_valid_traversal(self):
        source = self.root / "vision/pillars/shared.md"
        internal = self.root / "source-alias" / "shared-pillar.md"
        internal.parent.mkdir(parents=True)
        internal.write_bytes(source.read_bytes())
        source.unlink()
        source.symlink_to(internal)
        graph = load_delivery(self.root)
        goal = RecordRef("goal", "pillar:shared/finish-work")
        self.assertTrue(deliveries_for_goal(graph, goal))


if __name__ == "__main__":
    unittest.main()
