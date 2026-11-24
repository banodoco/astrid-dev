# Plan 77 launch binding design additions for #1611

## Slice 1 limits

Managed installer observation applies to post-start verification in managed `up` and `restart`. A fresh same-scope operation can extend the observation while installer verification follows one exact operation ID. Admission and ordinary readiness checks remain authoritative. If the last sample fails while a real native service starts under another operation, the caller can return the existing readiness failure even though that service later becomes ready. This false failure was already possible at the 90-second verification boundary. An observation cannot establish readiness or stop the other service. Install, update, rollback, repair and reconnect stay on their existing paths.

The module entry point can observe an operation already owned by Runtime. The installed Agent entry point still has three existing 120-second waits that the module change does not reach.

## Next design scope

Carry an expected realm UUID and root to native admission on both direct and managed routes. Carry an operation kind and ID tied to the originating native launch attempt across the managed service handoff. Keep the distinction between an attempt label and the Runtime operation ID explicit. The managed service observes its own admission operation by identity, including the case where a same-scope offline verifier holds the ongoing operation.

Give the installed caller a continuous parent-owned reservation from its guarded assessment through native launch and verified handoff. Specify who holds it, what validation the child repeats, what each ownership transition acknowledges and how the parent recovers after interruption. Put reservation, native launch binding and the operation-ID handoff in one lock-order review. A parent waiting for a child must release any lock the child needs to reach admission.

The 300-clip development sample measured a 143.5-second guarded inspection and 148.6-second native submission. Current installed Agent composition can do two guarded inspections before submission, for an illustrative `2 × 143.5 s + 148.6 s = 435.6 s`. Measure the two inspections and admission separately with one continuous reservation and prove any omitted repeat was redundant under that reservation.

Test selection changes at both handoffs, a parent that disappears before native admission, another caller trying to enter during every transition, a same-scope offline operation with a different ID and both supported and unsupported launchers. A caller must refuse if the selected workspace changes. No observer can establish readiness, start a second owner or stop an owner it joined. Ordinary identity, authority and integrity checks must still run.

Before an SDK caller starts its own cold child, a read-only Runtime capability should distinguish a supported installed launcher with a valid configured realm and no active operation from an unsupported or unavailable scope. Bind the answer to the same executable provenance, source manifest, profile and selected realm that native admission will use. This status is capability evidence only. Native admission, a positive exact operation observation and the existing readiness checks retain their own roles. The current `unavailable` answer covers both idle and unsupported callers, so slice 1 defers the owned-cold-child wait and limits the SDK observer to positive exact pending while acquisition is already held.
