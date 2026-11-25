import re
import tempfile
import unittest
import contextlib
import io
import shutil
import subprocess
from pathlib import Path

from views import View, _with_marker, check, check_view, sync


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def copy_repo_fixture(source: Path, destination: Path) -> None:
    """Copy authored checkout fixtures, never derived skills or private run state.

    Generated packages may contain repo symlinks pointing back to the checkout;
    following them during an ordinary copytree can recurse indefinitely.
    Preserve the *authored* legacy symlinks so the original view/alias tests run.
    """
    shutil.copytree(
        source, destination,
        ignore=shutil.ignore_patterns(".git", ".otto", "__pycache__", ".generated"),
        symlinks=True,
    )


def commit_base(root):
    """Make a base only in a disposable test repository."""
    git(root, "init", "-q", "-b", "main")
    git(root, "config", "user.name", "Test")
    git(root, "config", "user.email", "test@example.invalid")
    git(root, "add", ".")
    git(root, "commit", "-qm", "base")
    return git(root, "rev-parse", "HEAD")


class ViewTests(unittest.TestCase):
    def test_fixture_copy_ignores_generated_repo_symlink_cycle(self):
        with tempfile.TemporaryDirectory(prefix="view-derived-cycle-") as tmp:
            root = Path(tmp)
            source = root / "original"
            (source / "skills").mkdir(parents=True)
            (source / ".generated/skills/astrid-dev-start").mkdir(parents=True)
            (source / "README.md").write_text("authored\n", encoding="utf-8")
            (source / "skills/legacy.md").symlink_to("../README.md")
            (source / ".generated/skills/astrid-dev-start/repo").symlink_to(
                source, target_is_directory=True
            )
            copied = root / "fixture"
            copy_repo_fixture(source, copied)
            self.assertEqual((copied / "README.md").read_text(encoding="utf-8"), "authored\n")
            self.assertTrue((copied / "skills/legacy.md").is_symlink())
            self.assertEqual((copied / "skills/legacy.md").read_text(encoding="utf-8"), "authored\n")
            self.assertFalse((copied / ".generated").exists())
            self.assertTrue((source / ".generated/skills/astrid-dev-start/repo").is_symlink())

    def test_hand_edited_vision_title_fails_check(self):
        import astrid_dev
        source = Path(__file__).resolve().parent.parent
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repo"
            copy_repo_fixture(source, root)
            base = commit_base(root)
            target = root / "vision/README.md"
            content = target.read_text(encoding="utf-8")
            target.write_text(content.replace("# Astrid — ", "# Astrid — Hand edited ", 1), encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                body = Path(temporary) / "body.txt"
                body.write_text("", encoding="utf-8")
                code = astrid_dev.main(["check", "--base", base, "--body-file", str(body)], root=root)
            self.assertEqual(code, 1)
            self.assertIn("ERROR generated-views: view public-vision", output.getvalue())
            self.assertNotIn("ERROR public-vision-content:", output.getvalue())

    def test_pr_only_check_without_base_skips_catalog_render(self):
        import astrid_dev
        import checks
        import subprocess
        from unittest.mock import patch

        registry = [entry for entry in checks.REGISTRY if entry.id == "generated-views"]
        output = io.StringIO()
        # Without a base, this PR-only check never renders the check catalog.
        with patch("views.subprocess.run", side_effect=subprocess.CalledProcessError(1, ["astrid_dev.py", "list"])) as run:
            with contextlib.redirect_stdout(output):
                code = astrid_dev.main(["check"], registry=registry)
        self.assertEqual(code, 0)
        self.assertEqual(output.getvalue(), "")
        run.assert_not_called()

    def test_legacy_source_error_hides_both_owned_view_errors(self):
        import checks
        import golden
        import json
        import views

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repo"
            golden._copy_tree(root)
            overlay = json.loads((golden.FIXTURES / "bad-status/overlay.json").read_text(encoding="utf-8"))
            for relative, contents in overlay.items():
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(contents, encoding="utf-8")
            context = checks.Context(root)
            source_errors = checks._public_vision(context)
            self.assertTrue(any("invalid status 'maybe'" in line for line in source_errors), source_errors)
            raw_errors = views.check(root)
            self.assertTrue(any(line.startswith("view public-vision:") for line in raw_errors))
            self.assertTrue(any(line.startswith("view root-vision-summary:") for line in raw_errors))
            # Source errors remain owned by public-vision-content. With no base,
            # generated-views does not report either owned target or render it.
            self.assertEqual(checks._generated_views(context), [])

    def test_base_source_error_hides_hand_edited_vision_view_error(self):
        import astrid_dev
        import checks
        source = Path(__file__).resolve().parent.parent
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repo"
            copy_repo_fixture(source, root)
            base_readme = root / "README.md"
            original_readme = base_readme.read_text(encoding="utf-8")
            base_readme.write_text(original_readme.replace("<!-- vision-summary:end -->", "", 1),
                                   encoding="utf-8")
            base = commit_base(root)
            base_readme.write_text(original_readme, encoding="utf-8")
            plan = root / "plans/48-one-record-model/plan.md"
            text = plan.read_text(encoding="utf-8")
            plan.write_text(re.sub(r"(?m)^\*\*Status:\*\* \w+", "**Status:** maybe", text, count=1), encoding="utf-8")
            target = root / "vision/README.md"
            text = target.read_text(encoding="utf-8")
            target.write_text(text.replace("# Astrid — ", "# Astrid — Hand edited ", 1), encoding="utf-8")

            import views
            root_summary = next(view for view in views.VIEWS if view.name == "root-vision-summary")
            self.assertTrue(views.touched(root_summary, root, base))

            registry = [entry for entry in checks.REGISTRY
                        if entry.id in {"public-vision-content", "generated-views"}]
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                body = Path(temporary) / "body.txt"
                body.write_text("", encoding="utf-8")
                code = astrid_dev.main(["check", "--base", base, "--body-file", str(body)],
                                       root=root, registry=registry)
            error_lines = [line for line in output.getvalue().splitlines() if line.startswith("ERROR ")]
            self.assertEqual(code, 1)
            self.assertEqual(len(error_lines), 1, error_lines)
            self.assertIn("ERROR public-vision-content:", error_lines[0])
            self.assertIn("invalid status 'maybe'", error_lines[0])

    def test_view_check_is_registered(self):
        import checks
        registered = [entry for entry in checks.REGISTRY if entry.id == "generated-views"]
        self.assertEqual(len(registered), 1)
        self.assertEqual(registered[0].trigger, "pr")
        self.assertTrue(registered[0].description)
        self.assertTrue(callable(registered[0].run))

    def test_legacy_vision_failure_is_the_only_error_line(self):
        import astrid_dev
        source = Path(__file__).resolve().parent.parent
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repo"
            copy_repo_fixture(source, root)
            base = commit_base(root)
            target = root / "README.md"
            content = target.read_text(encoding="utf-8")
            target.write_text(content.replace("<!-- vision-summary:end -->", "hand edit\n<!-- vision-summary:end -->"), encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                body = Path(temporary) / "body.txt"
                body.write_text("", encoding="utf-8")
                code = astrid_dev.main(["check", "--base", base, "--body-file", str(body)], root=root)
            error_lines = [line for line in output.getvalue().splitlines() if line.startswith("ERROR ")]
            self.assertEqual(code, 1)
            self.assertEqual(len(error_lines), 1)
            self.assertIn("generated-views: view root-vision-summary", error_lines[0])

    def test_file_view_adds_standard_marker(self):
        view = View("sample", ("source.md",), "target.md", lambda root: "# Generated\n")
        self.assertEqual(
            _with_marker(view, "# Generated\n"),
            "<!-- Generated by Astrid Dev view: sample; sources: source.md. Do not edit. -->\n# Generated\n",
        )

    def test_region_view_preserves_surrounding_text_and_checks_hand_edits(self):
        view = View("summary", ("source.md",), "README.md", lambda root: "before\n<!-- vision-summary:start -->\nvalue\n<!-- vision-summary:end -->\nafter\n", True)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "README.md").write_text("before\n<!-- vision-summary:start -->\nvalue\n<!-- vision-summary:end -->\nafter\n", encoding="utf-8")
            import views
            previous = views.VIEWS
            try:
                views.VIEWS = (view,)
                self.assertEqual(sync(root), ["README.md"])
            finally:
                views.VIEWS = previous
            self.assertEqual(check_view(view, root), [])
            text = (root / "README.md").read_text(encoding="utf-8")
            self.assertIn("view: summary", text)
            (root / "README.md").write_text(text.replace("value", "hand edit"), encoding="utf-8")
            errors = check_view(view, root)
            self.assertEqual(len(errors), 1)
            self.assertIn("view summary", errors[0])

    def test_sync_is_idempotent(self):
        view = View("sample", ("source.md",), "target.md", lambda root: "content\n")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            original = (view,)
            import views
            previous = views.VIEWS
            try:
                views.VIEWS = original
                self.assertEqual(sync(root), ["target.md"])
                self.assertEqual(sync(root), [])
                self.assertEqual(check(root), [])
            finally:
                views.VIEWS = previous

    def test_sync_reports_shared_target_once_when_both_regions_are_stale(self):
        source = Path(__file__).resolve().parent.parent
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repo"
            copy_repo_fixture(source, root)
            # main's generated pages may be stale between a merge and the refresh job's
            # commit; bring every view current first so only plans/index.md is left to change.
            sync(root)
            target = root / "plans/index.md"
            content = target.read_text(encoding="utf-8")
            content = content.replace("<!-- plan-catalog:start -->", "<!-- plan-catalog:start -->\nhand edited catalog", 1)
            content = content.replace("<!-- status-definitions:start -->", "<!-- status-definitions:start -->\nhand edited definitions", 1)
            target.write_text(content, encoding="utf-8")

            self.assertEqual(sync(root), ["plans/index.md"])
            self.assertEqual(sync(root), [])


class PlanCatalogViewTests(unittest.TestCase):
    def view(self):
        import views
        matches = [view for view in views.VIEWS if view.name == "plan-catalog"]
        self.assertEqual(len(matches), 1, "PM-6b must register the plan-catalog view")
        view = matches[0]
        self.assertEqual(view.sources, ("plans/*/plan.md", "plans/priority.md"))
        self.assertEqual(view.target, "plans/index.md")
        self.assertEqual(view.region, "plan-catalog")
        return view

    def sources(self, root):
        from test_records import ProjectRecordTests as Records
        Records.write(root, "01-alpha", Records.plan(Project="Catalog alpha", Status="active",
                      Goal="Read [release](../../releases/12.md)", **{"Waiting on": "[work](../02-beta/plan.md)"}))
        Records.write(root, "02-beta", Records.plan(Project="Catalog beta", Status="done"))
        (root / "plans/priority.md").write_text("## Order\n- 02-beta\n- 01-alpha\n", encoding="utf-8")
        # Everything outside the table is owned by the author, including the
        # title, priority explanation, six definitions, edit guidance and notes.
        (root / "plans/index.md").write_text(
            self.before() + "<!-- plan-catalog:start -->\nold table\n"
            "<!-- plan-catalog:end -->" + self.after(), encoding="utf-8")

    @staticmethod
    def before():
        return ("# Our hand-written catalog title\n\n"
                "Priority follows plans/priority.md; edit facts in each plan.md and run sync.\n\n"
                "**Definitions:** `active` = explicitly started; `queued` = planned, not started; "
                "`blocked` = known impediment; `paused` = deliberately stopped; "
                "`done` = accepted completion evidence; `cancelled` = intentionally abandoned, "
                "with reason in the plan. Owner is accountability, not permission. "
                "Estimates are remaining human engineering days or `TBD`.\n\n")

    @staticmethod
    def after():
        return "\n\n## Delivery context\n\nHand-written notes stay intact.\n"

    def test_catalog_region_preserves_prose_and_generates_only_marker_and_table(self):
        import views
        from records import split_table_row
        view = self.view()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.sources(root)
            text = views.expected(view, root)
            before, rest = text.split("<!-- plan-catalog:start -->")
            generated, after = rest.split("<!-- plan-catalog:end -->")
            self.assertEqual(before, self.before())
            self.assertEqual(after, self.after())
            self.assertEqual(text.count("<!-- plan-catalog:start -->"), 1)
            self.assertEqual(text.count("<!-- plan-catalog:end -->"), 1)
            self.assertEqual(generated.splitlines()[1], view.marker)
            self.assertTrue(all(line.startswith("|") for line in generated.splitlines()[2:] if line))
            self.assertFalse((root / "plans/catalog-notes.md").exists())
            lines = [line for line in text.splitlines() if line.startswith("|")]
            self.assertEqual(split_table_row(lines[0]), ["Plan", "Project", "Goal", "Status", "Owner", "Estimate", "Waiting on"])
            rows = [split_table_row(line) for line in lines[2:]]
            self.assertEqual(rows, [
                ["[Plan 01](01-alpha/plan.md)", "Catalog alpha", "Read [release](../releases/12.md)",
                 "active", "Ada", "TBD", "[work](02-beta/plan.md)"],
                ["[Plan 02](02-beta/plan.md)", "Catalog beta", "Build **one** thing", "done", "Ada", "TBD", "—"],
            ])

    def test_catalog_has_no_generated_preamble_helper(self):
        import views
        self.assertFalse(hasattr(views, "_catalog_preamble"))

    def test_edits_outside_catalog_region_are_free_and_survive_regeneration(self):
        import views
        from test_records import ProjectRecordTests as Records
        from unittest.mock import patch
        view = self.view()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.sources(root)
            with patch.object(views, "VIEWS", (view,)):
                views.sync(root)
                target = root / "plans/index.md"
                text = target.read_text(encoding="utf-8")
                text = text.replace(self.before(), "# A new author title\n\nFree prose above.\n")
                text = text.replace(self.after(), "\nFree prose below.\n")
                target.write_text(text, encoding="utf-8")
                self.assertEqual(views.check(root), [])
                self.assertEqual(views.sync(root), [])
                self.assertEqual(target.read_text(encoding="utf-8"), text)
                Records.write(root, "01-alpha", Records.plan(Project="Changed source", Status="active"))
                self.assertEqual(views.sync(root), ["plans/index.md"])
                rewritten = target.read_text(encoding="utf-8")
                self.assertEqual(rewritten.split("<!-- plan-catalog:start -->")[0],
                                 text.split("<!-- plan-catalog:start -->")[0])
                self.assertEqual(rewritten.split("<!-- plan-catalog:end -->")[1],
                                 text.split("<!-- plan-catalog:end -->")[1])
                self.assertIn("Changed source", rewritten)
                self.assertEqual(views.check(root), [])

    def test_region_markers_take_a_generic_region_name(self):
        # Neither a view's name nor a hard-coded vision-summary region wins
        # over its declared region name.
        view = View("sample", ("source.md",), "target.md", lambda root: "", region="other-region")
        text = "before\n<!-- other-region:start -->\nvalue\n<!-- other-region:end -->\nafter\n"
        wanted = text.replace("\nvalue\n", "\n" + view.marker + "\nvalue\n")
        self.assertEqual(_with_marker(view, text), wanted)
        self.assertEqual(_with_marker(view, wanted), wanted)
        for malformed in (text.replace("<!-- other-region:start -->", ""),
                          text.replace("<!-- other-region:end -->", ""),
                          text + "<!-- other-region:start -->\n<!-- other-region:end -->\n"):
            with self.subTest(malformed=malformed), self.assertRaisesRegex(ValueError, "view sample"):
                _with_marker(view, malformed)

    def test_vision_summary_declares_its_region_name(self):
        import views
        view = next(view for view in views.VIEWS if view.name == "root-vision-summary")
        self.assertEqual(view.region, "vision-summary")

    def test_rebase_relative_links_preserves_external_and_fragment_targets(self):
        import views
        value = ("[release](../../releases/12.md) [peer](../02-beta/plan.md#scope) "
                 "[local](#design) [web](https://example.invalid/a) [mail](mailto:a@example.invalid) "
                 "[custom](custom+app:resource) [root](/assets/icon.svg) plain text")
        wanted = ("[release](../releases/12.md) [peer](02-beta/plan.md#scope) "
                  "[local](#design) [web](https://example.invalid/a) [mail](mailto:a@example.invalid) "
                  "[custom](custom+app:resource) [root](/assets/icon.svg) plain text")
        self.assertEqual(views.rebase_links(value, Path("plans/01-alpha"), Path("plans")), wanted)
        self.assertEqual(views.rebase_links("No links **here**", Path("plans/01-alpha"), Path("plans")),
                         "No links **here**")

    def test_catalog_sync_is_idempotent_and_hand_edit_names_the_view(self):
        import checks
        import views
        from unittest.mock import patch
        view = self.view()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.sources(root)
            with patch.object(views, "VIEWS", (view,)):
                self.assertEqual(views.sync(root), ["plans/index.md"])
                first = (root / "plans/index.md").read_bytes()
                self.assertEqual(views.sync(root), [])
                self.assertEqual((root / "plans/index.md").read_bytes(), first)
                self.assertEqual(views.check(root), [])
                base = commit_base(root)
                target = root / "plans/index.md"
                target.write_text(target.read_text().replace("Catalog alpha", "Hand-edited alpha"), encoding="utf-8")
                errors = checks._generated_views(checks.Context(root, base=base))
                self.assertTrue(any("view plan-catalog" in line and "plans/index.md" in line for line in errors), errors)

    def test_new_valid_folder_appears_last_among_open_rows_without_a_catalog_edit(self):
        import views
        from records import split_table_row
        from test_records import ProjectRecordTests as Records
        view = self.view()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.sources(root)
            # It sorts before 01-alpha by folder, but explicit priority wins.
            Records.write(root, "00-new", Records.plan(Project="New open"))
            lines = [line for line in views.expected(view, root).splitlines() if line.startswith("|")][2:]
            self.assertEqual([split_table_row(line)[1] for line in lines],
                             ["Catalog alpha", "New open", "Catalog beta"])


class TouchedViewTests(unittest.TestCase):
    def repo(self, *, region=False):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        view = View("sample", ("source.md",), "target.md", lambda root: "unused", region)
        text = ("before\n<!-- custom:start -->\ngenerated\n<!-- custom:end -->\nafter\n"
                if region else "generated\n")
        (root / view.target).write_text(text, encoding="utf-8")
        (root / "source.md").write_text("source\n", encoding="utf-8")
        return root, view, commit_base(root)

    def test_unchanged_file_and_source_only_edit_are_untouched(self):
        import views
        root, view, base = self.repo()
        self.assertFalse(views.touched(view, root, base))
        (root / "source.md").write_text("new source\n", encoding="utf-8")
        self.assertFalse(views.touched(view, root, base))

    def test_unstaged_and_staged_file_edits_are_touched(self):
        import views
        root, view, base = self.repo()
        (root / view.target).write_text("hand edit\n", encoding="utf-8")
        self.assertTrue(views.touched(view, root, base))
        git(root, "add", view.target)
        self.assertTrue(views.touched(view, root, base))

    def test_committed_file_edit_is_touched(self):
        import views
        root, view, base = self.repo()
        (root / view.target).write_text("committed edit\n", encoding="utf-8")
        git(root, "add", view.target)
        git(root, "commit", "-qm", "edit target")
        self.assertTrue(views.touched(view, root, base))

    def test_new_untracked_file_is_touched(self):
        import views
        root, view, _ = self.repo()
        git(root, "rm", "-q", view.target)
        git(root, "commit", "-qm", "base without target")
        base = git(root, "rev-parse", "HEAD")
        (root / view.target).write_text("new file\n", encoding="utf-8")
        self.assertTrue(views.touched(view, root, base))

    def test_deleted_file_is_touched(self):
        import views
        root, view, base = self.repo()
        (root / view.target).unlink()
        self.assertTrue(views.touched(view, root, base))

    def test_comparison_uses_merge_base_instead_of_base_tip(self):
        import views
        root, view, _ = self.repo()
        git(root, "switch", "-qc", "other")
        (root / view.target).write_text("other branch\n", encoding="utf-8")
        git(root, "add", view.target)
        git(root, "commit", "-qm", "other target")
        base = git(root, "rev-parse", "HEAD")
        git(root, "switch", "-q", "main")
        self.assertFalse(views.touched(view, root, base))
        # Equal to the base tip, but changed relative to the common ancestor.
        (root / view.target).write_text("other branch\n", encoding="utf-8")
        self.assertTrue(views.touched(view, root, base))

    def test_generic_region_ignores_prose_before_and_after_markers(self):
        import views
        root, view, base = self.repo(region="custom")
        target = root / view.target
        target.write_text(target.read_text().replace("before", "new title").replace("after", "new notes"),
                          encoding="utf-8")
        self.assertFalse(views.touched(view, root, base))

    def test_generic_region_content_edit_is_touched(self):
        import views
        root, view, base = self.repo(region="custom")
        target = root / view.target
        target.write_text(target.read_text().replace("generated", "hand edit"), encoding="utf-8")
        self.assertTrue(views.touched(view, root, base))

    def test_missing_working_tree_region_marker_raises(self):
        import views
        root, view, base = self.repo(region="custom")
        target = root / view.target
        target.write_text(target.read_text().replace("<!-- custom:end -->", ""), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "sample|region"):
            views.touched(view, root, base)

    def test_region_marker_missing_in_both_versions_is_not_untouched(self):
        import views
        root, view, _ = self.repo(region="custom")
        target = root / view.target
        target.write_text(target.read_text().replace("<!-- custom:start -->", ""), encoding="utf-8")
        git(root, "add", view.target)
        git(root, "commit", "-qm", "missing marker")
        with self.assertRaisesRegex(ValueError, "sample|region"):
            views.touched(view, root, git(root, "rev-parse", "HEAD"))

    def test_region_added_after_base_without_markers_is_checked(self):
        import views
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "target.md"
            target.write_text("before\nafter\n", encoding="utf-8")
            view = View("sample", ("source.md",), "target.md",
                        lambda root: "before\n<!-- custom:start -->\nrendered\n<!-- custom:end -->\nafter\n",
                        "custom")
            base = commit_base(root)
            target.write_text(views.expected(view, root), encoding="utf-8")

            self.assertTrue(views.touched(view, root, base))
            self.assertEqual(check_view(view, root), [])
            target.write_text(target.read_text(encoding="utf-8").replace("rendered", "hand edited"),
                              encoding="utf-8")
            self.assertTrue(views.touched(view, root, base))
            self.assertEqual(len(check_view(view, root)), 1)

    def test_repaired_region_markers_are_checked(self):
        import views
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "target.md"
            target.write_text("before\n<!-- custom:start -->\nold generated\nafter\n", encoding="utf-8")
            view = View("sample", ("source.md",), "target.md",
                        lambda root: "before\n<!-- custom:start -->\nrendered\n<!-- custom:end -->\nafter\n",
                        "custom")
            base = commit_base(root)
            target.write_text(views.expected(view, root), encoding="utf-8")

            self.assertTrue(views.touched(view, root, base))
            self.assertEqual(check_view(view, root), [])
            target.write_text(target.read_text(encoding="utf-8").replace("rendered", "hand edited"),
                              encoding="utf-8")
            self.assertTrue(views.touched(view, root, base))
            self.assertEqual(len(check_view(view, root)), 1)


class GeneratedViewsRefreshTests(unittest.TestCase):
    def repo(self, *, region=False):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "source.md").write_text("source\n", encoding="utf-8")

        def render(root):
            content = (root / "source.md").read_text(encoding="utf-8")
            if not region:
                return content
            before, rest = (root / "target.md").read_text(encoding="utf-8").split("<!-- custom:start -->")
            _, after = rest.split("<!-- custom:end -->")
            return before + "<!-- custom:start -->\n" + content + "<!-- custom:end -->" + after

        view = View("sample", ("source.md",), "target.md", render, "custom" if region else False)
        target = root / view.target
        target.write_text("before\n<!-- custom:start -->\nold\n<!-- custom:end -->\nafter\n", encoding="utf-8")
        import views
        target.write_text(views.expected(view, root), encoding="utf-8")
        return root, view, commit_base(root)

    def errors(self, root, view, base=None):
        import checks
        import views
        from unittest.mock import patch
        # Isolate the refresh rule from unrelated source validators.
        with patch.object(views, "VIEWS", (view,)), \
             patch.object(checks, "_catalog", return_value=[]), \
             patch.object(checks, "_public_vision", return_value=[]):
            return checks._generated_views(checks.Context(root, base=base))

    def test_no_base_skips_a_stale_target(self):
        root, view, _ = self.repo()
        (root / "source.md").write_text("changed source\n", encoding="utf-8")
        self.assertEqual(self.errors(root, view), [])

    def test_source_only_change_leaves_stale_untouched_target_allowed(self):
        root, view, base = self.repo()
        (root / "source.md").write_text("changed source\n", encoding="utf-8")
        self.assertEqual(self.errors(root, view, base), [])

    def test_correctly_regenerated_touched_target_is_allowed(self):
        import views
        root, view, base = self.repo()
        (root / "source.md").write_text("changed source\n", encoding="utf-8")
        (root / view.target).write_text(views.expected(view, root), encoding="utf-8")
        self.assertEqual(self.errors(root, view, base), [])

    def test_hand_edit_names_view_target_and_source_to_edit(self):
        root, view, base = self.repo()
        (root / view.target).write_text("hand edit\n", encoding="utf-8")
        errors = self.errors(root, view, base)
        self.assertEqual(len(errors), 1, errors)
        for text in ("view sample", "target.md", "edit source.md"):
            self.assertIn(text, errors[0])

    def test_prose_only_edit_does_not_expose_a_stale_region(self):
        root, view, base = self.repo(region=True)
        (root / "source.md").write_text("changed source\n", encoding="utf-8")
        target = root / view.target
        target.write_text(target.read_text().replace("before", "free prose").replace("after", "free notes"),
                          encoding="utf-8")
        self.assertEqual(self.errors(root, view, base), [])

    def test_missing_region_marker_is_reported_even_when_unchanged(self):
        root, view, _ = self.repo(region=True)
        target = root / view.target
        target.write_text(target.read_text().replace("<!-- custom:start -->", ""), encoding="utf-8")
        git(root, "add", view.target)
        git(root, "commit", "-qm", "missing marker")
        errors = self.errors(root, view, git(root, "rev-parse", "HEAD"))
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("view sample", errors[0])
        self.assertIn("target.md", errors[0])

    def test_touched_check_catalog_renderer_failure_is_reported(self):
        import views
        from unittest.mock import patch
        root, _, base = self.repo()
        view = View("check-catalog", ("scripts/checks.py",), "target.md", views._checks)
        (root / view.target).write_text("hand edit\n", encoding="utf-8")
        # Keep git calls real: only the declared renderer fails.
        with patch.object(views, "_checks", side_effect=subprocess.CalledProcessError(1, ["astrid_dev.py", "list"])):
            view = View(view.name, view.sources, view.target, views._checks)
            errors = self.errors(root, view, base)
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("view check-catalog:", errors[0])
        self.assertIn("target.md", errors[0])
        self.assertIn("scripts/checks.py", errors[0])


