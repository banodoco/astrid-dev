# Plan 77 second cut — launcher continuity and observable startup progress

Runtime owns each startup operation for an exact installation and selected realm. Managed workspace inspection and native daemon startup each have a separate operation ID, owner and verification. Admission remains the authority for health and editability. The first start after upgrade, a crash or an ambiguous prior shutdown still runs the full existing verification. The future sidecar is a separate step.

## Operation and ownership

The layer that launches admission establishes an operation identity before the long inspection. Bind it to the exact install/source generation, target realm, invoking owner, and live process birth or an existing custody reference. Runtime acquires the normal realm and workspace fences. Repeated requests for the same owned startup join its status. A request for a different realm, program generation or live owner receives the existing scope or ownership conflict. The launcher keeps one start attempt across the offline inspection and the native admission. Between them, it publishes the starting-service stage. The attempt ID supports display and correlation. Each operation runs its own checks. A successful offline inspection establishes offline verification only.

The installed Runtime’s `startup-status` command reads an owner-only record before the workspace HTTP listener exists. Runtime validates the record using its existing scope, install generation and process-birth checks. The record keeps the operation identity, current stage and observed work counts. It exposes no credential, private path contents or unverified project material. Confirm identity again when joining, and reject swapped, stale, wrong-owner or wrong-generation records. Mark ready only after current realm verification, exclusive custody and that instance's healthy listener all agree.

Runtime owns the start deadline and terminal result. Its bounded handoffs and liveness checks can still report genuine ownership, process, corruption or transport failure. The previous 120 s limit must let an owned healthy verification continue. The detached parent continues observing the same startup owner when its old 125 s wait expires. There is no timeout-driven restart or termination by observers. A failed observer can reconnect. The process lifecycle distinguishes an absent or exited owner from a slow verifier. A terminal bad-integrity result still refuses synchronously and carries the existing reason.

## Progress and callers

Report observable stages such as verifying workspace identity, checking realm data and objects, inspecting accepted history, and establishing service health. Counters can name completed units already visited. Use a total only where the work has an exact known count. Send a stage or heartbeat during long indivisible work, with no fabricated percent or early ready. Keep operation progress distinct from successful verification.

- The detached parent and managed inspection observe the active operation within their own admission stages. The launcher’s attempt identifies the service-start gap, and the native service verifies under its own operation ID.
- Agent CLI, the 90 s installer service verifier and the SDK launcher use the same operation status. Their individual I/O deadlines can bound a request. A pending status keeps waiting or returns an explicit resumable pending receipt without aborting the active operation, inducing retry/rollback or reporting corruption. OS relaunch applies to actual terminal failures. It never starts a second process merely because an observer’s wait elapsed.
- The local App launcher observes startup before launching the normal editor health and preview checks. The healthy Runtime and editor-ready markers stay after verified admission. Hosted editor pre-ready reporting requires a separate authenticated door design and ships later.


## Slice 1 integrity statement

Status and guarded inspection bind to the expected configured realm UUID and root. When the public caller has supplied neither value, Runtime captures the configured pair and rechecks it before returning an observation or assigning an inspection. Admission still verifies the existing current realm, history, custody and listener. A caller observing progress has no authority to restart an owner, roll back a launch or declare corruption.

The launcher custody check prevents two honest launchers from interfering with each other. It uses the verifier’s current kernel parent PID and ordered process birth. A launcher acting as a namespace init or subreaper can adopt an orphan that satisfies those checks. A hostile process running as the same user can already edit the realm’s files and falls outside this custody model.

The final launch uses the realm selected at admission on both the direct and managed routes. The final launch does not carry the caller’s expected realm UUID and root. A selection change after the last status check can start the newly selected realm. The existing post-start identity check then reports the mismatch. The Lead kept ordinary unscoped startup behavior and queued binding of both launch routes behind the first-cut landing and the remaining installer verifier, SDK and App caller work. The launch-binding step starts with its own reviewed design. [Launch-binding issue #1611](https://github.com/banodoco/astrid-dev/issues/1611)

## Proof before promotion

Fail first at the old clock boundary. Exercise both managed offline inspection and native detached/foreground startup with a valid realm whose full pass crosses the old budget. Check the exact owner and operation ID, progressing status across former caller deadlines and verified health at completion. Observe the same owned operation from two callers. Check absent and dead owner, mismatched process birth or install generation, stale record, real corruption and a custody conflict. An observer disconnect/reconnect leaves Runtime verifying the same lease.

Repeat the existing protected accepted-history corruption and active-restart assertions with no fixture or test relaxation. Keep the exact doctor checks, current startup integrity requirements, held browser route boundaries and Runtime refusal semantics. Measure startup milestones independently of editor navigation on the next exact installed stack. Review must challenge a false ready, double launch, stale status, process reuse and interruption following offline success. [Current clock inventory](../startup-timer-inventory/RESULT.md) [Earlier integrity analysis](../second-cut-design/DESIGN.md)
