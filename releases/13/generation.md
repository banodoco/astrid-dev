# Release 13 — Generation task detail (former Release 12 Track B)

> **Moved on 11 Nov 2026.** Hannah split the combined release; this work is now [Release 13](../13.md), which governs wherever it differs from this page. Read this page for SHAs, task cards and the GPU cell table. Its cross-track protocol is superseded: there is no Track A to wait for, no `A-FROZEN`/`FINAL-B7`/`FINAL-TUPLE` hand-off and no mailbox; the base is published Release 12. "Cheapest adequate GPU" is replaced by the RTX 4090/5090 rule in Release 13. Links into Release 12 sections refer to the pre-split brief at astrid-dev `a51e1a7`.

[Current manager transition](../../docs/handoffs/2026-11-11-release12-track-b-transition.md) · Confirm its refs and operating state before resuming.

## Current state — 11 Nov, 16:45 UTC

This is a progress snapshot, not a gate or freeze. Full history and acceptance criteria remain below and in the plan task records.

| Label | Exact ref or evidence | State and next action |
|---|---|---|
| P40-T9 | Agent `plan40/staging-int40` `d8931c281cf705273c3c7c01346b6f2722733cca` | Accepted focused handoff. |
| B5 | Agent `release12/gen-candidate` `1439ccc63bf8d9ed5422ac1f95ffdd6158560e1e` | Pushed WIP, **not B-CANDIDATE**. Reviewed error-contract handoff integrated; [focused merge-head receipt](../../plans/32-generation-placement-targets/evidence/release12-b5-focused-cpu.md) records the checks and Runtime-import rerun. H3 disposition and remaining required proof remain open. |
| R12-F2 | Agent handoff `plan32/r12-error-contract` `e1731b9e4e86638e6425cf5601160e32be683a72`; Runtime `handoff/r12-self-observe` `8b312c4b29bbb4fef5ac0849188678fe356b9e84` | Provisional pair; reviewed, focused checks and installed no-claim attachment/refusal checks passed. Runtime pin remains subject to freeze coordination. |
| Diagnostic App | App `handoff/r12-provisional-tts-e173` `c1dd6104df78f2849404ab1261d1ff628872aa54` | Provisional diagnostic handoff only; not a final App or release tuple. |
| Retention repair | Agent `handoff/r12-retention-fingerprint` `6dbe7f9aefc7d2ee6004787c5fe269644fcf9a49` | Pushed, divergent and unaccepted WIP; focused safety controls remain incomplete. |
| B6 / final tuple | No `A-FROZEN`, `FINAL-B7`, or `FINAL-TUPLE` | Final integration, B8, B9 and final cells await their named inputs. |
| P34 | Final qualification remains open | Follow the named tuple, consent, custody, census and budget rules below. |

[Release 12](../12.md) · [Track A: Fixes](../12/fixes.md) · Reference only: handoffs for [P32](../../plans/32-generation-placement-targets/handoff.md), [P40](../../plans/40-machine-lifetime-controls/handoff.md), [P20](../../plans/20-zero-to-first-image/handoff.md), [P34](../../plans/34-real-gpu-proof/handoff.md)

