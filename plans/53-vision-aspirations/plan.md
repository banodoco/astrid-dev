# Vision aspirations

**Project:** Vision aspirations

**Goal:** Anyone deciding how a part of Astrid should work, such as packs or generation, finds one short reference under the vision that says what we should do and what we should never do, and every gap is measured against it.

**Status:** queued

**Owner:** Unassigned

**Estimate:** about 4.5 (Phase 1 about 3.0; Phase 2 about 1.5)

**Waiting on:** the owner's decisions D4 to D16 in [inputs.md](inputs.md#owner-decisions), an independent critique, and the scope pull request

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

- **Every gap names one aspiration.** A gap's first line says `**Aspiration:**` and links one primary aspiration, with at most two supporting. A gap never names a pillar or principle directly; its element follows from its aspiration.
- **Three aspirations are new and two are reworded,** so 28 become 31. Packs and Generation are written from the owner's words. One more covers contributing in parallel. "Optional cloud capabilities" is reworded to say that everything should be able to run locally and nothing should have to, and "Built for reuse" is widened to cover being found. After that, every gap has an aspiration that fits ([mapping](inputs.md#the-proposed-mapping)).
- **F-008 and F-004 stop carrying the philosophy.** Their desired state shrinks to what is specific to the gap and points at the aspiration.
- **The generated vision overview lists each gap under its aspiration,** and the hand-kept gap lists at the foot of the element pages go.
- **A planner reads the aspirations of the plan's gaps.** Work that would break a "We should never" changes the aspiration first, in a pull request the owner approves.
- **The public vision page shows all of it.** In Phase 1 the lists appear on the page with no App change, because the page already renders each section's body as formatted text. In Phase 2 the App styles the lists and shows each gap under its aspiration.

**Included:** the parser, the template, the eight element pages, the 22 gaps' first line, the gap template, the checks and their tests and fixtures, the public feed, the generated overview, one rule in the contribution workflow with links to it, three glossary terms, and, in Phase 2, the App's vision page.

**Not included:**

