# Inputs — Timeline edits land and hold

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — included in Release 15 by the owner on 23 November 2026, recorded in the [Release 15 brief](../../releases/15.md). It is a second plan, separate from the render plan, that merges the useful timeline fixes from the same session and then iterates on real edits until they work. Filing authority only; no run has started.

**Prior art:** Plans 18, 63, 69, 76 and 77 own the designs around this work; their boundaries are in [plan.md](plan.md#outcome-and-scope). The three donor commits and their two reviews are the starting point. All evidence is held by [Plan 87](../87-render-works/inputs.md).

**Approach:** Land the two sound fixes with tests, replace the unsound exemption with the bounded rule, then use a loop of real edits, each confirmed by read-back and render, as the acceptance test.

**Challenge:** Reviewed — an independent code review and an independent judge both found the exemption unsafe and the media swap sound ([review](../87-render-works/evidence/review/ASTRA-530.md), [verdicts](../87-render-works/evidence/shipplan/VERDICTS.md)). A [second opinion](../87-render-works/evidence/astra-plans/OPINION.md) on this plan tightened TE-3's conditions, split the loop into must-pass edits and probes, and removed a double landing of the donor commits ([record](../87-render-works/inputs.md#second-opinion)).

**Proof and limits:** The donor fixes pass focused tests and have never run against a live Runtime. The loop is the first live proof. It covers one test timeline and one film.

**Review rounds:** One round at the end.

**Run start:** Pending — waits on Plan 87's RN-6 and a claimed run. The owner asked for the plans and issues to be set up, not executed.

## Owner decisions

| Decision | Options and recommendation | State |
| --- | --- | --- |
| T1 Word-anchored retime | Decided by the coordinating session at the owner's delegation: accept a timing-only edit only when the clip resolves to the same unique word before and after and its offset from that word is unchanged within one frame at both ends (the full conditions are in TE-3); otherwise refuse and name the supported form. Rejected: the exemption as written (a clip can drift from its word and be snapped back by a later reflow); refusing everything until full word binding exists (blocks the ripple edit a real film needed). | Decided |
| T2 The test timeline | Decided: the heavy fixture built by the App's [`scripts/save-loop/build-fixture.mjs`](https://github.com/banodoco/astrid-app/blob/release/15/plan-77/scripts/save-loop/build-fixture.mjs), standard variant, the same one Plan 87 renders, so every edit can be rendered on a stack already proven to render it. The builder was on `release/15/plan-77` at filing; use the copy on `release/15/main` or `main` if it has landed. The fixture's clips are generated media; the word-anchored cases in the loop (edits 1 and 5) also run on the film project, which has real narration. | Decided |

## Source identities

- Donor branch: astrid-agent `release/14/r6-fixes`, head `ad10ff6de370db547e3ae2af45311751d228f98f`, cut from `83d5f8fe`, which is contained in `release/15/main`. Commits `24740fdf`, `ad10ff6d`, `d4bf28e4`.
- Earlier single-fix branch: `release/14/fix-occurrence-media-swap` (`53833fd3`, draft PR banodoco/astrid-agent#526); it merges cleanly into `release/15/main` ([inventory](../87-render-works/evidence/eff/inventory.md)).
- Release heads at filing: astrid-agent `release/15/main` `8807f820`; astrid-runtime `23310dc8`; astrid-app `e3dbad64`.
- The film project and its overlay clips live in the data of the session's stack, not in a repository.

## References

- [Plan 87](../87-render-works/plan.md) and its [evidence index](../87-render-works/evidence/INDEX.md).
- Issues: [#1403](https://github.com/banodoco/astrid-dev/issues/1403), [#1404](https://github.com/banodoco/astrid-dev/issues/1404), [#1405](https://github.com/banodoco/astrid-dev/issues/1405), [#1401](https://github.com/banodoco/astrid-dev/issues/1401), [#1402](https://github.com/banodoco/astrid-dev/issues/1402), [#1406](https://github.com/banodoco/astrid-dev/issues/1406), [#1409](https://github.com/banodoco/astrid-dev/issues/1409), [#1430](https://github.com/banodoco/astrid-dev/issues/1430), [#1431](https://github.com/banodoco/astrid-dev/issues/1431).
