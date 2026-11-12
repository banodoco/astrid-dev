# Tasks — Vision aspirations

[Plan](plan.md) · [Inputs](inputs.md)

No run has started. Paths and line numbers were read at astrid-dev `0ed58f9` and the App's `237b28b`; re-check them at dispatch. Phase 1 lands on one integration branch, `int/53-vision-aspirations`, and reaches `main` in two pull requests: the contract (VA-1, VA-2), then the rest.

**Task ids:** `VA-1`, `VA-2`, …; review `R`. **Critical path:** VA-1 → VA-2 → VA-5 → R → VA-7, with the owner's mark-up of VA-3 and VA-4 joining before VA-5. Phase 2: VA-8 → VA-9 → VA-10. **Test inventory:** `scripts/test_vision_subject.py`, `scripts/test_export_public_vision.py`, `scripts/test_gap_relationships.py`, `scripts/test_check_gap_boundaries.py`, `scripts/test_checks.py`; and, passing unedited, `scripts/test_views.py`, `scripts/test_golden.py` (the oracle `scripts/fixtures/golden.txt` does not change in this plan) and `scripts/test_project_contract.py`. In the App, for VA-9: `src/pages/Home/publicVisionContent.test.ts`, `src/pages/Home/visionHierarchy.test.ts`, `tests/e2e/public-astrid-vision-characteristics.spec.ts`, `tests/e2e/public-astrid-vision-hierarchy.spec.ts`.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| VA-1 The authoring contract: an element has `## Aspirations`; each aspiration may carry the pair of lists | X | D2 | `scripts/vision_subject.py` (`SECTIONS`, `parse_subject`, `render_subject_markdown`); `vision/templates/subject.md` (text; the file keeps its name); the eight pages under `vision/pillars/` and `vision/principles/` (the one heading only); `scripts/checks.py:_subjects` (message wording only); `scripts/export_public_vision.py:render_readme` (the one sentence that says "characteristics"); `scripts/fixtures/vision/**` (the same heading); `scripts/test_vision_subject.py`, `scripts/test_export_public_vision.py` | `python3 -m unittest discover -s scripts -p "test_vision_subject.py"` with the cases in [details](#va-1); `test_export_public_vision.py` passes with the feed's keys unchanged; `python3 scripts/astrid_dev.py check` passes; `git diff --stat <base> -- scripts/fixtures/golden.txt` prints nothing | [ ] |
| VA-2 A gap's first line may name one aspiration, and the check proves it exists | X | VA-1; D3 | `scripts/gap_relationships.py` (`ENTRY`, `parse_gap_relationships` and its return contract); its three callers: `scripts/checks.py:_gap_structure`, `scripts/checks.py:_boundary_impl`, `scripts/export_public_vision.py:build` (the gap loop); `scripts/check_gap_boundaries.py` (`boundary_signature`, and in `assess_boundary` the pattern for the two connection fields); `scripts/checks.py:_link_anchors` (lift its nested `anchors` helper to module level, behaviour unchanged); `templates/gap.md` (line 3); the four gap test files in the inventory | Those test files pass with the cases in [details](#va-2); `check` passes with all 22 gaps still on the old line; for those 22 the feed is byte-identical to the base; `golden.txt` unchanged | [ ] |
| VA-3 Packs and Generation are written, in the owner's wording | T | VA-1 (the shape); D6; the owner's mark-up before merge | `vision/pillars/liquid-software.md` (one new `###` section); `vision/principles/eliminate-needless-technical-wrangling.md` (one new `###` section); the matching files under `scripts/fixtures/vision/` | The owner's marked-up text is what merges, recorded as a decision in `inputs.md`; each section has a sentence, a paragraph of at least 15 words and both lists, at most five bullets each; `check` passes; [details](#va-3) | [ ] |
| VA-4 One aspiration is added and two are reworded, in the owner's wording | T | VA-1; D7, D16; the owner's mark-up before merge | `vision/pillars/shared-endeavour.md` (one new section); `vision/principles/local-first-cloud-capable.md` (the section "Optional cloud capabilities"); `vision/principles/open-by-design.md` (the section "Built for reuse"); the matching fixture files | As VA-3, with lists only where [the drafts](inputs.md#the-drafts) have them; each page still has two to six aspirations | [ ] |
| VA-5 All 22 gaps name one aspiration; F-008 and F-004 keep only what is specific to them; the old line is refused from then on | X | VA-2; VA-3, VA-4 (the targets exist under their final titles); D3, D8, D9; the owner's mark-up of the two Desired states | the first metadata line of each file in `vision/gaps/`; the `## Desired state` section of `F-008-portable-generation.md` and `F-004-pack-lifecycle.md`; `vision/pillars/shared-endeavour.md` (the one References line about CA-004, only if D7 moves that gap); `scripts/gap_relationships.py:parse_gap_relationships` and `scripts/checks.py:_gap_structure` and `:_boundary_impl` (remove the old line's acceptance); the gap files under `scripts/fixtures/vision/` and the gaps embedded in the overlays `missing-gap-section`, `route-missing-closure-approach`, `route-missing-plan` and `route-status-word` | [Details](#va-5): no gap on the old line; `check` passes; `golden.txt` unchanged; the feed's `primaryAppliesTo` differs from the base only for gaps D7 or D8 moved to another element; the pull request cites D3 and carries a boundary record for exactly those gaps and for F-004 and F-008 | [ ] |
| VA-6 The one rule, the words that point at it, and their wording | X | VA-2; D12 | `docs/contribution-workflow.md` (the section "Define or reassess a vision gap"); `templates/gap.md` (the comment block); `skills/astrid-dev-gap/SKILL.md` (line 12 and one link); `skills/astrid-dev-plan/SKILL.md` (one link in step 1); `skills/astrid-dev-shared/glossary.md` (three terms: element, aspiration, and a gap's link to one) | `check` passes, including `link-anchors`; `git grep -n -i "characteristic" -- docs skills templates vision` prints nothing; before and after for each changed sentence; words added at most 150, counted with `wc -w` and stated in the pull request | [ ] |
| R Review rounds (at most 1, pending the owner's agreement) | S | VA-1 to VA-6 | read-only | Rounds per the [run contract](../../skills/astrid-dev-shared/run-contract.md): findings become rows `R1.<n>` added directly below this one, each with route, scope, dependencies and proof; the second pull request's merge and VA-7 wait for them; [what it looks for](#r) | [ ] |
| VA-7 The proof | N | R; the second pull request merged to `main`; a person for two minutes | `plans/53-vision-aspirations/evidence/phase-1.md` (new) | The observations in [details](#va-7) | [ ] |
| VA-8 Phase 2: the feed names each gap's aspiration | N | Release 13 published; VA-5 on `main` | `scripts/export_public_vision.py:build` (the gap loop); `scripts/test_export_public_vision.py` | The test file passes: each gap has `aspiration`, a reference that resolves to an item of `characteristics` under its `primaryAppliesTo` element; `vision-consumer-contract` passes | [ ] |
| VA-9 Phase 2: the App styles the lists and shows each gap under its aspiration | X | VA-8; the release that takes it, and that release's manager | in astrid-app: `src/pages/Home/publicVisionContent.ts` (types, `parsePublicVisionContent`: the optional `aspiration` field); `VisionDetailDialog.tsx` (the label at line 140; gaps under their aspiration); `visionHierarchy.ts`; `PublicAstridVision.css` (list rules for the section body); the test files in the inventory | That repository's own checks; [details](#va-9) | [ ] |
| VA-10 Phase 2: the live page, seen | owner | VA-9's release is live | the browser | The owner opens the vision page, opens a pillar, and sees its aspirations with marked, indented lists and its gaps under them; noted in `evidence/phase-2.md` | [ ] |

No review-stop row: after the cuts the contract is two tasks, and its questions are in R.

## Sizes and who runs each card

Engineering days. This table is the one home for sizes; `plan.md`'s Estimate line carries the totals.

| Task | Who | Size |
| --- | --- | --- |
| VA-1 | X worker | 0.4 |
| VA-2 | X worker | 0.6 |
| VA-3 | taste, then the owner | 0.3 |
| VA-4 | taste, then the owner | 0.2 |
| VA-5 | X worker, then the owner for two sections | 0.5 |
| VA-6 | X worker | 0.3 |
| R | high-judgment sub-agent | 0.2 |
| VA-7 | cheap worker | 0.1 |
| VA-8 | cheap worker | 0.1 |
| VA-9 | X worker, in the App | 0.8 |
| VA-10 | the owner | 0.1 |

Phase 1 is 2.6: X 1.8, T 0.5, S 0.2, N 0.1. Phase 2 is 1.0. The owner's reading time is not counted.

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

- **The line** starts `**Aspiration:**`, then one link, then ` · **Assessment:**`. The link's text is the aspiration's title; its target is `../pillars/` or `../principles/`, the element's file name, `#`, and the anchor. Under D3 (a) there is exactly one link and no `(primary)` mark. Under D3 (b) the line takes up to two more links marked `(supporting)`; build that only if the owner chooses it.
- **The anchor is the one GitHub makes from the heading,** so the link works in a browser. `_link_anchors` computes it in a nested helper (`scripts/checks.py:270-277`); lift that helper to module level and call it, and do not write a second one. The anchor differs from the parser's `slug` for one existing title: "Shared human–agent work" is `#shared-humanagent-work` as an anchor and `shared-human-agent-work` as an id. Resolve a link by matching its anchor against each heading's anchor on the target page, and take the id from the parser.
- **The return contract.** `parse_gap_relationships` keeps returning `(relationships, primary)` as element references (`pillar:<id>`, `principle:<id>`), so the exporter and the App's contract are untouched: with the new line, `relationships` is the one element of the gap's aspiration. A second function returns the aspiration's reference, `pillar:<element>/<id>` or `principle:<element>/<id>`. All three callers find the metadata line by either prefix; today two of them look for the literal `**Applies to:**`.
- **Until VA-5,** a gap may carry either line, never both. With the old line everything behaves as today.
- **The boundary check.** `boundary_signature` reads whichever line is present. When the base has the old line and the head has the new one, the line counts as unchanged if the aspiration's element equals the old primary element; the supporting elements that drop are covered by the owner's decision D3, which the pull request cites. An aspiration under a different element is a boundary change and needs its record. Once a gap is on the new line, any change to it is a boundary change. In `assess_boundary`, `Primary connection` accepts an aspiration reference (the pattern must allow `/`) and `Supporting connections` accepts `None`.
- **Tests,** all unit tests: an anchor that matches no heading fails; a link to an element page with no anchor fails; two links fail under D3 (a); both lines on one gap fail; a gap on the old line still passes; old line to new line under the same element needs no record; old line to new line under another element with no record fails.

### VA-3

Start from [the drafts](inputs.md#the-drafts). Each new aspiration needs a short paragraph as well as its lists: write one from the owner's words in [inputs.md](inputs.md#what-the-owner-said) and put it in front of her with the lists. The task tightens wording against the shape in VA-1 and the test "could a reasonable developer have done the opposite"; it adds no bullet she has not seen. Bullets marked *(inverted)* or *(suggested)* merge only if she keeps them. Under D6 (b), this task also removes the two sections Packs absorbs, and the mapping for LS-001, LS-002 and LS-005 changes with it.

### VA-5

- Each gap's line follows the mapping the owner approved under D8, D6, D7 and D16. Under D3 (a) the old supporting entries are dropped and nothing replaces them.
- F-008's and F-004's Desired state: each stays non-empty (the feed requires it), links its aspiration, and repeats none of its bullets. The pull request shows the removed text beside the aspiration, so a reader can see nothing was lost. Both need a boundary record, as does any gap whose element moved.
- The four overlays named in the scope embed whole gap files on the old line; convert the line in each so the trees still produce exactly the errors `golden.txt` lists.
- Proof: `git grep -c "^\*\*Applies to:" -- vision/gaps scripts/fixtures` prints nothing; a unit test shows a gap on the old line is refused; `check` passes; `test_golden.py` passes unedited.

### R

One round on the integration branch after VA-6. Beyond the run contract's usual reading, the reviewer answers: can any feed this code emits be rejected by the App's parser at its `main`; is there any gap for which `primaryAppliesTo` changed without a boundary record; does the transition rule let through anything other than a same-element move; does any person-facing file still say "characteristic".

### VA-7

Recorded in `evidence/phase-1.md`, each with the command and what came back:

1. `python3 scripts/astrid_dev.py check` on `main` passes; 22 gaps name an aspiration.
2. The six negative cases in [plan.md](plan.md#completion), each by its test name.
3. The `vision-consumer-contract` run on the merge commit, by its run link.
4. `git show origin/vision-published:vision.json`: the Packs item's `detailsMarkdown` holds both lists.
5. A person opens the live vision page, opens Liquid Software, expands Packs, and reports what they see against the expected Phase 1 look in [plan.md](plan.md#completion). Bullets run together or a missing label fails this step.

### VA-9

- The section body in the dialog gets list rules, so bullets are marked and indented; the page's base styling removes them today (`src/index.css:1`, and `PublicAstridVision.css:1526-1534` has no list rule).
- The screen-reader label at `VisionDetailDialog.tsx:140` says "Aspirations". It is the only place the page says "characteristic".
- The parser accepts an optional `aspiration` on each gap and checks that it resolves. The dialog lists each gap under the aspiration it names, and under the element as today when the field is absent.
- Code identifiers and the feed key stay `characteristics`.
- This card's base is the release line its release names; it opens no pull request to the App's `main`.
