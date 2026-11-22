#!/usr/bin/env python3
"""Read-only R13/R14 job + native test-ID audit. No workflow dispatch and no product writes.

Requires exact SHA, run and attempt on both sides and native test-ID evidence.
See publication-checklist.md for the freeze command and review procedure.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
import urllib.error
import urllib.request
from collections import Counter
from itertools import zip_longest
from pathlib import Path

BASE = "https://api.github.com/repos/banodoco"
DEFAULT_INHERITED_RED = Path(__file__).with_name("inherited-red.json")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
GH_TIME = re.compile(r"^\d{4}-\d\d-\d\dT\S+Z\s+")
GH_LOG_COLUMNS = re.compile(r"^[^\t]*\t([^\t]*)\t\d{4}-\d\d-\d\dT\S+Z\s+")
ANSI = re.compile(r"\x1b\[[0-9;]*m")
PYTEST = re.compile(r"^(PASSED|FAILED|ERROR|XFAIL|XPASS|SKIPPED) (.+)$")
PYTEST_PROGRESS = re.compile(r"^(.+::.+?)\s+(PASSED|FAILED|ERROR|XFAIL|XPASS|SKIPPED)\s+\[\s*\d+%\]$")
PYTEST_SKIP_GROUP = re.compile(r"^SKIPPED \[(\d+)\] .+")
PYTEST_TOTAL = re.compile(r"^(?:\d+ (?:passed|failed|skipped|xfailed|xpassed|errors?|warnings?|subtests)\b|no tests ran).*\bin \d")
PYTEST_OUTCOMES = dict(PASSED="PASS", FAILED="FAIL", ERROR="ERROR", XFAIL="XFAIL", XPASS="XPASS", SKIPPED="SKIP")
PYTEST_ADVERSITY = {status: rank for rank, status in enumerate(("PASS", "XFAIL", "SKIP", "XPASS", "FAIL", "ERROR"))}
PLAYWRIGHT_LOCATION = r"(?:\[([^]]+)\]\s+)?(?:›\s*)?(.+?\.(?:spec|test)\.[cm]?[jt]sx?):\d+:\d+\s+›\s+"
PLAYWRIGHT = re.compile(r"^[✓✘×x-]\s*\d+\s+" + PLAYWRIGHT_LOCATION + r"(.+?)(?:\s+\(\d+(?:\.\d+)?(?:ms|s|m)\))?$")
PLAYWRIGHT_FAILURE = re.compile(r"^(?:##\[error\]\s*)?\d+\)\s+" + PLAYWRIGHT_LOCATION + r"(.+?)\s*$")
REPO = {"agent": "astrid-agent", "app": "astrid-app", "runtime": "astrid-runtime", "vibecomfy": "VibeComfy"}
REQUIRED = {"agent": ("CI", "Lanes"), "app": ("Tests", "Lanes", "Direct Journey", "E2E"), "runtime": ("CI",), "vibecomfy": ("ci",)}


def clean(line: str) -> str:
    line = ANSI.sub("", line).lstrip("\ufeff")
    # `gh run view --log` prefixes each body with job, step, and timestamp.
    line = GH_LOG_COLUMNS.sub("", line)
    return GH_TIME.sub("", line).strip()


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


def pytest_steps(log):
    step, lines = None, []
    for raw in log.splitlines():
        line = clean(raw)
        columns = GH_LOG_COLUMNS.match(raw.lstrip("\ufeff"))
        next_step = columns[1] if columns else step
        if lines and (next_step != step or line.startswith("##[group]Run ")):
            yield lines
            lines = []
        step = next_step
        lines.append(line)
    if lines:
        yield lines


def pytest_job_results(log: str) -> tuple[dict[str, str], int]:
    outcomes, unbound_skips = {}, 0

    def record(raw_status, native_id):
        node = pytest_id(native_id)
        state = PYTEST_OUTCOMES[raw_status]
        if node and PYTEST_ADVERSITY[state] > PYTEST_ADVERSITY.get(outcomes.get(node), -1):
            outcomes[node] = state

    for lines in pytest_steps(log):
        # The parent runner writes its summary after any child output printed
        # in failure diagnostics. The step boundary keeps separate CI commands.
        summary_starts = [i for i, line in enumerate(lines) if line.strip(" =") == "short test summary info"]
        summary_start = summary_starts[-1] + 1 if summary_starts else None
        diagnostics = next((i for i, line in enumerate(lines)
                            if line.strip(" =") in ("FAILURES", "ERRORS") or line.startswith("----- Captured ")), len(lines))
        for line in lines[:min(diagnostics, summary_start or len(lines))]:
            match = PYTEST_PROGRESS.match(line)
            if match:
                record(match[2], match[1])
        summary = lines[summary_start:] if summary_start is not None else lines[:diagnostics]
        groups = set()
        for line in summary:
            match = PYTEST.match(line)
            if match:
                record(match[1], match[2])
                if PYTEST_SKIP_GROUP.match(line):
                    groups.add(line)
            elif summary_start is not None and PYTEST_TOTAL.match(line.strip(" =")):
                break
        unbound_skips += sum(int(PYTEST_SKIP_GROUP.match(line)[1]) for line in groups)
    leftover_skips = max(0, unbound_skips - sum(state == "SKIP" for state in outcomes.values()))
    return outcomes, leftover_skips


def parse_pytest(log: str) -> dict[str, str]:
    outcomes, _ = pytest_job_results(log)
    return outcomes


def parse_playwright(log: str) -> dict[str, str]:
    result = {}
    # Playwright's runner summary repeats failed test locations and titles,
    # often without native JSON. Only these explicitly numbered error rows
    # are recoverable; they establish failures, never passes or coverage.
    for raw in log.splitlines():
        line = clean(raw)
        m = PLAYWRIGHT.match(line)
        if m:
            status = "FAIL" if line[:1] in {"✘", "×", "x"} else "SKIP" if line[:1] == "-" else "PASS"
        else:
            m = PLAYWRIGHT_FAILURE.match(line)
            status = "FAIL"
        if not m:
            continue
        project, location, title = m.groups()
        location = location.replace("\\", "/")
        if "/tests/" in location:
            location = "tests/" + location.rsplit("/tests/", 1)[1]
        title = re.sub(r"\s+(?:─{2,}|\(retry #\d+\))$", "", title)
        key = " › ".join(([location, f"[{project}]"] if project else [location]) + [title])
        if result.get(key) != "FAIL":
            result[key] = status
    return result


def parse_vitest_multiset(path: Path) -> dict[str, str | list[str]]:
    """Read every Vitest assertion occurrence, retaining duplicate IDs and states."""
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
                out[key] = (out[key] if isinstance(out[key], list) else [out[key]]) + [st]
            else:
                out[key] = st
    return out


def parse_vitest_json(path: Path) -> dict[str, str]:
    """Backwards-compatible unique-ID Vitest reader."""
    result = parse_vitest_multiset(path)
    duplicates = [key for key, value in result.items() if isinstance(value, list)]
    if duplicates:
        raise ValueError(f"{path}: duplicate Vitest ID {duplicates[0]}")
    return result


def occurrences(records):
    """Normalize a per-ID state or list of repeated states to a flat list."""
    return {key: value if isinstance(value, list) else [value] for key, value in records.items()}


def parse_junit_xml(path: Path) -> dict[str, str | list[str]]:
    root = ET.parse(path).getroot()
    out = {}
    for case in root.iter("testcase"):
        title = case.get("name")
        if not title:
            raise ValueError(f"{path}: incomplete JUnit test identity")
        name = f"{case.get('classname', '')}::{title}"
        state = next((state for tag, state in (("error", "ERROR"), ("failure", "FAIL"), ("skipped", "SKIP"))
                      if case.find(tag) is not None), "PASS")
        out[name] = out.get(name, []) + [state] if isinstance(out.get(name), list) else ([out[name], state] if name in out else state)
    if not out:
        raise ValueError(f"{path}: no JUnit testcases")
    return out


def multiset_diff(old, new):
    """Return state-count changes without assigning arbitrary duplicate occurrences."""
    return dict(Counter(old) - Counter(new)) | {"added": dict(Counter(new) - Counter(old))} if Counter(old) != Counter(new) else {}



def _playwright_json_cases(path: Path):
    """Yield stable IDs and normalized audit records from native Playwright JSON."""
    report = json.loads(path.read_text())
    suites = report.get("suites")
    if not isinstance(suites, list) or not suites:
        raise ValueError(f"{path}: missing Playwright JSON suites")
    output = []
    status_map = {"passed": "PASS", "failed": "FAIL", "timedOut": "FAIL", "interrupted": "ERROR", "skipped": "SKIP"}
    expected_map = {"passed": "PASS", "failed": "FAIL", "skipped": "SKIP"}

    def visit(suite, parents):
        title = suite.get("title") or ""
        context = parents + ([title] if title and not title.endswith((".spec.ts", ".spec.tsx", ".test.ts", ".test.tsx")) else [])
        for spec in suite.get("specs", []):
            file = (spec.get("file") or suite.get("file") or "").replace("\\", "/")
            if "/tests/" in file:
                file = "tests/" + file.rsplit("/tests/", 1)[1]
            title = spec.get("title")
            for test in spec.get("tests", []):
                project_name = test.get("projectName")
                project = "<default>" if project_name is None or not str(project_name).strip() else str(project_name)
                state, expected = test.get("status"), test.get("expectedStatus", "passed")
                if not file or not title or state not in ("expected", "unexpected", "flaky", "skipped") or expected not in expected_map:
                    raise ValueError(f"{path}: incomplete/unknown Playwright expected status or identity")
                key = " › ".join([file, f"[{project}]", *context, title])
                results = test.get("results", [])
                if not isinstance(results, list):
                    raise ValueError(f"{path}: invalid Playwright results")
                actual = status_map.get(next((r.get("status") for r in reversed(results) if r.get("status")), None), "MISSING")
                expected_status = expected_map[expected]
                verdict = "PASS" if state in ("expected", "skipped") else "FAIL"
                record = {"expected": expected_status, "actual": actual, "status": verdict}
                if len(results) > 1 or state == "flaky":
                    record["retries"] = results
                output.append((key, record, state))
        for child in suite.get("suites", []):
            visit(child, context)
    for suite in suites:
        visit(suite, [])
    if not output:
        raise ValueError(f"{path}: no Playwright per-test records")
    return output


def parse_playwright_json(path: Path) -> dict[str, str | list[str]]:
    """Playwright JSON count parser; failed attempts and flakes stay adverse."""
    output = {}
    for key, record, state in _playwright_json_cases(path):
        # A skip stays red for qualification; expected failures are not passing outcomes.
        outcome = "SKIP" if state == "skipped" or record["actual"] == "SKIP" else "PASS" if record["actual"] == "PASS" and state != "flaky" else "FAIL"
        output[key] = output.get(key, []) + [outcome] if isinstance(output.get(key), list) else ([output[key], outcome] if key in output else outcome)
    return output


def parse_playwright_json_outcomes(path: Path) -> dict[str, list[dict[str, str]]]:
    """Retain expected status, observed result, verdict, and retry detail."""
    output = {}
    for key, record, _state in _playwright_json_cases(path):
        output[key] = output.get(key, []) + [record]
    return output


def validate_inherited_failures(inventory: dict, baseline_reds: list[dict], candidate_reds: list[dict] | None = None) -> list[str]:
    """Validate an explicit prior/current inventory as a count-based, shrink-only ceiling."""
    problems = []
    if not isinstance(inventory, dict) or not isinstance(inventory.get("approved_prior"), list) or not isinstance(inventory.get("current"), list):
        return ["inherited_failures requires approved_prior and current machine-readable lists"]
    fields = ("repo", "workflow", "job", "id", "status")
    red_statuses = {"FAIL", "SKIP", "ERROR"}
    def counts(rows, label):
        result = Counter()
        for row in rows:
            if not isinstance(row, dict) or any(not isinstance(row.get(k), str) or not row[k] for k in fields) or row.get("status") not in red_statuses:
                problems.append(f"inherited_failures {label}: malformed row or non-red status")
                continue
            result[tuple(row[k] for k in fields)] += 1
        return result
    prior, current, actual = counts(inventory["approved_prior"], "approved_prior"), counts(inventory["current"], "current"), counts(baseline_reds, "baseline")
    for key, count in prior.items():
        if actual[key] < count:
            problems.append(f"inherited_failures: approved ID not actually red in baseline: {key}")
    for key, count in actual.items():
        if prior[key] < count:
            problems.append(f"inherited_failures: baseline red missing from approved prior list: {key}")
    for key, count in current.items():
        if count > prior[key]:
            problems.append(f"inherited_failures: current red exceeds prior approved count: {key}")
    if candidate_reds is not None:
        candidates = counts(candidate_reds, "candidate")
        for key, count in candidates.items():
            if count > current[key]:
                problems.append(f"inherited_failures: candidate red exceeds current approved count: {key}")
    return problems


INHERITED_RED_STATUSES = frozenset({"FAIL", "ERROR", "SKIP"})
INHERITED_RED_FIELDS = ("repo", "workflow", "job", "id")


def row_red_key(row: dict) -> tuple[str, str, str, str]:
    return row["product"], row["workflow"], row["job"], row["id"]


def reviewed_inherited_red_counts(inventory: dict) -> tuple[Counter, list[str]]:
    """Validate the reviewed subset against the prior reviewed ceiling."""
    if (not isinstance(inventory, dict) or type(inventory.get("schema_version")) is not int
            or inventory["schema_version"] != 1
            or any(not isinstance(inventory.get(field), list) for field in ("sealed_prior", "current"))):
        return Counter(), ["inherited-red inventory requires schema_version=1, sealed_prior, and current lists"]

    counts, problems = {}, []
    for field in ("sealed_prior", "current"):
        counts[field] = Counter()
        for entry in inventory[field]:
            if (not isinstance(entry, dict)
                    or any(not isinstance(entry.get(key), str) or not entry[key].strip() for key in INHERITED_RED_FIELDS)
                    or entry["repo"] not in REPO
                    or type(entry.get("count", 1)) is not int or entry.get("count", 1) < 1):
                problems.append(f"inherited-red {field}: invalid entry; expected a repo, workflow, job, id and positive count")
                continue
            key = tuple(entry[name] for name in INHERITED_RED_FIELDS)
            counts[field][key] += entry.get("count", 1)
    for key, excess in (counts["current"] - counts["sealed_prior"]).items():
        problems.append(f"inherited-red {'/'.join(key)} exceeds the sealed prior count by {excess}")
    return counts["current"] & counts["sealed_prior"], problems


def check_inherited_red_observations(approved: Counter, rows: list[dict]) -> list[str]:
    red, green = Counter(), Counter()
    for row in rows:
        key = row_red_key(row)
        if row["candidate"] in INHERITED_RED_STATUSES:
            red[key] += 1
        elif row["candidate"] in ("PASS", "XFAIL", "XPASS"):
            green[key] += 1
    problems = []
    for key, excess in (Counter(approved) - red).items():
        label = "/".join(key)
        fixed = min(excess, green[key])
        if fixed:
            problems.append(f"inherited-red {label}: {fixed} fixed occurrence(s); remove them from current")
        if excess > fixed:
            problems.append(f"inherited-red {label}: {excess - fixed} reviewed occurrence(s) lack R14 evidence")
    return problems


def inherited_red_proposal(rows: list[dict]) -> dict:
    """Propose every observed R14 red occurrence without changing the reviewed inventory."""
    entries = []
    ordinals = Counter()
    for row in rows:
        if row["candidate"] not in INHERITED_RED_STATUSES:
            continue
        key = row_red_key(row)
        ordinals[key] += 1
        entries.append({
            **dict(zip(INHERITED_RED_FIELDS, key)),
            "occurrence": ordinals[key], "kind": row.get("kind", "test"),
            "classification": "red-on-both" if row["r13"] in INHERITED_RED_STATUSES else "R14-only",
            "r13_status": row["r13"], "r14_status": row["candidate"],
            "candidate_job": row.get("candidate_job"), "job_id": row.get("candidate_job_id"),
            "run_id": row.get("candidate_run_id"), "attempt": row.get("candidate_attempt"),
        })
    return {"schema_version": 1, "purpose": "Proposed R14 reds for review; grants no approvals",
            "counts": red_summary(rows), "reds": entries}


def write_inherited_red_candidate_list(path: Path, proposal: dict) -> None:
    # Creation only. A proposal must never overwrite the reviewed inventory.
    with path.open("x") as f:
        json.dump(proposal, f, indent=2)
        f.write("\n")


def api(path: str) -> bytes:
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
            if not isinstance(workflows, dict) or not workflows:
                raise ValueError(f"{side}/{product}: no workflow run IDs")
            for wf in REQUIRED[product]:
                if type(workflows.get(wf)) is not int or workflows[wf] < 1:
                    raise ValueError(f"{side}/{product}: missing run ID for {wf}")
            records[product][side] = {}
            for workflow, run_id in workflows.items():
                if type(run_id) is not int or run_id < 1:
                    raise ValueError(f"{side}/{product}/{workflow}: missing run ID")
                prefix = f"/{REPO[product]}/actions/runs/{run_id}"
                attempt = source.get("attempts", {}).get(workflow, 1)
                if type(attempt) is not int or attempt < 1:
                    raise ValueError(f"{side}/{product}/{workflow}: invalid run attempt")
                attempt_prefix = f"{prefix}/attempts/{attempt}"
                r = get_json(attempt_prefix)
                if r.get("head_sha") != sha or r.get("name") != workflow or r.get("status") != "completed":
                    raise ValueError(f"{side}/{product}/{workflow} run {run_id}: wrong SHA/name or incomplete")
                if r.get("id") != run_id or r.get("run_attempt") != attempt:
                    raise ValueError(f"{side}/{product}/{workflow}: expected attempt {attempt}, got {r.get('run_attempt')}")
                jobs = []
                page = 1
                while True:
                    payload = get_json(f"{attempt_prefix}/jobs?per_page=100&page={page}")
                    jobs.extend(payload.get("jobs", []))
                    if len(payload.get("jobs", [])) < 100:
                        break
                    page += 1
                if not jobs:
                    raise ValueError(f"{side}/{product}/{workflow}: no jobs")
                d = out / "raw" / product / side / f"{run_id}-{attempt}"
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
                    if job.get("run_attempt", attempt) != attempt:
                        raise ValueError(f"{side}/{product}/{workflow}: {name} returned from another attempt")
                    job_id = job["id"]
                    path = d / f"{job_id}.log"
                    log_error = None
                    log = b""
                    if job["conclusion"] != "skipped":
                        try:
                            log = api(f"/{REPO[product]}/actions/jobs/{job_id}/logs")
                        except urllib.error.HTTPError as exc:
                            if exc.code not in (404, 410):
                                raise
                            log_error = f"job log unavailable (HTTP {exc.code})"
                        if not log and not log_error:
                            log_error = "job log empty"
                    path.write_bytes(log)
                    failed_steps = [s["name"] for s in job.get("steps", []) if s.get("conclusion") == "failure"]
                    clean_jobs.append({
                        "name": name, "id": job_id, "attempt": attempt,
                        "conclusion": job["conclusion"], "log": str(path),
                        "failed_steps": failed_steps, "log_error": log_error,
                    })
                records[product][side][workflow] = {"id": run_id, "sha": sha, "conclusion": r.get("conclusion"), "attempt": attempt, "jobs": clean_jobs}
    return records


JOB_ID = "[job]"
UNATTRIBUTED_SKIP_ID = "[unattributed skip]"
SETUP_STEP = re.compile(r"^(?:set\s*up|install|check\s*out|configure|build|bootstrap|prepare)\b", re.I)


def job_inventory(product, workflow, side, run, vitest, playwright, junit, problems):
    inventory = {}
    for job in (run or {}).get("jobs", []):
        name = job["name"]
        if name in inventory:
            raise ValueError(f"{product}/{workflow}/{side}: duplicate job name {name}")
        label = f"{product}/{workflow}/{name} ({side})"
        path = job.get("log")
        conclusion = job["conclusion"]
        skipped = conclusion == "skipped"
        failed_steps = job.get("failed_steps", [])
        setup = conclusion == "failure" and any(SETUP_STEP.match(step) for step in failed_steps)
        log = Path(path).read_text(errors="replace") if path and Path(path).is_file() else ""
        if not skipped and path and not Path(path).is_file():
            problems.append(f"{label}: job log missing or empty")
        unattributed_skips = 0
        if product != "app":
            ids, unattributed_skips = pytest_job_results(log)
            if unattributed_skips:
                problems.append(f"{label}: no IDs for {unattributed_skips} reported pytest skip occurrence(s)")
            needs_ids = (
                (product == "agent" and ("unit shard" in name or "integration shard" in name))
                or (product == "runtime" and name.startswith(("unit", "portability-lifecycle", "sandbox-process-control")))
                or (product == "vibecomfy" and name == "test")
            )
            if needs_ids and not ids and not setup and not skipped:
                problems.append(f"{label}: complete test ID inventory required")
        elif (workflow, name) == ("Tests", "vitest"):
            if skipped:
                ids = {}
            elif junit.get(side):
                ids = parse_junit_xml(junit[side])
            elif vitest.get(side):
                ids = parse_vitest_multiset(vitest[side])
            else:
                ids = {}
                if not setup:
                    problems.append(f"{label}: assertion-level Vitest JSON or JUnit XML required")
        else:
            report = playwright.get(f"{side}/{workflow}/{name}")
            if report and skipped:
                problems.append(f"{label}: native input supplied for a skipped job")
            ids = parse_playwright_json(report) if report and not skipped else parse_playwright(log)
            needs_native = (
                workflow == "E2E" and name.startswith(("playwright-", "extension-"))
                or workflow == "Direct Journey" and name in ("direct-journey", "three-products")
                or workflow == "Lanes" and name in ("quick-journey", "checkout-lanes")
            )
            if needs_native and not report and not setup and not skipped:
                problems.append(f"{label}: complete native Playwright JSON required")
        if skipped:
            ids = {}
        ids = occurrences(ids)
        has_red = any(INHERITED_RED_STATUSES.intersection(states) for states in ids.values())
        job_outcome = (
            "SKIP" if skipped else
            "ERROR" if setup or conclusion not in ("success", "failure") else
            "FAIL" if conclusion == "failure" and not has_red else
            "PASS"
        )
        inventory[name] = {
            **job, "ids": ids, "run_id": run.get("id", ""), "attempt": job.get("attempt", run.get("attempt", "")),
            "setup": setup, "job_outcome": job_outcome,
            "emit_job_row": not ids or job_outcome != "PASS", "unattributed_skips": unattributed_skips,
        }
    return inventory


def renamed_to(aliases, key, original, description, problems):
    if key not in aliases:
        return original
    entry = aliases[key]
    if not isinstance(entry, dict) or any(not isinstance(entry.get(k), str) or not entry[k].strip()
                                         for k in ("to", "reason", "source")):
        problems.append(f"{key}: {description} rename lacks to/reason/source")
        return original
    return entry["to"]


def job_columns(old, new):
    columns = {}
    for role, job in (("r13", old), ("candidate", new)):
        job = job or {}
        columns.update({
            f"{role}_job": job.get("name", "MISSING"), f"{role}_job_id": job.get("id", ""),
            f"{role}_run_id": job.get("run_id", ""), f"{role}_attempt": job.get("attempt", ""),
        })
    return columns


def status_pairs(old, new):
    """Match identical outcomes first, then pair remaining red outcomes by count."""
    old, new = Counter(old), Counter(new)
    common = old & new
    for state in sorted(common, key=lambda state: (state == "PASS", state)):
        for _ in range(common[state]):
            yield state, state
    adverse_first = lambda state: (state not in INHERITED_RED_STATUSES, state)
    yield from zip_longest(sorted((old - common).elements(), key=adverse_first),
                           sorted((new - common).elements(), key=adverse_first), fillvalue="MISSING")


def test_classification(before, after):
    if before == after:
        return "same"
    if after == "MISSING":
        return "lost-or-regressed"
    if after in INHERITED_RED_STATUSES:
        return "failing-added" if before == "MISSING" else "red-on-both" if before in INHERITED_RED_STATUSES else "regressed"
    if before in INHERITED_RED_STATUSES and after == "PASS":
        return "fixed"
    return "changed"


def compare_job(product, workflow, old, new, id_aliases, dispositions, problems):
    identity = job_columns(old, new)
    name = (new or old)["name"]
    context = {"product": product, "workflow": workflow, "job": name, **identity}
    jobs = dict(context)
    for role, job in (("r13", old), ("candidate", new)):
        jobs[role] = job["conclusion"] if job else "MISSING"
        jobs[f"{role}_id_count"] = sum(map(len, job["ids"].values())) if job else 0
        jobs[f"{role}_failed_steps"] = ", ".join(job.get("failed_steps", [])) if job else ""
        jobs[f"{role}_setup"] = job["setup"] if job else ""

    mapped = {}
    for ident, states in (old["ids"] if old else {}).items():
        target = renamed_to(id_aliases, f"{product}/{workflow}/{ident}", ident, "test", problems)
        if target in mapped:
            problems.append(f"{product}/{workflow}/{name}: multiple R13 IDs map to {target}")
        mapped.setdefault(target, []).extend((ident, state) for state in states)
    destination = new["ids"] if new else {}
    rows = []
    for ident in sorted(mapped.keys() | destination.keys()):
        previous = mapped.get(ident, [])
        original = previous[0][0] if previous else ""
        disposition = dispositions.get(f"{product}/{workflow}/{ident}", {})
        for before, after in status_pairs([state for _, state in previous], destination.get(ident, [])):
            rows.append({
                **context, "kind": "test", "id": ident, "r13_id": original if before != "MISSING" else "",
                "r13": before, "candidate": after, "classification": test_classification(before, after),
                "explanation": disposition.get("reason", ""), "source": disposition.get("source", ""),
            })
    if any(job and job["emit_job_row"] for job in (old, new)):
        before = old["job_outcome"] if old else "MISSING"
        after = new["job_outcome"] if new else "MISSING"
        rows.append({**context, "kind": "job", "id": JOB_ID, "r13_id": JOB_ID if old else "",
                     "r13": before, "candidate": after, "classification": test_classification(before, after)})
    old_skips = ["SKIP"] * (old or {}).get("unattributed_skips", 0)
    new_skips = ["SKIP"] * (new or {}).get("unattributed_skips", 0)
    for before, after in status_pairs(old_skips, new_skips):
        rows.append({**context, "kind": "job", "id": UNATTRIBUTED_SKIP_ID,
                     "r13_id": UNATTRIBUTED_SKIP_ID if before != "MISSING" else "",
                     "r13": before, "candidate": after, "classification": test_classification(before, after)})
    return rows, jobs


def reconcile_agent_shards(rows):
    """Recognize an unambiguous move between Agent shards of the same suite."""
    missing, added = {}, {}
    for index, row in enumerate(rows):
        family = {"CI": "unit shard ", "Lanes": "integration shard "}.get(row["workflow"])
        if row["product"] != "agent" or row["kind"] != "test" or not family or not row["job"].startswith(family):
            continue
        key = row["workflow"], row["id"]
        if row["candidate"] == "MISSING":
            missing.setdefault(key, []).append(index)
        elif row["r13"] == "MISSING":
            added.setdefault(key, []).append(index)
    consumed = set()
    for key in missing.keys() & added.keys():
        if len(missing[key]) != 1 or len(added[key]) != 1:
            continue
        old_index, new_index = missing[key][0], added[key][0]
        old, new = rows[old_index], rows[new_index]
        for field in ("r13", "r13_id", "r13_job", "r13_job_id", "r13_run_id", "r13_attempt"):
            new[field] = old[field]
        new["classification"] = test_classification(new["r13"], new["candidate"])
        consumed.add(old_index)
    return [row for index, row in enumerate(rows) if index not in consumed]


def evaluate(manifest: dict, records: dict, out: Path, vitest: dict, playwright: dict | None = None,
             junit: dict | None = None, *, approved_counts: Counter | None = None) -> tuple[list[dict], list[dict], list[str]]:
    rows, jobs, problems = [], [], []
    aliases = manifest.get("job_renames", {})
    id_aliases = manifest.get("test_id_renames", {})
    dispositions = manifest.get("dispositions", {})
    playwright, junit = playwright or {}, junit or {}

    for product, sides in records.items():
        for workflow in sorted(sides["baseline"].keys() | sides["candidate"].keys()):
            base_run = sides["baseline"].get(workflow)
            candidate_run = sides["candidate"].get(workflow)
            if not base_run or not candidate_run:
                problems.append(f"{product}/{workflow}: workflow missing from one side")
            old = job_inventory(product, workflow, "baseline", base_run, vitest, playwright, junit, problems)
            new = job_inventory(product, workflow, "candidate", candidate_run, vitest, playwright, junit, problems)
            links = []
            for name, job in sorted(old.items()):
                target = renamed_to(aliases, f"{product}/{workflow}/{name}", name, "job", problems)
                match = new.pop(target, None)
                if not match:
                    problems.append(f"{product}/{workflow}: lost job {name}")
                links.append((job, match))
            links.extend((None, job) for _, job in sorted(new.items()))
            for before, after in links:
                compared, job = compare_job(product, workflow, before, after, id_aliases, dispositions, problems)
                rows.extend(compared)
                jobs.append(job)

    rows = reconcile_agent_shards(rows)
    candidate_reds = {}
    for row in rows:
        if row["candidate"] in INHERITED_RED_STATUSES:
            candidate_reds.setdefault(row_red_key(row), []).append(row)
    for key, observations in candidate_reds.items():
        approved = (approved_counts or {}).get(key, 0)
        by_introduction = sorted(observations, key=lambda row: row["r13"] not in INHERITED_RED_STATUSES)
        unapproved = Counter((row["r13"] not in INHERITED_RED_STATUSES, row["candidate"])
                             for row in by_introduction[approved:])
        for (new, status), count in unapproved.items():
            origin = "added" if new else "shared"
            problems.append(f"{'/'.join(key)}: {origin} {count} {status} occurrence(s) BLOCKS publish (exceeds approval ceiling)")
    for row in rows:
        if row["kind"] == "test" and row["candidate"] == "MISSING":
            label = "/".join(row_red_key(row))
            problems.append(f"{label}: disappearance requires destination/reason/source and a present destination; BLOCKS publish")
    return rows, jobs, problems


def check_canonical_baseline_diff(records: dict, out: Path) -> list[str]:
    """Run env/baseline-diff.py on all original -rA Agent shard logs.

    This diagnostic aggregates IDs across shards. The job-specific results and
    reviewed inherited-red inventory govern the publication verdict.
    """
    script = Path(__file__).resolve().parents[3] / "env" / "baseline-diff.py"
    if not script.is_file():
        return [f"required canonical comparator missing: {script}"]
    problems = []
    for wf, fragment in (("CI", "unit shard"), ("Lanes", "integration shard")):
        files = {}
        for side in ("baseline", "candidate"):
            run = records["agent"][side].get(wf, {})
            selected = [j for j in run.get("jobs", []) if fragment in j["name"]]
            expected = 8 if wf == "CI" else 4
            if len(selected) != expected:
                problems.append(f"agent/{wf}: expected {expected} original shards, found {len(selected)} on {side}")
                continue
            paths = []
            for j in selected:
                clean_path = out / "canonical-inputs" / wf / side / f"{j['id']}.log"
                clean_path.parent.mkdir(parents=True, exist_ok=True)
                path = j.get("log")
                log = Path(path).read_text(errors="replace") if path and Path(path).is_file() else ""
                clean_path.write_text("\n".join(clean(x) for x in log.splitlines()) + "\n")
                paths.append(str(clean_path))
            files[side] = paths
        if len(files) != 2:
            continue
        location = out / f"baseline-diff-{wf.lower()}"
        result = subprocess.run([sys.executable, "-I", str(script), "--baseline", "published-R13=" + ",".join(files["baseline"]), "--candidate", ",".join(files["candidate"]), "--out", str(location)], capture_output=True, text=True, timeout=120)
        (out / f"canonical-{wf.lower()}.txt").write_text(f"Exit {result.returncode}\n{result.stdout}\nSTDERR:\n{result.stderr}")
    return problems


def write_csv(path: Path, rows: list[dict], columns: list[str]) -> None:
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def read_rehearsal_records(path: Path, manifest: dict) -> dict:
    """Read precollected observations for a rehearsal that cannot qualify publication."""
    records = json.loads(path.read_text())
    if set(records) != set(REPO):
        raise ValueError("rehearsal needs records for all four repositories")
    for product, sides in records.items():
        for side in ("baseline", "candidate"):
            source = manifest[side][product]
            for workflow, run in sides[side].items():
                attempt = source.get("attempts", {}).get(workflow, 1)
                if (run["id"], run["sha"], run["attempt"]) != (source["workflows"][workflow], source["sha"], attempt):
                    raise ValueError(f"{side}/{product}/{workflow}: rehearsal records do not match manifest")
    return records


def red_summary(rows: list[dict]) -> dict:
    summary = {product: dict.fromkeys(("r13_red", "r14_red", "red_on_both", "r14_only", "fixed"), 0)
               for product in REPO}
    for row in rows:
        count = summary[row["product"]]
        old_red = row["r13"] in INHERITED_RED_STATUSES
        new_red = row["candidate"] in INHERITED_RED_STATUSES
        count["r13_red"] += old_red
        count["r14_red"] += new_red
        count["red_on_both"] += old_red and new_red
        count["r14_only"] += not old_red and new_red
        count["fixed"] += old_red and row["candidate"] == "PASS"
    return summary


def write_r14_only(path: Path, rows: list[dict]) -> None:
    groups = {}
    for row in rows:
        if row["candidate"] in INHERITED_RED_STATUSES and row["r13"] not in INHERITED_RED_STATUSES:
            key = row["product"], row["workflow"], row.get("candidate_job") or row["job"]
            groups.setdefault(key, []).append(row)
    with path.open("w") as f:
        print("# Observed R14-only red occurrences", file=f)
        print("\nA missing baseline observation is shown as MISSING.", file=f)
        for (product, workflow, job), group in sorted(groups.items()):
            print(f"\n## {product} / {workflow} / {job}\n", file=f)
            for row in group:
                print(f"- `{row['id']}` ({row['r13']} → {row['candidate']})", file=f)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--inherited-red", type=Path, default=DEFAULT_INHERITED_RED,
                    help="reviewed shrink-only inventory")
    ap.add_argument("--generate-candidate-list", type=Path, metavar="NEW_PATH",
                    help="write proposed red entries for review; grants no approvals")
    ap.add_argument("--rehearsal-records", type=Path,
                    help="compare existing job records without qualifying publication")
    ap.add_argument("--vitest-json-r13", type=Path, help="full R13 Vitest JSON reporter output")
    ap.add_argument("--vitest-json-r14", type=Path, help="full candidate Vitest JSON reporter output")
    ap.add_argument("--junit-xml-r13", type=Path, help="full R13 JUnit XML reporter output")
    ap.add_argument("--junit-xml-r14", type=Path, help="full candidate JUnit XML reporter output")
    ap.add_argument("--playwright-json", action="append", default=[], metavar="SIDE/WORKFLOW/JOB=PATH",
                    help="native per-ID JSON reporter for dot-output E2E/Lanes jobs, on BOTH sides")
    ap.add_argument("--playwright-inputs", type=Path,
                    help="JSON object mapping SIDE/WORKFLOW/JOB to a native Playwright JSON path")
    a = ap.parse_args(argv)
    try:
        playwright_specs = []
        if a.playwright_inputs:
            mapping = json.loads(a.playwright_inputs.read_text())
            if not isinstance(mapping, dict) or any(not isinstance(p, str) or not p for p in mapping.values()):
                raise ValueError("Playwright inputs must map SIDE/WORKFLOW/JOB to nonempty paths")
            playwright_specs.extend(mapping.items())
        for spec in a.playwright_json:
            key, sep, value = spec.partition("=")
            if not sep:
                raise ValueError(f"invalid --playwright-json: {spec}")
            playwright_specs.append((key, value))
        playwright = {}
        for key, value in playwright_specs:
            binding = key.split("/", 2)
            if len(binding) != 3 or binding[0] not in ("baseline", "candidate") or not all(binding) or not value or key in playwright:
                raise ValueError(f"invalid or duplicate Playwright binding: {key}")
            playwright[key] = Path(value)
        for side, json_report, junit_report in (("baseline", a.vitest_json_r13, a.junit_xml_r13),
                                                ("candidate", a.vitest_json_r14, a.junit_xml_r14)):
            if json_report and junit_report:
                raise ValueError(f"{side}: supply either Vitest JSON or JUnit XML")
        junit = {"baseline": a.junit_xml_r13, "candidate": a.junit_xml_r14}
        inputs = {f"app/Tests/{k}/vitest": p for k, p in {"baseline": a.vitest_json_r13, "candidate": a.vitest_json_r14}.items() if p}
        inputs.update({f"app/{key}/junit": path for key, path in junit.items() if path})
        inputs.update({f"app/{key}/playwright": path for key, path in playwright.items()})
        native_input_digests = {}
        for key, p in inputs.items():
            native_input_digests[key] = {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                                         "provenance": "MUST VERIFY run SHA, attempt, job, artifact/command before sign-off"}
        m = json.loads(a.manifest.read_text())
        inventory = json.loads(a.inherited_red.read_text())
        a.out.mkdir(parents=True, exist_ok=True)
        (a.out / "native-report-input-digests.json").write_text(json.dumps(native_input_digests, indent=2) + "\n")
        records = read_rehearsal_records(a.rehearsal_records, m) if a.rehearsal_records else collect_runs(m, a.out)
        (a.out / "resolved-runs.json").write_text(json.dumps(records, indent=2) + "\n")
        approved, inventory_problems = reviewed_inherited_red_counts(inventory)
        rows, jobs, problems = evaluate(m, records, a.out, {"baseline": a.vitest_json_r13, "candidate": a.vitest_json_r14},
                                        playwright, junit, approved_counts=approved)
        problems.extend(inventory_problems)
        problems.extend(check_inherited_red_observations(approved, rows))
        if a.generate_candidate_list:
            write_inherited_red_candidate_list(a.generate_candidate_list, inherited_red_proposal(rows))
        if a.rehearsal_records:
            problems.append("Rehearsal uses precollected records and cannot qualify publication.")
        for product, sides in records.items():
            for side, workflows in sides.items():
                for workflow, run in workflows.items():
                    if run.get("conclusion") not in ("success", "failure"):
                        problems.append(f"{side}/{product}/{workflow}: run {run['id']} ended {run.get('conclusion')}")
                    for job in run["jobs"]:
                        if job.get("log_error"):
                            problems.append(f"{side}/{product}/{workflow}/{job['name']}: {job['log_error']}")
        pw_outcomes = {}
        for key, path in playwright.items():
            side, workflow, job = key.split("/", 2)
            run = records["app"][side].get(workflow, {})
            matches = [j for j in run.get("jobs", []) if j["name"] == job]
            if len(matches) != 1:
                problems.append(f"app/{key}: native input has no matching job")
                continue
            pw_outcomes[key] = {"run_id": run["id"], "job": job, "job_id": matches[0]["id"],
                                "attempt": matches[0]["attempt"], "tests": parse_playwright_json_outcomes(path)}
        (a.out / "playwright-expected-actual.json").write_text(json.dumps(pw_outcomes, indent=2) + "\n")
        counts = red_summary(rows)
        (a.out / "counts.json").write_text(json.dumps(counts, indent=2) + "\n")
        write_r14_only(a.out / "r14-only.md", rows)
        problems.extend(check_canonical_baseline_diff(records, a.out))
        job_identity = ["r13_job", "candidate_job", "r13_run_id", "candidate_run_id",
                        "r13_job_id", "candidate_job_id", "r13_attempt", "candidate_attempt"]
        write_csv(a.out / "all-test-ids.csv", rows, ["product", "workflow", "job", "kind", "id", "r13_id",
                  "r13", "candidate", "classification", "explanation", "source", *job_identity])
        write_csv(a.out / "jobs.csv", jobs, ["product", "workflow", "r13", "candidate", *job_identity,
                  "r13_id_count", "candidate_id_count", "r13_setup", "candidate_setup",
                  "r13_failed_steps", "candidate_failed_steps"])
        counter = Counter(x["classification"] for x in rows)
        changes = [x for x in rows if x["classification"] != "same"]
        table = ["# R14 publication comparison", "",
                 "| Repo | R13 red | R14 red | Red on both | R14 only | Fixed |",
                 "|---|---:|---:|---:|---:|---:|"]
        table.extend(f"| {product} | " + " | ".join(map(str, totals.values())) + " |"
                     for product, totals in counts.items())
        table += ["", "Counts include observed test occurrences and job-level records. See `r14-only.md`.",
                  "", "| Native ID classification | Count |", "|---|---:|"]
        table.extend(f"| {name} | {count} |" for name, count in sorted(counter.items()))
        table += ["", f"Changed IDs: {len(changes)} (complete table: \u0060all-test-ids.csv\u0060)", "", "## Job-level evidence", "", "| Repo/workflow | R13 job | R13 / attempt | Candidate job | Candidate / attempt |", "|---|---|---|---|---|"]
        table.extend(f"| {j['product']}/{j['workflow']} | {j['r13_job']} | {j['r13']} / {j.get('r13_attempt', '')} | {j['candidate_job']} | {j['candidate']} / {j.get('candidate_attempt', '')} |" for j in jobs)
        table += ["", "## Outstanding / blockers", ""]
        table.extend("- " + p for p in sorted(set(problems)))
        (a.out / "report.md").write_text("\n".join(table) + "\n")
        print("Saved", a.out / "report.md", a.out / "all-test-ids.csv", a.out / "jobs.csv")
        print(f"ID rows={len(rows)}; job rows={len(jobs)}; outstanding={len(set(problems))}")
        return 1 if problems else 0
    except (ValueError, KeyError, OSError, ET.ParseError, subprocess.TimeoutExpired) as e:
        print("INCOMPLETE (no qualifying verdict):", e, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
