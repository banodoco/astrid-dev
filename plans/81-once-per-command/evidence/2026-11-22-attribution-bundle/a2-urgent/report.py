#!/usr/bin/env python3
"""Rank actual single-process A-2 cProfile measurements; no wall scaling."""
import gzip, json, pstats, tempfile
from pathlib import Path
root=Path(__file__).resolve().parent / 'profile'
manifest=json.loads((root/'manifest.json').read_text())
out=['# A-2 urgent source cProfile: one measured process per route', '', 'One cProfile sample per route, with profiling overhead. Self and cumulative seconds below are measured inside the profiled process; cumulative rows overlap. cProfile starts after interpreter and profiler bootstrap and does not directly explain all startup or process-exit seconds. The exact collector span is unavailable; the sum of exclusive timing rows is its available proxy. Outer wall minus that sum is an external residual including clock rounding and profiling/exit overhead, not an identified stage. Optional py-spy follows CLI subprocesses but does not follow the already-running Runtime/host and excludes idle threads by default.', '']
for route in 'WIE':
 t=next(r for r in manifest['trials'] if r['route']==route and not r['warmup'] and r.get('task_state')=='succeeded')
 data=json.loads((root/t['stdout']).read_text()); rows=data['timings']; assert data['start']=='process start'
 profile_path=root/(t['profile']+'.gz')
 with gzip.open(profile_path, 'rb') as compressed, tempfile.NamedTemporaryFile(suffix='.prof') as raw:
  raw.write(compressed.read()); raw.flush(); stats=pstats.Stats(raw.name)
 out += [f'## {route}', '', f"Outer spawn-to-exit {t['wall_seconds']:.6f} s; Runtime response emission {(t['admission_ns']-t['spawn_ns'])/1e9:.6f} s; target response emission {(t['target_ack_ns']-t['spawn_ns'])/1e9:.6f} s; timing start: {data['start']}; exact collector span unavailable; sum of exclusive timing rows {sum(r['seconds'] for r in rows):.6f} s; estimated external residual {t['wall_seconds']-sum(r['seconds'] for r in rows):.6f} s. Task `{t['task_id']}`, target prompt `{t['target_prompt_id']}`. Raw: [{profile_path.name}]({profile_path.name}), [{t['stdout']}]({t['stdout']}).", '', '| Stage | Parent | Self s | Inclusive s |', '| --- | --- | ---: | ---: |']
 for r in sorted(rows,key=lambda r:(-r.get('total_seconds',r['seconds']),r['stage'])):
  total=r.get('total_seconds'); out.append(f"| {r['stage']} | {r.get('parent') or '—'} | {r['seconds']:.6f} | {total:.6f} |" if total is not None else f"| {r['stage']} | {r.get('parent') or '—'} | {r['seconds']:.6f} | unknown |")
 for label,index in [('Self',2),('Cumulative',3)]:
  out += ['',f'### cProfile {label}', '', '| Function | Calls | Self s | Cumulative s |', '| --- | ---: | ---: | ---: |']
  entries=sorted(stats.stats.items(),key=lambda item:(-item[1][index],item[0]))[:40]
  for (filename,line,name),(_,calls,self_s,cum_s,_) in entries:
   out.append(f'| {filename}:{line}({name}) | {calls} | {self_s:.6f} | {cum_s:.6f} |')
 out.append('')
(root/'ranked-profile.md').write_text('\n'.join(out)+'\n')
