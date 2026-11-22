#!/usr/bin/env python3
"""One shared fixture ComfyUI endpoint for the before/after harness arms."""
import argparse
import hashlib
import http.server
import json
import os
from pathlib import Path
import sys
import threading
import time
sys.dont_write_bytecode = True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--agent', type=Path, required=True)
    parser.add_argument('--runtime', type=Path, required=True)
    parser.add_argument('--vibe', type=Path, required=True)
    parser.add_argument('--directory', type=Path, required=True)
    args = parser.parse_args()
    agent, runtime, vibe = (p.resolve() for p in (args.agent, args.runtime, args.vibe))
    directory = args.directory.resolve()
    directory.mkdir(parents=True, exist_ok=True)
    sys.path[:0] = list(map(str, (agent, runtime, vibe)))

    from tests.integrations.test_runpod_slot_path_cpu import SlotPod, _slot_classes
    from tests.integrations._pinned_source import attached_comfy
    from tests.integrations.runpod_slot_pod import receipt_files
    from astrid.core.generation import entries

    provider = SlotPod(directory / 'claim.json', directory / 'attempts', _slot_classes(('image', 't2i')))
    files = [path for engine in dict.fromkeys(('comfyui', *entries.runpod_engines()))
             for path in receipt_files(provider._receipt_for(engine))]
    provider.comfy.installed_files = lambda: files
    inventory = directory / 'target-inventory.json'
    inventory_bytes = (json.dumps(provider.comfy.object_info(), sort_keys=True, indent=2) + '\n').encode()
    inventory.write_bytes(inventory_bytes)
    events = directory / 'receipts.jsonl'
    events.touch(exist_ok=True)
    event_lock = threading.Lock()

    original_submit = provider.comfy.submit
    original_handle = http.server.BaseHTTPRequestHandler.handle_one_request
    pending = threading.local()

    def submit(body):
        status, payload = original_submit(body)
        if status == 200:
            pending.receipt = {'prompt_id': payload['prompt_id'], 'body': body}
        return status, payload

    def handle_one_request(handler):
        pending.receipt = None
        result = original_handle(handler)
        receipt = getattr(pending, 'receipt', None)
        if (getattr(handler, 'command', None) == 'POST' and
                getattr(handler, 'path', None) == '/prompt' and receipt is not None):
            row = {'time_ns': time.monotonic_ns(), 'prompt_id': receipt['prompt_id'],
                   'body': receipt['body']}
            line = (json.dumps(row, sort_keys=True) + '\n').encode()
            with event_lock:
                fd = os.open(events, os.O_WRONLY | os.O_APPEND)
                try:
                    os.write(fd, line)
                    os.fsync(fd)
                finally:
                    os.close(fd)
        return result

    provider.comfy.submit = submit
    http.server.BaseHTTPRequestHandler.handle_one_request = handle_one_request
    try:
        with attached_comfy(provider.comfy) as endpoint:
            ready = {'url': endpoint, 'inventory_file': inventory.name,
                     'inventory_sha256': hashlib.sha256(inventory_bytes).hexdigest(),
                     'receipts_file': events.name, 'agent': str(agent), 'runtime': str(runtime),
                     'vibe': str(vibe)}
            temporary_ready = directory / 'ready.pending'
            temporary_ready.write_text(json.dumps(ready, sort_keys=True, indent=2) + '\n')
            temporary_ready.replace(directory / 'ready.json')
            sys.stdout.write(json.dumps(ready, sort_keys=True) + '\n')
            sys.stdout.flush()
            # The driver owns the pipe and signals drain by closing its stdin.
            sys.stdin.buffer.read()
    finally:
        provider.comfy.submit = original_submit
        http.server.BaseHTTPRequestHandler.handle_one_request = original_handle


if __name__ == '__main__':
    main()
