# Inputs — Timeline edits land and hold

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Proposed on 23 November 2026 at the owner's direction: a second plan, separate from the render plan, that merges the useful timeline fixes from the same session and then iterates on real edits until they work. Filing authority only; no run has started.

**Prior art:** Plans 18, 63, 69, 76 and 77 own the designs around this work; their boundaries are in [plan.md](plan.md#outcome-and-scope). The three donor commits and their two reviews are the starting point. All evidence is held by [Plan 87](../87-render-works/inputs.md).

**Approach:** Land the two sound fixes with tests, replace the unsound exemption with the bounded rule, then use a loop of real edits, each confirmed by read-back and render, as the acceptance test.

**Challenge:** An independent code review and an independent judge both found the exemption unsafe and the media swap sound ([review](../87-render-works/evidence/review/ASTRA-530.md), [verdicts](../87-render-works/evidence/shipplan/VERDICTS.md)). A second opinion on this reshaped plan is pending.

**Proof and limits:** The donor fixes pass focused tests and have never run against a live Runtime. The loop is the first live proof. It covers one test timeline and one film.

**Review rounds:** One round at the end.

**Run start:** Pending — waits on Plan 87's RN-1 and on T1 and T2.

## Owner decisions

| Decision | Options and recommendation | State |
| --- | --- | --- |
| T1 Word-anchored retime | (a) Ship the exemption as written; (b) accept a timing-only edit only when the clip's offset from its resolved word is unchanged, else refuse and name the supported form; (c) refuse all such edits until full word binding exists (Plan 18). Recommendation (b). | Open |
| T2 The test timeline | Use the same heavy timeline the owner supplies for Plan 87, or a separate one built for editing. Recommendation: the same one, so each edit can be rendered on a stack that is already proven to render it. | Open |

## Source identities

- Donor branch: astrid-agent `release/14/r6-fixes`, head `ad10ff6de370db547e3ae2af45311751d228f98f`, cut from `83d5f8fe`, which is contained in `release/15/main`. Commits `24740fdf`, `ad10ff6d`, `d4bf28e4`.
- Earlier single-fix branch: `release/14/fix-occurrence-media-swap` (`53833fd3`, draft PR banodoco/astrid-agent#526); it merges cleanly into `release/15/main` ([inventory](../87-render-works/evidence/eff/inventory.md)).
- Release heads at filing: astrid-agent `release/15/main` `8807f820`; astrid-runtime `23310dc8`; astrid-app `e3dbad64`.
- The film project and its overlay clips live in the data of the session's stack, not in a repository.

## References

- [Plan 87](../87-render-works/plan.md) and its [evidence index](../87-render-works/evidence/INDEX.md).
- Issues: [#1403](https://github.com/banodoco/astrid-dev/issues/1403), [#1404](https://github.com/banodoco/astrid-dev/issues/1404), [#1405](https://github.com/banodoco/astrid-dev/issues/1405), [#1401](https://github.com/banodoco/astrid-dev/issues/1401), [#1402](https://github.com/banodoco/astrid-dev/issues/1402), [#1406](https://github.com/banodoco/astrid-dev/issues/1406), [#1409](https://github.com/banodoco/astrid-dev/issues/1409), [#1430](https://github.com/banodoco/astrid-dev/issues/1430), [#1431](https://github.com/banodoco/astrid-dev/issues/1431).
