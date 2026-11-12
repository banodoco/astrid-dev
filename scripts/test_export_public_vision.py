"""Focused checks for a public-page projection with no duplicated editorial copy."""
import re
import shutil
import tempfile
import unittest

from pathlib import Path
from views import VIEWS, expected
from export_public_vision import build, rewrite_links, render_root_readme, render_root_summary, canonical_agent_prompt


SHA = "a" * 40
FIXTURE_FILES = Path(__file__).parent / "fixtures" / "vision"


class PublicVisionProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._fixture_temp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls._fixture_temp.cleanup)
        cls.fixture_root = Path(cls._fixture_temp.name)
        for source in FIXTURE_FILES.rglob("*.fixture"):
            relative = source.relative_to(FIXTURE_FILES)
            if relative.name.endswith(".md.fixture"):
                relative = relative.with_name(relative.name[:-len(".fixture")])
            destination = cls.fixture_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
        cls.page = build(cls.fixture_root, SHA)

    def test_pillars_come_from_vision_in_declared_order(self):
        self.assertEqual(
            [p["title"] for p in self.page["pillars"]],
            ["A Tool for Artistic Ambition", "Agent-Powered Liquid Software",
             "Intelligence That Compounds", "A Shared Creative Endeavor"],
        )
        self.assertTrue(all(p["descriptor"] and p["bodyMarkdown"] for p in self.page["pillars"]))
        self.assertEqual(
            [p["descriptor"] for p in self.page["pillars"]],
            [
                "Astrid is designed to support serious, sustained artistic practice.",
                "Tools should adapt to creative work as people and agents create together.",
                "What anyone learns should become something everyone can build on.",
                "We want to create the conditions for the community to do more together.",
            ],
        )

    def test_both_subject_types_derive_from_the_same_canonical_template(self):
        from vision_subject import parse_subject
        for kind, items in (("pillars", self.page["pillars"]),
                            ("principles", self.page["principles"])):
            for subject in items:
                path = self.fixture_root / "vision" / kind / (subject["id"] + ".md")
                parsed = parse_subject(path.read_text(encoding="utf-8"), str(path))
                self.assertEqual(subject["statement"], parsed["statement"])
                self.assertEqual(subject["explanationMarkdown"], parsed["explanationMarkdown"])
                self.assertEqual(
                    [(c["id"], c["title"], c["summary"]) for c in subject["characteristics"]],
                    [(c["id"], c["title"], c["summary"]) for c in parsed["characteristics"]],
                )
                self.assertIn(subject["statement"], subject["bodyMarkdown"])

    def test_vision_contribution_call_to_action(self):
        vision = self.page["vision"]
        self.assertEqual(vision["title"], "A tool to unlock the collective artistic ambition of the open-source AI community")
        self.assertIn("Astrid aims to help individuals and the community as a whole", vision["introMarkdown"])
        self.assertEqual(vision["agentPrompt"], canonical_agent_prompt(self.fixture_root))
        self.assertIn("skills/astrid-dev/SKILL.md", vision["agentPrompt"])
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

        self.assertEqual(
            self.page["principles"][0]["statement"],
            "Everything should be designed to run fully locally, and cheaply and conveniently in the cloud.",
        )
        all_subjects = self.page["pillars"] + self.page["principles"]
        self.assertEqual(len(all_subjects), 8)
        for subject in all_subjects:
            self.assertGreaterEqual(len(subject["characteristics"]), 2)
            self.assertTrue(subject["explanationMarkdown"])
            self.assertEqual(len({c["id"] for c in subject["characteristics"]}),
                             len(subject["characteristics"]))
            self.assertTrue(all(c["summary"].endswith(".") and c["detailsMarkdown"]
                                for c in subject["characteristics"]))

    def test_local_first_promise_is_balanced_without_losing_offline_control(self):
        first = self.page["principles"][0]
        full = first["bodyMarkdown"]
        self.assertIn("even offline", full)
        self.assertIn("local project should remain authoritative", full)
        self.assertIn("costs", full)

    def test_principles_have_concise_openings_and_detailed_characteristics(self):
        principles = self.page["principles"]
        self.assertEqual(principles[1]["title"], "Completely open by design")
        self.assertEqual(principles[3]["title"], "Eliminate technical wrangling")
        self.assertTrue(all(len(p["statement"].split()) <= 25 for p in principles))
        self.assertTrue(all(20 <= len(p["explanationMarkdown"].split()) <= 105
                            for p in principles))
        self.assertTrue(all(2 <= len(p["characteristics"]) <= 6 for p in principles))
        self.assertTrue(all("## Characteristics" in p["bodyMarkdown"] for p in principles))

    def test_liquid_software_reframes_creative_friction_without_losing_core_constraints(self):
        liquid = self.page["pillars"][1]
        self.assertEqual(liquid["statement"],
                         "Tools should adapt to creative work as people and agents create together.")
        self.assertIn("twentieth century", liquid["explanationMarkdown"])
        self.assertIn("real time", liquid["explanationMarkdown"])
        self.assertIn("shared foundation", liquid["explanationMarkdown"])
        self.assertIn("small, dependable foundation", liquid["bodyMarkdown"].lower())
        self.assertNotIn("not just quick generations", self.page["pillars"][0]["bodyMarkdown"])
        self.assertNotIn("throughput", self.page["pillars"][0]["bodyMarkdown"])

    def test_characteristics_reflect_artistic_agency_agent_tools_and_affordable_cloud(self):
        pillars = {pillar["id"]: pillar for pillar in self.page["pillars"]}
        principles = {p["id"]: p for p in self.page["principles"]}

        ambition = pillars["artistic-ambition"]
        self.assertIn("deep, evolving partnership", ambition["explanationMarkdown"])
        self.assertIn("every session", ambition["bodyMarkdown"])
        self.assertIn("Every blocker", ambition["bodyMarkdown"])
        self.assertNotIn("throughput", ambition["bodyMarkdown"])

        liquid = pillars["liquid-software"]
        self.assertIn("live-tool-composition", {c["id"] for c in liquid["characteristics"]})
        self.assertIn("Agents should be equally free", liquid["bodyMarkdown"])
        self.assertIn("extend its own capabilities", liquid["bodyMarkdown"])

        wisdom = pillars["compounding-intelligence"]
        self.assertEqual(wisdom["characteristics"][0]["title"],
                         "An ecosystem of wisdom grounded in real work")

        local = principles["local-first-cloud-capable"]
        self.assertIn("cloud-as-frugal-as-possible", {c["id"] for c in local["characteristics"]})
        self.assertIn("cheap turpentine", local["bodyMarkdown"])
        self.assertIn("privacy", local["bodyMarkdown"])

        open_design = principles["open-by-design"]
        self.assertEqual(len(open_design["characteristics"]), 4)
        self.assertIn("Open decisions and working knowledge", open_design["bodyMarkdown"])
        self.assertIn("With the creator's permission", open_design["bodyMarkdown"])

        wrangling = principles["eliminate-needless-technical-wrangling"]
        self.assertIn("work for your agents", wrangling["statement"])
        self.assertIn("The technical work remains real", wrangling["bodyMarkdown"])

    def test_vision_communication_outcome_and_open_ownership_are_accurate(self):
        pillars = {p["id"]: p for p in self.page["pillars"]}
        principles = {p["id"]: p for p in self.page["principles"]}
        gaps = {g["id"]: g for g in self.page["gaps"]}
        self.assertIn("creative and technical discovery",
                      pillars["compounding-intelligence"]["explanationMarkdown"])
        self.assertIn("when knowledge is shared",
                      pillars["compounding-intelligence"]["explanationMarkdown"].lower())
        self.assertIn("core product and wider ecosystem",
                      pillars["shared-endeavour"]["explanationMarkdown"])
        self.assertIn("not yet settled",
                      principles["open-by-design"]["explanationMarkdown"])
        self.assertIn("our ownership", principles["open-by-design"]["statement"])
        self.assertEqual(len(gaps), 22)
        self.assertIn("CA-003", gaps)
        self.assertEqual(gaps["CA-003"]["primaryAppliesTo"], "principle:open-by-design")
        self.assertIn("pillar:shared-endeavour", gaps["CA-003"]["appliesTo"])
        self.assertEqual(gaps["CA-003"]["assessment"], "partially evidenced")
        self.assertIn("at least three substantive", gaps["CA-003"]["closureEvidenceMarkdown"])

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

    def test_cross_modal_gap_is_distinct_from_extension_composition(self):
        gaps = {gap["id"]: gap for gap in self.page["gaps"]}
        self.assertIn("LS-004", gaps)
        cross_modal = gaps["LS-004"]
        self.assertEqual(cross_modal["appliesTo"][0], "pillar:liquid-software")
        self.assertIn("principle:open-by-design", cross_modal["appliesTo"])
        self.assertIn("video plus at least two non-video modality foundations",
                      cross_modal["closureEvidenceMarkdown"])
        self.assertIn("another independent contributor", cross_modal["closureEvidenceMarkdown"])
        self.assertNotEqual(cross_modal["missingMarkdown"], gaps["LS-003"]["missingMarkdown"])
        self.assertIn("LS-003", cross_modal["missingMarkdown"])

    def test_contributor_ownership_plan_uses_existing_gap_and_prior_sources(self):
        plan = next((p for p in self.page["projects"] if p["id"] == "28-contributor-ownership"), None)
        self.assertIsNotNone(plan)
        self.assertEqual(plan["gapIds"], ["CA-002"])
        self.assertEqual(plan["status"], "queued")
        self.assertIn("earlier commitments", plan["goalMarkdown"].lower())
        path = self.fixture_root / "plans/28-contributor-ownership/inputs.md"
        inputs = path.read_text(encoding="utf-8")
        self.assertIn("Banodoco-website", inputs)
        self.assertIn("Equity Review", inputs)
        self.assertIn("Pending", inputs)

    def test_each_gap_linked_project_has_one_primary_gap(self):
        for project in self.page["projects"]:
            self.assertEqual(
                project["primaryGapId"],
                project["gapIds"][0] if project["gapIds"] else None,
            )

    def test_project_gap_ids_resolve(self):
        ids = {gap["id"] for gap in self.page["gaps"]}
        self.assertTrue(all(set(project["gapIds"]) <= ids for project in self.page["projects"]))

    def test_relative_markdown_links_point_at_pinned_source(self):
        text = rewrite_links("[source](../pillars/artistic-ambition.md)",
                             __import__("pathlib").Path("vision/gaps/AA-001-sustained-creative-work.md"),
                             SHA, self.fixture_root)
        self.assertEqual(text,
                         f"[source](https://github.com/banodoco/astrid-dev/blob/{SHA}"
                         "/vision/pillars/artistic-ambition.md)")

    def test_root_vision_counts_follow_source_data(self):
        actual = (self.fixture_root / "README.md").read_text(encoding="utf-8")
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

    @staticmethod
    def region(readme, name):
        return readme.split(f"<!-- {name}:start -->", 1)[1].split(f"<!-- {name}:end -->", 1)[0]

    SENTENCE = ("Astrid pairs an adaptable front end at [astrid.haus](https://astrid.haus) "
                "with an agent equipped with tools for creative work and open-source AI.")

    def test_root_statement_comes_from_the_vision_title(self):
        root = self.fixture_copy()
        intro = root / "vision/intro.md"
        intro.write_text(intro.read_text(encoding="utf-8").replace(
            "collective artistic ambition", "artistic potential", 1), encoding="utf-8")
        before = (root / "README.md").read_text(encoding="utf-8")
        view = next(v for v in VIEWS if v.name == "root-vision-statement")
        after = expected(view, root)
        statement = "**A tool to unlock the artistic potential of the open-source AI community.**"
        self.assertIn(statement, self.region(after, "vision-statement"))
        self.assertEqual(after.count("A tool to unlock"), 1)
        self.assertNotIn("collective artistic ambition", after)
        outside = lambda text: text.split("<!-- vision-statement:start -->", 1)[0] + text.split("<!-- vision-statement:end -->", 1)[1]
        self.assertEqual(outside(after), outside(before))
        self.assertEqual(render_root_readme(after, build(root, SHA)), after)

    def test_root_statement_is_its_own_region_and_the_sentence_is_hand_written(self):
        readme = (self.fixture_root / "README.md").read_text(encoding="utf-8")
        statement = f"**{self.page['vision']['title']}.**"
        self.assertEqual(readme.count(statement), 1)
        self.assertEqual(self.region(readme, "vision-statement").strip(), statement)
        self.assertNotIn(statement, self.region(readme, "vision-summary"))
        self.assertIn(f"<!-- vision-statement:end -->\n\n{self.SENTENCE}\n\n<!-- vision-summary:start -->", readme)
        self.assertNotIn(self.SENTENCE, self.region(readme, "vision-statement") + self.region(readme, "vision-summary"))
        view = next(v for v in VIEWS if v.name == "root-vision-statement")
        self.assertEqual(expected(view, self.fixture_root).count(self.SENTENCE), 1)

    def fixture_copy(self):
        """A private copy of the fixture tree that a test may damage."""
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name) / "tree"
        shutil.copytree(self.fixture_root, root)
        return root

    @staticmethod
    def swap_principle_entries(path, first, second):
        """Swap two third-level principle entries, each a heading line, in a Markdown file."""
        text = path.read_text(encoding="utf-8")
        headings = re.findall(r"^### \[[^\]]+\]\(principles/[^)]+\.md\)$", text, re.M)
        one, other = headings[first], headings[second]
        swapped = text.replace(one, "@@").replace(other, one).replace("@@", other)
        assert swapped != text
        path.write_text(swapped, encoding="utf-8")

    PRINCIPLE_ORDER = ["local-first-cloud-capable", "open-by-design",
                       "in-the-creators-control", "eliminate-needless-technical-wrangling"]

    def test_principles_are_the_entries_of_the_intro_section_in_its_order(self):
        intro = (self.fixture_root / "vision/intro.md").read_text(encoding="utf-8")
        section = intro.split("## Four driving principles\n", 1)[1].split("\n## ", 1)[0]
        entries = re.findall(r"^### \[([^\]]+)\]\(principles/([^)]+)\.md\)$", section, re.M)
        self.assertEqual(len(entries), 4)
        self.assertEqual([stem for _, stem in entries], self.PRINCIPLE_ORDER)
        self.assertEqual([(p["title"], p["id"]) for p in self.page["principles"]], entries)

    def test_an_intro_without_the_principle_section_is_refused(self):
        root = self.fixture_copy()
        intro = root / "vision/intro.md"
        text = intro.read_text(encoding="utf-8")
        head, rest = text.split("## Four driving principles\n", 1)
        intro.write_text(head + "## Build Astrid with us" + rest.split("## Build Astrid with us", 1)[1],
                         encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Four driving principles"):
            build(root, SHA)

    def test_swapping_principle_headings_in_the_generated_page_changes_nothing(self):
        root = self.fixture_copy()
        self.swap_principle_entries(root / "vision/README.md", 0, 3)
        self.assertEqual(build(root, SHA), self.page)

    def test_a_garbled_generated_page_changes_nothing(self):
        # The page must still exist: pillars and gaps link to it, and a link to a missing file is refused.
        root = self.fixture_copy()
        (root / "vision/README.md").write_text("garbled\n", encoding="utf-8")
        self.assertEqual(build(root, SHA), self.page)

    def test_swapping_two_intro_entries_changes_the_order(self):
        root = self.fixture_copy()
        self.swap_principle_entries(root / "vision/intro.md", 0, 1)
        page = build(root, SHA)
        first = self.page["principles"]
        self.assertEqual(page["principles"], [first[1], first[0], first[2], first[3]])

    def test_a_principle_file_that_disagrees_with_the_intro_names_the_intro(self):
        root = self.fixture_copy()
        path = root / "vision/principles/open-by-design.md"
        text = path.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# Completely open by design\n"))
        path.write_text(text.replace("# Completely open by design", "# Completely open", 1), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "open-by-design.md: principle heading must match the intro"):
            build(root, SHA)

    def test_immutable_revision_is_required(self):
        with self.assertRaisesRegex(ValueError, "40-character"):
            build(self.fixture_root, "main")


if __name__ == "__main__":
    unittest.main()
