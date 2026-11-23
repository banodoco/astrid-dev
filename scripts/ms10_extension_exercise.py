#!/usr/bin/env python3
"""MS10: scripted, disposable cold-start rehearsal of agent/README.md instructions.

A fresh LLM and real Claude/Codex skill menus are NOT exercised by this script.
"""
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
WORKSTREAM = "agent/shared/workstreams/extension-probe.md"
NAME = "astrid-dev-extension-probe"
TASK = ("Read agent/README.md. Add a shared workstream with skill: true; build, "
        "check, dry-run, install and load it in three disposable roots. "
        "Repeat for idempotence. Remove the flag, then prove owned-link "
        "retirement without changing the Markdown source or foreign skills.")
DOCUMENT = """---
description: Exercise safe temporary workstream discovery and retirement without modifying active Astrid rules.
skill: true
---

# Extension probe

## When to use

Use only for MS10 rehearsal in a disposable checkout.

## Outcome

Add and load a new workstream without changing established generated skills.

## Inputs

A staged authoring guide, a clean source and three disposable install roots.

## Procedure

Follow the [authoring guide](../../README.md#author-a-document).
Read this generated skill through its installed link and report what works.

## Completion

The workstream is loadable through the three generated skill links.
"""
LIMITS = [
    "Deterministic script, not a separately instructed fresh LLM agent.",
    "Symlinked SKILL.md loading does not prove actual Claude/Codex picker discovery.",
    "Linux hosted runner only; macOS, Windows, paid and credentialed clients not tested.",
    "D5, MS9 deletion, final MS10 acceptance, hostile-writer/power-loss guarantees not tested.",
]


def inventory(root):
    return {p.name: hashlib.sha256((p / "SKILL.md").read_bytes()).hexdigest()
            for p in (root / ".generated/skills").iterdir() if p.is_dir() and not p.is_symlink()}


def run(report, label, argv, cwd, env):
    done = subprocess.run(argv, cwd=cwd, env=env, capture_output=True,
                          text=True, errors="replace", timeout=180)
    report["commands"].append({
        "step": label, "argv": argv, "cwd": str(cwd),
        "exit": done.returncode, "stdout": done.stdout, "stderr": done.stderr,
    })
    if done.returncode:
        raise RuntimeError(f"{label}: exit {done.returncode}: {done.stderr[-1200:]}")
    return done.stdout


def check(report, label, yes, evidence):
    report["assertions"].append({"name": label, "pass": bool(yes), "evidence": evidence})
    if not yes:
        raise AssertionError(f"{label}: {evidence}")


