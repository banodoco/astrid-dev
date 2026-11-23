import sys, time
from astrid.sdk.timeline.api import Timeline
project, timeline = sys.argv[1], sys.argv[2]
t0 = time.time()
try:
    tl = Timeline.open(project, timeline)
    print('OPEN_OK elapsed=%.2fs' % (time.time() - t0))
except Exception as e:
    print('OPEN_REFUSED type=%s elapsed=%.2fs' % (type(e).__name__, time.time() - t0))
    print('MSG', str(e)[:300])
    d = getattr(e, 'details', None)
    if d is not None:
        print('DETAILS', str(d)[:300])
