#!/usr/bin/env python3
"""Read-only R13/R14 job + native test-ID audit. No workflow dispatch and no product writes.

Usage:
 GH_TOKEN=... python3 releases/14/evidence/publication_diff.py \
    --manifest releases/14/evidence/publication-diff-inputs.json --out /tmp/r14-publication

Requires full SHA/run IDs on BOTH sides, authentic GitHub Actions logs (and
machine-readable Vitest per-test reports). Fails closed for unknown coverage.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

BASE = "https://api.github.com/repos/banodoco"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
GH_TIME = re.compile(r"^\d{4}-\d\d-\d\dT\S+Z\s+")
ANSI = re.compile(r"\x1b\[[0-9;]*m")
PYTEST = re.compile(r"^(PASSED|FAILED|ERROR|XFAIL|XPASS|SKIPPED) (.+)$")
PLAYWRIGHT = re.compile(r"^[✓✘×x-]\s*\d+\s+(?:\[[^]]+\]\s+)?(.+?\.(?:spec|test)\.[cm]?[jt]sx?):\d+:\d+\s+›\s+(.+?)(?:\s+\(\d+(?:\.\d+)?(?:ms|s|m)\))?$", re.U)
REPO = {"agent": "astrid-agent", "app": "astrid-app"}
REQUIRED = {"agent": ("CI", "Lanes"), "app": ("Tests", "Lanes", "Direct Journey", "E2E")}


def clean(line: str) -> str:
    return ANSI.sub("", GH_TIME.sub("", line)).strip()


def pytest_id(rest: str) -> str | None:
    """Match env/baseline-diff.py's bracket-aware test-ID normalization."""
    head = rest.find("::")
    if head < 0:
        return None
    bracket, space = rest.find("[", head), rest.find(" ", head)
    if bracket >= 0 and (space < 0 or bracket < space):
        depth = 0
        for pos in range(bracket, len(rest)):
            if rest[pos] == "[":
                depth += 1
            elif rest[pos] == "]":
                depth -= 1
                if depth == 0:
                    return rest[:pos + 1]
        return None
    return rest if space < 0 else rest[:space]


def parse_pytest(log: str) -> dict[str, str]:
    result = {}
    for raw in log.splitlines():
        m = PYTEST.match(clean(raw))
        if not m:
            continue
        node = pytest_id(m.group(2))
        if not node:
            continue
        state = {"PASSED": "PASS", "XFAIL": "XFAIL", "XPASS": "XPASS", "FAILED": "FAIL", "ERROR": "ERROR", "SKIPPED": "SKIP"}[m.group(1)]
        if node in result and result[node] != state:
            raise ValueError(f"conflicting pytest result for {node}: {result[node]} / {state}")
        result[node] = state
    return result


def parse_playwright(log: str) -> dict[str, str]:
    result = {}
    for raw in log.splitlines():
        line = clean(raw)
        m = PLAYWRIGHT.match(line)
        if m:
            # Stable ID: location without variable line/column + full nested title.
            status = "FAIL" if line[:1] in {"✘", "×", "x"} else "SKIP" if line[:1] == "-" else "PASS"
            key = f"{m.group(1)} › {m.group(2)}"
            if key in result and result[key] != status:
                raise ValueError(f"conflicting Playwright result for {key}")
            result[key] = status
    return result


def parse_vitest_json(path: Path) -> dict[str, str]:
    """Vitest --reporter=json --outputFile=...; require assertion-level IDs."""
    report = json.loads(path.read_text())
    tests = report.get("testResults")
    if not isinstance(tests, list) or not tests:
        raise ValueError(f"{path}: no Vitest testResults")
    out = {}
    for file in tests:
        name = file.get("name") or file.get("testFilePath") or ""
        name = name.replace("\\", "/")
        if "/src/" in name:
            name = "src/" + name.rsplit("/src/", 1)[1]
        cases = file.get("assertionResults")
        if not isinstance(cases, list) or not cases:
            raise ValueError(f"{path}: no assertionResults for {name}")
        for case in cases:
            title = case.get("fullName") or " > ".join([*(case.get("ancestorTitles") or []), case.get("title", "")])
            if not title or not name:
                raise ValueError(f"{path}: incomplete Vitest test identity")
            raw = case.get("status")
            st = {"passed": "PASS", "failed": "FAIL", "pending": "SKIP", "skipped": "SKIP", "todo": "SKIP"}.get(raw)
            if not st:
                raise ValueError(f"{path}: unknown Vitest status {raw}")
            key = f"{name} › {title}"
            if key in out:
                raise ValueError(f"{path}: duplicate Vitest ID {key}")
            out[key] = st
    return out


