# B-owned Pinokio source-backed action and custody provider

Implement the distinct B Pinokio custody provider/wrapper behind Q's accepted
five-method platform-session contract. Use the same existing Agent worktree
`work/queue/running/M4-6-native-verifier/astrid-agent` on
`r1/M4-6-native-verifier`; observed base is
`64e18fb6b6812e04732f0bedd75e6e0f251ee6a9`. The separate direct-platform
observer task owns `scripts/m4_6_process_observer.py` and direct-provider
tests. Limit this task to `scripts/m4_6_pinokio_custody_provider.py`,
Pinokio-only helpers, and its tests; import the B observer rather than
duplicating OS observation. Q owns `scripts/native_service_adapter.py` and
Windows process-record normalization.
Do not edit Q-owned adapter/shared-driver/checker/workflow files or alter the
five methods. Do not switch branches, reset, clean, or stage the other task's
paths. Use path-scoped `git add` and commit only your files.

Use the immutable pinned-source research already retained at
`work/queue/running/M4-4a-pinokio-source-contract/PINOKIO-ENGINE-CONTRACT.md`
and `evidence/`, for Pinokio client
`pinokiocomputer/pterm@5be43718701c448b43daf0ce51d8935f170065bb`
and daemon
`pinokiocomputer/pinokiod@add4a674ad1ba95bb62ec427fce519fe5bf0e9bf`.
Implement a source-backed wrapper using the pinned request/response and error
semantics, and a separate Pinokio custody observer/provider for every Pinokio
slot. It must independently bind candidate `start.js`, `stop.js`, `update.js`
and resolved helper bytes, the selected installed app, engine/action/session
identity, controller and descendant process incarnations, and the private
transition ledger. Preserve the distinction between queued request acceptance
and terminal settlement. A clean client disconnect or exit code zero is not
success. Refusal, error, timeout, missing task readback, source mismatch,
ambiguous session, observer gap/overflow, or unbound executable must fail
closed before authorization or receipt construction.

Do not execute a descriptor directly with Node, call the installer as a
fallback, invent an engine API, treat a disposable command as an action, or
claim a live Pinokio engine exists. No daemon/action invocation, install,
clone, new worktree, fetch, hosted dispatch, credentials, or central edit. If
the host lacks the real engine/context, implement only the strictly
source-supported wrapper/provider logic that can be proven, leave live admission
closed, and report the exact missing engine-owned settlement/custody facts.
Q has floated the provisional internal type
`scripts.m4_6_trusted_launcher.TrustedCollectorContext`; it is not implemented
or approved authority yet. Coordinate the private context and attempt channel
with Q through shared coordination notes, and use the import only after its
authenticated claim source and binding semantics are reviewed. Do not invent
or stub the context or edit Q files; until then, keep live admission fail-closed.

Run focused existing-environment tests for request settlement/error handling,
immutable action/source binding, distinct direct-vs-Pinokio ownership, and
gap/unknown refusal. Return `REPORT.md` with exact base/head, source citations,
request/settlement contract, immutable bindings, changed paths, checks, Q
coordination, and unresolved live-engine/hosted evidence. No G3/M4-4a/M4-6 or
release claim. Host watcher owns `last.txt`, `exit`, `pid`, and `started`.
