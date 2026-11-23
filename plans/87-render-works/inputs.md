# Inputs — The renderer works end to end

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — included in Release 15 by the owner on 23 November 2026, recorded in the [Release 15 brief](../../releases/15.md). Reshaped the same day at the owner's direction: this plan gets the renderer working end to end with the fixes in the proper code; [Plan 88](../88-timeline-edits-land/plan.md) lands the timeline fixes; everything else is an issue. Filing authority only; no run has started.

**Prior art:** Plans 27, 39, 59, 69, 76, 77, 78 and 83 were read for overlap ([landscape](./evidence/eff/landscape.md)). No plan owns "render works"; Plan 27 keeps export choices, Plan 78 holds the open motion pack pin, Plan 83 the custody module split. The first full draft by an independent judge is kept as [evidence](./evidence/shipplan/PLAN.md).

**Approach:** Port the six sound render changes onto a Release 15 plan branch, carry two tracked experiments, write the remaining fixes properly with a short real render after each, prove it on the heavy fixture and the film, and keep one real render check in CI.

**Challenge:** Reviewed — an independent [code review](./evidence/review/ASTRA-530.md), a [trial integration](./evidence/mergescope/REPORT.md), a [root-cause investigation](./evidence/astra20/REPORT.md) and an independent [judge](./evidence/shipplan/VERDICTS.md) preceded this reshaping. A [second opinion](./evidence/astra-plans/OPINION.md) on the reshaped plan changed sixteen things and was declined on two ([record](#second-opinion)).

**Proof and limits:** A film rendered with the sixteen changes, in four ranges, on a stack cut from an older commit. Nothing has rendered on `release/15/main`. The cause of heartbeat renewals stopping is unknown. Fact checks of the release heads, CI and the branch inventory are in [evidence/eff](./evidence/eff/).

**Review rounds:** One round at the end.

**Run start:** Started 23 November 2026, all cards RN-0 to RN-12, in Release 15 (owner, 23 November 2026: "include both of them into Release 15", aggressively, in parallel with current work). **Accountable agent:** the hosting orchestrator, `session_011EzfW1FXS3o7GFnNSB7cZS` (the Plan 77 first-cut session, relaunched with cleared context once its first cut is closed), hosting one manager on route X; workers by card route (N Luna or Haiku, X Terra or Sonnet, S Sol or Opus), reviews by Astra or Opus. It holds the heavy fixtures and a render stack. It may, without asking: run Codex with full access in its session (or Claude subagents while that account's Codex limit lasts); cut and push `release/15/plan-87` in astrid-agent, astrid-runtime and astrid-app from `release/15/main`; cherry-pick the six render commits named in tasks.md; open PRs; merge them once the Release 15 Lead confirms the gate; dispatch hosted CI when the Lead gives the slot. It needs the owner's go for publishing, anything paid, rented machines, live installs on her machine or her own media (the real film render uses only material already in the evidence). **Coordination:** RN-3 and RN-4 (pack roots from one place) touch the same pack-discovery code as Plan 81's PB-7b; land PB-7b first or agree the order with `session_011EzfW2thrCzq1Cjp4k35mu` directly. Proof and measurement before hosted CI. **Advisor:** the Release 15 Lead, `session_011EzfW1gtAhRQwk8pgJMzhG`. Check-ins hourly.

## Owner decisions

The plan was reshaped on 23 November 2026 at the owner's direction: one plan that gets the renderer working end to end, a second plan for the timeline fixes ([Plan 88](../88-timeline-edits-land/plan.md)), and issues for everything else. The earlier decisions D1 to D7 are closed out below. P1 was decided by the owner; P2 and P3 by the coordinating session, which the owner asked to decide them. This is plan and issue set-up only: no run has started.

| Decision | Options and recommendation | State |
| --- | --- | --- |
| P1 The heavy test timeline | Decided by the owner, 23 November 2026: the generated heavy fixture built by the App's [`scripts/save-loop/build-fixture.mjs`](https://github.com/banodoco/astrid-app/blob/release/15/plan-77/scripts/save-loop/build-fixture.mjs) ([how to run it](https://github.com/banodoco/astrid-app/blob/release/15/plan-77/scripts/save-loop/README.md)). It generates its own media and needs no owner media or GPU. Standard variant: 616 parent clips, 46 shot occurrences, a 2.6 MB document. `large-shots` variant: three 480-second shots of 32 child clips each on 90-second generated sources. It asks for 25 GiB free. The links point at `release/15/plan-77`, where the builder was at filing; it may be on `release/15/main` or `main` by the time the plan runs, and the landed copy is the one to use. | Decided |
| P2 One motion pack revision | Decided by the coordinating session at the owner's delegation: the collection install is pinned to the revision the App vendors (upstream `ec0a9f5`, text defaults to ink), and a render reports a pack revision that differs from the editor's. Rejected: vendoring the pack into the Agent as well (a third copy); leaving it (render and preview disagree, [#1469](https://github.com/banodoco/astrid-dev/issues/1469)). The same pin is open in [Plan 78](../78-live-custom-element-editing/plan.md); tell its manager. | Decided |
| P3 The lease stopgap during the loop | Decided by the coordinating session at the owner's delegation: the two-hour lease stays on the plan branch until RN-8 replaces it, and the branch cannot be offered for merge while it is there. Rejected: holding every long render until the heartbeat cause is found, because that investigation has no known end. | Decided |

**How D1 to D7 were closed**

| Earlier decision | Outcome |
| --- | --- |
| D1 Target branch | Closed by fact: Release 14 was published on 22 November 2026 and takes changes only through its Lead ([landscape](evidence/eff/landscape.md)). Everything here targets `release/15/main`. |
| D2 Word-anchored retime | Moved to [Plan 88](../88-timeline-edits-land/plan.md), which carries the recommendation unchanged. |
| D3 Lease | Kept as "measure, then fix" (RN-7, RN-8); the interim question is P3. |
| D4 Launch-context check | Taken as recommended: keep the check, build the environment once, show path differences (RN-3). |
| D5 Pack roots | Taken as recommended: the generated registry owns the list (RN-4). Revision parity became P2. |
| D6 Outbox interim | Out of this plan. Belongs to [Plan 76](../76-editing-together/plan.md); evidence is on [#1402](https://github.com/banodoco/astrid-dev/issues/1402). |
| D7 Process | Two plans (87, 88) in Release 15. Whether the render check becomes a required check stays with the Release 15 Lead. |

## Judgement calls

Made by the coordinating session when reshaping the plan; each can be overruled.

1. **Port what is sound, write the rest properly, render at every step.** The draft built each proper fix separately before any render ran on Release 15, across two release lines. We port the six sound changes, carry two experiments, write the other fixes directly, and run a short real render after each. Reason: a real render is a better test than a hand-built one, and it is how the defects were found. (An earlier version ported all sixteen commits first; see the second opinion below.)
2. **Release 15 only.** Reason: Release 14 is published; every defect site is present on the Release 15 head; a second line doubled the conflict work.
3. **No new journey.** The draft specified a new render journey with its own fixture. An integration test that executes `rendering.render` against a real Runtime and pack host already exists, as does a full motion pack fixture and a lane that installs Remotion and a browser ([CI facts](evidence/eff/ci.md)). We extend that. Reason: about a day instead of several.
4. **Custody and lease stay in; recovery goes out.** A heavy render cannot finish while either can kill it, so RN-8 and RN-9 are render-path work. What happens after a failure (poisoned slot, stuck tasks, scratch, cancel wording) does not stop a render from working; restarting the stack is an acceptable workaround during the plan. It is [#1514](https://github.com/banodoco/astrid-dev/issues/1514).
5. **Resumable renders are an issue, not a task.** The draft added checkpointed renders after the film had to be rendered in ranges. With RN-8 and RN-9 a whole render should finish; resuming is an improvement, not a precondition. [#1515](https://github.com/banodoco/astrid-dev/issues/1515).
6. **The three timeline commits are not on this branch.** Plan 88 cherry-picks them itself. Reason: one of them is the unsound exemption, and this plan must not land it by carrying it along.
7. **Two experiments may sit on the plan branch, never on the release branch.** The lease and custody stopgaps are each a tracked row; the branch cannot be offered for merge while one remains.
8. **Write-path fixes left to their owners.** Plans 77 (active), 76 and 69 (active) already own saving, agents editing together and unbound shot clips. This plan sends evidence and fixes none of it.

## Second opinion

An independent senior review of both plans, with helpers checking facts in the code, on 23 November 2026: [opinion](evidence/astra-plans/OPINION.md). The coordinating session decided each point.

**Taken**

| Point | What changed |
| --- | --- |
| Sixteen cherry-picks would not reproduce the session's stack, and a render that depends on an override or a suppressed error is a poor reference | RN-1 ports six sound changes and two tracked experiments; RN-4 to RN-6 are written directly; frames are compared with the editor, never with an earlier render |
| Whole renders after every replacement are wasteful | A short contract render after each task; the film whole at three milestones |
| Carrying the timeline commits would land the unsound exemption through this plan | They are not on this branch; Plan 88 lands them |
| Record the exact versions; check the installed profile early, not only at the end | RN-0 stands up both stacks and records the tuple |
| RN-3 must keep selected-pack isolation and explicit values | Written into RN-3 |
| A bundler-only pack-root fix leaves worker discovery, the project compiler's alias and cache identity behind | RN-4 covers every consumer |
| A render should report the pack revision it actually resolved | Written into RN-5 |
| The fade failure is a missing declaration in the element's descriptor, not metadata lost by the generator | RN-6 rewritten; our earlier claim was wrong |
| Measure the host's lease pump, not only the Runtime | Written into RN-7 |
| Ten minutes does not qualify a lease fix | RN-8's proof covers thirty minutes, set-up through upload, worker death and stale fences |
| That the uncaptured process was exiting is unproved; nothing alive may be treated as gone | RN-9 rewritten as a bounded retry that keeps every custody check |
| A heavy render will meet whole-file reads, the one-hour deadline and output ingestion | RN-10 measures memory, wall time, disk and ingestion on every run |
| "Restart" is not a procedure | RN-0 writes and proves a reset procedure |
| Proving the plan branch is not proving the release head | RN-12 |
| The estimates are optimistic | Marked provisional, with two points at which to re-estimate |
| Superseded Release 14 routing was still in this file | Removed from the source identities |

**Not taken**

| Point | Why |
| --- | --- |
| Bring owner-fenced clean-up code back into this plan so the loop does not depend on restarts | The owner asked for cancel and recovery to be an issue ([#1514](https://github.com/banodoco/astrid-dev/issues/1514)). We took the procedure and left the code out, with a stated condition for bringing the smallest piece back |
| Treat nine and six days as unreliable until more is known | We kept the numbers, as the owner needs a size, and marked them provisional |

## Moved to issues

Everything found on 22 November that is not in this plan or Plan 88. New issues were filed only where none covered the defect; otherwise our evidence was added to the existing one. The full index is [evidence/tooling/ISSUES.md](evidence/tooling/ISSUES.md).

| Area | Issues |
| --- | --- |
| Cancel and recovery after a failed task | [#1514](https://github.com/banodoco/astrid-dev/issues/1514) (umbrella), [#1474](https://github.com/banodoco/astrid-dev/issues/1474), [#1475](https://github.com/banodoco/astrid-dev/issues/1475), [#1502](https://github.com/banodoco/astrid-dev/issues/1502), [#1246](https://github.com/banodoco/astrid-dev/issues/1246), [#1320](https://github.com/banodoco/astrid-dev/issues/1320) |
| Render visibility and convenience | [#1476](https://github.com/banodoco/astrid-dev/issues/1476), [#1515](https://github.com/banodoco/astrid-dev/issues/1515), [#1477](https://github.com/banodoco/astrid-dev/issues/1477), [#1504](https://github.com/banodoco/astrid-dev/issues/1504), [#1503](https://github.com/banodoco/astrid-dev/issues/1503), [#1501](https://github.com/banodoco/astrid-dev/issues/1501) |
| Seeing and hearing a timeline as an agent | [#1238](https://github.com/banodoco/astrid-dev/issues/1238), [#748](https://github.com/banodoco/astrid-dev/issues/748), and the viewing, audio-excerpt and listening issues in the index |
| Editor preview | [#1433](https://github.com/banodoco/astrid-dev/issues/1433), [#1434](https://github.com/banodoco/astrid-dev/issues/1434), [#1435](https://github.com/banodoco/astrid-dev/issues/1435), and the preview-jitter issues in the index |
| Saving and the write path | [#1401](https://github.com/banodoco/astrid-dev/issues/1401), [#1402](https://github.com/banodoco/astrid-dev/issues/1402), [#1406](https://github.com/banodoco/astrid-dev/issues/1406), [#1409](https://github.com/banodoco/astrid-dev/issues/1409), [#1430](https://github.com/banodoco/astrid-dev/issues/1430), [#1431](https://github.com/banodoco/astrid-dev/issues/1431), [#1436](https://github.com/banodoco/astrid-dev/issues/1436) (Plans 76 and 77) |
| Source stacks | [#759](https://github.com/banodoco/astrid-dev/issues/759), [#1398](https://github.com/banodoco/astrid-dev/issues/1398), [#1413](https://github.com/banodoco/astrid-dev/issues/1413) |
| Generation | [#1254](https://github.com/banodoco/astrid-dev/issues/1254) and the sound-effect and listening issues in the index |

## Source identities

- Filing base: astrid-dev `origin/main` `bcb2f5f4e100d86c45b7d8bb06e6f2d6d09b6d3e`, fetched for this task. A later fetch found main at `ed8fd707` with unrelated Plan 77 evidence updates; we retain those changes in the scope branch. Main has plans through 86; number 87 was independently checked against main and open scope PRs. Local isolated scope branch: `plan/87-render-works`.
- Candidate fixes: astrid-agent `release/14/r6-fixes` / draft [#530](https://github.com/banodoco/astrid-agent/pull/530), fetched and verified at `ad10ff6de370db547e3ae2af45311751d228f98f`. Cut base `83d5f8fe`; that base is already on 15, not 14. [#525](https://github.com/banodoco/astrid-agent/pull/525) and [#526](https://github.com/banodoco/astrid-agent/pull/526) are related component contributions. The original review stops at `0f6aea928`, before the legacy-overrun commit.
- Freshly fetched Agent release heads: 14 `c0ad6b54aadd21630d98bb5039613e37efe92a8f`; 15 `8807f820eb47d6018db723511e024a0a123fbe95`. Main equality is not publication proof. Historical Runtime refs in branches/merge reports (not freshly fetched by this filing): 14 `5120462d`, 15 branch `23310dc8`, stack `b2ea261`; historical Agent 15 Runtime pin `3c28211f`. Historical App refs: 14 `e0da794a`, 15 `c5ba8cd9`. These dependency snapshots must be refreshed before dispatch, not treated as current qualification.
- Evidence source: read-only diff and the two specified tests from the running Agent worktree; no file write, checkout, stash, reset or commit there. The archive is built in a separate worktree at the exact candidate head. It retains all final stopgap code except the requested dump removal and private-alias adaptation; the library patch is a diff against the adjacent `.r6-orig` file.
- Archive branch: [release/14/r6-render-stopgaps](https://github.com/banodoco/astrid-agent/tree/release/14/r6-render-stopgaps). No PR; do not merge. Separate commits:

- [`f4f5a321c`](https://github.com/banodoco/astrid-agent/commit/f4f5a321c5a3425d1899a4dacd4403be96b0af15) — STOPGAP (do not merge): #1253 command readiness kind
- [`f84c80be3`](https://github.com/banodoco/astrid-agent/commit/f84c80be3d876b9a163982b53380c46ce8191161) — STOPGAP (do not merge): #1253 empty pack path equals unset
- [`903805786`](https://github.com/banodoco/astrid-agent/commit/9038057864ef922d58c6f5fcdad8bba08e0ba03f) — STOPGAP (do not merge): #1470 source worker host pack roots
- [`fa3b6df14`](https://github.com/banodoco/astrid-agent/commit/fa3b6df14a372b219706b3e50d23f51191a29b5b) — STOPGAP (do not merge): #1470 bundler pack roots via parent mapping
- [`54e605c6f`](https://github.com/banodoco/astrid-agent/commit/54e605c6feb31cbc53d36e059c9be1514490672d) — STOPGAP (do not merge): #1471 relative shared-import alias
- [`007c40d3c`](https://github.com/banodoco/astrid-agent/commit/007c40d3cb2d14ee275f0f6a09d434328b91cc93) — STOPGAP (do not merge): #1469 App-vendored motion pack alias
- [`b051e8ccc`](https://github.com/banodoco/astrid-agent/commit/b051e8ccce02bdf2cd5875fc87c4dc1f3872b0de) — STOPGAP (do not merge): #1472 heartbeat lease_seconds and timeout
- [`7265aa5d8`](https://github.com/banodoco/astrid-agent/commit/7265aa5d8cbb8b37c68438713eb5a3b178f7122f) — STOPGAP (do not merge): #1473 custody wait before retry
- [`221e50033`](https://github.com/banodoco/astrid-agent/commit/221e500330f00aa79aab27844db802c7d4d0455c) — STOPGAP (do not merge): #1500 archive composition fade-easing patch

Implementation destination: `release/15/plan-87` in astrid-agent, cut from its `release/15/main` head on the day; the same branch name in astrid-runtime and astrid-app only if a task changes them. Release 14 is published and is not a destination. No implementation branch is created by this filing.

## References

### Per-change verdicts

The judge's table is preserved verbatim as recommendations, including historical target labels and hypothetical PR letters. S7 describes the then-current 600 s stopgap; the archive contains the later 7,200 s value. “Ship” is a proposed disposition, not merge authority. PR-A/B/C/D/E/F refer to draft work groupings, not new live PRs. Current release skill routing in plan/tasks governs dispatch.

| # | Change | Verdict | Target | Lands in |
|---|---|---|---|---|
| 1 | `7bf7d9086` drop the editor's own-object route (#1238) | Ship after additions | 14, flows to 15 | PR-A |
| 2 | `cb90a4b99` thumbnail metadata and redundant locators | Ship as is, squashed into 1 | 14, flows to 15 | PR-A |
| 3 | `7332e03d6` name the differing context fields | Ship after additions | 14, flows to 15 | PR-B |
| 4 | `0f6aea928` launch validation matches worker contexts | Ship after additions | 14, flows to 15 | PR-B |
| 5 | `24740fdf4` media swap keeps shot clips (#1404) | Ship after additions | 15 only | PR-E |
| 6 | `ad10ff6de` unchanged legacy overrun on a pure retime | Ship after additions and a review | 15 only | PR-E |
| 7 | `d4bf28e4d` word-provenance exemption (#1403) | **Replace** | 15 only | PR-F |
| S1 | `readiness_worker_kind="command"` | Ship as is, with its test | 14, flows to 15 | PR-B |
| S2 | Empty `ASTRID_PACKS_PATH` treated as unset | Ship after additions | 14, flows to 15 | PR-B |
| S3 | `R6-DEBUG` context dump | **Drop** | none | none |
| S4 | Source worker gets the host's pack roots | **Replace** | 14, flows to 15 | PR-C |
| S5 | Personal collection root passed to the bundler | **Replace** | 14, flows to 15 | PR-C |
| S6 | Relative `rendering/shared` alias in webpack | **Replace** | 14, flows to 15 | PR-C |
| S7 | Lease 600 s, 20 s timeout, hand-edited client | **Replace** | 15 | PR-D |
| S8 | Stopgap tests | Keep one, replace one | with PR-B | PR-B |

Later rows augment rather than silently replace the historical table: App pack alias — replace with revision parity (RW-30/#1469); unsupported easing discard — replace with composition contract (RW-25/#1500); custody wait — replace with measured bounded same-incarnation recovery (RW-23/#1473). Debug remains dropped. The word-exemption use/audit claim in the original verdict prose is false and superseded by the correction in plan.md.

### Issues and evidence

The full [tooling issue index](evidence/tooling/ISSUES.md) retains today's filings; [tasks](tasks.md) link each issue they intend to close wholly or partly. Render-path issues: [#1238](https://github.com/banodoco/astrid-dev/issues/1238), [#1253](https://github.com/banodoco/astrid-dev/issues/1253), [#748](https://github.com/banodoco/astrid-dev/issues/748), [#1469](https://github.com/banodoco/astrid-dev/issues/1469), [#1470](https://github.com/banodoco/astrid-dev/issues/1470), [#1471](https://github.com/banodoco/astrid-dev/issues/1471), [#1472](https://github.com/banodoco/astrid-dev/issues/1472), [#1473](https://github.com/banodoco/astrid-dev/issues/1473), [#1474](https://github.com/banodoco/astrid-dev/issues/1474), [#1475](https://github.com/banodoco/astrid-dev/issues/1475), [#1476](https://github.com/banodoco/astrid-dev/issues/1476), [#1477](https://github.com/banodoco/astrid-dev/issues/1477); related prior lease-channel issue [#1320](https://github.com/banodoco/astrid-dev/issues/1320) is not silently declared the same cause.

New distinct filings after open/closed duplicate searches: [#1500](https://github.com/banodoco/astrid-dev/issues/1500) fade/easing, [#1501](https://github.com/banodoco/astrid-dev/issues/1501) task inventory size, [#1502](https://github.com/banodoco/astrid-dev/issues/1502) queued orphan after restart, [#1503](https://github.com/banodoco/astrid-dev/issues/1503) stale validated dependency diagnosis, [#1504](https://github.com/banodoco/astrid-dev/issues/1504) range before admission. Fenced recovery covers the unresolved active-task count with #1474; expiry alone is not evidence of a dead process.

Deferred issue evidence remains attached: #1401 to Plan 77, broad #1402 to Plan 76, complete #1403 binding to Plan 18; #1407/#1408 project-pack CLI, #1410–#1412 and #1433–#1435 preview, #1431/#1432 broader editing, #1254/#1392–#1396 generation/media. We do not claim this plan closes them. #1411/#1412 are context for pack parity, not closure targets.

See [evidence/INDEX.md](evidence/INDEX.md) for every included file's purpose/task or issue, and [sanitizer summary](evidence/SANITIZER.md) for limits, exclusions and any refused files. Original judge artifacts retain historical prose and errors for traceability; newly authored prose uses team voice and refers to a film project. All absolute home paths and emails are sanitized in attached text, with credential-looking files refused rather than silently redacted.


**Filing verification (verified):** The archive head is `221e50033`, the original candidate remains `ad10ff6de`, and the archive library diff is byte-identical to the retained original/live difference. Six captured source/test files match the read-only source exactly; the other changes are the documented dump removal and alias adaptation. Changed Python parses and `node --check remotion/webpack-alias.mjs` passes. The 132 source payload hashes/text transformations were checked independently; all 134 evidence files are indexed, totalling 1,991,841 bytes, with zero skipped/refused/missing source files and nine decodable JPEGs below 300 KB. The scope branch merged main at `ed8fd7079305488b7e829e0618533a83828a6f8e`, then refreshed to `329ae89d97388a0c8a35ba205686c93e2184e3ba` before filing completed, retaining the intervening Plan 77/84 updates. The document check with `--base origin/main --body-file ../pr-body.md` passes. The complete 454-test script suite has 451 passes and three failures reproduced on untouched main: the two skill-installer cases encounter BSD sed behavior, and the atomic-write test compares `/var` against resolved `/private/var`. The three affected document tests pass again after the merge. These are filing/static checks, not a product-render or integrated-tuple qualification.
