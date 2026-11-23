import sys, json
from astrid.sdk.timeline.api import Timeline
from astrid.sdk.timeline.sync import _response
from astrid.sdk.workspace_client import WorkspaceClientError
project, timeline = sys.argv[1], sys.argv[2]
t = Timeline.open(project, timeline) if False else None
from astrid.sdk.timeline.api import Timeline as T
try:
    s = T.open(project, timeline)
    print('OPEN_OK')
except WorkspaceClientError as e:
    print('CODE', e.code if hasattr(e,'code') else '', 'ARGS', [str(a)[:120] for a in e.args])
    d = getattr(e, 'details', None) or {}
    print('DETAIL_KEYS', sorted(d.keys()) if isinstance(d, dict) else type(d))
    if isinstance(d, dict):
        for k in sorted(d.keys()):
            print(' ', k, '=', json.dumps(d[k], default=str)[:300])
