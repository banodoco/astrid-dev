# Sense-check: splitting Plan 66

> Historical research, not instructions. Where this differs from the current plan, inputs or tasks files, those win.

Read-only, 18 Nov 2026. Nothing run. Plans read in the worktree at `a1cd5f04` (the coordinator cites `e1054ea9` on main; I did not compare the two). I read Plan 66's task table, card details and the Functional additions section, and the cross-references in Plans 64, 65 and 67.

## Verdict

**The cut is right, with one piece on the wrong side of it and two conditions.**

- **Right:** 66 becomes a pure change of machinery with a clean live boundary (the same shots render the same through the new compiler). 68 and 70 each add something a creator can see. That is a better shape than one 15-day plan.
- **Wrong side:** composition by occurrence and the exact-delivery verifier sit inside CC-8, so they would go to 68. They are core contract, and 70 cannot work without them.
- **Condition 1:** the order is 66 → 68 → 70, not 68 and 70 in parallel.
- **Condition 2:** 66 must ship recipes and the rewritten general skill for what already exists, because it deletes v1 and the current skill teaches v1.

I would not merge 68 into 66. Keeping 66 free of new capability is what makes its live test a clean regression check.

## 1. Hidden dependencies

| Dependency | What it means for the split |
| --- | --- |
| **CC-8 contains three things.** A full-canvas source builder and chunk holds (the feature); composition "from each placed item at its own span and offset, keyed by occurrence"; and the exact-delivery checks from Functional additions, which note that today's verifier tolerates about 2% sample-count difference and "can't establish" exactness. | The second and third are core. Bridges and inserts place two clips at different offsets and need them. The design's invariant "only composition promises exactness" is unproven until they exist. Move both into 66 as their own card. 68 keeps the builder and the holds. |
| **CC-7a's first step** compares against CC-8's full-canvas source. | 70 follows 68. |
| **Guides inside a continuation.** The clocks addition (CC-9, CC-7, CC-8) says a guide at a delivered frame must be mapped into the sampled segment, or refused. | The plan that lands second owns it. With 68 before 70, that is 70. Say so in 70. |
| **Template machinery needs recipes** to be tested. | 66 ships recipes for what exists after Plans 64 and 65: start image with speaker clip, mouth redub, regional edit, Character Swap, plain generation. `test_skill_examples_admitted.py` is rewritten in 66. |
| **The skill.** CC-1.4 removes v1; the current skill teaches v1 first. | The base rewrite of the general skill and the thin Recast skill must be in 66. Later plans add one section each. |
| **Continuation during 66 and 68** still runs on the captured bundle, chosen by arrangement. | Fine. State it in 66 so nobody removes the bundle early. |
| **Functional additions spans cards.** | Split it by owner (list below). |
| **R depends on everything.** | See section 2. |
| **Plan 67's `speech-continue` recipe** needs continuation. | It waits for 70; the rest of 67 does not. |

## 2. Interfaces

| Plan | Consumes | Produces |
| --- | --- | --- |
| **66 One compiler** | Plan 64's record, table and audio mask; Plan 65's canvas and mask rasters; Plan 59's shot plan and Recast skill | the resolved job; `compile_job`; the capability table keyed by kind, with status and node-pack column; the dry-run view; end-relative time; composition by occurrence and the exact-delivery verifier; the template commands and recipe format; recipes for existing capabilities; the general skill and thin Recast; the one-page design |
| **68 Guides and exact stills** | 66's job, table, view, composition, recipe format | `role: guide` and its lowering function; placed stills at any frame with chunk holds; the full-canvas source builder; their recipes and skill lines |
| **70 Continuation, bridges, inserts** | 66 as above; 68's full-canvas builder and guide lowering | prefix, bridge and insert preparation in one function; removal of the captured workflows and the `continuation` flag; the delivered-to-sampled frame map; their recipes and skill lines |
| **67 Community steering** | 66's table, view and recipe format; 68's guide lowering; 70 for one recipe | as now |

**What 66 must reserve beyond what is already reserved:**

1. **`unavailable` rows for what 68 and 70 will add:** `role: guide`; a placed still off frame 0; two placed clips with a gap; a placed clip at a later offset. Each plan then flips a row and adds a lowering. Without this, 68 and 70 change the schema and admission, which is the reshaping the split is meant to avoid.
2. **The one function that looks at how placed items are arranged** lives in 66. In 66 it knows two arrangements (source covers the canvas; prefix, through the captured bundle) and refuses the rest from the table.
3. **A slot in the dry-run view for the delivered-to-sampled frame map.** In 66 it is the identity plus the tail trim. 70 fills it for continuations.
4. **The guide seam.** One sentence in 66's contract: guides enter through one function that takes ordered guides and returns conditioning. 68 implements it; 67 wraps it.

