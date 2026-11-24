"""Bind the supported canonical-renderer identity option during a real public emit.

The two workflow_bundle writers do not themselves forward this optional keyword.
The hook exercises identity/ordered-batch readers without mocking their result.
"""
import json,shutil,tempfile
from pathlib import Path
from unittest.mock import patch
from vibecomfy.workflow import VibeWorkflow, WorkflowSource
from vibecomfy import workflow_bundle as wb
from vibecomfy.porting.emit import entrypoints as ep
from vibecomfy.porting.object_info import consume as c
from vibecomfy.porting.object_info.index import CAPTURES
src=c.CACHE_DIR
ct='ImageResizeKJ'
def run(case,warm):
    with tempfile.TemporaryDirectory() as d:
        d=Path(d)
        cache=shutil.copytree(src,d/'cache')
        c.CACHE_DIR=cache
        idx=cache/'index.json'
        data=json.loads(idx.read_bytes())
        row=json.loads((cache/data[ct]).read_bytes())[ct]
        row.update(pack_slug='test-pack',git_commit='rev',evidence_identity='snap')
        a,z='aaa.json','zzz.json'
        data[CAPTURES]={json.dumps(['test-pack','git_commit','rev'],separators=(',',':')):[z,a]}
        idx.write_text(json.dumps(data))
        (cache/z).write_text(json.dumps({ct:row}))
        (cache/a).write_text(json.dumps({ct:row} if case=='ambiguous' else {}))
        if case in ('git_two_errors','evidence_two_errors','bulk_two_errors'):
            (cache/a).write_text('[');(cache/z).write_text('[]')
        if case=='bulk_two_errors':
            data['ZClass']=a;data['AClass']=z
            idx.write_text(json.dumps(data))
        wf=VibeWorkflow('sample',WorkflowSource('sample'))
        n=wf.add_node(ct,uid='stable')
        c.reset_cache()
        if warm:assert c.get_class(ct)
        original=ep.emit_canonical_python
        count=0
        identity={'pack_slug':'test-pack','git_commit':'rev'}
        if case in ('fallback','no_fallback'):identity['git_commit']='absent'
        if case=='evidence_two_errors': identity={'pack_slug':'test-pack','evidence_identity':'snap'}
        def render(*args,**kwargs):
            nonlocal count
            count+=1
            if case=='bulk_two_errors':c.get_classes(['AClass','ZClass'])
            if case=='no_fallback':assert c.resolve_class_entry(ct,identity,allow_class_fallback=False).source=='identity_miss'
            kwargs['object_info_identities']={n.id:identity}
            return original(*args,**kwargs)
        sha=wb._sha256_file; changed=False
        def digest(p):
            nonlocal changed
            result=sha(p)
            if case=='late_identity' and not changed:
                (cache/z).write_text('[]');changed=True
            return result
        dest=d/'dest'/'workflow.py'
        with patch.object(ep,'emit_canonical_python',render),patch.object(wb,'_sha256_file',digest):
            try: b=wb.emit_bundle(wf,dest,{});err=None
            except Exception as e:err=[type(e).__name__,str(e).replace(str(d),'<tmp>')]
        return dict(case=case,warm=warm,changed=changed,render=count,error=err,pair=[dest.is_file(),dest.with_suffix('.vibe.json').is_file()])
if __name__=='__main__':
    for case in ('hit','fallback','no_fallback','ambiguous','git_two_errors','evidence_two_errors','bulk_two_errors','late_identity'):
        for warm in (False,True):print(json.dumps(run(case,warm)),flush=True)
