"""Review routing reads project records on main and grants no merge authority."""
from contextlib import contextmanager
from pathlib import Path
import io
import os
import unittest
import urllib.error
from unittest.mock import call, patch

from review_intake import classify, parse_intent, route_event

REPO = "banodoco/astrid-dev"
FOLDER = "25-cloud"
PATH = f"plans/{FOLDER}/plan.md"
MAIN = "c" * 40
PLAN = (
    "# A title different from the project name\n\n"
    "**Project:** Cloud\n\n"
    "**Goal:** Deliver a useful result\n\n"
    "**Status:** queued\n\n"
    "**Owner:** @casey\n\n"
    "**Estimate:** TBD\n\n"
    "**Waiting on:** —\n\n"
    "## Scope\n\nA useful project.\n"
)
BASE = {"number": 37, "state": "open", "draft": False,
        "base": {"ref": "main", "repo": {"full_name": REPO}},
        "user": {"login": "casey", "type": "User"},
        "body": f"Project: {PATH}\nReview request: implementation\n"}


def submission(route, folder=FOLDER):
    return {**BASE, "body": f"Project: plans/{folder}/plan.md\nReview request: {route}\n"}


def modified_plan(status="modified"):
    return [{"filename": PATH, "status": status}]


def proposal_files():
    return [{"filename": f"plans/27-new/{name}", "status": "added"}
            for name in ("plan.md", "inputs.md", "tasks.md")]


