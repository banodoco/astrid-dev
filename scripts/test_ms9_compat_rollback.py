"""Disposable rollback policy tests; do not mutate real skill destinations."""
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from ms9_compat_rollback import restore_legacy_links, snapshot_links


class RollbackPreparationTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        self.legacy_root = self.repo / "skills" / "astrid-dev"
        self.new_root = self.repo / ".generated/skills/astrid-dev-manager"
        self.legacy_root.mkdir(parents=True)
        self.new_root.mkdir(parents=True)
        self.destination = Path(self.temp.name) / "install"
        self.destination.mkdir()
        self.legacy = {"astrid-dev": str(self.legacy_root)}
        self.generated = {"astrid-dev-manager": str(self.new_root)}
        (self.destination / "astrid-dev-manager").symlink_to(
            self.new_root, target_is_directory=True)

    def test_snapshot_and_round_trip_preserve_foreign_entry(self):
        foreign = self.destination / "other-person"
        foreign.write_text("untouched", encoding="utf-8")
        self.assertEqual(snapshot_links(self.destination), self.generated)
        actions = restore_legacy_links(
            self.destination, self.repo, self.legacy, self.generated)
        self.assertEqual(len(actions), 2)
        self.assertEqual(snapshot_links(self.destination), self.legacy)
        self.assertEqual(foreign.read_text(encoding="utf-8"), "untouched")

    def test_existing_foreign_file_blocks_every_mutation(self):
        collision = self.destination / "astrid-dev"
        collision.write_text("foreign", encoding="utf-8")
        before = snapshot_links(self.destination)
        with self.assertRaisesRegex(ValueError, "restoration collision"):
            restore_legacy_links(self.destination, self.repo, self.legacy, self.generated)
        self.assertEqual(snapshot_links(self.destination), before)
        self.assertEqual(collision.read_text(encoding="utf-8"), "foreign")

    def test_drifted_symlink_is_never_retreated_as_owned(self):
        foreign_dir = Path(self.temp.name) / "foreign-repository"
        foreign_dir.mkdir()
        entry = self.destination / "astrid-dev-manager"
        entry.unlink()
        entry.symlink_to(foreign_dir, target_is_directory=True)
        before = snapshot_links(self.destination)
        with self.assertRaisesRegex(ValueError, "installed link changed"):
            restore_legacy_links(self.destination, self.repo, self.legacy, self.generated)
        self.assertEqual(snapshot_links(self.destination), before)
        self.assertFalse((self.destination / "astrid-dev").exists())

    def test_traversal_target_is_not_accepted_as_legacy_owned(self):
        bad = {"astrid-dev": str(Path(self.temp.name) / "outside")}
        Path(bad["astrid-dev"]).mkdir()
        before = snapshot_links(self.destination)
        with self.assertRaisesRegex(ValueError, "outside authored checkout"):
            restore_legacy_links(self.destination, self.repo, bad, self.generated)
        self.assertEqual(snapshot_links(self.destination), before)

    def test_missing_legacy_target_does_not_erase_generated_links(self):
        self.legacy_root.rmdir()
        before = snapshot_links(self.destination)
        with self.assertRaisesRegex(ValueError, "outside authored checkout"):
            restore_legacy_links(self.destination, self.repo, self.legacy, self.generated)
        self.assertEqual(snapshot_links(self.destination), before)


if __name__ == "__main__":
    unittest.main()
