import re,sys,os,glob,json
G=sys.argv[1]; os.chdir(G)
totre=re.compile(r'^=*\s*(\d+ (?:failed|passed|error)[^=]*? in [\d.]+s[^=]*?)\s*=*$')
def parse(path,prefix=''):
    L=open(path,errors='replace').read().split('\n')
    tot=[l for l in L if totre.match(l)]
    end=max(i for i,l in enumerate(L) if totre.match(l))
    ids={}
    start=max(i for i,l in enumerate(L[:end]) if re.match(r'^=+ short test summary info',l)) if any(re.match(r'^=+ short test summary info',l) for l in L[:end]) else 0
    for l in L[start:end]:
        m=re.match(r'^(FAILED|ERROR) (\S.*)$',l)
        if not m: continue
        k,rest=m.groups(); tid=rest.split(' - ',1)[0].strip()
        if not tid.startswith('tests'): continue
        ids.setdefault((k,prefix+tid),rest.partition(' - ')[2][:200])
    return ids,L[end].strip('= ')
def ids_of(dir_,names):
    out={};tl={}
    for n in names:
        i,t=parse(f'{dir_}/{n}.log','darwin: ' if n=='darwin' else '')
        out[n]=i; tl[n]=t
    return out,tl
def load_base(p): return {tuple(l.rstrip('\n').split('\t',1)) for l in open(p) if l.strip()}
if sys.argv[2]=='ci':
    names=[f'shard{i}' for i in range(1,9)]+['darwin']
    cand,tl=ids_of('logs/ci',names)
    base=load_base('baseline-ci.tsv')
    allc={}
    for n in names:
        for k,v in cand[n].items(): allc.setdefault(k,(n,v))
    C=set(allc)
    for n in names:
        nf=sum(1 for k in cand[n] if k[0]=='FAILED'); ne=sum(1 for k in cand[n] if k[0]=='ERROR')
        print(n,'ids F/E',nf,ne,'|',tl[n])
    new=sorted(C-base); gone=sorted(base-C)
    print('cand F/E',sum(k=='FAILED' for k,_ in C),sum(k=='ERROR' for k,_ in C),'base F/E',sum(k=='FAILED' for k,_ in base),sum(k=='ERROR' for k,_ in base))
    print('NEW',len(new)); [print(k,t,'|',allc[(k,t)][0],'|',allc[(k,t)][1]) for k,t in new]
    print('GONE',len(gone)); [print(k,t) for k,t in gone]
    open('ci-cand-ids.tsv','w').write(''.join(f'{k}\t{t}\n' for k,t in sorted(C)))
else:
    names=['int1','int2','int3','int4','optin']
    a,ta=ids_of('logs/lanes-cand',names); b,tb=ids_of('logs/lanes-base',names)
    for n in names:
        A=set(a[n]);B=set(b[n])
        print('==',n,'cand F/E',sum(k=='FAILED' for k,_ in A),sum(k=='ERROR' for k,_ in A),'|',ta[n]); print('   base F/E',sum(k=='FAILED' for k,_ in B),sum(k=='ERROR' for k,_ in B),'|',tb[n])
        new=sorted(A-B);gone=sorted(B-A)
        print('NEW',len(new)); [print(' ',k,t,'|',a[n][(k,t)]) for k,t in new]
        print('GONE',len(gone)); [print(' ',k,t,'|',b[n][(k,t)]) for k,t in gone]