class PublicVisionRefreshTests(unittest.TestCase):
    def repo(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name) / "repo"
        import golden
        golden._copy_tree(root)
        return root

    def stale_targets(self, root):
        for name in ("vision/README.md", "README.md"):
            target = root / name
            target.write_text(target.read_text() + "\nStale generated content.\n", encoding="utf-8")
        # The root view owns only its region; stale content must go inside it.
        target = root / "README.md"
        target.write_text(target.read_text().replace("<!-- vision-summary:end -->",
                          "stale\n<!-- vision-summary:end -->"), encoding="utf-8")

    def test_public_vision_source_check_ignores_stale_targets(self):
        import checks
        root = self.repo()
        self.stale_targets(root)
        self.assertEqual(checks._public_vision(checks.Context(root)), [])

    def test_exporter_accepts_stale_targets_and_does_not_write_them(self):
        import export_public_vision as exporter
        import json
        from unittest.mock import patch
        root = self.repo()
        self.stale_targets(root)
        before = {name: (root / name).read_bytes() for name in ("vision/README.md", "README.md")}
        output = root.parent / "vision.json"
        revision = "0000000000000000000000000000000000000000"
        wanted = exporter.build(root, revision)
        with patch.object(exporter, "ROOT", root), \
             patch("sys.argv", ["export_public_vision.py", "--revision", revision, "--output", str(output)]), \
             contextlib.redirect_stdout(io.StringIO()):
            code = exporter.main()
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.read_text()), wanted)
        self.assertEqual({name: (root / name).read_bytes() for name in before}, before)

    def test_exporter_removes_sync_readme_option(self):
        import export_public_vision as exporter
        from unittest.mock import patch
        root = self.repo()
        with patch.object(exporter, "ROOT", root), \
             patch("sys.argv", ["export_public_vision.py", "--sync-readme", "--revision",
                                "0000000000000000000000000000000000000000"]), \
             contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                exporter.main()
        self.assertEqual(error.exception.code, 2)


