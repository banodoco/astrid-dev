"""A nonempty public emit on an already malformed committed generation."""
import shutil,sys,tempfile
from pathlib import Path
from unittest.mock import patch
from vibecomfy.workflow import VibeWorkflow,WorkflowSource
from vibecomfy.workflow_bundle import emit_bundle
from vibecomfy.porting.object_info import consume as c

def main():
    with tempfile.TemporaryDirectory() as tmp:
        d=Path(tmp);cache=shutil.copytree(c.CACHE_DIR,d/'cache');c.CACHE_DIR=cache
        w=VibeWorkflow('sample',WorkflowSource('sample'));w.add_node('ImageResizeKJ',uid='one')
        (cache/'CURRENT').write_text('v1')
        gens=cache/'generations'
        if sys.argv[1]=='parent':gens.symlink_to('generations')
        else:gens.mkdir();(gens/'v1').symlink_to('v1')
        c.reset_cache()
        dest=d/'out'/'workflow.py'
        for run in range(2):
            try:emit_bundle(w,dest,{});print('OK')
            except Exception as e:print(type(e).__name__,str(e).replace(tmp,'<tmp>'))
            print('members',dest.is_file(),dest.with_suffix('.vibe.json').is_file())
if __name__=='__main__':main()
