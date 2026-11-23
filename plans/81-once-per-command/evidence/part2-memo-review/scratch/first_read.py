"""Change one real pack at its first parser boundary inside a public bundle."""
import json,shutil,sys,tempfile
from pathlib import Path
from unittest.mock import patch
from vibecomfy.porting.object_info import consume as c
from vibecomfy.workflow import VibeWorkflow,WorkflowSource
from vibecomfy.workflow_bundle import emit_bundle
def main():
    with tempfile.TemporaryDirectory() as tmp:
        d=Path(tmp); cache=shutil.copytree(c.CACHE_DIR,d/'cache');c.CACHE_DIR=cache
        w=VibeWorkflow('probe',WorkflowSource('probe'));w.add_node('ImageResizeKJ',uid='one')
        c.reset_cache()
        idx=json.loads((cache/'index.json').read_bytes()); victim=idx['ImageResizeKJ']
        old=c.read_json; done=False; reads=0
        def read(root,name,**kw):
            nonlocal reads,done
            if name!=victim:return old(root,name,**kw)
            reads+=1
            if done:return old(root,name,**kw)
            done=True
            if sys.argv[1]=='before':
                (root/name).write_text('[]')
                return old(root,name,**kw)
            result=old(root,name,**kw)
            (root/name).write_text('[]')
            return result
        dest=d/'out'/'workflow.py'
        with patch.object(c,'read_json',read):
            try:emit_bundle(w,dest,{});print('OK')
            except Exception as e:print(type(e).__name__,str(e).replace(tmp,'<tmp>'))
        print('pack parser calls',reads,'changed',done,'pair',dest.is_file(),dest.with_suffix('.vibe.json').is_file())
if __name__=='__main__':main()
