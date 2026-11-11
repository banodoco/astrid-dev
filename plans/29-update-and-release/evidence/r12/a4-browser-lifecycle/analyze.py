import json, sys
begin, rejected, commits, routes, terminals, clients = {}, [], [], {}, set(), {}
for line in open(sys.argv[1], encoding='utf8'):
    if line.startswith('COMMIT '):
        commits.append(int(line.split()[1])); continue
    if line.startswith('CLIENT '):
        e = json.loads(line[7:]); clients.setdefault(e['guid'], []).append(e['event']); continue
    if not line.startswith('PROBE '): continue
    e = json.loads(line[6:]);
    if e['event'] == 'collision': raise SystemExit('Invalid probe: GUID digest collision')
    k = e.get('route')
    if e['event'] == 'created': routes[k] = (e['request'], e['guid'])
    if e['event'] == 'fail-begin': begin[k] = e['time']
    if e['event'] in ('fail-invalid-id', 'fail-invalid-state', 'fail-other'): rejected.append((k, begin.get(k), e['time']))
    if e['event'] in ('loading-failed', 'loading-finished'): terminals.add(e['request'])
matched = [(k, a, b, routes.get(k)) for k, a, b in rejected if a is not None and routes.get(k) is not None and any(a <= t <= b for t in commits)]
missing = [r for r in matched if r[3][0] not in terminals]
client_failed = [r for r in missing if 'requestfailed' in clients.get(r[3][1], [])]
client_missing = [r for r in missing if clients.get(r[3][1]) == ['request']]
print('commits:', len(commits), 'rejected:', len(rejected), 'across observed commit:', len(matched), 'without CDP terminal:', len(missing), 'client requestfailed despite missing CDP terminal:', len(client_failed), 'client terminal missing:', len(client_missing))
