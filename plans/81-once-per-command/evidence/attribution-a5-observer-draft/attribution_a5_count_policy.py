"""Unwired A-5 deterministic count policy preparation; not a live gate.

Policies and observations must come from independently measured, approved
fixture runs. Elapsed seconds are not count budgets. This module intentionally
provides no baseline values and makes no claim about instrumentation coverage.
"""
from __future__ import annotations

from collections.abc import Mapping

METRICS = frozenset({"hash_calls", "hash_bytes", "yaml_loads",
                     "discovery_occurrences", "launcher_starts"})
GROUPS = frozenset({"same", "changed", "image_same", "image_changed", "image_entry"})


def _integer(value, label):
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{label}: expected nonnegative integer")
    return value


def check_counts(group, sample, policy):
    """Check an observed process against its exact route/attempt policy.

    sample: {attempt_count: int, counts: {metric: int}}. The fixture supplies
    these from the real instrumented operation boundaries and verifies attempt
    and receipt identities independently. policy is a versioned mapping with
    ``groups[group][str(attempt_count)][metric]`` equal to an approved
    ``{min: int, max: int, rationale: nonempty str}``. No interpolation or
    per-attempt averaging is allowed; an unmeasured attempt count fails closed.
    A zero lower bound needs a rationale explaining why that operation is absent
    for this route and attempt count. Receipt, request, stage and residual checks
    are separate requirements; this function does not prove them.
    """
    if group not in GROUPS or not isinstance(sample, Mapping):
        raise ValueError("unknown group or invalid sample")
    if not isinstance(policy, Mapping) or policy.get('version') != 1 or isinstance(policy.get('version'), bool):
        raise ValueError("missing or unsupported count policy version")
    attempts = _integer(sample.get('attempt_count'), 'attempt_count')
    if attempts == 0:
        raise ValueError(f"{group}: at least one attempt is required")
    groups = policy.get('groups')
    if not isinstance(groups, Mapping) or not isinstance(groups.get(group), Mapping):
        raise ValueError(f"{group}: no approved count policy")
    limits = groups[group].get(str(attempts))
    counts = sample.get('counts')
    if not isinstance(limits, Mapping) or set(limits) != METRICS:
        raise ValueError(f"{group}: missing exact count policy for {attempts} attempts")
    if not isinstance(counts, Mapping) or set(counts) != METRICS:
        raise ValueError(f"{group}: missing or unexpected observed counts")
    for metric in sorted(METRICS):
        observed = _integer(counts[metric], f"{group} {metric}")
        limit = limits[metric]
        if not isinstance(limit, Mapping):
            raise ValueError(f"{group} {metric}: invalid policy")
        lower = _integer(limit.get('min'), f"{group} {metric} minimum")
        upper = _integer(limit.get('max'), f"{group} {metric} maximum")
        rationale = limit.get('rationale')
        if lower > upper or not isinstance(rationale, str) or not rationale.strip():
            raise ValueError(f"{group} {metric}: invalid policy range or rationale")
        if not lower <= observed <= upper:
            raise ValueError(f"{group} {metric}: observed {observed}, expected {lower}..{upper} for {attempts} attempts")
    return dict(counts)
