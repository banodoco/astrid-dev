"""Synthetic partial-observation checks, not fixture or coverage evidence."""
import pytest

from tests.integrations.attribution_a5_observed_counts import observed_lower_bounds


def event(kind, *, role='controller', pid=1, attempt='attempt-1', **fields):
    return dict(kind=kind, trial='trial', attempt=attempt, process_role=role,
                pid=pid, sequence=1, monotonic_ns=1, **fields)


def test_keeps_attempts_and_processes_separate_and_bytes_unknown():
    rows = [
        event('hash_call', api='hashlib.sha256', algorithm='sha256', initial_bytes=3, update_bytes=None),
        event('yaml_load', api='yaml.safe_load', attempt='attempt-2'),
        event('launcher_start', action='up', child_pid=44, role='worker', pid=2),
    ]
    counts = observed_lower_bounds(rows)
    assert counts[('controller', 1, 'attempt-1')]['hash_calls'] == 1
    assert counts[('controller', 1, 'attempt-1')]['hash_bytes'] is None
    assert 'yaml_loads' not in counts[('controller', 1, 'attempt-1')]
    assert counts[('controller', 1, 'attempt-2')]['yaml_loads'] == 1
    assert counts[('worker', 2, 'attempt-1')]['launcher_starts'] == 1


def test_absent_or_bypassed_events_are_not_zero_totals():
    rows = [event('coverage', attempt=None, api='hashlib.sha256', status='partial'),
            event('launcher_invoke', action='up'), event('launcher_return', action='up')]
    assert observed_lower_bounds(rows) == {}
    assert observed_lower_bounds([]) == {}


def test_duplicate_discovery_and_invalid_launcher_fail():
    discovery = event('discovery_occurrence', row_index=0)
    with pytest.raises(ValueError, match='duplicate discovery'):
        observed_lower_bounds([discovery, discovery])
    with pytest.raises(ValueError, match='child PID'):
        observed_lower_bounds([event('launcher_start', action='up', child_pid=0)])


def test_unknown_fields_and_unattributed_operation_fail():
    with pytest.raises(ValueError, match='malformed'):
        observed_lower_bounds([event('yaml_load', api='yaml.load', extra=1)])
    with pytest.raises(ValueError, match='unattributed'):
        observed_lower_bounds([event('yaml_load', api='yaml.load', attempt=None)])


@pytest.mark.parametrize('fields', [
    {'api': 'hashlib.sha256', 'algorithm': None, 'initial_bytes': 0, 'update_bytes': None},
    {'api': 'hashlib.sha256', 'algorithm': 'sha256', 'initial_bytes': 0, 'update_bytes': 1},
    {'api': 'hashlib.file_digest', 'algorithm': None, 'initial_bytes': 1, 'update_bytes': None},
    {'api': 'hashlib.file_digest', 'algorithm': 'sha256', 'initial_bytes': None, 'update_bytes': None},
])
def test_inconsistent_hash_observation_fails(fields):
    with pytest.raises(ValueError, match='invalid'):
        observed_lower_bounds([event('hash_call', **fields)])
