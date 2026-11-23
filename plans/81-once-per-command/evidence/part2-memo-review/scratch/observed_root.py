"""The middle root is actually observed by the same reader during this emit."""
import json,shutil,tempfile
from pathlib import Path
from unittest.mock import patch
from vibecomfy.workflow import VibeWorkflow, WorkflowSource
from vibecomfy import workflow_bundle as wb
from vibecomfy.porting.object_info import consume as c
def main():
    with tempfile.TemporaryDirectory() as d:
        d=Path(d); a=shutil.copytree(c.CACHE_DIR,d/'a'); b=shutil.copytree(a,d/'b')
        link=d/'configured'
        link.symlink_to(a)
        c.CACHE_DIR=link
        t='ImageResizeKJ'
        pack=b/json.loads((b/'index.json').read_bytes())[t]
        data=json.loads(pack.read_bytes());data[t]['description']='read from B'
        pack.write_text(json.dumps(data))
        w=VibeWorkflow('sample',WorkflowSource('sample'))
        w.add_node('LoadImage',uid='first');w.add_node(t,uid='second')
        c.reset_cache()
        redirected=False
        orig=c._resolve_class_type
        def point(p):
            temp=d/'new-link';temp.symlink_to(p);temp.replace(link)
        def resolve(ct):
            nonlocal redirected
            if ct==t and not redirected:
                redirected=True
                point(b)
                try:
                    entry=orig(ct)
                    print('middle answer',entry['description'],'resolved root',c._reader_state['root'].name)
                finally:
                    point(a)
                return entry
            return orig(ct)
        if hasattr(c,'_BundleClassMemo'):
            val=c._BundleClassMemo.validate
            def validate(owner,*args):
                if not args:
                    print('end roots in file read set',sorted({p.parent.name for p in owner.witnesses}),'root identity',owner.root_identity[0].name,'changed flag',owner.changed)
                return val(owner,*args)
            c._BundleClassMemo.validate=validate
        dest=d/'out'/'workflow.py'
        with patch.object(c,'_resolve_class_type',resolve):
            try:
                wb.emit_bundle(w,dest,{})
                print('OK')
            except Exception as e: print(type(e).__name__,str(e))
        print('output',dest.is_file(),dest.with_suffix('.vibe.json').is_file())
if __name__=='__main__': main()
