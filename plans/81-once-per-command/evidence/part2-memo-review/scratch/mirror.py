"""Replace one cache dependency with a different valid answer, at a named boundary."""
import json, shutil, sys, tempfile
from pathlib import Path
from unittest.mock import patch
from contextlib import ExitStack
from vibecomfy.workflow import VibeWorkflow,WorkflowSource
from vibecomfy import workflow_bundle as wb
from vibecomfy.porting.object_info import consume as c
import vibecomfy.porting.emit as emit
source=c.CACHE_DIR
name='ImageResizeKJ'
def run(kind, when):
    with tempfile.TemporaryDirectory() as d:
        d=Path(d)
        cache=shutil.copytree(source,d/'original')
        root=d/'configured'
        root.symlink_to(cache)
        c.CACHE_DIR=root
        index=json.loads((cache/'index.json').read_bytes())
        pack=cache/index[name]
        data=json.loads(pack.read_bytes())
        data[name]['description']='different valid schema description'
        changed_pack=json.dumps(data).encode()
        if kind=='index':
            (cache/'other.json').write_bytes(changed_pack)
        if kind=='root':
            alt=shutil.copytree(cache,d/'alternative')
            (alt/pack.name).write_bytes(changed_pack)
        def mutate():
            if kind=='pack':
                tmp=pack.with_suffix('.replacement');tmp.write_bytes(changed_pack);tmp.replace(pack)
            elif kind=='index':
                index[name]='other.json'
                tmp=cache/'new-index';tmp.write_text(json.dumps(index));tmp.replace(cache/'index.json')
            elif kind=='root':
                new=d/'new-link';new.symlink_to(alt);new.replace(root)
        counter=0
        renders=0
        digests=0
        trace=[]
        armed=True
        def fire(label):
            nonlocal armed
            if label==when and armed:
                armed=False
                mutate()
        orig=c._resolve_class_type
        def resolve(ct):
            nonlocal counter
            counter+=1
            fire('before-first' if counter==1 else 'before-second' if counter==2 else '-')
            answer=orig(ct)
            val='new' if answer and answer.get('description')==data[name]['description'] else 'old'
            if not trace or trace[-1]!=val: trace.append(val)
            return answer
        sha=wb._sha256_file
        def digest(p):
            nonlocal digests
            x=sha(p);digests+=1
            fire('digest')
            return x
        render=emit.emit_scratchpad_python
        def rendered(*a,**k):
            nonlocal renders
            r=render(*a,**k);renders+=1
            if renders==2: fire('after-render')
            return r
        dest=d/'out'/'workflow.py'
        wf=VibeWorkflow('sample',WorkflowSource('sample'))
        wf.add_node(name,uid='stable')
        c.reset_cache()
        with ExitStack() as stack:
            for obj,key,val in ((c,'_resolve_class_type',resolve),(wb,'_sha256_file',digest),(emit,'emit_scratchpad_python',rendered)):
                stack.enter_context(patch.object(obj,key,val))
            try:
                wb.emit_bundle(wf,dest,{})
                error=None
            except Exception as e:
                error=[type(e).__name__,str(e).replace(str(d),'<tmp>')]
        return dict(kind=kind,when=when,mutated=not armed,lookups=counter,render=renders,digests=digests,reads=trace,error=error,files=sorted(p.name for p in dest.parent.glob('*')))
if __name__=='__main__':
    for kind in ('pack','index','root'):
        for when in ('before-first','before-second','after-render','digest'):
            print(json.dumps(run(kind,when)),flush=True)
