"""Protect the shared authoring contract for all eight subject pages."""
import unittest

from check_docs import ROOT
from vision_subject import parse_subject, render_subject_markdown


SAMPLE = """# A subject

## Statement

Creative people should direct their own tools.

## Explanation

This is one short, coherent explanatory paragraph about how the creative intent drives the software. It leaves the distinct criteria to the following characteristics.

## Aspirations

### Agency

Artists should be able to control the result.

The creator makes consequential decisions and can check what the software has changed without losing understanding of the artistic work.

### Continuity

Work should remain editable across sessions.

Projects preserve the relevant resources, choices, revisions, and history so that the creator can return to a demanding task without starting again.

## References

See the broader vision.
"""


class SubjectStructureTests(unittest.TestCase):
    def test_all_eight_canonical_subjects_share_one_shape(self):
        files = sorted((ROOT / "vision/pillars").glob("*.md")) + sorted(
            (ROOT / "vision/principles").glob("*.md")
        )
        self.assertEqual(len(files), 8)
        for file in files:
            data = parse_subject(file.read_text(encoding="utf-8"), file.name)
            self.assertTrue(data["statement"].endswith("."))
            self.assertGreaterEqual(len(data["characteristics"]), 2)
            self.assertEqual(len({c["id"] for c in data["characteristics"]}),
                             len(data["characteristics"]))
            self.assertIn("## Aspirations", render_subject_markdown(data))

    def test_wrong_section_order_is_rejected(self):
        bad = SAMPLE.replace("## Statement", "## Overview")
        with self.assertRaisesRegex(ValueError, "sections"):
            parse_subject(bad, "test.md")

    def test_each_characteristic_needs_distinct_summary_and_explanation(self):
        bad = SAMPLE.replace("Artists should be able to control the result.\n\n", "")
        with self.assertRaisesRegex(ValueError, "summary sentence"):
            parse_subject(bad, "test.md")
        bad = SAMPLE.replace("## Aspirations", "## Aspirations\n\n### Empty\n\nOnly one sentence.\n")
        with self.assertRaisesRegex(ValueError, "summary sentence"):
            parse_subject(bad, "test.md")

    def test_one_sentence_opening_and_unique_ids(self):
        bad = SAMPLE.replace(
            "Creative people should direct their own tools.",
            "Creative people should direct their own tools. Also another sentence.",
        )
        with self.assertRaisesRegex(ValueError, "one complete"):
            parse_subject(bad, "test.md")
        bad = SAMPLE.replace("### Continuity", "### Agency")
        with self.assertRaisesRegex(ValueError, "unique"):
            parse_subject(bad, "test.md")

    def test_legacy_markdown_body_is_derived(self):
        data = parse_subject(SAMPLE, "test.md")
        markdown = render_subject_markdown(data)
        self.assertIn("## Aspirations", markdown)
        self.assertIn("### Agency", markdown)
        self.assertIn("## References", markdown)


    def test_lists_are_optional_paired_and_preserved_in_details_markdown(self):
        lists = "\n\n**We should:**\n\n- Keep consequential decisions visible to the creator.\n\n**We should never:**\n\n- Hide a consequential change from the creator."
        source = SAMPLE.replace("\n\n### Continuity", lists + "\n\n### Continuity")
        parsed = parse_subject(source, "test.md")
        self.assertIn(lists.strip(), parsed["characteristics"][0]["detailsMarkdown"])
        self.assertIn("**We should never:**", render_subject_markdown(parsed))

    def test_malformed_lists_are_rejected_without_counting_bullets_as_prose(self):
        prose = "The creator makes consequential decisions and can check what the software has changed without losing understanding of the artistic work."
        good = "\n\n**We should:**\n\n- Keep consequential decisions visible to the creator.\n\n**We should never:**\n\n- Hide a consequential change from the creator."
        cases = [
            good.split("**We should never:**")[0],
            good.replace("**We should:**", "**We should never:**", 1),
            good.replace("- Keep consequential decisions visible to the creator.", "\n".join(["- Keep consequential decisions visible to the creator."] * 6)),
            good.replace("- Keep consequential decisions visible to the creator.", "- Keep all decisions visible. Hide nothing from the creator."),
            good + "\n\nText after the second list is not a bullet.",
            good.replace("- Hide a consequential change from the creator.", ""),
        ]
        for bad in cases:
            with self.subTest(details=bad), self.assertRaises(ValueError):
                parse_subject(SAMPLE.replace(prose, prose + bad), "test.md")
        with self.assertRaisesRegex(ValueError, "15 words"):
            parse_subject(SAMPLE.replace(prose, "Too short." + good), "test.md")

    def test_old_heading_is_rejected_with_the_new_heading_in_the_error(self):
        with self.assertRaisesRegex(ValueError, "Aspirations"):
            parse_subject(SAMPLE.replace("## Aspirations", "## Characteristics"), "test.md")


if __name__ == "__main__":
    unittest.main()
