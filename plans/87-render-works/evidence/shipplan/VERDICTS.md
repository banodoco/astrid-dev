# Verdicts: seven commits and the stopgaps

22 November 2026. Read-only judgement: no tests, builds or installs were run, nothing was pushed or posted.

Source labels: **[V]** I read the code or log myself; **[P]** reported by another agent's write-up, not re-checked; **[I]** my inference.

Paths are in `~/Developer/astrid-release-src/wt-r14-r6-fixes` (Agent, base `83d5f8fe`, with the uncommitted stopgaps applied, so line numbers include them) and `~/Developer/astrid-release-src/wt/runtime-src` (Runtime `b2ea261`).

## Summary table

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

Nothing here is ready to merge from the stack branch. Every item is rebuilt on an issue-scoped branch from the release head (see PLAN.md).

## The seven commits

### 1 and 2. `7bf7d9086` + `cb90a4b99`: registry projection. Ship after additions.

- The fix is right in kind. The Runtime's render admission already drops an entry's own `/v1/objects/<id>` route as redundant; the Agent's managed check refused it, so one such entry, used or not, failed the whole timeline [V: commit message; P: `assets.py:66`, `managed_timeline.py:648`].
- I agree with the Astra review (no bypass; foreign routes still refused).
- Additions:
  1. The refusal's recovery advice says to replace the asset on the clips that use it; an unused bad entry still fails [P: Astra]. Make the message name the entry and say so.
  2. A test that an unused entry with a foreign locator is still refused, and one for rollback when admission fails.
  3. The editor still writes these fields on import. That is a separate App fix; without it the Agent keeps cleaning up after the writer.
- Trial cherry-pick is clean on both release branches [P: mergescope]. It replaces PR #525.

### 3. `7332e03d6`: name the differing fields. Ship after additions.

- Sound, and it is what made tonight's diagnosis possible at all [V: `probe1.log` names `registry_context.ASTRID_PACKS_PATH`].
- It conflicts on both targets, which already carry a different version of the same message [P: mergescope]. Reconcile; do not replace blindly.
- Addition: names were not enough. The main session still had to write a debug dump (S3) to see the two values. For the path-list fields (`ASTRID_PACKS_PATH`, `PYTHONPATH`, project directory) print expected and actual; they are paths, not secrets. Keep every other field name-only.

### 4. `0f6aea928`: launch validation matches worker contexts. Ship after additions.

- Correct for what it covers: the launch probe now uses the same dependency helper as the worker, and receives the host's expanded pack roots instead of the raw command-line roots [V: diff at `generic_host.py:1595`, `:2194`, `:18563`].
- It fixes two drifts between two hand-kept derivations of one fact, and S1 and S2 fix two more. That is the real defect (see PLAN.md, structural cause 2). Shipping four point fixes without removing the duplication invites a fifth.
- Additions:
  1. One function builds a worker's environment, and both the launch probe and the dispatch call it.
  2. A parity test through the real dispatch path for every Remotion-capable capability and both worker kinds. The current tests rebuild the expected path by hand [P: Astra], and S8 inspects the syntax tree of the call site [V].
- It does **not** establish why the *installed* stack failed the same check at 17:31 [V: `render/REPORT.md`, field unknown; P: Astra]. Only the render journey on an installed build will show that.

### 5. `24740fdf4`: media swap keeps shot clips. Ship after additions, Release 15 only.

- Direction is sound: guards on media kind, identity and occupied aliases; the Runtime re-verifies [P: Astra; P: 146 focused tests passed, `occ/bug-evidence-pack.md`].
- It cannot go to `release/14/main` as written: it builds on the word-signature baseline that only Plan 69's commits introduced [P: mergescope trial conflict]. Plan 69 is a Release 15 plan [V: astrid-dev `plans/69-project-elements/plan.md`].
- Additions: a live word-anchored swap was never shown (the sandbox clip had literal timing) [P]; the render journey must do one. Say in the PR that a rejected swap can leave imported objects in the project.
- It replaces PR #526.

### 6. `ad10ff6de`: unchanged legacy overrun. Ship after additions and a review, Release 15 only.

