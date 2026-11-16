"""Compare per-node ID, phase status, and full failure signatures.
Volatile normalization: `basetemp/<integer>` or truncated `emp/<integer>` temp roots;
hex object addresses; explicit pid/process-id values; monotonic `deadline=<number>`.
JUnit duration attributes and elapsed pytest summary text are excluded; semantic
assertion/exception messages and normalized full traceback text remain exact.
"""
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

patterns = [
    (re.compile(r'(?:basetemp|emp)/\d+'), 'temp-root/<RUN>'),
    (re.compile(r'0x[0-9a-fA-F]+'), '<ADDRESS>'),
    (re.compile(r'\b(?:pid|process(?:_id)?)(?:\s+|\s*[=:]\s*)\d+\b', re.I), '<PROCESS-ID>'),
    (re.compile(r'\bdeadline\s*=\s*[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?'), 'deadline=<TIME>'),
]

def normalize(text):
    for regex, replacement in patterns:
        text = regex.sub(replacement, text)
    return text

def load(path):
    rows = []
    for testcase in ET.parse(path).getroot().iter('testcase'):
        nodeid = testcase.get('classname', '') + '.' + testcase.get('name', '')
        phase = [item for item in testcase if item.tag in ('failure', 'error', 'skipped')]
        status = 'pass' if not phase else ','.join(item.tag for item in phase)
        signatures = tuple((item.tag, normalize(item.get('message', '')),
                            normalize(''.join(item.itertext()))) for item in phase)
        rows.append((nodeid, status, signatures))
    return rows

before, after = map(load, sys.argv[1:3])
ids_equal = Counter(row[0] for row in before) == Counter(row[0] for row in after)
bmap = {row[0]: row[1:] for row in before}
amap = {row[0]: row[1:] for row in after}
diffs = sorted(node for node in bmap.keys() | amap.keys() if bmap.get(node) != amap.get(node))
print(f'node_count_before={len(before)} node_count_after={len(after)} id_multiset_equal={ids_equal}')
print(f'outcomes_and_signatures_equal={ids_equal and not diffs} node_differences={len(diffs)}')
print(f'before_statuses={dict(Counter(row[1] for row in before))}')
print(f'after_statuses={dict(Counter(row[1] for row in after))}')
for node in diffs:
    print(f'DIFFERENT_NODE={node}')
    print(f'  before={bmap.get(node)}')
    print(f'  after={amap.get(node)}')
if not ids_equal or diffs:
    raise SystemExit(1)
