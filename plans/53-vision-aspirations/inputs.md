# Inputs — Vision aspirations

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Partly accepted — 12 Nov 2026. The owner chose the name "aspirations", the "We should / We should never" shape, that every gap is tied to an aspiration, that the existing characteristics are converted, that the vision page shows them, and that Packs and Generation exist ([what she said](#what-the-owner-said); D1 to D3, D16). She has not seen this pack. Next: she answers D4 to D16, and a maintainer-reviewed scope pull request records the answers.

**Prior art:** Read on astrid-dev `main` at `0ed58f99d1543ac87c1c5759549aba7edcd13320` and the App's `main` at `237b28be935af49c23464fa6ca1cf30db67ebaa0`, on 12 Nov 2026, by three read-only helpers; the planner re-read the code each task scope depends on. One parser already serves pillars and principles; the App rejects a feed without `characteristics` and ignores unknown keys; 18 of 22 gaps fit an existing characteristic under the element they already name as primary. [What was read](#prior-art-what-was-read).

**Approach:** Rename and extend what exists; add no record kind, folder or level. One heading changes in eight pages, the parser learns two optional lists, a gap's first line names an aspiration, and the feed adds fields beside the ones the App needs. A new level, a file per aspiration, a third kind of element, and doing only the two new pages were compared: [Alternatives](#alternatives-including-doing-less).

**Challenge:** Pending — required and not yet done. The plan changes astrid-dev's own checks and a contract another repository reads, so the planning skill requires an independent critique before greenlight. Next: the orchestrator sends this pack to a fresh session with no stake in it, briefed to build as little as possible and to check the claims against the code, and records its findings here. Tasks most likely to be cut are named in [What a critic should test](#what-a-critic-should-test).

**Proof and limits:** Every gap names an aspiration that exists; six planted failures are refused; the proposed feed passes the App's own check; the published feed and the live page show the Packs lists ([plan.md](plan.md#completion)). Never proven by this plan: that the bullets are the right ones, or that planners read them.

**Review rounds:** Recommended: one review stop of at most one round (RS1) after the contract, and one final round (R), both on the S route ([guide](../../skills/astrid-dev-shared/run-contract.md#review-and-promotion-boundaries)). The stop protects VA-4 to VA-11: a fault in the gap line or the feed fields found at the end would mean re-pointing 22 gaps twice and could break the live vision page. Next: the owner confirms the numbers (D15).

**Run start:** Pending — No run is authorized. Next: when the owner starts a run, record the date, the phase or tasks it covers, the accountable session ([who that is](../../skills/astrid-dev-shared/run-contract.md#who-answers-for-a-run)), what it may do without asking, what still needs the owner's go, and the advisor session if there is one. Recommended shape: a manager session that sends each N and X card to a Codex worker and keeps the T cards on Claude.

### What the owner said

In the [orchestrator's session](https://claude.ai/code/session_011EzfW38XJUpUFewfUM9MxF), 12 Nov 2026, in her words, shortened:

- On the purpose: she wants to "capture all the different parts of the vision, like the details and like how all the different pieces of the philosophy implemented work together", so that "when a developer, or an agent is working on that part, they have this reference document" that says "what this means, what this doesn't mean, bullet point, bullet point". "We don't want it to become overburdened."
- On the levels: "there's this overarching vision, then there's the kind of element … of two kinds, and then there's basically the characteristics of those". Pillars and principles are "two versions of the same thing … one version with a different type". She rejected a separate new level and the word "foundation".
- On the name: "I was talking about aspirations being instead of aims, to be clear."
- On the shape: "a paragraph maybe, and then … what this means we should do, what this means we should never do."
- On gaps: "whatever gaps are always associated … they should always be associated with kind of aims or aspirations."
- On the existing ones: "the bullet points should be converted into these, and then see how they're currently displayed on the … vision page. That these should be explained instead of them."
- On generation: "one generation path, and then you can choose the engine, which could be like either Cloud, ComfyUI, Wan2GP, other inference engines, then choose the machine … built in an almost neutral way so that you can plug in any inference engine plus any machine."
- On local and cloud: "everything should be ABLE to run locally but shouldn't have to".
- On packs: "the packs should basically render live. They should render instantly. They should be able to be live vibe coded. They should be … completely portable. They should … interoperate … You should be able to extend other packs inside one pack … there should be a defined way for creating an extension, that across the front end and Python back end that generalizes." And: "they should be able to run on the web app."

### Prior art: what was read

**The authoring contract, `scripts/vision_subject.py`:**

- `parse_subject` requires the sections Statement, Explanation, Characteristics and optional References, in order; two to six `###` sections; each a one-sentence summary, a blank line, then at least 15 words of detail.
- A section's id is `slug(title)`: lower case, apostrophes dropped, every other run of non-alphanumerics turned into one hyphen.
- It returns `characteristics: [{id, title, summary, detailsMarkdown}]`. `render_subject_markdown` writes the heading `## Characteristics` into the derived body.

**The feed and the generated overview, `scripts/export_public_vision.py`:**

- `project_subject` copies `characteristics` into each pillar and principle; `schemaVersion` is 1.
- Each gap's `appliesTo` and `primaryAppliesTo` come from `parse_gap_relationships` and must be in the set of `pillar:<id>` and `principle:<id>`.
- `render_readme` writes `vision/README.md`; one sentence there names the template file and the word "characteristics". The overview lists gaps flat, not under an element.

**A gap's first line, `scripts/gap_relationships.py`:** `**Applies to:**`, entries split on `·`, each a link to `../pillars/<x>.md` or `../principles/<x>.md` followed by `(primary)` or `(supporting)`; exactly one primary, first. No anchors are allowed.

**Checks, `scripts/checks.py`:** `gap-structure` requires the `**Applies to:**` field; `subjects` requires four files per folder and parses each; `markdown-links` names `vision/templates/subject.md` as a file that must exist; `link-anchors` checks fragments only for links into `skills/`, `templates/` and `docs/*.md`, so nothing today checks a fragment into `vision/`.

**The boundary check, `scripts/check_gap_boundaries.py`:** `boundary_signature` includes the text after `**Applies to:**`, so any change to that line asks for a seven-field record per gap in the pull request description; two of the fields accept only `pillar:<id>` or `principle:<id>`.

**The App's vision page, at `237b28b`:**

- `parsePublicVisionContent` (`src/pages/Home/publicVisionContent.ts`) is hand-written and keeps unknown keys. If any element has `statement`, `explanationMarkdown` or `characteristics`, every element must have all three, with two to six characteristics. Each gap's `appliesTo` must resolve to a pillar or principle.
- `VisionDetailDialog.tsx` shows each characteristic as a closed disclosure: title and summary, then `detailsMarkdown` rendered as CommonMark. A bold label and a bullet list inside it render today, with the browser's default list styling.
- The page never shows the word "characteristic": the heading is "What defines this". Other copy already says "aspirations".
- A pillar or principle's dialog lists the gaps whose `primaryAppliesTo` is that element. Nothing reads a link from a gap to a characteristic.
- `npm run vision:check` runs `publicVisionContent.test.ts`; with `PUBLIC_VISION_FEED_FILE` set it asserts the candidate feed parses, with four pillars and four principles.
- `scripts/quality/check-public-vision-production.mjs` checks the live page after a deploy; it expects `schemaVersion` 1 and the element id `gap-aa-001`.

**Who else names the old words:** `templates/gap.md:3`; `docs/contribution-workflow.md:36` ("Every gap has **one primary pillar or principle**"); `skills/astrid-dev-gap/SKILL.md:12`; `vision/templates/subject.md`; the eight element pages; `scripts/fixtures/vision/**`, a copy of the vision files that the fixture trees are built on. No file on `main` links to an anchor inside an element page.

**The gap ID letters** (`AA`, `LS`, `CI`, `CA`, `F`) are defined only by a pattern; no file says what they stand for. This plan does not change them.

### The proposed mapping

A helper read each gap's Desired state and Gap sections against the 28 section headings. This is a proposal for the owner (D8), not a finding of fact.

| Gap | Primary element today | Proposed aspiration | Confidence |
|---|---|---|---|
| AA-001 Sustained creative work | Artistic Ambition | Finished artistic work | medium: "Continuity and iteration" is close |
| CA-001 Creative challenge culture | Shared Endeavor | Shared challenges and ambition | high |
| CA-002 Contributor ownership | Shared Endeavor | A meaningful stake in the collective | high |
| CA-003 Vision, experiments, progress | Open by design | Open decisions and working knowledge | high |
| CA-004 Sharing and discovery | Shared Endeavor | none fits today; "Built for reuse" under Open by design, widened to "Built to be found and reused" | reworded aspiration, and the gap changes element (D7) |
| CA-005 Parallel contribution | Shared Endeavor | none fits today; new "Many hands, one clear way in" under Shared Endeavor | new aspiration (D7) |
| CI-001 Agent learning loop | Compounding | An ecosystem of wisdom grounded in real work | high |
| CI-002 Federated knowledge | Compounding | Share without surrendering control | high |
| CI-003 Public source ingestion | Compounding | Use knowledge with judgment | medium: ingestion itself is not covered |
| F-001 Platform reliability | Technical wrangling | Dependable execution and recovery | high |
| F-002 Safe user control | Creator's control | Explicit permissions and privacy | high |
| F-003 Creative execution | Technical wrangling | Dependable execution and recovery | high |
| F-004 Pack lifecycle | Liquid Software | none fits | new aspiration: Packs (D6) |
| F-005 Local files, cloud assist | Local-first | Optional cloud capabilities | high |
| F-006 Fully hosted workspace | Local-first | Optional cloud capabilities, reworded "Local or cloud, by choice" | low as it stands; high once reworded (D16) |
| F-007 First-class sandbox | Creator's control | Explicit permissions and privacy | high |
| F-008 Portable generation | Technical wrangling | none fits | new aspiration: Generation (D6) |
| LS-001 Portable components | Liquid Software | Live tool composition | high |
| LS-002 Agent workspace control | Liquid Software | Live tool composition | high |
| LS-003 Full-stack contributions | Liquid Software | Shared human–agent work | medium: Packs may fit better once written |
| LS-004 Cross-modal foundations | Liquid Software | A small, dependable foundation | medium |
| LS-005 Agent-managed tools | Liquid Software | Real-time functionality | high |

**What the table shows.** As the pages stand, thirteen fit with high confidence, four with medium, one with low, and four fit nothing. In all 18 that fit, the aspiration sits under the element the gap already names as primary, so the feed's `primaryAppliesTo` does not change for them. With the recommendations in D6, D7 and D16, every gap has a home: three aspirations are new (Packs, Generation, "Many hands, one clear way in") and two are reworded, so 28 become 31. The fullest page, Liquid Software, reaches six, the most a page allows; Shared Endeavor and technical wrangling reach four. Only CA-004 changes element, from Shared Endeavor to Open by design, so it alone moves on the vision page. Fourteen of the 28 existing aspirations have no gap at all: either Astrid is already there, or nobody has measured. That is recorded here as a finding; this plan writes no gaps for them.

### The drafts

Starting text for VA-4 and VA-5, for the owner to mark up. The "We should" bullets are her words rearranged. The "We should never" bullets marked *(inverted)* are the planner's inversions of what she said, and the ones marked *(suggested)* are the planner's own; neither kind is hers until she says so.

**Packs are live, portable and extensible** (under Agent-Powered Liquid Software)

A pack should be something you can change while you are using it and take anywhere Astrid runs.

We should:

- Render a pack's changes in the running app at once, including the web app.
- Let a creator or agent vibe-code a pack while working in it.
- Make one pack run unchanged on any install.
- Let a pack extend another pack from inside it.
- Give one defined way to build an extension that covers the front end and the Python back end together.

We should never:

- Require a rebuild or restart to see a pack change. *(inverted)*
- Tie a pack to one machine or one install. *(inverted)*
- Add a second way to write an extension for one side only. *(inverted)*
- Build a feature that only works because it bypasses the pack contract. *(suggested)*

**One generation path, any engine, any machine** (under Eliminate technical wrangling)

Every generation should run the same way wherever it runs and whatever runs it.

We should:

- Send every generation, in every modality, through one path.
- Make the engine a choice on that path: a cloud service, ComfyUI, Wan2GP, others.
- Make the machine a separate choice: this computer, your own server, a rented GPU.
- Let a new engine or machine plug in by meeting a declared contract, and then work with everything on the other side.

We should never:

- Add a route for one modality or one pack "just for now". *(inverted)*
- Build an engine so that it only works with one kind of machine. *(inverted)*
- Hide from the creator where a generation runs; there is a default they can change. *(suggested)*
- Build our own inference engine. *(suggested)*

One difference to settle while marking up: she named a cloud service as an engine; F-008 lists only ComfyUI and Wan2GP as engines and treats rented machines as machines.

**Local or cloud, by choice** (under Local-first, cloud-capable; today's "Optional cloud capabilities", reworded)

Everything should be able to run locally, and nothing should have to.

The sentence is hers. The bullets are the orchestrator's proposal to her, not yet read by her.

We should:

- Make every capability work fully on the creator's own machine.
- Let a creator run the whole workspace in the cloud if they choose.
- Let work move back into the creator's custody.

We should never:

- Ship a capability that only works in the cloud.
- Require a local machine to use Astrid.
- Move work to the cloud without the creator choosing it.

**Many hands, one clear way in** (new, under A Shared Creative Endeavor; the orchestrator's working title)

Any person or agent should be able to pick up useful work and land it without getting in anyone else's way.

No lists are drafted. VA-5 writes the paragraph, and lists only if the owner asks for them.

**Built to be found and reused** (under Completely open by design; today's "Built for reuse", widened)

VA-5 widens the title, sentence and paragraph so that finding a contribution is part of it. No lists are drafted.

### Alternatives, including doing less

| Option | What it gives | Why not, or why |
|---|---|---|
| A new level between elements and gaps ("areas") | A page per part of the product | The owner rejected it: the level below elements already exists. |
| A third kind of element ("foundations") | Packs and Generation as peers of pillars | The owner rejected it: it reads as the same level as a pillar. It would also change the App's "exactly four pillars" contract. |
| A file per aspiration | A stable path for each | About 31 files in place of 8, a new record kind and a new parser, for a reference people read a page at a time. |
| Only add Packs and Generation as two more characteristics; leave gaps alone | The two references she asked for, in a day | Gaps would still point at up to four elements, and F-008 would still hold the generation philosophy. It does not answer "gaps should always be associated with aspirations". |
| Rename in the feed at once | One word everywhere | The live page reads the feed directly and rejects it without `characteristics`. |
| This plan | Three levels, one link up from each, shown on the page from day one | Chosen. Costs a parser change, 22 one-line edits and a later App change. |

### What a critic should test

- **VA-8** (the overview lists gaps under aspirations, and the hand-kept lists go) is the task most likely not to earn its cost. The App's dialog will show the same thing in Phase 2.
- **D10** (how the one-time re-point passes the boundary check): whether the narrow exemption is honest, or whether 22 records are the right price.
- **VA-13 and VA-14** (emit both keys, then drop one): whether the feed should simply keep `characteristics` for good and never rename, since no reader sees the key.
- Whether both-or-neither and the five-bullet cap belong in the parser or only in the template's prose.

### Ten vivid statements

Offered to the owner before she reads the tasks. Each is true of the plan as written.

1. Now, a gap can point at four pillars and principles. After, it points at one aspiration.
2. The word "characteristic" disappears from everything a person reads, and no visitor to the vision page will notice, because the page never showed it.
3. Pillars and principles stay in two folders. The folder is the kind; nothing moves.
4. F-008 stops being where the generation philosophy lives. The philosophy moves up; the gap keeps only the distance.
5. The "We should never" lists appear on the live vision page the day they merge, with no App release.
6. An aspiration with a "We should" list and no "We should never" list is refused by a check.
7. No list may have a sixth bullet.
8. Twenty-eight aspirations become thirty-one. Only Packs, Generation and "Local or cloud, by choice" get lists in this plan; the rest keep their paragraph.
9. Renaming an aspiration breaks every gap that names it until they are fixed in the same pull request.
10. Fourteen aspirations will show, on the generated overview, that no gap measures them.
11. Plans still link gaps, never aspirations. Each level links one level up.
12. The App is not touched until Release 13 has published.

### Estimates

Engineering days. Phase 1: VA-1 0.4, VA-2 0.2, VA-3 0.6, RS1 0.2, VA-4 0.3, VA-5 0.1, VA-6 0.3, VA-7 0.2, VA-8 0.3, VA-9 0.2, VA-10 0.1, VA-11 0.1, R 0.2, about 3.2 with the manager's joins counted once. Phase 2: VA-12 1.0, VA-13 0.2, VA-14 0.1, VA-15 0.1, about 1.5 with review inside VA-12's own repository. The owner's reading time for VA-4, VA-5 and D8 is not counted.

## Owner decisions

- **D1. What is the third level called?** *Decided, 12 Nov 2026: "aspirations".* The top two are the vision and its elements (pillars and principles).
- **D2. What is an aspiration made of?** *Decided, 12 Nov 2026:* a title, one sentence, a short paragraph, and "We should" and "We should never". *Recommended, awaiting the owner:* the lists are optional but come as a pair; each has one to five bullets; each bullet is one sentence a reasonable developer could have done the opposite of.
- **D3. What does a gap attach to?** *Decided, 12 Nov 2026:* always an aspiration, never a pillar or principle directly. *Recommended, awaiting the owner:* exactly one primary and at most two supporting, each supporting one justified in the gap's text.
- **D4. Where do aspirations live?** (a) Inside the element's page, as today's `###` sections, with `## Characteristics` renamed `## Aspirations`; the two folders stay as the kind. (b) One file per aspiration. (c) One `vision/elements/` folder with a kind line. *Recommended: (a).* Awaiting the owner.
- **D5. Does the feed rename at once?** (a) Phase 1 keeps `characteristics`, `appliesTo` and `schemaVersion` 1, and adds fields; the key changes in Phase 2 after an App that reads it is live. (b) Rename now and change the App in the same week. (c) Never rename the key. *Recommended: (a).* (b) is not possible before Release 13 publishes. Awaiting the owner.
- **D6. Where do Packs and Generation sit, and does Packs absorb anything?** That they exist is *decided, 12 Nov 2026.* (a) Packs is a sixth aspiration under Agent-Powered Liquid Software, the most a page allows; Generation is a fourth under Eliminate technical wrangling. (b) Packs replaces "Live tool composition" and "Real-time functionality", which overlap with it. *Recommended: (a).* Under (b), LS-001, LS-002 and LS-005 lose the aspirations they fit with high confidence and would all hang on Packs. Awaiting the owner.
- **D7. What do CA-004 (sharing and discovery) and CA-005 (parallel contribution) attach to?** (a) CA-005 gets a new aspiration under A Shared Creative Endeavor, working title "Many hands, one clear way in"; CA-004 gets none: "Built for reuse" under Open by design is widened to "Built to be found and reused". (b) One new aspiration under Shared Endeavor for both. (c) Two new aspirations, one each. *Recommended: (a), the orchestrator's proposal.* Its cost: CA-004 changes element, so it moves on the vision page and needs a boundary record. Awaiting the owner.
- **D8. Is the [proposed mapping](#the-proposed-mapping) right?** The five medium and low rows (AA-001, CI-003, F-006, LS-003, LS-004) most need her eye. *Recommended:* accept the 13 high rows as they are and rule on the five. Awaiting the owner.
- **D9. Which gaps have their Desired state trimmed?** (a) Only F-008 and F-004, whose philosophy moves into Generation and Packs. (b) All eight that a helper judged to state philosophy. *Recommended: (a).* Each gap keeps a Desired state, which the App requires. Awaiting the owner.
- **D10. How does the one-time re-point of 22 gaps pass the boundary check?** (a) The check treats a move from the old line to an aspiration under the same primary element as no change of boundary; her approval of the mapping (D8) is the review; a gap whose element moves, or whose Desired state is trimmed, still needs its record. (b) All 22 carry the seven-field record. (c) The check is switched off for that pull request. *Recommended: (a).* After the move, changing a gap's aspiration always needs a record. Awaiting the owner.
- **D11. Does the generated overview list gaps under their aspiration?** (a) Yes, and the hand-kept gap lists in the element pages' References go. (b) No; leave the overview and the lists. *Recommended: (a), as its own task a critic may cut.* Awaiting the owner.
- **D12. Where is the one rule about using aspirations?** The rule: a planner reads the aspirations of the plan's gaps; work that would break a "We should never" changes the aspiration first, in a pull request the owner approves; wording under `vision/` is the owner's. (a) In the contribution workflow's section on vision gaps, with one link each from the plan skill and the gap skill. (b) In the plan skill. *Recommended: (a).* It binds reviewers and gap assessors as well as planners. Plans keep linking gaps only. Awaiting the owner.
- **D13. What do the files and the code call an element?** (a) What people read says "element" and "aspiration": the template becomes `vision/templates/element.md`; Python names such as `parse_subject` stay. (b) Rename the code as well. (c) Leave the template's name. *Recommended: (a).* It costs four references; (b) touches every caller and test for no reader's benefit. Awaiting the owner.
- **D14. Is Phase 2 committed?** (a) Yes: the App reads `aspirations`, styles the lists and shows each gap under its aspiration, in the first release after Release 13; then the feed drops the old key. (b) Stop after Phase 1 and decide later. *Recommended: (a).* Awaiting the owner.
- **D15. How many review rounds?** *Recommended:* one stop of at most one round after the contract (RS1), and one final round (R). Awaiting the owner.
- **D16. How does the vision say "local or cloud"?** *Decided, 12 Nov 2026, in her words:* "everything should be ABLE to run locally but shouldn't have to". *Recommended, awaiting the owner:* (a) the existing aspiration "Optional cloud capabilities" under Local-first, cloud-capable is reworded to carry it, with the title "Local or cloud, by choice", her sentence, and the lists in [The drafts](#the-drafts); F-006 then fits it. (b) Add a new aspiration and leave the old one, which would make two aspirations say nearly the same thing.

## Source identities

- **astrid-dev:** `banodoco/astrid-dev`, `main` at `0ed58f99d1543ac87c1c5759549aba7edcd13320` when this pack was written. The run records its own base at dispatch and re-checks every path and line here.
- **The App:** `banodoco/astrid-app`, `main` at `237b28be935af49c23464fa6ca1cf30db67ebaa0`, read only. Phase 2's base is the release line the release's manager names, not `main`.
- **Destination:** Phase 1 lands on an integration branch and reaches astrid-dev `main` by pull request. Phase 2's App change goes to a release's branches; this plan opens no pull request to the App's `main`.

## References

- The [orchestrator's session](https://claude.ai/code/session_011EzfW38XJUpUFewfUM9MxF), where the owner described the outcome and the three helpers reported.
- The public page: [astrid.haus/vision](https://astrid.haus/vision). The published feed: branch `vision-published`, file `vision.json`.
- [Plan 44](../44-vision-execution-trail/plan.md), which serves CA-003 from the evidence side.
