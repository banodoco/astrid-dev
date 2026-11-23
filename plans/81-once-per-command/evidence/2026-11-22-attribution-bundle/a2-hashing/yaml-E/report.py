import json, gzip, sys
from collections import defaultdict
from pathlib import Path
root=Path(sys.argv[1]); manifest=json.loads((root/'manifest.json').read_text()); trial=next(t for t in manifest['trials'] if not t['warmup'] and t.get('task_state')=='succeeded'); raw=json.loads(gzip.open(root/(trial['hash_log']+'.gz'),'rt').read()); events=[e for e in raw['events'] if e['kind'] in ('yaml.safe_load','yaml.load')]
out=['# E YAML parse observation — A-2 source', '', 'One instrumented process. The safe_load wrapper suppresses its nested load wrapper, so each observed public parse is counted once. Durations may overlap across threads and include parsing, not necessarily only YAML CPU. Direct Loader construction, aliases bound before instrumentation and subprocesses/daemon are outside this observer. Path.read_text links by object identity; open streams use their actual name. Unknown paths remain unknown; fixture basenames may alias. Metadata equality at observations does not prove content equality.', '',f"Wall {trial['wall_seconds']:.6f} s; peak RSS {raw['max_rss_kib']} KiB; peak retained bytes {raw['peak_retained_bytes']}; Runtime/target receipts `{trial['task_id']}` / `{trial['target_prompt_id']}`; [raw events]({trial['hash_log']}.gz).",'', '| API | Count | Unknown path | Sum duration s |', '| --- | ---: | ---: | ---: |']
for kind in ('yaml.safe_load','yaml.load'):
 a=[e for e in events if e['kind']==kind];out.append(f"| {kind} | {len(a)} | {sum(e['path'] is None for e in a)} | {sum(e['elapsed_ns'] for e in a)/1e9:.6f} |")
groups=defaultdict(list)
for e in events:groups[(e['kind'],tuple(e['caller']),e['path'] or '<unknown>')].append(e)
out += ['', '| API | Caller | File path | Count | Sum duration s | Equal before/after metadata | All repeated observations match |', '| --- | --- | --- | ---: | ---: | ---: | --- |']
for (kind,caller,path),items in sorted(groups.items(),key=lambda q:(-sum(i['elapsed_ns'] for i in q[1]),q[0])):
 equal=sum(e.get('metadata_before') is not None and e['metadata_before']==e.get('metadata_after') for e in items); metadata=[tuple(m) for e in items for m in (e.get('metadata_before'),e.get('metadata_after')) if m is not None]; across='unknown' if len(metadata)!=2*len(items) or path.startswith('<fixture>/') else 'yes' if len(set(metadata))==1 else 'no'
 out.append(f"| {kind} | {caller[0]}:{caller[1]} `{caller[2]}` | {path} | {len(items)} | {sum(e['elapsed_ns'] for e in items)/1e9:.6f} | {equal}/{len(items)} | {across} |")
(root/'yaml-attribution.md').write_text('\n'.join(out)+'\n')
