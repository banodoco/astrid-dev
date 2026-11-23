"""Focused installation safety tests for generated skill packages."""
import errno
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from skill_builder import build_packages
from skill_installer import install_packages


ROLE = """---
description: Lead work within the granted authority.
skill: true
---

# Leader

## Responsibility
Own the task.

## Authority
Follow the owner's grant.

## Responsibilities
Check the proof.

## Handoff
Report the result.
"""


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        role = self.root / "agent/roles/leader.md"
        role.parent.mkdir(parents=True)
        role.write_text(ROLE, encoding="utf-8")
        self.dest = self.root / "target/skills"
        self.dest.mkdir(parents=True)
        build_packages(self.root)

    def test_dry_run_is_inert_and_actual_install_is_idempotent(self):
        self.assertTrue(any("would-link" in x for x in
                            install_packages(self.root, [self.dest], dry_run=True)))
        self.assertEqual(list(self.dest.iterdir()), [])
        self.assertTrue(any("linked" in x for x in
                            install_packages(self.root, [self.dest])))
        link = self.dest / "astrid-dev-leader"
        self.assertTrue(link.is_symlink())
        self.assertTrue((link / "SKILL.md").is_file())
        self.assertTrue(any("already-linked" in x for x in
                            install_packages(self.root, [self.dest])))

    def test_retire_only_owned_symlinks(self):
        old = self.dest / "astrid-dev-old"
        old.symlink_to(self.root / "skills" / "roles" / "astrid-dev-old",
                       target_is_directory=True)
        foreign = self.dest / "elsewhere"
        foreign.symlink_to(self.root / "unrelated", target_is_directory=True)
        install_packages(self.root, [self.dest])
        self.assertFalse(old.is_symlink())
        self.assertTrue(foreign.is_symlink())

    def test_foreign_file_and_symlink_are_never_overwritten(self):
        file = self.dest / "astrid-dev-leader"
        file.write_text("foreign", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "foreign installation entry"):
            install_packages(self.root, [self.dest])
        self.assertEqual(file.read_text(), "foreign")
        file.unlink()
        file.symlink_to(self.root / "another-tool")
        with self.assertRaisesRegex(ValueError, "foreign symlink"):
            install_packages(self.root, [self.dest])
        self.assertTrue(file.is_symlink())

    def test_foreign_desired_entry_does_not_retire_existing_owned_link(self):
        old = self.dest / "astrid-dev-old"
        old.symlink_to(self.root / "skills/roles/astrid-dev-old")
        conflict = self.dest / "astrid-dev-leader"
        conflict.write_text("foreign", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "foreign installation entry"):
            install_packages(self.root, [self.dest])
        self.assertTrue(old.is_symlink())
        self.assertEqual(conflict.read_text(), "foreign")

    def test_later_destination_foreign_collision_preserves_earlier_destinations(self):
        old = self.dest / "astrid-dev-old"
        old.symlink_to(self.root / "skills/roles/astrid-dev-old")
        second = self.root / "second/skills"
        second.mkdir(parents=True)
        conflict = second / "astrid-dev-leader"
        conflict.write_text("foreign", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "foreign installation entry"):
            install_packages(self.root, [self.dest, second])
        self.assertTrue(old.is_symlink())
        self.assertFalse((self.dest / "astrid-dev-leader").exists())
        self.assertEqual(conflict.read_text(), "foreign")

    def test_missing_destination_is_refused(self):
        with self.assertRaisesRegex(ValueError, "must already be a real directory"):
            install_packages(self.root, [self.root / "not-created"])

    def test_old_owned_install_retargets_to_generated_package(self):
        old_dir = self.root / "skills/roles/astrid-dev-leader"
        old_dir.mkdir(parents=True)
        link = self.dest / "astrid-dev-leader"
        link.symlink_to(old_dir, target_is_directory=True)
        self.assertTrue(any("retargeted" in x for x in
                            install_packages(self.root, [self.dest])))
        self.assertEqual(link.resolve(),
                         (self.root / ".generated/skills/astrid-dev-leader").resolve())

    def test_flag_removed_retires_owned_install_after_rebuild(self):
        install_packages(self.root, [self.dest])
        role = self.root / "agent/roles/leader.md"
        role.write_text(ROLE.replace("skill: true\n", ""), encoding="utf-8")
        build_packages(self.root)
        self.assertTrue(any("retired" in x for x in
                            install_packages(self.root, [self.dest])))
        self.assertFalse((self.dest / "astrid-dev-leader").is_symlink())


    def test_failed_symlink_staging_preserves_existing_owned_link(self):
        old = self.root / "skills/roles/astrid-dev-leader"
        old.mkdir(parents=True)
        (old / "SKILL.md").write_text("legacy instruction\n", encoding="utf-8")
        link = self.dest / "astrid-dev-leader"
        link.symlink_to(old, target_is_directory=True)
        original = link.readlink()
        with patch.object(Path, "symlink_to", side_effect=OSError(errno.EPERM, "injected")):
            with self.assertRaisesRegex(ValueError, "previous owned link was preserved"):
                install_packages(self.root, [self.dest])
        self.assertEqual(link.readlink(), original)
        self.assertEqual((link / "SKILL.md").read_text(encoding="utf-8"), "legacy instruction\n")
        self.assertEqual(list(self.dest.iterdir()), [link])
        # After a transient permission failure, a normal retry is still possible.
        result = install_packages(self.root, [self.dest])
        self.assertTrue(any("retargeted" in action for action in result))
        self.assertEqual(link.resolve(), (self.root / ".generated/skills/astrid-dev-leader").resolve())

    def test_failed_atomic_retarget_preserves_original_and_cleans_staging(self):
        old = self.root / "skills/roles/astrid-dev-leader"
        old.mkdir(parents=True)
        (old / "SKILL.md").write_text("old work\n", encoding="utf-8")
        link = self.dest / "astrid-dev-leader"
        link.symlink_to(old, target_is_directory=True)
        raw = link.readlink()
        with patch("skill_installer.os.replace", side_effect=OSError(errno.EIO, "injected")):
            with self.assertRaisesRegex(ValueError, "previous owned link was preserved"):
                install_packages(self.root, [self.dest])
        self.assertEqual(link.readlink(), raw)
        self.assertEqual((link / "SKILL.md").read_text(encoding="utf-8"), "old work\n")
        self.assertEqual({p.name for p in self.dest.iterdir()}, {"astrid-dev-leader"})

    def test_failed_new_package_link_keeps_retirement_candidates_intact(self):
        old_dir = self.root / "skills/astrid-dev"
        old_dir.mkdir(parents=True)
        (old_dir / "SKILL.md").write_text("old entry\n", encoding="utf-8")
        obsolete = self.dest / "astrid-dev"
        obsolete.symlink_to(old_dir, target_is_directory=True)
        with patch.object(Path, "symlink_to", side_effect=OSError(errno.EPERM, "injected")):
            with self.assertRaisesRegex(ValueError, "could not create skill directory symlink"):
                install_packages(self.root, [self.dest])
        self.assertEqual(obsolete.resolve(), old_dir.resolve())
        self.assertEqual((obsolete / "SKILL.md").read_text(encoding="utf-8"), "old entry\n")
        self.assertFalse((self.dest / "astrid-dev-leader").exists())
        self.assertEqual({p.name for p in self.dest.iterdir()}, {"astrid-dev"})
        # Successful retry publishes the desired skill and then retires old entry.
        install_packages(self.root, [self.dest])
        self.assertFalse(obsolete.is_symlink())
        self.assertTrue((self.dest / "astrid-dev-leader/SKILL.md").is_file())

if __name__ == "__main__":
    unittest.main()
