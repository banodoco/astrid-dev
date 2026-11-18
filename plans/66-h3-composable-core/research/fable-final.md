# Final elegance check: Plans 64, 65 and 66

Read-only, 18 Nov 2026. Read the uncommitted worktree versions of all nine files. Nothing was run.

**Verdict: yes, the three plans now land on the end state.** The model, the three rules, the four layers and the template contract are stated once and consistently. The fields of the job record match across Plan 64 SR-3, Plan 65 and Plan 66 CC-1. D3, D4 and D5 are applied cleanly. What remains is one real gap (continuation between CC-1 and CC-7), three leftover contradictions, and a few small tightenings. None needs a restructure.

## 1. Still route-shaped, contradictory or over-built

1. **Continuation has no stated path between CC-1 and CC-7 (the one real gap).** CC-1 removes `branch_for` and "the route selector in the hook and CLI" in phase 1. The captured workflows and the `continuation` flag survive until CC-7, and CC-1's lowering table says only "Generated suffix after a placed prefix: CC-7". So for the whole of phase 1 it is undefined what compiles a continuation, and the phase 1 skill and "continue" recipe either carry a flag that the plan says does not exist, or change again in phase 2.
2. **Plan 64 says Plan 66 lifts the "still only at frame 0" limit; Plan 66 says it does not.** SR-4 detail: "refused from the limits table, as a lowering limit Plan 66 lifts." Plan 66 non-goals: "an exact end or interior still." Plan 66 gives a soft guide there, which is a different thing.
3. **Plan 64 points at the wrong task.** Its non-goals cite "Plan 66 CC-3" for `MiniMaxH3AddGuide`; guides are CC-4.
4. **Plan 65's scope still promises old digests.** "its bytes and digest are exactly what they are today" contradicts D4, since Plan 64 SR-1 breaks identity first. Its completion list already says the right thing.
5. **An agent-facing refusal names a plan.** Plan 65: "refused, pointing to Plan 66." CC-2 forbids internal names in refusals; a plan number is one. It should be a lowering-limit row like the others.
6. **Route wording that will be copied into code.** Plan 64 SR-3: "All three routes build the record from `canonical_spec`." `canonical_spec` is the single-source waist that CC-1 reduces to v1 translation. Building the new record on it means SR-1's "forward and reverse conversion" work in `spec.py` is written and then removed. The rest of Plan 64's "route" wording describes today's code and is harmless.
7. **Slightly over-built:** CC-3 asks for delivered ownership "per frame and per audio sample". Read literally that is a 48 kHz listing. Intervals are enough.

Not a problem, checked: `role: guide` instead of reusing `hard` (the stated reason holds); the two-block limits table; SR-4 lowering through the source-backed path; supplied audio as a placed item in the record; one continuation block per job; RS1 as a review stop.

## 2. Essential and missing

1. **A proof that features compose, not just that the four old shapes still work.** CC-1's completion list is the four former routes going through `compile_job`. That passes if `compile_job` is a switch over four folded compilers, which is route thinking under a new name. One request that no former route accepted would close this.
2. **Templates from outside the H3 pack.** The owner confirmed agents can write their own, and Recast ships its own brief and steps. CC-5 only loads `docs/recipes/` in the H3 pack by name. `--template` needs to take a file path, and `templates list` needs to include templates shipped by other installed skills.

Worth one line each, not essential: the follow-up issues (endless-continuation skill, continue-from-take, take lineage, exact interior still, Event Curve tool) are named as non-goals but not filed; Plan 64 SR-7 and Plan 65 DS-5 still write recipes as prose that CC-5 then converts.

## 3. Text edits, in priority order

1. **Plan 66 tasks, CC-1 detail, lowering table.** Replace the row "Generated suffix after a placed prefix | CC-7" with: "Generated suffix after a placed prefix | Selected by shape: one unchanged video prefix at frame 0 and uncovered time after it. In phase 1 this calls the captured bundle; CC-7 swaps in the ported stage. The `continuation` flag is accepted and ignored from CC-1, and removed from the schema in CC-7. No recipe or skill text uses it."
2. **Plan 66 tasks, CC-1 focused proof.** Append: "One combined request that no former route accepted (a placed clip with a region grant and an audio grant, three image references and a speaker clip) compiles, with each lowering present in the graph. `compile_job` chooses lowerings from the features present in the job, never from a classified shape."
3. **Plan 66 tasks, CC-5 scope.** After "`--template NAME`" add: "`NAME` may be a recipe name or a file path. `templates list` shows the H3 recipes and any template an installed skill ships in its own `recipes/` folder. An agent-written file is filled and checked the same way."
4. **Plan 64 tasks, SR-4 detail.** Replace "as a lowering limit [Plan 66] lifts" with "as a lowering limit. Plan 66 adds a soft guide at other frames (CC-4); an exact still off frame 0 stays refused."
5. **Plan 64 plan, non-goals.** Change "([Plan 66] CC-3)" to "([Plan 66] CC-4 adds guides)".
6. **Plan 65 plan, outcome.** Replace "the request is 1024×576 and its bytes and digest are exactly what they are today" with "the request is 1024×576, identical in bytes and digest to an explicit 1024×576 request".
7. **Plan 65 plan (completion) and tasks (DS-1).** Replace "refused, pointing to Plan 66" and "refused until Plan 66 CC-7" with "refused from the limits table as a lowering limit, which Plan 66 CC-7 removes".
8. **Plan 64 tasks, SR-3 rules.** Replace "All three routes build the record from `canonical_spec`" with "All three compilers build the record from the normalized v2 request, falling back to `canonical_spec` only for a v1 request". In SR-1 scope, change "`shared/spec.py` forward and reverse conversion" to "`shared/spec.py` only as far as v1 translation needs".
9. **Plan 66 tasks, CC-3 focused proof.** Change "delivered ownership per frame and per audio sample" to "delivered ownership as frame and sample intervals".
10. **Plan 64 SR-7 and Plan 65 DS-5 scope.** Add: "Write each new recipe as a complete request file that the admission test loads, so Plan 66 CC-5 adds holes instead of rewriting prose."

Edits 1 to 3 matter. Edits 4 to 7 remove contradictions an implementer would trip on. Edits 8 to 10 save rework and can be skipped without harm to the end state.
