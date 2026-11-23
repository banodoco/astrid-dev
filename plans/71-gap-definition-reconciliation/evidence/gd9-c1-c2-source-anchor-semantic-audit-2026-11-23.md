# C1/C2 source-anchor audit — verified identities and semantic remediation

**Prepared 23 November 2026. Source-only; no original HOLD/RS2 rerun, no owner GD-9 acceptance, no canonical migration.**

**Pins:** A frozen RS2 `ca97096ba6893108c90a932479e7473f679c724e`; B GD-6 `6d75abf9cb0d102a1fef494f78dd9184d4e45d1f`; C overlay `70d5ac857e8066f8cacf98cda7b9d5d686a12f71`; observed later main F `5be9a76f2a4037247e2a2d866db27c9d7a411a92`; C2 blob `bba487a5357c5c405b266421af6d49e4c5a2f481`. Proposal #1625 branch precursor `ad1235ee00decc0fa57cec2b03ad643c1f4f1600`. All are dated source observations, not an approved application base.

## C1: independently checked source deltas and exact limitations

Direct source reads confirm A→B's authored membership arithmetic: frozen A has **83** positive relationships; B adds eight distinct plan records P63/P69/P75/P76/P77/P78/P79/P80 with **10** positive declarations, and P18 removes its former F-001 supporting relationship. **83 + 10 − 1 = 92** positives in B. C adds P81 (two), P82 (one), P83 (one): **92 + 4 = 96** positive in C. The 22-gap C1 membership matrix independently sums to **83/92/96** and **60/68/71** distinct linked plans in A/B/C.

**Ancestry warning:** GitHub A→B compare says **DIVERGED, 112 ahead and 39 behind** (B relative to A), so these are comparative *set* deltas, not a single linear merge history or cherry-pick plan. B→C compare is ahead 25/behind 0. No unapproved source replay.

**Historical index limitation:** B's **95 raw** and C's **99 raw** indexed mentions were reported by the GD-6 historic `plans.json` method; **the raw index was not independently rerun on this turn**. The three nonaffirmative cases are P37's rejected AA-001/LS-002 and P18's former F-001; P72's CA-003/CA-005 mentions occur in a coordination `Vision role` and are already excluded by the historic indexing comparison. Affirmative-source counts **92/96** can be checked directly, but they must not be conflated with the 95/99 historic indexed units.

| Inspected source plan snapshot | Actual authored gap IDs | Blob-12 |
|---|---|---|
| P18 A | LS-003, F-001 | `25a3786db23c` |
| P18 B | LS-003 only | `4bc0bced68cc` |
| P63 B | F-001 | `c5bd06345ab4` |
| P69 B | F-004, LS-001 | `490b2c31dc57` |
| P75 B | F-001 | `84eb54fd4fd6` |
| P76 B | F-001 | `7bff0d7937d7` |
| P77 B | F-001 | `2e16d3703552` |
| P78 B | F-004 | `42c5a33cf2e0` |
| P79 B | F-003 | `2759971bd90b` |
| P80 B | F-003, F-002 | `b4d778c69bc5` |
| P81 C | F-008, F-001 | `ece51eccbc35` |
| P82 C | F-008 | `c9c2ca4a4aa3` |
| P83 C | F-001 | `7b0b7193be08` |

**Other semantic checks from frozen plan text:** P44 promises a prospective three-decision trace including failed/changed approach and unfamiliar reader; P53 explicitly disclaims CA-003 closure, P52 disclaims CA-005; P28 expressly proposes legally qualified *authorized implementation* but no issued entitlement, and P47 covers conflicts/migrations without explicit full untrusted-pack refusal. No actual implementation result has been observed here.

**Moving-source F overlay:** D `c84c002b0662e92464aa7e1b89b4d43a2579d373` = 83 total/74 gap-linked/9 coordination/99 positive; E `388ff3370d52671dd392d9f2dd060887a24d1e58` = 85/74/11/99 (P87/P88 coordination); F `5be9a76f2a4037247e2a2d866db27c9d7a411a92` = **86 total/75 gap-linked/11 coordination/100 positive** (new P89→F-001 primary). P75 keeps its F-001 primary and P87/P88 stay coordination notwithstanding other edits. F still has **22 canonical gap IDs; F-004 alone changed blob from A**. These are not delivered results or a current issue census.