def write_report(output, data):
    output.mkdir(parents=True, exist_ok=True)
    (output / "task.txt").write_text(TASK + "\n", encoding="utf-8")
    (output / "ms10-log.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    fence = chr(96) * 3
    lines = [
        "# Plan 73 MS10 — disposable authoring rehearsal", "",
        f"**Result:** {data['status']}",
        f"**Exact source SHA:** {data['source_sha']}", "",
        "**Scope:** scripted operator, not fresh AI agent acceptance.", "",
        "## Instructions from staged README", "", TASK, "",
        "## Assertions", "",
        "| Assertion | Result | Evidence |", "| --- | --- | --- |",
    ]
    for x in data["assertions"]:
        lines.append(f"| {x['name']} | {'PASS' if x['pass'] else 'FAIL'} | "
                     f"{str(x['evidence']).replace('|', ';')} |")
    lines += ["", "## Raw command receipts", ""]
    for x in data["commands"]:
        lines.extend([
            "### " + x["step"], "",
            "argv: " + json.dumps(x["argv"]),
            "cwd: " + x["cwd"], "exit: " + str(x["exit"]), "",
            fence + "text", "stdout:", x["stdout"] or "(empty)",
            "stderr:", x["stderr"] or "(empty)", fence, "",
        ])
    lines.extend(["## Limitations", ""])
    lines.extend("- " + s for s in LIMITS)
    if data["error"]:
        lines.extend(["", "## Error", "", data["error"]])
    (output / "ms10-log.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def exercise(sha, output):
    report = {"source_sha": sha, "status": "RUNNING", "task": TASK,
              "assertions": [], "commands": [], "limits": LIMITS, "error": None}
    try:
        check(report, "exact SHA supplied", bool(re.fullmatch("[a-f0-9]{40}", sha)), sha)
        check(report, "evidence outside source repo",
              not output.resolve().is_relative_to(SOURCE.resolve()), str(output))
        before = subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=no"],
                                         cwd=SOURCE, text=True)
        with tempfile.TemporaryDirectory(prefix="p73-ms10-") as name:
            temp = Path(name)
            repo, home = temp / "repo", temp / "home"
            home.mkdir()
            env = os.environ.copy()
            env.update({"HOME": str(home), "PYTHONDONTWRITEBYTECODE": "1",
                        "GIT_TERMINAL_PROMPT": "0", "GIT_CONFIG_GLOBAL": os.devnull})
            def git(label, *args):
                return run(report, label, ["git", *args], temp, env)
            def cli(label, *args):
                return run(report, label, ["python3", "scripts/astrid_dev.py",
                           "skills", *args], repo, env)

            git("init disposable checkout", "init", "-q", str(repo))
            git("fetch exact source locally", "-C", str(repo), "fetch",
                "-q", "--no-tags", str(SOURCE), sha)
            git("detach exact head", "-C", str(repo), "checkout",
                "-q", "--detach", "FETCH_HEAD")
            observed = git("identify checkout", "-C", str(repo), "rev-parse", "HEAD").strip()
            check(report, "checkout identity", observed == sha, observed)

            guide = (repo / "agent/README.md").read_text(encoding="utf-8")
            instructions = ["## Author a document", "## Build and install", "skill: true",
                "python3 scripts/astrid_dev.py skills build",
                "python3 scripts/astrid_dev.py skills check",
                "python3 scripts/astrid_dev.py skills install --dry-run --destination",
                "python3 scripts/astrid_dev.py skills install --destination"]
            check(report, "documented workflow available",
                  all(p in guide for p in instructions), instructions)

            source = repo / WORKSTREAM
            check(report, "new name not occupied", not source.exists(), WORKSTREAM)
            cli("baseline build", "build")
            cli("baseline check", "check")
            baseline = inventory(repo)
            check(report, "original packages present",
                  len(baseline) >= 14 and {"astrid-dev-start", "astrid-dev-manager",
                  "astrid-dev-iterate"}.issubset(baseline), len(baseline))

            source.write_text(DOCUMENT, encoding="utf-8")
            cli("add workstream: build", "build")
            cli("add workstream: check", "check")
            extended = inventory(repo)
            check(report, "original bytes preserved and one new skill",
                  set(extended) == set(baseline) | {NAME} and
                  all(extended[n] == h for n, h in baseline.items()), len(extended))
            again = cli("build idempotence", "build")
            check(report, "build is idempotent",
                  "Skill packages are current" in again and inventory(repo) == extended,
                  again.strip())

            destinations = [temp / client / "skills" for client in ("claude", "codex", "agents")]
            for dest in destinations:
                dest.mkdir()
                foreign = dest / "foreign-user-skill"
                foreign.write_text("UNCHANGED\n", encoding="utf-8")
                cli(f"dry-run {dest.parent.name}", "install", "--dry-run", "--destination", str(dest))
                check(report, f"dry-run does not write {dest.parent.name}",
                      list(dest.iterdir()) == [foreign], str(dest))
                cli(f"install {dest.parent.name}", "install", "--destination", str(dest))
                links = [p for p in dest.iterdir() if p.name in extended]
                check(report, f"all generated links present {dest.parent.name}",
                      len(links) == len(extended) and all(p.is_symlink() for p in links),
                      len(links))
                loaded = (dest / NAME / "SKILL.md").read_text(encoding="utf-8")
                m = re.search(r"\[authoring guide\]\(([^)]+)\)", loaded)
                guide_path = (dest / NAME / m[1].split("#")[0]) if m else None
                check(report, f"skill and linked guide readable {dest.parent.name}",
                      ("name: " + NAME in loaded and "## Procedure" in loaded and
                       guide_path is not None and guide_path.is_file()),
                      m[1] if m else "no link")
                cli(f"repeat install {dest.parent.name}", "install", "--destination", str(dest))
                check(report, f"foreign entry unchanged {dest.parent.name}",
                      foreign.read_text(encoding="utf-8") == "UNCHANGED\n", str(foreign))

            source.write_text(DOCUMENT.replace("skill: true\n", ""), encoding="utf-8")
            cli("remove opt-in: build", "build")
            cli("remove opt-in: check", "check")
            check(report, "retire only new package, keep source",
                  source.is_file() and inventory(repo) == baseline, len(inventory(repo)))
            for dest in destinations:
                cli(f"retire owned link {dest.parent.name}", "install", "--destination", str(dest))
                links = {p.name for p in dest.iterdir() if p.is_symlink()}
                check(report, f"stale retirement safe {dest.parent.name}",
                      links == set(baseline) and
                      not (dest / NAME).is_symlink() and
                      (dest / "foreign-user-skill").read_text(encoding="utf-8") == "UNCHANGED\n",
                      len(links))
            stable = cli("final repeat build", "build")
            cli("final check", "check")
            check(report, "final idempotence",
                  "Skill packages are current" in stable and inventory(repo) == baseline,
                  stable.strip())
        after = subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=no"],
                                        cwd=SOURCE, text=True)
        check(report, "source checkout unchanged", before == after, "tracked status equal")
        report["status"] = "PASS"
    except (AssertionError, RuntimeError, OSError, subprocess.TimeoutExpired) as e:
        report["status"] = "FAIL"
        report["error"] = type(e).__name__ + ": " + str(e)
    finally:
        write_report(output, report)
        print("MS10_REHEARSAL_" + report["status"] + " exact_sha=" + sha, flush=True)
        for x in report["assertions"]:
            print(("PASS " if x["pass"] else "FAIL ") + x["name"], flush=True)
        if report["error"]:
            print(report["error"], file=sys.stderr, flush=True)
        print("MS10_EVIDENCE_DIR=" + str(output), flush=True)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source-ref", required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    args = p.parse_args()
    raise SystemExit(exercise(args.source_ref, args.output_dir))
