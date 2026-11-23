"""Compare unchanged odd layouts; two successive public invocations per layout."""
import json, hashlib, os, shutil, stat, sys, tempfile, warnings
from pathlib import Path
from unittest.mock import patch
from vibecomfy.porting.object_info import consume as c
from vibecomfy.workflow import VibeWorkflow, WorkflowSource
from vibecomfy.workflow_bundle import emit_bundle
from generation import setup
source=c.CACHE_DIR
modes='valid missing_index only_index corrupt_index invalid_utf8_index unreadable_index directory_index unsafe_row bad_catalogue missing_marker gone_marker broken_marker marker_dir bad_marker wrong_generation bad_manifest corrupt_pack unreadable_pack symlinked_pack missing_provider directory_pack invalid_entry valid_symlink_root bad_symlink_root two_bad'.split()
def matrix(mode):
    with tempfile.TemporaryDirectory() as d:
        d=Path(d)
        cache=d/'cache'
        c.CACHE_DIR=source
        if mode in ('gone_marker','bad_manifest'):
            active=setup(cache)
        else:
            shutil.copytree(source,cache)
            active=cache
        idx=active/'index.json'
        marker=cache/'CURRENT'
        index=json.loads(idx.read_bytes())
        pack=active/index['ImageResizeKJ']
        before=pack.read_bytes()
        c.CACHE_DIR=cache
        w=VibeWorkflow('sample',WorkflowSource('sample'))
        w.add_node('LoadImage',uid='first')
        w.add_node('ImageResizeKJ',uid='second')
        c.reset_cache()
        if mode=='missing_index': idx.unlink()
        if mode=='only_index':
            for p in cache.glob('*.json'):
                if p!=idx: p.unlink()
        if mode=='corrupt_index': idx.write_text('[]')
        if mode=='invalid_utf8_index': idx.write_bytes(b'{"x":\xff}')
        if mode=='unreadable_index': idx.chmod(0)
        if mode=='directory_index': idx.unlink(); idx.mkdir()
        if mode=='unsafe_row': idx.write_text('{"ImageResizeKJ":"../x.json"}')
        if mode=='bad_catalogue': idx.write_text('{"__object_info_captures__": []}')
        if mode=='missing_marker': (cache/'generations'/'valid-name').mkdir(parents=True)
        if mode=='gone_marker':
            assert c.get_class('ImageResizeKJ')
            marker.unlink()
        if mode=='broken_marker': marker.symlink_to('absent')
        if mode=='marker_dir': marker.mkdir()
        if mode=='bad_marker': marker.write_text('../foo')
        if mode=='wrong_generation': (cache/'generations').mkdir(); marker.write_text('no-generation')
        if mode=='bad_manifest': (active/'manifest.json').write_text('{}')
        if mode in ('corrupt_pack','two_bad'): pack.write_text('[]')
        if mode=='two_bad': (active/index['LoadImage']).write_text('not JSON')
        if mode=='unreadable_pack': pack.chmod(0)
        if mode=='symlinked_pack':
            other=pack.with_name('other.json')
            pack.rename(other)
            pack.symlink_to(other)
        if mode=='missing_provider': pack.unlink()
        if mode=='directory_pack': pack.unlink(); pack.mkdir()
        if mode=='invalid_entry': pack.write_text('{"ImageResizeKJ": []}')
        if mode in ('valid_symlink_root','bad_symlink_root'):
            c.CACHE_DIR=d/'link'
            c.CACHE_DIR.symlink_to(cache)
            if mode=='bad_symlink_root': idx.write_text('[]')
        for rep in range(2):
            n=[]
            orig=c._resolve_class_type
            def resolve(name):
                n.append(name)
                return orig(name)
            dest=d/str(rep)/'workflow.py'
            with warnings.catch_warnings(record=True) as caught, patch.object(c,'_resolve_class_type',resolve):
                warnings.simplefilter('always')
                row={'case':mode,'rep':rep}
                try:
                    b=emit_bundle(w,dest,{})
                    row['revision']=b.revision_id
                except Exception as e:
                    row['error']=[type(e).__name__,str(e).replace(str(d),'<tmp>'),len(n),n[-1:]]
                row['warnings']=[[x.category.__name__,str(x.message).replace(str(d),'<tmp>')] for x in caught]
                row['dest']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(dest.parent.glob('*')) if p.is_file()}
                print(json.dumps(row,sort_keys=True),flush=True)
if __name__=='__main__':
    for mode in sys.argv[1:] or modes:
        matrix(mode)
