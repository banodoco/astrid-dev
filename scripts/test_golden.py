"""Freeze legacy documentation and exporter verdicts for the PM-0 fixtures."""
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

import golden


def _status():
    result = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=golden.ROOT, check=True, capture_output=True, text=True)
    return [line for line in result.stdout.splitlines() if "__pycache__/" not in line]


class GoldenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # One sweep serves every test here: it is the slow part of the suite.
        cls.status_before = _status()
        cls.collected = golden.collect()
        cls.status_after = _status()

    def test_real_tree_and_fixtures_match_golden_output(self):
        expected = (golden.FIXTURES / "golden.txt").read_text(encoding="utf-8").splitlines()
        self.assertEqual(self.collected, expected)

    def test_collect_does_not_change_the_repository(self):
        self.assertEqual(self.status_after, self.status_before)

    def test_overlay_restores_every_path_it_touched(self):
        with tempfile.TemporaryDirectory(prefix="astrid-golden-overlay-") as directory:
            root = Path(directory)
            (root / "kept.md").write_text("original\n", encoding="utf-8")
            (root / "there").mkdir()
            with golden._overlay(root, {"kept.md": "changed\n", "new/deep/file.md": "x\n",
                                        "there/added.md": "y\n"}):
                self.assertEqual((root / "kept.md").read_text(encoding="utf-8"), "changed\n")
                self.assertTrue((root / "new/deep/file.md").is_file())
            self.assertEqual((root / "kept.md").read_text(encoding="utf-8"), "original\n")
            self.assertEqual(sorted(p.name for p in root.iterdir()), ["kept.md", "there"])
            self.assertEqual(list((root / "there").iterdir()), [])

    def test_golden_fixture_copy_excludes_generated_symlink_cycle(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory(prefix="golden-derived-cycle-") as tmp:
            root = Path(tmp)
            source = root / "source"
            (source / ".generated/skills/astrid-dev-start").mkdir(parents=True)
            (source / "skills").mkdir(parents=True)
            (source / "README.md").write_text("authored\n", encoding="utf-8")
            (source / "skills/legacy.md").symlink_to("../README.md")
            (source / ".generated/skills/astrid-dev-start/repo").symlink_to(
                source, target_is_directory=True
            )
            target = root / "copy"
            with patch.object(golden, "ROOT", source):
                golden._copy_tree(target)
            self.assertEqual((target / "README.md").read_text(encoding="utf-8"), "authored\n")
            self.assertTrue((target / "skills/legacy.md").is_symlink())
            self.assertFalse((target / ".generated").exists())

    def test_deleting_a_status_field_in_a_scratch_copy_fails_the_oracle(self):
        with tempfile.TemporaryDirectory(prefix="astrid-golden-negative-") as directory:
            root = Path(directory) / "repo"
            golden._copy_tree(root)
            plan = root / "plans/20-zero-to-first-image/plan.md"
            text = plan.read_text(encoding="utf-8")
            self.assertRegex(text, r"(?m)^\*\*Status:\*\*")
            plan.write_text(re.sub(r"(?m)^\*\*Status:\*\*[^\n]*\n", "", text, count=1),
                            encoding="utf-8")
            errors = golden._errors(root)
            self.assertTrue(any("plans/20-zero-to-first-image/plan.md:" in error
                                and "Status" in error and "missing" in error.lower()
                                for error in errors), errors)



if __name__ == "__main__":
    unittest.main()
