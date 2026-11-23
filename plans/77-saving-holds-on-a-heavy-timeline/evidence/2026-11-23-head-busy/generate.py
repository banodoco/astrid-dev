"""Generate a synthetic timeline through the installed Astrid SDK."""
import os
from astrid.sdk.timeline.api import Timeline

PROJECT = os.environ.get('LE4_PROJECT', 'le4-synthetic')
TIMELINE = os.environ.get('LE4_TIMELINE', 'heavy')
tl = Timeline.open(PROJECT, TIMELINE)
def seed(t):
    for i in range(int(os.environ.get('LE4_PANELS','120'))):
        t.add_text(f'SYNTHETIC PANEL {i+1:03d}', at=float(os.environ.get('LE4_PANEL_START','240'))+i*2, hold=1.8,
                   track=f'titles-{i%4+1}', id=f'panel-{i+1:03d}')
r = tl.commit(seed, label='Build synthetic timeline', idempotency_key=f"{PROJECT}-seed-v1")
print('ok',r.get('ok'),'receipt',r.get('receipt',{}).get('receipt_id'),'head',r.get('data',{}).get('accepted_revision_id'))
