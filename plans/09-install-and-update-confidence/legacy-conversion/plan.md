# Convert a legacy Astrid installation to standalone

**Project:** Legacy-to-standalone conversion

**Goal:** A creator converts their existing legacy Astrid installation to the current standalone release and can edit the same project at the same data-root path with their media, credentials and instructions preserved.

**Status:** paused

**Owner:** Unassigned

**Estimate:** TBD — LC-0/LC-1 establish reuse and admission feasibility; no hours-to-completion claim is supported.

**Waiting on:** Draft review and an authorized implementation start; the live installation remains paused.

**Start:** [Astrid contributor skill](../../../skills/astrid-dev/SKILL.md) and [domain map](../../../skills/astrid-dev/references/domains.md). This is a paused draft extension to [Plan 09](../plan.md), not a separately queued project or authorization to start a run.

**Vision gaps:** [F-001 platform reliability](https://github.com/banodoco/astrid-dev/blob/d7666299d56dc502e06721b8263c6e2f5c594d14/vision/gaps/F-001-platform-reliability.md) (primary), [F-002 safe user control](https://github.com/banodoco/astrid-dev/blob/d7666299d56dc502e06721b8263c6e2f5c594d14/vision/gaps/F-002-safe-user-control.md) (supporting). No `Contributes to closure` claim yet: no gap route has been edited or accepted.

## Outcome and scope

One installer-owned conversion operation turns an admitted legacy workspace into a standalone installation. The latest officially qualified candidate is staged in a clean program directory. The existing data-root pathname, selected realm/project, timelines, media, credentials, agent instruction files and effective supported instruction behavior remain connected. The hosted editor must load and save the actual timeline and switch projects without the preview's blocked-save behavior. Pack-host/chat must function, not merely appear in health.

Include the macOS mixed-provenance legacy case that motivated this work. Historical startup provenance stays explicitly unknown; a separately reviewed recovery policy must establish current custody and recovery without falsely reconstructing that history. A pristine offline fixture is an intermediate acceptance row, not completion of this outcome. Normal updates, source checkouts and authentic R0/Pinokio paths retain their existing guards.

Out of scope: moving data to `-r1`, resetting workspaces, a second migrator/journal/identity system, cleaning unrelated caches or projects, frontend response interception as a fix, all-platform qualification, arbitrary foreign Runtime versions, paid creative jobs, publishing changes to astrid.haus, or live testing before qualification. Preserve prior backups. Do not auto-delete uncertain markers or directories.

## Existing work and decision

The reuse decision and evidence are in [inputs.md](inputs.md). Plan09 already owns transaction consolidation and installer lock handoff. This draft adds only a conversion source adapter plus genuinely missing Runtime custody/recovery behavior. Where Plan09/38 already delivers a needed contract, consume it instead of implementing another copy.

`Backend.stage`, `validate_candidate`, `backup`, `restore`, `upgrade`, `register`, `start`, verification and identity persistence remain the product operations. `Installer`'s existing durable transaction/recovery is factored to accept a conversion policy. Its normal R0/source refusals remain untouched; no made-up `Version` or manager label is supplied to reach it. Recovery uses a staged, pinned old-compatible installation and its compatible bootstrap rather than the unknown running environment.

Alternatives rejected: retry after stop (still refused and may strand work); restore a historical Pinokio marker (fabricated ownership); sibling-root adoption (changes the required path); custom copy/migration engine (duplicates existing machinery); read-only UI compatibility (does not update or restore editing). An offline-only first increment is useful but cannot be advertised as the requested switch tool.

## Sequence and readiness

1. Freeze the real source baseline and reconcile Plan09/38 ownership. Resolve the recovery-admission policy before implementing the handoff; an infeasible incident class stops the feature, not the live service.
2. Build only the missing Runtime custody handoff and the complete, independently pinned recovery installation in parallel. Review that load-bearing boundary once.
3. Factor the existing update transaction and integrate conversion, preserving its original entry guards. Implement journalled rollback/replay and service/selection publication using existing bootstrap and service-manager authority.
4. Run narrow native tests of actual legacy → current → injected failure → recovery, including full services, then the hosted editor journey on a disposable fixture. Test user-shaped lived-in state, not only an empty realm.
5. Review the integrated candidate, publish only through the ordinary authorized release path, then separately apply the official installer to the actual machine and prove its timeline. Merely producing code or a green fixture does not satisfy the original installation goal.

Task dependencies, exact scope and proof are in [tasks.md](tasks.md). Planning runs no checks. A concrete source/review budget is required before dispatch. Do not expand the test matrix or invent more protocol components unless a named failing acceptance case requires them. If a task's failure remains unresolved after the shared run contract's limit, escalate its exact failure instead of spinning on prototypes.

## Interfaces and handoff

Consumes the official candidate manifest and Agent↔Runtime pins, selected realm/profile/discovery, existing installer transaction context, Runtime admission and owner locks, process identity and custody broker, version-owned bootstrap/service declarations and authenticated backup/restore APIs. Every runtime-sensitive claim identifies the exact installed tuple.

Produces a supported installer conversion entry point (proposed spelling `--convert-legacy`, finalized after LC-1; not a command available today), a Runtime-owned custody operation consumed by that adapter, a conversion context in the existing journal, and a tested recovery installation descriptor. The custody handle is owned by the implementation, not a caller-supplied assertion. It binds root/realm, exact process incarnation, manager state, operation and recovery/candidate identities; it cannot be reused after loss or crash without validated recovery.

The transaction must prepare recovery before stop; hold continuous exclusion through stop, backup, migration and candidate/recovery launch; verify the exact spawned owner before relinquishing custody; preserve or restore selection only through existing owners; and record an unresolved failure as `recovery_required`. On macOS retain the existing Backend filesystem-clone snapshot producer, explicitly not an authenticated Runtime backup, and add canonical integrity/inventory validation while quiesced. For conversion only, refactor the existing restore operation to preserve the held realm-directory and owner-lock inodes while restoring verified contents with the existing journal; regular restore behavior remains unchanged. Do not call today's whole-realm rename under a now-stale directory fence. If that bounded extension cannot prove crash recovery, the conversion remains disabled rather than adding a second backup system.

The old pinned Runtime does not natively accept the new handoff. Proposed `Legacy31RecoveryBoundary` is a narrowly version-scoped adapter shipped with the newly qualified conversion feature: it delegates to the verified old pair's bootstrap/service implementation but supplies the brokered inherited-fence launch through an explicit adapter interface, not global monkeypatches or invented health identity. It checks exact old installed bytes and the new helper's own identity, restores truthful old release metadata per child, and performs normal publication through bootstrap. RS1 must prove this exact combination with real services; if the fixed old API cannot support it without a change, that compatibility change must have a truthful distinct identity and be reviewed before integration. Do not claim it is the unchanged historical release or silently widen this into an arbitrary-version launcher.

No general durable process-exit protocol is required by default. Add a narrow receipt extension only if an explicit crash acceptance row cannot be safely handled by the existing broker/recovery machinery. Unknown crash state remains preserved and inspectable, never “repaired” by deleting markers. Product PRs and integration destination are Pending, not implied by this draft.

## Completion

On a qualified macOS legacy fixture representing the incident, the public installer conversion entry—not a direct backend call—moves to the pinned current standalone release while preserving the exact data root and selected realm/project. The official Runtime health reports the candidate; the hosted editor loads the preserved timeline, saves a reversible edit, reloads it and switches projects. A real Agent connection sees retained instructions using a deterministic no-paid-provider test; a representative pack operation succeeds with the preserved tool/configuration binding. Secrets never appear in evidence.

Meaningful negatives: unchanged ordinary source/R0 refusal; conflicting owner or restart manager; occupied unowned program root; changed selection; competing writer/start; tampered recovery files; insufficient space; active noninterruptible task; candidate/service startup failure; and process death at the named durable boundaries. Before stop, refusal changes neither owner nor workspace. After mutation, failure either restores and starts verified compatible services or retains a truthful `recovery_required` state with intact data/backup and no second writer.

Evidence must include a real schema31→current conversion, a full-service rollback, fresh-process recovery after interruption and an actual browser journey against exact pins. No test monkeypatch can supply admission, identity, exit evidence or shutdown success. Test-only fault injection and temporary environment isolation must be disclosed. Hosted CI owns the full relevant integrated suite; focused task checks are not a claim that the whole product passed.

This qualifies only the declared family/platform. Official publication and the user's live application are separately authorized. Final user-goal completion requires the actual original timeline working on the latest standalone release, not only the project specification or fixture proof.
