#!/usr/bin/env python3
"""Sort a candidate's test failures against one or more baselines (see env/README.md).

Input: pytest output run with -rA (PYTEST_ADDOPTS=-rA), one or more log files per side, comma-separated.
  python3 -I baseline-diff.py --baseline served-11=base.log --baseline main=main1.log,main2.log \
      --candidate cand.log [--out DIR]

Buckets for each test the candidate ran:
  regression   failed on the candidate; ran and passed on at least one baseline. Blocks.
  no-baseline  failed on the candidate; ran on no baseline. Fix it if the run added the test.
               Reported always; blocks only with --fail-on-no-baseline (or --strict).
  preexisting  failed on the candidate and on every baseline it ran on. Goes to its own project.
  fixed        passed on the candidate; failed on a baseline and passed on none.
  missing      passed on a baseline; not run on the candidate (deleted, skipped or uncollected).
               Reported always; blocks only with --fail-on-missing (or --strict).
An XFAIL counts as passing, because the test met its expectation; a strict XPASS is reported FAILED by pytest.
What is read from a log: if it holds a "short test summary info" section, the last one before each of the log's own
runs' final result lines (sequential runs, such as a GitHub job's several pytest steps or a repeat loop, are each read;
pytest output that a test prints from an inner run is not counted), plus the failed subtests, which
pytest counts in "N failed" but gives no summary row; each is read from its SUBFAILED(...) progress line and keyed
"<nodeid> SUBFAILED(<params>)". A failed subtest with no entry on a baseline takes its parent test's status there.
A log with such a section but no final result line is truncated: bad input. A log with no such section (bare
PASSED/FAILED lines) is read line by line. GitHub's timestamp prefix is ignored.
Exit 0: nothing that blocks. Exit 1: regressions; also missing with --fail-on-missing, and no-baseline with
--fail-on-no-baseline (--strict sets both, which is what a gate uses). Exit 2: bad input.
"""
import argparse
import re
import sys
from pathlib import Path

_LINE = re.compile(r"^(PASSED|FAILED|ERROR|XFAIL|XPASS) (.+)$")
_STAMP = re.compile(r"^\d{4}-\d\d-\d\dT[\d:.]+Z ?")
_FINAL = re.compile(r"^=*\s*((?:\d+ (?:failed|passed|errors?|skipped|deselected|xfailed|xpassed)\b|no tests ran\b).*) in [\d.]+s\b")
_SUMMARY = re.compile(r"^=+ short test summary info =+$")
_SUBFAILED = re.compile(r"^(\S+::\S+) SUBFAILED(\(.*?\))\s+\[\s*\d+%\]$")
PASS, FAIL = "passed", "failed"


class TruncatedLog(ValueError):
    """A log with a short test summary section but no final result line after it."""


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
    # No [parameters]: the id runs to the " - " before a message, or to the end (an id may hold spaces, as
    # Playwright's do; a pytest id without brackets never does).
    return rest.split(" - ", 1)[0].strip()


_HEADER = re.compile(r"^=+ test session starts =+$")
_STEP = re.compile(r"^##\[group\]Run ")
_SELECTION = re.compile(r"^===== selection \d+ of \d+: ")
_CANCELLED = re.compile(r"^##\[error\]The operation was cancell?ed\.")


