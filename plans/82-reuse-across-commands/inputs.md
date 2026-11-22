# Inputs — Reuse across commands

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — The owner asked on 22 November 2026, in the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG), whether the under-a-second work could be done "in two plans with one half yielding a lot of the results", was given the split by how long a result is kept, and replied: "Let's do that split please". This is the second half. She has not chosen its release or answered D1 to D3. Next: she decides after [Plan 81](../81-once-per-command/plan.md)'s second baseline.

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

**Challenge:** Reviewed — these cards were reviewed as part of Plan 81 before the split, by an independent Codex critic (`gpt-6.2-astra`, high effort, read-only) commissioned from the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG) on 22 November 2026; its report is [critique.txt](../81-once-per-command/evidence/critique.txt). What it found that belongs here, all accepted: the compiled workflow must not be keyed on the prompt, or every new prompt rebuilds it (now RA-2 fills in the prompt and seed); the four reused results need four different proofs of freshness (now written into RA-1); the likeliest stage to keep `generate` above a second is the live check of ComfyUI's node list (`astrid/core/generation/backends/comfy_target.py:721`), so the budget is not promised before a real baseline (now D3 and RA-4). The split itself, and the choice between disk and a running process, have not had a critique; RA-1's review is that.

**Proof and limits:** The completion cases in [plan.md](plan.md#completion). Limits: every figure above is a component timing from a shared container running from source; the budget rests on real baselines, not on CI.

**Review rounds:** Recommended: the review inside RA-1, and one round at the end. Pending — the owner confirms.

**Run start:** Pending — No run is authorized. Next: when the owner starts a run, record the date, the tasks it covers, the accountable session, what it may do without asking and what still needs the owner's go.

## Owner decisions

- **D1 — disk, or a process that stays running.** RA-1 recommends from Plan 81's numbers. (a) Caches on disk, this plan as written. (b) Plan 55's resident process, and this plan keeps only the decision and the measurement. Recommendation: none until the baseline. Pending.
- **D2 — trusting an install.** May packs that came with an installed Astrid skip re-hashing, on the strength of the install's stamp, while a person's own packs and project packs are still hashed? The owner agreed to this on 22 November 2026 as Plan 81's D3, before the split; the critique then noted that a stamp proves pack bytes only if the install is stated to be immutable. Recommendation: yes, with that statement made and tested. Pending her confirmation of the condition.
- **The owner's direction, 22 November 2026,** in the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG), after Plan 81's result: "could we preload stuff once it's loaded once? ... why do we need to?" and "is there any way we could have [ComfyUI] ... give a signal when a new model ... has been updated to do the qualification stuff, or ... where a new custom node is installed, could there be a trigger for that?" She asked for both to be added to this plan. They are RA-0, the option added to RA-1, and the rewritten RA-4. The plan stays in no release.
- **D3 — ComfyUI's node list.** Each `generate` asks the attached ComfyUI what nodes and models it has. If the baseline shows that this alone takes most of a second: (a) keep asking every time and state the budget as Astrid's share; (b) reuse the last answer for a short time and refresh when ComfyUI rejects a job; (c) ask ComfyUI for a cheap sign that nothing changed, if it has one. Recommendation, revised 22 November 2026: reuse until ComfyUI signals a change (a restart for nodes; a changed models folder where Astrid runs ComfyUI itself), under the rule that Astrid never refuses from memory; (a) remains the fallback for an attached ComfyUI that offers no cheap check. Whether to add a small helper inside ComfyUI for engines Astrid manages is part of this decision. Qualification measured 0.51 s with a stand-in ComfyUI; a real one's cost is still unmeasured. Pending.

## Source identities

No code work has started. Read on 22 November 2026: astrid-agent `release/15/main` at `aac1ceb6`; astrid-runtime `release/15/main` at `1758a6df`; VibeComfy at `e65f4941`. At run start record the release, the plan branch `release/<NN>/plan-82` in astrid-agent and VibeComfy, the commit each was cut at, and the Plan 81 commit it builds on.

## References

- [Plan 81](../81-once-per-command/plan.md): the first half, its research and its critique.
- [Plan 55](../55-local-speed/plan.md): the resident process; [Plan 75](../75-fast-saving/plan.md): its timeline counterpart.
- [#1293](https://github.com/banodoco/astrid-dev/issues/1293): why one workflow takes 3.4 s to build and one entry up to 3.9 s to find is not known; a cheap fix underneath would shrink this plan.
