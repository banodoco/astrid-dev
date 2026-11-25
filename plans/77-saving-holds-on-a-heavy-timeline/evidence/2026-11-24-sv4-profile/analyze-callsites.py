import json,sys,collections
def run(f):
    d=json.load(open(f)); fr=d['shared']['frames']
    def fl(i): return fr[i]['file'].split('/')[-1]
    best=None
    for p in d['profiles']:
        if 'MainThread' in p['name']: continue
        cs=[s for s in p['samples'] if s and any('timeline_commit' in fr[i]['file'] for i in s)]
        if best is None or len(cs)>len(best[0]): best=(cs,p['name'])
    cs,name=best
    def stage(s):
        for i in s:
            if fl(i)=='timeline_commit_port.py' and fr[i]['name']=='accept': return 'port_store_accept'
        ex=[fr[i]['line'] for i in s if fl(i)=='timeline_commit_execution.py' and fr[i]['name']=='_execute']
        if ex:
            return 'durable_reconciliation' if ex[0]>=690 else ('provider_commit' if 655<=ex[0]<=680 else 'other')
        return 'other'
    def lib(i):
        f=fr[i]['file']
        return ('jsonschema' in f) or fl(i) in('copy.py',) or fr[i]['name'] in('value_equal','<genexpr>','<listcomp>') or fl(i) in('timeline_commit_producer.py',) or '/json/' in f
    res=collections.defaultdict(collections.Counter)
    for s in cs:
        st=stage(s)
        if st=='other': continue
        # category of leaf
        k=None
        for j in range(len(s)-1,-1,-1):
            f=fr[s[j]]['file']
            if 'jsonschema' in f: cat='jsonschema'; k=j; break
            if fr[s[j]]['name']=='value_equal' or fl(s[j])=='copy.py': cat='copy/compare'; k=j; break
            if '/json/' in f: cat='json'; k=j; break
        else: continue
        # call site = nearest ancestor (towards root) that is in runtime/agent source and not a library helper
        site=None
        for j in range(k,-1,-1):
            x=fr[s[j]]; f=x['file']
            if ('/source/' in f or '/astrid/' in f) and not lib(s[j]):
                site=f"{x['name']} {fl(s[j])}:{x['line']}"; break
        res[(st,cat)][site or '?']+=1
    return name,res
for f in sys.argv[1:]:
    name,res=run(f)
    print('==',f.split('/')[-1].replace('.speedscope.json',''))
    for (st,cat),c in sorted(res.items(), key=lambda kv:-sum(kv[1].values())):
        tot=sum(c.values())
        if tot<25: continue
        print('  %-18s %-13s %5.2f s'%(st,cat,tot*0.01))
        for k,v in c.most_common(3): print('       %5.2f  %s'%(v*0.01,k))
