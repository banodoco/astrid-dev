import argparse, hashlib, json, os, warnings
from pathlib import Path
from unittest.mock import patch
from vibecomfy.cli_loader import load_workflow_any
from vibecomfy.registry.ready import repo_ready_template_ids
from vibecomfy.security.provenance import Provenance
from vibecomfy.workflow_bundle import emit_bundle
from vibecomfy.porting.object_info import consume as c

root = Path.cwd()
args = argparse.ArgumentParser()
args.add_argument('shard', type=int)
args.add_argument('nshards', type=int)
args.add_argument('--twice', action='store_true')
args.add_argument('--cold', action='store_true')
opts = args.parse_args()
ids = repo_ready_template_ids(root=root/'ready_templates')
assert ids == [i['id'] for i in json.loads((root/'template_index.json').read_bytes())['templates'] if i.get('readiness_class')=='ready']
assert len(ids) == 53
for name in ids[opts.shard::opts.nshards]:
    for iteration in range(2 if opts.twice else 1):
        row = {'id': name, 'round': iteration}
        seq = []
        where = 'load'
        orig = c._resolve_class_type
        def traced(ct):
            seq.append(ct)
            return orig(ct)
        with patch.object(c,'_resolve_class_type', traced), warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            try:
                wf = load_workflow_any(name)
                dest = Path('../members-'+root.name+('-cold' if opts.cold else ''))/str(iteration)/name/'workflow.py'
                if opts.cold: c.reset_cache()
                where='emit'
                seq.clear()
                b=emit_bundle(wf,dest,Provenance.AGENT_AUTHORED)
                row['revision'] = b.revision_id
                row['pair'] = [hashlib.sha256(p.read_bytes()).hexdigest() for p in (dest,dest.with_suffix('.vibe.json'))]
            except Exception as exc:
                row['failure'] = [where,type(exc).__name__,str(exc),len(seq),seq[-1:]]
            row['warnings'] = [[x.category.__name__,str(x.message)] for x in caught]
            row['lookups'] = len(seq)
        print(json.dumps(row,sort_keys=True),flush=True)
