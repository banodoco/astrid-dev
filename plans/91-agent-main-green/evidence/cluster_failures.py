#!/usr/bin/env python3
"""Group pytest failures in GitHub Actions job logs by where they fail.

Usage: cluster_failures.py OUT_DIR LOG [LOG ...]

Each LOG is one job's plain-text log (from the run's log archive). The script
reads pytest's failure sections ("____ test_name ____"), takes the frame that
raised (the last "path.py:N: ExceptionType" line) and the first "E " line,
and groups failing IDs by that raise site. It joins sections to the
"FAILED/ERROR <nodeid> - message" summary lines by test name.

Writes OUT_DIR/clusters.json and OUT_DIR/clusters.md. Standard library only.
"""
from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

STAMP = re.compile(r"^\d{4}-\d\d-\d\dT[\d:.]+Z ?")
HEADER = re.compile(r"^_+ (.+?) _+$")
FRAME = re.compile(r"^([\w./\-]+\.py):(\d+): (\w[\w.]*)\s*$")
STDLIB = re.compile(r"(hostedtoolcache|/usr/lib/python|site-packages/(_pytest|pluggy))")
SUMMARY = re.compile(r"^(FAILED|ERROR) (\S+?)(?: - (.*))?$")
SECTION_END = re.compile(r"^(=+ (short test summary info|warnings summary|.*(passed|failed|error).* in [\d.]+s).*=+|-+ Captured .*-+)$")


def norm(text: str) -> str:
    text = re.sub(r"0x[0-9a-f]+", "<addr>", text)
    text = re.sub(r"\b[0-9a-f]{12,}\b", "<hash>", text)
    text = re.sub(r"/(tmp|home|opt|private|var)/\S*", "<path>", text)
    text = re.sub(r"\d+", "N", text)
    return text[:160]


def short_name(nodeid: str) -> str:
    return nodeid.split(" SUBFAILED(")[0].split("::")[-1]


FINAL = re.compile(r"^=*\s*(\d+ (failed|passed|errors?|skipped|deselected)\b.*) in [\d.]+s\b")
SUBFAILED = re.compile(r"^(\S+::\S+) SUBFAILED(\(.*?\))\s+\[\s*\d+%\]$")


def split_nodeid(rest: str):
    """Split "<nodeid> - <message>" where the nodeid may hold spaces inside its [parameters]."""
    depth = 0
    for index, char in enumerate(rest):
        if char == "[":
            depth += 1
        elif char == "]":
            depth = max(0, depth - 1)
        elif depth == 0 and rest.startswith(" - ", index):
            return rest[:index], rest[index + 3:]
    return rest, ""


SESSION = re.compile(r"^=+ test session starts =+$")
STEP = re.compile(r"^##\[group\]Run ")
SELECTION = re.compile(r"^===== selection \d+ of \d+: ")
SUMMARY_START = re.compile(r"^=+ short test summary info =+$")


def top_level_runs(lines):
    """The job's own pytest runs as [(start, summary_start or None, end)].

    A GitHub job log is cut at each "##[group]Run" step and each "===== selection i of n" repeat, and each piece's
    run is its last final result line with the last summary section before it; a plain log pairs "test session
    starts" with final result lines like brackets (an inner run stays inside its outer one); a plain log with no
    session header is one run. Same rule as astrid-dev env/baseline-diff.py and astrid-agent
    scripts/ci/agent_ceiling_compare.py.
    """
    runs = []
    if any(STEP.match(line) for line in lines):
        bounds = [i for i, line in enumerate(lines) if STEP.match(line) or SELECTION.match(line)]
        for a, b in zip([0] + bounds, bounds + [len(lines)]):
            finals = [i for i in range(a, b) if FINAL.match(lines[i])]
            if finals:
                starts = [i for i in range(a, finals[-1]) if SUMMARY_START.match(lines[i])]
                runs.append((a, starts[-1] if starts else None, finals[-1]))
        return runs
    if not any(SESSION.match(line) for line in lines):
        finals = [i for i, line in enumerate(lines) if FINAL.match(line)]
        if finals:
            starts = [i for i in range(finals[-1]) if SUMMARY_START.match(lines[i])]
            runs.append((0, starts[-1] if starts else None, finals[-1]))
        return runs
    stack = []
    for i, line in enumerate(lines):
        if SESSION.match(line):
            stack.append(i)
        elif FINAL.match(line) and stack:
            begin = stack.pop()
            if not stack:
                starts = [k for k in range(begin, i) if SUMMARY_START.match(lines[k])]
                runs.append((begin, starts[-1] if starts else None, i))
    return runs