## C2: independent 51-file frozen source identity check

Direct exact-A `fetch_file` reads matched **all 22 canonical gap files** and their **C2 `## Closure evidence` line anchors**, and matched the **12-character blob SHA prefixes on all 29 plan files** cited by the C2 appendix. All **69 C2 main rows** match the corresponding **69 appendix IDs and *ordered* plan references**. Correct refs and hashes do **not** establish the entire row's strategic merit or actual behavior.

### Frozen gap source anchors (22/22)

| Frozen gap | Blob SHA-12 | `Closure evidence` line | Scope of check |
|---|---|---:|---|
| [AA-001-sustained-creative-work.md](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/vision/gaps/AA-001-sustained-creative-work.md#L17) | `265a4fcfcf16` | 17 | verified source blob + closure heading |
| [CA-001-creative-challenge-culture.md](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/vision/gaps/CA-001-creative-challenge-culture.md#L17) | `23f119c650ad` | 17 | verified source blob + closure heading |
| [CA-002-contributor-ownership.md](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/vision/gaps/CA-002-contributor-ownership.md#L17) | `3e9e7a90618c` | 17 | verified source blob + closure heading |
| [CA-003-vision-experiments-progress.md](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/vision/gaps/CA-003-vision-experiments-progress.md#L17) | `ad65d65fc1e2` | 17 | verified source blob + closure heading |
| [CA-004-sharing-and-discovery.md](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/vision/gaps/CA-004-sharing-and-discovery.md#L17) | `388f7ca5322e` | 17 | verified source blob + closure heading |
| [CA-005-parallel-contribution.md](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/vision/gaps/CA-005-parallel-contribution.md#L20) | `5334ffa9f26c` | 20 | verified source blob + closure heading |
| [CI-001-agent-learning-loop.md](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/vision/gaps/CI-001-agent-learning-loop.md#L17) | `bccbd695cbb0` | 17 | verified source blob + closure heading |
| [CI-002-federated-knowledge.md](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/vision/gaps/CI-002-federated-knowledge.md#L17) | `589005d2cc1e` | 17 | verified source blob + closure heading |
| [CI-003-public-source-ingestion.md](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/vision/gaps/CI-003-public-source-ingestion.md#L17) | `2492eca0da50` | 17 | verified source blob + closure heading |
| [F-001-platform-reliability.md](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/vision/gaps/F-001-platform-reliability.md#L20) | `0da07176a0ab` | 20 | verified source blob + closure heading |
| [F-002-safe-user-control.md](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/vision/gaps/F-002-safe-user-control.md#L17) | `0c1ee79aee3a` | 17 | verified source blob + closure heading |
| [F-003-creative-execution.md](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/vision/gaps/F-003-creative-execution.md#L17) | `6f2ea533820c` | 17 | verified source blob + closure heading |
| [F-004-pack-lifecycle.md](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/vision/gaps/F-004-pack-lifecycle.md#L17) | `ac3ad9b076bd` | 17 | verified source blob + closure heading |
| [F-005-local-files-cloud-assist.md](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/vision/gaps/F-005-local-files-cloud-assist.md#L17) | `32f4cf04962a` | 17 | verified source blob + closure heading |
| [F-006-fully-hosted-workspace.md](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/vision/gaps/F-006-fully-hosted-workspace.md#L17) | `a3f57ad60dde` | 17 | verified source blob + closure heading |
| [F-007-first-class-sandbox.md](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/vision/gaps/F-007-first-class-sandbox.md#L17) | `9d4c3022f5a9` | 17 | verified source blob + closure heading |
| [F-008-portable-generation.md](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/vision/gaps/F-008-portable-generation.md#L31) | `a37c252e33e4` | 31 | verified source blob + closure heading |
| [LS-001-portable-components.md](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/vision/gaps/LS-001-portable-components.md#L17) | `7301d02b5d99` | 17 | verified source blob + closure heading |
| [LS-002-agent-workspace-control.md](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/vision/gaps/LS-002-agent-workspace-control.md#L17) | `dd35f158db06` | 17 | verified source blob + closure heading |
| [LS-003-full-stack-contributions.md](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/vision/gaps/LS-003-full-stack-contributions.md#L17) | `c4b47ff98b45` | 17 | verified source blob + closure heading |
| [LS-004-cross-modal-foundations.md](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/vision/gaps/LS-004-cross-modal-foundations.md#L17) | `4db0ac10e1fd` | 17 | verified source blob + closure heading |
| [LS-005-agent-managed-tools.md](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/vision/gaps/LS-005-agent-managed-tools.md#L17) | `6f43fe370e07` | 17 | verified source blob + closure heading |

### Frozen cited plan sources (29/29)

| Frozen plan | Blob SHA-12 | C2 plan anchor | Scope of check |
|---|---|---:|---|
| [01-installer-consent](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/01-installer-consent/plan.md#L21) | `8eb7c68a5d55` | 21 | verified frozen blob; scope merit separate |
| [04-concurrent-edits](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/04-concurrent-edits/plan.md#L21) | `29d16543388d` | 21 | verified frozen blob; scope merit separate |
| [08-release1-install-update](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/08-release1-install-update/plan.md#L34) | `80274fe989cb` | 34 | verified frozen blob; scope merit separate |
| [12-multiple-inference-routes](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/12-multiple-inference-routes/plan.md#L23) | `4cdce8cb2f73` | 23 | verified frozen blob; scope merit separate |
| [15-openshell-safe-execution](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/15-openshell-safe-execution/plan.md#L21) | `daa4f2966d8d` | 21 | verified frozen blob; scope merit separate |
| [17-vibecomfy-extensibility](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/17-vibecomfy-extensibility/plan.md#L108) | `543a1e9c6311` | 108 | verified frozen blob; scope merit separate |
| [20-zero-to-first-image](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/20-zero-to-first-image/plan.md#L37) | `f23e43282ab7` | 37 | verified frozen blob; scope merit separate |
| [22-hivemind-protocol](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/22-hivemind-protocol/plan.md#L19) | `8d86e84d7238` | 19 | verified frozen blob; scope merit separate |
| [23-agent-learning-integration](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/23-agent-learning-integration/plan.md#L19) | `041cc0fac25f` | 19 | verified frozen blob; scope merit separate |
| [24-liquid-workspace](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/24-liquid-workspace/plan.md#L19) | `ac9063c8fbb1` | 19 | verified frozen blob; scope merit separate |
| [25-cloud-assist-v1](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/25-cloud-assist-v1/plan.md#L19) | `eb750dd348c7` | 19 | verified frozen blob; scope merit separate |
| [26-fully-hosted-v2](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/26-fully-hosted-v2/plan.md#L19) | `09a8c91a66f1` | 19 | verified frozen blob; scope merit separate |
| [28-contributor-ownership](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/28-contributor-ownership/plan.md#L19) | `89764ef4076c` | 19 | verified frozen blob; scope merit separate |
| [29-update-and-release](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/29-update-and-release/plan.md#L21) | `5c34050bb62c` | 21 | verified frozen blob; scope merit separate |
| [30-update-everywhere](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/30-update-everywhere/plan.md#L19) | `8beb82941215` | 19 | verified frozen blob; scope merit separate |
| [32-generation-placement-targets](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/32-generation-placement-targets/plan.md#L21) | `0378a6013b10` | 21 | verified frozen blob; scope merit separate |
| [33-unblock-live-generation](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/33-unblock-live-generation/plan.md#L21) | `faccdf1475e3` | 21 | verified frozen blob; scope merit separate |
| [34-real-gpu-proof](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/34-real-gpu-proof/plan.md#L37) | `6b73ffc6b7d6` | 37 | verified frozen blob; scope merit separate |
| [37-generate-time-destination](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/37-generate-time-destination/plan.md#L21) | `5e71c3dac9a9` | 21 | verified frozen blob; scope merit separate |
| [41-agent-managed-tools](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/41-agent-managed-tools/plan.md#L19) | `6abdc1b6dde6` | 19 | verified frozen blob; scope merit separate |
| [42-hivemind-public-sources](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/42-hivemind-public-sources/plan.md#L19) | `e7721c28e0fe` | 19 | verified frozen blob; scope merit separate |
| [43-nonvideo-editors](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/43-nonvideo-editors/plan.md#L19) | `177b3b84deaf` | 19 | verified frozen blob; scope merit separate |
| [44-vision-execution-trail](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/44-vision-execution-trail/plan.md#L19) | `6d002198bde3` | 19 | verified frozen blob; scope merit separate |
| [45-component-connections](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/45-component-connections/plan.md#L19) | `bdc69dac84cd` | 19 | verified frozen blob; scope merit separate |
| [46-agent-workspace-operations](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/46-agent-workspace-operations/plan.md#L19) | `709e461a8c0a` | 19 | verified frozen blob; scope merit separate |
| [47-pack-stress-tests](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/47-pack-stress-tests/plan.md#L19) | `169a429dd23b` | 19 | verified frozen blob; scope merit separate |
| [48-one-record-model](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/48-one-record-model/plan.md#L21) | `41efb520bd7e` | 21 | verified frozen blob; scope merit separate |
| [49-contribution-discovery](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/49-contribution-discovery/plan.md#L19) | `d09ca04193f3` | 19 | verified frozen blob; scope merit separate |
| [51-astrid-dev-clean-up](https://github.com/banodoco/astrid-dev/blob/ca97096ba6893108c90a932479e7473f679c724e/plans/51-astrid-dev-clean-up/plan.md#L21) | `8e29e536ebf1` | 21 | verified frozen blob; scope merit separate |

## Reproducible semantic qualification gap and proposed fix

**Finding S1-C2-65/4: NOT INDEPENDENTLY VERIFIED.** Original C2 says **65 proposed row phrasings matched directly** and **four are bounded wording variants**, yet it does **not identify the four row IDs, exact source spans, or individual reasoning** in the public proposal. Frozen source SHA/section-anchor checks cannot by themselves prove a 65/4 semantic partition. The source-author's classification is preserved as historical reporting; **independent 65/4 attestation = NO-RESULT**. Do not invent four IDs.

**Concrete fix requested (source-only, no RS2 replay):** for *each* of 69 source row IDs, an eligible independent source assessor must record (a) exact frozen `Closure evidence` sentence/span, (b) direct paraphrase vs split/combined vs bounded wording variant, (c) cited plan's narrow goal/task text and whether it prospectively promises the outcome, (d) materially different negative/refusal case, and (e) accept/reword/reject. Name the four claimed bounded variants with their actual IDs **or report that the claim cannot be substantiated**. Do not open private HOLD/RS2 data. The assessor, review results and approval are **NO-RESULT**.

**Granularity clarification:** the **68** nonadjacent C2 rows are **68 proposed operational, testable subcriteria derived from the 22 authored gap `Closure evidence` sections**. They are **not** 68 separately authored Markdown acceptance bullets. Many frozen gaps have compound *prose paragraphs*; section-level anchors identify context, not row-level literal passages. Any future canonical criteria, scope expansion or proof-owner appointment needs separate acceptance.

**Preserved exceptions:** F-008-C09 remains adjacent **noncriterion** (paid consent once per lease, complete ComfyUI/VibeComfy ownership, and Plan 13-owned host split expressly outside F-008 closure); CA-002-C02 prospectively within P28 legal scope but no enforceable rights proven; F-004-C03 has untrusted-pack refusal proof missing despite P47's conflict/migration scope. No evidence here turns plans into completed outcomes.

**Original review:** independent RS2 **REWORK 1/1 consumed**, HOLD **1/1 consumed**, historical private counters **UNKNOWN**. All actual positive/adverse outcomes and newly accountable proof owners/verifiers **NO-RESULT**. This evidence-only artifact does not change original #1444, canonical gaps/plan/issue/Goal/App, project ownership, branch protections or releases; **no merge** and deferred Phases 6–7 untouched.
