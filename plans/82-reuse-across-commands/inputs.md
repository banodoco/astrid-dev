# Inputs — Reuse across commands

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — The owner asked on 22 November 2026, in the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG), whether the under-a-second work could be done "in two plans with one half yielding a lot of the results", was given the split by how long a result is kept, and replied: "Let's do that split please". This is the second half. On 24 November 2026 she placed it in Release 15 (below); D1 to D3 are recommended, pending.

**Prior art:** The research is Plan 81's, read and measured on 22 November 2026 at astrid-agent [`048ab307`](https://github.com/banodoco/astrid-agent/tree/048ab307), astrid-runtime [`1758a6df`](https://github.com/banodoco/astrid-runtime/tree/1758a6df) and VibeComfy `e65f4941`: [research-A.txt](../81-once-per-command/evidence/research-A.txt) (the `generate` path to admission), [research-B.txt](../81-once-per-command/evidence/research-B.txt) (the worker, and safe cache keys) and [research-G.txt](../81-once-per-command/evidence/research-G.txt) (a real Runtime timed in a container). What matters here:

- **The repeated work between commands, as components:** one default 10-node workflow 3.44 s to build; `find_entry("h3")` 3.9 s cold and 2.7 s warm; the model registry 1.8 s cold and 1.5 s warm. `generate` with no ComfyUI reachable spent 10.4 s of its own processor time, in pack discovery and file hashing when sampled (`astrid/core/pack/discovery.py:102`).
- **Safe keys, as the worker tracer inferred them:** workflow and companion content digests, compiler version, bindings and target schema digest for graphs; pack-source and declaration digests for entries and registries; validated content digests for pack files. Size and modification time alone can miss an edit.
- **Plan 55's template** (astrid-agent `24c68a270`, VibeComfy `d8e61a50` on `release/14/plan-55`) is bound to one process and session (`prepared.py` near 594).
- **Not measured by anyone:** `generate` to an admitted task with a reachable ComfyUI, and what ComfyUI's node list costs on a real install. Plan 81's US-0 measures both.

**Approach:** Two ways to keep a result between commands, to be chosen by RA-1 on Plan 81's numbers.

| Option | For | Against |
| --- | --- | --- |
| Caches on disk, keyed by content | The command line stays as it is; safe to delete; no process to supervise | Every use must prove freshness, and for ComfyUI's node list there is no cheap proof |
| A process that stays running ([Plan 55](../55-local-speed/plan.md)) | Holds results in memory and can know when they change; also removes the per-job process and polling | Costly to land so far; a lifecycle to supervise; version mismatch between client and process |
| Both | — | Builds one of them for nothing |

**Challenge:** Reviewed — these cards were reviewed as part of Plan 81 before the split, by an independent Codex critic (on the high-judgment role, high effort, read-only) commissioned from the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG) on 22 November 2026; its report is [critique.txt](../81-once-per-command/evidence/critique.txt). What it found that belongs here, all accepted: the compiled workflow must not be keyed on the prompt, or every new prompt rebuilds it (now RA-2 fills in the prompt and seed); the four reused results need four different proofs of freshness (now written into RA-1); the likeliest stage to keep `generate` above a second is the live check of ComfyUI's node list (`astrid/core/generation/backends/comfy_target.py:721`), so the budget is not promised before a real baseline (now D3 and RA-4). The split itself, and the choice between disk and a running process, have not had a critique; RA-1's review is that.

**Proof and limits:** The completion cases in [plan.md](plan.md#completion). Limits: every figure above is a component timing from a shared container running from source; the budget rests on real baselines, not on CI.

**Review rounds:** Recommended: the review inside RA-1, and one round at the end. Pending — the owner confirms.

**Run start:** Pending — No run is authorized. Next: when the owner starts a run, record the date, the tasks it covers, the accountable session, what it may do without asking and what still needs the owner's go.

## Owner decisions

**24 November 2026,** in the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG), recorded by the Lead:

1. **Release.** Plan 82 is in Release 15, not Release 16. (The owner had placed it in Release 16 on 23 November 2026.)
2. **Two layers.** First a general command layer that benefits every backend and pack: a thin client and a warm resident host; caches for shipped packs under the install stamp; the pack-host identity held warm; lazy imports. Then one per-backend "prepare once, fill per request" contract, implemented for ComfyUI only. Wan2GP is not available yet, so there is no Wan2GP work; the contract must not preclude another backend.
3. **No check is removed.** Per the [why-each-check note](evidence/2026-11-24-why-each-check/README.md), each check is kept every command or cached with its stated invalidation. Always kept: admission preflight, claimed-machine refusal, host liveness, the task POST, approval derived from the exact admitted bytes, and own and project pack refusals in their original order.

**The Lead's recommendations, pending the owner:**

- **D1 — a process that stays running, or disk caches.** Status: recommended, pending. Resident host plus thin client first; disk caches only to speed the first command after a restart. Waits on the thin-client floor experiment (evidence/2026-11-24-thin-client-floor, arriving); RA-1 records the choice from it.
- **D2 — trusting an install.** Status: recommended, pending. Yes for shipped packs, once installed files are made read-only so the stamp covers them (a stamp proves bytes only for an immutable install; the owner agreed to the idea on 22 November 2026 as Plan 81's D3). Own and project packs keep a per-command witness check, with their refusals first, in order.
- **D3 — ComfyUI's node list.** Status: recommended, pending. Keep the fetch every command until a real ComfyUI is measured; reusing it until a restart or models-folder change is RA-4's, under the rule that Astrid never refuses from memory.

**The owner's direction, 22 November 2026,** same session: "could we preload stuff once it's loaded once? ... why do we need to?" and "is there any way we could have [ComfyUI] ... give a signal when a new model ... has been updated to do the qualification stuff, or ... where a new custom node is installed, could there be a trigger for that?" These led to RA-0, RA-1 and RA-4.

## Source identities

No code work has started. Read on 22 November 2026: astrid-agent `release/15/main` at `aac1ceb6`; astrid-runtime `release/15/main` at `1758a6df`; VibeComfy at `e65f4941`. At run start record the release, the plan branch `release/15/plan-82` in astrid-agent and VibeComfy, the commit each was cut at, and the Plan 81 commit it builds on.

## References

- [Plan 81](../81-once-per-command/plan.md): the first half, its research and its critique.
- [Plan 55](../55-local-speed/plan.md): the resident process; [Plan 75](../75-fast-saving/plan.md): its timeline counterpart.
- [#1293](https://github.com/banodoco/astrid-dev/issues/1293): why one workflow takes 3.4 s to build and one entry up to 3.9 s to find is not known; a cheap fix underneath would shrink this plan.
