import json, sys
routes, failed, internal, independent = {}, [], set(), set()
collision = False
for line in open(sys.argv[1], encoding='utf8'):
    if line.startswith('PROBE '):
        event = json.loads(line[6:]); name = event['event']
        if name == 'created': routes[event['route']] = event.get('network')
        elif name in ('loading-failed', 'loading-finished'): internal.add(event.get('network'))
        elif name in ('fail-invalid-id', 'fail-invalid-state', 'fail-other'): failed.append(event['route'])
        elif name == 'collision': collision = True
    elif line.startswith('DUAL '):
        event = json.loads(line[5:]); name = event['event']
        if name in ('loadingFailed', 'loadingFinished'): independent.add(event.get('network'))
        elif name == 'collision': collision = True
if collision:
    raise SystemExit('Invalid probe: digest collision')
requests = [routes.get(route) for route in failed]
if any(request is None for request in requests):
    raise SystemExit('Invalid probe: missing request correlation')
print('rejected aborts:', len(requests), 'internal terminal missing:', sum(x not in internal for x in requests), 'independent terminal missing:', sum(x not in independent for x in requests), 'independent-only terminals:', sum(x not in internal and x in independent for x in requests))
