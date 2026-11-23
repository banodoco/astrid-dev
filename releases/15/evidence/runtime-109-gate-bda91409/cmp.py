import re,sys,os
root=sys.argv[1]
TS=re.compile(r'^﻿?\d{4}-\d\d-\d\dT[\d:.]+Z ?')
TOT=re.compile(r'^(=+ )?\d+ (failed|passed|error|errors|skipped).* in [\d.]+s.*')
def parse(p):
    lines=[TS.sub('',l.rstrip('\n')) for l in open(p,errors='replace')]
    idx=[i for i,l in enumerate(lines) if 'short test summary info' in l]
    if not idx: return None,None
    ids=set();tot=None
    for l in lines[idx[-1]+1:]:
        if l.startswith(('FAILED ','ERROR ')):
            ids.add(l.split(' ',1)[1].split(' - ')[0].strip())
        elif TOT.match(l): tot=l.strip();break
    return ids,tot
rows=[];out=[]
for f in sorted(os.listdir(root+'/base')):
    b,bt=parse(f'{root}/base/{f}')
    c,ct=parse(f'{root}/cand/{f}') if os.path.exists(f'{root}/cand/{f}') else (None,'MISSING')
    print('##',f,'\nbase:',len(b) if b is not None else None,bt,'\ncand:',len(c) if c is not None else None,ct)
    if b is not None and c is not None:
        print('NEW:',*sorted(c-b),sep='\n  ');print('GONE:',*sorted(b-c),sep='\n  ')
