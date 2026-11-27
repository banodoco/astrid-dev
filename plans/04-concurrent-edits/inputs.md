# Inputs: refined concurrent editing

> **Proposed Release 16 reconciliation, 27 November 2026.** Planning corrections only. Historical decisions/evidence remain in [prior inputs](https://github.com/banodoco/astrid-dev/blob/2b43946a85f63a0a114023e271baf4952ed209c2/plans/04-concurrent-edits/inputs.md) and [prior tasks](https://github.com/banodoco/astrid-dev/blob/2b43946a85f63a0a114023e271baf4952ed209c2/plans/04-concurrent-edits/tasks.md). Neither this record nor the investigations authorize execution.

[Plan](plan.md) · [Tasks](tasks.md)

## Evidence and assessment

[Observation #2057](https://github.com/banodoco/astrid-dev/issues/2057), [SC-04](https://github.com/banodoco/astrid-dev/blob/cbd951924424ecbad213d3ad999a75ade2aabb51/plans/04-concurrent-edits/evidence/release-16-scoping/SC-04.md) and [SC-63](https://github.com/banodoco/astrid-dev/blob/6cf0dda31179711582a6ed0d8fcf76d3456c4de9/plans/63-dependable-saving/evidence/release-16-scoping/SC-63.md) identify substantially overlapping residuals, not new implementation programmes. Existing receipt, outbox, conflict and inverse mechanisms remain the foundation.

Independently inspected on 27 November:

| Source | Verified credit / remaining limit |
|---|---|
| Agent R16 `4a2bad187f12e7b0d1ba5bd1164b4a076787516a`, [sync.py](https://github.com/banodoco/astrid-agent/blob/4a2bad187f12e7b0d1ba5bd1164b4a076787516a/astrid/sdk/timeline/sync.py) | Exact flight bytes/key/base/fence and late-ACK matching exist. Default scope remains realm/actor/project/timeline; sibling same-actor writer custody is a residual. |
| App main `cc1d48f016fde55ad6b0609c619d8a4bcec56823`, [localSaveSession.ts](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/tools/video-editor/commands/localSaveSession.ts) | The optimistic document already survives accepted prefixes while queued work drains. Browser capture, recovery and own-undo qualification remain. |
| Agent [reference_realm.py](https://github.com/banodoco/astrid-agent/blob/4a2bad187f12e7b0d1ba5bd1164b4a076787516a/astrid/core/dev/reference_realm.py) | CE-REF's commit_timeline migration is present; current journey qualification is not established here. |
| App [#363](https://github.com/banodoco/astrid-app/pull/363), open head `4be44de85511889539fbf4c1f1e1ba455e322317` | Existing owner-bound accepted-save/draft-cleanup repair and regressions. Unmerged; inspect/adopt compatible work through P63, not a new assignment. |
| Landed App [#375](https://github.com/banodoco/astrid-app/pull/375)/[#400](https://github.com/banodoco/astrid-app/pull/400), Agent [#612](https://github.com/banodoco/astrid-agent/pull/612)/[#648](https://github.com/banodoco/astrid-agent/pull/648), Runtime [#81](https://github.com/banodoco/astrid-runtime/pull/81)/[#123](https://github.com/banodoco/astrid-runtime/pull/123) | P77/P88/P89 opening, media-edit, history/rollback and timing improvements are baseline. Bounded historical proofs do not establish full current two-writer/heavy-undo acceptance. |

No tests, native installed qualification or fresh hosted two-writer run were performed for this planning correction. Definitions are distinct from passing evidence.

## Starting code and branch policy

Use the release's actual authorized predecessor and destination at dispatch. The inspected register was App main `cc1d48f016fde55ad6b0609c619d8a4bcec56823`, Agent R16 main `4a2bad187f12e7b0d1ba5bd1164b4a076787516a`, Runtime R16 main `55a541a7ab904873e63510e581a60742e1b83fb8`. This is a source snapshot, not a frozen execution or installed tuple.

Old Agent `4f111c2153184a73a5ca333a16f4b9a69a3313f1`, App `438159b030cd3b0b81653415f1018f9a1349f0c5` and Runtime `33e9195a8ac57c4ba61f372ef6f25139c37eaa97` remain historical evidence/donors. Do not merge their trees wholesale or revive `lane/M-GPU/integrated`.

P63 owns shared implementation branches. P04 supplies independent acceptance and routes demonstrated failures to that lane. The existing release owner handles one provider → Agent → App pin join and publication.

## Retained SDK acceptance map

The original seven definitions are recoverable at the retained Agent donor. Two CE-2 tests are in [test_timeline_ce2_retry.py](https://github.com/banodoco/astrid-agent/blob/4f111c2153184a73a5ca333a16f4b9a69a3313f1/tests/sdk/test_timeline_ce2_retry.py); five are in [test_timeline_sync.py](https://github.com/banodoco/astrid-agent/blob/4f111c2153184a73a5ca333a16f4b9a69a3313f1/tests/sdk/test_timeline_sync.py). This corrects the implication that their definitions cannot be recovered.

Current correspondence refers to [current sync tests](https://github.com/banodoco/astrid-agent/blob/4a2bad187f12e7b0d1ba5bd1164b4a076787516a/tests/sdk/test_timeline_sync.py). It is an evidence map, **not an approved equivalence or PASS**.

| Original selector | Retained requirement | Current correspondence / remaining work |
|---|---|---|
| `test_ce2_pending_user_editing_refusal_is_retryable_via_tl_retry` | Known refusal is durable pending; retry reviews before writing; contradictory user change preserved; compatible retry one effect | Current pending/retry semantics need mapping. Do not restore a retired editing lease merely to run the old selector. |
| `test_ce2_resend_preserves_body_key_base_flight` | Repeat sends preserve exact bytes, key, base and fence; one acceptance | Current literal-list lost-ACK, duplicate/late-flush and invalid-ACK controls cover related boundaries; complete equivalence unrecorded. |
| `test_user_editing_deadline_includes_an_unanswered_post` | Blocked HTTP consumes the same total deadline; timeout retains unknown flight | Exact-flight retention exists; total-deadline/current-route equivalence unrecorded. |
| `test_user_editing_http_wait_uses_single_budget_and_saves_acknowledged_refusal` | HTTP/backoff share one budget; known refusal durably retained with original flight | Map current outcome/limit behavior; no equivalent selector confirmed. |
| `test_user_editing_backoff_reaching_cap_does_not_resend` | Retry cap prevents another POST and retains the known refusal | Current bounded-retry equivalence unrecorded. |
| `test_user_editing_http_timeout_keeps_unknown_flight_with_single_budget` | Timeout keeps exact flight; unknown is not definitive refused pending | Current unknown-flight controls relevant; single-budget obligation still needs mapping. |
| `test_restore_lost_ack_retries_exact_request_after_reload` | Restore retries the original request after reload without another effect | Selector remains present; execute at final tuple or cite accepted equivalent exact-tuple evidence. |

Relevant current selectors are `test_literal_list_key_replays_lost_ack_exactly_once`, `test_duplicate_flush_and_late_completion_cannot_overwrite_new_flight`, `test_invalid_ack_retains_exact_flight_and_suffix`, `test_conflict_reevaluation_keeps_logical_key_and_uses_fresh_wire_key`, `test_conflict_attempt_unknown_outcome_replays_exact_wire_request_after_reopen` and `test_failed_ack_write_recovers_the_original_flight`. They do not replace the retained cooperative limit or hosted cases by assertion.

## Remaining historical evidence

| Record | Retained claim | What remains |
|---|---|---|
| App repair `438159b030cd3b0b81653415f1018f9a1349f0c5` | Eight hosted cases plus migration/owner and scope checks reported passed | Recover exact wrapper, fixture, selection and logs; historical report does not qualify the current tuple. |
| Historical 351 SDK passes | Evidence for unchanged internals only | Establish correspondence; no automatic transfer to composed inputs. |
| CE-0 and CE-LIMIT | Accepted prerequisites, including explicit cooperative-limit check | Recover definitions, proof and selector. Absence blocks final acceptance, not independent preparation. |
| END review | Existing scope and remaining-round budget | Recover and preserve limits when consolidating into R0. |

If recovery fails, the Lead presents a concrete outcome-preserving replacement and obtains the required owner decision. Do not invent the eight cases, silently narrow them or create another full-suite programme.

## Preserved decisions and cross-project boundaries

P63 [owner decisions](../63-dependable-saving/inputs.md#owner-decisions) remain binding where accepted: D15 parks the refused edit and whole queued suffix; D16 requires deliberate Keep mine for overlap and never automatic overwrite. No per-clip dependency analysis merely to bypass that policy. Discard is scoped to local retained work and cannot erase another writer's custody or prove an unknown attempt never committed.

D11's old same-key/changed-basis wording is not an executable retry contract: request-hash binding requires unchanged bytes for the same attempt. A definitive moved result permits a new attempt key under stable logical intent only after safe reevaluation or explicit decision. Preserve authentication, exact effects, read guards and historical inverse/rollback compatibility.

P79 owns media import facts, stable import identity, receipt reconciliation and small recovery metadata. P63 owns captured placement and save outcomes. Both use the existing P29 reload guard and P35 state-location/migration boundaries; neither adds another recovery store.

Recommend keeping new narrow-by-default semantics and ET-4b safety together in later P76 scope; D17's timing remains pending owner agreement, as recorded in P63. Supported disjoint behavior, true conflict safety and ordinary undo remain mandatory now.

## Qualification and authority

The active CPU packet programme does not replace installed two-writer acceptance. The Lead records an authorized venue and release-blocking verdict before final qualification. A parked blocker remains outstanding.

This reconciliation starts no implementation, reassigns no active writer, merges no code and authorizes no publication. The [shared run contract](../../agent/shared/run-contract.md), repository controls and current owner/Lead decisions govern execution.
