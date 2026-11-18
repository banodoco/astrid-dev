# H3 dynamic output size

**Project:** H3 dynamic output size

**Goal:** A creator chooses the H3 working size per request (small for voice-only takes, other aspect ratios, larger where it's worth paying for), and masks, previews, composition and checks follow it.

**Status:** `queued`

**Owner:** Unassigned

**Estimate:** 3 days for the builder routes, including the shared size contract and moving-mask handoff.

**Waiting on:** Owner greenlight and D3 (small-size continuation now or later).

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-003 — Creative execution isn't yet dependable end to end](../../vision/gaps/F-003-creative-execution.md) (primary).

## Outcome and scope

A creator can ask for `output.size: [512, 288]` on an H3 v2 image-guided generation, masked edit or Character Swap. The public request defaults to 1024×576. Source conform, generation, mask rasterization, composition, dry run and completed-job evidence use the same effective dimensions. Character Swap retains its existing input contract. Both captured continuation workflows retain default size only.

Static image masks and rectangles describe an authored working canvas. Creators can reuse them at a new size and preview the result before claiming compute. Moving masks retain their lossless, prepared-source-size and clock requirements. Automatic size selection, quality guidance across the entire node range, tuning `ref_image_size` and scaling moving masks are deferred. Continuation moves onto the builder under [#866](https://github.com/banodoco/astrid-dev/issues/866), including small-size continuation for [#885](https://github.com/banodoco/astrid-dev/issues/885). The remaining deferred input and identity changes are listed in [Plan 64’s scope](../64-h3-speaker-references/plan.md#outcome-and-scope).

## Existing work and decision

Reuse the v2 normalizer, source conform, generation builder, static-region resolver and managed artifact handoff. Composition already uses the prepared source dimensions but independently finds or redraws masks. The proposed change gives compilation ownership of the resolved permissions used in both generation and paste-back. The owner requested a plan. Scope, coordinate semantics and acceptance of the live proof remain pending. [Planning evidence](inputs.md#planning-evidence)

## Sequence and readiness

DS-1 establishes the size and frozen-source contracts. DS-2 carries size through conform while DS-4 defines and implements the mask handoff. DS-3 integrates the builder with that handoff. Once the CPU paths work together, the executable examples feed DS-5 and the live comparison can proceed in parallel in DS-6. Both feed the final review. Dispatch requires recorded decisions, exact revisions and authority for the three-job proof. [Task cards](tasks.md)

## Interfaces and handoff

The v2 request consumes the pinned H3 node's width and height rules. Compilation supplies one effective pixel pair and resolved mask artifacts indexed by edit and time interval. The dry-run plan and retained job result expose the effective dimensions. The standalone mask preview takes its own explicit `--size`.

Coordinate the shared normalizer, source-free path, masked and Character Swap calls, builder signature and skill examples with Plan 64. Prefer SR-2 first. SR-2 owns removal of the v1 translation and retains common bundle emission. Rebase DS-3 on that interface. If size lands first, DS-1 carries the size across the existing bridge and SR-2 keeps its public test. At the combined head compile one mixed-reference masked request at 768×448 and compare default image-only behavior to the prior bundle, bindings and digest. Record the integrated CPU result once and link it from both plans. Each project's GPU proof stands alone.

## Completion

On the image-guided source-free route, two otherwise identical spoken-line jobs render at 512×288 and 1024×576. Each transcript matches the intended words and the smaller job uses less GPU time under the same measurement protocol. Both captured continuation variants refuse non-default sizes before claim.

A 768×448 lens edit aligns to an asymmetric landmark. Decoded frames retain the prepared source pixels outside the authorized mask and interval. Dry-run and completed-job records agree with the decoded dimensions. Unsupported sizes fail before claim, and existing default request identities and compiled artifacts match the baseline. Evidence covers the tested routes, sizes and GPU type. Completion requires the final integrated review. Release and publication require separate authority.
