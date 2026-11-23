"""Summary of an A/B(/C) run: medians per arm per group, ratios against the first arm ("before"), the share of the saving
that the VibeComfy fix accounts for, and a stage table for every arm that ran with --timings. Pure functions over records
(no process starts), used by ab_run.py, rebuild_ab_summary.py and test_ab_summary.py. Tolerant of missing fields.
CLI: python3 ab_summary.py EVIDENCE_DIR   (rebuilds summary-ab.json from EVIDENCE_DIR/records.jsonl)"""
import json, math, statistics, sys
from datetime import datetime, timezone
from ab_receipt import timings_error
from pathlib import Path

GROUPS = ("same", "changed", "timeline")
BASE = "before"; FIX_ARM, NOFIX_ARM = "after", "vc48"   # saving = before - after; without the VibeComfy fix = before - vc48

def _med(v): return round(statistics.median(v), 3) if v else None
def _duration(value, field, stage):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
        raise ValueError(f"invalid {field} for stage {stage!r}: {value!r}")
    return value

def is_warmup(r): return str(r.get("name", "")).endswith("-warmup")

def group_summary(records, arms, group):
    g = {}
    for arm in arms:
        rs = [r for r in records if r.get("group") == group and r.get("arm") == arm and not is_warmup(r)]
        ok = [r for r in rs if r.get("ok")]; w = [r["wall_seconds"] for r in ok]
        g[arm] = {"runs": len(rs), "succeeded": len(ok), "median_wall_seconds": _med(w), "min": min(w, default=None),
                  "max": max(w, default=None), "walls": w,
                  "load_before_1m": [round(r["load_before"][0], 2) for r in rs if r.get("load_before")],
                  "load_after_1m": [round(r["load_after"][0], 2) for r in rs if r.get("load_after")]}
    b = g.get(BASE, {}).get("median_wall_seconds")
    for arm in arms:
        m = g[arm]["median_wall_seconds"]
        g[arm]["ratio_vs_before"] = round(m / b, 3) if m and b else None
        g[arm]["percent_change_vs_before"] = round((m / b - 1) * 100, 1) if m and b else None
    if {BASE, FIX_ARM, NOFIX_ARM} <= set(arms):
        a, c = g[FIX_ARM]["median_wall_seconds"], g[NOFIX_ARM]["median_wall_seconds"]
        if None not in (a, b, c) and abs(b - a) >= 0.05:   # a saving smaller than 50 ms is noise, no share
            g["vibecomfy_fix_share"] = {
                "total_saving_before_minus_after_s": round(b - a, 3),
                "saving_without_vibecomfy_fix_before_minus_vc48_s": round(b - c, 3),
                "vibecomfy_fix_saving_vc48_minus_after_s": round(c - a, 3),
                "vibecomfy_fix_share_of_total_saving": round((c - a) / (b - a), 3),
                "agent_only_share_of_total_saving": round((b - c) / (b - a), 3)}
        else:
            g["vibecomfy_fix_share"] = None
    return g

def stage_table(records, arm, group):
    rows = [r["timings"] for r in records if r.get("group") == group and r.get("arm") == arm and not is_warmup(r)
            and r.get("ok") and isinstance(r.get("timings"), list)]
    names = {}
    for index, timings in enumerate(rows):
        for stage in timings:
            if not isinstance(stage, dict) or "stage" not in stage: continue
            sec = _duration(stage.get("seconds"), "seconds", stage["stage"])
            # Inclusive durations can overlap; retain them only as occurrence statistics.
            total = _duration(stage["total_seconds"], "total_seconds", stage["stage"]) if "total_seconds" in stage else sec
            names.setdefault((stage["stage"], stage.get("parent")), []).append((index, sec, total))
    result = []
    for (name, parent), occurrences in names.items():
        command_seconds = [0.0] * len(rows)
        command_counts = [0] * len(rows)
        for index, seconds, _ in occurrences:
            command_seconds[index] += seconds
            command_counts[index] += 1
        result.append({"stage": name, "parent": parent, "occurrences_seen": len(occurrences),
                       "median_seconds": round(statistics.median(x[1] for x in occurrences), 4),
                       "median_total_seconds": round(statistics.median(x[2] for x in occurrences), 4),
                       "median_command_seconds": round(statistics.median(command_seconds), 4),
                       "median_command_occurrences": statistics.median(command_counts)})
    return sorted(result, key=lambda row: -row["median_command_seconds"])

