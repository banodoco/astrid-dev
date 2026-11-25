import json,sys,collections
def groups(f):
    d=json.load(open(f)); fr=d['shared']['frames']
    def hascommit(s): return any('timeline_commit' in fr[i]['file'] or 'timeline_commit' in fr[i]['name'] for i in s)
    best=None
    for p in d['profiles']:
        if 'MainThread' in p['name']: continue
        cs=[s for s in p['samples'] if s and hascommit(s)]
        if best is None or len(cs)>len(best[0]): best=(cs,p['name'])
    cs,name=best
    def cat(i):
        x=fr[i]; fl=x['file'].split('/')[-1]; nm=x['name']; full=x['file']
        if '/json/' in full and fl in('encoder.py','decoder.py','__init__.py','scanner.py'): return 'json encode/decode'
        if nm=='value_equal' or fl=='copy.py' or (fl=='timeline_commit_producer.py'): return 'record copy/compare (value_equal, deepcopy)'
        if fl in('validators.py','_keywords.py','_utils.py') and 'jsonschema' in full: return 'validation: jsonschema'
        if fl in('timeline_commit_auth.py','timeline_commit_validation.py'): return 'validation: commit auth/value'
        if nm.startswith('_verify_accepted') or fl=='timeline_commit_history.py': return 'old-history verification (_verify_accepted*)'
        if fl in('_commit_patch.py','_doc_patch.py'): return 'patch capture/payload (_commit_patch, _doc_patch)'
        if nm in('fetchone','fetchall','executemany','executescript') or ('sqlite' in full): return 'sqlite'
        return None
    tot=collections.Counter(); resid=collections.Counter()
    for s in cs:
        c=None
        for i in reversed(s):
            c=cat(i)
            if c: break
        if c: tot[c]+=1
        else:
            # residual attribute to the innermost frame within runtime_protocol/astrid sources
            k=None
            for i in reversed(s):
                x=fr[i]
                if 'source/' in x['file'] or 'astrid' in x['file']:
                    k=f"{x['name']} {x['file'].split('/')[-1]}:{x['line']}"; break
            resid[k or 'stdlib/other']+=1
    return len(cs),tot,resid,name
for f in sys.argv[1:]:
    n,tot,resid,name=groups(f)
    print('==',f.split('/')[-1],name,'commit-thread samples %.1fs'%(n*0.01))
    s=0
    for k,v in tot.most_common(): print('  %6.2f  %4.1f%%  %s'%(v*0.01,100*v/n,k)); s+=v
    r=n-s
    print('  %6.2f  %4.1f%%  other (not matched above)'%(r*0.01,100*r/max(n,1)))
    for k,v in resid.most_common(6): print('        %6.2f %s'%(v*0.01,k))
