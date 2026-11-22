# Inputs — A render that works, and stays working

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — we were asked to file this corrected plan, push an evidence-only stopgap branch, attach sanitized evidence, file missing defects and cross-link PR #530. This is filing authority, not agreement to D1–D7 or a product execution/release start. Next: scope review and explicit decisions.

**Prior art:** We read the contributor/plan/release/merge/bugfix skills and current project templates, strategy and prior Plans 18, 27, 39, 59, 63, 69, 75–78, 85 and 86. Plan 27 owns export choices; Plan 59 the creative outcome; Plan 39 general green checks; Plans 76/77/18 own large write-path/collaboration/binding designs. We retain the independent judge's draft/verdicts/decision log, review through `0f6aea928`, conditional cherry-pick trials, Astra receipt timeline, reports and render iteration as [indexed evidence](evidence/INDEX.md). Candidate tests cover pieces; the workflow inspection in mergescope found no representative installed/source collection-pack command-worker journey as a merge gate. We have not run product tests or independently qualified those historical claims in this filing.

**Approach:** Proposed — reuse the sound committed projection/media/context work with its missing tests; consolidate worker/registry ownership through existing channels; replace unsafe exemptions, lease inflation and aliases with contracts in their owning repositories; add one real journey and bounded recovery/checkpoint behavior. No new pack. We reject merging the donor or stopgap archive wholesale. A new plan is justified by independently useful shared render/recovery contracts across repositories; bounded defects still have issues and focused product PRs. Reuse Plan 85's measurement method and Plan 27's output contract.

**Challenge:** The independent judge supplied the verdict table below and [decision log](evidence/shipplan/DECISIONS.md), weighing [code review](evidence/review/ASTRA-530.md) and [trial integration](evidence/mergescope/REPORT.md). Those are recommendations, not accepted decisions. Pending — a fresh simplification critique of the corrected contracts and checkpoint scope before greenlight; the draft predates the new evidence. No fresh architectural approval is claimed by mechanical link/archive checks.

**Proof and limits:** Filing checks verify document structure, evidence sanitization/indexing and archive correspondence. Historical evidence establishes per-range completion with stopgaps and two distinct failure mechanisms. It does not qualify a clean integrated tuple, identify why heartbeat renewal stops, identify the failed helper executable/eventual exit, or prove any local stopgap fixes a cause. The exact >4 MiB and abandoned-caller cases need isolated reproduction. Seam cleanliness is reported with retained frames; no new numerical seam measurement is claimed.

**Review rounds:** Proposed — at most two final rounds per phase, plus one shared-contract stop RS1 before dependent integration/qualification. Agreement pending. The later native custody and checkpoint findings warrant the stop despite the historical judge's preference for end-only review. No review budget has been accepted or consumed for future implementation.

**Run start:** Pending — no product run authorized. The current task authorizes only this scope filing, evidence archive/branch, issue filings and one PR comment. We did not alter the running stack, timeline or installed release tree.

## Owner decisions

All D1–D7 remain open. The following recommendations preserve the judge's options; we have not selected them.

| Decision | Options and recommendation | State |
| --- | --- | --- |
| D1 Target | (a) Render-path fixes to 14 and forward, Plan 69-based fixes to 15; (b) everything to 15. Recommendation (a), conditional on the actual release cut/publication state. No render on current 14 head has been established. | Open |
| D2 Word-anchored retime | (a) Ship the exemption; (b) allow only unchanged offset from the resolved word, else supported cut-relative refusal; (c) refuse until binding exists. Recommendation (b), subject to resolvable-word/reflow proof. No film edit used the exemption; any first real temporary use requires prior independent audit. | Open |
| D3 Lease | (a) Ship a longer lease (draft 600 s, later 7,200 s); (b) measure, fix the blocked/stopped renewal path and declare the lease once in Runtime; (c) (b) with a declared 120 s interim at claim/heartbeat only if measurement puts the repair more than a week away. Recommendation (b). The verdict stands: **measure, then fix; a longer lease is wrong**. Astra shows abrupt final renewals at 145.990/155.869 s (32 receipts in C), not gradual slowing; no cause is established. B/F instead fail custody with valid leases at 1,205/200 s. A 7,200 s lease did not protect F. Instrument task reads, pump gates, host locks, request/ACK and thread exits before choosing which path to change. | Open |
| D4 Launch-context check | (a) Keep adding normalizations; (b) keep effects checks, build environment once, show safe path differences; (c) remove the check. Recommendation (b); retain negative changed-root proof. | Open |
| D5 Pack roots | Generated registry owns the list and bundler consumes it through the existing explicit channel. Recommendation yes, with pack revision parity and a named shared import rather than global relative aliases. | Open |
| D6 Outbox interim | Coordinate with Plan 76: dry-run flights never block and sessions do not replay each other's flights. Recommendation yes for the bounded interim; broad collaboration remains Plan 76. | Open |
| D7 Process | Proposed Plan 87 in Release 15 with older-line fix branches only if D1 is accepted, and a required real render check once green. Existing draft N1–N5 map to #1470/#1471, this plan's RW-7/RW-8, #1472, #1475 and #1477; later defects are now linked below. Release membership and required settings remain review decisions. | Open |

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
