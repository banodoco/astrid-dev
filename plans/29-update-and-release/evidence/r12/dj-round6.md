# Direct Journey round 6 evidence (App e1d42be39)

[Handoff](../../handoff.md) · [Tasks](../../tasks.md)

# Direct Journey release 12 — round 6

2026-11-10. Supplied CI run **42849600626**; App `cand/29-r12` at `e1d42be3974700d585d461df27469b63811fe544`, initially clean. Agent `313bbd46f1e24bfe635655d78b27ab0b321145d5`, Runtime `42ae24aff8d2cb854f874ce134161077a3ba3641`, matching `public/install-manifest.json` and the trace's source tuple. Candidate: uncommitted edits in `app/`. Both prior evidence packs were read before investigation. CI evidence was parsed as JSON/text only; nothing from `ev/` was executed.

## 1. Installed pack live effect — environment

Evidence: `ev/direct-journey-traces/direct-journey-pack-extens-59f7c-update-keeps-the-old-effect/trace/test.trace:20` throws at `packsCli`, source line 1047, before any pack install, fixture generation or browser assertion. No workflow supplied its mandatory `ASTRID_PACKS_AGENT`.

The existing workflow reads the Agent SHA from the App manifest, checks out that sibling tree, creates `astrid-agent/.venv`, installs the Agent editable there and installs the pinned sibling Runtime into that environment. `support/astrid.ts:18` uses that checkout and `ASTRID_PYTHON` for the other journeys. `support/harness.ts:759` also puts those same source trees on Runtime's Python path and sets its HOME to the isolated Agent home. Therefore the correct pack executable is **`${{ github.workspace }}/astrid-agent/.venv/bin/astrid`**.

Fix: `app/.github/workflows/direct-journey.yml:121` verifies that console script is executable after installation; line 140 supplies `ASTRID_PACKS_AGENT` to the direct journey. The existing explicit ref override remains supported; absent an override, this is exactly the manifest's pinned Agent, not a global runner binary.

Fixture audit: `direct-journey.spec.ts:1031,1091` uses checked-in `tests/e2e/fixtures/packs/live-effect/v1` and `v2-broken`, constructing a temporary local Git repository and two real commits. `liveEffectToolchain` uses the workflow's Node, the App lockfile's esbuild 0.27.7, and the hosted build's `dist/extension-shared-modules.json`. `playwright.direct.config.ts` invokes `global-setup.ts`, which builds the hosted App before the tests. Ubuntu's Git, the existing Node/npm setup and App install provide those tools. There is no remote pack URL or additional pack download required. Both CLI and Runtime use `harness.agentHome`, so installation and Runtime inventory share the same isolated packs root.

Pinned-source confirmation after resume: the orchestrator supplied clean `agent/` at the exact manifest SHA. `agent/pyproject.toml:66` declares `astrid = "astrid.console:main"`; `agent/astrid/console.py:22` directly routes `packs` to the pack CLI. PyYAML/jsonschema and other pack validation dependencies are core dependencies, not extras. `core/pack/cli_manage.py:305` derives the browser build inputs and uses the explicit toolchain; `pack_build.py:93` authenticates Node, esbuild and its API and runs the local builder. `core/pack/install.py:277` explicitly permits local Git file transport. The fixture declares no package requirements or pack dependencies. No additional install extra or network source is needed. `pack_api.py:13` confirms fixture API 2.3 matches the pinned Agent.

Strength: the mandatory missing-variable error stays unchanged. Passive-open security, actual install/build/admission, live rendering without reload, broken-update refusal with old-effect preservation, and removal/disposal assertions are unchanged. No skip or timeout change.

## 2. Concurrent edit — test drift

Evidence: `ev/three-products-traces/three-products-concurrent--81b8f-onflict-and-keeps-its-draft/trace/test.trace`:

- `:626`: full retained draft equality after Keep passes (source :581).
- `:804–813`: Save them opens the named conflict; complete retained slot equality and no additional POST pass (source :602–605).
- `:862–873`: explicit Use latest deletes the slot and creates no extra publication.
- `:1000–1069`: final reload shows canonical label/transition, reads B's revision, and the real Agent's status reports B.
- `:1072–1074`: only then does `shown.head_revision_id` fail, receiving `undefined` instead of B (`authoring-parent-revision-4495aed2…5b4a8`).

