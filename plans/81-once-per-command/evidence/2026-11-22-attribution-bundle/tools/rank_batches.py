#!/usr/bin/env python3
"""Reproduce descriptive attribution tables from a saved trial manifest."""
import argparse
import json
import math
import re
import statistics
from collections import defaultdict
from pathlib import Path
import pstats

IMPORT = re.compile(r'^import time:\s*(\d+)\s*\|\s*\d+\s*\|\s*(\S+)\s*$')


def median(values):
    return statistics.median(values)


def stage_summary(trials, root):
    samples = []
    for trial in trials:
        data = json.loads((root / trial['stdout']).read_text())
        rows = data.get('timings')
        if not isinstance(rows, list):
            raise ValueError(f"missing timing rows: {trial['stdout']}")
        totals = defaultdict(lambda: [0.0, 0.0, 0])
        has_total = {}
        for row in rows:
            key = (row['stage'], row.get('parent'))
            val = totals[key]
            val[0] += float(row['seconds'])
            val[2] += 1
            if 'total_seconds' in row:
                val[1] += float(row['total_seconds'])
                has_total[key] = True
            else:
                has_total[key] = False
        samples.append((totals, has_total))
    keys = sorted({key for sample, _ in samples for key in sample}, key=lambda k: (k[0], k[1] or ''))
    result = []
    for key in keys:
        # Missing rows mean zero occurrences in that trial. Inclusive values are
        # unknown if any observed row lacks them; never infer them from self time.
        observed = [flag[key] for rows, flag in samples if key in rows]
        result.append({'stage': key[0], 'parent': key[1],
                       'seconds_median': median([rows[key][0] if key in rows else 0 for rows, _ in samples]),
                       'total_seconds_median': median([rows[key][1] if key in rows else 0 for rows, _ in samples]) if all(observed) else None,
                       'count_median': median([rows[key][2] if key in rows else 0 for rows, _ in samples])})
    return result


def import_summary(trials, root):
    by_module = []
    for trial in trials:
        modules = defaultdict(int)
        for line in (root / trial['stderr']).read_text(errors='replace').splitlines():
            match = IMPORT.match(line)
            if match:
                modules[match[2]] += int(match[1])
        if not modules:
            raise ValueError(f"no importtime records: {trial['stderr']}")
        by_module.append(modules)
    by_package = []
    for modules in by_module:
        packages = defaultdict(int)
        for name, value in modules.items():
            packages[name.split('.')[0]] += value
        by_package.append(packages)
    def ranked(samples):
        keys = {key for sample in samples for key in sample}
        return sorted(((key, median([sample.get(key, 0) for sample in samples]) / 1e6) for key in keys), key=lambda x: (-x[1], x[0]))[:25]
    return ranked(by_package), ranked(by_module)


def profile_summary(trials, root):
    samples = []
    for trial in trials:
        stats = pstats.Stats(str(root / trial['profile']))
        if stats.total_tt <= 0:
            raise ValueError(f"empty profile: {trial['profile']}")
        functions = {}
        for (filename, line, name), (primitive, calls, self_time, cumulative, _callers) in stats.stats.items():
            label = f'{filename}:{line}({name})'
            functions[label] = (calls, self_time, cumulative, self_time / stats.total_tt, cumulative / stats.total_tt)
        samples.append(functions)
    keys = {key for sample in samples for key in sample}
    rows = []
    for key in keys:
        values = [sample.get(key, (0, 0, 0, 0, 0)) for sample in samples]
        rows.append((key, *(median([v[i] for v in values]) for i in range(5))))
    return rows


def fmt(value):
    return 'unknown' if value is None else f'{value:.6f}'


