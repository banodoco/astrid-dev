# Inputs — Reuse across commands

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — on 22 November 2026, in the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG), the owner split the under-a-second work from Plan 81 ("Let's do that split please"); on 24 November 2026 she placed this half in Release 15 and split it again (below).

**Prior art:** Plan 81's research, read at astrid-agent [`048ab307`](https://github.com/banodoco/astrid-agent/tree/048ab307), astrid-runtime [`1758a6df`](https://github.com/banodoco/astrid-runtime/tree/1758a6df) and VibeComfy `e65f4941`: [research-A.txt](../81-once-per-command/evidence/research-A.txt), [research-B.txt](../81-once-per-command/evidence/research-B.txt), [research-G.txt](../81-once-per-command/evidence/research-G.txt). Repeated work between commands: a default workflow 3.44 s to build; `find_entry("h3")` 3.9 s cold and 2.7 s warm; the model registry 1.8 s and 1.5 s. Safe keys: content digests of workflow, companion, compiler, bindings and target schema; pack-source and declaration digests; size and modification time alone can miss an edit. Plan 55's template (`24c68a270`, VibeComfy `d8e61a50`) is bound to one process (`prepared.py` near 594).

**Approach:** Caches only, no new long-running process: shipped-pack and registry results under the install stamp, lazy imports, and a ComfyUI prepared template keyed on structure, with every existing check kept or cached with its invalidation ([why each check](evidence/2026-11-24-why-each-check/README.md)) and the approval receipt checked against the admitted bytes (RA-6). Rejected for this release: the resident host and thin client, which is [Plan 92](../92-generate-within-a-second/plan.md).

**Challenge:** Reviewed — by an independent Codex critic for Plan 81 on 22 November 2026 ([critique.txt](../81-once-per-command/evidence/critique.txt)); accepted: the compiled workflow is not keyed on the prompt (RA-2 fills in prompt and seed); the four reused results need four proofs of freshness (Plan 92's GS-1); the node-list check is the likeliest stage to keep `generate` above a second (Plan 92's D3 and GS-4). The disk-or-resident choice has not had a critique; Plan 92 holds that review.

**Proof and limits:** [plan.md](plan.md#completion); figures are component timings from a shared container; the target rests on real baselines.

**Review rounds:** Recommended: one round at the end (R). Pending — the owner confirms.

**Run start:** Pending — No run is authorized. Next: record the date, tasks, accountable session and limits when the owner starts one.

## Owner decisions

**24 November 2026,** in the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG), after the [floor experiment](evidence/2026-11-24-thin-client-floor/README.md) (0.32 s resident with held results; 4.33 s resident without; disk caches alone near 2 s *est.*):

1. **Order kept.** Caches in Release 15; the resident host and thin client in Release 16. Plan 82 is split in two. **This plan** stays in Release 15: about 3 to 4 days, caches only, no new long-running process, goal about 3 s. It keeps RA-0a, RA-0b, RA-1b, RA-2 and R, and gains RA-6 (the Runtime refuses a mismatched receipt or companion digest; before any cache ships). **[Plan 92](../92-generate-within-a-second/plan.md)**, Release 16, takes the rest as GS-1 to GS-5.
2. **No check is removed.** Each is kept every command or cached with its stated invalidation ([why each check](evidence/2026-11-24-why-each-check/README.md)). Always kept: admission preflight, claimed-machine refusal, host liveness, the task POST, approval derived from the exact admitted bytes, and own and project pack refusals in their original order.
3. **Backend scope.** The prepared-template contract is implemented for ComfyUI only; no Wan2GP work, and it must not preclude another backend.

**D1** (resident or disk) moved to Plan 92, recorded "resident first, supported by the floor experiment". **D3** (ComfyUI's node list) moved with GS-4.

**D2 — trusting an install.** Status: **decided, yes** (the owner, 24 November 2026, in the Release 15 Lead session, with her go for this plan's dispatch). Yes for shipped packs, once installed files are made read-only so the stamp covers them (the owner agreed to the idea on 22 November 2026 as Plan 81's D3). Own and project packs keep a per-command witness check (Plan 92).

**The owner, 22 November 2026:** "could we preload stuff once it's loaded once? ... why do we need to?" and "is there any way we could have [ComfyUI] ... give a signal when a new model ... has been updated to do the qualification stuff, or ... where a new custom node is installed, could there be a trigger for that?" These led to RA-0 and, in Plan 92, GS-1 and GS-4.

## Source identities

No code work has started. Read on 22 November 2026: astrid-agent `aac1ceb6`; astrid-runtime `1758a6df`; VibeComfy `e65f4941`. Floor experiment: Agent `a09ea669`, Runtime `24e2c929`, VibeComfy `c0e910ca`. At run start record the release, the plan branch `release/15/plan-82` in astrid-agent, astrid-runtime and VibeComfy, the commit each was cut at, and the Plan 81 commit it builds on.

## References

- [Plan 81](../81-once-per-command/plan.md): the first half, its research and its critique.
- [Plan 92](../92-generate-within-a-second/plan.md): the other half. [Plan 55](../55-local-speed/plan.md): the resident process; [Plan 75](../75-fast-saving/plan.md): its timeline counterpart.
- [#1293](https://github.com/banodoco/astrid-dev/issues/1293): why one workflow takes 3.4 s to build and one entry up to 3.9 s to find is not known; a cheap fix underneath would shrink this plan.
