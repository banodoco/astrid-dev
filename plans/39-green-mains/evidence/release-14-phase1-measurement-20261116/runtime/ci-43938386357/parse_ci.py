from pathlib import Path
import collections
import hashlib
import json
import re

ROOT = Path(__file__).parent
WORKSPACE = ROOT.parents[2]
OLD = {r['nodeid']: r for j in json.loads((WORKSPACE / 'p39-g1-evidence/runtime/audited-per-id.json').read_text()) for r in j['rows']}
RUN = json.loads((ROOT / 'run-metadata.json').read_text())
JOBS = {j['id']: j for j in json.loads((ROOT / 'jobs-attempt-1.json').read_text())['jobs']}
ARTIFACTS = json.loads((ROOT / 'artifacts.json').read_text())['artifacts']
ARTIFACT_NAMES = {
    133548963680: 'test-results-sandbox-process-control-all-Linux',
    133548963714: 'test-results-portability-lifecycle-all-ubuntu-latest',
    133548963731: 'test-results-unit-all-ubuntu-latest',
    133548963837: 'test-results-portability-lifecycle-all-macos-latest',
    133548963937: 'test-results-unit-all-macos-latest',
}

def clean(raw):
    return re.sub(r'\x1b\[[0-9;]*m', '', re.sub(r'^\S+Z ', '', raw.lstrip('\ufeff'))).lstrip('\ufeff')

def classify(row, job):
    node, msg = row['nodeid'], row['literal_message']
    old = OLD.get(node, {})
    p38 = old.get('plan38_waiting')
    p55 = old.get('plan55_waiting')
    row['plan38_waiting'] = p38
    row['plan55_waiting'] = p55
    row['ownership_status'] = ('WAITING — Plan 38 ' + p38) if p38 else ('WAITING — Plan 55 ' + p55) if p55 else 'No exact hold established; no fix authorized by measurement'
    if p38:
        return 'R-m', 'Plan 38 waiting; retain the observed error without changing owned tests'
    if p55:
        return 'R-j / Plan 55', 'Plan 55 task-lifecycle/publication waiting; cause not resolved'
    if 'portability-lifecycle' in job['name']:
        return 'R-k / RT7', 'Portability lifecycle failure; cause requires focused investigation'
    if 'astrid.sdk.timeline' in msg and ('ModuleNotFoundError' in msg or 'ImportError' in msg):
        return 'new — RE1/RE2 API compatibility', 'Agent is present but the named SDK module/export is unavailable; product versus test contract not settled'
    if 'admitted_element_snapshot_descriptor' in msg or '_RuntimeSourceCustody' in msg:
        return 'new — RE1/RE2 API compatibility', 'Named Agent API is unavailable; product versus test contract not settled'
    if "No such file or directory: 'tsc'" in msg:
        return 'R-f / RE4', 'TypeScript compiler not on the executing test process PATH'
    if 'cannot archive required commit' in msg or ('git' in msg and 'archive' in msg and 'CalledProcessError' in msg):
        return 'R-c / RE3', 'Required historical object is unavailable to archive; authentic source remains required'
    if 'frozen ordinary Agent source is unavailable' in msg or '/home/user/work/wt/agt-pin-' in msg:
        return 'R-b / RE2', 'Private checkout fixture dependency remains'
    if 'Astrid checkout is unavailable' in msg or "No module named 'astrid'" in msg:
        return 'R-a / RE1', 'Agent checkout or import unavailable in the named execution environment'
    if 'v33 provider/baseline verification is pending' in msg:
        return 'R-d / RT1', 'Readiness fence is intact; fixture-versus-product diagnosis pending'
    if 'migrated realm requires fresh Timeline provider registration' in msg:
        return 'R-e / RT2', 'Migrated-realm provider requirement is intact; diagnosis pending'
    if 'tests/test_skip_registry.py' in node:
        return 'R-j / K1b follow-up', 'Registry/declared-lane guard failure; preserve its enforcement'
    if 'tests/test_skip_policy.py' in node:
        return 'R-j / K1b follow-up', 'Direct skip policy guard failure; preserve its enforcement'
    if "'types.SimpleNamespace' object has no attribute" in msg:
        return 'R-i / RT5', 'Test-double interface mismatch; product contract must be checked before repair'
    if old.get('triage') in ('R-g', 'R-h', 'R-i'):
        return old['triage'], 'Existing G1 triage row; changed signature is not proof of root cause'
    return 'R-j / RT6' if node in OLD else 'new — unclassified', 'Unclassified cause; real product bug must be ruled out before changing the test'

