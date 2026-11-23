"""A real capture reads its public schema_provider before entering the nested writer."""
import hashlib,json,os,shutil,sys,tempfile
from pathlib import Path
from unittest.mock import patch
from vibecomfy import workflow_bundle as wb
from vibecomfy.schema.provider import ObjectInfoIndexSchemaProvider
from vibecomfy.porting.object_info import consume as c
def main():
    with tempfile.TemporaryDirectory() as tmp:
        d=Path(tmp); cache=shutil.copytree(c.CACHE_DIR,d/'capture-cache')
        c.CACHE_DIR=shutil.copytree(c.CACHE_DIR,d/'scalar-cache')
        raw={'workflow_id':'capture-repro','1':{'class_type':'ImageResizeKJ','inputs':{}}}
        provider=ObjectInfoIndexSchemaProvider(cache)
        victim=cache/json.loads((cache/'index.json').read_bytes())['ImageResizeKJ']
        opened=[]
        def evt(event,args):
            if event=='open' and args[0]==str(victim) and 'r' in str(args[1]): opened.append(1)
        sys.addaudithook(evt)
        sha=wb._sha256_file
        changed=False
        def digest(p):
            nonlocal changed
            result=sha(p)
            if not changed:
                assert opened
                changed=True
                victim.write_text('[]')
            return result
        if hasattr(c,'_BundleClassMemo'):
            validate=c._BundleClassMemo.validate
            def checked(owner,*args):
                if not args: print('final includes capture provider?',victim in owner.witnesses)
                return validate(owner,*args)
            c._BundleClassMemo.validate=checked
        dest=d/'out'/'workflow.py'
        with patch.object(wb,'_sha256_file',digest):
            try:
                b=wb.capture_bundle(raw,dest,{},schema_provider=provider)
                node=next(iter(b.workflow.nodes.values()))
                print('OK captured node',node.class_type,'schema data',node.metadata.get('schema_status'),node.native_output_names)
            except Exception as e: print(type(e).__name__,str(e).replace(str(d),'<tmp>'))
        print('capture pack read',len(opened),'changed',changed,'output',dest.is_file(),dest.with_suffix('.vibe.json').is_file())
if __name__=='__main__': main()
