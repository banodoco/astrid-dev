# Inputs — One model for astrid-dev's records, checks and generated pages

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — on 11 Nov 2026 the owner asked for a review of astrid-dev's overall structure before it scales, agreed with the direction and asked for it to be specified as a project linked to the vision-communication gap ([planning session](https://claude.ai/code/session_011EzfW38XJUpUFewfUM9MxF)). The scope itself and decisions D1 to D6 below are not yet chosen. Next: the owner answers D1 to D6 and confirms or cuts the phases.

**Prior art:** a read of every script, workflow, skill and template at astrid-dev `e27e30a`, plus two read-only surveys of all 47 packs and all 227 evidence files ([planning session](https://claude.ai/code/session_011EzfW38XJUpUFewfUM9MxF)); findings are under [What exists today](#what-exists-today). Reused: [`project_contract.py`](../../scripts/project_contract.py), [`vision_subject.py`](../../scripts/vision_subject.py), [`export_public_vision.py`](../../scripts/export_public_vision.py) and the `publish-vision` job. Overlapping plans: [Plan 31](../31-releases-from-astrid-dev/plan.md) and [Plan 44](../44-vision-execution-trail/plan.md).

**Approach:** finish the shared layer the existing scripts already imply (one parser, a check registry, a view mechanism), then move the catalog onto it, then declare the pack shape, lifecycle, forms and evidence. Alternatives compared under [Alternatives](#alternatives): do nothing; fix only the catalog; adopt a documentation framework or a database; this plan.

**Challenge:** Pending — an independent high-judgment critique, briefed to build as little as possible and to verify claims in code, was requested in the [planning session](https://claude.ai/code/session_011EzfW38XJUpUFewfUM9MxF). Next: record its findings and what was accepted or rejected under [Critique](#critique).

**Proof and limits:** see [plan.md](plan.md#completion). The proof is structural: same verdicts and a byte-identical public feed across the refactor, conflict-free parallel plan PRs, and one-file extension examples. It does not show that contributors find the result clearer beyond one fresh-agent trial.

**Review rounds:** Pending — recommend one review stop of one round after Phase 1's model (every later task builds on it) and at most two final rounds. PM-7 changes privileged automation, which is why two and not one. Next: the owner confirms the numbers.

**Ambiguity pass:** Pending. Other agents will run these tasks and several are X or S, so N helpers run one pass per phase before dispatch.

## Owner decisions

All open. Each has a recommendation.

- **D1. Where does priority live once the catalog is generated?** Row order is the priority today and it is the one fact that belongs to no single project. *Recommend:* a small ordered file of project ids (`plans/priority.md`), edited only to reprioritize; a project missing from it sorts last among open work. Alternative: a numeric priority field in each plan, which makes reordering touch many files.
- **D2. Which field syntax do project facts use?** The repository already has two: bold lines (`**Vision gaps:** …`) in plans, gaps and releases, and plain header lines (`Date: …`) in ledger entries and PR forms. *Recommend:* bold lines at the top of `plan.md`, next to `**Vision gaps:**`, and no third syntax. Alternative: YAML front matter, which GitHub renders as a table but needs a parser the standard library does not have.
- **D3. When are generated files refreshed?** Today the author runs the generator and CI fails if the file is stale. With many open PRs each adding a plan, every one of them edits the same generated catalog and the same count line in the root README, and they conflict. *Recommend:* refresh on `main` by a bot, so PRs never contain generated output. Cost: a bot commits to `main` (needs O-1) and the page lags a merge by about a minute. Alternative: keep the stale check and accept rebases; drop PM-8.
- **D4. Do existing packs get reshaped?** Only 10 of 47 `plan.md` files use the template's headings. *Recommend:* reshape queued drafts by script, leave packs with a live run and finished packs alone, and report the drift. Alternative: check new packs only.
- **D5. Order against Plan 31.** *Recommend:* Phase 1 before Plan 31's RL-1a to RL-1c, so Plan 31 registers its checks and its manifest as a view. Both wait for Release 12. Alternative: Plan 31 first, then fold its scripts in (more rework, no delay to releases).
- **D6. Where does this sit in the catalog's order?** The scope PR places it directly above Plan 31 because of D5. That placement is the owner's to change.

## Ten statements for the owner

Offered to the owner in the planning session to show the anchors and edges; each is true of the plan as written. Reactions become decisions above.

1. Now, the list defines the plans. After, the plans define the list.
2. Now, claiming a project means editing a shared table. After, it means changing one line in that project's own file.
3. Now, a hundred people changing status collide in one file. After, nobody edits a file someone else is editing.
4. Now, a fact shown twice is sometimes generated and sometimes hand-copied and compared. After, every repeated fact is generated, with no exceptions.
5. Now, you learn what is checked by reading five scripts. After, one command prints every check, and that printout is the documentation.
6. Now, checks can pass locally and fail in CI. After, it is the same command in both places.
7. Now, adding a stage means editing a template, a skill, a PR form and a pattern. After, it is one entry in one file.
8. Now, the template is a suggestion ten of 47 plans follow. After, a new plan that does not match the shape does not land.
9. Now, evidence is eleven shapes only a person can read. After, it is one shape, so a machine can confirm it names the exact version, the command and the result, and still not whether it proves the claim.
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
- **This plan, cut after any phase.** Each phase stands alone. Phases 3 and 4 are the first to drop if the owner wants less.

## What following the planning process showed

Written while planning this project with the installed skills. Each is evidence for a task above or a decision for the owner; none is fixed here.

1. **Three documents name `plan.md`'s parts differently.** The [template](../../templates/project/plan.md) has five headings, [project-format](../../docs/project-format.md) lists different words, and 37 of 47 plans use neither. It is not clear which a new plan should copy. (PM-11)
2. **Planning evidence has more fields than the template.** Plan 31 records `Review rounds` and `Ambiguity pass` and an `## Owner decisions` section; the plan skill requires recording all three in `inputs.md`; the template and the check know only five labels. Decision ids (D1, P39-D8) are an unwritten convention. (PM-11)
3. **A field's value must sit on its label's line** or the check does not read it, so evidence is squeezed into one long line. (PM-1)
4. **A new plan must take a priority.** Adding a catalog row means choosing a position, and position is priority, which is the owner's call. There is no "not yet prioritized" place. (D1, D6)
5. **Project numbers are picked by looking.** Nothing reserves one, and two folders are already numbered 40. (PM-9)
6. **Every new plan edits the root README.** The generated summary counts projects, so a scope PR changes that line and any two scope PRs conflict on it. (D3, PM-8)
7. **"Planning runs no checks", but a scope PR must pass them,** and the planning check reads commits only, so it reports "OK for 0 projects" until the pack is committed. (PM-2)
8. **Gap or enabler is a judgment with no guide.** This project serves CA-003 indirectly. CA-003 has no route to closure, so nothing asks which closure evidence the plan delivers, and Plan 44 is already primary on the same gap with nothing surfacing the overlap.
9. **"Consult the advisor" assumes a run.** A planner working alone has no advisor session; the skill does not say that an independent critic in the same session is acceptable. It was used here.
10. **An owner's decision made in conversation has no durable link.** The check wants a URL or SHA; the only one available is a private session link, as Plan 31 also uses.
11. **Three step lists, no map.** The main skill's six stages, the plan skill's six steps and the catalog's six statuses describe the same journey in three vocabularies. (PM-12)
12. **Task ids and the test inventory have no home in the template.** Each plan invents a prefix; the skill requires a test inventory that the template never mentions. (PM-11)
13. **The strategy has no place for work on astrid-dev itself.** It lists releases; a process project fits only under "Not now".

## Critique

Pending; see **Challenge** above.

## Source identities

Planning read astrid-dev `e27e30a6` and wrote this pack on `b43f4e8936e668d4735bfae4f6d409251b311062`. Only astrid-dev changes. The App is consumed read-only through the existing `vision-consumer-contract` job at its `main`. Record each task's actual base SHA when it starts.

## References

- [Contribution design principles](../../docs/contribution-design-principles.md), especially 2, 7 and 8.
- [Process ledger archive](../../docs/process-ledger.md) rows 3, 17, 38, 44 and 50.
- [Maintainer setup and adversarial smoke test](../../docs/contribution-automation-setup.md).
