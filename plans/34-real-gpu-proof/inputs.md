# Inputs — Real-GPU proof of generation

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — the owner asked on 8 Nov 2026 for a GPU-tests plan to follow Plan 33 (merge-run desk `merge-run/DECISIONS-LEDGER.md`, M-78 and M-79). Next: the owner gives the go and a RunPod budget once Plan 33's review passes.

**Prior art:** the live RunPod attempts of 7–8 Nov 2026 and their records in `banodoco/astrid-overnight-2026-11-05`, branch `merge-run/2026-11-07`:
- `merge-run/live/outputs/final/`: image and edit passed; voice failed four times; music never produced an output; sfx was refused; h3_av was not run.
- `merge-run/path-review/EXISTING-MACHINERY.md`: volume, reuse and VibeComfy commands.

**Approach:** run VibeComfy smoke on the pod first, then the Astrid route, and route failures rather than patching them. This keeps hardware problems separate from routing problems.

**Challenge:** Not needed. Fixes run as repair tasks on Plan 32's line.

**Owner decision (Hannah, 8 Nov, later):** "live GPU validation on RunPod once this is done, $25 budget, and fix every issue you find". It runs once, after Plan 32, with $25 approved. Every failure is fixed and re-run, not only recorded.

**Proof and limits:** recorded outputs per slot with exact revisions, a pod census, and volume reuse. Limits: one region, the available GPU types, and no performance claims.

## Source identities

Set when Plan 33 lands: the Agent, Runtime, VibeComfy and lifecycle SHAs of its landing candidate, the storage volume id and its datacenter.

## Closed pull request #260: first GPU validation run record (16 Nov 2026)

astrid-dev pull request #260 ("Record Plan 34 first GPU validation", draft), branch `plan34/gpu-validation-2026-11-10`, head `730e7865173737615dcec8d1cf2494ec918ee032`, was closed on 16 Nov 2026 because it cannot merge today: Plan 34 is `queued`, and the record on the branch is an interim one ("paused for handoff") whose pull request text still says no GPU cell has passed. The branch is kept.

- **What it holds:** `validation/gpu/2026-11-10-cc084ebd9.md` (the run of 10 Nov 2026: revisions, 18 pods and their release, censuses, spend), `validation/gpu/2026-11-10-sfx-candidate.md` (the SFX candidate pin audit) and the synthetic fixtures under `validation/gpu/fixtures/plan34-synthetic/`. By its own account: image and music passed, audio sound effects and text-to-speech failed, and i2v, v2v and video-edit were not run.
- **Facts still missing:** results for the cells not run; the final pod census and final spend and balance reconciliation; a final run record (records are add-only, so a completed run needs its own file); the owner's go and budget that the plan still waits on.

## References

- [Plan 33](../33-unblock-live-generation/plan.md): the candidate under test.
- [Plan 32](../32-generation-placement-targets/plan.md): the second pass.
