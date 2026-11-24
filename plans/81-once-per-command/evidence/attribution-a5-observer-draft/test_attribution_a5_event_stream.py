"""Synthetic integrity checks only; these do not prove operational coverage."""
from __future__ import annotations

import json

import pytest

from tests.integrations.attribution_a5_event_stream import read_event_stream


def _row(kind, sequence, *, attempt=None):
    return {'kind': kind, 'sequence': sequence, 'trial': 'trial-1',
            'process_role': 'controller', 'pid': 123, 'attempt': attempt,
            'monotonic_ns': sequence}


def _write(path, rows, *, newline=True):
    raw = '\n'.join(json.dumps(row) for row in rows)
    path.write_text(raw + ('\n' if newline else ''), encoding='utf-8')
    stat = path.stat()
    return stat.st_dev, stat.st_ino


def _read(path, identity):
    return read_event_stream(path, identity=identity, trial='trial-1',
                             process_role='controller', pid=123, attempts={'attempt-1'})


def _rows():
    return [_row('observer_start', 1), _row('coverage', 2),
            _row('hash_call', 3, attempt='attempt-1'), _row('observer_end', 4)]


def test_valid_stream_returns_raw_rows(tmp_path):
    path = tmp_path / 'events'
    rows = _rows()
    rows[2].update(initial_bytes=None, update_bytes=None)
    identity = _write(path, rows)
    assert _read(path, identity) == rows


@pytest.mark.parametrize('damage', ['truncated', 'missing_end', 'sequence', 'attempt',
                                    'pid', 'role', 'trial', 'duplicate_start',
                                    'clock', 'kind', 'malformed'])
def test_invalid_stream_rejected(tmp_path, damage):
    path = tmp_path / 'events'
    rows = _rows()
    if damage == 'missing_end':
        rows.pop()
    elif damage == 'sequence':
        rows[2]['sequence'] = 4
    elif damage == 'attempt':
        rows[2]['attempt'] = 'unknown'
    elif damage == 'pid':
        rows[2]['pid'] = 124
    elif damage == 'role':
        rows[2]['process_role'] = 'worker'
    elif damage == 'trial':
        rows[2]['trial'] = 'other'
    elif damage == 'duplicate_start':
        rows[2]['kind'] = 'observer_start'
    elif damage == 'clock':
        rows[2]['monotonic_ns'] = 0
    elif damage == 'kind':
        rows[2]['kind'] = 'unrecognised'
    identity = _write(path, rows, newline=damage != 'truncated')
    if damage == 'malformed':
        path.write_text('{bad json}\n', encoding='utf-8')
    with pytest.raises(ValueError):
        _read(path, identity)


def test_missing_or_replaced_sink_rejected(tmp_path):
    path = tmp_path / 'events'
    identity = _write(path, _rows())
    replacement = tmp_path / 'replacement'
    _write(replacement, _rows())
    path.unlink()
    with pytest.raises(ValueError):
        _read(path, identity)
    replacement.rename(path)
    with pytest.raises(ValueError):
        _read(path, identity)
