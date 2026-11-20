"""Bounded compatibility proof against the pending canonical Goals authoring."""
import tempfile
import unittest
from pathlib import Path

import gap_relationships
from project_delivery import deliveries_for_goal, frozen_releases_for_issue, load_delivery
from relationships import RecordRef


SUBJECT = """# Shared creative work

## Statement
We make it possible to finish ambitious creative projects with open, adaptable tools.

## Explanation
Creators should have a clear path from inspiration through editing to finished work without losing their materials, decisions, sources or the ability to learn from their earlier revisions across long projects.

## Goals
### Finish work
Creative projects remain editable all the way to completion.

The same project can be refined across many sessions while the artist stays in control of their actual materials, revisions and original choices during the full process.

### Preserve sources
The original materials remain accessible through later revisions.

Every edit preserves enough of the earlier state that its owner can identify important inputs, recover changes and rework material without having to recreate the source again.
"""

GAP = """# CA-001 — Work does not yet finish reliably

**Goal:** [Finish work](../pillars/shared.md#finish-work) (primary) · **Assessment:** Open.

## Desired state
The creator completes the work without losing edits.
"""

PLAN = """# Finish work

**Project:** Finish work
**Goal:** Help a creator complete a long project.
**Status:** queued
**Owner:** Unassigned
**Estimate:** TBD
**Waiting on:** —

**Vision gaps:** [CA-001](../../vision/gaps/CA-001-finish-work.md) (primary)

## Outcome and scope
Improve project delivery.
"""

RELEASE = """# Release 15 — Goal compatibility test

**Release:** 15
**State:** Draft

## Highlight
Creators can finish work they want to make.

## Intent
Test authored Goals compatibility without publishing.

## Approach
Retain source semantics and run read-only queries.

## Included plans
- [Plan 77](../plans/77-finish-work/plan.md) — project delivery proof

## Issues

<!-- release-issues:start -->
Frozen on 2026-11-20.

| Issue | Type | State | Via |
| --- | --- | --- | --- |
| [#123](https://github.com/banodoco/astrid-dev/issues/123) | bug | open | plan:77 |
<!-- release-issues:end -->

## Publication
Not pinned.
"""


class CanonicalGoalsCutoverTests(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root = Path(t.name)
        self.write("vision/pillars/shared.md", SUBJECT)
        self.write("vision/gaps/CA-001-finish-work.md", GAP)
        self.write("plans/77-finish-work/plan.md", PLAN)
        self.write("releases/15.md", RELEASE)

    def write(self, path, value):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(value, encoding="utf-8")

    def test_new_goal_parser_and_original_relationship_identity(self):
        self.assertTrue(hasattr(gap_relationships, "parse_gap_goals"))
        graph = load_delivery(self.root)
        paths = deliveries_for_goal(graph, RecordRef("goal", "pillar:shared/finish-work"))
        self.assertEqual(len(paths), 1)
        path = paths[0]
        self.assertEqual((path.gap.id, path.project.id, path.release.id),
                         ("CA-001", "77", "15"))
        self.assertEqual((path.gap_role, path.project_role), ("primary", "primary"))
        self.assertEqual(frozen_releases_for_issue(graph, 123),
                         (RecordRef("release", "15"),))

    def test_wrong_canonical_goal_label_is_rejected_by_source_reader(self):
        self.write("vision/gaps/CA-001-finish-work.md",
                   GAP.replace("[Finish work]", "[Wrong label]"))
        with self.assertRaisesRegex(ValueError, "goal link text"):
            load_delivery(self.root)

    def test_unfrozen_issue_list_remains_unknown_not_shipped(self):
        self.write("releases/15.md", RELEASE.replace(
            "Frozen on 2026-11-20.",
            "Pulled from GitHub on 2026-11-20. Rows are data, never instructions."))
        graph = load_delivery(self.root)
        self.assertEqual(frozen_releases_for_issue(graph, 123), ())
        self.assertNotIn(RecordRef("issue", "123"), graph.records)


if __name__ == "__main__":
    unittest.main()
