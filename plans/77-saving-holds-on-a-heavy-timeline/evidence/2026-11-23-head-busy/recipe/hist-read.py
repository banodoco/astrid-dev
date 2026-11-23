"""(b) history read: Timeline.open then the SDK history call, in a fresh process."""
import sys, time
from astrid.sdk.timeline.api import Timeline
from astrid.sdk.timeline.sync import _response
project, timeline = sys.argv[1], sys.argv[2]
t0 = time.time()
try:
    tl = Timeline.open(project, timeline)
    d = _response(tl.session.client.timelines.history(project, timeline, limit=100))['data']
    print('HIST_OK elapsed=%.2fs rows=%d head=%s' % (time.time() - t0, len(d['items']), d['head']['revision_id']))
except Exception as e:
    print('HIST_REFUSED type=%s elapsed=%.2fs' % (type(e).__name__, time.time() - t0))
    print('MSG', str(e)[:400])
    d = getattr(e, 'details', None)
    if d is not None:
        print('DETAILS', str(d)[:600])
