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
