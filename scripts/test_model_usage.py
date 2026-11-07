"""Model provenance is recorded during work, not invented during review."""
import tempfile
import unittest
from pathlib import Path
from model_usage import append_record, make_record, read_records, summarize


class ModelUseTests(unittest.TestCase):
    def test_live_append_and_summary(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            item = make_record("gpt-6", "openai", "implementation",
                               "task-1", "self-reported", "high")
            append_record(root, item)
            rows = read_records(root)
            self.assertEqual(len(rows), 1)
            self.assertIn("openai / gpt-6", summarize(rows))
            self.assertIn("self-reported", summarize(rows))
            self.assertIn("Not recorded", summarize([]))
            self.assertEqual((root / "model-usage.jsonl").read_text().count("\n"), 1)

    def test_verified_claim_requires_receipt(self):
        with self.assertRaisesRegex(ValueError, "requires a source"):
            make_record("model", "provider", "review", "task", "runtime-observed")
        self.assertEqual(make_record("model", "provider", "review", "task",
                                     "runtime-observed", receipt="run/actual.json")["basis"],
                         "runtime-observed")

    def test_unknown_is_not_guessed(self):
        self.assertEqual(make_record("unknown", "unknown", "research", "investigation",
                                     "self-reported")["model_id"], "unknown")
        with self.assertRaises(ValueError):
            make_record("", "p", "research", "task", "self-reported")

    def test_bad_source_is_reported(self):
        with tempfile.TemporaryDirectory() as t:
            (Path(t) / "model-usage.jsonl").write_text("nonsense\n")
            with self.assertRaisesRegex(ValueError, "malformed"):
                read_records(Path(t))


if __name__ == "__main__":
    unittest.main()
