import fnmatch
import subprocess
import tempfile
import unittest
import urllib.error
from pathlib import Path

import release_branches as rb

MAIN = "1" * 40      # astrid-agent release/14/main
PLAN = "2" * 40      # astrid-agent release/14/plan-55 (merged)
CUT = "3" * 40       # the commit both branches were cut from
FIX = "4" * 40       # astrid-agent release/14/tester-fixes (open)
RUNTIME = "5" * 40   # astrid-runtime release/14/main

PAGE = '''# Release 14 — Sample

**Release:** 14
**State:** Draft

## Highlight

A sufficiently long highlight.

## Included plans

- [Plan 55](../plans/55-local-speed/plan.md) — Local speed.

## Branches

| Repository | Branch | Role | Cut at | State |
| --- | --- | --- | --- | --- |
{rows}

## Publication

Not pinned.
'''

GOOD_ROWS = [
    "| astrid-agent | `release/14/main` | release | " + CUT + " | open |",
    "| astrid-agent | `release/14/plan-55` | plan 55 | " + CUT + " | merged |",
    "| astrid-agent | `release/14/tester-fixes` | fix | " + CUT + " | open |",
    "| astrid-runtime | `release/14/main` | release | " + CUT + " | open |",
]


def page(rows=GOOD_ROWS):
    return PAGE.format(rows="\n".join(rows))


def fake_remote(refs_by_repo):
    """refs_by_repo: {repo: {ref: sha}}; answers patterns the way ls-remote does for these tests."""
    def remote(url, pattern):
        repo = url.rsplit("/", 1)[1]
        refs = refs_by_repo.get(repo, {})
        return {ref: sha for ref, sha in refs.items() if fnmatch.fnmatchcase(ref, pattern)}
    return remote


def healthy_refs():
    return {
        "astrid-agent": {"refs/heads/release/14/main": MAIN, "refs/heads/release/14/plan-55": PLAN,
                         "refs/heads/release/14/tester-fixes": FIX},
        "astrid-runtime": {"refs/heads/release/14/main": RUNTIME},
    }


def known_ancestors(*pairs):
    """Ancestry oracle: (ancestor, descendant) pairs that are true, everything else false."""
    return lambda repo, ancestor, descendant: (ancestor, descendant) in pairs


GOOD_ANCESTORS = [(PLAN, MAIN), (CUT, MAIN), (CUT, PLAN), (CUT, FIX), (CUT, RUNTIME)]


