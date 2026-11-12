# Inputs — Vision aspirations

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Partly accepted — 12 Nov 2026. The owner chose the name "aspirations", the "We should / We should never" shape, that every gap is tied to an aspiration, that the existing characteristics are converted, that the vision page shows them, that Packs and Generation exist, and that everything should be able to run locally without having to ([what she said](#what-the-owner-said); D1 to D3, D6, D8, D9, D16). She then answered the open decisions the same day (D3, D6, D8, D9, D16; D7 in substance). Still hers: the wording of the five new or reworded aspirations and the proposed supporting aspirations, both marked up inside the run. Next: a maintainer-reviewed scope pull request ([astrid-dev#629](https://github.com/banodoco/astrid-dev/pull/629)) records this.

**Prior art:** Read on astrid-dev `main` at `0ed58f99d1543ac87c1c5759549aba7edcd13320` and the App's `main` at `237b28be935af49c23464fa6ca1cf30db67ebaa0`, on 12 Nov 2026, by three read-only helpers; the planner re-read the code each task scope depends on, and the critic re-read it again. One parser already serves pillars and principles; the App rejects a feed without `characteristics`; 18 of 22 gaps fit an existing characteristic under the element they already name as primary. [What was read](#prior-art-what-was-read).

**Approach:** Rename and extend what exists; add no record kind, folder, file, level or feed field in Phase 1. One heading changes in eight pages, the parser learns two optional lists, and a gap's first line names one aspiration. A new level, a file per aspiration, a third kind of element, renaming the feed, and doing only the two new pages were compared: [Alternatives](#alternatives-including-doing-less).

**Challenge:** Reviewed — one round on 12 Nov 2026 by a fresh session with no stake in the draft, on commit `2a22b12` of this pack's branch, read against both repositories. It was required: the plan changes astrid-dev's own checks and a contract another repository reads. It found three blockers and eight should-fix items; all were accepted, one in a different form, and the pack was revised. The revised pack has not had a second round. [Critique](#critique).

**Proof and limits:** Every gap names one aspiration that exists; six planted failures are refused, each by a unit test; the proposed feed passes the App's own check; the published feed and the live page show the Packs lists in their plain Phase 1 form ([plan.md](plan.md#completion)). Never proven by this plan: that the bullets are the right ones, or that planners read them.

**Review rounds:** One final round (R), at most one, on the S route ([guide](../../skills/astrid-dev-shared/run-contract.md#review-and-promotion-boundaries)), before the second pull request merges. No review stop: after the critique's cuts the contract is two tasks, and the stop's questions moved into R. Decided by the planner (D15); the owner may change the number.

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
- On local and cloud: "everything should be ABLE to run locally but shouldn't have to"; and, for its title, "everything can be local or cloud by choice".
- On how many aspirations a gap has: "one main one" and "as many as need be supporting".
- On the vision page: show "the gaps beneath each characteristic… that you can then expand, so it just shows the gaps in the title, and you can expand to look at them and the projects within that"; "the aspiration, then the gap title, and then… 3 projects tackling this, and then they can click into it to get the description… and what the projects tackling it are". It should make the pop-ups "a lot more succinct" and give "a really nice hierarchy of ideas… visual for people to understand"; today it feels "a little bit disconnected" because gaps and projects sit below.
- On the recommendations: "I agree with where you say for positioning", "I agree with what you mean for the gap placement", "and the desired state".
- On packs: "the packs should basically render live. They should render instantly. They should be able to be live vibe coded. They should be … completely portable. They should … interoperate … You should be able to extend other packs inside one pack … there should be a defined way for creating an extension, that across the front end and Python back end that generalizes." And: "they should be able to run on the web app."

### Prior art: what was read

**The authoring contract, `scripts/vision_subject.py`:**

- `parse_subject` requires the sections Statement, Explanation, Characteristics and optional References, in order; two to six `###` sections; each a one-sentence summary, a blank line, then at least 15 words of detail. A References section, if present, must not be empty.
- A section's id is `slug(title)`: lower case, apostrophes dropped, every other run of non-alphanumerics turned into one hyphen.
- It returns `characteristics: [{id, title, summary, detailsMarkdown}]`. `render_subject_markdown` writes the heading `## Characteristics` into the derived body.

**The feed and the generated overview, `scripts/export_public_vision.py`:**

- `project_subject` copies `characteristics` into each pillar and principle; `schemaVersion` is 1.
- Each gap's `appliesTo` and `primaryAppliesTo` come from `parse_gap_relationships` and must be in the set of `pillar:<id>` and `principle:<id>`.
- `render_readme` writes `vision/README.md`; one sentence there says "characteristics".

**A gap's first line, `scripts/gap_relationships.py`:** `**Applies to:**`, entries split on `·`, each a link to `../pillars/<x>.md` or `../principles/<x>.md` followed by `(primary)` or `(supporting)`; exactly one primary, first. No anchors are allowed. Three callers use it: `checks.py:_gap_structure`, `checks.py:_boundary_impl` (which finds the line by the literal `**Applies to:**`), and the exporter.

**Checks, `scripts/checks.py`:** `gap-structure` requires the `**Applies to:**` field; `subjects` requires four files per folder and parses each; `link-anchors` checks fragments only for links into `skills/`, `templates/` and `docs/*.md`, so nothing today checks a fragment into `vision/`. Its anchor function is a closure nested inside `_link_anchors` (lines 270 to 277).

**The boundary check, `scripts/check_gap_boundaries.py`:** `boundary_signature` includes the text after `**Applies to:**`, so any change to that line asks for a seven-field record per gap in the pull request description; two of the fields accept only `pillar:<id>` or `principle:<id>`, a pattern that cannot hold a `/`.

**Fixtures:** `scripts/fixtures/vision/**` is a copy of the vision files that the fixture trees are built on. Four overlays embed whole gap files on the old line: `missing-gap-section`, `route-missing-closure-approach`, `route-missing-plan`, `route-status-word`. No line of `scripts/fixtures/golden.txt` mentions "characteristics" or "Applies to".

**The App's vision page, at `237b28b`:**

- `parsePublicVisionContent` (`src/pages/Home/publicVisionContent.ts`) is hand-written and keeps unknown keys. If any element has `statement`, `explanationMarkdown` or `characteristics`, every element must have all three, with two to six characteristics (lines 118 to 129). Each gap's `appliesTo` must resolve to a pillar or principle.
- `VisionDetailDialog.tsx` shows each characteristic as a closed disclosure: title and summary, then `detailsMarkdown` rendered as CommonMark. A bullet list inside it becomes list elements, but the page's base styling removes list markers and indents (`src/index.css:1`), and the stylesheet has no list rule for that body (`PublicAstridVision.css:1526-1534`). So a list shows today as plain lines, one per bullet.
- The page says "characteristic" in one place: a screen-reader label at `VisionDetailDialog.tsx:140`. The visible heading is "What defines this", and the page's own copy already says "aspirations" (`PublicAstridVision.tsx:544`, "How we plan to reach our aspirations"), so the name matches what visitors read.
- A pillar or principle's dialog lists the gaps whose `primaryAppliesTo` is that element (`visionHierarchy.ts:27`). Supporting entries in `appliesTo` are never shown. Nothing reads a link from a gap to a characteristic.
- `npm run vision:check` runs `publicVisionContent.test.ts`; with `PUBLIC_VISION_FEED_FILE` set it asserts the candidate feed parses, with four pillars and four principles.

**Who else names the old words:** `templates/gap.md:3`; `docs/contribution-workflow.md:36` ("Every gap has **one primary pillar or principle**"); `skills/astrid-dev-gap/SKILL.md:12`; `vision/templates/subject.md`; the eight element pages. No file on `main` links to an anchor inside an element page.

**The gap ID letters** (`AA`, `LS`, `CI`, `CA`, `F`) are defined only by a pattern; no file says what they stand for. This plan does not change them.

### The proposed mapping

A helper read each gap's Desired state and Gap sections against the 28 section headings. This is a proposal for the owner (D8), not a finding of fact. The primary column is accepted (D8). The last column takes each supporting pillar or principle a gap names today and proposes the aspiration inside it that fits; those are proposals for her mark-up inside VA-5.

| Gap | Primary element today | Primary aspiration | Confidence | Supporting today → proposed supporting aspiration |
|---|---|---|---|---|
| AA-001 Sustained creative work | Artistic Ambition | Finished artistic work | medium: "Continuity and iteration" is close | Creator's control → Approachable, reversible choices |
| CA-001 Creative challenge culture | Shared Endeavor | Shared challenges and ambition | high | none |
| CA-002 Contributor ownership | Shared Endeavor | A meaningful stake in the collective | high | none |
| CA-003 Vision, experiments, progress | Open by design | Open decisions and working knowledge | high | Shared Endeavor → none fits, drop |
| CA-004 Sharing and discovery | Shared Endeavor | "Built for reuse" under Open by design, widened to "Built to be found and reused" | reworded, and the gap changes element (D7) | Compounding → An ecosystem of wisdom grounded in real work |
| CA-005 Parallel contribution | Shared Endeavor | new "Many hands, one clear way in" under Shared Endeavor | new aspiration (D7) | Open by design → Open decisions and working knowledge |
| CI-001 Agent learning loop | Compounding | An ecosystem of wisdom grounded in real work | high | Creator's control → Explicit permissions and privacy |
| CI-002 Federated knowledge | Compounding | Share without surrendering control | high | Open by design → Built to be found and reused; Creator's control → Explicit permissions and privacy |
| CI-003 Public source ingestion | Compounding | Use knowledge with judgment | medium: ingestion itself is not covered | Open by design → Open decisions and working knowledge |
| F-001 Platform reliability | Technical wrangling | Dependable execution and recovery | high | Creator's control → Approachable, reversible choices |
| F-002 Safe user control | Creator's control | Explicit permissions and privacy | high | none |
| F-003 Creative execution | Technical wrangling | Dependable execution and recovery | high | Artistic Ambition → Finished artistic work |
| F-004 Pack lifecycle | Liquid Software | new Packs (D6) | new aspiration | Open by design → Built to be found and reused |
| F-005 Local files, cloud assist | Local-first | Optional cloud capabilities, reworded "Everything local or cloud, by choice" | high | Technical wrangling → Important decisions stay visible; Creator's control → Explicit permissions and privacy |
| F-006 Fully hosted workspace | Local-first | Optional cloud capabilities, reworded "Everything local or cloud, by choice" | low as it stands; high once reworded (D16) | Technical wrangling → Agents handle the setup; Creator's control → Control at every layer |
| F-007 First-class sandbox | Creator's control | Explicit permissions and privacy | high | Technical wrangling → Important decisions stay visible |
| F-008 Portable generation | Technical wrangling | new Generation (D6) | new aspiration | Local-first → Everything local or cloud, by choice; Open by design → Built to be found and reused; Liquid Software → A small, dependable foundation |
| LS-001 Portable components | Liquid Software | Live tool composition | high | Creator's control → Control at every layer |
| LS-002 Agent workspace control | Liquid Software | Live tool composition | high | Creator's control → Explicit permissions and privacy |
| LS-003 Full-stack contributions | Liquid Software | Shared human–agent work | medium: Packs may fit better once written | Open by design → Built to be found and reused |
| LS-004 Cross-modal foundations | Liquid Software | A small, dependable foundation | medium | Artistic Ambition → Artistic agency; Open by design → Built to be found and reused |
| LS-005 Agent-managed tools | Liquid Software | Real-time functionality | high | Creator's control → Explicit permissions and privacy |

**What the table shows.** As the pages stand, thirteen fit with high confidence, four with medium, one with low, and four fit nothing. In all 18 that fit, the aspiration sits under the element the gap already names as primary. With the recommendations in D6, D7 and D16, every gap has a home: three aspirations are new (Packs, Generation, "Many hands, one clear way in") and two are reworded, so 28 become 31. The fullest page, Liquid Software, reaches six, the most a page allows; Shared Endeavor and technical wrangling reach four. Only CA-004 changes element, from Shared Endeavor to Open by design, so it alone moves on the vision page. Fourteen of the 28 existing aspirations have no gap at all: either Astrid is already there, or nobody has measured. That is recorded here as a finding; this plan writes no gaps for them.

### Supporting aspirations

The owner decided each gap has "one main one" and "as many as need be supporting" (D3). So nothing a gap says today is lost by default: each supporting pillar or principle becomes a supporting aspiration inside that element.

- **The proposals** are the last column of the table above. They were made from each aspiration's title and each gap's summary, not from a close reading of every gap, so they are a starting point. VA-5 puts them in front of her as one table.
- **One is proposed for dropping:** CA-003's supporting link to A Shared Creative Endeavor, where no aspiration is about a public trail of decisions. A dropped supporting element is a boundary change and gets a record.
- **On the page:** nothing changes. The App lists a gap only under its primary element and never shows supporting entries.
- **In the feed:** `appliesTo` is the primary aspiration's element, then the supporting aspirations' elements, without repeats. With the proposals as written it is unchanged for 20 gaps; it changes for CA-003 (one dropped) and CA-004 (primary moved).
- **In the boundary check:** the one-time move needs no record where the primary element and the set of supporting elements are the same as before. Anything else needs one.

### The vision page in Phase 2

Decided by the owner as an outcome (D17); the look is a taste task she sees before it ships (VA-10).

- **Inside an element's full-screen view,** each aspiration is a row showing its title and first sentence.
- **An aspiration, opened,** shows its paragraph, its two lists, then its gaps, one line each: ID, title, assessment, and "N projects tackling this".
- **A gap, opened,** shows its description (desired state, current state, what is missing, closure evidence) and its projects.
- **A gap sits under its primary aspiration.** *Recommended by the planner:* a supporting link shows as one quiet line inside the opened gap, "Also relates to", naming the other aspirations; it does not list the gap a second time. An aspiration with no gap shows one quiet line, "No gap is measured against this yet".
- **The element-level list "Gaps preventing this" is replaced** by this.
- **The main page's flat gap list and its projects section stay as they are** in this plan, as the view across all elements. *Recommended by the planner.*
- **Data.** The feed already carries gaps and projects with `gapIds` and `primaryGapId`. The only new data is each gap's aspiration references (VA-8).

### The drafts

Starting text for VA-3 and VA-4, for the owner to mark up. Each draft still needs a short paragraph, which those tasks write from her words for her to mark up; the parser requires one. The "We should" bullets are her words rearranged. The "We should never" bullets marked *(inverted)* are the planner's inversions of what she said, and the ones marked *(suggested)* are the planner's own; neither kind is hers until she says so.

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

**Everything local or cloud, by choice** (under Local-first, cloud-capable; today's "Optional cloud capabilities", reworded)

Everything should be able to run locally, and nothing should have to.

The sentence is hers, and the title is drafted from her words, "everything can be local or cloud by choice"; it is 36 characters, inside the parser's limit of 3 to 65. The bullets are the orchestrator's proposal to her, not yet read by her.

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

No lists are drafted. VA-4 writes the paragraph, and lists only if the owner asks for them.

**Built to be found and reused** (under Completely open by design; today's "Built for reuse", widened)

VA-4 widens the title, sentence and paragraph so that finding a contribution is part of it. No lists are drafted.

### Alternatives, including doing less

| Option | What it gives | Why not, or why |
|---|---|---|
| A new level between elements and gaps ("areas") | A page per part of the product | The owner rejected it: the level below elements already exists. |
| A third kind of element ("foundations") | Packs and Generation as peers of pillars | The owner rejected it: it reads as the same level as a pillar. It would also change the App's "exactly four pillars" contract. |
| A file per aspiration | A stable path for each | About 31 files in place of 8, a new record kind and a new parser, for a reference people read a page at a time. |
| Only add Packs and Generation as two more characteristics; leave gaps alone | The two references she asked for, in a day | Gaps would still point at up to four elements, and F-008 would still hold the generation philosophy. It does not answer "gaps should always be associated with aspirations". |
| Rename the feed's key, now or later | One word everywhere | No reader sees the key, and App builds already installed reject a feed without `characteristics`. The key stays for good. |
| Add structured list fields and a per-aspiration gap list to the feed and the overview in Phase 1 | Data for a later App change | Nothing reads them yet. Cut after the critique; a field is added with the code that reads it. |
| This plan | Three levels, one link up from each, on the page from day one in plain form | Chosen. Costs a parser change, 22 one-line edits and a later App change. |

### Ten vivid statements

Offered to the owner before she reads the tasks. Each is true of the plan as written.

1. Now, a gap points at pillars and principles. After, it points at one main aspiration and whichever others support it, and never at a pillar or principle.
2. Every supporting pillar or principle a gap names today is turned into a named aspiration or dropped on the record; none disappears quietly.
3. The word "characteristic" disappears from everything a person reads, and stays in the feed and the code, where nobody reads it.
4. Pillars and principles stay in two folders. No file moves or is renamed.
5. F-008 stops being where the generation philosophy lives. The philosophy moves up; the gap keeps only the distance.
6. The "We should never" lists are on the live vision page the day they merge, as plain unmarked lines; they look like lists only after the next App release.
7. An aspiration with a "We should" list and no "We should never" list is refused by a check, and no list may have a sixth bullet.
8. Twenty-eight aspirations become thirty-one. Only Packs, Generation and "Everything local or cloud, by choice" get lists in this plan.
9. Renaming an aspiration breaks every gap that names it until they are fixed in the same pull request.
10. Plans still link gaps, never aspirations. Each level links one level up.

### Critique

One round, 12 Nov 2026, by a fresh session with no stake in the draft, on commit `2a22b12`, read against astrid-dev and the App. The orchestrator ruled on each finding under the owner's delegation; D3 goes to the owner.

**Blockers.**

| Finding | What was done |
|---|---|
| B1. The mapping gave no supporting aspirations, though the gap line allowed two; F-008 has three supporting elements; the task that moves the gaps could not be executed, and the boundary rule compared only the primary. | Accepted. The owner then decided D3: one primary and any number of supporting. The mapping now proposes a supporting aspiration for each supporting element, for her mark-up ([how](#supporting-aspirations)). |
| B2. The gap-line task missed `checks.py:_boundary_impl`, the parser's return contract for its three callers, and a record-field pattern that cannot hold `/`. | Accepted. All three are in VA-2's scope and details. |
| B3. The drafts for Packs, Generation and "Local or cloud" had no paragraph, but the 15-word minimum counts prose only. | Accepted; the rule stays. VA-3 and VA-4 write a short paragraph for each new or reworded aspiration from the owner's words, for her mark-up. |

**Should fix.**

| Finding | What was done |
|---|---|
| S1. The one-time exemption in the boundary check was too loose and had no negative test. | Accepted as written: the move needs no record only if the primary element and the set of supporting elements are the same after projecting each aspiration to its element; a moved primary or a dropped supporting element without a record fails, by test. |
| S2. `should` and `shouldNever` in the feed have no reader. | Accepted. Phase 1 adds no feed field. |
| S3. Never rename the feed key: no reader sees it, and App builds already installed reject a feed without `characteristics`. | Accepted. The two rename tasks are cut; the key stays for good. |
| S4. Cut the generated gap lists in the overview: an emptied References section fails the parser, and four pages mention gaps in prose. | Accepted. The task is cut; only the one line about CA-004 changes, if that gap moves. |
| S5. Cut the review stop. | Accepted. Its questions are in R, one round. |
| S6. Four overlays embed gaps on the old line; the pack's claims about `golden.txt` were wrong. | Accepted. The overlays are named in VA-5; negative cases are unit tests; `golden.txt` does not change, and each task proves that. |
| S7. Cut the template file's rename. | Accepted. `vision/templates/subject.md` and the Python names keep "subject"; what people read says "element" and "aspiration". |
| S8. Sizes were stated in three places with two totals, and the run shape twice. | Accepted. Sizes have one home in `tasks.md`; the run shape is on the Run start line. |
| Merge the wording task into the rule task, the Desired-state task into the gap task, and drop an anchor search that could not fail. | Accepted. Lifting the anchor helper out of `_link_anchors` is part of VA-2. |

**Wrong claims, corrected.** A list in an aspiration does not show as a bulleted list on today's page: the base styling removes markers and indents, so it shows as plain lines until VA-9. The page does say "characteristic", once, in a screen-reader label. No `golden.txt` line mentions the old words. The anchor helper is a nested closure, not a reusable function.

**Weak proof, corrected.** "Renamed without its gaps" duplicated "names a non-existent aspiration" and is now one case. The exemption has its negative case. The proof no longer excuses unreadable lists in advance: it states the expected plain look and what would count as a failure.

**Phase 2 after the critique:** one App task and the one feed field it reads, added in the same phase. The owner then asked for more from the page (D17), so Phase 2 grew to the hierarchy, with its layout as a separate taste task.

## Owner decisions

Still for the owner: her confirmation of D7 with its wording, the wording of the five new or reworded aspirations, and the proposed supporting aspirations. The rest are decided: by her where it says so, otherwise by the planner, with reasons; she may overrule any of them. Her words are quoted in [What the owner said](#what-the-owner-said).

- **D1. What is the third level called?** *Decided by the owner, 12 Nov 2026: "aspirations".* The top two are the vision and its elements (pillars and principles).
- **D2. What is an aspiration made of?** *Decided by the owner, 12 Nov 2026:* a title, one sentence, a short paragraph, and "We should" and "We should never". *Decided by the planner:* the lists are optional but come as a pair; each has one to five bullets; each bullet is one sentence. Reason: her instruction that it must not become overburdened.
- **D3. What does a gap attach to?** *Decided by the owner, 12 Nov 2026:* always aspirations, never a pillar or principle directly; "one main one" and "as many as need be supporting". So: exactly one primary aspiration, any number of supporting, no cap. Each supporting element a gap names today gets a proposed aspiration for her mark-up, or is dropped on the record where none fits ([proposals](#supporting-aspirations)).
- **D4. Where do aspirations live?** *Decided by the planner:* inside the element's page, as today's `###` sections, with `## Characteristics` renamed `## Aspirations`; the two folders stay as the kind. Reason: a file each would be about 31 files and a new record kind.
- **D5. Is the feed's key renamed?** *Decided by the planner, after the critique:* never. It stays `characteristics`, with `appliesTo` and `schemaVersion` 1. Reason: no reader sees it, and installed App builds reject a feed without it.
- **D6. Where do Packs and Generation sit, and does Packs absorb anything?** *Decided by the owner, 12 Nov 2026, as recommended* ("I agree with where you say for positioning"): Packs is a sixth aspiration under Agent-Powered Liquid Software, the most a page allows, and absorbs nothing; Generation is a fourth under Eliminate technical wrangling.
- **D7. What do CA-004 (sharing and discovery) and CA-005 (parallel contribution) attach to?** CA-005 gets a new aspiration under A Shared Creative Endeavor, working title "Many hands, one clear way in"; CA-004 gets none: "Built for reuse" under Open by design is widened to "Built to be found and reused", so CA-004 changes element, moves on the vision page and needs a boundary record. *Agreed with the positioning, 12 Nov 2026* (the orchestrator reads "I agree with where you say for positioning" as covering it); *the owner to confirm with the wording* in VA-4.
- **D8. Is the [proposed mapping](#the-proposed-mapping) right?** *Decided by the owner, 12 Nov 2026, as recommended* ("I agree with what you mean for the gap placement"): the primary column stands, including the four medium rows. The supporting column is still hers to mark up (D3).
- **D9. Which gaps have their Desired state trimmed?** *Decided by the owner, 12 Nov 2026, as recommended* ("and the desired state"): only F-008 and F-004, whose philosophy moves into Generation and Packs. Each keeps a Desired state, which the feed requires.
- **D10. How does the one-time move of 22 gaps pass the boundary check?** *Decided by the planner, after the critique:* no record where the primary element and the set of supporting elements are the same after projecting each aspiration to its element; a record where the primary element moves, a supporting element is dropped or added, or the Desired state is trimmed; after the move, any change to a gap's aspirations needs one. Reason: her decisions D3 and D8 are the review for a like-for-like move, and 22 seven-field records would repeat them.
- **D11. Does the generated overview list gaps under their aspiration?** *Decided by the planner, after the critique:* no. Reason: the App shows it in Phase 2, and the hand-kept lists cannot be emptied without failing the parser.
- **D12. Where is the one rule about using aspirations?** The rule: a planner reads the aspirations of the plan's gaps; work that would break a "We should never" changes the aspiration first, in a pull request the owner approves; wording under `vision/` is the owner's. *Decided by the planner:* in the contribution workflow's section on vision gaps, with one link each from the plan skill and the gap skill. Reason: it binds reviewers and gap assessors as well as planners. Plans keep linking gaps only.
- **D13. What do the files and the code call an element?** *Decided by the planner, after the critique:* what people read says "element" and "aspiration"; the template file and the Python names keep "subject". Reason: renaming them helps no reader.
- **D14. Is Phase 2 committed?** *Decided by the planner:* yes, as one feed field and one App task, in the first release after Release 13. Reason: until then the lists show as plain lines.
- **D15. How many review rounds?** *Decided by the planner, after the critique:* one final round, no review stop.
- **D16. How does the vision say "local or cloud"?** *Decided by the owner, 12 Nov 2026, in her words:* "everything should be ABLE to run locally but shouldn't have to", titled "everything can be local or cloud by choice". The existing aspiration "Optional cloud capabilities" under Local-first, cloud-capable is reworded to carry it, with the draft title "Everything local or cloud, by choice", her sentence, and the lists in [The drafts](#the-drafts); F-005 and F-006 then fit it. The wording is hers to mark up in VA-4.
- **D17. What does the vision page show in Phase 2?** *Decided by the owner, 12 Nov 2026:* the hierarchy in [The vision page in Phase 2](#the-vision-page-in-phase-2): aspiration, then its gaps by title, then each gap's description and projects, opened level by level. *Decided by the planner, for her to overrule when she sees it:* how a supporting link and an empty aspiration show, and that the main page's flat lists stay.

## Source identities

- **astrid-dev:** `banodoco/astrid-dev`, `main` at `0ed58f99d1543ac87c1c5759549aba7edcd13320` when this pack was written. The run records its own base at dispatch and re-checks every path and line here.
- **The App:** `banodoco/astrid-app`, `main` at `237b28be935af49c23464fa6ca1cf30db67ebaa0`, read only. Phase 2's base is the release line the release's manager names, not `main`.
- **Destination:** Phase 1 lands on an integration branch and reaches astrid-dev `main` by pull request. Phase 2's App change goes to a release's branches; this plan opens no pull request to the App's `main`.

## References

- The [orchestrator's session](https://claude.ai/code/session_011EzfW38XJUpUFewfUM9MxF), where the owner described the outcome, the three helpers reported and the critique was ruled on.
- The public page: [astrid.haus/vision](https://astrid.haus/vision). The published feed: branch `vision-published`, file `vision.json`.
- [Plan 44](../44-vision-execution-trail/plan.md), which serves CA-003 from the evidence side.
