"""Focused tests for milestone ownership, filters and strategy projection."""
import argparse
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

import project_query as query
import records
import views
from check_docs import release_errors


def plan(name, status="queued", owner="Unassigned", target=None):
    return (f"# {name}\n\n**Project:** {name}\n**Goal:** A useful {name} outcome.\n"
            f"**Status:** {status}\n**Owner:** {owner}\n**Estimate:** TBD\n**Waiting on:** —\n"
            + (f"**Target milestone:** {target}\n" if target is not None else "")
            + "\n## Outcome and scope\n**Target milestone:** 9.9\n")


def brief(n, kind, folder, state="Draft"):
    return (f"# Release {n} — Example\n\n**Release:** {n}\n**State:** {state}\n**Kind:** {kind}\n\n"
            "## Highlight\n\nA substantive creator-facing change.\n\n## Intent\n\nWhy.\n\n## Approach\n\nHow.\n\n"
            f"## Included plans\n\n- [Plan {folder.split('-')[0]}](../plans/{folder}/plan.md) — A useful contribution.\n\n"
            "## Publication\n\nNot pinned.\n")


class TargetTests(unittest.TestCase):
    def test_optional_header_and_invalid_values(self):
        self.assertIsNone(records.project_target_milestone(plan("One")))
        self.assertEqual(records.project_target_milestone(plan("One", target="0.5")), "0.5")
        self.assertEqual(set(records.project_fields(plan("One", target="0.5"))), set(records.PROJECT_FIELDS))
        for value in ("", "0.5.0", "next", "00.5", "0.05", "0.5 | 0.6"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                records.project_fields(plan("One", target=value))
        with self.assertRaisesRegex(ValueError, "duplicated"):
            records.project_fields(plan("One", target="0.5").replace("**Target milestone:** 0.5", "**Target milestone:** 0.5\n**Target milestone:** 0.6"))

    def test_three_digit_release_links(self):
        text = brief(7, "minor", "106-tool")
        self.assertEqual(records.release_brief(text)["plan_links"], [("106", "106-tool")])
        # This fixture predates branch-table enforcement; ensure the same
        # full ID comparison is also used by the actual docs validator.
        self.assertFalse(any("number does not match" in e for e in release_errors("7.md", text)))
        wrong = text.replace("[Plan 106]", "[Plan 10]")
        self.assertTrue(any("number does not match" in e for e in release_errors("7.md", wrong)))


class ProjectQueryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "plans").mkdir()
        (self.root / "releases").mkdir()
        (self.root / "strategy.md").write_text(
            "# Path\n\n## Versions\n\n" + "\n\n".join(
                f"### Version 0.{n}\n\n**Aim:** Demo.\n\n<!-- strategy-0.{n}:start -->\n<!-- strategy-0.{n}:end -->" for n in range(1, 10)
            ) + "\n\n### Version 1.0\n\n**Aim:** Demo.\n\n## Decisions\n",
            encoding="utf-8")
        for folder, value in {
            "10-derived": plan("Derived", "active", "Ada"),
            "57-storage": plan("Storage", target="0.3"),
            "99-late": plan("Late", "paused", "Ada", "0.1"),
            "100-early": plan("Early", target="0.5"),
            "101-untargeted": plan("Untargeted", "blocked"),
            "102-history": plan("History", "done", "Ada"),
        }.items():
            path = self.root / "plans" / folder / "plan.md"
            path.parent.mkdir()
            path.write_text(value, encoding="utf-8")
        for n, kind, folder, state in ((1,"patch","102-history","Final"), (2,"minor","10-derived","Draft"), (3,"patch","99-late","Draft"), (4,"minor","100-early","Draft")):
            (self.root / "releases" / f"{n}.md").write_text(brief(n, kind, folder, state), encoding="utf-8")
        (self.root / "plans/priority.md").write_text("# Priority\n\n## Order\n\n- 57-storage\n- 10-derived\n", encoding="utf-8")

    def test_query_pending_owner_target_release_and_late(self):
        rows = query.load_projects(self.root)
        def ids(**kwargs):
            return [r["id"] for r in query.filter_projects(rows, **kwargs)]
        self.assertEqual(ids(pending=True), [57, 10, 100, 101, 99])
        self.assertEqual(ids(pending=True, owner="unassigned", unallocated=True), [57,101])
        self.assertEqual(ids(milestone="0.1"), [10,99])
        self.assertEqual(ids(milestone="0.5", pending=True), [100])
        self.assertEqual(ids(late=True), [99])
        self.assertEqual(ids(release=1), [102])
        self.assertEqual(ids(statuses=["blocked"], milestone="unassigned"), [101])
        self.assertEqual(ids(search="storage"), [57])
        self.assertEqual(next(r for r in rows if r["id"] == 102)["target_milestone"], None)
        self.assertEqual(next(r for r in rows if r["id"] == 100)["target_source"], "explicit")

    def test_unknown_target_refused(self):
        p = self.root / "plans/57-storage/plan.md"
        p.write_text(plan("Storage", target="8.8"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "no authored strategy milestone"):
            query.load_projects(self.root)

    def test_strategy_only_unallocated_and_late_links(self):
        rendered = views._strategy(self.root, "0.3")
        region = rendered.split("<!-- strategy-0.3:start -->")[1].split("<!-- strategy-0.3:end -->")[0]
        self.assertIn("**Targeted projects (not allocated):** [Plan 57](plans/57-storage/plan.md)", region)
        first = views._strategy(self.root, "0.1").split("<!-- strategy-0.1:start -->")[1].split("<!-- strategy-0.1:end -->")[0]
        self.assertIn("**Later release allocation — review target:** [Plan 99]", first)
        self.assertNotIn("[Plan 10]", first)

    def test_json_cli_projection(self):
        parser = argparse.ArgumentParser()
        query.add_arguments(parser)
        args = parser.parse_args(["--pending", "--target-milestone", "0.3", "--json"])
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(query.run(self.root, args), 0)
        result = json.loads(output.getvalue())
        self.assertEqual([r["id"] for r in result], [57])
        self.assertEqual(result[0]["target_milestone"], "0.3")


if __name__ == "__main__":
    unittest.main()
