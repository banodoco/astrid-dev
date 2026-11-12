"""Plan-file contract for trusted claim validation; all remote reads are mocked."""
import base64
from contextlib import contextmanager, ExitStack
import unittest
from unittest.mock import call, patch
from urllib.error import HTTPError

import contribution_api
from claim_project import eligible, handle_run, main_has_protection, verify_claim, verify_live_claim

REPO = "banodoco/astrid-dev"
FOLDER = "25-cloud"
PATH = f"plans/{FOLDER}/plan.md"
HEAD = "a" * 40
BASE_REF = "b" * 40
LIVE = "c" * 40
BASE = (
    "# A title different from the project name\n\n"
    "**Project:** Cloud\n\n"
    "**Goal:** Deliver a useful result\n\n"
    "**Status:** queued\n\n"
    "**Owner:** Unassigned\n\n"
    "**Estimate:** TBD\n\n"
    "**Waiting on:** —\n\n"
    "## Scope\n\nKeep this body unchanged.\n"
)
CLAIMED = BASE.replace("**Owner:** Unassigned", "**Owner:** @casey")


def pull():
    return {"number": 37, "state": "open", "draft": False,
            "base": {"ref": "main", "sha": BASE_REF, "repo": {"full_name": REPO}},
            "head": {"sha": HEAD, "repo": {"full_name": "casey/astrid-dev"}},
            "user": {"login": "casey", "type": "User"}}


def changed(**updates):
    return {"filename": PATH, "status": "modified", "additions": 1,
            "deletions": 1, **updates}


class PlanTextTests(unittest.TestCase):
    def test_reads_plain_utf8_file_at_requested_ref(self):
        response = {"type": "file", "encoding": "base64",
                    "content": base64.b64encode(BASE.encode("utf-8")).decode("ascii")}
        with patch("contribution_api.request", return_value=response) as request:
            self.assertEqual(contribution_api.plan_text(REPO, "topic/claim", FOLDER), BASE)
        request.assert_called_once_with(
            "GET", f"/repos/{REPO}/contents/{PATH}?ref=topic%2Fclaim")

    def test_missing_plan_is_none_only_on_404(self):
        error = HTTPError("https://example.invalid", 404, "not found", {}, None)
        with patch("contribution_api.request", side_effect=error):
            self.assertIsNone(contribution_api.plan_text(REPO, HEAD, FOLDER))

    def test_other_transport_failures_propagate(self):
        for error in (HTTPError("https://example.invalid", code, "failure", {}, None)
                      for code in (401, 403, 429, 500)):
            with self.subTest(code=error.code):
                with patch("contribution_api.request", side_effect=error), \
                        self.assertRaises(HTTPError) as caught:
                    contribution_api.plan_text(REPO, HEAD, FOLDER)
                self.assertIs(caught.exception, error)
        with patch("contribution_api.request", side_effect=OSError("offline")), \
                self.assertRaises(OSError):
            contribution_api.plan_text(REPO, HEAD, FOLDER)

    def test_non_plain_files_are_refused(self):
        encoded = base64.b64encode(BASE.encode()).decode()
        for response in (
            [{"type": "file", "name": "child"}],
            {"type": "dir"},
            {"type": "symlink", "target": "elsewhere", "encoding": "base64", "content": encoded},
            {"type": "file", "target": "elsewhere", "encoding": "base64", "content": encoded},
            {"type": "submodule", "submodule_git_url": "https://example.invalid/repo"},
        ):
            with self.subTest(response=response), \
                    patch("contribution_api.request", return_value=response), \
                    self.assertRaises(ValueError):
                contribution_api.plan_text(REPO, HEAD, FOLDER)

    def test_catalog_reader_and_constant_are_removed(self):
        self.assertFalse(hasattr(contribution_api, "catalog"))
        self.assertFalse(hasattr(contribution_api, "CATALOG"))


