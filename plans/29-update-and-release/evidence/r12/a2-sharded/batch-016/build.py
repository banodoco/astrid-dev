import hashlib,json,pathlib,re,subprocess,sys
src=pathlib.Path('/workspace/r12-a2-resume/sharded'); out=pathlib.Path('/workspace/r12-a2-evidence-016'); sides=('r10','r11','base','candidate'); all_results={}
for n in map(lambda x:f'{x:03}',range(16,17)):
 for side in sides:
  p=src/'receipts'/n/side
  subprocess.run([sys.executable,str(src/'verify.py'),side,n],check=True,stdout=subprocess.DEVNULL)
  log=p/'pytest.log'; lines=log.read_text(errors='replace').splitlines(); outcomes=[]; failures=[]
  for line in lines:
   m=re.match(r'^(tests/.*?) (PASSED|FAILED|ERROR|SKIPPED|XFAIL|XPASS)(?:\s|$)',line)
   if m: outcomes.append({'id':m.group(1),'outcome':m.group(2)})
   if re.match(r'^(FAILED|ERROR) tests/',line): failures.append(line)
  summary=next(x for x in reversed(lines) if re.match(r'^=+ .* in [\d.]+s(?: .*?)? =+$',x))
  d={'batch':n,'side':side,'modules':(p/'module.txt').read_text().splitlines(),'pins_and_python':(p/'pins.txt').read_text().splitlines(),'toolchain':(p/'toolchain.txt').read_text().splitlines(),'start_utc':(p/'start.txt').read_text().strip(),'end_utc':(p/'end.txt').read_text().strip(),'exit':int((p/'exit.txt').read_text()),'summary':summary,'outcomes':outcomes,'failure_summary_lines':failures,'source_log_sha256':hashlib.sha256(log.read_bytes()).hexdigest(),'source_receipt_sha256':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in p.iterdir() if x.is_file() and x.name not in ('pytest.log',)}}
  if n=='004' and side=='r11':d['limitation']=(p/'overlap-disposition.txt').read_text().strip()
  (out/f'{n}-{side}.json').write_text(json.dumps(d,indent=2,ensure_ascii=True)+'\n');all_results[(n,side)]=d
matrix=[]
for n in map(lambda x:f'{x:03}',range(16,17)):
 for line in all_results[(n,'candidate')]['failure_summary_lines']:
  matching=[s for s in sides[:3] if line in all_results[(n,s)]['failure_summary_lines']]
  matrix.append({'batch':n,'candidate_failure_summary':line,'exact_matching_baselines':matching})
(out/'failure-matches.json').write_text(json.dumps(matrix,indent=2)+'\n')
print('receipts',len(all_results),'outcomes',sum(len(v['outcomes']) for v in all_results.values()),'candidate failures',len(matrix))
