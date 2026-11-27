# 04 — Refined concurrent editing

> **Proposed Release 16 reconciliation, 27 November 2026.** This is the current reviewable planning contract, replacing the obsolete donor-composition instructions. It does not start implementation, alter active assignments or grant publication authority. Historical scope and evidence remain linked in [inputs](inputs.md).

**Project:** Refined concurrent editing

**Goal:** Independent writers preserve each other's work: supported disjoint edits survive, genuine conflicts are explicit, and retry, recovery, restore and undo never silently overwrite another writer.

**Status:** queued

**Owner:** Unassigned

**Estimate:** 1–2 engineering days of incremental evidence mapping and independent qualification; no separate implementation budget (shared repairs are counted in P63)

**Waiting on:** Original hosted eight-case wrapper, CE-0 and CE-LIMIT evidence mapping; a reviewed P63 candidate and an authorized installed-product qualification venue. Historical passes and source presence do not qualify the Release 16 tuple.

**Vision gaps:** [Trustworthy user control](../../vision/gaps/F-002-safe-user-control.md) (primary).

**Contributing:** [Astrid contributor entrypoint](../../agent/start.md).

## Outcome and scope

[Plan 63](../63-dependable-saving/plan.md) is the single implementation lane for saving and concurrent-editing repairs. This project retains its own safety requirements and independently judged verdict. There is no second queue, merger, lease service, implementation branch or publisher.

The retained outcome covers an editor beside an SDK/CLI writer, two SDK processes using the same authenticated actor, and two browser tabs. Supported disjoint writes preserve both edits. A genuine overlap or stale delete/restore does not silently overwrite the first accepted change. An unknown reply retains the exact attempt; a sibling writer cannot replay or settle it. Ordinary undo targets the writer's own edit, preserves later disjoint work and explicitly refuses or parks an overlap. Keep the accepted cooperative limit and bounded retry behavior; recovering their original evidence is work, not permission to invent new semantics.

Richer presence, attribution, live-adoption polish and a new narrow-by-default policy remain with [P76](../76-editing-together/plan.md). Existing supported-route safety and basic undo remain Release 16 requirements.

## Delivery structure

1. **CE-FINAL** maps the retained seven SDK and eight hosted outcomes to current public routes, recovers the missing historical acceptance records, and prepares independent checks alongside P63 work.
2. **CE-REPAIR** routes only demonstrated failures to the existing P63 owner and task. **CE-REF** verifies the already implemented reference builder instead of rebuilding it.
3. **CE-COMPOSE** joins the shared Release 16 provider → Agent → App pin integration. Run affected acceptance against the exact resulting tuple.
4. **CE-END / CE-REVIEW** produce the named independent concurrent-editing verdict inside P63's R0 review. The verdict is an output of that review, not a prerequisite for starting it.
5. **CE-PROMOTE** is satisfied only by the existing Release Lead's one authorized publication; there is no project-specific promotion.

## Completion boundary

Completion requires an independently accepted exact-tuple result covering the retained SDK guarantees, the eight hosted outcomes, CE-0, CE-LIMIT and the relevant writer-custody/recovery negatives. A historical selector may be replaced only through a recorded equivalence decision that preserves its outcome. Missing evidence is not a pass.

The shared installed witness must check actual accepted revisions/publications and per-item contents, including simultaneous submissions, restart/reload, unknown versus definitive failure, late acknowledgements and wrong-owner recovery. P63's saving verdict and this project's concurrency verdict remain separate even when they use the same fixture and run.

No full-suite expansion or repeated qualification of unchanged boundaries is required merely because this project exists. A moved relevant pin requires affected checks and an explicit impact record. A CPU packet marked Done or Parked is not installed-product acceptance; a parked blocking requirement prevents release acceptance.

## Read next

- [Tasks](tasks.md): every retained task and its disposition.
- [Inputs](inputs.md): verified source credit, recovered SDK definitions, historical limits and unresolved evidence.
- [Release 16](../../releases/16.md): shared integration and qualification.
