# Inputs — One generation placement and target lifecycle

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — Hannah agreed this scope on 8 Nov 2026 (recorded in https://github.com/banodoco/astrid-dev/pull/79), with two amendments: (1) a default placement that can be changed per generation (including which local GPU, attached server or RunPod), built towards from the first version; (2) pods and other sessions may outlive a job when warm or explicitly started, governed by a lease with a default idle timeout beyond the job. A third amendment (Hannah, 8 Nov, later): a remote job relays its run events to the local run while it runs, and cancelling it stops the job and releases the machine (T5). This adds about half a day to a day to T5. A design sense check the same day (Opus reviewer, fed four maps of the code) kept the spine and moved ComfyUI specifics into the `comfyui` engine contribution: the manifest's `extra`, retrieve as the job directory, the engine's `align`, `probe` and `build`, and a lease keyed on machine custody. It replaced the event relay with the host's existing progress file and `job_cancel`, kept Placement as task data with the Runtime target `default` (the Runtime binds only to loopback), dropped the project tier of Placement precedence, and deleted `engine-index.json` instead of generating it. The aim: Wan2GP lands in Plan 12 as one more `generation.engine` contribution, with no core change. **Start (Hannah, 8 Nov, later):** Plan 32 starts now, in parallel with Plan 33 and before Plan 34, as fast as possible. Its integration branch is cut from Plan 33's (`int/33-unblock-live-generation`) and takes each Plan 33 landing by merge. While Plan 33 is open, only tasks that touch no function an open Plan 33 task touches run. Owner @AstridPseudon. Sequenced before Plan 12. Estimate, after the 8 Nov extension: about 6–9 days of engineering, raised to about 8–11 days on 8 Nov for the `vibecomfy.workflows` hooks and T6b (`merge-run/path-review/H3-GENERALIZATION.md` section 4); the live proof is Plan 34's.

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

Plan 32 began alongside [Plan 33](../33-unblock-live-generation/plan.md) and incorporated its work by merge. Plan 33's [U9 record](../33-unblock-live-generation/tasks.md#u9-land) identifies the tuple landed on 9 Nov below; its Agent head is an ancestor of the Plan 32 completion candidate. The earlier base row preserves the source on which the original selectors were checked.

| Repository | Ref | SHA | Role |
|---|---|---|---|
| astrid-agent | Plan 33's landed head (`main` after its U9) | `a105de3a4852cb61b9647dfe2c920118bd29f272` | consumed Plan 33 landing; ancestor of the completion candidate |
| astrid-agent, Plan 33's base | `cand/plan06-agent-20261107-33` | `5eac07e3fcadf8a6cca7eb6cf77c0fe234590894` | where the cited lines and selectors were checked (8 Nov) |
| VibeComfy | the pin in Plan 33's landed Agent | `e65f4941d09b1cb4d1dd5aae6171c73e648706f4` | base for T4's and T6b's VibeComfy changes |
| astrid-runtime | `runtime.lock.json` `source_commit` in Plan 33's landed Agent | `4f5477cb0f5b03d28bec991a1fe34edcd8fc309f` | landed Runtime dependency; supersedes the planning pin `b983b04` |
| runpod-lifecycle | the pin in Plan 33's landed Agent | `f2948817eeb94af8dee76be21f6d673724f1606e` | fixed; `ship_and_run` (`src/runpod_lifecycle/runner.py:88`) |

**What it takes from Plan 33:**
- the CPU pod-path test `tests/integrations/test_runpod_slot_path_cpu.py` (U1), which T1 extends;
- `--align check|trust` (U2), which T4 extends with `align`;
- the interim inventory document (U2), which T5 deletes;
- the volume model cache at `<mount>/astrid/engines/comfyui/models` (U6), which T5 turns into the models root;
- the reuse key with the engine id (U7), which T5 keeps.

Line numbers in [tasks.md](tasks.md) are at Agent `5eac07e3f` and must be re-checked on the landed head.

### Integrated CPU candidate for completion review

The current integrated candidate for T8 on 10 Nov 2026 is Agent [`26eeaff4f90fc5b91e25e0769477a9081deee5d3`](https://github.com/banodoco/astrid-agent/commit/26eeaff4f90fc5b91e25e0769477a9081deee5d3), on `int/32-one-generation-path`. It includes G18's independently security-re-reviewed owned-doctor schema and custody repairs: post-mutation integrity is verified before launch, and preparation retains exact stop/drain or uncertain-custody fencing through completion. Original doctor validation and missing-model refusal remain. The reviewed candidate passed 12 integration and 38 unit CPU checks; exact integrated head passed 12 managed-host integration and 12 schema checks. Final-head CI comparison remains pending. Earlier repairs retain their own recorded CPU proof. The table above records the historical planning inputs; the candidate's committed dependency files identify the versions below, unchanged from `41da1ff86`.

| Source | Exact revision | Candidate source of identity |
|---|---|---|
| astrid-runtime | `4f5477cb0f5b03d28bec991a1fe34edcd8fc309f` | `runtime.lock.json`, `source_commit` |
| VibeComfy | `e65f4941d09b1cb4d1dd5aae6171c73e648706f4` | `astrid/packs/{vibecomfy,runpod}/pins.json`, `sources.vibecomfy.revision` |
| ComfyUI | `423cbd20511becb1f16122ab518e92e58bfa03d9` | the same pins, `sources.comfyui.revision` |
| runpod-lifecycle | `f2948817eeb94af8dee76be21f6d673724f1606e` | `astrid/packs/runpod/pins.json` and `pyproject.toml` |

CPU proof and review findings remain in [tasks.md](tasks.md); the existing draft completion PR [#276](https://github.com/banodoco/astrid-dev/pull/276) carries the final integrated assessment when ready. CI run [`42799672641`](https://github.com/banodoco/astrid-agent/actions/runs/42799672641) is active on this exact candidate. Concurrent main run [`42768047490`](https://github.com/banodoco/astrid-agent/actions/runs/42768047490), on `a105de3a`, reproduced intermittent apt setup delays (task progress 48); this is infrastructure evidence rather than a completed no-regression result. The earlier i2v bootstrap heartbeat failure was not reproduced by its passing exact retry on `41da1ff86`; its cause remains unknown and is assigned to Plan 34's liveness-family follow-up. Same-marker altered imports before reset also remain unproven. The doctor CLI fixture uses an editable VibeComfy source layout; it does not qualify wheel-only installs. Plan 34 owns real inference, real model and node downloads, real RunPod capacity and volume behavior; its live proof is not a T8 prerequisite. Any later product merge requires the completion assessment to name the new candidate and revalidate the evidence affected by that merge.

## Owner decisions

Recorded from the lead's relay of the owner's choices (Hannah, 8 Nov 2026, about 15:40Z):
1. **CPU only for now.** Every task is provable on CPU, with no paid pods. The live proof (T7) leaves this plan and becomes a later pass of [Plan 34](../34-real-gpu-proof/plan.md). That plan comes right after Plan 33 completes on CPU, before this plan, because the priority is to get unblocked and running on GPU, then elegance.
2. **Review rounds: at most 3, owner-agreed** (D3, M-79, on the lead's recommendation). The reason is the run contract's case for a cross-repository contract change: an Agent plus VibeComfy integration, three new extension points, and the deletion of several routes (the bridge, the second `/view` client, `pip_embedded`, `checkout_server`, h3's route).
3. **The pack extension protocol is its own plan,** [Plan 17](../17-vibecomfy-extensibility/plan.md). This plan creates only the three points it needs (`generation.engine`, `generation.machine`, `vibecomfy.workflows`) and references Plan 17 for the rest.

Decided by the owner at about 16:05Z (M-79, [ledger](https://github.com/banodoco/astrid-overnight-2026-11-05/blob/merge-run/2026-11-07/merge-run/DECISIONS-LEDGER.md)):

4. **D1, the comfy packs:** delete the old `comfyui` pack and `comfy_wrap` in T2b, which also owns the engine merge. This supersedes M06-4's hold on Plan 06 PK-15B for these packs.
5. **D2, the rename:** rename `--target` to `--placement` (and `target_policy` to `placement_policy`) in one change in T3, updating the App's callers, with no alias.
6. **D3:** 3 review rounds (decision 2 above).

The run shape is also set: one plan per manager at a time, Plan 33 first, then Plan 34, then this plan.

The scope decision above covers the original scope; the 8 Nov extension is confirmed when this plan is next in line.

## Ambiguity pass (8 Nov 2026, from code)

Settled from code at Agent `5eac07e3f` and VibeComfy `e65f4941`:
- **The protocol exists and is unused:** `astrid/core/extensions/` (commit `864179976`), with tests in `tests/core/extensions`. `side` is fixed to `client` (`schema/point.json:11`, `model.py:86,428`). T2 allows `agent`.
- **`Placement` is already a name:** a `Literal["local", "runpod"]` alias (`engine_contracts.py:9`), plus the pack-declared `PlacementDescriptor` (~475). T3 replaces the alias. Its `kind` is open and validated against `generation.machine` contributions, so packs can declare machines without a core change.
- **Plugin templates are invisible today** (`entries.py:38`, `include_dynamic=False`). VibeComfy exposes `registered_ready_roots()` (`extras.py:62`).
- **The node-pack hook is decided: none.** Workflow pins are authoritative over the lock (`custom_node_refs.py:241-247`).
- **The `engines:` pack property is unused** (`schemas/v3/pack.json:195`), so T2 deletes it.
- **Plan 33 U6's cache is keyed by lock row** (`model_downloader.py:173-177`), not in ComfyUI layout. T5 moves the entries into the models root by rename on the same volume, so nothing is downloaded again.
- **The old T6 question about VibeComfy's `PluginAPI` growing a node-pack hook** is answered by the bullet above.
- **`build`, not VibeComfy ops or the router.** The Agent never calls VibeComfy ops or the router (no `lookup_op`, `vibecomfy.ops` or `vibecomfy.router` use), so h3's graph builder becomes the point's `build` field instead of a second call path (`merge-run/path-review/H3-GENERALIZATION.md` section 2).
- **h3's `comfy_commit` and model rows are an inverted dependency** (`compile.py:576,774,1115`, `generation.py:173-188,265`). T2 makes them literals in h3's templates.
- **`license_notice` already exists** as a `ReadyMetadata` extra (VibeComfy `ready_templates/audio/hunyuan_video_foley.py:56`, Agent `entries.py:89,441`). No licence field is needed.
- **T4 keeps `model_downloader.py`,** because RunPod installs through it until T5 (`TASKS-SENSE-CHECK.md` section 8). **T3 precedes T2b,** because both touch `sdk/generation.py`.

### Open owner decisions

None. D1–D3 were decided on 8 Nov (owner decisions 4–6 above).

## References

- Routing map: `merge-run/review/generation-routing-map.md` in `banodoco/astrid-overnight-2026-11-05`, branch `merge-run/2026-11-07`.
- [Plan 02](../02-consistent-generation/plan.md) (predecessor), [Plan 12](../12-multiple-inference-routes/plan.md) (consumer), [Plan 13](../13-execution-host-refactor/plan.md) (host split, excluded), [Plan 25](../25-cloud-assist-v1/plan.md) (would reuse Placement, the remote machine and the volume cache), [Plan 33](../33-unblock-live-generation/plan.md) (predecessor), [Plan 17](../17-vibecomfy-extensibility/plan.md) (the extension protocol).
