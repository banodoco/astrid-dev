#!/usr/bin/env python3
"""Per-file test counts and failures from an astrid-app `test.yml` job log (the `vitest` job).

The App's hosted job prints vitest's default reporter, which names each test FILE with its count
("✓ src/x.test.ts (360 tests) 185ms") but names single tests only when they are slow or fail. So a
whole-run comparison with Release 14 is made on three things this script extracts:
  * every file with its test count and its failed / skipped / todo counts (a missing file or a
    smaller count is a lost id and counts as red until explained);
  * every failing test, named, from the failure blocks ("FAIL  <file> > <suite> > <test>");
  * the run totals (Test Files, Tests), and the node:test totals of `node --test` steps.

  python3 -I app_test_ids.py extract JOB.log > counts.tsv        # also prints totals to stderr
  python3 -I app_test_ids.py diff BASE.tsv CAND.tsv [--strict]   # exit 1 on new failure / lost count

TSV columns: kind (FILE|FAIL|TOTAL), file-or-id, tests, failed, skipped.
Exit codes: 0 nothing blocks, 1 new failure or lost tests, 2 bad input (log truncated, no totals line).
"""
import re
import sys

_STAMP = re.compile(r"^﻿?\d{4}-\d\d-\d\dT[\d:.]+Z ?")
_ANSI = re.compile(r"\x1b\[[0-9;]*m")
# " ✓ src/a.test.ts (360 tests) 185ms"   " ❯ src/a.test.ts (12 tests | 2 failed | 1 skipped) 90ms"
_FILE = re.compile(r"^\s*([✓❯↓×])\s+(\S+\.(?:test|spec)\.[cm]?[jt]sx?)\s+\((\d+) tests?((?: \| \d+ (?:failed|skipped|todo))*)\)")
_FAIL = re.compile(r"^\s*(?:FAIL|×)\s+(\S+\.(?:test|spec)\.[cm]?[jt]sx?(?: > .+)?)\s*$")
_TOTAL_FILES = re.compile(r"^\s*Test Files\s+(\d.*)$")
_TOTAL_TESTS = re.compile(r"^\s*Tests\s+(\d.*)$")
_COUNT = re.compile(r"(\d+) (failed|passed|skipped|todo)")


def _lines(path):
    with open(path, errors="replace") as f:
        for raw in f:
            yield _ANSI.sub("", _STAMP.sub("", raw.rstrip("\n")))


def extract(path):
    files, fails, totals, runs = {}, set(), {}, 0
    for line in _lines(path):
        m = _FILE.match(line)
        if m:
            name, n, extras = m.group(2), int(m.group(3)), m.group(4)
            failed = sum(int(x) for x, k in re.findall(r"(\d+) (failed)", extras))
            skipped = sum(int(x) for x, k in re.findall(r"(\d+) (skipped|todo)", extras))
            files[name] = (n, failed, skipped)
            continue
        m = _FAIL.match(line)
        if m:
            fails.add(m.group(1).strip())
            continue
        m = _TOTAL_FILES.match(line)
        if m:  # a job can hold several vitest runs (npm test, then the sdk-boundary run): keep each, numbered
            runs += 1
            totals[f"files#{runs}"] = dict((k, int(v)) for v, k in _COUNT.findall(m.group(1)))
        m = _TOTAL_TESTS.match(line)
        if m:
            totals[f"tests#{runs}"] = dict((k, int(v)) for v, k in _COUNT.findall(m.group(1)))
    if not runs:
        raise SystemExit("bad input: no vitest 'Tests' totals line (log truncated or the job did not run vitest)")
    return files, fails, totals


def write_tsv(files, fails, totals, out):
    out.write("kind\tid\ttests\tfailed\tskipped\n")
    for k in sorted(totals):
        t = totals[k]
        out.write(f"TOTAL\t{k}\t{sum(t.values())}\t{t.get('failed', 0)}\t{t.get('skipped', 0)}\n")
    for name in sorted(files):
        n, f, s = files[name]
        out.write(f"FILE\t{name}\t{n}\t{f}\t{s}\n")
    for ident in sorted(fails):
        out.write(f"FAIL\t{ident}\t\t\t\n")


def read_tsv(path):
    files, fails, totals = {}, set(), {}
    for line in open(path):
        p = line.rstrip("\n").split("\t")
        if p[0] == "FILE":
            files[p[1]] = (int(p[2]), int(p[3]), int(p[4]))
        elif p[0] == "FAIL":
            fails.add(p[1])
        elif p[0] == "TOTAL":
            totals[p[1]] = int(p[2])
    return files, fails, totals


def diff(base, cand, strict):
    bf, bx, bt = read_tsv(base)
    cf, cx, ct = read_tsv(cand)
    new_fail = sorted(cx - bx)
    fixed = sorted(bx - cx)
    lost_files = sorted(set(bf) - set(cf))
    added_files = sorted(set(cf) - set(bf))
    shrunk = sorted((f, bf[f][0], cf[f][0]) for f in set(bf) & set(cf) if cf[f][0] < bf[f][0])
    grown = sorted((f, bf[f][0], cf[f][0]) for f in set(bf) & set(cf) if cf[f][0] > bf[f][0])
    new_failing_files = sorted(f for f in cf if cf[f][1] and not (f in bf and bf[f][1]))
    print(f"base totals {bt}  candidate totals {ct}")
    for title, rows in (("NEW FAILING TESTS", new_fail), ("FILES NEWLY FAILING", new_failing_files),
                        ("LOST FILES (in base, absent in candidate)", lost_files),
                        ("FILES WITH FEWER TESTS", shrunk), ("fixed", fixed),
                        ("added files", added_files), ("files with more tests", grown)):
        print(f"{title}: {len(rows)}")
        for r in rows[:50]:
            print("  ", r)
    blocks = bool(new_fail or new_failing_files)
    if strict:
        blocks = blocks or bool(lost_files or shrunk)
    return 1 if blocks else 0


def main(argv):
    if len(argv) >= 3 and argv[1] == "extract":
        files, fails, totals = extract(argv[2])
        write_tsv(files, fails, totals, sys.stdout)
        print(f"{len(files)} files, totals {totals}, {len(fails)} failing tests", file=sys.stderr)
        return 0
    if len(argv) >= 4 and argv[1] == "diff":
        return diff(argv[2], argv[3], "--strict" in argv)
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
