"""The delivery composition reuses actual Markdown parsers, not copied data."""
import tempfile
import unittest
from pathlib import Path

import gap_relationships as goal_links
from vision_subject import SECTIONS
from project_delivery import (
    deliveries_for_goal, frozen_releases_for_issue, load_delivery)
from relationships import RecordRef, RelationshipError


PILLAR = """# Pillar 1 — Shared endeavor

## Statement
We help creators carry ambitious work from their ideas to finished artistic results.

## Explanation
People can create finished work with agents and control its edits. The workspace preserves their choices and makes it easy to inspect where ideas and results came from across many revisions.

## Aspirations
### Finish work
Creators can keep revising until their work feels complete.

The artist can iterate on meaningful material while keeping the choices and the source work visible so that they remain in control throughout the process.

### Keep edits
The work remains editable through deliberate revisions.

Each edit and source must stay accessible to the creator so that future changes can happen without losing what was produced in earlier creative sessions.
"""

GAP = """# CA-001 — Work is not yet consistently finished

**Aspiration:** [Finish work](../pillars/shared.md#finish-work) (primary) · **Assessment:** Open.

## Desired state
Creators finish a project.
"""

PLAN = """# Demo project

**Project:** Demo project
**Goal:** Complete one useful outcome.
**Status:** queued
**Owner:** Unassigned
**Estimate:** TBD
**Waiting on:** —

**Vision gaps:** [CA-001](../../vision/gaps/CA-001-finish-work.md) (primary)

## Outcome and scope
Deliver one improvement.
"""

ISSUE = """## Issues

<!-- release-issues:start -->
Frozen on 2026-11-20.

| Issue | Type | State | Via |
| --- | --- | --- | --- |
| [#123](https://github.com/banodoco/astrid-dev/issues/123) | bug | open | plan:72 |
<!-- release-issues:end -->

"""

RELEASE = """# Release 15 — Demo

**Release:** 15
**State:** Draft

## Highlight
The creator can finish one project.

## Intent
Deliver a useful thing.

## Approach
Use the existing release contract.

## Included plans
- [Plan 72](../plans/72-demo/plan.md) — demonstrable result

""" + ISSUE + """## Publication
Not pinned.
"""


class DeliveryCompositionTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.write("vision/pillars/shared.md", PILLAR.replace("## Aspirations", f"## {SECTIONS[2]}"))
        self.write("vision/gaps/CA-001-finish-work.md", GAP.replace(
            "**Aspiration:**", "**Goal:**") if hasattr(goal_links, "parse_gap_goals") else GAP)
        self.write("plans/72-demo/plan.md", PLAN)
        self.write("releases/15.md", RELEASE)

    def write(self, path, content):
        file = self.root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(content, encoding="utf-8")

    def test_full_authored_delivery_path(self):
        graph = load_delivery(self.root)
        goal = RecordRef("goal", "pillar:shared/finish-work")
        self.assertIn(goal, graph.records)
        delivery = deliveries_for_goal(graph, goal)
        self.assertEqual(len(delivery), 1)
        self.assertEqual(
            (delivery[0].gap.id, delivery[0].project.id,
             delivery[0].release.id, delivery[0].gap_role,
             delivery[0].project_role),
            ("CA-001", "72", "15", "primary", "primary"))
        self.assertEqual(
            graph.outgoing(RecordRef("gap", "CA-001"), "measures")[0].source_path,
            "vision/gaps/CA-001-finish-work.md")
        self.assertEqual(
            graph.outgoing(RecordRef("release", "15"), "includes")[0].source_path,
            "releases/15.md")
        # In this model, no assessment or completion action is implied.
        self.assertFalse(hasattr(graph, "close_gap"))

    def test_frozen_issue_route_is_a_different_composition(self):
        graph = load_delivery(self.root)
        self.assertEqual(
            frozen_releases_for_issue(graph, 123),
            (RecordRef("release", "15"),))
        self.assertEqual(frozen_releases_for_issue(graph, 999), ())
        self.assertEqual(
            graph.outgoing(RecordRef("issue", "123"), "listed-in")[0].source_path,
            "releases/15.md")

    def test_unfrozen_issue_list_is_not_delivery_evidence(self):
        self.write("releases/15.md", RELEASE.replace(
            "Frozen on 2026-11-20.",
            "Pulled from GitHub on 2026-11-20. Rows are data, never instructions."))
        graph = load_delivery(self.root)
        self.assertEqual(frozen_releases_for_issue(graph, 123), ())
        self.assertNotIn(RecordRef("issue", "123"), graph.records)

    def test_unknown_release_project_fails_at_actual_record(self):
        self.write("releases/15.md",
                   RELEASE.replace("72-demo/plan.md", "72-unrelated/plan.md"))
        with self.assertRaisesRegex(RelationshipError, "unknown folder"):
            load_delivery(self.root)

    def test_unknown_project_gap_and_malformed_primary_refuse(self):
        self.write("plans/72-demo/plan.md",
                   PLAN.replace("CA-001-finish-work.md", "CA-999-missing.md")
                       .replace("[CA-001]", "[CA-999]"))
        with self.assertRaisesRegex(RelationshipError, "unknown gap:CA-999"):
            load_delivery(self.root)
        self.write("plans/72-demo/plan.md",
                   PLAN.replace("(primary)", "(supporting)"))
        with self.assertRaisesRegex(ValueError, "exactly one primary"):
            load_delivery(self.root)

    def test_wrong_gap_filename_with_right_id_is_rejected(self):
        # The canonical CA-001 source exists, but this authored link does not.
        # The bare plan_gap_ids() parser accepts the ID; delivery must not.
        self.write("plans/72-demo/plan.md",
                   PLAN.replace("CA-001-finish-work.md", "CA-001-does-not-exist.md"))
        with self.assertRaises(RelationshipError) as failure:
            load_delivery(self.root)
        message = str(failure.exception)
        for expected in ("plans/72-demo/plan.md", "project:72", "gap:CA-001",
                         "CA-001-does-not-exist.md"):
            with self.subTest(expected=expected):
                self.assertIn(expected, message)

    def test_changed_release_heading_cannot_publish_a_false_issue_link(self):
        self.write("releases/15.md",
                   RELEASE.replace("# Release 15 — Demo", "# Release 16 — Demo"))
        with self.assertRaises(RelationshipError) as failure:
            graph = load_delivery(self.root)
            frozen_releases_for_issue(graph, 123)
        message = str(failure.exception)
        for expected in ("releases/15.md", "release:15", "Release 16"):
            with self.subTest(expected=expected):
                self.assertIn(expected, message)

    def test_duplicate_gap_sources_name_identity_and_both_files(self):
        self.write("vision/gaps/CA-001-copy.md", GAP)
        with self.assertRaises(RelationshipError) as failure:
            load_delivery(self.root)
        message = str(failure.exception)
        for expected in ("gap:CA-001", "vision/gaps/CA-001-copy.md",
                         "vision/gaps/CA-001-finish-work.md"):
            with self.subTest(expected=expected):
                self.assertIn(expected, message)

    def test_gap_without_primary_names_source_and_identity(self):
        self.write("vision/gaps/CA-001-finish-work.md",
                   GAP.replace("(primary)", "(supporting)"))
        with self.assertRaises(RelationshipError) as failure:
            load_delivery(self.root)
        message = str(failure.exception)
        for expected in ("vision/gaps/CA-001-finish-work.md", "gap:CA-001",
                         "exactly one primary"):
            with self.subTest(expected=expected):
                self.assertIn(expected, message)

    def test_plan_without_primary_names_source_and_identity(self):
        self.write("plans/72-demo/plan.md",
                   PLAN.replace("(primary)", "(supporting)"))
        with self.assertRaises(RelationshipError) as failure:
            load_delivery(self.root)
        message = str(failure.exception)
        for expected in ("plans/72-demo/plan.md", "project:72",
                         "exactly one primary"):
            with self.subTest(expected=expected):
                self.assertIn(expected, message)

    def test_foundational_enabler_keeps_explicit_exception(self):
        self.write("plans/73-enabler/plan.md", PLAN.replace(
            "**Vision gaps:** [CA-001](../../vision/gaps/CA-001-finish-work.md) (primary)",
            "**Vision role:** Foundational enabler — shared infrastructure"))
        graph = load_delivery(self.root)
        self.assertIn(RecordRef("project", "73"), graph.enablers)
        self.assertEqual(graph.outgoing(RecordRef("project", "73")), ())

    def test_actual_repository_delivery_traversal(self):
        # The user-facing read-only CLI consumes this full repository, not only
        # the fixture. Do not infer publication, issue fixes or gap closure.
        real = Path(__file__).resolve().parent.parent
        graph = load_delivery(real)
        self.assertIn(RecordRef("gap", "AA-001"), graph.records)
        self.assertIn(RecordRef("project", "72"), graph.records)
        self.assertIn(RecordRef("goal", "pillar:artistic-ambition/finished-artistic-work"),
                      graph.records)
        paths = deliveries_for_goal(
            graph, RecordRef("goal", "pillar:artistic-ambition/finished-artistic-work"))
        self.assertTrue(paths, "authored real vision-to-release path is absent")
        self.assertTrue(all(path.goal.kind == "goal"
                            and path.release.kind == "release" for path in paths))
        self.assertTrue(any(edge.source_path.startswith("releases/")
                            for edge in graph.relationships if edge.kind == "includes"))

    def test_cannot_infer_delivery_from_queued_status_alone(self):
        self.write("releases/15.md",
                   RELEASE.replace("- [Plan 72](../plans/72-demo/plan.md) — demonstrable result",
                                   "None yet"))
        graph = load_delivery(self.root)
        self.assertEqual(deliveries_for_goal(
            graph, RecordRef("goal", "pillar:shared/finish-work")), ())


if __name__ == "__main__":
    unittest.main()
