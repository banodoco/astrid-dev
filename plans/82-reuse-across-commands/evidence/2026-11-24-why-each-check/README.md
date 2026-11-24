# Why `generate` does each check, before Plan 82 caches anything (24 November 2026)

A read-only "Chesterton's fence" check, run by the Release 15 Lead with a Sonnet subagent after the owner asked that Plan 82 keep only the checks it needs, and noted there may be good reasons for the existing ones. Sources: astrid-agent `a09ea669` (release/15/main; line numbers are for it), VibeComfy `c0e910ca`, astrid-dev `bf6b94c9`. ComfyUI's own validation (`validate_prompt`: class exists, required inputs, link and widget types, combo membership, min/max) is taken from knowledge of ComfyUI, not read from its source.

**Key finding.** After a task is queued, the worker repeats the node-list and approval checks against the live target: `packs/vibecomfy/local_server_engine.py:120-210` runs the live `/object_info` preflight with `VIBECOMFY_SCHEMA_WARN_ONLY=0`, and `:215` runs `_approve_live`, which compiles again. So the command-side copies are what refuse **before a task exists**. They are not the last line of defence.

**Conclusion.** No step is pure duplication of ComfyUI. Plan 82's speed comes from caching what only changes at install or restart, not from removing checks.

| Step | Protects against | Origin | ComfyUI covers? | Plan 82 treatment | Invalidation |
|---|---|---|---|---|---|
| Pack discovery and tree hash (`core/pack/discovery.py:113-146`) | A duplicate pack id shadowing a core pack (`:568-590`), symlinks, a dirty managed checkout, a pending pack install or update transaction; own and project packs hold executable code | `b50a4e196`; the `_tree_fingerprint` docstring; Plan 81 PB-7c admission-order bug | No | Shipped roots: cache under the install stamp. Own and project packs: keep a per-command witness check, with the duplicate and pending-transaction refusals running on every warm hit, in their original order | Install stamp; any root change; a new duplicate; a pending transaction |
| Model registry load (`core/model_catalog/registry.py:104`) | The catalog checked against installed packs' backends and taxonomy | — | No | Keep, cached | Shipped `models.yaml`, pack set |
| Candidate qualification (`sdk/generation.py:1815`, `core/generation/availability.py`) | Releasing routes the pack manifests declare unqualified (`generation_route_unqualified`) | `54ecde552`, `b0f50d6b7` | No | Keep, cached; refusals recomputed | As for discovery |
| Node-list fetch (`entries.py:1198 target_schema`) | A missing node or model refused before a task (`:1223`); a managed target's model bytes re-verified against the lock (`validate_model_root_binding(verify_files=True)`, `:1260`); input to `align` download planning | `6730cc58d`, `896eb2a8b` | Partly (names at POST, and the worker repeats them); no model-byte hashing, no refusal before the task | Keep every command until a real ComfyUI is measured (D3a); measure the model-root hashing separately | ComfyUI restart (nodes), models folder (models) |
| VibeComfy object-info re-hash (`porting/object_info/consume.py`, `generation.py:85`) | A torn or replaced schema cache; a custom node class is accepted only if its lock-pinned identity resolves in the cache (`workflow_bundle.py:2216`, `:2330`) | `19034057`, `004bc946` | No (supply-chain evidence for custom-node pins) | Keep, cached, only once installed files are stated immutable (D2) | Manifest or generation change |
| Workflow build | Binds inputs, picks models (not a safety check) | — | n/a | Cache per structure key; values filled per request | Template hash, VibeComfy version, role plan, node-list digest |
| Emission and witnesses (`generation.py:2065`) | The exact `workflow.py` and companion bytes are what is admitted; `require_canonical_authority` refuses raw imports | `9724d2f9` | No | Cache the value-independent part; always render current values and derive the approval from the admitted bytes | Structure digest, object-info manifest, VibeComfy version, provenance |
| Approval compile x2 (`workflow_bundle.py:2752`) | A stale revision; unresolved requirements; classes must be in the target schema, the lock-pinned packs or core; lock-pin conflicts; target model spelling; schema validation; `workflow.py` loads through the capability fence (`scratchpad_loader.py:253`, `security/gate.py`) | `9a9c8f73`, `93f0192b`, `f68b9c22` | Partly (schema and range); not pins, provenance or the fence | Split: the structural part cached, slot values and projection per request | Structure and node-list digests |
| Pack-host attach and source digest (`host_bootstrap.py:1883`, `:2171`) | The task runs on a pack host whose Agent pack-tree bytes match what the Runtime registered; stale-host refusal | `eea40774b`, `596248efb`, `4e6e8c9fa` | No | Keep, cached; host liveness every command | Install stamp; host restart; editable checkouts keep hashing |
| Admission preflights (`sdk/remote.py:2235`, `packs/vibecomfy/invocation_preflight.py:401`) | An empty prompt, unresolved `{{x}}`, blank media, the source-video digest, attached as an `invocation_preflight` receipt; project canonicalisation; capability digest; recovery freeze | `4af8833bd`; `ce92efb43` (17 November: a free check that ran only after renting) | No | Keep every command | Per request |
| Claimed-machine refusal (`sdk/generation.py:1855`, `cli.py:826`) | No machine: refuse before admission | `889312e1f` (generate never rents) | No | Keep every command | — |
| Task POST | Idempotency key, recovery receipt, digest-bound spec | — | n/a | Keep every command | — |

**Looks redundant but is not:**
- **Pack discovery hashing** is the only per-command guard against shadowing, symlinks, dirty checkouts and pending transactions. PB-7c showed a warm cache skip two of them.
- **The command-side node-list fetch** is the only refusal before a task exists, and it hashes model roots on managed targets.
- **The 287.6 MB object-info re-hash** is the supply-chain evidence for custom-node pins.
- **The admission preflight** exists because of the 17 November paid-machine incident.

**Unknown:**
- whether an installed Astrid is immutable (D2);
- the node-list cost on a real ComfyUI;
- the model-root hashing cost on managed targets;
- whether the worker's recheck makes a stale command-side node list acceptable.
