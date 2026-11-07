"""Focused checks for the project decision record and issue/project distinction."""
import subprocess
import tempfile
import unittest
from pathlib import Path
from check_project_planning import validate_pack, changed_projects

DRAFT = """# Inputs

## Planning evidence

**Scope decision:** Pending — The end state is not yet chosen. Next: ask the owner to select the outcome.
**Prior art:** Pending — The current implementation is unknown. Next: inspect relevant product paths.
**Approach:** Pending — We have not evaluated reuse. Next: compare existing pack and core.
**Challenge:** Pending — Consequence is not clear. Next: determine whether independent review is needed.
**Proof and limits:** Pending — No acceptance scenario exists. Next: define a real user test.
"""

ACCEPTED = """# Inputs

## Planning evidence

**Scope decision:** Accepted — Owner chose a bounded outcome in https://github.com/banodoco/astrid-dev/issues/99.
**Prior art:** https://github.com/banodoco/astrid-app/tree/main documents the existing behavior, and related issue #99 records the remaining gap.
**Approach:** Reuse the established extension path instead of a new host; avoid replacing working editor foundations.
**Challenge:** Not needed — This choice changes one existing adapter, not a shared architecture or cross-repository contract.
**Proof and limits:** Test the actual exported artifact at the intended size; one unsupported codec must fail clearly.
"""

REVIEWED = ACCEPTED.replace(
    "**Challenge:** Not needed — This choice changes one existing adapter, not a shared architecture or cross-repository contract.",
    "**Challenge:** Reviewed — https://github.com/banodoco/astrid-dev/issues/100 records the independent simplification critique."
)

class PlanningTests(unittest.TestCase):
    def test_draft_can_be_honestly_pending(self):
        self.assertEqual(validate_pack("28-example", DRAFT), [])

    def test_accepted_with_justified_skipped_or_actual_challenge(self):
        self.assertEqual(validate_pack("28-example", ACCEPTED), [])
        self.assertEqual(validate_pack("28-example", REVIEWED), [])

    def test_unsubstantiated_approval_or_prior_art_fails(self):
        bad = ACCEPTED.replace("https://github.com/banodoco/astrid-dev/issues/99", "someone said yes")
        self.assertTrue(any("owner decision" in x for x in validate_pack("28-example", bad)))
        bad = ACCEPTED.replace("https://github.com/banodoco/astrid-app/tree/main", "We looked around")
        self.assertTrue(any("Prior art" in x for x in validate_pack("28-example", bad)))

    def test_pending_and_missing_record(self):
        bad = DRAFT.replace("Next: inspect relevant product paths.", "Will investigate.")
        self.assertTrue(any("Prior art" in x for x in validate_pack("28-example", bad)))
        bad = ACCEPTED.replace("**Approach:** Reuse the established extension path instead of a new host; avoid replacing working editor foundations.",
                               "**Approach:** Pending — We will decide. Next: compare options.")
        self.assertTrue(any("cannot leave" in x for x in validate_pack("28-example", bad)))
        self.assertTrue(any("Planning evidence" in x for x in validate_pack("28-example", "# Inputs\n")))

    def test_duplicate_field_and_unreviewed_challenge(self):
        self.assertTrue(any("duplicate" in x for x in
                            validate_pack("28-example", ACCEPTED + "\n**Prior art:** another source")))
        bad = ACCEPTED.replace("**Challenge:** Not needed — This choice changes one existing adapter, not a shared architecture or cross-repository contract.",
                               "**Challenge:** Reviewed — I asked another agent.")
        self.assertTrue(any("source reference" in x for x in validate_pack("28-example", bad)))

    def test_only_projects_trigger_evidence_gate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            def git(*args: str) -> str:
                return subprocess.check_output(["git", *args], cwd=root, text=True).strip()
            git("init", "-q")
            git("config", "user.name", "Test")
            git("config", "user.email", "test@example.com")
            legacy = root / "strategy/projects/20-old"
            legacy.mkdir(parents=True)
            (legacy / "plan.md").write_text("# Old\n")
            (legacy / "inputs.md").write_text("# Inputs\nNo record yet\n")
            git("add", ".")
            git("commit", "-qm", "baseline")
            base = git("rev-parse", "HEAD")
            issue = root / "docs/quick-bugfix.md"
            issue.parent.mkdir()
            issue.write_text("Small issue: no new project.\n")
            (legacy / "plan.md").write_text("# Old\nMinor edit\n")
            git("add", ".")
            git("commit", "-qm", "issue and legacy edit")
            self.assertEqual(changed_projects(base, root), set())
            new = root / "strategy/projects/28-new"
            new.mkdir()
            (new / "plan.md").write_text("# New\n")
            (new / "inputs.md").write_text(DRAFT)
            git("add", ".")
            git("commit", "-qm", "new draft")
            self.assertEqual(changed_projects(base, root), {"28-new"})
            (legacy / "inputs.md").write_text(DRAFT)
            git("add", ".")
            git("commit", "-qm", "legacy opts in")
            self.assertEqual(changed_projects(base, root), {"20-old", "28-new"})


if __name__ == "__main__":
    unittest.main()