**Reviews.** Keep RS1 where it is. Give 66 its own closing review, because everything after cites its contract; a review only after 70 is too late to catch a contract fault cheaply. 68 and 70 need no round of their own beyond their proofs. Keep the one integrated review after 70.

## 3. Recipes and skill text per plan

The risk is real: four plans each adding lines to one page will drift in vocabulary and length. Three mechanical guards remove most of it:

1. **Skills contain no request text.** Every example is a recipe file named in the skill and loaded by `test_skill_examples_admitted.py`. A test fails if the skill names a recipe that does not exist.
2. **The kinds list in the skill is checked against `describe`.** A test fails if a kind with a status other than `unavailable` is missing from the page, or if the page names a field the schema does not have.
3. **A length cap and a standing cold read.** The page has a line limit. Each plan re-runs the same small-model asks plus one for its new capability.

Then each plan adds at most one short section and one row to the kinds table, and the final trim pass after 70 edits wording only.

**Where the contract lives.** "Changes go only in Plan 66" will not hold once 66 is closed, because closed plans are history. Ship the one-page design as a file in the pack (for example `astrid/packs/h3_av/docs/design.md`) in 66. Plans 67, 68 and 70 cite that file and amend it in the same change as the code.

## 4. Alternatives considered

- **Merge 68 into 66.** Rejected. It would give 66 new capability and blur its regression boundary. 68 is small, and that is acceptable.
- **Run 68 and 70 in parallel.** Possible only if CC-7a's full-canvas check is deferred, which defeats its purpose: that check decides whether CC-7b and CC-7c exist at all.
- **Move the full-canvas builder into 66 as well.** Not needed. It is only used by stills and by CC-7a's check.

## 5. References and sequencing

**Keep the card ids.** CC-4 and CC-8 keep their names in 68; CC-7a to CC-7d keep theirs in 70. Thirteen research files and three other plans cite them, and renumbering would break every one.

**Order:** 59 → 64 → 65 → 66 → 68 → 70, with 67 overlapping:

- 67's timed prompts, signals, ControlNet and LoRA phase (CS-2, CS-5, CS-6, CS-7) can start after 66.
- Guide phase and the curve tool (CS-3, CS-4) wait for 68.
- 67's recipes (CS-8) come last; `speech-continue` waits for 70.

**Live sessions**, if the owner agrees to D6: after 64, after 66 (regression renders of the shipped recipes), after 68 and after 70.

## What to edit

1. **Plan 66:** retitle; keep CC-1.1 to CC-1.4, RS1, CC-2, CC-3, CC-9; add a card for composition by occurrence and exact-delivery verification (taken from CC-8's composition bullet and "Functional additions exact"); keep the template commands from CC-5 with recipes for existing capabilities; keep the base skill rewrite from CC-6; add the four reservations in section 2; add the three skill guards in section 3; ship the design page into the pack; keep a closing review. Estimate about 8 days.
2. **Plan 68 (new):** CC-4, and CC-8 without its composition bullet; their recipes and one skill section. Depends on 66. About 2 days.
3. **Plan 70 (new):** CC-7a to CC-7d, the CC-7 lattice summary, "Functional additions assembly", and the guide-in-continuation part of "clocks"; their recipes and one skill section; the final trim pass and the integrated review. Depends on 66 and 68. About 6 days.
4. **Functional additions, by owner:** masks, two masks, occurrences, bindings, refusals, resources, templates and exact → 66; clocks → 66 for end-relative time, 70 for segment mapping; assembly → 70.
5. **Plan 64:** in the non-goals and SR-4, change "Plan 66 CC-4" and "Plan 66 CC-8" to Plan 68. References to the record, the table and CC-1.1 stay on 66.
6. **Plan 65:** change "Continuation gets size from Plan 66 CC-7a" and the D1 text to Plan 70.
7. **Plan 67:** "Waiting on" becomes Plans 64, 65, 66 and 68, with 70 for the `speech-continue` recipe; "guide lowering" is cited from 68; the design is cited from the pack file.
8. **`priority.md`:** list them in the order 64, 65, 66, 68, 70, 67, since the numbers no longer show the order.

## Not checked

- Whether main at `e1054ea9` differs from the worktree I read.
- The day estimates; they are rough reallocations of the plan's own 15.5 days.
