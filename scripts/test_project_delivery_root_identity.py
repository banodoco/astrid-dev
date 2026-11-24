"""F72.4 regression probes for existing directories without Astrid source roots.

An unrelated existing folder must not masquerade as a validated empty
Astrid Dev delivery graph. This does not add required release membership or
change the meaning of absent issue/release edges in a real source tree.
"""
import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from project_delivery import load_delivery, main
from relationships import RelationshipError


class DeliveryRootIdentityTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def test_existing_empty_directory_is_not_a_delivery_root(self):
        with self.assertRaisesRegex(RelationshipError, "canonical.*directories"):
            load_delivery(self.root)

    def test_unrelated_markdown_does_not_make_a_delivery_root(self):
        (self.root / "notes.md").write_text("# Notes\n", encoding="utf-8")
        with self.assertRaisesRegex(RelationshipError, "canonical.*directories"):
            load_delivery(self.root)

    def test_cli_check_refuses_existing_unrelated_directory(self):
        (self.root / "notes.md").write_text("# Notes\n", encoding="utf-8")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = main(["check", "--root", str(self.root)])
        self.assertEqual(result, 1)
        self.assertIn("ERROR project delivery:", output.getvalue())
        self.assertIn("canonical", output.getvalue())

    def test_partial_canonical_tree_still_allows_unknown_relationships(self):
        # A real source area may have no authored records yet; absent
        # release links must stay unknown, not become a validation failure.
        (self.root / "plans").mkdir()
        graph = load_delivery(self.root)
        self.assertEqual(graph.records, frozenset())
        self.assertEqual(graph.relationships, ())


if __name__ == "__main__":
    unittest.main()
