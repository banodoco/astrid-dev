# Inputs — H3 continuation, bridges and inserts

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — the redesigned programme, agreed by the owner on 28 Nov 2026 ([#2065](https://github.com/banodoco/astrid-dev/issues/2065))

**Prior art:** The cards were written and reviewed as part of Plan 66. Its [planning evidence](../66-h3-composable-core/inputs.md#planning-evidence) holds the source findings, the direction and functional reviews, the restrictions and ambiguity passes, and the alignment review. The design they follow is in [Plan 66's plan](../66-h3-composable-core/plan.md#outcome-and-scope), shipped as `astrid/packs/h3_av/docs/design.md`.

**Approach:** port only the captured graph's active path into ordinary lowering functions chosen by the arrangement function Plan 66 reserves, after Plan 68 so CC-7a can first compare against the full-canvas source. Alternative considered: running in parallel with Plan 68, rejected because that comparison decides whether bridges and inserts need lowerings of their own.

**Challenge:** Reviewed — the split review of 18 November 2026 ([Plan 66 research/split-review.md](../66-h3-composable-core/research/split-review.md)) checked the cut, the order, the interfaces each plan consumes and produces, and the reservations Plan 66 must make. Its recommendations were accepted.

**Proof and limits:** CPU only (D1). CPU tests prove compiled graphs, refusals, dry-run records and exact delivery; quality is judged in the owner's live check afterwards.

**Review rounds:** Recommend 1: the integrated review (R) of Plans 66, 68 and 70 together, at the end of this plan. Next: the owner confirms.

**Run start:** Lane [h3](../../releases/16/briefs/h3.md): the brief records the owner's go, authority and limits.

## Owner decisions

- **D1 — CPU only (decided 18 Nov 2026, owner in the Plan 59 session: "we're not going to do a GPU test. This is just CPU… We'll do a test afterwards").** No task claims a machine or spends money. Live checks are [Plan 66 D6](../66-h3-composable-core/inputs.md#owner-decisions), pending.

## Source identities

Planning snapshot: as recorded in [Plan 66's source identities](../66-h3-composable-core/inputs.md#source-identities). At dispatch, record the release, its `release/<NN>/main` SHA, the merge SHAs of the plans this one depends on, and the `release/<NN>/plan-<PP>` head.

## References

- [Plan 66](../66-h3-composable-core/plan.md), [its split review](../66-h3-composable-core/research/split-review.md), [Plan 67](../67-h3-community-steering/plan.md).
