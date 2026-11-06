"""Focused checks for a public-page projection with no duplicated editorial copy."""
import unittest

from check_docs import ROOT
from export_public_vision import build, rewrite_links


SHA = "a" * 40


class PublicVisionProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = build(ROOT, SHA)

    def test_pillars_come_from_vision_in_declared_order(self):
        self.assertEqual(
            [p["title"] for p in self.page["pillars"]],
            ["A Tool for Artistic Ambition", "Agent-Powered Liquid Software",
             "Intelligence That Compounds", "A Shared Creative Endeavor"],
        )
        self.assertTrue(all(p["descriptor"] and p["bodyMarkdown"] for p in self.page["pillars"]))

    def test_vision_contribution_call_to_action(self):
        vision = self.page["vision"]
        self.assertIn("collective artistic ambition", vision["title"])
        self.assertIn("Astrid aims to help people", vision["introMarkdown"])
        self.assertIn("ownership", vision["contributeMarkdown"])

    def test_principles_and_gap_relationships(self):
        self.assertEqual(len(self.page["principles"]), 4)
        self.assertGreater(len(self.page["gaps"]), 0)
        self.assertEqual(len({g["id"] for g in self.page["gaps"]}), len(self.page["gaps"]))
        self.assertTrue(all(g["appliesTo"] and g["currentMarkdown"] and g["desiredMarkdown"]
                            for g in self.page["gaps"]))
        self.assertTrue(all(g["assessment"] in
                            {"open", "partially evidenced", "closed", "needs recheck"}
                            for g in self.page["gaps"]))

    def test_open_projects_derive_from_catalog_in_priority_order(self):
        projects = self.page["projects"]
        self.assertGreater(len(projects), 0)
        self.assertEqual(len({p["id"] for p in projects}), len(projects))
        open_projects = [p for p in projects if p["status"] not in {"done", "cancelled"}]
        self.assertTrue(all(p["status"] in {"queued", "active", "blocked", "paused"} for p in open_projects))
        self.assertEqual([p["priorityOrder"] for p in projects], list(range(1, len(projects)+1)))
        self.assertEqual(self.page["schemaVersion"], 1)
        self.assertTrue(all(p["title"] and p["goalMarkdown"] and p["githubUrl"] for p in projects))
        self.assertTrue(all(p["githubUrl"].startswith(
            "https://github.com/banodoco/astrid-dev/blob/" + SHA + "/plans/")
                            for p in projects))

    def test_project_gap_ids_resolve(self):
        ids = {gap["id"] for gap in self.page["gaps"]}
        self.assertTrue(all(set(project["gapIds"]) <= ids for project in self.page["projects"]))

    def test_relative_markdown_links_point_at_pinned_source(self):
        text = rewrite_links("[source](../pillars/artistic-ambition.md)",
                             __import__("pathlib").Path("visions/gaps/AA-001-sustained-creative-work.md"),
                             SHA, ROOT)
        self.assertEqual(text,
                         f"[source](https://github.com/banodoco/astrid-dev/blob/{SHA}"
                         "/visions/pillars/artistic-ambition.md)")

    def test_immutable_revision_is_required(self):
        with self.assertRaisesRegex(ValueError, "40-character"):
            build(ROOT, "main")


if __name__ == "__main__":
    unittest.main()
