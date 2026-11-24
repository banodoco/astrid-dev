#!/usr/bin/env python3
"""Summarize raw A-6 runner samples without hiding invalid evidence.

Pass one or more runner output directories (for example, the before/after
comparison subdirectories). The JSON report is written to stdout. This tool
does not run commands or impose a coverage percentage gate.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys
from typing import Any

REMAINDER_NAME = "other command work"


def _number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def _receipt_errors(trial: dict[str, Any], seen_tasks: set[str], seen_prompts: set[str]) -> list[str]:
    errors: list[str] = []
    if trial.get("returncode") != 0:
        errors.append(f"command returncode is {trial.get('returncode')!r}, expected 0")
    task_id = trial.get("task_id")
    if not isinstance(task_id, str) or not task_id.strip():
        errors.append("missing Runtime task_id receipt")
    elif task_id in seen_tasks:
        errors.append(f"duplicate Runtime task_id receipt: {task_id}")
    else:
        seen_tasks.add(task_id)
    if trial.get("task_state") != "succeeded":
        errors.append(f"Runtime task_state is {trial.get('task_state')!r}, expected 'succeeded'")
    prompt_id = trial.get("target_prompt_id")
    if not isinstance(prompt_id, str) or not prompt_id.strip():
        errors.append("missing target_prompt_id receipt")
    elif prompt_id in seen_prompts:
        errors.append(f"duplicate target_prompt_id receipt: {prompt_id}")
    else:
        seen_prompts.add(prompt_id)
    if not _number(trial.get("admission_ns")):
        errors.append("missing or invalid Runtime admission timestamp")
    if not _number(trial.get("target_ack_ns")):
        errors.append("missing or invalid target acknowledgement timestamp")
    if _number(trial.get("spawn_ns")) and _number(trial.get("admission_ns")):
        if trial["admission_ns"] < trial["spawn_ns"]:
            errors.append("Runtime admission timestamp precedes spawn")
    # Target work is asynchronous: its acknowledgement can legitimately arrive
    # after the CLI exits, so do not impose an ordering against exit_ns.
    return errors


def _analyze_sample(directory: Path, trial: Any, seen_tasks: set[str], seen_prompts: set[str], tolerance: float) -> dict[str, Any]:
    errors: list[str] = []
    if not isinstance(trial, dict):
        return {"directory": str(directory), "sample": None, "errors": ["trial manifest entry is not an object"]}

    sample_id = f"{trial.get('route', '?')}-{trial.get('mode', '?')}-" + (
        "warmup" if trial.get("warmup") else str(trial.get("trial", "?")))
    sample: dict[str, Any] = {
        "directory": str(directory), "sample": sample_id,
        "route": trial.get("route"), "mode": trial.get("mode"),
        "warmup": trial.get("warmup"), "trial": trial.get("trial"),
        "errors": errors,
    }
    errors.extend(_receipt_errors(trial, seen_tasks, seen_prompts))

    wall = trial.get("wall_seconds")
    if not _number(wall) or wall < 0:
        errors.append(f"invalid outer wall_seconds: {wall!r}")
        wall = None
    sample["W_seconds"] = wall

    stdout_name = trial.get("stdout")
    if not isinstance(stdout_name, str) or not stdout_name:
        errors.append("missing stdout path in manifest")
        return sample
    stdout_path = (directory / stdout_name).resolve()
    try:
        stdout_path.relative_to(directory.resolve())
    except ValueError:
        errors.append(f"stdout path escapes runner directory: {stdout_name!r}")
        return sample
    try:
        payload = _load_json(stdout_path)
    except (OSError, ValueError) as exc:
        errors.append(f"cannot read stdout JSON {stdout_name!r}: {exc}")
        return sample
    if not isinstance(payload, dict):
        errors.append("stdout JSON is not an object")
        return sample

    rows = payload.get("timings")
    if rows is None and trial.get("mode") == "plain":
        sample["C_seconds"] = None
        sample["S_seconds"] = None
        sample["R_seconds"] = None
        sample["W_minus_C_seconds"] = None
        sample["(W_minus_S)_over_W"] = None
        sample["S_plus_R_minus_C_seconds"] = None
        sample["discrepancy_within_tolerance"] = None
        sample["tolerance_seconds"] = tolerance
        sample["stage_counts"] = {}
        sample["occurrences"] = []
        return sample
    if not isinstance(rows, list):
        errors.append("stdout JSON has no timings array (use a --timings runner sample)")
        return sample
    collector_span = payload.get("collector_span_seconds")
    if not _number(collector_span) or collector_span < 0:
        errors.append(f"invalid or missing collector_span_seconds: {collector_span!r}")
        collector_span = None
    sample["C_seconds"] = collector_span

    occurrence_rows: list[dict[str, Any]] = []
    remainders: list[dict[str, Any]] = []
    ids: dict[int, dict[str, Any]] = {}
    stage_counts: dict[str, int] = {}
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"timing row {index} is not an object")
            continue
        stage_name = row.get("stage")
        if not isinstance(stage_name, str) or not stage_name:
            errors.append(f"timing row {index} has missing/invalid stage name")
            stage_name = "<invalid stage>"
        stage_counts[stage_name] = stage_counts.get(stage_name, 0) + 1
        seconds = row.get("seconds")
        if not _number(seconds) or seconds < 0:
            errors.append(f"timing row {index} ({stage_name}) has invalid exclusive seconds: {seconds!r}")
        total_seconds = row.get("total_seconds")
        if total_seconds is not None:
            if not _number(total_seconds) or total_seconds < 0:
                errors.append(f"timing row {index} ({stage_name}) has invalid inclusive total_seconds: {total_seconds!r}")
            elif _number(seconds) and total_seconds + tolerance < seconds:
                errors.append(f"timing row {index} ({stage_name}) inclusive total_seconds {total_seconds!r} is below exclusive seconds {seconds!r}")
        if stage_name == REMAINDER_NAME:
            remainders.append(row)
            continue
        occurrence_rows.append(row)
        occurrence_id = row.get("occurrence_id")
        if not isinstance(occurrence_id, int) or isinstance(occurrence_id, bool) or occurrence_id <= 0:
            errors.append(f"timing row {index} ({stage_name}) has malformed occurrence_id: {occurrence_id!r}")
        elif occurrence_id in ids:
            errors.append(f"duplicate occurrence_id {occurrence_id} on rows {ids[occurrence_id].get('_index')} and {index}")
        else:
            row_with_index = dict(row)
            row_with_index["_index"] = index
            ids[occurrence_id] = row_with_index

    if len(remainders) != 1:
        errors.append(f"expected exactly one '{REMAINDER_NAME}' row, found {len(remainders)}")
    remainder = remainders[0].get("seconds") if len(remainders) == 1 else None
    if not _number(remainder) or remainder < 0:
        errors.append(f"invalid remainder seconds: {remainder!r}")
        remainder = None
    sample["R_seconds"] = remainder
    sample["stage_counts"] = stage_counts

    ancestry: list[dict[str, Any]] = []
    for occurrence_id, row in ids.items():
        parent_id = row.get("parent_id")
        parent_name = row.get("parent")
        if parent_id is None:
            if parent_name is not None:
                errors.append(f"occurrence {occurrence_id} has parent name {parent_name!r} but null parent_id")
        elif not isinstance(parent_id, int) or isinstance(parent_id, bool) or parent_id <= 0:
            errors.append(f"occurrence {occurrence_id} has malformed parent_id: {parent_id!r}")
        elif parent_id not in ids:
            errors.append(f"occurrence {occurrence_id} references missing parent_id {parent_id}")
        elif ids[parent_id].get("stage") != parent_name:
            errors.append(f"occurrence {occurrence_id} parent name {parent_name!r} does not match parent_id {parent_id} stage {ids[parent_id].get('stage')!r}")
        ancestry.append({
            "occurrence_id": occurrence_id,
            "stage": row.get("stage"),
            "detail": row.get("detail"),
            "parent": parent_name,
            "parent_id": parent_id,
            "seconds": row.get("seconds"),
            "total_seconds": row.get("total_seconds"),
        })
    for occurrence_id in ids:
        visited: set[int] = set()
        current = occurrence_id
        while current in ids:
            if current in visited:
                errors.append(f"cycle in ancestry starting at occurrence_id {occurrence_id}")
                break
            visited.add(current)
            parent_id = ids[current].get("parent_id")
            if not isinstance(parent_id, int) or isinstance(parent_id, bool):
                break
            current = parent_id
    sample["occurrences"] = ancestry

    if all(_number(row.get("seconds")) and row["seconds"] >= 0 for row in occurrence_rows):
        named = sum(row["seconds"] for row in occurrence_rows)
        sample["S_seconds"] = named
    else:
        named = None
        sample["S_seconds"] = None
    sample["tolerance_seconds"] = tolerance
    if named is not None and remainder is not None and collector_span is not None:
        discrepancy = named + remainder - collector_span
        sample["S_plus_R_minus_C_seconds"] = discrepancy
        sample["discrepancy_within_tolerance"] = abs(discrepancy) <= tolerance
        if abs(discrepancy) > tolerance:
            errors.append(f"S+R differs from collector span C by {discrepancy:.9f}s (tolerance {tolerance:.9f}s)")
    else:
        sample["S_plus_R_minus_C_seconds"] = None
        sample["discrepancy_within_tolerance"] = None
    if wall is not None:
        sample["W_minus_C_seconds"] = wall - collector_span if collector_span is not None else None
        sample["(W_minus_S)_over_W"] = (wall - named) / wall if named is not None and wall > 0 else None
        if collector_span is not None and collector_span - wall > tolerance:
            errors.append(f"collector span C exceeds outer wall W by {collector_span - wall:.9f}s (tolerance {tolerance:.9f}s)")
        if named is not None and named - wall > tolerance:
            errors.append(f"negative outer residual W-S: named exclusive time exceeds wall by {named - wall:.9f}s (tolerance {tolerance:.9f}s)")
    else:
        sample["W_minus_C_seconds"] = None
        sample["(W_minus_S)_over_W"] = None
    return sample


def analyze(directory: Path, tolerance: float) -> dict[str, Any]:
    errors: list[str] = []
    result: dict[str, Any] = {"directory": str(directory), "samples": [], "errors": errors}
    manifest_path = directory / "manifest.json"
    try:
        manifest = _load_json(manifest_path)
    except (OSError, ValueError) as exc:
        errors.append(f"cannot read manifest.json: {exc}")
        return result
    if not isinstance(manifest, dict) or not isinstance(manifest.get("trials"), list):
        errors.append("manifest must be an object containing a trials array")
        return result
    seen_tasks: set[str] = set()
    seen_prompts: set[str] = set()
    for trial in manifest["trials"]:
        result["samples"].append(_analyze_sample(directory, trial, seen_tasks, seen_prompts, tolerance))
    if not result["samples"]:
        errors.append("manifest contains no trials")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runner_directories", nargs="+", type=Path,
                        help="one or more runner output directories, such as before/after subdirectories")
    parser.add_argument("--tolerance-seconds", type=float, default=0.001,
                        help="absolute tolerance for |S+R-C| in seconds (default: 0.001)")
    args = parser.parse_args()
    if not math.isfinite(args.tolerance_seconds) or args.tolerance_seconds < 0:
        parser.error("--tolerance-seconds must be finite and non-negative")
    report = {
        "schema": "attribution-a6-analysis-v1",
        "explicit_discrepancy_tolerance_seconds": args.tolerance_seconds,
        "coverage_threshold_applied": False,
        "runs": [analyze(path.resolve(), args.tolerance_seconds) for path in args.runner_directories],
    }
    json.dump(report, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0 if all(not run["errors"] and all(not sample["errors"] for sample in run["samples"])
                    for run in report["runs"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
