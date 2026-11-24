"""Partial cache-witness observations; not a whole-process count gate.

Install before consumer/provider imports in each independently identified process
and actual attempt context. The caller must independently pin and validate the
witness source and its branch semantics, process inventory, stream and health.
These patches are process-global and require exclusive ownership. Context-local
scope does not propagate to threads or children. No paths or contents are logged.
OS bytes read (including partial failed reads) remain unknown.
"""
from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from functools import wraps
import hashlib
from pathlib import Path
import sys

from tests.integrations.attribution_a5_live_adapter import ObserverHealth


@contextmanager
def observe_cache_file_witness(generation, sink):
    """Observe this module's witness calls under its verified implementation.

    The consumer and provider bind the function at import, so installation
    fails if either is already imported. Earlier unknown aliases and other
    processes remain unobserved; the fixture must establish their absence.
    """
    aliases = ('vibecomfy.porting.object_info.consume', 'vibecomfy.schema.provider')
    if any(name in sys.modules for name in aliases):
        raise RuntimeError('install witness observer before consumer and provider imports')
    original_witness = generation.cache_file_witness
    original_read = Path.read_bytes
    original_sha = hashlib.sha256
    health = ObserverHealth(sink)
    scope = ContextVar('a5_witness_scope', default=None)

    @wraps(original_read)
    def read(path, *args, **kwargs):
        state = scope.get()
        if state is None:
            return original_read(path, *args, **kwargs)
        state['reads'] += 1
        try:
            data = original_read(path, *args, **kwargs)
        except BaseException:
            state['read_failed'] = True
            raise
        if type(data) is not bytes or state['reads'] != 1:
            health.failed = True
        else:
            state['buffer'] = data
        return data

    @wraps(original_sha)
    def sha(*args, **kwargs):
        state = scope.get()
        if state is not None:
            state['sha_calls'] += 1
            if (state['sha_calls'] != 1 or len(args) != 1 or kwargs
                    or state['buffer'] is None or args[0] is not state['buffer']):
                health.failed = True
            else:
                state['digest_bytes'] = len(state['buffer'])
        return original_sha(*args, **kwargs)

    @wraps(original_witness)
    def witness(*args, **kwargs):
        if scope.get() is not None:
            health.failed = True
            return original_witness(*args, **kwargs)
        state = {'reads': 0, 'read_failed': False, 'buffer': None,
                 'sha_calls': 0, 'digest_bytes': 0}
        token = scope.set(state)
        try:
            result = original_witness(*args, **kwargs)
        except BaseException:
            health.failed = True
            raise
        else:
            return result
        finally:
            scope.reset(token)
            if (state['reads'] > 1 or state['sha_calls'] > 1
                    or (state['buffer'] is not None and state['sha_calls'] != 1)
                    or (state['read_failed'] and state['sha_calls'])):
                health.failed = True
            health.emit('cache_file_witness', digest_input_bytes=state['digest_bytes'],
                        os_read_bytes=None)

    generation.cache_file_witness = witness
    Path.read_bytes = read
    hashlib.sha256 = sha
    try:
        yield health
    finally:
        for name in aliases:
            module = sys.modules.get(name)
            if module is not None:
                if getattr(module, 'cache_file_witness', None) is witness:
                    module.cache_file_witness = original_witness
                else:
                    health.failed = True
        hashlib.sha256 = original_sha
        Path.read_bytes = original_read
        generation.cache_file_witness = original_witness
