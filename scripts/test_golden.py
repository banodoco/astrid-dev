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
