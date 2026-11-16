from pathlib import Path
import collections, hashlib, json, zipfile
import xml.etree.ElementTree as ET

root=Path(__file__).parent
repo=root.parents[2]/'p39-repair/astrid-runtime'
oldroot=root.parent/'xml-reconciliation'
mapping={
 133603709482:(14269247265,oldroot/'ci-portability-ubuntu-14263697451/portability-lifecycle.xml',133548963714),
 133603709490:(14272675371,oldroot/'ci-unit-ubuntu-14263361597/unit.xml',133548963731),
 133603709503:(14272008264,oldroot/'ci-process-control-14263048850/sandbox-process-control.xml',133548963680),
 133603709524:(14272245594,oldroot/'ci-portability-macos-14264336834/portability-lifecycle.xml',133548963837),
 133603709671:(14272906578,oldroot/'ci-unit-macos-14265574916/unit.xml',133548963937),
}
def read_xml(path):
 tree=ET.parse(path)
 suites=list(tree.iter('testsuite'))
 totals={k:sum(int(s.attrib.get(k,0)) for s in suites) for k in ('tests','failures','errors','skipped')}
 rows={}
 for t in tree.iter('testcase'):
  classname=t.get('classname',''); name=t.get('name',''); parts=classname.split('.')
  node=None
  for n in range(len(parts),0,-1):
   file='/'.join(parts[:n])+'.py'
   if (repo/file).is_file():
    node=file+'::'+'::'.join([*parts[n:],name]);break
  if node is None: node=classname+'::'+name
  assert node not in rows,('duplicate testcase ID',node,path)
  bad=t.find('error'); status='error'
  if bad is None: bad=t.find('failure');status='failure'
  if bad is None:
   bad=t.find('skipped');status='skipped'
   if bad is not None and 'xfail' in bad.get('type','').lower():status='xfailed'
  if bad is None:status='passed'
  rows[node]={'nodeid':node,'classname':classname,'name':name,'status':status,'message':bad.get('message','') if bad is not None else None,'detail':bad.text if bad is not None else None}
 return totals,rows

summary=[]; all_cases=[]; all_changes=[]
for job,(artifact,oldxml,oldjob) in mapping.items():
 report=json.loads((root/f'job-{job}.json').read_text())
 archive=root/f'artifact-{artifact}.zip';digest=hashlib.sha256(archive.read_bytes()).hexdigest()
 assert 'sha256:'+digest==report['junit_artifact']['digest']
 with zipfile.ZipFile(archive) as z:
  names=[n for n in z.namelist() if n.endswith('.xml')]
  assert len(names)==1
  name=Path(names[0]);assert not name.is_absolute() and '..' not in name.parts
  dest=root/f'xml-{artifact}'/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(z.read(names[0]))
 totals,cases=read_xml(dest);oldtotals,oldcases=read_xml(oldxml)
 expected=report['junit_summary']
 assert all(totals[k]==expected[k] for k in totals),(job,totals,expected)
 assert len(cases)+report['pytest_counts'].get('subtests passed',0)==totals['tests']
 red={r['nodeid']:r['outcome'].lower() for r in report['outer_outcomes']}
 assert len(red)==totals['failures']+totals['errors']
 assert {n:('failed' if r['status']=='failure' else 'error') for n,r in cases.items() if r['status'] in ('error','failure')}==red
 common=set(cases)&set(oldcases); added=sorted(set(cases)-set(oldcases)); removed=sorted(set(oldcases)-set(cases))
 trans=collections.Counter((oldcases[n]['status'],cases[n]['status']) for n in common)
 changes=[{'job_id':job,'prior_job_id':oldjob,'nodeid':n,'prior_status':oldcases[n]['status'],'new_status':cases[n]['status'],'prior_message':oldcases[n]['message'],'new_message':cases[n]['message']} for n in sorted(common) if oldcases[n]['status']!=cases[n]['status']]
 all_changes.extend(changes)
 all_cases.append({'job_id':job,'prior_job_id':oldjob,'current_testcases':list(cases.values()),'prior_xml':str(oldxml.relative_to(root.parent))})
 item={'job_id':job,'prior_job_id':oldjob,'name':report['provenance']['job_name'],'summary':report['pytest_summary'],'artifact_id':artifact,'artifact_sha256':digest,'xml_totals':totals,'testcase_records':len(cases),'passing_subtests_in_root_total':report['pytest_counts'].get('subtests passed',0),'status_counts':dict(collections.Counter(r['status'] for r in cases.values())),'old_xml_totals':oldtotals,'same_testcase_ids':not added and not removed,'common_testcase_ids':len(common),'added_ids':added,'removed_ids':removed,'transitions':{a+'->'+b:n for (a,b),n in sorted(trans.items())},'distinct_literal_message_groups':report['distinct_literal_message_count'],'ownership_waiting':report['ownership_waiting']}
 summary.append(item)
 report['junit_artifact'].update({'downloaded':True,'verified_sha256':digest,'xml_file':str(dest.relative_to(root)),'testcase_count':len(cases),'all_failed_ids_reconciled':True})
 report['limitations']=[s for s in report['limitations'] if not s.startswith('JUnit XML was not downloaded')]
 report['limitations'].append('Downloaded XML and archive digest verified; passing subtests appear in suite totals but have no separate testcase element.')
 (root/f'job-{job}.json').write_text(json.dumps(report,indent=2)+'\n')
 md=root/f'job-{job}.md';text=md.read_text()
 text=text.replace('The archive was not downloaded; the emitted JUnit totals above were reconciled to pytest.', 'The archive was downloaded, its SHA-256 matched GitHub metadata, and XML totals and every failure/error ID were reconciled to the log. See XML reconciliation for subtest accounting and exact-ID comparison.')
 text=text.replace('- JUnit XML was not downloaded; totals are the always-run summary emitted in the job log.','- Actual downloaded XML was reconciled to log totals and every failure/error ID. Passing subtests appear in suite totals but not as individual testcase elements.')
 md.write_text(text)
 (root/f'job-{job}-status-comparison.json').write_text(json.dumps({'summary':item,'changed':changes,'unchanged_ids':[n for n in sorted(common) if oldcases[n]['status']==cases[n]['status']]},indent=2)+'\n')

