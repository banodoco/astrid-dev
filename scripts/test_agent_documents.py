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
        by_path = {doc.relative.as_posix(): doc for doc in documents}
        # Preserve every migrated original source and its required skill identity,
        # while allowing MS-10 to add well-formed Markdown and opted-in skills.
        required_skills = {
            "start.md": "astrid-dev-start",
            "roles/leader.md": "astrid-dev-leader",
            "roles/orchestrator.md": "astrid-dev-orchestrator",
            "roles/manager.md": "astrid-dev-manager",
            "roles/worker.md": "astrid-dev-worker",
            "shared/workstreams/bugfix.md": "astrid-dev-bugfix",
            "shared/workstreams/gap.md": "astrid-dev-gap",
            "shared/workstreams/gpu-validate.md": "astrid-dev-gpu-validate",
            "shared/workstreams/green.md": "astrid-dev-green",
            "shared/workstreams/improve.md": "astrid-dev-improve",
            "shared/workstreams/iterate.md": "astrid-dev-iterate",
            "shared/workstreams/merge.md": "astrid-dev-merge",
            "shared/workstreams/plan.md": "astrid-dev-plan",
            "shared/workstreams/release.md": "astrid-dev-release",
        }
        required_references = {
            "README.md",
            "guides/codex-cloud/README.md",
            "guides/codex-in-claude-cloud/README.md",
            "guides/codex-in-claude-cloud/manager-brief.md",
            "roles/leader/multi-manager-release.md",
            "roles/manager/chatgpt-packet.md",
            "roles/manager/whole-project.md",
            "roles/orchestrator/codex-cloud-sessions.md",
            "roles/orchestrator/codex-in-claude-cloud.md",
            "roles/orchestrator/multi-manager-dispatch.md",
            "shared/domains.md",
            "shared/glossary.md",
            "shared/release-sources.md",
            "shared/run-contract.md",
            "shared/templates/decisions-ledger.md",
        }
        self.assertTrue(set(required_skills).issubset(by_path), sorted(set(required_skills) - set(by_path)))
        self.assertTrue(required_references.issubset(by_path), sorted(required_references - set(by_path)))
        for path, skill_name in required_skills.items():
            with self.subTest(path=path):
                self.assertEqual(by_path[path].skill_name, skill_name)
        self.assertEqual(validate_documents(root), [])

    def test_valid_workstream_extension_adds_a_skill_without_removing_any(self):
        from shutil import copytree
        source = Path(__file__).resolve().parents[1]
        with TemporaryDirectory(prefix="agent-extensibility-") as tmp:
            root = Path(tmp)
            copytree(source / "agent", root / "agent", symlinks=True)
            before = discover_documents(root)
            before_skills = {doc.skill_name for doc in before if doc.skill}
            self.assertEqual(validate_documents(root), [])
            addition = root / "agent/shared/workstreams/extension-probe.md"
            addition.write_text(STREAM.replace("# Plan\n", "# Extension probe\n"), encoding="utf-8")
            after = discover_documents(root)
            after_skills = {doc.skill_name for doc in after if doc.skill}
            self.assertEqual(len(after), len(before) + 1)
            self.assertEqual(after_skills, before_skills | {"astrid-dev-extension-probe"})
            self.assertEqual(validate_documents(root), [])

    def test_staged_dispatch_names_canonical_manager_and_ci_checks_packages(self):
        root = Path(__file__).resolve().parents[1]
        orchestrator = (root / "agent/roles/orchestrator.md").read_text(encoding="utf-8")
        self.assertIn("Follow the astrid-dev-manager skill.", orchestrator)
        self.assertNotIn("Follow the astrid-dev-manage skill.", orchestrator)
        workflow = (root / ".github/workflows/docs.yml").read_text(encoding="utf-8")
        self.assertIn("python3 scripts/astrid_dev.py skills build", workflow)
        self.assertIn("python3 scripts/astrid_dev.py skills check", workflow)

    def test_staged_roles_use_one_shared_workstream_index(self):
        root = Path(__file__).resolve().parents[1]
        catalog = (root / "agent/README.md").read_text(encoding="utf-8")
        self.assertEqual(catalog.count("## Shared workstreams"), 1)
        for name in ("bugfix", "gap", "gpu-validate", "green", "improve",
                     "iterate", "merge", "plan", "release"):
            with self.subTest(workstream=name):
                self.assertIn(f"(shared/workstreams/{name}.md)", catalog)
        for role in ("leader", "orchestrator", "manager", "worker"):
            with self.subTest(role=role):
                text = (root / "agent/roles" / f"{role}.md").read_text(encoding="utf-8")
                self.assertIn("[shared workstream index](../README.md#shared-workstreams)", text)
                self.assertNotIn("Refer to shared workstreams when needed", text)

    def test_reject_source_symlink(self):
        original = self.write("shared/workstreams/plan.md", STREAM)
        link = self.root / "agent/shared/workstreams/other.md"
        link.symlink_to(original)
        self.assertIn("not a symlink", str(validate_documents(self.root)))


if __name__ == "__main__":
    unittest.main()