class ClaimTests(unittest.TestCase):
    def test_claim_changes_only_header_owner_preserving_line_endings(self):
        # Passing is the contract here; a plan's title does not encode its folder.
        for ending in ("\n", "\r\n"):
            with self.subTest(ending=repr(ending)):
                verify_claim(BASE.replace("\n", ending), CLAIMED.replace("\n", ending), "casey")

    def test_cannot_change_anything_else(self):
        for reason, proposed in {
            "another handle": CLAIMED.replace("@casey", "@other"),
            "login letter case": CLAIMED.replace("@casey", "@Casey"),
            "goal": CLAIMED.replace("useful result", "different result"),
            "status": CLAIMED.replace("queued", "active"),
            "body": CLAIMED.replace("body unchanged", "body rewritten"),
            "title": CLAIMED.replace("# A title", "# Another title"),
            "added line": CLAIMED + "Extra line\n",
            "removed line": CLAIMED.replace("Keep this body unchanged.\n", ""),
            "owner trailing space": CLAIMED.replace("@casey\n", "@casey \n"),
            "owner line ending": CLAIMED.replace("@casey\n", "@casey\r\n"),
            "all line endings": CLAIMED.replace("\n", "\r\n"),
            "no edit": BASE,
        }.items():
            with self.subTest(reason=reason), self.assertRaises(ValueError):
                verify_claim(BASE, proposed, "casey")

    def test_cannot_steal_owner(self):
        owned = BASE.replace("Unassigned", "@alex")
        with self.assertRaises(ValueError):
            verify_claim(owned, owned.replace("@alex", "@casey"), "casey")

    def test_blocked_or_active_projects_cannot_be_claimed(self):
        for status in ("blocked", "active", "done", "cancelled", "proposed"):
            before = BASE.replace("queued", status)
            after = CLAIMED.replace("queued", status)
            with self.subTest(status=status), self.assertRaises(ValueError):
                verify_claim(before, after, "casey")

    def test_owner_line_must_be_exact_before_and_after(self):
        for owner in ("unassigned", " Unassigned", "Unassigned ", "TBD"):
            before = BASE.replace("**Owner:** Unassigned", "**Owner:** " + owner)
            with self.subTest(owner=owner), self.assertRaises(ValueError):
                verify_claim(before, CLAIMED, "casey")

    def test_duplicate_header_owner_at_base_or_head_is_refused(self):
        # Cover an invalid base, an invalid head, and duplicate fields shared by
        # both versions whose only differing line is the apparent owner claim.
        duplicate_base = BASE.replace("## Scope", "**Owner:** Unassigned\n## Scope")
        duplicate_head = CLAIMED.replace("## Scope", "**Owner:** @casey\n## Scope")
        for before, after in ((duplicate_base, CLAIMED), (BASE, duplicate_head)):
            with self.subTest(before=before, after=after), self.assertRaises(ValueError):
                verify_claim(before, after, "casey")
        for owner in ("Unassigned", "@casey"):
            duplicate = "**Owner:** " + owner + "\n"
            before = BASE.replace("## Scope", duplicate + "## Scope")
            after = CLAIMED.replace("## Scope", duplicate + "## Scope")
            with self.subTest(duplicate=owner), self.assertRaises(ValueError):
                verify_claim(before, after, "casey")

    def test_both_texts_must_have_valid_project_fields(self):
        for field, value in (("Project", "Cloud"), ("Goal", "Deliver a useful result"),
                             ("Status", "queued"), ("Estimate", "TBD"), ("Waiting on", "—")):
            line = f"**{field}:** {value}"
            for invalid in ("", f"**{field}:**", f"**{field}:** left | right"):
                before, after = BASE.replace(line, invalid), CLAIMED.replace(line, invalid)
                with self.subTest(field=field, invalid=invalid), self.assertRaises(ValueError):
                    verify_claim(before, after, "casey")

    def test_changed_body_owner_decoy_is_refused(self):
        before = BASE + "**Owner:** Unassigned\n"
        after = BASE + "**Owner:** @casey\n"
        with self.assertRaises(ValueError):
            verify_claim(before, after, "casey")

    def test_unchanged_body_owner_decoy_does_not_block_real_claim(self):
        decoy = "**Owner:** Unassigned\n"
        verify_claim(BASE + decoy, CLAIMED + decoy, "casey")

    def test_live_claim_accepts_identical_project_file(self):
        verify_live_claim(BASE, CLAIMED, BASE, "casey")

    def test_live_claim_refuses_any_changed_byte(self):
        for reason, live in {
            "owner": BASE.replace("Unassigned", "@another"),
            "goal": BASE.replace("useful result", "different result"),
            "status": BASE.replace("queued", "blocked"),
            "body": BASE.replace("body unchanged", "body rewritten"),
            "whitespace": BASE + " ",
            "line endings": BASE.replace("\n", "\r\n"),
            "removed content": "",
        }.items():
            with self.subTest(reason=reason), self.assertRaises(ValueError):
                verify_live_claim(BASE, CLAIMED, live, "casey")

    def test_privileged_claims_refuse_unprotected_main(self):
        for protected in (False, True):
            with self.subTest(protected=protected), \
                    patch("claim_project.api", return_value={"protected": protected}):
                self.assertEqual(main_has_protection(REPO), protected)


