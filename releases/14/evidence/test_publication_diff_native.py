"""Provenance boundary tests for native reports; all network calls are mocked."""
import hashlib
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

import publication_diff as mod


class NativeProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.out = Path(self.temp.name)
        self.run = {"app": {"baseline": {"Tests": {"id": 41, "sha": "a" * 40, "attempt": 2,
                    "jobs": [{"name": "vitest", "id": 51, "attempt": 2,
                              "started_at": "2026-01-01T00:00:00Z", "completed_at": "2026-01-01T00:02:00Z"}]}}}}
        self.contents = {
            "vitest": json.dumps({"testResults": [{"name": "/src/a.test.ts", "assertionResults": [
                {"fullName": "suite test", "status": "passed"}]}]}).encode(),
            "junit": b'<testsuite><testcase classname="suite" name="test"/></testsuite>',
            "playwright": json.dumps({"suites": [{"title": "a.spec.ts", "file": "tests/a.spec.ts", "specs": [
                {"title": "test", "file": "tests/a.spec.ts", "tests": [{"projectName": "chromium", "status": "expected", "expectedStatus": "passed", "results": [{"status": "passed"}]}]}]}]}).encode(),
        }

    def tearDown(self): self.temp.cleanup()

    def test_api_token_is_unredirected_header(self):
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def read(self, size): return b"{}"
        with mock.patch.dict("os.environ", {"GH_TOKEN": "test-token"}), mock.patch.object(mod.urllib.request, "urlopen", return_value=Response()) as open_url:
            mod.api("/astrid-app/actions/artifacts/77/zip")
        request = open_url.call_args.args[0]
        self.assertEqual(request.unredirected_hdrs["Authorization"], "Bearer test-token")
        self.assertNotIn("Authorization", request.headers)

    def _artifact(self, key, kind, data, *, run_id=41, sha=None):
        archive = io.BytesIO()
        with zipfile.ZipFile(archive, "w") as zf: zf.writestr("reports/report", data)
        zipped = archive.getvalue()
        spec = {"type": "artifact", "run_id": run_id, "attempt": 2, "sha": sha or "a" * 40,
                "sha256": hashlib.sha256(data).hexdigest(), "artifact_id": 77, "member": "reports/report"}
        artifact = {"id": 77, "expired": False, "workflow_run": {"id": 41, "head_sha": "a"*40},
                    "created_at": "2026-01-01T00:01:00Z", "digest": "sha256:"+hashlib.sha256(zipped).hexdigest(),
                    "archive_download_url": "https://untrusted.invalid/a.zip"}
        attempt = {"id": 41, "run_attempt": 2, "head_sha": "a"*40,
                   "run_started_at": "2026-01-01T00:00:00Z", "updated_at": "2026-01-01T00:02:00Z"}
        with mock.patch.object(mod, "get_json", side_effect=[artifact, attempt]), mock.patch.object(mod, "api", return_value=zipped) as api:
            result = mod.validate_native_reports({"native_reports": {key: spec}}, self.run,
                {key: self._path(kind, data)}, self.out)
            if not result[1]: api.assert_called_once_with("/astrid-app/actions/artifacts/77/zip")
            return result

    def _path(self, kind, data):
        p = self.out / f"source.{ {'vitest':'json','junit':'xml','playwright':'json'}[kind]}"
        p.write_bytes(data)
        return p

    def test_all_three_formats_are_bound_to_exact_artifact_member(self):
        for kind in self.contents:
            key = "baseline/app/Tests/vitest" if kind != "playwright" else "baseline/app/E2E/playwright-chromium"
            if kind == "playwright":
                self.run["app"]["baseline"]["E2E"] = {"id": 41, "sha": "a" * 40, "attempt": 2,
                    "jobs": [{"name": "playwright-chromium", "id": 51, "attempt": 2,
                              "started_at": "2026-01-01T00:00:00Z", "completed_at": "2026-01-01T00:02:00Z"}]}
            resolved, problems, _, _ = self._artifact(key, kind, self.contents[kind])
            self.assertFalse(problems)
            path = resolved[key]
            if kind == "vitest": self.assertTrue(mod.parse_vitest_multiset(path))
            elif kind == "junit": self.assertTrue(mod.parse_junit_xml(path))
            else: self.assertTrue(mod.parse_playwright_json(path))

    def test_wrong_run_and_tampered_bytes_are_not_resolved(self):
        key = "baseline/app/Tests/vitest"
        self.assertTrue(self._artifact(key, "vitest", self.contents["vitest"], run_id=999)[1])
        spec_key = key
        zipped = io.BytesIO()
        with zipfile.ZipFile(zipped, "w") as zf: zf.writestr("reports/report", self.contents["vitest"])
        spec = {"type": "artifact", "run_id": 41, "attempt": 2, "sha": "a"*40,
                "sha256": "0"*64, "artifact_id": 77, "member": "reports/report"}
        with mock.patch.object(mod, "get_json", side_effect=[{"id":77,"expired":False,"workflow_run":{"id":41,"head_sha":"a"*40},"created_at":"2026-01-01T00:01:00Z","digest":"sha256:"+hashlib.sha256(zipped.getvalue()).hexdigest()},
             {"id": 41, "run_attempt": 2, "head_sha": "a"*40}]), mock.patch.object(mod, "api", return_value=b"bad"):
            resolved, problems, _, _ = mod.validate_native_reports({"native_reports": {spec_key: spec}}, self.run,
                {spec_key: self._path("vitest", self.contents["vitest"])}, self.out)
        self.assertFalse(resolved)
        self.assertTrue(problems)

    def test_local_evidence_visible_approved_and_unapproved_blocks(self):
        key = "baseline/app/Tests/vitest"
        p = self._path("vitest", self.contents["vitest"])
        spec = {"type": "local", "run_id": 41, "attempt": 2, "sha": "a"*40,
                "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
        resolved, problems, visible, receipt = mod.validate_native_reports({"native_reports": {key: spec}}, self.run,
            {key: p}, self.out)
        self.assertFalse(resolved)
        self.assertTrue(problems)
        self.assertIn(key, " ".join(visible))
        self.assertIn("unapproved", " ".join(visible))
        self.assertTrue(mod.validate_native_reports({"native_reports": {key: spec}}, self.run, {key: p}, self.out,
            rehearsal=True)[1])
        approved = {"native_reports": {key: spec}, "local_evidence_exceptions": {key: {**spec, "approve_reason": "owner signed local capture"}}}
        resolved, problems, visible, receipt = mod.validate_native_reports(approved, self.run, {key: p}, self.out)
        self.assertIn(key, resolved)
        self.assertFalse(problems)
        self.assertIn("owner-approved", visible[0])
        self.assertEqual(receipt[key]["approval_reason"], "owner signed local capture")

    def test_invalid_approval_note_type_is_unapproved_and_missing_job_window_fails_closed(self):
        key = "baseline/app/Tests/vitest"
        path = self._path("vitest", self.contents["vitest"])
        local = {"type": "local", "run_id": 41, "attempt": 2, "sha": "a"*40,
                 "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        manifest = {"native_reports": {key: local},
                    "local_evidence_exceptions": {key: {**local, "approve_reason": ["not", "text"]}}}
        resolved, problems, visible, receipt = mod.validate_native_reports(manifest, self.run, {key: path}, self.out, rehearsal=True)
        self.assertTrue(resolved)
        self.assertTrue(problems)
        self.assertIn("unapproved", visible[0])
        self.run["app"]["baseline"]["Tests"]["jobs"][0].pop("started_at")
        archive = io.BytesIO()
        with zipfile.ZipFile(archive, "w") as zf: zf.writestr("reports/report", self.contents["vitest"])
        zipped = archive.getvalue()
        artifact = {"id": 77, "expired": False, "workflow_run": {"id": 41, "head_sha": "a"*40},
                    "created_at": "2026-01-01T00:01:00Z", "digest": "sha256:"+hashlib.sha256(zipped).hexdigest()}
        with mock.patch.object(mod, "get_json", side_effect=[artifact, {"id":41,"run_attempt":2,"head_sha":"a"*40}]), mock.patch.object(mod, "api", return_value=zipped):
            resolved, problems, _, _ = mod.validate_native_reports({"native_reports": {key: {**local, "type":"artifact", "artifact_id":77, "member":"reports/report"}}}, self.run, {key:path}, self.out)
        self.assertFalse(resolved)
        self.assertTrue(problems)

    def test_cli_local_provenance_appears_in_verdict_and_requires_exact_owner_exception(self):
        path = self._path("junit", self.contents["junit"])
        baseline = self.run["app"]["baseline"]["Tests"]
        baseline.update(conclusion="success")
        baseline["jobs"][0].update(conclusion="success")
        candidate = dict(baseline, id=42, sha="b" * 40)
        candidate["jobs"] = [dict(baseline["jobs"][0], id=52)]
        self.run["app"]["candidate"] = {"Tests": candidate}
        reports = {}
        for side, run in (("baseline", baseline), ("candidate", candidate)):
            reports[f"{side}/app/Tests/vitest"] = {
                "type": "local", "run_id": run["id"], "attempt": run["attempt"],
                "sha": run["sha"], "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
        inventory = self.out / "inventory.json"
        inventory.write_text(json.dumps({"schema_version": 1, "sealed_prior": [], "current": []}))
        manifest = self.out / "manifest.json"
        inputs = {"native_reports": reports}
        manifest.write_text(json.dumps(inputs))
        verdict = self.out / "verdict"
        args = ["--manifest", str(manifest), "--inherited-red", str(inventory), "--inherited-base", "HEAD", "--out", str(verdict),
                "--junit-xml-r13", str(path), "--junit-xml-r14", str(path)]
        with mock.patch.object(mod, "collect_runs", return_value=self.run), mock.patch.object(
                mod, "check_canonical_baseline_diff", return_value=[]), mock.patch.object(
                mod, "resolve_inherited_base", return_value=("a" * 40, {"schema_version": 1, "sealed_prior": [], "current": []})):
            self.assertEqual(mod.main(args), 1)
            report = (verdict / "report.md").read_text()
            self.assertLess(report.index("## LOCAL-EVIDENCE"), report.index("| Repo"))
            self.assertIn("unapproved", report)
            inputs["local_evidence_exceptions"] = {
                key: {**binding, "approve_reason": "Owner-reviewed fixture"} for key, binding in reports.items()
            }
            manifest.write_text(json.dumps(inputs))
            self.assertEqual(mod.main(args), 0)
            receipt = json.loads((verdict / "native-report-input-digests.json").read_text())
            self.assertEqual(receipt["candidate/app/Tests/vitest"]["job_id"], 52)
            self.assertEqual(receipt["candidate/app/Tests/vitest"]["approval_reason"], "Owner-reviewed fixture")


if __name__ == "__main__": unittest.main()