- No independent reviewer has read it; Astra's review stopped one commit earlier.
- My read [V]: the helper is narrow. Every field but `at`/`at_ms` must be equal, the asset entry must be equal, and the overrun may not grow.
- It also changes something its title does not say: `previous_bound` now comes from the baseline placement even when the occurrence's duration changed (`validation.py:844-852`). Before, a changed duration re-checked every clip; now a *grown* occurrence no longer re-checks untouched clips. I think that is correct, but it is a behaviour change and needs its own test.
- Additions: tests for a grown bound, a shrunk bound with an untouched clip, and a speed or source-window change; one reviewer pass.

### 7. `d4bf28e4d`: word-provenance exemption. Replace.

- What it does [V: diff]: a second signature leaves out `at`, `at_ms`, `hold` and `duration`, so a shot clip that declares `on: "word"` keeps its legacy exemption when only its interval changes.
- Why that is wrong: nothing proves the narration moved by the same amount. The clip is left with two statements of its time that disagree: the declaration and the interval. Validation suppresses the declaration; reflow resolves it again and can move the clip back [P: Astra, `_timing_evaluators.py:545`, `reflow.py:394`]. So the edit is neither proven nor durable. The tests use a word that cannot be resolved, so they miss this [P: Astra].
- I agree with Astra and the merge analysis that it must not merge as is. I disagree with both on the size of the replacement. They ask for full occurrence-owned binding capture (target and source identities, transcript digest, word ids, migration). That is the right end state, but it is Plan 18 phase A's design work, not a fix.
- The replacement that is safe and small:
  1. Keep the second signature, but grant it only when the word resolves in both baseline and candidate and the clip's offset from the resolved word is unchanged within one frame. That is the ripple case, and it *is* the proof that the narration moved.
  2. Otherwise refuse, and name the supported move: make the clip cut-relative (`on: '+3.13s'`), which already works [P: `edits/DEFECTS.md` §10].
  3. Add the missing regression: a resolvable word, move, then reflow.
- Until that lands, the exemption stays only on the film's stack. The film's ripple tonight went through it unaudited (PLAN.md task RW-13).

## The stopgaps

### S1. `readiness_worker_kind="command"`: ship as is.
A command-dispatched worker was checked under the native rule [V: `generic_host.py:10708`]. One line, plainly correct. Keep the first test in `test_captured_render_readiness.py`.

### S2. Empty pack path treated as unset: ship after additions.
- The empty value is deliberate: a task's selected-pack environment writes `ASTRID_PACKS_PATH` as the collections of the capability's own packs, which is empty for a built-in capability, and present-but-empty stops the child inheriting the parent's value [V: `core/pack/imports.py:169-176`].
- Discovery reads it with `.get(..., "")` and skips empty entries, so empty and unset select the same packs [V: `core/pack/discovery.py:124`, `:355`, `:458`]. The merge analysis asks for this to be demonstrated first; the code shows it.
- Additions: move the rule into `_normalize_registry_selectors`, where the other equivalences live (`remotion_runtime.py:585-617`), and test it there.

### S3. `R6-DEBUG`: drop.
It writes the environment to a predictable file in `/private/tmp` and swallows errors [V: `remotion_runtime.py:1279-1284`]. Its useful part becomes the path-field values in item 3.

### S4, S5, S6. Pack roots for the worker and the bundler: replace all three with one fix.

- Today five things each answer "which packs does this render see" [V]:
  1. The host's `pack_roots`: configured roots plus the personal collection (`generic_host.py:6732-6741`).
  2. The task's selected-pack environment: only the capability's packs (`imports.py:157-176`).
  3. Python discovery in the worker, which finds the personal collection by its own default root (`personal_packs_root.py:13-29`).
  4. The bundler, which scans in-tree packs and `ASTRID_PACKS_PATH` (`webpack-alias.mjs:162-166`).
  5. `ASTRID_RENDER_PACK_ROOTS`, an explicit JSON list already used for project packs (`webpack-alias.mjs:167-170`).