def render(route, groups, root):
    out = [f'# Attribution: {route}', '', 'Descriptive source measurements; cProfile values are profiled measurements and are not converted to plain wall seconds.', '']
    for mode in ('plain', 'timings', 'importtime', 'cprofile'):
        trials = groups.get(mode, [])
        if trials:
            walls = [float(t['wall_seconds']) for t in trials]
            out += [f'{mode} wall: n={len(walls)}, median={median(walls):.6f} s, min={min(walls):.6f} s, max={max(walls):.6f} s.', '']
    plain = groups.get('plain', [])
    wall = median([float(t['wall_seconds']) for t in plain]) if plain else None
    stages = stage_summary(groups['timings'], root) if groups.get('timings') else []
    out += ['## Stages', '', 'Self and inclusive medians are sums within each trial; missing inclusive data is unknown. Parent names are reported as recorded.', '', '| Stage | Parent | Count median | Self s | Inclusive s |', '| --- | --- | ---: | ---: | ---: |']
    for row in sorted(stages, key=lambda r: (-(r['total_seconds_median'] if r['total_seconds_median'] is not None else -1), r['stage'], r['parent'] or '')):
        out.append(f"| {row['stage']} | {row['parent'] or '—'} | {fmt(row['count_median'])} | {fmt(row['seconds_median'])} | {fmt(row['total_seconds_median'])} |")
    out.append('')
    if groups.get('importtime'):
        for label, rows in zip(('Packages', 'Modules'), import_summary(groups['importtime'], root)):
            out += [f'## Imports: {label}', '', 'Median self seconds from separately instrumented processes; these do not partition plain wall.', '', '| Name | Self s |', '| --- | ---: |']
            out += [f'| {name} | {value:.6f} |' for name, value in rows]
            out.append('')
    if groups.get('cprofile'):
        rows = profile_summary(groups['cprofile'], root)
        for label, index in (('Self', 4), ('Cumulative', 5)):
            out += [f'## cProfile: {label}', '', 'Shares are medians of each function’s share of its own profiled run total. Cumulative shares overlap and cannot be summed.', '', '| Function | Calls median | Self s | Cumulative s | Self share | Cumulative share |', '| --- | ---: | ---: | ---: | ---: | ---: |']
            for name, calls, self_s, cum_s, self_share, cum_share in sorted(rows, key=lambda r: (-r[index], r[0]))[:40]:
                out.append(f'| {name} | {fmt(calls)} | {fmt(self_s)} | {fmt(cum_s)} | {self_share:.2%} | {cum_share:.2%} |')
            out.append('')
    return '\n'.join(out) + '\n', stages


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    root = args.manifest.resolve().parent
    groups = defaultdict(lambda: defaultdict(list))
    seen_tasks, seen_targets = set(), set()
    for trial in manifest['trials']:
        if trial.get('warmup', False):
            continue
        if trial.get('returncode', 0) != 0:
            raise ValueError('refusing to rank a failed trial')
        if manifest.get('source') == 'source':
            if trial.get('task_state') != 'succeeded' or not trial.get('task_id') or not trial.get('target_prompt_id'):
                raise ValueError('refusing trial without a successful matched task and target receipt')
            if trial['task_id'] in seen_tasks or (trial.get('fixture_id'), trial['target_prompt_id']) in seen_targets:
                raise ValueError('reused task or target receipt')
            seen_tasks.add(trial['task_id']); seen_targets.add((trial.get('fixture_id'), trial['target_prompt_id']))
            start, admission, ack, end = (trial[k] for k in ('spawn_ns', 'admission_ns', 'target_ack_ns', 'exit_ns'))
            if not (start <= admission and start <= ack and start <= end):
                raise ValueError('invalid trial event ordering')
        wall = float(trial['wall_seconds'])
        if not math.isfinite(wall) or wall <= 0:
            raise ValueError('invalid wall_seconds')
        groups[trial['route']][trial['mode']].append(trial)
    args.output.mkdir(parents=True, exist_ok=True)
    for route, modes in sorted(groups.items()):
        if route not in ('W', 'I', 'E'):
            raise ValueError(f'invalid route: {route}')
        report, stages = render(route, modes, root)
        (args.output / f'attribution-{route}.md').write_text(report)
        (args.output / f'stages-{route}.json').write_text(json.dumps(stages, indent=2, sort_keys=True) + '\n')


if __name__ == '__main__':
    main()
