"""Differential for a stable valid JSON provider with one unused nested value."""
import sys,json,shutil,tempfile
from pathlib import Path
from unittest.mock import patch
from vibecomfy.porting.object_info import consume as c
from vibecomfy.workflow import VibeWorkflow,WorkflowSource
from vibecomfy.workflow_bundle import emit_bundle
def main():
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        cache=root/'cache'
        shutil.copytree(c.CACHE_DIR,cache)
        c.CACHE_DIR=cache
        # Start with exactly the shipped provider; append an unused JSON metadata field.
        idx=json.loads((cache/'index.json').read_bytes())
        pack=cache/idx['ImageResizeKJ']
        data=pack.read_bytes().rstrip()
        assert data[-1:]==b'}'
        w=VibeWorkflow('probe',WorkflowSource('probe'))
        w.add_node('ImageResizeKJ',uid='stable')
        for depth in map(int,sys.argv[1:]):
            pack.write_bytes(data[:-1]+b',"review_metadata":{"unused":'+b'['*depth+b'0'+b']'*depth+b'}}')
            c.reset_cache()
            dest=root/str(depth)/'workflow.py'
            try:
                emit_bundle(w,dest,{})
                print(depth,'OK',dest.is_file(),flush=True)
            except Exception as e:
                print(depth,type(e).__name__,str(e),dest.is_file(),flush=True)
if __name__=='__main__': main()
