# PB-7 pack-discovery profile (route N)

Source: `/home/user/p81b/wt/pb7-profile`, HEAD `b324d7c1e94713e7ae48d3d98a70db1214ef658f`. No source files changed. Existing timing input: `/home/user/p81b/box/part2b/receipts/run/summary-ab.json` (12 records; installed before/after builds, stand-in ComfyUI, `--no-wait`). This receipt is useful for stage attribution, but does not attest runtime source bytes/listener identity and does not capture Python caller stacks or root arguments.

## Observed discovery calls

Each of the 12 generate records contains 16 `pack discovery` timed occurrences (192 in total). The following table groups occurrences by the timing parent visible in record `same-before-warmup`; parent counts are stable across all 12 records. `caller` names are the smallest source-level attribution supported by the receipt and current code. The four unparented occurrences are not exactly attributable from available evidence.

| Caller | Parent stage | Roots | Count / generate |
|---|---|---|---:|
| Model registry assembly (`ModelRegistry.load_default`) | `model registry` | default discovery roots (see below) | 2 |
| Candidate source/readiness lookup and qualification paths | `candidate qualification` (6 calls) | default discovery roots; cache behavior is not exposed by timings | 6 |
| Workflow entry / workflow construction resolution | `workflow build` | default discovery roots | 1 |
| Capability registry assembly | `capability registries` | default discovery roots | 2 |
| Invocation capability/context resolution | `invocation` | default discovery roots | 1 |
| Other generation discovery calls; exact source caller not exposed | no timing parent (4 calls) | default discovery roots inferred from the common default discovery API | 4 |

The parent-stage labels above are literal receipt data. Timing boundaries alone cannot distinguish multiple source call sites under a parent or establish an exact Python caller. The `candidate qualification` calls likely correspond to per-candidate readiness checks, but attribution to named functions remains inference until a stack-enabled run is captured.

## Roots and re-reads

`discover_pack_metadata`'s default scan considers the bundled `loader.packs_root()`, verified managed source roots, the conventional `~/Astrid/packs` root, the selected personal packs root, explicit extra roots, and roots listed in `ASTRID_PACKS_PATH`. A default discovery call re-enumerates ownership names across selected roots and walks their manifests/resources; roots are deduplicated within that call. The discovery-scope cache is opt-in and keyed by a content fingerprint, but these timing records do not report cache hits, concrete resolved roots, or fingerprint I/O. Therefore the evidence does **not** establish a numerical filesystem-root re-read count, nor whether any given timed discovery was a cache hit. `pack_discovery_scope` is created by the CLI only for `--dry-run`; the receipt invocation is a real `generate ... --no-wait`, not dry-run.

## Reproduction / extraction

Commands run:

```sh
git -C /home/user/p81b/wt/pb7-profile status --short --branch
git -C /home/user/p81b/wt/pb7-profile rev-parse HEAD
python - <<'PY'
import json
p='/home/user/p81b/box/part2b/receipts/run/summary-ab.json'
d=json.load(open(p))
print('records', len(d['records']))
for r in d['records']:
    rows=[x for x in r.get('timings',[]) if x.get('stage')=='pack discovery']
    print(r['name'], len(rows))
PY
python - <<'PY'
import json,collections
d=json.load(open('/home/user/p81b/box/part2b/receipts/run/summary-ab.json'))
r=d['records'][0]
c=collections.Counter(x.get('parent') or '(none)' for x in r['timings'] if x.get('stage')=='pack discovery')
print(dict(c), sum(c.values()))
print('all_counts', sorted(set(sum(x.get('stage')=='pack discovery' for x in z.get('timings',[])) for z in d['records'])))
PY
rg -n 'timed_call\("pack discovery"|discover_pack_metadata\(' astrid/sdk/generation.py astrid/core/generation astrid/core/model_catalog astrid/sdk/invocation.py astrid/sdk/discovery.py
```

Source checks: `astrid/core/pack/discovery.py` (`@stage("pack discovery")`, default root enumeration, `pack_discovery_scope` and fingerprint cache); `astrid/sdk/generation.py` (model registry and candidate resolution); `astrid/sdk/discovery.py` (executor/orchestrator/element registry composition). No focused run was performed because the receipt does not identify a safe matching live runtime/placement, and the missing root/caller fields cannot be recovered from its timing payload without a new instrumented generate run. No tests, benchmarks, GPU, credentials, or environment files were accessed.

Elapsed: under 45 minutes; one analysis attempt. Main uncertainty: exact source callers and concrete root counts require caller-stack + resolved-root instrumentation during a focused generate invocation.
