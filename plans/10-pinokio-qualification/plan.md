# 10 — Pinokio qualification: engine controls, custody and fully-local

**Vision gaps:** [Platform reliability](../../visions/gaps/F-001-platform-reliability.md) (primary). [Supporting gap](../../visions/gaps/F-002-safe-user-control.md).

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

## Read next

- [tasks.md](tasks.md): task index, routes, dependencies, focused checks, and completion evidence.
- [inputs.md](inputs.md): source identities, retained work, provenance, and evidence limits.
- [Project status and owner](../../README.md): queue authority.
