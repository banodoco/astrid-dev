"""Run with PYTHONPATH=. from either extracted revision; compare the inner pair."""
import contextvars, shutil, tempfile, threading
from pathlib import Path
from unittest.mock import patch
from vibecomfy import workflow_bundle as bundle
from vibecomfy.porting.object_info import consume as reader
from vibecomfy.workflow import VibeWorkflow, WorkflowSource

with tempfile.TemporaryDirectory() as folder:
    root = Path(folder)
    reader.CACHE_DIR = shutil.copytree(reader.CACHE_DIR, root / 'cache')
    index = reader.CACHE_DIR / 'index.json'
    wf = VibeWorkflow('sample', WorkflowSource('sample'))
    wf.add_node('ImageResizeKJ', uid='one')
    reader.reset_cache()
    inner, outer = [root / name / 'workflow.py' for name in ('inner', 'outer')]
    reached, finished = threading.Event(), threading.Event()
    old_read, old_lookup, old_journal = Path.read_bytes, reader._resolve_class_type, bundle._write_publish_transaction
    count, worker, swapped = 0, None, False
    def read(path):
        global swapped
        value = old_read(path)
        if threading.current_thread() is worker and count == 30 and path == index and not swapped:
            index.write_text('[]')
            swapped = True
        return value
    def lookup(name):
        global count
        if threading.current_thread() is not worker:
            return old_lookup(name)
        count += 1
        try:
            return old_lookup(name)
        finally:
            if count == 30:
                reached.set()
                assert finished.wait(15)
    def inner_emit():
        try:
            bundle.emit_bundle(wf, inner, {})
            print('inner published')
        except Exception as e:
            print('inner refused', type(e).__name__, str(e).replace(folder, '<tmp>'))
        finally:
            reached.set()
    def journal(path, record):
        global worker
        old_journal(path, record)
        if path == outer and record['state'] == 'prepared' and worker is None:
            worker = threading.Thread(target=contextvars.copy_context().run, args=(inner_emit,))
            worker.start()
            assert reached.wait(15)
    with patch.object(Path,'read_bytes',read), patch.object(reader,'_resolve_class_type',lookup), patch.object(bundle,'_write_publish_transaction',journal):
        try:
            bundle.emit_bundle(wf, outer, {})
        finally:
            finished.set()
            if worker: worker.join(15)
    assert swapped and index.read_text() == '[]'
    print('inner members', inner.exists(), inner.with_suffix('.vibe.json').exists())
