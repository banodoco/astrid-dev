# 04 — Refined concurrent editing: completion and integration

[README queue](../README.md) · [Initiative handoff](MANAGER.md). Final publication follows [generation merge](03-generation-merge.md); independent completion on the retained tuple may proceed earlier after initiative start.

## Goal

Keep users in control: agent edits must respect user edits, surface conflicts, and retry safely without silently overwriting changes.

Reuse Agent `4f111c2153184a73a5ca333a16f4b9a69a3313f1`, App `438159b030cd3b0b81653415f1018f9a1349f0c5`, Runtime `33e9195a8ac57c4ba61f372ef6f25139c37eaa97`. App's full eight-case repair verification passed; original CE-2 still needs independent final acceptance. Prior 351 SDK passes are reusable evidence for unchanged internals, not proof of a newly composed tuple.

| ID | Action and output | Dependencies | Lead | Done evidence |
|---|---|---|---|---|
| CE-FINAL | Run the exact final tuple checks below, retaining code and fixture repairs. | Verified App repair, CE-LIMIT, retained Agent/Runtime | N / Luna | Independent verifier passes the seven SDK nodes and full-eight hosted cases on the recorded tuple. No unchanged 351-node replay. |
| CE-REPAIR, only if required | Reproduce a newly demonstrated failed boundary; repair its real cause with one owner. | Exact failure from CE-FINAL | S / Sol + Luna | Same boundary and affected neighboring checks pass; preserve unknown flights, late ACKs, body/key/base/fence, deadline and user edits. Sol is reserved for unresolved concurrency/ownership invariants, not setup or test-running. Ordinary fixture/setup repairs remain N/Luna. |
| CE-END | Existing project END review of required outcomes and exact tuple. | CE-FINAL, CE-0, CE-LIMIT | Review / Astra | No blocking findings; real hosted outcomes, SDK guarantees and cooperative limit all evidenced. |
| CE-COMPOSE | Freeze rolling pre-main after plan03; compose accepted CE Runtime, Agent, App inputs once and regenerate canonical pins/locks. | CE-END; plan03 promotion | X / Terra + Luna | Preserve generation/installer behavior while integrating lease/retry/save contracts; actual final tuple passes affected checks below. |
| CE-REVIEW | Scoped review of composed tuple and changed-boundary proof. | CE-COMPOSE | Review / Astra | Exact immutable heads have no blocking integration findings. |
| CE-PROMOTE | Publish fresh immutable increment lanes and promote those same heads to pre-main. | CE-REVIEW | N / Luna | Remote heads equal reviewed heads; moved targets handled by MANAGER.md, no force or second aggregate. |

## Starting code and branch policy

Plan 04 consumes the exact promoted plan 03 Agent/App/Runtime tuple, then the retained CE work: Agent `4f111c2153184a73a5ca333a16f4b9a69a3313f1`, App `438159b030cd3b0b81653415f1018f9a1349f0c5`, Runtime `33e9195a8ac57c4ba61f372ef6f25139c37eaa97`. Those are historical donor/checkpoint identities, not current target heads. A plan-04 merge base was not frozen in the supplied audit; its concrete base is the exact plan-03 promoted Agent/App/Runtime tuple plus then-current destination refs at execution. Audit-time target details were not frozen for this later increment; capture actual current pre-main heads when integration starts and use them as bases. Use fresh isolated candidate branches in touched repos, and promote exact independently reviewed candidates to pre-main. Do not reuse the historical `lane/M-GPU/integrated` lane.

## Exact focused selectors

Two functions in `tests/sdk/test_timeline_ce2_retry.py`:

- `test_ce2_pending_user_editing_refusal_is_retryable_via_tl_retry`
- `test_ce2_resend_preserves_body_key_base_flight`

Five functions in `tests/sdk/test_timeline_sync.py`:

- `test_user_editing_deadline_includes_an_unanswered_post`
- `test_user_editing_http_wait_uses_single_budget_and_saves_acknowledged_refusal`
- `test_user_editing_backoff_reaching_cap_does_not_resend`
- `test_user_editing_http_timeout_keeps_unknown_flight_with_single_budget`
- `test_restore_lost_ack_retries_exact_request_after_reload`

Also run the original unchanged full-eight hosted wrapper (J1–J5 variants and recovery) on the recorded Agent/App/Runtime tuple. There are **seven SDK nodes and eight hosted cases**, not seven hosted cases. Materialize these selectors in the staged card: the old CE-2 contract still selects four SDK files. Reuse identical independent evidence only where exact tuple, wrapper and selection match; changed dependencies or composition require the affected final checks.

Include CE-LIMIT's existing explicit check and the migration/owner negative regression only if the merge changes those boundaries. No full SDK/UI suite. Restore/lost-ACK/unknown-flight assertions must not be weakened to get green. Tests failing before the change still block if they represent these included features; unrelated baseline failures stay outside scope.

Source: [CE-2 card](../references/evidence-summary.md), [CE END](../references/evidence-summary.md), [App repair verdict](../references/evidence-summary.md), [minimal test decision](../references/evidence-summary.md). Freeze any new repaired heads at execution; listed SHAs are retained checkpoints, not instructions to ignore later reviewed work.