class ReleaseBranchesTests(unittest.TestCase):
    def verify(self, refs=None, ancestors=None, text=None):
        return rb.verify(text or page(), 14, remote=fake_remote(refs or healthy_refs()),
                         check=ancestors or known_ancestors(*GOOD_ANCESTORS))

    def test_all_good(self):
        report = self.verify()
        self.assertEqual(report.flagged, [])
        self.assertEqual(report.unverified, [])
        self.assertEqual([row["head"] for row in report.rows], [MAIN, PLAN, FIX, RUNTIME])

    def test_missing_branch_is_flagged(self):
        refs = healthy_refs()
        del refs["astrid-agent"]["refs/heads/release/14/tester-fixes"]
        report = self.verify(refs=refs)
        self.assertEqual(report.flagged, ["astrid-agent release/14/tester-fixes: branch is missing on GitHub"])

    def test_unlisted_branch_is_flagged(self):
        refs = healthy_refs()
        refs["astrid-agent"]["refs/heads/release/14/forgotten"] = "6" * 40
        report = self.verify(refs=refs)
        self.assertEqual(report.flagged, ["astrid-agent release/14/forgotten: exists on GitHub but is not in the Branches table"])

    def test_merged_but_not_ancestor_is_flagged(self):
        report = self.verify(ancestors=known_ancestors((CUT, MAIN), (CUT, PLAN), (CUT, FIX), (CUT, RUNTIME)))
        self.assertEqual(len(report.flagged), 1)
        self.assertIn("marked merged, but head 22222222 is not in release/14/main", report.flagged[0])

    def test_cut_at_not_ancestor_is_flagged(self):
        report = self.verify(ancestors=known_ancestors((PLAN, MAIN), (CUT, MAIN), (CUT, PLAN), (CUT, RUNTIME)))
        self.assertEqual(len(report.flagged), 1)
        self.assertIn("astrid-agent release/14/tester-fixes: Cut at 33333333 is not an ancestor", report.flagged[0])

    def test_not_verified_never_fails(self):
        def unknowable(repo, ancestor, descendant):
            raise rb.NotVerified("no clone")
        report = self.verify(ancestors=unknowable)
        self.assertEqual(report.flagged, [])
        self.assertEqual(len(report.unverified), 5)  # astrid-agent: 4 claims; astrid-runtime: 1 cut
        self.assertTrue(any("not verified (no clone)" in line for line in report.unverified))

    def test_not_yet_cut_is_not_verified(self):
        rows = [row.replace(CUT, "not yet cut") for row in GOOD_ROWS]
        report = self.verify(text=page(rows), ancestors=known_ancestors(*GOOD_ANCESTORS))
        self.assertEqual(report.flagged, [])
        self.assertEqual(sum("Cut at is not yet cut" in line for line in report.unverified), 4)

    def test_missing_release_main_leaves_merged_row_not_verified(self):
        refs = healthy_refs()
        del refs["astrid-agent"]["refs/heads/release/14/main"]
        report = self.verify(refs=refs)
        self.assertTrue(any("release main is missing" in line for line in report.unverified))

    def test_malformed_table_raises(self):
        with self.assertRaisesRegex(ValueError, "Branches table is malformed"):
            self.verify(text=page(["| astrid-agent | release/14/main | release | " + CUT + " | open |"]))

    def test_api_ancestor_statuses(self):
        def api(status):
            return lambda method, path: {"status": status}
        self.assertTrue(rb.api_ancestor(api("ahead"), "astrid-agent", CUT, MAIN))
        self.assertTrue(rb.api_ancestor(api("identical"), "astrid-agent", CUT, CUT))
        self.assertFalse(rb.api_ancestor(api("diverged"), "astrid-agent", CUT, MAIN))
        self.assertFalse(rb.api_ancestor(api("behind"), "astrid-agent", CUT, MAIN))
        with self.assertRaises(rb.NotVerified):
            rb.api_ancestor(api("weird"), "astrid-agent", CUT, MAIN)

    def test_api_404_is_a_flag_and_other_errors_are_not_verified(self):
        def not_found(method, path):
            raise urllib.error.HTTPError(path, 404, "Not Found", None, None)
        with self.assertRaisesRegex(ValueError, "is not a commit"):
            rb.api_ancestor(not_found, "astrid-agent", CUT, MAIN)
        def forbidden(method, path):
            raise urllib.error.HTTPError(path, 403, "Forbidden", None, None)
        with self.assertRaises(rb.NotVerified):
            rb.api_ancestor(forbidden, "astrid-agent", CUT, MAIN)

    def test_no_clone_and_no_token_is_not_verified(self):
        with self.assertRaises(rb.NotVerified):
            rb.ancestor_check({}, None)("astrid-agent", CUT, MAIN)

    def test_clone_ancestor_uses_git_objects(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            git = ["git", "-C", str(path), "-c", "user.name=t", "-c", "user.email=t@example.com"]
            subprocess.run(["git", "init", "-q", str(path)], check=True)
            subprocess.run(git + ["commit", "-q", "--allow-empty", "-m", "one"], check=True)
            first = subprocess.run(["git", "-C", str(path), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
            subprocess.run(git + ["commit", "-q", "--allow-empty", "-m", "two"], check=True)
            second = subprocess.run(["git", "-C", str(path), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
            self.assertTrue(rb.clone_ancestor(path, first, second))
            self.assertFalse(rb.clone_ancestor(path, second, first))
            with self.assertRaises(rb.NotVerified):
                rb.clone_ancestor(path, "9" * 40, second)

    def test_parse_clones_rejects_unknown_repository(self):
        with self.assertRaises(ValueError):
            rb.parse_clones(["NotAProduct=/tmp/x"])
        self.assertEqual(rb.parse_clones(["VibeComfy=/tmp/v"]), {"VibeComfy": Path("/tmp/v")})

    def test_list_table_shows_heads_and_missing(self):
        refs = healthy_refs()
        del refs["astrid-agent"]["refs/heads/release/14/tester-fixes"]
        rows = rb.release_rows(page(), 14)
        rb.read_heads(rows, fake_remote(refs))
        text = rb.table(rows)
        self.assertIn(MAIN[:8], text)
        self.assertIn("missing", text)
        self.assertIn("not yet cut", rb.table([{**rows[0], "cut": "not yet cut"}]))


if __name__ == "__main__":
    unittest.main()
