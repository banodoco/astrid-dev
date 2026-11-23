"""Read-only Plan 73 source-crosswalk and MS9 decision-gate regression tests."""
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from ms9_cutover_preflight import assess, markdown, primary_sources, proposed_route


class CutoverPreparationTests(unittest.TestCase):
    def test_original_twenty_sources_resolve_to_distinct_staged_documents(self):
        mapping = primary_sources()
        self.assertEqual(len(mapping), 20)
        self.assertEqual(len(set(mapping.values())), 20)
        root = Path(__file__).resolve().parents[1]
        for old, new in mapping.items():
            with self.subTest(source=old):
                self.assertTrue((root / old).is_file(), old)
                self.assertTrue((root / new).is_file(), new)

    def test_view_sync_is_not_mistaken_for_legacy_installer(self):
        mk = lambda name, path="docs/extending.md": {
            "file": path, "scope": "active-consumer",
            "reference": name, "proposed_target": None
        }
        self.assertEqual(proposed_route(mk("scripts/astrid_dev.py sync"))[0],
                         "keep-general-generated-view-sync")
        self.assertEqual(proposed_route(mk("sync.sh"))[0],
                         "retire-legacy-installer-only-after-D5")
        self.assertEqual(proposed_route(mk("skills/shared/workstreams",
                                          "scripts/workstreams.py"))[0],
                         "replace-legacy-generated-index-with-tests")
        self.assertEqual(proposed_route({
            **mk("skills/astrid-dev/SKILL.md"), "proposed_target": "agent/start.md"
        })[0], "candidate-source-link-after-D5")
        self.assertEqual(proposed_route({
            **mk("skills/shared/run-contract.md"), "scope": "historical-evidence"
        })[0], "preserve-provenance")

    def test_disposable_source_inventory_does_not_mutate_or_approve_cutover(self):
        with TemporaryDirectory(prefix="p73-ms9-tests-") as d:
            root = Path(d)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            files = {
                "README.md": "Use [start](skills/astrid-dev/SKILL.md).\n",
                "docs/extending.md": "python3 scripts/astrid_dev.py sync\n",
                "scripts/workstreams.py": "Old skills/shared/workstreams routes.\n",
                "skills/astrid-dev/SKILL.md": "# Legacy\n",
                "agent/start.md": "# Staged\n",
                "docs/handoffs/old.md": "Keep skills/shared/run-contract.md.\n",
            }
            for path, contents in files.items():
                file = root / path
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text(contents, encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "-c", "user.name=Fixture", "-c",
                            "user.email=fixture@example.invalid", "commit", "-qm", "baseline"],
                           cwd=root, check=True)
            status_before = subprocess.check_output(
                ["git", "status", "--porcelain"], cwd=root)
            result = assess(root)
            status_after = subprocess.check_output(
                ["git", "status", "--porcelain"], cwd=root)
            self.assertEqual(status_before, status_after)
            self.assertEqual(result["readiness"], "HOLD_PENDING_D5_AND_INDEPENDENT_ACCEPTANCE")
            self.assertEqual(len(result["primary_source_map"]), 20)
            self.assertTrue(result["missing_or_mismatched_primary"])
            self.assertIn("README.md", result["active_consumer_files"])
            self.assertEqual(result["route_counts"]["keep-general-generated-view-sync"], 1)
            self.assertEqual(result["route_counts"]["preserve-provenance"], 1)
            report = markdown(result)
            self.assertIn("Remaining owner decisions", report)
            self.assertIn("HOLD_PENDING_D5", report)
            self.assertNotIn("CUTOVER APPROVED", report)


if __name__ == "__main__":
    unittest.main()