totals=collections.Counter()
for s in summary:
 totals.update(s['transitions'])
measurement={'repository':'banodoco/astrid-runtime','head_sha':'359e2d7e55369562ca9513557282ea8aff7645bc','tree_sha':'0291fadcde521650fdc71257a9ec2fd61b7226a4','run_id':43954031461,'attempt':1,'prior_head_sha':'4fe2c0b847cf83771b2f3ce4e4fba0934f64f6ce','prior_run_id':43938386357,'classification':'provisional post-batch measurement; phase1/G2/RS1 incomplete','failed_job_count':5,'failure_error_records':sum(s['xml_totals']['failures']+s['xml_totals']['errors'] for s in summary),'literal_per_job_message_groups':sum(s['distinct_literal_message_groups'] for s in summary),'transition_counts_per_job_occurrence':dict(totals),'all_same_testcase_sets':all(s['same_testcase_ids'] for s in summary),'jobs':summary}
(root/'measurement.json').write_text(json.dumps(measurement,indent=2)+'\n')
(root/'testcase-index.json').write_text(json.dumps(all_cases,indent=2)+'\n')
(root/'changed-testcases.json').write_text(json.dumps(all_changes,indent=2)+'\n')
lines=['# Runtime CI 43954031461 — provisional post-batch measurement','',f"Exact head `{measurement['head_sha']}`, tree `{measurement['tree_sha']}`, attempt1. Prior comparable CI43938386357 at4fe2c0b. Five failed jobs, **{measurement['failure_error_records']} failure/error records** and **{measurement['literal_per_job_message_groups']} per-job distinct full literal-message groups**. All five actual XML archives verified against GitHub SHA-256 metadata; every failure/error ID matches the raw log.",'','| Job | Job ID | Complete pytest summary | Message groups |','|---|---|---|---:|']
for s in summary:lines.append(f"| {s['name']} | [{s['job_id']}](https://github.com/banodoco/astrid-runtime/actions/runs/43954031461/job/{s['job_id']}) | {s['summary']} | {s['distinct_literal_message_groups']} |")
lines+=['','The other jobs: boundary, typescript-client, windows-realm-publication and darwin-native passed; landing reference was skipped. Exact statuses are retained in jobs-attempt-1.json.','','## Same-ID comparison','',f"All five jobs have identical testcase ID sets to their corresponding previous jobs: **{measurement['all_same_testcase_sets']}**. Counts below count job occurrences, so the same test on several platforms is counted several times.",'','| Prior -> current | Count |','|---|---:|']
for k,v in sorted(totals.items()):lines.append(f'| {k} | {v} |')
lines+=['','A prior error that now reaches a failing assertion is newly exposed behavior, not automatically a product regression. Changed-testcases.json contains every exact changed ID and both messages. The paired per-job Markdown/JSON reports contain all literal messages with counts and triage or new, including ownership holds.','','## Artifact reconciliation','', '| Job ID | Artifact ID | Archive SHA-256 | XML tests | Testcase records | Passing subtests without separate elements |','|---|---|---|---:|---:|---:|']
for s in summary:lines.append(f"| {s['job_id']} | [{s['artifact_id']}](https://github.com/banodoco/astrid-runtime/actions/runs/43954031461/artifacts/{s['artifact_id']}) | `{s['artifact_sha256']}` | {s['xml_totals']['tests']} | {s['testcase_records']} | {s['passing_subtests_in_root_total']} |")
lines+=['','Expected xfails are included in XML skipped totals. The three broad jobs include60 passing subtests in suite totals without individual testcase elements; this is reconciled, not a missing-case claim. Raw logs, actual XML and the complete testcase index are retained outside the repository evidence package for the separate evidence archive. Formal RS1 remains0/1; this report is not acceptance or proof that every cause is understood.']
(root/'README.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({k:v for k,v in measurement.items() if k!='jobs'},indent=2))
