"""Fresh-interpreter witness checks; not full coverage or budget evidence."""
from __future__ import annotations

import subprocess
import sys
import textwrap

import pytest


_CASE = textwrap.dedent('''
    import hashlib
    import importlib
    import os
    from pathlib import Path
    import sys
    from types import SimpleNamespace

    from tests.integrations.attribution_a5_live_adapter import attempt_scope, EventSink
    from tests.integrations.attribution_a5_witness_observer import observe_cache_file_witness
    from tests.integrations.attribution_a5_event_stream import read_event_stream

    generation = importlib.import_module('vibecomfy.porting.object_info.generation')
    case, root = sys.argv[1], Path(sys.argv[2])
    path = root / 'witness'

    class Sink:
        def __init__(self): self.rows = []
        def emit(self, kind, **fields): self.rows.append((kind, fields))

    class Broken:
        def emit(self, *args, **kwargs): raise OSError('sink broken')

    def unhealthy(health):
        try: health.assert_healthy()
        except RuntimeError: return
        raise AssertionError('observer health did not fail')

    if case == 'branches':
        path.write_bytes(b'hello')
        before = generation.cache_file_witness(path)
        original_sha, original_read = hashlib.sha256, Path.read_bytes
        original_witness = generation.cache_file_witness
        sink = Sink()
        with observe_cache_file_witness(generation, sink) as health:
            with attempt_scope('actual-attempt'):
                assert generation.cache_file_witness(path) == before
                assert generation.cache_file_witness(root / 'missing') is None
                assert generation.cache_file_witness(root)[-1] is None
            health.assert_healthy()
        assert sink.rows == [('cache_file_witness', {'digest_input_bytes': size, 'os_read_bytes': None})
                             for size in (5, 0, 0)]
        assert hashlib.sha256 is original_sha and Path.read_bytes is original_read
        assert generation.cache_file_witness is original_witness
    elif case == 'read_error':
        path.write_bytes(b'hello')
        def fail(_self): raise OSError('read failed')
        Path.read_bytes = fail
        sink = Sink()
        with observe_cache_file_witness(generation, sink) as health:
            result = generation.cache_file_witness(path)
            health.assert_healthy()
        assert result[-1] is None
        assert sink.rows == [('cache_file_witness', {'digest_input_bytes': 0, 'os_read_bytes': None})]
    elif case == 'alias':
        original = generation.cache_file_witness
        with observe_cache_file_witness(generation, Sink()) as health:
            consume = importlib.import_module('vibecomfy.porting.object_info.consume')
            assert consume.cache_file_witness is generation.cache_file_witness
            health.assert_healthy()
        assert consume.cache_file_witness is original
        health.assert_healthy()
        try:
            with observe_cache_file_witness(generation, Sink()): pass
        except RuntimeError: pass
        else: raise AssertionError('prebound consumer alias accepted')
    elif case == 'unexpected_sha':
        def unexpected(_path): return hashlib.sha256(b'not observed read').hexdigest()
        fake = SimpleNamespace(cache_file_witness=unexpected)
        expected = unexpected(None)
        with observe_cache_file_witness(fake, Sink()) as health:
            assert fake.cache_file_witness(None) == expected
            unhealthy(health)
    elif case == 'exception':
        def raises(_path): raise LookupError('product error')
        fake = SimpleNamespace(cache_file_witness=raises)
        with observe_cache_file_witness(fake, Broken()) as health:
            try: fake.cache_file_witness(None)
            except LookupError as exc: assert str(exc) == 'product error'
            else: raise AssertionError('product exception lost')
            unhealthy(health)
    elif case == 'sink_failure':
        path.write_bytes(b'hello')
        expected = generation.cache_file_witness(path)
        with observe_cache_file_witness(generation, Broken()) as health:
            assert generation.cache_file_witness(path) == expected
            unhealthy(health)
    elif case == 'stream':
        path = root / 'events'
        sink = EventSink(path, trial='trial', process_role='worker')
        identity = sink.identity
        with attempt_scope('attempt'):
            sink.emit('cache_file_witness', digest_input_bytes=3, os_read_bytes=None)
        sink.close()
        rows = read_event_stream(path, identity=identity, trial='trial', process_role='worker',
                                 pid=os.getpid(), attempts={'attempt'})
        assert rows[1]['digest_input_bytes'] == 3
        try:
            read_event_stream(path, identity=identity, trial='trial', process_role='worker',
                              pid=os.getpid(), attempts={'another'})
        except ValueError: pass
        else: raise AssertionError('unmatched attempt accepted')
    else:
        raise AssertionError(case)
''')


@pytest.mark.parametrize('case', ['branches', 'read_error', 'alias', 'unexpected_sha',
                                  'exception', 'sink_failure', 'stream'])
def test_witness_observation_in_fresh_process(case, tmp_path):
    subprocess.run([sys.executable, '-c', _CASE, case, str(tmp_path)], check=True)
