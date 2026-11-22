#!/usr/bin/env python3
"""Rank actual single-process A-2 cProfile measurements; no wall scaling."""
import gzip, json, pstats, tempfile
from pathlib import Path
root=Path(__file__).resolve().parent / 'profile'
manifest=json.loads((root/'manifest.json').read_text())
out=['# A-2 urgent source cProfile: one measured process per route', '', 'One cProfile sample per route, with profiling overhead. Self and cumulative seconds below are measured inside the profiled process; cumulative rows overlap. cProfile starts after interpreter and profiler bootstrap and does not directly explain all startup or process-exit seconds. The exact collector span is unavailable; the sum of exclusive timing rows is its available proxy. Outer wall minus that sum is an external residual including clock rounding and profiling/exit overhead, not an identified stage. Optional py-spy follows CLI subprocesses but does not follow the already-running Runtime/host and excludes idle threads by default.', 'Applicability labels are inferred from cited source code, not measured as a source-vs-installed comparison. The timings and cProfile rows are source-run observations. The timed pack host source identity stage is `both`: astrid/sdk/host_bootstrap.py:2142,2171-2175 executes that stage in installed mode too, which also adds the verifier at astrid/core/source_identity.py:102-124. `both` means shared code, not equal timing. `unknown` means installed applicability is not established by this evidence. No installed savings are inferred; the separately reported 4.397 s cache_file_witness digest-call total is not classified source-only.', '']
for route in 'WIE':
 t=next(r for r in manifest['trials'] if r['route']==route and not r['warmup'] and r.get('task_state')=='succeeded')
 data=json.loads((root/t['stdout']).read_text()); rows=data['timings']; assert data['start']=='process start'
 profile_path=root/(t['profile']+'.gz')
 with gzip.open(profile_path, 'rb') as compressed, tempfile.NamedTemporaryFile(suffix='.prof') as raw:
  raw.write(compressed.read()); raw.flush(); stats=pstats.Stats(raw.name)
 out += [f'## {route}', '', f"Outer spawn-to-exit {t['wall_seconds']:.6f} s; Runtime response emission {(t['admission_ns']-t['spawn_ns'])/1e9:.6f} s; target response emission {(t['target_ack_ns']-t['spawn_ns'])/1e9:.6f} s; timing start: {data['start']}; exact collector span unavailable; sum of exclusive timing rows {sum(r['seconds'] for r in rows):.6f} s; estimated external residual {t['wall_seconds']-sum(r['seconds'] for r in rows):.6f} s. Task `{t['task_id']}`, target prompt `{t['target_prompt_id']}`. Raw: [{profile_path.name}]({profile_path.name}), [{t['stdout']}]({t['stdout']}).", '', '| Stage | Parent | Self s | Inclusive s | Code applicability (inferred) |', '| --- | --- | ---: | ---: | --- |']
 for r in sorted(rows,key=lambda r:(-r.get('total_seconds',r['seconds']),r['stage'])):
  stage=r['stage']
  if stage=='pack host source identity': app='both; inferred: astrid/sdk/host_bootstrap.py:2142,2171-2175; installed verifier also at astrid/core/source_identity.py:102-124'
  elif stage=='other command work': app='unknown; aggregated collector remainder at astrid/sdk/command_timing.py:64'
  elif stage.startswith(('Runtime GET ','Runtime POST ')): app='both; inferred: shared client methods in astrid_runtime_client/generated.py:723-729,822,1251-1280,1540'
  else:
   refs={'Runtime acquisition lock':'astrid/sdk/autobootstrap.py:463-465','in-process Runtime acquisition lock':'astrid/sdk/autobootstrap.py:465','pack host attachment':'astrid/sdk/autobootstrap.py:524','pack host readiness':'astrid/sdk/host_bootstrap.py:2230-2241','pack host lifecycle lock':'astrid/sdk/host_bootstrap.py:2241','pack discovery':'astrid/core/pack/discovery.py:366','entry discovery':'astrid/sdk/generation.py:1744-1745','entry lookup':'astrid/sdk/generation.py:1066,1731-1751','model registry':'astrid/sdk/generation.py:623-626','target check':'astrid/sdk/generation.py:884,1825-1900','workflow build':'astrid/sdk/generation.py:470,1900-1976','Runtime launcher connection':'astrid/sdk/client.py:392-410,469-471'}
   app=f"both; inferred: {refs[stage]}" if stage in refs else 'unknown; generic collector only, astrid/sdk/command_timing.py:140-168'
  total=r.get('total_seconds'); out.append(f"| {stage} | {r.get('parent') or '—'} | {r['seconds']:.6f} | {total:.6f} | {app} |" if total is not None else f"| {stage} | {r.get('parent') or '—'} | {r['seconds']:.6f} | unknown | {app} |")
 for label,index in [('Self',2),('Cumulative',3)]:
  out += ['',f'### cProfile {label}', '', 'Per-function applicability is `unknown`: this evidence has source-checkout profiles only and no matched installed profile. The function file and line are the code citation; 4.397 s from cache_file_witness is a separate digest-call observation, not proof of source-only behavior.', '', '| Function | Calls | Self s | Cumulative s | Code applicability (inferred) |', '| --- | ---: | ---: | ---: | --- |']
  entries=sorted(stats.stats.items(),key=lambda item:(-item[1][index],item[0]))[:40]
  for (filename,line,name),(_,calls,self_s,cum_s,_) in entries:
   out.append(f'| {filename}:{line}({name}) | {calls} | {self_s:.6f} | {cum_s:.6f} | unknown; installed applicability unverified |')
 out.append('')
(root/'ranked-profile.md').write_text('\n'.join(out)+'\n')
