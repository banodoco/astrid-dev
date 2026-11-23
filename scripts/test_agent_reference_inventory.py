"""Tests for the non-mutating MS-7 pre-cutover reference inventory."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from agent_reference_inventory import inventory, mapped_target, render_markdown, scope_for, tracked_paths


class ReferenceInventoryTests(unittest.TestCase):
    def test_source_crosswalk_only_maps_known_canonical_targets(self):
        examples = {
            "skills/astrid-dev/SKILL.md": "agent/start.md",
            "skills/roles/astrid-dev-lead/SKILL.md": "agent/roles/leader.md",
            "skills/roles/astrid-dev-manage/workstreams/whole-project.md": "agent/roles/manager/whole-project.md",
            "skills/roles/astrid-dev-orchestrate/workstreams/codex-cloud/README.md": "agent/guides/codex-cloud/README.md",
            "skills/shared/workstreams/astrid-dev-gpu-validate/SKILL.md": "agent/shared/workstreams/gpu-validate.md",
            "skills/capabilities/astrid-dev-gap": "agent/shared/workstreams/gap.md",
            "skills/shared/workstreams/astrid-dev-release/references/sources.md": "agent/shared/release-sources.md",
            "skills/shared/templates/run.yaml": "agent/shared/templates/run.yaml",
        }
        for old, target in examples.items():
            with self.subTest(source=old):
                self.assertEqual(mapped_target(old, "path"), target)
        self.assertIsNone(mapped_target("skills/shared/workstreams/astrid-dev-gpu-validate/records/file.md", "path"))
        self.assertIsNone(mapped_target("sync.sh", "command"))
        self.assertEqual(mapped_target("astrid-dev-manage", "skill"), "astrid-dev-manager")

    def test_scope_requires_human_decision_for_plan_and_release_records(self):
        expected = {
            "README.md": "active-consumer",
            "agent/roles/manager.md": "staged-agent",
            "skills/roles/astrid-dev-manage/SKILL.md": "current-authority",
            "plans/73-markdown-first-agent-skills/tasks.md": "plan-owner-review",
            "releases/15.md": "release-lead-review",
            "releases/14/packets/R14-FIX-01.md": "release-lead-review",
            "releases/14/evidence/report.md": "historical-evidence",
            "docs/handoffs/2026-11-10.md": "historical-evidence",
            "docs/ledger/entry.md": "historical-evidence",
            "scripts/test_workstreams.py": "pinned-test-or-fixture",
            ".github/workflows/docs.yml": "active-consumer",
        }
        for path, scope in expected.items():
            with self.subTest(path=path):
                self.assertEqual(scope_for(path), scope)

    def test_exact_tracked_file_line_inventory_without_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            files = {
                "README.md": "Old [manager](skills/roles/astrid-dev-manage/SKILL.md).\n"
                             "Install ~/.agents/skills/astrid-dev-manager/SKILL.md instead.\n"
                             "python3 scripts/astrid_dev.py sync\n",
                "docs/handoffs/old.md": "See skills/shared/run-contract.md for the old review.\n",
                "releases/15/packets/P.md": "Follow astrid-dev-orchestrate.\n",
                "scripts/test_x.py": "Assert skills/capabilities/astrid-dev-gap.\n",
                "agent/start.md": "See skills/astrid-dev/SKILL.md.\n",
            }
            for path, body in files.items():
                p = root / path
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(body, encoding="utf-8")
            (root / "untracked.md").write_text("sync.sh\n", encoding="utf-8")
            subprocess.run(["git", "add", "README.md", "docs", "releases", "scripts", "agent"], cwd=root, check=True)
            before = subprocess.check_output(["git", "status", "--porcelain"], cwd=root)
            rows = inventory(root)
            after = subprocess.check_output(["git", "status", "--porcelain"], cwd=root)
            self.assertEqual(before, after)
            self.assertEqual(len(rows), 6)
            self.assertTrue(all(isinstance(row["line"], int) and row["text"] for row in rows))
            self.assertEqual([(row["line"], row["reference"]) for row in rows if row["file"] == "README.md"], [
                (1, "skills/roles/astrid-dev-manage/SKILL.md"),
                (3, "scripts/astrid_dev.py sync"),
            ])
            self.assertEqual(next(row for row in rows if row["file"] == "agent/start.md")["disposition"], "candidate-after-D5")
            self.assertEqual(next(row for row in rows if row["file"] == "docs/handoffs/old.md")["disposition"], "preserve-history")
            self.assertEqual(next(row for row in rows if row["file"] == "scripts/test_x.py")["disposition"], "owner-adjudicate")
            self.assertIn("README.md", tracked_paths(root))
            report = render_markdown(rows, "a" * 40)
            self.assertIn("**Matches:** 6", report)
            self.assertIn("README.md#L1", report)
            self.assertIn("preserve-history", report)
            self.assertEqual(len(json.loads(json.dumps(rows))), 6)


if __name__ == "__main__":
    unittest.main()
