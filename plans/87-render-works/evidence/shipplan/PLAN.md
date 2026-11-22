# A render that works, and stays working

Draft of 22 November 2026, written from a read-only review. It is one file here; when filed in astrid-dev it splits at the three part headings into `plan.md`, `tasks.md` and `inputs.md` under `plans/84-render-works/` (84 is the next free number on astrid-dev `main` at `91230134`; re-check before filing). Section headings follow `templates/project/`. Recording this plan authorises nothing.

Source labels: **[V]** read by me in code or logs; **[P]** reported by another agent's write-up; **[I]** inferred. Verdicts on each existing change are in [VERDICTS.md](VERDICTS.md); the choices between competing opinions are in [DECISIONS.md](DECISIONS.md).

---

# Part 1 — plan.md

**Project:** A render that works, and stays working

**Goal:** A creator or agent renders a real timeline (built-in, collection-pack and project elements, word-anchored clips, newly imported media) on an install and on a source stack, and CI stops any change that breaks it.

**Status:** `queued`

**Owner:** Unassigned

**Estimate:** About 20 engineering days in three phases: 8, 6 and 6.

**Waiting on:** owner decisions D1 to D7; a manager; filing of five issues.

**Vision role:** Foundational enabler — rendering is how any finished work leaves Astrid, and Release 14's highlight is "a real video is finished with Astrid's own tools".

## Outcome and scope

**End state, each line checkable:**

1. The render journey (below) passes on `release/14/main` and `release/15/main`, installed and source profiles, on Linux for pull requests and macOS on push.
2. A 3-minute render on a loaded 8 GB machine keeps its lease; a killed render frees its scratch and the next one is admitted.
3. Every render refusal names the fact that differs and a recovery that works.
4. An agent can swap media on, and ripple-retime, a word-anchored shot clip, and cannot leave the clip's declaration and interval in disagreement.

**In scope, in four groups:**

- **(a) Render and edit work at all:** registry projection, worker launch context, pack roots for the bundler, media swap, legacy overrun, constrained word retime.
- **(b) Safety net:** the render journey in CI; a test that every printed command hint parses.
- **(c) Agent-facing quality:** lease kept under load, scratch reclaimed, truthful errors, render progress, whole-timeline revert.
- **(d) Write path, small fixes only:** scoped delete guard, oversized dry runs, item-scoped list removal, the dry-run crash, an outbox interim.

**Non-goals:**

