#!/usr/bin/env python3
"""Copy the fixed environment into two matching arm environments without importing Vibe."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess

HERE = Path(__file__).resolve().parent
BASE = Path('/root/codex/plan-81m/attribution-evidence.env')
BEFORE = Path('/root/codex/plan-81m/witness-vibe-base')
AGENT = Path('/root/codex/plan-81m/attribution-a3')
BASE_SOURCE = Path('/root/codex/plan-81m/VibeComfy')
RUNTIME = Path('/root/codex/plan-81m/a4-runtime')


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def inventory(root, excluded):
    rows = {}
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root).as_posix()
        if rel == excluded:
            continue
        mode = stat.S_IMODE(path.lstat().st_mode)
        if path.is_symlink():
            rows[rel] = ['link', mode, os.readlink(path)]
        elif path.is_dir():
            rows[rel] = ['directory', mode]
        elif path.is_file():
            rows[rel] = ['file', mode, sha(path)]
        else:
            raise RuntimeError(f'unsupported environment entry: {path}')
    return rows


def distributions(python, site):
    # -S prevents execution of any .pth file, including the arm source path.
    code = ("import importlib.metadata as m,json,sys; "
            "print(json.dumps(sorted((d.metadata.get('Name',''),d.version) "
            "for d in m.distributions(path=[sys.argv[1]]))))")
    return json.loads(subprocess.check_output([str(python), '-B', '-S', '-c', code, str(site)], text=True))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('output', type=Path, help='new directory for both copied environments')
    p.add_argument('--after-vibe', type=Path, required=True)
    p.add_argument('--before-vibe', type=Path, default=BEFORE)
    p.add_argument('--base', type=Path, default=BASE)
    p.add_argument('--agent', type=Path, default=AGENT)
    p.add_argument('--runtime', type=Path, default=RUNTIME)
    args = p.parse_args()
    base = args.base.resolve(strict=True)
    before = args.before_vibe.resolve(strict=True)
    after = args.after_vibe.resolve(strict=True)
    agent = args.agent.resolve(strict=True)
    runtime = args.runtime.resolve(strict=True)
    if before == after:
        p.error('arm source directories must be distinct')
    sites = list((base / 'lib').glob('python*/site-packages'))
    if len(sites) != 1:
        raise RuntimeError('expected exactly one base site-packages directory')
    site_rel = sites[0].relative_to(base)
    pth_rel = site_rel / 'attribution-source.pth'
    lines = (base / pth_rel).read_text().splitlines()
    original = [str(Path('/root/codex/plan-81m/a4-agent')), str(RUNTIME), str(BASE_SOURCE)]
    if lines != original:
        raise RuntimeError('base attribution-source.pth differs from the fixed original')
    source_prefix = [str(agent), str(runtime)]
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    roots = {arm: out / arm for arm in ('before', 'after')}
    for arm, source in (('before', before), ('after', after)):
        shutil.copytree(base, roots[arm], symlinks=True, copy_function=shutil.copy2)
        (roots[arm] / pth_rel).write_text('\n'.join(source_prefix + [str(source)]) + '\n')
        site = roots[arm] / site_rel
        if (site / 'sitecustomize.py').exists() or (site / 'host_attest.py').exists():
            raise RuntimeError('base environment already contains an attestation hook')
    inventories = {arm: inventory(root, pth_rel.as_posix()) for arm, root in roots.items()}
    if inventories['before'] != inventories['after']:
        raise RuntimeError('arm environment trees differ outside attribution-source.pth')
    binary_hashes = {arm: sha((root / 'bin/python').resolve(strict=True)) for arm, root in roots.items()}
    if len(set(binary_hashes.values())) != 1 or next(iter(binary_hashes.values())) != sha((base / 'bin/python').resolve(strict=True)):
        raise RuntimeError('arm interpreter binaries differ')
    packages = {arm: distributions(root / 'bin/python', root / site_rel) for arm, root in roots.items()}
    if packages['before'] != packages['after']:
        raise RuntimeError('arm installed package metadata differs')
    pip = ['/usr/bin/python3', '-I', '-B', '-m', 'pip']
    pip_version = subprocess.check_output(pip + ['--version'], text=True).strip()
    freeze_commands = {arm: pip + ['freeze', '--all', '--path', str(root / site_rel)]
                       for arm, root in roots.items()}
    freezes = {arm: subprocess.check_output(command, text=True).splitlines()
               for arm, command in freeze_commands.items()}
    if freezes['before'] != freezes['after']:
        raise RuntimeError('arm pip freeze output differs')
    report = {'base': str(base), 'original_source_lines': lines, 'source_prefix': source_prefix, 'arms': {arm: {'environment': str(root), 'python': str(root / 'bin/python'),
              'source': str(before if arm == 'before' else after), 'source_pth_sha256': sha(root / pth_rel),
              'python_binary_sha256': binary_hashes[arm]} for arm, root in roots.items()},
              'site_packages_relative': str(site_rel), 'tree_excluding_source_pth': inventories['before'],
              'installed_distributions': packages['before'],
              'pip_version': pip_version, 'pip_freeze_commands': freeze_commands,
              'pip_freeze_all': freezes['before'],
              'note': 'Metadata inventory is not a runtime import proof; no Vibe module was imported.'}
    (out / 'environment-identity.json').write_text(json.dumps(report, indent=2) + '\n')
    print(out / 'environment-identity.json')


if __name__ == '__main__':
    main()
