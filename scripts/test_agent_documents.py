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

    def test_reject_source_symlink(self):
        original = self.write("shared/workstreams/plan.md", STREAM)
        link = self.root / "agent/shared/workstreams/other.md"
        link.symlink_to(original)
        self.assertIn("not a symlink", str(validate_documents(self.root)))

    def test_repository_source_catalog_can_be_discovered(self):
        root = Path(__file__).resolve().parents[1]
        docs = discover_documents(root)
        self.assertEqual(len([doc for doc in docs if doc.skill]), 14)
        self.assertEqual(len(docs), 29)
        self.assertEqual(validate_documents(root), [])
        expected = {"astrid-dev-start", "astrid-dev-leader", "astrid-dev-orchestrator",
                    "astrid-dev-manager", "astrid-dev-worker", "astrid-dev-plan"}
        self.assertTrue(expected.issubset({doc.skill_name for doc in docs if doc.skill}))


if __name__ == "__main__":
    unittest.main()
