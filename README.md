# Astrid development workspace

This is where Astrid connects its creative ambition to practical work, alongside development skills and the plan catalog. Our [contribution design principles](docs/contribution-design-principles.md) guide how we keep that work rigorous and simple.

## What we're building

**[A tool to unlock the collective artistic ambition of the open-source community](visions/vision.md).** Four artistic [pillars](visions/vision.md#four-pillars) describe the creative aim; four [guiding principles](visions/principles.md) — local-first/cloud-capable, open by design, creator-controlled and eliminating needless technical wrangling — apply across the whole system.

**[Vision → Gaps → Plans → Evidence](visions/README.md).** The vision defines the destination. [Gaps](visions/README.md)—relevant to one or more pillars and principles—record what's not yet true and what would prove it. The plans below are attempts to close those gaps; their actual evidence informs the next assessment. **Completing a plan does not automatically close a gap.**

The [plan catalog](plans/index.md) owns status, ownership and priority; the list below is generated from it. [How gap reassessment works](visions/gaps.md) · [Dated plan-to-gap assessment](visions/references/plan-gap-assessment-2026-11-06.md).

## Want to contribute? Give this to your agent.

Copy this prompt into your agent:

```text
Help me contribute to Astrid. Begin at
https://github.com/banodoco/astrid-dev and read
skills/astrid-dev/SKILL.md and docs/contribution-workflow.md.
Find existing issues or project tasks before suggesting new work.
Match a useful contribution to my interests, time and tools.
For bugs and small fixes, use an issue and real focused proof,
not a project. For independently useful new scope, investigate
prior art, choose a simple approach, and agree a clear outcome.
Respect source identity, user data and execution permissions.
```

**[How to contribute: claim, propose, submit and complete](docs/contribution-workflow.md).** You can [claim an available project](https://github.com/banodoco/astrid-dev/edit/main/plans/index.md) with a single owner-only PR, [propose a project](https://github.com/banodoco/astrid-dev/issues/new?template=project-proposal.md), or [open an issue](https://github.com/banodoco/astrid-dev/issues/new) for a small fix.

The [contributor entrypoint](skills/astrid-dev/SKILL.md) owns the agent process; the [domain map](skills/astrid-dev/references/domains.md) routes people to the right code and references.

## Highest-priority active and upcoming plans

The ten highest-ranked nonterminal plans from the [full plan catalog](plans/index.md), preserving its existing relative order. The catalog also includes completed and cancelled plans. Neither ranking nor ownership authorizes product work.

<!-- plans:top10:start -->
| Project | Goal | Status | Owner | Estimate | Waiting on | Plan |
|---|---|---|---|---:|---|---|
| Pinokio basic (R1.1) | Prove users can install, start, stop (including while busy), update and remove Astrid through Pinokio on Linux, macOS and Windows, with a separate three-row hosted gate. Shipped on indicative evidence (5 Nov); gaps in the plan. | active | Release 1 merge coordinator | TBD | — | [Plan 07](plans/07-pinokio/plan.md) |
| Zero-to-first-image onboarding | Go from an existing inference setup to a generated image visible on the timeline through one simple command, with tested recovery and minimal agent effort. | queued | Unassigned | TBD | scope agreement | [Plan 20](plans/20-zero-to-first-image/plan.md) |
| Install and update confidence | Make installing and updating dependable on all three OSes: one update path, and a real hosted test for every install, update, rollback and removal route. | queued | Unassigned | TBD | — | [Plan 09](plans/09-install-and-update-confidence/plan.md) |
| Installer consent | Let users choose what Astrid installs and enables, with clear consent, saved preferences, and predictable behavior. | queued | Unassigned | 0.5–1 day | — | [Plan 01](plans/01-installer-consent/plan.md) |
| Consistent generation path | Make supported generation choose consistent defaults and set up a compatible, pinned stack, proven on fixtures and a fresh Linux install; real model inference is not proven here. | queued | Unassigned | 4–5 days after Plan 01 (includes the RunPod dry-run work, the installed-package test and the final rebase), plus a Linux x86_64 environment | Plan 01 (from phase 3); a Linux x86_64 environment for task V2 only | [Generation plan](plans/02-consistent-generation/plan.md) |
| Pinokio qualification | Engine Stop/Quit refusal veto, direct custody and fully-local mode, qualified natively. | queued | Unassigned | TBD | — | [Plan 10](plans/10-pinokio-qualification/plan.md) |
| Refined concurrent editing | Keep users in control: agent edits must respect user edits, surface conflicts, and retry safely without silently overwriting changes. | queued | Unassigned | TBD | — | [Plan 04](plans/04-concurrent-edits/plan.md) |
| Release fixes integration | Bring the accepted fixes together into a coherent release while preserving existing behavior. | queued | Unassigned | TBD | — | [Plan 05](plans/05-remaining-fixes/plan.md) |
| Packs v1.3 | Simplify and standardize how packs work, moving pack-specific features out of core while preserving supported workflows. | queued | Unassigned | TBD | owner's go; a Playwright browser for the App checks | [Plan 06](plans/06-packs/plan.md) |
| Three.js as a pack | Move the existing built-in Three.js functionality into a native pack that remains included by default, with current behavior preserved through conversion. | queued | Unassigned | TBD | scope agreement | [Plan 11](plans/11-threejs-pack/plan.md) |
<!-- plans:top10:end -->

For statuses, delivery context, remaining work and the full history, see the [plan catalog](plans/index.md).

## How to use this repo

Start at the [contributor entrypoint](skills/astrid-dev/SKILL.md). Small fixes and incidents use [issues](https://github.com/banodoco/astrid-dev/issues); independently useful projects use [one catalog](plans/index.md) and the [three-file project format](docs/project-format.md). The [domain map](skills/astrid-dev/references/domains.md) points to product repositories and references.

[Vision and gap outcomes](visions/README.md) inform the work; [repository rules](AGENTS.md) and the [run contract](skills/astrid-dev-shared/run-contract.md) preserve source identity, permissions, focused evidence and review boundaries. Creating a plan does not authorize execution.
