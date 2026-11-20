"""Inspect an unchanged hosted verdict ZIP; invoke with the path to artifact 14614377040."""
import argparse
import collections
import hashlib
import json
import re
import zipfile
from pathlib import Path

OFFICIAL_DIGEST = '84491e3752b056f6acb7dc63f07cc211897bfd3d899f339230ef1865325de1fb'
NATIVE = 'artifact-14609831662'
TLS_NAMES = {
    'test_certificate_failure_retries_once_with_verified_context': 'test_certificate_failure_stops_after_one_verified_attempt',
    'test_default_success_uses_one_attempt_without_changing_ssl': 'test_success_uses_one_verified_attempt_without_changing_ssl',
    'test_open_with_tls_fallback_keeps_handlers_and_retries_once_natively': 'test_open_with_tls_fallback_keeps_handlers_and_uses_shared_policy_once',
    'test_repeated_certificate_failure_stops_after_two_attempts': 'test_repeated_certificate_failure_is_never_retried',
    'test_retry_still_rejects_a_checksum_mismatch': 'test_shared_trust_still_rejects_a_checksum_mismatch',
    'test_retry_works_in_dependency_free_bootstrap': 'test_shared_policy_works_in_dependency_free_bootstrap',
}

def identity(row):
    return (row['lane'], row['native_id'], json.dumps(row['parameter']), json.dumps(row['subtest']))

def temp_pattern(subtest):
    # A diagnostic comparison for two known subtests; original keys stay distinct.
    return re.sub(r'/tmp/tmp[0-9a-z_]+/', '<temporary-directory>/', subtest)

def inspect(path):
    if hashlib.sha256(path.read_bytes()).hexdigest() != OFFICIAL_DIGEST:
        raise ValueError('Unexpected hosted ZIP digest')
    with zipfile.ZipFile(path) as z:
        verdict = json.loads(z.read('verdict.json'))
        jobs = json.loads(z.read('observed.json'))['jobs']
        archive = z.read(NATIVE+'/artifact.zip')
        provenance = json.loads(z.read(NATIVE+'/provenance.json'))
        assert 'sha256:'+hashlib.sha256(archive).hexdigest() == provenance['digest']
        native_records = []
        for name in z.namelist():
            if name.startswith(NATIVE+'/files/step-18/') and name.endswith('.jsonl'):
                records = [json.loads(line) for line in z.open(name)]
                if '--collect-only' not in records[0]['args']:
                    assert not native_records
                    native_records = records
    lost = {tuple(json.loads(e.removeprefix('lost ID: '))) for e in verdict['errors'] if e.startswith('lost ID: ')}
    suites = {int(j['job'].split()[2]):j['suites'][0] for j in jobs if j['job'].startswith('unit shard')}
    current = {identity(r):r for s in suites.values() for r in s['tests']}
    selected = {node for s in suites.values() for node in s['collected']}
    shard = suites[2]
    counts = collections.Counter(map(identity, shard['tests']))
    duplicates = [(k,c) for k,c in counts.items() if c>1]
    assert len(duplicates)==1
    dup, occurrences = duplicates[0]
    raw = [r for r in native_records if r['event']=='report']
    collided = [r for r in raw if r['native_id']==dup[1] and json.dumps(r['subtest'])==dup[3]]
    intersection = lost.intersection(counts)
    shifted = []
    absent = []
    for k in sorted(lost - intersection):
        lane, node, param, subtest = k
        if node in selected:
            candidates = [r for key,r in current.items() if key[:3]==k[:3] and key[3]!=subtest and temp_pattern(key[3])==temp_pattern(subtest)]
            assert len(candidates)==1
            shifted.append({'node':node, 'subtest_pattern':temp_pattern(json.loads(subtest)), 'observed':candidates[0]['outcome']})
            continue
        filename,test=node.split('::')
        method=test.split('[')[0]
        if method in TLS_NAMES:
            names=[node.replace('::'+method,'::'+TLS_NAMES[method])]
            commit='b9740f64b300b5d5fc69b84499b071093f4fe68e'
        elif 'test_handoff_sentence' in filename:
            names=sorted(n for n in selected if n.startswith(filename+'::test_skills_off_closes_with_a_runnable_launcher_scan_hint['))
            commit='a525e87e4bf66558af627cb3773ae4740f78a6b9'
        elif 'test_installer_shim' in filename:
            names=[node.replace('None-False-True-','None-False-False-')]
            commit='a525e87e4bf66558af627cb3773ae4740f78a6b9'
        else:
            raise ValueError(node)
        replacements={k2[1]:r['outcome'] for k2,r in current.items() if k2[1] in names and r['subtest'] is None}
        assert names and len(names)==len(replacements)
        absent.append({'absent_native_id':node,'source_change':commit,'observed_successors':replacements})
    return {'verdict_artifact':14614377040,'verdict_digest':OFFICIAL_DIGEST,'verdict':verdict['verdict'],
        'native_artifact':provenance['id'],'native_digest':provenance['digest'],'run':provenance['workflow_run']['id'],
        'head':verdict['head'],'lane':shard['lane'],'collected_primary':len(shard['collected']),
        'native_end':native_records[-1], 'primary_outcomes':dict(collections.Counter(r['outcome'] for r in shard['tests'] if r['subtest'] is None)),
        'phase_counts':dict(sorted(collections.Counter(r['stage']+' '+r['outcome'] for r in raw).items())),'native_reports':len(raw),
        'normalized_rows':len(shard['tests']),'distinct_full_keys':len(counts),'duplicate':{'parent':dup[1],'subtest':json.loads(dup[3]),
        'native_outcomes':[r['outcome'] for r in collided], 'stage':[r['stage'] for r in collided], 'occurrences':occurrences},
        'sealed_lost_total':len(lost),'with_exact_shard2_receipt':len(intersection),
        'matching_primary':sum(k[3]=='null' for k in intersection),'matching_subtest':sum(k[3]!='null' for k in intersection),
        'current_shard2_keys_outside_lost_inventory':len(set(counts)-lost),'temporary_path_subtests':shifted,'absent_primaries':absent}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive',type=Path)
    print(json.dumps(inspect(parser.parse_args().archive),indent=2))
