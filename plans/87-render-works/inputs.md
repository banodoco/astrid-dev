# Inputs — The renderer works end to end

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Reshaped on 23 November 2026 at the owner's direction: this plan gets the renderer working end to end with the fixes in the proper code; [Plan 88](../88-timeline-edits-land/plan.md) lands the timeline fixes; everything else is an issue. Filing authority only; no run has started.

**Prior art:** Plans 27, 39, 59, 69, 76, 77, 78 and 83 were read for overlap ([landscape](evidence/eff/landscape.md)). No plan owns "render works"; Plan 27 keeps export choices, Plan 78 holds the open motion pack pin, Plan 83 the custody module split. The first full draft by an independent judge is kept as [evidence](evidence/shipplan/PLAN.md).

**Approach:** Port the sixteen changes onto a Release 15 plan branch, get a render working, replace the stopgaps one by one with the render as the test, prove it on the owner's heavy timeline, then add one real render check to CI.

**Challenge:** An independent [code review](evidence/review/ASTRA-530.md), a [trial integration](evidence/mergescope/REPORT.md), a [root-cause investigation](evidence/astra20/REPORT.md) and an independent [judge](evidence/shipplan/VERDICTS.md) all preceded this reshaping. A second opinion on the reshaped plan is pending.

**Proof and limits:** A film rendered with the sixteen changes, in four ranges, on a stack cut from an older commit. Nothing has rendered on `release/15/main`. The cause of heartbeat renewals stopping is unknown. Fact checks of the release heads, CI and the branch inventory are in [evidence/eff](evidence/eff/).

**Review rounds:** One round at the end.

**Run start:** Pending — waits on a claimed run. The owner asked for the plans and issues to be set up, not executed.

## Owner decisions

The plan was reshaped on 23 November 2026 at the owner's direction: one plan that gets the renderer working end to end, a second plan for the timeline fixes ([Plan 88](../88-timeline-edits-land/plan.md)), and issues for everything else. The earlier decisions D1 to D7 are closed out below. P1 was decided by the owner; P2 and P3 by the coordinating session, which the owner asked to decide them. This is plan and issue set-up only: no run has started.

| Decision | Options and recommendation | State |
| --- | --- | --- |
| P1 The heavy test timeline | Decided by the owner, 23 November 2026: the generated heavy fixture built by the App's [`scripts/save-loop/build-fixture.mjs`](https://github.com/banodoco/astrid-app/blob/release/15/plan-77/scripts/save-loop/build-fixture.mjs) ([how to run it](https://github.com/banodoco/astrid-app/blob/release/15/plan-77/scripts/save-loop/README.md)). It generates its own media and needs no owner media or GPU. Standard variant: 616 parent clips, 46 shot occurrences, a 2.6 MB document. `large-shots` variant: three 480-second shots of 32 child clips each on 90-second generated sources. It asks for 25 GiB free. | Decided |
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

1. **Get it working first, then make it right.** The draft built each proper fix separately before any render ran on Release 15. We port everything, stopgaps included, render, then replace stopgaps one by one with the render as the test. Reason: a working render from day 2 is a better regression test than any hand-built one, and it is how the defects were found in the first place.
2. **Release 15 only.** Reason: Release 14 is published; every defect site is present on the Release 15 head; a second line doubled the conflict work.
3. **No new journey.** The draft specified a new render journey with its own fixture. An integration test that executes `rendering.render` against a real Runtime and pack host already exists, as does a full motion pack fixture and a lane that installs Remotion and a browser ([CI facts](evidence/eff/ci.md)). We extend that. Reason: about a day instead of several.
4. **Custody and lease stay in; recovery goes out.** A heavy render cannot finish while either can kill it, so RN-8 and RN-9 are render-path work. What happens after a failure (poisoned slot, stuck tasks, scratch, cancel wording) does not stop a render from working; restarting the stack is an acceptable workaround during the plan. It is [#1514](https://github.com/banodoco/astrid-dev/issues/1514).
5. **Resumable renders are an issue, not a task.** The draft added checkpointed renders after the film had to be rendered in ranges. With RN-8 and RN-9 a whole render should finish; resuming is an improvement, not a precondition. [#1515](https://github.com/banodoco/astrid-dev/issues/1515).
6. **The three timeline commits ride the branch but belong to Plan 88.** Splitting them out of the donor branch before porting would cost a second conflict resolution for no gain; they do not affect rendering.
7. **Stopgaps may sit on the plan branch, never on the release branch.** Each is a tracked row; the branch cannot be offered for merge while one remains.
8. **Write-path fixes left to their owners.** Plans 77 (active), 76 and 69 (active) already own saving, agents editing together and unbound shot clips. This plan sends evidence and fixes none of it.

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

Proposed implementation destinations, pending D1/D7: shared-contract work in `release/15/plan-87` in each affected repository, cut from its current `release/15/main`; bounded older-line fixes in issue-scoped branches only if that release is still open, then forward to 15. No such implementation branches are created here. Runtime producer/generator changes must precede regenerated Agent pin/client artifacts; App manifest/pack pins follow the exact qualified tuple. The published motion-pack alias requires the override in the bundler process environment; a host-level export can be stripped by child-environment policy, so reproduction must supply it explicitly at that boundary. No end-to-end rerender of the sanitized adaptation is claimed. Composition source/repository identity is still to be resolved from the installed package's provenance before RW-25 dispatch.

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
