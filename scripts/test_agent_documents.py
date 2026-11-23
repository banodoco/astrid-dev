"""Focused contract tests for Markdown-first role and workstream documents."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from agent_documents import discover_documents, parse_document, validate_documents


ROLE = """---
description: Lead bounded work and own the outcome.
skill: true
---

# Leader

## Responsibility

Own an accepted outcome.

## Authority

Follow the active run permission boundary.

## Responsibilities

Review evidence and make decisions.

## Handoff

Report accepted results and blockers.
"""

STREAM = """---
description: Plan an independently useful outcome.
skill: true
---

# Plan

## When to use

When an approved planning assignment arrives.

## Outcome

An independently verifiable plan.

## Inputs

Prior art and approved scope.

## Procedure

Investigate, choose and document the narrow route.

## Completion

A plan with evidence and task cards.
"""

REF = """---
description: Shared terms used by agents.
---

# Glossary

Terms stay defined in one place.
"""


class AgentDocumentTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "agent").mkdir()

    def write(self, path, body):
        file = self.root / "agent" / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(body, encoding="utf-8")
        return file

    def test_roles_workstreams_and_references_share_one_document_format(self):
        self.write("roles/leader.md", ROLE)
        self.write("roles/leader/run.md", STREAM.replace("skill: true\n", ""))
        self.write("shared/workstreams/plan.md", STREAM)
        self.write("shared/glossary.md", REF)
        docs = discover_documents(self.root)
        self.assertEqual(len(docs), 4)
        self.assertEqual({doc.skill_name for doc in docs if doc.skill},
                         {"astrid-dev-leader", "astrid-dev-plan"})
        self.assertEqual({doc.kind for doc in docs}, {"role", "workstream", "reference"})
        self.assertEqual(validate_documents(self.root), [])

    def test_location_does_not_determine_skill_status(self):
        path = self.write("shared/workstreams/iterate.md", STREAM.replace("skill: true\n", ""))
        self.assertIsNone(parse_document(self.root, path).skill_name)
        path.write_text(STREAM, encoding="utf-8")
        self.assertEqual(parse_document(self.root, path).skill_name, "astrid-dev-iterate")

    def test_duplicate_skill_stems_fail_without_name_override(self):
        self.write("roles/plan.md", ROLE)
        self.write("shared/workstreams/plan.md", STREAM)
        self.assertIn("duplicate skill name astrid-dev-plan",
                      str(validate_documents(self.root)))

    def test_invalid_skill_value_and_manual_name_refused(self):
        file = self.write("shared/workstreams/plan.md", STREAM)
        for replacement in ("skill: yes", "skill: 1", "skill: True", "skill: astrid-dev-plan"):
            with self.subTest(replacement=replacement):
                file.write_text(STREAM.replace("skill: true", replacement), encoding="utf-8")
                self.assertIn("literal boolean", str(validate_documents(self.root)))
        file.write_text(STREAM.replace("skill: true", "name: astrid-dev-plan"), encoding="utf-8")
        self.assertIn("only description", str(validate_documents(self.root)))

    def test_missing_description_and_invalid_filename_fail(self):
        file = self.write("shared/workstreams/plan.md", STREAM)
        file.write_text(STREAM.replace("description: Plan an independently useful outcome.\n", ""), encoding="utf-8")
        self.assertIn("description", str(validate_documents(self.root)))
        file.unlink()
        self.write("shared/workstreams/NotPlan.md", STREAM)
        self.assertIn("lowercase kebab-case", str(validate_documents(self.root)))

    def test_missing_or_empty_procedure_is_refused(self):
        file = self.write("shared/workstreams/plan.md", STREAM)
        file.write_text(STREAM.replace("## Procedure", "## Method"), encoding="utf-8")
        self.assertIn("## Procedure", str(validate_documents(self.root)))
        file.write_text(STREAM.replace("Investigate, choose and document the narrow route.", ""), encoding="utf-8")
        self.assertIn("must contain actual instructions", str(validate_documents(self.root)))

    def test_orphan_role_workstream_is_refused(self):
        self.write("roles/leader/run.md", STREAM)
        self.assertIn("has no definition", str(validate_documents(self.root)))

    def test_parse_document_accepts_symlinked_checkout_root(self):
        # macOS commonly spells its temporary root /var while resolve() uses /private/var.
        # A deliberate local alias reproduces the differing spellings on Linux CI too.
        document = self.write("roles/leader.md", ROLE)
        checkout_alias = self.root / "checkout-alias"
        checkout_alias.symlink_to(self.root, target_is_directory=True)
        parsed = parse_document(checkout_alias, checkout_alias / "agent/roles/leader.md")
        self.assertEqual(parsed.relative, Path("roles/leader.md"))
        self.assertEqual(parsed.path, document.resolve())

    def test_dangling_agent_directory_symlink_is_not_an_empty_document_tree(self):
        # Lexical existence is false for dangling symlinks, but this is a refusal,
        # not permission to retire previously generated packages.
        (self.root / "agent").rmdir()
        (self.root / "agent").symlink_to(self.root / "missing-agent", target_is_directory=True)
        problems = validate_documents(self.root)
        self.assertTrue(any("real directory" in issue for issue in problems), problems)

    def test_real_repository_markdown_catalog(self):
        root = Path(__file__).resolve().parents[1]
        documents = discover_documents(root)
        self.assertEqual(len(documents), 29)
        expected = {
            "astrid-dev-start", "astrid-dev-leader", "astrid-dev-orchestrator",
            "astrid-dev-manager", "astrid-dev-worker", "astrid-dev-bugfix",
            "astrid-dev-gap", "astrid-dev-gpu-validate", "astrid-dev-green",
            "astrid-dev-improve", "astrid-dev-iterate", "astrid-dev-merge",
            "astrid-dev-plan", "astrid-dev-release",
        }
        self.assertEqual({doc.skill_name for doc in documents if doc.skill}, expected)
        self.assertEqual(validate_documents(root), [])

    def test_staged_dispatch_names_canonical_manager_and_ci_checks_packages(self):
        root = Path(__file__).resolve().parents[1]
        orchestrator = (root / "agent/roles/orchestrator.md").read_text(encoding="utf-8")
        self.assertIn("Follow the astrid-dev-manager skill.", orchestrator)
        self.assertNotIn("Follow the astrid-dev-manage skill.", orchestrator)
        workflow = (root / ".github/workflows/docs.yml").read_text(encoding="utf-8")
        self.assertIn("python3 scripts/astrid_dev.py skills build", workflow)
        self.assertIn("python3 scripts/astrid_dev.py skills check", workflow)

    def test_reject_source_symlink(self):
        original = self.write("shared/workstreams/plan.md", STREAM)
        link = self.root / "agent/shared/workstreams/other.md"
        link.symlink_to(original)
        self.assertIn("not a symlink", str(validate_documents(self.root)))


if __name__ == "__main__":
    unittest.main()
