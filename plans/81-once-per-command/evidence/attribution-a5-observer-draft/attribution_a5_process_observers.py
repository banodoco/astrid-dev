"""Partial in-process A-5 probes; these are not a count gate.

Install before the observed code obtains aliases. Instrumentation errors invalidate observations and are not zero counts. See attribution_a5_process_observers_notes.md.
"""
from contextlib import contextmanager
from contextvars import ContextVar
from functools import wraps
import hashlib
import subprocess

from tests.integrations.attribution_a5_live_adapter import ObserverHealth


@contextmanager
def observe_launcher_starts(sink):
    """Observe successful Popen creation within autobootstrap invocation.

    Global patching requires exclusive ownership of both patched attributes.
    The context variable confines attribution to the invoking thread/context.
    """
    from astrid.sdk import autobootstrap
    original_invoke = autobootstrap._invoke_launcher
    original_init = subprocess.Popen.__init__
    action_context = ContextVar('a5_launcher_action', default=None)
    health = ObserverHealth(sink)
    health.emit('coverage', api='autobootstrap._invoke_launcher/subprocess.Popen.__init__',
              status='partial', detail='this process and invoking context only')

    @wraps(original_init)
    def observed_init(process, *args, **kwargs):
        original_init(process, *args, **kwargs)
        action = action_context.get()
        if action is not None:
            health.emit('launcher_start', action=action, child_pid=process.pid)

    @wraps(original_invoke)
    def observed_invoke(command, *, action, allowed_statuses):
        token = action_context.set(action)
        try:
            return original_invoke(command, action=action, allowed_statuses=allowed_statuses)
        finally:
            action_context.reset(token)

    subprocess.Popen.__init__ = observed_init
    autobootstrap._invoke_launcher = observed_invoke
    try:
        yield health
    finally:
        autobootstrap._invoke_launcher = original_invoke
        subprocess.Popen.__init__ = original_init


def _known_initial_bytes(args, kwargs):
    # Avoid arbitrary buffer conversion, attribute access, or calling user code.
    # Successful sha256 constructors use at most one positional data argument.
    if args:
        value = args[0]
    elif 'string' in kwargs:
        value = kwargs['string']
    else:
        return 0
    if type(value) in (bytes, bytearray):
        return len(value)
    if type(value) is memoryview:
        return value.nbytes
    return None


@contextmanager
def observe_hashlib(sink):
    """Observe successful hashlib.sha256/file_digest calls, retaining native objects.

    Per-call byte values are only the initial sha256 constructor buffer; native
    hash-object updates and file_digest stream bytes remain explicitly unknown.
    """
    original_sha256 = hashlib.sha256
    original_file_digest = hashlib.file_digest
    health = ObserverHealth(sink)
    health.emit('coverage', api='hashlib.sha256', status='partial',
              detail='constructor input only; native update and copy bytes unknown')
    health.emit('coverage', api='hashlib.file_digest', status='partial',
              detail='successful calls only; algorithm and bytes can be unknown')

    @wraps(original_sha256)
    def observed_sha256(*args, **kwargs):
        result = original_sha256(*args, **kwargs)
        try:
            initial_bytes = _known_initial_bytes(args, kwargs)
        except BaseException:
            health.failed = True
            initial_bytes = None
        health.emit('hash_call', api='hashlib.sha256', algorithm='sha256',
                  initial_bytes=initial_bytes,
                  update_bytes=None)
        return result

    @wraps(original_file_digest)
    def observed_file_digest(*args, **kwargs):
        result = original_file_digest(*args, **kwargs)
        # Do not introspect the returned object or stream: user-defined digest
        # factories and streams can have side effects or raise on access.
        health.emit('hash_call', api='hashlib.file_digest', algorithm=None,
                  initial_bytes=None, update_bytes=None)
        return result

    hashlib.sha256 = observed_sha256
    hashlib.file_digest = observed_file_digest
    try:
        yield health
    finally:
        hashlib.sha256 = original_sha256
        hashlib.file_digest = original_file_digest
