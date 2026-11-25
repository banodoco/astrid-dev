# RS2-C1 — Source-version and affirmative relationship reconciliation (REWORK proposal)

**Preservation draft — NOT MERGE-READY.** Source qualification is incomplete. All source-derived counts, memberships, scope assignments and outcome claims below remain provisional; where not independently checked against an established non-HOLD source, the result is **NO-RESULT**. No ownership assignment, outcome, review acceptance, migration approval or project completion is implied.

**Status:** Exact original independent RS2 review returned **REWORK**; its only authorized round is **1/1 consumed**. This is a prospective correction to *proposal evidence* only, not canonical migration, no new independent RS2 review. All 22 IDs stay provisionally unchanged. The original report and signed pre-read attestation have been checked privately and must **not** be placed in GitHub.

**Three distinct pin/denominator/unit pairs:**

| State | Frozen source | Plans / linked plans | Raw indexed gap mentions | Affirmative authored links | Served gaps | Routes | Meaning |
|---|---|---|---|---|---|---|---|
| **A — RS2 project proposal** | `ca97096ba6893108c90a932479e7473f679c724e` (tree `d0973b101dc80dcb9e750b156662f7ab22aac58b`) | **69 / 60** | 83 | **83** | **20** | **2**: CA-005, F-008 | The only actual tree reviewed by RS2, with 8 contributor-plan statements and 52 linked plans lacking one |
| **B — GD-6 census** | `6d75abf9cb0d102a1fef494f78dd9184d4e45d1f` | **77 / 68** | **95** (historical worker index) | **92** after excluding false-positive comparison/former-role IDs | **21 as indexed / 20 affirmative** | **3**: CA-005, F-004, F-008 | The fixed GD-6 source and 232-issue cutoff; counts are historical, not frozen A |
| **C — later overlay** | `70d5ac857e8066f8cacf98cda7b9d5d686a12f71` | **80 / 71** | **99** (historical worker index convention) | **96** affirmative | **20** affirmative | **3** | Adds P81/P82/P83 and four positive relationships; not part of A or B |

**Method:** A was extracted from the actual 69-plan source audit of the original independent reviewer (verified 69 plans, 83 explicit links, 60 linked, 8 contributor plan statements). B is the source-pinned `plans.json` metadata in the original GD-6 transfer. It stores 95 literal ID matches, **not** 95 unambiguous positive relationships. To compare positive authored relationships fairly, remove only explicit rejected/former roles from that index. C is B plus four separately verified positive authored links in Plans 81–83. In all three versions, plan links are context unless the plan explicitly promises a closure criterion. The reviewer did not inspect raw GD-6 historical issue bodies; neither did this correction.

**False-positive cases essential to C1:** [P37](https://github.com/banodoco/astrid-dev/blob/6d75abf9cb0d102a1fef494f78dd9184d4e45d1f/plans/37-generate-time-destination/plan.md#L17) lists F-003 as primary and *explicitly rejects* AA-001 and LS-002: **−2** B indexed IDs. [P18](https://github.com/banodoco/astrid-dev/blob/6d75abf9cb0d102a1fef494f78dd9184d4e45d1f/plans/18-timeline-editing/plan.md#L15) now assigns only LS-003 and says former F-001 responsibility moved to P63: **−1** B indexed ID. [P72](https://github.com/banodoco/astrid-dev/blob/6d75abf9cb0d102a1fef494f78dd9184d4e45d1f/plans/72-composable-project-delivery/plan.md) links CA-003 and CA-005 only to **disclaim** closing either; the historic index already excludes those two links and neither is a delivered route. Thus **95 indexed − 3 in-context but non-affirmative identifiers = 92 positive links**, whereas the earlier preliminary manager draft's claim of 93 was wrong. In C, 99 indexed − 3 = 96 positive links (not 97). A→B 83 + 10 new positive links on eight new plans − one removed P18 F-001 = 92. The 22 gap IDs remain unchanged throughout.

**Missing/route effect:** A has two unserved gaps **AA-001 and CA-001**, and only CA-005/F-008 have authored routes; F-004 on A is blob `ac3ad9b076bddeb1320c748f6f4c2fee4b56c191` with *no route*, and P78 does not exist there. At B, F-004 blob `41e9160f8bfb7d3345899a676031cc4cc9ebcaa5` adds a **partial P78 route**, with broader lifecycle proof explicitly unplanned. A’s 18 served-but-unrouted gaps and B’s 17 *affirmatively* served-but-unrouted gaps are different memberships; the old B index’s 18 follows its false-positive AA-001 inbound classification. Do not silently claim one set is the other.

**Per-gap replay-safe positive-link membership** (IDs in lists are plan numbers, not completed deliverables):

| Gap | Frozen A positive inbound | GD-6 B positive inbound | Later C additions | A/B route |
|---|---|---|---|---|
| AA-001 | — | — | — | no / no |
| CA-001 | — | — | — | no / no |
| CA-002 | P28 | P28 | — | no / no |
| CA-003 | P44, P53 | P44, P53 | — | no / no |
| CA-004 | P49 | P49 | — | no / no |
| CA-005 | P48, P51, P52, P58, P73 | P48, P51, P52, P58, P73 | — | yes / yes |
| CI-001 | P23 | P23 | — | no / no |
| CI-002 | P22, P23 | P22, P23 | — | no / no |
| CI-003 | P42 | P42 | — | no / no |
| F-001 | P07, P08, P09, P10, P18, P26, P29, P30, P31, P38, P39, P50, P54 | P07, P08, P09, P10, P26, P29, P30, P31, P38, P39, P50, P54, P63, P75, P76, P77 | P81, P83 | no / no |
| F-002 | P01, P04, P10, P15, P25, P26, P27, P29, P35, P36, P40 | P01, P04, P10, P15, P25, P26, P27, P29, P35, P36, P40, P80 | — | no / no |
| F-003 | P02, P12, P16, P20, P25, P27, P32, P33, P34, P37, P59, P64, P65, P66, P67, P68, P70 | P02, P12, P16, P20, P25, P27, P32, P33, P34, P37, P59, P64, P65, P66, P67, P68, P70, P79, P80 | — | no / no |
| F-004 | P06, P11, P47, P57 | P06, P11, P47, P57, P69, P78 | — | no / yes |
| F-005 | P25, P35, P36 | P25, P35, P36 | — | no / no |
| F-006 | P26 | P26 | — | no / no |
| F-007 | P15 | P15 | — | no / no |
| F-008 | P12, P17, P32, P33, P34, P40, P50, P54, P55, P56, P59 | P12, P17, P32, P33, P34, P40, P50, P54, P55, P56, P59 | P81, P82 | yes / yes |
| LS-001 | P24 | P24, P69 | — | no / no |
| LS-002 | P46 | P46 | — | no / no |
| LS-003 | P06, P17, P18, P45, P57 | P06, P17, P18, P45, P57 | — | no / no |
| LS-004 | P43 | P43 | — | no / no |
| LS-005 | P41 | P41 | — | no / no |

**Application base decision:** Rework source/diff is pinned to project branch A at `ca97096ba6893108c90a932479e7473f679c724e`. The **eventual** canonical gap/plan/application write base is `astrid-dev/main` at a **future owner-approved GD-9 exact SHA**, which is **not yet pinned or authorized**. Recalculate per-gap memberships and App feed/Goals compatibility at that time; no mechanical replay of A/B/C is permitted today. Preserve issue cutoff and all historic counts as dated evidence, not live statuses. Plans 53/73/App retain their separate owners. No change to canonical `vision/gaps`, IDs, issue labels, task statuses, releases, public feed or scopes.
