import sys,re
# Resolve conflicts: default keep both sides (ours then theirs); for lines starting with "| <ID> " present on both sides, keep the side named by PREFER[ID] (ours/theirs), else ours.
path=sys.argv[1]; prefer=dict(a.split('=') for a in sys.argv[2:])
out=[];state=None;ours=[];theirs=[]
for line in open(path).read().split('\n'):
    if line.startswith('<<<<<<< '): state='o';ours=[];theirs=[];continue
    if line.startswith('=======') and state=='o': state='t';continue
    if line.startswith('>>>>>>> ') and state=='t':
        def rid(l):
            m=re.match(r'\| ([A-Z]+[0-9.]+) ',l); return m.group(1) if m else None
        tids={rid(l):l for l in theirs if rid(l)}; oids={rid(l) for l in ours if rid(l)}
        res=[]
        for l in ours:
            i=rid(l)
            if i and i in tids: res.append(tids[i] if prefer.get(i)=='theirs' else l)
            else: res.append(l)
        res+= [l for l in theirs if not (rid(l) and rid(l) in oids)]
        out+=res; state=None; continue
    (ours if state=='o' else theirs if state=='t' else out).append(line)
open(path,'w').write('\n'.join(out))