def api(path: str, *, binary: bool = False) -> bytes:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ValueError("GH_TOKEN/GITHUB_TOKEN is required for read-only GitHub fetches")
    request = urllib.request.Request(BASE + path, headers={
        "Authorization": "Bearer " + token,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "r14-publication-diff-readonly",
    })
    with urllib.request.urlopen(request, timeout=120) as resp:
        body = resp.read(60_000_001)
    if len(body) > 60_000_000:
        raise ValueError(f"GitHub response unexpectedly large at {path}")
    return body


def get_json(path: str) -> dict:
    return json.loads(api(path))


def collect_runs(manifest: dict, out: Path) -> dict:
    records = {}
    for product in REPO:
        records[product] = {}
        for side in ("baseline", "candidate"):
            source = manifest[side][product]
            sha = source.get("sha")
            if not isinstance(sha, str) or not SHA_RE.fullmatch(sha):
                raise ValueError(f"{side}/{product}: requires frozen full SHA")
            workflows = source.get("workflows", {})
            for wf in REQUIRED[product]:
                if not isinstance(workflows.get(wf), int) or workflows[wf] < 1:
                    raise ValueError(f"{side}/{product}: missing run ID for {wf}")
            records[product][side] = {}
            for workflow, run_id in workflows.items():
                if not isinstance(run_id, int) or run_id < 1:
                    raise ValueError(f"{side}/{product}/{workflow}: missing run ID")
                prefix = f"/{REPO[product]}/actions/runs/{run_id}"
                r = get_json(prefix)
                if r.get("head_sha") != sha or r.get("name") != workflow or r.get("status") != "completed":
                    raise ValueError(f"{side}/{product}/{workflow} run {run_id}: wrong SHA/name or incomplete")
                # A post-rerun record requires an explicit attempt pin (no silent mixing).
                attempt = source.get("attempts", {}).get(workflow, 1)
                if r.get("run_attempt") != attempt:
                    raise ValueError(f"{side}/{product}/{workflow}: expected attempt {attempt}, got {r.get('run_attempt')}")
                jobs = []
                page = 1
                while True:
                    payload = get_json(f"{prefix}/jobs?per_page=100&page={page}")
                    jobs.extend(payload.get("jobs", []))
                    if len(payload.get("jobs", [])) < 100:
                        break
                    page += 1
                if not jobs:
                    raise ValueError(f"{side}/{product}/{workflow}: no jobs")
                d = out / "raw" / product / side / re.sub(r"[^A-Za-z0-9_-]+", "_", workflow)
                d.mkdir(parents=True, exist_ok=True)
                clean_jobs = []
                seen = set()
                for job in jobs:
                    name = job.get("name")
                    if name in seen:
                        raise ValueError(f"{side}/{product}/{workflow}: duplicate job name {name}; reconcile job identity")
                    seen.add(name)
                    if job.get("status") != "completed" or job.get("conclusion") is None:
                        raise ValueError(f"{side}/{product}/{workflow}: job {name} incomplete")
                    path = d / f"{job['id']}.log"
                    if not path.exists():
                        path.write_bytes(api(f"/{REPO[product]}/actions/jobs/{job['id']}/logs", binary=True))
                    clean_jobs.append({"name": name, "id": job["id"], "conclusion": job["conclusion"], "log": str(path)})
                records[product][side][workflow] = {"id": run_id, "sha": sha, "conclusion": r.get("conclusion"), "attempt": attempt, "jobs": clean_jobs}
    return records


