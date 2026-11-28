import json
import tempfile
import unittest
from pathlib import Path
from datetime import datetime, timezone
from unittest import mock

import boards

NOW = datetime(2026, 11, 24, 12, 0, tzinfo=timezone.utc)
BODY = """| Role | Mailbox name | Who |
| --- | --- | --- |
| Lead | `r15-release-lead` | Claude session `session_LEAD1` |
| Orchestrator | `r15-p87-orchestrator` | lane session `session_ORCH1`: writes packets |
| Manager | `r15-p87-manager-1` | Starts sessions |
| Packet sessions | `r15-<packet>-<n>` | One packet each |
"""
BOARD = {"title": "board: release 15 plan 87", "number": 1776, "body": BODY}


def comment(when, sender, extra=""):
    return {"created_at": when, "body": f"run: r15\nfrom: x\nfrom_session: {sender}\nto: all\n\n{extra}"}


FIXTURE = json.loads(json.dumps([
    comment("2026-11-24T11:30:00Z", "r15-p87-orchestrator", "session: session_ORCH2"),
    comment("2026-11-24T08:00:00Z", "r15-p87-orchestrator"),
    comment("2026-11-24T11:00:00Z", "session_PKT9"),
    comment("2026-11-24T05:00:00Z", "r15-P87-01-1"),
]))


class BoardsTest(unittest.TestCase):
    def test_table_skips_placeholders_and_header(self):
        self.assertEqual(boards.parse_table(BODY), {
            "r15-release-lead": "session_LEAD1", "r15-p87-orchestrator": "session_ORCH1", "r15-p87-manager-1": None})

    def test_posts_keep_last_time_and_newest_announce(self):
        p = boards.parse_posts(FIXTURE)
        self.assertEqual(p["r15-p87-orchestrator"], {"last": "2026-11-24T11:30:00Z", "session": "session_ORCH2"})
        self.assertEqual(p["session_PKT9"]["session"], "session_PKT9")

    def test_flags(self):
        rows = {r["name"]: r for r in boards.rows_for(BOARD, FIXTURE, NOW)}
        self.assertEqual(rows["r15-p87-orchestrator"]["flags"], [])
        self.assertEqual(rows["r15-p87-orchestrator"]["session"], "session_ORCH2")
        self.assertEqual(rows["r15-p87-orchestrator"]["age_hours"], 0.5)
        self.assertEqual(rows["r15-P87-01-1"]["flags"], ["QUIET"])
        self.assertEqual(rows["r15-p87-manager-1"]["flags"], ["STALE-ROSTER"])
        self.assertEqual(rows["r15-release-lead"]["session"], "session_LEAD1")
        self.assertNotIn("STALE-ROSTER", rows["r15-P87-01-1"]["flags"])

    def test_find_boards_filters_titles_and_roster_output(self):
        items = [{"title": "board: release 15 lead", "number": 2}, {"title": "board: release 150 x", "number": 3},
                 {"title": "board: release 15", "number": 1}]
        with mock.patch.object(boards, "api", return_value={"items": items}):
            self.assertEqual([b["number"] for b in boards.find_boards("15")], [1, 2])
        text = boards.render(boards.rows_for(BOARD, FIXTURE, NOW))
        self.assertIn("STALE-ROSTER", text)
        self.assertIn("r15-p87-orchestrator", text)

    def test_roster_finds_lane_boards_for_briefs_listing_the_release(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            briefs = root / "releases" / "16" / "briefs"
            briefs.mkdir(parents=True)
            for lane, releases in (("h3", "16, continuing in 17"), ("later", "17")):
                (briefs / f"{lane}.md").write_text(
                    f"# Lane brief — {lane}\n\n**Lane:** {lane}\n**Releases:** {releases}\n\n## Outcome\n\nFixture.\n",
                    encoding="utf-8")
            items = {"board: lane h3": [{"title": "board: lane h3", "number": 2100}],
                     "board: release 16": [{"title": "board: release 16 plan 66", "number": 2101},
                                           {"title": "board: lane h3 old", "number": 2999}]}
            queries = []

            def fake_api(path):
                queries.append(path)
                key = "board: lane h3" if "lane%20h3" in path else "board: release 16"
                return {"items": items.get(key, [])}

            with mock.patch.object(boards, "api", side_effect=fake_api):
                found = boards.find_boards("16", root)
                self.assertEqual([b["title"] for b in found], ["board: lane h3", "board: release 16 plan 66"])
                self.assertEqual(boards.lane_names("16", root), ["h3"])
                self.assertEqual(boards.lane_names("17", root), ["h3", "later"])
                self.assertFalse(any("later" in q for q in queries))

    def test_comments_pages_until_short_page(self):
        pages = [[{"n": i} for i in range(100)], [{"n": 100}]]
        with mock.patch.object(boards, "api", side_effect=pages) as m:
            self.assertEqual(len(boards.comments(5)), 101)
        self.assertIn("page=2", m.call_args[0][0])


if __name__ == "__main__":
    unittest.main()
