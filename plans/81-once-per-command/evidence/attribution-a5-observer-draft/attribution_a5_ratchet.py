"""Compare count baselines; independent fixture and oracle validation remains required."""
from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping

GROUPS = frozenset({'same', 'changed', 'image_same', 'image_changed', 'image_entry'})
METRICS = frozenset({'hash_calls', 'hash_bytes', 'yaml_loads', 'discovery_occurrences', 'launcher_starts'})
PREFLIGHTS = frozenset({'SDK admission preflight', 'Remote admission preflight', 'Workspace admission preflight'})


def baseline_digest(baseline):
    """Fingerprint exact structured baseline contents, without trusting candidate metadata."""
    raw = json.dumps(baseline, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()


def _integer(value, label):
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f'{label}: expected nonnegative integer')
    return value


def _evidence(mapping, key, label):
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{label}: missing evidence reference')


def _validate(baseline):
    if not isinstance(baseline, Mapping) or type(baseline.get('version')) is not int or baseline['version'] != 1:
        raise ValueError('unsupported baseline version')
    groups = baseline.get('groups')
    if not isinstance(groups, Mapping) or not GROUPS.issubset(groups):
        raise ValueError('missing required groups')
    for group, cases in groups.items():
        if not isinstance(group, str) or not group.strip() or not isinstance(cases, Mapping) or not cases:
            raise ValueError('invalid group or empty cases')
        for case, policy in cases.items():
            if not isinstance(case, str) or not case.strip() or not isinstance(policy, Mapping):
                raise ValueError(f'{group}: invalid case')
            metrics, stages, preflights = (policy.get(key) for key in ('metrics', 'stages', 'preflights'))
            if not isinstance(metrics, Mapping) or not METRICS.issubset(metrics):
                raise ValueError(f'{group}/{case}: missing mandatory metrics')
            for metric, bounds in metrics.items():
                if not isinstance(metric, str) or not metric.strip() or not isinstance(bounds, Mapping):
                    raise ValueError(f'{group}/{case}: invalid metric')
                lower = _integer(bounds.get('min'), f'{metric} minimum')
                upper = _integer(bounds.get('max'), f'{metric} maximum')
                if lower > upper:
                    raise ValueError(f'{metric}: minimum exceeds maximum')
            if not isinstance(stages, Mapping) or not stages:
                raise ValueError(f'{group}/{case}: missing positive stages')
            for stage, count in stages.items():
                if not isinstance(stage, str) or not stage.strip() or _integer(count, 'stage minimum') == 0:
                    raise ValueError(f'{group}/{case}: invalid stage minimum')
            if not isinstance(preflights, Mapping) or set(preflights) != PREFLIGHTS:
                raise ValueError(f'{group}/{case}: missing preflight dispositions')
            for stage, disposition in preflights.items():
                if not isinstance(disposition, Mapping) or type(disposition.get('required')) is not bool:
                    raise ValueError(f'{stage}: invalid disposition')
                _evidence(disposition, 'evidence', stage)
                if disposition['required'] != (stage in stages):
                    raise ValueError(f'{stage}: disposition conflicts with required stages')
    return groups


def compare_baseline(prior, candidate, *, pinned_prior_digest, introductions, minimum_changes):
    """Reject dropped work and raised count limits against the separately pinned prior.

    introductions maps (group, None), (group, case), or
    (group, case, 'metrics'|'stages', name) to evidence references. Each
    introduced item needs its own reference, including children of new groups.
    minimum_changes maps (group, case, 'metrics'|'stages', name) to evidence
    references. References require independent verification by the calling gate;
    their presence here alone does not establish an actual operation or oracle.
    """
    if not isinstance(pinned_prior_digest, str) or baseline_digest(prior) != pinned_prior_digest:
        raise ValueError('prior baseline does not match pinned digest')
    if not isinstance(introductions, Mapping) or not isinstance(minimum_changes, Mapping):
        raise ValueError('introduction and minimum change evidence must be mappings')
    old_groups, new_groups = _validate(prior), _validate(candidate)
    if set(old_groups) - set(new_groups):
        raise ValueError('baseline groups removed')
    for group, cases in new_groups.items():
        if group not in old_groups:
            _evidence(introductions, (group, None), f'{group} introduction')
        old_cases = old_groups.get(group, {})
        if set(old_cases) - set(cases):
            raise ValueError(f'{group}: baseline cases removed')
        for case, policy in cases.items():
            if case not in old_cases:
                _evidence(introductions, (group, case), f'{group}/{case} introduction')
            old = old_cases.get(case)
            for field in ('metrics', 'stages'):
                prior_items = old[field] if old is not None else {}
                for name in set(policy[field]) - set(prior_items):
                    _evidence(introductions, (group, case, field, name),
                              f'{group}/{case}: {field} {name} introduction')
            if old is None:
                continue
            for field in ('metrics', 'stages'):
                if set(old[field]) - set(policy[field]):
                    raise ValueError(f'{group}/{case}: {field} removed')
            for name, bounds in old['metrics'].items():
                new = policy['metrics'][name]
                if new['max'] > bounds['max']:
                    raise ValueError(f'{group}/{case}: {name} maximum increased')
                if bounds['min'] > 0 and new['min'] == 0:
                    raise ValueError(f'{group}/{case}: {name} positive minimum removed')
                if new['min'] != bounds['min']:
                    _evidence(minimum_changes, (group, case, 'metrics', name), f'{name} minimum change')
            for name, minimum in old['stages'].items():
                if policy['stages'][name] != minimum:
                    _evidence(minimum_changes, (group, case, 'stages', name), f'{name} minimum change')
            for name, disposition in old['preflights'].items():
                if disposition['required'] and not policy['preflights'][name]['required']:
                    raise ValueError(f'{group}/{case}: required {name} removed')
