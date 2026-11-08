# Inputs — Unblock live generation on RunPod and locally

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — Hannah, 8 Nov 2026, merge-run desk DECISIONS-LEDGER.md M-78/M-79 (https://github.com/banodoco/astrid-overnight-2026-11-05/blob/merge-run/2026-11-07/merge-run/DECISIONS-LEDGER.md): the amended scope, CPU only, with at most 2 review rounds. It was drafted the same day at her request after the live merge-run proof stalled on voice ("a plan to get it unblocked … and to unblock any of these silly preconditions we've added"), with Plan 32 as the long-term structural plan. Owner @AstridPseudon.

**Prior art:** the work rests on material on the merge-run desk (`banodoco/astrid-overnight-2026-11-05`, branch `merge-run/2026-11-07`, https://github.com/banodoco/astrid-overnight-2026-11-05/tree/merge-run/2026-11-07/merge-run/path-review):
- `merge-run/path-review/VISION.md`: the owner's one-path vision.
- Seven read-only audits: `1-requirements.md`, `2-4-placement-submit.md`, `3a-align-local.md`, `3b-align-runpod.md`, `5-retrieve.md`, `6-modality-branches.md` and `7-why-confused.md`.
- `HOLISTIC.md`: an independent holistic review. Its verdict: voice alone needs one wire; the full scope is complex. It also gives the target design and the glossary.
- `DECISIONS-LEDGER.md` M-72 to M-75: the live voice failure, its root cause, the path map and the pause.

Key facts the tasks rely on (Agent `5eac07e3f`, VibeComfy `e65f4941`):
- **RunPod route.** It is the host bind, which sets `comfy_url` to a bridge on the controller's 127.0.0.1 (`adapter.py:253-258`). The run then goes through `local_server` (`run.py:753-758`) and `_live_preflight`, with model custody "local" (`local_server_engine.py:67`).
- **VibeComfy approval** (`workflow_bundle.py` ~2479–2630):
  - Loader-combo models listed in the place's object_info pass.
  - Authored assets are checked on the controller's disk unless the schema provider has `auxiliary_model_custody="target"` with `target_model_assets` (`schema/provider.py` ~1518–1601).
  - The Qwen3 voice model is 13 authored HuggingFace-folder assets.
- **Receipt rows.** The controller already parses and verifies the pod's install receipt row by row, then keeps only its hash (`remote_placement.py:738-757`, `engine_runner.py:938-950`).
- **Sound effects** is refused on RunPod at four sites (`02f4a7a3d` "FOLEY_REFUSAL … pre-allocation refusal"). The host also rejects the separate `source_video` input for URL-attached runs (`generic_host.py:12215-12216`), which Foley does not use (see the ambiguity pass). Media upload for image, audio and video inputs already exists (`local_server_engine.py` upload_media).
- **Pod reuse** is refused across `generate` invocations (`target_selection.py` ~446–452).
- **The whole 95.8 GB lock** is required by readiness (`engine_readiness.py:745-756`). Narrowing it is Plan 32.

**Approach:** finish the one missing wire using VibeComfy's existing target custody, and delete the preconditions that have no product reason (the sfx refusal, h3's separate pod route, the legacy route). Use the verified volume model cache and pod reuse that already exist off the main path (`engines install --model-cache-root`, used by `scripts/pod_session.py`; `prepare_retained_generation`), relaxing the checks that refuse reuse. See `merge-run/path-review/EXISTING-MACHINERY.md`. Alternatives not chosen:
- **Lock-derived inventory:** it claims rows a pod may not have; the receipt is the attested witness.
- **Switching RunPod to the remote-machine model now:** it is the right end state (Plan 32), but h3's existing machine route bypasses paid consent (its spend limit comes from an environment variable), so generalizing it is not a short-term change.
- **A new inventory type or VibeComfy change:** the mechanism already exists.
- **The full Plan 32 redesign first:** too large to unblock the landing.

**Challenge:** Reviewed — two independent checks on the merge-run desk (https://github.com/banodoco/astrid-overnight-2026-11-05/tree/merge-run/2026-11-07/merge-run/path-review).
- `PLAN-SENSE-CHECK.md` rated the plan good with edits. Applied: U2 is interim, with the receipt rows and a non-circular check; `--align check|trust`; h3_av as one run per job; the corrected storage and `comfy_wrap` facts.
- `TASKS-SENSE-CHECK.md` rated the task breakdown ready with edits. Applied:
  - `-m integration` and the full environment in `PYT_POD`;
  - U5 shrunk to the dead binder, with the legacy route moved to Plan 32 T6b;
  - the uncovered-entry case pointed at an explicit entry;
  - the receipt check moved into the host;
  - a validating stand-in;
  - the cache device and mount id;
  - the reuse signature, with U7 routed S;
  - the merge order.
- The pack-extension review (`PACK-EXTENSION-PROTOCOL.md`) added one rule: no new extension key, engine-index row or backend descriptor.

**Proof and limits:** CPU only (owner, 8 Nov): the CPU pod-path test (U1), extended by every later task, plus the focused nodes each task names. Not proven here: real inference, real model downloads to the storage volume, RunPod capacity, and whether the model cache accepts RunPod's network volume. The real-GPU proof moves to [Plan 34](../34-real-gpu-proof/plan.md) (real-GPU proof), which follows this plan. Each fresh pod still copies its rows from the volume to container disk (U6).

## Source identities

Start from the merge-run candidates, and re-freeze before work. Only the Agent changes (plus the App repin in U9); every other row is a fixed dependency.

| Repository | Ref | SHA | Role |
|---|---|---|---|
| astrid-agent | `cand/plan06-agent-20261107-33` | `5eac07e3fcadf8a6cca7eb6cf77c0fe234590894` | base for U1–U7 |
| astrid-agent (WIP for U2) | bundle `merge-run/bundles/agent-34-wip-e003778be.bundle` on the desk, ref `refs/heads/m02/agent34-m73` | `e003778bed4998d515d4dd165a948543fee894f0` | U2 donor (plumbing and tests only) |
| astrid-runtime | `cand/plan06-runtime-20261107-10` | `b983b0457dffbfd435e74a5c828e129e8ec46ba3` | fixed; `runtime.lock.json` `source_commit` |
| VibeComfy | merge-run pin | `e65f4941d09b1cb4d1dd5aae6171c73e648706f4` | fixed; `packs/{vibecomfy,runpod}/pins.json` |
| runpod-lifecycle | merge-run pin | `f2948817eeb94af8dee76be21f6d673724f1606e` | fixed; `pyproject.toml` pin; `LC` for `PYT_POD` |
| poms_packs | `cand/plan06-poms_packs-20261107-10` | `2379ab54aca522019ff4f869cfdf9375bdb56dfc` | U9 creates `main` |
| astrid-app | last candidate `-16` (its PK-14 pass is retracted) | `2191d866f` | U9 base for App `-17` |

Fetch the WIP with `git fetch <desk>/merge-run/bundles/agent-34-wip-e003778be.bundle refs/heads/m02/agent34-m73`; it touches six files (`generic_host.py`, `runpod/adapter.py`, `vibecomfy/local_server_engine.py` and three test files).

**Consumed by:** [Plan 32](../32-generation-placement-targets/plan.md) starts from this plan's landed Agent head (recorded at U9), after Plan 34's first pass.

## Owner decisions

Recorded from the lead's relay of the owner's choices (Hannah, 8 Nov 2026, about 15:40Z), in addition to those in [plan.md](plan.md#owner-decisions-recorded-8-nov-2026):

1. **CPU only for now.** Every task is provable on CPU, with no paid pods. The live proof (former U8) leaves this plan. The real-GPU proof moves to [Plan 34](../34-real-gpu-proof/plan.md) (real-GPU proof), which follows this plan, written after Plan 33 completes on CPU and run before Plan 32, because the priority is to get unblocked and running on GPU, then elegance. U9 depends on the CPU tasks and the review rounds, and still needs the owner's explicit go to promote to main.
2. **Review rounds: at most 2** (owner-agreed). The run contract's guide would give 3 for cross-repository landing work. 2 is accepted here because the change is Agent-only, interim, and replaced by Plan 32, and because the real-GPU proof follows in its own plan. The lead recommends 3 for Plan 32, not for this plan.
3. **The pack extension protocol is its own plan,** [Plan 17](../17-vibecomfy-extensibility/plan.md). This plan adds no new extension key, engine-index row or backend descriptor.

Decided by the owner at about 16:05Z (M-79, [ledger](https://github.com/banodoco/astrid-overnight-2026-11-05/blob/merge-run/2026-11-07/merge-run/DECISIONS-LEDGER.md)):

4. **D1, video with an image but no entry:** `generate video` refuses, with guidance to `--entry h3`, until Plan 32 T6b (U4).
5. **D2, scope:** the amended scope is accepted (the Scope decision above).
6. The `comfyui` and `comfy_wrap` packs are deleted by Plan 32 T2b, superseding the M06-4 hold for them. They stay in this plan.

## Ambiguity pass (8 Nov 2026, from code)

Settled from code at Agent `5eac07e3f`, VibeComfy `e65f4941` and lifecycle `f2948817`, so no owner question is needed:
- **U1 is not network-bound.** It needs no GitHub fetch (M02-43's reason). `tuple_sources` clones three local checkouts named by `ASTRID_RUNTIME_CHECKOUT`, `ASTRID_VIBECOMFY_CHECKOUT` and `ASTRID_TEST_LIFECYCLE_CHECKOUT`. The source gate then requires them clean at the pinned commits (`remote_placement.py:174-190`). CI sets no `ASTRID_TEST_LIFECYCLE_CHECKOUT`, so the tests cannot pass there as is. `PYT_POD` in tasks.md sets all three.
- **U3: the `source_video` rejections are not on the sfx path.** Foley's video is a media input that travels in `managed_assets` and `upload_media`. The host and child rejections cover only the separate `source_video` input, so they stay.
- **U4: the Matrix request does not use `_refs`.** It has no reference images, so it uses `native_h3_continuation`, whose LoRA is locked. The Step 0 is resolved.
- **U4: h3 through `generate` already uses the host bind.** Its own pod route is reached only with `--placement runpod`, so U4 is deletion.
- **U5 is only the dead binder.** The rest of the legacy route is wired into `generic_host.py` (five `endpoint_checkout` imports) and h3's `legacy_prepared` route, so it moves to Plan 32 T6b. `comfy_wrap` and `comfyui` stay here, because Plan 32 T2b deletes them (M-79).
- **U6 reuses the existing verified model cache** (`--model-cache-root`, keyed by the lock row). No `extra_model_paths.yaml` or receipt change is needed. The directory takes the engine contribution key `comfyui`.
- **U7: an engine change with an idle retained pod is refused today** (`adapter.py:461`). Reuse would make that refusal common, so U7 releases the idle pod instead. This is the third change allowed before the stop rule.

### Open owner decisions

None. D1 and D2 were decided on 8 Nov (owner decisions 4 and 5 above).

## References

- [Plan 32](../32-generation-placement-targets/plan.md): the structural follow-up that this plan's outputs feed.
- [Plan 02](../02-consistent-generation/plan.md) and [Plan 06](../06-packs/plan.md): they land with this plan's evidence.
- The merge-run desk, as above.