- Merging `release/14/r6-fixes` or any stack branch. It carries 21 Plan 69 commits into Release 14 [P: mergescope].
- Redesigning saving. Edits that fold in unrelated rewrites (#1401), agents editing together (#1402 in full) and word binding for shot clips (#1403 in full) belong to Plans 77, 76 and 18 phase A, which are already in Release 15 [V: `releases/15.md`]. This plan sends them its evidence.
- Editor preview defects (#1410 to #1412, #1433 to #1435), project-pack command gaps (#1407, #1408), generation gaps (#1254, #1392 to #1396).
- Windows in the render journey (follow-up once Linux and macOS are green).
- Rendering speed.

## Existing work and decision

**Why rendering had never worked end to end on these builds.** Five gates failed one after another, each hiding the next: registry admission, launch-context validation, worker readiness, bundler resolution, then the lease [V: `render/REPORT.md`, `take/probe1.log` to `probe6.log`, `almost-ready-v38-full.log`]. Three structural causes produce all of them.

1. **No check runs the real path.** Each layer is tested against a hand-built copy of its neighbour: launch tests rebuild the expected path by hand, one inspects a call site's syntax tree [V: `tests/core/rendering/test_remotion_host_regressions.py`], and the installed journey is not a pull-request check [P: mergescope §4]. Nothing renders a timeline that has a collection-pack element, through a command worker, on an install.
   *Remedy:* the render journey (RW-7, RW-8).
2. **One fact has several owners, and they drift.** Release 14's own rule is "one owner for each fact" [V: `releases/14.md`]. Tonight's drifts:
   - Which packs a render sees: five answers (VERDICTS.md, S4 to S6).
   - A worker's environment: predicted at launch, built again at dispatch; four mismatches in one evening.
   - What a registry entry may hold: the schema admits `thumbnailUrl`, the editor writes an own-object route, the Runtime drops it, the Agent refused it.
   - A clip's time: the word declaration and the interval.
   - Commit rules: the client accepts an item-scoped removal the Runtime refuses (#1409); `check` passes what `publish` refuses (#1405); `validate` passes what `admit` rejects (#1408).
   *Remedy:* one builder for the worker environment (RW-2); the generated registry owns pack roots (RW-3); one shared case table per client and Runtime rule pair, starting with #1409 (RW-20).
3. **Guards fail closed without a diagnosis or a way back, on shared single channels.** A refusal says "context differs", "an older Astrid is still running" or "may or may not have been committed", and the advice it prints is wrong [P: `edits/DEFECTS.md` §2, §8]. Failures leave state that blocks the next try: scratch, an unknown flight, a lease with unresolved custody. One Runtime mutex and one outbox per actor and timeline let one slow or stuck party stall everyone [V: `server.py:1574-1576`; P: 487 timeouts, `packtimeout/REPORT.md`].
   *Remedy:* a guard names the differing fact and a recovery that CI has run (RW-2, RW-9, RW-14, RW-15); failed work cleans up (RW-12); the heartbeat leaves the starved path (RW-10, RW-11).

**What is kept.** Five of the seven commits and two stopgaps, rebuilt on release-head branches. PRs #525, #526 and #530 close in favour of the split below.

**What is replaced.** The word-provenance exemption, the 600 s lease, and three pack-root stopgaps. Reasons are in VERDICTS.md.

**Why a plan and not only issues.** The fixes are issues and fix branches. The journey, the pack-root owner and the lease change are new shared contracts across Agent and Runtime, which is project scope.

## Sequence and readiness

**Target branch.** Fixes flow forward only [V: release skill, step 2]. So:

- A fix to code that exists on `release/14/main` lands there on a `release/14/<topic>` branch and reaches 15 by the usual `release/15/forward-14-N` merge: PR-A, PR-B, PR-C, PR-G, PR-H.
- A fix built on Plan 69 code lands on `release/15/main` only: PR-E, PR-F. Their base does not exist on 14 [P: trial conflicts].
- Design-bearing work lands on 15 only: PR-D, PR-I.

Release 14 has an agreed publication bar and adds no capability [V: `releases/14.md`]. If its Lead says it is closed to these fixes, everything goes to 15 and 14 records render as a known gap (D1).

**What I would need to know to be surer:**

1. Whether render fails on the `release/14/main` head at all. All of tonight's evidence is from the Plan 69 line. RW-7's first run answers this.
2. Why Agent `main` equals `release/14/main` (`c0ad6b54`) [P: mergescope]. If Release 14 has been published since the brief I read, a 14 fix is a fix release with the next number.
3. The cause of the installed stack's context mismatch (#1253), never identified.

**Pull requests, in order.** All in astrid-agent unless named. Each is cut from the release head on the day.

| PR | Branch | Holds | Closes |
|---|---|---|---|
| A | `release/14/fix-1238-registry-projection` | RW-1 | #1238 |
| B | `release/14/fix-1253-worker-context` | RW-2 | #1253, part of #748 |
| C | `release/14/fix-bundler-pack-roots` | RW-3 | new issue N1 |
| A′ | astrid-app `release/14/fix-1238-import-locators` | RW-6 | #1238 (writer) |
| G | `release/14/render-journey` | RW-7, RW-8, RW-9 | new issue N2 |
| E | `release/15/fix-1404-occurrence-media-swap` | RW-4 | #1404, part of #1405 |
| F | `release/15/fix-1403-word-retime` | RW-5 | part of #1403 |
| D | astrid-runtime and astrid-agent `release/15/fix-lease-starvation` | RW-10, RW-11 | new issue N3 |
| H | `release/14/fix-render-recovery` (one PR per task) | RW-12, RW-14 to RW-17 | N4, N5, #1398, #1397, #1413, #1430 (part) |
| I | `release/15/fix-<issue>` (one PR per task) | RW-18 to RW-22 | #1406, #1246, #1409, #1436, part of #1402 |

A, B and C merge in that order. G is developed first and run by dispatch against each fix branch as its proof; it merges after C, so it is green when it lands, and only then is it asked for as a required check.

**Blocked on a decision:** PR-F on D2; RW-11 on D3 and RW-10's measurements; RW-2's shape on D4; RW-3 on D5; RW-22 on D6; the required check on D7.

**Risks.**

- `generic_host.py` is 18,888 lines and changed on both release lines; PR-B conflicts on both [P]. Keep PR-B to the builder and its callers.
- The journey may be slow or flaky on hosted runners. Hold it to a 3 s, 480×270 timeline; the lease case is a separate Runtime test.
- The motion pack is pinned from outside the Agent; RW-3 needs its pin moved in step.
- A Runtime change needs regenerated Agent pins and a new installer tuple [P: mergescope §4].
- The film's stack keeps the unsafe exemption until PR-F lands.

**First three days.**

- *Day 1.* File N1 to N5; ask the Leads for `release:14` and `release:15` labels. Cut PR-A and PR-B. Start RW-7 and run its skeleton by dispatch on both release heads, both profiles; record the first failing stage for each. Run RW-13 once the film render has finished.
- *Day 2.* Land PR-A on 14. Review PR-B. Cut PR-E from the 15 head (its picks apply cleanly there). Open the Runtime instrumentation half of PR-D (RW-10). Start PR-C.
- *Day 3.* Forward 14 into 15. Land PR-B and PR-E. Journey passes through worker readiness on both lines. Take D2 and D3 to the owner with RW-10's first numbers.

## Interfaces and handoff

**Consumes:** `release/14/main` and `release/15/main` heads in astrid-agent, astrid-runtime and astrid-app at cut time; the Runtime pin in `runtime.lock.json`; the motion pack's pin.

**Produces:**

- `ASTRID_RENDER_PACK_ROOTS` as the bundler's only source of pack roots, written from the generated registry.
- One worker-environment builder in the execution host.
- The render journey, runnable by `workflow_dispatch` against any branch, reporting the first failing stage by name.
- A Runtime slow-request log line and a declared lease length.

**Limits:** Windows is not covered. The journey does not prove a long render keeps its lease; RW-11's own test does.

## Completion

- The journey is green on both release heads, both profiles, and red when any one of the five gates is re-broken (each negative case is in RW-7).
- A killed render leaves less than 100 MB of scratch and the next render is admitted.
- The film renders on a build made from `release/15/main` with no local patches.
- Limits of this proof: one fixture timeline, two operating systems, no rented machine.

---

# Part 2 — tasks.md

**Task ids:** `RW-n`. **Critical path:** RW-7 → RW-1 → RW-2 → RW-3 → RW-8. **Test inventory:** `tests/packs/rendering/test_managed_timeline_render.py`, `tests/core/rendering/test_managed_asset_identity.py`, `test_remotion_host_regressions.py`, `test_remotion_registry_context_key.py`, `test_remotion_runtime.py`, `tests/packs/rendering/test_remotion_v3_aliases.py`, `tests/core/test_subprocess_env.py`, `tests/integrations/test_generic_host_remotion_render.py`, `test_lease_publication_journey.py`, `tests/timeline/test_occurrence_media_swap.py`, `test_legacy_occurrence_timing_provenance.py`, `tests/editing_conformance/test_commit_boundaries_d12.py`. Every scope and line reference below: re-check against the code at dispatch.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| **Phase 1 (a): render and edit work** | | | | | |
| RW-1 Own-object routes and thumbnail metadata are projected out before the managed check; refusal names the entry | N | — | `astrid/core/rendering/assets.py`, `packs/rendering/actions/render/managed_timeline.py`, three SDK callers | `test_managed_timeline_render.py`, `test_managed_asset_identity.py`, plus unused-foreign-entry and admission-rollback cases | [ ] |
| RW-2 One function builds a worker's environment; the launch probe and dispatch both call it. Includes command readiness kind, empty-equals-unset in `_normalize_registry_selectors`, field names plus path values in the mismatch message. No debug dump | X | — | `generic_host.py:_dependency_pythonpath`, `_launch_worker_probe_environments`, `_child_environment`, `_run_command_definition`; `remotion_runtime.py:_registry_context`, `_normalize_registry_selectors`, `_validated_runtime` | New parity test through real dispatch for every Remotion-capable record × {native, command} × {source, installed}; `test_remotion_registry_context_key.py`. N helpers: list the records; port the three existing tests | [ ] |
| RW-3 The registry generator writes the pack roots it used; the render passes them as `ASTRID_RENDER_PACK_ROOTS`; the bundler stops scanning `ASTRID_PACKS_PATH`. Shared contracts import by name; motion pack's four imports changed and its pin moved | X | D5 | registry generator in `remotion_runtime.py`; `renderers/remotion/run.py:_execute_remotion_locked`; `remotion/webpack-alias.mjs:packElementAliases`, `applyAliasesForRoot`; project-element compiler; motion pack repo | `test_remotion_v3_aliases.py` plus a case with a pack in a collection root outside the tree, both profiles; journey stage "bundle" | [ ] |
| RW-4 Media swap keeps shot clips; unchanged legacy overrun survives a pure start shift | X | — | `sdk/timeline/media_swap.py`, `native_occurrence_media_commands.py`, `commit_session.py`, `_commit_timing_validation.py:_fixed_visual_duration`, `validation.py:_retained_overrun_does_not_worsen`, `validate_final_candidate` | `test_occurrence_media_swap.py`, `test_commit_boundaries_d12.py`, plus grown-bound, shrunk-bound and speed-change cases | [ ] |
| RW-5 An interval-only edit to an unbound word-anchored shot clip passes only when its offset from the resolved word is unchanged within one frame; otherwise refused, naming the cut-relative form | S | RW-4, D2 | `_commit_timing_validation.py:_BasisReader.signature`, `_signed_failures`, `_legacy_exemptions`; reads `reflow.py`, `_timing_evaluators.py` | `test_legacy_occurrence_timing_provenance.py`, plus resolvable-word move then reflow (no snap-back) and a move without narration change (refused) | [ ] |
| RW-6 The editor's import stops writing own-object routes and thumbnail locators into registry entries | N | — | astrid-app import writer (path found at dispatch) | The app's import test; an old entry still opens | [ ] |
| RW-13 Read-only audit of the film: for each word-anchored shot clip, authored start against resolved word plus offset; list disagreements | N | film render finished | none (script in scratch) | The list itself, checked by the main session | [ ] |
| **Phase 1 (b): safety net** | | | | | |
| RW-7 Render journey: fixture and test (specification below) | X | — | new `tests/journeys/test_render_journey.py`, `tests/fixtures/render_journey/` | Runs by dispatch; reports first failing stage on both heads; each negative case fails as named | [ ] |
| RW-8 Journey wired into CI: path-filtered job on pull requests into `release/*/main`, both profiles on push in `lanes.yml` | N | RW-1, RW-2, RW-3, RW-7, D7 | `.github/workflows/ci.yml`, `lanes.yml` | One green run per profile on each release head | [ ] |
| RW-9 Every command the CLI prints as a hint parses under its own parser | N | — | new test; hint strings where found | Fails today on `media open … --to` | [ ] |
| **Phase 2 (c): agent-facing quality** | | | | | |
| RW-10 The Runtime logs any request that waited or held the store mutex over 1 s; a lease-loss message carries the last acknowledged heartbeat | X | — | astrid-runtime `runtime_protocol/server.py:_dispatch`; Agent `generic_host.py` lease diagnostic | Unit test of the log line; one loaded render with the log attached | [ ] |
| RW-11 Heartbeat no longer queues behind long store sections; first heartbeat is sent at claim; lease length declared once in the Runtime and carried by the generated client | S | RW-10, D3 | astrid-runtime `store.py:heartbeat_task`, claim path, client generator; Agent pin regeneration | New Runtime test: a 40 s store section does not expire a live lease; a dead worker's lease still expires; `test_lease_publication_journey.py` | [ ] |
| RW-12 A failed, cancelled or lease-lost attempt reclaims its scratch; an admission refusal for disk names reclaimable scratch and the command | X | — | execution host attempt clean-up; admission message | Kill a render mid-run; scratch under 100 MB; next admission passes | [ ] |
| RW-14 The identity refusal says which case it is: source changed since start, caller without an install stamp, or a truly older Astrid | N | — | astrid-runtime `astrid_runtime/identity.py`, `runtime_protocol/startup_identity.py` | Three cases, three messages | [ ] |
| RW-15 Render failure shows the first real error first; cancel reports the task's true state; a timeout is not reported as an install fault | N | — | render error assembly; `tasks cancel`; identity retry message | Golden text for the `probe3` failure; cancel on a failed task | [ ] |
| RW-15T Wording pass on the messages from RW-2, RW-12, RW-14, RW-15 | T | those four | message strings only | Read aloud against the owner's error-headline rule | [ ] |
| RW-16 `tasks follow` shows frames rendered and total | N | — | follow printer; existing progress relay | A 3 s render prints at least two progress lines | [ ] |
| RW-17 `timelines revert --to <revision>` restores a whole timeline to an earlier revision, if the Runtime's restore route supports it | X | — | Agent CLI and SDK; reads Runtime restore route | Edit, revert, read back equal | [ ] |
| **Phase 3 (d): write path, small fixes** | | | | | |
| RW-18 `clip.delete` refuses only when a declaration names the selected clip | N | — | `sdk/timeline/_delete_commands.py` | The two sandbox probes in `edits/` as tests | [ ] |
| RW-19 An oversized request is refused before a flight is saved, with the limit; retry advice keeps the dry-run mode; a dry-run flight can be abandoned | X | — | `sdk/timeline/sync.py`, `commit_session.py`, `_commit_wording.py` | `oversize_dryrun.py` repro as a test | [ ] |
| RW-20 Item-scoped `list.remove` is accepted by the Runtime, with one case table both sides run | X | — | Agent `_doc_patch.py`; astrid-runtime `timeline_commit_auth.py` | `list-observation-repro.py` as a shared case | [ ] |
| RW-21 Dry-run diff no longer raises `KeyError: '_runtime_document'` | N | — | SDK preview hydration | The `tlfix` repro | [ ] |
| RW-22 A dry-run flight never blocks; a flight carries its session; another session does not replay it | X | D6 | `sdk/timeline/sync.py` | Two sessions, one outbox: neither replays the other | [ ] |
| R Review rounds (at most 2, at the end of phase 1 and again before phase 3 lands) | S | all other tasks in the phase | read-only | Findings become rows `R<round>.<n>` | [ ] |

### RW-7: the render journey

**Timeline fixture** (3 s, 30 fps, 480×270, about 200 KB of media):

- A built-in element from the in-tree rendering pack.
- An element from a collection pack installed in the personal collection by the real install route (the pinned motion pack's `am-burst`).
- A project-pack element, admitted with the real `project-pack admit`. Skipped on a line without Plan 69, and reported as skipped by name.
- A shot holding two word-anchored clips against a 3 s narration with word times, one clip per second.
- An image and a short video imported during the test with the real import command, placed on a shot clip by `--swap-asset`.
- One registry entry written the way the editor writes it (own-object route, `thumbnailUrl`), unused by any clip.
- Each element paints a known flat colour in its own corner.

**Steps:** start a real stack (installed: build the wheel and run the installer into a temporary root; source: the source launcher); create a project; import; admit; build the timeline through SDK commits, including the swap and a ripple retime of the narration; `timelines render --wait` through a command worker.

**Asserts:**

- Exit 0, and a Runtime receipt with an output object.
- `ffprobe`: 90 frames, 480×270, an audio stream.
- At 0.5 s, 1.5 s and 2.5 s, each expected corner has its colour (a missing element fails by name).
- The moved word-anchored clip starts at its resolved word plus offset.
- At least one heartbeat was acknowledged.
- Nothing remains in the attempt's scratch.

**Negative cases, each expected to fail with a message naming the cause:** a foreign locator in a registry entry; a pack root changed after launch; a word-anchored clip moved without its narration; a worker killed mid-render, after which a second render is admitted.

**Where it runs:** Linux on pull requests that touch `astrid/core/rendering/**`, `astrid/core/execution/**`, `astrid/core/pack/**`, `astrid/packs/rendering/**`, `remotion/**` or `runtime.lock.json`; Linux and macOS, both profiles, on every push to `release/*/main`.

**What it would have caught:** the own-object route and thumbnail refusals; the native-for-command readiness rule; the empty pack path; the dependency-path and pack-root mismatches; the unresolved motion-pack alias; the relative shared import; #1403 and #1404 at the build step. It would not have caught the lease loss, which needs load; RW-11's test covers that.

---

# Part 3 — inputs.md

## Planning evidence

**Scope decision:** Pending — the owner has not chosen. Next: the owner reads D1 to D7.

**Prior art:** Seven commits and six stopgap areas on `release/14/r6-fixes` (base `83d5f8fe`); PRs astrid-agent #525, #526, #530; the Astra review and the merge analysis; Plans 39, 59, 63, 69, 75 to 78 and 18 on astrid-dev `main` `91230134`. Existing tests `test_generic_host_remotion_render.py` and `test_pinned_element_render_proof.py` exercise a render but not a collection pack through a command worker on an install [I: from names and tonight's failures; not read in full]. Negative finding: no issue covers lease loss, render scratch or the `--to` hint.

**Approach:** Reuse five commits and two stopgaps; replace four changes; add one journey. No new pack, no new mechanism: pack roots reuse `ASTRID_RENDER_PACK_ROOTS`; the lease reuses the Runtime's existing `lease_seconds`.

**Challenge:** Pending — this plan crosses a repository contract and exceeds five days, so an advisor critique of the written plan is required before greenlight. Done so far: the Astra review of the committed code and the merge analysis, both weighed in DECISIONS.md. Next: one fresh critique briefed to remove tasks.

**Proof and limits:** In Completion. Limits: no test was run for this draft; lease cause unmeasured; installed-profile cause unknown.

**Review rounds:** Recommended 2, at the end of each phase, no review stops. RW-5 and RW-11 are routed S because a mistake there damages data or strands work. The owner confirms.

**Run start:** Pending — no run is authorised.

## Owner decisions

- **D1 Target.** (a) Render-path fixes to 14 and forward, Plan 69-based fixes to 15; (b) everything to 15. Recommend (a), unless the Release 14 Lead says 14 is closed.
- **D2 Word-anchored retime.** (a) Ship the exemption as written; (b) allow only when the offset from the resolved word is unchanged, else refuse and name the cut-relative form; (c) refuse all until binding exists. Recommend (b).
- **D3 Lease.** (a) Ship 600 s; (b) measure, then move the heartbeat off the starved path and declare the lease once; (c) as (b), with a declared 120 s lease at claim and heartbeat meanwhile. Recommend (b); (c) only if RW-10 shows the fix is more than a week away.
- **D4 Launch-context check.** (a) Keep as is with more normalisations; (b) keep the checks on effects, build the environment in one place, print path values; (c) remove the check. Recommend (b).
- **D5 Pack roots.** The generated registry is the one owner and the bundler reads its list. Recommend yes.
- **D6 Outbox interim** (with Plan 76's manager). Dry-run flights never block and sessions do not replay each other's flights, ahead of Plan 76. Recommend yes.
- **D7 Process.** File this as Plan 84 in Release 15 with 14 fix branches; file issues N1 to N5; add the journey to the `release/*/main` ruleset once green. The ruleset is the owner's to set.

## Source identities

- astrid-agent `release/14/main` `c0ad6b54`, `release/15/main` `8807f820`, stack base `83d5f8fe`, fix branch head `ad10ff6de` [P: mergescope].
- astrid-runtime `release/14/main` `5120462d`, `release/15/main` `23310dc8`, stack pin `b2ea261` [P: branches report].
- astrid-app `release/14/main` `e0da794a`, `release/15/main` `c5ba8cd9` [P].
- Destinations: `release/<NN>/<topic>` fix branches cut from each release head at dispatch.

## References

- Evidence root: `~/` — `review/ASTRA-530.md`, `mergescope/REPORT.md`, `edits/DEFECTS.md`, `occ/bug-evidence-pack.md`, `render/REPORT.md`, `render/BLOCKER-TRACE.md`, `packtimeout/REPORT.md`, `tooling/ISSUES.md`, `take/*.log`.
- Issues to file: **N1** bundler cannot resolve collection-pack elements; **N2** no end-to-end render check; **N3** lease lost under load; **N4** failed renders leave scratch that blocks admission; **N5** printed export hint is rejected.
