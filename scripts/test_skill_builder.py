"""Focused generated-skill packaging, reference and refusal tests."""
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

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


if __name__ == "__main__":
    unittest.main()
