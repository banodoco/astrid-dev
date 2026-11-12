# Tasks — Vision aspirations

[Plan](plan.md) · [Inputs](inputs.md)

No run has started. Paths and line numbers were read at astrid-dev `0ed58f9` and the App's `237b28b`; re-check them at dispatch. Phase 1 lands on one integration branch, `int/53-vision-aspirations`, and reaches `main` in two pull requests: the contract (VA-1 to VA-3, after RS1), then the rest.

**Task ids:** `VA-1`, `VA-2`, …; review stop `RS1`; review `R`. **Critical path:** VA-1 → VA-3 → RS1 → VA-6 → VA-8 → VA-11 → R, with the owner's mark-up of VA-4 and VA-5 joining before VA-6. Phase 2: VA-12 → VA-13 → VA-14 → VA-15. **Test inventory:** `scripts/test_vision_subject.py`, `scripts/test_export_public_vision.py`, `scripts/test_gap_relationships.py`, `scripts/test_check_gap_boundaries.py`, `scripts/test_checks.py`, `scripts/test_views.py`, `scripts/test_golden.py` (with the oracle `scripts/fixtures/golden.txt`), `scripts/test_project_contract.py` (must pass unedited). In the App, for VA-12: `src/pages/Home/publicVisionContent.test.ts`, `src/pages/Home/visionHierarchy.test.ts`, `tests/e2e/public-astrid-vision-characteristics.spec.ts`, `tests/e2e/public-astrid-vision-hierarchy.spec.ts`.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| VA-1 The authoring contract: an element has `## Aspirations`; each aspiration may carry the pair of lists | X | D2, D4, D13 | `scripts/vision_subject.py` (`SECTIONS`, `parse_subject`, `render_subject_markdown`); `vision/templates/subject.md` renamed `vision/templates/element.md`; the eight pages under `vision/pillars/` and `vision/principles/` (the one heading only); `scripts/checks.py:_subjects` (messages) and the file list in `_markdown_links`; `scripts/export_public_vision.py:render_readme` (the one sentence naming the template); `scripts/fixtures/vision/**` (the same heading and file rename); `scripts/fixtures/golden.txt` (only lines whose wording changes) | `python3 -m unittest discover -s scripts -p "test_vision_subject.py"` with the cases in [details](#va-1); `python3 scripts/astrid_dev.py check` passes; `git diff --stat <base> -- scripts/fixtures/golden.txt` shows only the lines listed on the card | [ ] |
| VA-2 The feed carries the lists and still reads as before | N | VA-1; D5 | `scripts/export_public_vision.py:project_subject`; `scripts/test_export_public_vision.py` | `python3 -m unittest discover -s scripts -p "test_export_public_vision.py"`: each item of `characteristics` keeps `id, title, summary, detailsMarkdown`, and has `should` and `shouldNever` only when the source has lists; `schemaVersion` is 1; in CI, `vision-consumer-contract` passes | [ ] |
| VA-3 A gap's first line may name an aspiration, and the check proves it exists | X | VA-1; D3, D10 | `scripts/gap_relationships.py` (`ENTRY`, `parse_gap_relationships`); `scripts/checks.py:_gap_structure`; `scripts/check_gap_boundaries.py` (`boundary_signature`, `assess_boundary`); `scripts/export_public_vision.py:build` (the gap loop); `templates/gap.md` (line 3); their four test files; fixtures under `scripts/fixtures/` for the negative cases; `scripts/fixtures/golden.txt` (added lines only) | The four test files pass with the cases in [details](#va-3); `check` passes with all 22 gaps still on the old line; the feed's `appliesTo` and `primaryAppliesTo` are byte-identical to the base for all 22 | [ ] |
| RS1 Review stop after the contract (rounds at most 1): the parser, the feed fields and the gap line | S | VA-1, VA-2, VA-3 | read-only | Same protocol as R, on the integration branch after VA-3; findings become rows `RS1.<n>`; VA-4 to VA-11 depend on this row; [what it looks for](#rs1) | [ ] |
| VA-4 Packs and Generation are written, in the owner's wording | T | VA-1 (the shape); D6; the owner's mark-up before merge | `vision/pillars/liquid-software.md` (one new `###` section); `vision/principles/eliminate-needless-technical-wrangling.md` (one new `###` section); the matching files under `scripts/fixtures/vision/` | The owner's marked-up text is what merges, recorded as a decision in `inputs.md`; `check` passes; each list has at most five bullets; [details](#va-4) | [ ] |
| VA-5 One aspiration is added and two are reworded, in the owner's wording | T | VA-1; D7, D16; the owner's mark-up before merge | `vision/pillars/shared-endeavour.md` (one new section); `vision/principles/local-first-cloud-capable.md` (the section "Optional cloud capabilities"); `vision/principles/open-by-design.md` (the section "Built for reuse"); the matching fixture files | As VA-4; each page still has two to six aspirations; no file on `main` links the two old anchors (`git grep` for `#optional-cloud-capabilities` and `#built-for-reuse` prints nothing) | [ ] |
| VA-6 All 22 gaps name an aspiration, and the old line is refused from then on | N | RS1; VA-4, VA-5 (the targets exist under their final titles); D8, D10 | the first metadata line of each file in `vision/gaps/`; `scripts/gap_relationships.py:parse_gap_relationships` and `scripts/checks.py:_gap_structure` (remove the old line's acceptance); the fixture gaps; `scripts/fixtures/golden.txt` (listed lines) | `git grep -c "^\*\*Applies to:" -- vision/gaps` prints nothing; `check` passes; a fixture gap with the old line fails; the feed's `primaryAppliesTo` differs from the base only for the gaps D7 and D8 moved to another element; the pull request carries a boundary record for exactly those gaps and for F-004 and F-008 | [ ] |
| VA-7 F-008 and F-004 keep only what is specific to the gap | T | VA-4, VA-6; D9; the owner's mark-up before merge | the `## Desired state` section of `vision/gaps/F-008-portable-generation.md` and `vision/gaps/F-004-pack-lifecycle.md` | Each Desired state is non-empty, links its aspiration and repeats none of its bullets; nothing in the removed text is missing from the aspiration (a side-by-side in the pull request); the boundary records for both are in the description | [ ] |
| VA-8 The generated overview lists each gap under its aspiration; the hand-kept gap lists go | N | VA-6; D11 | `scripts/export_public_vision.py:render_readme`; `scripts/views.py` (only if the view's sources change); `vision/README.md` (generated; do not hand-edit); the `## References` sections of the eight element pages (the lines that list gaps only); `scripts/test_export_public_vision.py`, `scripts/test_views.py` | `python3 scripts/astrid_dev.py sync` then `check` pass; the overview shows 22 gaps, each once, each under the aspiration its file names, and marks an aspiration with no gap; no element page lists a gap by hand | [ ] |
| VA-9 The one rule and the words that point at it | X | VA-3; D12, D13 | `docs/contribution-workflow.md` (the section "Define or reassess a vision gap"); `templates/gap.md` (the comment block); `skills/astrid-dev-gap/SKILL.md` (line 12 and one link); `skills/astrid-dev-plan/SKILL.md` (one link in step 1); `skills/astrid-dev-shared/glossary.md` (three terms: element, aspiration, and gap's link to one) | `check` passes, including `link-anchors`; `git grep -n -i "characteristic" -- docs skills templates vision` prints nothing outside `scripts/`; total added words at most 150, counted with `wc -w` before and after and stated in the pull request | [ ] |
| VA-10 The wording of the template and the rule | T | VA-1, VA-9 | `vision/templates/element.md` (prose only: no heading changes); the paragraph VA-9 added to `docs/contribution-workflow.md` | Before and after for each sentence; all tests pass unedited; the word count is not higher than after VA-9 | [ ] |
| VA-11 The proof | N | VA-2, VA-6, VA-7, VA-8, VA-9; the second pull request merged to `main`; a person for two minutes | `plans/53-vision-aspirations/evidence/phase-1.md` (new) | The observations in [details](#va-11) | [ ] |
| R Review rounds (at most 1, pending the owner's agreement) | S | VA-1 to VA-10 | read-only | Rounds per the [run contract](../../skills/astrid-dev-shared/run-contract.md): findings become rows `R1.<n>` added directly below this one, each with route, scope, dependencies and proof; the second pull request's merge and VA-11 wait for them | [ ] |
| VA-12 Phase 2: the App reads `aspirations`, styles the lists and shows each gap under its aspiration | X | Release 13 published; D14; the release that takes it, and that release's manager | in astrid-app: `src/pages/Home/publicVisionContent.ts` (types, `parsePublicVisionContent`); `VisionDetailDialog.tsx`; `visionHierarchy.ts`; `PublicAstridVision.tsx` (`GapPoint`); `PublicAstridVision.css`; the test files in the inventory; `scripts/quality/check-public-vision-production.mjs` | That repository's own checks; the parser accepts a feed with `characteristics` only, with both keys, and with `aspirations` only; the dialog shows a gap under its aspiration; [details](#va-12) | [ ] |
| VA-13 Phase 2: the feed carries `aspirations` beside `characteristics` | N | VA-12 on the App's `main` | `scripts/export_public_vision.py:project_subject`; `scripts/test_export_public_vision.py` | The test file passes; `vision-consumer-contract` passes; both keys hold the same items | [ ] |
| VA-14 Phase 2: the feed drops `characteristics` | N | VA-13; the release with VA-12 is live, confirmed by its manager or the owner | `scripts/export_public_vision.py:project_subject`; `scripts/vision_subject.py` (the returned key); their tests | The test files pass; `vision-consumer-contract` passes; the published feed has no `characteristics` key | [ ] |
| VA-15 Phase 2: the live page, seen | owner | VA-14 | the browser | The owner opens the vision page, opens a pillar, and sees its aspirations with styled lists and its gaps under them; noted in `evidence/phase-2.md` | [ ] |

## Sizes and who runs each card

Engineering days, from [inputs.md](inputs.md#estimates). The recommended run is a manager session that sends each N and X card to a Codex worker and keeps T cards on Claude; the review rows go to a fresh high-judgment sub-agent that has not seen the cards being built.

| Task | Who | Size |
| --- | --- | --- |
| VA-1 | X worker | 0.4 |
| VA-2 | cheap worker | 0.2 |
| VA-3 | X worker | 0.6 |
| RS1 | high-judgment sub-agent | 0.2 |
| VA-4 | taste, on Claude, then the owner | 0.3 |
| VA-5 | taste, on Claude, then the owner | 0.1 |
| VA-6 | cheap worker | 0.3 |
| VA-7 | taste, on Claude, then the owner | 0.2 |
| VA-8 | cheap worker | 0.3 |
| VA-9 | X worker | 0.2 |
| VA-10 | taste, on Claude | 0.1 |
| VA-11 | cheap worker | 0.1 |
| R | high-judgment sub-agent | 0.2 |
| VA-12 | X worker, in the App | 1.0 |
| VA-13, VA-14 | cheap worker | 0.3 |
| VA-15 | the owner | 0.1 |

Phase 1 about 3.2: N 1.0, X 1.2, S 0.4, T 0.7, rounded down to 3.0 for the cards that run side by side. Phase 2 about 1.5.

**What can run side by side:** VA-4, VA-5 and VA-9's drafting can start as soon as VA-1's shape is fixed; they merge after RS1. VA-2 and VA-3 both change `export_public_vision.py`, in different functions: merge VA-2 first.

## Details

### VA-1

- Section names become Statement, Explanation, Aspirations, optional References. `## Characteristics` is refused with a message that names the new heading.
- Inside an aspiration, after the summary sentence and a blank line: prose, then optionally a paragraph that is exactly `**We should:**` followed by a bullet list, then a paragraph that is exactly `**We should never:**` followed by a bullet list. Nothing follows the second list.
- Both or neither. One to five bullets in each. Each bullet passes `one_sentence`. The 15-word minimum counts the prose only.
- The parsed item keeps `id, title, summary, detailsMarkdown`, where `detailsMarkdown` still holds the lists as written, and gains `should` and `shouldNever` (lists of strings) when present.
- The returned key stays `characteristics` until VA-14, so every caller is unchanged in Phase 1.
- Tests: the eight real pages parse; an aspiration with both lists parses; one list alone fails; six bullets fail; a two-sentence bullet fails; text after the second list fails; the old heading fails.

### VA-3

- The line starts `**Aspiration:**`; its entries are split on `·` as today; each is a link followed by `(primary)` or `(supporting)`; `**Assessment:**` follows. A link's text is the aspiration's title and its target is `../pillars/` or `../principles/`, the element's file name, `#`, and the anchor. Exactly one primary, first; at most two supporting.
- **The anchor is the one GitHub makes from the heading,** so the link works in a browser. `scripts/checks.py:_link_anchors` already computes it; reuse that function and do not write a second one. It differs from the parser's `slug` for one existing title: "Shared human–agent work" is `#shared-humanagent-work` as an anchor and `shared-human-agent-work` as an id. Resolve a link to its aspiration by matching the anchor against each heading's anchor, and take the feed id from the parser.
- The reference is `pillar:<element>/<id>` or `principle:<element>/<id>`. The feed gains `aspiration` (the primary) and `supportingAspirations` on each gap. `appliesTo` becomes the elements of those aspirations, primary first, without repeats; `primaryAppliesTo` is the primary's element.
- Until VA-6, a gap may carry either line, never both. With the old line the feed is unchanged and has no `aspiration` field.
- `boundary_signature` reads whichever line is present. Under D10 (a): when the base has the old line and the head has the new one, the line counts as unchanged if the primary element is the same; any later change to the aspiration line is a boundary change. `assess_boundary`'s two connection fields accept an aspiration reference.
- Tests and fixtures: an anchor that matches no heading fails; a link to an element page with no anchor fails; two primaries fail; three supporting fail; both lines on one gap fail; a gap on the old line still passes.
- Do not extend `_link_anchors` to all of `vision/`: this task checks the gap line's anchors only.

### RS1

The reviewer reads the integration branch after VA-3 and answers: can any feed this code emits be rejected by the App's parser at its `main`; is there any input for which the old and new gap lines give different `primaryAppliesTo`; does the D10 exemption let through anything other than a same-element move; are the new feed field names ones Phase 2 can keep.

### VA-4

Start from [the drafts](inputs.md#the-drafts). The task tightens wording against the shape in VA-1 and the test "could a reasonable developer have done the opposite"; it adds no bullet the owner has not seen. The bullets marked *(inverted)* or *(suggested)* merge only if she keeps them. Under D6 (b), this task also removes the two sections Packs absorbs, and VA-6's mapping for LS-001, LS-002 and LS-005 changes with it.

### VA-11

Recorded in `evidence/phase-1.md`, each with the command and what came back:

1. `python3 scripts/astrid_dev.py check` on `main` passes; the count of gaps naming an aspiration is 22.
2. The six negative cases in [plan.md](plan.md#completion), each by its test or fixture name.
3. The `vision-consumer-contract` run on the merge commit, by its run link.
4. `git show origin/vision-published:vision.json`: the Packs item's `detailsMarkdown` holds both lists, and `should` and `shouldNever` are present.
5. A person opens the live vision page, opens Liquid Software, expands Packs, and says what they see. If the lists are unreadable with default styling, that is a finding for VA-12, not a failure of Phase 1.

### VA-12

The App's parser treats `aspirations` and `characteristics` as the same list under two names and accepts either or both; with neither it falls back to `bodyMarkdown` as today. The dialog's heading and the screen-reader label say "Aspirations". Each gap is listed under the aspiration named in its `aspiration` field, and under the element as today when the field is absent. The production check script stops assuming one fixed gap id. This card's base is the release line its release names; it opens no pull request to the App's `main`.
