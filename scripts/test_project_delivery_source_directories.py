"""Pre-RS1 fail-closed checks for canonical source-directory symlink aliases.

The authored-file containment guard cannot inspect an empty outside directory.
A symlinked source area outside the selected checkout must be refused even
before that source area contains any Markdown files. In-tree aliases remain legal.
"""
import tempfile
import unittest
from pathlib import Path

from project_delivery import load_delivery
from relationships import RelationshipError


class CanonicalSourceDirectoryTests(unittest.TestCase):
    def setUp(self):
        inside = tempfile.TemporaryDirectory()
        outside = tempfile.TemporaryDirectory()
        self.addCleanup(inside.cleanup)
        self.addCleanup(outside.cleanup)
        self.root = Path(inside.name)
        self.external = Path(outside.name)

    def outside_directory(self, relative):
        link = self.root / relative
        link.parent.mkdir(parents=True, exist_ok=True)
        target = self.external / relative.replace("/", "-")
        target.mkdir(parents=True, exist_ok=True)
        link.symlink_to(target, target_is_directory=True)

    def assert_outside_source_refused(self, relative):
        self.outside_directory(relative)
        with self.assertRaisesRegex(RelationshipError, "outside delivery root") as failure:
            load_delivery(self.root)
        self.assertIn(relative, str(failure.exception))

    def test_external_empty_vision_root_is_not_canonical(self):
        self.assert_outside_source_refused("vision")

    def test_external_empty_plans_root_is_not_canonical(self):
        self.assert_outside_source_refused("plans")

    def test_external_empty_releases_root_is_not_canonical(self):
        self.assert_outside_source_refused("releases")

    def test_external_empty_pillar_area_is_not_canonical(self):
        self.assert_outside_source_refused("vision/pillars")

    def test_external_empty_principle_area_is_not_canonical(self):
        self.assert_outside_source_refused("vision/principles")

    def test_external_empty_gap_area_is_not_canonical(self):
        self.assert_outside_source_refused("vision/gaps")

    def test_external_source_area_refuses_even_with_valid_partial_area(self):
        (self.root / "plans").mkdir()
        self.assert_outside_source_refused("vision")

    def test_dangling_source_area_is_not_silently_ignored(self):
        (self.root / "plans").mkdir()
        (self.root / "releases").symlink_to(
            self.external / "missing", target_is_directory=True
        )
        with self.assertRaisesRegex(RelationshipError, "source directory"):
            load_delivery(self.root)

    def test_internal_source_directory_alias_preserves_partial_tree(self):
        target = self.root / "source-alias" / "plans"
        target.mkdir(parents=True)
        (self.root / "plans").symlink_to(target, target_is_directory=True)
        graph = load_delivery(self.root)
        self.assertEqual(graph.records, frozenset())
        self.assertEqual(graph.relationships, ())


if __name__ == "__main__":
    unittest.main()
