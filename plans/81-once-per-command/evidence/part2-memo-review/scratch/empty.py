"""Unused but unresolvable configured cache path on an empty canonical workflow."""
import shutil,sys,tempfile
from pathlib import Path
from unittest.mock import patch
from vibecomfy.workflow import VibeWorkflow, WorkflowSource
from vibecomfy import workflow_bundle as wb
from vibecomfy.porting.object_info import consume as c
def main():
    with tempfile.TemporaryDirectory() as tmp:
        d=Path(tmp)
        cache=shutil.copytree(c.CACHE_DIR,d/'cache')
        root=d/'configured'
        root.symlink_to(root.name if sys.argv[1]=='loop' else cache)
        c.CACHE_DIR=root
        hits=[]
        def record():
            hits.append(1)
            return original()
        original=c._sync_reader
        dest=d/'dest'/'workflow.py'
        with patch.object(c,'_sync_reader',record):
            try:
                workflow=VibeWorkflow('empty',WorkflowSource('empty'))
                if 'cas' in sys.argv[2:]:
                    wb.emit_bundle_with_candidate(workflow,dest,{},None,expected_members={dest:'stale'})
                else:
                    wb.emit_bundle(workflow,dest,{})
                print('OK')
            except Exception as e:print(type(e).__name__,str(e).replace(str(d),'<tmp>'))
        print('reader syncs',len(hits),'files',sorted(p.name for p in dest.parent.glob('*')))
if __name__=='__main__':main()
