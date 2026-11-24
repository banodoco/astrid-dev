# Where `generate`'s remaining time should go: a first-principles note (23 November 2026)

For [Plan 82](../../plan.md). Code: astrid-agent `045064b6` (`A:`), VibeComfy `c0e910ca` (`V:`). Numbers: B-arm medians, [summary-ab.json](../../../81-once-per-command/evidence/2026-11-23-part2b-installed-fixed/run/summary-ab.json) (installed, 4 vCPU, stand-in ComfyUI, 5.83 s). *est.* marks an estimate.

## Answer

Of about 5.8 s, only about 0.3 s depends on this request: put the prompt, seed and size into a graph, check them, import two objects, create the task. The rest depends only on what changes at install or restart (pack bytes, template, VibeComfy's object-info set, the Agent source tree, ComfyUI's node list), yet is recomputed and re-hashed every command. Caching it on disk, keyed by content and recomputing on any doubt, brings a warm `generate` to about 2.0 s *est.* A thin client handing the request to the already-running pack host (Plan 55's design) takes it to about 1.3 s *est.*: Plan 82's last step. Under 1 s is not shown by these numbers.

## Every stage

| Stage (s) | Per-request or cacheable | Key | Invalidation | Where it lives | Saved *est.* |
| --- | --- | --- | --- | --- | ---: |
| Pack discovery, 16 scans (2.31; model registry x2 1.07, qualification x6 0.58, unparented x4 0.29, capability registries x2 0.19, two more 0.19) | Cacheable. Each scan content-hashes every root (`A:astrid/core/pack/discovery.py:113-146`, `:170`), twice per reused projection (`:191-200`) | Shipped roots: install stamp. Own and project packs: tree witness (PB-7b's Linux stat witness, or a content digest) | New stamp; any change in a root; a new duplicate must still be refused | In-process (PB-7b), then on disk (RA-0, RA-3) | 2.2 |
| Workflow build (0.65 self) | Mostly cacheable: template sha256 pin, `workflow_from_ready` (`A:astrid/core/generation/backends/vibecomfy.py:246-305`), model-role binding. Per-request: `set_input` of prompt, seed, size (`:557-579`, `A:astrid/sdk/generation.py:948`) | Template hash, VibeComfy version, entry and mode, role plan digest, target node-list digest | Any of these | On disk (RA-2) | 0.6 |
| Target node list (0.004 on stand-in) | Per-request today (`A:astrid/core/generation/backends/comfy_target.py:266-271`) | ComfyUI restart or models folder (RA-4) | — | Keep fetching (D3a) until a real ComfyUI is measured | 0 |
| Workflow emission (0.50) | A pure function of the graph *including* the prompt literals, the provenance, the emitter version and the object-info set (`V:vibecomfy/workflow_bundle.py:3238-3296`). 53 templates emit identically ([PB-3](../../../81-once-per-command/evidence/2026-11-23-part2b-installed-fixed/README.md)). Still hashed per command: 246 object-info SHA calls, 287.6 MB (read set and re-check: `V:vibecomfy/porting/object_info/consume.py:311-482`) | Structure digest (graph with value slots masked) + object-info manifest digest + VibeComfy version | Any of these; a new value only re-renders | On disk; object-info trust under the install stamp (RA-0) | 0.45 |
| Approval compile x2 (0.33) | Split. `load_bundle` and the structural checks (`V:vibecomfy/workflow_bundle.py:2752-2848`) are cacheable. The API projection carries the values (`:2790`), so slot values are checked per request | Structure digest + target node-list digest | Either changes | On disk with the template (RA-2) | 0.28 |
| Pack host attachment (0.41) and source identity (0.16) | Cacheable. Re-digests the Agent source tree per command (`A:astrid/sdk/host_bootstrap.py:2171-2173`) | Install stamp + host registration | New stamp; host restart | On disk (proposed for RA-0); gone with a thin client | 0.45 |
| Other command work (0.47) | Imports and untimed work (`A:astrid/sdk/command_timing.py:100`) | — | — | Lazy imports (RA-0), then a thin client | 0.2 to 0.4 |
| Runtime launcher connection (0.20) | Per-process (`A:astrid/core/generation/cli.py:64`) | — | — | Thin client (Plan 55) | 0.15 |
| Interpreter start (0.13) | Floor for a process | — | — | — | 0 |
| Small stages (0.40 self time; the facts' ~0.8 includes their parents) | Per-request: admission preflights, object import, task POST (~0.15). Cacheable: registry, readiness (~0.15) | As for discovery | As for discovery | RA-0 | 0.15 |

## Integrity rules

1. **The key is every input the function reads,** from content, or from an install stamp only if the install is stated immutable (D2). If it cannot be computed (symlink, unreadable root, no witness on this platform), compute as today and say so in the timings.
2. **Cache successes only.** Refusals are recomputed every time, so they stay refusals and keep their order ([PB-7c's lesson](../../../81-once-per-command/evidence/2026-11-23-pb7b-handoff/README.md)).
3. **A hit never skips a per-request check:** prompt, seed, project, output prefix, target readiness, node-list fetch.
4. **Approval binds bytes, never keys.** The task carries the digests of the emitted `workflow.py` and companion (`A:astrid/sdk/generation.py:2254-2255`). The local approval digest is recomputed from the filled projection each time (`:2150-2151`). So wrong cached bytes produce a different admitted object, never an old approval on a new graph. A 53-template differential test (cached against full build) holds this.
5. **Safe to delete.**

## Target architecture and floor

(a) Per command: one discovery (PB-7b). (b) On disk, under the install stamp and content keys: discovery and registry results, object-info trust, source identity, and a prepared template per structure key; a command fills slots, checks them, renders, admits. (c) The CLI as a thin client to the warm pack host, which holds (b) in memory.

Floor after (b): about 2.0 s *est.* (5.83 minus about 3.8 s from steps 1 to 4). After (c): about 1.3 s *est.* (minus step 5's 0.7). What stays is interpreter 0.13, per-request work about 0.3, 0.27 the collector does not attribute, and about 0.3 of other work: under 1 s is unproven.

## Steps, in order

1. **PB-7b, if RN-4 takes it** (discover once per command). Measured: 1.17 s of discovery's 2.2.
2. **RA-0, widened:** shipped packs and the model registry under the install stamp; the pack host source identity under the same stamp; VibeComfy trusting a validated object-info generation by its manifest, which removes the 287.6 MB of per-command hashing. about 1.3 s *est.* (rest of discovery 1.0, identity 0.16, object-info hashing 0.15)
3. **RA-2 keyed on structure, not the prompt:** a prepared template, then fill, check slots, render. Removes most of build, emission and approval compile: about 1.1 s *est.* (build 0.6, render and compile 0.5)
4. **Lazy imports (RA-0's measurement):** 0.2 s *est.*
5. **A thin client to the warm pack host** (RA-1's option, Plan 55): removes attachment, launcher connection, start-up overhead: about 0.7 s *est.*

## Fit with other plans

- **PB-7b / [Plan 87](../../../87-render-works/plan.md) RN-4** owns per-command discovery and the pack-root seam; RA-0 and RA-3 build on it.
- **Plan 82:** steps 2 to 4 are RA-0 and RA-2; RA-3 shrinks to own packs; RA-4 is off the critical path.
- **[Plan 55](../../../55-local-speed/plan.md):** step 5; its prepared template (`24c68a270`/`d8e61a50`) is RA-2's donor, made process-independent by content keys.

**Changes to Plan 82's task list I would make:**

- RA-0: add object-info trust and the source-identity stamp (nobody owns them).
- RA-2: key on the structure digest; split the approval compile; add the differential test.
- RA-1: record that disk caches alone stay near 2 s *est.*: "disk now, thin client last".
- RA-4: conditional on a real ComfyUI measurement.

## What I am least sure of

How much of emission (0.50) and approval compile (0.33) is value-independent: unprofiled; if rendering dominates, step 3 saves less. Second: whether the 0.27 s unattributed time and "other command work" vanish with a thin client; that decides whether 1 s is reachable.

## Independent critique (Astra, read-only, from the first draft)

**Verdict — Revise before adopting.** The receipts identify expensive stages. They establish neither the safety of the proposed cache hits nor the claimed warm floor. Without product source, I could not verify the cited read sets, compiler split, or approval binding.

1. “Refusals are recomputed every time, so they stay refusals and keep their order.” A prior success can bypass a *new* refusal. PB-7c observed a warm hit miss a pending transaction and dirty-inventory validation precede duplicate rejection. Specify which live checks run before each hit, in their original order. PB-7b’s narrow Linux witness needs separate justification across commands.

2. “Structure digest + target node-list digest” omits compiler identity and the bundle being checked. The emission key likewise omits provenance, which its own row names as an input. Reuse only a value-independent intermediate. Render the current literals and private output prefix, then derive approval from the projection of the exact workflow and companion bytes admitted. PB-3’s 53-template comparison does not exercise a stale cross-process hit.

3. “VibeComfy trusting a validated object-info generation by its manifest” assumes the manifest proves current file contents. A file can change under an unchanged manifest unless immutability covers those files. Otherwise charge for revalidation. Likewise, host source identity may be reusable while host liveness and compatibility still require a current check.

4. “Floor after (b): 1.3 to 1.5 s *est.*” Steps 1–4 imply **2.06 s** (5.83 − 1.17 − 1.30 − 1.10 − 0.20), even transferring PB-7b’s gain from another baseline. Steps 2 and 3 both claim emission and compile savings. The floor’s components sum to 1.20 s. Neither calculation establishes that subsecond requires a thin client.

5. “Land PB-7b through Plan 87 RN-4” turns a parked, below-threshold handoff into a prerequisite. Leave that decision with RN-4. Plan 82’s RA-1 chooses disk or Plan 55 residency before funding both.

**First change:** Move RA-0’s installed measurements first. Separate hashing, rendering, compile checks, and live attachment costs, then recalculate the floor from nonoverlapping savings.

## Author's note on the critique

Finding 4 (the floor did not follow from the steps) was right and is fixed above: steps 1 to 4 leave about 2.0 s *est.*, step 5 about 1.3 s *est.*, and under 1 s is stated as unproven. Findings 1 to 3 and 5 are conditions on RA-1 and RA-2, not corrections to the table: which live checks run before a hit and in what order (PB-7c's two refusals), what the structure key must include (compiler identity, provenance), whether an install stamp proves object-info bytes, and RN-4 owning PB-7b. They should be written into those task cards. The first change Astra asks for, measuring hashing, rendering, compile checks and attachment separately before funding the rest, is RA-0's first step.

