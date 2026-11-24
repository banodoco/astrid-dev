"""Fix #6 regressions: explicit attempts and latest-run provenance."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

FILE = Path(__file__).with_name("publication_diff.py")
import importlib.util
spec = importlib.util.spec_from_file_location("r14_attempt", FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class PublicationAttemptSafety(unittest.TestCase):
    def setup_case(self, temp):
        sha = "a" * 40
        source = {"sha": sha, "workflows": {"ci": 10}, "attempts": {"ci": 2}}
        manifest = {side: {"vibecomfy": source} for side in ("baseline", "candidate")}
        latest = {"id": 10, "head_sha": sha, "name": "ci", "status": "completed", "run_attempt": 2, "conclusion": "success"}
        job = {"name": "test", "status": "completed", "conclusion": "success", "id": 20, "run_attempt": 2, "steps": []}
        prefix = "/VibeComfy/actions/runs/10"
        attempt = prefix + "/attempts/2"
        data = {prefix: latest, attempt: dict(latest), attempt + "/jobs?per_page=100&page=1": {"jobs": [job]}}
        return sha, source, manifest, latest, job, prefix, attempt, data

    def test_collector_requires_attempt_and_checks_latest_and_rechecks_after_gather(self):
        with tempfile.TemporaryDirectory() as d:
            _, source, manifest, latest, _, prefix, attempt, data = self.setup_case(d)
            source.pop("attempts")
            with mock.patch.object(mod, "REPO", {"vibecomfy": "VibeComfy"}), mock.patch.object(mod, "get_json", side_effect=data.__getitem__), mock.patch.object(mod, "api", return_value=b"log"):
                with self.assertRaisesRegex(ValueError, "invalid run attempt"):
                    mod.collect_runs(manifest, Path(d))
            source["attempts"] = {"ci": 2}
            data[prefix] = dict(latest, run_attempt=3)
            with mock.patch.object(mod, "REPO", {"vibecomfy": "VibeComfy"}), mock.patch.object(mod, "get_json", side_effect=data.__getitem__):
                with self.assertRaisesRegex(ValueError, "latest"):
                    mod.collect_runs(manifest, Path(d))
            # Latest changes between initial validation and completed evidence gathering.
            data[prefix] = latest
            calls = []
            def get(path):
                calls.append(path)
                if path == prefix and calls.count(prefix) == 2:
                    return dict(latest, run_attempt=3)
                return data[path]
            with mock.patch.object(mod, "REPO", {"vibecomfy": "VibeComfy"}), mock.patch.object(mod, "get_json", side_effect=get), mock.patch.object(mod, "api", return_value=b"log"):
                with self.assertRaisesRegex(ValueError, "latest"):
                    mod.collect_runs(manifest, Path(d))

    def test_rehearsal_requires_explicit_matching_complete_workflow_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            _, source, manifest, _, job, _, _, _ = self.setup_case(d)
            records = {"vibecomfy": {side: {"ci": {"id": 10, "sha": source["sha"], "attempt": 2, "conclusion": "success", "jobs": [dict(job, attempt=2, log="offline.log")]}} for side in ("baseline", "candidate")}}
            p = Path(d) / "records.json"
            with mock.patch.object(mod, "REPO", {"vibecomfy": "VibeComfy"}):
                p.write_text(json.dumps(records))
                self.assertEqual(mod.read_rehearsal_records(p, manifest), records)
                source.pop("attempts")
                with self.assertRaisesRegex(ValueError, "invalid run attempt"):
                    mod.read_rehearsal_records(p, manifest)
                source["attempts"] = {"ci": 2}
                del records["vibecomfy"]["candidate"]["ci"]
                p.write_text(json.dumps(records))
                with self.assertRaisesRegex(ValueError, "missing workflow"):
                    mod.read_rehearsal_records(p, manifest)