- Python (3) generated imports for the motion pack; the bundler (4) could not resolve them [V: `probe3.log`, `probe5.log`].
- S4 widens the worker's discovery in source mode only. Installed mode refuses any explicit pack root (`remotion_runtime.py:545`), so the two profiles now behave differently. S5 patches the bundler's environment through a side door. Both are expedient.
- **The one owner should be the generated registry.** The Python step that writes `effects.generated.ts` knows exactly which packs it emitted imports for. It writes that list (pack id, root, kinds) beside the registry; the render passes it to the bundler through the existing `ASTRID_RENDER_PACK_ROOTS` channel; the bundler stops scanning `ASTRID_PACKS_PATH`. Then what is imported and what can be resolved cannot disagree, in either profile.
- S6: the motion pack's elements import `../../../../rendering/shared/element_contracts`, a path that exists only when the pack sits in the product tree [V: `probe6.log`; four imports in the pack, two spellings]. A global alias on two relative spellings can rewrite an unrelated import that happens to use the same string. Replace with a named import (`@astrid/rendering-shared`) provided by the bundler and by the project-element compiler, and change the pack's four imports. I agree with the merge analysis here.
- [I] Because the motion pack lives in the personal collection on an install, and installed mode forbids `ASTRID_PACKS_PATH`, I expect every installed render to fail at bundling today. Not verified; the render journey will show it.

### S7. Lease 600 s: replace.

- What the stopgap does [V: `generic_host.py:5684-5694`, `generated.py:1343-1345`]: every heartbeat, for every task kind, asks for a 600 s lease, with a 20 s timeout, through a hand edit to a file the Runtime generates.
- Why it is wrong:
  1. The first claim still gets 30 s (`store.py:4434`), and one earlier attempt lost its lease *before any heartbeat* [P: `fixed/LOG.md` 19:05]. The stopgap would not have saved it.
  2. A lease also holds the task's reservations (`store.py:6272`). A crashed render would keep its disk reservation for ten minutes, on a machine where 6.9 GB of scratch already blocked the next admission [V: `almost-ready-v38-full-2.log`].
  3. The hand edit breaks the vendored-client boundary check [P: mergescope].
- Is a longer lease the right fix at all? No. Losing a 30 s lease with a 5 s beat and a 2 s timeout means the Runtime did not answer a small request for about 25 s. That blackout is the defect.
- What I could establish [V]:
  - Every request except binary transfer and timeline commit runs under one store mutex (`server.py:1574-1576`), and the heartbeat takes it again and reaps overdue leases each time (`store.py:6255-6256`).
  - Object reads take the mutex only briefly and hash outside it (`service.py:6116-6133`), so "serving the film's inputs" is not obviously the holder.
  - The Runtime has no access log (`server.py:209`), so nobody can say what held it.
  - The same afternoon the installed stack logged 487 `transport_timeout` lines [P: `packtimeout/REPORT.md`]. Starvation is chronic, not special to this render.
- What I could not establish: who held the mutex, or whether the host's own heartbeat lock, which admission shares (`generic_host.py:5456`), was the blocker. [I] A candidate is admission hashing every media pin inside a store method (`store.py:2346-2353`), which repeats after each Runtime restart; tonight's script restarted before each probe.
- The proper fix, in order:
  1. Measure: a slow-request line in the Runtime (route, wait for the mutex, time held) and the last acknowledged heartbeat in the failure message.
  2. Take the heartbeat off the starved path, in the Runtime and, if the measurement says so, in the host.
  3. Declare the lease once, in the Runtime, and have the client generator carry it.
- I agree with the merge analysis ("redo first") and add the point about the first claim and the reservations.

### S8. Stopgap tests.
- Keep `test_command_dispatch_uses_command_readiness`.
- Replace the syntax-tree assertion in `test_remotion_host_regressions.py` with the parity test from item 4. A test that inspects the argument name at a call site proves nothing about behaviour.

## Not code, but found tonight and unfixed

| Finding | Evidence | Lands in |
|---|---|---|
| Failed attempts leave scratch that blocks the next admission ("needs 6.90 GB plus 2.15 GB free-space reserve; 7.74 GB free") | [V] `take/almost-ready-v38-full-2.log` | PR-H, not filed |
| "lease expired with unresolved custody; reconciliation required"; cancel returns ok but the task stays failed | [V] `take/almost-ready-v38-full.log`; [P] `tighten/FRICTION.md` | PR-D and PR-H, not filed |
| "An older Astrid is still running" after any source edit, and for an unstamped caller | [P] `edits/DEFECTS.md` §8, `fixed/FRICTION.md` | PR-H, #1398 |
| The export hint `media open … --to FILE` is rejected | Main session's account only; in no log | PR-H, not filed |
| The render failure text opens with an esbuild warning about `import.meta`, above the real "Module not found" | [V] `probe3.log` | PR-H, #1397 |
