# 10 — Pinokio qualification: engine controls, custody and fully-local

**Project:** Pinokio qualification

**Goal:** Engine Stop/Quit refusal veto, direct custody and fully-local mode, qualified natively.

**Status:** queued

**Owner:** Unassigned

**Estimate:** TBD

**Waiting on:** —

**Vision gaps:** [Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (primary). [Supporting gap](../../vision/gaps/F-002-safe-user-control.md).

**Contributing:** [Astrid development skill](../../skills/astrid-dev/SKILL.md).

Qualify Pinokio Stop/Quit safety, direct custody, fully-local journeys, and unknown-state stop on every supported OS. This follows [Plan 07](../07-pinokio/plan.md), from its verified launcher and gate; no legacy migration is needed because Pinokio had no users when R1 shipped.

## Goal and scope

- **Included:** engine-backed Stop/Quit refusal or safe settlement while Astrid is busy; end-to-end direct custody; the same journey in hosted and fully-local modes on every supported OS; unknown-state stop as a negative control. Also a hosted row that drives the Pinokio app itself (its Install, Start, Stop and Update buttons through `pinokio.js`), which Plan 07's launcher-command rows do not cover. Fully-local CI rows are `pinokio-fully-local-{linux,macos,windows}`.
- **Deferred:** old-launcher compatibility. No dependency on Packs completion; if work is composed into the Astrid product tuple, use then-current reviewed Agent, Runtime, and App pins.
- Native engine veto and settlement semantics, deployed version, supported API, and OS qualification remain to be established. Historical reports, fake fixtures, and adapter lifecycle ordering do not qualify these behaviors.

## What we build on

Plan 07's verified launcher and gate, Task L's interface and validation requirements, and historical M4-4a/M4-6 research. Reconcile each source against current heads before reuse; [inputs](inputs.md) records identities and evidence limits.

## Sequence

Freeze and reconcile source identities (PIN-0), then preserve launcher behavior (PIN-1) and establish actual engine controls (PIN-2). Reconcile custody against current owners (PIN-3); validate and review the exact candidate (PIN-4), record disposition (PIN-END), and publish an accepted launcher increment only under its existing authority (PIN-PROMOTE). See [tasks](tasks.md) for dependencies and selectors.

## Completion

Report only demonstrated outcomes. Missing deployed veto, settlement/readback, or custody evidence leaves that release boundary unqualified with a concrete NEEDS report. A launcher increment may be delivered independently only without unsupported native safety or qualification claims. Publication remains limited to the reviewed immutable candidate and resolved `pre-main` under ordinary create/fast-forward rules; this plan itself authorizes no execution or mutation.

## Carried from Plan 07

Plan 07 (Pinokio basic) closed on 7 Nov 2026 with hosted Linux, macOS and Windows rows passing all six steps on `main` (astrid-agent `709492fa`, App `915bfa84`, Runtime `f4c7a462`, launcher `d15c58b5`; run https://github.com/banodoco/astrid-agent/actions/runs/42421306190). These Plan 07 gaps are now part of this plan:

| Gap | Next step |
|---|---|
| The real Pinokio app is not exercised by the hosted rows: they run the launcher's own commands, not Pinokio's buttons or `pinokio.js` wiring | macOS: the owner tested the real Pinokio app by hand on 5 Nov 2026 and everything worked. Linux and Windows: not yet checked by hand. Add a hosted row that drives the Pinokio app itself |
| A process that ignores the graceful stop is left running after the refusal | Accepted fail-closed limitation; Plan 10 covers engine Stop/Quit |
| The "other Runtime unchanged" process check was dropped (it was macOS-only) | Add a per-OS check |
| A Windows Pinokio install made before the private-record fix keeps its inherited version records, so a stopped uninstall refuses (safely, keeping data) until one Update rewrites them | None needed while Pinokio has no users; recheck if any pre-fix install is reported |
| On fast runners the busy-stop task can finish before Stop lands; the row then sends Stop right after admission and accepts a clean stop, so a busy refusal is not exercised every run | Use a deterministic long-running test task |

## Test robustness

Getting the Windows Pinokio row to pass on 7 Nov 2026 took seven fix-and-rerun rounds. Each 20–40 minute run showed only the next failure, and early rounds had to guess the cause. These changes make one run show every failure, with its cause:

| Gap | Next step |
|---|---|
| A row stops at its first failed step, and its evidence was cut short: the receipt kept only the first 500 characters of an error, and Windows and macOS logs were not uploaded until added one by one | Run every step even after one fails, record each step's full error in the receipt, and always upload every Astrid log and install record for every OS |
| A test candidate is built by hand: repin, commit an App candidate, hash the manifest and install scripts, and start the run. The Release-1 workflow tests the Agent the App pins, not the Agent commit just landed, and forgetting that cost a run | One script that builds a candidate from the commits under test, starts the chosen rows and prints the run link, and refuses when the App does not pin the Agent being tested |
| Windows install records were written with inherited permissions that the Runtime's private read refuses, which caused three separate failures (installed packages, the selection record and version records) | One shared helper that writes every record the Runtime reads privately, plus a cross-repo test that each written record passes the Runtime's own Windows read |

## Read next

- [tasks.md](tasks.md): task index, routes, dependencies, focused checks, and completion evidence.
- [inputs.md](inputs.md): source identities, retained work, provenance, and evidence limits.
- [Project status and owner](../../README.md): queue authority.