This is not another failure of `restoreRetainedConflict`: the new branch, resolution and durability checks all pass. The test's hand-written `show` type describes the old cut-table projection. At the pinned Agent, `astrid/packs/timeline/cli.py:1067` sends JSON show to `open_composition`; `astrid/sdk/remote.py:1227` builds the actual native projection. Its revision and head are **`summary.revision_id` / `summary.head_revision_id`**, not top-level fields; it has a flat **`clips`** array, not `rows[].layers`. Each clip preserves the native **`asset_id`** and `authored_fields` rather than the old cut-table `asset`. `remote.py:1317` also exposes pagination. The source's cut-table JSON path is a different projection and must not be substituted for this native read.

Fix: `app/tests/e2e/local/three-products.spec.ts:288,323` declares/reads the verified native projection. Lines 633–641 check revision and current head against the same independently known B, require currentness and complete paging, find exactly one occurrence-scoped clear clip, require its asset_id to be null, and compare its complete authored fields to B's stored clip. The shared helper's restart and QUICK callers use `summary.revision_id` at lines 725 and 3489. `expectAgentRevision` at line 1467 had the same misplaced top-level field and is corrected centrally for its skipped gesture callers. No fallback to status or expected values and no alternate-shape acceptance. The real published CLI read, exact head equality and media-clear assertion retain their strength; occurrence identity and complete authored readback checks are added. Rounds 4 and 5 product changes and unit regressions are untouched.

## 3. Native None bulk — test drift / harness deadlock

Evidence bases: `ev/three-products-traces/three-products-M2-native-N-4956c-ict-retains-the-whole-draft/` and its `-retry1` counterpart.

Both attempts pass the round 5 five-read assertion, the complete intermediate derived-mirror equality and final mirror equality (`trace/test.trace:354,363,365`, source :2867,2887,2888). The expected history sequence is no longer the failure.

Both `trace/0-trace.network` files show `/commit` at lines **127, 140, 1404**: a successful server fetch (200), the original browser request whose ACK is deliberately lost, then an automatic browser retry held by the fault route until teardown. All three carry exactly the same body resource hash and idempotency key. The original body matches the durable pending request byte for byte. `trace/0-trace.trace:616` (first attempt) and `:612` (retry1) return that intact one-intent owner with outcome `retry`, error `unknown / Failed to fetch`.

`faultFirstCommit.loseAck()` explicitly waits for the automatic retry to be staged. But source :3023 then clicks the removed `timeline-command-retry` / Retry save control instead of releasing that staged route. `trace/test.trace:408` begins this locator wait on both attempts; it ends only when the 300-second test ceiling closes the page. The teardown's `abortStagedRetry` stack further confirms a request was held. Source `useTimelineSave.ts:382` automatically recovers the single native owner; `localSaveSession.ts` sends its original durable request. There is no product transport hang.

Fix: `app/tests/e2e/local/three-products.spec.ts:3037–3051` observes the exact two original/retry identities and only one forwarded acceptance, then calls the existing `releaseStagedRetry()`. Complete POST equality still requires identical method, path, body, key, status, receipt and canonical closure. Additional complete history and revision-list equality prove this replay creates neither a publication nor a revision. Outbox-drained, restart/reload, opaque data and inverse assertions remain.

The previously unreachable recovery tail used the same removed command recovery UI. Lines 3112–3141 now exercise automatic owner recovery, the existing unsaved-changes banner's **Save them**, and the named conflict dialog. Exact retained pending request and intent equality remain across reload and conflict reopening; full durable slot equality and complete revision-list equality were added. Both original clear edits are checked in the retained intent's entire canonical parent, including opaque values. The mounted display is checked separately against the actual Agent publication: its first transition is None and its second remains crossfade. `localSaveSession.rollback` intentionally adopts that canonical image while retaining the entire rejected chain. Showing both unsaved clears as canonical would contradict that product contract. The round 5 mounted unit regression also explicitly requires canonical display after recovery/reopening while the full original draft survives.

