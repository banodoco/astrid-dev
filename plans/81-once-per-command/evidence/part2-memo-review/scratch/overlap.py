"""Overlapping public emits in a copied Python context; no cache restoration."""
import contextvars,shutil,tempfile,threading,sys
from pathlib import Path
from contextlib import nullcontext
from unittest.mock import patch
from vibecomfy.workflow import VibeWorkflow,WorkflowSource
from vibecomfy import workflow_bundle as wb
from vibecomfy.porting.object_info import consume as c

def main(mode):
    with tempfile.TemporaryDirectory() as tmp:
        d=Path(tmp)
        cache=shutil.copytree(c.CACHE_DIR,d/'cache')
        c.CACHE_DIR=cache
        wf=VibeWorkflow('sample',WorkflowSource('sample'))
        wf.add_node('ImageResizeKJ',uid='stable')
        outer=d/'outer'/'workflow.py';inner=d/'inner'/'workflow.py'
        c.reset_cache()
        checkpoint=threading.Event();outer_done=threading.Event()
        inner_thread=None
        state=threading.local();changed=False
        idx=cache/'index.json'
        def is_inner():return threading.current_thread() is inner_thread
        def active_owner():
            var=getattr(c,'_BUNDLE_CLASS_MEMO',None)
            owner=var.get() if var is not None else None
            return 'absent' if owner is None else ('active' if owner.active else 'revoked')
        def wait_for(event):
            if not event.wait(20):raise RuntimeError('event timed out')
        count=0
        old=c._resolve_class_type
        def resolve(ct):
            nonlocal count
            if not is_inner():return old(ct)
            count+=1
            if mode in ('persistent','fresh','keep-active') and count==30:
                state.final=True
                try:return old(ct)
                finally:
                    state.final=False
                    print('inner leaves final scalar, owner',active_owner())
                    if mode != 'keep-active':
                        checkpoint.set()
                        wait_for(outer_done)
                    print('inner resumes, owner',active_owner())
            return old(ct)
        read=Path.read_bytes
        def read_bytes(p):
            nonlocal changed
            result=read(p)
            if getattr(state,'final',False) and p==idx and not changed:
                idx.write_text('[]')
                changed=True;print('invalid index installed permanently after first index read of inner lookup',count)
            return result
        sha=wb._sha256_file
        def digest(p):
            nonlocal changed
            result=sha(p)
            if is_inner() and mode=='late' and not changed:
                checkpoint.set();wait_for(outer_done)
                print('inner digest resumes, owner',active_owner())
                idx.write_text('[]');changed=True
            return result
        def run_inner():
            try:
                wb.emit_bundle(wf,inner,{})
                print('inner OK')
            except Exception as e:
                print('inner',type(e).__name__,str(e).replace(str(d),'<tmp>'))
            finally: checkpoint.set()
        journal=wb._write_publish_transaction
        def write(p,record):
            nonlocal inner_thread
            result=journal(p,record)
            if p==outer and record['state']=='prepared' and inner_thread is None:
                ctx=contextvars.Context() if mode=='fresh' else contextvars.copy_context()
                inner_thread=threading.Thread(target=ctx.run,args=(run_inner,))
                inner_thread.start()
                wait_for(checkpoint)
            return result
        check=getattr(wb,'_validate_bundle_cache_witness',None)
        def check_owner():
            if is_inner():print('inner prepublication callback sees owner',active_owner())
            return check()
        checks=patch.object(wb,'_validate_bundle_cache_witness',check_owner) if check else nullcontext()
        with checks,patch.object(wb,'_write_publish_transaction',write),patch.object(wb,'_sha256_file',digest),patch.object(c,'_resolve_class_type',resolve),patch.object(Path,'read_bytes',read_bytes):
            try:
                wb.emit_bundle(wf,outer,{})
                print('outer OK')
            finally:
                outer_done.set()
                if inner_thread is not None:inner_thread.join(25)
        print('inner scalar lookups',count,'index remains invalid',idx.read_text()=='[]','outer pair',outer.is_file(),outer.with_suffix('.vibe.json').is_file(),'inner pair',inner.is_file(),inner.with_suffix('.vibe.json').is_file())
if __name__=='__main__':main(sys.argv[1])
