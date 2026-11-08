# Inputs — Real-GPU proof of generation

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — the owner asked on 8 Nov 2026 for a GPU-tests plan to follow Plan 33 (merge-run desk `merge-run/DECISIONS-LEDGER.md`, M-78 and M-79). Next: the owner gives the go and a RunPod budget once Plan 33's review passes.

**Prior art:** the live RunPod attempts of 7–8 Nov 2026 and their records in `banodoco/astrid-overnight-2026-11-05`, branch `merge-run/2026-11-07`:
- `merge-run/live/outputs/final/`: image and edit passed; voice failed four times; music never produced an output; sfx was refused; h3_av was not run.
- `merge-run/path-review/EXISTING-MACHINERY.md`: volume, reuse and VibeComfy commands.

**Approach:** run VibeComfy smoke on the pod first, then the Astrid route, and route failures rather than patching them. This keeps hardware problems separate from routing problems.

**Challenge:** Not needed — a proof-only plan with no code changes; failures go to the owning plans.

**Proof and limits:** recorded outputs per slot with exact revisions, a pod census, and volume reuse. Limits: one region, the available GPU types, and no performance claims.

## Source identities

Set when Plan 33 lands: the Agent, Runtime, VibeComfy and lifecycle SHAs of its landing candidate, the storage volume id and its datacenter.

## References

- [Plan 33](../33-unblock-live-generation/plan.md): the candidate under test.
- [Plan 32](../32-generation-placement-targets/plan.md): the second pass.
