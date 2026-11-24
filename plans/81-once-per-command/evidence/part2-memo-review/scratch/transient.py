"""Identical paired schedule: swap after the first index read in lookup 2, restore at lookup exit."""
import json,shutil,tempfile
from pathlib import Path
from unittest.mock import patch
from vibecomfy.workflow import VibeWorkflow,WorkflowSource
from vibecomfy.workflow_bundle import emit_bundle
from vibecomfy.porting.object_info import consume as c
def main():
    with tempfile.TemporaryDirectory() as d:
        d=Path(d)
        cache=shutil.copytree(c.CACHE_DIR,d/'cache')
        c.CACHE_DIR=cache
        idx=cache/'index.json'
        temp=cache/'invalid';temp.write_text('[]')
        original=cache/'original'
        w=VibeWorkflow('sample',WorkflowSource('sample'))
        w.add_node('ImageResizeKJ',uid='node')
        c.reset_cache()
        reader=c._resolve_class_type
        read_bytes=Path.read_bytes
        count=0
        window=False
        def read(path):
            result=read_bytes(path)
            if window and path==idx and not original.exists():
                idx.rename(original)
                temp.replace(idx)
                print('installed invalid index during lookup',count)
            return result
        def resolve(ct):
            nonlocal count,window
            count+=1
            if count!=2:return reader(ct)
            window=True
            try: return reader(ct)
            finally:
                window=False
                if original.exists():
                    original.replace(idx)
                    print('restored the original index on lookup exit')
        dest=d/'out'/'workflow.py'
        with patch.object(c,'_resolve_class_type',resolve),patch.object(Path,'read_bytes',read):
            try:
                emit_bundle(w,dest,{})
                print('OK')
            except Exception as e: print(type(e).__name__,str(e).replace(str(d),'<tmp>'))
        print('lookup',count,'files',sorted(p.name for p in dest.parent.glob('*')))
if __name__=='__main__': main()