def outer_summary(lines):
    """FAILED/ERROR rows of the job's own pytest runs, plus their failed subtests.

    A failed subtest is counted by pytest in "N failed" but has no summary row, so it is taken from its progress line
    and keyed "<nodeid> SUBFAILED(<params>)". Pytest output that a test prints from an inner run is not counted.
    """
    rows = []
    for begin, summary, end in top_level_runs(lines):
        if summary is not None:
            for line in lines[summary + 1:end]:
                match = re.match(r"^(FAILED|ERROR) (.+)$", line)
                if match and "::" in match.group(2):
                    nodeid, message = split_nodeid(match.group(2))
                    rows.append((match.group(1), nodeid.strip(), message.strip()))
        seen = set()
        for line in lines[begin:end]:
            match = SUBFAILED.match(line)
            if match:
                nodeid = f"{match.group(1)} SUBFAILED{match.group(2)}"
                if nodeid not in seen:
                    seen.add(nodeid)
                    rows.append(("FAILED", nodeid, ""))
    return rows


def summary_counts(lines):
    """The (failed, errors) summed over the job's own runs' final result lines, or None when it has none."""
    runs = top_level_runs(lines)
    if not runs:
        return None
    failed = errors = 0
    for _, _, end in runs:
        text = lines[end]
        f = re.search(r"(\d+) failed", text)
        e = re.search(r"(\d+) errors?", text)
        failed += int(f.group(1)) if f else 0
        errors += int(e.group(1)) if e else 0
    return failed, errors


def parse(log: Path, job: str):
    lines = [STAMP.sub("", raw.rstrip("\n")) for raw in log.read_text(errors="replace").splitlines()]
    summary = outer_summary(lines)
    sections = {}
    current, body = None, []

    def close():
        if current is None:
            return
        frames = [FRAME.match(item) for item in body]
        frames = [m for m in frames if m]
        e_lines = [item[1:].strip() for item in body if item.startswith("E ")]
        raise_site = f"{frames[-1].group(1)}:{frames[-1].group(2)}" if frames else "?"
        exc = frames[-1].group(3) if frames else (e_lines[0].split(":")[0] if e_lines else "?")
        product = [f"{m.group(1)}:{m.group(2)}" for m in frames
                   if not m.group(1).startswith("tests/") and not STDLIB.search(m.group(1))]
        test_frames = [f"{m.group(1)}:{m.group(2)}" for m in frames if m.group(1).startswith("tests/")]
        sections.setdefault(current, []).append({
            "raise_site": raise_site,
            "exception": exc,
            "message": norm(e_lines[0]) if e_lines else "",
            "first_product_frame": product[0] if product else None,
            "last_test_frame": test_frames[-1] if test_frames else None,
        })

    for line in lines:
        header = HEADER.match(line)
        if header:
            close()
            name = header.group(1)
            name = re.sub(r"^(ERROR at (setup|teardown) of |)", "", name).strip()
            current, body = name, []
            continue
        if current is not None and SECTION_END.match(line):
            close()
            current, body = None, []
            continue
        if current is not None:
            body.append(line)
    close()

    records = []
    used = collections.Counter()
    for outcome, nodeid, message in summary:
        name = short_name(nodeid)
        candidates = sections.get(name) or []
        index = used[name]
        used[name] += 1
        detail = candidates[index] if index < len(candidates) else (candidates[-1] if candidates else None)
        records.append({
            "job": job,
            "outcome": outcome,
            "id": nodeid,
            "summary_message": norm(message),
            **(detail or {"raise_site": "?", "exception": "?", "message": "", "first_product_frame": None,
                          "last_test_frame": None}),
        })
    return records


