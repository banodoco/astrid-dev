"""Pure negative tests for the privileged owner-only claim validation."""
import unittest
from unittest.mock import patch
from claim_project import eligible, verify_claim, verify_live_claim
from check_docs import HEADER, DIVIDER

BASE = ("# Projects\n\n" + HEADER + "\n" + DIVIDER + "\n"
        "| Alpha | Goal | queued | Unassigned | TBD | — | [Plan 25](25-cloud/plan.md) |\n"
        "| Beta | Goal | queued | Unassigned | TBD | — | [Plan 26](26-hosted/plan.md) |\n")

class ClaimTests(unittest.TestCase):
    def test_claim(self):
        self.assertEqual(verify_claim(BASE, BASE.replace("| Unassigned |", "| @casey |", 1), "casey"), "25-cloud")

    def test_cannot_change_anything_else(self):
        claimed = BASE.replace("| Unassigned |", "| @casey |", 1)
        cases = {
            "wrong person": BASE.replace("| Unassigned |", "| @other |", 1),
            "two projects": claimed.replace("| Unassigned |", "| @casey |", 1),
            "project scope": claimed.replace("Alpha", "Renamed"),
            "project status": claimed.replace("queued", "active", 1),
            "extra line": claimed + "a malicious extra line\n",
            "header edit": claimed.replace("# Projects", "# Projects!"),
            "no edit": BASE,
        }
        for reason, content in cases.items():
            with self.subTest(reason=reason), self.assertRaises(ValueError):
                verify_claim(BASE, content, "casey")

    def test_unrelated_catalog_updates_do_not_block_claim(self):
        claimed = BASE.replace("| Unassigned |", "| @casey |", 1)
        main = BASE.replace("Beta | Goal", "Beta | Another updated goal")
        self.assertEqual(verify_live_claim(BASE, claimed, main, "casey"), "25-cloud")
        # Changes to the actual project, including ownership, scope or status,
        # require a rebase or a human review.
        for changed in (
            BASE.replace("| Unassigned |", "| @another |", 1),
            BASE.replace("Alpha | Goal", "Alpha | Different goal"),
            BASE.replace("| queued |", "| blocked |", 1),
        ):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                verify_live_claim(BASE, claimed, changed, "casey")

    def test_cannot_steal_owner(self):
        old = BASE.replace("Unassigned", "@alex", 1)
        with self.assertRaisesRegex(ValueError, "not unassigned"):
            verify_claim(old, old.replace("@alex", "@casey"), "casey")

    def test_blocked_or_active_projects_cannot_be_claimed(self):
        for status in ("blocked", "active", "done"):
            original = BASE.replace("| queued |", "| " + status + " |", 1)
            claimed = original.replace("| Unassigned |", "| @casey |", 1)
            with self.subTest(status=status), self.assertRaises(ValueError):
                verify_claim(original, claimed, "casey")

    def test_privileged_claims_refuse_unprotected_main(self):
        from claim_project import main_has_protection
        with patch("claim_project.api", return_value={"protected": False}):
            self.assertFalse(main_has_protection("banodoco/astrid-dev"))
        with patch("claim_project.api", return_value={"protected": True}):
            self.assertTrue(main_has_protection("banodoco/astrid-dev"))

    def test_eligibility_filters_untrusted_prs(self):
        p = {"state": "open", "draft": False,
             "base": {"ref": "main", "repo": {"full_name": "banodoco/astrid-dev"}},
             "head": {"sha": "a"*40, "repo": {"full_name": "casey/astrid-dev"}},
             "user": {"login": "casey", "type": "User"}}
        changed = [{"filename": "plans/index.md", "status": "modified"}]
        self.assertTrue(eligible(p, "banodoco/astrid-dev", "a"*40, changed))
        self.assertFalse(eligible(p, "banodoco/astrid-dev", "b"*40, changed))
        self.assertFalse(eligible(p, "banodoco/astrid-dev", "a"*40,
                                  changed + [{"filename": "scripts/evil.py", "status": "added"}]))
        self.assertFalse(eligible({**p, "draft": True}, "banodoco/astrid-dev", "a"*40, changed))
        self.assertFalse(eligible({**p, "user": {"login": "casey", "type": "Bot"}},
                                  "banodoco/astrid-dev", "a"*40, changed))

if __name__ == "__main__":
    unittest.main()
