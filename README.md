# Astrid development workspace

This is where Astrid connects its creative ambition to practical work, alongside development skills and the plan catalog.

## What we're building

**[Make Extraordinary Art Possible, Together](visions/vision.md).** Four artistic [pillars](visions/vision.md#four-pillars) describe the creative aim; three [operating principles](visions/principles.md) — local-first/cloud-capable, open by design and creator-controlled — apply across the whole system.

**[Vision → Gaps → Plans → Evidence](visions/README.md).** The vision defines the destination. [Gaps](visions/README.md)—relevant to one or more pillars and principles—record what's not yet true and what would prove it. The plans below are attempts to close those gaps; their actual evidence informs the next assessment. **Completing a plan does not automatically close a gap.**

The [plan catalog](plans/index.md) owns status, ownership and priority; the list below is generated from it. [How gap reassessment works](visions/gaps.md) · [Dated plan-to-gap assessment](visions/references/plan-gap-assessment-2026-11-06.md).

## Want to contribute? Give this to your agent.

Copy this prompt into your agent or browse the current plans below.

```text
Help me choose and complete a contribution to Astrid. Start at
https://github.com/banodoco/astrid-dev: open my existing checkout or clone it, and
update it only while preserving local changes. Read its AGENTS.md and README.md. From
the repository root, preview and sync the skills (./sync.sh --dry-run, then ./sync.sh),
which links them into my existing ~/.claude/skills, ~/.codex/skills or ~/.agents/skills,
respecting local permissions; the destination must already exist, and use --destination
/path/to/skills if needed. Keep the linked checkout in place.

Inspect the [plan catalog](plans/index.md) and selected skill guide. Start each project at its folder’s
plan.md, then read tasks.md for the work and inputs.md for the source material. First ask me
whether I already have something in mind that I’d like to contribute. Then ask about
my preferred time/token budget (quick fix, a few hours, or a larger project),
interests, experience, available tools, hardware and agent capabilities, what I would
personally find useful in Astrid, and what help I want.

If I have something in mind, help me shape it into one bounded contribution and check
it against the queue and plans. If not, recommend 2–3 bounded contributions that fit
my budget and capabilities, including one small, satisfying starting task. Explain why
each is interesting and how it would help other people. Check current ownership and
dependencies to avoid duplicate work. Before implementation, agree with me on one task,
its starting code, and focused completion checks. Follow the repository’s existing
workflow and current authorization.

Plans tag every task with a route, and building uses the same routes: N (everything
below very hard, including ordinary hard work) goes to Haiku or Luna, X (very hard) to
Sonnet or Terra, and S (super hard) to Opus or Sol. When we build, coordinate rather
than doing everything yourself: keep the judgment, hand each task to a subagent on its
route’s model, run independent tasks in parallel, and check what comes back. If you
can’t start subagents, tell me and do the work yourself.
```

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

- See the [extensibility philosophy](docs/extensibility-philosophy.md) for the design direction.
- Start with [Astrid's vision](visions/vision.md), its [four pillars and operating principles](visions/README.md), and the [gap/plan evidence contract](visions/gaps.md); implementation authority remains in the project plans.
- Keep all status, priority and estimates in the [plan catalog](plans/index.md), and task progress in the plan folders. Completed and cancelled entries remain in that same catalog.
- Look up unfamiliar terms in the [glossary](docs/glossary.md).
- Read [repository rules](AGENTS.md) and the selected workflow guide before work. Use the [project folder template](templates/project/plan.md) for new projects.
- Keep plans and evidence portable; `.otto/` is local run state.
- Follow the selected project’s plan and current run controls. Record the actual source and destination; do not assume branches or refs.
- Pinokio historical findings need current-source review before they count as evidence.
- To start a project, get the go from its owner in the catalog. If the owner is `Unassigned`, open an issue in [banodoco/astrid-dev](https://github.com/banodoco/astrid-dev/issues) naming the plan and the tasks you want to take.

## Project format

Every project is a folder, including an early draft. New plans link to relevant gap IDs (or explain why they are foundational enablers) in `plan.md`:

```text
plans/<id-name>/
  plan.md     # What, why, scope, what exists, sequence, and completion
  tasks.md    # Task index → detailed instructions, routes, checks, and progress
  inputs.md   # Source materials, starting identities, references, and evidence limits
```

Start at `plan.md`; every catalog row links there. Short tasks stay in `tasks.md`. Add supporting files only when they have a distinct job. See [how project folders grow](docs/project-format.md) for the website example, other project types, and how to handle a larger catalog.

Copy [the template folder](templates/project) for a new project. Drafts use the same three files and can be brief. The catalog owns project status, owner, priority and estimate; the task index or linked card owns task progress. Mark finished work `done` in the catalog, keeping its folder and history in place.
