# Inputs — One model for astrid-dev's records, checks and generated pages

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — Phase 1 only. On 11 Nov 2026 the owner asked for the first phase to be handed to a manager and driven to completion, with normal, very hard and super hard tasks on Codex and taste and review on Claude ([planning session](https://claude.ai/code/session_011EzfW38XJUpUFewfUM9MxF)). Phase 2 stays unaccepted until D1 to D4 are answered; Phases 3 and 4 stay proposed (D7). On 11 Nov 2026 the owner also asked for Phases 3 and 4 to be specified to task level; that is a go to specify, not acceptance and not a go to run them ([specification](#phases-3-and-4-specification)). Also on 11 Nov 2026, with D1 to D3 decided, the owner asked for Phase 2 to be made ready to execute with Codex doing the bulk of the work; that too is a go to specify and not a go to run ([re-plan](#phase-2-re-plan-against-phase-1)).

**Prior art:** a read of every script, workflow, skill and template at astrid-dev `e27e30a`, plus two read-only surveys of all 47 packs and all 227 evidence files ([planning session](https://claude.ai/code/session_011EzfW38XJUpUFewfUM9MxF)); findings are under [What exists today](#what-exists-today). Reused: [`project_contract.py`](../../scripts/project_contract.py), [`vision_subject.py`](../../scripts/vision_subject.py), [`export_public_vision.py`](../../scripts/export_public_vision.py) and the `publish-vision` job. Overlapping plans: [Plan 31](../31-releases-from-astrid-dev/plan.md) and [Plan 44](../44-vision-execution-trail/plan.md).

**Approach:** finish the shared layer the existing scripts already imply (one helper, a check registry, a view mechanism), then move the catalog onto it. Declaring the pack shape, lifecycle, forms and evidence is proposed, not committed (D7). Alternatives compared under [Alternatives](#alternatives): do nothing; fix only the catalog; adopt a documentation framework or a database; this plan.

**Challenge:** Reviewed — one independent high-judgment critique, briefed to build as little as possible and to verify claims in code ([planning session](https://claude.ai/code/session_011EzfW38XJUpUFewfUM9MxF)). It found three blocking errors in the first draft, all fixed, and recommends a scope about a third the size; what was accepted, and what is left to the owner, is under [Critique](#critique). The Phase 3 and 4 task cards change astrid-dev's own checks, so they need their own critique before any greenlight; that second critique was done on 11 Nov 2026 by a fresh session (`session_011EzfW2YVR3oTr7E9efK4ar`) on commit `ee47263`: five blocking findings, all accepted, and a recommendation to cut most of both phases, left to the owner ([Second critique](#second-critique)). The re-planned Phase 2 cards change the completion gate, review intake, the claim bot and a workflow that pushes to `main`, so they needed a third critique: done on 11 Nov 2026 by a fresh session (`session_011EzfW3TiCsjmR3PQMUFENy`) on commit `b82baf3`, with 4 blocking findings, all accepted, and 20 more: 19 accepted and one partly, with two simplifications left for the reviews to decide ([Third critique](#third-critique)).

**Proof and limits:** see [plan.md](plan.md#completion). The proof is structural: same verdicts and a byte-identical public feed across the refactor, conflict-free parallel plan PRs, and one-file extension examples. It does not show that contributors find the result clearer beyond one fresh-agent trial.

**Review rounds:** one round on Phase 1's integrated head (row R1), under the owner's policy of 11 Nov 2026 that reviews are minimal and only for meaningful complexity; Phase 1 qualifies because every later phase and Plan 31 build on it. Pending for Phase 2 — recommend one review stop on the two contracts (RS1), one round before the cut-over (R2) and one round on the refresh job before it goes live (R8) ([why](#review-rounds-1)). Next: the owner confirms with Phase 2's run start. For Phases 3 and 4, recommend one round each (R3, R4), pending with D7 ([why](#review-rounds)).

**Ambiguity pass:** done for Phase 1 by the planner; the choices are in [tasks.md](tasks.md#phase-1-dispatch-notes). Done for Phase 2 by the planner on 11 Nov 2026 from the code on `main` at `12a54b6` ([what it resolved](#ambiguity-pass-1)); four decisions are left to the owner, D14 to D17. Done for Phases 3 and 4 by the planner from the code at `ee69971` ([what it resolved](#ambiguity-pass)); it must be repeated against Phase 2's result before dispatch.

## Owner decisions

Open unless marked decided. Each has a recommendation.

- **D1. Where does priority live once the catalog is generated?** Row order is the priority today and it is the one fact that belongs to no single project. *Recommend:* a small ordered file of project ids (`plans/priority.md`), edited only to reprioritize; a project missing from it sorts last among open work. Alternative: a numeric priority field in each plan, which makes reordering touch many files. **Decided, 11 Nov 2026:** the owner agreed: a small ordered file of project ids.
- **D2. Which field syntax do project facts use?** The repository already has two: bold lines (`**Vision gaps:** …`) in plans, gaps and releases, and plain header lines (`Date: …`) in ledger entries and PR forms. *Recommend:* bold lines at the top of `plan.md`, next to `**Vision gaps:**`, and no third syntax. Alternative: YAML front matter, which GitHub renders as a table but needs a parser the standard library does not have. **Decided, 11 Nov 2026:** the owner agreed: bold lines at the top of `plan.md`, no third syntax.
- **D3. When are generated files refreshed?** Today the author runs the generator and CI fails if the file is stale. With many open PRs each adding a plan, every one of them edits the same generated catalog and the same count line in the root README, and they conflict. *Recommend:* refresh on `main` by a bot, so PRs never contain generated output. Cost: a bot commits to `main` (needs O-1) and the page lags a merge by about a minute. Alternative: keep the stale check and accept rebases; drop PM-8. **Decided, 11 Nov 2026:** the owner agreed: a bot refreshes generated files on `main`, so PM-8 stays. It still needs the bot identity (O-1), which only the owner can set up; `main` now requires a pull request, so that identity needs a bypass.
- **D4. Do existing packs get reshaped?** Only 10 of 47 `plan.md` files use the template's headings. *Recommend:* reshape queued drafts by script, leave packs with a live run and finished packs alone, and report the drift. Alternative: check new packs only. *11 Nov 2026, from the Phase 3 specification:* only eight queued drafts can be reshaped without inventing content, and only in `plan.md` (three heading renames each); the planner now leans to the alternative, with the report. PM-11c is the row this decides. **Decided, 11 Nov 2026:** the owner agreed to check new packs only and leave existing packs as they are. PM-11c is dropped.
- **Run start (decided, 11 Nov 2026).** The owner's go covers starting Phase 1 now, not after Release 12 publishes. To keep that release safe, Phase 1 lands on `int/48-one-record-model`, the old check commands keep working, and the one PR to `main` waits for the owner's go. **Accountable session:** `session_011EzfW3FH6dvD1UHyzGnajf`, the Claude session hosting the Codex manager ([who answers for a run](../../skills/astrid-dev-shared/run-contract.md#who-answers-for-a-run)). **Without asking:** everything in Phase 1 up to opening that PR, per the owner's instruction to drive every Phase 1 task to completion. **Needs the owner's go:** merging that PR, and anything in Phase 2. **Advisor:** `session_011EzfW38XJUpUFewfUM9MxF`, for hard blocks and choices that would change scope, a check's verdict or the public feed.
- **Run start, Phase 2 (12 Nov 2026).** The owner asked on 11 Nov for the queue to be kept moving and delegated approval to the orchestrator session; she asked on 12 Nov why the run had stopped. Under that delegation the orchestrator starts Phase 2 now, on `int/48-one-record-model` cut afresh from `main`, with only the cut-over to `main` (C-1) waiting for Release 12 to publish. **Accountable session:** `session_011EzfW3FH6dvD1UHyzGnajf`, the Claude session hosting the Codex manager ([who answers for a run](../../skills/astrid-dev-shared/run-contract.md#who-answers-for-a-run)). **Manager's route:** X is recommended; that session runs on a normal-route model today, so the owner may switch its model, and until she does the orchestrator checks its merges at each check-in. **Without asking:** every Phase 2 card up to opening C-1, with Codex running the cards marked for it. **Needs a go:** C-1 and C-2, merged by the orchestrator under the delegation only after their reviews have no blocking finding and the required checks pass; O-1 is the owner's alone. **Standing go for the queue:** PM-13h, then Phase 3's track A and track B (D9). *Amended 12 Nov 2026 by the orchestrator under the same delegation:* Phase 2 was built to its cut-over in under two hours and then sat behind Release 12, so this work starts now, from its re-planned cards, on `int/48-phase3` cut from the Phase 2 candidate head. It merges to `main` only after the cut-over (C-1), by the orchestrator, after R3 has no blocking finding and the required checks pass. **Advisor:** `session_011EzfW38XJUpUFewfUM9MxF`. **Check-ins:** every three hours from the advisor, until the queue is done or the owner says stop. **Review rounds:** RS1, R2 and R8, one round each, as the re-plan recommends.
- **D5. Order against Plan 31.** *Recommend:* Phase 1 before Plan 31's RL-1a to RL-1c, so Plan 31 registers its checks and its manifest as a view. Both wait for Release 12. Alternative: Plan 31 first, then fold its scripts in (more rework, no delay to releases). **Settled by events, 11 Nov 2026:** Phase 1 reached `main` before Plan 31 started, so Plan 31 registers its checks and views ([its overlap note](../31-releases-from-astrid-dev/tasks.md)).
- **D6. Where does this sit in the catalog's order?** The row is last among the open rows, as the plan skill now says for any new plan. *Recommend:* the owner moves it directly above Plan 31 if D5 is accepted. *11 Nov 2026:* the owner first said Plan 31 would be queued after this plan's Phase 2, then withdrew that the same day: Plan 31 is not queued for now. The row stays last among the open rows, and D6 stays open.
- **D7. Do Phases 3 and 4 happen?** The owner agreed with the direction in the planning session. The critique says no recorded failure asks for a declared lifecycle, generated forms or an evidence envelope, and that their only named consumer (Plan 44) is an unscoped draft; by [principle 8](../../docs/contribution-design-principles.md) they should wait. *Recommend:* commit Phases 1 and 2 now, and decide Phases 3 and 4 after Phase 2 lands, taking PM-11 (pack shape) first because its evidence is strongest (ten of 47 plans match the template). The catalog estimate covers the committed phases, with the proposed ones stated separately. *11 Nov 2026:* the owner asked for both phases to be specified to task level, which is now done; D7 is still open, D9 offers smaller first steps than either phase, and a second critique again recommends cutting most of both. *Later on 11 Nov 2026, after reading the specification's summary:* the owner said to "queue up this project after the current is done". Recorded as: Phases 3 and 4 are wanted and queued behind the committed work (Phase 2), not started now. Which rows that covers is not yet decided: it waits for her answers to D9 to D13, and no run is authorized. **Decided, 11 Nov 2026:** yes in part, per D9. Phase 4 and Phase 3's track C stay proposed and unscheduled.
- **D8. Which gap?** Decided in part, 11 Nov 2026: the owner said the plan need not close a gap but should connect to a relevant one, and that a new one may be needed. The first draft named CA-003; the critique showed the plan delivers none of CA-003's closure evidence and Plan 44 already holds it. No existing gap covers contributing in parallel through one clear process, so this PR drafts [CA-005](../../vision/gaps/CA-005-parallel-contribution.md) and routes this plan in it. *Still open:* the owner accepts CA-005's wording and boundary in the scope PR's boundary review, or asks for the enabler line instead.
- **D9. If anything in Phases 3 and 4 is taken, what goes first, and may it start before Phase 2?** Only the lifecycle track needs Phase 2; the pack-shape and form tracks need only Phase 1 on `main`, and PM-13h needs nothing. Options: (a) nothing, until a recorded failure asks (the first critique); (b) PM-13h alone, as an ordinary fix (the second critique's floor); (c) PM-13h, then track A (PM-11a, PM-11b, PM-11t and one review round), about two days, once Phase 1 is on `main`; (d) all of Phase 3 after Phase 2, then Phase 4. *Recommend:* (c), then decide the rest on what it shows. If a track lands before Phase 2, Phase 2's cards are re-planned against it, since PM-6 edits the same template and PM-10 moves the gate that track C touches. **Decided, 11 Nov 2026:** the owner chose (c) and added track B. Accepted and queued to run after Phase 2: PM-13h; track A (PM-11a, PM-11b, PM-11t); track B without its gate (PM-12a, PM-12b, PM-12t); and one review round, R3. Not scheduled, kept specified: track C (PM-13a, PM-13b, PM-13t) and Phase 4. Dropped: PM-11c (D4) and PM-12c (D10). Because track A now runs after Phase 2 instead of before it, its cards are re-planned against Phase 2's result first. No run is authorized by this decision.
- **D10. Is there a gate on status changes, and which changes does it allow?** Nothing defines this today, so it cannot be read from the code, and planning could not compare a table with history. Options: (a) no gate: keep PM-12a and PM-12b, drop PM-12c (the second critique); (b) a gate with this table: a new project starts `queued`; `queued` to `active`, `blocked`, `paused` or `cancelled`; `active` to `blocked`, `paused`, `done`, `cancelled` or back to `queued`; `blocked` to `active`, `paused`, `queued` or `cancelled`; `paused` to `active`, `queued` or `cancelled`; nothing leaves `done` or `cancelled`; and one escape, a line in the PR description, `Status correction: <folder> — <reason>`, which a reviewer sees. *Recommend:* (a) now, and (b) only after PM-12c's history check shows the table would have refused nothing legitimate. Sub-choices under (b): whether `cancelled` may return to `queued`, and whether `queued` may go straight to `done`. **Decided, 11 Nov 2026:** the owner agreed to (a), no gate now. PM-12c is dropped; (b) stays specified.
- **D11. Two questions about the envelope.** First, may a PR that asks for implementation review fail CI for an incomplete envelope? Nothing checks those PRs today. *Recommend:* yes, for PRs carrying `Review request: implementation` only. Alternative: print the block in the form and check nothing. Second, does the completion assessment take the envelope's labels? Options: (a) no: it keeps `Evidence`, `Completion`, `Integrated candidate`, `Unproven` and `Routes used`, and the envelope lives in the implementation form and the GPU record; (b) yes: rename them in one step, which also changes `scripts/model_usage.py` and its test, the run contract, `docs/contribution-workflow.md` and `templates/product-pr/review.md`, rewrites seven tests of the gate, and needs every open completion PR refilled. *Recommend:* (a). The cards are written for (a). **Decided, 11 Nov 2026:** the owner agreed to both recommendations: CI may fail an implementation review request for an incomplete envelope, and the completion assessment keeps its own labels, option (a).
- **D12. When does the GPU record change shape?** Plan 34 has run evidence on a branch in the current shape, and `validation/gpu/` holds no record on `main` yet. *Recommend:* PM-14c lands after Plan 34's first record is merged, or with its owner's agreement to add the block to it. Alternative: change the template now and have Plan 34 convert before merging. **Decided, 11 Nov 2026:** the owner agreed: PM-14c lands after Plan 34's first record is merged, or with its owner's agreement.
- **D13. What must every new pack contain?** With the templates as the declaration, a new pack needs all seven planning-evidence labels, including `Review rounds` and `Run start`, and the `## Owner decisions` section even when empty. This pack itself would not pass: its run start is a bullet under its decisions. Options: (a) everything in the template, each label with the template's own `Pending —` text until known, and `None` under Owner decisions; (b) the headings and only the five labels the older check already requires, which keeps a second list in code. *Recommend:* (a), because a draft copies the template's pending lines at no cost; but it changes what a draft must hold, so it is the owner's call before PM-11a. **Decided, 11 Nov 2026:** the owner agreed to (a), everything in the template.
- **D14. Where does a project's catalog name come from?** The catalog's project name and the plan's own title differ in 26 of 48 packs, and the public vision feed carries the catalog's name. Options: (a) a `**Project:**` line in every pack, written by the migration from today's catalog name; titles are not touched and the feed stays byte-identical; (b) the title becomes the name: the migration rewrites 26 titles to the catalog's names, including in packs with a live run, which the plan's boundary rules out; (c) the title as it stands becomes the name: 26 names change in the catalog and on the public vision page, and someone has to review them. *Recommend:* (a). It leaves one fact in two places for now (title and name), which is today's state, and a pack's owner can later make them equal. The cards are written for (a); (b) or (c) changes one function and the migration script. **Decided, 12 Nov 2026, by the orchestrator under the owner's delegation** (11 Nov: "I give you permission to approve everything"; "keep it going no matter what"): (a), a `**Project:**` line in every pack. The owner may reverse it before the cut-over.
- **D15. How is a stale PR that still edits the catalog made to fail?** `main`'s ruleset does not require a branch to be up to date, so a PR that passed its checks before the cut-over could merge after it and hand-edit a generated file, and the edit would then be lost without a word. Options: (a) the generated table keeps today's seven cells and moves the Plan link to the first column, so every row line differs from the hand-written one and any open PR that edits, adds or removes a row conflicts in git and cannot merge (the critic tried each in a scratch merge); it protects rows only, so the host also reads and comments on every open PR that touches the file; (b) the owner turns on "require branches to be up to date" for the cut-over, which stops every stale PR in the repository until it is updated, at about 150 commits a day; (c) the host's comments only, which leaves a few seconds in which a PR with auto-merge on can slip through. *Recommend:* (a): it needs no setting and cannot be missed. Its cost is a visible change to the catalog page's column order. The cards are written for (a). **Decided, 12 Nov 2026, by the orchestrator under the owner's delegation** (11 Nov: "I give you permission to approve everything"; "keep it going no matter what"): the recommended option: the Plan column first in the generated table, plus the host's sweep of open pull requests at the cut-over.
- **D16. Does the cut-over wait for the bot?** The refresh job (PM-8) needs O-1, which only the owner can do, and a hosted proof in a scratch repository. Options: (a) do not wait: the cut-over goes without the job, authors run `sync` for the days between, and PM-8 follows as a second PR (C-2) after its hosted proof and one review round of its own; (b) wait: one PR, and Phase 2 does not land until O-1 is done and the job is proven. *Recommend:* (a). The claim bot has waited on the same kind of setting since it was written; the cut-over should not, and a smaller cut-over is easier to undo. Its cost: between the two PRs, a status change is two files, not one, and no claim can be auto-merged. The cards are written for (a). **Decided, 12 Nov 2026, by the orchestrator under the owner's delegation** (11 Nov: "I give you permission to approve everything"; "keep it going no matter what"): (a), the cut-over does not wait for the bot; the refresh job is a second pull request (C-2).
- **D17. Which identity pushes generated files, and where is it proven?** D3 chose a bot that commits to `main`; `main` now requires a pull request, so a direct push needs a bypass, and GitHub cannot limit a bypass to certain files. Options: (a) a new GitHub App used for nothing else, with Contents: write only, on the ruleset's bypass list, installed also on a scratch repository with the same ruleset so the job is proven there first; (b) the claim bot's App for both jobs: one thing to set up, but one identity that can then both merge claims and push to `main`; (c) no bypass: the App opens a pull request with the refreshed files and merges it when the two checks pass, which keeps `main`'s rules whole but takes several minutes per refresh, opens a bot PR for most plan changes, and changes D3's "commits to `main`". *Recommend:* (a). What limits the App to generated files is the job's own steps (it commits only what `sync` reports and fails on anything else), which PM-8h and the review check; the owner should know that is the only limit. O-1 lists the settings. **Decided, 12 Nov 2026, by the orchestrator under the owner's delegation** (11 Nov: "I give you permission to approve everything"; "keep it going no matter what"): (a) as the design to build and prove against. Creating the identity and its bypass stays the owner's action (O-1); nothing before C-2 needs it.

## Ten statements for the owner

Offered to the owner in the planning session to show the anchors and edges; each is true of the plan as written. Reactions become decisions above.

1. Now, the list defines the plans. After, the plans define the list.
2. Now, claiming a project means editing a shared table. After, it means changing one line in that project's own file.
3. Now, a hundred people changing status collide in one file. After, nobody edits a file someone else is editing.
4. Now, a fact shown twice is sometimes generated and sometimes hand-copied and compared. After, every repeated fact is generated, with no exceptions.
5. Now, you learn what is checked by reading five scripts. After, one command prints every check, and that printout is the documentation.
6. Now, checks can pass locally and fail in CI. After, it is the same command in both places.
7. Now, adding a stage means editing a template, a skill, a PR form and a pattern. After, it is one entry in one file. (Phase 3, proposed only.)
8. Now, the template is a suggestion ten of 47 plans follow. After, a new plan that does not match the shape does not land. (Phase 3, proposed only.)
9. Now, evidence is eleven shapes only a person can read. After, it is one shape, so a machine can confirm it names the exact version, the command and the result, and still not whether it proves the claim. (Phase 4, proposed only.)
10. Nobody will be able to fix the catalog by hand any more: a wrong row is fixed in the plan it came from, and a bot, not a person, writes the page.

## What exists today

Counts are at astrid-dev `e27e30a`.

**Record parsing.** Twelve scripts hold 41 compiled patterns. "Text under a heading" is written five times (`check_docs.py:gap_section`, `release_section`; `check_gap_boundaries.py:section`; `check_project_planning.py:planning_block`; `export_public_vision.py:section`), `has_real_reason` twice with different placeholder lists, and a git wrapper three times. Allowed statuses are stated in `check_docs.py:STATUSES`, again in `ROUTE_STATUS`, and in catalog prose.

**Checks.** `check_docs.py:check` is one 110-line function covering the catalog, gaps, releases, strategy, ledger and links. Three more scripts gate PRs; two bots act on them. There is no list of what is checked. Local and CI runs differ ([ledger 3 and 17](../../docs/process-ledger.md)). Several gates exist only as skill prose (the GPU gate, the release gate, review rounds).

**Generated pages.** One script generates `vision/README.md`, the root README summary and the public feed. It is the right pattern, built once and not reusable. `vision/README.md` is both an output and the source of two of its own sections. Its unit tests assert the wording of the live vision files, so an editorial change can fail a code test.

**One fact, several homes.**

| Fact | Homes | Kept in step by |
| --- | --- | --- |
| Pillar, principle and gap summaries | source files; `vision/README.md` | generated |
| Gap and project counts | sources; root `README.md` | generated |
| Release highlight and plans | `releases/N.md`; `strategy.md` | hand copy, CI compares |
| Gap and plan links | gap route table; plan's closure line | hand-written twice, CI compares |
| Project title | plan heading; catalog row | nothing; several differ |
| Project status | catalog; prose in the pack | nothing; Plans 02, 06 and 07 disagree with the catalog |
| Release 12 state | release pages; Plan 29 handoff and brief; dated handoffs | nothing |

**The catalog.** `plans/index.md` is hand-written and is the authority; a plan folder without a row fails CI. Every status, owner, estimate and priority change by anyone edits that one file.

**Pack shape.** Ten of 47 `plan.md` files have the template's five headings. `tasks.md` has 12 different table headers and four files have no table. Task progress is free text. Two folders are numbered 40, and the completion check identifies a project by its number.

**Lifecycle.** Six statuses; two transitions are checked (claim, and to `done`). The six-step path (Orient to Land) is in the principles and the main skill; the plan skill has its own six steps and the manage skill its own seven, with no mapping. "Phase", "gate", "stage" and "track" are prose with several meanings each.

**Evidence.** Eleven JSON shapes across 137 files with no shared fields; three PR forms ask for claim, check, result, routes and limits in different words; the completion gate accepts any URL or SHA. `validation/gpu/` defines a record and holds none.

## Alternatives

- **Do nothing.** Works at today's size. The costs already recorded (local and CI disagreeing, progress PRs waiting on a shared file, a duplicated project number) grow with each plan and contributor, and Plan 31 adds a fourth one-off checker and a second publisher.
- **Fix only the catalog** (Phase 2 alone). Removes the shared file, but needs a parser and a generator anyway, so it would add a second generator beside the vision one. Phase 1 is the smaller way to get there.
- **Adopt a framework or a store** (a static-site generator, a schema library, GitHub Projects or a database for status). Each adds a dependency or a second home for facts and breaks "stdlib only, Markdown is the source". Rejected.
- **This plan, cut after any phase.** Each phase stands alone. Phases 3 and 4 are proposed only (D7).

## What following the planning process showed

Written while planning this project with the installed skills. Each is evidence for a task above or a decision for the owner; none is fixed here.

1. **Three documents name `plan.md`'s parts differently.** The [template](../../templates/project/plan.md) has five headings, [project-format](../../docs/project-format.md) lists different words, and 37 of 47 plans use neither. It is not clear which a new plan should copy. (PM-11)
2. **Planning evidence has more fields than the template.** Plan 31 records `Review rounds` and `Ambiguity pass` and an `## Owner decisions` section; the plan skill requires recording all three in `inputs.md`; the template and the check know only five labels. Decision ids (D1, P39-D8) are an unwritten convention. (PM-11)
3. **A field's value must sit on its label's line** or the check does not read it, so evidence is squeezed into one long line. (PM-1)
4. **A new plan must take a priority.** Adding a catalog row means choosing a position, and position is priority, which is the owner's call. There is no "not yet prioritized" place. (D1, D6)
5. **Project numbers are picked by looking.** Nothing reserves one, and two folders are already numbered 40. (PM-9)
6. **Every new plan edits the root README.** The generated summary counts projects, so a scope PR changes that line and any two scope PRs conflict on it. (D3, PM-8)
7. **"Planning runs no checks", but a scope PR must pass them,** and the planning check reads commits only, so it reports "OK for 0 projects" until the pack is committed. (PM-2)
8. **Gap or enabler is a judgment with no guide.** The first draft named CA-003, which this project serves only indirectly. CA-003 has no route to closure, so nothing asked which closure evidence the plan delivers, and Plan 44 was already primary on it with nothing surfacing the overlap. Resolved here by drafting CA-005.
9. **"Consult the advisor" assumes a run.** A planner working alone has no advisor session; the skill does not say that an independent critic in the same session is acceptable. It was used here.
10. **An owner's decision made in conversation has no durable link.** The check wants a URL or SHA; the only one available is a private session link, as Plan 31 also uses.
11. **Three step lists, no map.** The main skill's six stages, the plan skill's six steps and the catalog's six statuses describe the same journey in three vocabularies. (PM-12)
14. **The critique changed the plan more than any other step,** and the skill makes it conditional. It caught a gate that would have failed open. For a plan that changes checks or automation, it should not be optional.
12. **Task ids and the test inventory have no home in the template.** Each plan invents a prefix; the skill requires a test inventory that the template never mentions. (PM-11)
13. **The strategy has no place for work on astrid-dev itself.** It lists releases; a process project fits only under "Not now".

## Fixed alongside this plan

At the owner's request on 11 Nov 2026, the small process fixes that needed no new machinery were made in this branch: the templates are stated as the one definition of a pack's sections (findings 1, 2 and 12); a new plan's row goes last among open rows (finding 4); the advisor may be a fresh subagent (finding 9); an independent critique is required for the listed cases, including changes to astrid-dev's own checks (finding 14); and review rounds are proportional, with none for a simple project.

## Critique

One independent review of the first draft (plan and tasks), read-only, verifying claims in code. Findings and what was done:

| Finding | Severity | Decision |
| --- | --- | --- |
| Moving status out of `plans/index.md` silently disables the completion gate: `check_completion.py` detects a move to `done` by comparing the index at base and head, and review intake requires the index to be modified. Once nobody edits the index, the gate passes everything | blocking | **Accepted.** PM-6 now moves the gate and review intake to the project's own status in the same PR, with a negative test; it is routed S |
| "No check's result changes" was false. The section helpers differ on a missing section (nothing, empty string, or an error), the two placeholder lists differ by one word, and PM-2 changes behaviour on purpose | blocking | **Accepted.** PM-1 keeps each caller's behaviour as a parameter and lists the differences; the working-tree fix is a stated change |
| Ordering hazards: the strategy-table task overlapped Plan 31's RL-1a and contradicted its design; PM-6 touched live-run packs the plan said were off-limits; renaming a Plan 40 folder could break Release 12's citation | blocking | **Accepted.** The strategy task is dropped and left to Plan 31; the boundary now says exactly which lines move in every pack; only `40-contribution-discovery` is renumbered |
| The "same verdicts" proof could not be run: the broken cases are inline strings in unit tests, and removing the old modules breaks imports from trusted workflows | should-fix | **Accepted.** Fixture trees are built first; old modules stay as shims through Phase 1 |
| The claim bot needs new rules in a project file (duplicate field lines, one path shape, status read at base, head and live `main`), a claim would trigger the planning check, and a not-found reply becomes a failure | should-fix | **Accepted** into PM-7. Noted: the bot is disabled today because `main` is unprotected |
| Routes, dependencies and proofs: PM-6 should be S; PM-5 needs no dependency; the test inventory was wrong; rows named no test files; PM-8's stand-in branch proved nothing about the real rules; the docs grep missed the "only in the catalog" Start line | should-fix | **Accepted.** All corrected in `tasks.md` |
| A views framework for one consumer is premature; keep the exporter as is | should-fix | **Partly accepted.** PM-3 is cut down to making the exporter's existing marker and stale check reusable, and it has three consumers in Phase 1 and the catalog in Phase 2. The owner asked for one standard way to generate pages |
| Defer Phase 2 until conflicts are measured. Measured in the review: `main` took about 150 commits a day on 10 and 11 Nov and `plans/index.md` 14 to 18 a day on 7 to 9 Nov; edits to non-adjacent rows merge cleanly today; "author regenerates plus a stale check" would be worse than today at this rate; a bot on `main` needs settings that are still unset; cheaper options are to leave the table and move only the most-edited cell | should-fix | **Left to the owner (D3).** Phase 2 stays committed because the owner asked for plans to define the list, with these costs recorded. No conflict count was measured, only edit rates |
| Cut Phases 3 and 4: no recorded failure asks for them | blocking, in the reviewer's view | **Left to the owner (D7).** Marked proposed, not committed, and left out of the committed estimate |
| The CA-003 link is not honest; use the enabler line | should-fix | **Accepted.** The plan now links a new gap, CA-005, drafted for the owner's boundary review (D8) |
| Hard to reverse: a bot bypass on `main`, a renamed plan folder, and status split across every plan file. All are in Phase 2 | consider | Recorded. Phase 1 has none of these |

The reviewer's own minimal scope is Phase 1 without the view mechanism, plus the duplicate-number check.

## Phases 3 and 4: specification

Written on 11 Nov 2026 after the owner asked for Phases 3 and 4 to be specified to task level ([planning session](https://claude.ai/code/session_011EzfW38XJUpUFewfUM9MxF)). **That request is a go to specify. It is not acceptance of D7 and not a go to run anything.** The tension stands and has grown: both critiques say no recorded failure asks for a declared lifecycle, generated forms or an evidence envelope. This section is the evidence for the cards in [tasks.md](tasks.md); it read the code on `int/48-one-record-model` at `ee69971`.

### What already exists that each track reuses

| Track | Already there | So the track adds only |
| --- | --- | --- |
| A, pack shape | The plan skill and `docs/project-format.md` already name `templates/project/*.md` as "the one definition of each file's sections and fields". `scripts/records.py` reads headings, bold labels and table rows. `check_project_planning.py:changed_projects` already finds new packs, reading the working tree | A reader of the templates and one `pr` check. No second declaration, no generated template |
| B, lifecycle | `check_docs.py:STATUSES` and `VISIBLE` are the status set and the open/terminal split; `ROUTE_STATUS` repeats the six names as a pattern; `unnamed_active_owners` is "active needs a named owner"; `check_completion.py:transitions_to_done` is "done needs an assessment"; the catalog's preamble defines each status in a sentence. PM-6 will add a status reader at base and head | One declaration those five read; then, separately, one `pr` check for the moves nothing checks today |
| C, completion form | `scripts/views.py` already writes a marked file, and `generated-views` already fails a stale or hand-edited one. `check_completion.py:assess_completion` already holds every rule and message, and stays as it is | One form definition, one view entry, and the gate taking its label strings from the definition |
| Phase 4, envelope | The run contract already lists the fields in prose ("exact command, candidate SHA/tree, relevant inputs/environment, actual inner command status … result, and limitations") and the result words `PASS`, `FAIL`, `RETRYING`, `NO-RESULT`. `scripts/model_usage.py` already prints a `Routes used:` line. The completion gate already has reference, placeholder and route rules to copy. The GPU skill already has a record template | One declaration of eight lines, two checks where nothing is checked today, and a block in the GPU template |

### What the code shows today

Each was checked in the code at `ee69971`, and the second critic checked the counts again.

- **Shape.** Of 48 `plan.md` files, 11 have the template's five headings in order and 7 have exactly those five. (The earlier "ten of 47" was at `e27e30a`, before this pack existed.) 13 `tasks.md` files have the template's table header; there are 16 different headers and four files with no table. 21 of 48 `inputs.md` files have `## Planning evidence`, and none matches the template in full: this pack's own has no `**Run start:**` label.
- **The template and its check disagree.** `templates/project/inputs.md` has seven labels; `check_project_planning.py:LABELS` knows five (`Review rounds` and `Run start` are unchecked).
- **`docs/project-format.md` no longer restates the sections.** That was fixed alongside this plan on 11 Nov. What still restates the shape is the check's label list and 37 packs.
- **The completion form and its gate disagree.** `assess_completion` requires `Gap impact: None — <reason>` for a project with no gap; `project-completion.md` has no such line. The form has a `Strategy:` line the gate never reads (it checks that `strategy.md` changed, by path).
- **The completion form's hints satisfy most of its gate.** With the plan number filled in and nothing else, only `Integrated candidate` and the gap line fail; the `Evidence`, `Completion`, `Implementation PRs`, `Unproven` and `Routes used` hints pass as printed. (Traced from the patterns by the planner and by the critic; not run.) With the number left as `NN` the heading does not match and the gate gives one error, so it does not pass unfilled.
- **The gate's tests assert substrings,** not exact output, and seven of the thirteen in `test_check_completion.py` build on one sample description that carries all the fields.
- **`Routes used:` is printed by a script** (`scripts/model_usage.py`), and the run contract, `docs/contribution-workflow.md` and `templates/product-pr/review.md` tell people to paste it.
- **Statuses.** The six names are written in `check_docs.py` three times, as literals in `check_completion.py` and `claim_project.py`, and in the catalog's preamble. Outside the catalog they are used, not defined, in two skills, three docs and the claim form. No template names them. Two moves are checked: a claim needs `queued`, and a move to `done` needs an assessment. Each project's status also goes into the public feed.
- **Views.** `scripts/views.py:_with_marker` supports whole files generally, but its region support is hard-coded to the `vision-summary` markers; `scripts/test_views.py` pins the marker's exact text.
- **PR templates.** There are five: the default `.github/pull_request_template.md` and four under `PULL_REQUEST_TEMPLATE/`. A check reads the fields of one (completion); review intake reads two header lines of three; `claim.md` is read by nothing, because the claim bot reads the diff.
- **Evidence.** 168 JSON files sit under `plans/*/evidence/` (137 at the earlier survey). `validation/gpu/` holds its README and no record; Plan 34's branch adds records and fixtures there. The release skill's GPU gate reads that record.
- **The oracle.** `scripts/golden.py` runs `check` with no base on a copy of the real tree, so a new `pr` check cannot change `golden.txt`, and nothing in it covers the three PR gates.

### Alternatives, including doing less

- **Do nothing (the first critique's position).** Costs nothing. The two disagreements above stay: a project with no gap learns about `Gap impact` from a failed check, and two template labels are unchecked.
- **Fix the completion form by hand, and stop (the second critique's first line; PM-13h).** One line in the form and one test: under an hour, no new code. It repairs today's drift and catches the next missing label. It belongs in an ordinary fix PR whatever D7 decides.
- **That, plus track A for new packs.** About a day more. Track A has the strongest evidence and does not need Phase 2. Its weakness, from the second critique: it enforces a shape no code reads.
- **A separate declaration file for the pack shape, with the templates generated from it.** Rejected: the templates were named the one definition on 11 Nov; a second declaration would undo that, and generating them would move guidance prose into code.
- **Hold old files that already match to the shape.** Rejected after the critique: no `inputs.md` matches, and the `plan.md` and `tasks.md` files that do are mostly in packs with live runs.
- **Reshape old packs widely.** Rejected: 11 packs share a heading set with no `Interfaces and handoff` section, so matching them would mean writing one; no `tasks.md` outside the 13 can gain Route and Scope columns without inventing their contents. Eight drafts can be reshaped honestly, in `plan.md` alone (PM-11c), and that buys little: D4.
- **Generate every PR and issue template.** Rejected: all but the completion form are prose no check reads; a definition for them would be the same prose in a Python string.
- **Make the completion gate read its rules from the form definition.** Rejected after the critique: the rules are not uniform, and a definition that lost a field would then weaken the gate without a failure.
- **Rename the completion assessment's fields to the envelope's.** Not in the cards after the critique; it is option (b) of D11, with its cost.
- **Convert the existing evidence files to the envelope.** Rejected: they are historical receipts under packs with live or finished runs.
- **Cut from the outline, as nothing reads them:** task progress states, a Phase field, a drift report, and one definition for the six-step path and "phase".

### Ambiguity pass

Done by the planner from the code; the choices are in [tasks.md](tasks.md#phases-3-and-4-dispatch-notes). Resolved without the owner: the templates are the declaration; extra headings are allowed; only new packs are checked, and a rename is not new; `plan.md` header lines are outside the shape; the declarations for statuses, the form and the envelope are Python data; the completion gate's rules, review intake, the claim bot and `model_usage.py` are not touched; the envelope uses plain `Key: value` lines and keeps the label `Routes used`; the GPU check reads only added files with a record's name. What only the owner can decide is D9 to D13 above. D4 and D7 stay open.

### Ten statements for Phases 3 and 4

Shown to the owner in the planning session. Eight were changed here so that each is true of the tasks as written; the owner has not yet seen the changed wording.

1. Now, the template is a suggestion that eleven of 48 plans follow. After, a new plan that doesn't match the shape does not land. *(Changed: the count, at `ee69971`; was "ten of 47".)*
2. Now, the template lists seven planning-evidence fields, its check knows five, and 37 plans use other headings. After, the template is the one declaration and the new check reads it; the docs point to it and list nothing; the older check keeps its five labels, and a test fails if one stops being a template label. *(Changed: the docs stopped restating the sections on 11 Nov, no fourth file is added, and the second critic noted the five labels remain a hand-written list.)*
3. Old plans stay messy. Live and finished packs are left as they are and are never checked; eight queued drafts get their `plan.md` headings renamed by one command, and nothing else is reshaped because it would mean inventing content. *(Changed: was "only queued drafts are reshaped, by script". True only if D4 keeps PM-11c.)*
4. Now, the six statuses are written three times in one script, twice more as literals, and defined again in the catalog's prose. After, adding a stage is one entry in one file in astrid-dev; the App, which receives each project's status in the public feed, may need to learn it too. *(Changed: no template and no skill defines them; the claim bot keeps its own `queued` test; the App's side was not checked.)*
5. Now, a status can jump from anywhere to anywhere unless a script happens to catch it. After, only declared transitions pass, unless the PR says it is correcting a status and why. *(Changed: the correction line. True only if D10 keeps PM-12c.)*
6. Now, a PR form and the check that reads it are written separately and drift apart. After, the completion form is generated from the definition its gate takes its labels from. *(Changed: one form, and labels, not rules.)*
7. Nobody edits the completion form by hand again: a hand edit fails the check. After Phase 4 the same holds for the implementation form. Every other template, which no check reads, stays hand-written. *(Changed: was "a PR template".)*
8. Now, evidence comes in eleven shapes that only a person can read. After, new evidence in the implementation review form and in the GPU record is one envelope: claim, exact version, command, environment, result, receipt, limits and routes. The files already in the repository are not converted and may keep arriving in any shape, and the completion assessment keeps its own lines. *(Changed: the eleven shapes are JSON files this does not touch; the completion form is left alone.)*
9. A machine will confirm the envelope is complete, and will still not know whether the evidence proves the claim. *(Unchanged; PM-14a pins it with a test.)*
10. The GPU validation record changes shape to fit the envelope, so its skill and its readers change with it. *(Unchanged: the skill, the README and the release skill's gate sentence change; the revisions table stays; Plan 34's pack is not edited and its owner is told.)*

### Estimates

Remaining engineering days, not in the catalog's committed figure.

| | Days | Note |
| --- | --- | --- |
| PM-13h alone | under 0.25 | an ordinary fix |
| Phase 3, track A | 1–1.25 | PM-11a, PM-11b, PM-11t; PM-11c adds a quarter |
| Phase 3, track B | 1.25–1.75 | PM-12c adds 0.5–0.75, more if assumption A3 fails |
| Phase 3, track C | 1.25–1.75 | the corpus is about half of PM-13a |
| Phase 3 review | 0.5 | R3 |
| **Phase 3, everything** | **4–6.5** | the upper end includes PM-11c and PM-12c; about 2.5 elapsed with three tracks in parallel |
| **Phase 4** | **2–3** | PM-14a to R4 |
| PM-13h and track A, with one review round | about 2 | the slice recommended under D9 |

### Review rounds

Recommend one round per phase (R3, R4), each on the phase's integrated head before its PR to `main`. Each phase adds checks beside a gate, so ordinary PR review is not enough; neither crosses a repository, a release or user data, so one round is. No separate review stop: Phase 4 builds only on track C, and PM-14a waits for a round on it. If only PM-13h and track A are taken, one round on track A; PM-13h needs none. Pending — the owner's agreed number.

### Second critique

Reviewed on 11 Nov 2026 by a fresh session with no stake in the draft (`session_011EzfW2YVR3oTr7E9efK4ar`), read-only, on commit `ee47263`, briefed to build as little as possible and to verify claims in the code, not in the summary. It confirmed the counts and the code claims listed above, and found the following. The cards in `tasks.md` are the revised ones.

| Finding | Severity | Decision |
| --- | --- | --- |
| Renaming the completion assessment's fields breaks a line a script prints (`model_usage.py`) and three documents tell people to paste; the cards' scope omitted all of them | blocking | **Accepted.** Phase 4 no longer touches the completion gate or its form. The envelope keeps the label `Routes used`. Renaming is left to the owner as D11 (b), with these files listed |
| No independent oracle for "the gate refuses everything it refused before": the same phase rewrote the gate and seven of its thirteen tests | blocking | **Accepted,** by the same change: `test_check_completion.py` is not edited in either phase |
| Undisclosed verdict changes: a receipt could be any existing path; a candidate could no longer be a URL; `Completion: Yes —` disappeared | blocking | **Accepted.** A receipt is a URL or a full SHA; the envelope applies only where nothing is checked today, so no existing verdict moves |
| "Matched at base means checked" fails closed on a folder rename, including Phase 2's own PM-9 | blocking | **Accepted.** A renamed folder is never a new pack; PM-11a pins it |
| "Every message unchanged" in the form task had no oracle: existing tests assert substrings and `golden.txt` cannot see a `pr` check | blocking | **Accepted.** PM-13a first pins the gate's exact output over a set of descriptions. The gate's rules stay code; only label strings move. Route stays N for PM-13b because of that oracle; the critic asked for X |
| The "already matches, must keep matching" rule is the costly half of track A and would hold almost only live packs' files | should-fix | **Accepted.** New packs only |
| Generated forms are machinery behind one real defect, the missing `Gap impact` line; scope and implementation definitions would be prose in Python; a data-driven gate can be weakened by thinning the definition | should-fix (cut) | **Partly accepted.** PM-13h is that one-line fix, usable alone. Track C shrinks to the completion form, with no data-driven rules. Cutting track C entirely is left to the owner (D7, D9), because the owner asked for a generated form |
| Track B consolidates five literals, then adds a hard gate from a table nobody could check against history, with no way to correct a wrong status | should-fix (cut or shrink) | **Partly accepted.** The gate is split into PM-12c, droppable, with a correction line and a history check before it is registered. Cutting it is D10 (a) |
| A new pack written as this one was would fail: `Run start`, `Review rounds` and `## Owner decisions` become mandatory for every draft | should-fix | **Left to the owner (D13)** |
| "Unfilled form fails once per required field" cannot be built as worded: the heading needs a plan number, and `Unproven` accepts any text | should-fix | **Accepted.** Reworded in the card, the plan and here |
| The envelope's place was unspecified and an `Evidence` heading inside a completion assessment would cut the section short | should-fix | **Accepted.** The heading, the end of an envelope and the several-envelopes rule are in PM-14a; nothing goes inside a completion assessment |
| The GPU check would fire on fixtures under `validation/gpu/`, said both "follows" and "starts with", and collapsed four labelled SHAs into one line | should-fix | **Accepted.** Only added files named like a record; found by its heading; the revisions table stays and `Candidate` is the Agent's SHA |
| Unreal dependencies (PM-12a on PM-10; Phase 4 on all of R3; a fixed merge order), and no words or review cards for the recommended slice | should-fix | **Accepted.** Dependencies cut; words split per track; R3 covers whichever tracks are accepted; PM-12c and PM-14c write their own tests so nothing waits red on a decision |
| The drift report has no reader; the grep proof missed `ROUTE_STATUS`; "no fixture may end in `.md`" was overstated | consider | **Accepted.** Report cut; proof names the symbol; note reworded |
| The `Result` words are not in the run contract | should-fix | **Rejected.** They are, in its "Checks and failure repair" section: "Use `PASS`, `FAIL`, `RETRYING` … and `NO-RESULT`" |
| The pack-shape check enforces a shape no code reads | consider | **Left to the owner (D7, D9).** Recorded as track A's weakness |

**The critic's own minimal scope:** PM-13h and PM-11c's command in one hand-made PR; track A for new packs only if the owner wants a gate, with `Run start` settled first; cut tracks B and C and all of Phase 4 until a recorded failure asks, and if Phase 4 returns, add fields without renaming. The planner agrees with the first two lines and has kept the rest specified because the owner asked for it; D7 and D9 are where it is cut.

## Phase 2: re-plan against Phase 1

Written on 11 Nov 2026. **The owner asked that day for Phase 2 to be made ready to execute, with Codex doing the bulk of the work** ([planning session](https://claude.ai/code/session_011EzfW38XJUpUFewfUM9MxF)). That is a go to specify. It is not a go to run: no Run start is written for Phase 2, and it still waits for Release 12 to publish. The cards are in [tasks.md](tasks.md); this section is their evidence. It read astrid-dev `main` at `12a54b6`.

### What the code showed

Each was read in the code or in the repository's settings, not taken from the earlier cards.

- **`main`'s rules** (ruleset `main`, read through the API): no deletion, no force-push, a pull request with zero approvals, the checks `documentation` and `vision-consumer-contract`, branches need not be up to date, and no bypass actor. `branches/main` now reports `protected: true`, so the claim bot's own refusal on an unprotected `main` no longer holds it off; only the unset `CLAIM_AUTO_MERGE_ENABLED` variable does.
- **Who reads `plans/index.md`:** `check_docs.py:catalog_rows` and, through it, eleven guards and two rules in `checks.py`; the completion gate (`check_completion.py:plan_statuses`, `transitions_to_done`, `catalog_at_revision`); `export_public_vision.py:build`; `claim_project.py`; `review_intake.py:classify`; and `contribution_api.py:catalog`, which fetches it from GitHub. The two bots run `main`'s copy of their scripts, so they switch at the moment the cut-over merges.
- **Who else assumes the table:** six test files build one from `check_docs.HEADER`, and four oracle fixtures overlay the whole file.
- **The catalog against the packs:** 48 rows and 48 folders. In 26 the row's project name differs from the plan's title. One cell holds a relative link. One row's link label is not `Plan NN`. Every `plan.md` has its title on line 1 and a blank line 2. No `plan.md` has a `**Status:**`, `**Owner:**`, `**Estimate:**` or `**Waiting on:**` line; Plan 17 has a `**Goal:**` line in its body. Twelve packs carry the template's sentence that these facts live only in the catalog, and more say it in other words.
- **Planning evidence:** 21 packs have the section and all 21 pass today.
- **Generated pages:** three views exist. `vision/README.md` is still read as the source of the principle list. `export_public_vision.py`'s own command fails on an out-of-date page, and two CI jobs run it.
- **The old commands** hold the rule functions; only their `main` functions are shims. Five documents outside `plans/` name them.
- **The Phase 1 integration branch** has merged and been deleted, so its name is free.

### Ambiguity pass

Done by the planner from the code. Resolved without the owner, each written into a card or the dispatch notes:

- **Field syntax and place:** six bold lines directly under the title, each its own paragraph, read from the header block only.
- **Field values** are written relative to the plan and re-based for the catalog and the feed, so the feed stays byte-identical.
- **`plans/priority.md`** lists folder ids, one per line, under `## Order`. It starts as today's row order, terminal projects included, so the generated order equals today's. A project it omits sorts last among open ones, so a new pack edits no shared file.
- **The catalog's hand-written "Delivery context" text** moves word for word to `plans/catalog-notes.md`, which the view prints; its "How to edit safely" text becomes part of the generated preamble. Nothing is deleted by a script.
- **Existing packs get the six lines and nothing else,** live run or not. The old sentence in their Start lines stays until each run ends. This keeps the plan's boundary and D4.
- **A status change now re-runs the planning-evidence check** for a pack that has that section. All 21 pass, so no exemption is built (the first draft had one; the critique cut it).
- **The completion gate can read a base from before the cut-over,** so the cut-over PR itself is not asked for six completion assessments, and a status it cannot read counts as not done.
- **The oracle:** fixtures add a synthetic pack; `golden.txt` is always the script's output; each card names the only lines that may differ.
- **PM-10** removes entry points, not modules.
- **The renumbered project** takes the lowest free number when PM-9 starts, and PM-9 lands after the cut-over, so the migration at cut-over still finds every row's folder.
- **Review intake and the claim bot** move in the same PR as the gate, because both run `main`'s code.
- **Two refresh modes:** authors run `sync` and commit until C-2; afterwards they leave generated files out and a hand edit fails.
- **In CI the base of a PR check** becomes the first parent of the merge commit, in the cut-over itself (PM-6a). Whether the event's own base SHA can lag behind it was not verified; the card does not depend on the answer.

What only the owner can decide is D14 to D17 above.

### Estimates

Engineering days for Phase 2, by card, are in [tasks.md](tasks.md#phase-2-dispatch-notes).

| | Days | Note |
| --- | --- | --- |
| Codex, N route | 4.2 | nine cards |
| Codex, S route | 2.75 | the three tests-first contracts |
| Hosting session, taste | 0.85 | three cards |
| Hosting session, review | 1.0 | RS1, R2 and R8 |
| Hosting session, hosted proof and the two landings | 1.25 | PM-8h, C-1, C-2 |
| Hosting session, handling each Codex card, and review findings | about 1 | not on any card |
| **Phase 2, all of it** | **about 11** | 6.85 of the cards' 10 days come before the cut-over, about 6.5 elapsed; roughly 60% of the whole is Codex's |

The catalog row says "phase 2 5–6". That figure predates the tests-first split, the review stop and the hosted proof; it is close to the elapsed time to the cut-over, not to the work. The row is outside this pack and was not edited here.

### Review rounds

**Recommend one review stop and one final round.** RS1, one round, on the two contracts (PM-6a, PM-7a) before PM-6b and PM-7b build on them: they decide what the completion gate and the claim bot refuse, a hole found at the end would mean redoing both implementations, and it puts a second model's eyes on tests a Codex route wrote. R2, one round, on the integrated head before the cut-over. R8, one round, on the refresh job's diff before C-2, because it is a job that pushes to `main` past the ruleset and it lands separately (D16). Nothing here crosses a repository or touches user data, so no more than that. Pending — the owner's agreed number.

### Third critique

Reviewed on 11 Nov 2026 by a fresh session with no stake in the draft (`session_011EzfW3TiCsjmR3PQMUFENy`), read-only, on commit `b82baf3`, briefed to build as little as possible, to verify claims in the code, and to find any way a gate fails open or a claim is wrongly merged. It ran the checks and the tests, and tried the conflict claim and the renumbering in scratch clones. The cards in `tasks.md` are the revised ones.

| Finding | Severity | Decision |
| --- | --- | --- |
| K1. The cut-over re-runs the migration from `main`'s table, which still names `40-contribution-discovery` after PM-9 has renamed it | blocking | **Accepted.** PM-9 leaves the cut-over and lands as its own PR after it. The cut-over's feed is then byte-identical, a stronger proof |
| K2. A fifth fixture, `route-plan-backlink-mismatch`, overlays a real pack's whole `plan.md`; after the migration it would lack the six lines and change three `golden.txt` lines the proof forbids | blocking | **Accepted.** PM-6a names it; PM-6b gives the overlay the six lines and its lines must not change |
| K3. The refresh job would fail on every run: bytecode is tracked, so `sync` dirties paths it did not print | blocking | **Accepted.** The job sets `PYTHONDONTWRITEBYTECODE=1` and stages only printed paths |
| K4. The migration script was told both to replace its lines on a second run and to refuse lines it did not write, and cannot tell them apart | blocking | **Accepted.** Defined by position: the block at lines 3 to 14 is the script's; a label elsewhere in the header is the refusal |
| K5. Taking the PR base from the merge commit's first parent is a gate fix, not part of the bot; left with PM-8 it would wait. If the event's base lags, a plan reopened on `main` and set `done` again could show as no move | should-fix | **Accepted.** Moved into PM-6a (5), with a check that the second parent is the event's head; it lands in the cut-over |
| K6. The live-`main` check compared six fields against the event's base, so body text that differs between merge base, base and `main` was unchecked | should-fix | **Accepted.** The file on `main` must be byte-equal to the file at the base, and the files entry must show one addition and one deletion. Simpler than the first rule |
| K7. No check sees what the job will write, and its commit skips the required checks | should-fix | **Accepted.** PM-8a adds a PR step: `sync`, then `check` with no base |
| K8. "A PR may contain a correctly regenerated file" stops being true when `main` moves, and telling every author to commit generated files keeps the conflicts D3 set out to remove. A deleted region marker was unpinned | should-fix | **Accepted.** After C-2 authors leave generated files out; a missing marker is an error |
| K9. The job could not tell a push refused because `main` moved from any other refusal, and no proof covered the loop | should-fix | **Accepted.** It re-fetches and exits 0 only if `main` moved; PM-8h and C-2 record the second run ending at "nothing changed" |
| K10. PM-8b's `golden.txt` rule missed the stale-view lines of fixtures that add a pack | should-fix | **Accepted.** Removed lines may contain `--sync-readme` or `: view ` |
| K11. PM-6b could not prove its exporter change before the fixture tree was migrated | should-fix | **Accepted.** The migration is applied in PM-6m, where nothing reads the new lines yet; PM-6b implements, regenerates and deletes the script; PM-6d is gone |
| K12. Three proofs did not work for a worker that cannot commit | should-fix | **Accepted.** Reworded: `git status --porcelain`, and a copy of the worktree in place of a clone |
| K13. PM-10 needs nothing from Phase 2 and, run late, made PM-6b port a command about to be deleted; PM-10e sat on the critical path | should-fix | **Accepted.** PM-10 goes first; PM-10e moves after the cut-over |
| K14. The planning-evidence exemption for field-only changes buys nothing: every pack it could affect passes | should-fix | **Accepted.** Cut. A status change now re-runs that check for a pack with the section, stated as a behaviour change |
| K15. The `\s*` behind finding R1.2 is in `records.field_match`, outside PM-9b's scope, and the same fault would make an empty `**Owner:**` read the next field as its value | should-fix | **Accepted.** PM-9b uses a local pattern; PM-6a pins an empty value as an error |
| K16. "The eight names" listed six; fixed counts go stale as `main` gains packs | should-fix | **Accepted.** All eight are named; counts are per row |
| K17. Branch bases and the critical path were wrong in places | should-fix | **Accepted.** Each branch's base is stated; PM-7a is on the path |
| K18. Between the two PRs no claim can be auto-merged, because a field change needs two files | should-fix | **Accepted.** Stated in PM-7b, D16 and the cut-over order; the owner's smoke test waits for C-2 |
| K19. The arithmetic held, but left out the host's work on each sandboxed card and the reviews' findings; PM-6a was too small | should-fix | **Accepted.** About 11 days, roughly 60% Codex's; PM-6a 1.5, C-1 0.5 |
| K20. The column move protects rows only; an edit to the catalog's prose merges clean | consider | **Accepted.** D15 and step 8 say so; the sweep reads every such PR |
| K21. The reader of the old table had no removal card | consider | **Accepted.** PM-6z, after the cut-over |
| K22. The `documentation` job runs the PR's own checks and `main` needs no approval, so every gate is advisory against an author who edits the checks | consider | **Accepted** as a stated limit in R2's brief. Nothing is built |
| K23. Four `sync` guards duplicate the job's own check; `rebase_links` exists for one link; a marked region around the table would need no notes file or generated preamble | consider | **Partly accepted.** The guards are cut to two. The other two are left for RS1 and R2 to decide, because the owner asked for the catalog to be a generated page |
| K24. "Runs in seconds" is about 40 seconds; other files can conflict at the cut-over; a progress PR per card is about 20 PRs | consider | **Accepted.** Reworded; progress is ticked once per branch merge |

**What it verified as true:** the counts under "What the code showed", the eleven guards, the five documents that name the old commands, that both bot workflows check out `main`, that the exporter fails on an out-of-date page in two jobs, that a row edit, add or delete conflicts against a column-reordered table, and that PM-9's rename passes every check.

**What it could not verify:** `main`'s ruleset and the claim variable (the planner read the ruleset through the API; the variable is not readable); whether the event's base SHA lags; what the files API reports for a mode-only or symlink change; an App token's push behaviour. The last three are why PM-8h is a hosted proof and why RS1 reads the claim tests.

**The critic's own minimal Phase 2** is the order the cards now follow: PM-10 first; the two contracts and RS1; the migration applied, then the readers; the base step, R2 and the cut-over with one words pass; then, as separate small PRs, the renumbering, the R1.2 fix, the refresh job and the extension guide.

## Phase 3 queue: re-plan against Phase 2

*12 Nov 2026.* The queue the owner accepted under D9 (PM-13h; PM-11a, PM-11b, PM-11t; PM-12a, PM-12b, PM-12t; R3) was specified before Phase 2 existed. Its eight cards in [tasks.md](tasks.md) are now rewritten against the Phase 2 candidate, `int/48-one-record-model` at `da22d14`, read from the code; the whole inventory (205 tests) and `astrid_dev.py check` pass at that commit. No design changed except where the code made the old one impossible. Track C and Phase 4 were not touched.

### What changed in the cards, and why

- **PM-12b: the definitions sentence is a second small generated region, not a line the catalog view prints.** Phase 2 made the catalog page hand-written prose around one generated table (RS1), so there is no generated preamble to print into. The two ways left were to check the hand-written sentence against the declaration, or to generate it in its own region. Generated was chosen: a check would need a parser for a prose sentence and a new error message, and would leave a repeated fact hand-copied and compared, which statement 4 above rules out; a region reuses `generated-views`, its stale message and `sync`, and adds no check. It was tried at `da22d14`: two region views on one page check, sync and re-sync correctly with `views.py` as it is. The cost is one added line in `golden.txt`, because the `stale-plan-catalog` fixture replaces the page with one that has no such region; the card names that line, and nothing else in the oracle may change.
- **PM-12a and PM-12b: the list of readers is the real one.** Status words now sit in `check_docs.py` (`STATUSES`, `VISIBLE`, `ROUTE_STATUS`, `unnamed_active_owners`), `checks.py:_catalog`, `records.py:projects` (validity, and the sort that puts terminal rows last) and `check_completion.py:transitions_to_done`. Phase 2 also wrote the list out inside the invalid-status message, twice; that message now comes from the declaration, whose order is the message's order so that it does not change by a byte. The old proof grepped for quoted words and would have missed a comma list, so the new proof greps for the bare words. The catalog page's sentence takes the declaration's order (`queued` first); its meanings do not change.
- **PM-12t is dropped** (fourth critique, below). With the gate's messages gone (D10) it had no required output: `docs/extending.md` does not exist, the meanings are today's wording, and PM-12b adds no message. R3 reads the sentence.
- **PM-11a and PM-11b: one fault, one line.** Phase 2 left three checks that already speak about a new pack: `plan-files` (a missing file), `plan-catalog` (the six field lines, on every pack) and `project-planning-evidence` (which runs on every new pack and requires the `## Planning evidence` heading and five labels). `pack-shape` is now silent on all of those, so it reports the headings, the table header and the two labels D13 added (`Review rounds`, `Run start`). `check --base` needs a body since Phase 2, so the command test passes one, with a one-entry registry in a temporary repository.
- **PM-13h** was checked against the gate as it stands: the form filled with an example per label passes for a gap-linked plan and fails for an enabler, so the fix is still needed. The card now gives the line's wording and says the test calls `assess_completion` with the plan text, so it needs no pack on disk.
- **R3** names what the reviewer checks first, reviews the branch after `main` has been merged into it, and lists the open PRs that add a pack before the new check reaches them.
- **Where it lands.** `int/48-phase3`, cut from the Phase 2 candidate's head, merged to `main` only after the cut-over. Starting on a side branch before the cut-over is the orchestrator's call under the delegation on the Phase 2 `Run start` line, which queued this work "after the cut-over"; nothing reaches `main` earlier either way.
- **The assumptions table** (A1 to A9, and a new A10 for track C) now states what Phase 2 built.

### Sizes

PM-13h 0.1; PM-11a 0.5; PM-11b 0.5; PM-11t 0.25; PM-12a 0.5; PM-12b 0.75; R3 0.5: 3.1 days of cards, about two elapsed with the tracks side by side. The [estimates](#estimates) above gave these rows about 2.5 to 3; PM-12b grew by the second region and the readers Phase 2 added.

### Owner decisions

None is open for this queue; D18 is not used. D4, D10 and D13 decide the cards' substance, and the choice between a check and a generated region is an implementation choice that follows from statement 4. Two things she may want to know, neither needing an answer: the catalog page's definitions will list `queued` before `active`; and from the day the queue reaches `main`, an open PR that adds a pack not matching the templates fails (D13), which R3 lists beforehand.

### Not placed in the queue

The follow-up to R2's second point (the principle list is still read from the generated `vision/README.md`) is not one of D9's rows, has no card yet, and shares no file with a queued card. It goes with the after-cut-over PRs to `main`. "Before track A" was a preference of order, not a dependency: track A reads only the templates.

### Fourth critique

**12 Nov 2026, one round.** An independent critic, read-only, on the cards at `1218da4` against the candidate at `da22d14`, briefed to build as little as possible, to verify each claim in the candidate's code and to find a verdict that would change unannounced. **Verdict: dispatch after the listed fixes.** The four claims it was asked to test all hold. Its findings, and what was done:

| | Finding | Outcome |
| --- | --- | --- |
| F1 | PM-11b's rename proof used `--base HEAD` after a committed move, which proves nothing | Accepted: record `B=$(git rev-parse HEAD)` before the move and run `check --base $B` |
| F2 | "In a scratch clone" assumes the worker can commit, and it cannot | Accepted: a scratch copy of the working tree (`cp -a`, including `.git`), or the host runs the rename case after its commit |
| F3 | With `## Planning evidence` absent, `pack-shape` would add label lines to the planning gate's one line | Accepted: it reports no label then; one test case |
| F4 | PM-12b's `plans/index.md` diff proof left out the rest of the paragraph moving to its own line | Accepted: the proof names it |
| F5 | PM-12t has no required output: `docs/extending.md` does not exist, the meanings are today's wording, no message is added | Accepted: the card is dropped; R3 reads the sentence |
| F6 | `new_packs` did not say what an unavailable base does | Accepted: it raises `ValueError`, as `changed_projects` does; one test case |
| F7 | Rename detection over the whole tree can pair unrelated files | Accepted: the diff is limited to `'plans/*/plan.md'` |
| F8 | A PR that deletes one pack and adds a similar one pairs as a rename, so the new pack is unchecked | Accepted as a stated limit: one sentence in the notes, and R3 looks for a `D` and an `A` of a `plan.md` in one PR |
| F9 | The one new `golden.txt` line carries the generic "summary region" message | Recorded, no change: accepted knowingly, so that no new message is written |
| F10 | The new form line passes the gate unfilled | Recorded, no change: the form's other hints do the same; it is track C's subject |
| F11 | A `tasks.md` with no table was not pinned | Accepted: it gives one line |
| F12 | Whether `requiring` and the "what entering requires" field earn their place | Recorded, no change: both stay, and the second grep proof stays |

The queue is now seven rows: six cards and R3. What the planner had verified itself by running code at `da22d14`: the completion form's enabler failure; two region views on one target; the inventory and `check` green; every status literal outside tests, by grep. Still not run by anyone: the pack-shape functions (they do not exist), and the App's parser.

## Source identities

Planning read astrid-dev `e27e30a6` and wrote this pack on `b43f4e8936e668d4735bfae4f6d409251b311062`. Only astrid-dev changes. The App is consumed read-only through the existing `vision-consumer-contract` job at its `main`. Record each task's actual base SHA when it starts. The Phase 3 and 4 specification read `int/48-one-record-model` at `ee69971f` (Phase 1 integrated, not yet on `main`) and changes only this pack. The Phase 2 re-plan read `main` at `12a54b6` (Phase 1 merged) and changes only this pack.

## References

- [Contribution design principles](../../docs/contribution-design-principles.md), especially 2, 7 and 8.
- [Process ledger archive](../../docs/process-ledger.md) rows 3, 17, 38, 44 and 50.
- [Maintainer setup and adversarial smoke test](../../docs/contribution-automation-setup.md).