class EligibilityTests(unittest.TestCase):
    def test_exactly_one_modified_plan_with_one_addition_and_deletion(self):
        self.assertTrue(eligible(pull(), REPO, HEAD, [changed()]))
        for folder in ("99-fixture", "125-long-name"):
            with self.subTest(folder=folder):
                self.assertTrue(eligible(pull(), REPO, HEAD,
                                         [changed(filename=f"plans/{folder}/plan.md")]))

    def test_two_plans_or_any_extra_file_are_refused(self):
        for path in ("plans/26-hosted/plan.md", "README.md", "scripts/evil.py",
                     ".github/workflows/docs.yml", "plans/index.md", "vision/README.md"):
            with self.subTest(path=path):
                self.assertFalse(eligible(pull(), REPO, HEAD,
                                          [changed(), changed(filename=path)]))
        self.assertFalse(eligible(pull(), REPO, HEAD, []))

    def test_generated_files_and_resembling_paths_are_refused(self):
        for path in ("plans/index.md", "vision/README.md", "docs/checks.md",
                     "plans/x/notes/plan.md", "templates/project/plan.md",
                     "plans/x/plan.md", "plans/25-cloud/notes/plan.md",
                     "plans/25-cloud/plan.md.bak", "prefix/plans/25-cloud/plan.md",
                     "plans/25-Cloud/plan.md", "plans/25-cloud/plan.md\n"):
            with self.subTest(path=path):
                self.assertFalse(eligible(pull(), REPO, HEAD, [changed(filename=path)]))

    def test_added_removed_or_renamed_file_is_refused(self):
        for status in ("added", "removed", "renamed"):
            with self.subTest(status=status):
                self.assertFalse(eligible(pull(), REPO, HEAD, [changed(status=status)]))

    def test_other_diff_counts_are_refused(self):
        for additions, deletions in ((0, 1), (1, 0), (2, 1), (1, 2), (2, 2)):
            with self.subTest(additions=additions, deletions=deletions):
                self.assertFalse(eligible(pull(), REPO, HEAD,
                                          [changed(additions=additions, deletions=deletions)]))
        for key in ("additions", "deletions"):
            entry = changed()
            del entry[key]
            with self.subTest(missing=key):
                self.assertFalse(eligible(pull(), REPO, HEAD, [entry]))

    def test_eligibility_filters_untrusted_prs(self):
        for update in ({"draft": True}, {"state": "closed"},
                       {"user": {"login": "casey", "type": "Bot"}},
                       {"user": {"login": "bad/login", "type": "User"}},
                       {"head": {"sha": "d" * 40, "repo": {"full_name": "casey/astrid-dev"}}},
                       {"base": {"ref": "other", "repo": {"full_name": REPO}}},
                       {"base": {"ref": "main", "repo": {"full_name": "other/repo"}}}):
            with self.subTest(update=update):
                self.assertFalse(eligible({**pull(), **update}, REPO, HEAD, [changed()]))