for path in sorted(ROOT.glob('job-*.log')):
    job_id = int(path.stem.split('-')[-1]); job = JOBS[job_id]
    lines = [clean(l) for l in path.read_text().splitlines()]
    idx = max(i for i,l in enumerate(lines) if re.match(r'^=+ short test summary info =+$', l))
    end = next(i for i in range(idx+1,len(lines)) if re.match(r'^[= ]*\d+ (?:passed|failed|skipped|deselected|error)',lines[i]) and re.search(r'\bin \d+(?:\.\d+)?s',lines[i]))
    rows=[]; current=None; skips=[]; xfails=[]
    for i in range(idx+1,end):
        line=lines[i]; m=re.match(r'^(FAILED|ERROR|PASSED|SKIPPED|XFAIL|XPASS|SUBPASSED|SUBFAILED(?:\(.*\))?) (.*?)(?: - (.*))?$', line)
        if m:
            current=None
            if m[1] in ('FAILED','ERROR'):
                current={'outcome':m[1],'nodeid':m[2],'summary_message':m[3] or '', 'outer_summary_line':i+1}; rows.append(current)
            elif m[1]=='SKIPPED': skips.append({'literal':line,'outer_summary_line':i+1})
            elif m[1]=='XFAIL': xfails.append({'literal':line,'outer_summary_line':i+1})
        elif current is not None: current['summary_message'] += '\n' + line
    headers=[];section=''
    for i,line in enumerate(lines[:idx]):
        sec=re.match(r'^=+ (.*?) =+$',line)
        if sec:
            if headers and headers[-1].get('end') is None: headers[-1]['end']=i
            section=sec[1]
        header=re.match(r'^_+ (.*?) _+$',line)
        if header and section in ('ERRORS','FAILURES') and set(header[1]) != {'_',' '}:
            if headers and headers[-1].get('end') is None: headers[-1]['end']=i
            headers.append({'start':i,'end':None,'header':header[1], 'outcome':'ERROR' if section=='ERRORS' else 'FAILED'})
    if headers and headers[-1]['end'] is None: headers[-1]['end']=idx
    unmatched=[]; ambiguous=[]; used=[]
    for row in rows:
        labels={row['nodeid'].split('::')[-1], '.'.join(row['nodeid'].split('::')[1:])}
        choices=[h for h in headers if h['outcome']==row['outcome'] and re.sub(r'^ERROR at (?:setup|teardown) of ', '', h['header']) in labels]
        if len(choices)>1:
            candidates=[h for h in choices if any(row['nodeid'].split('::')[0]+':' in l for l in lines[h['start']:h['end']])]
            if candidates: choices=candidates
        row['summary_message']=row['summary_message'].rstrip()
        if not choices: unmatched.append(row['nodeid'])
        elif len(choices)>1: ambiguous.append(row['nodeid'])
        else:
            h=choices[0]; used.append(h['start'])
            row['detail_header']=h['header'];row['detail_line_range']=[h['start']+1,h['end']]
            block=lines[h['start']+1:h['end']]
            captured=next((i for i,l in enumerate(block) if re.match(r'^-+ Captured .* -+$',l)),len(block))
            block=block[:captured]
            groups=[];g=[]
            for line in block:
                if re.match(r'^E(?:\s|$)',line): g.append(line[1:])
                elif g: groups.append(g);g=[]
            if g:groups.append(g)
            if groups:
                g=groups[-1];indent=min(len(l)-len(l.lstrip()) for l in g if l.strip())
                row['detail_message']='\n'.join(l[indent:] if l.strip() else '' for l in g).rstrip()
            else:row['detail_message']=''
            row['detail_all_e_lines']=[l for l in block if re.match(r'^E(?:\s|$)',l)]
        row['literal_message']=row['summary_message'] or row.get('detail_message','')
        row['message_source']='outer short summary (including continuations)' if row['summary_message'] else 'last contiguous E-line group of matched outer detail block'
        row['triage'],row['classification_note']=classify(row,job)
    outcomes=dict(collections.Counter(r['outcome'] for r in rows))
    counts={k:int(v) for v,k in re.findall(r'(\d+) (failed|passed|skipped|xfailed|errors|deselected|subtests passed)',lines[end])}
    assert outcomes.get('FAILED',0)==counts.get('failed',0)
    assert outcomes.get('ERROR',0)==counts.get('errors',0)
    assert not unmatched and not ambiguous,(job_id,unmatched,ambiguous)
    assert len(used)==len(set(used))==len(rows)==len(headers),(job_id,len(used),len(headers))
    assert all(r['literal_message'] for r in rows)
    junit=[]
    for i,line in enumerate(lines[end+1:],end+1):
        m=re.match(r'([\w-]+\.xml): tests=(\d+) failures=(\d+) errors=(\d+) skipped=(\d+)$',line)
        if m:junit.append({'literal':line,'log_line':i+1,'tests':int(m[2]),'failures':int(m[3]),'errors':int(m[4]),'skipped':int(m[5])})
    assert len(junit)==1
    assert junit[0]['failures']==counts.get('failed',0) and junit[0]['errors']==counts.get('errors',0)
    assert junit[0]['skipped']==counts.get('skipped',0)+counts.get('xfailed',0)
    assert junit[0]['tests']==sum(counts.get(x,0) for x in ('failed','passed','errors','skipped','xfailed','subtests passed'))
    groups=[]
    for message,n in collections.Counter(r['literal_message'] for r in rows).most_common():
        subset=[r for r in rows if r['literal_message']==message]
        groups.append({'literal_message':message,'count':n,'outcomes':dict(collections.Counter(r['outcome'] for r in subset)),'triage_counts':dict(collections.Counter(r['triage'] for r in subset)),'ownership_counts':dict(collections.Counter(r['ownership_status'] for r in subset)),'nodeids':[r['nodeid'] for r in subset]})
    data={
      'provenance':{'repository':'banodoco/astrid-runtime','head_sha':RUN['head_sha'],'tree_sha':RUN['head_commit']['tree_id'],'branch':RUN['head_branch'],'run_id':RUN['id'],'run_attempt':1,'event':RUN['event'],'job_id':job_id,'job_name':job['name'],'job_url':job['html_url'],'conclusion':job['conclusion'],'started_at':job['started_at'],'completed_at':job['completed_at'],'raw_log_file':path.name,'raw_log_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'raw_log_bytes':path.stat().st_size},
      'measurement_status':'post-batch measurement / provisional G2; phase-1 acceptance pending; formal RS1 0/1',
      'pytest_summary':lines[end],'pytest_counts':counts,'pytest_summary_log_line':end+1,'junit_summary':junit[0],
      'counting_method':{'outer_short_summary_log_line':idx+1,'matched_outer_detail_blocks':len(headers),'unmatched':unmatched,'ambiguous':ambiguous,'message_format':'Timestamp/ANSI/BOM framing removed. Continuation lines and literal values are preserved. Summary used when populated; otherwise last contiguous E-line group in matched outer detail block. Common pytest E-line indentation removed, no path/value normalization. Captured nested test output never counted.'},
      'outcome_counts':outcomes,'distinct_literal_message_count':len(groups),'triage_counts':dict(collections.Counter(r['triage'] for r in rows)),
      'ownership_waiting':{'plan38':sum(bool(r['plan38_waiting']) for r in rows),'plan55':sum(bool(r['plan55_waiting']) for r in rows)},
      'distinct_literal_messages':groups,'outer_outcomes':rows,'skip_reason_rows':skips,'xfail_rows':xfails,
      'limitations':['One hosted attempt is measurement, not root-cause proof.','JUnit XML was not downloaded; totals are the always-run summary emitted in the job log.','The exact G1 Plan 38/55 holds are retained; newly diagnosed lifecycle/publication contracts require ownership review before any fix. No broad file family is automatically assigned to Plan 39.','Pytest may abbreviate its own long values. Full captured logs and detailed E-lines remain available.']
    }
    artifact = next(a for a in ARTIFACTS if a['name'] == ARTIFACT_NAMES[job_id])
    data['junit_artifact'] = {k:artifact[k] for k in ('id','name','digest','size_in_bytes','expired')}
    data['junit_artifact']['downloaded'] = False
    data['ownership_review_candidates'] = [
        {'nodeid':r['nodeid'],'status':'WAITING — Plan 55 ownership confirmation before test changes',
         'reason':'Runtime producer task publication, cancellation, stale fence or retry; Plan 55 inventory includes task lifecycle and publication. Confirm against LS-7 before assigning repairs.'}
        for r in rows if r['nodeid'].startswith('tests/test_timeline_render_publication.py::')
    ]
    path.with_suffix('.json').write_text(json.dumps(data,indent=2)+'\n')
    md=[f"# Runtime CI {RUN['id']} / {job['name']} — provisional G2",'',f"- Exact head: `{RUN['head_sha']}`; tree `{RUN['head_commit']['tree_id']}`.",f"- Attempt 1; job [{job_id}]({job['html_url']}); result **failure**.",f"- Pytest: **{lines[end]}**.",f"- JUnit summary: `{junit[0]['literal']}`. Subtests are included in the JUnit test total; expected xfails are included in skipped.",f"- Reconciled {len(rows)} outer failures/errors with {len(headers)} matched detailed blocks; {len(groups)} distinct full literal messages.",f"- Exact held outcomes: Plan 38 **{data['ownership_waiting']['plan38']}**; Plan 55 **{data['ownership_waiting']['plan55']}**.",f"- Raw log: `{path.name}` ({path.stat().st_size} bytes), SHA-256 `{data['provenance']['raw_log_sha256']}`.",'','Formal RS1 remains **0/1**. This measurement does not close phase-1 acceptance.','','## Every distinct literal message with counts','', '| Count | Outcomes | Triage | Exact full message |','|---:|---|---|---|']
    for group in groups:
        esc=group['literal_message'].replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('|','&#124;').replace('\n','<br>')
        md.append(f"| {group['count']} | {', '.join(f'{k} {v}' for k,v in group['outcomes'].items())} | {', '.join(f'{k}: {v}' for k,v in group['triage_counts'].items())} | <code>{esc}</code> |")
    md+=['','## Waiting outcomes','']
    for row in rows:
        if row['plan38_waiting'] or row['plan55_waiting']:md.append(f"- `{row['nodeid']}` — {row['ownership_status']}; outer summary line {row['outer_summary_line']}.")
    if not any(r['plan38_waiting'] or r['plan55_waiting'] for r in rows):md.append('No previously established exact Plan 38/55 hold appears in this job’s failures/errors. Ownership must still be reviewed before modifying a newly diagnosed lifecycle/publication test.')
    md+=['','## Additional ownership review holds','']
    if data['ownership_review_candidates']:
        md += [f"- `{r['nodeid']}` — {r['status']}. {r['reason']}" for r in data['ownership_review_candidates']]
    else:
        md.append('No additional candidate is asserted by this measurement. This is not clearance to alter an unreviewed task-lifecycle or publication test.')
    md+=['','## JUnit artifact','',f"Artifact `{artifact['name']}`, ID `{artifact['id']}`, digest `{artifact['digest']}`. The archive was not downloaded; the emitted JUnit totals above were reconciled to pytest."]
    md+=['','## Method and limitations','',data['counting_method']['message_format'],'']+['- '+s for s in data['limitations']]
    md+=['','The paired JSON contains every exact test ID, full literal message, detailed E-lines, line anchors, triage, and waiting status.']
    path.with_suffix('.md').write_text('\n'.join(md)+'\n')
    print(job_id,job['name'],outcomes,'distinct',len(groups),'waiting',data['ownership_waiting'],'triage',data['triage_counts'])
