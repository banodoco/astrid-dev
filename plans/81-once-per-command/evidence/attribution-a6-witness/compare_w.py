#!/root/codex/plan-81m/attribution-evidence.env/bin/python
"""Run the W fixture with one shared target and two pinned Vibe checkouts."""
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
import prepare_envs

HERE = Path(__file__).resolve().parent
ROOT = Path('/root/codex/plan-81m')
AGENT = ROOT / 'attribution-a3'
AGENT_SHA = '72bc29d88e0c1a605842a9f9407e5ca4dbfcb17a'
PYTHON = ROOT / 'attribution-evidence.env/bin/python'
A2_CONSOLE = ROOT / 'run/a2-console/astrid'
BASE_VIBE_SHA = '48b5fa9e45630e1bc502651975ec0ef3a5e74c4c'
TEMPLATE = Path('ready_templates/image/qwen_image_2_1_turbo.py')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def pin(path, expected):
    if len(expected) != 40 or any(c not in '0123456789abcdef' for c in expected):
        raise ValueError('pin must be a full lowercase SHA')
    sha = subprocess.check_output(['git', '-C', str(path), 'rev-parse', 'HEAD'], text=True).strip()
    dirty = subprocess.check_output(['git', '-C', str(path), 'status', '--porcelain'], text=True).strip()
    if sha != expected or dirty:
        raise RuntimeError(f'pin or clean state mismatch: {path}')

def validate_environments(before_python, after_python, before, after):
    pythons = {'before': before_python.absolute(), 'after': after_python.absolute()}
    roots = {arm: python.parent.parent for arm, python in pythons.items()}
    if roots['before'] == roots['after'] or roots['before'].parent != roots['after'].parent:
        raise RuntimeError('arm environments must be distinct siblings')
    report_path = roots['before'].parent / 'environment-identity.json'
    report = json.loads(report_path.read_text())
    site = Path(report['site_packages_relative'])
    if site.is_absolute() or '..' in site.parts:
        raise RuntimeError('invalid site-packages path')
    pth = site / 'attribution-source.pth'
    base = Path(report['base'])
    if report['source_prefix'] != [str(AGENT), str(ROOT / 'a4-runtime')]:
        raise RuntimeError('environment source prefix mismatch')
    base_pth = (base / pth).read_text().splitlines()
    if len(base_pth) != 3:
        raise RuntimeError('base source path shape changed')
    inventories = {}
    for arm, source in (('before', before), ('after', after)):
        root, python = roots[arm], pythons[arm]
        record = report['arms'][arm]
        if (str(root) != record['environment'] or str(python) != record['python']
                or str(source) != record['source'] or python != root / 'bin/python'):
            raise RuntimeError(f'{arm} environment identity mismatch')
        arm_pth = root / pth
        if arm_pth.read_text().splitlines() != report['source_prefix'] + [str(source)]:
            raise RuntimeError(f'{arm} source path mismatch')
        if prepare_envs.sha(arm_pth) != record['source_pth_sha256']:
            raise RuntimeError(f'{arm} source path changed')
        if (prepare_envs.sha(python.resolve(strict=True)) != record['python_binary_sha256']
                or prepare_envs.sha(python.resolve(strict=True)) != prepare_envs.sha((base / 'bin/python').resolve(strict=True))):
            raise RuntimeError(f'{arm} interpreter binary mismatch')
        inventories[arm] = prepare_envs.inventory(root, pth.as_posix())
        if inventories[arm] != report['tree_excluding_source_pth']:
            raise RuntimeError(f'{arm} environment files changed')
        if prepare_envs.distributions(python, root / site) != report['installed_distributions']:
            raise RuntimeError(f'{arm} package metadata changed')
    if inventories['before'] != inventories['after']:
        raise RuntimeError('arm environments differ beyond source path')
    return {'report': str(report_path), 'sha256': prepare_envs.sha(report_path)}

@contextlib.contextmanager
def attestation_hook(python, report_path, destination):
    report = json.loads(Path(report_path).read_text())
    site = python.absolute().parent.parent / report['site_packages_relative']
    paths = [site / 'host_attest.py', site / 'sitecustomize.py']
    created = []
    try:
        entry = f'import host_attest; host_attest.install({str(destination)!r})\n'.encode()
        for path, data in zip(paths, ((HERE / 'host_attest.py').read_bytes(), entry)):
            with path.open('xb') as stream:
                created.append(path)
                stream.write(data)
        yield
    finally:
        for path in reversed(created):
            path.unlink()

