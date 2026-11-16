#!/usr/bin/env python3
"""Sort a candidate's test failures against one or more baselines (see env/README.md).

Input: pytest output run with -rA (PYTEST_ADDOPTS=-rA), one or more log files per side, comma-separated.
  python3 -I baseline-diff.py --baseline served-11=base.log --baseline main=main1.log,main2.log \
      --candidate cand.log [--out DIR]

Buckets for each test the candidate ran:
  regression   failed on the candidate; ran and passed on at least one baseline. Blocks.
  no-baseline  failed on the candidate; ran on no baseline. Fix it if the run added the test.
  preexisting  failed on the candidate and on every baseline it ran on. Goes to its own project.
  fixed        passed on the candidate; failed on a baseline and passed on none.
  missing      passed on a baseline; not run on the candidate (deleted, skipped or uncollected).
An XFAIL counts as passing, because the test met its expectation; a strict XPASS is reported FAILED by pytest.
Exit 0: no regressions. Exit 1: regressions. Exit 2: bad input.
"""
import argparse
import re
import sys
from pathlib import Path

_LINE = re.compile(r"^(PASSED|FAILED|ERROR|XFAIL|XPASS) (.+)$")
PASS, FAIL = "passed", "failed"


def _node_id(rest):
    """The node id at the start of a summary line's remainder; FAILED/ERROR lines append ' - message'."""
    head = rest.find("::")
    if head < 0:
        return rest.split(" - ", 1)[0].strip()
    bracket = rest.find("[", head)
    space = rest.find(" ", head)
    if bracket >= 0 and (space < 0 or bracket < space):
        depth = 0
        for i in range(bracket, len(rest)):
            if rest[i] == "[":
                depth += 1
            elif rest[i] == "]":
                depth -= 1
                if depth == 0:
                    return rest[: i + 1]
        return rest.strip()
    return rest if space < 0 else rest[:space]


def parse(paths):
    """Map node id to passed/failed across the given -rA logs; a failure anywhere wins."""
    out = {}
    for path in paths:
        for line in Path(path).read_text(errors="replace").splitlines():
            m = _LINE.match(line.strip())
            if not m:
                continue
            status, node = m.group(1), _node_id(m.group(2))
            result = FAIL if status in ("FAILED", "ERROR") else PASS
            if out.get(node) != FAIL:
                out[node] = result
    return out


def sort_results(baselines, candidate):
    """baselines: {label: {id: status}}; candidate: {id: status}. Returns {bucket: sorted ids}."""
    buckets = {k: [] for k in ("regression", "no-baseline", "preexisting", "fixed", "missing")}
    for node, status in candidate.items():
        seen = [b[node] for b in baselines.values() if node in b]
        if status == FAIL:
            if PASS in seen:
                buckets["regression"].append(node)
            elif seen:
                buckets["preexisting"].append(node)
            else:
                buckets["no-baseline"].append(node)
        elif FAIL in seen and PASS not in seen:
            buckets["fixed"].append(node)
    passed_somewhere = {n for b in baselines.values() for n, s in b.items() if s == PASS}
    buckets["missing"] = sorted(passed_somewhere - candidate.keys())
    return {k: sorted(v) for k, v in buckets.items()}


def summary(labels, buckets, counts):
    lines = ["| Side | Tests run |", "|---|---|"]
    lines += [f"| {label} | {counts[label]} |" for label in labels] + [f"| candidate | {counts['candidate']} |", ""]
    lines += ["| Bucket | Count |", "|---|---|"] + [f"| {k} | {len(v)} |" for k, v in buckets.items()]
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--baseline", action="append", required=True, metavar="LABEL=LOG[,LOG]")
    ap.add_argument("--candidate", required=True, metavar="LOG[,LOG]")
    ap.add_argument("--out", help="directory for summary.md and one <bucket>.txt per bucket (one id per line)")
    a = ap.parse_args(argv)
    baselines, counts = {}, {}
    try:
        for spec in a.baseline:
            label, sep, logs = spec.partition("=")
            if not sep or not label or not logs:
                ap.error(f"--baseline needs LABEL=LOG, got {spec!r}")
            baselines[label] = parse(logs.split(","))
            counts[label] = len(baselines[label])
        candidate = parse(a.candidate.split(","))
    except OSError as e:
        print(f"baseline-diff: {e}", file=sys.stderr)
        return 2
    counts["candidate"] = len(candidate)
    if not candidate or not all(baselines.values()):
        print("baseline-diff: a side has no PASSED/FAILED lines; run pytest with -rA", file=sys.stderr)
        return 2
    buckets = sort_results(baselines, candidate)
    text = summary(list(baselines), buckets, counts)
    if a.out:
        out = Path(a.out)
        out.mkdir(parents=True, exist_ok=True)
        (out / "summary.md").write_text(text)
        for k, v in buckets.items():
            (out / f"{k}.txt").write_text("".join(n + "\n" for n in v))
    sys.stdout.write(text)
    for node in buckets["regression"]:
        print(f"REGRESSION {node}")
    return 1 if buckets["regression"] else 0


if __name__ == "__main__":
    sys.exit(main())
