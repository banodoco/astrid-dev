"""PR intake routes are explicit, ownership verified, and never merge approvals."""
import unittest
from check_docs import HEADER, DIVIDER
from review_intake import classify, parse_intent

CATALOG = ("# Projects\n" + HEADER + "\n" + DIVIDER + "\n"
           "| Cloud | Goal | queued | @casey | TBD | — | [Plan 25](25-cloud/plan.md) |\n")
BASE = {"state": "open", "draft": False,
        "base": {"ref": "main", "repo": {"full_name": "banodoco/astrid-dev"}},
        "user": {"login": "casey", "type": "User"},
        "body": "Project: plans/25-cloud/plan.md\nReview request: implementation\n"}


class ReviewIntakeTests(unittest.TestCase):
    def test_existing_project_owner_can_request_review(self):
        self.assertEqual(classify(BASE, "banodoco/astrid-dev", CATALOG, []), "implementation")
        wrong = {**BASE, "user": {"login": "other", "type": "User"}}
        self.assertIsNone(classify(wrong, "banodoco/astrid-dev", CATALOG, []))
        self.assertIsNone(classify({**BASE, "draft": True}, "banodoco/astrid-dev", CATALOG, []))
        self.assertIsNone(classify({**BASE, "user": {"login": "casey", "type": "Bot"}},
                                   "banodoco/astrid-dev", CATALOG, []))

    def test_completion_requires_matching_receipt_and_catalog_change(self):
        body = ("Project: plans/25-cloud/plan.md\nReview request: completion\n"
                "## Completion assessment — Plan 25\n")
        pr = {**BASE, "body": body}
        files = [{"filename": "plans/index.md", "status": "modified"}]
        self.assertEqual(classify(pr, "banodoco/astrid-dev", CATALOG, files), "completion")
        self.assertIsNone(classify(pr, "banodoco/astrid-dev", CATALOG, []))
        self.assertIsNone(classify({**pr, "body": body.replace("Plan 25", "Plan 26")},
                                   "banodoco/astrid-dev", CATALOG, files))

    def test_new_scope_routes_any_contributor_with_three_file_pack(self):
        proposal = {**BASE, "body": "Project: plans/27-new/plan.md\nReview request: scope\n",
                    "user": {"login": "new", "type": "User"}}
        files = [{"filename": f"plans/27-new/{name}", "status": "added"}
                 for name in ("plan.md", "inputs.md", "tasks.md")]
        files.append({"filename": "plans/index.md", "status": "modified"})
        self.assertEqual(classify(proposal, "banodoco/astrid-dev", CATALOG, files), "scope")
        self.assertIsNone(classify(proposal, "banodoco/astrid-dev", CATALOG, files[:2]))

    def test_missing_duplicate_or_unrelated_intent(self):
        self.assertIsNone(parse_intent("Ordinary bug fix"))
        with self.assertRaises(ValueError):
            parse_intent(BASE["body"] + "Review request: completion\n")
        with self.assertRaises(ValueError):
            parse_intent("Review request: implementation\n")
        with self.assertRaises(ValueError):
            parse_intent("Project: plans/25-cloud/plan.md\n")
        self.assertIsNone(classify({**BASE, "base": {"ref": "other",
                              "repo": {"full_name": "banodoco/astrid-dev"}}},
                              "banodoco/astrid-dev", CATALOG, []))


if __name__ == "__main__":
    unittest.main()
