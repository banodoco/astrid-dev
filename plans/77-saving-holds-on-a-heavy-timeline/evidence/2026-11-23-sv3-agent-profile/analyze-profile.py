import json,sys,collections
def analyze(f):
    d=json.load(open(f)); fr=d['shared']['frames']
    def hascommit(s): return any('timeline_commit' in fr[i]['file'] or 'timeline_commit' in fr[i]['name'] for i in s)
    best=None
    for p in d['profiles']:
        if 'MainThread' in p['name']: continue
        cs=[s for s in p['samples'] if s and hascommit(s)]
        if best is None or len(cs)>len(best[0]): best=(cs,p['name'])
    cs,name=best
    def fl(i): return fr[i]['file'].split('/')[-1]
    def cat(i):
        x=fr[i]; nm=x['name']; full=x['file']; f1=fl(i)
        if '/json/' in full and f1 in('encoder.py','decoder.py','__init__.py','scanner.py'): return 'json encode/decode'
        if nm=='value_equal' or f1=='copy.py' or f1=='timeline_commit_producer.py': return 'copy/compare'
        if f1 in('validators.py','_keywords.py','_utils.py') and 'jsonschema' in full: return 'validation: jsonschema'
        if f1 in('timeline_commit_auth.py','timeline_commit_validation.py'): return 'validation: commit auth/value'
        if nm.startswith('_verify_accepted'): return 'old-history verification'
        if f1 in('_commit_patch.py','_doc_patch.py'): return 'patch capture/payload'
        if nm in('fetchone','fetchall','executemany','executescript') or 'sqlite' in full: return 'sqlite'
        return None
    tot=collections.Counter()
    for s in cs:
        c=None; k=len(s)
        for j in range(len(s)-1,-1,-1):
            c=cat(s[j])
            if c: k=j; break
        if c=='copy/compare':
            anc=[fr[i]['name']+' '+fl(i) for i in s[:k]]
            if any(a.startswith('covers timeline_commit_auth') for a in anc): c='copy/compare via auth.covers'
            elif any(a.startswith('payload _doc_patch') or a.startswith('capture _commit_patch') for a in anc): c='copy/compare via patch capture/payload'
            else: c='copy/compare via other callers'
        tot[c or 'other']+=1
    selfc=collections.Counter(); callers=collections.defaultdict(collections.Counter)
    for s in cs:
        leaf=s[-1]; k=f"{fr[leaf]['name']} {fl(leaf)}:{fr[leaf]['line']}"
        selfc[k]+=1
        ch=' < '.join(f"{fr[i]['name']} {fl(i)}:{fr[i]['line']}" for i in reversed(s[-4:-1]))
        callers[k][ch]+=1
    return name,len(cs),tot,selfc,callers
out=[]
for f in sys.argv[1:]:
    name,n,tot,selfc,callers=analyze(f)
    print('==',f.split('/')[-1].replace('.speedscope.json',''),name,'commit-thread %.1fs'%(n*0.01))
    for k,v in tot.most_common(): print('  %6.2f  %4.1f%%  %s'%(v*0.01,100*v/n,k))
    print('  top 15 self frames (seconds) with callers:')
    for k,v in selfc.most_common(15):
        c,cv=callers[k].most_common(1)[0]
        print('   %5.2f %s   <= %s (%.2f)'%(v*0.01,k,c,cv*0.01))
