"""Reusable document-structure primitives used by workstream and project-pack checks."""
import unittest

from document_structure import frontmatter, headings, ordered_bold_fields, ordered_heading_error, section


class DocumentStructureTests(unittest.TestCase):
    def test_frontmatter_parses_single_line_fields(self):
        data, body = frontmatter("---\nname: astrid-dev-demo\ndescription: Do one thing.\n---\n\n# Demo\n")
        self.assertEqual(data, {"name": "astrid-dev-demo", "description": "Do one thing."})
        self.assertTrue(body.startswith("\n# Demo"))
        for invalid, pattern in (
            ("# No frontmatter\n", "missing frontmatter"),
            ("---\nname: example\n", "unclosed frontmatter"),
            ("---\nname: first\nname: second\n---\n", "duplicate frontmatter"),
            ("---\nname:\n---\n", "single-line"),
        ):
            with self.subTest(invalid=invalid):
                with self.assertRaisesRegex(ValueError, pattern):
                    frontmatter(invalid)

    def test_sections_and_order_can_be_reused_without_domain_rules(self):
        text = "# Demo\n\n## Outcome\nProof.\n\n## Details\nMore.\n\n## Completion\nDone.\n"
        self.assertEqual(headings(text), ["Outcome", "Details", "Completion"])
        self.assertEqual(section(text, "Outcome"), "Proof.")
        self.assertEqual(ordered_heading_error(headings(text), ["Outcome", "Completion"]), None)
        self.assertIn("out of order", ordered_heading_error(headings(text), ["Completion", "Outcome"]))
        self.assertIn("missing heading", ordered_heading_error(headings(text), ["Inputs"]))
        with self.assertRaisesRegex(ValueError, "exactly one"):
            section(text + "\n## Outcome\nMore\n", "Outcome")

    def test_contract_field_order_duplicate_and_substance(self):
        labels = ("Outcome", "Inputs")
        block = "**Outcome:** An accepted outcome with proof.\n**Inputs:** An approved brief and source.\n\nFurther details can follow."
        parsed = ordered_bold_fields(block, labels)
        self.assertEqual(tuple(parsed), labels)
        self.assertIn("accepted outcome", parsed["Outcome"])
        for invalid, pattern in (
            (block.replace("**Outcome:**", "**Inputs:**"), "duplicate contract field"),
            (block.replace("**Outcome:** An accepted outcome with proof.\n", ""), "contract fields must be"),
            (block.replace("**Inputs:** An approved brief and source.", "**Inputs:** TODO"), "substantive"),
            (block.replace("**Inputs:** An approved brief and source.", "Inputs: An approved brief and source."), "single-line"),
        ):
            with self.subTest(invalid=invalid):
                with self.assertRaisesRegex(ValueError, pattern):
                    ordered_bold_fields(invalid, labels)


if __name__ == "__main__":
    unittest.main()
