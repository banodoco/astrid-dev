# Speed: what we know, how we measure, what is next

A living summary of Astrid's speed work, so findings outlive the sessions that made them. Each section links to the evidence it rests on; the evidence is the record, this page is the map. Update it when a measurement changes the picture. [Plan 85](../plans/85-one-place-to-measure/plan.md) will give measurement one shared home; until then, this page is it.

## How we measure

- **Profile the real installed path before building a speed fix.** A stand-in measurement (bytes hashed in a development setup, a unit benchmark) can point at the wrong cost: Plan 81's first Part 2 cut hashing by two thirds in development and saved nothing installed, because the installed command took a path the memo switched itself off on.
- **Account for the whole time.** A stage table (`astrid generate --timings`) or a sampling profiler (`py-spy`, 100 Hz, idle frames included) on the installed build; report seconds by function group covering at least 95% of the wall time, and say what is unattributed.
- **Compare arms on the same machine, same instrumentation, alternating samples,** five after a warm-up, medians. Absolute times differ between machines; the saving is what counts.
- **Prove speed and behaviour before hosted CI.** A full Agent CI run takes about three hours; it is the final check on something already shown to work.

## Generate (`astrid generate`, installed, to "task queued", stand-in ComfyUI)

| Build | Median | Evidence |
| --- | ---: | --- |
| Before Release 15 work | 14.7 to 16.6 s | [installed baseline](../plans/81-once-per-command/evidence/installed-container-baseline/) |
| Plan 81 Part 1 (landed) | 10.8 to 12.3 s | [Part 2 three-arm run](../plans/81-once-per-command/evidence/installed-container-baseline/runs/2026-11-23-part2-lead-machine/README.md) |
| Plan 81 Part 2b (VibeComfy `c0e910ca`) | 5.8 s (11.84 s on the same box without it) | Part 2b fixed-head receipts, astrid-dev #1679; landed on Agent `release/15/main` as `045064b6` (#564) |
| Pack discovery once per command (PB-7b, **parked, not landed**) | 5.06 s (6.23 s on the same box without it; 1.17 s saved) | [hand-off](../plans/81-once-per-command/evidence/2026-11-23-pb7b-handoff/README.md), astrid-agent #557 (draft) |

- **Where Part 2b's 6 s came from:** about 5 s of workflow emission was SHA-256 re-witnessing of the shipped offline node list (63 files, 13.7 MB) on every class lookup: about 7,550 witnesses and 5.4 GB per command. Part 2b checks each file once per call and the whole set once before publishing ([emission profile](../plans/81-once-per-command/evidence/2026-11-23-installed-emission-profile/README.md)). ComfyUI's own checks cost about 0.004 s.
- **What is left in about 6 s:** pack discovery about 2.2 s (16 scans per command under four callers: model registry, candidate qualification, capability registries, unparented), workflow build 0.7 s, emission 0.5 s, other command work 0.5 s, pack host attachment 0.4 s, approval compile 0.4 s, launcher connection 0.2 s, interpreter start 0.1 s.
- **Next:** pack discovery once per command was tried on Linux for unmanaged packs (Plan 81 PB-7b): 1.17 s saved after restoring the refusal order the first version had changed, below the 1.3 s line, so it is parked and handed to Plan 87 (RN-4: one place for pack roots) rather than landed. Below about 3 s needs reuse across commands ([Plan 82](../plans/82-reuse-across-commands/plan.md)).

## Saving a heavy timeline (300 clips, installed, release to "Saved")

| Build | First save | Later saves | Evidence |
| --- | ---: | ---: | --- |
| First cut (Runtime `737843e9`) | 57.5 s | 19.7 s | [two-save profile](../plans/77-saving-holds-on-a-heavy-timeline/evidence/2026-11-23-save-profile/) |
| Save run `f2da02e1` (copying removed, poll fix) | 24.8 s | about 22 s | SV-3 run 4, astrid-dev #1685 |

Every save goes through the same Runtime route (`POST /v1/projects/{p}/timelines/{t}/commit`, `commit_timeline`, `accept`), from the App editor and from Agent, CLI and SDK commits alike, so a Runtime fix speeds all of them. Agent commits also compile and validate locally first.

- **Where the time went (profile, Runtime request thread):** re-verifying already-accepted history 38.1 s on the first save, 3.6 s when the verified result was reused; validating this edit 6.0 and 3.9 s; Python record copying and comparison about 10 s on every save.
- **Why verified history was thrown away:** the verification fence refused or discarded on any movement of SQLite `total_changes`, `data_version` or the WAL. The pack host's idle claim poll (about once a second) writes to a temporary table and its executor re-registers about every 31 s, so long replays could never finish clean. On the first cut this also refused **opening** a timeline of more than a few dozen clips while the pack host ran (found by Plan 78's live proof).
- **Done on the save branch:** record copying removed (Runtime #104), the temporary-table writes no longer count (#105), commit stage timings reach the log (#103). Ready: the executor re-registration skips when nothing changed (#106).
- **Next:** profile a warm save with #106 to see whether the verified result now survives between saves and where the remaining seconds go; then the validation step.
- **Longer term:** a commit that costs the change, not the history: [Plan 89](../plans/89-heavy-saves-in-seconds/plan.md) now (measure and remove the largest costs to about 2 s), then [Plan 75](../plans/75-fast-saving/plan.md) (one acceptor per timeline, 300 ms target) and history stored as summaries (#1561).

**Several edits in a row:** not yet measured. The editor saves locally first and sends one commit at a time, so edits made while a commit is in flight should be gathered into the next one rather than each paying a full commit; that is the design, not a measurement. An earlier report that overlapped drags coalesced into one commit was wrong (the drag tool accepted one drag at a time). The save run times bursts (5 edits in 3 s, 10 in 5 s: last edit to "Saved", commit count, document as expected) in its next run.

## Opening a heavy timeline

Plan 77's first cut: reopen 4.1 to 4.5 s on 300 clips (4.8 s after a save), from minutes before; the page is ready 5 to 6 s after a cold start with the save run's fixes ([first-cut requalification](../plans/77-saving-holds-on-a-heavy-timeline/evidence/2026-11-22-release-15/first-cut-installed-requalification/RESULT.md)).
