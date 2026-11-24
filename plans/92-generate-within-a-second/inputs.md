# Inputs — Generate within a second

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — see below; the Release 16 half of [Plan 82](../82-reuse-across-commands/inputs.md#owner-decisions).

**Prior art:** the [floor experiment](../82-reuse-across-commands/evidence/2026-11-24-thin-client-floor/README.md), [why each check](../82-reuse-across-commands/evidence/2026-11-24-why-each-check/README.md), Plan 81's [critique](../81-once-per-command/evidence/critique.txt) and [Plan 55](../55-local-speed/plan.md)'s resident-session branch.

**Approach:** A resident host that holds discovery results and prepared templates, and a thin client that sends the request to it, falling back to today's full path when the host is missing or a different version. The [floor experiment](../82-reuse-across-commands/evidence/2026-11-24-thin-client-floor/README.md) measured 0.32 s this way. Rejected: disk caches as the main path, which stay near 2 s; they are [Plan 82](../82-reuse-across-commands/plan.md), kept to speed the first command after a restart.

**Challenge:** Reviewed — Astra's independent critique of the [first-principles note](../82-reuse-across-commands/evidence/2026-11-23-generate-first-principles/README.md#independent-critique-astra-read-only-from-the-first-draft) and the Lead's risk analysis of 24 November 2026, recorded in [plan.md](plan.md); GS-1 also gets its own high-judgment review before it lands.

**Proof and limits:** [plan.md](plan.md#completion); timings come from a container and a stand-in ComfyUI.

**Review rounds:** Recommended: GS-1's, and one at the end. Pending.

**Run start:** Pending.

## Owner decisions

**24 November 2026,** [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG), after the floor experiment: keep the agreed order (caches in Release 15, resident host and thin client in Release 16); about 5 to 6 days, after Plan 82's RA-2 and RA-6.

- **D1 — resident process or disk caches.** Status: decided as "resident first, supported by the floor experiment"; Plan 82's disk caches speed only the first command after a restart.
- **D3 — ComfyUI's node list.** Status: recommended, pending. Keep the fetch every command until a real ComfyUI is measured; reuse until a restart or models-folder change is GS-4's, under the rule that Astrid never refuses from memory.
- **D2** (trusting a shipped-pack install) is [Plan 82's](../82-reuse-across-commands/inputs.md#owner-decisions); GS-2 and GS-3 use it.

## Source identities

No code work has started. Floor experiment: Agent `a09ea669`, Runtime `24e2c929`, VibeComfy `c0e910ca`. At run start record each `release/16/plan-92` branch's commit and the Plan 82 commit it builds on.

## References

[Plan 82](../82-reuse-across-commands/plan.md), [Plan 81](../81-once-per-command/plan.md), [Plan 38](../38-one-process-identity/plan.md).
