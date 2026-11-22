#!/usr/bin/env python3
"""Exercise saved inputs twice and check determinism and representative values."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

here = Path(__file__).resolve().parent
with tempfile.TemporaryDirectory() as tmp:
    paths = [Path(tmp) / 'one', Path(tmp) / 'two']
    for path in paths:
        subprocess.run([sys.executable, str(here / 'rank.py'), str(here / 'fixture/manifest.json'), '--output', str(path)], check=True)
    for name in ('attribution-W.md', 'stages-W.json'):
        assert (paths[0] / name).read_bytes() == (paths[1] / name).read_bytes(), name
    rows = json.loads((paths[0] / 'stages-W.json').read_text())
    outer = next(row for row in rows if row['stage'] == 'outer')
    assert outer['seconds_median'] == .2 and outer['total_seconds_median'] == .4
    assert next(row for row in rows if row['stage'] == 'child')['parent'] == 'outer'
    assert next(row for row in rows if row['stage'] == 'other command work')['total_seconds_median'] is None
    report = (paths[0] / 'attribution-W.md').read_text()
    assert '| pkg | 0.006000 |' in report
    assert report.index('example.py:2(child)') < report.index('example.py:1(outer)')
    assert 'plain wall seconds' in report and '3.200000 s' in report
print('saved fixture: deterministic tables and expected stage, import and profile rankings')
