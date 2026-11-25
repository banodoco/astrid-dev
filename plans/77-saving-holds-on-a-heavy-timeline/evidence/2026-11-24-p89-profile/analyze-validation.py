import json,sys,collections
def run(f):
    d=json.load(open(f)); fr=d['shared']['frames']
    def fl(i): return fr[i]['file'].split('/')[-1]
    best=None
    for p in d['profiles']:
        if 'MainThread' in p['name']: continue
        cs=[s for s in p['samples'] if s and any('timeline_commit' in fr[i]['file'] for i in s)]
        if best is None or len(cs)>len(best[0]): best=(cs,p['name'])
    cs,name=best; n=len(cs)
    def cnt(pred): return sum(1 for s in cs if any(pred(i) for i in s))
    out=collections.OrderedDict()
    out['commit thread s']=n*0.01
    out['under timeline_commit_validation.py']=cnt(lambda i:fl(i)=='timeline_commit_validation.py')*0.01
    out['under validate_commit_value']=cnt(lambda i:fr[i]['name']=='validate_commit_value')*0.01
    out['under any jsonschema frame']=cnt(lambda i:'jsonschema' in fr[i]['file'])*0.01
    out['under jsonschema descend']=cnt(lambda i:'jsonschema' in fr[i]['file'] and fr[i]['name']=='descend')*0.01
    out['under jsonschema iter_errors']=cnt(lambda i:'jsonschema' in fr[i]['file'] and fr[i]['name']=='iter_errors')*0.01
    for nm in ('_remember_success','_subtree_bytes','_has_subtree_recursion_headroom','_memoized_reference','_reviewed_item_nodes','_schema_resources'):
        out['frame '+nm]=cnt(lambda i,nm=nm:fr[i]['name']==nm and fl(i)=='timeline_commit_validation.py')*0.01
    # frames of timeline_commit_validation.py by name with seconds
    names=collections.Counter()
    for s in cs:
        seen=set()
        for i in s:
            if fl(i)=='timeline_commit_validation.py':
                k=f"{fr[i]['name']}:{fr[i]['line']}"
                if k not in seen: names[k]+=1; seen.add(k)
    return name,out,names
for f in sys.argv[1:]:
    name,out,names=run(f)
    print('==',f.split('/')[-1].replace('.speedscope.json',''),name)
    for k,v in out.items(): print('   %-40s %6.2f'%(k,v))
    print('   timeline_commit_validation.py frames (inclusive s):', ', '.join(f'{k} {v*0.01:.2f}' for k,v in names.most_common(8)))