class ClaimRunTests(unittest.TestCase):
    @contextmanager
    def remote(self, texts=None, fresh=None, main_refs=None):
        pr = pull()
        texts = {(REPO, BASE_REF, FOLDER): BASE,
                 ("casey/astrid-dev", HEAD, FOLDER): CLAIMED,
                 (REPO, LIVE, FOLDER): BASE, **(texts or {})}
        refs = iter(main_refs or [LIVE, LIVE])

        def response(method, path, payload=None):
            if method == "GET" and path.endswith("/git/ref/heads/main"):
                return {"object": {"sha": next(refs)}}
            if method == "GET" and path.endswith("/pulls/37"):
                return next(pr_reads)
            if method in ("PUT", "POST"):
                return {}
            raise AssertionError(f"unexpected API call: {method} {path}")

        pr_reads = iter([pr, fresh or pr])
        with ExitStack() as stack:
            api = stack.enter_context(patch("claim_project.api", side_effect=response))
            reader = stack.enter_context(patch("claim_project.plan_text", create=True,
                                               side_effect=lambda repo, ref, folder: texts[repo, ref, folder]))
            # Keep the old transport offline while the tests expose its use.
            stack.enter_context(patch("claim_project.catalog", create=True, return_value="old catalog"))
            stack.enter_context(patch("claim_project.main_has_protection", return_value=True))
            stack.enter_context(patch("claim_project.open_pulls", return_value=[pr]))
            stack.enter_context(patch("claim_project.files_in_pr", return_value=[changed()]))
            yield api, reader

    def run_claim(self, **updates):
        return handle_run(REPO, {"event": "pull_request", "conclusion": "success",
                                 "head_sha": HEAD, **updates})

    def assert_no_merge(self, api):
        self.assertFalse(any(c.args[0] == "PUT" for c in api.call_args_list))

    def test_reads_base_head_and_live_plan_and_merges_exact_head(self):
        with self.remote() as (api, reader):
            self.assertEqual(self.run_claim(), [FOLDER])
            self.assertEqual(sorted(reader.call_args_list), sorted([
                call(REPO, BASE_REF, FOLDER), call("casey/astrid-dev", HEAD, FOLDER),
                call(REPO, LIVE, FOLDER)]))
            merge = next(c for c in api.call_args_list if c.args[0] == "PUT")
            self.assertEqual(merge.args[1], f"/repos/{REPO}/pulls/37/merge")
            self.assertEqual(merge.args[2]["sha"], HEAD)
            self.assertEqual(merge.args[2]["merge_method"], "squash")
            comment = next(c.args[2]["body"] for c in api.call_args_list if c.args[0] == "POST")
            self.assertIn(f"/blob/main/{PATH}", comment)
            self.assertIn("@casey", comment)

    def test_missing_base_head_or_live_plan_skips_without_failing(self):
        for location in ((REPO, BASE_REF, FOLDER), ("casey/astrid-dev", HEAD, FOLDER),
                         (REPO, LIVE, FOLDER)):
            with self.subTest(location=location), self.remote({location: None}) as (api, reader):
                self.assertEqual(self.run_claim(), [])
                self.assertIn(call(*location), reader.call_args_list)
                self.assert_no_merge(api)

    def test_different_project_change_on_main_does_not_block(self):
        # The new main ref includes a change to another project. Only this file
        # is returned; trying to fetch any other folder fails the fixture lookup.
        unrelated_main = "e" * 40
        with self.remote({(REPO, unrelated_main, FOLDER): BASE},
                         main_refs=[unrelated_main, unrelated_main]) as (api, reader):
            self.assertEqual(self.run_claim(), [FOLDER])
            reader.assert_any_call(REPO, unrelated_main, FOLDER)
            self.assertTrue(any(c.args[0] == "PUT" for c in api.call_args_list))

    def test_failed_missing_or_wrong_ci_never_merges(self):
        for update in ({"conclusion": "failure"}, {"conclusion": None},
                       {"conclusion": "cancelled"}, {"event": "push"},
                       {"head_sha": ""}):
            with self.subTest(update=update), self.remote() as (api, reader):
                self.assertEqual(self.run_claim(**update), [])
                reader.assert_not_called()
                self.assert_no_merge(api)
        with self.remote() as (api, reader):
            self.assertEqual(handle_run(REPO, {}), [])
            self.assert_no_merge(api)

    def test_unprotected_main_prevents_merge(self):
        with self.remote() as (api, reader), \
                patch("claim_project.main_has_protection", return_value=False):
            with self.assertRaises(ValueError):
                self.run_claim()
            reader.assert_not_called()
            self.assert_no_merge(api)

    def test_head_moving_during_validation_prevents_merge(self):
        fresh = pull()
        fresh["head"]["sha"] = "d" * 40
        # Isolate the orchestration race from the separately tested pure gates.
        with self.remote(fresh=fresh) as (api, reader), \
                patch("claim_project.eligible", return_value=True), \
                patch("claim_project.verify_live_claim", return_value=FOLDER):
            with self.assertRaises(ValueError):
                self.run_claim()
            self.assertEqual(reader.call_count, 3)
            self.assert_no_merge(api)

    def test_main_moving_during_validation_prevents_merge(self):
        with self.remote(main_refs=[LIVE, "d" * 40]) as (api, reader), \
                patch("claim_project.eligible", return_value=True), \
                patch("claim_project.verify_live_claim", return_value=FOLDER):
            with self.assertRaises(ValueError):
                self.run_claim()
            self.assertEqual(reader.call_count, 3)
            self.assert_no_merge(api)


if __name__ == "__main__":
    unittest.main()
