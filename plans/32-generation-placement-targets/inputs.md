# Inputs — One generation placement and target lifecycle

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — Hannah agreed this scope on 8 Nov 2026 (recorded in https://github.com/banodoco/astrid-dev/pull/79), with two amendments: (1) a default placement that can be changed per generation (including which local GPU, attached server or RunPod), built towards from the first version; (2) pods and other sessions may outlive a job when warm or explicitly started, governed by a lease with a default idle timeout beyond the job. Owner @AstridPseudon. Sequenced before Plan 12. Estimate about 2-4 days of engineering plus the live proof.

**Prior art:** the merge run's routing map, `merge-run/review/generation-routing-map.md` in `banodoco/astrid-overnight-2026-11-05`, branch `merge-run/2026-11-07`, written while proving `astrid generate --target runpod` live on 7-8 Nov 2026. It lists six placement decision points, two remote mechanisms, five dry-run divergences, three duplicated sfx/foley RunPod refusals and an h3_av-specific pod command in the runpod pack's `remote_placement.py`. About 43 test references are affected, and the routing map estimates 6-10 hours for the Placement half alone. [Plan 02](../02-consistent-generation/plan.md) lands the guard-rail tests and a targeted routing fix first. Next: re-check each cited line against current source before work starts.

**Approach:** compute a frozen Placement once in `GenerationFacade._generate_on_target`, pass it down, and run through one Target interface with local, attached and RunPod implementations. Packs supply only a Job. This replaces the six decision points rather than patching each. Alternatives not chosen: keep patching each site (leaves two mechanisms and the dry-run drift), and let packs own their pod commands (keeps h3_av ignoring `--target`).

**Challenge:** Not needed — at the scope stage. The independent review of the Placement shape (default/override, `device`) and the Target lease semantics is instead the entry gate of task T2 (see [tasks.md](tasks.md)), because it must review the design against the source revision being built.

**Proof and limits:** the invariant test over every default slot x {auto, local, runpod}, dry run == live, and no pod unless execution happens on it (from Plan 02, extended in T1), plus a live matrix of six default slots and h3_av on RunPod and locally (T5). Limits: the live proof needs a RunPod budget and an authorized start that are not yet decided. Fixtures cover refusal and release on failure; they do not replace the live runs.

## Source identities

Not yet recorded. Before code work, record the actual repository, ref and SHA for astrid-agent (`astrid/sdk/generation.py`, `core/generation`, `core/execution/generic_host.py`, `sdk/invocation.py`), the vibecomfy, h3_av and runpod packs, and the merged Plan 02 revision this project consumes. The routing map line numbers come from the merge run branch and must be re-checked against the branch being built.

## References

- Routing map: `merge-run/review/generation-routing-map.md` in `banodoco/astrid-overnight-2026-11-05`, branch `merge-run/2026-11-07`.
- [Plan 02](../02-consistent-generation/plan.md) (predecessor), [Plan 12](../12-multiple-inference-routes/plan.md) (consumer), [Plan 13](../13-execution-host-refactor/plan.md) (host split, excluded), [Plan 25](../25-cloud-assist-v1/plan.md) (would reuse Placement and Target).
