#!/usr/bin/env python3
"""MS7/MS9 disposable compatibility and rollback rehearsal (never a D5 cutover).

Run on exact-source detached checkout. Nothing is installed into real HOME.
An explicit snapshot-based restoration is tested; sync.sh is NOT a safe
automatic rollback of generated skills and no such capability is claimed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile

SOURCE = Path(__file__).resolve().parents[1]
LIMITS = [
    "All switches and restorations occur only in a disposable exact-SHA checkout and skill root.",
    "Legacy sync.sh is not an automatic rollback after generated installation.",
    "Restoration preflight is an exercise helper, not a crash-safe atomic multi-entry transaction.",
    "No D5, MS9 deletion, real user home, live Claude/Codex client, Windows or macOS acceptance.",
    "No hostile concurrent writers, power-loss durability, orphan cleanup or broad snapshot guarantee.",
    "The historical RS1 BLOCK, independent final R and final owner GO remain unchanged.",
]


def snapshot_links(directory: Path) -> dict[str, str]:
    return {p.name: os.readlink(p) for p in sorted(directory.iterdir()) if p.is_symlink()}


def hashes_via_links(directory: Path, names: dict[str, str]) -> dict[str, str]:
    out = {}
    for name in sorted(names):
        file = directory / name / "SKILL.md"
        if file.is_file():
            out[name] = hashlib.sha256(file.read_bytes()).hexdigest()
    return out


def restore_legacy_links(directory: Path, checkout: Path, legacy: dict[str, str],
                         generated: dict[str, str]) -> list[str]:
    """Only for a disposable test root. Fail closed before touching any link.

    All generated names must still have exact raw targets observed after switch;
    restored source paths must be inside the current checkout's existing skills/.
    Check name collisions before touching any entry. This is not atomic against
    noncooperating writers or failures during mutation.
    """
    directory, checkout = directory.resolve(), checkout.resolve()
    old_root, new_root = checkout / "skills", checkout / ".generated/skills"
    for name, raw in legacy.items():
        if "/" in name or name in (".", ".."):
            raise ValueError(f"unsafe legacy name {name!r}")
        target = (directory / raw).resolve()
        if not target.is_relative_to(old_root) or not target.is_dir():
            raise ValueError(f"legacy target outside authored checkout: {name}")
    for name, raw in generated.items():
        if "/" in name or name in (".", ".."):
            raise ValueError(f"unsafe generated name {name!r}")
        current = directory / name
        if not current.is_symlink() or os.readlink(current) != raw:
            raise ValueError(f"installed link changed, refusing restoration: {name}")
        target = (directory / raw).resolve()
        if not target.is_relative_to(new_root) or not target.is_dir():
            raise ValueError(f"generated target outside owned checkout: {name}")
    for name in legacy:
        if name not in generated:
            dest = directory / name
            if dest.exists() or dest.is_symlink():
                raise ValueError(f"restoration collision, refusing all changes: {name}")
    result = []
    # All names were checked. Safe only in this disposable, single-writer root.
    for name in sorted(generated):
        link = directory / name
        if not link.is_symlink() or os.readlink(link) != generated[name]:
            raise ValueError(f"unexpected mutation during restoration: {name}")
        link.unlink()
        result.append(f"removed generated {name}")
    for name, raw in sorted(legacy.items()):
        link = directory / name
        if link.exists() or link.is_symlink():
            raise ValueError(f"unexpected restoration collision: {name}")
        link.symlink_to(raw, target_is_directory=True)
        result.append(f"restored legacy {name}")
    return result


def command(report: dict, name: str, argv: list[str], cwd: Path, env: dict,
            *, expect_failure: str | None = None) -> str:
    p = subprocess.run(argv, cwd=cwd, env=env, capture_output=True,
                       text=True, errors="replace", check=False, timeout=180)
    report["commands"].append({
        "name": name, "argv": argv, "cwd": str(cwd), "exit": p.returncode,
        "stdout": p.stdout, "stderr": p.stderr, "expected_failure": expect_failure,
    })
    combined = p.stdout + "\n" + p.stderr
    if expect_failure is None and p.returncode:
        raise AssertionError(f"{name}: exit {p.returncode}: {combined[-1200:]}")
    if expect_failure is not None and (p.returncode == 0 or expect_failure not in combined):
        raise AssertionError(f"{name}: expected refusal {expect_failure!r}; exit={p.returncode}; {combined[-1200:]}")
    return combined


def check(report: dict, name: str, passed: bool, detail):
    report["assertions"].append({"name": name, "pass": bool(passed), "detail": detail})
    if not passed:
        raise AssertionError(f"{name}: {detail}")


def render(output: Path, report: dict):
    output.mkdir(parents=True, exist_ok=True)
    (output / "ms9-compat-rollback.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    fence = chr(96) * 3
    lines = [
        "# Plan 73 MS7/MS9 disposable compatibility and rollback rehearsal", "",
        f"**Status:** {report['status']}",
        f"**Exact SHA:** {report['source_sha']}",
        f"**Environment:** {report['environment']}", "",
        "**Scope:** installation switch and restoration in one temporary skill directory;",
        "historical authored sources and real client homes remain untouched.", "",
        "## Assertions", "", "| Assertion | Result | Detail |", "| --- | --- | --- |",
    ]
    for a in report["assertions"]:
        lines.append(f"| {a['name']} | {'PASS' if a['pass'] else 'FAIL'} | "
                     f"{str(a['detail']).replace('|', ';').replace(chr(10), ' ')} |")
    lines += ["", "## Raw CLI command receipts", ""]
    for v in report["commands"]:
        lines += ["### " + v["name"], "", "argv: " + json.dumps(v["argv"]),
                  "cwd: " + v["cwd"], "exit: " + str(v["exit"]),
                  "expected failure: " + str(v["expected_failure"]), "",
                  fence + "text", "stdout:", v["stdout"] or "(empty)",
                  "stderr:", v["stderr"] or "(empty)", fence, ""]
    lines += ["## Limitations", ""]
    lines.extend("- " + s for s in LIMITS)
    if report["error"]:
        lines += ["", "## Error", "", report["error"]]
    (output / "ms9-compat-rollback.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def exercise(sha: str, output: Path) -> int:
    report = {"source_sha": sha, "status": "RUNNING", "environment": platform.platform(),
              "assertions": [], "commands": [], "limits": LIMITS, "error": None}
    try:
        check(report, "exact 40-character source SHA",
              bool(re.fullmatch("[a-f0-9]{40}", sha)), sha)
        check(report, "evidence path outside original checkout",
              not output.resolve().is_relative_to(SOURCE.resolve()), str(output))
        before = subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=no"],
                                         cwd=SOURCE, text=True)
        with tempfile.TemporaryDirectory(prefix="p73-ms9-rollback-") as tmp:
            scratch = Path(tmp)
            repo, dest, home = scratch / "repo", scratch / "clients" / "skills", scratch / "home"
            dest.mkdir(parents=True)
            home.mkdir()
            env = os.environ.copy()
            env.update({"HOME": str(home), "PYTHONDONTWRITEBYTECODE": "1",
                        "GIT_TERMINAL_PROMPT": "0", "GIT_CONFIG_GLOBAL": os.devnull})
            def git(name, *args):
                return command(report, name, ["git", *args], scratch, env)
            def legacy(name, *args, expect_failure=None):
                return command(report, name, ["bash", "sync.sh", *args], repo, env,
                               expect_failure=expect_failure)
            def generated(name, *args):
                return command(report, name, ["python3", "scripts/astrid_dev.py",
                               "skills", *args], repo, env)

            git("initialize isolated checkout", "init", "-q", str(repo))
            git("fetch full source SHA locally", "-C", str(repo), "fetch",
                "-q", "--no-tags", str(SOURCE), sha)
            git("detach source SHA", "-C", str(repo), "checkout", "-q", "--detach", "FETCH_HEAD")
            observed = git("verify exact source", "-C", str(repo), "rev-parse", "HEAD").strip()
            check(report, "source identity matches", observed == sha, observed)

            foreign = dest / "foreign-user-skill"
            foreign.write_text("FOREIGN-PRESERVE\n", encoding="utf-8")
            legacy("install historical packages", "--destination", str(dest))
            legacy_links = snapshot_links(dest)
            original_hashes = hashes_via_links(dest, legacy_links)
            check(report, "historical layout installed",
                  len(legacy_links) == 15 and "astrid-dev" in legacy_links
                  and "shared" in legacy_links and "astrid-dev-iterate" in legacy_links,
                  {"count": len(legacy_links), "names": sorted(legacy_links)})
            check(report, "original skill instructions load through symlinks",
                  "astrid-dev" in original_hashes and
                  "astrid-dev-iterate" in original_hashes and
                  "shared" not in original_hashes,
                  {"hash_count": len(original_hashes)})

            generated("build staged generated packages", "build")
            generated("check staged generated packages", "check")
            before_dry = snapshot_links(dest)
            generated("dry run transition to new packages", "install",
                      "--dry-run", "--destination", str(dest))
            check(report, "new installer dry run does not change old links",
                  snapshot_links(dest) == before_dry, "legacy links unchanged")
            generated("transition to generated packages", "install",
                      "--destination", str(dest))
            generated_links = snapshot_links(dest)
            check(report, "generated destination contains expected packages",
                  len(generated_links) == 14 and "astrid-dev-start" in generated_links
                  and "astrid-dev-manager" in generated_links
                  and "astrid-dev" not in generated_links and "shared" not in generated_links,
                  {"count": len(generated_links), "names": sorted(generated_links)})
            check(report, "generated instructions readable",
                  all((dest / name / "SKILL.md").is_file() for name in generated_links),
                  "all 14 links contain SKILL.md")
            generated("reinstall generated packages idempotently", "install",
                      "--destination", str(dest))
            check(report, "generated link target set stable after repeat",
                  snapshot_links(dest) == generated_links, "14 symlinks unchanged")
            check(report, "foreign file preserved during forward transition",
                  foreign.read_text(encoding="utf-8") == "FOREIGN-PRESERVE\n", str(foreign))

            # Do NOT run legacy sync.sh for real after switching: its dry-run
            # is an expected conflict, not a safe rollback mechanism.
            old_dry = snapshot_links(dest)
            legacy("probe unsupported automatic legacy rollback (dry run only)",
                   "--dry-run", "--destination", str(dest),
                   expect_failure="foreign symlink")
            check(report, "legacy installer correctly not treated as automatic rollback",
                  snapshot_links(dest) == old_dry,
                  "dry run returned foreign symlink refusal and changed no links")

            # Simulate a changed unknown entry and prove rollback refuses
            # before touching any owned link. Remove the test-only conflict.
            collision = dest / "astrid-dev"
            collision.write_text("UNOWNED-COLLISION\n", encoding="utf-8")
            before_conflict = snapshot_links(dest)
            try:
                try:
                    restore_legacy_links(dest, repo, legacy_links, generated_links)
                except ValueError as exc:
                    verify_collision = "restoration collision" in str(exc)
                else:
                    verify_collision = False
                check(report, "manual rollback preflight refuses foreign collision",
                      verify_collision and snapshot_links(dest) == before_conflict
                      and collision.read_text(encoding="utf-8") == "UNOWNED-COLLISION\n",
                      "no installed symlink modified when collision detected")
            finally:
                collision.unlink(missing_ok=True)

            restore_actions = restore_legacy_links(dest, repo, legacy_links, generated_links)
            check(report, "all original legacy targets restored exactly",
                  snapshot_links(dest) == legacy_links,
                  {"restored": len(legacy_links), "actions": len(restore_actions)})
            check(report, "original historical SKILL.md contents match baseline",
                  hashes_via_links(dest, legacy_links) == original_hashes,
                  "all historical instruction hashes match original")
            check(report, "foreign entry unchanged through rollback",
                  foreign.read_text(encoding="utf-8") == "FOREIGN-PRESERVE\n",
                  "foreign file content identical")
            legacy("original installer works again after manual restore",
                   "--dry-run", "--destination", str(dest))
            check(report, "restoration does not remove canonical old sources",
                  all((repo / "skills" / path).exists() for path in (
                      "astrid-dev/SKILL.md",
                      "roles/astrid-dev-manage/SKILL.md",
                      "shared/workstreams/astrid-dev-iterate/SKILL.md",
                  )), "old skill tree remains authoritative")
        after = subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=no"],
                                        cwd=SOURCE, text=True)
        check(report, "original checkout tracked files unchanged",
              before == after, "tracked status identical before and after")
        report["status"] = "PASS"
    except (OSError, ValueError, AssertionError, subprocess.TimeoutExpired) as exc:
        report["status"] = "FAIL"
        report["error"] = f"{type(exc).__name__}: {exc}"
    finally:
        render(output, report)
        print(f"MS9_COMPAT_ROLLBACK_{report['status']} exact_source={sha}", flush=True)
        for assertion in report["assertions"]:
            print(("PASS " if assertion["pass"] else "FAIL ") + assertion["name"], flush=True)
        if report["error"]:
            print(report["error"], file=sys.stderr, flush=True)
        print("MS9_COMPAT_EVIDENCE=" + str(output), flush=True)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source-ref", required=True, help="Exact immutable PR-head SHA")
    p.add_argument("--output-dir", type=Path, required=True)
    args = p.parse_args()
    raise SystemExit(exercise(args.source_ref, args.output_dir))
