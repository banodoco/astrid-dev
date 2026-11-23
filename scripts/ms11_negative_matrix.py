#!/usr/bin/env python3
"""MS11 pre-cutover negative matrix on an isolated exact-SHA Git checkout.

This checks bounded, explicitly expected refusals. It is not MS11 completion,
a D5 cutover, an independent reviewer or a real Claude/Codex client run.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

SOURCE = Path(__file__).resolve().parents[1]
ROLE_DUPLICATE = """---
description: A disposable duplicate skill identity for a negative migration probe.
skill: true
---

# Gap role

## Responsibility

Demonstrate that duplicate generated identities are refused.

## Authority

Do not change any real role or persistent source.

## Responsibilities

Run only within the disposable checkout.

## Handoff

Record the negative validation result.
"""
WORKSTREAM = """---
description: A disposable workstream to probe missing-reference refusal.
skill: true
---

# MS11 broken link

## When to use

Use only for the isolated negative validation probe.

## Outcome

A failed build with the original packages untouched.

## Inputs

The exact source revision and temporary checkout.

## Procedure

Follow the [missing target](../../definitely-not-there-ms11.md).
Report that this link must be refused.

## Completion

A failed validation is recorded, without publishing a package.
"""
INVALID_FLAG = WORKSTREAM.replace("skill: true", "skill: yes")
LIMITATIONS = [
    "Hosted Linux and this exact repository candidate only: no macOS/Windows claims.",
    "No real Claude/Codex picker, authenticated session or fresh independent agent.",
    "No hostile concurrent writer, crash/reboot, power loss or general orphan recovery proof.",
    "All mutations are limited to a disposable detached checkout and temporary skill roots.",
    "Expected nonzero refusals count as negative-case success only when the named error and unchanged output are verified.",
    "The original RS1 technical BLOCK, D5 hold, MS7/MS9, formal R and owner main GO are unchanged.",
]


def snapshot(repo: Path) -> dict[str, str]:
    result = {}
    for item in (repo / ".generated/skills").iterdir():
        if item.is_dir() and not item.is_symlink():
            result[item.name] = hashlib.sha256((item / "SKILL.md").read_bytes()).hexdigest()
    return dict(sorted(result.items()))


def execute(report: dict, label: str, argv: list[str], cwd: Path, env: dict, *, refusal: str | None = None):
    proc = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, text=True,
                          errors="replace", timeout=180, check=False)
    report["commands"].append({
        "step": label, "argv": argv, "cwd": str(cwd), "exit": proc.returncode,
        "stdout": proc.stdout, "stderr": proc.stderr, "expected_refusal": refusal,
    })
    combined = proc.stdout + "\n" + proc.stderr
    if refusal is None and proc.returncode != 0:
        raise AssertionError(f"{label}: expected exit zero, got {proc.returncode}: {combined[-1200:]}")
    if refusal is not None and (proc.returncode == 0 or refusal not in combined):
        raise AssertionError(f"{label}: expected nonzero and {refusal!r}; exit={proc.returncode}; {combined[-1200:]}")
    return proc.stdout


def verify(report: dict, title: str, condition: bool, evidence: object):
    report["assertions"].append({"name": title, "pass": bool(condition), "evidence": evidence})
    if not condition:
        raise AssertionError(f"{title}: {evidence}")


def write_report(folder: Path, report: dict):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "ms11-negative-matrix.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    fence = chr(96) * 3
    lines = [
        "# Plan 73 MS11 — isolated negative-matrix preparation",
        "",
        "**Status:** " + report["status"],
        "**Exact source SHA:** " + report["source_sha"],
        "**Environment:** GitHub Actions hosted Linux disposable checkout",
        "**Scope:** baseline, fail-closed duplicate, broken link, bad frontmatter, package drift and foreign installation collision",
        "",
        "This is a preparatory negative matrix; it does not certify MS11, MS10, or a D5 cutover.",
        "",
        "## Invariant assertions",
        "",
        "| Assertion | Result | Evidence |", "| --- | --- | --- |",
    ]
    for result in report["assertions"]:
        detail = str(result["evidence"]).replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {result['name']} | {'PASS' if result['pass'] else 'FAIL'} | {detail} |")
    lines.extend(["", "## Exact command receipts", ""])
    for cmd in report["commands"]:
        lines.extend([
            "### " + cmd["step"], "",
            "Arguments: " + json.dumps(cmd["argv"]),
            "cwd: " + cmd["cwd"],
            "Exit: " + str(cmd["exit"]),
            "Expected refusal: " + str(cmd["expected_refusal"]),
            "",
            fence + "text", "stdout:", cmd["stdout"] or "(empty)",
            "stderr:", cmd["stderr"] or "(empty)", fence, "",
        ])
    lines.extend(["## Limitations", ""])
    lines.extend("- " + x for x in LIMITATIONS)
    if report["error"]:
        lines.extend(["", "## Error", "", report["error"]])
    (folder / "ms11-negative-matrix.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def matrix(sha: str, output: Path):
    report = {
        "source_sha": sha, "status": "RUNNING", "assertions": [],
        "commands": [], "limitations": LIMITATIONS, "error": None,
    }
    try:
        verify(report, "exact 40-character source commit", bool(re.fullmatch(r"[a-f0-9]{40}", sha)), sha)
        verify(report, "report directory outside source checkout",
               not output.resolve().is_relative_to(SOURCE.resolve()), str(output))
        original_before = subprocess.check_output(
            ["git", "status", "--porcelain", "--untracked-files=no"], cwd=SOURCE, text=True)
        with tempfile.TemporaryDirectory(prefix="p73-ms11-negative-") as d:
            base = Path(d)
            repo, home = base / "repo", base / "home"
            home.mkdir()
            env = os.environ.copy()
            env.update({
                "HOME": str(home), "GIT_TERMINAL_PROMPT": "0",
                "PYTHONDONTWRITEBYTECODE": "1", "GIT_CONFIG_GLOBAL": os.devnull,
            })

            def git(label, *args):
                return execute(report, label, ["git", *args], base, env)

            def cli(label, action, *options, refusal=None):
                return execute(report, label, ["python3", "scripts/astrid_dev.py",
                               "skills", action, *options], repo, env, refusal=refusal)

            git("create temporary checkout", "init", "-q", str(repo))
            git("fetch exact source locally", "-C", str(repo), "fetch",
                "-q", "--no-tags", str(SOURCE), sha)
            git("detach at exact source", "-C", str(repo), "checkout", "-q", "--detach", "FETCH_HEAD")
            observed = git("verify exact checkout", "-C", str(repo), "rev-parse", "HEAD").strip()
            verify(report, "source SHA matches detached checkout", observed == sha, observed)

            cli("build exact baseline", "build")
            cli("check exact baseline", "check")
            baseline = snapshot(repo)
            verify(report, "expected original identity subset present",
                   len(baseline) >= 14 and {"astrid-dev-start", "astrid-dev-manager",
                   "astrid-dev-gap", "astrid-dev-iterate"}.issubset(baseline),
                   {"number": len(baseline), "required_subset": True})

            duplicate = repo / "agent/roles/gap.md"
            verify(report, "duplicate negative source absent", not duplicate.exists(), str(duplicate))
            try:
                duplicate.write_text(ROLE_DUPLICATE, encoding="utf-8")
                cli("refuse duplicate opted-in skill name", "build",
                    refusal="duplicate skill name astrid-dev-gap")
                verify(report, "duplicate rejection preserves published packages",
                       snapshot(repo) == baseline, "all generated SKILL.md content hashes unchanged")
            finally:
                duplicate.unlink(missing_ok=True)
            cli("check after duplicate refusal", "check")

            missing = repo / "agent/shared/workstreams/ms11-broken-link.md"
            verify(report, "broken-link probe source absent", not missing.exists(), str(missing))
            try:
                missing.write_text(WORKSTREAM, encoding="utf-8")
                cli("refuse missing authored Markdown link", "build", refusal="missing link target")
                verify(report, "link rejection preserves published packages",
                       snapshot(repo) == baseline, "all package hashes unchanged")
            finally:
                missing.unlink(missing_ok=True)
            cli("check after missing-link refusal", "check")

            bad = repo / "agent/shared/workstreams/ms11-invalid-flag.md"
            verify(report, "malformed metadata source absent", not bad.exists(), str(bad))
            try:
                bad.write_text(INVALID_FLAG, encoding="utf-8")
                cli("refuse nonboolean skill metadata", "build", refusal="literal boolean")
                verify(report, "metadata rejection preserves package set",
                       snapshot(repo) == baseline, "all package hashes unchanged")
            finally:
                bad.unlink(missing_ok=True)
            cli("check after malformed-metadata refusal", "check")

            manager_file = repo / ".generated/skills/astrid-dev-manager/SKILL.md"
            original = manager_file.read_bytes()
            try:
                manager_file.write_bytes(original + b"\nMS11-DRIFT-PROBE\n")
                cli("detect generated package content drift", "check",
                    refusal="astrid-dev-manager: generated SKILL.md is stale")
                verify(report, "check is read-only on tampered package",
                       manager_file.read_bytes().endswith(b"MS11-DRIFT-PROBE\n"),
                       "tamper remains until explicit rebuild")
            finally:
                # Restore original bytes even if the negative assertion failed.
                manager_file.write_bytes(original)
            cli("check restored exact package bytes", "check")
            verify(report, "published hashes restored after drift probe",
                   snapshot(repo) == baseline, "baseline restored exactly")

            target = base / "foreign-file" / "skills"
            target.mkdir(parents=True)
            collision = target / "astrid-dev-manager"
            collision.write_text("FOREIGN FILE - DO NOT MODIFY\n", encoding="utf-8")
            unrelated = target / "unrelated-user-skill"
            unrelated.write_text("USER FILE - DO NOT MODIFY\n", encoding="utf-8")
            expected_files = {p.name: p.read_bytes() for p in target.iterdir()}
            cli("dry-run refuses foreign desired-name file", "install",
                "--dry-run", "--destination", str(target), refusal="foreign installation entry")
            cli("actual install refuses foreign desired-name file", "install",
                "--destination", str(target), refusal="foreign installation entry")
            verify(report, "foreign-file refusal makes no partial destination changes",
                   {p.name: p.read_bytes() for p in target.iterdir()} == expected_files,
                   sorted(expected_files))

            linked = base / "foreign-link" / "skills"
            linked.mkdir(parents=True)
            outside = base / "separate-unmanaged-package"
            (linked / "astrid-dev-manager").symlink_to(outside, target_is_directory=True)
            raw = os.readlink(linked / "astrid-dev-manager")
            cli("dry-run refuses foreign desired-name symlink", "install",
                "--dry-run", "--destination", str(linked), refusal="foreign symlink")
            cli("actual install refuses foreign desired-name symlink", "install",
                "--destination", str(linked), refusal="foreign symlink")
            verify(report, "foreign symlink remains unchanged and no links are installed",
                   len(list(linked.iterdir())) == 1 and
                   (linked / "astrid-dev-manager").is_symlink() and
                   os.readlink(linked / "astrid-dev-manager") == raw,
                   {"foreign_link": raw, "entry_count": len(list(linked.iterdir()))})

            cli("final build is idempotent", "build")
            cli("final check", "check")
            verify(report, "all baseline packages remain byte-identical",
                   snapshot(repo) == baseline,
                   {"count": len(baseline), "exact_hashes_restored": True})
        original_after = subprocess.check_output(
            ["git", "status", "--porcelain", "--untracked-files=no"], cwd=SOURCE, text=True)
        verify(report, "original checked-out source remains unchanged",
               original_before == original_after, "tracked git status identical")
        report["status"] = "PASS"
    except (AssertionError, RuntimeError, OSError, subprocess.TimeoutExpired) as exc:
        report["status"] = "FAIL"
        report["error"] = f"{type(exc).__name__}: {exc}"
    finally:
        write_report(output, report)
        print("MS11_NEGATIVE_MATRIX_" + report["status"] + " exact_sha=" + sha, flush=True)
        for item in report["assertions"]:
            print(("PASS " if item["pass"] else "FAIL ") + item["name"], flush=True)
        if report["error"]:
            print(report["error"], file=sys.stderr, flush=True)
        print("MS11_EVIDENCE_DIR=" + str(output), flush=True)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-ref", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    raise SystemExit(matrix(args.source_ref, args.output_dir))
