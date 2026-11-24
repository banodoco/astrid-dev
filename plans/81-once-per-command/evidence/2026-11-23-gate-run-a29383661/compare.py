from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import json
import re
import subprocess

d = Path(__file__).resolve().parent
s = d.parent
old = s / 'second'
sha = 'a29383661ad990da7ab43185f1a07132e074fadf'
api = 'https://api.github.com/repos/banodoco/astrid-agent/actions/'

def download(endpoint, path):
    part = path.with_suffix(path.suffix + '.part')
    subprocess.run(['curl', '-qfsSL', '--retry', '2', '--max-time', '75', api + endpoint, '-o', str(part)], check=True)
    part.replace(path)

def parse(job):
    filename = f"job-{job['id']}.log"
    path = next((p for p in (d/filename, old/filename, s/filename, *s.glob(f'*/{filename}')) if p.is_file() and p.stat().st_size), None)
    if path is None:
        path = d / filename
        download(f"jobs/{job['id']}/logs", path)
    rows = {k:(v,reason.strip()) for v,k,reason in re.findall(r' (PASSED|FAILED|ERROR|SKIPPED|XFAIL|XPASS) (tests/[^\s]+::[^\s]+)([^\n]*)',path.read_text(errors='replace'))}
    if not rows:
        raise RuntimeError(f"no pytest results in {path}")
    return rows

targets = json.loads((s/'frozen/37.json').read_text())
groups = {}
original = {}
interesting = {}
look = ('test_ready_entries_reports_first_resource_failure','test_fresh_process_command_counts','test_workflow_input_delay_is_attributed','test_defaults_is_ready_once_the_files_are_listed','test_a_partly_installed_default_names_only_what_is_missing','test_secret_never_appears_in_receipt_state_or_cli_output','test_rendered_mp4_contains_audio_stream','test_shared_redo_rechecks_source_archive_at_acceptance','audio/tts-local-managed-trust]')
for lane,base,previous,merged in [('unit',45031908687,45095434060,45106316187),('integration',45031908621,45095437908,45106319353)]:
    info_path = d / f'run-{merged}.json'
    download(f'runs/{merged}', info_path)
    info = json.loads(info_path.read_text())
    assert info['head_sha'] == sha and info['event'] == 'workflow_dispatch'
    jobs_path = d / f'jobs-{merged}.json'
    download(f'runs/{merged}/jobs?per_page=100', jobs_path)
    all_jobs = [json.loads((old/f'jobs-{v}.json').read_text())['jobs'] for v in (base,previous)] + [json.loads(jobs_path.read_text())['jobs']]
    for group in ((lane,'darwin') if lane=='unit' else (lane,'opt-in')):
        def match(j):
            return j['name'].startswith(lane+' shard') if group==lane else j['name']==('darwin native' if group=='darwin' else 'opt-in')
        sides = []
        pending = []
        for side, jobs in enumerate(all_jobs):
            rows = {}
            subset = [j for j in jobs if match(j)]
            if side == 2:
                pending=[j['name'] for j in subset if j['status']!='completed']
            with ThreadPoolExecutor(max_workers=3) as pool:
                for part in pool.map(parse, [j for j in subset if j['status']=='completed']):
                    rows.update(part)
            sides.append(rows)
        b,p,h = sides
        red = {k:{'base': b.get(k,('absent',''))[0], 'previous':p.get(k,('absent',''))[0], 'head':v, 'detail':t[:500]} for k,(v,t) in h.items() if v in ('FAILED','ERROR','XPASS')}
        groups[group] = dict(run=merged, status=info['status'], conclusion=info['conclusion'],pending=pending, red=red)
        print(group, info['status'],info['conclusion'],pending,len(red),Counter(r['base'] for r in red.values()), flush=True)
        for k,r in red.items():
            if r['base'] not in ('FAILED','ERROR'):
                print(k,r,flush=True)
        if group in ('unit','integration'):
            original.update({k:v for k,(v,_) in h.items() if k in targets})
        for k,(v,reason) in h.items():
            if any(t in k for t in look):
                interesting.setdefault(group,{})[k] = [v, reason[:300]]
ledger = {k:original.get(k,'unobserved') for k in targets}
result=dict(groups=groups,ledger=ledger,selected=interesting)
(d/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print('original 37:',Counter(ledger.values()),flush=True)
