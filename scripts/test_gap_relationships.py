"""Focused tests for the primary/supporting gap relationship grammar."""
import unittest

from gap_relationships import gap_metadata, parse_gap_aspirations, parse_gap_relationships

PRIMARY = "[Live tool composition](../pillars/liquid-software.md#live-tool-composition) (primary)"
SUPPORT = "[Explicit permissions and privacy](../principles/in-the-creators-control.md#explicit-permissions-and-privacy) (supporting)"


class GapRelationshipTests(unittest.TestCase):
    def test_one_primary_and_optional_supporting_entries(self):
        refs, primary = parse_gap_relationships(
            "**Aspiration:** " + PRIMARY + " · " + SUPPORT + " · **Assessment:** Open")
        self.assertEqual(refs, ["pillar:liquid-software", "principle:in-the-creators-control"])
        self.assertEqual(primary, "pillar:liquid-software")
        self.assertEqual(
            parse_gap_relationships("**Aspiration:** " + PRIMARY + " · **Assessment:** Open"),
            (["pillar:liquid-software"], "pillar:liquid-software"))

    def test_rejects_missing_or_multiple_primary_relationships(self):
        for metadata in [
            "**Aspiration:** " + PRIMARY.replace("(primary)", "(supporting)") + " · **Assessment:** Open",
            "**Aspiration:** " + PRIMARY + " · " + SUPPORT.replace("(supporting)", "(primary)") + " · **Assessment:** Open",
            "**Aspiration:** " + PRIMARY.replace(" (primary)", "") + " · **Assessment:** Open",
        ]:
            with self.subTest(metadata=metadata), self.assertRaises(ValueError):
                parse_gap_relationships(metadata)

    def test_rejects_duplicate_or_malformed_connections(self):
        for metadata in [
            "**Aspiration:** " + PRIMARY + " · " + PRIMARY + " · **Assessment:** Open",
            "**Aspiration:** " + SUPPORT + " · " + PRIMARY + " · **Assessment:** Open",
            "**Aspiration:** " + PRIMARY + " · [Other](https://example.com) (supporting) · **Assessment:** Open",
        ]:
            with self.subTest(metadata=metadata), self.assertRaises(ValueError):
                parse_gap_relationships(metadata)


    def test_anchor_is_githubs_but_reference_uses_the_parser_id(self):
        metadata = "**Aspiration:** [Shared human–agent work](../pillars/liquid-software.md#shared-humanagent-work) (primary) · **Assessment:** Open"
        self.assertEqual(parse_gap_aspirations(metadata),
                         (["pillar:liquid-software/shared-human-agent-work"], "pillar:liquid-software/shared-human-agent-work"))
        with self.assertRaisesRegex(ValueError, "anchor"):
            parse_gap_aspirations(metadata.replace("#shared-humanagent-work", "#shared-human-agent-work"))

    def test_supporting_aspirations_have_no_cap_and_elements_are_deduplicated(self):
        entries = [PRIMARY, SUPPORT,
            "[Control at every layer](../principles/in-the-creators-control.md#control-at-every-layer) (supporting)",
            "[A small, dependable foundation](../pillars/liquid-software.md#a-small-dependable-foundation) (supporting)",
            "[Artistic agency](../pillars/artistic-ambition.md#artistic-agency) (supporting)"]
        metadata = "**Aspiration:** " + " · ".join(entries) + " · **Assessment:** Open"
        self.assertEqual(len(parse_gap_aspirations(metadata)[0]), 5)
        self.assertEqual(parse_gap_relationships(metadata)[0],
            ["pillar:liquid-software", "principle:in-the-creators-control", "pillar:artistic-ambition"])

    def test_missing_anchor_unknown_heading_wrong_label_and_old_line_fail(self):
        metadata = "**Aspiration:** " + PRIMARY + " · **Assessment:** Open"
        cases = [
            metadata.replace("#live-tool-composition", ""),
            metadata.replace("#live-tool-composition", "#does-not-exist"),
            metadata.replace("[Live tool composition]", "[Wrong title]"),
            metadata.replace("**Aspiration:**", "**Applies to:**"),
            metadata + "\n" + metadata,
        ]
        for source in cases:
            with self.subTest(source=source), self.assertRaises(ValueError):
                parse_gap_aspirations(source)
        with self.assertRaises(ValueError):
            gap_metadata(metadata + "\n" + metadata.replace("**Aspiration:**", "**Applies to:**"))
        with self.assertRaises(ValueError):
            gap_metadata(metadata + "\n" + metadata)


if __name__ == "__main__":
    unittest.main()
