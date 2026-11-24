"""Validate one closed A-5 observer stream; this does not establish coverage.

The caller must obtain the file identity at sink creation and the process and
attempt identities independently. A valid stream is only a record of events
that reached the sink, not evidence that all operations were observed.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

_OPERATION_KINDS = frozenset({
    'yaml_load', 'launcher_invoke', 'launcher_error', 'launcher_return',
    'launcher_start', 'hash_call', 'discovery_occurrence', 'cache_file_witness',
})
_KINDS = _OPERATION_KINDS | {'observer_start', 'observer_end', 'coverage'}


def read_event_stream(path, *, identity, trial, process_role, pid, attempts):
    """Read a closed stream after checking its independently retained identity.

    ``identity`` is the (device, inode) from the sink's creation, not a stat
    performed at read time. ``attempts`` contains actual fixture-observed
    attempt identities. This function neither infers zeros nor validates
    observer health, API coverage, receipt matching, or count budgets.
    """
    if (not isinstance(identity, tuple) or len(identity) != 2
            or any(type(v) is not int or v < 0 for v in identity)):
        raise ValueError('invalid retained sink identity')
    if any(not isinstance(v, str) or not v for v in (trial, process_role)):
        raise ValueError('invalid trial or process role')
    if type(pid) is not int or pid <= 0:
        raise ValueError('invalid process identity')
    if not isinstance(attempts, (set, frozenset)) or any(
        not isinstance(v, str) or not v for v in attempts
    ):
        raise ValueError('invalid attempt identities')
    path = Path(path)
    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
        with os.fdopen(fd, 'rb') as stream:
            before = os.fstat(stream.fileno())
            if (before.st_dev, before.st_ino) != identity or before.st_nlink != 1:
                raise ValueError('sink replaced or unlinked')
            data = stream.read()
            after = os.fstat(stream.fileno())
            current = path.stat()
            if ((after.st_dev, after.st_ino) != identity or after.st_nlink != 1
                    or (current.st_dev, current.st_ino) != identity or current.st_nlink != 1
                    or before.st_size != after.st_size):
                raise ValueError('sink changed during read')
    except OSError as exc:
        raise ValueError('sink unavailable') from exc
    if not data or not data.endswith(b'\n'):
        raise ValueError('missing or truncated stream')
    rows = []
    previous = -1
    for sequence, line in enumerate(data.splitlines(), 1):
        try:
            row = json.loads(line)
        except (ValueError, UnicodeDecodeError) as exc:
            raise ValueError('malformed event') from exc
        if not isinstance(row, dict):
            raise ValueError('invalid event')
        kind = row.get('kind')
        if not isinstance(kind, str) or kind not in _KINDS:
            raise ValueError('unknown event kind')
        if (row.get('trial') != trial or row.get('process_role') != process_role
                or type(row.get('pid')) is not int or row['pid'] != pid
                or type(row.get('sequence')) is not int or row['sequence'] != sequence):
            raise ValueError('event identity or sequence mismatch')
        stamp = row.get('monotonic_ns')
        if type(stamp) is not int or stamp < 0 or stamp < previous:
            raise ValueError('invalid event clock')
        previous = stamp
        if 'attempt' not in row:
            raise ValueError('missing event attempt')
        attempt = row['attempt']
        if kind in _OPERATION_KINDS:
            if not isinstance(attempt, str) or attempt not in attempts:
                raise ValueError('unknown operation attempt')
        elif attempt is not None and (not isinstance(attempt, str) or attempt not in attempts):
            raise ValueError('unknown event attempt')
        rows.append(row)
    if (len(rows) < 2 or rows[0]['kind'] != 'observer_start'
            or rows[-1]['kind'] != 'observer_end'
            or any(row['kind'] in {'observer_start', 'observer_end'} for row in rows[1:-1])):
        raise ValueError('invalid observer lifecycle')
    return rows
