#!/usr/bin/env python3
"""CPU attached-target attribution. Run via run.sh; see README."""
import argparse
import contextlib
import json
import importlib.metadata
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import time

ROOT = Path('/root/codex/plan-81m')
AGENT, RUNTIME, VIBE = ROOT / 'a4-agent', ROOT / 'a4-runtime', ROOT / 'VibeComfy'
os.environ['ASTRID_RUNTIME_CHECKOUT'] = str(RUNTIME)
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
sys.path[:0] = [str(AGENT), str(RUNTIME), str(VIBE)]
import pytest
from tests.helpers.runtime import new_runtime_daemon
from tests.integrations.runpod_slot_pod import PodComfy
from tests.integrations import test_runpod_slot_path_cpu as fixture
_drive = fixture._drive


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output', type=Path)
    parser.add_argument('--trials', type=int, default=5)
    parser.add_argument('--modes', nargs='+', default=['plain', 'timings', 'importtime', 'cprofile'], choices=['plain', 'timings', 'importtime', 'cprofile'])
    args = parser.parse_args()
    if args.trials < 1:
        parser.error('trials must be positive')
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    manifest = {'source': 'source', 'python': sys.version, 'executable': sys.executable,
                'platform': platform.platform(), 'cpu_count': os.cpu_count(), 'cpu': next((line.partition(':')[2].strip() for line in Path('/proc/cpuinfo').read_text().splitlines() if line.startswith('model name')), 'unknown'), 'load': os.getloadavg(),
                'packages': sorted(f"{d.metadata['Name']}=={d.version}" for d in importlib.metadata.distributions() if d.metadata.get('Name')),
                'revisions': {}, 'seed': 12345, 'sampler': 'not collected', 'trials': []}
    for label, path in [('agent', AGENT), ('runtime', RUNTIME), ('vibecomfy', VIBE)]:
        manifest['revisions'][label] = subprocess.check_output(['git', '-C', str(path), 'rev-parse', 'HEAD'], text=True).strip()
        if subprocess.check_output(['git', '-C', str(path), 'status', '--porcelain'], text=True).strip():
            raise RuntimeError(f'{label} checkout is dirty')
    expected = {'agent':'315b8b7a9336ec3147b399f6bf6f168011d09b27', 'runtime':'182311f9d363712c0339254bd27e091d0e18318d', 'vibecomfy':'799d90f619a6723d0b376b7e77aef09c244a0821'}
    if manifest['revisions'] != expected:
        raise RuntimeError('source pins do not match')
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    monkeypatch = pytest.MonkeyPatch()
    daemon_holder = {}
    admissions, acknowledgements = [], []
    original_submit = PodComfy.submit
    def submit(self, body):
        status, payload = original_submit(self, body)
        if status == 200:
            acknowledgements.append((time.monotonic_ns(), payload['prompt_id'], body))
        return status, payload
    monkeypatch.setattr(PodComfy, 'submit', submit)
    with tempfile.TemporaryDirectory(prefix='a4-fixture-') as scratch:
        scratch = Path(scratch)
        connection = scratch / 'connection.json'
        def runtime():
            support = scratch / 'support'; support.mkdir(mode=0o700)
            daemon = new_runtime_daemon(scratch / 'realm', support_root=support).start()
            daemon_holder['daemon'] = daemon
            original = daemon.service.create_task
            def create(*a, **kw):
                value = original(*a, **kw)
                admissions.append((time.monotonic_ns(), value))
                return value
            daemon.service.create_task = create
            connection.write_text(json.dumps({'endpoint': daemon.endpoint, 'credential_file': str(daemon.credential_path), 'realm_id': daemon.service.realm['id'], 'actor_id': 'owner'}))
            return daemon
        def call(_facade, controls, _tmp):
            env = {key: os.environ[key] for key in ('PATH', 'LANG', 'LC_ALL', 'SSL_CERT_FILE') if key in os.environ}
            env.update(HOME=str(scratch), TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1', ASTRID_RUNTIME_CHECKOUT=str(RUNTIME), ASTRID_PREPARED_CONNECTION=str(connection), PYTHONPATH=os.pathsep.join(map(str, (AGENT, RUNTIME, VIBE))))
            client = controls['client']
            seen = set()
            for route in ('W', 'I', 'E'):
                for mode in args.modes:
                    for n in range(-1, args.trials):
                        label = f'{route}-{mode}-' + ('warmup' if n == -1 else str(n + 1))
                        prompt = f'A red cube on a white tabletop. {label}'
                        base = ['generate'] + (['workflow', str(VIBE / 'ready_templates/image/qwen_image_2_1_turbo.py'), '--prompt', prompt] if route == 'W' else ['image', prompt])
                        if route == 'E': base += ['--entry', 'qwen-image-2.1-turbo']
                        base += ['--placement', controls['placement'], '--project', controls['project'], '--seed', '12345', '--no-wait', '--json']
                        if mode == 'timings': base += ['--timings']
                        profile = out / f'{label}.prof'
                        launch = [sys.executable] + (['-X', 'importtime'] if mode == 'importtime' else [])
                        code = 'from astrid.console import main; raise SystemExit(main())'
                        if mode == 'cprofile':
                            code = 'import cProfile; from astrid.console import main; p=cProfile.Profile();\ntry: result=p.runcall(main)\nfinally: p.dump_stats(' + repr(str(profile)) + ')\nraise SystemExit(result)'
                        launch += ['-c', code, *base]
                        before_a, before_p = len(admissions), len(acknowledgements)
                        start = time.monotonic_ns()
                        proc = subprocess.run(launch, env=env, capture_output=True, timeout=240)
                        end = time.monotonic_ns()
                        def redact(data):
                            for value in (controls['placement'], daemon_holder['daemon'].endpoint, str(scratch)):
                                data = data.replace(value.encode(), b'<local-redacted>')
                            return data
                        (out / f'{label}.stdout').write_bytes(redact(proc.stdout))
                        (out / f'{label}.stderr').write_bytes(redact(proc.stderr))
                        row = {'route': route, 'mode': mode, 'warmup': n == -1, 'trial': n + 1, 'returncode': proc.returncode, 'spawn_ns': start, 'exit_ns': end, 'wall_seconds': (end-start)/1e9, 'stdout': f'{label}.stdout', 'stderr': f'{label}.stderr', 'profile': profile.name if mode == 'cprofile' else None, 'load': os.getloadavg(), 'prompt': prompt, 'argv': [part.replace(controls['placement'], '<target>').replace(str(scratch), '<scratch>') for part in launch]}
                        manifest['trials'].append(row)
                        (out / 'manifest.json').write_text(json.dumps(manifest, indent=2, default=str) + '\n')
                        if proc.returncode: raise RuntimeError(f'{label}: command failed; see retained output')
                        payload = json.loads(proc.stdout)
                        task = payload.get('kernel_task_id') or payload.get('task_id')
                        if not task or task in seen: raise RuntimeError(f'{label}: missing or repeated task')
                        seen.add(task)
                        deadline = time.monotonic() + 120
                        while time.monotonic() < deadline:
                            result = client.tasks.show(task)
                            if result.ok and result.data.get('state') in ('succeeded', 'failed', 'cancelled'):
                                break
                            time.sleep(.05)
                        if not result.ok or result.data.get('state') != 'succeeded': raise RuntimeError(f'{label}: task did not succeed')
                        matches = [(ts, value) for ts, value in admissions[before_a:] if task in json.dumps(value, default=str)]
                        acks = acknowledgements[before_p:]
                        if len(matches) != 1 or len(acks) != 1 or prompt not in json.dumps(acks[0][2]): raise RuntimeError(f'{label}: admission or target acknowledgement mismatch')
                        row.update(task_id=task, admission_ns=matches[0][0], target_ack_ns=acks[0][0], target_prompt_id=acks[0][1], task_state='succeeded')
                        (out / f'{label}.target.json').write_text(json.dumps(acks[0][2], indent=2) + '\n')
                        (out / 'manifest.json').write_text(json.dumps(manifest, indent=2, default=str) + '\n')
                        print(label, 'ok', flush=True)
        try:
            # The upstream fixture otherwise closes the target before host shutdown.
            with contextlib.ExitStack() as target_lifetime:
                original_target = fixture._attached_comfy
                @contextlib.contextmanager
                def keep_target(*a, **kw):
                    yield target_lifetime.enter_context(original_target(*a, **kw))
                monkeypatch.setattr(fixture, '_attached_comfy', keep_target)
                with _drive(('image', 't2i'), scratch, monkeypatch, runtime, scratch, call=call, target_kind='attached'):
                    pass
        finally:
            monkeypatch.undo()

if __name__ == '__main__': main()
