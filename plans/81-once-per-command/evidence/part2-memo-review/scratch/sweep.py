"""Exhaust the 60 public scalar lookup boundaries of the two-node fixture."""
import hashlib,json,os,shutil,sys,tempfile
from pathlib import Path
from unittest.mock import patch
from vibecomfy.workflow import VibeWorkflow,WorkflowSource
from vibecomfy.workflow_bundle import emit_bundle
from vibecomfy.porting.object_info import consume as c

def main():
    origin=c.CACHE_DIR
    with tempfile.TemporaryDirectory() as tmp:
        t=Path(tmp)
        cache=shutil.copytree(origin,t/'cache')
        c.CACHE_DIR=cache
        index=json.loads((cache/'index.json').read_bytes())
        first=cache/index['LoadImage']
        second=cache/index['ImageResizeKJ']
        idx=cache/'index.json'
        w=VibeWorkflow('sample',WorkflowSource('sample'))
        w.add_node('LoadImage',uid='first');w.add_node('ImageResizeKJ',uid='second')
        dest=t/'dest'/'workflow.py'
        for fault in sys.argv[1:] or ('first','second','both','index','missing','unused'):
            for at in range(1,61):
                c.reset_cache()
                seen=[]
                orig=c._resolve_class_type
                changed=[]
                def resolve(ct):
                    seen.append(ct)
                    if len(seen)==at:
                        paths={'first':[first],'second':[second],'both':[first,second],'index':[idx],'missing':[second],'unused':[cache/'LanPaint@2.1.0.json']}[fault]
                        for p in paths:
                            changed.append(p)
                            if fault=='missing':p.unlink()
                            else:p.write_bytes(b'[' if p==first else b'[]')
                    return orig(ct)
                with patch.object(c,'_resolve_class_type',resolve):
                    try:
                        b=emit_bundle(w,dest,{})
                        error=None
                    except Exception as exc:
                        error=[type(exc).__name__,str(exc).replace(str(t),'<tmp>')]
                print(json.dumps(dict(fault=fault,at=at,lookup=len(seen),error=error,mutated=bool(changed),pair=[dest.exists(),dest.with_suffix('.vibe.json').exists()],files=sorted(p.name for p in dest.parent.glob('*')))),flush=True)
                for p in changed:shutil.copyfile(origin/p.name,p)
                if dest.parent.exists():shutil.rmtree(dest.parent)
if __name__=='__main__':main()
