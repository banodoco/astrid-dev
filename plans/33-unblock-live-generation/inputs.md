# Inputs — Unblock live generation on RunPod and locally

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — drafted on 8 Nov 2026 at Hannah's request after the live merge-run proof stalled on voice ("a plan to get it unblocked … and to unblock any of these silly preconditions we've added"), with Plan 32 as the long-term structural plan. Owner @AstridPseudon. Next: the owner reviews this plan together with the independent sense check, and accepts or amends it.

**Prior art:** the work rests on material on the merge-run desk (`banodoco/astrid-overnight-2026-11-05`, branch `merge-run/2026-11-07`):
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
- **Sound effects** is refused on RunPod at four sites (`02f4a7a3d` "FOLEY_REFUSAL … pre-allocation refusal"). The host also rejects `source_video` for URL-attached runs (`generic_host.py:12215-12216`). Media upload for image, audio and video inputs already exists (`local_server_engine.py` upload_media).
- **Pod reuse** is refused across `generate` invocations (`target_selection.py` ~446–452).
- **The whole 95.8 GB lock** is required by readiness (`engine_readiness.py:745-756`). Narrowing it is Plan 32.

**Approach:** finish the one missing wire using VibeComfy's existing target custody, and delete the preconditions that have no product reason (the sfx refusal, the source_video rejection, h3's separate pod route, the legacy route). Lifecycle changes (warm reuse) wait for Plan 32. Alternatives not chosen:
- **Lock-derived inventory:** it claims rows a pod may not have; the receipt is the attested witness.
- **Switching RunPod to the remote-machine model now:** it is the right end state (Plan 32), but h3's existing machine route bypasses paid consent (its spend limit comes from an environment variable), so generalizing it is not a short-term change.
- **A new inventory type or VibeComfy change:** the mechanism already exists.
- **The full Plan 32 redesign first:** too large to unblock the landing.

**Challenge:** Pending — an independent sense check (merge-run desk, `merge-run/path-review/PLAN-SENSE-CHECK.md`) rated this plan good with edits, and those edits are applied: U2 is interim with the receipt rows and a non-circular check; `--align check|trust`; the child-side sfx rejection; h3_av as one run per job; warm reuse dropped; the corrected storage and `comfy_wrap` facts. Next: the owner accepts the plan or amends it.

**Proof and limits:** the CPU pod-path test (U1) and the live matrix (U7). The first pod for each engine still downloads the full lock.

## Source identities

Start from the merge-run candidates, and re-freeze before work:

| Repository | Ref | SHA |
|---|---|---|
| astrid-agent | `cand/plan06-agent-20261107-33` | `5eac07e3fcadf8a6cca7eb6cf77c0fe234590894` |
| astrid-agent (WIP for U2) | bundle `merge-run/bundles/agent-34-wip-e003778be.bundle` on the desk | `e003778bed4998d515d4dd165a948543fee894f0` |
| astrid-runtime | `cand/plan06-runtime-20261107-10` | `b983b0457dffbfd435e74a5c828e129e8ec46ba3` |
| VibeComfy | merge-run pin | `e65f4941` |
| runpod-lifecycle | merge-run pin | `f2948817` |
| poms_packs | `cand/plan06-poms_packs-20261107-10` | `2379ab54aca522019ff4f869cfdf9375bdb56dfc` |
| astrid-app | last candidate `-16` (its PK-14 pass is retracted) | `2191d866f` |

## References

- [Plan 32](../32-generation-placement-targets/plan.md): the structural follow-up that this plan's outputs feed.
- [Plan 02](../02-consistent-generation/plan.md) and [Plan 06](../06-packs/plan.md): they land with this plan's evidence.
- The merge-run desk, as above.
