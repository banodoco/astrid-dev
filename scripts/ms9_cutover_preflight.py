#!/usr/bin/env python3
"""Read-only MS7/MS9 transition preflight; never authorizes D5 or deletes files."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
import os
from pathlib import Path
import subprocess
import tempfile

from agent_reference_inventory import inventory, mapped_target, tracked_paths

REPOSITORY = Path(__file__).resolve().parents[1]
ROLES = {
    "lead": "leader", "manage": "manager",
    "orchestrate": "orchestrator", "worker": "worker",
}
ROLE_WORKSTREAMS = {
    "lead": ("multi-manager-release",),
    "manage": ("chatgpt-packet", "whole-project"),
    "orchestrate": ("codex-cloud-sessions", "codex-in-claude-cloud", "multi-manager-dispatch"),
}
SHARED = ("bugfix", "gap", "gpu-validate", "green", "improve",
          "iterate", "merge", "plan", "release")


def primary_sources() -> dict[str, str]:
    paths = {"skills/astrid-dev/SKILL.md": "agent/start.md"}
    for old, new in ROLES.items():
        paths[f"skills/roles/astrid-dev-{old}/SKILL.md"] = f"agent/roles/{new}.md"
    for role, stems in ROLE_WORKSTREAMS.items():
        for stem in stems:
            paths[f"skills/roles/astrid-dev-{role}/workstreams/{stem}.md"] = (
                f"agent/roles/{ROLES[role]}/{stem}.md")
    for stem in SHARED:
        paths[f"skills/shared/workstreams/astrid-dev-{stem}/SKILL.md"] = (
            f"agent/shared/workstreams/{stem}.md")
    return paths


def proposed_route(row: dict) -> tuple[str, str]:
    scope = row["scope"]
    path = str(row["file"])
    reference = str(row["reference"])
    if scope == "historical-evidence":
        return "preserve-provenance", "historical custodian"
    if scope == "current-authority":
        return "retain-until-D5-and-MS9", "Plan 73 owner"
    if scope == "pinned-test-or-fixture":
        return "preserve-and-replace-oracle-only-after-D5", "validator owner"
    if scope == "release-lead-review":
        return "D5-release-lead-decision", "active Release Lead"
    if scope == "plan-owner-review":
        return "active-vs-historical-plan-adjudication", "plan owner"
    if path.startswith(("scripts/workstreams.py", "scripts/views.py")) and reference.startswith("skills/"):
        return "replace-legacy-generated-index-with-tests", "MS8/MS9 check owner"
    if reference == "scripts/astrid_dev.py sync":
        # Old CLI view-generation must not be conflated with old sync.sh installation.
        return "keep-general-generated-view-sync", "view/check owner"
    if reference == "sync.sh" or path == "sync.sh":
        return "retire-legacy-installer-only-after-D5", "MS9 owner"
    if row["proposed_target"]:
        return "candidate-source-link-after-D5", "active document owner"
    return "manual-consumer-triage-before-D5", "active document owner"


def assess(root: Path) -> dict:
    root = Path(root).resolve()
    files = tracked_paths(root)
    rows = inventory(root, paths=files)
    checked = []
    for old, new in sorted(primary_sources().items()):
        left, right = root / old, root / new
        checked.append({
            "old": old, "new": new,
            "old_exists": left.is_file() and not left.is_symlink(),
            "new_exists": right.is_file() and not right.is_symlink(),
            "map_matches_inventory": mapped_target(old, "path") == new,
        })
    aliases = sorted(path for path in files
                     if path.startswith(("skills/capabilities/", "skills/roles/astrid-dev-plan"))
                     and (root / path).is_symlink())
    categories = Counter()
    grouped: dict[str, list[dict]] = defaultdict(list)
    for original in rows:
        item = dict(original)
        route, owner = proposed_route(item)
        item["route"] = route
        item["decision_owner"] = owner
        categories[route] += 1
        grouped[str(item["file"])].append(item)
    active = sorted({str(row["file"]) for row in rows if row["scope"] == "active-consumer"})
    return {
        "checkout_sha": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(),
        "readiness": "HOLD_PENDING_D5_AND_INDEPENDENT_ACCEPTANCE",
        "authority": "skills/ remains authoritative; this result cannot grant cutover",
        "primary_source_map": checked,
        "missing_or_mismatched_primary": [x for x in checked
                                         if not (x["old_exists"] and x["new_exists"]
                                                 and x["map_matches_inventory"])],
        "tracked_legacy_skill_manifests": sorted(
            p for p in files if p.startswith("skills/") and p.endswith("/SKILL.md")),
        "tracked_legacy_aliases": aliases,
        "active_consumer_files": active,
        "scope_counts": dict(sorted(Counter(str(row["scope"]) for row in rows).items())),
        "route_counts": dict(sorted(categories.items())),
        "references": [entry for path in sorted(grouped) for entry in grouped[path]],
        "reference_count": len(rows),
    }


def markdown(data: dict) -> str:
    b = chr(96)
    lines = [
        "# Plan 73 — MS7/MS9 pre-cutover decision and source inventory", "",
        f"**Exact head:** {b}{data['checkout_sha']}{b}",
        f"**Disposition:** {data['readiness']}",
        "",
        "This document is a source/consumer decision packet, never a go signal.",
        "Historical evidence stays immutable. Do not rewrite active release instructions",
        "without the Lead's explicit D5 handoff. Keep general generated-view sync:",
        "it is not the legacy sync.sh skill installer.", "",
        f"**Primary mappings:** {len(data['primary_source_map'])}; "
        f"missing/mismatched: {len(data['missing_or_mismatched_primary'])}.",
        f"**Tracked old SKILL.md:** {len(data['tracked_legacy_skill_manifests'])}. "
        f"**Aliases:** {len(data['tracked_legacy_aliases'])}.",
        f"**References:** {data['reference_count']}; "
        f"active-consumer files: {len(data['active_consumer_files'])}.", "",
        "## Routing and ownership", "",
        "| Decision route | Matches |", "| --- | ---: |",
    ]
    lines += [f"| {route} | {count} |" for route, count in data["route_counts"].items()]
    lines += ["", "## Primary source crosswalk", "",
              "| Authored legacy source | Staged new source | Legacy | Staged | Mapped |",
              "| --- | --- | --- | --- | --- |"]
    for row in data["primary_source_map"]:
        lines.append(f"| {b}{row['old']}{b} | {b}{row['new']}{b} | "
                     f"{'yes' if row['old_exists'] else 'NO'} | "
                     f"{'yes' if row['new_exists'] else 'NO'} | "
                     f"{'yes' if row['map_matches_inventory'] else 'NO'} |")
    lines += ["", "## Active-consumer decision queue", "",
              "| File:line | Old reference | Candidate | Decision | Owner |",
              "| --- | --- | --- | --- | --- |"]
    for item in data["references"]:
        if item["scope"] != "active-consumer":
            continue
        lines.append(f"| {b}{item['file']}:{item['line']}{b} | "
                     f"{b}{item['reference'].replace(chr(96), '')}{b} | "
                     f"{b}{item['proposed_target'] or 'manual'}{b} | "
                     f"{item['route']} | {item['decision_owner']} |")
    lines += [
        "", "## Remaining owner decisions", "",
        "- D5: identify exact release owners, handoff date and active consumer migration GO.",
        "- MS7: qualify each live reference, retain historical proof and resolve manual commands.",
        "- MS8/MS9: remove legacy role-index machinery only with replacement oracles;",
        "- MS9: retire old authored packages and aliases only after active consumers switch.",
        "- MS10: independent fresh-agent and real client discovery remain NO-RESULT.",
        "- MS11: full integrated post-cutover proof across supported clients is not complete.",
        "- Preserve original RS1 BLOCK and bounded finding dispositions; formal review R remains.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source-ref", required=True, help="Full immutable PR-head SHA")
    p.add_argument("--output-dir", type=Path, required=True)
    args = p.parse_args()
    if not __import__("re").fullmatch("[a-f0-9]{40}", args.source_ref):
        p.error("--source-ref must be a full SHA")
    if args.output_dir.resolve().is_relative_to(REPOSITORY.resolve()):
        p.error("output-dir must be outside the checkout")
    with tempfile.TemporaryDirectory(prefix="p73-ms9-preflight-") as tmp:
        root = Path(tmp) / "repo"
        env = os.environ.copy()
        env.update({"GIT_TERMINAL_PROMPT": "0", "GIT_CONFIG_GLOBAL": os.devnull})
        commands = [
            ["git", "init", "-q", str(root)],
            ["git", "-C", str(root), "fetch", "-q", "--no-tags", str(REPOSITORY), args.source_ref],
            ["git", "-C", str(root), "checkout", "-q", "--detach", "FETCH_HEAD"],
        ]
        for cmd in commands:
            subprocess.run(cmd, check=True, env=env, capture_output=True, text=True, timeout=90)
        result = assess(root)
        if result["checkout_sha"] != args.source_ref:
            raise ValueError("disposable checkout did not match exact source-ref")
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / "ms9-readiness.json").write_text(
            json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (args.output_dir / "ms9-readiness.md").write_text(markdown(result), encoding="utf-8")
        print("MS9_PREFLIGHT_RECORDED " + args.source_ref
              + " primary=" + str(len(result["primary_source_map"]))
              + " references=" + str(result["reference_count"])
              + " active_files=" + str(len(result["active_consumer_files"]))
              + " disposition=" + result["readiness"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
