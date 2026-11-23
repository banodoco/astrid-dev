# Inputs — Workflow set-up: one exact plan and one approval

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — this is the original scope of [Plan 56](../56-workflow-setup/plan.md), accepted 15 November 2026 (D1–D3) and extended on 23 November 2026 with the exact-plan approval the owner described in [issue 1731](https://github.com/banodoco/astrid-dev/issues/1731); Plan 56 took the 90/10 for Release 15 and this plan is its follow-up. The owner agreed the numbering on 23 November 2026; Next: the owner picks its release (D1).

**Prior art:** Plan 56's [inputs](../56-workflow-setup/inputs.md#planning-evidence) (code readings of 15–16 and 23 November 2026, the lookup, version and consent findings). Plan 35 owns where user choices live; Plan 32 owns the manifest and F4.

**Approach:** One plan function and digest over Plan 56's approval record; reuse `fetch-models`, `align` and the controlled installer. Alternatives: only the 90/10 (no exact-plan approval, no reusable trust); a per-user trust store first (little value before the plan exists).

**Challenge:** Codex Astra reviewed the 80/20 on 23 November 2026 (critique recorded in Plan 56's inputs). Accepted: terminal approval is a speed bump; one immutable approval record; reusable trust deferred to Plan 35; conflicting pins refused; first-use hashing reduced to saving the download receipt.

**Proof and limits:** Completion is in [plan.md](plan.md#completion). Estimates are inferred.

**Review rounds:** Pending — recommended: RS1 after the plan and approval contract, plus two final rounds; cross-repository security work. Next: the owner confirms.

**Run start:** Pending — No run is authorized. Next: when the owner starts a run, record the date, the phase or tasks it covers, the accountable session, what it may do without asking, what still needs the owner's go, and the advisor session.

## Owner decisions

- **D1 Release.** Which release carries this follow-up? Recommendation: the one after Release 15, once Plan 56 has landed.
- **D2 Reusable trust.** Does it wait for Plan 35? Recommendation: yes.

## Source identities

Planning read: as in [Plan 56](../56-workflow-setup/inputs.md#source-identities). Code work: `release/<NN>/plan-90` from each repository's `release/<NN>/main` for the release D1 picks, recorded at run start.

## References

- [Plan 56](../56-workflow-setup/plan.md) and its [inputs](../56-workflow-setup/inputs.md)
- [Issue 1731](https://github.com/banodoco/astrid-dev/issues/1731)
