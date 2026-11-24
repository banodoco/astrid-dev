"""Wrap the unchanged shipped cache in a correctly hashed generation."""
import hashlib, json, os, shutil, sys, tempfile
from pathlib import Path
from unittest.mock import patch
from vibecomfy.workflow import VibeWorkflow, WorkflowSource
from vibecomfy import workflow_bundle as wb
from vibecomfy.porting.object_info import consume as c, generation as gen
from vibecomfy.schema import provider as sp

def setup(cache):
    active = cache/'generations'/'v1'
    active.mkdir(parents=True)
    shutil.copytree(c.CACHE_DIR,active,dirs_exist_ok=True)
    manifest = {f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(active.glob('*.json'))}
    (active/'manifest.json').write_text(json.dumps(dict(generation='v1',format_version=1,files=manifest)))
    (cache/'CURRENT').write_text('v1')
    return active

def main():
    scenario, mutation = sys.argv[1:3]
    supplemental = scenario in ('supplemental','supplemental_early')
    warmed = scenario != 'cold'
    with tempfile.TemporaryDirectory() as d:
        d=Path(d)
        os.chdir(d)
        cache=d/'cache'
        active=setup(cache)
        c.CACHE_DIR = cache
        sp._default_object_info_index_root = lambda:cache
        os.environ['VIBECOMFY_ON_DEMAND_SCHEMAS']='0'
        name='ImageResizeKJ'
        if warmed:
            assert c.get_class(name)
        w=VibeWorkflow('probe',WorkflowSource('probe'))
        node=w.add_node(name,uid='stable')
        if supplemental:
            node.metadata['_ui']={'outputs':[{'name':'IMAGE','type':'IMAGE'}]}
        victim=active/mutation
        if not warmed:
            c.reset_cache()
            gen._VALIDATED_GENERATIONS.clear()
        elif supplemental:
            # Invalidate the generation's stat-only fast path before emission.
            # All input bytes and all manifest hashes are still correct.
            ts=victim.stat()
            os.utime(victim,ns=(ts.st_atime_ns,ts.st_mtime_ns+1000000000))
        sha=wb._sha256_file
        audit=[]
        def hook(event,args):
            if event=='open' and isinstance(args[0],str) and Path(args[0]).absolute() == victim and 'r' in str(args[1]):
                if not audit or audit[-1] != 'read':
                    audit.append('read')
        sys.addaudithook(hook)
        changed=[]
        def change():
            print('mutation after',audit)
            victim.write_text('[]')
            changed.append(True)
        def digest(path):
            result=sha(path)
            if not changed:
                change()
            return result
        if hasattr(c,'_BundleClassMemo'):
            original=c._BundleClassMemo.validate
            def validate(owner,*args):
                if not args:
                    print('final victim recorded?',victim in owner.witnesses,'directories',len(owner.directories),'witnesses',len(owner.witnesses),'memo',owner.memo_allowed)
                return original(owner,*args)
            c._BundleClassMemo.validate=validate
        origresolve=c._resolve_class_type
        n=0
        def resolve(ct):
            nonlocal n
            n+=1
            if scenario=='supplemental_early' and not changed and audit:
                change()
            return origresolve(ct)
        target=d/'dest'/'workflow.py'
        with patch.object(wb,'_sha256_file',digest),patch.object(c,'_resolve_class_type',resolve):
            try:
                wb.emit_bundle(w,target,{})
                print('OK')
            except Exception as e:
                print(type(e).__name__,str(e).replace(str(d),'<tmp>'))
        print('victim read in emit?',bool(audit),'changed?',bool(changed),'lookup',n,'output',target.exists(),target.with_suffix('.vibe.json').exists())
if __name__=='__main__': main()
