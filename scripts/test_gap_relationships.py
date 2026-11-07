"""Focused tests for the primary/supporting gap relationship grammar."""
import unittest

from gap_relationships import parse_gap_relationships

PRIMARY = "[Agent-Powered Liquid Software](../pillars/liquid-software.md) (primary)"
SUPPORT = "[In the creator's control](../principles/in-the-creators-control.md) (supporting)"


class GapRelationshipTests(unittest.TestCase):
    def test_one_primary_and_optional_supporting_entries(self):
        refs, primary = parse_gap_relationships(
            "**Applies to:** " + PRIMARY + " · " + SUPPORT + " · **Assessment:** Open")
        self.assertEqual(refs, ["pillar:liquid-software", "principle:in-the-creators-control"])
        self.assertEqual(primary, "pillar:liquid-software")
        self.assertEqual(
            parse_gap_relationships("**Applies to:** " + PRIMARY + " · **Assessment:** Open"),
            (["pillar:liquid-software"], "pillar:liquid-software"))

    def test_rejects_missing_or_multiple_primary_relationships(self):
        for metadata in [
            "**Applies to:** " + PRIMARY.replace("(primary)", "(supporting)") + " · **Assessment:** Open",
            "**Applies to:** " + PRIMARY + " · " + SUPPORT.replace("(supporting)", "(primary)") + " · **Assessment:** Open",
            "**Applies to:** " + PRIMARY.replace(" (primary)", "") + " · **Assessment:** Open",
        ]:
            with self.subTest(metadata=metadata), self.assertRaises(ValueError):
                parse_gap_relationships(metadata)

    def test_rejects_duplicate_or_malformed_connections(self):
        for metadata in [
            "**Applies to:** " + PRIMARY + " · " + PRIMARY + " · **Assessment:** Open",
            "**Applies to:** " + SUPPORT + " · " + PRIMARY + " · **Assessment:** Open",
            "**Applies to:** " + PRIMARY + " · [Other](https://example.com) (supporting) · **Assessment:** Open",
        ]:
            with self.subTest(metadata=metadata), self.assertRaises(ValueError):
                parse_gap_relationships(metadata)


if __name__ == "__main__":
    unittest.main()
