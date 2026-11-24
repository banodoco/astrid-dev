#!/usr/bin/env python3
"""Summarize individual A-6 hash observer logs without making savings claims."""

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import sys


KINDS = ("sha256", "sha256.file_digest", "yaml.safe_load")


def load_log(path):
    if not path.is_file():
        raise ValueError(f"missing log: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read valid JSON log {path}: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("events"), list):
        raise ValueError(f"invalid log structure in {path}: expected an events array")
    for index, event in enumerate(data["events"]):
        if not isinstance(event, dict) or not isinstance(event.get("kind"), str):
            raise ValueError(f"invalid event {index} in {path}: expected an object with kind")
    return data


def caller_label(event):
    caller = event.get("caller")
    if not isinstance(caller, list) or len(caller) != 3:
        return "unknown caller"
    filename, line, function = caller
    return f"{filename}:{line} `{function}`"


def number(value):
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def summarize(path, data):
    events = data["events"]
    raw_counts = Counter(event["kind"] for event in events)
    lines = [f"## {path}", "", f"Raw events: {len(events)}.", "", "### Raw event counts", "", "| Kind | Events |", "| --- | ---: |"]
    for kind, count in sorted(raw_counts.items()):
        lines.append(f"| `{kind}` | {count} |")

    lines += [
        "",
        "### Counts, bytes, and elapsed time by event kind",
        "",
        "Known bytes sum only numeric `bytes` fields; unknown bytes counts events without a numeric byte count. Elapsed values are summed observed call durations.",
        "",
        "| Kind | Events | Known bytes | Unknown byte counts | Summed elapsed (s) | Partial observer bookkeeping (s) |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for kind in KINDS:
        rows = [event for event in events if event["kind"] == kind]
        known_bytes = sum(number(event.get("bytes")) or 0 for event in rows)
        unknown_bytes = sum(number(event.get("bytes")) is None for event in rows)
        elapsed_ns = sum(number(event.get("elapsed_ns")) or 0 for event in rows)
        observer_ns = sum(number(event.get("observer_ns")) or 0 for event in rows)
        observer = f"{observer_ns / 1e9:.6f}" if kind == "sha256" else "not measured"
        lines.append(f"| `{kind}` | {len(rows)} | {known_bytes} | {unknown_bytes} | {elapsed_ns / 1e9:.6f} | {observer} |")

    lines += [
        "",
        "### Counts, bytes, and elapsed time by caller",
        "",
        "| Kind | Caller | Events | Known bytes | Unknown byte counts | Summed elapsed (s) | Partial observer bookkeeping (s) |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    groups = defaultdict(list)
    for event in events:
        if event["kind"] in KINDS:
            groups[(event["kind"], caller_label(event))].append(event)
    for (kind, caller), rows in sorted(groups.items()):
        escaped_caller = caller.replace("|", "\\|")
        known_bytes = sum(number(event.get("bytes")) or 0 for event in rows)
        unknown_bytes = sum(number(event.get("bytes")) is None for event in rows)
        elapsed_ns = sum(number(event.get("elapsed_ns")) or 0 for event in rows)
        observer_ns = sum(number(event.get("observer_ns")) or 0 for event in rows)
        observer = f"{observer_ns / 1e9:.6f}" if kind == "sha256" else "not measured"
        lines.append(f"| `{kind}` | {escaped_caller} | {len(rows)} | {known_bytes} | {unknown_bytes} | {elapsed_ns / 1e9:.6f} | {observer} |")

    lines += [
        "",
        "### Interpretation limits",
        "",
        "- Summed call durations can overlap across threads; SHA-256 copies can inherit elapsed time and lead to repeated accounting. These sums do not partition wall time.",
        "- `sha256.file_digest` elapsed time includes file reads and hashing; keep it separate from pure SHA-256 wrapper timing.",
        "- Observer bookkeeping is partial and reported only where the SHA-256 wrapper provides `observer_ns`; it is not total instrumentation overhead.",
        "- Coverage is limited to instrumented hash/YAML calls in the process that loaded the probe. Launcher subprocesses, already-running services, native/OpenSSL constructors, and unobserved file-read APIs may be absent. Unknown byte counts and unmatched paths remain unknown.",
        "- These observations do not establish performance savings or a complete process-wide census.",
        "",
    ]
    return lines


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("logs", nargs="+", type=Path, help="individual JSON hash log files")
    args = parser.parse_args()
    try:
        output = ["# A-6 hash witness summaries", ""]
        for path in args.logs:
            output.extend(summarize(path, load_log(path)))
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    sys.stdout.write("\n".join(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
