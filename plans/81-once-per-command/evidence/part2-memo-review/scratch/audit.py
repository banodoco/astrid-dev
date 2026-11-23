"""Audit cache and non-cache reads through one representative unmodified Qwen workflow."""
import json, os, shutil, sys, tempfile
from pathlib import Path
from collections import defaultdict
from vibecomfy.cli_loader import load_workflow_any
from vibecomfy.workflow_bundle import emit_bundle
from vibecomfy.porting.object_info import consume as c
from vibecomfy.security.provenance import Provenance
def main():
    repo=Path.cwd()
    wf=load_workflow_any('image/qwen_image_2_1_turbo')
    with tempfile.TemporaryDirectory() as tmp:
        tmp=Path(tmp)
        c.CACHE_DIR=shutil.copytree(c.CACHE_DIR,tmp/'cache')
        c.reset_cache()
        ops=defaultdict(set)
        enabled=True
        classes=set()
        def evt(event,args):
            if not enabled or event not in ('open','os.listdir','os.scandir','os.readlink'):return
            if event=='open' and not (isinstance(args[2],int) and args[2]&os.O_ACCMODE != os.O_WRONLY): return
            if not isinstance(args[0],(str,bytes)):return
            path=os.fsdecode(args[0])
            if '/__pycache__/' in path or path.endswith(('.so','.pyc')): return
            frame=sys._getframe(1)
            stack=[]
            while frame and len(stack)<5:
                fname=frame.f_code.co_filename
                if '/vibecomfy/' in fname:stack.append(fname.split('/vibecomfy/')[-1]+':'+str(frame.f_lineno))
                frame=frame.f_back
            ops[path.replace(str(repo),'<repo>').replace(str(tmp),'<tmp>')].add(' > '.join(stack))
        sys.addaudithook(evt)
        original=c._resolve_class_type
        def record(ct):
            classes.add(ct);return original(ct)
        c._resolve_class_type=record
        if hasattr(c,'_BundleClassMemo'):
            orig=c._BundleClassMemo.validate
            def checked(owner,*args):
                if not args:print('FINAL',json.dumps(sorted(str(p).replace(str(tmp),'<tmp>') for p in owner.witnesses)), 'memo',owner.memo_allowed)
                return orig(owner,*args)
            c._BundleClassMemo.validate=checked
        dest=tmp/'dest'/'workflow.py'
        emit_bundle(wf,dest,Provenance.AGENT_AUTHORED)
        enabled=False
        print('CLASSES',sorted(classes))
        for path,stacks in sorted(ops.items()):
            print(json.dumps([path,sorted(stacks)]))
if __name__=='__main__':main()
