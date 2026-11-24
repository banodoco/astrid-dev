#!/usr/bin/env python3
"""Collect separate fixture batches without changing their raw receipts."""
import argparse
import json
import shutil
from pathlib import Path
p = argparse.ArgumentParser()
p.add_argument('--output', required=True, type=Path)
p.add_argument('manifests', nargs='+', type=Path)
a = p.parse_args()
a.output.mkdir(parents=True, exist_ok=False)
merged = {'source': 'source', 'trials': [], 'batches': []}
for i, path in enumerate(a.manifests):
    source = path.resolve().parent
    data = json.loads(path.read_text())
    if data.get('teardown_returncode') != 0:
        raise ValueError(f'unclean batch: {path}')
    name = f'batch-{i+1:02d}'
    dest = a.output / name
    shutil.copytree(source, dest)
    merged['batches'].append({'fixture_id': name, 'manifest': f'{name}/manifest.json'})
    for row in data['trials']:
        trial = dict(row, fixture_id=name)
        for field in ('stdout', 'stderr', 'profile'):
            if trial.get(field): trial[field] = f"{name}/{trial[field]}"
        merged['trials'].append(trial)
(a.output / 'manifest.json').write_text(json.dumps(merged, indent=2) + '\n')
