# 05 — Release fixes integration

**Vision role:** Foundational enabler — integrates previously accepted fixes without independently proving a new user-facing outcome.

**Contributing:** [Astrid development skill](../../../skills/astrid-dev/SKILL.md).

Account for the accepted remaining fixes and compose the eligible changes into a coherent release while preserving existing behavior. The [project queue](../../../README.md) remains authoritative for status, owner, and estimate.

## Goal and scope

- **Included:** compare accepted fixes with the promoted Plan 02 integration and Plan 04 result; integrate only missing eligible behavior; separately compose Runtime CAS/fold work; account for every ledger member exactly once as included, equivalent, or deferred.
- **Deferred:** parked H3/GPU work and any feature not selected by the evidence-based inventory. A ledger disposition alone is not product acceptance.
- **Owned elsewhere:** Plan 06 PK-6 consumes the Agent health fold once; this plan records that outstanding closure but does not merge it.

## What we build on

The work starts from the exact promoted Plan 02 integration and Plan 04 heads. The accepted SF receipts and donor commits are historical provenance, not a frozen destination base. The original audit found no later Plan 05 base; at execution, freeze then-current `pre-main` for each changed repository after predecessor promotion. See [inputs](inputs.md) for exact historical identities and limits.

## Sequence

1. [Inventory](tasks.md#sf-inventory) the ledger against actual Plan 02 integration and Plan 04 heads and map each item to a single disposition.
2. Complete only selected independent rows, including the post-CE Runtime CAS/fold composition where still absent; Plan 06 owns the Agent-fold execution.
3. [Compose and review](tasks.md#sf-compose) the producer-to-consumer tuple once, then [promote](tasks.md#sf-promote) only exact reviewed candidates. This plan does not wait for Packs merely to ship unrelated selected fixes.

## Completion

Plan 05 completes when selected changes are promoted and every accepted item has an evidenced disposition. The Agent fold is recorded as fold transferred to Plan 06 PK-6, which closes it; Plan 05 does not wait for Plan 06. This plan does not prove H3/GPU readiness or final initiative completion. Use the existing candidate and publication authority recorded in [inputs](inputs.md); do not assume branches or publish empty changes.

## Read next

- [tasks.md](tasks.md): task index, routes, dependencies, checks, and progress.
- [inputs.md](inputs.md): historical donors, accepted receipts, source limits, and target rules.
