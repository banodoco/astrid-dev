# Astrid development workspace

This workspace brings together Astrid development skills and current projects.

## Want to contribute? Give this to your agent.

Copy this prompt into your agent or browse the current plans below.

```text
Help me choose and complete a contribution to Astrid. Start at
https://github.com/banodoco/astrid-dev: open my existing checkout or clone it, and
update it only while preserving local changes. Read its AGENTS.md and README.md. From
the repository root, preview and sync the skills with ./sync.sh --dry-run and ./sync.sh,
respecting local permissions; the destination must already exist, and use --destination
/path/to/skills if needed. Keep the linked checkout in place.

Inspect the current queue, relevant plans, and selected skill guide. First ask me
whether I already have something in mind that I’d like to contribute. Then ask about
my preferred time/token budget (quick fix, a few hours, or a larger project),
interests, experience, available tools, hardware and agent capabilities, what I would
personally find useful in Astrid, and what help I want.

If I have something in mind, help me shape it into one bounded contribution and check
it against the queue and plans. If not, recommend 2–3 bounded contributions that fit
my budget and capabilities, including one small, satisfying starting task. Explain why
each is interesting and how it would help other people. Check active ownership and
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

## Active and upcoming projects

Each goal describes an intended outcome; its plan defines scope and evidence. Owner names the accountable person, team, or coordinating role; it does not imply that work is authorized or active. Use `Unassigned` when no current owner is known. Estimates are remaining human engineering days, not agent elapsed time. Use a range when supported by evidence, or `TBD`.

| Project | Goal | Status | Owner | Estimate | Plan |
|---|---|---|---|---:|---|
| Release 1: install and update | Ship R1: new users install and update on Linux, macOS and Windows; R0 users on Linux and macOS upgrade without data loss, proven by the five-row hosted gate. | active | Release 1 merge coordinator | TBD | [Plan 08](plans/08-release1-install-update.md) |
| Pinokio basic (R1.1) | Prove users can install, start, stop (including while busy), update and remove Astrid through Pinokio on Linux, macOS and Windows, with a separate three-row hosted gate. | active | Release 1 merge coordinator | TBD | [Plan 07](plans/07-pinokio.md) |
| Zero-to-first-image onboarding | Go from an existing inference setup to a generated image visible on the timeline through one simple command, with tested recovery and minimal agent effort. | queued | Unassigned | TBD | [Plan 20](plans/20-zero-to-first-image.md) |
| Install and update confidence | Make installing and updating dependable on all three OSes: one update path, and a real hosted test for every install, update, rollback and removal route. | queued | Unassigned | TBD | [Plan 09](plans/09-install-and-update-confidence.md) |
| Installer consent | Let users choose what Astrid installs and enables, with clear consent, saved preferences, and predictable behavior. | queued | Unassigned | 0.5–1 day | [Plan 01](plans/01-installer-consent.md) |
| Consistent generation path | Provide one consistent end-to-end path for supported generation, with shared defaults and predictable setup, execution, and results. | queued | Unassigned | 1–2 days + native Linux x86_64 verification | [Generation plan](plans/02-consistent-generation/plan.md) |
| Pinokio qualification | Engine Stop/Quit refusal veto, direct custody and fully-local mode, qualified natively. | queued | Unassigned | TBD | [Plan 10](plans/10-pinokio-qualification.md) |
| Refined concurrent editing | Keep users in control: agent edits must respect user edits, surface conflicts, and retry safely without silently overwriting changes. | queued | Unassigned | TBD | [Plan 04](plans/04-concurrent-edits.md) |
| Release fixes integration | Bring the accepted fixes together into a coherent release while preserving existing behavior. | queued | Unassigned | TBD | [Plan 05](plans/05-remaining-fixes.md) |
| Packs v1.3 | Simplify and standardize how packs work, moving pack-specific features out of core while preserving supported workflows. | queued | Unassigned | TBD | [Plan 06](plans/06-packs.md) |
| Three.js as a pack | Move the existing built-in Three.js functionality into a native pack that remains included by default, with current behavior preserved through conversion. | queued | Unassigned | TBD | [Plan 11](plans/11-threejs-pack.md) |
| Multiple inference routes (Wan2GP) | Keep VibeComfy as the primary route and add Wan2GP through the shared generation path, with shared setup, task/resource ownership, model lifecycle, and cleanup. | queued | Unassigned | TBD | [Plan 12](plans/12-multiple-inference-routes.md) |
| Execution host refactor | Split the oversized execution host into clear, maintainable modules while preserving supported execution behavior. | queued | Unassigned | TBD | [Plan 13](plans/13-execution-host-refactor.md) |
| Repository cleanup | Make the repositories easy to navigate and maintain by removing proven clutter and consolidating code, docs, and tooling. | queued | Unassigned | TBD | [Plan 14](plans/14-repository-cleanup.md) |
| Sandboxed execution with OpenShell | Let users onboard into an isolated full Astrid stack, including the app/frontend and backend, with explicit permissions and tested boundaries. | queued | Unassigned | TBD | [Plan 15](plans/15-openshell-safe-execution.md) |
| Streamlined agent setup and execution | Simplify account connection and execution, and let contributors add an agent in one place while preserving alternative agents and pack runs. | queued | Unassigned | TBD | [Plan 16](plans/16-streamlined-agent-experience.md) |
| VibeComfy extensibility with H3_AV | Make it easy to build and share higher-level tools on VibeComfy workflows, using H3_AV to prove reusable extension primitives. | queued | Unassigned | TBD | [Plan 17](plans/17-vibecomfy-extensibility.md) |
| Extensible timeline editing | Provide reliable timeline editing primitives as a pack that people and agents can extend with their own views, tools, and creative workflows. | queued | Unassigned | TBD | [Plan 18](plans/18-timeline-editing.md) |
| First-principles documentation | Make Astrid understandable to humans and agents through a clear path from its purpose and central skill to workflows, pack design, and precise references. | queued | Unassigned | TBD | [Plan 19](plans/19-first-principles-documentation.md) |
| Astrid website | Build the scroll journey below the Astrid homepage hero: three sections and a vision finale that re-explain the hero's notes, with the sky following the visitor's time of day. The rest of the website is not yet scoped. | queued | Unassigned | TBD | [Plan 21](plans/21-astrid-website/README.md) |

### Status key

- `queued`: planned and waiting for its actual start.
- `active`: product work has been explicitly started and is underway.
- `blocked`: a named dependency, evidence gap, or decision prevents progress.
- `paused`: work was deliberately stopped after starting; record the reason in its plan's run evidence.
- `done`: agreed acceptance evidence exists and the intended integration is recorded.
- `cancelled`: the owner explicitly abandoned the project; preserve the reason in [ARCHIVE.md](ARCHIVE.md).

Project status is recorded in the queue above. Plans 08 (Release 1) and 07 (Pinokio basic) are coordinated by the Release 1 merge coordinator. Plan 09 follows Plan 08; Plan 07 runs as Release 1.1 alongside it, and Plan 10 follows Plan 07. Plans 01–06 define the staged pre-main sequence: Generation integration follows Installer Consent, while independent work can proceed when its inputs and authorization are available. Plan 10 begins by reconciling historical Pinokio notes with current source. Zero-to-first-image onboarding (Plan 20) is a top-priority upcoming project. Plans 11–20 are draft scopes awaiting source identity and remaining scoping decisions before execution. Plan 21 is a complete hand-off for the homepage journey; nothing is built yet. See [plans](plans/) and [shared references](references/) for details.

## How to use this repo

- See the [extensibility philosophy](docs/extensibility-philosophy.md) for the design direction.
- Keep project status and remaining estimates in the queue, and task progress in the plans. Move finished or cancelled projects to [ARCHIVE.md](ARCHIVE.md), keeping their plan links stable.
- Read [repository rules](AGENTS.md) and the selected workflow guide before work. Use the [plan template](templates/project.md) for new plans.
- Keep plans and evidence portable; `.otto/` is local run state.
- Follow the selected project’s plan and current run controls. Record the actual source and destination; do not assume branches or refs.
- Pinokio historical findings need current-source review before they count as evidence.
