"""Guard the uncoached MS10 packet and separate real-client evaluator protocol."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "plans/73-markdown-first-agent-skills/evidence"
ACTOR = EVIDENCE / "ms10-fresh-agent-assignment-20261123.md"
EVALUATOR = EVIDENCE / "ms10-client-discovery-protocol-20261123.md"
DECISIONS = EVIDENCE / "ms7-ms9-transition-decision-20261123.md"


class FreshAgentPacketTests(unittest.TestCase):
    def test_assignment_does_not_leak_scoring_or_bespoke_recipe(self):
        actor = ACTOR.read_text(encoding="utf-8")
        self.assertIn("agent/README.md", actor)
        # Do not coach the actor on the exact opt-in syntax; the README owns it.
        self.assertNotIn("skill: true", actor)
        self.assertIn("independently callable new shared workstream", actor)
        self.assertIn("disposable", actor)
        self.assertIn("NO-RESULT", actor)
        self.assertIn("Do not", actor)
        for phrase in (
            "ms10_extension_exercise.py",
            "extension-probe.md",
            "ms10-client-discovery-protocol-20261123.md",
            "ms11_negative_matrix.py",
            "## Evaluator checklist",
            "exact 14", "14→15", "26/26", "score:",
        ):
            with self.subTest(leaked=phrase):
                self.assertNotIn(phrase, actor)

    def test_evaluator_is_a_separate_usable_client_verification_packet(self):
        content = EVALUATOR.read_text(encoding="utf-8")
        self.assertIn("ms10-fresh-agent-assignment-20261123.md", content)
        for key in (
            "git rev-parse HEAD", "git status --porcelain",
            "learn.chatgpt.com/docs/build-skills",
            "code.claude.com/docs/en/skills",
            "codex --version", "claude --version",
            "$HOME/.agents/skills", "$HOME/.claude/skills",
            "/skills", "/astrid-dev-", "implicit", "explicit",
            "NO-RESULT", "INDEPENDENT", "skill: true",
        ):
            with self.subTest(proof=key):
                self.assertIn(key.casefold(), content.casefold())
        self.assertIn("Keep this evaluator protocol", content)

    def test_all_three_documents_still_explicitly_gate_cutover(self):
        for file in (ACTOR, EVALUATOR, DECISIONS):
            with self.subTest(file=file.name):
                content = file.read_text(encoding="utf-8")
                self.assertTrue(file.is_file())
                self.assertRegex(content, r"D5|cutover")
                self.assertNotIn("CUTOVER APPROVED", content)

    def test_relative_references_in_proctor_packet_resolve(self):
        content = EVALUATOR.read_text(encoding="utf-8")
        names = re.findall(r"\]\((ms10-[^)#]+\.md)(?:#[^)]+)?\)", content)
        self.assertTrue(names)
        for name in names:
            self.assertTrue((EVIDENCE / name).is_file(), name)


if __name__ == "__main__":
    unittest.main()
