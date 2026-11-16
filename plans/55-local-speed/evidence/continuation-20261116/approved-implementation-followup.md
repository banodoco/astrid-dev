# Plan 55 implementation decisions and pickup — 16 November 2026

[Accepted approvals](../../decisions.md) · [Plan](../../plan.md) · [Task record](../../tasks.md)

Same run `2026-11-15-local-speed`, accountable manager
`chatgpt-workspace-6ee41b0f0cca/root`. This addendum records implementation
choices and their exact limitations; it is not completion or independent review.
The original ignored run configuration and child worktree remain untouched.

## E1 — Use the existing pin generator, not the obsolete seven-file list

Owner D10 is approved and recorded through dev #765. The exact VibeComfy pin
is `7fde33e2523281f840121b93a8a865a7f5d847de`; later pins remain separate decisions.
The real generator changes six package files, because the separate RunPod
engine declaration named in the old proposal no longer exists at this base.
The shared VibeComfy declaration references both platform recipes. Do not
invent a seventh file or change unrelated locks to match that stale list.

Agent #371 head `5f3fff9790f8c4a658a3af438bf185bc08db609c` carries these generated
bytes. Hosted run `43936115263`, job `133541564887`, checked out the complete
approved source, regenerated with zero tracked differences, and passed the
named Agent pin/recipe and VibeComfy transport checks. The pin is not a
measured speed improvement or completed LS-5.

## E2 — Repair offline trace conversion separately from generation timeouts

The Windows fixture-only DACL correction under D12 passed real positive and
negative security tests. The subsequent default-encoding schema defect was
repaired by reading packaged JSON as UTF-8. Neither fix weakens security.

The retained Windows evidence from run `43934937473`, candidate
`13a6501b730ce1038ed17be893fdb05ac3935d24`, shows both SDK/CLI latency tests and
both separate instrumented tests passing. WPR start, proof and stop return
zero. The later tracerpt conversion reaches about 46 percent before its
independent 180-second conversion deadline returns 124. Native counts
remain NO-RESULT; successful Python tests do not replace native proof.

Chosen repair: separately cap conversion of an already-finished trace at
900 seconds and provide an offline decoder entry point. Keep the product
test timeout, caller timer, original output/task assertions, trace-loss
checks and completed-flush attribution unchanged. Prove the decoder using
the retained ETL before repeating generation. This is a diagnostic runtime
allowance, not a relaxed product-speed target.

The candidate is `91e8af010ef0e177b0f709626bebcdcda5422695` on Agent branch
`p55/windows-trace-decode-20261116`, descended from the newer #359 observer
head `74ed3d7b838a0ced901a12c707b7d3ee2a4cd4eb`. Its focused unit and actual
offline Windows replay checks were submitted; no result is assumed here.
The active #359 ref was not overwritten or pushed during its qualifying run.

## E3 — Preserve the evidence-identity discrepancy rather than hide it

An earlier connector inventory reported Windows artifact `14260928127` as
SHA-256 `e96b3c8ef56f5c5b065f1d90b0d639db22887ec0c4591002d9d3cd7243f99044`.
The first bounded diagnostic rejected a download mismatch before parsing.
A fresh inventory and direct live metadata instead identify the same run's
artifact as `79ff6ce339b569cd769c993705edb9cf4f133439d0b9ccac6d46df7e7da25578`.
Diagnostic run `43942960060` verified the current run/head, downloaded
498,214,489 bytes and independently matched that latter hash. It did not
assert identity with the earlier differently reported local download.

Its small extracted diagnostic is artifact `14263426816`, SHA-256
`aeb41414f0568745b64c419f8116db2c6774fe56352718a3d64878f43821a471`.
Both reported identities and the first rejection are retained. Do not
rewrite the original record or infer a cause for the metadata discrepancy.

The verified Windows archive contains single second-job observations of
66.734 seconds SDK and 32.234 seconds CLI, 13 Comfy requests each, with a
92-byte 16-by-16 PNG. These are baseline samples, not medians, one-megapixel
qualification, or a speed improvement. Offline decoding creates no new
generation measurements. Older Linux statuses must be checked against
their actual archived results; retrieved metadata snapshots have differed.

## E4 — Do not lose or misrepresent the unpublished guarded connection code

Before local execution became unavailable, the guarded held-connection
implementation passed 21 real-loopback socket cases. A retired WebSocket
client-session leak was reproduced and fixed. Those edits are not yet on
#371 and have no verified remote candidate identity.

Last-known supporting workspace: `/mnt/data/plan55-owner-approved-eadow7h3`.
The files are under `agent-ls5/astrid/core/generation/backends/`:
`comfy_target.py`, `vibecomfy_local_server.py`, plus
`agent-ls5/tests/core/generation/backends/test_comfy_held_transport.py`.
Clean proof files are `proof/ls5-held-fixed.log`, `.xml` and `.command.json`.
Recover and inspect those exact bytes before publishing or carrying proof
forward. Do not reconstruct different code from a summary and label it
the tested candidate. This scratch directory is not the original run.

