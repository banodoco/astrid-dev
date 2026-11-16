# Tasks — Vision aspirations

[Plan](plan.md) · [Inputs](inputs.md)

The 13 Nov run implements both phases under the owner's direct end-to-end and main-promotion request; see [current evidence](evidence/execution.md). The original task scopes below remain the acceptance inventory. Paths and line numbers were read at astrid-dev `0ed58f9` and the App's `237b28b`; re-check them at dispatch. Phase 1 lands on one integration branch, `int/53-vision-aspirations`, and reaches `main` in two pull requests: the contract (VA-1, VA-2), then the rest.

**Task ids:** `VA-1`, `VA-2`, …; review `R`. **Critical path:** VA-1 → VA-2 → VA-5 → R → VA-7, with the owner's mark-up of VA-3 and VA-4 joining before VA-5. Phase 2: VA-8 → VA-9 → VA-10 → VA-11. **Test inventory:** `scripts/test_vision_subject.py`, `scripts/test_export_public_vision.py`, `scripts/test_gap_relationships.py`, `scripts/test_check_gap_boundaries.py`, `scripts/test_checks.py`; and, passing unedited, `scripts/test_views.py`, `scripts/test_golden.py` (the oracle `scripts/fixtures/golden.txt` does not change in this plan) and `scripts/test_project_contract.py`. In the App, for VA-9: `src/pages/Home/publicVisionContent.test.ts`, `src/pages/Home/visionHierarchy.test.ts`, `tests/e2e/public-astrid-vision-characteristics.spec.ts`, `tests/e2e/public-astrid-vision-hierarchy.spec.ts`.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| VA-1 The authoring contract: an element has `## Aspirations`; each aspiration may carry the pair of lists | X | D2 | `scripts/vision_subject.py` (`SECTIONS`, `parse_subject`, `render_subject_markdown`); `vision/templates/subject.md` (text; the file keeps its name); the eight pages under `vision/pillars/` and `vision/principles/` (the one heading only); `scripts/checks.py:_subjects` (message wording only); `scripts/export_public_vision.py:render_readme` (the one sentence that says "characteristics"); `scripts/fixtures/vision/**` (the same heading); `scripts/test_vision_subject.py`, `scripts/test_export_public_vision.py` | `python3 -m unittest discover -s scripts -p "test_vision_subject.py"` with the cases in [details](#va-1); `test_export_public_vision.py` passes with the feed's keys unchanged; `python3 scripts/astrid_dev.py check` passes; `git diff --stat <base> -- scripts/fixtures/golden.txt` prints nothing | [ ] |
| VA-2 A gap's first line may name its aspirations, one primary and any number supporting, and the check proves each exists | X | VA-1; D3 | `scripts/gap_relationships.py` (`ENTRY`, `parse_gap_relationships` and its return contract); its three callers: `scripts/checks.py:_gap_structure`, `scripts/checks.py:_boundary_impl`, `scripts/export_public_vision.py:build` (the gap loop); `scripts/check_gap_boundaries.py` (`boundary_signature`, and in `assess_boundary` the pattern for the two connection fields); `scripts/checks.py:_link_anchors` (lift its nested `anchors` helper to module level, behaviour unchanged); `templates/gap.md` (line 3); the four gap test files in the inventory | Those test files pass with the cases in [details](#va-2); `check` passes with all 22 gaps still on the old line; for those 22 the feed is byte-identical to the base; `golden.txt` unchanged | [ ] |
| VA-3 Packs and Generation are written, in the owner's wording | T | VA-1 (the shape); D6; the owner's mark-up before merge | `vision/pillars/liquid-software.md` (one new `###` section); `vision/principles/eliminate-needless-technical-wrangling.md` (one new `###` section); the matching files under `scripts/fixtures/vision/` | The owner's marked-up text is what merges, recorded as a decision in `inputs.md`; each section has a sentence, a paragraph of at least 15 words and both lists, at most five bullets each; `check` passes; [details](#va-3) | [ ] |
| VA-4 One aspiration is added and two are reworded, in the owner's wording | T | VA-1; D7, D16; the owner's mark-up before merge | `vision/pillars/shared-endeavour.md` (one new section); `vision/principles/local-first-cloud-capable.md` (the section "Optional cloud capabilities"); `vision/principles/open-by-design.md` (the section "Built for reuse"); the matching fixture files | As VA-3, with lists only where [the drafts](inputs.md#the-drafts) have them; each page still has two to six aspirations | [ ] |
| VA-5 All 22 gaps name their aspirations; F-008 and F-004 keep only what is specific to them; the old line is refused from then on | X | VA-2; VA-3, VA-4 (the targets exist under their final titles); D3, D8, D9; the owner's mark-up of the supporting proposals and of the two Desired states | the first metadata line of each file in `vision/gaps/`; the `## Desired state` section of `F-008-portable-generation.md` and `F-004-pack-lifecycle.md`; `vision/pillars/shared-endeavour.md` (the one References line about CA-004, only if D7 moves that gap); `scripts/gap_relationships.py:parse_gap_relationships` and `scripts/checks.py:_gap_structure` and `:_boundary_impl` (remove the old line's acceptance); the gap files under `scripts/fixtures/vision/` and the gaps embedded in the overlays `missing-gap-section`, `route-missing-closure-approach`, `route-missing-plan` and `route-status-word` | [Details](#va-5): no gap on the old line; `check` passes; `golden.txt` unchanged; the feed's `appliesTo` differs from the base only for gaps whose primary element moved or whose supporting element was dropped; the pull request carries a boundary record for exactly those gaps and for F-004 and F-008 | [ ] |
| VA-6 The rules, each in its one home, the words that point at them, and their wording | X | VA-2; D12 | `docs/contribution-workflow.md` (the "Vision" row of its table at line 23, and the section "Define or reassess a vision gap" at line 36); `templates/gap.md` (the comment block); `skills/astrid-dev-gap/SKILL.md` (line 12 and one link); `skills/astrid-dev-plan/SKILL.md` (one link in step 1); `skills/astrid-dev-improve/SKILL.md` (one new row in the table of homes); `skills/astrid-dev-shared/glossary.md` (three terms) | [Details](#va-6); `check` passes, including `link-anchors`; `git grep -n -i "characteristic" -- docs skills templates vision` prints nothing; before and after for each changed sentence; words added at most 200, counted with `wc -w` and stated in the pull request | [ ] |
| R Review rounds (at most 1, pending the owner's agreement) | S | VA-1 to VA-6 | read-only | Rounds per the [run contract](../../skills/astrid-dev-shared/run-contract.md): findings become rows `R1.<n>` added directly below this one, each with route, scope, dependencies and proof; the second pull request's merge and VA-7 wait for them; [what it looks for](#r) | [ ] |
| VA-7 The proof | N | R; the second pull request merged to `main`; a person for two minutes | `plans/53-vision-aspirations/evidence/phase-1.md` (new) | The observations in [details](#va-7) | [ ] |
| VA-8 Phase 2: the feed names each gap's aspirations | N | Release 13 published; VA-5 on `main` | `scripts/export_public_vision.py:build` (the gap loop); `scripts/test_export_public_vision.py` | The test file passes: each gap has `aspiration` and `supportingAspirations`, each reference carrying the element and the aspiration's id and resolving to an item of that element's `characteristics`; `aspiration` sits under the gap's `primaryAppliesTo`; `vision-consumer-contract` passes | [ ] |
| VA-9 Phase 2: the page is one hierarchy: aspiration, its gaps, each gap's description and projects | X | VA-8; D17; the release that takes it, and that release's manager | in astrid-app: `src/pages/Home/publicVisionContent.ts` (types; the validator for the two new fields, tolerant of their absence); `VisionDetailDialog.tsx`; `visionHierarchy.ts`; `PublicAstridVision.css`; the unit tests and Playwright specs in the inventory | That repository's own checks; [details](#va-9) | [ ] |
| VA-10 Phase 2: the hierarchy's layout and copy, "simple and elegant", seen by the owner before it ships | T | VA-9; the owner's look | in astrid-app: `PublicAstridVision.css`; copy strings in `VisionDetailDialog.tsx` (the heading "What defines this", the two quiet lines, the projects count); no change to data, structure or tests' logic | Screenshots at desktop and phone width in the pull request; the owner's go recorded; the specs pass with only their copy strings changed | [ ] |
| VA-11 Phase 2: the live page, seen | owner | VA-10's release is live | the browser | The owner opens the vision page and walks the hierarchy in [plan.md](plan.md#completion); noted in `evidence/phase-2.md` | [ ] |

No review-stop row: after the cuts the contract is two tasks, and its questions are in R.

## Sizes and who runs each card

Engineering days. This table is the one home for sizes; `plan.md`'s Estimate line carries the totals.

| Task | Who | Size |
| --- | --- | --- |
| VA-1 | X worker | 0.4 |
| VA-2 | X worker | 0.6 |
| VA-3 | taste, then the owner | 0.3 |
| VA-4 | taste, then the owner | 0.2 |
| VA-5 | X worker, then the owner for the supporting table and two sections | 0.6 |
| VA-6 | X worker | 0.3 |
| R | high-judgment sub-agent | 0.2 |
| VA-7 | cheap worker | 0.1 |
| VA-8 | cheap worker | 0.1 |
| VA-9 | X worker, in the App | 1.2 |
| VA-10 | taste, in the App, then the owner | 0.4 |
| VA-11 | the owner | 0.1 |

Phase 1 is 2.7: X 1.9, T 0.5, S 0.2, N 0.1. Phase 2 is 1.8: N 0.1, X 1.2, T 0.4, the owner 0.1. The owner's reading time is not counted.

**What can run side by side:** VA-3, VA-4 and VA-6's drafting start as soon as VA-1's shape is fixed. VA-1 and VA-2 both touch `export_public_vision.py`, in different functions: merge VA-1 first.

## Details

### VA-1

- Section names become Statement, Explanation, Aspirations, optional References. `## Characteristics` is refused with a message that names the new heading.
- Inside an aspiration, after the summary sentence and a blank line: prose of at least 15 words, then optionally a paragraph that is exactly `**We should:**` followed by a bullet list, then a paragraph that is exactly `**We should never:**` followed by a bullet list. Nothing follows the second list.
- Both or neither. One to five bullets in each. Each bullet passes `one_sentence`. The 15-word minimum counts the prose only, so every aspiration keeps a paragraph.
- The parsed item is unchanged: `id, title, summary, detailsMarkdown`, with the lists inside `detailsMarkdown` as written. The returned key stays `characteristics`, and so does the feed's. No field is added.
- Code names (`parse_subject`, `CHARACTERISTIC`) may stay; messages a person reads say "aspiration".
- Tests: the eight real pages parse; an aspiration with both lists parses; one list alone fails; six bullets fail; a two-sentence bullet fails; text after the second list fails; fewer than 15 words of prose before the lists fails; the old heading fails.

### VA-2

- **The line** starts `**Aspiration:**`; its entries are split on `·` as today; each is a link followed by `(primary)` or `(supporting)`; `**Assessment:**` follows. A link's text is the aspiration's title; its target is `../pillars/` or `../principles/`, the element's file name, `#`, and the anchor. Exactly one primary, first; any number of supporting, no cap; no aspiration twice (D3).
- **The anchor is the one GitHub makes from the heading,** so the link works in a browser. `_link_anchors` computes it in a nested helper (`scripts/checks.py:270-277`); lift that helper to module level and call it, and do not write a second one. The anchor differs from the parser's `slug` for one existing title: "Shared human–agent work" is `#shared-humanagent-work` as an anchor and `shared-human-agent-work` as an id. Resolve a link by matching its anchor against each heading's anchor on the target page, and take the id from the parser.
- **The return contract.** `parse_gap_relationships` keeps returning `(relationships, primary)` as element references (`pillar:<id>`, `principle:<id>`), so the exporter and the App's contract are untouched: with the new line, `relationships` is the primary aspiration's element, then the supporting aspirations' elements in order, without repeats. A second function returns the aspiration references themselves, primary first, each `pillar:<element>/<id>` or `principle:<element>/<id>`. All three callers find the metadata line by either prefix; today two of them look for the literal `**Applies to:**`.
- **Until VA-5,** a gap may carry either line, never both. With the old line everything behaves as today.
- **The boundary check.** `boundary_signature` reads whichever line is present. When the base has the old line and the head has the new one, the line counts as unchanged only if, after projecting each aspiration to its element, the primary element is the same and the set of supporting elements is the same. Anything else (a primary under another element, a supporting element dropped or added) is a boundary change and needs its record. Once a gap is on the new line, any change to it is a boundary change. In `assess_boundary`, `Primary connection` and `Supporting connections` accept aspiration references (the pattern must allow `/`), and `Supporting connections` still accepts `None`.
- **Tests,** all unit tests: an anchor that matches no heading fails; a link to an element page with no anchor fails; two primaries fail; no primary fails; a primary that is not first fails; the same aspiration twice fails; four supporting aspirations pass; both lines on one gap fail; a gap on the old line still passes; old line to new line with the same primary element and the same set of supporting elements needs no record; a moved primary element with no record fails; a dropped supporting element with no record fails.

### VA-3

Start from [the drafts](inputs.md#the-drafts). Each new aspiration needs a short paragraph as well as its lists: write one from the owner's words in [inputs.md](inputs.md#what-the-owner-said) and put it in front of her with the lists. The task tightens wording against the shape in VA-1 and the test "could a reasonable developer have done the opposite"; it adds no bullet she has not seen. Bullets marked *(inverted)* or *(suggested)* merge only if she keeps them. Under D6 (b), this task also removes the two sections Packs absorbs, and the mapping for LS-001, LS-002 and LS-005 changes with it.

### VA-5

- Each gap's primary follows the mapping the owner approved (D6, D7, D8, D16). Its supporting aspirations start from [the proposals](inputs.md#supporting-aspirations): put them in front of the owner as one table, and merge what she marks up. Where she agrees none fits, the supporting element is dropped and that gap gets a boundary record saying so. Nothing is dropped without her seeing it.
- F-008's and F-004's Desired state: each stays non-empty (the feed requires it), links its aspiration, and repeats none of its bullets. The pull request shows the removed text beside the aspiration, so a reader can see nothing was lost. Both need a boundary record, as does any gap whose element moved.
- The four overlays named in the scope embed whole gap files on the old line; convert the line in each so the trees still produce exactly the errors `golden.txt` lists.
- Proof: `git grep -c "^\*\*Applies to:" -- vision/gaps scripts/fixtures` prints nothing; a unit test shows a gap on the old line is refused; `check` passes; `test_golden.py` passes unedited.

### VA-6

Each rule has one home; the others link to it. Homes were checked against the [improve skill's table](../../skills/astrid-dev-improve/SKILL.md#where-things-go):

- **Changing the vision's wording** already has a home: the "Vision" row of the table in `docs/contribution-workflow.md` (line 23), which says to edit the source files in `vision/`. Add to that row, in a clause: an aspiration is added, reworded or given lists by a pull request the owner approves, following `vision/templates/subject.md`. It does not say who approves today.
- **How a gap picks its aspirations** already has a home: the section "Define or reassess a vision gap" in the same file (line 36 says "one primary pillar or principle"). Reword it: one primary aspiration, the one the gap measures the distance to; supporting aspirations only where each explains a distinct relationship; never a pillar or principle. `templates/gap.md` line 3 and its comment show the line's form and link here; `skills/astrid-dev-gap/SKILL.md` line 12 names elements and aspirations and links here.
- **Using aspirations when planning** is new and goes in that same section (D12): a planner reads the aspirations of the plan's gaps; work that would break a "We should never" changes the aspiration first. One link from step 1 of the plan skill.
- **The table of homes** has no row for the vision: add one, "Vision wording: an element, an aspiration, its lists", pointing at the workflow row above, enforced by `subjects` and the owner's review. `docs/extending.md` needs nothing.
- **The glossary** has none of the three terms: add element, aspiration, and primary and supporting aspiration (of a gap), one line each.
- Then read every changed sentence once more for wording, against the glossary.

### R

One round on the integration branch after VA-6. Beyond the run contract's usual reading, the reviewer answers: can any feed this code emits be rejected by the App's parser at its `main`; is there any gap for which `appliesTo` changed without a boundary record; does the transition rule let through anything other than a move that keeps the same elements; does any person-facing file still say "characteristic".

### VA-7

Recorded in `evidence/phase-1.md`, each with the command and what came back:

1. `python3 scripts/astrid_dev.py check` on `main` passes; 22 gaps name an aspiration.
2. The six negative cases in [plan.md](plan.md#completion), each by its test name.
3. The `vision-consumer-contract` run on the merge commit, by its run link.
4. `git show origin/vision-published:vision.json`: the Packs item's `detailsMarkdown` holds both lists.
5. A person opens the live vision page, opens Liquid Software, expands Packs, and reports what they see against the expected Phase 1 look in [plan.md](plan.md#completion). Bullets run together or a missing label fails this step.

### VA-9

The outcome is [decided](inputs.md#the-vision-page-in-phase-2); this card builds its structure and data, and VA-10 its look.

- **With nothing opened,** an aspiration shows its title and first sentence, and beneath it one line per gap: the gap's name, the number of projects whose `primaryGapId` (or first `gapIds` entry) is that gap, and the name of the top one, the lowest `priorityOrder` among them. A gap with no project shows "No project yet".
- **An aspiration, opened,** adds the paragraph and the two lists.
- **A gap line, opened,** adds desired state, current state, what is missing and closure evidence, then all its projects, then, if it has supporting aspirations, one "Also relates to" line naming them.
- **A gap is listed once,** under its primary aspiration. An aspiration with no gap shows one quiet line.
- **The list "Gaps preventing this"** (`VisionDetailDialog.tsx:165-171`) is removed. The main page's flat gap list and projects section are not touched.
- **The lists** get rules so bullets are marked and indented; the page's base styling removes them today (`src/index.css:1`, and `PublicAstridVision.css:1526-1534` has no list rule).
- **The screen-reader label** at `VisionDetailDialog.tsx:140` says "Aspirations". It is the only place the page says "characteristic".
- **The validator** accepts optional `aspiration` and `supportingAspirations` on each gap and checks that each resolves to an element and one of its items. With the fields absent, gaps fall back to today's list under the element, so an older feed still loads.
- **Tests:** unit tests for grouping gaps by primary aspiration, the projects count, the top project, a gap with no project, the fallback, and a reference that resolves to nothing. A Playwright spec with a fixture feed asserts the at-a-glance line (gap name, count, top project) before anything is opened, then opens an aspiration, a gap and its projects.
- Code identifiers and the feed key stay `characteristics`.
- This card's base is the release line its release names; it opens no pull request to the App's `main`.

## 13 November execution updates

The owner delegated the two phases and the dismissal fix together. The implementation uses the accepted primary/supporting mapping and wording recommendations, without claiming personal markup or an independent reviewer. The feed fields and consumer ship together; no intermediate release that renders unstyled lists is needed.

| Follow-up | Scope and disposition | Proof |
| --- | --- | --- |
| VA-12 Outside taps dismiss once | Native dialog stays in the top layer through the final captured click; pointer cancellation, drag and keyboard activation do not dismiss it. | Delayed-click and real-touch tests pass in Chromium and WebKit in the initial candidate run. |
| R1.1 All linked projects | The new hierarchy counts all primary-linked projects, including finished work with its status; the legacy current-work list stays unchanged. | Unit expectation now includes the completed project; final candidate run pending. |
| R1.2 Null is not an omitted array | Reject null supporting-aspiration lists while preserving absence for older feeds. | Added negative unit case; final candidate run pending. |
| R1.3 Discovery has one home | Remove CA-004 from Shared Endeavor references after moving its primary to Open by design. | Element fixture and source updated together; structure and golden checks. |
| R1.4 Correct test scope | The new disclosure assertion selects the decision-list body, not its bold title. WebKit runs serially with a cold-transform budget, without retries. | Initial traces show the overbroad selector and unresolved cold Vite CSS load, not a failing dismissal. Rerun the same browser inventory. |
| Baseline test repairs | Mobile goal clamp: fixed five-line assumption becomes the actual responsive CSS budget. Color grouping: a deterministic primary-only fixture replaces an assumption that supporting gaps are duplicated. Layout: expand the existing ten-gap limit before selecting F-003. | These three tests failed on the untouched baseline. No golden line, test or assertion of the intended behavior was removed. |

Review provenance: the findings above are the implementer's source review, not an independent completion review. Production publication and the owner's physical-device look are not claimed until observed.
