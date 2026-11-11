"""Freeze legacy documentation and exporter verdicts for the PM-0 fixtures."""
import re
import tempfile
import unittest
from pathlib import Path

import golden


class GoldenTests(unittest.TestCase):
    def test_real_tree_and_fixtures_match_golden_output(self):
        expected = (golden.FIXTURES / "golden.txt").read_text(encoding="utf-8").splitlines()
        self.assertEqual(golden.collect(), expected)

    def test_deleting_a_catalog_row_in_a_scratch_copy_fails_the_oracle(self):
        with tempfile.TemporaryDirectory(prefix="astrid-golden-negative-") as directory:
            root = Path(directory) / "repo"
            golden._copy_tree(root)
            catalog = root / "plans/index.md"
            text = catalog.read_text(encoding="utf-8")
            row = next(line for line in text.splitlines()
                       if line.startswith("|") and re.search(r"\[Plan \d+\]\(", line))
            catalog.write_text(text.replace(row + "\n", "", 1), encoding="utf-8")
            errors = golden._errors(root)
            self.assertTrue(any("plan folder absent from catalog" in error for error in errors), errors)



if __name__ == "__main__":
    unittest.main()
