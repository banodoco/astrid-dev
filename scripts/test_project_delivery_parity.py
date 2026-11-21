"""Read-only cross-checks against Astrid Dev's existing public vision publisher.

These checks do NOT claim byte parity with an earlier Git revision: that
requires paired exact-source captures at PD-11. They do pin the live schema-v1
projection and ensure the relationship reader cannot silently reclassify
projects or mutate the publisher's output.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from export_public_vision import build
from project_delivery import load_delivery
from relationships import RecordRef


ROOT = Path(__file__).resolve().parents[1]
REVISION = "0000000000000000000000000000000000000000"


class ReadOnlyFeedParityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.feed = build(ROOT, REVISION)
        cls.graph = load_delivery(ROOT)

    def test_schema_v1_projection_is_unchanged_by_a_graph_query(self):
        original = json.dumps(self.feed, ensure_ascii=False, indent=2) + "\n"
        # Read the actual canonical records a second time. No writer, publish
        # state, URL, generated view or schema transformation is authorized.
        load_delivery(ROOT)
        after = json.dumps(build(ROOT, REVISION), ensure_ascii=False, indent=2) + "\n"
        self.assertEqual(self.feed["schemaVersion"], 1)
        self.assertEqual(after, original)
        self.assertEqual(self.feed["source"]["revision"], REVISION)

    def test_every_public_project_preserves_primary_and_supporting_gap_ids(self):
        self.assertTrue(self.feed["projects"], "public vision has no projects")
        for item in self.feed["projects"]:
            project = RecordRef("project", item["id"].split("-", 1)[0])
            with self.subTest(project=str(project)):
                links = self.graph.outgoing(project, "addresses")
                self.assertEqual(
                    {link.target.id for link in links}, set(item["gapIds"]))
                primaries = [link.target.id for link in links if link.role == "primary"]
                expected = [item["primaryGapId"]] if item["primaryGapId"] else []
                self.assertEqual(primaries, expected)
                self.assertEqual(
                    project in self.graph.enablers, item["primaryGapId"] is None)

    def test_original_feed_keeps_public_projects_under_one_primary_gap(self):
        projects_by_gap = {gap["id"]: [] for gap in self.feed["gaps"]}
        for item in self.feed["projects"]:
            primary = item["primaryGapId"]
            if primary is not None:
                self.assertIn(primary, projects_by_gap)
                projects_by_gap[primary].append(item["id"])
        all_classified = [id_ for ids in projects_by_gap.values() for id_ in ids]
        self.assertEqual(len(all_classified), len(set(all_classified)))


if __name__ == "__main__":
    unittest.main()
