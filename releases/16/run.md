# Release 16 — run board

The live state of the Release 16 run, rewritten at each check-in by the release manager. The [brief](../16.md) holds intent, included plans, branches and issues; each plan's `tasks.md` holds its progress.

## Scope change — 25 November 2026

The owner now places the full Plan 91 green programme in [Release 17](../17.md), not Release 16. The existing plan branch, packet names, mailbox, evidence and active authority below are preserved; nothing is deleted, renamed, force-pushed or merged by this scoping change. **Do not land Plan 91 into release/16/main.** Before another target-dependent dispatch or landing, the existing Lead and Plan 91 orchestrator must record a coordinated handoff, confirm in-flight work, and rebind destination, branch and proof on the Release 17 base. Until then use the existing lane only for already-authorized bounded work on its retained branch; do not start a competing lane or treat the historical launch message below as fresh authorization. The Release 17 brief is the intended destination, and the older dispatch section remains the record of the original run.

The Plan 91 mailbox records the owner-directed [STOP](https://github.com/banodoco/astrid-dev/issues/1826#issuecomment-7129888302) and [manager confirmation](https://github.com/banodoco/astrid-dev/issues/1826#issuecomment-7130215692): no packet was started and monitoring stopped. The older bounded-authority text does not override that STOP; only a later owner or orchestrator decision can resume it. Preserve its actual Agent branch and records.

## H3 programme lane

One orchestrator runs Plans 66, 68, 70 and 67, then Plan 107 in Release 17. It answers to the owner. Everything about how it runs is in the lane brief [briefs/h3.md](briefs/h3.md): plans and order, queue, dispatch, proof, reviews, merges, rulings, cut line, coordination and launch. State: running; the owner gave the go on 28 November 2026 (see the Lanes table and the brief's `**Go:**`).

### Lanes

| Lane | Session | Brief | State |
|---|---|---|---|
| h3 (Plans 66, 68, 70, 67; board `board: lane h3`) | not yet recorded; the orchestrator records it in its brief at its first progress PR | [briefs/h3.md](briefs/h3.md) | running, from the owner's go of 28 November |

## Proposed H3 programme queue (66, 68, 70, 67)

**Superseded 28 November:** the [H3 programme lane](#h3-programme-lane) replaces this queue and its Lead activation; the packets below are acceptance history only. The rows below remain the acceptance history. Prepared at the owner's request, 27 November. **Draft only: not active authority, branch cut, dispatch or Ready.** Preserve all existing R16 recovery lanes, active Plans table and boards. Existing Lead [#2030](https://github.com/banodoco/astrid-dev/issues/2030) reviews [PR #2056](https://github.com/banodoco/astrid-dev/pull/2056) and explicitly activates rows with exact accepted source and current standing rulings. No competing Lead, native subagents, new scheduler or extra chat/CI/GPU allocation.

**Readiness gate.** Independent high-judgment review of revised P66/P67 contract, including existing hook injection, registry/soft-default boundaries and unchanged H3 no-Astrid-imports guard. At preparation observed Agent R16 main `4a2bad187f12e7b0d1ba5bd1164b4a076787516a`, VibeComfy R16 main `55c3948212d23cf037fae8a4c6faad77d33e7279`, R15 Agent `dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5`, published poms default pin `2379ab54aca522019ff4f869cfdf9375bdb56dfc`. Observations, not dispatch pins. Lead refreshes actual refs, verifies retained P59/64/65 ancestor/contract, checks adequate CPU venue, capacity and function reservations, then cuts P66 from accepted R16 integration. No P17 prerequisite. Each packet needs actual focused base selectors/results, executed node IDs and configured marks/deselections, precise May touch functions and dependencies present in consumer's exact base. No baseline was executed in this planning session. New tests not on base are explicitly accounted for on head. Preserve existing checks; missing collection, resource/transport errors or incomplete source closure are NO-RESULT, not PASS. Exact approved replacement selectors required if v1/capture cleanup removes a test; do not silently omit.

**Proof/authority.** Current Lead-managed recovery handoff supersedes historical in-chat proof assumption for this proposed lane. One fresh normal ChatGPT author per implementation packet (N High, X Extra High, S Pro; T editorial cards propose Pro, confirm actual binding). Early STATUS and draft PR, then exact READY-PROOF with repository/PR/head/selectors and stop. No tests/build/merge/native subagents by author absent current explicit Lead ruling. Lead/custodian runs exact base and candidate proof in adequate pinned environment and commissions independent RS/R review. Keep real failure IDs and full node inventories/logs, no silent skip/xfail/deselect or test weakening. Review/diagnostic and installed proof rows are Lead assignments, not author chats. Real native/cold reads/CPU ComfyUI/installation proof and pin changes use Lead-authorized venue; CPU compile is not live quality. R16 final exact-tuple qualification and separately authorized live/GPU gate remain. A Parked dependency never unlocks a consumer; actual accepted handoff must be present in its exact base.

**Sequence.** P66 serial job/compile/caller cutover, RS1, one capability/provider table, describe, node inventory, neutral receipt, clocks, occurrence compose/verify, templates and skills, then independent closing review and accepted R16 integration. After 66, two tracks run subject to actual writer/slot reservations:
- Native track: P68 guide → full-canvas still preparation → exact mask/compose proof → recipes, then P70 compare full canvas vs active capture → prefix → bridge → insert → delete capture/flag → recipes → integrated review. 70-01 is a decision gate, not permission to assume equal latent shapes. P70 bridge/insert may author concurrently only with reviewed disjoint functions/fixtures; conservative queue serializes them.
- P67 shared track: 01 independent contract review, 02 staged admission (only missing P17 P1 slice), 03 bounded host/worker custody; 04 pure default selector can proceed beside 02 if exact schema/parser functions are disjoint; 05 joins shared transaction. 08 pinned VC NKD schema cache can proceed independently after 01. External activation remains blocked if an unscoped generic prerequisite appears; native steering does not wait for it.
- Native P67 10–14 follow accepted P70 in the conservative queue (shared H3 schema/builder/receipt/table writers); they do **not** depend on CS-0/installer or NKD. 14 stock guide phase is independent of NKD fallback. 06 point injection after 03 and P70, 07 independent pack root, 09 node declaration/soft companion require 05/07/08; reserve H3 functions against 10–14. If Lead can isolate disjoint earlier native or point/hook functions, advance reviewed slices after producer contract, with exact accepted base sync; no parallel writers to same schema/builder/table/shared tests/skill. Do not rely on clean merge as proof. 15 actual curve and conditional fallback waits 14 and independent package/node handoff. 16 native recipes may proceed after native 14 even if external blocked; 17 provider recipes joins both. 18 actual default install, 19 shared/chained installed graph, 20 controller/worker custody, independent 67-R. This preserves every original 67 outcome including P70 speech-continue.
- Existing P09/P35 install and grants, P90/P93/P94 generation/VC/worker pins and receipt owners, P31 manifest, actual proof/CI/chat limits remain protected. Lead reserves actual functions, not entire repos. Same-source default pins for NKD and astrid_motion remain in existing manifest; poms_packs is an external input, not an unsupported release-branch-table repo. Lead designates reviewed external candidate target (proposed `p67/r16-provider` from approved source), no author writes to main. P31 alone publishes exact pins. Keep full P17 paused; reuse actual P1 evidence once.

All rows below are **Prepared / Blocked** until approved. Only the Lead reconciles them into active dispatch; [manager briefs](briefs/README.md) are prepared, not launched.

### Proposed H3 Plan 66 queue

| Packet | Task slice | Repository | Route | Depends (accepted) |
| --- | --- | --- | --- | --- |
| [R16-P66-01](packets/R16-P66-01.md) Freeze measured job and ownership | CC-1.1 (a) | astrid-agent | S | readiness gate |
| [R16-P66-02](packets/R16-P66-02.md) Persist and reuse the resolved job | CC-1.1 (b) | astrid-agent | S | R16-P66-01 |
| [R16-P66-03](packets/R16-P66-03.md) Introduce compile_job and source-free feature lowering | CC-1.2 (a) | astrid-agent | S | R16-P66-02 |
| [R16-P66-04](packets/R16-P66-04.md) Unify masks, adapters and retained continuation | CC-1.2 (b) | astrid-agent | S | R16-P66-03 |
| [R16-P66-05](packets/R16-P66-05.md) Move public and lifecycle callers to compile_job | CC-1.3 (a) | astrid-agent | X | R16-P66-04 |
| [R16-P66-06](packets/R16-P66-06.md) Consolidate interim transport without losing custody | CC-1.3 (b) | astrid-agent | S | R16-P66-05 |
| [R16-P66-07](packets/R16-P66-07.md) Migrate v2 canonical-spec consumers | CC-1.4 (a) | astrid-agent | S | R16-P66-06 |
| [R16-P66-08](packets/R16-P66-08.md) Retire v1 and route classification | CC-1.4 (b) | astrid-agent | S | R16-P66-07 |
| [R16-P66-RS1](packets/R16-P66-RS1.md) Independent resolved-job contract review | RS1 | astrid-agent (Lead) | S | R16-P66-08 |
| [R16-P66-09](packets/R16-P66-09.md) One capability table and typed provider assembly | CC-2 (a) | astrid-agent | X | R16-P66-RS1 |
| [R16-P66-10](packets/R16-P66-10.md) One public describe and admission projection | CC-2 (b) | astrid-agent | X | R16-P66-09 |
| [R16-P66-11](packets/R16-P66-11.md) Read worker node inventory from existing pins | CC-2 (c; Plan 64 SR-3) | astrid-agent | X | R16-P66-10 |
| [R16-P66-12](packets/R16-P66-12.md) Serialize the pack-owned resolved-job view | CC-3 (a) | astrid-agent | X | R16-P66-11 |
| [R16-P66-13](packets/R16-P66-13.md) Authenticate neutral producer evidence through SDK readback | CC-3 (b; retained SR-6 receipt) | astrid-agent | X | R16-P66-12 |
| [R16-P66-14](packets/R16-P66-14.md) Resolve end-relative times on stream clocks | CC-9 | astrid-agent | X | R16-P66-13 |
| [R16-P66-15](packets/R16-P66-15.md) Paste exact media by occurrence | CC-10 (a) | astrid-agent | X | R16-P66-14 |
| [R16-P66-16](packets/R16-P66-16.md) Verify exact delivered pixels and per-channel PCM | CC-10 (b) | astrid-agent | X | R16-P66-15 |
| [R16-P66-17](packets/R16-P66-17.md) Generic recipe discovery, typed fill and normal submission | CC-5 (a) | astrid-agent | X | R16-P66-16 |
| [R16-P66-18](packets/R16-P66-18.md) Ship and prove recipes for existing features | CC-5 (b) | astrid-agent | X | R16-P66-17 |
| [R16-P66-19](packets/R16-P66-19.md) Rewrite general H3 skill and thin Recast | CC-6 | astrid-agent | S | R16-P66-18 |
| [R16-P66-R](packets/R16-P66-R.md) Close compiler foundation | R | astrid-agent (Lead) | S | R16-P66-19, R16-P66-16 |

### Proposed H3 Plan 68 queue

| Packet | Task slice | Repository | Route | Depends (accepted) |
| --- | --- | --- | --- | --- |
| [R16-P68-01](packets/R16-P68-01.md) Soft timed guides through the ordered guide seam | CC-4 | astrid-agent | X | R16-P66-R |
| [R16-P68-02](packets/R16-P68-02.md) Full-canvas source and still chunk ownership | CC-8 (a) | astrid-agent | X | R16-P68-01 |
| [R16-P68-03](packets/R16-P68-03.md) Exact still masks and delivered holds | CC-8 (b) | astrid-agent | X | R16-P68-02 |
| [R16-P68-04](packets/R16-P68-04.md) Guide and still recipes and producer handoff | CC-11 | astrid-agent | S | R16-P68-03 |

### Proposed H3 Plan 70 queue

| Packet | Task slice | Repository | Route | Depends (accepted) |
| --- | --- | --- | --- | --- |
| [R16-P70-01](packets/R16-P70-01.md) Compare full-canvas vs motion-context preparation | CC-7a (a) | astrid-agent (Lead) | S | R16-P68-04 |
| [R16-P70-02](packets/R16-P70-02.md) Port active prefix continuation | CC-7a (b) | astrid-agent | S | R16-P70-01 |
| [R16-P70-03](packets/R16-P70-03.md) Bridge placed clips through the same arrangement function | CC-7b | astrid-agent | S | R16-P70-02 |
| [R16-P70-04](packets/R16-P70-04.md) Insert a placed clip between generated spans | CC-7c | astrid-agent | S | R16-P70-03 |
| [R16-P70-05](packets/R16-P70-05.md) Remove captured workflow and inert flag | CC-7d | astrid-agent | S | R16-P70-04 |
| [R16-P70-06](packets/R16-P70-06.md) Native continuation recipes and final skill trim | CC-12 | astrid-agent | S | R16-P70-05 |
| [R16-P70-R](packets/R16-P70-R.md) Independent integrated native H3 review | R | astrid-agent (Lead) | S | R16-P70-06 |

### Proposed H3 Plan 67 queue

| Packet | Task slice | Repository | Route | Depends (accepted) |
| --- | --- | --- | --- | --- |
| [R16-P67-01](packets/R16-P67-01.md) Independent provider/admission/default boundary review | CS-0 (a) | astrid-agent (Lead) | S | R16-P66-R |
| [R16-P67-02](packets/R16-P67-02.md) Staged extension admission and owner dependency | CS-0 (b; P17 P1 subset) | astrid-agent | X | R16-P67-01 |
| [R16-P67-03](packets/R16-P67-03.md) Trusted effective contribution and worker admission | CS-0 (c; only proven gap) | astrid-agent | S | R16-P67-02 |
| [R16-P67-04](packets/R16-P67-04.md) Pure generic default-companion selection | CS-10 (a) | astrid-agent | X | R16-P67-01 |
| [R16-P67-05](packets/R16-P67-05.md) Use one existing consent and default transaction | CS-10 (b) | astrid-agent | X | R16-P67-04, R16-P67-02 |
| [R16-P67-06](packets/R16-P67-06.md) H3-owned provider point and host injection | CS-1 (a) | astrid-agent | X | R16-P67-03, R16-P70-R |
| [R16-P67-07](packets/R16-P67-07.md) Independent NKD package root | CS-1 (b) | poms_packs | N | R16-P67-06 |
| [R16-P67-08](packets/R16-P67-08.md) Pinned NKD object-info schema evidence | CS-1 (c) | VibeComfy | N | R16-P67-01 |
| [R16-P67-09](packets/R16-P67-09.md) Used-only NKD requirements and soft default declaration | CS-1 (d) | astrid-agent | X | R16-P67-07, R16-P67-08, R16-P67-05 |
| [R16-P67-10](packets/R16-P67-10.md) Timed prompts use existing text mechanism | CS-2 | astrid-agent | X | R16-P70-R |
| [R16-P67-11](packets/R16-P67-11.md) Report actual reference tag and intended actor | CS-6 | astrid-agent | N | R16-P67-10 |
| [R16-P67-12](packets/R16-P67-12.md) ControlNet lowering or honest unsupported refusal | CS-5 | astrid-agent | S | R16-P67-11 |
| [R16-P67-13](packets/R16-P67-13.md) LoRA phase only if H3 hook is proven | CS-7 | astrid-agent | X | R16-P67-12 |
| [R16-P67-14](packets/R16-P67-14.md) Guide denoise phase through the existing guide function | CS-3 (stock decision; external fallback conditional) | astrid-agent | X | R16-P67-13, R16-P68-04 |
| [R16-P67-15](packets/R16-P67-15.md) Real independent NKD curve action | CS-4; CS-3 fallback if 14 requires it | poms_packs | X | R16-P67-14, R16-P67-07, R16-P67-09 |
| [R16-P67-16](packets/R16-P67-16.md) Native steering recipes and skill | CS-8 (a) | astrid-agent | S | R16-P67-14, R16-P70-R |
| [R16-P67-17](packets/R16-P67-17.md) Provider-owned recipes and guidance | CS-8 (b) | poms_packs | S | R16-P67-16, R16-P67-15 |
| [R16-P67-18](packets/R16-P67-18.md) Prove real release default delivery and opt-out | CS-11 | astrid-agent (Lead) | X | R16-P67-17, R16-P67-05 |
| [R16-P67-19](packets/R16-P67-19.md) Installed shared and chained toolkit proof | CS-9 (a) | astrid-agent | S | R16-P67-18 |
| [R16-P67-20](packets/R16-P67-20.md) Controller and worker exact provider custody | CS-9 (b) | astrid-agent | S | R16-P67-19 |
| [R16-P67-R](packets/R16-P67-R.md) Independent close of default-provider programme | R | astrid-agent (Lead) | S | R16-P67-20, R16-P67-18, R16-P67-17 |

## Proposed R16 readiness — pending scope agreement and dispatch

The brief holds strategy; each plan's tasks hold work and progress. This section records current readiness, branch/function reservations, scarce proof slots and source/pin deltas. It does not start a run. Reconfirm the existing Lead and each carried custodian before dispatch; preserve R15 priority, the P91 R17 handoff and held P82 authority.

1. Establish the current served/predecessor/candidate register and actual old origins. Confirm narrow owner decisions: qualification mode, retained P89 gate, Windows route, P38 role scope, and grant restore/revoke policy. Independent inventory, fixtures, native feasibility and bounded implementation preparation proceed together once authorized.
2. Fill every ready nonconflicting work package: records/protection; native update/Pinokio/systemd; provider/closure; state/grants; existing and managed environments/exact plan; save model/corpus/capture; streaming media; pack/output/recovery; bounded paid safety; comparable evidence using existing measurement drivers. For each, link canonical task IDs, current branch/function holder, exact predecessor, next landing contract and proof venue. A different function in the same file is not a blanket conflict.
3. Hold only real joins: provider/schema review before dependent consumer landing; exact authorization before privileged apply; verified migration before retirement; individual inverse feasibility before batching; actual native engine authority before lifecycle proof. Start fixtures, adapters and venue discovery before those joins where useful.
4. Record two interim vertical checkpoints independently: existing-environment first creation with decline/consent; substantial import/edit/recovery/undo/reopen/short-render/next-render. Record exact tuples and limits. These are internal integration evidence, not shipment or automatic final acceptance.
5. Converge all retained outcomes, P56 residuals and bounded adjunct product changes through one pin integrator. Rehearse changed-schema lived-in update/rollback, grant/state recovery, native custody and generated publication. Resolve unknown causes; preserve original task history. Name current resource reservations and actual waits, not a new task list.
6. Freeze exact product/Runtime/client/schema/pack/bootstrap/launcher/engine identities after required landings and code/interface reviews. Qualify the retained support/negative matrix, actual served origins, heavy and native journeys; require complete comparable inventories and effective required checks. Then complete RL-R and final qualification reviews on that evidence before the owner's go. Rerun only affected evidence when inputs move, with explicit impact rationale; do not silently carry old passes.
7. Owner approves one exact tuple and ledger. P31 performs one protected Final transition and coherent generated sync/deploy, then verifies complete served bytes and live identity. Plans do not publish separately. Retain named post-live owner observations/administrative closure without pretending they happened before publication.

**Conditional critical path (proposal):** reviewed producer/identity/schema/grant contracts → slowest retained native custody, managed/exact workflow, save/inverse/migration, media/output or install/update consumer → coherent pin convergence → exact-tuple changed-schema/native/support/negative/heavy proof → RL-R and required final reviews → owner go → one protected Final/deploy and served readback. This is conditional on measured work and venue availability, not a committed duration.

**Shared-function reservations:** the existing Lead records the actual holder, branch/function, next landing contract and proof venue when each lane is authorized and ready. Reserve the P38 Runtime lock, P90/P56 workflow command and schema, readiness/error case table, P63 outcome/queue mutation, shared media add/placement, pack/schema generator, and release pins/publication writer individually. No holder, branch, date or capacity is assigned by this proposed section. Independent fixtures and venue discovery can start before these joins once authorized.

At every check-in: read all current mailbox messages; reconcile predecessor moves, task receipts, exact writer conflicts and proof availability; start ready work within actual authorized capacity; report blocked contracts/resources with owner and next action. Agent CI remains subject to existing shared authority and the current Release Lead's priority and capacity decisions. P91's historical launch text is not new R16 authorization. No new permanent scheduler, strategy file or tracker is introduced.

## Delivery: Lead and managers

How Release 16 runs unattended for days. **All judgment happens once, in advance, before anyone is left running; every brief is prepared in [briefs/](briefs/README.md).** After that, each role repeats one short loop. This section is each role's whole job for this run: where it differs from a skill, this section wins. Don't open the skills to look for more work.

| Role | Runs in | Every | Job |
|---|---|---|---|
| Lead (`r16-lead`) | Codex | hour | Sends one Luna per active plan to run the plan loop; acts on what comes back; sends Sol for capped fixes; merges finished plans. It reads only one-line results, never code or logs. |
| Manager (`r16-p<PP>-manager`) | Codex, one per active plan | hour | Starts the next packet in a new ChatGPT chat, and resumes or replaces silent chats. |
| Packet (`R16-P<PP>-<nn>-<n>`) | a normal chat in ChatGPT on the web, opened by its manager in the browser | — | Writes one packet's code and tests, runs its Proof command in the chat, and pushes code and result to its branch after each task. |

**Packets go only to a normal chat in ChatGPT on the web:** the manager opens chatgpt.com in its browser, signed in to the owner's own account. Never ChatGPT for Work, never Codex. The mode follows the packet's Route, every time:

| Route | The task is | ChatGPT mode |
|---|---|---|
| N | normal | High |
| X | hard | Extra High |
| S | very hard | Pro |

Never one mode for everything. If a mode isn't offered, use the next one up; if none is, post `PARKED <packet>: mode not offered`.

### The six rules

1. **The queue is fixed.** Every packet is written in advance, in order. Nobody running the release adds, splits, re-scopes or reorders work. A plan is **finished** when every packet in it is Done or Parked.
2. **Proof runs where the code is written, and is pushed with it.** Every packet names one **Proof:** command. The packet runs it in its own ChatGPT chat (Sol in its own sandbox) and pushes to its branch on GitHub after each task. The commit that finishes the packet carries the result as its last line: `Proof: <command> — PASS <summary>`. That pushed line on the head is the proof, and nobody re-runs it. Nothing runs on a machine we set up, and nobody dispatches hosted CI.
3. **Every loop has a cap.** At the cap, mark the item **Parked**, post one line saying why, and move on. Parked work waits for the owner; everything else keeps moving.
4. **Park, don't ask.** A question this section doesn't answer is parked, never debated. Nobody waits for an answer.
5. **Replace once, then park.** A silent packet chat or manager is resumed or nudged once, then replaced once. A second need parks it. The state is on GitHub, not in the chat.
6. **A missed check isn't made up.** If your scheduled check didn't fire, run the loop once now; don't backfill.

### Never, at any level

- Write evidence files, receipts, audits, readbacks, summaries or re-verifications. A one-line board comment is the whole record.
- Clone, build or run tests outside a packet chat, dispatch hosted CI, or collect proof of any other kind.
- Edit plans, `tasks.md`, skills, this section or `releases/16.md`. The planning session reconciles `tasks.md` when the run ends.
- Start a new plan, investigation, review or document.
- Rebase, force-push, or create a branch outside the table below.
- Spend money, or use the owner's machine or media.

### Branches

| Branch | Who creates it | Who merges into it |
|---|---|---|
| `release/16/main` | the Lead, at start-up, from `release/15/main` | the Lead, when a plan is finished |
| `release/16/plan-<PP>` | the Lead, when it starts that plan, from `release/16/main` | a Luna on a valid PASS; the Lead, merging `release/16/main` in when the plan is finished |
| `p<PP>/<packet-id>` | the packet chat, from its plan branch's head | nobody: it is the PR's head |

Merge, never rebase. A PR always targets its plan branch. Push after each task. Before posting READY, the packet merges its plan branch's head in, runs the Proof, and pushes.

### Where things are, and the commands

Use these commands, exactly. `<repo>` is the product repository a packet names (`astrid-agent`, `astrid-runtime`, `astrid-app` or `VibeComfy`). Every board is an issue in `banodoco/astrid-dev`, and packets and this section live there too.

| To | Run |
|---|---|
| Find a board's issue number | `gh api "search/issues?q=repo:banodoco/astrid-dev+is:issue+is:open+in:title+%22board:+release+16+lead%22" --jq '.items[]\|[.number,.title]\|@tsv'` (put the board's title in place of `lead`, e.g. `plan+63`) |
| Read a board after a cursor (0 for the whole board) | `gh api "repos/banodoco/astrid-dev/issues/<issue>/comments?per_page=100" --paginate --jq '.[] \| select(.id > <cursor>) \| "\(.id) \(.created_at) \(.body)"'` |
| Read a file on astrid-dev `main`, such as a packet | `gh api repos/banodoco/astrid-dev/contents/<path> --jq .content \| base64 -d` |
| Post on a board | `gh issue comment <issue> -R banodoco/astrid-dev --body "<text>"`; start every comment with your mailbox name |
| A PR's changed files | `gh pr view <PR> -R banodoco/<repo> --json files --jq '.files[].path'` |
| A head commit's last line | `gh api repos/banodoco/<repo>/commits/<head> --jq .commit.message \| tail -n 1` |
| A branch's last commit time | `gh api repos/banodoco/<repo>/commits/<branch> --jq .commit.committer.date` |
| Whether a PR merges cleanly | `gh pr view <PR> -R banodoco/<repo> --json mergeable --jq .mergeable` (`MERGEABLE` is clean) |
| Merge a PR into its plan branch | `gh pr merge <PR> -R banodoco/<repo> --merge` |
| Create a branch from another, if it doesn't exist (a 422 "already exists" reply is fine) | `gh api repos/banodoco/<repo>/git/refs -f ref=refs/heads/<new> -f sha="$(gh api repos/banodoco/<repo>/git/ref/heads/<from> --jq .object.sha)"` |
| Open a board | `gh issue create -R banodoco/astrid-dev --title "<title>" --body "$(gh api repos/banodoco/astrid-dev/contents/releases/16/briefs/board.md --jq .content \| base64 -d)"` |
| Merge one branch into another | `gh api repos/banodoco/<repo>/merges -f base=<into> -f head=<from>`; a 409 reply is a conflict, so park, never resolve it by hand |

Your mailbox name is only the name you sign with; there is no other mailbox.

**The Codex side** (creating a session, sending it its brief, your hourly scheduled task, sending a Luna or Sol helper and getting its one-line final reply, and the manager's browser) is recorded in the toolkit table below. Use the newest Luna model for plan loops and the newest Sol model for Sol briefs.

| Role | To | How (from the Lead board's TOOLKIT comments) |
|---|---|---|
| Lead and manager | Schedule your hourly check | — |
| Lead | Create a manager session and send it its brief | — |
| Lead | Send a Luna or Sol helper and read its final reply | — |
| Manager | Open a new ChatGPT chat on the web, pick its mode and name it | — |
| Manager | Resume an existing ChatGPT chat | — |
| Packet | Read the repository, push a branch, open a draft PR and comment, through the chat's GitHub connector | — |

**Toolkit check, the first time each role starts:** first read the Lead board's `TOOLKIT` comments; a row already recorded there is just followed. For a row not yet recorded, your first real use of it is the trial: the Lead's first manager is the real one, a manager's first chat is its first packet, and the Sol row is recorded the first time a Sol is sent. Once a row works, post one comment on the Lead board: `TOOLKIT <row>: <the exact steps that worked>`. A row you can't do is one `PARKED <role>: can't <row>` for the owner. The comments are the record; the table only lists the rows.

The recorded steps for these rows are in the [Codex app guide](../../agent/guides/codex-app/README.md).

**The packet row** is proved by the first packet's early STATUS. If that packet instead posts BLOCKED because the chat can't reach GitHub, the manager posts `PARKED plan <PP>: packet chats can't reach GitHub`, and the Lead starts no more managers until the owner answers.

### Packet states

| State | Set by | When |
|---|---|---|
| Queued | prepared in advance | written, waiting its turn |
| Running | the manager | its chat has started; Rework 1 and 2 count as Running |
| Ready | the packet | it posted READY, and its head commit ends with a PASS line |
| Rework 1, Rework 2 | a Luna | the PASS wasn't valid, or the result was FAIL |
| Sol | the Lead | it failed after Rework 2, or posted BLOCKED; Sol has one try, and the manager leaves it alone |
| Done | a Luna | a valid PASS, merged into the plan branch |
| Parked | whoever hits a cap | it frees its slot, and the Luna parks each packet that depends on it |

**Every park is one comment on the plan's board:** `PARKED <packet or plan <PP>>: <reason>`. A parked plan gets no new packets.

The live state is the newest STATUS on each plan's board. Each role's own last STATUS is its memory: it carries what was nudged, resumed and replaced. Nobody keeps a second copy.

### Prepared in advance (before the Lead starts)

A planning session prepares this with the owner; no running role does it, and preparing it again is the only way to change the run. The Lead does everything after it.
1. Choose the plans for this run. Take only plans whose owner decisions are answered and whose packets can all be proved on CPU inside a chat. Everything needing real hardware, a real install or the network stays out.
2. For each plan, write every packet under `releases/16/packets/R16-P<PP>-<nn>.md`. Each packet has:
   - one contract, about three hours;
   - **Repository**, **Route** and **Depends** (earlier packets of the same plan only);
   - **May touch** and **Must not touch**;
   - **Files to load:** everything the chat needs to run the proof;
   - one **Proof:** command that runs only the narrow tests of the code this packet changes: its own module's tests and the new ones it writes, never a broad suite or an external or integration test. The tests need no network and run on CPU, inside the chat, in under 10 minutes.
   Packets that touch the same file get a Depends link. Plans in one run touch no file in common. Review stops (RS, R) are packets too.
3. Fill in the Plans table and each plan's queue table below, in dispatch order.
4. The owner pastes [briefs/lead.md](briefs/lead.md) into a new Codex session. The earlier Release 16 Lead (`session_011EzfW1C63rxLXsL6TkHHVV`) stands down.

### Plans

**Active at once:** four plans in ChatGPT, one chat each (owner, 28 November 2026, replacing the two of 26 November); the H3 lane runs beside them under its own brief. When a plan finishes or is parked, the Lead starts the next plan in this table whose **Starts after** plan is done or parked.

| Order | Plan | Starts after | Repositories for its branches | Queue |
|---|---|---|---|---|
| 1 | 93 ComfyUI Desktop and existing environments | — (first) | astrid-agent | [Plan 93 queue](#plan-93-queue) |
| 2 | 35 One home for user state | — (first) | astrid-agent, astrid-runtime | [Plan 35 queue](#plan-35-queue) |
| 3 | 94 Dependable environment setup and recovery | 93 | astrid-agent | [Plan 94 queue](#plan-94-queue) |
| 4 | 38 One process identity (its CPU half) | 35 | astrid-runtime, astrid-agent | [Plan 38 queue](#plan-38-queue) |

### Queues

One table per plan, in dispatch order. A manager starts them in this order and no other.

#### Plan 93 queue

| Packet | Repository | Route | Depends |
|---|---|---|---|
| [R16-P93-01](packets/R16-P93-01.md) Redacted Desktop states as fixtures | astrid-agent | N | none |
| [R16-P93-02](packets/R16-P93-02.md) The readiness ladder in the envelope | astrid-agent | X | none |
| [R16-P93-03](packets/R16-P93-03.md) Observing the four existing-install rungs | astrid-agent | X | R16-P93-02 |
| [R16-P93-04](packets/R16-P93-04.md) `generate targets` probes before it says ready | astrid-agent | N | R16-P93-03 |
| [R16-P93-RS1](packets/R16-P93-RS1.md) Review stop on the ladder | astrid-agent | S | R16-P93-02, R16-P93-03, R16-P93-04 |
| [R16-P93-05](packets/R16-P93-05.md) Telling ComfyUI Desktop's states apart | astrid-agent | X | R16-P93-RS1, R16-P93-01 |
| [R16-P93-06](packets/R16-P93-06.md) The scan checks every responder and reports installations | astrid-agent | X | R16-P93-05 |
| [R16-P93-07](packets/R16-P93-07.md) Desktop states on the ladder, with their next actions | astrid-agent | X | R16-P93-05 |
| [R16-P93-08](packets/R16-P93-08.md) `generate targets` uses Desktop's state, and attaches only on a yes | astrid-agent | X | R16-P93-04, R16-P93-06, R16-P93-07 |
| [R16-P93-09](packets/R16-P93-09.md) The setup and VibeComfy skills run `generate targets` and do its next action | astrid-agent | N | R16-P93-08 |
| [R16-P93-10](packets/R16-P93-10.md) The states in the words the person reads | astrid-agent | N | R16-P93-09 |
| [R16-P93-R](packets/R16-P93-R.md) Final review of Plan 93 | astrid-agent | S | R16-P93-01, R16-P93-02, R16-P93-03, R16-P93-04, R16-P93-RS1, R16-P93-05, R16-P93-06, R16-P93-07, R16-P93-08, R16-P93-09, R16-P93-10 |

Each packet's file holds its May touch, Files to load and Proof.

#### Plan 35 queue

| Packet | Repository | Route | Depends |
|---|---|---|---|
| [R16-P35-01](packets/R16-P35-01.md) One helper for Runtime user-state documents | astrid-agent | N | none |
| [R16-P35-02](packets/R16-P35-02.md) One-time import with a receipt | astrid-agent | X | R16-P35-01 |
| [R16-P35-03](packets/R16-P35-03.md) Protected grant ledger with revoke and reapprove | astrid-runtime | X | none |
| [R16-P35-04](packets/R16-P35-04.md) State survives backup and restore (Runtime proof) | astrid-runtime | N | R16-P35-03 |
| [R16-P35-RS1](packets/R16-P35-RS1.md) Review of the Runtime state and grant work | astrid-runtime | S | R16-P35-03, R16-P35-04 |
| [R16-P35-05](packets/R16-P35-05.md) Check that flags a new user-state side store | astrid-agent | N | none |
| [R16-P35-06](packets/R16-P35-06.md) User choices document with a safe mirror rule | astrid-agent | X | R16-P35-02 |
| [R16-P35-07](packets/R16-P35-07.md) Skills opt-outs read from and mirrored to the Runtime | astrid-agent | N | R16-P35-06 |
| [R16-P35-08](packets/R16-P35-08.md) Compute profiles in the Runtime, with one import | astrid-agent | N | R16-P35-02 |
| [R16-P35-09](packets/R16-P35-09.md) Removal date for the old VibeComfy TOML import | astrid-agent | N | none |
| [R16-P35-R](packets/R16-P35-R.md) Review of the Agent state work | astrid-agent | S | R16-P35-01, R16-P35-02, R16-P35-05, R16-P35-06, R16-P35-07, R16-P35-08, R16-P35-09 |

Each packet's file holds its May touch, Files to load and Proof.

#### Plan 94 queue

| Packet | Repository | Route | Depends |
|---|---|---|---|
| [R16-P94-01](packets/R16-P94-01.md) CPU fixtures for the starting states | astrid-agent | N | none |
| [R16-P94-02](packets/R16-P94-02.md) The computes probe and its causes | astrid-agent | X | none |
| [R16-P94-03](packets/R16-P94-03.md) Peak-space check before any write, in the model download | astrid-agent | N | R16-P94-01 |
| [R16-P94-04](packets/R16-P94-04.md) One progress line and named failures in the model download | astrid-agent | N | R16-P94-03 |
| [R16-P94-05](packets/R16-P94-05.md) No model transfer after a failed computes check | astrid-agent | N | R16-P94-02, R16-P94-04 |
| [R16-P94-06](packets/R16-P94-06.md) The Portable pin and the install offer | astrid-agent | N | R16-P94-01 |
| [R16-P94-07](packets/R16-P94-07.md) The resumable install: journal and consent | astrid-agent | S | R16-P94-06 |
| [R16-P94-08](packets/R16-P94-08.md) The real download and unpack steps | astrid-agent | X | R16-P94-07 |
| [R16-P94-09](packets/R16-P94-09.md) Attach the new install, with the old choice kept | astrid-agent | N | R16-P94-08 |
| [R16-P94-10](packets/R16-P94-10.md) The one install command | astrid-agent | N | R16-P94-09 |
| [R16-P94-11](packets/R16-P94-11.md) The install offer as the ladder's next action | astrid-agent | X | R16-P94-10 |
| [R16-P94-RS1](packets/R16-P94-RS1.md) Review the install's write and consent boundary | astrid-agent | S | R16-P94-06, R16-P94-07, R16-P94-08, R16-P94-09, R16-P94-10, R16-P94-11 |
| [R16-P94-12](packets/R16-P94-12.md) The computes rung on the ladder | astrid-agent | X | R16-P94-02, R16-P94-11 |
| [R16-P94-13](packets/R16-P94-13.md) The setup skill's no-target branch | astrid-agent | N | R16-P94-10, R16-P94-11 |
| [R16-P94-R](packets/R16-P94-R.md) Final local review | astrid-agent | S | R16-P94-01, R16-P94-02, R16-P94-03, R16-P94-04, R16-P94-05, R16-P94-06, R16-P94-07, R16-P94-08, R16-P94-09, R16-P94-10, R16-P94-11, R16-P94-12, R16-P94-13, R16-P94-RS1 |

Each packet's file holds its May touch, Files to load and Proof.

#### Plan 38 queue

| Packet | Repository | Route | Depends |
|---|---|---|---|
| [R16-P38-01](packets/R16-P38-01.md) One closure definition file with golden vectors (Runtime) | astrid-runtime | X | none |
| [R16-P38-02](packets/R16-P38-02.md) Process-binding provider API (Linux and Windows delegation) | astrid-runtime | X | none |
| [R16-P38-03](packets/R16-P38-03.md) Linux peer authority retained through a pidfd | astrid-runtime | S | R16-P38-02 |
| [R16-P38-04](packets/R16-P38-04.md) Linux birth helpers, zombie witness and census in the provider | astrid-runtime | N | R16-P38-03 |
| [R16-P38-RS1](packets/R16-P38-RS1.md) Review stop after the provider | astrid-runtime | S | R16-P38-01, R16-P38-02, R16-P38-03, R16-P38-04 |
| [R16-P38-05](packets/R16-P38-05.md) Linux boundary tests carry the pidfd mark; a named refusal gate | astrid-runtime | N | R16-P38-RS1 |
| [R16-P38-06](packets/R16-P38-06.md) Stale-owner tests use well-formed Linux births | astrid-runtime | N | R16-P38-RS1 |
| [R16-P38-07](packets/R16-P38-07.md) Runtime one-implementation guard | astrid-runtime | N | R16-P38-01, R16-P38-02, R16-P38-03, R16-P38-04, R16-P38-05 |
| [R16-P38-08](packets/R16-P38-08.md) Agent closure reads the shared definition | astrid-agent | N | R16-P38-01, R16-P38-RS1 |
| [R16-P38-09](packets/R16-P38-09.md) Agent custody uses the provider on Linux and Windows | astrid-agent | X | R16-P38-02, R16-P38-03, R16-P38-RS1 |
| [R16-P38-10](packets/R16-P38-10.md) Agent birth ids and Linux census from the provider | astrid-agent | X | R16-P38-04, R16-P38-09 |
| [R16-P38-11](packets/R16-P38-11.md) Remaining Agent birth readers go through the provider | astrid-agent | N | R16-P38-10 |
| [R16-P38-12](packets/R16-P38-12.md) Agent one-implementation guard | astrid-agent | N | R16-P38-08, R16-P38-09, R16-P38-10, R16-P38-11 |
| [R16-P38-R](packets/R16-P38-R.md) Final review of phase 1 (both repositories) | astrid-runtime and astrid-agent (work in the Agent checkout; the Runtime checkout is `../astrid-runtime/`) | S | R16-P38-RS1, R16-P38-01, R16-P38-02, R16-P38-03, R16-P38-04, R16-P38-05, R16-P38-06, R16-P38-07, R16-P38-08, R16-P38-09, R16-P38-10, R16-P38-11, R16-P38-12 |
| [R16-P38-13](packets/R16-P38-13.md) Shared role-custody base in runtime_protocol (Runtime) | astrid-runtime | N | R16-P38-07, R16-P38-R |
| [R16-P38-14](packets/R16-P38-14.md) Agent broker imports the shared role-custody base | astrid-agent | N | R16-P38-13, R16-P38-12 |
| [R16-P38-R2](packets/R16-P38-R2.md) Review of the shared role-custody base (both repositories) | astrid-runtime and astrid-agent (work in the Agent checkout; the Runtime checkout is `../astrid-runtime/`) | S | R16-P38-13, R16-P38-14 |

Each packet's file holds its May touch, Files to load and Proof.


### The Lead — every hour

**Job:** run the plan loops through Lunas, act on their flags, and merge finished plans. Nothing else.

1. **Read** your own last STATUS, and new comments on your board after its cursor. If the Plans table names no plans, nothing was prepared: post `PARKED lead: nothing prepared` and stop.
2. **Send one Luna per active plan,** all at once, each sent [briefs/luna.md](briefs/luna.md) with that plan's last result line. Wait for each one's single result line. A Luna that hasn't returned its final reply within 30 minutes, or by the end of your check, leaves that plan's line as it was, with `no-result` raised by one; at `no-result 2`, park the plan. A result resets it to 0.
3. **Act on each flag** in the results:
   - `SOL <packet>: <reason>` → post `SOL <packet>` on the plan's board, then send one Sol [briefs/sol.md](briefs/sol.md) with that reason;
   - `NO-CHATS <PP>` → add it to "for the owner", and do nothing else;
   - `REPLACE manager <PP>` → replace that manager, once, and add `manager replaced` to its line; if it was already replaced, park the plan;
   - `FINISHED <PP>` → in each repository the Plans table lists for it, merge `release/16/main` into the plan branch, then the plan branch into `release/16/main`. If either won't merge cleanly, park the plan. Then start the plan whose Starts after names it, as step 6 of [briefs/lead.md](briefs/lead.md) says; do the same when a plan is parked.
4. **Parked:** copy any new Parked lines into your STATUS, under "for the owner". Don't solve them.
5. **Post** one STATUS on your board, then stop until the next check:

   ```text
   STATUS r16-lead | <each active plan's last result line, with no-result <n> and manager replaced if so> | … | sol: <packet and time sent, or none> | merged to release/16/main: <plans or none> | managers: <PP>=<session>, … | plans done: <list> | plans parked: <list> | for the owner: <parked and NO-CHATS lines, or none> | cursor: <last comment id on your board>
   ```

**Never:** read code, diffs or logs yourself, run tests, write or reorder packets, answer technical questions, or change a plan.

### Plan loop and Sol

Each Luna runs the plan loop in [briefs/luna.md](briefs/luna.md) and replies with one line. Each Sol follows [briefs/sol.md](briefs/sol.md), with one try per packet.

### The manager — every hour

**Job:** start the next packet. You are a dispatcher, not a reviewer.

1. **Read** your own last STATUS, then new comments on your plan's board, after your cursor. Drop each packet posted as `PARKED`, `DONE` or `SOL` from your Running list: a SOL packet is Sol's, not yours. If the plan itself is parked, post a final STATUS and stop.
2. **Each REWORK** on the board: send it to that packet's chat. If that chat won't load, use a new chat at the PR's head.
3. **Each Running packet** with no commit and no post for 3 hours, counted from the later of those and your last resume or replacement of it:
   - send the resume message;
   - if it was already resumed, replace the chat, once;
   - if the replacement goes silent too, post `PARKED <packet>: silent after replacement`;
   - a packet Running for 8 hours in all without READY: post `PARKED <packet>: no READY in 8 hours`.
4. **Free slots:** at most three packets per plan Running. A replaced chat counts as closed. If the account refuses a new chat, post `NO-CHATS` and try again at the next check. Fill them with Queued packets, in queue order, whose Depends are all Done. Each packet gets a NEW normal chat in ChatGPT on the web, opened at chatgpt.com in your browser (never ChatGPT for Work, never Codex), in its Route's mode: N High, X Extra High, S Pro. Send it [briefs/packet.md](briefs/packet.md) filled in, and name it `<packet id>-<n>`, for example `R16-P63-01-1`. Your first packet goes alone, until it posts its first STATUS.
5. **Post** one STATUS, then stop until the next check:

   ```text
   STATUS r16-p<PP>-manager | running: <id since time, …> | chats: <packet>=<chat name and link>, … | next: <id> | started: <ids or none> | resumed ever: <ids> | replaced ever: <ids> | cursor: <id>
   ```

**Never:** edit the repository, merge, judge code, answer a packet's question, or start packets out of order.

### Briefs and fixed messages

Every message is prepared in [briefs/](briefs/README.md): the Lead's, the manager's, the packet's, the Luna's and the Sol's briefs, the board header, and the nudge, resume, rework and replace messages. Fill in the `{NAME}`s; never write a different message.

### The owner's check-ins

Once a day, read the newest STATUS on `board: release 16 lead`. "For the owner" lists everything parked. If that STATUS is over 2 hours old, the Lead has stopped: paste [briefs/lead.md](briefs/lead.md) into a fresh session, adding the Replace line from [briefs/messages.md](briefs/messages.md); it starts no new managers. Answer parked items there; to change the run, prepare it again.

## Now (11:20 UTC, Tue 24 Nov; historical before the scope change)

Release 16 is a draft. Plan 91 (Agent main green) runs now as its own lane, moved here from Release 15 by the owner on 24 November 2026; its section is below. The Release 16 Lead is `session_011EzfW1C63rxLXsL6TkHHVV`.

## Plan 91 dispatch

Added 24 November 2026. The owner started [Plan 91](../../plans/91-agent-main-green/plan.md) in its orchestrator's session and confirmed its D1 and D3–D15. The same day, in the Release 15 Lead's session, she moved it to Release 16 (D1, "Move Plan 91 to Release 16"): it runs now, at the same pace, and targets `release/16/main` from the start. It works like Release 15's [Plans 87 and 89 dispatch](../15/run.md#plans-87-and-89-dispatch), with the same roles, standing rulings, manager startup checks and cadence, and with the names and differences below. The [Run start](../../plans/91-agent-main-green/inputs.md#planning-evidence) holds the owner's authority.

| Plan | Mailbox | Run | Orchestrator | Manager |
|---|---|---|---|---|
| 91 | [astrid-dev #1826](https://github.com/banodoco/astrid-dev/issues/1826) | `r15-p91-dispatch` | `r15-p91-orchestrator`, Claude session `session_011EzfW1yUojAfWkGcaZNRph` | `r15-p91-manager-1` |

The mailbox names keep their `r15-` prefix, as they were opened before the move. Packet sessions are `r16-P91-<nn>-<n>`.

- **Lead:** the Release 16 Lead (`session_011EzfW1C63rxLXsL6TkHHVV`). Its DECISIONs bind the orchestrator, the manager and packet sessions within this section and the Run start. Its gate covers only the landing into `release/16/main`.
- **Plan branch:** astrid-agent `release/16/plan-91`, cut by the orchestrator at `514499de` (the `release/15/main` head of 24 November). `release/16/main` is not yet cut, so the orchestrator merges `release/15/main` forward into the plan branch as it moves, and `release/16/main` once it exists. `release/15/plan-91`, cut first at the same commit, is superseded and unused. The manager's check 6 covers astrid-agent, and astrid-dev for R16-P91-06's `env/` change.
- **In the orchestrator's own lane:** AG-0 (done), AG-1 (the gate, the `workflow_dispatch` inputs and the comparison), AG-2, every hosted card run and batch run, the ceiling ratchet, RS1, R and AG-10. Packet sandboxes cannot reach `github.com`: packets post `READY-PROOF astrid-agent <PR> <head> <selectors>` and the orchestrator runs the proof.
- **Needs the owner:** changing an existing assertion beyond what Plan 91's [triage rules](../../plans/91-agent-main-green/tasks.md#triage-rules) allow; any Runtime PR or release (D8); accepting a D6 or D3 ceiling entry; turning on required checks.

### Standing rulings (Plan 91)

1. Release 15's Plans 87 and 89 rulings 1–3, 5 and 6 apply as written.
2. Release 15's [rulings for Plan 82](../15/run.md#rulings-for-plan-82) apply to Plan 91, from the Release 15 Lead's review of the first twelve merged packets:
   - packets have no network and run no hosted test, so each packet's list of already-failing IDs and its focused selectors come from AG-0's [card lists](../../plans/91-agent-main-green/evidence/release-15-514499de/cards/);
   - one contract per PR, aimed at about three hours; a larger card is delivered as consecutive PRs at its seams;
   - every packet lists what must pass unchanged, and an existing assertion changes only as the triage rules allow; a packet that finds this untrue posts `BLOCKED` once with the exact list;
   - measurement stays in the lane;
   - sweeps carry their count;
   - the orchestrator answers each `READY-PROOF` within 45 minutes, independent proofs in parallel, and reads the mailbox to the last page at every check.
3. **Comparisons are whole-run by id,** keyed by job family (`unit`, `integration`, `darwin native`, `opt-in`, and single jobs by name), never per shard: tests move between shards across runs ([AG-0](../../plans/91-agent-main-green/evidence/release-15-514499de/README.md#two-findings-for-ag-1)).
4. **Cap:** at most **five** packets in Running or Review at once (the owner's choice for this plan). The first packet goes alone, until its early STATUS shows a session can push, open a draft PR and comment.
5. **Agent CI is shared with Release 15** while it is unpublished: at most two Agent CI runs at once across both releases, and Release 15's landing gates take a slot first. The orchestrator checks the running `ci.yml` and `lanes.yml` runs before it dispatches, names its slot in each hourly report, and asks the Release 15 Lead for any slot that competes with a Release 15 gate.
6. Packets never edit `ci/agent-ceiling.tsv`. Only the orchestrator ratchets it, and only down, after a hosted batch run.

### Dispatch queue (Plan 91)

The order is tasks.md's [dispatch order](../../plans/91-agent-main-green/tasks.md#dispatch-order). Wave C packets are written after RS1 regenerates its list. Each packet names its own dependencies.

| Packet brief | Source plan/tasks | Handoff | Session | Next action / evidence |
|---|---|---|---|---|
| [R16-P91-01](packets/R16-P91-01.md) | AG-P1 (X): the prune pass, CI | Ready (first, alone) | — | One PR per area; posts kept IDs early |
| [R16-P91-02](packets/R16-P91-02.md) | AG-P2 (X): the prune pass, Lanes | Ready (after R16-P91-01's early STATUS) | — | D12's legacy archive tests retire |
| [R16-P91-03](packets/R16-P91-03.md) | AG-A8 (S): clip-level namespaced data and the reader check | Ready (design note first) | — | D13; RS1 reviews |
| [R16-P91-04](packets/R16-P91-04.md) | AG-A9 (S): rational frame rates | Ready (investigation note first) | — | D8; a Runtime PR needs the owner's go |
| [R16-P91-05](packets/R16-P91-05.md) | AG-A7 (N): fixtures write `output.resolution` | Ready | — | The largest single refusal |
| [R16-P91-06](packets/R16-P91-06.md) | AG-A1 (N): the unit shards install the Runtime editable | Ready (merges after AG-1) | — | astrid-agent, and astrid-dev `env/` |
| [R16-P91-07](packets/R16-P91-07.md) | AG-A2 (N): CI provides the tests' inputs | Blocked on R16-P91-06 merging | — | Same `ci.yml` steps |
| [R16-P91-08](packets/R16-P91-08.md) | AG-A10 (N): the fake client takes `**kwargs` | Ready | — | 0.25 days |
| [R16-P91-09](packets/R16-P91-09.md) | AG-A6 (N): the ABI-1 binding fixture | Ready | — | — |
| [R16-P91-10](packets/R16-P91-10.md) | AG-A3 (N): fixtures and resources | Ready | — | D10, D11 |
| [R16-P91-11](packets/R16-P91-11.md) | AG-A5 (X): the kept installer tests | Blocked on R16-P91-01's verdict | — | — |
| [R16-P91-12](packets/R16-P91-12.md) to [R16-P91-30](packets/R16-P91-30.md) | AG-B1 to AG-B22 (Wave B, in index order) | Ready as slots free, each after its own dependency | — | Listed in [tasks](../../plans/91-agent-main-green/tasks.md#run-decisions) |

### Manager launch message

The owner pastes this into the manager's own session (a Codex session, as for Plans 87 and 89).

```text
You are the manager for Release 16 Plan 91 (Agent main green), mailbox name r15-p91-manager-1, reporting to the Plan 91 orchestrator (mailbox name r15-p91-orchestrator, Claude session session_011EzfW1yUojAfWkGcaZNRph).
Follow agent/roles/orchestrator/multi-manager-dispatch.md in banodoco/astrid-dev, with the orchestrator as "the Lead".
Read releases/16/run.md on main, section "Plan 91 dispatch", then again at every hourly check. Ready rows link the packets.
Mailbox: https://github.com/banodoco/astrid-dev/issues/1826, format in its first post.
First do the manager startup checks (Release 15's "Manager startup checks" for Plans 87 and 89, run against #1826, for astrid-agent and astrid-dev) and post one STATUS with each result. Dispatch nothing until the orchestrator's DECISION answers it.
Then give each Ready packet a FRESH ChatGPT session in the mode its packet's Route sets (N High, X Extra High, S Pro), with the workstream's packet start message, naming the session r16-P91-<nn>-<n>. Dispatch R16-P91-01 alone first.
Every hour: read the mailbox to the last page, check every open packet, run the parallelism pass (start every Ready packet with no unmet dependency and no file conflict with a Running one, up to five in Running or Review), resume or replace stalled sessions, pass submissions and READY-PROOF posts to the orchestrator, and post one STATUS.
You may start, resume, stop and replace packet sessions and comment on the mailbox. You may not merge, edit the repository, approve anything or dispatch hosted CI. Send anything reserved to the owner to the orchestrator.
If a check fails, say which manual step the owner must do instead of promising automation.
```