def validate_records(records, arms, samples, legacy_missing_collector_span=False):
    """Reject incomplete, duplicate, failed, or malformed command sets."""
    if not arms or not isinstance(samples, int) or isinstance(samples, bool) or samples < 1:
        raise ValueError("a nonempty arm list and positive sample count are required")
    expected = {f"{group}-{arm}-{k}" for group in GROUPS for arm in arms
                for k in ["warmup", *range(1, samples + 1)]}
    seen = set()
    for r in records:
        if not isinstance(r, dict): raise ValueError("record is not an object")
        name = r.get("name")
        if not isinstance(name, str) or name not in expected or name in seen:
            raise ValueError(f"unexpected or duplicate record: {name!r}")
        seen.add(name)
        if name not in {f"{r.get('group')}-{r.get('arm')}-{k}" for k in ["warmup", *range(1, samples + 1)]}:
            raise ValueError(f"record identity mismatch: {name}")
        wall = r.get("wall_seconds")
        if r.get("ok") is not True or r.get("exit_code") != 0 or isinstance(wall, bool) or not isinstance(wall, (int, float)) or not math.isfinite(wall) or wall < 0:
            raise ValueError(f"failed or malformed record: {name}")
        args = r.get("args", [])
        if (r.get("reconstructed") is not True and isinstance(args, list)
                and args[:2] == ["generate", "image"] and "--timings" in args):
            error = timings_error(r, allow_missing_span=legacy_missing_collector_span)
            if error: raise ValueError(f"{name}: {error}")
    if seen != expected:
        raise ValueError(f"incomplete records: missing {sorted(expected - seen)}")

def qualification(records, arms, samples, load_max, legacy=False, require_attestation=False):
    """Assess the fixed release gate without discarding descriptive evidence."""
    reasons = []
    if len(arms) != 3 or set(arms) != {"before", "after", "vc48"}:
        reasons.append("release qualification requires exactly before, after, and vc48 arms")
    if samples != 5:
        reasons.append("release qualification requires five measured samples per arm and group")
    if legacy or any(r.get("reconstructed") is True for r in records):
        reasons.append("historical or reconstructed evidence cannot establish the release gate")
    if (isinstance(load_max, bool) or not isinstance(load_max, (int, float))
            or not math.isfinite(load_max) or load_max != 1.0):
        reasons.append("release qualification requires the fixed load threshold 1.0")
    for r in records:
        if require_attestation:
            before, after = r.get("listener_before"), r.get("listener_after")
            required = {"port", "address_hex", "socket_table", "socket_inode", "pid", "start_ticks", "exe", "cwd", "selected_version", "manifest_shas", "scope"}
            if (not isinstance(before, dict) or not isinstance(after, dict) or not required <= before.keys()
                    or not required <= after.keys() or {k: v for k, v in before.items() if k != "scope"} !=
                    {k: v for k, v in after.items() if k != "scope"} or before.get("port") != r.get("door_port")):
                reasons.append(f"{r['name']}: missing or changed listener attestation")
        load = r.get("load_before")
        if (not isinstance(load, (list, tuple)) or not load
                or isinstance(load[0], bool) or not isinstance(load[0], (int, float))
                or not math.isfinite(load[0]) or load[0] < 0 or load[0] >= 1.0
                or (isinstance(load_max, (int, float)) and math.isfinite(load_max) and load[0] >= load_max)):
            reasons.append(f"{r['name']}: invalid or over-threshold start load")
    for arm in arms:
        if any(r.get('timeline_status') != 'accepted' for r in records
               if r.get('arm') == arm and r.get('group') == 'timeline'):
            reasons.append(f"{arm}: timeline receipt lacks accepted status")
        for groups, field in ((('same', 'changed'), 'kernel_task_id'), (('timeline',), 'accepted_revision_id')):
            rows = [r for r in records if r.get('arm') == arm and r.get('group') in groups]
            ids = [r.get(field) for r in rows]
            if any(not isinstance(value, str) or not value.strip() for value in ids):
                reasons.append(f"{arm}: missing {field}")
            elif len(set(ids)) != len(ids):
                reasons.append(f"{arm}: duplicate {field}")
    for group in ('same', 'changed'):
        medians = {}
        for arm in ('before', 'after'):
            walls = [r['wall_seconds'] for r in records if r.get('group') == group and r.get('arm') == arm and not is_warmup(r)]
            if walls: medians[arm] = statistics.median(walls)
        if ('before' not in medians or 'after' not in medians or medians['before'] <= 0
                or medians['after'] / medians['before'] > 0.5):
            reasons.append(f"{group}: after/before median ratio must be <= 0.5")
    return {"passed": not reasons, "reasons": reasons}