def evaluate(manifest: dict, records: dict, out: Path, vitest: dict[str, Path | None]) -> tuple[list[dict], list[dict], list[str]]:
    rows, jobs, problems = [], [], []
    aliases = manifest.get("job_renames", {})
    id_aliases = manifest.get("test_id_renames", {})
    dispositions = manifest.get("dispositions", {})
    for product, work in records.items():
        for workflow in sorted(set(work["baseline"]) | set(work["candidate"])):
            old = work["baseline"].get(workflow)
            new = work["candidate"].get(workflow)
            if not old or not new:
                problems.append(f"{product}/{workflow}: workflow missing from one side")
                continue
            a = {j["name"]: j for j in old["jobs"]}
            b = {j["name"]: j for j in new["jobs"]}
            used = set()
            for old_name, oldjob in sorted(a.items()):
                to_name = aliases.get(f"{product}/{workflow}/{old_name}", old_name)
                newjob = b.get(to_name)
                used.add(to_name)
                jobs.append({"product": product, "workflow": workflow, "r13_job": old_name, "candidate_job": to_name if newjob else "MISSING", "r13": oldjob["conclusion"], "candidate": newjob["conclusion"] if newjob else "MISSING", "r13_job_id": oldjob["id"], "candidate_job_id": newjob["id"] if newjob else ""})
                if newjob is None:
                    problems.append(f"{product}/{workflow}: lost job {old_name}")
                    continue
                if oldjob["conclusion"] == "success" and newjob["conclusion"] != "success":
                    problems.append(f"{product}/{workflow}: passing job {old_name} became {newjob['conclusion']}")
                if product == "agent":
                    parser = parse_pytest
                elif "vitest" in old_name.lower():
                    p0, p1 = vitest.get("baseline"), vitest.get("candidate")
                    if not p0 or not p1:
                        problems.append(f"{product}/{workflow}/{old_name}: Vitest logs lack assertion-level IDs; supply both JSON reports")
                        continue
                    old_ids, new_ids = parse_vitest_json(p0), parse_vitest_json(p1)
                else:
                    parser = parse_playwright
                if product != "app" or "vitest" not in old_name.lower():
                    old_ids = parser(Path(oldjob["log"]).read_text(errors="replace"))
                    new_ids = parser(Path(newjob["log"]).read_text(errors="replace"))
                # Not every job is a test job (e.g. lint, wheel, aggregate).
                required_ids = (product == "agent" and ("unit shard" in old_name or "integration shard" in old_name)) or (product == "app" and ("vitest" in old_name.lower() or "journey" in old_name.lower() or "checkout" in old_name.lower() or "three-products" in old_name.lower() or "e2e" in old_name.lower()))
                if required_ids and (not old_ids or not new_ids):
                    problems.append(f"{product}/{workflow}/{old_name}: no comparable native test IDs on both sides")
                if not old_ids and not new_ids:
                    continue
                mapped = {}
                for ident, state in old_ids.items():
                    new_id = id_aliases.get(f"{product}/{workflow}/{ident}", ident)
                    if new_id in mapped:
                        raise ValueError(f"non-injective test ID rename: {new_id}")
                    mapped[new_id] = (ident, state)
                for ident in sorted(set(mapped) | set(new_ids)):
                    old_id, old_state = mapped.get(ident, ("", "MISSING"))
                    new_state = new_ids.get(ident, "MISSING")
                    disposition = dispositions.get(f"{product}/{workflow}/{ident}", {})
                    why = disposition.get("reason", "")
                    ref = disposition.get("source", "")
                    result = "same"
                    if old_state != new_state:
                        result = "changed"
                        if old_state in ("PASS", "XFAIL", "XPASS") and new_state in ("FAIL", "ERROR", "SKIP", "MISSING"):
                            result = "lost-or-regressed"
                        elif old_state == "MISSING" and new_state in ("FAIL", "ERROR"):
                            result = "failing-added"
                        if result in ("lost-or-regressed", "failing-added") and not why:
                            problems.append(f"{product}/{workflow}/{ident}: {old_state} -> {new_state} unexplained")
                    rows.append({"product": product, "workflow": workflow, "job": old_name, "id": ident, "r13_id": old_id, "r13": old_state, "candidate": new_state, "classification": result, "explanation": why, "source": ref})
            for new_name in sorted(set(b) - used):
                job = b[new_name]
                jobs.append({"product": product, "workflow": workflow, "r13_job": "MISSING", "candidate_job": new_name, "r13": "MISSING", "candidate": job["conclusion"], "r13_job_id": "", "candidate_job_id": job["id"]})
                if job["conclusion"] != "success":
                    problems.append(f"{product}/{workflow}: newly failing job {new_name}")
    return rows, jobs, problems


