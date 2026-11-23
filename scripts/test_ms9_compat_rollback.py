"""Disposable rollback policy tests; do not mutate real skill destinations."""
import os
import hashlib
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
        (self.legacy_root / "SKILL.md").write_text("Legacy fixture\n", encoding="utf-8")
        (self.new_root / "SKILL.md").write_text("Generated fixture\n", encoding="utf-8")
        self.legacy_hashes = {
            "astrid-dev": hashlib.sha256(
                (self.legacy_root / "SKILL.md").read_bytes()).hexdigest()
        }
        self.generated_hashes = {
            "astrid-dev-manager": hashlib.sha256(
                (self.new_root / "SKILL.md").read_bytes()).hexdigest()
        }
        self.destination = Path(self.temp.name) / "install"
        self.destination.mkdir()
        self.legacy = {"astrid-dev": str(self.legacy_root)}
        self.generated = {"astrid-dev-manager": str(self.new_root)}
        (self.destination / "astrid-dev-manager").symlink_to(
            self.new_root, target_is_directory=True)

    def restore(self, destination, checkout, legacy, generated):
        return restore_legacy_links(
            destination, checkout, legacy, generated,
            expected_legacy_hashes=self.legacy_hashes,
            expected_generated_hashes=self.generated_hashes)

    def test_snapshot_and_round_trip_preserve_foreign_entry(self):
        foreign = self.destination / "other-person"
        foreign.write_text("untouched", encoding="utf-8")
        self.assertEqual(snapshot_links(self.destination), self.generated)
        actions = self.restore(
            self.destination, self.repo, self.legacy, self.generated)
        self.assertEqual(len(actions), 2)
        self.assertEqual(snapshot_links(self.destination), self.legacy)
        self.assertEqual(foreign.read_text(encoding="utf-8"), "untouched")

    def test_existing_foreign_file_blocks_every_mutation(self):
        collision = self.destination / "astrid-dev"
        collision.write_text("foreign", encoding="utf-8")
        before = snapshot_links(self.destination)
        with self.assertRaisesRegex(ValueError, "restoration collision"):
            self.restore(self.destination, self.repo, self.legacy, self.generated)
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
            self.restore(self.destination, self.repo, self.legacy, self.generated)
        self.assertEqual(snapshot_links(self.destination), before)
        self.assertFalse((self.destination / "astrid-dev").exists())

    def test_traversal_target_is_not_accepted_as_legacy_owned(self):
        bad = {"astrid-dev": str(Path(self.temp.name) / "outside")}
        Path(bad["astrid-dev"]).mkdir()
        before = snapshot_links(self.destination)
        with self.assertRaisesRegex(ValueError, "outside authored checkout"):
            self.restore(self.destination, self.repo, bad, self.generated)
        self.assertEqual(snapshot_links(self.destination), before)

    def test_missing_legacy_target_does_not_erase_generated_links(self):
        (self.legacy_root / "SKILL.md").unlink()
        self.legacy_root.rmdir()
        before = snapshot_links(self.destination)
        with self.assertRaisesRegex(ValueError, "outside authored checkout"):
            self.restore(self.destination, self.repo, self.legacy, self.generated)
        self.assertEqual(snapshot_links(self.destination), before)


    def test_unrecorded_owned_generated_link_fails_before_any_mutation(self):
        extra = self.repo / ".generated/skills/astrid-dev-extra"
        extra.mkdir()
        (self.destination / "astrid-dev-extra").symlink_to(
            extra, target_is_directory=True)
        before = snapshot_links(self.destination)
        with self.assertRaisesRegex(ValueError, "unrecorded generated link"):
            self.restore(
                self.destination, self.repo, self.legacy, self.generated)
        self.assertEqual(snapshot_links(self.destination), before)
        self.assertFalse((self.destination / "astrid-dev").exists())

    def test_unknown_foreign_symlink_is_preserved_during_restore(self):
        foreign = Path(self.temp.name) / "unrelated-package"
        foreign.mkdir()
        (self.destination / "another-person").symlink_to(
            foreign, target_is_directory=True)
        before = os.readlink(self.destination / "another-person")
        self.restore(self.destination, self.repo, self.legacy, self.generated)
        self.assertEqual(snapshot_links(self.destination)["another-person"], before)
        self.assertTrue((self.destination / "astrid-dev").is_symlink())

    def test_empty_rollback_snapshots_fail_closed(self):
        before = snapshot_links(self.destination)
        for old, new in (({}, self.generated), (self.legacy, {}), ({}, {})):
            with self.subTest(old=old, new=new):
                with self.assertRaisesRegex(ValueError, "nonempty"):
                    self.restore(self.destination, self.repo, old, new)
                self.assertEqual(snapshot_links(self.destination), before)

    def test_symlinked_destination_is_refused(self):
        alias = Path(self.temp.name) / "symlinked-install"
        alias.symlink_to(self.destination, target_is_directory=True)
        before = snapshot_links(self.destination)
        with self.assertRaisesRegex(ValueError, "real directory"):
            self.restore(alias, self.repo, self.legacy, self.generated)
        self.assertEqual(snapshot_links(self.destination), before)

    def test_legacy_manifest_content_drift_refused_before_mutation(self):
        (self.legacy_root / "SKILL.md").write_text("ALTERED\n", encoding="utf-8")
        before = snapshot_links(self.destination)
        with self.assertRaisesRegex(ValueError, "legacy manifest content changed"):
            self.restore(self.destination, self.repo, self.legacy, self.generated)
        self.assertEqual(snapshot_links(self.destination), before)

    def test_generated_manifest_content_drift_refused_before_mutation(self):
        (self.new_root / "SKILL.md").write_text("ALTERED\n", encoding="utf-8")
        before = snapshot_links(self.destination)
        with self.assertRaisesRegex(ValueError, "generated manifest content changed"):
            self.restore(self.destination, self.repo, self.legacy, self.generated)
        self.assertEqual(snapshot_links(self.destination), before)

    def test_missing_legacy_manifest_refuses_before_mutation(self):
        (self.legacy_root / "SKILL.md").unlink()
        before = snapshot_links(self.destination)
        with self.assertRaisesRegex(ValueError, "legacy manifest missing"):
            self.restore(self.destination, self.repo, self.legacy, self.generated)
        self.assertEqual(snapshot_links(self.destination), before)

    def test_incomplete_content_hash_snapshots_fail_closed(self):
        before = snapshot_links(self.destination)
        for old_hashes, new_hashes in (
            ({}, self.generated_hashes), (self.legacy_hashes, {}),
        ):
            with self.subTest(old_hashes=old_hashes, new_hashes=new_hashes):
                with self.assertRaisesRegex(ValueError, "manifest hash snapshot incomplete"):
                    restore_legacy_links(
                        self.destination, self.repo, self.legacy, self.generated,
                        expected_legacy_hashes=old_hashes,
                        expected_generated_hashes=new_hashes)
                self.assertEqual(snapshot_links(self.destination), before)

    def test_shared_reference_only_legacy_folder_has_no_skill_manifest(self):
        shared = self.repo / "skills/shared"
        shared.mkdir(parents=True)
        old = {**self.legacy, "shared": str(shared)}
        self.restore(self.destination, self.repo, old, self.generated)
        self.assertEqual(snapshot_links(self.destination), old)
        self.assertFalse((self.destination / "shared/SKILL.md").exists())

if __name__ == "__main__":
    unittest.main()
