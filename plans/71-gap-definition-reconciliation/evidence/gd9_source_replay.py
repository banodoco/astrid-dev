#!/usr/bin/env python3
"""Read-only Plan 71 C1/C2 source preflight; never touches HOLD or modifies Git."""
import argparse
import re
import subprocess
import sys
from pathlib import Path

A = 'ca97096ba6893108c90a932479e7473f679c724e'
B = '6d75abf9cb0d102a1fef494f78dd9184d4e45d1f'
C = '70d5ac857e8066f8cacf98cda7b9d5d686a12f71'
PREFIX = 'plans/71-gap-definition-reconciliation/evidence/'
C2 = PREFIX + 'gd8-criterion-route-decisions-2026-11-22.md'
WITNESS = PREFIX + 'gd9-c2-exact-wording-witness-matrix-2026-11-23.md'
S5 = PREFIX + 'gd9-s5-criterion-proof-workpackets-2026-11-23.md'
ID = r'(?:AA|CA|CI|F|LS)-\d{3}-C\d{2}'
GAPLINK = re.compile(r'\]\(\.\./\.\./vision/gaps/([A-Z]{1,3}-\d{3})-[^)]+\.md\)')
PLANPATH = re.compile(r'^plans/\d{2}-[a-z0-9-]+/plan\.md$')
RAW_GAP_ID = re.compile(r'\b(?:AA|CA|CI|F|LS)-\d{3}\b')


def ids_in_plan(text):
    gaps = re.findall(r'^\*\*Vision gaps:\*\*\s*(.+)$', text, re.M)
    roles = re.findall(r'^\*\*Vision role:\*\*\s*(.+)$', text, re.M)
    if len(gaps) + len(roles) != 1:
        raise AssertionError('one Vision gaps/role declaration required')
    if roles:
        return []
    ids = GAPLINK.findall(gaps[0])
    if not ids or len(ids) != len(set(ids)) or gaps[0].count('(primary)') != 1:
        raise AssertionError('bad primary/link cardinality')
    first_link = GAPLINK.search(gaps[0])
    primary_at = gaps[0].index('(primary)')
    second_link = list(GAPLINK.finditer(gaps[0]))
    if primary_at < first_link.end() or (len(second_link) > 1 and primary_at > second_link[1].start()):
        raise AssertionError('primary must be the first linked gap')
    return ids


def raw_declaration_ids(text):
    """Count unique raw ID mentions on Vision gaps only, never coordination roles."""
    gaps = re.findall(r'^\*\*Vision gaps:\*\*\s*(.+)$', text, re.M)
    roles = re.findall(r'^\*\*Vision role:\*\*\s*(.+)$', text, re.M)
    if len(gaps) + len(roles) != 1:
        raise AssertionError('one Vision gaps/role declaration required')
    if roles:
        return []
    return list(dict.fromkeys(RAW_GAP_ID.findall(gaps[0])))


def self_test():
    assert ids_in_plan('**Vision gaps:** [F-001](../../vision/gaps/F-001-example.md) (primary)') == ['F-001']
    assert ids_in_plan('**Vision gaps:** [F-008](../../vision/gaps/F-008-example.md) (primary), [F-001](../../vision/gaps/F-001-example.md) (supporting)') == ['F-008', 'F-001']
    assert ids_in_plan('**Vision role:** enabler; no primary delivery [F-001](../../vision/gaps/F-001-example.md)') == []
    for malformed in ('**Vision gaps:** no link (primary)', '**Vision gaps:** [F-001](../../vision/gaps/F-001-example.md)', '**Vision gaps:** [F-001](../../vision/gaps/F-001-example.md) (primary) [F-001](../../vision/gaps/F-001-example.md)', '**Vision gaps:** [F-001](../../vision/gaps/F-001-example.md) (primary)\n**Vision role:** enabler'):
        try:
            ids_in_plan(malformed)
        except AssertionError:
            pass
        else:
            raise AssertionError('malformed plan accepted')
    assert raw_declaration_ids('**Vision gaps:** [F-003](../../vision/gaps/F-003-example.md) (primary). Why F-003 and not AA-001 or LS-002.') == ['F-003', 'AA-001', 'LS-002']
    assert raw_declaration_ids('**Vision gaps:** [LS-003](../../vision/gaps/LS-003-example.md) (primary). Former F-001 role transferred.') == ['LS-003', 'F-001']
    assert raw_declaration_ids('**Vision role:** Foundational enabler [CA-003](../../vision/gaps/CA-003-example.md) not delivered.') == []
    for malformed in ('**Vision gaps:** F-001\n**Vision role:** no', 'no declaration'):
        try:
            raw_declaration_ids(malformed)
        except AssertionError:
            pass
        else:
            raise AssertionError('malformed raw declaration accepted')
    print('PASS parser self-test: 6 positive, 6 negative')


