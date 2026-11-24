# Heavy saves in seconds

**Project:** Heavy saves in seconds

**Goal:** On a heavy timeline (the 300-clip fixture), an ordinary edit reaches "Saved" in about 2 s at the median with none over 4 s (the Release 15 target is the fastest the loop cards reach, about 3 to 3.5 s, with the 2 s gate in Release 16 with Plan 75; see the target section below), from the editor and from Agent commits alike, and the save path is measured stage by stage so a regression shows in a log line.

**Status:** active

**Owner:** Orchestrator session `session_011EzfW2o5WfJcvHwr8fSDzC` (Plan 77's save run), hosting a Codex manager

**Estimate:** About 4 engineering days (SV-L1 to SV-L5), plus whatever the measure-and-fix loop funds

**Waiting on:** Plan 77 save run card SV-4 (the copy and compare removal) landing on `release/15/plan-77-save`

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-001 — Reliability isn't proven across supported setups](../../vision/gaps/F-001-platform-reliability.md) (primary): a save that takes tens of seconds is where a person stops trusting the editor.

## Outcome and scope

The save path is made measurable and the largest measured costs are removed until the gate holds: permanent stage spans and sizes on every commit's timing line, timing marks from the editor, counters proving copy and compare work does not grow with history, a real burst-of-edits test with an independent check of what was stored, and accepted history that the database refuses to change. Then a loop: measure the installed build, stop at the gate, otherwise fund the largest measured residual as a new card.

It continues [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md)'s save run (which removed the pack host's false refusals and the history re-verification) in the same session, on branches `release/15/plan-89` cut from the save run's `release/15/plan-77-save` heads. It does **not** do [Plan 75](../75-fast-saving/plan.md)'s structural work (validate only what the effects touch, the Runtime applying the effect list): that is the 300 ms target and a later release.

## Existing work and decision

Measured on 23 November 2026 (evidence under [Plan 77](../77-saving-holds-on-a-heavy-timeline/evidence/)): 57.5 s first save on the first cut; 24.8 s first and about 22 s later saves after the save run's fence and copy fixes; on the candidate with the pack-host write fix, 72 to 76% of a warm commit is Python copy and compare (`value_equal`, `deepcopy`), which Plan 77's SV-4 removes. The cards here are the cheap, independent parts of Plan 75 that an independent Astra critique (recorded in [Plan 75's inputs](../75-fast-saving/inputs.md)) recommended doing now: FS-0, FS-1, a narrow CC-1 and CC-11, plus the burst test. It advised deferring FS-5, FS-2 and FS-3a, which are not standalone. The owner chose on 23 November 2026 to do this now, as its own plan, separate from Plan 75.

## Sequence and readiness

After Plan 77's SV-4 lands on the save branch: SV-L1 and SV-L2 first (every later number is a log read), then SV-L3 and SV-L4, then the first loop measurement; SV-L5 in parallel. Cards and proofs: [tasks.md](tasks.md). Measurement runs use the 300-clip fixture on the first-cut lane's box (`session_011EzfW1FXS3o7GFnNSB7cZS`) or a rebuilt copy.

## Interfaces and handoff

Consumes astrid-runtime, astrid-agent and astrid-app `release/15/main` plus the save run's `release/15/plan-77-save` heads, from which `release/15/plan-89` is cut. Produces: stage spans and size fields on the commit timing line, editor timing marks, a copy and compare counter test at 3, 30 and 300 history entries, a burst test, immutable accepted history, and installed measurements in [docs/speed.md](../../docs/speed.md). Landing follows the Release 15 run board: Runtime, then one generator-only Agent pin commit and the full hosted run, then the App pin.

## Release 15 target and stop rule (restated 24 November 2026)

The installed measurement of the save-run candidate (Plan 77 SV-4, evidence in [Plan 77's SV-3 and SV-4 runs](https://github.com/banodoco/astrid-dev/pull/1685); SV-L2 marks, folder `evidence/2026-11-24-sv-l2-run`) put a warm 300-clip save at a **6.15 s median, 6.85 s worst, gesture end to "Saved"**: client side about 1.5 s (1.08 s before the POST, which includes the 500 ms save debounce; 0.44 s from the response to the Saved badge) and Runtime about 4.6 s (`provider_commit` 2.33 s, `port_store_accept` 1.54 s, reconciliation 0.40 s, handler 0.28 s). It was about 22 s the day before. Removing the remaining repeated work (validating and copying the unchanged clips, the Agent payload) can plausibly reach about 3 to 3.5 s; reaching 2 s needs one-edit acceptance that is O(change), which is [Plan 75](../75-fast-saving/plan.md)'s structural work.

- **Release 15 target:** land SV-L10, SV-L11 and SV-L12 (and SV-L13 if it earns its place), ordered by measured saving per day, and report the measured warm median, gesture end to "Saved", as the release's number (about 3 to 3.5 s expected).
- **Stop rule:** stop when the next card's projected saving is under about 0.3 s, or when the freeze arrives.
- **Moves to Release 16 with Plan 75:** the 2 s median gate (O(change) one-edit acceptance), the watermark SV-L9b and full burst coalescing (SV-L7).
- **Unchanged:** the 500 ms debounce stays; it keeps bursts from multiplying commits.

## Completion

The four Plan 77 scenarios plus the bursts (5 edits in 3 s, 10 in 5 s) on the installed 300-clip fixture with the pack host running: median at most 2 s to "Saved", none over 4 s, refusals only on real clashes, the stored document and receipts equal to the expected edits; one Agent authoring commit measured end to end. If the loop cannot reach the gate, the plan ends with the measured residual handed to Plan 75. Limits: one fixture, one machine class; it does not prove the 616-clip target or 300 ms.