def summarize(records, OUT, SETTING, LOAD_MAX, ARMS, SAMPLES, quiet=False, legacy_missing_collector_span=False, unqualified_legacy=False, require_attestation=False, attestation=None):
    arms = list(ARMS)
    validate_records(records, arms, SAMPLES, legacy_missing_collector_span)
    summary = {"setting": SETTING, "when_utc": datetime.now(timezone.utc).isoformat(), "load_max": LOAD_MAX,
               "qualification": qualification(records, arms, SAMPLES, LOAD_MAX, legacy_missing_collector_span or unqualified_legacy, require_attestation),
               "arms": {a: {"launcher": v.get("launcher"), "door_port": v.get("door_port"), "generate_extra": v.get("generate_extra", [])} for a, v in ARMS.items()},
               "reconstructed": any(r.get("reconstructed") is True for r in records),
               "interpretation": "Fixed arm order and differing --timings instrumentation limit comparisons; median differences and shares do not establish causation.",
               "groups": {gr: group_summary(records, arms, gr) for gr in GROUPS}, "records": records,
               "stage_tables": {a: {gr: stage_table(records, a, gr) for gr in ("same", "changed")}
                                for a in arms if ARMS[a].get("generate_extra")}}
    if attestation is not None:
        summary["attestation"] = attestation
        if attestation == "off":
            summary["interpretation"] += " Runtime source bytes and listener identity were not attested."
    if any(r.get("reconstructed") is True and r.get("collector_span_seconds") is None for r in records):
        summary["interpretation"] += " Some reconstructed records lack collector span data; it cannot be recovered from those records."
    if legacy_missing_collector_span:
        summary["interpretation"] += " Historical import permits missing collector span data; those spans are unverified. Historical receipts and release qualification are unverified."
    Path(OUT).mkdir(parents=True, exist_ok=True)
    (Path(OUT) / "summary-ab.json").write_text(json.dumps(summary, indent=2))
    if not quiet: print_summary(summary, SAMPLES)
    return summary

def print_summary(summary, SAMPLES):
    arms = list(summary["arms"]); print("\nSETTING:", summary["setting"])
    if "attestation" in summary: print("Attestation:", summary["attestation"])
    print("Qualification:", "PASS" if summary["qualification"]["passed"] else "FAIL")
    for reason in summary["qualification"]["reasons"]: print("  ", reason)
    head = f"{'group':9s}" + "".join(f"{a + ' med s':>14s}" for a in arms) + "".join(f"{a + '/before':>14s}" for a in arms[1:]) + "   ok  load1 before-cmd"
    print(head)
    for gr, g in summary["groups"].items():
        lb = [x for a in arms for x in g[a]["load_before_1m"]]
        print(f"{gr:9s}" + "".join(f"{g[a]['median_wall_seconds']!s:>14s}" for a in arms)
              + "".join(f"{(str(g[a]['ratio_vs_before']) + ' (' + str(g[a]['percent_change_vs_before']) + '%)'):>14s}" for a in arms[1:])
              + "   " + "/".join(str(g[a]["succeeded"]) for a in arms) + f"  {min(lb, default=0):.2f}-{max(lb, default=0):.2f}")
    for gr, g in summary["groups"].items():
        s = g.get("vibecomfy_fix_share")
        if s: print(f"  {gr}: median differences before-after {s['total_saving_before_minus_after_s']} s; "
                    f"before-vc48 {s['saving_without_vibecomfy_fix_before_minus_vc48_s']} s; "
                    f"vc48-after {s['vibecomfy_fix_saving_vc48_minus_after_s']} s. "
                    "Differences do not establish causation (fixed order and differing instrumentation).")
    for arm, tabs in summary["stage_tables"].items():
        for gr, rows in tabs.items():
            print(f"\n{arm} arm stages, {gr} (median of {SAMPLES} commands; top 12 by exclusive seconds per command):")
            for r in rows[:12]: print(f"  {r['median_command_seconds']:8.3f} s exclusive/command  {r['median_command_occurrences']:g} occurrences/command  {r['median_seconds']:8.3f} s exclusive/occurrence  {r['stage']}  (in: {r['parent']})")