def _top_level_runs(lines):
    """The log's own pytest runs as [(start, summary_start or None, end)], and problems.

    A log can hold several sequential runs (a GitHub job's several pytest steps, a repeat loop, two runs pasted
    together), and a test can print an inner run's output inside the outer one. A GitHub job log is cut at each
    "##[group]Run" step line and each "===== selection i of n" repeat line, and each piece's run is its last final
    result line with the last summary section before it (inner output comes before the outer summary). A plain log
    pairs each "test session starts" line with a final result line like a bracket: a top-level pair is a run, a pair
    inside another is an inner run. A plain log with no session header (pytest -q) is one run. A run that starts and
    never ends, or GitHub's cancel line, is a problem.
    """
    runs, problems = [], []
    if any(_CANCELLED.match(line) for line in lines):
        problems.append("the job was cancelled or timed out")
    if any(_STEP.match(line) for line in lines):
        bounds = [i for i, line in enumerate(lines) if _STEP.match(line) or _SELECTION.match(line)]
        for a, b in zip([0] + bounds, bounds + [len(lines)]):
            finals = [i for i in range(a, b) if _FINAL.match(lines[i])]
            if not finals:
                if any(_HEADER.match(lines[i]) or _SUMMARY.match(lines[i]) for i in range(a, b)):
                    problems.append(f"a pytest run from line {a + 1} has no final result line")
                continue
            starts = [i for i in range(a, finals[-1]) if _SUMMARY.match(lines[i])]
            runs.append((a, starts[-1] if starts else None, finals[-1]))
        return runs, problems
    if not any(_HEADER.match(line) for line in lines):
        finals = [i for i, line in enumerate(lines) if _FINAL.match(line)]
        starts = [i for i, line in enumerate(lines) if _SUMMARY.match(line)]
        if finals:
            before = [i for i in starts if i < finals[-1]]
            runs.append((0, before[-1] if before else None, finals[-1]))
        if starts and (not finals or starts[-1] > finals[-1]):
            problems.append("a short test summary section has no final result line after it")
        return runs, problems
    stack = []
    for i, line in enumerate(lines):
        if _HEADER.match(line):
            stack.append(i)
        elif _FINAL.match(line) and stack:
            begin = stack.pop()
            if not stack:
                starts = [k for k in range(begin, i) if _SUMMARY.match(lines[k])]
                runs.append((begin, starts[-1] if starts else None, i))
    if stack:
        problems.append(f"a pytest session from line {stack[0] + 1} has no final result line")
    return runs, problems


def _result_lines(path):
    """(status, node id) for the lines of one log that count: each of the log's own runs' summary sections and failed
    subtests (see _top_level_runs), or every line of a log with no summary section at all (bare PASSED/FAILED lines)."""
    lines = [_STAMP.sub("", raw).strip() for raw in Path(path).read_text(errors="replace").splitlines()]
    if not any(_SUMMARY.match(line) or _HEADER.match(line) or _STEP.match(line) for line in lines):
        for line in lines:
            m = _LINE.match(line)
            if m:
                yield m.group(1), _node_id(m.group(2))
        return
    runs, problems = _top_level_runs(lines)
    if problems or not runs:
        raise TruncatedLog(f"{path}: " + ("; ".join(problems) or "no final result line")
                           + " (cancelled, timed out or truncated job)")
    for begin, summary, end in runs:
        if summary is not None:
            for line in lines[summary + 1:end]:
                m = _LINE.match(line)
                if m:
                    yield m.group(1), _node_id(m.group(2))
        seen = set()
        for line in lines[begin:end]:
            m = _SUBFAILED.match(line)
            if m and line not in seen:
                seen.add(line)
                yield "FAILED", f"{m.group(1)} SUBFAILED{m.group(2)}"


def parse(paths):
    """Map node id to passed/failed across the given -rA logs; a failure anywhere wins."""
    out = {}
    for path in paths:
        for status, node in _result_lines(path):
            result = FAIL if status in ("FAILED", "ERROR") else PASS
            if out.get(node) != FAIL:
                out[node] = result
    return out


def sort_results(baselines, candidate):
    """baselines: {label: {id: status}}; candidate: {id: status}. Returns {bucket: sorted ids}."""
    buckets = {k: [] for k in ("regression", "no-baseline", "preexisting", "fixed", "missing")}
    for node, status in candidate.items():
        seen = [b[node] for b in baselines.values() if node in b]
        if not seen and " SUBFAILED(" in node:  # a subtest that fails is only new if its parent test was not failing
            parent = node.split(" SUBFAILED(")[0]
            seen = [b[parent] for b in baselines.values() if parent in b]
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
    ap.add_argument("--fail-on-missing", action="store_true",
                    help="exit 1 when any test that passed on a baseline did not run on the candidate")
    ap.add_argument("--fail-on-no-baseline", action="store_true",
                    help="exit 1 when a test fails on the candidate and ran on no baseline (a new failing test)")
    ap.add_argument("--strict", action="store_true", help="both --fail-on-missing and --fail-on-no-baseline")
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
    except (OSError, TruncatedLog) as e:
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
    fail_missing = a.fail_on_missing or a.strict
    fail_new = a.fail_on_no_baseline or a.strict
    if fail_missing:
        for node in buckets["missing"]:
            print(f"MISSING {node}")
    if fail_new:
        for node in buckets["no-baseline"]:
            print(f"NO-BASELINE {node}")
    blocked = buckets["regression"] or (fail_missing and buckets["missing"]) or (fail_new and buckets["no-baseline"])
    return 1 if blocked else 0


if __name__ == "__main__":
    sys.exit(main())
