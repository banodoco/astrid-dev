from pathlib import Path
import ast, collections, hashlib, json
p=Path(__file__).resolve().parent
def rows(f):return [json.loads(s) for s in (p/f).read_text().splitlines()]
for suffix in ('','-cold'):
    a,b=(rows(f'{r}-templates{suffix}.jsonl') for r in ('base','head'))
    assert len(a)==len(b)==53 and {x['id'] for x in a}=={x['id'] for x in b}
    print('templates',suffix or 'ordinary', 'equal rows',sum(x==y for x,y in zip(a,b)),'of',len(a),'members',sum(len(x.get('pair',[])) for x in a),'scalar lookups',sum(x['lookups'] for x in a),'refusals',sum('failure' in x for x in a),sum('failure' in x for x in b))
for name in ('static','permission','identity','sweep'):
    a,b=(rows(f'{name}-{r}.jsonl') for r in ('base','head'))
    print(name,len(a),len(b),'fully equal',sum(x==y for x,y in zip(a,b)))
    if name=='sweep':
        total=collections.Counter()
        for x,y in zip(a,b):
            assert (x['fault'],x['at'])==(y['fault'],y['at']) and x['mutated'] and y['mutated']
            total[(tuple(x['pair']),tuple(y['pair']),x['error']==y['error'],x['lookup']==y['lookup'])]+=1
        print(total)
for r in ('base','head'):
    source=(p/r/'vibecomfy/porting/object_info/generation.py').read_bytes().splitlines(keepends=True)
    n=next(n for n in ast.parse(b''.join(source)).body if getattr(n,'name','')=='cache_file_witness')
    b=b''.join(source[n.lineno-1:n.end_lineno])
    print(r,'witness bytes',len(b),'sha256',hashlib.sha256(b).hexdigest())
    for test in ('tests','194'):
        log=(p/f'{r}-{test}.log').read_text().splitlines()
        print(r,test,log[-1].strip('= '))
        assert [s.split(' - ')[0] for s in log if s.startswith('FAILED ')]==[s.split(' - ')[0] for s in (p/f'base-{test}.log').read_text().splitlines() if s.startswith('FAILED ')]
