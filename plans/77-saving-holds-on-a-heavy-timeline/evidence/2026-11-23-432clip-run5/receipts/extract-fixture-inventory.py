#!/usr/bin/env python3
import datetime, hashlib, json
from pathlib import Path
source=Path('/root/codex/p77box/fixture/outbox-c2930794/save-loop-heavy-c2930794.json')
raw=source.read_bytes()
sha=hashlib.sha256(raw).hexdigest()
assert sha=='9346d2d69188f1793f1abff3be6e2d5abfc3eae38dbf5861ed037f69797f8943'
x=json.loads(raw)
project='23e489705d764d1497e6c9b830f55ffe'
timeline='save-loop-heavy-c2930794'
revision='authoring-parent-revision-811ee570a87ee8eb1a3fd7d94309320dd12485a2db35aef4e1f774fb6d4ad69b'
publication='txn-f3cbd404b1a0417ebc39901a3cd2b97a'
assert x['scope']['project_id']==project and x['scope']['timeline_id']==timeline
assert x['base']=={'revision_id':revision,'publication_id':publication}
assert x['pending']==[] and x['flight'] is None
commands=[]
for item in x['acknowledged'].values():
    body=json.loads(item['body'])
    assert body['project_id']==project and body['timeline_id']==timeline
    commands.extend(body['commands'])
clips=[c for c in commands if c['op']=='clip.add-media']
ids=[c['args']['row']['id'] for c in clips]
assert len(ids)==len(set(ids))==432
expected_tracks=['V1','A1','V2','V3','V4','V5','V6','A2','A3']
for c in clips:
    selections={s['key']:s for s in c['selections']}
    assert selections['collection.tracks']['order']==['parent/track:'+t for t in expected_tracks]
    assert selections['collection.occurrences']['members']==[]
    assert c['args']['row']['track'] in expected_tracks
assert len({c['op'] for c in commands if c['op']!='clip.add-media'})==1
assert len(x['acknowledged'])==37
assert clips[0]['args']['row']['id']=='fixture-image-0000' and clips[0]['args']['row']['track']=='V2'
last={s['key']:s for s in clips[-1]['selections']}
assert len(last['collection.clips']['members'])==431
inventory={'project_id':project,'timeline_id':timeline,'clip_ids':ids,'track_ids':expected_tracks,'control_clip_id':'fixture-image-0000','control_track_id':'V2','occurrence_ids':[],'revision':revision,'publication':publication,'content_digest':'sha256:5d8e8ce015e55bc0692ee906bc4d01d612e1dded960a65de75c8bfc6bc8c5036'}
out=Path('/root/codex/p77box/run5/receipts/fixture-inventory.json')
out.write_text(json.dumps(inventory,indent=2)+'\n')
result={'source':str(source),'source_sha256':sha,'inventory_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'recorded_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'acknowledged_entries':len(x['acknowledged']),'clip_commands':len(clips),'unique_clip_ids':len(set(ids)),'track_ids':expected_tracks,'occurrences_in_every_recorded_selection':0,'last_pre_command_clip_selection':len(last['collection.clips']['members']),'digest_source':'run/receipts/READY.md independently recorded canonical SHA-256; public content_digest uses sha256: prefix'}
Path('/root/codex/p77box/run5/receipts/fixture-extraction.json').write_text(json.dumps(result,indent=2)+'\n')