class ReviewIntakeTests(unittest.TestCase):
    def test_existing_project_owner_can_request_review(self):
        self.assertEqual(classify(BASE, REPO, PLAN, []), "implementation")

    def test_owner_comparison_ignores_case(self):
        pr = {**BASE, "user": {"login": "Casey", "type": "User"}}
        for route in ("implementation", "completion"):
            body = submission(route)["body"]
            if route == "completion":
                body += "## Completion assessment — Plan 25\n"
            with self.subTest(route=route):
                self.assertEqual(classify({**pr, "body": body}, REPO, PLAN,
                                          modified_plan()), route)

    def test_non_owner_or_unknown_project_cannot_request_owner_review(self):
        for route in ("implementation", "completion"):
            pr = submission(route)
            pr["body"] += "## Completion assessment — Plan 25\n"
            for plan in (None, PLAN.replace("@casey", "@other"),
                         PLAN.replace("@casey", "Unassigned")):
                with self.subTest(route=route, plan=plan):
                    self.assertIsNone(classify(pr, REPO, plan, modified_plan()))

    def test_completion_requires_modified_plan_and_matching_assessment(self):
        pr = submission("completion")
        pr["body"] += "## Completion assessment — Plan 25\n"
        self.assertEqual(classify(pr, REPO, PLAN, modified_plan()), "completion")

    def test_completion_refuses_missing_added_removed_or_renamed_plan(self):
        pr = submission("completion")
        pr["body"] += "## Completion assessment — Plan 25\n"
        for files in ([], modified_plan("added"), modified_plan("removed"),
                      modified_plan("renamed"),
                      [{"filename": "plans/26-hosted/plan.md", "status": "modified"}],
                      [{"filename": "plans/index.md", "status": "modified"}]):
            with self.subTest(files=files):
                self.assertIsNone(classify(pr, REPO, PLAN, files))

    def test_completion_refuses_missing_wrong_or_duplicate_assessment(self):
        pr = submission("completion")
        for heading in ("", "## Completion assessment — Plan 26\n",
                        "## Completion assessment — Plan 25\n" * 2):
            with self.subTest(heading=heading):
                self.assertIsNone(classify({**pr, "body": pr["body"] + heading},
                                           REPO, PLAN, modified_plan()))

    def test_new_scope_routes_any_contributor_with_three_added_files(self):
        pr = {**submission("scope", "27-new"),
              "user": {"login": "new", "type": "User"}}
        self.assertEqual(classify(pr, REPO, None, proposal_files()), "scope")

    def test_new_scope_requires_each_pack_file_to_be_added(self):
        pr = submission("scope", "27-new")
        for index in range(3):
            incomplete = proposal_files()
            del incomplete[index]
            with self.subTest(missing=index):
                self.assertIsNone(classify(pr, REPO, None, incomplete))
            for status in ("modified", "removed", "renamed"):
                files = proposal_files()
                files[index]["status"] = status
                with self.subTest(index=index, status=status):
                    self.assertIsNone(classify(pr, REPO, None, files))

    def test_known_scope_requires_own_plan_among_changed_files(self):
        pr = {**submission("scope"), "user": {"login": "new", "type": "User"}}
        self.assertEqual(classify(pr, REPO, PLAN, modified_plan()), "scope")
        for files in ([], [{"filename": "plans/index.md", "status": "modified"}],
                      [{"filename": "plans/26-hosted/plan.md", "status": "modified"}]):
            with self.subTest(files=files):
                self.assertIsNone(classify(pr, REPO, PLAN, files))

    def test_index_edit_earns_no_review_route(self):
        index = [{"filename": "plans/index.md", "status": "modified"}]
        for route, plan, folder in (("scope", PLAN, FOLDER), ("scope", None, "27-new"),
                                    ("implementation", None, FOLDER),
                                    ("completion", PLAN, FOLDER)):
            pr = submission(route, folder)
            pr["body"] += "## Completion assessment — Plan 25\n"
            with self.subTest(route=route, known=plan is not None):
                self.assertIsNone(classify(pr, REPO, plan, index))

    def test_malformed_main_plan_raises_for_every_route(self):
        for route in ("scope", "implementation", "completion"):
            pr = submission(route)
            pr["body"] += "## Completion assessment — Plan 25\n"
            for malformed in ("# No fields\n",
                              PLAN.replace("**Owner:** @casey", "**Owner:**"),
                              PLAN.replace("## Scope", "**Owner:** @other\n## Scope"),
                              PLAN.replace("**Goal:** Deliver a useful result", "**Goal:** left | right")):
                with self.subTest(route=route, malformed=malformed), self.assertRaises(ValueError):
                    classify(pr, REPO, malformed, modified_plan())

    def test_body_owner_decoy_does_not_grant_ownership(self):
        plan = PLAN.replace("@casey", "@other") + "**Owner:** @casey\n"
        self.assertIsNone(classify(BASE, REPO, plan, []))
        self.assertEqual(classify(BASE, REPO, PLAN + "**Owner:** @other\n", []),
                         "implementation")

    def test_untrusted_prs_do_not_enter_review_queue(self):
        for update in ({"draft": True}, {"state": "closed"},
                       {"user": {"login": "casey", "type": "Bot"}},
                       {"base": {"ref": "other", "repo": {"full_name": REPO}}},
                       {"base": {"ref": "main", "repo": {"full_name": "other/repo"}}}):
            with self.subTest(update=update):
                self.assertIsNone(classify({**BASE, **update}, REPO, PLAN, []))

    def test_missing_duplicate_or_unrelated_intent(self):
        self.assertIsNone(parse_intent("Ordinary bug fix"))
        self.assertIsNone(classify({**BASE, "body": "Ordinary bug fix"}, REPO, PLAN, []))
        for body in (BASE["body"] + "Review request: completion\n",
                     BASE["body"] + f"Project: {PATH}\n",
                     "Review request: implementation\n", f"Project: {PATH}\n"):
            with self.subTest(body=body), self.assertRaises(ValueError):
                parse_intent(body)


class ReviewIntakeTokenTests(unittest.TestCase):
    def test_workflow_can_label_a_pull_request(self):
        # Adding a label to a pull request is refused with 403 "Resource not
        # accessible by integration" unless the token has pull-requests: write.
        text = (Path(__file__).resolve().parents[1] / ".github/workflows/review-intake.yml").read_text(encoding="utf-8")
        self.assertIn("  pull-requests: write\n", text)
        self.assertIn("  issues: write\n", text)

    def test_a_refused_call_names_the_method_and_path(self):
        import contribution_api
        error = urllib.error.HTTPError("https://api.github.com/x", 403, "Forbidden", {}, io.BytesIO(b"{}"))
        with patch.dict(os.environ, {"GH_TOKEN": "t"}), \
                patch("urllib.request.urlopen", side_effect=error), \
                self.assertRaises(urllib.error.HTTPError) as caught:
            contribution_api.request("POST", "/repos/o/r/issues/7/labels", {"labels": ["x"]})
        self.assertEqual(caught.exception.code, 403)
        self.assertIn("POST /repos/o/r/issues/7/labels", str(caught.exception))


