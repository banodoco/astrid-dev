"""Focused project-pack evidence tests; do not require retroactive legacy migration."""
import subprocess
import tempfile
import unittest
from pathlib import Path

from check_project_planning import changed_projects, validate_pack

DRAFT = """# Inputs: Example

## Planning evidence

**Scope decision:** Pending — The owner has not yet selected a specific outcome. Next: present the end-state options and record the owner's choice.

### Prior art and behavior traced

Pending — Current repositories and reuse paths have not been mapped. Next: inspect existing sources, record relevant revisions and trace input through output.

### Reuse and placement decision

Pending — There is no justified choice of existing pack, new pack or core. Next: compare each option and document the smallest viable approach.

### Independent simplification challenge

Pending — A separate high-judgment review has not taken place. Next: ask a distinct planner for concrete removals and record decisions.

### End-state options and owner choice

Pending — Ten meaningful alternatives have not been presented to the owner. Next: record options and the owner's actual selected outcome.

### Assumptions and evidence limits

Pending — Environment and source identity limitations remain unknown. Next: distinguish observed behavior from assumptions and named blockers.
"""

ACCEPTED = """# Inputs: Example

## Planning evidence

**Scope decision:** Accepted — The owner chose a bounded behavior and accepted the tradeoff; recorded at https://github.com/example/decision/1.

### Prior art and behavior traced

Reviewed https://github.com/banodoco/astrid-app/tree/main. Followed the input to the existing output contract; found useful extension code and one unimplemented path, rather than assuming the feature was absent.

### Reuse and placement decision

Reuse the current extension path, not a new host or core framework. The existing work supports the necessary interaction, while the custom path adds an extra maintenance surface without changing the result.

### Independent simplification challenge

Independent planner review https://github.com/example/review/2 proposed removing a registry and reusing the existing adapter; kept the simpler solution, documented the only lost optional feature.

### End-state options and owner choice

Ten concrete end states and alternatives are preserved at https://github.com/example/options/3. The owner chose the smallest working integration and rejected a generalized engine for this stage.

### Assumptions and evidence limits

Observed that the existing adapter handles requests; platform compatibility has not been verified and must be checked in the assigned task. This is a scoped assertion, not release evidence.
"""


class ProjectPlanningEvidenceTests(unittest.TestCase):
    def test_pending_draft_has_actionable_gaps_and_is_valid(self):
        self.assertEqual(validate_pack("28-example", DRAFT), [])

    def test_accepted_pack_requires_recorded_sources(self):
        self.assertEqual(validate_pack("28-example", ACCEPTED), [])

    def test_acceptance_cannot_hide_unperformed_challenge(self):
        bad = ACCEPTED.replace(
            "Independent planner review https://github.com/example/review/2 proposed removing a registry and reusing the existing adapter; kept the simpler solution, documented the only lost optional feature.",
            "Pending — No challenge has taken place. Next: ask a separate high-judgment planner for critique and record the outcome.")
        self.assertTrue(any("cannot leave" in e for e in validate_pack("28-example", bad)))

    def test_poor_draft_and_unsourced_acceptance_fail(self):
        bad = DRAFT.replace(
            "Pending — Current repositories and reuse paths have not been mapped. Next: inspect existing sources, record relevant revisions and trace input through output.",
            "Pending — TBD.")
        self.assertTrue(any("Prior art" in e for e in validate_pack("28-example", bad)))
        bad = ACCEPTED.replace(
            "https://github.com/example/decision/1", "the owner said yes")
        self.assertTrue(any("owner decision" in e for e in validate_pack("28-example", bad)))

    def test_missing_planning_evidence_fails(self):
        self.assertTrue(any("Planning evidence" in e for e in
                            validate_pack("28-example", "# Inputs\n## What we build on\nAn old plan.")))

    def test_only_new_or_opted_in_packs_are_reviewed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            def git(*args):
                return subprocess.check_output(["git", *args], cwd=root, text=True).strip()
            git("init", "-q")
            git("config", "user.name", "Project test")
            git("config", "user.email", "project@example.com")
            legacy = root / "plans/20-legacy"
            legacy.mkdir(parents=True)
            (legacy / "plan.md").write_text("# Legacy\n", encoding="utf-8")
            (legacy / "inputs.md").write_text("# Inputs\nOld context\n", encoding="utf-8")
            git("add", ".")
            git("commit", "-qm", "base")
            base = git("rev-parse", "HEAD")
            (legacy / "inputs.md").write_text("# Inputs\nMinor legacy correction\n", encoding="utf-8")
            new = root / "plans/28-example"
            new.mkdir(parents=True)
            (new / "plan.md").write_text("# New plan\n", encoding="utf-8")
            (new / "inputs.md").write_text(DRAFT, encoding="utf-8")
            git("add", ".")
            git("commit", "-qm", "new draft and legacy edit")
            self.assertEqual(changed_projects(base, root), {"28-example"})
            (legacy / "inputs.md").write_text(DRAFT, encoding="utf-8")
            git("add", ".")
            git("commit", "-qm", "legacy adopts evidence")
            self.assertEqual(changed_projects(base, root), {"20-legacy", "28-example"})


if __name__ == "__main__":
    unittest.main()
