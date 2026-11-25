"""Focused generated-skill packaging, reference and refusal tests."""
import os
import subprocess
import select
import sys
import threading
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from skill_builder import build_packages, check_packages, expected_packages


ROLE = """---
description: Lead an accepted outcome and preserve authority.
skill: true
---

# Leader

## Responsibility

Own the outcome.

## Authority

Follow the shared [rules](../shared/run-contract.md#rules).

## Responsibilities

Review real results.

## Handoff

Report exact evidence.
"""
STREAM = """---
description: Plan an independently useful outcome.
skill: true
---

# Plan

## When to use

When scope is needed.

## Outcome

A verifiable plan.

## Inputs

Existing work and authority.

## Procedure

Use the [rules](../run-contract.md#rules) and [notes](../../../docs/notes.md).

## Completion

Give the next agent a complete plan.
"""


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "agent" / "roles").mkdir(parents=True)
        (self.root / "agent" / "shared" / "workstreams").mkdir(parents=True)
        (self.root / "docs").mkdir()
        (self.root / "docs" / "notes.md").write_text("# Notes\n", encoding="utf-8")
        (self.root / "agent" / "shared" / "run-contract.md").write_text(
            "---\ndescription: Shared rules.\n---\n\n# Run contract\n\n## Rules\n\nNever grant missing authority.\n", encoding="utf-8")
        (self.root / "agent" / "start.md").write_text(
            "---\ndescription: Start Astrid development work.\nskill: true\n---\n\n"
            "# Contribute to Astrid\n\nBegin with the accepted assignment.\n",
            encoding="utf-8")
        (self.root / "agent" / "roles" / "leader.md").write_text(ROLE, encoding="utf-8")
        (self.root / "agent" / "shared" / "workstreams" / "gap.md").write_text(
            STREAM, encoding="utf-8")

    def package(self, name):
        return self.root / ".generated" / "skills" / name

    def test_generate_canonical_metadata_and_links(self):
        self.assertEqual(check_packages(self.root), ["generated skill packages are missing"])
        build_packages(self.root)
        self.assertEqual(check_packages(self.root), [])
        self.assertTrue((self.package("astrid-dev-start") / "SKILL.md").is_file())
        leader = self.package("astrid-dev-leader")
        text = (leader / "SKILL.md").read_text()
        self.assertIn("name: astrid-dev-leader", text)
        self.assertIn("repo/agent/shared/run-contract.md#rules", text)
        self.assertNotIn("name: astrid-dev-gap", text)
        self.assertEqual(os.readlink(leader / "repo"), "../../../")
        self.assertEqual((leader / "repo" / "agent" / "shared" / "run-contract.md").resolve(),
                         (self.root / "agent" / "shared" / "run-contract.md").resolve())
        plan = (self.package("astrid-dev-gap") / "SKILL.md").read_text()
        self.assertIn("repo/docs/notes.md", plan)

    def test_build_is_deterministic_and_second_build_does_nothing(self):
        self.assertTrue(build_packages(self.root))
        self.assertEqual(build_packages(self.root), [])
        self.assertEqual(check_packages(self.root), [])

    def test_skill_name_length_limit_builds_53_character_stem(self):
        stem = "check-generated-workstream-and-shared-policy-discover"
        name = f"astrid-dev-{stem}"
        self.assertEqual(len(name), 64)
        path = self.root / "agent" / "shared" / "workstreams" / f"{stem}.md"
        path.write_text(STREAM, encoding="utf-8")
        build_packages(self.root)
        skill = self.package(name) / "SKILL.md"
        self.assertIn(f"name: {name}", skill.read_text(encoding="utf-8").splitlines())
        self.assertEqual(check_packages(self.root), [])

    def test_overlong_skill_name_refuses_cold_build(self):
        stem = "check-generated-workstream-and-shared-policy-discovery"
        path = self.root / "agent" / "shared" / "workstreams" / f"{stem}.md"
        path.write_text(STREAM, encoding="utf-8")
        message = (f"agent/shared/workstreams/{stem}.md: generated skill name "
                   f"'astrid-dev-{stem}' is 65 characters; limit is 64")
        with self.assertRaises(ValueError) as raised:
            build_packages(self.root)
        self.assertEqual(str(raised.exception), message)
        self.assertFalse((self.root / ".generated" / "skills").exists())

    def test_overlong_skill_name_preserves_existing_generation(self):
        build_packages(self.root)
        output = self.root / ".generated" / "skills"

        def snapshot():
            return {str(p.relative_to(output)): (("link", os.readlink(p)) if p.is_symlink()
                    else ("file", p.read_bytes()) if p.is_file() else ("dir",))
                    for p in sorted(output.rglob("*"))}

        before = snapshot()
        source = self.root / "agent" / "start.md"
        source.write_text(source.read_text(encoding="utf-8") + "\nChanged.\n",
                          encoding="utf-8")
        workstreams = self.root / "agent" / "shared" / "workstreams"
        (workstreams / "new-workstream.md").write_text(STREAM, encoding="utf-8")
        stem = "check-generated-workstream-and-shared-policy-discovery"
        (workstreams / f"{stem}.md").write_text(STREAM, encoding="utf-8")
        message = (f"agent/shared/workstreams/{stem}.md: generated skill name "
                   f"'astrid-dev-{stem}' is 65 characters; limit is 64")
        with self.assertRaises(ValueError) as raised:
            build_packages(self.root)
        self.assertEqual(str(raised.exception), message)
        self.assertEqual(snapshot(), before)
        self.assertFalse(self.package("astrid-dev-new-workstream").exists())
        self.assertFalse(self.package(f"astrid-dev-{stem}").exists())

    def test_overlong_skill_name_refused_by_validator_after_clean_build(self):
        from agent_documents import validate_documents

        build_packages(self.root)
        self.assertEqual(check_packages(self.root), [])
        self.assertEqual(validate_documents(self.root), [])
        stem = "check-generated-workstream-and-shared-policy-discovery"
        path = self.root / "agent" / "shared" / "workstreams" / f"{stem}.md"
        path.write_text(STREAM, encoding="utf-8")
        message = (f"agent/shared/workstreams/{stem}.md: generated skill name "
                   f"'astrid-dev-{stem}' is 65 characters; limit is 64")
        self.assertEqual(validate_documents(self.root), [f"agent documents: {message}"])

    def test_turning_skill_flag_off_retires_only_owned_output(self):
        build_packages(self.root)
        file = self.root / "agent" / "roles" / "leader.md"
        file.write_text(ROLE.replace("skill: true\n", ""), encoding="utf-8")
        self.assertTrue(build_packages(self.root))
        self.assertFalse(self.package("astrid-dev-leader").exists())
        self.assertTrue(file.exists())
        self.assertTrue(self.package("astrid-dev-gap").is_dir())

    def test_missing_reference_and_heading_fail_before_mutation(self):
        file = self.root / "agent" / "roles" / "leader.md"
        for replaced in ("../shared/not-here.md", "../shared/run-contract.md#missing"):
            with self.subTest(replaced=replaced):
                file.write_text(ROLE.replace("../shared/run-contract.md#rules", replaced), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "missing"):
                    expected_packages(self.root)
        file.write_text(ROLE, encoding="utf-8")

    def test_out_of_checkout_reference_refused(self):
        file = self.root / "agent" / "roles" / "leader.md"
        file.write_text(ROLE.replace("../shared/run-contract.md#rules", "../../../../etc/passwd"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "escapes checkout"):
            expected_packages(self.root)

    def test_tampering_and_foreign_dirs_are_not_silently_accepted(self):
        build_packages(self.root)
        (self.package("astrid-dev-leader") / "SKILL.md").write_text("tampered\n", encoding="utf-8")
        self.assertTrue(check_packages(self.root))
        self.assertTrue(build_packages(self.root))
        foreign = self.root / ".generated" / "skills" / "foreign"
        foreign.mkdir()
        (foreign / "SKILL.md").write_text("not ours", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unmanaged"):
            build_packages(self.root)
        self.assertTrue(foreign.exists())

    def test_description_with_yaml_special_characters_is_preserved(self):
        from json import loads

        path = self.root / "agent" / "roles" / "leader.md"
        description = 'Guide migration: keep "#tag" intact.'
        path.write_text(
            ROLE.replace("Lead an accepted outcome and preserve authority.", description),
            encoding="utf-8",
        )
        build_packages(self.root)
        skill = (self.package("astrid-dev-leader") / "SKILL.md").read_text(encoding="utf-8")
        line = next(line for line in skill.splitlines() if line.startswith("description: "))
        self.assertEqual(loads(line.removeprefix("description: ")), description)

    def test_foreign_package_refusal_does_not_retire_owned_packages(self):
        build_packages(self.root)
        source = self.root / "agent" / "roles" / "leader.md"
        source.write_text(ROLE.replace("skill: true\n", ""), encoding="utf-8")
        foreign = self.root / ".generated" / "skills" / "zz-foreign"
        foreign.mkdir()
        (foreign / "SKILL.md").write_text("foreign", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unmanaged"):
            build_packages(self.root)
        self.assertTrue(self.package("astrid-dev-leader").exists())
        self.assertTrue(foreign.exists())

    def test_fragment_only_links_must_point_to_an_existing_heading(self):
        path = self.root / "agent" / "roles" / "leader.md"
        original = "[rules](../shared/run-contract.md#rules)"
        path.write_text(ROLE.replace(original, "[section](#missing-heading)"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "missing heading"):
            expected_packages(self.root)
        path.write_text(ROLE.replace(original, "[section](#authority)"), encoding="utf-8")
        content = expected_packages(self.root)["astrid-dev-leader"][0]
        self.assertIn("[section](#authority)", content)

    def test_matching_skill_symlink_is_rejected_by_check(self):
        build_packages(self.root)
        skill = self.package("astrid-dev-start") / "SKILL.md"
        foreign = self.root / "foreign-skill.md"
        foreign.write_text(skill.read_text(encoding="utf-8"), encoding="utf-8")
        skill.unlink()
        skill.symlink_to(foreign)
        self.assertTrue(any("symlinked SKILL.md" in error
                            for error in check_packages(self.root)))
        self.assertTrue(skill.is_symlink())
        self.assertEqual(foreign.read_text(encoding="utf-8"),
                         skill.read_text(encoding="utf-8"))

    def test_skill_symlink_preflight_precedes_any_stale_retirement(self):
        build_packages(self.root)
        skill = self.package("astrid-dev-start") / "SKILL.md"
        foreign = self.root / "foreign-skill.md"
        foreign.write_text(skill.read_text(encoding="utf-8"), encoding="utf-8")
        skill.unlink()
        skill.symlink_to(foreign)
        leader_source = self.root / "agent" / "roles" / "leader.md"
        leader_source.write_text(ROLE.replace("skill: true\n", ""), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "symlinked SKILL.md"):
            build_packages(self.root)
        self.assertTrue(self.package("astrid-dev-leader").exists())
        self.assertTrue(skill.is_symlink())

    def test_reference_style_definition_rewrites_to_repository_link(self):
        path = self.root / "agent" / "roles" / "leader.md"
        path.write_text(ROLE.replace(
            "Follow the shared [rules](../shared/run-contract.md#rules).",
            "Follow the shared [rules][contract].\n\n[contract]: ../shared/run-contract.md#rules"
        ), encoding="utf-8")
        build_packages(self.root)
        generated = (self.package("astrid-dev-leader") / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("[rules][contract]", generated)
        self.assertIn("[contract]: repo/agent/shared/run-contract.md#rules", generated)
        self.assertEqual(check_packages(self.root), [])

    def test_missing_reference_style_file_blocks_build(self):
        path = self.root / "agent" / "roles" / "leader.md"
        path.write_text(ROLE.replace(
            "Follow the shared [rules](../shared/run-contract.md#rules).",
            "Follow the shared [rules][contract].\n\n[contract]: ../shared/absent-contract.md"
        ), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "missing link target"):
            build_packages(self.root)

    def test_missing_reference_style_file_blocks_check(self):
        build_packages(self.root)
        path = self.root / "agent" / "roles" / "leader.md"
        path.write_text(ROLE.replace(
            "Follow the shared [rules](../shared/run-contract.md#rules).",
            "Follow the shared [rules][contract].\n\n[contract]: ../shared/absent-contract.md"
        ), encoding="utf-8")
        self.assertTrue(any("missing link target" in error
                            for error in check_packages(self.root)),
                        check_packages(self.root))

    def test_stale_repo_entry_is_validated_before_any_retirement(self):
        build_packages(self.root)
        leader = self.package("astrid-dev-leader")
        gap = self.package("astrid-dev-gap")
        link = leader / "repo"
        link.unlink()
        link.symlink_to(self.root / "foreign-repo", target_is_directory=True)
        (self.root / "agent" / "roles" / "leader.md").write_text(
            ROLE.replace("skill: true\n", ""), encoding="utf-8")
        (self.root / "agent" / "shared" / "workstreams" / "gap.md").write_text(
            STREAM.replace("skill: true\n", ""), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "canonical repo link"):
            build_packages(self.root)
        self.assertTrue(leader.is_dir())
        self.assertTrue(gap.is_dir())
        self.assertTrue(link.is_symlink())

    def test_stale_repo_directory_is_not_owned_for_cleanup(self):
        build_packages(self.root)
        leader = self.package("astrid-dev-leader")
        link = leader / "repo"
        link.unlink()
        link.mkdir()
        (self.root / "agent" / "roles" / "leader.md").write_text(
            ROLE.replace("skill: true\n", ""), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "canonical repo link"):
            build_packages(self.root)
        self.assertTrue(leader.is_dir())
        self.assertTrue(link.is_dir())

    def test_stale_package_missing_skill_is_not_deleted(self):
        build_packages(self.root)
        leader = self.package("astrid-dev-leader")
        (leader / "SKILL.md").unlink()
        (self.root / "agent" / "roles" / "leader.md").write_text(
            ROLE.replace("skill: true\n", ""), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "SKILL.md"):
            build_packages(self.root)
        self.assertTrue(leader.is_dir())

    def test_absolute_and_file_links_are_not_portable_local_sources(self):
        source = self.root / "agent" / "roles" / "leader.md"
        original = "Follow the shared [rules](../shared/run-contract.md#rules)."
        for address in ("/tmp/missing-secret", "file:///tmp/missing-secret",
                        "FILE:///tmp/missing-secret", "file:../missing-secret",
                        "C:/private/missing-secret"):
            with self.subTest(address=address):
                source.write_text(
                    ROLE.replace(original, f"Follow the shared [unsafe]({address})."),
                    encoding="utf-8",
                )
                with self.assertRaisesRegex(ValueError, "absolute|file:|filesystem"):
                    expected_packages(self.root)

    def test_reference_definition_cannot_bypass_local_file_refusal(self):
        source = self.root / "agent" / "roles" / "leader.md"
        original = "Follow the shared [rules](../shared/run-contract.md#rules)."
        for address in ("/tmp/missing-secret", "file:///tmp/missing-secret"):
            with self.subTest(address=address):
                source.write_text(
                    ROLE.replace(original,
                                 f"Follow the shared [unsafe][ref].\n\n[ref]: {address}"),
                    encoding="utf-8",
                )
                with self.assertRaisesRegex(ValueError, "absolute|file:|filesystem"):
                    expected_packages(self.root)

    def test_skills_check_refuses_absolute_and_file_links_in_source(self):
        build_packages(self.root)
        source = self.root / "agent" / "roles" / "leader.md"
        original = "Follow the shared [rules](../shared/run-contract.md#rules)."
        for address in ("/tmp/missing-secret", "file:///tmp/missing-secret"):
            with self.subTest(address=address):
                source.write_text(
                    ROLE.replace(original, f"Follow the shared [unsafe]({address})."),
                    encoding="utf-8",
                )
                problems = check_packages(self.root)
                self.assertTrue(
                    any("absolute" in error or "file:" in error or "filesystem" in error
                        for error in problems), problems,
                )

    def test_local_encoded_space_remains_url_encoded_in_inline_skill_link(self):
        notes = self.root / "docs" / "a space.md"
        notes.write_text("# A space\n", encoding="utf-8")
        source = self.root / "agent" / "roles" / "leader.md"
        source.write_text(
            ROLE.replace(
                "Follow the shared [rules](../shared/run-contract.md#rules).",
                "Follow the shared [notes](../../docs/a%20space.md).",
            ), encoding="utf-8",
        )
        build_packages(self.root)
        text = (self.package("astrid-dev-leader") / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("[notes](repo/docs/a%20space.md)", text)
        self.assertNotIn("[notes](repo/docs/a space.md)", text)
        self.assertEqual(check_packages(self.root), [])

    def test_local_encoded_space_remains_url_encoded_in_reference_definition(self):
        notes = self.root / "docs" / "a space.md"
        notes.write_text("# A space\n", encoding="utf-8")
        source = self.root / "agent" / "roles" / "leader.md"
        source.write_text(
            ROLE.replace(
                "Follow the shared [rules](../shared/run-contract.md#rules).",
                "Follow the shared [notes][notes-ref].\n\n"
                "[notes-ref]: ../../docs/a%20space.md",
            ), encoding="utf-8",
        )
        build_packages(self.root)
        text = (self.package("astrid-dev-leader") / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("[notes-ref]: repo/docs/a%20space.md", text)
        self.assertNotIn("[notes-ref]: repo/docs/a space.md", text)
        self.assertEqual(check_packages(self.root), [])

    def test_external_web_links_remain_unchanged(self):
        source = self.root / "agent" / "roles" / "leader.md"
        source.write_text(
            ROLE.replace(
                "Follow the shared [rules](../shared/run-contract.md#rules).",
                "Follow the shared [web](https://example.org/guide?x=1#usage).",
            ), encoding="utf-8",
        )
        build_packages(self.root)
        text = (self.package("astrid-dev-leader") / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("[web](https://example.org/guide?x=1#usage)", text)
        self.assertEqual(check_packages(self.root), [])

    def test_dangling_agent_symlink_never_retires_owned_packages(self):
        build_packages(self.root)
        before = {package.name: (package / "SKILL.md").read_bytes()
                  for package in (self.root / ".generated" / "skills").iterdir()}
        agent = self.root / "agent"
        agent.rename(self.root / "parked-agent")
        agent.symlink_to(self.root / "missing-agent", target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "real directory"):
            build_packages(self.root)
        self.assertTrue(any("real directory" in issue
                            for issue in check_packages(self.root)))
        for name, contents in before.items():
            self.assertEqual((self.package(name) / "SKILL.md").read_bytes(), contents)

    def test_undefined_full_collapsed_and_shortcut_references_refused(self):
        source = self.root / "agent" / "roles" / "leader.md"
        old = "Follow the shared [rules](../shared/run-contract.md#rules)."
        for usage in ("[rules][undefined]", "[undefined][]", "[undefined]"):
            with self.subTest(usage=usage):
                source.write_text(ROLE.replace(old, f"Follow the shared {usage}."),
                                  encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "undefined reference"):
                    expected_packages(self.root)

    def test_valid_full_collapsed_and_shortcut_references_are_supported(self):
        source = self.root / "agent" / "roles" / "leader.md"
        old = "Follow the shared [rules](../shared/run-contract.md#rules)."
        for usage in ("[rules][contract]", "[contract][]", "[contract]"):
            with self.subTest(usage=usage):
                source.write_text(
                    ROLE.replace(old, f"Follow the shared {usage}.\n\n"
                                 "[contract]: ../shared/run-contract.md#rules"),
                    encoding="utf-8")
                generated = expected_packages(self.root)["astrid-dev-leader"][0]
                self.assertIn("[contract]: repo/agent/shared/run-contract.md#rules",
                              generated)

    def test_multiline_reference_definition_is_rebased_and_checked(self):
        source = self.root / "agent" / "roles" / "leader.md"
        source.write_text(ROLE.replace(
            "Follow the shared [rules](../shared/run-contract.md#rules).",
            "Follow the shared [rules][contract].\n\n"
            "[contract]:\n  ../shared/run-contract.md#rules",
        ), encoding="utf-8")
        build_packages(self.root)
        generated = (self.package("astrid-dev-leader") / "SKILL.md").read_text()
        self.assertIn("[contract]:\n  repo/agent/shared/run-contract.md#rules",
                      generated)
        self.assertEqual(check_packages(self.root), [])

    def test_missing_multiline_reference_target_is_refused(self):
        source = self.root / "agent" / "roles" / "leader.md"
        source.write_text(ROLE.replace(
            "Follow the shared [rules](../shared/run-contract.md#rules).",
            "Follow the shared [rules][contract].\n\n"
            "[contract]:\n  ../shared/absent-contract.md",
        ), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "missing link target"):
            expected_packages(self.root)

    def test_inline_code_references_and_fake_links_are_literals(self):
        source = self.root / "agent" / "roles" / "leader.md"
        source.write_text(
            ROLE + "\nUse " + chr(96) + "[literal][undefined]" + chr(96)
            + " and " + chr(96) + "[example](missing.md)" + chr(96)
            + " as textual examples.\n", encoding="utf-8")
        build_packages(self.root)
        generated = (self.package("astrid-dev-leader") / "SKILL.md").read_text()
        self.assertIn(chr(96) + "[literal][undefined]" + chr(96), generated)
        self.assertIn(chr(96) + "[example](missing.md)" + chr(96), generated)

    def test_tilde_fenced_phantom_heading_cannot_satisfy_fragment(self):
        source = self.root / "agent" / "roles" / "leader.md"
        source.write_text(
            ROLE + "\n~~~markdown\n## Phantom Heading\n~~~\n"
            "\nSee [phantom](#phantom-heading).\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "missing heading"):
            expected_packages(self.root)

    def test_tilde_fenced_heading_in_target_cannot_satisfy_fragment(self):
        notes = self.root / "docs" / "notes.md"
        notes.write_text("# Notes\n\n~~~markdown\n## Phantom\n~~~\n",
                         encoding="utf-8")
        source = self.root / "agent" / "shared" / "workstreams" / "gap.md"
        source.write_text(STREAM.replace(
            "[notes](../../../docs/notes.md)",
            "[notes](../../../docs/notes.md#phantom)",
        ), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "missing heading"):
            expected_packages(self.root)

    def test_stale_marker_parent_traversal_is_not_ownership(self):
        build_packages(self.root)
        leader = self.package("astrid-dev-leader")
        (leader / ".astrid-dev-generated").write_text(
            "agent/../../outside.md\n", encoding="utf-8")
        (self.root / "agent" / "roles" / "leader.md").write_text(
            ROLE.replace("skill: true\n", ""), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "ownership marker"):
            build_packages(self.root)
        self.assertTrue(leader.is_dir())
        self.assertTrue(self.package("astrid-dev-start").is_dir())

    def test_stale_marker_source_mismatch_is_not_ownership(self):
        build_packages(self.root)
        leader = self.package("astrid-dev-leader")
        (leader / ".astrid-dev-generated").write_text(
            "agent/roles/other.md\n", encoding="utf-8")
        (self.root / "agent" / "roles" / "leader.md").write_text(
            ROLE.replace("skill: true\n", ""), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "ownership marker"):
            build_packages(self.root)
        self.assertTrue(leader.is_dir())

    def test_fenced_examples_are_not_rewritten(self):
        path = self.root / "agent" / "roles" / "leader.md"
        fence = chr(96) * 3
        path.write_text(ROLE + "\n" + fence + "markdown\n[Example](not-a-real-file.md)\n" + fence + "\n", encoding="utf-8")
        build_packages(self.root)
        text = (self.package("astrid-dev-leader") / "SKILL.md").read_text()
        self.assertIn("[Example](not-a-real-file.md)", text)

    def test_generated_folder_symlinks_refused(self):
        (self.root / ".generated").symlink_to(self.root / "agent", target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "cannot be a symlink"):
            build_packages(self.root)


    def test_nested_dangling_alias_preserves_output(self):
        build_packages(self.root)
        skill = self.package("astrid-dev-start") / "SKILL.md"
        before = skill.read_bytes()
        (self.root / "agent" / "missing-dir").symlink_to(self.root / "gone", target_is_directory=True)
        self.assertTrue(any("symlink" in issue for issue in check_packages(self.root)))
        with self.assertRaisesRegex(ValueError, "symlink"):
            build_packages(self.root)
        self.assertEqual(skill.read_bytes(), before)

    def test_parent_directory_builds_twice(self):
        folder = self.root / "agent" / "Team_Notes"
        folder.mkdir()
        (self.root / "agent" / "start.md").rename(folder / "start.md")
        build_packages(self.root)
        self.assertEqual(build_packages(self.root), [])
        self.assertEqual(check_packages(self.root), [])

    def test_empty_alt_rebases_and_missing_refuses(self):
        source = self.root / "agent" / "start.md"
        original = source.read_text()
        source.write_text(original + "\n![](../docs/notes.md)\n")
        build_packages(self.root)
        skill = self.package("astrid-dev-start") / "SKILL.md"
        self.assertIn("![](repo/docs/notes.md)", skill.read_text())
        before = skill.read_bytes()
        source.write_text(original + "\n![](missing.png)\n")
        with self.assertRaisesRegex(ValueError, "missing link target"):
            build_packages(self.root)
        self.assertEqual(skill.read_bytes(), before)

    def test_encoded_fragments_and_reference_destinations(self):
        source = self.root / "agent" / "start.md"
        original = source.read_text()
        (self.root / "docs" / "notes.md").write_text("# Café\n")
        source.write_text(original + "\n[one](../docs/notes.md#caf%C3%A9)\n[two](<../docs/notes.md>)\n[three][r]\n\n[r]:\n../docs/notes.md\n")
        build_packages(self.root)
        text = (self.package("astrid-dev-start") / "SKILL.md").read_text()
        self.assertIn("repo/docs/notes.md#caf%C3%A9", text)
        self.assertIn("<repo/docs/notes.md>", text)
        self.assertIn("[r]:\nrepo/docs/notes.md", text)
        source.write_text(original + "\n[bad](../docs/notes.md#absent)\n")
        with self.assertRaisesRegex(ValueError, "missing heading"):
            build_packages(self.root)
        source.write_text(original + "\n[bad](<../../outside>)\n")
        with self.assertRaisesRegex(ValueError, "escapes checkout"):
            build_packages(self.root)

    def test_multiline_code_and_quoted_fence_are_literals(self):
        source = self.root / "agent" / "start.md"
        source.write_text(source.read_text() + "\n`[literal]\nname`\n\n> ~~~\n> [example](missing.md)\n> ~~~\n\n[real](../docs/notes.md)\n")
        build_packages(self.root)
        text = (self.package("astrid-dev-start") / "SKILL.md").read_text()
        self.assertIn("`[literal]\nname`", text)
        self.assertIn("> [example](missing.md)", text)
        self.assertIn("[real](repo/docs/notes.md)", text)
        source.write_text(source.read_text() + "\n[bad](missing.md)\n")
        with self.assertRaisesRegex(ValueError, "missing link target"):
            build_packages(self.root)

    def test_failed_refresh_preserves_packages_and_retry_succeeds(self):
        build_packages(self.root)
        stale = self.package("astrid-dev-leader")
        active = self.package("astrid-dev-start") / "SKILL.md"
        before = active.read_bytes()
        (self.root / "agent" / "roles" / "leader.md").write_text(ROLE.replace("skill: true\n", ""))
        start = self.root / "agent" / "start.md"
        start.write_text(start.read_text() + "\nChanged.\n")
        real_open = Path.open
        def fail_refresh(path, *args, **kwargs):
            if path.resolve() == active.resolve() and args and args[0] == "r+":
                raise PermissionError("refused refresh")
            return real_open(path, *args, **kwargs)
        with patch.object(Path, "open", fail_refresh):
            with self.assertRaisesRegex(PermissionError, "refused refresh"):
                build_packages(self.root)
        self.assertTrue(stale.is_dir())
        self.assertEqual(active.read_bytes(), before)
        build_packages(self.root)
        self.assertFalse(stale.exists())
        self.assertIn("Changed.", active.read_text())
        self.assertEqual(check_packages(self.root), [])


    def test_escaped_and_angle_destinations(self):
        source = self.root / "agent" / "start.md"
        original = source.read_text()
        (self.root / "docs" / "note(1).md").write_text("# Note\n")
        (self.root / "docs" / "with space.md").write_text("# Note\n")
        source.write_text(original + r"\n[escaped](../docs/note\(1\).md)\n[angle](<../docs/with space.md>)\n[ref][r]\n\n[r]: <../docs/with space.md>\n".replace(r"\n", "\n"))
        build_packages(self.root)
        text = (self.package("astrid-dev-start") / "SKILL.md").read_text()
        self.assertIn("[escaped](repo/docs/note%281%29.md)", text)
        self.assertIn("[angle](<repo/docs/with%20space.md>)", text)
        self.assertIn("[r]: <repo/docs/with%20space.md>", text)
        source.write_text(original + r"\n[bad](../docs/missing\(1\).md)\n".replace(r"\n", "\n"))
        with self.assertRaisesRegex(ValueError, "missing link target"):
            build_packages(self.root)

    def test_list_and_unclosed_quote_fences_do_not_hide_adjacent_links(self):
        source = self.root / "agent" / "start.md"
        original = source.read_text()
        body = "\n- ~~~\n  [example](missing.md)\n  ~~~\n\n> ~~~\n> [quoted](missing.md)\n\n[real](../docs/notes.md)\n"
        source.write_text(original + body)
        build_packages(self.root)
        text = (self.package("astrid-dev-start") / "SKILL.md").read_text()
        self.assertIn("[example](missing.md)", text)
        self.assertIn("[quoted](missing.md)", text)
        self.assertIn("[real](repo/docs/notes.md)", text)
        source.write_text(original + body + "\n[bad](missing.md)\n")
        with self.assertRaisesRegex(ValueError, "missing link target"):
            build_packages(self.root)

    def test_unmatched_code_delimiters_cannot_hide_link_across_paragraphs(self):
        source = self.root / "agent" / "start.md"
        source.write_text(source.read_text() + "\nUnclosed ` example.\n\n[bad](missing.md) and ` later.\n")
        with self.assertRaisesRegex(ValueError, "missing link target"):
            build_packages(self.root)


    def test_second_update_failure_rolls_back_whole_package_set(self):
        build_packages(self.root)
        output = self.root / ".generated" / "skills"
        def snapshot():
            result = {}
            for item in sorted(output.rglob("*")):
                key = str(item.relative_to(output))
                result[key] = ("link", os.readlink(item)) if item.is_symlink() else (
                    ("file", item.read_bytes()) if item.is_file() else ("dir",))
            return result
        before = snapshot()
        for path in (self.root / "agent" / "roles" / "leader.md", self.root / "agent" / "start.md"):
            path.write_text(path.read_text() + "\nChanged.\n")
        second = self.package("astrid-dev-start") / "SKILL.md"
        real_open = Path.open
        def fail_second(path, *args, **kwargs):
            if path.resolve() == second.resolve() and args and args[0] in ("r+", "w"):
                raise PermissionError("second update refused")
            return real_open(path, *args, **kwargs)
        with patch.object(Path, "open", fail_second):
            with self.assertRaisesRegex(PermissionError, "second update refused"):
                build_packages(self.root)
        self.assertEqual(snapshot(), before)
        build_packages(self.root)
        self.assertEqual(check_packages(self.root), [])


    def test_second_staged_update_failure_keeps_original_tree(self):
        build_packages(self.root)
        output = self.root / ".generated" / "skills"
        def snapshot():
            return {str(p.relative_to(output)): (("link", os.readlink(p)) if p.is_symlink()
                    else ("file", p.read_bytes()) if p.is_file() else ("dir",))
                    for p in sorted(output.rglob("*"))}
        before = snapshot()
        for source in (self.root / "agent" / "roles" / "leader.md", self.root / "agent" / "start.md"):
            source.write_text(source.read_text() + "\nChanged.\n")
        real_replace = os.replace
        writes = []
        def fail_second(src, dst):
            dst = Path(dst)
            if dst.name == "SKILL.md" and ".skills-build-" in str(dst):
                writes.append(dst.parent.name)
                if len(writes) == 2:
                    raise PermissionError("second staged update failed")
            return real_replace(src, dst)
        with patch("skill_builder.os.replace", side_effect=fail_second):
            with self.assertRaisesRegex(PermissionError, "second staged update"):
                build_packages(self.root)
        self.assertEqual(writes, ["astrid-dev-leader", "astrid-dev-start"])
        self.assertEqual(snapshot(), before)
        build_packages(self.root)
        self.assertEqual(check_packages(self.root), [])

    def test_publication_failure_restores_prior_tree(self):
        from skill_builder import _exchange_paths
        build_packages(self.root)
        output = (self.root / ".generated" / "skills").resolve()
        skill = output / "astrid-dev-start" / "SKILL.md"
        marker = output / "astrid-dev-start" / ".astrid-dev-generated"
        link = output / "astrid-dev-start" / "repo"
        before = (skill.read_bytes(), marker.read_bytes(), os.readlink(link))
        source = self.root / "agent" / "start.md"
        source.write_text(source.read_text() + "\nChanged.\n")
        def fail_publish(left, right):
            if left == output:
                raise OSError("publish failed")
            return _exchange_paths(left, right)
        with patch("skill_builder._exchange_paths", side_effect=fail_publish):
            with self.assertRaisesRegex(OSError, "publish failed"):
                build_packages(self.root)
        self.assertEqual((skill.read_bytes(), marker.read_bytes(), os.readlink(link)), before)
        build_packages(self.root)
        self.assertEqual(check_packages(self.root), [])

    def test_crash_before_or_after_exchange_keeps_public_generation_and_recovers(self):
        build_packages(self.root)
        source = self.root / "agent" / "start.md"
        output = self.root / ".generated" / "skills"
        skill = output / "astrid-dev-start" / "SKILL.md"
        old = skill.read_bytes()
        source.write_text(source.read_text() + "\nChanged.\n")
        child = """from pathlib import Path
import os, sys
import skill_builder as b
root = Path(sys.argv[1]).resolve()
phase = sys.argv[2]
original = b._exchange_paths
def crash(left, right):
    if left == root / b.OUTPUT:
        if phase == 'before': os._exit(71)
        original(left, right)
        os._exit(72)
    original(left, right)
b._exchange_paths = crash
b.build_packages(root)
"""
        for phase, expected_exit in (("before", 71), ("after", 72)):
            with self.subTest(phase=phase):
                result = subprocess.run([sys.executable, "-c", child, str(self.root), phase],
                                        cwd=Path(__file__).parent, check=False)
                self.assertEqual(result.returncode, expected_exit)
                self.assertTrue(output.is_dir())
                self.assertFalse(output.is_symlink())
                if phase == "before":
                    self.assertEqual(skill.read_bytes(), old)
                else:
                    self.assertIn(b"Changed.", skill.read_bytes())
                self.assertTrue((output / "astrid-dev-start" / "repo").is_symlink())
        build_packages(self.root)
        self.assertEqual(check_packages(self.root), [])

    def test_lock_conflict_and_changed_source_refuse_stale_publish(self):
        from skill_builder import _build_lock, _build_output
        build_packages(self.root)
        output = self.root / ".generated" / "skills"
        skill = output / "astrid-dev-start" / "SKILL.md"
        before = skill.read_bytes()
        source = self.root / "agent" / "start.md"
        source.write_text(source.read_text() + "\nFirst.\n")
        with _build_lock(output.parent.resolve()):
            with self.assertRaisesRegex(RuntimeError, "another skill build"):
                build_packages(self.root)
        def change_source(stage, expected):
            result = _build_output(stage, expected)
            source.write_text(source.read_text() + "\nLater.\n")
            return result
        with patch("skill_builder._build_output", side_effect=change_source):
            with self.assertRaisesRegex(RuntimeError, "sources changed"):
                build_packages(self.root)
        self.assertEqual(skill.read_bytes(), before)
        build_packages(self.root)
        self.assertIn("Later.", skill.read_text())
        self.assertEqual(check_packages(self.root), [])

    def test_unsupported_exchange_and_foreign_lock_fail_closed(self):
        build_packages(self.root)
        output = self.root / ".generated" / "skills"
        skill = output / "astrid-dev-start" / "SKILL.md"
        before = skill.read_bytes()
        source = self.root / "agent" / "start.md"
        source.write_text(source.read_text() + "\nChanged.\n")
        with patch("skill_builder._exchange_paths", side_effect=OSError("unsupported")):
            with self.assertRaisesRegex(OSError, "unsupported"):
                build_packages(self.root)
        self.assertEqual(skill.read_bytes(), before)
        lock = output.parent / ".skills-build.lock"
        lock.write_text("foreign lock")
        with self.assertRaisesRegex(ValueError, "foreign skill build lock"):
            build_packages(self.root)
        self.assertEqual(lock.read_text(), "foreign lock")
        self.assertEqual(skill.read_bytes(), before)

    def test_exchange_keeps_live_path_available_to_concurrent_reader(self):
        from skill_builder import expected_packages
        build_packages(self.root)
        output = self.root / ".generated" / "skills"
        skill = output / "astrid-dev-start" / "SKILL.md"
        source = self.root / "agent" / "start.md"
        initial = source.read_text()
        expected_contents = {skill.read_text()}
        for i in range(8):
            source.write_text(initial + f"\nRevision {i}.\n")
            expected_contents.add(expected_packages(self.root)["astrid-dev-start"][0])
        source.write_text(initial)
        stop = threading.Event()
        started = threading.Event()
        seen = []
        errors = []
        def reader():
            while not stop.is_set():
                try:
                    seen.append(skill.read_text())
                    started.set()
                except OSError as exc:
                    errors.append(repr(exc))
                    started.set()
        thread = threading.Thread(target=reader)
        thread.start()
        try:
            self.assertTrue(started.wait(3))
            for i in range(8):
                source.write_text(initial + f"\nRevision {i}.\n")
                build_packages(self.root)
        finally:
            stop.set()
            thread.join(timeout=3)
        self.assertFalse(thread.is_alive())
        self.assertTrue(seen)
        self.assertEqual(errors, [])
        self.assertTrue(all(item in expected_contents for item in seen))
        self.assertEqual(check_packages(self.root), [])

    def test_lock_symlink_and_unsupported_first_publish_refuse(self):
        output = self.root / ".generated" / "skills"
        with patch("skill_builder._exchange_paths", side_effect=OSError("unsupported")):
            with self.assertRaisesRegex(OSError, "unsupported"):
                build_packages(self.root)
        self.assertFalse(output.exists())
        lock = output.parent / ".skills-build.lock"
        lock.unlink()
        with TemporaryDirectory() as temp:
            foreign = Path(temp) / "foreign"
            foreign.write_text("keep")
            lock.symlink_to(foreign)
            with self.assertRaises(OSError):
                build_packages(self.root)
            self.assertEqual(foreign.read_text(), "keep")
            self.assertFalse(output.exists())

    def test_second_process_is_refused_while_lock_holder_is_alive(self):
        build_packages(self.root)
        output = self.root / ".generated" / "skills"
        skill = output / "astrid-dev-start" / "SKILL.md"
        before = skill.read_bytes()
        source = self.root / "agent" / "start.md"
        source.write_text(source.read_text() + "\nChanged.\n")
        child = """from pathlib import Path
import sys
from skill_builder import _build_lock
with _build_lock(Path(sys.argv[1]).resolve()):
    print('locked', flush=True)
    sys.stdin.read(1)
"""
        process = subprocess.Popen([sys.executable, "-c", child, str(output.parent)],
                                   cwd=Path(__file__).parent, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            readable, _, _ = select.select([process.stdout], [], [], 5)
            self.assertTrue(readable, "lock holder did not start")
            self.assertEqual(process.stdout.readline().strip(), "locked")
            with self.assertRaisesRegex(RuntimeError, "another skill build"):
                build_packages(self.root)
            self.assertEqual(skill.read_bytes(), before)
            process.stdin.write("x")
            process.stdin.flush()
            self.assertEqual(process.wait(timeout=5), 0)
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()
            process.stdin.close()
            process.stdout.close()
            process.stderr.close()
        build_packages(self.root)
        self.assertEqual(check_packages(self.root), [])

    def test_existing_install_symlink_survives_exchange(self):
        build_packages(self.root)
        output = self.root / ".generated" / "skills"
        package = output / "astrid-dev-start"
        install = self.root / "install"
        install.mkdir()
        (install / "astrid-dev-start").symlink_to(package, target_is_directory=True)
        source = self.root / "agent" / "start.md"
        source.write_text(source.read_text() + "\nUpdated.\n")
        build_packages(self.root)
        self.assertFalse(output.is_symlink())
        self.assertFalse(package.is_symlink())
        self.assertIn("Updated.", (install / "astrid-dev-start" / "SKILL.md").read_text())
        self.assertEqual((install / "astrid-dev-start" / "repo" / "agent" / "start.md").resolve(), source.resolve())
        self.assertEqual(check_packages(self.root), [])

    def test_lock_setup_crash_leaves_usable_complete_lock(self):
        parent = self.root / ".generated"
        parent.mkdir()
        child = """from pathlib import Path
import os, sys
import skill_builder as b
real = os.link
def crash(*args, **kwargs):
    real(*args, **kwargs)
    os._exit(73)
b.os.link = crash
with b._build_lock(Path(sys.argv[1])):
    pass
"""
        result = subprocess.run([sys.executable, "-c", child, str(parent)],
                                cwd=Path(__file__).parent, check=False)
        self.assertEqual(result.returncode, 73)
        self.assertEqual((parent / ".skills-build.lock").stat().st_nlink, 2)
        build_packages(self.root)
        self.assertEqual(check_packages(self.root), [])

    def test_unexpected_output_during_first_build_is_preserved(self):
        from skill_builder import _build_output
        output = self.root / ".generated" / "skills"
        def foreign_appears(stage, expected):
            actions = _build_output(stage, expected)
            output.mkdir()
            (output / "foreign").write_text("keep")
            return actions
        with patch("skill_builder._build_output", side_effect=foreign_appears):
            with self.assertRaisesRegex(RuntimeError, "output changed"):
                build_packages(self.root)
        self.assertEqual((output / "foreign").read_text(), "keep")

    def test_post_publication_cleanup_failure_reports_committed_generation(self):
        from skill_builder import _build_lock
        build_packages(self.root)
        source = self.root / "agent" / "start.md"
        source.write_text(source.read_text() + "\nPublished.\n")
        @contextmanager
        def fail_after_lock(parent):
            with _build_lock(parent):
                yield
            raise OSError("finalization failure")
        with patch("skill_builder._build_lock", fail_after_lock):
            with self.assertRaisesRegex(OSError, "published.*finalization") as caught:
                build_packages(self.root)
        self.assertIsInstance(caught.exception.__cause__, OSError)
        skill = self.package("astrid-dev-start") / "SKILL.md"
        self.assertIn("Published.", skill.read_text())
        self.assertEqual(check_packages(self.root), [])

    def test_installed_symlink_polling_during_repeated_exchanges(self):
        build_packages(self.root)
        package = self.package("astrid-dev-start")
        install = self.root / "install"
        install.mkdir()
        link = install / "astrid-dev-start"
        link.symlink_to(package, target_is_directory=True)
        source = self.root / "agent" / "start.md"
        initial = source.read_text()
        valid = {(link / "SKILL.md").read_text()}
        for i in range(8):
            source.write_text(initial + f"\nVersion {i}.\n")
            valid.add(expected_packages(self.root)["astrid-dev-start"][0])
        source.write_text(initial)
        stop, started = threading.Event(), threading.Event()
        seen, errors = [], []
        def reader():
            while not stop.is_set():
                try:
                    seen.append((link / "SKILL.md").read_text())
                    if not (link / "repo" / "agent" / "start.md").is_file():
                        errors.append("installed repo link unavailable")
                    started.set()
                except OSError as exc:
                    errors.append(repr(exc))
                    started.set()
        thread = threading.Thread(target=reader)
        thread.start()
        try:
            self.assertTrue(started.wait(3))
            for i in range(8):
                source.write_text(initial + f"\nVersion {i}.\n")
                build_packages(self.root)
        finally:
            stop.set()
            thread.join(timeout=3)
        self.assertFalse(thread.is_alive())
        self.assertTrue(seen)
        self.assertEqual(errors, [])
        self.assertTrue(all(item in valid for item in seen))
        self.assertEqual(check_packages(self.root), [])

    def test_two_real_builders_contend_before_publication(self):
        build_packages(self.root)
        source = self.root / "agent" / "start.md"
        source.write_text(source.read_text() + "\nChanged.\n")
        skill = self.package("astrid-dev-start") / "SKILL.md"
        before = skill.read_bytes()
        child = """from pathlib import Path
import sys
import skill_builder as b
original = b._build_output
def pause(stage, expected):
    result = original(stage, expected)
    print('staged', flush=True)
    sys.stdin.read(1)
    return result
b._build_output = pause
b.build_packages(Path(sys.argv[1]))
"""
        process = subprocess.Popen([sys.executable, "-c", child, str(self.root)],
                                   cwd=Path(__file__).parent, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            readable, _, _ = select.select([process.stdout], [], [], 5)
            self.assertTrue(readable, "first builder did not stage")
            self.assertEqual(process.stdout.readline().strip(), "staged")
            with self.assertRaisesRegex(RuntimeError, "another skill build"):
                build_packages(self.root)
            self.assertEqual(skill.read_bytes(), before)
            process.stdin.write("x")
            process.stdin.flush()
            self.assertEqual(process.wait(timeout=5), 0)
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()
            process.stdin.close()
            process.stdout.close()
            process.stderr.close()
        self.assertIn("Changed.", skill.read_text())
        self.assertEqual(check_packages(self.root), [])

    def test_crash_orphans_are_preserved_and_not_followed(self):
        build_packages(self.root)
        source = self.root / "agent" / "start.md"
        source.write_text(source.read_text() + "\nChanged.\n")
        child = """from pathlib import Path
import os, sys
import skill_builder as b
root = Path(sys.argv[1]).resolve()
original = b._exchange_paths
def crash(left, right):
    if left == root / b.OUTPUT: os._exit(71)
    original(left, right)
b._exchange_paths = crash
b.build_packages(root)
"""
        process = subprocess.run([sys.executable, "-c", child, str(self.root)],
                                 cwd=Path(__file__).parent, check=False)
        self.assertEqual(process.returncode, 71)
        parent = self.root / ".generated"
        orphans = list(parent.glob(".skills-build-*"))
        self.assertEqual(len(orphans), 1)
        artifact = orphans[0] / "skills" / "astrid-dev-start" / "SKILL.md"
        before = artifact.read_bytes()
        with TemporaryDirectory() as temp:
            foreign = Path(temp) / "foreign"
            foreign.mkdir()
            (foreign / "keep").write_text("safe")
            (parent / ".skills-build-foreign").symlink_to(foreign, target_is_directory=True)
            build_packages(self.root)
            self.assertEqual(artifact.read_bytes(), before)
            self.assertTrue((parent / ".skills-build-foreign").is_symlink())
            self.assertEqual((foreign / "keep").read_text(), "safe")
        self.assertEqual(check_packages(self.root), [])

    def test_crash_after_exchange_retains_old_recovery_material(self):
        build_packages(self.root)
        package = self.package("astrid-dev-start")
        old = ((package / "SKILL.md").read_bytes(),
               (package / ".astrid-dev-generated").read_bytes(),
               os.readlink(package / "repo"))
        source = self.root / "agent" / "start.md"
        source.write_text(source.read_text() + "\nChanged.\n")
        child = """from pathlib import Path
import os, sys
import skill_builder as b
root = Path(sys.argv[1]).resolve()
original = b._exchange_paths
def crash(left, right):
    original(left, right)
    if left == root / b.OUTPUT: os._exit(72)
b._exchange_paths = crash
b.build_packages(root)
"""
        result = subprocess.run([sys.executable, "-c", child, str(self.root)],
                                cwd=Path(__file__).parent, check=False)
        self.assertEqual(result.returncode, 72)
        self.assertIn("Changed.", (package / "SKILL.md").read_text())
        self.assertEqual((package / "repo" / "agent" / "start.md").resolve(), source.resolve())
        orphans = list((self.root / ".generated").glob(".skills-build-*/skills/astrid-dev-start"))
        self.assertEqual(len(orphans), 1)
        orphan = orphans[0]
        self.assertEqual(((orphan / "SKILL.md").read_bytes(),
                          (orphan / ".astrid-dev-generated").read_bytes(),
                          os.readlink(orphan / "repo")), old)
        build_packages(self.root)
        self.assertTrue(orphan.is_dir())
        self.assertEqual(check_packages(self.root), [])

    def test_interrupted_first_publication_can_retry(self):
        parent = self.root / ".generated"
        output = parent / "skills"
        child = """from pathlib import Path
import os, sys
import skill_builder as b
root = Path(sys.argv[1]).resolve()
original = b._exchange_paths
def crash(left, right):
    if left == root / b.OUTPUT: os._exit(71)
    original(left, right)
b._exchange_paths = crash
b.build_packages(root)
"""
        result = subprocess.run([sys.executable, "-c", child, str(self.root)],
                                cwd=Path(__file__).parent, check=False)
        self.assertEqual(result.returncode, 71)
        self.assertTrue(output.is_dir())
        self.assertEqual(list(output.iterdir()), [])
        build_packages(self.root)
        self.assertEqual(check_packages(self.root), [])

    def test_quoted_reference_definition_rewrites_and_refuses_missing(self):
        source = self.root / "agent" / "start.md"
        original = source.read_text()
        source.write_text(original + "\n> [read][r]\n>\n> [r]: ../docs/notes.md\n")
        build_packages(self.root)
        text = (self.package("astrid-dev-start") / "SKILL.md").read_text()
        self.assertIn("> [r]: repo/docs/notes.md", text)
        source.write_text(original + "\n> [read][r]\n>\n> [r]: missing.md\n")
        with self.assertRaisesRegex(ValueError, "missing link target"):
            build_packages(self.root)

    def test_balanced_parentheses_in_destination(self):
        source = self.root / "agent" / "start.md"
        original = source.read_text()
        (self.root / "docs" / "note(1).md").write_text("# Note\n")
        source.write_text(original + "\n[read](../docs/note(1).md)\n")
        build_packages(self.root)
        self.assertIn("[read](repo/docs/note%281%29.md)", (self.package("astrid-dev-start") / "SKILL.md").read_text())
        source.write_text(original + "\n[bad](../../outside(1).md)\n")
        with self.assertRaisesRegex(ValueError, "escapes checkout"):
            build_packages(self.root)



    def test_nested_container_matrix_and_escaped_reference(self):
        source = self.root / "agent" / "start.md"
        original = source.read_text()
        (self.root / "docs" / "note(1).md").write_text("# Note\n")
        body = ("> - ~~~\n>   [literal](missing.md)\n>   ~~~\n\n"
                "- item\n  - ~~~\n    [literal](missing.md)\n    ~~~\n\n"
                "``[literal]\nmore`` and [real][r]\n\n"
                "[r]: ../docs/note\\(1\\).md\n")
        source.write_text(original + "\n" + body)
        build_packages(self.root)
        text = (self.package("astrid-dev-start") / "SKILL.md").read_text()
        self.assertIn("[literal](missing.md)", text)
        self.assertIn("[r]: repo/docs/note%281%29.md", text)
        self.assertIn("``[literal]\nmore``", text)
        for destination in (r"..\/../outside.md", "%2e%2e/%2e%2e/outside.md"):
            source.write_text(original + "\n[bad](" + destination + ")\n")
            with self.assertRaisesRegex(ValueError, "escapes checkout"):
                build_packages(self.root)


    def test_top_level_indented_code_and_adjacent_live_links(self):
        source = self.root / "agent" / "start.md"
        original = source.read_text()
        body = ("\n    [one](missing.md)\n    [two](missing.md)\n\n"
                "    [three](missing.md)\n\n[real](../docs/notes.md)\n")
        source.write_text(original + body)
        build_packages(self.root)
        text = (self.package("astrid-dev-start") / "SKILL.md").read_text()
        self.assertIn("    [one](missing.md)", text)
        self.assertIn("    [three](missing.md)", text)
        self.assertIn("[real](repo/docs/notes.md)", text)
        source.write_text(original + body + "\n[bad](missing.md)\n")
        with self.assertRaisesRegex(ValueError, "missing link target"):
            build_packages(self.root)
        source.write_text(original + "\n    ## Fake\n\n[bad](#fake)\n")
        with self.assertRaisesRegex(ValueError, "missing heading"):
            build_packages(self.root)

    def test_paragraph_and_list_continuations_stay_live(self):
        source = self.root / "agent" / "start.md"
        original = source.read_text()
        for body in ("Paragraph\n    [bad](missing.md)",
                     "- item\n\n    [bad](missing.md)",
                     "- item\n  - nested\n\n    [bad](missing.md)",
                     "-     item\n\n    [bad](missing.md)",
                     "1.     item\n\n    [bad](missing.md)"):
            with self.subTest(body=body):
                source.write_text(original + "\n" + body + "\n")
                with self.assertRaisesRegex(ValueError, "missing link target"):
                    build_packages(self.root)
        source.write_text(original + "\n- item\n\n    [bad](../../outside.md)\n")
        with self.assertRaisesRegex(ValueError, "escapes checkout"):
            build_packages(self.root)

    def test_top_level_code_after_closed_list(self):
        source = self.root / "agent" / "start.md"
        source.write_text(source.read_text() + "\n- item\n\nprose\n\n    [literal](missing.md)\n\n[real](../docs/notes.md)\n")
        build_packages(self.root)
        text = (self.package("astrid-dev-start") / "SKILL.md").read_text()
        self.assertIn("    [literal](missing.md)", text)
        self.assertIn("[real](repo/docs/notes.md)", text)


    def test_quoted_and_tab_indented_code_with_adjacent_links(self):
        source = self.root / "agent" / "start.md"
        original = source.read_text()
        cases = (">     [literal](missing.md)\n\n[real](../docs/notes.md)",
                 "> paragraph\n>\n>     [literal](missing.md)\n\n[real](../docs/notes.md)",
                 "\t[literal](missing.md)\n\n[real](../docs/notes.md)",
                 "  \t[literal](missing.md)\n\n[real](../docs/notes.md)")
        for body in cases:
            with self.subTest(body=body):
                source.write_text(original + "\n" + body + "\n")
                build_packages(self.root)
                text = (self.package("astrid-dev-start") / "SKILL.md").read_text()
                self.assertIn("[literal](missing.md)", text)
                self.assertIn("[real](repo/docs/notes.md)", text)
                source.write_text(original + "\n" + body + "\n\n[bad](missing.md)\n")
                with self.assertRaisesRegex(ValueError, "missing link target"):
                    build_packages(self.root)

    def test_quoted_and_tab_list_continuations_remain_live(self):
        source = self.root / "agent" / "start.md"
        original = source.read_text()
        cases = ("> paragraph\n>     [bad](missing.md)",
                 "> - item\n>\n>     [bad](missing.md)",
                 "paragraph\n\t[bad](missing.md)",
                 "- item\n\n\t[bad](missing.md)",
                 "- item\n  - nested\n\n      [bad](missing.md)")
        for body in cases:
            with self.subTest(body=body):
                source.write_text(original + "\n" + body + "\n")
                with self.assertRaisesRegex(ValueError, "missing link target"):
                    build_packages(self.root)
        for body in ("- item\n\n\t[bad](../../outside.md)",
                     "- item\nlazy continuation\n\n    [bad](../../outside.md)"):
            source.write_text(original + "\n" + body + "\n")
            with self.assertRaisesRegex(ValueError, "escapes checkout"):
                build_packages(self.root)


    def test_list_contained_indented_code_matrix(self):
        source = self.root / "agent" / "start.md"
        original = source.read_text()
        bodies = ("- item\n\n      [literal](missing.md)",
                  "12. item\n\n        [literal](missing.md)",
                  "- item\n  - nested\n\n        [literal](missing.md)",
                  "> - item\n>\n>       [literal](missing.md)",
                  "- item\n\n\t\t[literal](missing.md)")
        for body in bodies:
            with self.subTest(body=body):
                source.write_text(original + "\n" + body + "\n\n[real](../docs/notes.md)\n")
                build_packages(self.root)
                text = (self.package("astrid-dev-start") / "SKILL.md").read_text()
                self.assertIn("[literal](missing.md)", text)
                self.assertIn("[real](repo/docs/notes.md)", text)

    def test_list_code_does_not_hide_live_links_or_traversal(self):
        source = self.root / "agent" / "start.md"
        original = source.read_text()
        bodies = ("- item\n\n    [bad](missing.md)",
                  "- item\n      [bad](missing.md)",
                  "- item\nlazy continuation\n\n    [bad](missing.md)",
                  "12. item\n\n    [bad](missing.md)",
                  "- item\n  - nested\n\n      [bad](missing.md)",
                  "> - item\n>\n>     [bad](missing.md)",
                  "> 1.\titem\n>\n>         [bad](missing.md)",
                  "- item\n\n\t[bad](missing.md)",
                  "- item\n  - nested\n\n        [literal](missing.md)\n\n    [bad](missing.md)")
        for body in bodies:
            with self.subTest(body=body):
                source.write_text(original + "\n" + body + "\n")
                with self.assertRaisesRegex(ValueError, "missing link target"):
                    build_packages(self.root)
        for body in ("- item\n\n\t[bad](../../outside.md)",
                     "- item\nlazy continuation\n\n    [bad](../../outside.md)"):
            source.write_text(original + "\n" + body + "\n")
            with self.assertRaisesRegex(ValueError, "escapes checkout"):
                build_packages(self.root)


    def test_quoted_tab_code_uses_physical_columns(self):
        source = self.root / "agent" / "start.md"
        original = source.read_text()
        bodies = ("> \t\t[literal](missing.md)",
                  "> -\titem\n>\n>       [literal](missing.md)",
                  "> 1.\titem\n>\n>           [literal](missing.md)",
                  "> - item\n>\n> \t\t[literal](missing.md)",
                  "> \t\t[undefined]",
                  "> -\titem\n>\n>       [undefined]")
        for body in bodies:
            with self.subTest(body=body):
                source.write_text(original + "\n" + body + "\n\n[real](../docs/notes.md)\n")
                build_packages(self.root)
                text = (self.package("astrid-dev-start") / "SKILL.md").read_text()
                self.assertIn("[real](repo/docs/notes.md)", text)
                self.assertIn("[literal](missing.md)" if "literal" in body else "[undefined]", text)

    def test_quoted_tab_live_links_keep_safety_refusals(self):
        source = self.root / "agent" / "start.md"
        original = source.read_text()
        with TemporaryDirectory() as temp:
            outside = Path(temp) / "outside.md"
            outside.write_text("# Outside\n")
            (self.root / "docs" / "outside.md").symlink_to(outside)
            cases = (("missing.md", "missing link target"),
                     ("../../outside.md", "escapes checkout"),
                     ("%2e%2e/%2e%2e/outside.md", "escapes checkout"),
                     ("/absolute/path", "absolute filesystem"),
                     ("file:///tmp/outside", "file:"),
                     ("C:/outside.md", "absolute filesystem"),
                     ("../docs/outside.md", "escapes checkout"))
            for destination, message in cases:
                with self.subTest(destination=destination):
                    source.write_text(original + "> 1.\titem\n>\n>         [bad](" + destination + ")\n")
                    with self.assertRaisesRegex(ValueError, message):
                        build_packages(self.root)


    def test_immediate_quote_tabs_and_closed_quote_list_literals(self):
        source = self.root / "agent" / "start.md"
        original = source.read_text()
        bodies = (">\t\t[literal](missing.md)",
                  ">\t\t\t[literal](missing.md)",
                  ">\t\t[undefined]",
                  "> - item\n\n>     [literal](missing.md)",
                  "> - item\n\n>     [undefined]",
                  "> - item\n\n    [literal](missing.md)")
        for body in bodies:
            with self.subTest(body=body):
                source.write_text(original + "\n" + body + "\n\n[real](../docs/notes.md)\n")
                build_packages(self.root)
                text = (self.package("astrid-dev-start") / "SKILL.md").read_text()
                self.assertIn("[real](repo/docs/notes.md)", text)
                self.assertIn("[undefined]" if "undefined" in body else "[literal](missing.md)", text)

    def test_open_quote_list_and_immediate_tab_live_links_are_checked(self):
        source = self.root / "agent" / "start.md"
        original = source.read_text()
        for body in (">\t[bad](missing.md)",
                     "> paragraph\n>\t\t[bad](missing.md)",
                     ">\t- item\n>\n>\t\t[bad](missing.md)",
                     ">\t1. item\n>\n>\t\t[bad](missing.md)",
                     "> - item\n>\n>     [bad](missing.md)",
                     "> - item\n> lazy\n>\n>     [bad](missing.md)"):
            with self.subTest(body=body):
                source.write_text(original + "\n" + body + "\n")
                with self.assertRaisesRegex(ValueError, "missing link target"):
                    build_packages(self.root)
        for dest in ("../../outside.md", "%2e%2e/%2e%2e/outside.md"):
            for prefix in ("> - item\n>\n>     ", ">\t- item\n>\n>\t\t"):
                source.write_text(original + prefix + "[bad](" + dest + ")\n")
                with self.assertRaisesRegex(ValueError, "escapes checkout"):
                    build_packages(self.root)


    def test_quote_tab_prefixed_list_code_physical_columns(self):
        source = self.root / "agent" / "start.md"
        original = source.read_text()
        cases = (">\t- item\n>\n>         [literal](missing.md)",
                 ">\t- item\n>\n>\t\t\t[literal](missing.md)",
                 ">\t- item\n>\n>         [undefined]",
                 ">\t1. item\n>\n>          [literal](missing.md)")
        for body in cases:
            with self.subTest(body=body):
                source.write_text(original + "\n" + body + "\n\n[real](../docs/notes.md)\n")
                build_packages(self.root)
                text = (self.package("astrid-dev-start") / "SKILL.md").read_text()
                self.assertIn("[real](repo/docs/notes.md)", text)
                self.assertIn("[undefined]" if "undefined" in body else "[literal](missing.md)", text)

    def test_quote_tab_prefixed_numbered_list_live_link_safety(self):
        source = self.root / "agent" / "start.md"
        original = source.read_text()
        with TemporaryDirectory() as temp:
            outside = Path(temp) / "outside.md"
            outside.write_text("# Outside\n")
            (self.root / "docs" / "outside.md").symlink_to(outside)
            cases = (("missing.md", "missing link target"),
                     ("../../outside.md", "escapes checkout"),
                     ("%2e%2e/%2e%2e/outside.md", "escapes checkout"),
                     ("/absolute/path", "absolute filesystem"),
                     ("file:///tmp/outside", "file:"),
                     ("C:/outside.md", "absolute filesystem"),
                     ("../docs/outside.md", "escapes checkout"))
            for dest, message in cases:
                with self.subTest(dest=dest):
                    source.write_text(original + ">\t1. item\n>\n>         [bad](" + dest + ")\n")
                    with self.assertRaisesRegex(ValueError, message):
                        build_packages(self.root)
                    source.write_text(original + ">  \t- item\n>\n>        [bad](" + dest + ")\n")
                    with self.assertRaisesRegex(ValueError, message):
                        build_packages(self.root)


    def test_generated_marker_and_lock_identity_bytes_are_stable(self):
        from skill_builder import MARKER, _LOCK_CONTENT

        self.assertEqual(MARKER, ".astrid-dev-generated")
        self.assertEqual(_LOCK_CONTENT, b"astrid-dev-skill-build-lock-v1\n")
        build_packages(self.root)
        marker = self.package("astrid-dev-leader") / MARKER
        self.assertEqual(marker.read_bytes(), b"agent/roles/leader.md\n")

    def test_stale_generated_skill_diagnostic_is_read_only_and_rebuild_repairs(self):
        build_packages(self.root)
        skill = self.package("astrid-dev-leader") / "SKILL.md"
        original = skill.read_bytes()
        tampered = original + b"\nUnapproved local change.\n"
        skill.write_bytes(tampered)
        self.assertEqual(check_packages(self.root),
                         ["astrid-dev-leader: generated SKILL.md is stale"])
        self.assertEqual(skill.read_bytes(), tampered)
        self.assertTrue(build_packages(self.root))
        self.assertEqual(skill.read_bytes(), original)
        self.assertEqual(check_packages(self.root), [])



class LinkPatternTests(unittest.TestCase):
    """The link pattern must not backtrack catastrophically and must keep matching ordinary links as before."""

    # (text, expected search result (whole match, destination, span) or None, expected fullmatch or None),
    # recorded from the pattern this one replaced: ordinary links must keep matching exactly as before.
    UNCHANGED = (
        ("[x](../a.md)", ("[x](../a.md)", "../a.md", (0, 12)), "[x](../a.md)"),
        ('[x](../a.md "title")', ('[x](../a.md "title")', '../a.md "title"', (0, 20)), '[x](../a.md "title")'),
        ("[x](<a b.md>)", ("[x](<a b.md>)", "<a b.md>", (0, 13)), "[x](<a b.md>)"),
        ("[x](<a(b).md>)", ("[x](<a(b).md>)", "<a(b).md>", (0, 14)), "[x](<a(b).md>)"),
        ("[x](a(b).md)", ("[x](a(b).md)", "a(b).md", (0, 12)), "[x](a(b).md)"),
        ("[x](a(b(c)).md)", None, None),
        ("[x](a\\(b\\).md)", ("[x](a\\(b\\).md)", "a\\(b\\).md", (0, 14)), "[x](a\\(b\\).md)"),
        ("![x](image.png)", ("![x](image.png)", "image.png", (0, 15)), "![x](image.png)"),
        ("[x](https://example.test/a<b)", ("[x](https://example.test/a<b)", "https://example.test/a<b", (0, 29)),
         "[x](https://example.test/a<b)"),
        ("[x](https://example.test/a>b)", ("[x](https://example.test/a>b)", "https://example.test/a>b", (0, 29)),
         "[x](https://example.test/a>b)"),
        ("[x](https://example.test/a<>b)", ("[x](https://example.test/a<>b)", "https://example.test/a<>b", (0, 30)),
         "[x](https://example.test/a<>b)"),
        ("[x](https://example.test/a<b) >", ("[x](https://example.test/a<b)", "https://example.test/a<b", (0, 29)), None),
        ("[x](a) [y](b)", ("[x](a)", "a", (0, 6)), None),
        ("[x]()", None, None),
        ("[x](<>)", ("[x](<>)", "<>", (0, 7)), "[x](<>)"),
        ("[x](<a>b)", ("[x](<a>b)", "<a>b", (0, 9)), "[x](<a>b)"),
    )

    def test_unclosed_destinations_are_matched_in_bounded_time(self):
        code = (
            "import sys, time\n"
            "from skill_builder import _LINK\n"
            "for suffix, count in (('<>', 5000), ('<', 5000), ('(<>', 3000), ('<>', 50000)):\n"
            "    text = '[](' + suffix * count\n"
            "    start = time.perf_counter()\n"
            "    match = _LINK.search(text)\n"
            "    elapsed = time.perf_counter() - start\n"
            "    print(match is None, elapsed < 1.0)\n"
        )
        result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=30,
                                cwd=Path(__file__).resolve().parent)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.split("\n")[:4], ["True True"] * 4)

    def test_ordinary_links_match_exactly_as_the_previous_pattern_did(self):
        from skill_builder import _LINK

        for text, searched, full in self.UNCHANGED:
            with self.subTest(text=text):
                match = _LINK.search(text)
                self.assertEqual(None if match is None else (match.group(0), match.group(2), match.span()), searched)
                whole = _LINK.fullmatch(text)
                self.assertEqual(None if whole is None else whole.group(0), full)

    def test_angle_form_is_a_destination_only_at_its_start(self):
        from skill_builder import _LINK

        mid = _LINK.search("[x](a<b)c>d)")
        self.assertEqual(mid.group(0), "[x](a<b)")
        self.assertIsNone(_LINK.fullmatch("[x](a<b)c>d)"))
        raw = "[x](https://example.test/a<(`>x`)y)"
        self.assertEqual(_LINK.fullmatch(raw).group(0), raw)
        self.assertEqual(_LINK.search(raw).group(0), raw)



if __name__ == "__main__":
    unittest.main()
