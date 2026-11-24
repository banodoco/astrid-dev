"""Exercise public emit/candidate paths and inspect files during and after refusal."""
import json, os, shutil, stat, sys, tempfile
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch
from vibecomfy import workflow_bundle as wb
from vibecomfy.workflow import VibeWorkflow, WorkflowSource
from vibecomfy.porting.object_info import consume as c

def main(mode, preexisting=False):
    with tempfile.TemporaryDirectory() as d:
        d=Path(d)
        c.CACHE_DIR=shutil.copytree(c.CACHE_DIR,d/'cache') if not isinstance(c.CACHE_DIR,str) else d/'cache'
        out=d/'out'
        out.mkdir()
        stage=d/'stage'
        stage.mkdir()
        dest=out/'workflow.py'
        stage_observations=[]
        def roster():
            return sorted([p.name,oct(stat.S_IMODE(p.stat().st_mode)),p.stat().st_size] for p in out.iterdir())
        w=VibeWorkflow('probe', WorkflowSource('probe'))
        w.add_node('LoadImage',uid='stable')
        c.reset_cache()
        origmk=tempfile.mkstemp
        origsha=wb._sha256_file
        if preexisting:
            wb.emit_bundle(w,dest,{})
            existing={p.name:p.read_bytes() for p in out.iterdir()}
        else:
            existing={}
        hits=0
        def make(*args,**kw):
            nonlocal hits
            if Path(kw.get('dir') or stage)==out:
                hits+=1
                if hits==2:
                    print('after first staging write',roster())
                    if mode=='exception':
                        raise OSError('scheduled second staging allocation failure')
            return origmk(*args,**kw)
        def sha(path):
            result=origsha(path)
            if mode in ('end','end_exception') and path.parent==out and not stage_observations:
                stage_observations.append(True)
                print('transaction digest',roster())
                if mode=='end':
                    (c.CACHE_DIR/'index.json').write_text('[]')
                else:
                    Path(c.CACHE_DIR/'index.json').rename(c.CACHE_DIR/'old-index')
                    # Changes real evidence; end I/O failure is injected separately.
                    (c.CACHE_DIR/'index.json').write_text('[]')
            return result
        def end_error(path):
            if stage_observations:
                raise OSError('scheduled final witness read failure')
            return c._cache_file_witness(path)
        origres=c._resolve_class_type
        n=0
        def resolve(ct):
            nonlocal n
            n+=1
            if n==2 and mode=='early':
                raise KeyboardInterrupt('scheduled mid-emit interrupt')
            return origres(ct)
        with ExitStack() as stack:
            for obj,name,func in [(tempfile,'tempdir',str(stage)),(tempfile,'mkstemp',make),(wb,'_sha256_file',sha),(c,'_resolve_class_type',resolve)]:
                stack.enter_context(patch.object(obj,name,func))
            if mode=='end_exception' and hasattr(c,'_bundle_end_witness'):
                stack.enter_context(patch.object(c,'_bundle_end_witness',end_error))
            try:
                kwargs={'expected_members':{dest:'wrong'}} if mode=='condition' else {}
                wb.emit_bundle_with_candidate(w,dest,{},None,**kwargs)
                print('OK')
            except BaseException as e:
                print(type(e).__name__,str(e).replace(str(d),'<tmp>'))
        print('final',roster(),'private staging',list(stage.iterdir()),'existing bytes preserved',all((out/k).read_bytes()==v for k,v in existing.items()))
if __name__=='__main__': main(sys.argv[1],sys.argv[2:]==['preexisting'])