Active P32, P40, P20 and P34 brief as of 10 Nov 2026. Follow the shared [operating principles](../12.md#operating-principles-every-manager-reads-these-first), [How-to](../12.md#how-to-tools-every-manager-uses), branch rules and [mailbox protocol](../12.md#hand-offs-all-via-mailboxes). Handoff next steps, gates, freezes and budgets are superseded.

## START HERE — Track B manager

One session owns all four role blocks below. Read each block and its linked task cards; delegate work by the existing routes and preserve each role's branch/evidence ownership. A bounded manager may own a substantial subproject when useful, while the track manager remains accountable. Start P40's B1 and P20's three independent preparation tasks while preparing P32 composition and P34's unpaid inputs. Consume completed internal dependencies directly, recording their handoff labels for the orchestrator. A role's waiting instruction does not stop the whole session while another assigned role has ready work. Track B ends `DONE` only after all four completion records are accepted and the orchestrator closes every role.

Use the shared [issue mailbox and session mapping](../12.md#hand-offs-all-via-mailboxes) for the separate chats; local files in another chat are not an inbox.

## Rules for every Track B role

- **Worker routing:** delegate normal work to Luna, X / extra-hard work to Terra, and super-hard work to Sol, preserving task-card routes. **Consult Astra for high-stakes major decisions and whenever blocked**, under the shared [role and authority rules](../12.md#roles-one-orchestrator-two-track-managers). Escalate tricky/nefarious bugfixes and previous-agent struggles to Astra. Send advice and a recommendation to the orchestrator for reserved decisions; Hannah retains product behavior, scope/budget and publication authority. Independent reviews remain Astra; consultation does not reset review budgets.
- **First:** push `scratch/<plan>-push-test` and run `smoke.sh` once, per How-to.
- **Branches:** push only your product branches below; use merge commits for integration, never force-push or rebase. Each manager may also push fresh astrid-dev progress/completion branches under the shared branch rules; P34 keeps GPU evidence in PR #260. No `int/**` or `main` pushes before the orchestrator's publication/post-publish instructions; CI-trigger prep waits until after publish.
- **CI and GPU:** B8 is the only planned Agent CI dispatch here; the shared CI rules cover any missing baseline collection. Only P34 rents. Reruns of CI, reviews or GPU cells require the orchestrator's OK.
- **Waiting:** re-read the agreed issue inbox (or registered mailbox for a shared-host runner), then end your reply with `RUN-STATUS: WAITING <label> from <sender>`. Use `WAITING`, never `DONE`, while another manager may need you.
- **Review budgets:** P32 3/3, P40 1/1, P20 R1 1/1 and R2 1/1 are used; P20 R3 has one round left. T9 has the separately authorized focused review in its task card. B9 covers new merge changes; follow-up verification of blocker fixes does not reopen unrelated rounds.

## START HERE — P40 manager

**Transition:** P40-T9 is already accepted at `d8931c281cf705273c3c7c01346b6f2722733cca`; see the [current handoff](../../docs/handoffs/2026-11-11-release12-track-b-transition.md). The following original sequence is retained for context and is not an instruction to redo it. Other P40 acceptance rows remain governed by their task records.

- **Do now:** B1, P40-R1.1–R1.4, on `plan40/staging-int40` (`b15e286b6`).
- **Then:** B2, merging `plan32/staging-int32` `d28cac190` and Plan 34 fix N `e0d95d7b8` (branch `plan34/fix-failure-diagnostics`). Then B3, **P40-T9** per its card in Plan 40's `tasks.md`, with its focused review.
- **Push:** `plan40/staging-int40` only.
- **Done when:** you have posted `P40-T9 sha=<sha>` (reviewed). Then end `RUN-STATUS: WAITING CHECKPOINT-B from orchestrator`, not `DONE`, so you can answer P32's questions during composition.

## START HERE — P20 manager

**Transition:** P20 Agent preparation is pushed at `e28a509b6bd8c352514d4b4cc14c95628a8302e7` and incorporated into B5 WIP. P20 App preparation is pushed at `ee9e0b9a6995a08c63040e031d049a7a320f7ef1`; its final refresh still waits for exact `A-FROZEN`. VibeComfy `release12/vibecomfy` already exists at `8d065a8fef3dd602d5462e27d8eca088cf4e8262`. These are preparation handoffs, not final release acceptance; use the [current handoff](../../docs/handoffs/2026-11-11-release12-track-b-transition.md) and task records before resuming. The original sequence below is historical, not a request to recreate those branches.

- **Do now, in parallel:**
  1. Merge `plan32/staging-int32` `d28cac190` into `plan20/staging-agent` (`d2a84370f`), re-prove it, and post `P20-AGENT sha=<sha>`. Confirm the reviewed P1.5 phase-1 changes (`6fb1d5861`, draft Agent #341) are present; reconcile any missing change with P32 rather than merging an old release base wholesale. Run the maintained-guide, setup-pack and setup-branch selectors, mirror check and README render check; verify installer quotations against this candidate. Cover the changed P20 integration with its one remaining independent Astra R3 round before `P20-AGENT`; [R3's task card](../../plans/20-zero-to-first-image/tasks.md) requires later integration changes to have review coverage before P3.5. Review the exact staged head and changes since its prior report, resolve blockers and record the receipt; do not restart R1/R2 or exceed R3's two-round total. B9 still covers subsequent final merge changes. Plan 29's donor `bc5aa747` is also in Track A's candidate; P32 checks for duplicate behavior during B5 and again when Track A joins at B7; keep one implementation and prove P20-P3.3b's selection and opt-out tests.
  2. B6: prepare `plan20/staging-app` (`e61607a1a`) against the current App candidate while A4 continues. Once `A-FROZEN` arrives, merge its exact App SHA, re-prove P20-P2.3, P20-P2.4 and the R2 repairs, and post the final `P20-APP sha=<sha> base-app=<A-FROZEN-app>`. Only this final handoff feeds A5-prep; a replacement freeze requires a matching refresh.
  3. B4a: create VibeComfy `release12/vibecomfy` from VibeComfy `main` (`e65f4941`), merging #165 (`38969618`) and #166 (`af5cb429`) `--no-ff`. Run their focused tests, push once, and post `VIBECOMFY-RELEASE sha=<sha>`. This is the one pin change Plan 20 makes; it overrides your handoff's hard limit for this release only.
- **The S2 rule** ("P2.3's link not live before S2 is on Agent `main`") is satisfied by shipping P2.3 and S2 in the same Release 12 tuple. Don't strip the link.
- **Push:** `plan20/staging-agent`, `plan20/staging-app` and VibeComfy `release12/vibecomfy`.
- **Done when:** `P20-AGENT`, final `P20-APP` and `VIBECOMFY-RELEASE` are posted. Then end `RUN-STATUS: WAITING CHECKPOINT-B from orchestrator`; remain available for Agent/App composition conflicts.

## START HERE — P32 manager

- **Do now:** keep `plan32/staging-int32` current. The three CI collection errors are P29's task A0; fix any **further** collection errors caused by generation code on your staging branch.
- **When `P40-T9` and `P20-AGENT` arrive:** B5. Create `release12/gen-candidate` from `plan32/staging-int32`, then merge `--no-ff` exactly those two SHAs, P40 first. Apply the agreed B4 pins, run each plan's focused proof and post `B-CANDIDATE sha=<sha>`. Composition may overlap the early TTS diagnosis; if that diagnosis finds a blocker, merge the owning plan's repair and post the replacement candidate before B7.
- **When `A-FROZEN`, accepted `B-CANDIDATE` and B4 pins exist, and the TTS diagnosis has no unresolved blocker:** B7. Create `release12/gen-rehearsal` from the frozen Agent, merge exactly `B-CANDIDATE` `--no-ff`, explicitly preserve the still-needed `d70bed508` repair, reconcile both parents and pins, and run focused proof of all four plans, including P20's guide/mirror/README checks and installer quotations against this integrated Agent revision. This is P1.5's pre-publication proof for the combined release; P20 verifies the published revision again after publication. Post `FINAL-B7 sha=<sha>`. An eligible early rehearsal may be promoted instead; subsequent changes use the shared re-freeze rules.
- **Then, once each, on `FINAL-B7`:**
  - B8: dispatch Agent CI. Either `POST https://api.github.com/repos/banodoco/astrid-agent/actions/workflows/ci.yml/dispatches` with body `{"ref":"release12/gen-rehearsal"}`, or ask the orchestrator to dispatch it. Compare complete test IDs against `A-FROZEN`'s `ci-run` and recorded R10/R11/main evidence under P39-D8; do not infer parity from an aborted baseline. Post `B8-RESULT PASS|FAIL sha=<sha> ci-run=<id> evidence=<path>` with the comparison and all unresolved buckets.
  - B9: the orchestrator runs one independent Astra merge-delta review. Start with `git log --merges --remerge-diff <A-FROZEN-agent>..<FINAL-B7>`, inspect both-parent resolutions, the `d70bed508` port and pin files; finish with the App merge delta and re-pin #2 once `FINAL-TUPLE` arrives. Each plan's own code was reviewed in its own rounds. Report all blockers before `CHECKPOINT-B`.
- **Push:** `plan32/staging-int32`, `release12/gen-candidate`, `release12/gen-rehearsal` and the one optional `scratch/p32-gen-rehearsal`.
- **Done when:** B8 meets the regression rule and B9 has no open blocker. Refresh the P32-T8 completion draft [#276](https://github.com/banodoco/astrid-dev/pull/276) against `FINAL-B7`, then end `RUN-STATUS: WAITING CHECKPOINT-B from orchestrator`; do not mark the plan complete before its publication requirements hold.
- **Early rehearsal:** once on `scratch/p32-gen-rehearsal`, using `A-CAND` and the current generation candidate. It is not final proof. At B7, promote it only if both parents equal the accepted frozen inputs and all B7 repairs, pins and focused checks are present; otherwise build the correct rehearsal. No CI or final GPU run on speculative inputs.

## START HERE — P34 manager

- **Use only exact SHAs recorded in accepted handoff events.** The Track B manager records internal role outputs; orchestrator-issued labels come through the agreed issue inbox (or registered shared-host mailbox). Don't watch `int/32`, which won't move.
- **Do now:** nothing paid. Prepare cell inputs from committed fixtures and obtain `RUNPOD_API_KEY` from the environment (never print it). While T9 is unfinished, continue the other Track B responsibilities. Do not start paid diagnosis until the orchestrator names its complete diagnostic inputs after `P40-T9`.
- **Installing a candidate:** follow [astrid-dev-gpu-validate](../../skills/astrid-dev-gpu-validate/SKILL.md) for the install and census mechanics only. The cell table below replaces its flow, its budget and its release-on-failure rule. For the TTS diagnosis, build a manifest override for the named candidate the way the [SFX audit](https://github.com/banodoco/astrid-dev/blob/plan34/gpu-validation-2026-11-10/validation/gpu/2026-11-10-sfx-candidate.md) did, and install with `run-astrid install --manifest <file>`. For final cells, wait for P29's `FINAL-TUPLE` from A5-prep: install its exact App-branch manifest, already pinned to `FINAL-B7`, with its recorded sha256. Do not edit the manifest locally or install the earlier Checkpoint A tuple.
- **When `P40-T9` arrives:** one **TTS diagnosis** on the pushed candidate the orchestrator names, containing T9, fix N and the TTS repair from `d28cac190`, with manifest and engine pins aligned. If it fails, inspect the retained pod within T9's limits and post `TTS-DIAG` with cause, exact inputs and spend. Keep only the allowlisted failure summary, never raw prompts, URLs, logs or keys. Route any blocker to its owning plan before B7; CPU repair proof may close the diagnostic finding, while the final TTS cell still must pass live.
- **When `FINAL-B7` and `FINAL-TUPLE` arrive:** install the named manifest, verify Agent/Runtime and all generation pins including the pod's VibeComfy HEAD, then run the in-scope **final qualification** cells below, **each once**, in **warm batches**: group the cells by GPU type, and run each group back to back on one pod ([principle 8](../12.md#operating-principles-every-manager-reads-these-first)). The same-pod warm-reuse cell is the second job of a batch. Up to **two batches at a time**, each in its own isolated install and data root. Post each result with its exact Agent/pins, manifest digest and spend. CI and review may run concurrently; if the orchestrator withdraws the tuple, stop starting affected cells and follow its re-freeze instructions.
- **Rules:**
  - one waiting product command per cell, with no time window;
  - no geographic filters;
  - the cheapest adequate GPU;
  - a census before each rental and after each release. Keep the pod idle between cells of the same batch, within its consented idle and spend limits. Release it when the batch ends, at the idle limit, or at once if reuse is unsafe. Never leave a pod up after a batch is done;
  - count setup, idle time and overlapping batches against the same $25 ledger. Before renting, allocate non-overlapping remaining amounts to concurrent batches; never treat each root as having $25. Keep the original $1 safety margin within the remaining total, and stop before a new rental would exceed its allocation;
  - **at $25 total, stop, release every pod owned by this run, and report `BLOCKED: budget`.** An unknown/unowned pod stops new claims; report it rather than releasing another owner's pod.
- **A failed final cell:** report and inspect it within T9's limits. Keep a safe pod warm while immediate diagnosis or unaffected same-batch work remains, then release at batch end/idle limit; never rent repeated attempts blindly. After a repair, rerun the failed cell once only with the orchestrator's OK and sufficient remaining budget. If Agent/pins change, earlier final-cell passes on the old inputs are history: the replacement tuple must satisfy the full final-cell gate, with all reruns charged to the same cap.
- **Push:** the evidence branch `plan34/gpu-validation-2026-11-10` only, which updates record PR [#260](https://github.com/banodoco/astrid-dev/pull/260).
- **Done when:** every in-scope final qualification cell has passed on the accepted `FINAL-B7`/`FINAL-TUPLE` inputs and PR #260 has the receipts and spend. Run Plan 34's final review (H3: it runs, but does not gate unless Hannah adds it), route any actual release blocker, then end `RUN-STATUS: WAITING PUBLISHED from orchestrator`.

## Finish after publication

On `PUBLISHED`, complete the shared [post-publish checklist](../12.md#after-publish): P32's CI-trigger prep and completion draft, P40's completion evidence, P20's published-revision quotations then P3.5 hosted CPU journeys (including the weaker-agent row) and P3.6, and P34's final review/receipts/spend/empty owned-pod census. Record H3 exclusions and unproved wider Plan 34 claims. Post a separate `COMPLETION-READY plan=<NN>` for each responsibility. A blocked hosted journey or other remaining task stays open with its next action; waiting on that role does not prevent finishing another role. If H4 splits, follow the revised scope and leave generation completion open until its eventual publication.

Hannah's 11 Nov direction adds **live h3_av qualification immediately after publication** as P34's first ready post-publication work; it does not add a pre-publication gate cell. Follow the [Plan 34 task](../../plans/34-real-gpu-proof/tasks.md): bind the installed manifest, Agent, Runtime and engine pins to the exact `PUBLISHED` tuple and record output, revisions, consent, spend and census. Before renting, confirm the published tuple actually contains the path, reconcile the shared ledger and current account state, and establish that the remaining existing authorization covers this post-publication work. The $25 stop, $1 margin, custody and census rules remain; no budget increase or extra rental authority is implied. If the existing scope, authorization or remaining funds cannot cover it, post `BLOCKED` to the orchestrator with the smallest justified next action. Do not leave a paid pod running while waiting.

## GPU cells

$3.13 is already spent. The caps below are ceilings, not targets. Rows on `FINAL-B7` are the final qualification cells; the early diagnosis has a separate purpose and never substitutes for final TTS proof.

| Cell | In scope? | Runs on | Max runs | Cap |
|---|---|---|---|---|
| TTS diagnosis (diagnostic only, not gate 5) | in | candidate with T9 | 1 | $3 (first-look pool) |
| image t2i | in | `FINAL-B7` | 1 | $1 |
| image edit | in | `FINAL-B7` | 1 | $1 |
| music | in | `FINAL-B7` | 1 | $1 |
| TTS | in | `FINAL-B7` | 1 | $3 |
| SFX | in | `FINAL-B7` | 1 | $3 |
| video i2v, v2v, edit | in | `FINAL-B7` | 1 each | $2 each ($6) |
| same-pod warm reuse (second job, same pod) | in (H3) | `FINAL-B7` | 1 | $1 |
| reruns after a fix | — | re-frozen `FINAL-B7` | orchestrator's OK | from what's left of the $25 |
| local-managed, attached, h3_av | **out** until Hannah decides (H3) | — | 0 | — |

The warm-reuse cell is a separate second job within a batch. Record both job identities, the unchanged pod/lease identity, reuse of its prepared engine/models and unchanged paid deadline; a second successful output alone does not prove reuse. It proves same-pod reuse, not G5's second-pod volume reuse.

The planned cell ceilings total $3.13 + $3 + $16 = $22.13, leaving at most $2.87 for overhead/reruns ($1 remains a safety margin, not another cell allocation). Actual setup and idle charges reduce that remainder. If required proof will exceed the available allocation, post `BLOCKED: budget`; the orchestrator recommends either the smallest justified increase or H4's fixes-only release to Hannah. Never omit a required final cell to fit the cap.

## Task index (for the orchestrator)

| # | Task | Owner | Depends on |
|---|---|---|---|
| B1 | P40-R1.1–R1.4 | P40 | — |
| B2 | staging + fix N into `plan40/staging-int40` | P40 | B1 |
| B3 | P40-T9 + focused review | P40 | B2 |
| B4 | Pins: VibeComfy release (P20, B4a); ComfyUI and Runtime per the [pin rule](../12.md#pins-default-rule-b4) | P20 + orchestrator | — |
| B3a | Early TTS diagnosis; route and repair any blocker | P34 + owning plan | B3; orchestrator names complete diagnostic inputs |
| B5 | Compose `release12/gen-candidate` | P32 | B3, B4, `P20-AGENT`; incorporate B3a repairs before B7 |
| B6 | Final P20 App merge/proof against frozen App | P20 | Prepare now; finalize after `A-FROZEN` |
| B7 | `release12/gen-rehearsal` → `FINAL-B7` | P32 | `A-FROZEN`, B4, accepted B5; B3a has no unresolved blocker |
| B8 | One Agent CI on `FINAL-B7` vs `A-FROZEN` | P32 | B7 |
| B9 | One Agent/App merge-delta review | Orchestrator | Start after B7; finish after A5-prep / `FINAL-TUPLE` |
| B10 | Final GPU qualification cells | P34 | B7, B4, A5-prep / `FINAL-TUPLE` |
| B11 | Prepare completion records (P32-T8, P40 phase, P20 proof, P34 record); finish the shared post-publish steps and post `COMPLETION-READY` | Each plan | B8–B10 for drafts; `PUBLISHED` and each plan's remaining tasks for completion |

`CHECKPOINT-B agent=<sha> app=<sha>` is posted by the orchestrator when B8 meets D8, B9 has no open blocker and B10 has all final-cell passes for the accepted `FINAL-TUPLE`. The early TTS diagnosis is not a second final gate. If H4 splits the release, Track B continues preparation but does not block Release 12; further paid proof waits for an explicitly revised scope/budget.
