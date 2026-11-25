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

    def test_skill_name_length_limit_accepts_53_character_stem(self):
        stem = "check-generated-workstream-and-shared-policy-discover"
        self.assertEqual(len(stem), 53)
        path = self.write(f"shared/workstreams/{stem}.md", STREAM)
        name = parse_document(self.root, path).skill_name
        self.assertEqual(name, f"astrid-dev-{stem}")
        self.assertEqual(len(name), 64)
        self.assertEqual(validate_documents(self.root), [])

    def test_skill_name_length_limit_refuses_54_character_stem(self):
        stem = "check-generated-workstream-and-shared-policy-discovery"
        self.assertEqual(len(stem), 54)
        path = self.write(f"shared/workstreams/{stem}.md", STREAM)
        message = (f"agent/shared/workstreams/{stem}.md: generated skill name "
                   f"'astrid-dev-{stem}' is 65 characters; limit is 64")
        with self.assertRaises(ValueError) as raised:
            parse_document(self.root, path)
        self.assertEqual(str(raised.exception), message)
        self.assertEqual(validate_documents(self.root), [f"agent documents: {message}"])

    def test_long_non_skill_filenames_are_accepted(self):
        stem = "check-generated-workstream-and-shared-policy-discovery"
        for flag in ("skill: false\n", ""):
            with self.subTest(flag=flag):
                path = self.write(f"shared/workstreams/{stem}.md",
                                  STREAM.replace("skill: true\n", flag))
                self.assertIsNone(parse_document(self.root, path).skill_name)
                self.assertEqual(validate_documents(self.root), [])

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


    def test_canonical_agent_source_root_and_skill_prefix_are_stable(self):
        from agent_documents import AGENT_SOURCE_ROOT, SKILL_PREFIX

        self.assertEqual(AGENT_SOURCE_ROOT, "agent")
        self.assertEqual(SKILL_PREFIX, "astrid-dev-")
        path = self.write("roles/leader.md", ROLE)
        document = parse_document(self.root, path)
        self.assertEqual(document.relative, Path("roles/leader.md"))
        self.assertEqual(document.skill_name, "astrid-dev-leader")

    def test_invalid_descriptions_and_missing_title_are_refused(self):
        original = "description: Plan an independently useful outcome."
        file = self.write("shared/workstreams/plan.md", STREAM)
        for description in ("", "No terminal punctuation", "x" * 240 + ".",
                            "\tLeading tab.", "Trailing space. ", "A [linked] sentence.",
                            "A | table.", "A\ttab.", "First line.\n  Second line."):
            with self.subTest(description=description):
                file.write_text(STREAM.replace(original, "description: " + description), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "description|frontmatter"):
                    parse_document(self.root, file)
        file.write_text(STREAM.replace("# Plan\n", "Plan\n", 1), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "nonempty # title"):
            parse_document(self.root, file)

    def test_required_role_and_workstream_sections_are_unique_even_after_paragraphs(self):
        for path, original, heading in (("roles/leader.md", ROLE, "Authority"),
                                        ("shared/workstreams/plan.md", STREAM, "Outcome")):
            with self.subTest(path=path):
                file = self.write(path, original + f"\nExtra paragraph.\n\n## {heading}\n\nAnother instruction.\n")
                with self.assertRaisesRegex(ValueError, "exactly one"):
                    parse_document(self.root, file)
                for fence in ("```", "~~~"):
                    file.write_text(original + f"\n{fence}\n## {heading}\nExample only.\n{fence}\n", encoding="utf-8")
                    self.assertEqual(parse_document(self.root, file).title,
                                     "Leader" if path.startswith("roles/") else "Plan")

    def test_required_sections_cannot_be_missing_out_of_order_or_empty(self):
        from document_structure import section
        cases = (("roles/leader.md", ROLE, ("Responsibility", "Authority", "Responsibilities", "Handoff")),
                 ("shared/workstreams/plan.md", STREAM, ("When to use", "Outcome", "Inputs", "Procedure", "Completion")))
        for path, original, headings in cases:
            file = self.write(path, original)
            for heading in headings:
                for bad in (original.replace(f"## {heading}\n", f"## Missing {heading}\n", 1),
                            original.replace(section(original, heading), "", 1)):
                    with self.subTest(path=path, heading=heading, bad=bad):
                        file.write_text(bad, encoding="utf-8")
                        with self.assertRaisesRegex(ValueError, "missing or out-of-order|actual instructions"):
                            parse_document(self.root, file)
            first, second = headings[:2]
            swapped = original.replace(f"## {first}\n", "## Temporary\n", 1)
            swapped = swapped.replace(f"## {second}\n", f"## {first}\n", 1).replace("## Temporary\n", f"## {second}\n", 1)
            file.write_text(swapped, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "out-of-order"):
                parse_document(self.root, file)

    def test_required_workstream_sections_keep_the_legacy_substance_minimum(self):
        from document_structure import section
        file = self.write("shared/workstreams/plan.md", STREAM)
        for heading in ("When to use", "Outcome", "Inputs", "Procedure", "Completion"):
            for value in ("short", "TBD", "TODO", "12345678901"):
                with self.subTest(heading=heading, value=value):
                    file.write_text(STREAM.replace(section(STREAM, heading), value, 1), encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, "substantive instructions"):
                        parse_document(self.root, file)
            file.write_text(STREAM.replace(section(STREAM, heading), "123456789012", 1), encoding="utf-8")
            self.assertEqual(parse_document(self.root, file).kind, "workstream")

    def test_duplicate_titles_under_one_role_are_refused_without_a_skill_flag(self):
        self.write("roles/leader.md", ROLE)
        first = STREAM.replace("skill: true\n", "").replace("# Plan\n", "# same title\n")
        self.write("roles/leader/first.md", first)
        second = self.write("roles/leader/second.md", first.replace("# same title\n", "# Same title\n"))
        self.assertIn("duplicate workstream title", str(validate_documents(self.root)))
        second.unlink()
        self.write("roles/manager.md", ROLE.replace("skill: true\n", ""))
        self.write("roles/manager/second.md", first)
        self.write("roles/leader/setup/README.md", REF.replace("# Glossary", "# Same title"))
        self.assertEqual(validate_documents(self.root), [])
        self.assertEqual(len([doc for doc in discover_documents(self.root) if doc.kind == "workstream"]), 2)

    def test_real_workstreams_all_keep_five_substantive_sections(self):
        from document_structure import section
        root = Path(__file__).resolve().parents[1]
        streams = [doc for doc in discover_documents(root) if doc.kind == "workstream"]
        self.assertGreaterEqual(len(streams), 15)
        for document in streams:
            for heading in ("When to use", "Outcome", "Inputs", "Procedure", "Completion"):
                with self.subTest(source=document.relative, heading=heading):
                    self.assertGreaterEqual(len(section(document.body, heading)), 12)

    def test_routing_table_detection_ignores_fences_role_routes_and_mode_tables(self):
        from agent_documents import routing_table_headers
        table = "| Route | Work | Claude | Codex |\n| --- | --- | --- | --- |\n| N | Work | First | Second |\n"
        self.assertEqual(len(routing_table_headers(table)), 1)
        for fence in ("```", "~~~", "````"):
            with self.subTest(fence=fence):
                self.assertEqual(routing_table_headers(fence + "markdown\n" + table + fence + "\n"), ())
        self.assertEqual(routing_table_headers(
            "| Route | The manager's own work |\n| --- | --- |\n| X | Decisions |\n\n"
            "| Route | ChatGPT mode |\n| --- | --- |\n| X | Extra High |\n"), ())
        self.assertEqual(len(routing_table_headers(
            "Route | Model family\n:--- | ---:\nS | A chosen family\n")), 1)
        self.assertEqual(len(routing_table_headers(
            "| **Route** | `Claude` | Codex |\n| - | :-: | -: |\n| S | First | Second |\n")), 1)



if __name__ == "__main__":
    unittest.main()
