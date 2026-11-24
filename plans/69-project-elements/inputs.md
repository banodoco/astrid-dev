# Inputs — Project elements

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — the owner confirmed on 21 November 2026 that this plan "makes sense" for their editing work, and set the order (this plan, then Plan 77, one manager): [decision](https://github.com/banodoco/astrid-dev/issues/1224#issuecomment-7067275617). Background: the owner said on 21 November 2026 that this work ("the existing timeline work that we're working on top of") goes into the next release and should be set up properly with its plan and branch; that it was "just me trying to edit a clip on the timeline and actually edit the tools", not Plan 59's project; and "we should create a plan for this and correlate it" with Plan 78, "fixing and improving a bunch of stuff for the practical use of the video editor and timeline". The outcome in [plan.md](plan.md) was read from the commits; PE-1 checks it against the code.

**Prior art:** The work itself, on `release/14/plan-69`, 18 to 21 November 2026; commit lists per repository are in [source identities](#source-identities). [Plan 78](../78-live-custom-element-editing/inputs.md#source-identities) recorded the same donor heads. No astrid-dev plan, pull request or issue recorded it before this pack (searched 21 November: plans, releases, pull requests, issues and the Release 14 mailbox #796).

**Approach:** Record the existing work as a plan and move it to Release 15's branches by merge, rather than rewrite or rebase it, so nothing already pushed is lost and its session can carry on.

**Challenge:** Not needed — this pack records existing work and moves its branch; it decides no new design. The work's own review happens at PE-2 and in the Release 15 qualification.

**Proof and limits:** See [completion](plan.md#completion); the outcome is read from commit titles until PE-1 checks it in the code.

**Review rounds:** One final review of at most 2 rounds (R), because the code exists and its own tests ran; no review stop.

**Run start:** 21 November 2026 — Codex manager (hosted in Claude session session_011EzfW1FXS3o7GFnNSB7cZS), route S. The owner asked for a Codex manager on 21 November 2026. The host checks in hourly. May open and merge PRs into `release/15/plan-69` after focused proof, dispatch workers, and merge `release/15/main` into the plan branch. The owner gave a standing go for PE-3 to the hosting session on 21 November 2026, subject to D7. The broader grant on 21 November, given to the hosting session, also authorizes bounded R2 follow-up and the Release 15 Agent model-lock repair under D8. Changes to `release/14/*` or a product `main`, publication, live installs, the owner's timelines, and paid spend remain outside this run.

## Owner decisions

- **D1 Release.** Decided, 21 November 2026: Release 15, with its branch `release/15/plan-69` (the owner's choice in the Release 15 setup session).
- **D2 Scope.** Decided, 21 November 2026: accepted as written ([decision](https://github.com/banodoco/astrid-dev/issues/1224#issuecomment-7067275617)).
- **D3 Order.** Decided, 21 November 2026: this plan first, then Plan 77, run back to back by one manager.
- **D4 Vendor restore.** Decided on 21 November 2026, given to the hosting session. Restore App #297's five vendored `am-footage` and `am-discord` files and their provenance entries to `release/15/main` bytes. Check vendor sources and the focused preview behavior.
- **D5 Top-level animation render.** Decided on 21 November 2026, given to the hosting session. Complete Plan 69 for effects and components. The Agent will explicitly refuse an admitted top-level animation before managed render and preserve existing reference validation. Track parity and the `@banodoco/timeline-composition` change and repin separately. [Parity issue #1257](https://github.com/banodoco/astrid-dev/issues/1257)
- **D6 Optional motion pack.** Decided on 21 November 2026, given to the hosting session. Rendering an `astrid_motion` effect requires the pack installation. For a known uninstalled effect, name the pack to install and retain refusal for unregistered effects.
- **D7 Standing PE-3 go.** Decided on 21 November 2026, given to the hosting session. Land Runtime, then Agent repinned to the landed Runtime, then App repinned to both, after R2 passes on the exact integrated tuple and full hosted CI on each combined plan head shows no failing ID absent from `release/15/main`. Dispatch the full workflow only while the repository has no queued or running `release/14/*` runs. Each landing PR names Plan 69, records the inherited RunPod digest mismatch and larger-commit WAL refusal, links the narrowed animation render scope, and states the optional pack requirement. If a condition fails, hold the landing and report the reason to the host.

- **D8 Bounded review follow-up and Release 15 repair.** Decided on 21 November 2026, given to the hosting session. If R2 identifies a small contained finding, fix it and have the same reviewer recheck that finding on the exact commits. Bring design-level findings to the host. The lane may open a small Agent release PR that aligns the Linux RunPod recipe with the actual model-lock digest, using focused proof and the same full comparison gate.

The hosting session updated CI scheduling on 21 November so Release 14 runs no longer defer the Release 15 dispatches. Reuse exact completed base evidence and complete missing Agent base shards. The owner authorized one replacement full App run after the test-only 0.2.15 fixture correction, on the exact new combined App head.

## Source identities

Before 21 November the work was on `release/14/plan-69`, based on `release/14/main` (not on Plan 59): App `e0c6f7cdb` (10 commits), Agent `83d5f8fe3` (21 commits), Runtime `b2ea261` (5 commits), heads on 21 November.

`release/15/plan-69` in each repository is `release/15/main` after the 21 November forward of `release/14/main` ([astrid-dev#1224](https://github.com/banodoco/astrid-dev/issues/1224)), with `release/14/plan-69` merged in:

| Repository | `release/15/plan-69` head | Pins |
| --- | --- | --- |
| astrid-app | `5866b23bb` | Agent `58c749cab`, Runtime `1046f4074` |
| astrid-agent | `58c749cab` | Runtime `1046f4074` |
| astrid-runtime | `1046f4074` | — |

What the merge changed, and what PE-1 should check first:

- **Runtime:** Plan 59's verify-once CAS design (already on `release/15/main`) is kept; this plan's duplicate (`b2ea261`) and its API tests are dropped, and `test_descriptor_reader_does_not_inherit_live_cas_proofs` is a strict xfail for [astrid-dev#1222](https://github.com/banodoco/astrid-dev/issues/1222).
- **App:** the preview keeps both Release 15's `getCurrentFrame` and this plan's removal of the element-readiness gate.
- **Agent:** three esbuild-discovery tests in `tests/core/test_project_packs.py` fail on `release/14/plan-69` itself (`KeyError: 'ASTRID_REMOTION_PROJECT_DIR'`), and element admission needs the renderer's pinned Node v20.19.4 (`ASTRID_NODE_EXECUTABLE`).
- Every focused test failing on these heads also fails on `release/15/main` or on `release/14/plan-69`; none is new. Destination for every task: the same repository's `release/15/plan-69`.

## PE-1 inventory (21 November 2026)

Verified on App `5866b23bb`, Agent `58c749cab` and Runtime `1046f4074`, with the scoped selections in [tasks](tasks.md).

- **Admission.** Agent's `astrid/core/element/project_packs.py` compiles with the renderer's pinned Node and esbuild and binds the compiled result into the snapshot. `test_project_pack_snapshots.py` passed 48 tests, including compiled module and legacy readmission. All three compiler-discovery cases passed with `ASTRID_REMOTION_PROJECT_DIR` pointing at the checkout's renderer and Node 20.19.4 selected.
- **Serving.** Runtime's project elements routes in `runtime_protocol/server.py` and `service.py` list current admissions from project documents and serve verified bundle bytes within the selected project. All 33 `test_runtime_project_elements_http.py` cases passed, including list without CAS reads, cross-project refusal and closure verification.
- **Loading.** App's `admittedElementLoader.ts` and `admitted-elements.ts` check project ownership and digest, fence stale selections and preserve the editor when list or import fails. `admittedElementLoader.test.ts`, `admitted-elements.test.ts` and the applicable Remotion preview and placeholder cases passed. Local browser-backed tests could not start the Playwright revision selected by App. CI and the integrated journey supply browser evidence.
- **One compiler.** `test_render_stages_the_admitted_compiled_module_as_the_component` passed in Agent. The App loader consumes the digest-pinned bundle that Runtime serves. Preview to final-render visual parity is still open on the integrated stack.
- **Editing verbs.** Agent's `timeline_elements.py` places the exact admitted element reference and `_clip_scalar_commands.py` rejects unbound clips. The named element placement and selected schema tests passed.
- **Speed and validation.** The named Agent timing and boundary tests passed, including scoped validation, untouched-baseline handling and the Runtime HTTP timeout. Runtime retains Plan 59's live identity cache. The named history tests cover warm reuse and changed-object rejection, and PE-2 supplies the real pinned-reader check. These checks cover correctness. They supply no live editor latency claim.

The Agent's two CLI parity failures occurred on both comparison heads. App's named failure IDs appeared on the Release 15 base or the Plan 69 donor, and the two extra admitted-loader type diagnostics also appeared on the donor. Runtime's original scoped comparison found 23 pre-existing failed or errored IDs, including fixture setup errors from the tracked Agent pin. The inventory identifies one outstanding integrated journey in [PE-1a](tasks.md).

## Installed qualification (21 November 2026)

- Initial combined App `e576c7fe`, Agent `efccee92`, Runtime `162500fe` served admitted digests and rendered the synthetic effect at 1920 × 1080. The center RGB matched its preview within one channel value. A fresh browser with the list returning HTTP 503 displayed the missing-element reason, and a normal track edit saved and survived a fresh reopen.
- On App `b0d4d83a`, Agent `134c6dd0`, Runtime `95920f84`, the SDK placed a project effect on installed `animated-media-transform`, with a durable public receipt. The editor fetched two compiled bundles with HTTP 200 and displayed the expected project effect and animation colors. The managed renderer refused the top-level selected animation at `$.clips[1].clipType`. Render parity for the animation remains open.
- The ordinary installed launcher reported `am-discord` as unregistered in its reusable visual element catalog. The App vendor’s `am-discord` descriptor keeps the same ID, kind and owner between the Release 15 base and the deliberate vendor revert. Its descriptor and two implementation file hashes differ. The am-discord refusal remains separate evidence from the successful installed-effect control.
- A fresh profile in the real App used the locally mocked ACP boundary. When two exact element list calls returned HTTP 503 the composer sent a synthetic project-scoped prompt and displayed the canned reply. The browser recorded zero external-network attempts. Independent App tests also cover prompt dispatch during both pending and immediately failed list calls.

- On the current App review candidate `fece2c96` with Agent `134c6dd0` and Runtime `95920f84`, a registered-effect-only preview and managed render matched within one RGB value per channel. A separate normal track rename with the element list returning HTTP 503 saved one full-v2 commit step, advanced the public version once and reopened at that exact head with the renamed track and missing-element reason.

## Inherited Agent model-lock failure (21 November 2026)

Agent Release 15 base `aac1ceb6` and Plan 69 `134c6dd0` contain the same RunPod model lock and recipe pin. The actual hash of `astrid/packs/runpod/models.lock.json` is `e35d5189557b8fe09b54a218b69666a74c678182ea31344245726581130595ff`. The Linux cu130 recipe expects `40f37e271863e67d02fd6bcd6badb00a474eb6ec051ead7e8edf04281b2ef72a`. The release lead reported 35 failures out of 50 in the untouched base’s `tests/packs/runpod/test_h3_release.py`. The manager compared the exact source hashes on both heads. The owner authorized this lane to fix the release base. The focused candidate restored 34 of the 35 failing cases and introduced no new failing IDs. The remaining failure reaches an existing null revision that the earlier digest refusal had masked. [Base repair #473](https://github.com/banodoco/astrid-agent/pull/473) · [Source revision follow-up #1264](https://github.com/banodoco/astrid-dev/issues/1264)

## References

- [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md), which builds on this plan's branch.
- [Plan 78](../78-live-custom-element-editing/plan.md), which names this work as its donor (`release/14/plan-69` heads in its source identities) and starts from it.
