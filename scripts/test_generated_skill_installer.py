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

    def test_cleanup_error_after_committed_retarget_reports_new_link(self):
        """The prior helper falsely said the old link was preserved on cleanup error."""
        old = self.root / "skills/roles/astrid-dev-leader"
        old.mkdir(parents=True)
        (old / "SKILL.md").write_text("old authority\n", encoding="utf-8")
        link = self.dest / "astrid-dev-leader"
        link.symlink_to(old, target_is_directory=True)
        import tempfile
        real_temp = tempfile.TemporaryDirectory

        class FailAfterCleanup:
            def __init__(self, *args, **kwargs):
                self.inner = real_temp(*args, **kwargs)

            def __enter__(self):
                return self.inner.__enter__()

            def __exit__(self, *args):
                self.inner.__exit__(*args)
                raise OSError(errno.EIO, "injected post-commit cleanup failure")

        with patch("skill_installer.tempfile.TemporaryDirectory", FailAfterCleanup):
            with self.assertRaisesRegex(ValueError, "new link is installed"):
                install_packages(self.root, [self.dest])
        self.assertEqual(
            link.resolve(), (self.root / ".generated/skills/astrid-dev-leader").resolve())
        self.assertNotEqual(link.resolve(), old.resolve())
        self.assertTrue((link / "SKILL.md").is_file())
        self.assertEqual({entry.name for entry in self.dest.iterdir()}, {"astrid-dev-leader"})
        self.assertTrue(any("already-linked" in x for x in
                            install_packages(self.root, [self.dest])))

    def test_late_retarget_failure_preserves_old_entrypoint_and_retry_converges(self):
        """A partial multi-package attempt must retain legacy start and recover cleanly."""
        old_start = self.root / "skills/astrid-dev"
        old_start.mkdir(parents=True)
        (old_start / "SKILL.md").write_text("original start\n", encoding="utf-8")
        (self.dest / "astrid-dev").symlink_to(old_start, target_is_directory=True)
        old_lead = self.root / "skills/roles/astrid-dev-leader"
        old_lead.mkdir(parents=True)
        (old_lead / "SKILL.md").write_text("original leader\n", encoding="utf-8")
        (self.dest / "astrid-dev-leader").symlink_to(old_lead, target_is_directory=True)
        (self.root / "agent/roles/worker.md").write_text(
            ROLE.replace("# Leader", "# Worker"), encoding="utf-8")
        build_packages(self.root)

        original_symlink = Path.symlink_to

        def fail_later_new_package(self, target, *args, **kwargs):
            if self.name == "astrid-dev-worker":
                raise OSError(errno.EIO, "injected later new-package failure")
            return original_symlink(self, target, *args, **kwargs)

        with patch.object(Path, "symlink_to", fail_later_new_package):
            with self.assertRaisesRegex(ValueError, "could not create skill directory symlink"):
                install_packages(self.root, [self.dest])
        self.assertEqual((self.dest / "astrid-dev").resolve(), old_start.resolve())
        # The earlier desired package was already retargeted: a real partial state.
        self.assertEqual(
            (self.dest / "astrid-dev-leader").resolve(),
            (self.root / ".generated/skills/astrid-dev-leader").resolve())
        self.assertTrue((self.dest / "astrid-dev").is_symlink())
        self.assertFalse((self.dest / "astrid-dev-worker").is_symlink())
        foreign = self.dest / "unrelated-user-file"
        foreign.write_text("never touch\n", encoding="utf-8")
        result = install_packages(self.root, [self.dest])
        self.assertTrue(any("linked" in x for x in result))
        self.assertTrue(any("retired" in x for x in result))
        self.assertFalse((self.dest / "astrid-dev").exists())
        self.assertTrue((self.dest / "astrid-dev-leader/SKILL.md").is_file())
        self.assertTrue((self.dest / "astrid-dev-worker/SKILL.md").is_file())
        self.assertEqual(foreign.read_text(encoding="utf-8"), "never touch\n")
        self.assertTrue(any("already-linked" in x for x in
                            install_packages(self.root, [self.dest])))

    def test_foreign_replacement_during_staging_blocks_atomic_retarget(self):
        """A foreign writer wins during staging; publication must not overwrite it."""
        original_package = self.root / "skills/roles/astrid-dev-leader"
        original_package.mkdir(parents=True)
        link = self.dest / "astrid-dev-leader"
        link.symlink_to(original_package, target_is_directory=True)
        foreign = self.root / "another-repository/skills/leader"
        foreign.mkdir(parents=True)
        (foreign / "SKILL.md").write_text("foreign instructions\n", encoding="utf-8")
        original_symlink = Path.symlink_to
        destination = self.dest

        def inject_during_staging(self, target, *args, **kwargs):
            result = original_symlink(self, target, *args, **kwargs)
            if self.name == "package" and self.parent.parent == destination:
                link.unlink()
                original_symlink(link, foreign, target_is_directory=True)
            return result

        with patch.object(Path, "symlink_to", inject_during_staging):
            with self.assertRaisesRegex(ValueError, "changed during staged retarget"):
                install_packages(self.root, [self.dest])
        self.assertEqual(link.resolve(), foreign.resolve())
        self.assertEqual((link / "SKILL.md").read_text(encoding="utf-8"),
                         "foreign instructions\n")
        self.assertEqual({p.name for p in self.dest.iterdir()}, {"astrid-dev-leader"})
        # No silent takeover on a normal follow-up either.
        with self.assertRaisesRegex(ValueError, "foreign symlink"):
            install_packages(self.root, [self.dest])
        self.assertEqual(link.resolve(), foreign.resolve())

    def test_second_destination_retarg_failure_is_partial_and_retryable(self):
        """A later destination fails; earlier install remains and retry converges."""
        first, second = self.dest, self.root / "second/skills"
        second.mkdir(parents=True)
        old = self.root / "skills/roles/astrid-dev-leader"
        old.mkdir(parents=True)
        (old / "SKILL.md").write_text("old leader\n", encoding="utf-8")
        previous = second / "astrid-dev-leader"
        previous.symlink_to(old, target_is_directory=True)
        original_symlink = Path.symlink_to

        def reject_second_stage(self, target, *args, **kwargs):
            if self.name == "package" and self.parent.parent == second:
                raise OSError(errno.EPERM, "injected second-destination error")
            return original_symlink(self, target, *args, **kwargs)

        with patch.object(Path, "symlink_to", reject_second_stage):
            with self.assertRaisesRegex(ValueError, "previous owned link was preserved"):
                install_packages(self.root, [first, second])
        self.assertTrue((first / "astrid-dev-leader/SKILL.md").is_file())
        self.assertEqual(previous.resolve(), old.resolve())
        self.assertEqual((previous / "SKILL.md").read_text(encoding="utf-8"),
                         "old leader\n")
        self.assertEqual({p.name for p in second.iterdir()}, {"astrid-dev-leader"})
        # The multi-destination call is deliberately not a transaction.
        result = install_packages(self.root, [first, second])
        self.assertTrue(any("already-linked" in x for x in result))
        self.assertTrue(any("retargeted" in x for x in result))
        self.assertEqual(previous.resolve(),
                         (self.root / ".generated/skills/astrid-dev-leader").resolve())

if __name__ == "__main__":
    unittest.main()
