"""Run from scratch/{base,head} with PYTHONPATH=. and the interpreter in commands.txt."""
import argparse, collections, json, os, shutil, tempfile
from pathlib import Path
from unittest.mock import patch
from vibecomfy.porting.object_info import consume as c
from vibecomfy.workflow import VibeWorkflow, WorkflowSource
from vibecomfy import workflow_bundle as wb

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--at', type=int, default=0)
    parser.add_argument('--classes', default='LoadImage,ImageResizeKJ')
    parser.add_argument('--break-classes', default='LoadImage')
    parser.add_argument('--warm', action='store_true')
    parser.add_argument('--entry', default='emit')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        cache = tmp/'cache'
        shutil.copytree(c.CACHE_DIR, cache)
        c.CACHE_DIR = cache
        index = json.loads((cache/'index.json').read_bytes())
        out = tmp/'out'
        out.mkdir()
        stage = tmp/'staging'
        stage.mkdir()
        tempfile.tempdir = str(stage)
        w = VibeWorkflow('sample', WorkflowSource('sample'))
        for i, name in enumerate(args.classes.split(',')):
            w.add_node(name, uid='uid-'+str(i))
        if not args.warm:
            c.reset_cache()
        orig = c._resolve_class_type
        n = 0
        def resolve(name):
            nonlocal n
            n += 1
            print('lookup', n, name)
            if n == args.at:
                for victim in args.break_classes.split(','):
                    f = cache / index.get(victim, victim)
                    print('corrupt', f.name)
                    f.write_text('[]')
            return orig(name)
        with patch.object(c,'_resolve_class_type',resolve):
            try:
                dest = out/'sample.py'
                if args.entry == 'candidate':
                    wb.emit_bundle_with_candidate(w,dest,{},None)
                elif args.entry == 'capture':
                    wb.capture_bundle(w,dest,{})
                else:
                    wb.emit_bundle(w,dest,{})
                print('OK')
            except Exception as e:
                print(type(e).__name__, str(e).replace(str(tmp),'<tmp>'))
        print('destination', sorted(p.name for p in out.iterdir()), 'stage', sorted(p.name for p in stage.iterdir()))
        tempfile.tempdir = None
if __name__ == '__main__': main()
