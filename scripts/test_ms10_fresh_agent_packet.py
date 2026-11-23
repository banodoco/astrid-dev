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


    def test_proctor_requires_selected_source_identity_not_just_skill_name(self):
        content = EVALUATOR.read_text(encoding="utf-8")
        self.assertIn("same-name", content)
        self.assertIn("installed source path", content)
        self.assertIn("content hash", content)
        self.assertIn("NO-RESULT", content)
        self.assertIn("actual client trace", content)

    def test_clean_clone_of_pr_only_head_needs_explicit_fetch(self):
        """Use file transport so a new client receives main, not the PR-only ref."""
        import subprocess
        from tempfile import TemporaryDirectory

        with TemporaryDirectory(prefix="p73-pr-ref-fixture-") as temp:
            root = Path(temp)
            bare = root / "origin.git"
            writer = root / "writer"
            fresh = root / "fresh"

            def git(*args, cwd=None):
                p = subprocess.run(
                    ["git", *args], cwd=cwd, capture_output=True, text=True,
                    timeout=30, check=False,
                )
                self.assertEqual(p.returncode, 0, f"git {args}: {p.stderr}")
                return p.stdout.strip()

            git("init", "-q", "--bare", "--initial-branch=main", str(bare))
            git("clone", "-q", "file://" + str(bare), str(writer))
            git("config", "user.name", "Fixture", cwd=writer)
            git("config", "user.email", "fixture@example.invalid", cwd=writer)
            (writer / "README.md").write_text("main\n", encoding="utf-8")
            git("add", "README.md", cwd=writer)
            git("commit", "-qm", "main", cwd=writer)
            git("push", "-q", "origin", "HEAD:refs/heads/main", cwd=writer)
            (writer / "draft.md").write_text("PR-only candidate\n", encoding="utf-8")
            git("add", "draft.md", cwd=writer)
            git("commit", "-qm", "draft PR", cwd=writer)
            pinned = git("rev-parse", "HEAD", cwd=writer)
            git("push", "-q", "origin", "HEAD:refs/pull/1627/head", cwd=writer)
            git("clone", "-q", "file://" + str(bare), str(fresh))

            absent = subprocess.run(
                ["git", "checkout", "-q", "--detach", pinned],
                cwd=fresh, capture_output=True, text=True, check=False,
            )
            self.assertNotEqual(absent.returncode, 0)
            git("fetch", "-q", "--no-tags", "origin", "pull/1627/head", cwd=fresh)
            self.assertEqual(git("rev-parse", "FETCH_HEAD", cwd=fresh), pinned)
            git("checkout", "-q", "--detach", pinned, cwd=fresh)
            self.assertEqual(git("rev-parse", "HEAD", cwd=fresh), pinned)

    def test_proctor_fetches_and_verifies_pinned_pr_head_before_checkout(self):
        content = EVALUATOR.read_text(encoding="utf-8")
        fetch = 'git fetch --no-tags origin "pull/${SOURCE_PR}/head"'
        verify = 'test "$(git rev-parse FETCH_HEAD)" = "$SOURCE_SHA"'
        checkout = 'git checkout --detach "$SOURCE_SHA"'
        self.assertIn(fetch, content)
        self.assertIn(verify, content)
        self.assertLess(content.index(fetch), content.index(verify))
        self.assertLess(content.index(verify), content.index(checkout))
        self.assertIn("stop and obtain a new pinned assignment", content)

if __name__ == "__main__":
    unittest.main()
