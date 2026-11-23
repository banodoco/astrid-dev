#!/usr/bin/env python3
"""Summarize identity-linked hash and YAML observations without content claims."""
from collections import defaultdict
import json, gzip, sys
from pathlib import Path
ROOT=Path(sys.argv[1])
x=json.loads((ROOT/'manifest.json').read_text())
out=['# A-2 CLI hashing and YAML observations', '', 'One instrumented measured process per route, not cProfile. Only the CLI process is instrumented; its launcher subprocess, already-running Runtime/host, native direct/OpenSSL constructors and unobserved file-read APIs are blind spots. SHA-256 and file_digest are separate: file_digest time includes file reads and must not be summed as pure hash time. Path.read_bytes correlations use retained object identity, never proximity; file_digest uses its stream name. Unmatched paths remain unknown. Fixture basename paths may alias and are excluded from distinct/repeat claims. Metadata equality means device/inode/size/mtime/ctime matched at observations, not that contents are equal. Observer hooks, up to 8 MiB retained data, YAML preload and JSON logging inside process-exit wall add overhead. Observer self time below covers only part of SHA wrapper bookkeeping, not the whole observer. Durations are sums of observed calls, may overlap across threads and may double-count work inherited by copied hash objects; they do not partition wall or establish savings. Byte totals omit unknown byte counts.', '']
def family(p):
 if not p:return 'unknown'
 if p.startswith('<fixture>/'):return 'fixture basename (ambiguous)'
 for prefix,label in [('/root/codex/plan-81m/profile-a2/','Agent'),('/root/codex/plan-81m/VibeComfy/','VibeComfy'),('/root/codex/plan-81m/a4-runtime/','Runtime')]:
  if p.startswith(prefix):return label
 return 'other'
for route in 'WIE':
 t=next(r for r in x['trials'] if r['route']==route and not r['warmup'] and r.get('task_state')=='succeeded')
 raw=json.loads(gzip.open(ROOT/(t['hash_log']+'.gz'),'rt').read()); ev=raw['events']; timing=json.loads((ROOT/t['stdout']).read_text())
 out += [f'## {route}', '', f"Outer wall {t['wall_seconds']:.6f} s; start provenance {timing.get('start')}; Runtime response emission {(t['admission_ns']-t['spawn_ns'])/1e9:.6f} s; target response emission {(t['target_ack_ns']-t['spawn_ns'])/1e9:.6f} s; peak RSS {raw['max_rss_kib']} KiB; peak retained bytes {raw['peak_retained_bytes']}. Task `{t['task_id']}`; prompt `{t['target_prompt_id']}`. [Raw events]({t['hash_log']}.gz).", '']
 for kind in ('sha256','sha256.file_digest','yaml.safe_load'):
  subset=[e for e in ev if e['kind']==kind]; out += [f'### {kind}', '', f"Events: {len(subset)}; unmatched path: {sum(e['path'] is None for e in subset)}; byte count unknown: {sum(e.get('bytes') is None for e in subset)}; summed observed call time {sum(e['elapsed_ns'] for e in subset)/1e9:.6f} s; partial observer time {str(round(sum(e.get('observer_ns',0) for e in subset)/1e9, 6))+' s' if kind=='sha256' else 'not measured'}.", '', '| Caller | File family | Count | Bytes observed | Elapsed s |', '| --- | --- | ---: | ---: | ---: |']
  groups=defaultdict(lambda:[0,0,0])
  for e in subset:
   key=(tuple(e['caller']),family(e['path'])); row=groups[key];row[0]+=1;row[1]+=e.get('bytes') or 0;row[2]+=e['elapsed_ns']
  for (caller,fam), (count,size,ns) in sorted(groups.items(),key=lambda q:(-q[1][2],q[0])):
   out.append(f"| {caller[0]}:{caller[1]} `{caller[2]}` | {fam} | {count} | {size} | {ns/1e9:.6f} |")
  files=defaultdict(list)
  for e in subset:
   if family(e['path']) not in ('unknown','fixture basename (ambiguous)'):files[e['path']].append(e)
  repeated=sum(len(v)>1 for v in files.values()); out += ['', f'Exact identifiable paths: {len(files)}; paths observed more than once: {repeated}.', '', '| Path | Count | Bytes observed | Elapsed s | Equal before/after metadata observations | All repeated observations match |', '| --- | ---: | ---: | ---: | ---: | --- |']
  for path,items in sorted(files.items(),key=lambda q:(-sum(i['elapsed_ns'] for i in q[1]),q[0])):
   equal=sum(e.get('metadata_before') is not None and e['metadata_before']==e.get('metadata_after') for e in items)
   metadata=[tuple(m) for e in items for m in (e.get('metadata_before'),e.get('metadata_after')) if m is not None]
   across='unknown' if len(metadata)!=2*len(items) else 'yes' if len(set(metadata))==1 else 'no'
   out.append(f"| {path} | {len(items)} | {sum(e.get('bytes') or 0 for e in items)} | {sum(e['elapsed_ns'] for e in items)/1e9:.6f} | {equal}/{len(items)} | {across} |")
  out.append('')
(ROOT/'hash-attribution.md').write_text('\n'.join(out)+'\n')