class ReviewEventTests(unittest.TestCase):
    @contextmanager
    def remote(self, pr=None, plan=PLAN, files=None):
        pr = {**BASE, "labels": [], **(pr or {})}

        def response(method, path, payload=None):
            if method == "GET" and path.endswith("/pulls/37"):
                return pr
            if method == "GET" and path.endswith("/git/ref/heads/main"):
                return {"object": {"sha": MAIN}}
            if method in ("POST", "DELETE"):
                return {}
            raise AssertionError(f"unexpected API call: {method} {path}")

        with patch("review_intake.request", side_effect=response) as request, \
                patch("review_intake.plan_text", create=True, return_value=plan) as reader, \
                patch("review_intake.catalog", create=True, return_value=plan), \
                patch("review_intake.changed_files", return_value=files or []), \
                patch("review_intake.ensure_review_label") as ensure:
            yield request, reader, ensure

    def route(self):
        return route_event({"pull_request": {"number": 37}}, REPO)

    def assert_only_queue_writes(self, request):
        for action in request.call_args_list:
            if action.args[0] != "GET":
                self.assertEqual(action.args[0], "POST")
                self.assertIn(action.args[1], (f"/repos/{REPO}/issues/37/labels",
                                              f"/repos/{REPO}/issues/37/comments"))

    def test_live_plan_read_queues_owner_without_approval_or_merge(self):
        with self.remote() as (request, reader, ensure):
            self.assertIn("Queued", self.route())
            reader.assert_called_once_with(REPO, MAIN, FOLDER)
            ensure.assert_called_once_with(REPO, "needs-review")
            self.assertIn(call("POST", f"/repos/{REPO}/issues/37/labels",
                               {"labels": ["needs-review"]}), request.call_args_list)
            self.assert_only_queue_writes(request)

    def test_new_scope_without_index_is_labeled_without_approval(self):
        pr = submission("scope", "27-new")
        with self.remote(pr, None, proposal_files()) as (request, reader, ensure):
            self.assertIn("Queued", self.route())
            reader.assert_called_once_with(REPO, MAIN, "27-new")
            ensure.assert_called_once_with(REPO, "needs-review")
            self.assert_only_queue_writes(request)

    def test_completion_queues_owner_with_modified_plan(self):
        pr = submission("completion")
        pr["body"] += "## Completion assessment — Plan 25\n"
        with self.remote(pr, PLAN, modified_plan()) as (request, reader, ensure):
            self.assertIn("Queued", self.route())
            reader.assert_called_once_with(REPO, MAIN, FOLDER)
            self.assert_only_queue_writes(request)

    def test_stale_label_is_removed_when_owner_no_longer_matches(self):
        pr = {"user": {"login": "other", "type": "User"},
              "labels": [{"name": "needs-review"}]}
        with self.remote(pr) as (request, reader, ensure):
            self.assertIn("Removed stale", self.route())
            reader.assert_called_once_with(REPO, MAIN, FOLDER)
            request.assert_any_call("DELETE", f"/repos/{REPO}/issues/37/labels/needs-review")
            ensure.assert_not_called()
            self.assertFalse(any(c.args[0] in ("POST", "PUT") for c in request.call_args_list))

    def test_edited_body_loses_stale_label(self):
        with self.remote({"body": "Ordinary bug fix", "labels": [{"name": "needs-review"}]}) as (
                request, reader, ensure):
            self.assertIn("Removed stale", self.route())
            request.assert_any_call("DELETE", f"/repos/{REPO}/issues/37/labels/needs-review")
            ensure.assert_not_called()

    def test_malformed_main_plan_fails_closed_before_label_changes(self):
        with self.remote(plan="# No fields\n") as (request, reader, ensure):
            with self.assertRaises(ValueError):
                self.route()
            ensure.assert_not_called()
            self.assertFalse(any(c.args[0] != "GET" for c in request.call_args_list))

    def test_missing_main_plan_does_not_queue_owner_request(self):
        with self.remote(plan=None) as (request, reader, ensure):
            self.assertIn("Not an eligible", self.route())
            reader.assert_called_once_with(REPO, MAIN, FOLDER)
            ensure.assert_not_called()
            self.assertFalse(any(c.args[0] != "GET" for c in request.call_args_list))


if __name__ == "__main__":
    unittest.main()