def key(record):
    site = record["raise_site"]
    if site == "?":
        return f"no traceback | {record['summary_message'][:90]}"
    if STDLIB.search(site):
        # Raised inside the standard library or pytest: the caller decides the cause.
        caller = record["first_product_frame"] if record["first_product_frame"] and not STDLIB.search(record["first_product_frame"]) else record["last_test_frame"]
        return f"{record['exception']} via {caller or site}"
    return f"{record['exception']} at {site}"


def main(argv):
    out = Path(argv[1])
    out.mkdir(parents=True, exist_ok=True)
    records = []
    for name in argv[2:]:
        path = Path(name)
        job = re.sub(r"^\d+_", "", path.stem)  # the archive numbers its files in no stable order
        job_records = parse(path, job)
        records.extend(job_records)
        lines = [STAMP.sub("", raw) for raw in path.read_text(errors="replace").splitlines()]
        counts = summary_counts(lines)
        rows = collections.Counter(r["outcome"] for r in job_records)
        if counts is None:
            print(f"{job}: NO RESULT LINE (cancelled, timed out or truncated)")
        else:
            ok = (rows["FAILED"], rows["ERROR"]) == counts
            print(f"{job}: summary {counts[0]} failed, {counts[1]} errors; rows {rows['FAILED']} FAILED, {rows['ERROR']} ERROR"
                  f"{'' if ok else '  MISMATCH'}")
    groups = collections.defaultdict(list)
    for record in records:
        groups[key(record)].append(record)
    clusters = []
    for k, items in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        files = collections.Counter(r["id"].split("::")[0] for r in items)
        messages = collections.Counter(r["message"] or r["summary_message"] for r in items)
        products = collections.Counter(r["first_product_frame"] for r in items if r["first_product_frame"])
        clusters.append({
            "key": k,
            "count": len(items),
            "files": files.most_common(),
            "messages": messages.most_common(3),
            "first_product_frames": products.most_common(3),
            "ids": [r["id"] for r in items],
        })
    rows = ["cluster\toutcome\tjob\tid"]
    for number, (k, items) in enumerate(sorted(groups.items(), key=lambda kv: -len(kv[1])), 1):
        for r in sorted(items, key=lambda r: r["id"]):
            rows.append(f"C{number}\t{r['outcome']}\t{r['job']}\t{r['id']}")
    (out / "failing-ids.tsv").write_text("\n".join(rows) + "\n")
    (out / "clusters.json").write_text(json.dumps({"total": len(records), "clusters": clusters}, indent=1))
    lines = [f"# Failure clusters\n", f"{len(records)} failing IDs in {len(clusters)} clusters "
             f"(grouped by exception type and raise site).\n",
             "| # | IDs | Raise site | Top message | Top files |", "| --- | ---: | --- | --- | --- |"]
    for number, cluster in enumerate(clusters, 1):
        message = (cluster["messages"][0][0] if cluster["messages"] else "").replace("|", "\\|")[:110]
        files = ", ".join(f"`{f}` ({n})" for f, n in cluster["files"][:2])
        lines.append(f"| C{number} | {cluster['count']} | `{cluster['key']}` | {message} | {files} |")
    by_file = collections.Counter(r["id"].split("::")[0] for r in records)
    lines += ["", "## Failing IDs by test file", "", "| IDs | Clusters | File |", "| ---: | ---: | --- |"]
    clusters_per_file = collections.Counter()
    for cluster in clusters:
        for f, _ in cluster["files"]:
            clusters_per_file[f] += 1
    for f, n in by_file.most_common():
        lines.append(f"| {n} | {clusters_per_file[f]} | `{f}` |")
    (out / "clusters.md").write_text("\n".join(lines) + "\n")
    print(f"test files: {len(by_file)}")
    sizes = [c["count"] for c in clusters]
    for threshold in (50, 100, 150, 200):
        print(f"top {threshold} clusters cover {sum(sizes[:threshold])} of {len(records)}")
    print(f"clusters: {len(clusters)}; singletons: {sum(1 for s in sizes if s == 1)}; no traceback: "
          f"{sum(c['count'] for c in clusters if c['key'].startswith('no traceback'))}")


if __name__ == "__main__":
    main(sys.argv)