@contextlib.contextmanager
def timing_lock(*, quiet=False):
    """Cooperative lock; quiet samples require load1 < 1 while holding it."""
    deadline = time.monotonic() + 600
    with open('/tmp/astrid-timing.lock', 'a') as lock:
        while True:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                pass
            else:
                load = os.getloadavg()
                if not quiet or load[0] < 1:
                    try:
                        yield load
                    finally:
                        fcntl.flock(lock, fcntl.LOCK_UN)
                    return
                fcntl.flock(lock, fcntl.LOCK_UN)
            if time.monotonic() >= deadline:
                raise TimeoutError('timing lock or load1 < 1 unavailable within 600 seconds')
            time.sleep(min(1, max(0, deadline - time.monotonic())))

@contextlib.contextmanager
def target(out, vibe):
    directory = out / 'target'
    directory.mkdir()
    cmd = [sys.executable, str(HERE / 'target.py'), '--agent', str(AGENT),
           '--runtime', str(ROOT / 'a4-runtime'), '--vibe', str(vibe), '--directory', str(directory)]
    with (directory / 'stdout').open('wb') as stdout, (directory / 'stderr').open('wb') as stderr:
        with timing_lock():
            proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr)
            deadline = time.monotonic() + 60
            ready = directory / 'ready.json'
            while not ready.exists():
                if proc.poll() is not None or time.monotonic() >= deadline:
                    if proc.poll() is None:
                        proc.terminate()
                        proc.wait(timeout=30)
                    raise RuntimeError('shared target did not start; see target stderr')
                time.sleep(.05)
        try:
            yield json.loads(ready.read_text()), directory / 'receipts.jsonl'
        finally:
            def stop():
                proc.stdin.close()
                try:
                    code = proc.wait(timeout=30)
                except subprocess.TimeoutExpired:
                    proc.terminate()
                    try:
                        proc.wait(timeout=30)
                    except subprocess.TimeoutExpired:
                        proc.kill()
                        proc.wait()
                    raise RuntimeError('shared target failed to stop cleanly')
                if code:
                    raise RuntimeError('shared target failed; see target stderr')
            try:
                with timing_lock():
                    stop()
            except TimeoutError:
                # Do not leave the target running even if another holder blocks teardown.
                stop()
                raise

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('output', type=Path, help='new output directory')
    p.add_argument('--before-vibe', type=Path, default=ROOT / 'witness-vibe-base')
    p.add_argument('--before-sha', default=BASE_VIBE_SHA)
    p.add_argument('--after-vibe', type=Path, required=True)
    p.add_argument('--after-sha', required=True)
    p.add_argument('--before-python', type=Path, required=True)
    p.add_argument('--after-python', type=Path, required=True)
    args = p.parse_args()
    before, after = args.before_vibe.resolve(), args.after_vibe.resolve()
    if before == after:
        p.error('before and after Vibe checkouts must be distinct')
    if Path(sys.executable).resolve() != PYTHON.resolve():
        p.error('invoke using the fixed A-2 interpreter')
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    pin(AGENT, AGENT_SHA)
    pin(ROOT / 'a4-runtime', '182311f9d363712c0339254bd27e091d0e18318d')
    pin(before, args.before_sha)
    pin(after, args.after_sha)
    environments = validate_environments(args.before_python, args.after_python, before, after)
    console_hash = digest(A2_CONSOLE)
    if digest(HERE / 'astrid') != console_hash:
        raise RuntimeError('console shim differs from A-2')
    template_hash = digest(before / TEMPLATE)
    if digest(after / TEMPLATE) != template_hash:
        raise RuntimeError('workflow template bytes differ')
    identity = {'agent': str(AGENT), 'agent_sha': AGENT_SHA, 'python': str(PYTHON),
                'python_sha256': digest(PYTHON.resolve()), 'console_sha256': console_hash,
                'template_sha256': template_hash, 'observer_sha256': digest(HERE / 'hash_probe.py'),
                'script_sha256': {name: digest(HERE / name) for name in ('compare_w.py', 'runner.py', 'target.py', 'summarize.py', 'prepare_envs.py', 'host_attest.py')},
                'before_vibe': str(before), 'before_sha': args.before_sha,
                'after_vibe': str(after), 'after_sha': args.after_sha,
                'environments': environments,
                'before_python': str(args.before_python.absolute()),
                'after_python': str(args.after_python.absolute())}
    journal = {'identity': identity, 'schedule': [], 'lock': '/tmp/astrid-timing.lock',
               'interpretation': 'Three paired plain W observations and one separately instrumented CLI per arm; no statistical proof or inferred savings.'}
    def save():
        (out / 'comparison.json').write_text(json.dumps(journal, indent=2) + '\n')
    save()
    with target(out, before) as (info, receipts):
        identity['target'] = info
        seen_tasks, seen_prompts = set(), set()
        schedule = []
        for n in range(1, 4):
            for arm in ('before', 'after'):
                schedule.extend([(f'attest-before-wall-{n:02d}', arm, False),
                                 (f'wall-{n:02d}', arm, False),
                                 (f'attest-after-wall-{n:02d}', arm, False)])
        schedule += [('observer', 'before', True), ('observer', 'after', True)]
        for label, arm, observed in schedule:
            vibe, sha = (before, args.before_sha) if arm == 'before' else (after, args.after_sha)
            if validate_environments(args.before_python, args.after_python, before, after) != environments:
                raise RuntimeError('environment report changed')
            pin(AGENT, AGENT_SHA)
            pin(vibe, sha)
            if any(digest(HERE / name) != value for name, value in identity['script_sha256'].items()):
                raise RuntimeError('harness script bytes changed')
            if (digest(PYTHON.resolve()) != identity['python_sha256'] or digest(HERE / 'astrid') != console_hash
                or digest(A2_CONSOLE) != console_hash or digest(vibe / TEMPLATE) != template_hash
                or digest(HERE / 'hash_probe.py') != identity['observer_sha256']):
                raise RuntimeError('fixed input bytes changed')
            name = f'{label}-{arm}'
            arm_python = args.before_python if arm == 'before' else args.after_python
            cmd = [str(arm_python.absolute()), '-B', str(HERE / 'runner.py'), '--agent', str(AGENT), '--agent-sha', AGENT_SHA,
                   '--vibe', str(vibe), '--vibe-sha', sha, str(out / name), '--trials', '1',
                   '--routes', 'W', '--modes', 'plain', '--target-url', info['url'],
                   '--target-receipts', str(receipts)]
            if observed:
                cmd += ['--observer-log']
            if label.startswith('attest-'):
                cmd += ['--attest', arm]
            row = {'label': label, 'arm': arm, 'observed': observed, 'directory': name,
                   'command': cmd, 'load_before': os.getloadavg()}
            journal['schedule'].append(row)
            save()
            with timing_lock(quiet=True) as load_before:
                row['load_before'] = load_before
                save()
                hook = attestation_hook(arm_python, environments['report'], out / name / 'host-attestation.jsonl') if label.startswith('attest-') else contextlib.nullcontext()
                with hook:
                    with (out / (name + '.runner.stdout')).open('wb') as stdout, (out / (name + '.runner.stderr')).open('wb') as stderr:
                        result = subprocess.run(cmd, stdout=stdout, stderr=stderr)
                row.update(returncode=result.returncode, load_after=os.getloadavg())
            save()
            if result.returncode:
                raise RuntimeError(f'{name} failed; preserve logs and stop the comparison')
            pin(AGENT, AGENT_SHA)
            pin(ROOT / 'a4-runtime', '182311f9d363712c0339254bd27e091d0e18318d')
            pin(vibe, sha)
            if validate_environments(args.before_python, args.after_python, before, after) != environments:
                raise RuntimeError('environment report changed during invocation')
            if any(digest(HERE / script) != value for script, value in identity['script_sha256'].items()):
                raise RuntimeError('harness script bytes changed during invocation')
            if (digest(PYTHON.resolve()) != identity['python_sha256'] or digest(HERE / 'astrid') != console_hash
                    or digest(A2_CONSOLE) != console_hash or digest(vibe / TEMPLATE) != template_hash
                    or digest(HERE / 'hash_probe.py') != identity['observer_sha256']):
                raise RuntimeError('fixed input bytes changed during invocation')
            manifest = json.loads((out / name / 'manifest.json').read_text())
            for sample in manifest['trials']:
                task, prompt = sample['task_id'], sample['target_prompt_id']
                if task in seen_tasks or prompt in seen_prompts:
                    raise RuntimeError('repeated task or prompt receipt')
                seen_tasks.add(task)
                seen_prompts.add(prompt)
            if digest(out / name / 'target-inventory.json') != info['inventory_sha256']:
                raise RuntimeError('target inventory differs')
            if observed and not (out / name / 'W-plain-1.hash.json').is_file():
                raise RuntimeError('observer output missing; run is invalid')
        journal['complete'] = True
        save()

if __name__ == '__main__':
    main()
