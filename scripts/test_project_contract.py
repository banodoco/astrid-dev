"""Focused identity and gap-link tests shared by CI and the public feed."""
import unittest
from project_contract import plan_gap_ids, project_number

class ProjectContractTests(unittest.TestCase):
    def test_gap_links_and_enabler(self):
        text = ("**Vision gaps:** [Execution](../../vision/gaps/F-003-creative-execution.md) "
                "(primary); [Control](../../vision/gaps/F-002-safe-user-control.md) (supporting).\n")
        self.assertEqual(plan_gap_ids(text), ["F-003", "F-002"])
        self.assertEqual(plan_gap_ids("**Vision role:** Foundational enabler — documentation\n"), [])

    def test_rejects_duplicates_and_ambiguity(self):
        gap = "**Vision gaps:** [Execution](../../vision/gaps/F-003-creative-execution.md)\n"
        for text in ["# Missing", gap + gap,
                     gap + "**Vision role:** Foundational enabler\n",
                     "**Vision gaps:** missing link\n",
                     "**Vision gaps:** [1](../../vision/gaps/F-003-a.md) [2](../../vision/gaps/F-003-b.md)"]:
            with self.subTest(text=text), self.assertRaises(ValueError):
                plan_gap_ids(text)

    def test_primary_gap_must_be_first_and_unique(self):
        first = "[One](../../vision/gaps/F-001-platform-reliability.md)"
        second = "[Two](../../vision/gaps/F-002-safe-user-control.md)"
        for entry in [
            "**Vision gaps:** " + first + " (supporting).\n",
            "**Vision gaps:** " + first + " (primary) " + second + " (primary).\n",
            "**Vision gaps:** " + first + " (supporting) " + second + " (primary).\n",
        ]:
            with self.subTest(entry=entry), self.assertRaises(ValueError):
                plan_gap_ids(entry)

    def test_project_ids_scale(self):
        self.assertEqual(project_number("plans/01-first/plan.md"), "01")
        self.assertEqual(project_number("plans/100-many/plan.md"), "100")
        with self.assertRaises(ValueError):
            project_number("plans/1-bad/plan.md")

if __name__ == "__main__":
    unittest.main()
