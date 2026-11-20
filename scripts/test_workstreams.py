"""One workstream contract across skill packages and role-specific documents."""
import tempfile
import unittest
from pathlib import Path

from checks import Context, REGISTRY
from views import VIEWS, View, check_view, expected
from workstreams import END, START, PARENT_SKILLS, ROLE_SKILLS, SHARED_START, SHARED_END, CONTRACT_FIELDS, parse_workstream, shared_skill_files, metadata, render_index, render_shared_index, validate, workstream_files


MANAGE = "skills/roles/astrid-dev-manage/SKILL.md"

CONTRACT = (
    "\n## Workstream contract\n\n"
    "**Outcome:** Deliver an accepted and testable result with receipts.\n"
    "**When to use:** Select this workstream for the assigned operating context.\n"
    "**Inputs:** An authorized brief, source identity and accepted proof requirements.\n"
    "**Procedure:** Read the brief, perform the defined steps and preserve original outcomes.\n"
    "**Completion:** Report source, evidence and remaining blockers to the accountable agent.\n"
)


def shared_workstream(root, name="astrid-dev-sample"):
    folder = root / "skills/shared/workstreams" / name
    folder.mkdir(parents=True, exist_ok=True)
    skill = folder / "SKILL.md"
    skill.write_text(
        f"---\nname: {name}\ndescription: Deliver an independently useful result.\n---\n\n"
        "# Example shared workstream\n" + CONTRACT + "\nRun the existing procedure.\n",
        encoding="utf-8",
    )
    return skill



def workstream(root, name, description="Execute this operating pattern and provide verifiable results.",
               title=None):
    path = root / MANAGE.replace("SKILL.md", "workstreams/" + name + ".md")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"---\ndescription: {description}\n---\n\n# Workstream: {title or name}\n" + CONTRACT + "\nSteps.\n",
        encoding="utf-8",
    )
    return path


def fixture(root):
    for parent in ROLE_SKILLS:
        path = root / parent
        path.parent.mkdir(parents=True, exist_ok=True)
        body = "# Role\n\nBefore.\n\n"
        if parent in PARENT_SKILLS:
            body += "## Workstreams\n\n" + START + "\n" + END + "\n\n"
        body += "## Shared workstreams\n\n" + SHARED_START + "\n" + SHARED_END + "\n\nAfter.\n"
        path.write_text(body, encoding="utf-8")


