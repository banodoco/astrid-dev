"""The schema provider of a real staged ready-wrapper has its own warm dependencies."""
import json,os,shutil,sys,tempfile
from pathlib import Path
from unittest.mock import patch
from vibecomfy.cli_loader import load_workflow_any
from vibecomfy import workflow_bundle as wb,templates
from vibecomfy.schema import provider as sp
from vibecomfy.porting.object_info import consume as c
def main():
    with tempfile.TemporaryDirectory() as d:
        d=Path(d)
        cache=shutil.copytree(c.CACHE_DIR,d/'cache');c.CACHE_DIR=cache
        sp._default_object_info_index_root=lambda:cache
        w=load_workflow_any('image/qwen_image_2_1_turbo')
        templates._ready_schema_provider.cache_clear()
        templates._ready_native_schema_carrier.cache_clear()
        pp=templates._ready_schema_provider()
        assert pp.get_schema('ImageResizeKJ')
        victim=cache/json.loads((cache/'index.json').read_bytes())['ImageResizeKJ']
        c.reset_cache()
        activity=[]
        def hook(event,args):
            if event=='open' and args[0]==str(victim) and 'r' in str(args[1]):
                activity.append(1)
        sys.addaudithook(hook)
        orig=wb._sha256_file
        changed=False
        def sha(path):
            nonlocal changed
            r=orig(path)
            if not changed:
                assert activity, 'warmed supplemental pack was not read'
                victim.write_text('[]');changed=True
            return r
        if hasattr(c,'_BundleClassMemo'):
            val=c._BundleClassMemo.validate
            def check(owner,*args):
                if not args:print('final includes spare?',victim in owner.witnesses,'memo',owner.memo_allowed)
                return val(owner,*args)
            c._BundleClassMemo.validate=check
        dest=d/'out'/'workflow.py'
        with patch.object(wb,'_sha256_file',sha):
            try:wb.emit_bundle(w,dest,{});print('OK')
            except Exception as e:print(type(e).__name__,str(e))
        print('supplemental reads',len(activity),'changed',changed,'output',dest.exists(),dest.with_suffix('.vibe.json').exists())
if __name__=='__main__':main()
