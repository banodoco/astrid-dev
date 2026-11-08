# Inputs — One generation placement and target lifecycle

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — Hannah agreed this scope on 8 Nov 2026 (recorded in https://github.com/banodoco/astrid-dev/pull/79), with two amendments: (1) a default placement that can be changed per generation (including which local GPU, attached server or RunPod), built towards from the first version; (2) pods and other sessions may outlive a job when warm or explicitly started, governed by a lease with a default idle timeout beyond the job. Owner @AstridPseudon. Sequenced before Plan 12. Estimate, after the 8 Nov extension: about 6–9 days of engineering plus the live proof.

**Prior art:** the merge run's routing map, `merge-run/review/generation-routing-map.md` in `banodoco/astrid-overnight-2026-11-05`, branch `merge-run/2026-11-07`, written while proving `astrid generate --target runpod` live on 7-8 Nov 2026. It lists six placement decision points, two remote mechanisms, five dry-run divergences, three duplicated sfx/foley RunPod refusals and an h3_av-specific pod command in the runpod pack's `remote_placement.py`. About 43 test references are affected, and the routing map estimates 6-10 hours for the Placement half alone. [Plan 02](../02-consistent-generation/plan.md) lands the guard-rail tests and a targeted routing fix first. Next: re-check each cited line against current source before work starts.

**Approach:** compute a frozen Placement once in `GenerationFacade._generate_on_target` and pass it down. One `run(job, placement)` runs the whole path on the machine where ComfyUI runs; RunPod is a rented machine that runs the same local path. This replaces the decision points and the remote-ComfyUI plumbing rather than patching each. Alternatives not chosen: keep patching each site (leaves two mechanisms and the dry-run drift), and let packs own their pod commands (keeps h3_av ignoring `--target`).

**Scope extension (8 Nov 2026):** after the live merge-run proof stalled, Hannah set the target as one path for every generation: requirements, placement, optional alignment, run and retrieve. Its evidence is the path review on the desk (`merge-run/path-review/`: `VISION.md`, seven audits, and `HOLISTIC.md`). The independent review there found four root causes:
- placement carries no inventory past the host boundary;
- requirements are per engine (a 95.8 GB whole lock per pod), not per request;
- alignment is a hidden precondition with three inventories;
- the only test of the pod path was a paid live run.

So this plan now also owns the manifest, `align`, per-request model sets, the volume cache, a single submit and retrieve, RunPod as a remote machine, and modality as data. An independent sense check (`merge-run/path-review/PLAN-SENSE-CHECK.md`) recommended the remote-machine model for RunPod over carrying the pod's inventory to the controller. The short-term unblock moved to [Plan 33](../33-unblock-live-generation/plan.md).

**h3_av as a VibeComfy plugin** (`merge-run/path-review/H3-AS-VIBECOMFY-EXTENSION.md`, adopted with one exception):
- VibeComfy's `vibecomfy.plugins` mechanism already registers templates, operations and routes, and its templates carry the model and node rows.
- h3's pod route already is the remote-machine model, so T5 generalizes it.
- h3 currently reads its model URLs from the Agent's engine lock, which is the dependency upside down.
- 20 h3 sites leave Astrid (the table is in the report).
- The one exception is a new optional per-entry `finalize` step for post-ComfyUI work (ffmpeg compose and verify).
- [Plan 17](../17-vibecomfy-extensibility/plan.md) then documents the plugin contract and proves it with a second plugin.

**Glossary and renames** (HOLISTIC.md section 7):
- `--target` → `--placement`, and `target_policy` → `placement_policy`.
- Profiles: `pip_embedded` and `checkout_server` are deleted (T4), and `local_server` becomes the one local `run` path.
- The readiness profile and the generation bridge are deleted (T4, T5).
- `managed_assets` → `staged_inputs`.
- `endpoint_checkout` is deleted.
- `pending_host_readiness` → `pending_bind`.
- Approval is called the `target check` in Agent text.
- `auxiliary_model_custody: local|target` → `model_inventory: controller|placement`.
- Stop using `ComfyTarget(url, "attached")` for the RunPod bridge.

**Challenge:** Not needed — at the scope stage. The independent review of the Placement shape (default/override, `device`) and the lease semantics is instead the entry gate of task T3 (see [tasks.md](tasks.md)), because it must review the design against the source revision being built. The sense check (`merge-run/path-review/PLAN-SENSE-CHECK.md`) and the pack-extension review (`merge-run/path-review/PACK-EXTENSION-PROTOCOL.md`) are applied: one Placement and `run`, and the three extension points.

**Proof and limits:** CPU only (owner, 8 Nov). The evidence is the invariant test over every default slot × {local, attached, runpod}, dry run == live, and no pod unless execution happens on it (from Plan 02, extended in T1). It is followed by T5's remote-machine harness on a CPU fake, with a test machine contribution. Not proven by this plan: real inference, real model downloads, RunPod capacity and the volume on a real pod; the live proof (T7) is a later pass of [Plan 34](../34-real-gpu-proof/plan.md) (real-GPU proof), which follows Plan 33. Fixtures cover refusal and release on failure.

## Source identities

Plan 32 consumes [Plan 33](../33-unblock-live-generation/plan.md)'s landed revisions, not the merge-run candidates directly. Record the exact SHAs here at Plan 33's U9, before T1.

| Repository | Ref | SHA | Role |
|---|---|---|---|
| astrid-agent | Plan 33's landed head (`main` after its U9) | Pending — recorded at Plan 33 U9. Next: copy it here | base for T1–T6 |
| astrid-agent, Plan 33's base | `cand/plan06-agent-20261107-33` | `5eac07e3fcadf8a6cca7eb6cf77c0fe234590894` | where the cited lines and selectors were checked (8 Nov) |
| VibeComfy | the pin in Plan 33's landed Agent | `e65f4941d09b1cb4d1dd5aae6171c73e648706f4` unless Plan 33 moved it | base for T4 and T6's VibeComfy changes |
| astrid-runtime | `runtime.lock.json` `source_commit` in Plan 33's landed Agent | `b983b0457dffbfd435e74a5c828e129e8ec46ba3` unless moved | fixed |
| runpod-lifecycle | the pin in Plan 33's landed Agent | `f2948817eeb94af8dee76be21f6d673724f1606e` unless moved | fixed; `ship_and_run` (`src/runpod_lifecycle/runner.py:88`) |

**What it takes from Plan 33:**
- the CPU pod-path test `tests/integrations/test_runpod_slot_path_cpu.py` (U1), which T1 extends;
- `--align check|trust` (U2), which T4 extends with `align`;
- the interim inventory document (U2), which T5 deletes;
- the volume model cache at `<mount>/astrid/engines/comfyui/models` (U6), which T5 turns into the models root;
- the reuse key with the engine id (U7), which T5 keeps.

Line numbers in [tasks.md](tasks.md) are at Agent `5eac07e3f` and must be re-checked on the landed head.

## Owner decisions

Recorded from the lead's relay of the owner's choices (Hannah, 8 Nov 2026, about 15:40Z):
1. **CPU only for now.** Every task is provable on CPU, with no paid pods. The live proof (T7) leaves this plan and becomes a later pass of [Plan 34](../34-real-gpu-proof/plan.md). That plan comes right after Plan 33 completes on CPU, before this plan, because the priority is to get unblocked and running on GPU, then elegance.
2. **Review rounds: owner-agreed 2, lead recommendation 3.** The row is set to at most 3. The reason for 3 is the run contract's case for a cross-repository contract change: an Agent plus VibeComfy integration, three new extension points, and the deletion of several routes (the bridge, the second `/view` client, `pip_embedded`, `checkout_server`, h3's route). Pending owner agreement of the third round.
3. **The pack extension protocol is its own plan,** [Plan 17](../17-vibecomfy-extensibility/plan.md). This plan creates only the three points it needs (`generation.engine`, `generation.machine`, `vibecomfy.workflows`) and references Plan 17 for the rest.

