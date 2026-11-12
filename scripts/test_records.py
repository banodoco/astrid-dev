"""Policies shared by Markdown and Git record readers."""
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from records import (
    PLACEHOLDERS_ACTIVE_OWNER,
    PLACEHOLDERS_COMPLETION,
    PLACEHOLDERS_GAP,
    PLACEHOLDERS_PLANNING,
    field_match,
    git_output,
    git_result,
    git_show,
    heading,
    is_placeholder,
    key_value_lines,
    matching_sections,
    named_field_matches,
    read_text,
    section,
    section_after_match,
    split_table_row,
)


class MarkdownRecordTests(unittest.TestCase):
    def test_heading_missing_policy_and_exact_prefix(self):
        text = "# Main\n## Sub\n"
        self.assertEqual(heading(text), "Main")
        self.assertEqual(heading(text, "## "), "Sub")
        self.assertIsNone(heading(text, "### ", missing="none"))
        self.assertEqual(heading(text, "### ", missing="empty"), "")
        with self.assertRaisesRegex(ValueError, "missing heading: ### "):
            heading(text, "### ")

    def test_section_missing_and_empty_policies(self):
        text = "## Present\n   \n## Next\nvalue\n"
        self.assertEqual(section(text, "Present", boundary=r"^## "), "")
        self.assertEqual(section(text, "Absent"), "")
        self.assertIsNone(section(text, "Absent", missing="none"))
        with self.assertRaisesRegex(ValueError, "missing section: Absent"):
            section(text, "Absent", missing="error")

    def test_section_boundary_and_strip_are_caller_policies(self):
        text = "## Start\n  keep\n### Nested\ninside\n#### Deeper\nend\n## Next\nstop\n"
        # check_docs/exporter stop at any line beginning with H2 syntax; H3 is included.
        self.assertEqual(section(text, "Start", boundary=r"^## "), "keep\n### Nested\ninside\n#### Deeper\nend")
        # completion stops at H1-H3, but returns raw whitespace/content.
        match = matching_sections(text, r"^## Start\s*$")[0]
        self.assertEqual(section_after_match(text, match, boundary=r"^#{1,3}\s+\S"), "\n  keep\n")
        # planning evidence uses a narrower H2 boundary and strips the result.
        self.assertEqual(section(text, "Start", boundary=r"^## \S"), "keep\n### Nested\ninside\n#### Deeper\nend")

    def test_plain_and_bold_fields_preserve_key_and_value_policies(self):
        text = "Evidence: https://example.test\n**Prior art:**  a source  \nEvidence: second\n"
        self.assertEqual(field_match(text, "Evidence").group(1), "https://example.test")
        self.assertEqual(field_match(text, "Prior art", style="bold").group(1), "a source  ")
        self.assertIsNone(field_match(text, "Missing"))
        self.assertEqual(field_match("completion: Yes — reason", "Completion",
                                     value_pattern=r"(Yes|Met)\s*[—:-]\s*(.+)",
                                     flags=re.I | re.M).groups(), ("Yes", "reason"))
        with self.assertRaisesRegex(ValueError, "unknown field style"):
            field_match(text, "Evidence", style="table")

    def test_named_bold_fields_keep_exact_labels_and_duplicate_order(self):
        text = "**Prior art:** first\n**Approach:** do this\n**Prior art:** second\n"
        matches = named_field_matches(text, ("Prior art", "Approach"))
        self.assertEqual([match.groups() for match in matches],
                         [("Prior art", "first"), ("Approach", "do this"), ("Prior art", "second")])

    def test_header_lines_keep_malformed_and_duplicate_entries_visible(self):
        self.assertEqual(key_value_lines("Date: 2026-11-11\nKind: fix\n"),
                         [("Date", ":", "2026-11-11"), ("Kind", ":", "fix")])
        self.assertEqual(key_value_lines("**Owner:** Ada\n", style="bold"), [("Owner", ":", "Ada")])
        self.assertEqual(key_value_lines("No separator\n"), [("No separator", "", "")])
        self.assertEqual(key_value_lines("Date: a\nDate: b\n")[0][0], "Date")

    def test_table_split_matches_simple_pipe_table_rules(self):
        self.assertEqual(split_table_row(" | First | Second | "), ["First", "Second"])
        self.assertEqual(split_table_row(r"| a\|b | c |"), ["a\\", "b", "c"])


