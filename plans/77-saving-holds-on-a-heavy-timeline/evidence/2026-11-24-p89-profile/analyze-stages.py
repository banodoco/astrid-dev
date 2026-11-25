import json,sys,collections
SRC=('source/','astrid/')
def analyze(f):
    d=json.load(open(f)); fr=d['shared']['frames']
    def fl(i): return fr[i]['file'].split('/')[-1]
    def hascommit(s): return any('timeline_commit' in fr[i]['file'] for i in s)
    best=None
    for p in d['profiles']:
        if 'MainThread' in p['name']: continue
        cs=[s for s in p['samples'] if s and hascommit(s)]
        if best is None or len(cs)>len(best[0]): best=(cs,p['name'])
    cs,name=best
    def stage(s):
        for i in s:
            if fl(i)=='timeline_commit_port.py' and fr[i]['name']=='accept': return 'port_store_accept'
        ex=[fr[i]['line'] for i in s if fl(i)=='timeline_commit_execution.py' and fr[i]['name']=='_execute']
        if ex:
            l=ex[0]
            if l>=650: return 'durable_reconciliation'
            if 615<=l<=640: return 'provider_commit'
            if 598<=l<612: return 'initial_replay_lookup'
        return 'handler/other'
    def cat(i):
        x=fr[i]; nm=x['name']; full=x['file']; f1=fl(i)
        if '/json/' in full and f1 in('encoder.py','decoder.py','__init__.py','scanner.py'): return 'json encode/decode'
        if nm=='value_equal' or f1=='copy.py' or f1=='timeline_commit_producer.py': return 'copy/compare'
        if f1 in('validators.py','_keywords.py','_utils.py') and 'jsonschema' in full: return 'jsonschema'
        if f1 in('timeline_commit_auth.py','timeline_commit_validation.py'): return 'auth/value validation'
        if nm.startswith('_verify_accepted') or nm in('_history_chain','_accepted_replay'): return 'old-history verification'
        if f1 in('_commit_patch.py','_doc_patch.py'): return 'patch capture/payload'
        if nm in('fetchone','fetchall','executemany','executescript') or 'sqlite' in full: return 'sqlite'
        return None
    tab=collections.defaultdict(collections.Counter); stot=collections.Counter()
    sites=collections.defaultdict(collections.Counter)
    for s in cs:
        st=stage(s); stot[st]+=1
        c=None;k=len(s)
        for j in range(len(s)-1,-1,-1):
            c=cat(s[j])
            if c: k=j;break
        if c=='copy/compare':
            anc=[fr[i]['name']+' '+fl(i) for i in s[:k]]
            c='copy/compare via covers' if any(a.startswith('covers timeline_commit_auth') for a in anc) else ('copy/compare via patch capture' if any(a.startswith(('payload _doc_patch','capture _commit_patch')) for a in anc) else 'copy/compare via other callers')
        if not c:
            # call site: innermost frame in Runtime/Agent source
            c='other'
            for j in range(len(s)-1,-1,-1):
                x=fr[j] if False else fr[s[j]]
                if '/source/' in x['file'] or '/astrid/' in x['file']:
                    sites[st][f"{x['name']} {fl(s[j])}:{x['line']}"]+=1; break
        tab[st][c]+=1
    return name,len(cs),stot,tab,sites
for f in sys.argv[1:]:
    name,n,stot,tab,sites=analyze(f)
    print('==',f.split('/')[-1].replace('.speedscope.json',''),name,'commit-thread %.1fs'%(n*0.01))
    for st in ('provider_commit','port_store_accept','durable_reconciliation','initial_replay_lookup','handler/other'):
        if not stot[st]: continue
        print('  %-24s %5.2f s'%(st,stot[st]*0.01))
        for c,v in tab[st].most_common(): print('       %5.2f  %s'%(v*0.01,c))
        for k,v in sites[st].most_common(5): print('       other call site %5.2f  %s'%(v*0.01,k))
