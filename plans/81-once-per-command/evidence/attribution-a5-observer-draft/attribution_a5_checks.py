"""Preparation for the A-5 sibling gate; not a substitute for its live fixture.

Inputs are per-process observations, never group medians. The fixture must
provide attempt-correlated receipts, separate controller/worker counts, and
monotonic timestamps from the same host clock. See attribution_a5_preparation.md.
"""
from __future__ import annotations

import math
from collections import Counter

GROUPS = ("same", "changed", "image_same", "image_changed", "image_entry")
PREFLIGHT_STAGES = frozenset({"SDK admission preflight", "Remote admission preflight",
                              "Workspace admission preflight"})
REMAINDER = "other command work"


def _number(value, label, *, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{label} must be finite")
    if value < 0 or (positive and value == 0):
        raise ValueError(f"{label} must be {'positive' if positive else 'nonnegative'}")
    return value


def check_sample(group, sample, *, clock_tolerance_seconds, stage_policy):
    """Validate one successful process and return its independent partition.

    stage_policy maps group, then the string form of attempt_count, to an
    object containing required_counts and preflights. Each of the three actual
    preflight names needs a disposition {required: bool, reason: nonempty str};
    required ones must appear in required_counts with a positive minimum. The
    caller must derive this policy from real route/attempt traces and verify it
    independently. A declaration that a preflight does not apply is not proof.
    Upper count ratchets are separate from this coverage helper.
    """
    if group not in GROUPS:
        raise ValueError(f"unknown group {group!r}")
    tol = _number(clock_tolerance_seconds, "clock tolerance")
    if sample.get("ok") is not True:
        raise ValueError(f"{group}: process did not succeed")
    wall = _number(sample.get("wall_seconds"), "wall", positive=True)
    span = _number(sample.get("collector_span_seconds"), "collector span")
    rows = sample.get("timings")
    if not isinstance(rows, list):
        raise ValueError(f"{group}: missing occurrence rows")
    names = Counter()
    ids = set()
    remainder = []
    named = []
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("stage"), str) or not row['stage']:
            raise ValueError(f"{group}: invalid timing row")
        seconds = _number(row.get("seconds"), f"{group}: {row['stage']} seconds")
        if row['stage'] == REMAINDER:
            if 'occurrence_id' in row:
                raise ValueError(f"{group}: remainder must not be an occurrence")
            remainder.append(seconds)
            continue
        occurrence = row.get('occurrence_id')
        if isinstance(occurrence, bool) or not isinstance(occurrence, int) or occurrence <= 0 or occurrence in ids:
            raise ValueError(f"{group}: missing or duplicate occurrence identity")
        ids.add(occurrence)
        names[row['stage']] += 1
        named.append(seconds)
    if len(remainder) != 1:
        raise ValueError(f"{group}: expected exactly one remainder")
    attempts = sample.get("attempt_count")
    if isinstance(attempts, bool) or not isinstance(attempts, int) or attempts <= 0:
        raise ValueError(f"{group}: missing positive attempt count")
    if not isinstance(stage_policy, dict) or not isinstance(stage_policy.get(group), dict):
        raise ValueError(f"{group}: missing route stage policy")
    policy = stage_policy[group].get(str(attempts))
    if not isinstance(policy, dict):
        raise ValueError(f"{group}: missing stage policy for {attempts} attempts")
    required_counts = policy.get("required_counts")
    preflights = policy.get("preflights")
    if not isinstance(required_counts, dict) or not required_counts:
        raise ValueError(f"{group}: missing required count policy")
    if not isinstance(preflights, dict) or set(preflights) != PREFLIGHT_STAGES:
        raise ValueError(f"{group}: missing preflight dispositions")
    for name, disposition in preflights.items():
        if (not isinstance(disposition, dict) or not isinstance(disposition.get("required"), bool)
                or not isinstance(disposition.get("reason"), str) or not disposition["reason"].strip()):
            raise ValueError(f"{group}: invalid {name} disposition")
        if disposition["required"] != (name in required_counts):
            raise ValueError(f"{group}: {name} disposition and required counts disagree")
    for name, minimum in required_counts.items():
        if not isinstance(name, str) or not name or isinstance(minimum, bool) or not isinstance(minimum, int) or minimum <= 0:
            raise ValueError(f"{group}: invalid required count policy")
        if names[name] < minimum:
            raise ValueError(f"{group}: {name} count {names[name]} below {minimum}")
        if any(row['stage'] == name and row['seconds'] <= 0 for row in rows):
            raise ValueError(f"{group}: {name} has no positive work")
    total = math.fsum(named)
    residual = remainder[0]
    if abs(total + residual - span) > tol:
        raise ValueError(f"{group}: exclusive rows and remainder do not partition collector span")
    if span > wall + tol or total > wall + tol:
        raise ValueError(f"{group}: collector or named work exceeds parent wall")
    gap = wall - span
    uncovered = wall - total
    if uncovered > 0.10 * wall + tol:
        raise ValueError(f"{group}: uncovered {uncovered:.6f}s exceeds 10% of wall; remainder {residual:.6f}s, wall minus collector {gap:.6f}s")
    return {'wall_seconds': wall, 'named_seconds': total, 'remainder_seconds': residual,
            'collector_span_seconds': span, 'wall_minus_collector_seconds': gap,
            'uncovered_share': uncovered / wall, 'stage_counts': dict(names)}


def check_receipts(groups):
    """Validate five attempt-matched receipts per group and completed drains.

    All timestamps are absolute monotonic readings from the same host clock;
    target acknowledgement and CLI exit may occur in either order.
    """
    if set(groups) != set(GROUPS):
        raise ValueError('all five generation groups are required')
    task_ids, target_ids, attempts = set(), set(), set()
    for group, samples in groups.items():
        if len(samples) != 5:
            raise ValueError(f"{group}: expected five processes")
        for sample in samples:
            attempt, task, target = (sample.get(k) for k in ('attempt_id', 'task_id', 'target_prompt_id'))
            if any(not isinstance(x, str) or not x for x in (attempt, task, target)):
                raise ValueError(f"{group}: missing attempt or receipt")
            if attempt in attempts or task in task_ids or target in target_ids:
                raise ValueError(f"{group}: receipts and attempts must be distinct")
            attempts.add(attempt); task_ids.add(task); target_ids.add(target)
            if sample.get('target_attempt_id') != attempt or sample.get('task_attempt_id') != attempt:
                raise ValueError(f"{group}: unmatched task and target receipts")
            if sample.get('drained') is not True:
                raise ValueError(f"{group}: trial was not drained")
            spawn, admission, ack, exit_at, drained = (_number(sample.get(k), k) for k in
                ('spawn_monotonic', 'admission_monotonic', 'target_ack_monotonic', 'exit_monotonic', 'drained_monotonic'))
            if min(admission, ack, exit_at) < spawn or drained < max(admission, ack, exit_at):
                raise ValueError(f"{group}: invalid boundary ordering")
