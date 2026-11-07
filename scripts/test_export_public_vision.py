"""Focused checks for a public-page projection with no duplicated editorial copy."""
import unittest

from check_docs import ROOT
from export_public_vision import build, rewrite_links, render_root_readme, render_root_summary


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
        self.assertEqual(vision["introMarkdown"], "We want to inspire people to push themselves beyond their creative limits with AI - and reward them for doing so.")
        self.assertNotIn("100% of the ownership", vision["introMarkdown"])
        self.assertNotIn("actual allocation and legal structure", vision["introMarkdown"].lower())
        self.assertNotIn("legal and allocation model", vision["contributeMarkdown"].lower())
        self.assertNotIn("The information on this page is pulled from", vision["introMarkdown"])
        self.assertNotIn("collective inspires ambitious work", vision["introMarkdown"])
        self.assertIn(
            "[Give these instructions to your agent](https://github.com/banodoco/astrid-dev/blob/"
            + SHA + "/README.md#want-to-contribute-give-this-to-your-agent)",
            vision["contributeMarkdown"],
        )

    def test_principles_and_gap_relationships(self):
        self.assertEqual(len(self.page["principles"]), 4)
        self.assertGreater(len(self.page["gaps"]), 0)
        self.assertEqual(len({g["id"] for g in self.page["gaps"]}), len(self.page["gaps"]))
        self.assertTrue(all(g["appliesTo"] and g["currentMarkdown"] and g["desiredMarkdown"]
                            for g in self.page["gaps"]))
        self.assertTrue(all(g["primaryAppliesTo"] == g["appliesTo"][0]
                            and g["appliesTo"].count(g["primaryAppliesTo"]) == 1
                            for g in self.page["gaps"]))
        self.assertEqual(
            {g["id"]: g["primaryAppliesTo"] for g in self.page["gaps"] if g["id"] in
             {"CA-002", "F-001", "F-002", "F-003", "F-005", "LS-001"}},
            {"CA-002": "pillar:shared-endeavour",
             "F-001": "principle:eliminate-needless-technical-wrangling",
             "F-002": "principle:in-the-creators-control",
             "F-003": "principle:eliminate-needless-technical-wrangling",
             "F-005": "principle:local-first-cloud-capable",
             "LS-001": "pillar:liquid-software"},
        )
        self.assertTrue(all(g["assessment"] in
                            {"open", "partially evidenced", "closed", "needs recheck"}
                            for g in self.page["gaps"]))

    def test_principles_are_concise_and_balanced(self):
        bodies = [p["bodyMarkdown"] for p in self.page["principles"]]
        lengths = [len(body.split()) for body in bodies]
        self.assertEqual(len(lengths), 4)
        self.assertLessEqual(max(lengths), 60)
        self.assertLessEqual(max(lengths) - min(lengths), 10)
        self.assertTrue(all("not a claim" not in body.lower() for body in bodies))

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

    def test_video_rendering_options_is_a_queued_gap_linked_plan(self):
        matches = [p for p in self.page["projects"] if p["id"] == "27-video-render-options"]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["status"], "queued")
        self.assertIn("F-003", matches[0]["gapIds"])
        self.assertIn("F-002", matches[0]["gapIds"])

    def test_sandbox_outcome_is_distinct_from_its_openshell_project(self):
        gaps = {gap["id"]: gap for gap in self.page["gaps"]}
        projects = {project["id"]: project for project in self.page["projects"]}
        self.assertIn("F-007", gaps)
        self.assertNotIn("OpenShell", gaps["F-007"]["title"])
        self.assertIn("F-007", projects["15-openshell-safe-execution"]["gapIds"])
        self.assertIn("F-002", projects["15-openshell-safe-execution"]["gapIds"])
        self.assertEqual(projects["15-openshell-safe-execution"]["status"], "queued")

    def test_contributor_ownership_plan_uses_existing_gap_and_prior_sources(self):
        plan = next((p for p in self.page["projects"] if p["id"] == "28-contributor-ownership"), None)
        self.assertIsNotNone(plan)
        self.assertEqual(plan["gapIds"], ["CA-002"])
        self.assertEqual(plan["status"], "queued")
        self.assertIn("earlier commitments", plan["goalMarkdown"].lower())
        path = ROOT / "plans/28-contributor-ownership/inputs.md"
        inputs = path.read_text(encoding="utf-8")
        self.assertIn("Banodoco-website", inputs)
        self.assertIn("Equity Review", inputs)
        self.assertIn("Pending", inputs)

    def test_project_gap_ids_resolve(self):
        ids = {gap["id"] for gap in self.page["gaps"]}
        self.assertTrue(all(set(project["gapIds"]) <= ids for project in self.page["projects"]))

    def test_relative_markdown_links_point_at_pinned_source(self):
        text = rewrite_links("[source](../pillars/artistic-ambition.md)",
                             __import__("pathlib").Path("vision/gaps/AA-001-sustained-creative-work.md"),
                             SHA, ROOT)
        self.assertEqual(text,
                         f"[source](https://github.com/banodoco/astrid-dev/blob/{SHA}"
                         "/vision/pillars/artistic-ambition.md)")

    def test_root_vision_counts_follow_source_data(self):
        actual = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertEqual(render_root_readme(actual, self.page), actual)
        self.assertIn("Our vision has four main pillars and four guiding principles.", actual)
        self.assertIn(f"We've identified {len(self.page['gaps'])} gaps", actual)
        self.assertIn(f"informing {len(self.page['projects'])} projects.", actual)
        self.assertIn("[Vision](vision/README.md) · [Pillars]", actual)
        self.assertIn("[Principles](vision/README.md#four-driving-principles)", actual)
        self.assertIn(f"[Gaps](vision/README.md#gaps--{len(self.page['gaps'])}-assessed-outcomes)", actual)
        self.assertIn("[Projects](plans/index.md)", actual)
        self.assertNotIn("Read the full vision", actual)

        hypothetical = {**self.page,
                        "gaps": self.page["gaps"] + [{}],
                        "projects": self.page["projects"] + [{}]}
        changed = render_root_summary(hypothetical)
        self.assertIn(f"We've identified {len(self.page['gaps']) + 1} gaps", changed)
        self.assertIn(f"informing {len(self.page['projects']) + 1} projects", changed)
        self.assertIn(f"gaps--{len(self.page['gaps']) + 1}-assessed-outcomes", changed)
        self.assertNotEqual(actual, render_root_readme(actual, hypothetical))

    def test_immutable_revision_is_required(self):
        with self.assertRaisesRegex(ValueError, "40-character"):
            build(ROOT, "main")


if __name__ == "__main__":
    unittest.main()