def check_canonical_baseline_diff(records: dict, out: Path) -> list[str]:
    """Run env/baseline-diff.py on all original -rA Agent shard logs.

    Additional per-ID SKIP/ERROR details and job statuses are retained by our CSV.
    A canonical regression (exit 1) is a blocker; missing input (exit 2) is unknown.
    """
    script = Path(__file__).resolve().parents[3] / "env" / "baseline-diff.py"
    if not script.is_file():
        return [f"required canonical comparator missing: {script}"]
    problems = []
    for wf, fragment in (("CI", "unit shard"), ("Lanes", "integration shard")):
        files = {}
        for side in ("baseline", "candidate"):
            selected = [j for j in records["agent"][side][wf]["jobs"] if fragment in j["name"]]
            expected = 8 if wf == "CI" else 4
            if len(selected) != expected:
                problems.append(f"agent/{wf}: expected {expected} original shards, found {len(selected)} on {side}")
                continue
            paths = []
            for j in selected:
                original = Path(j["log"])
                clean_path = original.with_name(original.stem + ".clean.log")
                if not clean_path.exists():
                    clean_path.write_text("\n".join(clean(x) for x in original.read_text(errors="replace").splitlines()) + "\n")
                paths.append(str(clean_path))
            files[side] = paths
        if len(files) != 2:
            continue
        location = out / f"baseline-diff-{wf.lower()}"
        result = subprocess.run([sys.executable, "-I", str(script), "--baseline", "published-R13=" + ",".join(files["baseline"]), "--candidate", ",".join(files["candidate"]), "--out", str(location)], capture_output=True, text=True)
        (out / f"canonical-{wf.lower()}.txt").write_text(result.stdout + "\nSTDERR:\n" + result.stderr)
        if result.returncode:
            problems.append(f"agent/{wf}: canonical env/baseline-diff.py exit {result.returncode} (see canonical-{wf.lower()}.txt)")
    return problems


def write_csv(path: Path, rows: list[dict], columns: list[str]) -> None:
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--vitest-json-r13", type=Path, help="full R13 Vitest JSON reporter output")
    ap.add_argument("--vitest-json-r14", type=Path, help="full candidate Vitest JSON reporter output")
    a = ap.parse_args(argv)
    try:
        m = json.loads(a.manifest.read_text())
        a.out.mkdir(parents=True, exist_ok=True)
        records = collect_runs(m, a.out)
        (a.out / "resolved-runs.json").write_text(json.dumps(records, indent=2) + "\n")
        rows, jobs, problems = evaluate(m, records, a.out, {"baseline": a.vitest_json_r13, "candidate": a.vitest_json_r14})
        problems.extend(check_canonical_baseline_diff(records, a.out))
        write_csv(a.out / "all-test-ids.csv", rows, ["product", "workflow", "job", "id", "r13_id", "r13", "candidate", "classification", "explanation", "source"])
        write_csv(a.out / "jobs.csv", jobs, ["product", "workflow", "r13_job", "candidate_job", "r13", "candidate", "r13_job_id", "candidate_job_id"])
        counter = Counter(x["classification"] for x in rows)
        changes = [x for x in rows if x["classification"] != "same"]
        table = ["# R14 publication comparison (not an approval)", "", "| Native ID classification | Count |", "|---|---:|"]
        table.extend(f"| {name} | {count} |" for name, count in sorted(counter.items()))
        table += ["", f"Changed IDs: {len(changes)} (complete table: \u0060all-test-ids.csv\u0060)", "", "## Job-level evidence", "", "| Repo/workflow | R13 job | R13 | Candidate job | Candidate |", "|---|---|---|---|---|"]
        table.extend(f"| {j['product']}/{j['workflow']} | {j['r13_job']} | {j['r13']} | {j['candidate_job']} | {j['candidate']} |" for j in jobs)
        table += ["", "## Outstanding / blockers", ""]
        table.extend("- " + p for p in sorted(set(problems)))
        (a.out / "report.md").write_text("\n".join(table) + "\n")
        print("Saved", a.out / "report.md", a.out / "all-test-ids.csv", a.out / "jobs.csv")
        print(f"ID rows={len(rows)}; job rows={len(jobs)}; outstanding={len(set(problems))}")
        return 1 if problems else 0
    except (ValueError, KeyError, OSError, urllib.error.URLError, json.JSONDecodeError) as e:
        print("INCOMPLETE (no qualifying verdict):", e, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
