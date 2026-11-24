"""A new pack in an already active generation uses an unobserved directory guard."""
import os,sys,tempfile
from pathlib import Path
from unittest.mock import patch
from generation import setup
from vibecomfy.workflow import VibeWorkflow,WorkflowSource
from vibecomfy import workflow_bundle as wb
from vibecomfy.porting.object_info import consume as c, generation as g

def main():
    with tempfile.TemporaryDirectory() as d:
        d=Path(d)
        cache=d/'cache'
        active=setup(cache)
        c.CACHE_DIR=cache
        assert c.get_class('LoadImage')
        w=VibeWorkflow('sample',WorkflowSource('sample'))
        w.add_node('ImageResizeKJ',uid='stable')
        seen=0
        original=g._validate_generation_root
        def guard(path):
            nonlocal seen
            if path==active:
                seen+=1
            return original(path)
        def change():
            other=active.with_name('original-data')
            active.rename(other)
            active.symlink_to(other)
            print('changed after',seen,'real directory guard calls')
        old=c._resolve_class_type
        count=0
        def resolve(ct):
            nonlocal count
            count+=1
            if sys.argv[1]=='between' and count==2:change()
            return old(ct)
        sha=wb._sha256_file
        late=False
        def digest(path):
            nonlocal late
            result=sha(path)
            if sys.argv[1]=='digest' and not late:
                late=True;change()
            return result
        if hasattr(c,'_BundleClassMemo'):
            originalval=c._BundleClassMemo.validate
            def val(owner,*args):
                if not args:print('final recorded guard directory?',active in owner.directories,'memo enabled?',owner.memo_allowed)
                return originalval(owner,*args)
            c._BundleClassMemo.validate=val
        dest=d/'dest'/'workflow.py'
        with patch.object(g,'_validate_generation_root',guard),patch.object(wb,'_sha256_file',digest),patch.object(c,'_resolve_class_type',resolve):
            try:
                wb.emit_bundle(w,dest,{})
                print('OK')
            except Exception as e:print(type(e).__name__,str(e).replace(str(d),'<tmp>'))
        print('directory still symlink?',active.is_symlink(),'lookups',count,'files',sorted(p.name for p in dest.parent.glob('*')))
        try:g.active_cache_root(cache)
        except Exception as e:print('fresh generation admission:',type(e).__name__,str(e).replace(str(d),'<tmp>'))
if __name__=='__main__': main()