class WorkstreamDiscoveryTests(unittest.TestCase):
    def test_repository_workstreams_are_all_valid_and_indexes_are_current(self):
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(validate(root), [])
        # Discovery remains open to additions and legitimate removals; no frozen roster.
        for path in workstream_files(root):
            self.assertTrue(metadata(path)[1])
        for parent in PARENT_SKILLS:
            registered = [v for v in VIEWS if v.target == parent and v.region == "workstreams"]
            self.assertEqual(len(registered), 1, parent)
            view = registered[0]
            # A source-only PR may leave the checked-in view stale until the
            # post-main refresh; tests must not force duplicate parent edits.
            generated = expected(view, root)
            self.assertIn(START, generated)
            self.assertIn(END, generated)
            for path in workstream_files(root):
                if (path.parent.parent / "SKILL.md").relative_to(root).as_posix() == parent:
                    title, description = metadata(path)
                    self.assertIn(f"[{title}](workstreams/{path.name}) — {description}", generated)

    def test_add_edit_and_remove_workstream_from_single_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            first = workstream(root, "alpha", title="Alpha")
            original = render_index(root, MANAGE)
            self.assertIn("[Alpha](workstreams/alpha.md)", original)
            second = workstream(root, "beta", title="Beta")
            added = render_index(root, MANAGE)
            self.assertIn("[Beta](workstreams/beta.md)", added)
            self.assertLess(added.index("[Alpha]"), added.index("[Beta]"))
            workstream(root, "beta", "Follow the updated procedure and report the evidence.", title="Beta")
            self.assertIn("updated procedure", render_index(root, MANAGE))
            second.unlink()
            self.assertEqual(render_index(root, MANAGE), original)
            first.unlink()
            self.assertNotIn("[Alpha]", render_index(root, MANAGE))

    def test_regeneration_preserves_human_authored_content_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            workstream(root, "alpha", title="Alpha")
            view = View("test-workstreams", ("skills/roles/astrid-dev-manage/workstreams/*.md",),
                        MANAGE, lambda root: render_index(root, MANAGE), "workstreams")
            generated = expected(view, root)
            self.assertIn("Before.", generated)
            self.assertIn("After.", generated)
            self.assertIn("<!-- Generated by Astrid Dev view: test-workstreams;", generated)
            (root / MANAGE).write_text(generated, encoding="utf-8")
            self.assertEqual(expected(view, root), generated)
            self.assertEqual(check_view(view, root), [])

    def test_rejects_missing_or_multiline_description_and_missing_heading(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            path = workstream(root, "alpha")
            for invalid, expected_message in (
                ("# Workstream: alpha\n", "missing frontmatter"),
                ("---\ndescription: A line.\n  extra: bad\n---\n# Workstream: alpha\n",
                 "frontmatter fields must be nonempty"),
                ("---\ndescription: \n---\n# Workstream: alpha\n", "frontmatter fields must be nonempty"),
                ("---\ndescription: No terminal punctuation\n---\n# Workstream: alpha\n",
                 "plain-text sentence"),
                ("---\ndescription: Good sentence.\n---\n# Wrong heading\n",
                 "first body heading"),
            ):
                with self.subTest(invalid=invalid):
                    path.write_text(invalid, encoding="utf-8")
                    self.assertTrue(any(expected_message in error for error in validate(root)))

    def test_duplicate_titles_fail_and_nested_guides_are_not_workstreams(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            workstream(root, "one", title="Same")
            workstream(root, "two", title="Same")
            errors = validate(root)
            self.assertTrue(any("duplicate workstream title" in error for error in errors), errors)
            guide = root / MANAGE.replace("SKILL.md", "workstreams/setup/README.md")
            guide.parent.mkdir(parents=True)
            guide.write_text("A guide without workstream metadata.\n", encoding="utf-8")
            self.assertEqual(len(workstream_files(root)), 2)

    def test_unregistered_parent_fails_without_extending_write_allowlist(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            stranger = root / "skills/roles/astrid-dev-new/workstreams/new.md"
            stranger.parent.mkdir(parents=True)
            stranger.write_text("---\ndescription: Execute a new route and report evidence.\n---\n"
                                "# Workstream: New route\n", encoding="utf-8")
            self.assertTrue(any("unregistered parent" in error for error in validate(root)))

    def test_broken_parent_markers_fail_without_erasing_prose(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            workstream(root, "alpha")
            path = root / MANAGE
            path.write_text(path.read_text().replace(END, ""), encoding="utf-8")
            self.assertTrue(any("exactly one ordered" in error for error in validate(root)))
            with self.assertRaisesRegex(ValueError, "exactly one ordered"):
                render_index(root, MANAGE)

    def test_shared_workstream_skills_require_namespaced_folder_and_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            folder = root / "skills/shared/workstreams/astrid-dev-sample"
            folder.mkdir(parents=True)
            skill = folder / "SKILL.md"
            shared_workstream(root, "astrid-dev-sample")
            self.assertEqual(validate(root), [])
            skill.write_text(skill.read_text().replace("name: astrid-dev-sample", "name: sample"), encoding="utf-8")
            self.assertTrue(any("skill name must be an astrid-dev-*" in message for message in validate(root)))
            skill.write_text(skill.read_text().replace("description: Deliver an independently useful result.\n", ""), encoding="utf-8")
            self.assertTrue(any("frontmatter must contain exactly" in message for message in validate(root)))

    def test_shared_workstream_names_render_without_descriptions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            folder = root / "skills/shared/workstreams/astrid-dev-foo"
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_text(
                "---\nname: astrid-dev-foo\ndescription: Do the shared task.\n---\n"
                "\n# Example shared workstream\n" + CONTRACT, encoding="utf-8")
            for parent in ROLE_SKILLS:
                skill = root / parent
                rendered = render_shared_index(root, parent)
                self.assertIn("- [astrid-dev-foo](../../shared/workstreams/astrid-dev-foo/SKILL.md)", rendered)
                self.assertNotIn("Do the shared task", rendered)

    def test_all_parent_skills_register_shared_indexes(self):
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(validate(root), [])
        for parent in ROLE_SKILLS:
            views = [v for v in VIEWS if v.target == parent and v.region == "shared-workstreams"]
            self.assertEqual(len(views), 1)
            self.assertIn("astrid-dev-plan", expected(views[0], root))


    def test_one_parsed_contract_for_both_packaging_formats(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            doc = parse_workstream(workstream(root, "alpha"))
            skill = parse_workstream(shared_workstream(root))
            self.assertEqual((doc.outcome, doc.when_to_use, doc.inputs, doc.procedure, doc.completion),
                             (skill.outcome, skill.when_to_use, skill.inputs, skill.procedure, skill.completion))
            self.assertEqual(doc.kind, "document")
            self.assertIsNone(doc.name)
            self.assertEqual(skill.kind, "skill")
            self.assertEqual(skill.name, "astrid-dev-sample")
            self.assertEqual(len(CONTRACT_FIELDS), 5)
            self.assertEqual(validate(root), [])

    def test_missing_out_of_order_empty_and_duplicate_contract_fields_fail_in_both_formats(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            documents = [workstream(root, "alpha"), shared_workstream(root)]
            for path in documents:
                original = path.read_text(encoding="utf-8")
                wrong = [
                    (original.replace("## Workstream contract", "## Different", 1), "first ## section"),
                    (original.replace("**Inputs:** An authorized brief, source identity and accepted proof requirements.\n", ""), "contract fields must be"),
                    (original.replace("**Inputs:** An authorized brief, source identity and accepted proof requirements.\n",
                                      "**Inputs:** \n"), "contract must contain only"),
                    (original.replace("**Procedure:** Read the brief, perform the defined steps and preserve original outcomes.\n",
                                      "**Completion:** Read the brief, perform the defined steps and preserve original outcomes.\n"),
                     "duplicate contract field"),
                    (original.replace("**Inputs:** An authorized brief, source identity and accepted proof requirements.\n"
                                      "**Procedure:** Read the brief, perform the defined steps and preserve original outcomes.\n",
                                      "**Procedure:** Read the brief, perform the defined steps and preserve original outcomes.\n"
                                      "**Inputs:** An authorized brief, source identity and accepted proof requirements.\n"),
                     "contract fields must be"),
                ]
                for altered, error in wrong:
                    with self.subTest(path=path.name, error=error):
                        path.write_text(altered, encoding="utf-8")
                        self.assertTrue(any(error in finding for finding in validate(root)), validate(root))
                path.write_text(original, encoding="utf-8")
            self.assertEqual(validate(root), [])

    def test_all_existing_workstreams_have_the_same_five_fields(self):
        root = Path(__file__).resolve().parents[1]
        all_files = [*workstream_files(root), *shared_skill_files(root)]
        self.assertGreaterEqual(len(all_files), 15)
        for path in all_files:
            with self.subTest(path=path.relative_to(root).as_posix()):
                entry = parse_workstream(path)
                for value in (entry.outcome, entry.when_to_use, entry.inputs, entry.procedure, entry.completion):
                    self.assertGreaterEqual(len(value), 12)

    def test_one_line_description_is_an_always_on_ci_gate(self):
        checks = [check for check in REGISTRY if check.id == "workstream-structure"]
        self.assertEqual(len(checks), 1)
        self.assertEqual(checks[0].trigger, "always")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            path = workstream(root, "alpha")
            self.assertEqual(checks[0].run(Context(root=root)), [])
            path.write_text("# Workstream: alpha\n", encoding="utf-8")
            errors = checks[0].run(Context(root=root))
            self.assertTrue(any("missing frontmatter" in error for error in errors), errors)

    def test_metadata_is_only_in_workstream_and_title_is_h1(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            path = workstream(root, "alpha", title="The actual route")
            self.assertEqual(metadata(path), ("The actual route",
                            "Execute this operating pattern and provide verifiable results."))


if __name__ == "__main__":
    unittest.main()
