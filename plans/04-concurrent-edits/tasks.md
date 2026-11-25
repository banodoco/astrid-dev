# Tasks: refined concurrent editing

> **Draft reconciliation:** The dated Release 16 proposal below supersedes conflicting historical scope or dependency wording for review only. Existing statuses, decisions and delivery authority remain the historical record until the owner accepts a change.

[Plan](plan.md) · [Inputs](inputs.md) · [Project status and owner](../index.md)

## Task index

| ID / outcome | Route and dependency | Progress |
|---|---|---|
| [CE-FINAL](#ce-final): accept exact retained tuple | N / Luna · App repair, CE-LIMIT, retained Agent and Runtime | Not recorded |
| [CE-REPAIR](#ce-repair-only-if-required): fix a demonstrated boundary failure, if any | S / Sol + Luna · exact CE-FINAL failure | Conditional; not recorded |
| [CE-END](#ce-end): existing project END review | Review / Astra · CE-FINAL, CE-0, CE-LIMIT | Not recorded |
| [CE-COMPOSE](#ce-compose): compose CE inputs after generation integration | X / Terra + Luna · CE-END and generation integration promotion | Not recorded |
| [CE-REVIEW](#ce-review): review exact composed heads | Review / Astra · CE-COMPOSE | Not recorded |
| [CE-PROMOTE](#ce-promote): promote reviewed immutable heads | N / Luna · CE-REVIEW | Not recorded |
| [CE-REF](#ce-ref): dev reference builder on commitTimeline | X / Terra + Luna · none recorded; fixes App CI Lanes/quick-journey | Not recorded |

## Task details

### CE-FINAL

- **Outcome / work:** Independently verify the retained concurrent-editing tuple, retaining code and fixture repairs. The App repair's full eight-case verification passed, but CE-2 still requires independent final acceptance. Prior 351 SDK passes are reusable only for unchanged internals; they do not establish acceptance of a newly composed tuple.
- **Route:** N / Luna.
- **Dependencies and inputs:** Verified App repair, CE-LIMIT, and retained Agent/Runtime inputs; see [inputs](inputs.md#starting-code-and-branch-policy).
- **Focused checks:** Run the seven SDK nodes below and the original, unchanged full-eight hosted wrapper (J1–J5 variants and recovery) on the recorded Agent/App/Runtime tuple. There are seven SDK nodes and eight hosted cases. The older CE-2 contract selects four SDK files; retain that file-level selection when applying that contract. Reuse independent evidence only when tuple, wrapper, and selection match exactly; changed dependencies or composition require affected final checks. Include CE-LIMIT's existing explicit check. Run migration/owner negative regression only if a merge changes those boundaries. Do not run full SDK/UI suites or weaken restore, lost-ACK, or unknown-flight assertions. In-scope failures present before the change remain blocking; unrelated baseline failures remain out of scope.
- **Done:** Independent verifier passes all seven SDK nodes and eight hosted cases on the recorded tuple, without replaying unchanged 351 nodes.

SDK selectors in `tests/sdk/test_timeline_ce2_retry.py`:

- `test_ce2_pending_user_editing_refusal_is_retryable_via_tl_retry`
- `test_ce2_resend_preserves_body_key_base_flight`

SDK selectors in `tests/sdk/test_timeline_sync.py`:

- `test_user_editing_deadline_includes_an_unanswered_post`
- `test_user_editing_http_wait_uses_single_budget_and_saves_acknowledged_refusal`
- `test_user_editing_backoff_reaching_cap_does_not_resend`
- `test_user_editing_http_timeout_keeps_unknown_flight_with_single_budget`
- `test_restore_lost_ack_retries_exact_request_after_reload`

The CE-LIMIT check selector and the exact identities/definitions of CE-0 and CE-LIMIT are not present in the supplied card; recover them from the source evidence at setup. Do not infer them.

### CE-REPAIR, only if required

- **Outcome / work:** Reproduce a newly demonstrated failed boundary and repair its cause with one owner.
- **Route:** S / Sol + Luna for unresolved concurrency or ownership invariants; ordinary fixture/setup repair is N / Luna. Sol is not for setup or test-running.
- **Dependencies and inputs:** Exact failure from CE-FINAL.
- **Focused checks:** Recheck the failed boundary and affected neighboring checks; preserve unknown flights, late acknowledgements, request body/key/base/fence, deadline, and user edits.
- **Done:** Same boundary and affected neighboring checks pass.

### CE-END

- **Outcome / work:** Conduct the existing project END review of required outcomes and the exact tuple.
- **Route:** Review / Astra.
- **Dependencies and inputs:** CE-FINAL, CE-0, and CE-LIMIT.
- **Focused checks:** Existing END scope; no new review stage or budget is specified here. Recover accepted review details at setup.
- **Done:** No blocking findings; real hosted outcomes, SDK guarantees, and the cooperative limit are evidenced.

### CE-COMPOSE

- **Outcome / work:** After generation integration, freeze rolling `pre-main`, compose accepted CE Runtime, Agent, and App inputs once, and regenerate canonical pins/locks.
- **Route:** X / Terra + Luna.
- **Dependencies and inputs:** CE-END and generation integration promotion; exact inputs and current bases in [inputs](inputs.md#starting-code-and-branch-policy).
- **Focused checks:** Preserve generation/installer behavior while integrating lease/retry/save contracts; run affected final checks, including the tuple checks specified above. Do not assume historical evidence proves the composed tuple.
- **Done:** Actual final tuple passes its affected checks.

### CE-REVIEW

- **Outcome / work:** Review the composed tuple and changed-boundary proof.
- **Route:** Review / Astra.
- **Dependencies and inputs:** CE-COMPOSE; exact immutable candidate heads.
- **Focused checks:** Existing scoped review; retain its accepted scope and remaining rounds.
- **Done:** No blocking integration findings on the exact immutable heads.

### CE-PROMOTE

- **Outcome / work:** Publish fresh immutable increment lanes and promote those same heads to `pre-main`.
- **Route:** N / Luna.
- **Dependencies and inputs:** CE-REVIEW and its exact reviewed heads.
- **Focused checks:** Verify remote heads equal reviewed heads; reconcile moved targets and rerun affected checks under the [run contract](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/shared/run-contract.md).
- **Done:** Exact reviewed heads are promoted; no force push and no second aggregate. Existing project/initiative authority governs publication.

### CE-REF

- **Outcome / work:** Move the dev reference builder off the retired publish path. Astrid-agent `astrid/core/dev/reference_realm.py` `build_reference` still calls the retired `publish_parent_composition`, which fails App CI Lanes/quick-journey. Rebuild it on `commit_timeline` as a fresh-timeline commit: `track.create` plus `clip.add-media` with a `MediaSelection`, steps, and base revision. Update `tests/journeys/test_journey_plumbing.py` and `tests/journeys/test_quick_journey_f1.py` to match.
- **Route:** X / Terra + Luna.
- **Dependencies and inputs:** Agent source in astrid-agent; the failing App CI Lanes/quick-journey job. No other dependency is recorded.
- **Focused checks:** `tests/journeys/test_journey_plumbing.py` and `tests/journeys/test_quick_journey_f1.py`, plus the App CI Lanes/quick-journey job. Exact selectors TBD at setup.
- **Done:** The builder commits through `commit_timeline`, the two journey test files pass, and the retired call is gone from the builder.

## Proposed Release 16 reconciliation — 25 November 2026

Draft pending independent review and owner scope agreement; preserve existing task progress and accepted decisions. Source: [SYN-01 original](https://github.com/banodoco/astrid-dev/blob/4259785be40565ba940ecb076ca8c9889742d7cf/releases/16/evidence/scoping/SYN-01.md).

keep all seven **Not recorded** statuses and conditional CE-REPAIR. CE-FINAL uses actual R16 tuple and original seven SDK/eight hosted outcomes; recover CE-0/CE-LIMIT/wrapper selectors or get explicit equivalence ruling. CE-REPAIR routes only shown gaps to CC-4b/5b/13/14. CE-END and CE-REVIEW become a named independent concurrency verdict within R0, preserving review scope/limits. CE-COMPOSE replaces retired pre-main/generation-promotion dependency with normal reviewed provider→Agent→App pins. CE-PROMOTE joins the one Release Lead go. CE-REF verifies the now-existing commit_timeline reference builder rather than rebuilding an obsolete missing path. Missing original acceptance remains a real proof blocker. Evidence: [SC-04](https://github.com/banodoco/astrid-dev/blob/cbd951924424ecbad213d3ad999a75ade2aabb51/plans/04-concurrent-edits/evidence/release-16-scoping/SC-04.md), [SC-63](https://github.com/banodoco/astrid-dev/blob/6cf0dda31179711582a6ed0d8fcf76d3456c4de9/plans/63-dependable-saving/evidence/release-16-scoping/SC-63.md), [INV-03](https://github.com/banodoco/astrid-dev/blob/5d924e96aee1a2afdaeeb86131f698f5a57a5daf/releases/16/evidence/scoping/INV-03.md), [AUD-01](https://github.com/banodoco/astrid-dev/blob/43e3e390d6ffe026e6f2a61f0c866b0ac94daf9b/releases/16/evidence/scoping/AUD-01.md).
