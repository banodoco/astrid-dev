# Astrid development plans

This repository holds Astrid development workflows and initiative plans. The queue below is the source of project status and remaining engineering-day estimates. Plans track task progress. Move finished or cancelled projects to [ARCHIVE.md](ARCHIVE.md), keeping each plan at its stable path.

**This planned initiative is paused.** Product work and product workers have not started. Existing advisor and orchestrator automations remain paused. Preparing a plan or installing its skills does not start the initiative.

Start with the example that matches your work:

- [Dev (`astrid-dev`)](skills/astrid-dev/SKILL.md): “Which repo owns installer consent?”
- [Plan (`astrid-dev-plan`)](skills/astrid-dev-plan/SKILL.md): “Plan a reusable captions pack, starting with existing solutions.”
- [Iterate (`astrid-dev-iterate`)](skills/astrid-dev-iterate/SKILL.md): “Fix exported captions losing their timing; run focused checks.”
- [Release (`astrid-dev-release`)](skills/astrid-dev-release/SKILL.md): “Integrate the reviewed installer changes onto pre-main.”

For this initiative, see the [plan queue](plans/) and [handoff](plans/MANAGER.md).

## Active and upcoming projects

Each goal describes an intended outcome; its plan defines scope and evidence. Estimates are remaining human engineering days, not agent elapsed time. Use a range when supported by evidence, or `TBD`.

| Project | Goal | Status | Estimate | Plan |
|---|---|---|---:|---|
| Release 1: install and update | Ship R1: new users install and update on Linux, macOS and Windows; R0 users on Linux and macOS upgrade without data loss, proven by the five-row hosted gate. | active | TBD | [Plan 08](plans/08-release1-install-update.md) |
| Install and update confidence | Make installing and updating dependable on all three OSes: one update path, and a real hosted test for every install, update, rollback and removal route. | queued | TBD | [Plan 09](plans/09-install-and-update-confidence.md) |
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

Project status is separate from the initiative pause. Plan 08 (Release 1) is underway under its own merge coordinator, outside this initiative; no other product work has started. Plan 09 follows Plan 08 and is first in the queue. Plans 01–06 define the staged pre-main sequence; Generation may be prepared after an explicit start, and its integration follows Installer Consent. Plan 07 begins by reconciling historical notes with current source. See [plans](plans/) and [shared references](references/) for details.

## How to use this repo

- Read [repository rules](AGENTS.md) and the selected workflow guide before work. Use the [plan template](templates/project.md) for new plans.
- Keep plans and evidence portable; `.otto/` is local run state.
- Product work stays paused until explicitly started. When started, follow the plan and record the actual source and destination; do not assume branches or refs.
- Pinokio historical findings need current-source review before they count as evidence.

## Install the role skills

From the repository root, preview or install the workflow skills and shared guide:

```sh
./sync.sh --dry-run
./sync.sh
```

The destination skill directories must already exist. To target another existing directory, add `--destination /path/to/skills` to either command. The script links only these Astrid files, leaves unrelated files and links untouched, and reports conflicts. Keep this checkout in place while using the links. Installing skills does not start the initiative.
