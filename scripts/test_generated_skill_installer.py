"""Focused installation safety tests for generated skill packages."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

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


if __name__ == "__main__":
    unittest.main()