## Ambiguity pass (8 Nov 2026, from code)

Settled from code at Agent `5eac07e3f` and VibeComfy `e65f4941`:
- **The protocol exists and is unused:** `astrid/core/extensions/` (commit `864179976`), with tests in `tests/core/extensions`. `side` is fixed to `client` (`schema/point.json:11`, `model.py:86,428`). T2 allows `agent`.
- **`Placement` is already a name:** a `Literal["local", "runpod"]` alias (`engine_contracts.py:9`), plus the pack-declared `PlacementDescriptor` (~475). T3 replaces the alias. Its `kind` is open and validated against `generation.machine` contributions, so packs can declare machines without a core change.
- **Plugin templates are invisible today** (`entries.py:38`, `include_dynamic=False`). VibeComfy exposes `registered_ready_roots()` (`extras.py:62`).
- **The node-pack hook is decided: none.** Workflow pins are authoritative over the lock (`custom_node_refs.py:241-247`).
- **The `engines:` pack property is unused** (`schemas/v3/pack.json:195`), so T2 deletes it.
- **Plan 33 U6's cache is keyed by lock row** (`model_downloader.py:173-177`), not in ComfyUI layout. T5 moves the entries into the models root by rename on the same volume, so nothing is downloaded again.
- **The old T6 question about VibeComfy's `PluginAPI` growing a node-pack hook** is answered by the bullet above.

### Genuine owner decisions

- **D1, Plan 06 PK-15B (held, M06-4).** T2b merges `comfyui` and `vibecomfy-h3` into one base engine, which deletes the Linux `comfyui` recipe, and that is PK-15B's scope. Recommended: release PK-15B's engine half to T2b. Alternative: keep two engines through this plan, with two warm machines and two cache users.
- **D2, renaming `--target` to `--placement`** (and `target_policy` to `placement_policy`) in T3. Recommended: rename in one change, updating the App's callers, with no alias. Alternative: keep `--target` as a deprecated alias for one release.
- **D3, the third review round** (owner decision 2 above).

## References

- Routing map: `merge-run/review/generation-routing-map.md` in `banodoco/astrid-overnight-2026-11-05`, branch `merge-run/2026-11-07`.
- [Plan 02](../02-consistent-generation/plan.md) (predecessor), [Plan 12](../12-multiple-inference-routes/plan.md) (consumer), [Plan 13](../13-execution-host-refactor/plan.md) (host split, excluded), [Plan 25](../25-cloud-assist-v1/plan.md) (would reuse Placement, the remote machine and the volume cache), [Plan 33](../33-unblock-live-generation/plan.md) (predecessor), [Plan 17](../17-vibecomfy-extensibility/plan.md) (the extension protocol).
