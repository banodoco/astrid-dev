"""Exercise the actual release status reader and explicit snapshot lifecycle."""
import contextlib
import io
from pathlib import Path
import tempfile
import unittest

from release_status import progress, report, run, snapshot, validate_change


BRIEF = """# Release 15 — Fixture

**Release:** 15
**State:** Draft

## Included plans

- [Plan 40](../plans/40-example/plan.md) — Example

## Branches

| Repository | Branch | Role | Cut at | State |
| --- | --- | --- | --- | --- |
| astrid-agent | release/15/plan-40 | plan 40 | abc | merged |

## Publication

Not pinned.
"""
PLAN = """# Example

**Project:** Example
**Goal:** A goal
**Status:** queued
**Owner:** Unassigned
**Estimate:** 2
**Waiting on:** A manager
"""
TASKS = """# Tasks

| Task / outcome | Route | Progress |
| --- | --- | --- |
| T1 example | N | [x] merge |
| T2 example | X | [ ] pending |
| T3 example | N | Release 16 |

| Other | Progress |
| --- | --- |
| Not a card | [x] |
"""


class ReleaseStatusTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.path = self.root / "releases/15.md"
        self.path.parent.mkdir()
        self.path.write_text(BRIEF, encoding="utf-8")
        self.plan = self.root / "plans/40-example"
        self.plan.mkdir(parents=True)
        (self.plan / "plan.md").write_text(PLAN, encoding="utf-8")
        (self.plan / "tasks.md").write_text(TASKS, encoding="utf-8")

    def invoke(self, **kwargs):
        with contextlib.redirect_stdout(io.StringIO()):
            return run(self.root, 15, **kwargs)

    def test_progress_only_task_tables(self):
        self.assertEqual(progress(TASKS), ({"ticked": 1, "open": 1, "other": 1}, ["T2", "T3"]))
        self.assertEqual(progress("no table"), (None, []))

    def test_queued_merged_and_partial_work_are_not_done(self):
        body = report(self.root, 15, BRIEF)
        self.assertIn("queued | Unassigned | 1 / 1 / 1 | merged", body)
        self.assertIn("reconcile queued status", body)
        self.assertIn("T2, T3", body)
        self.assertIn("review whole-plan versus release-slice", body)
        self.assertNotIn("| done |", body)

    def test_read_only_refresh_check_and_drift(self):
        self.assertEqual(self.invoke(), 0)
        self.assertEqual(self.path.read_text(), BRIEF)
        self.assertEqual(self.invoke(check=True), 1)
        self.assertEqual(self.invoke(refresh=True), 0)
        first = self.path.read_text()
        self.assertEqual(self.invoke(check=True), 0)
        self.assertEqual(self.invoke(refresh=True), 0)
        self.assertEqual(first, self.path.read_text())
        self.assertEqual(first.replace("## Plan status snapshot\n\n<!-- release-status:start -->\n" + snapshot(first) + "<!-- release-status:end -->\n\n", ""), BRIEF)
        (self.plan / "plan.md").write_text(PLAN.replace("queued", "active").replace("Unassigned", "Manager"))
        self.assertEqual(self.invoke(check=True), 1)
        self.assertEqual(self.invoke(refresh=True), 0)
        self.assertEqual(self.invoke(check=True), 0)

    def test_final_never_reads_current_plan_or_refreshes(self):
        self.invoke(refresh=True)
        final = self.path.read_text().replace("**State:** Draft", "**State:** Final")
        self.path.write_text(final)
        (self.plan / "plan.md").unlink()
        self.assertEqual(self.invoke(), 0)
        with self.assertRaisesRegex(ValueError, "historical"):
            self.invoke(refresh=True)
        self.assertEqual(self.path.read_text(), final)

    def test_bad_markers_and_membership(self):
        self.path.write_text(BRIEF + "\n<!-- release-status:start -->\n")
        with self.assertRaisesRegex(ValueError, "markers"):
            self.invoke(refresh=True)
        with self.assertRaisesRegex(ValueError, "ambiguous"):
            report(self.root, 15, BRIEF.replace("Plan 40", "Plan 41"))

    def test_pr_gate_checks_changed_snapshot_and_final_transition(self):
        self.assertEqual(validate_change(self.root, 15, BRIEF, BRIEF), [])
        self.assertTrue(validate_change(self.root, 15, BRIEF, BRIEF.replace("Draft", "Final")))
        self.invoke(refresh=True)
        current = self.path.read_text()
        self.assertEqual(validate_change(self.root, 15, BRIEF, current), [])
        tampered = current.replace("| queued |", "| done |")
        self.assertTrue(validate_change(self.root, 15, current, tampered))
        (self.plan / "plan.md").write_text(PLAN.replace("queued", "active").replace("Unassigned", "Manager"))
        self.assertEqual(validate_change(self.root, 15, current, current), [])
        self.assertTrue(validate_change(self.root, 15, current, current.replace("Draft", "Final")))
        self.invoke(refresh=True)
        fresh = self.path.read_text()
        final = fresh.replace("Draft", "Final")
        self.assertEqual(validate_change(self.root, 15, current, final), [])
        self.assertTrue(validate_change(self.root, 15, final, final.replace("| active |", "| done |")))
        self.assertTrue(validate_change(self.root, 15, fresh, BRIEF))

    def test_legacy_final_backfill_without_snapshot(self):
        old = BRIEF.replace("Release 15", "Release 14").replace("**Release:** 15", "**Release:** 14")
        self.assertEqual(validate_change(self.root, 14, old, old.replace("Draft", "Final")), [])

    def test_missing_progress_and_partial_landing(self):
        (self.plan / "tasks.md").unlink()
        extra = "| astrid-runtime | release/15/plan-40 | plan 40 | abc | open |\n"
        body = report(self.root, 15, BRIEF.replace("\n## Publication", "\n" + extra + "\n## Publication"))
        self.assertIn("not recorded | partial", body)
        self.assertIn("no readable task Progress table", body)


if __name__ == "__main__":
    unittest.main()
