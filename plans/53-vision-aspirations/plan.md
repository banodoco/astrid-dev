# Vision aspirations

**Project:** Vision aspirations

**Goal:** Anyone deciding how a part of Astrid should work, such as packs or generation, finds one short reference under the vision that says what we should do and what we should never do, and every gap is measured against it.

**Status:** active

**Owner:** Plan 53 manager

**Estimate:** about 4.5 (Phase 1 about 2.7; Phase 2 about 1.8)

**Waiting on:** the owner's mark-up of five aspirations and of the proposed supporting aspirations ([inputs.md](inputs.md#owner-decisions))

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [CA-003 — Our vision and execution aren't yet fully connected](../../vision/gaps/CA-003-vision-experiments-progress.md) (primary): this plan makes each gap point at one stated aspiration, so a reader can follow vision, aspiration, gap and plan in one line. CA-003 has no route to closure and none of its closure-evidence items is delivered here, so there is no `Contributes to closure` line.

## Outcome and scope

Today the vision has two levels that carry weight, and a third that does not. Pillars and principles each have "characteristics": 28 short sections that say what must be true. They do not say what that rules out, and no gap points at one. A gap names up to four pillars and principles instead. The philosophy for a part of the product has no home: the owner's idea of how generation should work is written inside gap F-008 as its desired state, and how packs should work is spread over five characteristics, two gaps and a plan.

When this is done, the vision is three levels, and each level links only one level up:

1. **The vision:** the one statement.
2. **Elements:** the pillars and principles. One type, two kinds; the folder (`vision/pillars/`, `vision/principles/`) is the kind.
3. **Aspirations:** what each element is trying to reach. Today's characteristics, renamed, in the same place: a `###` section inside the element's page.

An aspiration is a title, one sentence, a short paragraph, and two optional lists: **We should** and **We should never**. The lists are what a developer or agent decides from. Each bullet is one sentence that a reasonable developer could have done the opposite of; a list has at most five.

Then:

- **Every gap names one main aspiration,** and as many supporting ones as it needs. A gap never names a pillar or principle; its elements follow from its aspirations. Each supporting pillar or principle a gap names today becomes a supporting aspiration inside it, or is dropped with a record where none fits ([proposals](inputs.md#supporting-aspirations); D3).
- **Three aspirations are new and two are reworded,** so 28 become 31. Packs and Generation are written from the owner's words. One more covers contributing in parallel. "Optional cloud capabilities" is reworded to say that everything should be able to run locally and nothing should have to, and "Built for reuse" is widened to cover being found. After that, every gap has an aspiration that fits ([mapping](inputs.md#the-proposed-mapping)).
- **F-008 and F-004 stop carrying the philosophy.** Their desired state shrinks to what is specific to the gap and points at the aspiration.
- **A planner reads the aspirations of the plan's gaps.** Work that would break a "We should never" changes the aspiration first, in a pull request the owner approves.
- **The public vision page shows it in two steps.** In Phase 1 the new text is on the page with no App change, but plainly: the lists appear as unmarked, unindented lines under their bold labels, because the page's styling removes list markers. In Phase 2 the page becomes one hierarchy a visitor can open level by level: inside a pillar or principle, each aspiration shows at a glance its gaps by name, with the number of projects and the top project for each; opening an aspiration adds its paragraph and lists, and opening a gap adds its description and all its projects ([the decided outcome](inputs.md#the-vision-page-in-phase-2); D17).

**Included:** the parser, the template's text, the eight element pages, the 22 gaps' first line, the gap template, the gap checks and their tests and fixtures, one rule in the contribution workflow with links to it, one row in the improve skill's table of homes, three glossary terms, and, in Phase 2, two fields in the feed and the App's vision page.

**Not included:**

- a fourth level, or a new kind of element;
- a file per aspiration, or moving or renaming any vision file;
- renaming anything in the feed: its key stays `characteristics` for good, since no reader sees it and older App builds reject a feed without it;
- renaming code: Python names and the template file keep "subject";
- renumbering gaps: `F-008` and `LS-001` stay, since plans, labels and issues cite them;
- writing the two lists for the 28 existing aspirations. They are filled in later, one at a time, where a decision keeps being re-argued;
- a generated list of gaps under each aspiration in `vision/README.md` (cut after the critique; the App shows it in Phase 2);
- new gaps for the 14 aspirations that have none. That count is a finding ([inputs.md](inputs.md#the-proposed-mapping)), not work;
- a bot, or any automation that edits text under `vision/`;
- any App change before Release 13 publishes.

**Limits a reader should know.** A check can prove a gap names an aspiration that exists. It cannot prove the aspiration is the right one, or that a bullet is worth having; the owner's reading does that. The lists give a planner something to decide from; they do not stop a pull request that ignores them.

## Existing work and decision

Almost all of the machinery exists, and this plan changes its words more than its shape. One parser (`scripts/vision_subject.py`) already reads pillars and principles from one template, so "one type, two kinds" is already true in code. One exporter builds the public feed from the same files. One parser reads a gap's first line, and three callers use it.

The App, read at its `main` ([inputs.md](inputs.md#prior-art-what-was-read)), rejects the whole feed unless each element has a `characteristics` list of two to six items, and requires each gap's `appliesTo` to name a pillar or principle. So the feed keeps both, worked out from the new source. Phase 1 adds no field to the feed: an aspiration's lists travel inside the text the feed already carries.

[Plan 44](../44-vision-execution-trail/plan.md) serves the same gap from the other end: it proposes a public trail from projects and evidence back to gaps. This plan fixes the link above the gap. Neither needs the other.

Alternatives compared, including a new level, a file per aspiration, and doing only the two new pages: [inputs.md](inputs.md#alternatives-including-doing-less). An independent critique read this pack against the code and cut it by about a fifth; its findings and what was done are in [inputs.md](inputs.md#critique). The owner's choices are in [Owner decisions](inputs.md#owner-decisions); what is still hers is wording.

## Sequence and readiness

1. **The contract:** the parser reads `## Aspirations` and the two lists (VA-1); a gap's line may name an aspiration (VA-2). During this step a gap may use either line, so nothing else has to move at the same time.
2. **The words the owner marks up:** Packs and Generation (VA-3); the third new aspiration and the two reworded ones (VA-4). These are drafted while step 1 runs and merge after it.
3. **The gaps move:** all 22 name an aspiration, F-008 and F-004 are trimmed, and the old line is refused from then on (VA-5).
4. **The rule and its links** (VA-6), one review round (R), then the proof (VA-7).
5. **Phase 2, with the first release after Release 13:** the feed gains each gap's aspirations (VA-8); the App shows the hierarchy (VA-9); its layout is polished and the owner looks at it before it ships (VA-10).

**Constraints.** astrid-dev's required check `vision-consumer-contract` runs the App's `vision:check` at the App's `main`, unpinned, so every astrid-dev pull request must keep the feed readable by whatever the App's `main` is that day. The live page reads the published feed directly. App `main` deploys to production; its change rides with a release.

**Ready to run** once the scope pull request merges and the owner starts a run; her mark-up of the wording happens inside VA-3, VA-4 and VA-5. Recording this plan authorizes no work. [Tasks](tasks.md).

## Interfaces and handoff

**Consumes:** astrid-dev `main` at the run's base; the App's `main` as CI checks it out, for the feed's contract (read at `237b28b` for this plan); the eight element pages and 22 gaps as they stand.

**Produces:**

- the authoring contract in `vision/templates/subject.md`: `## Aspirations`, each with an optional pair of lists;
- the gap line, in `templates/gap.md`: `**Aspiration:**`, then one link marked `(primary)` and any number marked `(supporting)`, then `**Assessment:**`. Each link's text is the aspiration's title and its target is the element's page with the aspiration's anchor, for example `../pillars/liquid-software.md#live-tool-composition`;
- an aspiration's reference, `pillar:<element>/<aspiration>` or `principle:<element>/<aspiration>`, used in a gap's boundary record and, from Phase 2, in the feed;
- a feed whose shape is unchanged in Phase 1: `schemaVersion` 1, `characteristics`, `appliesTo` and `primaryAppliesTo` all stay. Each gap's `appliesTo` is the element of its primary aspiration, then the elements of its supporting ones, without repeats;
- in Phase 2, two added fields on each gap, `aspiration` and `supportingAspirations`, each reference carrying the element and the aspiration's id, in the same phase as the App code that reads them.

**Limits.** An aspiration's identity is its title: renaming one changes its anchor and reference, and the check then fails every gap that names it until they are updated in the same pull request. That is the intended cost of a rename. The link's anchor is the one GitHub makes from the heading, which differs from the feed's id for one existing title ([VA-2](tasks.md#va-2)).

## Completion

Phase 1 is done when all of these are observed:

- `python3 scripts/astrid_dev.py check` passes on `main`, and every gap's first line names one primary aspiration, and only aspirations that exist under an element page.
- The Liquid Software page has the Packs aspiration, the technical-wrangling page has the Generation aspiration, and the local-first page has "Everything local or cloud, by choice", each with a paragraph and both lists, in wording the owner marked up.
- The proposed feed passes the App's `vision:check` in CI, and the feed on the `vision-published` branch holds the Packs lists inside that item's `detailsMarkdown`.
- A person opens the live vision page, opens Liquid Software, expands Packs, and sees the paragraph, the two bold labels, and each bullet as its own plain line with no marker or indent. That plain look is the expected Phase 1 result; anything worse (bullets run together, a label missing) is a failure.

**Negative cases,** each a unit test, so the oracle `scripts/fixtures/golden.txt` does not change:

- a gap naming an aspiration that does not exist fails (this also covers an aspiration renamed without its gaps);
- a gap still using `**Applies to:**` fails;
- a gap with two primary aspirations, or none, fails;
- an aspiration with one list and not the other fails;
- a list of six bullets fails;
- in the pull request that moves the gaps, a gap whose primary element or set of supporting elements differs from before, with no boundary record, fails.

The gap line's anchor check is part of `python3 scripts/astrid_dev.py check`, which the required `documentation` check runs on every pull request.

Phase 2 is done when, on the deployed App, a visitor opens a pillar and, without opening anything further, sees under each aspiration one line per gap with its name, its number of projects and its top project (a Playwright spec asserts that line against a fixture feed); opening an aspiration adds its paragraph and lists; opening a gap adds its description and all its projects; the lists are marked and indented; the old element-level "Gaps preventing this" list is gone; and the page still loads a feed that has no `aspiration` field.

**Limits of this proof:** it shows the structure holds and the page shows it. It does not show that planners read the aspirations, or that the bullets settle arguments; the first plan that touches packs or generation after this is the real test. Publishing the App change belongs to a release and its owner, not to this plan.