Remaining LS-5 checks include failing closed on custom-opener policy
mismatch, the actual pack progress consumer, a prompt-scoped WebSocket in
the attached stand-in, existing affected-file regression tests and composed
generation proof. Cross-job resident lifetime belongs to LS-15. Keep the
attested pod route, per-attempt witness and no-replay-on-unknown-ack rules.

Local container and Python calls returned backend ClientError, including
trivial reads and an attempt to package these files. No new portable ZIP
was successfully created. Hosted execution and the authenticated GitHub
connector remain available; no new credentials or privileges were added.

## Boundaries and continuation

D10–D13 are accepted, not pending. Task PRs target `release/14/plan-55`;
product integration targets `release/14/main`. The progress-only exception
to astrid-dev/main remains in force; check existing PRs before opening one.
Preserve new work on #359 and any active qualifying run before merging.
Only LS-11 is complete, spend is zero, and RS1/final R are each 0/1 at this
checkpoint. CPU work remains authorised; GPU proof and the final review
stay open. No unspecified re-pin, publication or product-main merge follows
from this addendum. Routes used: Unknown — original bindings unavailable;
direct bounded manager work, not an independent reviewer.

## E5 — Newest completed attached-meter run and bounded-memory Windows replay

Observed on 16 November 2026 from GitHub's finished job steps and actual
job logs, not from the previous queued statuses. Agent #359's current task
head is `d083878970ef1ac04ff11426b8c716397d675a6d`; the append-only
commit repaired the invalid `os.fsync(-1)` observer oracle using a real
closed descriptor. The focused C-error oracle passed on Linux and Windows
in [run 43950915734](https://github.com/banodoco/astrid-agent/actions/runs/43950915734).

The subsequent two-platform [meter run 43951310565](https://github.com/banodoco/astrid-agent/actions/runs/43951310565)
**finished**:

- Linux job `133594213925` **succeeded**. The actual attached SDK/CLI
  stand-in meter returned `status: PASS`, with two latency cases and no
  failures/errors/skips, valid output and task records, and explicitly
  `budget_certified: false`. The native calibration counted nine successful
  flushes (one fsync, eight fdatasync), zero failed, no coverage gaps.
  Original artifact `14272385237`, upload-log SHA-256
  `e9318173bb0f4e4468b4382fe8e9efea7db0f3e6d1baffaa032c876cdd920565`.
- Windows job `133594213473` **failed**. The repaired observer, positive and
  negative secure-directory oracles, UTF-8 schema handling and native
  calibration all passed. The attached meter then returned
  `decode_exit: 124`: the native tracerpt conversion again hit its existing
  180-second limit. It is **NO-RESULT for completed native generation counts**,
  not a security failure or an acceptable speed sample. Original artifact
  `14269207422`, upload-log SHA-256
  `c247c7ab2668c7910e541af0b4ccc811c6f242c768ce6650b803d8dc0025c86d`.

The first offline [replay 43945137375](https://github.com/banodoco/astrid-agent/actions/runs/43945137375)
converted the original saved Windows ETL in about 8m42s inside the separate
900-second deadline, but GitHub cancelled its strict XML iteration at the
35-minute job limit. It returned no native counts. That exposed a bounded-memory
parser defect: cleared Event objects were still attached to their parent.
The support branch `p55/windows-trace-decode-20261116`, head
`18518e0e285f8ccc75b2d7ed9231786d60a649bc`, removes each Event only
*after* its complete decode/yield. Full-scan loss checks, completed-flush
pairing and unknown-owner refusal remain unchanged. The actual existing
native-reader checks (14) and new decoder/streaming oracles (8) passed on
**both** Linux and Windows in [43952611444](https://github.com/banodoco/astrid-agent/actions/runs/43952611444).

The load-bearing replay of the retained ETL
[43951926641](https://github.com/banodoco/astrid-agent/actions/runs/43951926641)
was still running in its strict attribution step at this checkpoint. Do not
merge the decoder or claim native counts based on the unit checks; collect that
exact job first. The parser support branch diverges from Agent #359 only by
its own four additive commits versus #359's separately appended oracle fix;
normal merge after both run gates preserves both histories, never rebase/force.

The confirmed facts have also been posted to the existing
[Agent #359 discussion](https://github.com/banodoco/astrid-agent/pull/359#issuecomment-6929082945).
The earlier conflicting reported artifact identities in E3 remain preserved;
these newer artifact SHA values are the exact upload-log values, **not a claim
of equality to either earlier downloaded copy**. No current D1 warm-model
speed commitment has been proven, no task completion is ticked, and RS1/R
remain 0/1 with spend zero and Plan 54 queued. This is additional evidence,
not an independent reviewer or a permission/re-pin/product-main authorization.
