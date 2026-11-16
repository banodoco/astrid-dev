# Plan 55 decisions — implementation continuation

[Plan](plan.md) · [Inputs](inputs.md) · [Tasks](tasks.md)

This append-only log records the owner's decisions and consequential implementation
choices for the existing run `2026-11-15-local-speed`. Accountable manager remains
`chatgpt-workspace-6ee41b0f0cca/root`. It does not replace the original ignored
run configuration or its evidence. Read newer owner replies before acting.

## Owner approvals — 16 November 2026

Source: the owner was shown four explicit requests in this same conversation:
the exact LS-5 re-pin, the bounded LS-6 scope extension, the fixture-only Windows
secure-directory repair and original-command retry, and the tasks-only progress
exception. The owner replied: "Yes, you can use the connection improvements as
well. And yeah, you can do all that stuff across the board. So please keep going",
and required decisions to be logged in astrid-dev.

This approves those four requests; it is not unlimited authority to change pins,
permissions, product guarantees or release policy.

### D10 — LS-5 connection integration and exact re-pin: approved

Approve Agent's VibeComfy dependency change from
`dba38f8644c46f652376f2cd5112ea161e40f09b` to
**`7fde33e2523281f840121b93a8a865a7f5d847de`**, using the existing pin generator
and its associated recipe/digest updates, for Plan 55 integration and testing.

The [original request](evidence/ls5-repin-request.md) names the seven generated
surfaces and the composed tests. No Runtime, lifecycle or ComfyUI re-pin is
included. Templates and dependency declarations are expected unchanged and must
be checked. Preserve guarded loopback/attested transports, redirect and proxy
refusal, bounded responses, per-attempt witness/journal custody and no replay
after uncertain acknowledgement. Pod contracts are regression-tested, not a
new rented-machine optimization workstream.

Implementation and proof land through task PRs into `release/14/plan-55`.
Later pins, product-main promotion and publication remain separate gates.

### D11 — LS-6 bounded implementation scope: approved

Approve the additional Agent, VibeComfy and Runtime files/repository boundaries
in [the existing scope request](evidence/ls6-scope-request.md). This permits
carrying the original retrieval digest and length through the result path,
bounded streaming over existing object routes, and tracked Runtime-backed
thumbnail follow-up rather than an untracked thread.

The outcome is unchanged: success means stored and recorded; every caller goes
through Runtime; the caller gets an independent copy; no writable CAS path or
broader worker authority is exposed. Necessary Runtime integrity checks stay.
Do not remove caller verification merely because an earlier read was verified.

The protocol and thumbnail-admission design still go through LS-3 and the
existing RS1 before their implementation. Prove mutations, truncation,
exact-length corruption, final response completion, caller disconnection and
attempt/lease/fence isolation. This scope approval does not approve a future
Runtime or VibeComfy re-pin.

### D12 — Windows fixture repair and named retry: approved

Approve a fixture-only correction for P55-WIN-DACL: preserve POSIX handling;
let the unchanged pinned Runtime securely create a fresh pytest-owned Windows
support directory using its existing creator. Do not pre-create it with
mkdir/chmod and thereby supply an unsafe inherited DACL. Existing unsafe
directories must still be refused, not silently repaired.

After the focused positive/negative fixture checks, retry the originally refused
measurement on the repaired candidate:

```text
python -m tests.local_speed_meter_run --output plan55-meter-proof --timeout 1800
```

The original refusal remains evidence: Agent `b79080f03b0c0d5e0d3930bb0dfb841629ea3d71`,
run `43913596410`, Windows job `133461734871`, artifact `14247918947`.
Approval covers that correction and retry, not privilege elevation, arbitrary
ACL changes, credential changes, a security-check bypass or a Runtime re-pin.
Another materially different permission refusal returns to the owner.

### D13 — progress-only exception: approved

A PR changing **only `plans/55-local-speed/tasks.md`** may target
`astrid-dev/main` and be merged by the manager after the repository check and
required hosted checks. Keep at most one such progress PR open.

All implementation/evidence task PRs still target `release/14/plan-55`;
product integration drafts target `release/14/main`. Never push
`int/55-local-speed`. Add commits only: no rebase, amend or force-push.
This exception does not permit any product-main merge or release publication.

## Preserved boundaries

D1–D9 and the owner's corrected dependency order remain accepted. Continue all
independent CPU work. LS-3/RS1 use CPU and stand-in measurements; GPU cells do
not hold unrelated implementation. The one RS1 and one final R are not waived.
Both remain 0/1 at this decision checkpoint, spend is $0, and Plan 54 remains
queued. Only LS-11 was complete when these approvals were given.

Be aggressive about in-scope repairs and simplification, record changed
assumptions and before/after proof, and never weaken an assertion merely to
obtain a pass. Calibration durations and component microbenchmarks are not
generation-speed acceptance. Missing/failed measurements are not zero or green.