def rebuild(d, legacy_missing_collector_span=False, legacy_arms=None, legacy_samples=None):
    if legacy_missing_collector_span and (legacy_arms is None or legacy_samples is None):
        raise ValueError("historical rebuild requires explicit arms and samples")
    d = Path(d)
    lines = (d / "records.jsonl").read_text().splitlines()
    if not lines or any(not line.strip() for line in lines):
        raise ValueError("empty or malformed records.jsonl")
    entries = [json.loads(line) for line in lines]
    if not all(isinstance(r, dict) for r in entries):
        raise ValueError("records must be objects")
    marker = entries[-1]
    records = entries[:-1]
    if marker.get("records_complete") is not True or type(marker.get("count")) is not int or marker["count"] != len(records):
        raise ValueError("missing or invalid completion marker")
    if not legacy_missing_collector_span and any(
            r.get("reconstructed") is not True and isinstance(r.get("args"), list)
            and r["args"][:2] == ["generate", "image"] and "--timings" in r["args"]
            for r in records) and (type(marker.get("timing_receipt_schema")) is not int or marker["timing_receipt_schema"] != 1):
        raise ValueError("timed records require timing receipt schema 1; use --legacy-records for historical imports")
    arms = legacy_arms if legacy_missing_collector_span and legacy_arms is not None else marker.get("arms")
    samples = legacy_samples if legacy_missing_collector_span and legacy_samples is not None else marker.get("samples")
    if not isinstance(arms, list) or not arms or any(not isinstance(a, str) or not a for a in arms) or len(set(arms)) != len(arms):
        raise ValueError("completion marker lacks valid arm metadata")
    ports = marker.get("door_ports", {})
    if not isinstance(ports, dict): raise ValueError("invalid door port metadata")
    arm_config = {a: {"door_port": ports.get(a)} for a in arms}
    for a in arms:
        if any(r.get("arm") == a and "--timings" in r.get("args", []) for r in records):
            arm_config[a]["generate_extra"] = ["--timings"]
    schema = marker.get("qualification_schema")
    mode = marker.get("attestation")
    if schema == 2 and mode not in (None, "on") or schema == 3 and mode != "off":
        raise ValueError("invalid qualification schema and attestation mode")
    if mode is not None and schema not in (2, 3):
        raise ValueError("invalid qualification schema and attestation mode")
    attestation = "on" if schema == 2 else "off" if schema == 3 else None
    return summarize(records, d, "rebuilt from complete records.jsonl", marker.get("load_max"), arm_config, samples,
                     legacy_missing_collector_span=legacy_missing_collector_span,
                     unqualified_legacy=schema not in (2, 3),
                     require_attestation=schema == 2, attestation=attestation)

if __name__ == "__main__":
    try:
        import argparse
        parser = argparse.ArgumentParser(description="Rebuild an A/B summary from complete records")
        parser.add_argument("directory")
        parser.add_argument("--legacy-records", action="store_true", help="explicitly permit absent collector spans in historical records")
        parser.add_argument("--arms", nargs="+")
        parser.add_argument("--samples", type=int)
        options = parser.parse_args()
        if (options.arms is not None or options.samples is not None) and not options.legacy_records:
            parser.error("--arms and --samples require --legacy-records")
        result = rebuild(options.directory, legacy_missing_collector_span=options.legacy_records,
                         legacy_arms=options.arms, legacy_samples=options.samples)
        marker = json.loads((Path(options.directory) / "records.jsonl").read_text().splitlines()[-1])
        if marker.get("qualification_schema") in (1, 2, 3) and not result["qualification"]["passed"]:
            sys.exit("Qualification failed; summary and raw evidence retained")
    except (OSError, ValueError, TypeError, IndexError) as exc:
        sys.exit(f"Cannot rebuild summary: {exc}")
