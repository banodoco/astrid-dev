import json,pathlib,re,subprocess
d=pathlib.Path(__file__).parent
def ids(log):
    return {k:v for v,k in re.findall(r' (PASSED|FAILED|ERROR) (tests/[^\s]+::[^\s]+)',log.read_text(errors='replace'))}
s=d.parent
old8=ids(s/'recovery-Kz7iLY/job-137289348449.log')
base8=ids(s/'recovery-Kz7iLY/job-137237128837.log')
target={k for k,v in old8.items() if v!='PASSED' and base8.get(k)=='PASSED'}
for f in ['hosted-1843','hosted-1910']:
    for row in json.loads((s/f/'paired.json').read_text()): target.update(row['base_passes'])
assert len(target)==37
result={x:'unobserved' for x in sorted(target)}
live={}
for run in (45081061979,45081065076):
    def fetch(url,path):
        subprocess.run(['curl','-qfsSL','--max-time','45',url,'-o',str(path)],check=True)
    url='https://api.github.com/repos/banodoco/astrid-agent/actions'
    runfile=d/f'status-{run}.json';fetch(f'{url}/runs/{run}',runfile)
    runinfo=json.loads(runfile.read_text());assert runinfo['head_sha'].startswith('13d328dc'); print(run,runinfo['status'],runinfo['conclusion'])
    jobs=d/f'jobs-{run}.json';fetch(f'{url}/runs/{run}/jobs?per_page=100',jobs)
    for j in json.loads(jobs.read_text())['jobs']:
        if j['status']!='completed' or not j['name'].startswith(('unit shard','integration shard','fast checks')): continue
        log=d/f"job-{j['id']}.log"
        if not log.exists(): fetch(f"{url}/jobs/{j['id']}/logs",log)
        results=ids(log)
        for k,v in results.items():
            if k in target: result[k]=v
            if 'test_workflow_input_delay_attribution' in k or 'test_fresh_process_command_counts' in k: live[k]=v
(d/'37.json').write_text(json.dumps(result,indent=2));print({v:list(result.values()).count(v) for v in set(result.values())},live)