def audit(root, expected_head):
    def git(*args):
        result = subprocess.run(['git', *args], cwd=root, text=True, capture_output=True)
        if result.returncode:
            raise AssertionError('git ' + ' '.join(args) + ': ' + result.stderr.strip())
        return result.stdout

    def read(commit, path):
        return git('show', f'{commit}:{path}')

    head = git('rev-parse', 'HEAD').strip()
    assert head == expected_head, f'HEAD {head} != {expected_head}'
    changed = git('diff', '--name-only', A, head).splitlines()
    assert changed and all(p.startswith(PREFIX) for p in changed), f'non-evidence changes: {changed}'
    assert not git('diff', '--check', A, head).strip(), 'git diff --check reported whitespace errors'

    for name, ref, expected, expected_raw in (('A', A, (69, 60, 83), None), ('B', B, (77, 68, 92), 95), ('C', C, (80, 71, 96), 99)):
        paths = [p for p in git('ls-tree', '-r', '--name-only', ref, '--', 'plans').splitlines() if PLANPATH.fullmatch(p)]
        linked, associations, raw = 0, 0, 0
        for path in paths:
            plan_text = read(ref, path)
            found = ids_in_plan(plan_text)
            linked += bool(found)
            associations += len(found)
            raw += len(raw_declaration_ids(plan_text))
        got = (len(paths), linked, associations)
        assert got == expected, f'{name} authored plan census {got} != {expected}'
        if expected_raw is not None:
            assert raw == expected_raw, f'{name} raw declaration reconstruction {raw} != {expected_raw}'
        print(f'PASS {name}: {got[0]} plans, {got[1]} linked, {got[2]} affirmative links' +
              (f', {raw} reconstructed raw declaration IDs' if expected_raw is not None else ''))
    print('NOTE historical plans.json algorithm not recovered; B/C declaration-line reconstruction independently matches 95/99')

    text = read(head, C2)
    first = text.split('## Frozen source and historical-owner crosswalk')[0]
    appendix = text.split('## Frozen source and historical-owner crosswalk')[1].split('## Promotion gates')[0]
    main_rows = [line for line in first.splitlines() if re.match(r'^\| ' + ID + r' —', line)]
    app_rows = [line for line in appendix.splitlines() if re.match(r'^\| ' + ID + r' \|', line)]
    main_ids = [re.search(ID, line).group(0) for line in main_rows]
    app_ids = [re.search(ID, line).group(0) for line in app_rows]
    assert len(main_ids) == 69 and main_ids == app_ids and len(set(main_ids)) == 69
    counts = {'PLAN_SCOPE': 0, 'SPECIFIC_EVIDENCE_MISSING': 0, 'UNPLANNED': 0}
    for line, refline in zip(main_rows, app_rows):
        cells = line.split('|')[1:-1]
        category = re.search(r'\*\*(PLAN_SCOPE|SPECIFIC_EVIDENCE_MISSING|UNPLANNED)\*\*', cells[1]).group(1)
        counts[category] += 1
        plans = re.findall(r'\[P(\d+)\]', cells[1])
        source_plans = re.findall(r'\[P(\d+) §\]', refline.split('|')[3])
        assert plans == source_plans, f'{re.search(ID, line).group(0)} plan mismatch'
        m = re.search(r'/blob/([0-9a-f]{40})/(vision/gaps/[^)#]+\.md)#L(\d+)\) `([0-9a-f]{12})`', refline)
        assert m and m.group(1) == A
        gap = read(A, m.group(2)).splitlines()
        assert git('rev-parse', f'{A}:{m.group(2)}').startswith(m.group(4))
        assert gap[int(m.group(3))-1] == '## Closure evidence'
        for commit, plan, prefix in re.findall(r'/blob/([0-9a-f]{40})/(plans/\d{2}-[a-z0-9-]+/plan\.md)#L\d+\) `([0-9a-f]{12})`', refline):
            assert commit == A and git('rev-parse', f'{A}:{plan}').startswith(prefix), plan
    assert counts == {'PLAN_SCOPE': 47, 'SPECIFIC_EVIDENCE_MISSING': 15, 'UNPLANNED': 7}

    witness_rows = [s for s in read(head, WITNESS).splitlines() if re.match(r'^\| \[' + ID + r'\]', s)]
    assert len(witness_rows) == 69
    found_ids = []
    for line in witness_rows:
        id_match = re.match(r'^\| \[(' + ID + r')\]', line)
        rowid = id_match.group(1)
        found_ids.append(rowid)
        m = re.search(r'/blob/([0-9a-f]{40})/(vision/gaps/[^)#]+\.md)#L(\d+)\): “([^”]+)”', line)
        assert m and m.group(1) == A, rowid
        lines = read(A, m.group(2)).splitlines()
        assert m.group(4) in lines[int(m.group(3))-1], rowid
        assert rowid.startswith(re.search(r'/([A-Z]{1,3}-\d{3})-', m.group(2)).group(1) + '-'), rowid
        assert 'NO-RESULT' in line, rowid
        if rowid == 'F-008-C09':
            assert 'ADJACENT ROUTE WITNESS (NONCRITERION)' in line
    assert found_ids == main_ids, 'witness order/IDs changed'
    task_ids = re.findall(r'^\| \[S5-(' + ID + r')\]', read(head, S5), re.M)
    assert len(task_ids) == 68 and set(task_ids) == set(main_ids) - {'F-008-C09'}
    print('PASS C2: 69 ordered rows + source witnesses; 68 distinct S5 tasks; categories 47/15/7 including adjacent C09')
    print('SOURCE-ONLY PASS; 65/4 semantic verdict, real outcomes and proof owners remain NO-RESULT')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path.cwd())
    parser.add_argument('--head', help='required exact PR commit SHA for full checkout audit')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    try:
        if args.self_test:
            self_test()
        else:
            if not args.head or not re.fullmatch(r'[0-9a-f]{40}', args.head):
                parser.error('--head must be the exact 40-hex PR head')
            audit(args.repo, args.head)
    except (AssertionError, OSError, ValueError, IndexError, AttributeError) as exc:
        print('FAIL source preflight:', exc, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