class SharedBlockTests(unittest.TestCase):
    OWNER = ("# Contract\n\n## Routing rules\n\n<!-- block-source:{name}:start -->\nRule {name} with [a link](sibling.md) and [here](#routing-rules).\n"
             "<!-- block-source:{name}:end -->\n")
    COPY = "Intro.\n\n<!-- block:{name}:start -->\n<!-- block:{name}:end -->\n\nOutro.\n"

    def setUp(self):
        import views
        from unittest.mock import patch
        patcher = patch.object(views, "VIEWS", ())  # only the block views, found under the temporary root
        patcher.start()
        self.addCleanup(patcher.stop)

    def repo(self, root, files, add=True):
        for name, text in files.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        git(root, "init", "-q")
        if add:
            git(root, "add", ".")

    def basic(self, root):
        self.repo(root, {"shared/owner.md": self.OWNER.format(name="r"), "shared/sibling.md": "# S\n",
                         "agent/deep/user.md": self.COPY.format(name="r")})

    def test_copy_is_filled_from_owner_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.basic(root)
            self.assertEqual(sync(root), ["agent/deep/user.md"])
            self.assertEqual(sync(root), [])
            self.assertEqual(check(root), [])
            text = (root / "agent/deep/user.md").read_text(encoding="utf-8")
            self.assertIn("Rule r with", text)
            self.assertTrue(text.startswith("Intro.\n\n"))
            self.assertTrue(text.endswith("\nOutro.\n"))
            self.assertIn("*From [Routing rules](../../shared/owner.md#routing-rules); edit it there.*", text)

    def test_links_and_same_file_anchors_are_rebased(self):
        import check_docs
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.basic(root)
            sync(root)
            text = (root / "agent/deep/user.md").read_text(encoding="utf-8")
            self.assertIn("[a link](../../shared/sibling.md)", text)
            self.assertIn("[here](../../shared/owner.md#routing-rules)", text)
            self.assertEqual(check_docs.local_links(root, Path("agent/deep/user.md")), [])

    def test_hand_edit_to_a_copy_fails_check_but_text_outside_does_not(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.basic(root)
            sync(root)
            target = root / "agent/deep/user.md"
            original = target.read_text(encoding="utf-8")
            target.write_text(original.replace("Outro", "Changed outro"), encoding="utf-8")
            self.assertEqual(check(root), [])
            target.write_text(original.replace("Rule r", "Hand rule"), encoding="utf-8")
            errors = check(root)
            self.assertEqual(len(errors), 1)
            self.assertIn("edit shared/owner.md instead", errors[0])

    def test_two_blocks_in_one_file(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.repo(root, {"a.md": self.OWNER.format(name="one"), "b.md": self.OWNER.format(name="two"),
                             "docs/c.md": self.COPY.format(name="one") + self.COPY.format(name="two")})
            self.assertEqual(sync(root), ["docs/c.md"])
            self.assertEqual(sync(root), [])
            self.assertEqual(check(root), [])
            text = (root / "docs/c.md").read_text(encoding="utf-8")
            self.assertIn("Rule one", text)
            self.assertIn("Rule two", text)

    def test_fenced_examples_are_ignored_beside_a_real_copy(self):
        for fence in ("```", "~~~"):
            with tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                example = f"{fence}\n<!-- block:r:start -->\n<!-- block:r:end -->\n{fence}\n\n"
                self.repo(root, {"o.md": f"{fence}\n<!-- block-source:r:start -->\n{fence}\n\n" + self.OWNER.format(name="r"),
                                 "docs/c.md": example + self.COPY.format(name="r")})
                self.assertEqual(sync(root), ["docs/c.md"])
                self.assertEqual(sync(root), [])
                self.assertEqual(check(root), [])
                text = (root / "docs/c.md").read_text(encoding="utf-8")
                self.assertTrue(text.startswith(example))
                self.assertEqual(text.count("Rule r"), 1)

    def test_untracked_files_are_not_scanned(self):
        import views
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.repo(root, {"o.md": self.OWNER.format(name="r"), "agent/c.md": self.COPY.format(name="r")}, add=False)
            git(root, "add", "o.md")
            self.assertEqual(views.block_views(root), ((), []))
            (root / ".gitignore").write_text("ignored.md\n", encoding="utf-8")
            (root / "ignored.md").write_text(self.OWNER.format(name="r"), encoding="utf-8")
            git(root, "add", ".gitignore", "agent/c.md")
            self.assertEqual(views.block_views(root)[1], [])

    def test_errors_are_returned_not_raised(self):
        import views
        cases = {
            "no owner": ({"agent/c.md": self.COPY.format(name="lost")}, "agent/c.md: block lost has no owner"),
            "two owners": ({"a.md": self.OWNER.format(name="r"), "b.md": self.OWNER.format(name="r")}, "2 owners (a.md, b.md)"),
            "copy in owner": ({"a.md": self.OWNER.format(name="r") + self.COPY.format(name="r")}, "a.md: block r has a copy region inside its own owner"),
            "history": ({"o.md": self.OWNER.format(name="r"), "docs/ledger/x.md": self.COPY.format(name="r")}, "docs/ledger/x.md: block r copy is not allowed here"),
            "github": ({"o.md": self.OWNER.format(name="r"), ".github/x.md": self.COPY.format(name="r")}, ".github/x.md: block r copy is not allowed here"),
            "unpaired": ({"o.md": self.OWNER.format(name="r"), "agent/bad.md": "<!-- block:r:start -->\n"}, "agent/bad.md: block:r needs exactly one start marker"),
            "duplicate": ({"o.md": self.OWNER.format(name="r"), "agent/bad.md": self.COPY.format(name="r") * 2}, "agent/bad.md: block:r needs exactly one start marker"),
        }
        for label, (files, message) in cases.items():
            with self.subTest(label), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self.repo(root, files)
                errors = views.block_views(root)[1]
                self.assertTrue(any(message in e for e in errors), errors)
                self.assertTrue(any(message in e for e in check(root)))
                with self.assertRaisesRegex(ValueError, "shared blocks"):
                    sync(root)

    def test_importing_views_survives_a_malformed_marker_in_the_repository(self):
        import views
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.repo(root, {"agent/bad.md": "<!-- block:r:start -->\n"})
            self.assertEqual(views.block_views(root)[0], ())
            self.assertEqual(views.views_for(root)[0], ())

    def test_generated_views_check_reports_block_errors_without_a_base(self):
        import checks
        from types import SimpleNamespace
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.repo(root, {"agent/c.md": self.COPY.format(name="lost")})
            errors = checks._generated_views(SimpleNamespace(root=root, base=None))
            self.assertEqual(len(errors), 1)
            self.assertIn("block lost has no owner", errors[0])

    def test_real_repository_routing_copies(self):
        # P73-07 decision 7159672645: real canonical consumers use direct links.
        import views
        from agent_documents import discover_documents, routing_table_headers
        from document_structure import section
        from test_agent_documents import REF
        root = Path(__file__).resolve().parent.parent
        found, errors = views.block_views(root)
        self.assertEqual(errors, [])
        documents = discover_documents(root)
        owners = {(Path("agent") / doc.relative).as_posix(): len(routing_table_headers(doc.body))
                  for doc in documents if routing_table_headers(doc.body)}
        self.assertEqual(owners, {"agent/shared/run-contract.md": 1})
        consumers = {
            "guides/codex-in-claude-cloud/README.md": "../../shared/run-contract.md#routing-and-bindings",
            "guides/codex-in-claude-cloud/manager-brief.md": "../../shared/run-contract.md#routing-and-bindings",
            "roles/leader/lane-orchestrators.md": "../../shared/run-contract.md#routing-and-bindings",
            "roles/leader/multi-manager-release.md": "../../shared/run-contract.md#routing-and-bindings",
            "roles/manager/astra-reflection.md": "../../shared/run-contract.md#routing-and-bindings",
            "roles/orchestrator.md": "../shared/run-contract.md#routing-and-bindings",
            "roles/orchestrator/codex-in-claude-cloud.md": "../../shared/run-contract.md#routing-and-bindings",
            "shared/workstreams/improve.md": "../run-contract.md#routing-and-bindings",
            "shared/workstreams/plan.md": "../run-contract.md#routing-and-bindings",
        }
        for relative, destination in consumers.items():
            with self.subTest(consumer=relative):
                self.assertIn("](" + destination + ")", (root / "agent" / relative).read_text(encoding="utf-8"))
        self.assertEqual(views._agent_routing_errors(root, documents, found), [])
        policy = next(doc for doc in documents if doc.relative == Path("shared/run-contract.md"))
        with tempfile.TemporaryDirectory() as directory:
            scratch = Path(directory)
            shutil.copytree(root / "agent", scratch / "agent", symlinks=True)
            (scratch / "agent/competing.md").write_text(
                REF + "\n" + section(policy.body, "Routing and bindings"), encoding="utf-8")
            problems = views._agent_routing_errors(scratch, discover_documents(scratch), ())
            self.assertTrue(any("agent/competing.md: competing route-to-model-family table"
                                in problem for problem in problems), problems)

    def test_retired_skills_root_is_not_an_allowed_block_copy(self):
        import views
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.repo(root, {"o.md": self.OWNER.format(name="r"),
                             "skills/c.md": self.COPY.format(name="r")})
            declarations, errors = views.block_views(root)
            self.assertEqual(declarations, ())
            self.assertTrue(any("skills/c.md: block r copy is not allowed here" in error for error in errors), errors)
            with self.assertRaisesRegex(ValueError, "not allowed here"):
                sync(root)


class SyncTargetSafetyTests(unittest.TestCase):
    def assert_refused_before_writing(self, root, unsafe):
        import views
        from unittest.mock import patch
        safe = root / "safe.md"
        safe.write_text("unchanged\n", encoding="utf-8")
        safe_view = View("safe", ("source.md",), "safe.md", lambda root: "new safe content\n")
        unsafe_view = View("unsafe", ("source.md",), unsafe, lambda root: "unsafe content\n")
        # The invalid target comes second: a per-write check is too late.
        with patch.object(views, "VIEWS", (safe_view, unsafe_view)):
            with self.assertRaisesRegex(ValueError, "unsafe|target|repository|symlink"):
                views.sync(root)
        self.assertEqual(safe.read_text(), "unchanged\n")

    def test_target_symlink_inside_repository_is_refused_before_any_write(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            real = root / "real.md"
            real.write_text("real content\n", encoding="utf-8")
            (root / "link.md").symlink_to("real.md")
            self.assert_refused_before_writing(root, "link.md")
            self.assertEqual(real.read_text(), "real content\n")

    def test_parent_symlink_leaving_repository_is_refused_before_any_write(self):
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            root = parent / "repo"
            root.mkdir()
            outside = parent / "outside"
            outside.mkdir()
            (root / "escape").symlink_to(outside, target_is_directory=True)
            self.assert_refused_before_writing(root, "escape/target.md")
            self.assertFalse((outside / "target.md").exists())

    def test_parent_traversal_leaving_repository_is_refused_before_any_write(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            root.mkdir()
            self.assert_refused_before_writing(root, "../outside.md")
            self.assertFalse((root.parent / "outside.md").exists())

    def test_absolute_target_outside_repository_is_refused_before_any_write(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            root.mkdir()
            outside = Path(directory) / "outside.md"
            self.assert_refused_before_writing(root, str(outside))
            self.assertFalse(outside.exists())


class PullRequestBaseTests(unittest.TestCase):
    def test_workflow_uses_main_as_of_merge_first_parent_or_event_base(self):
        import os
        import subprocess
        import textwrap
        source = (Path(__file__).resolve().parents[1] / ".github/workflows/docs.yml").read_text(encoding="utf-8")
        pr_step = source.split("      - name: Run repository checks\n", 1)[1].split("      - name:", 1)[0]
        self.assertIn("PR_HEAD_SHA: ${{ github.event.pull_request.head.sha }}", pr_step)
        script = textwrap.dedent(pr_step.split("        run: |\n", 1)[1])
        # The first parent is main as of that merge, not the event's base.
        for second_parent, first_parent, status, wanted_base in (
            ("pr-head", "merge-main", 0, "merge-main"),
            ("", "", 0, "event-base"),
            ("wrong-head", "merge-main", 1, None),
        ):
            with self.subTest(second_parent=second_parent), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                bin_dir = root / "bin"
                bin_dir.mkdir()
                git = bin_dir / "git"
                git.write_text("#!/bin/sh\ncase \"$*\" in\n"
                               "  'rev-parse --verify HEAD^2') [ -n \"$SECOND_PARENT\" ] || exit 1; printf '%s\\n' \"$SECOND_PARENT\" ;;\n"
                               "  'rev-parse HEAD^1') printf '%s\\n' \"$FIRST_PARENT\" ;;\n"
                               "  *) exit 2 ;;\nesac\n", encoding="utf-8")
                python = bin_dir / "python3"
                python.write_text("#!/bin/sh\nprintf '%s\\n' \"$@\" > \"$CAPTURE\"\n", encoding="utf-8")
                git.chmod(0o755)
                python.chmod(0o755)
                capture = root / "args.txt"
                env = dict(os.environ, PATH=str(bin_dir) + os.pathsep + os.environ["PATH"],
                           SECOND_PARENT=second_parent, FIRST_PARENT=first_parent,
                           PR_BASE_SHA="event-base", PR_HEAD_SHA="pr-head",
                           GITHUB_EVENT_PATH="event.json", CAPTURE=str(capture))
                result = subprocess.run(["bash", "-c", script], cwd=root, env=env,
                                        text=True, capture_output=True)
                self.assertEqual(result.returncode, status, result.stderr)
                if wanted_base is None:
                    self.assertFalse(capture.exists())
                else:
                    self.assertEqual(capture.read_text().splitlines(),
                                     ["scripts/astrid_dev.py", "check", "--base", wanted_base, "--event", "event.json"])


class RootStatementTests(unittest.TestCase):
    def test_root_readme_statement_is_generated_once_from_the_intro(self):
        root = Path(__file__).resolve().parent.parent
        intro = (root / "vision/intro.md").read_text(encoding="utf-8")
        title = intro.splitlines()[0].removeprefix("# Astrid — ")
        readme = (root / "README.md").read_text(encoding="utf-8")
        statement = f"**{title}.**"
        sentence = ("Astrid pairs an adaptable front end at [astrid.haus](https://astrid.haus) "
                    "with an agent equipped with tools for creative work and open-source AI.")
        self.assertEqual(readme.count(statement), 1)
        region = readme.split("<!-- vision-statement:start -->", 1)[1].split("<!-- vision-statement:end -->", 1)[0]
        self.assertIn(statement, region)
        self.assertNotIn(sentence, region)
        self.assertIn(f"## What we're building\n\n<!-- vision-statement:start -->", readme)
        self.assertIn(f"<!-- vision-statement:end -->\n\n{sentence}\n\n<!-- vision-summary:start -->", readme)


class StrategyViewTests(unittest.TestCase):
    def test_two_versions_roll_up_and_preserve_prose(self):
        import views
        from test_check_docs import StrategyTests
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'releases').mkdir()
            from test_records import ProjectRecordTests
            ProjectRecordTests.write(root, '40-machine-lifetime-controls', ProjectRecordTests.plan(Project='Machine lifetime controls'))
            (root / 'strategy.md').write_text(StrategyTests.GOOD, encoding='utf-8')
            def brief(n, kind, sentence):
                return (StrategyTests.RELEASE.replace('Release 13', f'Release {n}').replace('**Release:** 13', f'**Release:** {n}')
                        .replace('**State:** Draft', f'**State:** Draft\n**Kind:** {kind}')
                        .replace('Include spend control.', sentence))
            for n, kind in ((1, 'patch'), (2, 'minor'), (3, 'patch'), (4, 'minor')):
                (root / f'releases/{n}.md').write_text(brief(n, kind, f'Contribution {n}.'), encoding='utf-8')
            prior = views.VIEWS
            try:
                views.VIEWS = tuple(v for v in prior if v.name.startswith('strategy-'))
                self.assertEqual(sync(root), ['strategy.md'])
                self.assertEqual(sync(root), [])
                text = (root / 'strategy.md').read_text(encoding='utf-8')
                first = text.split('<!-- strategy-0.1:start -->')[1].split('<!-- strategy-0.1:end -->')[0]
                second = text.split('<!-- strategy-0.2:start -->')[1].split('<!-- strategy-0.2:end -->')[0]
                self.assertIn('Release 1 — GPU control', first)
                self.assertIn('Release 2](releases/2.md)', first)
                self.assertIn('[Release 1](releases/1.md): Contribution 1; [Release 2](releases/2.md): Contribution 2.', first)
                self.assertEqual(first.count('[Plan 40 — Machine lifetime controls]'), 1)
                self.assertIn('[Release 3](releases/3.md): Contribution 3; [Release 4](releases/4.md): Contribution 4.', second)
                self.assertIn('**Aim:** Fast.', text)
                (root / 'strategy.md').write_text(text.replace('Contribution 1;', 'Edited;'), encoding='utf-8')
                self.assertTrue(check_view(views.VIEWS[0], root))
                (root / 'strategy.md').write_text(text.replace('<!-- strategy-0.1:end -->', ''), encoding='utf-8')
                self.assertIn('restore', check_view(views.VIEWS[0], root)[0])
            finally:
                views.VIEWS = prior

    def test_frozen_issue_counts_use_reader_fields(self):
        from unittest.mock import patch
        import records
        import views
        from test_check_docs import StrategyTests
        from test_records import ProjectRecordTests
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'releases').mkdir()
            (root / 'strategy.md').write_text(StrategyTests.GOOD, encoding='utf-8')
            ProjectRecordTests.write(root, '40-machine-lifetime-controls', ProjectRecordTests.plan(Project='Machine lifetime controls'))
            (root / 'releases/13.md').write_text(StrategyTests.RELEASE, encoding='utf-8')
            original = records.release_brief
            def reader(text, **kwargs):
                brief = original(text, **kwargs)
                brief.update(issues=[{'number': 1}, {'number': 2}], issues_frozen=True,
                             issues_present=True, issues_date='2026-11-15')
                return brief
            with patch.object(records, 'release_brief', side_effect=reader):
                rendered = views._strategy(root, '0.1')
            self.assertIn('[Release 13 issues](releases/13.md#issues): 2', rendered)
            # A blank line separates the counts from the plan bullets above them.
            self.assertIn('.\n\n[Release 13 issues](releases/13.md#issues): 2', rendered)

    def test_normal_check_reports_missing_marker_before_sync(self):
        import astrid_dev
        source = Path(__file__).resolve().parent.parent
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'repo'
            copy_repo_fixture(source, root)
            target = root / 'strategy.md'
            target.write_text(target.read_text().replace('<!-- strategy-0.1:end -->', ''), encoding='utf-8')
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = astrid_dev.main(['check'], root=root)
            self.assertEqual(code, 1)
            self.assertIn('strategy-0.1:end', output.getvalue())
            self.assertNotIn('Traceback', output.getvalue())

    def test_sync_reports_missing_marker_as_one_error_line(self):
        import astrid_dev
        source = Path(__file__).resolve().parent.parent
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'repo'
            copy_repo_fixture(source, root)
            target = root / 'strategy.md'
            target.write_text(target.read_text(encoding='utf-8').replace('<!-- strategy-0.1:end -->', ''), encoding='utf-8')
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = astrid_dev.main(['sync'], root=root)
            self.assertEqual(code, 1)
            self.assertTrue(output.getvalue().startswith(
                'ERROR sync: view strategy-0.1: target must contain exactly one ordered'), output.getvalue())
            self.assertEqual(output.getvalue().count('\n'), 1)
            self.assertNotIn('Traceback', output.getvalue())

    def test_major_membership_and_next_version(self):
        from views import release_membership
        briefs = [{'number': str(n), 'kind': kind} for n, kind in
                  ((1, 'minor'), (2, 'patch'), (3, 'major'))]
        self.assertEqual([b['number'] for b in release_membership(briefs)['1.0']], ['2', '3'])
        self.assertEqual([b['number'] for b in release_membership(briefs[:2])['0.2']], ['2'])

    def test_after_ninth_minor_patches_belong_to_major_with_or_without_it(self):
        from views import release_membership
        minors = [{'number': str(n), 'kind': 'minor'} for n in range(1, 10)]
        patches = [{'number': '10', 'kind': 'patch'}, {'number': '11', 'kind': 'patch'}]
        for tail in (patches, patches + [{'number': '12', 'kind': 'major'}]):
            membership = release_membership(minors + tail)
            self.assertEqual([b['number'] for b in membership['1.0']], [b['number'] for b in tail])
            self.assertNotIn('0.10', membership)

    def test_major_renders_all_contributions_and_frozen_counts(self):
        from unittest.mock import patch
        import records
        import views
        from test_check_docs import StrategyTests
        from test_records import ProjectRecordTests
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'releases').mkdir()
            (root / 'strategy.md').write_text(StrategyTests.GOOD, encoding='utf-8')
            ProjectRecordTests.write(root, '40-machine-lifetime-controls', ProjectRecordTests.plan(Project='Machine lifetime controls'))
            self.assertIn('No release yet.', views._strategy(root, '1.0'))
            for n, kind in ((1, 'minor'), (2, 'patch'), (3, 'major')):
                brief = (StrategyTests.RELEASE.replace('Release 13', f'Release {n}')
                         .replace('**Release:** 13', f'**Release:** {n}')
                         .replace('**State:** Draft', f'**State:** Draft\n**Kind:** {kind}')
                         .replace('Include spend control.', f'Contribution {n}.'))
                (root / f'releases/{n}.md').write_text(brief, encoding='utf-8')
            original = records.release_brief
            def reader(text, **kwargs):
                brief = original(text, **kwargs)
                brief.update(issues=[{'number': 1}, {'number': 2}], issues_frozen=True)
                return brief
            with patch.object(records, 'release_brief', side_effect=reader):
                rendered = views._strategy(root, '1.0').split('<!-- strategy-1.0:start -->')[1].split('<!-- strategy-1.0:end -->')[0]
            self.assertIn('[Release 3](releases/3.md) — GPU control (Draft): Creators can control rented GPU machine lifetime.', rendered)
            self.assertIn('On the way: [Release 2 — GPU control](releases/2.md)', rendered)
            self.assertEqual(rendered.count('[Plan 40 — Machine lifetime controls]'), 1)
            self.assertIn('[Release 2](releases/2.md): Contribution 2; [Release 3](releases/3.md): Contribution 3.', rendered)
            self.assertEqual(rendered.count('Contribution 2'), 1)
            self.assertEqual(rendered.count('Contribution 3'), 1)
            self.assertNotIn('Contribution 1', rendered)
            self.assertIn('[Release 2 issues](releases/2.md#issues): 2', rendered)
            self.assertIn('[Release 3 issues](releases/3.md#issues): 2', rendered)


class AgentIndexTests(unittest.TestCase):
    TABLE = ("| Route | Work | Claude | Codex |\n| --- | --- | --- | --- |\n"
             "| N | Bounded work | First family | Second family |\n")
    NAMES = {"workstream-index-leader", "workstream-index-manager",
             "workstream-index-orchestrator", "shared-workstream-index"}

    def declarations(self):
        import views
        return tuple(view for view in views.VIEWS if view.name in self.NAMES)

    def fixture(self, root):
        from test_agent_documents import ROLE, REF
        for role in ("leader", "manager", "orchestrator"):
            path = root / "agent/roles" / f"{role}.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(ROLE.replace("# Leader", "# " + role.capitalize()) +
                            "\nBefore navigation.\n\n## Workstreams\n\n"
                            "<!-- workstreams:start -->\n<!-- workstreams:end -->\n\n"
                            "After navigation.\n", encoding="utf-8")
        (root / "agent/README.md").write_text(
            REF + "\n## Shared workstreams\n\nBefore shared navigation.\n\n"
            "<!-- shared-workstreams:start -->\n<!-- shared-workstreams:end -->\n\n"
            "After shared navigation.\n", encoding="utf-8")
        policy = root / "agent/shared/run-contract.md"
        policy.parent.mkdir(parents=True)
        policy.write_text(REF + "\n## Routing and bindings\n\n" + self.TABLE, encoding="utf-8")

    def stream(self, root, relative, title="Alpha", description=None, skill=False):
        from test_agent_documents import STREAM
        text = STREAM.replace("# Plan\n", f"# {title}\n")
        if not skill:
            text = text.replace("skill: true\n", "")
        if description is not None:
            text = text.replace("description: Plan an independently useful outcome.",
                                "description: " + description)
        path = root / "agent" / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_real_canonical_indexes_have_only_the_four_declared_targets(self):
        import views
        from agent_documents import discover_documents
        root = Path(__file__).resolve().parents[1]
        declarations = self.declarations()
        self.assertEqual(len(declarations), 4)
        self.assertEqual({view.name: view.target for view in declarations}, {
            "workstream-index-leader": "agent/roles/leader.md",
            "workstream-index-manager": "agent/roles/manager.md",
            "workstream-index-orchestrator": "agent/roles/orchestrator.md",
            "shared-workstream-index": "agent/README.md",
        })
        self.assertEqual(views.agent_index_errors(root), [])
        documents = discover_documents(root)
        for view in declarations:
            rendered = views.expected(view, root)
            self.assertIn(view.marker, rendered)
            self.assertTrue(all(source.startswith("agent/") for source in view.sources))
            if view.region == "workstreams":
                role = Path(view.target).stem
                for document in documents:
                    if document.kind == "workstream" and document.relative.parent == Path("roles") / role:
                        self.assertIn(f"- [{document.title}]({role}/{document.path.name}) — {document.description}", rendered)
            else:
                region = rendered.split("<!-- shared-workstreams:start -->", 1)[1].split("<!-- shared-workstreams:end -->", 1)[0]
                for document in documents:
                    if document.kind == "workstream" and document.relative.parent == Path("shared/workstreams"):
                        self.assertIn(f"- [{document.title}](shared/workstreams/{document.path.name})", region)
                        self.assertNotIn(document.description, region)

    def test_add_edit_remove_uses_only_canonical_workstream_metadata(self):
        import views
        from test_agent_documents import REF
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            first = self.stream(root, "roles/manager/alpha.md")
            view = next(view for view in self.declarations() if view.name == "workstream-index-manager")
            original = views.expected(view, root)
            self.assertIn("[Alpha](manager/alpha.md)", original)
            second = self.stream(root, "roles/manager/beta.md", "Beta")
            added = views.expected(view, root)
            self.assertLess(added.index("[Alpha]"), added.index("[Beta]"))
            self.stream(root, "roles/manager/beta.md", "Beta changed", "Follow the updated procedure and report evidence.")
            changed = views.expected(view, root)
            self.assertIn("[Beta changed](manager/beta.md) — Follow the updated procedure and report evidence.", changed)
            guide = root / "agent/roles/manager/setup/README.md"
            guide.parent.mkdir()
            guide.write_text(REF, encoding="utf-8")
            self.assertEqual(views.expected(view, root), changed)
            second.unlink()
            self.assertEqual(views.expected(view, root), original)
            first.unlink()
            self.assertNotIn("[Alpha]", views.expected(view, root))

    def test_shared_index_lists_reference_only_and_opted_in_workstreams_without_descriptions(self):
        import views
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            self.stream(root, "shared/workstreams/alpha.md", "Alpha", skill=False)
            self.stream(root, "shared/workstreams/beta.md", "Beta", skill=True)
            view = next(view for view in self.declarations() if view.name == "shared-workstream-index")
            rendered = views.expected(view, root)
            self.assertIn("- [Alpha](shared/workstreams/alpha.md)", rendered)
            self.assertIn("- [Beta](shared/workstreams/beta.md)", rendered)
            self.assertNotIn("Plan an independently useful outcome.", rendered)
            self.assertLess(rendered.index("[Alpha]"), rendered.index("[Beta]"))

    def test_regeneration_preserves_prose_and_is_idempotent(self):
        import views
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            self.stream(root, "roles/manager/alpha.md")
            self.stream(root, "shared/workstreams/shared.md", "Shared")
            declarations = self.declarations()
            before = {view.target: (root / view.target).read_text(encoding="utf-8") for view in declarations}
            with patch.object(views, "VIEWS", declarations):
                self.assertEqual(set(sync(root)), set(before))
                self.assertEqual(sync(root), [])
                self.assertEqual(check(root), [])
            for view in declarations:
                text = (root / view.target).read_text(encoding="utf-8")
                start, end = f"<!-- {view.region}:start -->", f"<!-- {view.region}:end -->"
                self.assertEqual(text.split(start, 1)[0], before[view.target].split(start, 1)[0])
                self.assertEqual(text.split(end, 1)[1], before[view.target].split(end, 1)[1])
                self.assertEqual(text.count(view.marker), 1)

    def test_source_only_edit_keeps_refresh_policy_and_hand_edited_index_refuses(self):
        import checks
        import views
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            self.stream(root, "roles/manager/alpha.md")
            declarations = self.declarations()
            view = next(view for view in declarations if view.name == "workstream-index-manager")
            with patch.object(views, "VIEWS", declarations), \
                 patch.object(checks, "_catalog", return_value=[]), \
                 patch.object(checks, "_public_vision", return_value=[]):
                sync(root)
                base = commit_base(root)
                self.stream(root, "roles/manager/alpha.md", "New title", "Follow the updated procedure and report evidence.")
                self.assertTrue(check_view(view, root))
                self.assertEqual(checks._generated_views(checks.Context(root, base=base)), [])
                self.assertEqual(sync(root), [view.target])
                self.assertEqual(check_view(view, root), [])
                target = root / view.target
                target.write_text(target.read_text(encoding="utf-8").replace("[New title]", "[Hand edit]"), encoding="utf-8")
                errors = checks._generated_views(checks.Context(root, base=base))
                self.assertTrue(any("view workstream-index-manager:" in error for error in errors), errors)

    def test_every_marker_failure_refuses_before_any_generated_write(self):
        import views
        from unittest.mock import patch
        declarations = self.declarations()
        for view in declarations:
            for kind in ("missing", "repeated", "reversed"):
                with self.subTest(target=view.target, kind=kind), tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    self.fixture(root)
                    start, end = f"<!-- {view.region}:start -->", f"<!-- {view.region}:end -->"
                    target = root / view.target
                    original = target.read_text(encoding="utf-8")
                    if kind == "missing":
                        altered = original.replace(end, "", 1)
                    elif kind == "repeated":
                        altered = original.replace(start, start + "\n" + start, 1)
                    else:
                        altered = original.replace(start, "REPLACE_START", 1).replace(end, start, 1).replace("REPLACE_START", end, 1)
                    target.write_text(altered, encoding="utf-8")
                    safe = root / "safe.md"
                    safe.write_text("untouched\n", encoding="utf-8")
                    first = View("sentinel", ("input.md",), "safe.md", lambda root: "changed\n")
                    before = {item.target: (root / item.target).read_bytes() for item in declarations}
                    with patch.object(views, "VIEWS", (first, *declarations)):
                        with self.assertRaisesRegex(ValueError, "exactly one ordered"):
                            sync(root)
                    self.assertEqual(safe.read_text(encoding="utf-8"), "untouched\n")
                    self.assertEqual({path: (root / path).read_bytes() for path in before}, before)

    def test_undeclared_role_does_not_expand_write_targets(self):
        import checks
        import views
        from test_agent_documents import ROLE
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            (root / "agent/roles/stranger.md").write_text(ROLE, encoding="utf-8")
            self.stream(root, "roles/stranger/work.md")
            declarations = self.declarations()
            safe = root / "safe.md"
            safe.write_text("untouched\n", encoding="utf-8")
            first = View("sentinel", ("input.md",), "safe.md", lambda root: "changed\n")
            with patch.object(views, "VIEWS", (first, *declarations)):
                errors = checks._workstream_structure(checks.Context(root))
                self.assertTrue(any("unregistered parent agent/roles/stranger.md" in error for error in errors), errors)
                self.assertNotIn("agent/roles/stranger.md", {view.target for view in views.views_for(root)[0]})
                with self.assertRaisesRegex(ValueError, "unregistered parent"):
                    sync(root)
            self.assertEqual(safe.read_text(encoding="utf-8"), "untouched\n")

    def test_description_refusal_stays_in_one_always_on_registered_gate(self):
        import checks
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            path = self.stream(root, "roles/manager/alpha.md")
            gates = [gate for gate in checks.REGISTRY if gate.id == "workstream-structure"]
            self.assertEqual(len(gates), 1)
            self.assertEqual(gates[0].trigger, "always")
            self.assertEqual(gates[0].run(checks.Context(root)), [])
            path.write_text(path.read_text(encoding="utf-8").replace("description: Plan an independently useful outcome.\n", ""), encoding="utf-8")
            self.assertTrue(any("description" in error for error in gates[0].run(checks.Context(root))))

    def test_duplicate_missing_and_competing_route_policies_refuse(self):
        import checks
        from test_agent_documents import REF
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            policy = root / "agent/shared/run-contract.md"
            original = policy.read_text(encoding="utf-8")
            for altered in (original + "\n" + self.TABLE, original.replace(self.TABLE, "No table.\n")):
                policy.write_text(altered, encoding="utf-8")
                errors = checks._workstream_structure(checks.Context(root))
                self.assertTrue(any("exactly one route-to-model-family table" in error for error in errors), errors)
            policy.write_text(original, encoding="utf-8")
            rival = root / "agent/rival.md"
            for body in (self.TABLE, "<!-- block:routing:start -->\n" + self.TABLE + "<!-- block:routing:end -->\n"):
                rival.write_text(REF + "\n" + body, encoding="utf-8")
                errors = checks._workstream_structure(checks.Context(root))
                self.assertTrue(any("agent/rival.md: competing route-to-model-family table" in error for error in errors), errors)

    def test_role_mode_tables_and_fenced_routing_examples_remain_valid(self):
        import checks
        from test_agent_documents import REF
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            ordinary = ("| Route | The manager's own work |\n| --- | --- |\n| X | Decisions |\n\n"
                        "| Route | ChatGPT mode |\n| --- | --- |\n| X | Extra High |\n")
            for fence in ("```", "~~~"):
                (root / "agent/examples.md").write_text(REF + "\n" + ordinary + "\n" + fence + "\n" + self.TABLE + fence + "\n", encoding="utf-8")
                self.assertEqual(checks._workstream_structure(checks.Context(root)), [])

    def test_generated_routing_region_requires_its_real_owner_and_can_refresh(self):
        import checks
        import views
        from test_agent_documents import REF
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            policy = root / "agent/shared/run-contract.md"
            text = policy.read_text(encoding="utf-8")
            policy.write_text(text.replace(self.TABLE, "<!-- block-source:routing:start -->\n" + self.TABLE + "<!-- block-source:routing:end -->\n"), encoding="utf-8")
            copy = root / "agent/copied.md"
            copy.write_text(REF + "\n<!-- block:routing:start -->\n<!-- block:routing:end -->\n", encoding="utf-8")
            git(root, "init", "-q")
            git(root, "add", "agent")
            with patch.object(views, "VIEWS", self.declarations()):
                sync(root)
                self.assertEqual(check(root), [])
                self.assertEqual(checks._workstream_structure(checks.Context(root)), [])
                policy.write_text(policy.read_text(encoding="utf-8").replace("First family", "Updated family"), encoding="utf-8")
                self.assertTrue(check(root))
                self.assertEqual(sync(root), ["agent/copied.md"])
                self.assertIn("Updated family", copy.read_text(encoding="utf-8"))
                self.assertEqual(check(root), [])
                copy.write_text(copy.read_text(encoding="utf-8") + "\n" + self.TABLE, encoding="utf-8")
                errors = checks._workstream_structure(checks.Context(root))
                self.assertTrue(any("competing route-to-model-family table" in error for error in errors), errors)
                with self.assertRaisesRegex(ValueError, "competing route-to-model-family table"):
                    sync(root)


if __name__ == "__main__":
    unittest.main()
