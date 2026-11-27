# 10 — Pinokio qualification: engine controls, custody and fully-local

[Final Release 16 programme review](../../releases/16/evidence/final-programme-review.md) records current dependencies, estimates and remaining decisions.

**Project:** Pinokio qualification

**Goal:** Engine Stop/Quit refusal veto, direct custody and fully-local mode, qualified natively.

**Status:** queued

**Owner:** Unassigned

**Estimate:** 1–2 engineering days remaining implementation plus 1–2 incremental integration/qualification days; shared P09/P10/P29/P30 total 6–11 + 3–5, counted once, excluding existing P38/P93/P94/P31 work and venue waits.

**Waiting on:** Existing P07 launcher and consent fix retained; [SC-10](https://github.com/banodoco/astrid-dev/blob/d358b3b9de02c156d8a5576495256d6dea73c577/plans/10-pinokio-qualification/evidence/release-16-scoping/SC-10.md) identifies missing engine refusal-veto, native custody and fully-local paired recovery. R16 needs actual engine and six OS/mode witnesses with P38/P09/P30, not surrogate proof.

**Vision gaps:** [Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (primary). [Supporting gap](../../vision/gaps/F-002-safe-user-control.md).

**Contributing:** [Astrid development skill](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/start.md).

## Release 16 residual

**End state:** the real Pinokio application installs, opens, updates, safely stops and removes Astrid in hosted and fully local mode on Windows, macOS and Linux. Busy/unknown Stop or Quit cannot abandon a live owned task; failure leads to a truthful recovery path and successful retry. User data and unrelated applications remain intact.

P07's launcher/menu/bootstrap and consent behavior already exist. Preserve them; fix only the missing native-engine or paired-recovery seam. This is the engine-specific part of [P09's shared installation programme](../09-install-and-update-confidence/plan.md), not another installer or process supervisor. The [sense-check #2060](https://github.com/banodoco/astrid-dev/issues/2060) confirms that the current hosted row's update leg calls the installer directly; that receipt cannot establish an actual Pinokio Update/Stop/Quit action.

PIN-0 refreshes actual launcher and deployed engine identities. PIN-2 establishes the supported engine API, action/session identity, refusal and terminal settlement early, independently of other project completion. PIN-1 preserves launcher behavior and paired App/Runtime recovery. PIN-3 consumes the reviewed P38 provider and the real PIN-2 contract; it does not reimplement custody. PIN-4 proves six OS × hosted/local cells, including the actual engine's Install/Start/Open/Update/Stop/Quit/Reset/Uninstall actions, busy/unknown refusal, interrupted recovery, same-session retry and user-data preservation. Bind helper bytes before and after any launcher pull.

Keep PIN-1's original focused tests and accepted regression obligations. Use deterministic busy/unknown barriers. Descriptor inspection, Node invocation, queued acceptance, process exit zero or fake engine fixtures are not native action settlement. If a required deployed API is absent, record the exact unsupported capability and consequence. The owner chooses any support-contract change; no silent substitution or extra supervisor is authorized.

PIN-END records the demonstrated outcome and remaining gaps. PIN-PROMOTE hands the reviewed immutable launcher candidate and evidence to P31's single publication. The four-plan shared residual estimate lives in P09 and is counted once. Source implementation, independent review, integrated native qualification and release acceptance remain distinct.

## History and next records

[Tasks](tasks.md) preserve every PIN ID and focused selector. [Inputs](inputs.md) preserve P07/Task L/M4 provenance and their limits. The [previous complete plan](https://github.com/banodoco/astrid-dev/blob/2b43946a85f63a0a114023e271baf4952ed209c2/plans/10-pinokio-qualification/plan.md) retains historical test-robustness findings; only defects that block the retained current journey are launch work. Do not revive an old pre-main promotion lane.
