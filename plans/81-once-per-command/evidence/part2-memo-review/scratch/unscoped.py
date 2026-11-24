"""Public re-render/copy paths that use the pair publisher directly."""
import json,shutil,sys,tempfile,runpy
from pathlib import Path
from unittest.mock import patch
from vibecomfy.workflow import VibeWorkflow,WorkflowSource
from vibecomfy import workflow_bundle as wb,templates
from vibecomfy.porting.object_info import consume as c
from vibecomfy.schema import provider as sp
from vibecomfy.cli import main as cli

def main():
    mode=sys.argv[1]
    with tempfile.TemporaryDirectory() as d:
        d=Path(d)
        cache=shutil.copytree(c.CACHE_DIR,d/'cache');c.CACHE_DIR=cache
        sp._default_object_info_index_root=lambda:cache
        src=d/'original'/'workflow.py';src.parent.mkdir()
        if mode=='copy':
            from vibecomfy.cli_loader import load_workflow_any
            w=load_workflow_any('image/qwen_image_2_1_turbo')
            wb.emit_bundle(w,src,{})
            dest=d/'new'/'workflow.py'
            def act(): print('CLI exit',cli(['copy-to-recipe',str(src),'--out',str(dest)]))
        else:
            test=runpy.run_path('tests/test_runtime_reconciliation.py')
            w=test['_bundle'](src.parent).workflow
            initial=wb.emit_bundle(w,src,{'operation':'authored','provenance':{'source':'test'}})
            bound=wb._make_bundle(w,python_path=src,ui_sidecar=initial.ui_sidecar,provenance=initial.provenance,operation='authored')
            dest=src
            def act():
                result=test['reconcile_before_queue'](bound,target_schema_provider=test['_LiveProvider'](),publish=True)
                print('successor',result.changed)
        before=dest.read_bytes() if dest.is_file() else None
        c.reset_cache()
        templates._ready_native_schema_carrier.cache_clear()
        templates._ready_schema_provider.cache_clear()
        victim=cache/'index.json'
        opened=[]
        def hook(event,args):
            if event=='open' and args[0]==str(victim) and 'r' in str(args[1]): opened.append(1)
        sys.addaudithook(hook)
        changed=False
        sha=wb._sha256_file
        def digest(path):
            nonlocal changed
            result=sha(path)
            if path.parent==dest.parent and path.name.startswith('.') and not changed:
                if not opened:
                    print('no object-info read before digest')
                    return result
                print('prior index opens',len(opened))
                victim.write_text('[]');changed=True
            return result
        with patch.object(wb,'_sha256_file',digest):
            try: act()
            except Exception as e: print(type(e).__name__,str(e).replace(str(d),'<tmp>'))
        print('changed',changed,'new bytes published',dest.is_file() and dest.read_bytes()!=before,'pair',dest.is_file(),dest.with_suffix('.vibe.json').is_file())
if __name__=='__main__':main()
