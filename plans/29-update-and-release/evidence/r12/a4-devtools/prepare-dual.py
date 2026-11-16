from pathlib import Path
import sys
p = Path(sys.argv[1])
s = p.read_text()
a = 'request:__probe.id(requestWillBeSentEvent.requestId), route:'
b = 'request:__probe.id(requestWillBeSentEvent.requestId), network:__probe.guid(requestWillBeSentEvent.requestId), route:'
c = 'request:__probe.id(event.requestId)});'
d = 'request:__probe.id(event.requestId), network:__probe.guid(event.requestId)});'
if s.count(a) != 1 or s.count(c) != 2:
    raise SystemExit('unexpected instrumentation anchors')
p.write_text(s.replace(a, b).replace(c, d))
