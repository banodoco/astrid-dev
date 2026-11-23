"""One public emit with a shipped provider pack at the standard supplemental location."""
import json, os, shutil, sys, tempfile, warnings
from pathlib import Path
from unittest.mock import patch
from vibecomfy.workflow import VibeWorkflow, WorkflowSource
from vibecomfy import workflow_bundle as wb
from vibecomfy.porting.object_info import consume as c
from vibecomfy.schema import provider as sp
from vibecomfy.errors import ObjectInfoCacheCorruptError

def main():
    mode = sys.argv[1]
    name = 'ImageResizeKJ'
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        os.chdir(d)
        shutil.copytree(c.CACHE_DIR, 'cache')
        c.CACHE_DIR = d/'cache'
        sp._default_object_info_index_root = lambda: c.CACHE_DIR
        os.environ['VIBECOMFY_ON_DEMAND_SCHEMAS']='0'
        schema = Path('out/cache/object_info.snapshot.json')
        schema.parent.mkdir(parents=True)
        index_path = c.CACHE_DIR/'index.json'
        index = json.loads(index_path.read_bytes())
        shutil.copyfile(c.CACHE_DIR/index.pop(name), schema)
        index_path.write_text(json.dumps(index))
        w = VibeWorkflow('probe',WorkflowSource('probe'))
        w.add_node(name,uid='stable').metadata['_ui']={'outputs':[{'name':'IMAGE','type':'IMAGE'}]}
        target = Path('dest/workflow.py')
        c.reset_cache()
        reads = []
        def hook(event,args):
            if event == 'open' and isinstance(args[0], str) and Path(args[0]).absolute() == schema.absolute():
                reads.append(args[1])
        sys.addaudithook(hook)
        sha = wb._sha256_file
        def digest(path):
            result = sha(path)
            if mode == 'changed' and reads and not changed:
                changed.append(True)
                schema.write_text('[]')
            return result
        changed = []
        def validate(owner,*args,**kwargs):
            if not args:
                print('final witnessed supplemental?',schema.absolute() in owner.witnesses,'observed',*[p.name for p in owner.witnesses])
            return original(owner,*args,**kwargs)
        if hasattr(c,'_BundleClassMemo'):
            original = c._BundleClassMemo.validate
            c._BundleClassMemo.validate = validate
        with patch.object(wb,'_sha256_file',digest):
            try:
                wb.emit_bundle(w,target,{})
                print('OK')
            except Exception as e:
                print(type(e).__name__,str(e))
        print('supplemental opens',reads,'changed',bool(changed),'output',target.exists(),target.with_suffix('.vibe.json').exists())
if __name__ == '__main__': main()