Strength: no history normalization, ignored reads/writes, new timeout, skip, retry-key regeneration, rebase or shortened conflict coverage. The original atomic intent, unknown revision, literal `__proto__` data, exact replay, undo, original conflict guards, full rejected request, restart and durability requirements remain. Product code is unchanged because evidence supports test/environment defects.

## The 11 skipped three-products cases

Names and source lines below refer to the supplied report / starting head, so they remain usable after this patch shifts lines.

| Skipped case | Exposure to these causes |
| --- | --- |
| Runtime restart with the App open (:635) | Shared Agent show field (fixed centrally); also still waits for removed Recover saved edits. |
| M1 real gesture (:1508) | Shared expectAgentRevision field (fixed centrally); still uses removed explicit Recover saved edits after lost ACK/reopen. |
| M2 real gate 5, M1 mounted path (:1621) | Shared expectAgentRevision field (fixed centrally). Same automatic retry mechanism, but already stages/releases it; no identical stale selector found. |
| M2 ordinary extension batch (:1838) | Still uses removed Recover saved edits after lost ACK/restart. |
| M2 real mounted manual video drop (:2009) | Still uses removed Recover saved edits after lost ACK/reopen. |
| M2 real gate 5 bootstrap actual consumer (:2241) | Still uses removed Recover saved edits after lost ACK/restart. |
| M1 real dependency conflict (:2424) | Exact same removed Retry save deadlock, plus removed recovery button and recovery notice in its later conflict tail. |
| M2 native occurrence duplicate (:2487) | Still uses removed Recover saved edits after lost ACK/restart. |
| M2 mixed editing (:2669) | Shared expectAgentRevision field (fixed centrally); still uses removed Recover saved edits after lost ACK/reload. |
| Render R, publish R+1 (:3176) | No demonstrated same cause: does not call show or the native retry/recovery controls. |
| Empty bootstrap (:3475) | No demonstrated same cause: no Agent show or these retry controls. |

The eight cases with obsolete controls are identified, not claimed replayed or repaired. Their other representation assertions may also need the earlier rounds' documentIntent audit when reached. No skipped three-products case installs packs through `packsCli`, so none shares the missing pack executable environment variable.

## Validation, candidate and handoff

Resume audit: no `run.yaml` or `tasks.md` exists in the supplied working tree; both mailboxes, the evidence pack, App branch/worktree/head and complete diff were read before continuing. App remains on its original head with only the intended two modified files. The newly supplied Agent is clean at its exact pin, was read as a source donor only, and remains unchanged. The provisional top-level `revision_id` edit was corrected to the fully verified nested native shape before handoff.

- PASS: `python3 round6-audit.py` checks the successful concurrent recovery/resolution events, exact failure location, successful None history checks on both attempts, identical request bytes/key, intact retry owner and missing Agent environment precondition. This is a read-only evidence audit, not patched product execution.
- PASS: `python3 -c 'import yaml,sys; yaml.safe_load(open(sys.argv[1]))' app/.github/workflows/direct-journey.yml`.
- PASS: `git -C app diff --check`.
- NO-RESULT: TypeScript, Vitest, Playwright. `node_modules` is absent and installation/test execution is forbidden here. CI must execute the three named selectors and the None conflict tail. No live reproduction or green candidate runtime result is claimed.
- No product change, so no new product unit regression is appropriate. Existing round 4/5 regression remains intact.
- Workspace approximately 765 MB including the supplied Agent donor, below 2 GB. No git mutation/commit, dependency install, pods, credentials, publication or live workspace changes.

Exact candidate: `git -C app diff --binary | sha256sum` = `5663995eeb5e1f3f6ac75c0764603c34f5cfa65025f4c42fbee3f69aebac7a30` on the App head named above. Changes remain uncommitted.

Apply the uncommitted candidate and replay the named journeys in the pinned CI environment. Rollback is reverting these focused workflow/test hunks; no durable user data was altered here. This pack is the local incident draft/handoff; no issue or PR was published.

Routes used: Unknown — no run manifest or independent model provenance was supplied for this scoped repair.
