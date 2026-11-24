"""Summarize partial A-5 observations, never complete counts or budget results.

The caller must first validate stream integrity and independently correlate each
process and attempt with the actual fixture. The observers cover only parts of
those processes; absent events do not establish zero work, and these lower bounds
cannot be used to enforce an upper budget. Native hash update and file-digest
bytes remain unknown even when no hash event appears.
"""
from __future__ import annotations

from collections.abc import Mapping

_BASE = frozenset({'kind', 'trial', 'attempt', 'process_role', 'pid', 'sequence', 'monotonic_ns'})
_FIELDS = {
    'observer_start': frozenset(), 'observer_end': frozenset(),
    'coverage': frozenset({'api', 'status', 'detail'}),
    'yaml_load': frozenset({'api'}),
    'discovery_occurrence': frozenset({'row_index'}),
    'launcher_start': frozenset({'action', 'child_pid'}),
    'launcher_invoke': frozenset({'action'}),
    'launcher_return': frozenset({'action'}),
    'launcher_error': frozenset({'action'}),
    'hash_call': frozenset({'api', 'algorithm', 'initial_bytes', 'update_bytes'}),
}
_METRICS = {'hash_call': 'hash_calls', 'yaml_load': 'yaml_loads',
            'discovery_occurrence': 'discovery_occurrences', 'launcher_start': 'launcher_starts'}


def _nonnegative_integer(value):
    return type(value) is int and value >= 0


def observed_lower_bounds(rows):
    """Return observed event lower bounds keyed by (role, PID, actual attempt).

    Only keys with an observed operation are returned; absence is not a zero.
    Each record's hash_bytes is always None. This function does not validate
    stream lifecycle, prove coverage, verify identity, or apply a budget.
    """
    if not isinstance(rows, (list, tuple)):
        raise ValueError('expected validated event rows')
    result = {}
    discoveries = set()
    for row in rows:
        if not isinstance(row, Mapping):
            raise ValueError('invalid event')
        kind = row.get('kind')
        if kind not in _FIELDS or not _BASE.issubset(row) or set(row) - (_BASE | _FIELDS[kind]):
            raise ValueError('unknown or malformed event')
        role, pid, attempt = row['process_role'], row['pid'], row['attempt']
        if not isinstance(role, str) or not role or type(pid) is not int or pid <= 0:
            raise ValueError('invalid process identity')
        if kind not in _METRICS:
            continue
        if not isinstance(attempt, str) or not attempt:
            raise ValueError('unattributed operation')
        if kind == 'hash_call':
            if row.get('api') not in ('hashlib.sha256', 'hashlib.file_digest'):
                raise ValueError('unknown hash API')
            if (row['api'] == 'hashlib.sha256' and
                    (row.get('algorithm') != 'sha256' or row.get('update_bytes') is not None)):
                raise ValueError('invalid sha256 observation')
            if (row['api'] == 'hashlib.file_digest' and
                    any(row.get(field) is not None for field in ('algorithm', 'initial_bytes', 'update_bytes'))):
                raise ValueError('invalid file digest observation')
            if any(value is not None and not _nonnegative_integer(value)
                   for value in (row.get('initial_bytes'), row.get('update_bytes'))):
                raise ValueError('invalid hash bytes')
            if not {'api', 'algorithm', 'initial_bytes', 'update_bytes'}.issubset(row):
                raise ValueError('missing hash data')
        elif kind == 'yaml_load':
            if row.get('api') not in ('yaml.load', 'yaml.safe_load'):
                raise ValueError('unknown YAML API')
        elif kind == 'discovery_occurrence':
            index = row.get('row_index')
            if not _nonnegative_integer(index) or (role, pid, index) in discoveries:
                raise ValueError('invalid or duplicate discovery row')
            discoveries.add((role, pid, index))
        elif kind == 'launcher_start':
            if type(row.get('child_pid')) is not int or row['child_pid'] <= 0:
                raise ValueError('invalid launcher child PID')
            if not isinstance(row.get('action'), str) or not row['action']:
                raise ValueError('invalid launcher action')
        key = (role, pid, attempt)
        if key not in result:
            result[key] = {'hash_bytes': None}
        metric = _METRICS[kind]
        result[key][metric] = result[key].get(metric, 0) + 1
    return result
