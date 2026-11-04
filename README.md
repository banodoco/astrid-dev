# Astrid development plans

This private planning repository holds the shared Megado method and focused plans. The ordered table below is the sole source for project status and remaining human engineering-days estimates. Task checkboxes inside plans track task progress only. Finished or explicitly cancelled projects move from this queue to [ARCHIVE.md](ARCHIVE.md); keep their plan file at its stable path.

**Initiative status: paused.** The owner has not started product execution. All worker activity and existing automation remain stopped. Preparing or linking a plan does not start it.

Navigation: [plan index](plans/MASTER.md) · [execution handoff](plans/MANAGER.md) · [focused check-in notes](plans/CHECK-IN.md) · [paused schedules](plans/SCHEDULE.md).

## Active and upcoming projects

The goals below are intended outcomes, not claims of delivery; each plan specifies current scope, exclusions, and proof. Estimates are human focused engineering days remaining, not agent elapsed time. Use a range when evidence supports one and `TBD` otherwise. Estimates inform sequencing and capacity; they are not approval gates.

| Project | Goal | Status | Estimate | Plan |
|---|---|---|---:|---|
| Installer consent | Let users choose what Astrid installs and enables, with clear consent, saved preferences, and predictable behavior. | queued | 0.5–1 day | [Plan 01](plans/01-installer-consent.md) |
| Generation | Provide one consistent end-to-end path for supported generation, with shared defaults and predictable setup, execution, and results. | queued | 1–2 days + native Linux x86_64 verification | [Completion 02](plans/02-generation-completion.md), [merge 03](plans/03-generation-merge.md) |
| Concurrent editing | Keep users in control: agent edits must respect user edits, surface conflicts, and retry safely without silently overwriting changes. | queued | TBD | [Plan 04](plans/04-concurrent-edits.md) |
| Remaining fixes | Bring the accepted fixes together into a coherent release while preserving existing behavior. | queued | TBD | [Plan 05](plans/05-remaining-fixes.md) |
| Packs | Simplify and standardize how packs work, moving pack-specific features out of core while preserving supported workflows. | queued | TBD | [Plan 06](plans/06-packs.md) |
| Pinokio | Provide a tested, reliable Pinokio launcher for installing, starting, updating, stopping, and removing Astrid safely. | queued | TBD | [Plan 07](plans/07-pinokio.md) |

### Status key

- `queued`: planned and waiting for its actual start.
- `active`: product work has been explicitly started and is underway.
- `blocked`: a named dependency, evidence gap, or decision prevents progress.
- `paused`: work was deliberately stopped after starting; record the reason in its plan's run evidence.
- `done`: agreed acceptance evidence exists and the intended integration is recorded.
- `cancelled`: the owner explicitly abandoned the project; preserve the reason in [ARCHIVE.md](ARCHIVE.md).

The status above applies to each project. The initiative-wide pause is separate and keeps every product activity stopped until the owner starts it. Plans 01–06 form the staged pre-main sequence; generation work may be prepared independently after an explicit start, while its final integration consumes the installer increment. Plan 07 starts with reconciliation and is independent of the Packs gate unless that review identifies a real dependency.

## How to use this repo

- Read the vendored [Megado skill](.agents/skills/megado/SKILL.md) and [repo rules](AGENTS.md) before planning or executing.
- Use the [project-plan template](templates/project.md) for new plans. Keep project status and estimate here, not duplicated in individual plans.
- Keep plans, shared references, and proof summaries portable. `.otto/` is ignored local run-control/evidence state.
- Product work targets `pre-main` only when explicitly started and supported by the current plan. Do not infer branch names or source refs; freeze and record actual inputs at execution time.
- Pinokio's historical findings are leads, not current delivery or proof. Reconciliation comes first; it does not resume its blocked product work.