class PlaceholderPolicyTests(unittest.TestCase):
    def test_caller_token_sets_and_normalization_remain_distinct(self):
        self.assertTrue(is_placeholder(" pending. ", PLACEHOLDERS_COMPLETION))
        self.assertTrue(is_placeholder(" because ", PLACEHOLDERS_GAP))
        self.assertFalse(is_placeholder(" because ", PLACEHOLDERS_COMPLETION))
        self.assertFalse(is_placeholder("pending", PLACEHOLDERS_PLANNING, trim=" .", empty=False))
        self.assertTrue(is_placeholder("TBD.", PLACEHOLDERS_PLANNING, trim=" .", empty=False))
        self.assertTrue(is_placeholder(" Unassigned ", PLACEHOLDERS_ACTIVE_OWNER, trim=None))
        self.assertFalse(is_placeholder("unassigned.", PLACEHOLDERS_ACTIVE_OWNER, trim=None))
        self.assertFalse(is_placeholder("   ", PLACEHOLDERS_PLANNING, trim=" .", empty=False))


class GitRecordTests(unittest.TestCase):
    def test_working_tree_read_uses_utf8_and_keeps_missing_file_error(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            (root / "docs/source.md").write_text("café\n", encoding="utf-8")
            self.assertEqual(read_text(root, Path("docs/source.md")), "café\n")
            with self.assertRaises(FileNotFoundError):
                read_text(root, Path("missing.md"))

    def test_git_show_has_required_and_optional_failure_policies(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "PM-1 test"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "pm1-test@example.invalid"], cwd=root, check=True)
            (root / "record.md").write_text("first\n", encoding="utf-8")
            subprocess.run(["git", "add", "record.md"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)
            revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
            self.assertEqual(git_show(root, revision, "record.md"), "first\n")
            self.assertIsNone(git_show(root, revision, "absent.md", missing="none"))
            with self.assertRaisesRegex(ValueError, "does not exist"):
                git_show(root, revision, "absent.md")
            self.assertEqual(git_result(root, "status", "--short").returncode, 0)

    def test_git_output_raises_check_output_style_error(self):
        failure = subprocess.CalledProcessError(128, ["git", "rev-parse", "HEAD"])
        with patch("records.subprocess.check_output", side_effect=failure):
            with self.assertRaises(subprocess.CalledProcessError):
                git_output(Path("."), "rev-parse", "HEAD")


if __name__ == "__main__":
    unittest.main()


class ProjectRecordTests(unittest.TestCase):
    """Project rows retain the legacy seven-cell shape for existing consumers."""
    FIELDS = ("Project", "Goal", "Status", "Owner", "Estimate", "Waiting on")

    @staticmethod
    def plan(**changes):
        values = dict(zip(ProjectRecordTests.FIELDS,
                          ("Catalog name", "Build **one** thing", "queued", "Ada", "TBD", "—")))
        values.update(changes)
        return "# A different title\n\n" + "\n\n".join(
            f"**{key}:** {value}" for key, value in values.items()) + "\n\n"

    @staticmethod
    def write(root, folder, text):
        target = root / "plans" / folder / "plan.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    @staticmethod
    def git(root, *args):
        return subprocess.check_output(["git", *args], cwd=root, text=True).strip()

    def test_six_fields_preserve_values_and_ignore_body_fields(self):
        import records
        self.assertEqual(records.PROJECT_FIELDS, self.FIELDS)
        text = self.plan() + "## Design\n**Goal:** Body goal\n**Status:** done\n"
        self.assertEqual(records.project_fields(text), dict(zip(self.FIELDS,
                         ("Catalog name", "Build **one** thing", "queued", "Ada", "TBD", "—"))))

    def test_each_missing_field_names_the_field_and_reason(self):
        import records
        for field in self.FIELDS:
            lines = self.plan().splitlines()
            text = "\n".join(line for line in lines if not line.startswith(f"**{field}:**"))
            text += f"\n## Body\n**{field}:** Not a header\n"
            with self.subTest(field=field):
                pattern = rf"(?is)(?=.*{re.escape(field)})(?=.*missing)"
                with self.assertRaisesRegex(ValueError, pattern):
                    records.project_fields(text)

    def test_each_duplicate_field_is_refused_even_when_values_match(self):
        import records
        for field in self.FIELDS:
            original = next(line for line in self.plan().splitlines() if line.startswith(f"**{field}:**"))
            with self.subTest(field=field):
                pattern = rf"(?is)(?=.*{re.escape(field)})(?=.*duplicat)"
                with self.assertRaisesRegex(ValueError, pattern):
                    records.project_fields(self.plan() + original + "\n")

    def test_empty_field_cannot_swallow_the_next_paragraph(self):
        import records
        for field in self.FIELDS:
            for whitespace in ("", " \t "):
                with self.subTest(field=field, whitespace=whitespace):
                    pattern = rf"(?is)(?=.*{re.escape(field)})(?=.*empty)"
                    with self.assertRaisesRegex(ValueError, pattern):
                        records.project_fields(self.plan(**{field: whitespace}))

    def test_pipe_in_any_field_is_malformed(self):
        import records
        for field in self.FIELDS:
            with self.subTest(field=field):
                pattern = rf"(?is)(?=.*{re.escape(field)})(?=.*malformed)"
                with self.assertRaisesRegex(ValueError, pattern):
                    records.project_fields(self.plan(**{field: "left | right"}))

    def test_priority_is_only_the_order_section_and_keeps_duplicates_for_validation(self):
        import records
        text = "# Priority\n- 99-ignore\n\n## Order\n\n- 02-beta\n- 01-alpha\n- 02-beta\n\n## Notes\n- 98-ignore\n"
        self.assertEqual(records.priority_order(text), ["02-beta", "01-alpha", "02-beta"])
        self.assertEqual(records.priority_order(None), [])
        self.assertEqual(records.priority_order("# Priority\n"), [])

    def test_projects_partition_open_and_terminal_then_use_priority_and_folder_order(self):
        import records
        from check_docs import PLAN_LINK
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for folder, status in (("01-alpha", "queued"), ("02-beta", "paused"),
                                   ("03-gamma", "active"), ("04-delta", "blocked"),
                                   ("05-epsilon", "done"), ("06-zeta", "cancelled"),
                                   ("07-eta", "done"), ("100-later", "queued")):
                self.write(root, folder, self.plan(Project=folder, Status=status))
            self.write(root, "not-a-plan", self.plan())
            (root / "plans/08-no-pack").mkdir()
            (root / "plans/priority.md").write_text(
                "## Order\n- 06-zeta\n- 02-beta\n- 05-epsilon\n- 04-delta\n", encoding="utf-8")
            rows = records.projects(root)
            folders = [PLAN_LINK.fullmatch(row[6]).group(1).removesuffix("/plan.md") for row in rows]
            self.assertEqual(folders, ["02-beta", "04-delta", "01-alpha", "03-gamma", "100-later",
                                       "06-zeta", "05-epsilon", "07-eta"])
            self.assertEqual(rows[0], ["02-beta", "Build **one** thing", "paused", "Ada", "TBD", "—",
                                       "[Plan 02](02-beta/plan.md)"])
            (root / "plans/priority.md").unlink()
            rows = records.projects(root)
            self.assertEqual([row[0] for row in rows], ["01-alpha", "02-beta", "03-gamma", "04-delta",
                                                        "100-later", "05-epsilon", "06-zeta", "07-eta"])

    def test_revision_reads_git_blobs_and_priority_instead_of_working_tree(self):
        import records
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.git(root, "init", "-q")
            self.git(root, "config", "user.name", "Contract test")
            self.git(root, "config", "user.email", "contract@example.invalid")
            self.write(root, "01-alpha", self.plan(Project="Old alpha", Status="active"))
            self.write(root, "02-beta", self.plan(Project="Old beta"))
            (root / "plans/priority.md").write_text("## Order\n- 02-beta\n- 01-alpha\n", encoding="utf-8")
            self.git(root, "add", ".")
            self.git(root, "commit", "-qm", "record base")
            revision = self.git(root, "rev-parse", "HEAD")
            self.write(root, "01-alpha", self.plan(Project="New alpha", Status="done"))
            (root / "plans/02-beta/plan.md").unlink()
            self.write(root, "03-gamma", self.plan(Project="New gamma"))
            (root / "plans/priority.md").write_text("## Order\n- 03-gamma\n", encoding="utf-8")
            self.assertEqual([row[0] for row in records.projects(root, revision)], ["Old beta", "Old alpha"])
            self.assertEqual([row[0] for row in records.projects(root)], ["New gamma", "New alpha"])
