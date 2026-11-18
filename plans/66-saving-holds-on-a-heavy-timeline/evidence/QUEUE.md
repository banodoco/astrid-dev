# Main-thread queue (18 Nov 2026)

0a. **Fable's design** (`fable-save-category-design.md`) was **accepted by the main thread**: one home, four outcomes, refusals leave the queue, signed checks, an edit costs the change.
   - **Main-thread change:** N10 (health off the mutex) and N11 (timing logs) are promoted into the "now" set, because slow saves were the owner's first complaint.
   - **Builds:**
     - App #299 `release/14/save-recovery` (Sonnet): N3, N4, N7, N8, N9, N12;
     - Runtime #61 `release/14/selection-digest`: N1, with a one-format check;
     - Runtime `release/14/transport` (Sonnet): N5, N10, N11;
     - App `release/14/app-transport` (Haiku): N6, plus the N11 proxy log.
   - **Then:**
     1. Merge into the plan-59 branches.
     2. **Bump the Agent's Runtime pin** with `regenerate_runtime_pins.py`.
     3. Rebuild :2400.
     4. Browser test: a drop; a second drop during a save; stop and start the Runtime during a save; a reload during each; Discard. Record the commit timing line and `netstat -m`.
     5. Then live.
   - **The r14 profile** (`sonnet-commit-profile-r14.md`) measured what Fable had inferred (1–2 s).
     - A commit takes about 9 s, and 67% is `_legacy_exemptions` → `_reference_basis` (`:74`): 400 calls and 25.6M deepcopies. Being fixed on agent `release/14/legacy-basis`.
     - An import during a commit waits 5–7 s on `store._mutex` while the commit is in the ancestry walk (`timeline_commit_store.py:196/1172/853`). Being fixed on runtime `release/14/ancestry`, with the walk memoised and the mutex held only for reads.
     - History is flat at short lengths.
   - **Build status (main thread):**
     - **Merged:** runtime #62 (`1af7ed60`); app #300 (`48202a7a`).
     - **Merging:** app #299 (`c0750f500`: N3, N4, N7, N8, N9, N12, 18 table tests); agent #400 into `release/14/main`, then main into plan-59.
     - **#61:** the retained reader keeps the old digest behind `retained=True` (history re-checks it). The v33 "affected" test is being re-seeded with an identity change, plus a new metadata-only pin that stays verified (main-thread decision).
     - **Runtime transport** (N5, N10, N11): PR pending.
     - **Then:** merge #61 and transport into runtime plan-59 → **Agent pin bump** → rebuild :2400 → browser test. Run the Opus review alongside.
   - **Owner, 18 Nov:** "SORRY, FOR RELEASE 14 I MEANT" was about pushing current work to `release/14/main`. Then: **"DONT DO THE STABILITZ ONE, JUST ADD IT TO ASTRID-DEV"**.
     - **Plan 63 "Dependable saving"** is astrid-dev PR #880 (queued, in no release; CC-5 split into a/b). It's held until the fresh Fable check (`fable-dependable-saving-check.md`) comes back.
       - **Fable check: proceed lean (about 30 days), accepted by the main thread.**
         - **Cuts:** CC-10 becomes in-memory retry; CC-9 becomes 2 tests; the CC-8 ratchets go; CC-4 covers routes only; D15 becomes park-plus-two-buttons.
         - **Additions:** an old-Runtime decoder fallback, browser migration, the other outbox users, a two-tab rule, the import-lock re-measure, I-3 covered by R14 save-recovery-2, and immutability triggers.
         - **Plan 18 shaping:** an opaque payload, the `register_rule` prefix and purity, and the stale `retryable` wording fixed.
         - Being applied to #880. The agent-edits question has gone to the same Fable (`fable-agent-edits.md`).
       - **Then (owner):** consider the check, and ask Fable how it works with **agent edits**, meaning timelines edited by agents through the Agent's CLI, pack actions and bundles, as with Almost Ready. Is there one clear and consistent approach for editor edits and agent edits?
       - Fold the results into #880 before merging it.
     - **Opus review** (`opus-r14-save-fixes-review.md`): four must-fix findings.
       - **App 1, 2, 3, plus 5 to 10:** being fixed on `release/14/save-recovery-2` (Sonnet). The edit during replay **awaits** the replay instead of throwing. A drop places onto the current document.
       - **Runtime 4:** #65 `release/14/commit-hook`, with the hook moved to the service store. The authorizer/tag recheck bounding was **rejected by the main thread** as resting on an unproven invariant plus the re-prepare cost; it's being reverted, keeping a "no more than the re-walk" count.
       - **#65 HELD:** at 30 entries, a head-only re-read after an absorbed write costs 217 statements against 179 discarded, so #62's per-write recheck may be net-negative on long histories.
         - The profiler is measuring A (absorb) against B (discard) on a real realm clone.
         - If discard wins, revert #62's retention and keep the immutability triggers as the Plan 63 answer. If absorb wins, merge #65.
       - **Agent 12:** #402 (oracle frozen; 33 cases identical against `84c2f5247`), ready to merge.
       - **Plan 63 input:** accepted-history immutability enforced by SQLite triggers, so proofs need no per-write recheck.
       - **After these land:** pin bump plus an `astrid-release update` (keeps the owner's :2400 data) rather than rm -rf.
     - **BLOCKED 11:45: the GitHub credential is gone after the reboot** (no `github.com` keychain item). The owner has been asked to re-add it in Keychain Access. Pending pushes:
       - agent `release/14/runtime-pin-r14b` `ae9c3bb44` (`wt-agent-pin-r14b`) → PR → merge → :2400 rebuild with App `2ce3c44fa`;
       - astrid-dev `plan/63-dependable-saving` `fe8e09dd` (worktree `scratchpad/wt63b`; the ref lives in `~/Developer/astrid-dev/.git`) → #880, with the body changed to "about 35";
       - app `release/14/quick-edits` `ff34621e9` (`wt-app-quick-edits`; empty-queue adopt plus progress watchdog; PR body drafted by the Sonnet) → PR → merge → in-place `astrid-release update`;
       - astrid-dev `3dc1b4ed`: four plans (63 Dependable saving, about 30 days; 64 Fast saving, about 11 days plus a conditional 9; 65 Editing together, about 11.5 days; 18 extensible), all queued in no release (`fable-four-questions.md`).
       - Held: runtime #65 (A/B measurement pending) and agent #402 (merge).
     - **:2400 rebuilt 12:0x** at the latest plan-59 (App `f236327ca`, Agent `2829f180`, Runtime `e6f4d5c2`); backup at `data-20261118-1204`. Main-thread browser test:
       - **Discard:** one click clears the screen and draft, and a reload is clean.
       - **Single nudge:** server head at 5.85–6.26 s. The commit timing is handler 5317 ms, **`provider_commit` 5116 ms**, accept 468.
       - **10-nudge burst:** all 10 saved in order with nothing undone, but drained serially over 64 s, with "Dirty" for 11 s before the first send.
       - **Bugs, sent to `release/14/live-fixes`:**
         1. Try again on a recovered draft with a base from the old realm loops silently (no commit; inspect, health and handshake loops; no reason shown), and the badge says "Saved" while the bar says unsaved.
         2. Discard left 37 old-realm outbox rows.
         3. The 11 s Dirty delay; the IDB write is being measured (a 5.9 MB record for one move).
       - The profiler is profiling `provider_commit`.
       - The owner's 11:10 move of clip-2 on chrome (4.27 → 7.13 s, old realm) is backed up in IDB `claude.owner-draft-backup`.
     - **The stability plan is written only:** a queued plan in no release, D9 open (Release 15 recommended), no branches. The Sonnet is writing the PR.
     - **Today's fixes must reach `release/14/main`:** after the :2400 browser validation passes, merge `release/14/plan-59` into `release/14/main` (App, Runtime, Agent).
   - **Release 15** (cut on the earlier reading; harmless, keep it):
     - `release/15/main` was cut and Release 14 brought forward: App `358dd0157` (#301), Runtime `3a609a6f2` (#64), Agent `1ad6160a9` (#401). The App's `vendor/timeline-composition` deletions are intended (plan-59 `7cc473e5b`).
     - **To do:**
       - forward-merge again after the pin bump and #61 (release/14/plan-59 → release/15/main in each repo, through a `release/15/forward-14*` branch);
       - fill the cut SHAs into the `releases/15.md` Branches table;
       - the "Dependable saving" plan (probably 63) is being written by a Sonnet; review it before it merges.
   - **Named gap: App `direct-journey` fails on plan-59 PRs** (#299 and #300 both fail; #295 into `release/14/main` passed).
     - The page never reaches `connected` (`direct-journey.spec.ts:107`, `support/app.ts:250`), and 43 of 45 tests didn't run. CI runs the Runtime and Agent at the **App's manifest pins**.
     - **Likely cause:** App pin skew on plan-59. The App lock pins Runtime `2d490617`.
     - **Fix at release freeze:** `regenerate_runtime_pins.py --app-checkout <real App>`, so the App lock and `public/install-manifest.json` move to the plan-59 Agent and Runtime. Then rerun `direct-journey`.
     - It doesn't block :2400, which takes its pins from the Agent.
     - The logs are at scratchpad `dj-300.log` and `dj-299.log`.
   - **Fable's sequencing** (`fable-stability-sequencing.md`), accepted by the main thread:
     - Stability is separable and goes first. Phase 0 becomes "dependable saving", in Release 15 (D9): CC-1 to CC-10, about 37 engineering days and about 15 elapsed.
     - TL-5 stays in extensibility. TL-10's upload half becomes CC-10.
     - The Release 14 cut-line: N1 to N12, the `_reference_basis` fix and the model-test seed. The structure goes in Release 15.
     - The owner still needs to decide D15 and D9.
   - **Plan 18 deltas** (Fable section 3) are applied after the owner's D15.
   - **Owner decisions:** D15 (refusal: remove and list, recommended, or leave visible and marked); D9 (Release 15 recommended); D10 synthetic; D14 persist `file_identity`.

0. **[10:30 owner] "GATHER EVIDENCE FOR ALL OF THIS AND ASK FABLE FOR THE ELEGANT APPROACH HERE THAT PREVENTS THIS WHOLE CATEGORY OF ISSUES".**
   - **Evidence** (in progress): `save-failures-evidence-pack.md` (Haiku), `save-state-map.md` (App fix Sonnet), `sonnet-commit-profile-r14.md` (profile Sonnet).
   - **Design:** Fable writes `fable-save-category-design.md`. Its first review, `fable-still-slow-review.md`, found:
     - the 12 s is a health call behind `store._mutex` plus an `ENOBUFS` lost reply, not commit computation;
     - the upload failure is `ENOBUFS` from `AudioAnalysisProvider.tsx:150-181` re-downloading all audio;
     - the stuck editor: the digest signs lifecycle fields (`:1061`), an untyped 409 retries (`client.ts:337-345`), and Discard is a no-op unless the outcome is `rejected` (`localSaveSession.ts:413`).
   - The App fix Sonnet (`release/14/save-recovery`) does only the guard plus the 409 rule now, and holds items 3–5 for Fable's design.
   - The owner's stuck :2400 state was cleared at about 10:25: two owner records were backed up to IndexedDB `claude.owner-draft-backup`/`stuck-20261118` on the 127.0.0.1:2400 origin, then removed. The head is `txn-76e8a3e2`.
   - **Next:** judge Fable's design on the main thread, plus an Opus elegance check if it's consequential. Then brief the builds and validate in the browser (two drops at once, a refused save, then Discard).

1. **[later status] All the Release 14 near-instant fixes are merged.**
   - **App** plan-59 `fbb8168bd`: #294, #295, #296 and #297.
   - **Agent** plan-59 `9de62436`: #394 and #396 (the memo on `RuntimeCommitService`).
   - **Runtime** plan-59 `d725811`: #59.
   
   Disk was cleaned to 8.1 GiB. :2400 is being rebuilt.
   - **09:55 finding.** The first rebuild ran the old Runtime `519b404`: the Agent's `runtime.lock.json` pins the Runtime, and nobody bumped it after #59. The owner's drop did save (`txn-ca7bcd49` at 08:55:41Z) but took a minute or more, and history GETs took about 9 s. **Fixed:** agent #399 → plan-59 `458d9d51` pins `d725811` (`scripts/regenerate_runtime_pins.py`), and :2400 is rebuilding again.
     - **At release freeze,** rerun `regenerate_runtime_pins.py` with `--app-checkout`, so the App lock (now `2d490617`) and `public/install-manifest.json` move with it (release coherence).
     - **Lesson:** any Runtime fix needs a pin bump in astrid-agent before a stack runs it.
     - The 127.0.0.1 outbox has 34 owner records (33 empty) plus one pending "Edit timeline" intent from an old tab. Watch that it resolves cleanly after the rebuild.
   - **Next, the main thread's browser test on 127.0.0.1:2400.** Measure the wall time of a drop with a check in server history, a move, a trim, a drop during another save, and inspector typing. Also try the stale localhost tab's buttons. Re-profile with counters only if a gesture still takes more than about 2 s. Opus flagged the Runtime's O(N²) ancestry walk as the next suspect.
   - **Then:** publish the bundle on :2400 once, and get the owner's OK on stills.
   - **Owner decisions:** the 6.9 GB folder and the older :2400 backups (`.data-20261118-0138`, `0147` and `0258`).
   - **Kept by the clean-up:** `wt-shot-trim`, which has an unpushed commit and 8 modified files and isn't ours.

   **[04:15 status]** The Opus set review (`opus-r14-set-review.md`) returned "merge after small fixes" for #59, #394, #295, #296 and #294, and "merge" for #297. Fixes are back with each PR's author agent. #295's `stale_head` auto-rebase premise is under verification. `commit-loads` was stalled and has been nudged.
   - **Merge order:** #59 into runtime `plan-59`; #394 (and `commit-loads`) into agent `main`; #294, #297 and #295 into app `main`; #296 into app `plan-59`; then each `main` into `plan-59`, rebuild :2400, re-profile (count opens too), and validate in the browser.
   - Before publication, poms_packs `100f388` must land on poms_packs `main`.

   **Release 14 near-instant saves.** Four PRs (runtime commit-cost, agent legacy-probes and commit-loads, app #295) plus #294. Steps:
   1. Review, then merge into `release/14/main`, and the Runtime one into `plan-59`.
   2. Merge `release/14/main` into `plan-59`.
   3. Rebuild :2400.
   4. **Main thread validates in the browser.** A drop saves, confirmed by server history, with its wall time. A move and a trim save. The stuck tab's buttons discharge it. Inspector typing doesn't storm.
2. **DONE 18 Nov.** astrid-dev #871 merged into `main` as `f97410b13`, and #842 is reopened with a comment. Owner decisions still open: D9 (the release), D10 (corpus data), D14 (cold start), plus phase 1's D4, D5, D6 and D8. **Plan 18 Phase 0 PR into astrid-dev `main`.** One PR: `d9ac42a4` + `bd535a5d` (the other session's draft phases) + `8e1ce0f3` / `1b4e654e` / `35f26b2b`. Open it after the Opus review and its edits, then merge at the owner's request. The body says the TL and EX phases are a draft awaiting D4, D5, D6 and D8, and Phase 0's open decisions are D9 and D10.
3. **After 1: the Almost Ready animation edits, LIVE on the owner's real Almost Ready.** Owner's words: "fix any issues that prevent it from working". It's only done when live.
   - **Handoff:** `/private/tmp/claude-501/-Users-hannahomalley/46bbf37f-d117-4667-992f-187a1428b815/scratchpad/ar-anim/`. It holds `bundle.json` (38 changes, built on head `969b5e41…`), `build.py` (rebases onto any head), `diff.md`, and `PUBLISH.txt` (use `publish_doc.py`; the skill's `timeline_document.py` is stale, astrid-dev #869).
   - **Elements:** `~/Developer/poms_packs`, branch `task/plan59-am-camera-inset`, commit `100f388` (am-discord ×3, am-footage ×2).
   - **The four changes:**
     1. 0:06–0:08, three linear beat zooms (the last on "Tomorrow"), then a lingering zoom;
     2. ~0:22, one continuous zoom with no snap at the end;
     3. ~2:20, "You can adapt everything" slides in from the left, pushing the stats cards right, then goes into the existing zoom;
     4. ~2:37, the text becomes "A shared creative foundation for the open source ecosystem."
   - **Steps:**
     1. Rebase the bundle onto the current head.
     2. Publish once, with no retry on a lost response.
     3. Check stills at 0:05–0:09, 0:18–0:23 and 2:24–2:40. No render.
     4. Send the owner the editor link with timecodes.
   - **Live blockers:**
     - Live R13 refuses every publish to Almost Ready (half catalog association `a09025f7`), so it needs #393 on live. R13 lacks `_preexisting.py`. The other session's draft backport plan is at `.../46bbf37f-…/scratchpad/live-fix/plan.md`.
     - The five element changes must reach the live editor. If live uses the hosted astrid.haus editor, it ignores local pack files.
   - **Scoped 18 Nov (Haiku, read-only):**
     - **Bundle base.** The bundle is built on `969b5e41`, which is also the live head copied into :2400 at the rebuild. The other session ran one publish attempt on :2400 from 02:11:56Z to 02:13:43Z (traceback in `publish.out`, outcome unknown). Check :2400 history before any retry.
     - **The live Agent:** R13 `9814193a`, Runtime `6855dfa8`.
       - It has no `_preexisting.py` and no `split_findings`.
       - The three files #393 touches are byte-identical to `5369ea9ed^`, so the hunks apply cleanly, plus copy `_preexisting.py` (36 lines).
       - The proper route is an R13 hotfix through the installer, not an in-place edit; see the other session's `live-fix/optionB.diff`.
     - **The live editor is hosted astrid.haus.** Nothing serves :2222; the door is :17340.
       - Hosted astrid.haus bundles its own motion pack, so the five element changes (poms_packs `100f388`) won't reach it without a hosted App deploy.
       - The alternative, per memory: rework the edits onto existing element params, or per-frame clips.
       - Decide when we get there. A hosted deploy is outward-facing, so confirm its specifics with the owner.
   - **18 Nov, owner:** "get second opinions from fable on blockers on the strategy too … make sure to test live to validate on that too … do everything in subagents". Fable's strategy review goes to `fable-live-blockers.md`. The plan has to finish with a live validation: server history and head, plus stills in the editor.
   - **Fable's strategy** (`fable-live-blockers.md`), accepted by the main thread: **ride Release 14.**
     - The hosted editor compiles its vendored pack, and there's no runtime pack path, so the elements reach astrid.haus only through an App deploy at publication.
     - #393 is already on `release/14/main`, and live's Agent is its ancestor.
     - Rebuilding the edits on existing params isn't feasible: zoom clamps to integers 1–3 and there's no feather.
     - Don't publish to live before the editor deploys.
   - **Sequence:**
     1. Preserve the handoff (`~/Developer/astrid-release-src/ar-anim-handoff/`) and push poms_packs `100f388`.
     2. Vendor the five files to `release/14/am-camera-inset` (astrid-app PR), and fix #869 on `release/14/skill-writer`.
     3. Merge everything into `release/14/main`, merge that into plan-59, and rebuild :2400 through the installer.
     4. Validate saves in the browser.
     5. Publish the bundle on :2400 once, with no blind retry: poll history for the key. Get the owner's OK on stills.
     6. **Owner's go to publish Release 14.**
     7. Publish the bundle to live once, after asserting the endpoint is :17340 live and that :2400 is stopped or not targeted.
     8. Validate live: one new revision with our key and 38 changes, then astrid.haus stills against :2400 at the three ranges (feather and zoom above 3 prove the new code).
   - **#869 needs no source change.** astrid-agent `release/14/main` `astrid/packs/rendering/docs/scripts/timeline_document.py` is already current. The stale copy is the installed skill (`~/.claude/skills/astrid-rendering`, which links to `~/.local/state/astrid/skills/...`, plus the rename, live-main and labs trees), and it refreshes with the Release 14 install. For the publish, use the handoff's `publish_doc.py` or the Release 14 script.
   - **Gaps to file:** the App vendor refresh reads only an Agent commit, but `astrid_motion` now lives in poms_packs. Also, `PUBLISH.txt` and `runpy.sh` target :2400.
4. **Deferred filings:** F5, F7, the typed `CheckReport.existing`, `validation.py` churn, overrun crop-vs-block (the other session's), and `shot-group-pack-commands.ts:189-190`, which can still write a half association.
