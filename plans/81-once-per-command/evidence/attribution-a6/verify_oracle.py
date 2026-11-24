#!/usr/bin/env python3
"""Verify timed A-6 processes against an independently reviewed route oracle."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import sys

import analyze


def load_oracle(path: Path) -> tuple[dict, str]:
    raw = path.read_bytes()
    # Duplicate keys make an oracle ambiguous, including nested route keys.
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate oracle key: {key!r}")
            result[key] = value
        return result
    oracle = json.loads(raw, object_pairs_hook=unique)
    if not isinstance(oracle, dict) or set(oracle) != {"schema", "version", "derivation", "independent_validation", "routes"}:
        raise ValueError("oracle must contain exactly schema, version, derivation, independent_validation and routes")
    if oracle["schema"] != "attribution-a6-route-oracle-v1":
        raise ValueError("unsupported oracle schema")
    for key in ("version", "derivation", "independent_validation"):
        if not isinstance(oracle[key], str) or not oracle[key].strip():
            raise ValueError(f"oracle {key} must be a nonempty string")
    routes = oracle["routes"]
    if not isinstance(routes, dict) or not routes or any(route not in {"W", "I", "E"} for route in routes):
        raise ValueError("oracle routes must be a nonempty object keyed by W, I or E")
    for route, entries in routes.items():
        if not isinstance(entries, list) or not entries:
            raise ValueError(f"route {route} must have a nonempty list of occurrence expectations")
        seen = set()
        for entry in entries:
            if not isinstance(entry, dict) or set(entry) != {"stage", "parent", "count"}:
                raise ValueError(f"route {route}: each expectation needs exactly stage, parent and count")
            stage, parent, count = entry["stage"], entry["parent"], entry["count"]
            if not isinstance(stage, str) or not stage.strip() or stage == analyze.REMAINDER_NAME:
                raise ValueError(f"route {route}: invalid named stage {stage!r}")
            if parent is not None and (not isinstance(parent, str) or not parent.strip()):
                raise ValueError(f"route {route}: parent must be null or a nonempty stage name")
            if not isinstance(count, int) or isinstance(count, bool) or count < 0:
                raise ValueError(f"route {route}: count must be a nonnegative integer")
            if (stage, parent) in seen:
                raise ValueError(f"route {route}: duplicate stage and parent expectation")
            seen.add((stage, parent))
        if not any(entry["count"] for entry in entries):
            raise ValueError(f"route {route}: at least one named occurrence is required")
    return oracle, hashlib.sha256(raw).hexdigest()


def verify_sample(sample: dict, oracle: dict) -> dict:
    result = {"sample": sample.get("sample"), "route": sample.get("route"),
              "mode": sample.get("mode"), "warmup": sample.get("warmup"),
              "errors": list(sample.get("errors", [])), "coverage": None,
              "occurrence_mismatches": []}
    errors = result["errors"]
    if sample.get("mode") == "plain":
        result["coverage_status"] = "invalid" if errors else "not_evaluated_plain"
        return result
    if sample.get("mode") != "timings":
        errors.append("unknown sample mode")
        result["coverage_status"] = "invalid"
        return result
    route = sample.get("route")
    if route not in oracle["routes"]:
        errors.append(f"missing oracle for route {route!r}")
    else:
        expected = {(entry["stage"], entry["parent"]): entry["count"] for entry in oracle["routes"][route]}
        actual = Counter()
        for row in sample.get("occurrences", []):
            stage, parent = row.get("stage"), row.get("parent")
            if not isinstance(stage, str) or (parent is not None and not isinstance(parent, str)):
                errors.append("invalid occurrence stage or parent name")
                continue
            actual[(stage, parent)] += 1
        for stage, parent in sorted(set(expected) | set(actual), key=lambda pair: (pair[0], pair[1] or "")):
            want, got = expected.get((stage, parent), 0), actual.get((stage, parent), 0)
            if want != got:
                result["occurrence_mismatches"].append({"stage": stage, "parent": parent, "expected": want, "actual": got})
        if result["occurrence_mismatches"]:
            errors.append("named occurrence counts or parents differ from oracle")
    if sample.get("stage_counts", {}).get(analyze.REMAINDER_NAME, 0) != 1:
        errors.append("expected exactly one remainder row")
    invalid_evidence = bool(errors)
    wall, named = sample.get("W_seconds"), sample.get("S_seconds")
    if not analyze._number(wall) or wall <= 0 or not analyze._number(named):
        errors.append("cannot evaluate coverage without positive W and valid S")
        result["coverage_status"] = "invalid"
    else:
        fraction = (wall - named) / wall
        result["coverage"] = {"W_seconds": wall, "S_seconds": named, "R_seconds": sample.get("R_seconds"),
                              "C_seconds": sample.get("C_seconds"),
                              "W_minus_C_seconds": sample.get("W_minus_C_seconds"),
                              "residual_fraction": fraction, "limit": 0.10,
                              "within_limit": 0 <= fraction <= 0.10}
        result["coverage_status"] = "pass" if result["coverage"]["within_limit"] else "fail"
        if not result["coverage"]["within_limit"]:
            errors.append("per-process residual is outside [0, 0.10]")
    if invalid_evidence:
        result["coverage_status"] = "invalid"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--oracle", required=True, type=Path)
    parser.add_argument("--tolerance-seconds", type=float, default=0.001)
    parser.add_argument("runner_directories", nargs="+", type=Path)
    args = parser.parse_args()
    if not math.isfinite(args.tolerance_seconds) or args.tolerance_seconds < 0:
        parser.error("--tolerance-seconds must be finite and non-negative")
    try:
        oracle, digest = load_oracle(args.oracle)
    except (OSError, ValueError, UnicodeError) as exc:
        parser.error(f"invalid oracle: {exc}")
    runs = []
    for path in args.runner_directories:
        analyzed = analyze.analyze(path.resolve(), args.tolerance_seconds)
        samples = [verify_sample(sample, oracle) for sample in analyzed["samples"]]
        errors = list(analyzed["errors"])
        if not any(sample["mode"] == "timings" for sample in samples):
            errors.append("no timed processes to evaluate")
        runs.append({"directory": str(path.resolve()), "errors": errors, "processes": samples})
    report = {"schema": "attribution-a6-oracle-verification-v1", "oracle_version": oracle["version"],
              "oracle_sha256": digest, "tolerance_seconds": args.tolerance_seconds, "runs": runs}
    json.dump(report, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return int(any(run["errors"] or any(sample["errors"] for sample in run["processes"]) for run in runs))


if __name__ == "__main__":
    raise SystemExit(main())
