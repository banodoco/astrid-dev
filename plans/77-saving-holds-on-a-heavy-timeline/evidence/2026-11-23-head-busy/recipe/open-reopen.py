"""(c) editor-style reopen: two sequential SDK Timeline.open calls in one fresh process (as open-read.py, twice)."""
import sys, time
from astrid.sdk.timeline.api import Timeline
project, timeline = sys.argv[1], sys.argv[2]
for n in (1, 2):
    t0 = time.time()
    try:
        Timeline.open(project, timeline)
        print('REOPEN%d_OK elapsed=%.2fs' % (n, time.time() - t0))
    except Exception as e:
        print('REOPEN%d_REFUSED type=%s elapsed=%.2fs' % (n, type(e).__name__, time.time() - t0))
        print('MSG', str(e)[:400])
        d = getattr(e, 'details', None)
        if d is not None:
            print('DETAILS', str(d)[:600])