- a fourth level, or a new kind of element;
- a file per aspiration, or moving the element pages;
- renumbering gaps: `F-008` and `LS-001` stay, since plans, labels and issues cite them;
- writing the two lists for the 28 existing aspirations. They are filled in later, one at a time, where a decision keeps being re-argued;
- new gaps for the 14 aspirations that have none. That count is a finding ([inputs.md](inputs.md#the-proposed-mapping)), not work;
- a bot, or any automation that edits text under `vision/`;
- any App change before Release 13 publishes.

**Limits a reader should know.** A check can prove a gap names an aspiration that exists. It cannot prove the aspiration is the right one, or that a bullet is worth having; the owner's reading does that. The lists give a planner something to decide from; they do not stop a pull request that ignores them.

## Existing work and decision

Almost all of the machinery exists, and this plan changes its words more than its shape. One parser (`scripts/vision_subject.py`) already reads pillars and principles from one template, so "one type, two kinds" is already true in code. One exporter builds the public feed and the generated overview from the same files. One parser reads a gap's first line. The App's page already says "aspirations" in its copy and never shows the word "characteristic".

Two constraints come from the App, read at its `main` ([inputs.md](inputs.md#prior-art-what-was-read)). It rejects the whole feed unless each element has a `characteristics` list of two to six items, and it requires each gap's `appliesTo` to name a pillar or principle. It ignores keys it does not know. So Phase 1 keeps both of those in the feed, working them out from the new source, and adds the new fields beside them. Nothing on the page can break, and the lists show at once.

[Plan 44](../44-vision-execution-trail/plan.md) serves the same gap from the other end: it proposes a public trail from projects and evidence back to gaps. This plan fixes the link above the gap. Neither needs the other.

Alternatives compared, including a new level, a file per aspiration, and doing only the two new pages: [inputs.md](inputs.md#alternatives-including-doing-less). The owner's choices so far, and the ones still open, are in [Owner decisions](inputs.md#owner-decisions). An independent critique is required before greenlight and has not happened yet.

## Sequence and readiness

1. **The contract first:** the parser reads `## Aspirations` and the two lists (VA-1); the feed carries them (VA-2); a gap's line may name an aspiration (VA-3). During this step a gap may use either line, so nothing else has to move at the same time.
2. **A review stop** (RS1) on that contract, because every later task builds on it.
3. **The words the owner marks up:** Packs and Generation (VA-4); the third new aspiration and the two reworded ones (VA-5). These can be drafted while step 1 runs; they merge after it.
4. **The gaps move:** all 22 name an aspiration, and the old line is refused from then on (VA-6); F-008 and F-004 are trimmed (VA-7).
5. **The generated overview and the rule** (VA-8, VA-9, VA-10), then the proof (VA-11) and one review round (R).
6. **Phase 2, with the first release after Release 13:** the App reads the new shape (VA-12); only when that release is live does the feed drop the old key (VA-13, VA-14).

**Constraints.** astrid-dev's required check `vision-consumer-contract` runs the App's `vision:check` at the App's `main`, unpinned, so every astrid-dev pull request in Phase 1 must keep the feed readable by whatever the App's `main` is that day. The live page reads the published feed directly, so the feed may drop `characteristics` only after an App that reads `aspirations` is deployed. App `main` deploys to production; its change rides with a release.

**Not ready until:** the owner has answered D4 to D16, and the critique has been read and answered. Recording this plan authorizes no work. [Tasks](tasks.md).

## Interfaces and handoff

**Consumes:** astrid-dev `main` at the run's base; the App's `main` as CI checks it out, for the feed's contract (read at `237b28b` for this plan); the eight element pages and 22 gaps as they stand.

**Produces:**

- the authoring contract in `vision/templates/element.md`: `## Aspirations`, each with an optional pair of lists;
- the gap line, in `templates/gap.md`: `**Aspiration:**`, then one link marked `(primary)` and up to two marked `(supporting)`, then `**Assessment:**`. Each link's text is the aspiration's title and its target is the element's page with the aspiration's anchor, for example `../pillars/liquid-software.md#live-tool-composition`;
- an aspiration's reference, `pillar:<element>/<aspiration>` or `principle:<element>/<aspiration>`, used in the feed and in a gap's boundary record;
- feed fields added in Phase 1, all ignored by today's App: `should` and `shouldNever` on each item of `characteristics`; `aspiration` and `supportingAspirations` on each gap. `schemaVersion` stays 1, and `characteristics`, `appliesTo` and `primaryAppliesTo` stay, derived;
- in Phase 2, the key `aspirations` on each element, first beside `characteristics` and later instead of it.

**Limits.** An aspiration's identity is its title: renaming one changes its anchor and reference, and the check then fails every gap that names it until they are updated in the same pull request. That is the intended cost of a rename. The link's anchor is the one GitHub makes from the heading, which differs from the feed's id for one existing title ([VA-3](tasks.md#va-3)).

## Completion

Phase 1 is done when all of these are observed:

- `python3 scripts/astrid_dev.py check` passes on `main`, and every gap's first line names an aspiration that exists under an element page.
- The Liquid Software page has the Packs aspiration, the technical-wrangling page has the Generation aspiration, and the local-first page has "Local or cloud, by choice", each with both lists, in wording the owner marked up.
- The proposed feed passes the App's `vision:check` in CI, and the feed on the `vision-published` branch holds the Packs lists inside that item's `detailsMarkdown`, and as `should` and `shouldNever`.
- A person opens the live vision page, opens Liquid Software, and sees the two lists under Packs.
- The generated `vision/README.md` shows each gap under its aspiration.

**Negative cases:** a gap naming an aspiration that does not exist fails the check; a gap still using `**Applies to:**` fails; a gap with two primary aspirations, or three supporting, fails; an aspiration with one list and not the other fails; a list of six bullets fails; an aspiration renamed without its gaps fails. Each is a fixture or a unit test, and the lines they add to the oracle `scripts/fixtures/golden.txt` are listed on the task that adds them.

Phase 2 is done when the deployed App shows each gap under its aspiration, styles the lists, and still loads with a feed that has only `aspirations`; and the feed has then dropped `characteristics`.

**Limits of this proof:** it shows the structure holds and the page shows it. It does not show that planners read the aspirations, or that the bullets settle arguments; the first plan that touches packs or generation after this is the real test. Publishing the App change belongs to a release and its owner, not to this plan.
