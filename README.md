# Astrid development workspace

This workspace brings together Astrid development skills and current projects.

## Want to contribute? Give this to your agent.

Copy this prompt into your agent, or browse the current plans below.

```text
Help me choose and complete a contribution to Astrid. Start at
https://github.com/banodoco/astrid-dev: open my existing checkout or clone it, and
update it only while preserving local changes. Read its AGENTS.md and README.md. From
the repository root, preview and sync the skills with ./sync.sh --dry-run and ./sync.sh,
respecting local permissions; the destination must already exist, and use --destination
/path/to/skills if needed. Keep the linked checkout in place.

Inspect the current queue, relevant plans, and selected skill guide. First ask about my
preferred time/token budget (quick fix, a few hours, or a larger project), interests,
experience, available tools, hardware and agent capabilities, what I would personally
find useful in Astrid, and what help I want.

Suggest 2–3 bounded contributions that fit. If I have nothing in mind, recommend one
small, satisfying starting task that fits my budget and capabilities instead. Explain
why it is interesting and how it would help other people. Check active ownership and
dependencies to avoid duplicate work. Before implementation, agree with me on one task,
its starting code, and focused completion checks. Follow the repository’s existing
workflow and current authorization.
```

## Active and upcoming projects

Each goal describes an intended outcome; its plan defines scope and evidence. Owner names the accountable person, team, or coordinating role; it does not imply that work is authorized or active. Use `Unassigned` when no current owner is known. Estimates are remaining human engineering days, not agent elapsed time. Use a range when supported by evidence, or `TBD`.

| Project | Goal | Status | Owner | Estimate | Plan |
|---|---|---|---|---:|---|
| Release 1: install and update | Ship R1: new users install and update on Linux, macOS and Windows; R0 users on Linux and macOS upgrade without data loss, proven by the five-row hosted gate. | active | Release 1 merge coordinator | TBD | [Plan 08](plans/08-release1-install-update.md) |
| Install and update confidence | Make installing and updating dependable on all three OSes: one update path, and a real hosted test for every install, update, rollback and removal route. | queued | Unassigned | TBD | [Plan 09](plans/09-install-and-update-confidence.md) |
| Installer consent | Let users choose what Astrid installs and enables, with clear consent, saved preferences, and predictable behavior. | queued | Unassigned | 0.5–1 day | [Plan 01](plans/01-installer-consent.md) |
| Generation | Provide one consistent end-to-end path for supported generation, with shared defaults and predictable setup, execution, and results. | queued | Unassigned | 1–2 days + native Linux x86_64 verification | [Completion 02](plans/02-generation-completion.md), [merge 03](plans/03-generation-merge.md) |
| Concurrent editing | Keep users in control: agent edits must respect user edits, surface conflicts, and retry safely without silently overwriting changes. | queued | Unassigned | TBD | [Plan 04](plans/04-concurrent-edits.md) |
| Remaining fixes | Bring the accepted fixes together into a coherent release while preserving existing behavior. | queued | Unassigned | TBD | [Plan 05](plans/05-remaining-fixes.md) |
| Packs | Simplify and standardize how packs work, moving pack-specific features out of core while preserving supported workflows. | queued | Unassigned | TBD | [Plan 06](plans/06-packs.md) |
| Pinokio basic (R1.1) | Prove users can install, start, stop (including while busy), update and remove Astrid through Pinokio on Linux, macOS and Windows, with a separate three-row hosted gate. | active | Release 1 merge coordinator | TBD | [Plan 07](plans/07-pinokio.md) |
| Pinokio qualification | Engine Stop/Quit refusal veto, direct custody and fully-local mode, qualified natively. | queued | Unassigned | TBD | [Plan 10](plans/10-pinokio-qualification.md) |
| Three.js as a pack | Move the existing built-in Three.js functionality into a native pack that remains included by default, with current behavior preserved through conversion. | queued | Unassigned | TBD | [Plan 11](plans/11-threejs-pack.md) |
| Multiple inference routes (Wan2GP) | Keep VibeComfy as the primary route and add Wan2GP through the shared generation path, reusing existing setup and connection infrastructure where it fits. | queued | Unassigned | TBD | [Plan 12](plans/12-multiple-inference-routes.md) |

### Status key

- `queued`: planned and waiting for its actual start.
- `active`: product work has been explicitly started and is underway.
- `blocked`: a named dependency, evidence gap, or decision prevents progress.
- `paused`: work was deliberately stopped after starting; record the reason in its plan's run evidence.
- `done`: agreed acceptance evidence exists and the intended integration is recorded.
- `cancelled`: the owner explicitly abandoned the project; preserve the reason in [ARCHIVE.md](ARCHIVE.md).

Project status is recorded in the queue above. Plans 08 (Release 1) and 07 (Pinokio basic) are coordinated by the Release 1 merge coordinator. Plan 09 follows Plan 08 and is next in the queue; Plan 07 runs as Release 1.1 alongside it, and Plan 10 follows Plan 07. Plans 01–06 define the staged pre-main sequence: Generation integration follows Installer Consent, while independent work can proceed when its inputs and authorization are available. Plan 10 begins by reconciling historical Pinokio notes with current source. Plans 11 and 12 are draft scopes awaiting source identity and remaining scoping decisions before execution. See [plans](plans/) and [shared references](references/) for details.

## How to use this repo

- Keep project status and remaining estimates in the queue, and task progress in the plans. Move finished or cancelled projects to [ARCHIVE.md](ARCHIVE.md), keeping their plan links stable.
- Read [repository rules](AGENTS.md) and the selected workflow guide before work. Use the [plan template](templates/project.md) for new plans.
- Keep plans and evidence portable; `.otto/` is local run state.
- Follow the selected project’s plan and current run controls. Record the actual source and destination; do not assume branches or refs.
- Pinokio historical findings need current-source review before they count as evidence.
