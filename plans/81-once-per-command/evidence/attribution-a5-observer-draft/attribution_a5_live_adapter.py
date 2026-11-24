"""Unqualified observation primitives for an eventual A-5 fixture.

Nothing here starts a fixture, establishes a policy, or asserts complete coverage.
Install only around a real operation in the process being observed.  Each event
is tagged with the caller-supplied trial/attempt and actual PID; unassociated
work is explicitly labelled, never silently assigned to an attempt.
"""
from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from functools import wraps
import json
import os
from pathlib import Path
import threading
import time

_attempt = ContextVar('a5_attempt', default=None)


class EventSink:
    """Exclusive, append-only per-process sink; deletion or replacement fails."""
    def __init__(self, path, *, trial, process_role):
        self.path = Path(path)
        self.trial = trial
        self.process_role = process_role
        self.lock = threading.Lock()
        self.fd = os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_APPEND, 0o600)
        self.identity = os.fstat(self.fd).st_dev, os.fstat(self.fd).st_ino
        self.sequence = 0
        self.emit('observer_start')

    def emit(self, kind, **fields):
        with self.lock:
            try:
                st = self.path.stat()
                if (st.st_dev, st.st_ino) != self.identity or st.st_nlink != 1:
                    raise RuntimeError('A5 observation sink replaced or unlinked')
                self.sequence += 1
                row = dict(kind=kind, trial=self.trial, attempt=_attempt.get(),
                           process_role=self.process_role, pid=os.getpid(),
                           sequence=self.sequence, monotonic_ns=time.monotonic_ns(), **fields)
                data = (json.dumps(row, sort_keys=True) + '\n').encode()
                if os.write(self.fd, data) != len(data):
                    raise RuntimeError('short A5 observation write')
            except Exception as exc:
                raise RuntimeError('A5 observation failed') from exc

    def close(self):
        try:
            self.emit('observer_end')
        finally:
            os.close(self.fd)


class ObserverHealth:
    """Non-throwing product-path reporting; the harness must check health."""
    def __init__(self, sink):
        self.sink = sink
        self.failed = False

    def emit(self, kind, **fields):
        if self.failed:
            return
        try:
            self.sink.emit(kind, **fields)
        except BaseException:
            # Do not affect a native call or leak a just-created child. The
            # harness must treat this flag or a missing end marker as invalid.
            self.failed = True

    def assert_healthy(self):
        if self.failed:
            raise RuntimeError('A5 observer failed; observations are invalid')


@contextmanager
def attempt_scope(attempt_id):
    if not attempt_id:
        raise ValueError('attempt identity must be observed, not inferred')
    token = _attempt.set(attempt_id)
    try:
        yield
    finally:
        _attempt.reset(token)


@contextmanager
def observe_yaml(sink):
    """Count outermost calls through yaml.safe_load/load in this process."""
    import yaml
    health = ObserverHealth(sink)
    health.emit('coverage', api='yaml.safe_load/yaml.load', status='partial')
    depth = ContextVar('a5_yaml_depth', default=0)
    originals = {name: getattr(yaml, name) for name in ('safe_load', 'load')}
    def wrap(name, original):
        @wraps(original)
        def observed(*args, **kwargs):
            nesting = depth.get()
            token = depth.set(nesting + 1)
            try:
                if nesting == 0:
                    health.emit('yaml_load', api='yaml.' + name)
                return original(*args, **kwargs)
            finally:
                depth.reset(token)
        return observed
    for name, original in originals.items():
        setattr(yaml, name, wrap(name, original))
    try:
        yield health
    finally:
        for name, original in originals.items():
            setattr(yaml, name, original)


@contextmanager
def observe_launcher(sink):
    """Observe attempts to invoke the actual autobootstrap launcher boundary.

    This records entry, not successful subprocess creation. A failing launch is
    distinguished and must not be treated as a confirmed subprocess start.
    """
    from astrid.sdk import autobootstrap
    original = autobootstrap._invoke_launcher
    health = ObserverHealth(sink)
    @wraps(original)
    def observed(command, *, action, allowed_statuses):
        health.emit('launcher_invoke', action=action)
        try:
            result = original(command, action=action, allowed_statuses=allowed_statuses)
        except BaseException:
            health.emit('launcher_error', action=action)
            raise
        health.emit('launcher_return', action=action)
        return result
    autobootstrap._invoke_launcher = observed
    try:
        yield health
    finally:
        autobootstrap._invoke_launcher = original


def observe_discovery_rows(sink, rows):
    """Record exclusive collector occurrences; require the caller's raw rows."""
    for index, row in enumerate(rows):
        if row.get('stage') == 'pack discovery':
            sink.emit('discovery_occurrence', row_index=index)
