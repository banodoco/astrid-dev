#!/usr/bin/env python3
"""Interleave isolated fixture runs under the shared timing lock."""
import argparse
import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
TEMPLATE = Path('ready_templates/image/qwen_image_2_1_turbo.py')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

@contextlib.contextmanager
def timing_lock(nonblocking=False):
    with open('/tmp/astrid-timing.lock', 'a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | (fcntl.LOCK_NB if nonblocking else 0))
        yield

@contextlib.contextmanager
def target(args, out):
    directory = out / 'target'
    directory.mkdir()
    command = [sys.executable, str(HERE / 'target.py'), '--agent', str(args.before_agent.resolve()),
               '--runtime', '/root/codex/plan-81m/a4-runtime', '--vibe', str(args.before_vibe.resolve()),
               '--directory', str(directory)]
    with (directory / 'stdout').open('wb') as stdout, (directory / 'stderr').open('wb') as stderr:
        process = None
        try:
            with timing_lock():
                process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr)
                deadline = time.monotonic() + 60
                ready = directory / 'ready.json'
                while not ready.exists():
                    if process.poll() is not None or time.monotonic() >= deadline:
                        raise RuntimeError('shared target did not start; see target stderr')
                    time.sleep(.05)
                info = json.loads(ready.read_text())
            yield info, directory / 'receipts.jsonl'
        finally:
            if process is not None:
                with timing_lock():
                    process.stdin.close()
                    try:
                        code = process.wait(timeout=30)
                    except subprocess.TimeoutExpired:
                        process.terminate()
                        process.wait(timeout=30)
                        raise RuntimeError('shared target failed to stop')
                    if code:
                        raise RuntimeError('shared target failed; see target stderr')

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('output', type=Path, help='new output directory')
    p.add_argument('--before-only', action='store_true', help='run only the before arm')
    for arm in ('before', 'after'):
        p.add_argument('--' + arm + '-agent', type=Path, required=arm == 'before')
        p.add_argument('--' + arm + '-sha', required=arm == 'before')
        p.add_argument('--' + arm + '-vibe', type=Path)
        p.add_argument('--' + arm + '-vibe-sha')
    p.add_argument('--trials', type=int, default=5)
    p.add_argument('--routes', nargs='+', choices=('W', 'I', 'E'), default=['W', 'I', 'E'])
    args = p.parse_args()
    if args.before_only:
        if any(getattr(args, 'after_' + name) is not None for name in ('agent', 'sha', 'vibe', 'vibe_sha')):
            p.error('--before-only does not accept after-arm arguments')
    elif args.after_agent is None or args.after_sha is None:
        p.error('--after-agent and --after-sha are required unless --before-only is set')
    for arm in ('before', 'after'):
        if getattr(args, arm + '_vibe') is None:
            setattr(args, arm + '_vibe', Path('/root/codex/plan-81m/VibeComfy'))
        if getattr(args, arm + '_vibe_sha') is None:
            setattr(args, arm + '_vibe_sha', '799d90f619a6723d0b376b7e77aef09c244a0821')
    if args.trials < 1:
        p.error('trials must be positive')
    if not args.before_only and args.before_agent.resolve() == args.after_agent.resolve():
        p.error('arms require distinct Agent worktrees')
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    with target(args, out) as (target_info, receipts):
        identity = {'python': str(Path(sys.executable).resolve()), 'python_sha256': digest(Path(sys.executable).resolve()),
                    'console_sha256': digest(HERE / 'astrid'), 'target': target_info,
                    'template_sha256': digest(args.before_vibe.resolve() / TEMPLATE)}
        if not args.before_only and digest(args.after_vibe.resolve() / TEMPLATE) != identity['template_sha256']:
            raise RuntimeError('VibeComfy template bytes differ')
        journal = {'identity': identity, 'schedule': [], 'lock': '/tmp/astrid-timing.lock',
                   'note': 'The target endpoint is shared; Runtime is isolated per arm. Warmup and drain occur outside measured intervals.'}
        def save():
            (out / 'comparison.json').write_text(json.dumps(journal, indent=2) + '\n')
        save()
        seen_tasks, seen_prompts = set(), set()
        for route in args.routes:
            for mode in ('plain', 'timings'):
                for trial in range(1, args.trials + 1):
                    arms = ('before',) if args.before_only else (('before', 'after') if trial % 2 else ('after', 'before'))
                    for arm in arms:
                        agent = getattr(args, arm + '_agent').resolve()
                        vibe = getattr(args, arm + '_vibe').resolve()
                        if (digest(Path(sys.executable).resolve()) != identity['python_sha256'] or
                            digest(HERE / 'astrid') != identity['console_sha256'] or
                            digest(vibe / TEMPLATE) != identity['template_sha256']):
                            raise RuntimeError('interpreter, console or template changed during comparison')
                        label = f'{route}-{mode}-{trial:02d}-{arm}'
                        cmd = [sys.executable, str(HERE / 'runner.py'), '--agent', str(agent),
                               '--agent-sha', getattr(args, arm + '_sha'), '--vibe', str(vibe),
                               '--vibe-sha', getattr(args, arm + '_vibe_sha'), str(out / label),
                               '--trials', '1', '--routes', route, '--modes', mode,
                               '--target-url', target_info['url'], '--target-receipts', str(receipts)]
                        row = {'route': route, 'mode': mode, 'trial': trial, 'arm': arm, 'directory': label,
                               'command': cmd}
                        journal['schedule'].append(row)
                        save()
                        wait_start = time.monotonic()
                        if args.before_only:
                            row['load_wait'] = {'threshold': 1.0, 'timeout_seconds': 600, 'observations': []}
                        while True:
                            if args.before_only and time.monotonic() - wait_start >= 600:
                                row['load_wait']['status'] = 'busy'
                                row['load_wait']['elapsed_seconds'] = time.monotonic() - wait_start
                                save()
                                raise RuntimeError(f'{label} host busy for 10 minutes; no sample taken')
                            try:
                                lock = timing_lock(nonblocking=args.before_only)
                                lock.__enter__()
                            except BlockingIOError:
                                time.sleep(min(1, max(0, 600 - (time.monotonic() - wait_start))))
                                continue
                            try:
                                load = os.getloadavg()
                                elapsed = time.monotonic() - wait_start
                                if args.before_only:
                                    row['load_wait']['observations'].append({'elapsed_seconds': elapsed, 'load': load})
                                    save()
                                if args.before_only and elapsed >= 600:
                                    row['load_wait']['status'] = 'busy'
                                    save()
                                    raise RuntimeError(f'{label} host busy for 10 minutes; no sample taken')
                                if not args.before_only or load[0] < 1.0:
                                    if args.before_only:
                                        row['load_wait']['status'] = 'ready'
                                    row['load_before'] = load
                                    save()
                                    with (out / (label + '.runner.stdout')).open('wb') as stdout, (out / (label + '.runner.stderr')).open('wb') as stderr:
                                        result = subprocess.run(cmd, stdout=stdout, stderr=stderr)
                                    row['returncode'] = result.returncode
                                    row['load_after'] = os.getloadavg()
                                    break
                            finally:
                                lock.__exit__(None, None, None)
                            time.sleep(min(1, max(0, 600 - (time.monotonic() - wait_start))))
                        save()
                        if result.returncode:
                            raise RuntimeError(f'{label} failed; raw output retained')
                        manifest = json.loads((out / label / 'manifest.json').read_text())
                        for sample in manifest['trials']:
                            task, prompt = sample['task_id'], sample['target_prompt_id']
                            if task in seen_tasks or prompt in seen_prompts:
                                raise RuntimeError('repeated task or target receipt across fixtures')
                            seen_tasks.add(task)
                            seen_prompts.add(prompt)
                        inventory_hash = digest(out / label / 'target-inventory.json')
                        row['target_inventory_sha256'] = inventory_hash
                        if inventory_hash != target_info['inventory_sha256']:
                            save()
                            raise RuntimeError('fixture inventory differs from shared target')
                        if 'target_inventory_sha256' not in identity:
                            identity['target_inventory_sha256'] = inventory_hash
                        elif identity['target_inventory_sha256'] != inventory_hash:
                            save()
                            raise RuntimeError('target inventory differs across fixtures')
                        save()
        journal['complete'] = True
        save()

if __name__ == '__main__':
    main()
