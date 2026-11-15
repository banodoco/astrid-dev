"""Offline policy and API-file adapter tests for planning auto-merge."""

import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from auto_merge import eligibility_reason, main


class EligibilityTests(unittest.TestCase):
    def reason(self, **changes):
        inputs = dict(draft=False, author_association="MEMBER", labels=[], body=None,
                      changed_paths=["plans/01-example/plan.md"])
        inputs.update(changes)
        return eligibility_reason(**inputs)

    def test_allowed_associations_and_paths(self):
        for association in ("OWNER", "MEMBER", "COLLABORATOR"):
            with self.subTest(association=association):
                self.assertIsNone(self.reason(author_association=association, changed_paths=[
                    "plans/a.md", "releases/13.md", "vision/gaps/a.md", "docs/guide.md",
                    "strategy.md", "README.md", "docs/nested/README.md"]))

    def test_draft(self):
        self.assertEqual(self.reason(draft=True), "draft pull request")

    def test_untrusted_associations(self):
        for association in ("CONTRIBUTOR", "FIRST_TIMER", "FIRST_TIME_CONTRIBUTOR",
                            "NONE", "MANNEQUIN", "member", "", None):
            with self.subTest(association=association):
                self.assertIsNotNone(self.reason(author_association=association))

    def test_hold_label_is_exact(self):
        self.assertEqual(self.reason(labels=["needs-review", "hold"]), "hold label")
        self.assertIsNone(self.reason(labels=["Hold", "hold-off", "needs-review"]))

    def test_body_phrase_is_exact_and_anywhere(self):
        for body in ("Owner decision needed", "Before\nOwner decision needed: scope\nAfter"):
            self.assertEqual(self.reason(body=body), "Owner decision needed in body")
        for body in (None, "", "owner decision needed", "Owner Decision Needed"):
            self.assertIsNone(self.reason(body=body))

    def test_empty_file_list(self):
        self.assertEqual(self.reason(changed_paths=[]), "empty file list")

    def test_disallowed_paths_and_case_differences(self):
        for path in ("scripts/x.py", ".github/workflows/docs.yml", "skills/x.md",
                     "templates/x.md", "env/x", "src/x", "other.md", "plans-other/x",
                     "plans", "Plans/x", "DOCS/x", "readme.md", "Strategy.md",
                     "README.md/extra", "strategy.md.bak"):
            with self.subTest(path=path):
                self.assertIsNotNone(self.reason(changed_paths=["docs/ok.md", path]))

    def test_noncanonical_paths(self):
        for path in ("plans/../scripts/x", "plans/../docs/x", "../plans/x", "./docs/x",
                     "/docs/x", "docs//x", "docs/./x", "docs/", "", "docs\\x",
                     "docs/a/../../scripts/x", None):
            with self.subTest(path=path):
                self.assertEqual(self.reason(changed_paths=[path]), "non-canonical changed path")

    def test_rename_sources_must_also_be_planning(self):
        self.assertIsNotNone(self.reason(changed_paths=["plans/new.md", "scripts/old.py"]))
        self.assertIsNone(self.reason(changed_paths=["plans/new.md", "docs/old.md"]))


class JsonInputTests(unittest.TestCase):
    def decide(self, pages, **changes):
        pr = dict(draft=False, author_association="OWNER", labels=[], body=None,
                  changed_files=sum(len(page) for page in pages))
        pr.update(changes)
        with tempfile.TemporaryDirectory() as directory:
            pr_path = Path(directory) / "pr.json"
            files_path = Path(directory) / "files.json"
            pr_path.write_text(json.dumps(pr), encoding="utf-8")
            files_path.write_text(json.dumps(pages), encoding="utf-8")
            output = io.StringIO()
            with patch("sys.argv", ["auto_merge.py", "--pr", str(pr_path), "--files", str(files_path)]):
                with contextlib.redirect_stdout(output):
                    main()
            return output.getvalue().strip()

    def test_all_pages_are_inspected(self):
        first = [{"filename": f"docs/{i}.md"} for i in range(100)]
        self.assertEqual(self.decide([first, [{"filename": "plans/x.md"}]]), "eligible")
        self.assertEqual(self.decide([first, [{"filename": "scripts/x.py"}]]),
                         "changed path outside planning content")

    def test_rename_source_from_later_page_is_inspected(self):
        pages = [[{"filename": "docs/ok.md"}], [{"filename": "plans/new.md",
                  "status": "renamed", "previous_filename": "scripts/old.py"}]]
        self.assertEqual(self.decide(pages), "changed path outside planning content")
        pages[1][0]["previous_filename"] = "docs/old.md"
        self.assertEqual(self.decide(pages), "eligible")
        del pages[1][0]["previous_filename"]
        self.assertEqual(self.decide(pages), "missing rename source")

    def test_incomplete_or_duplicate_file_lists(self):
        self.assertEqual(self.decide([[{"filename": "docs/x.md"}]], changed_files=3001),
                         "incomplete file list")
        self.assertEqual(self.decide([[{"filename": "docs/x.md"}] for _ in range(2)]),
                         "incomplete file list")

    def test_empty_pages(self):
        for pages in ([], [[]]):
            self.assertEqual(self.decide(pages), "empty file list")

    def test_metadata_is_passed_to_policy(self):
        pages = [[{"filename": "README.md"}]]
        self.assertEqual(self.decide(pages, draft=True), "draft pull request")
        self.assertEqual(self.decide(pages, labels=[{"name": "hold"}]), "hold label")
        self.assertEqual(self.decide(pages, body="Owner decision needed"), "Owner decision needed in body")
        self.assertNotEqual(self.decide(pages, author_association="NONE"), "eligible")


if __name__ == "__main__":
    unittest.main()
