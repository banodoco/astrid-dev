# Part 2b design note (record only)

[`part2b-design.md`](./part2b-design.md) is a design-only note for a narrow "Part 2b" of the object-info memo, written at the Release 15 Lead's request on 23 November 2026 from the failed Part 2 candidate (VibeComfy PR #182 at `675f5dc2658197318a95e0e1b7c5b232b17cd9d5`). It is a record so that whoever builds Part 2b starts from it. No code, measurement or review exists for the design.

What it proposes: an invocation-owned read set created in each emit call and passed explicitly (no borrowing between invocations, no revocation), one final full-content re-witness of the whole eligible read set before anything is published, and unsafe paths bypassing the memo so the base guards and refusal order are kept. It maps each class of the [Part 2 memo review](../part2-memo-review/README.md) to a closure test, and states the open risks: omitted propagation edges must bypass rather than guess, the recursion-depth boundary is unproven, and expected hash counts are arithmetic, not measured.

Status at record time: the Lead held the go; the owner was deciding whether Part 2b restarts as Plan 82 in a fresh session with a clean brief.
