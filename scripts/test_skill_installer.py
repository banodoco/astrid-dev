"""Skill layout installs with stable names from grouped source folders."""
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SkillInstallerTests(unittest.TestCase):
    def test_grouped_skills_install_flat_with_original_names(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / "skills"
            dest.mkdir()
            subprocess.run(["bash", str(ROOT / "sync.sh"), "--destination", str(dest)],
                           cwd=ROOT, check=True, capture_output=True, text=True)
            expected = {
                "astrid-dev": "astrid-dev",
                "shared": "shared",
                "astrid-dev-worker": "roles/astrid-dev-worker",
                "astrid-dev-lead": "roles/astrid-dev-lead",
                "astrid-dev-orchestrate": "roles/astrid-dev-orchestrate",
                "astrid-dev-manage": "roles/astrid-dev-manage",
                "astrid-dev-plan": "shared/workstreams/astrid-dev-plan",
                "astrid-dev-iterate": "shared/workstreams/astrid-dev-iterate",
                "astrid-dev-green": "shared/workstreams/astrid-dev-green",
                "astrid-dev-gpu-validate": "shared/workstreams/astrid-dev-gpu-validate",
                "astrid-dev-bugfix": "shared/workstreams/astrid-dev-bugfix",
                "astrid-dev-gap": "shared/workstreams/astrid-dev-gap",
                "astrid-dev-merge": "shared/workstreams/astrid-dev-merge",
                "astrid-dev-release": "shared/workstreams/astrid-dev-release",
                "astrid-dev-improve": "shared/workstreams/astrid-dev-improve",
            }
            self.assertEqual({p.name for p in dest.iterdir()}, set(expected))
            for name, relative in expected.items():
                with self.subTest(skill=name):
                    link = dest / name
                    self.assertTrue(link.is_symlink())
                    self.assertEqual(link.resolve(), (ROOT / "skills" / relative).resolve())
                    self.assertTrue(link.is_dir())
                    if name != "shared":
                        self.assertTrue((link / "SKILL.md").is_file())
                    else:
                        self.assertFalse((link / "SKILL.md").exists())


    def test_old_owned_install_links_are_retargeted_without_touching_foreign_links(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / "skills"
            dest.mkdir()
            for name, old in (
                ("astrid-dev-plan", "roles/astrid-dev-plan"),
                ("astrid-dev-iterate", "capabilities/astrid-dev-iterate"),
            ):
                (dest / name).symlink_to(ROOT / "skills" / old, target_is_directory=True)
            run = subprocess.run(["bash", str(ROOT / "sync.sh"), "--destination", str(dest)],
                                 cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            for name in ("astrid-dev-plan", "astrid-dev-iterate"):
                self.assertEqual((dest / name).resolve(),
                                 (ROOT / "skills/shared/workstreams" / name).resolve())
                self.assertEqual((dest / name).readlink(),
                                 ROOT / "skills/shared/workstreams" / name)
            self.assertIn("retargeted", run.stdout)

            alien = dest / "astrid-dev-release"
            alien.unlink()
            alien.symlink_to(dest / "another-repository", target_is_directory=True)
            run = subprocess.run(["bash", str(ROOT / "sync.sh"), "--destination", str(dest)],
                                 cwd=ROOT, capture_output=True, text=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn("foreign symlink", run.stderr)
            self.assertEqual(alien.readlink(), dest / "another-repository")


if __name__ == "__main__":
    unittest.main()
