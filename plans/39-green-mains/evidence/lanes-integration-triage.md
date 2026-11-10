# Lanes integration: first run, 659 failures, triaged for R12

[Plan 39](../inputs.md) · [Tasks](../tasks.md)

## Purpose

The first run of the Agent Lanes integration jobs failed 659 times. This record triages those failures for Release 12. Each row gives the class and first cause, and whether served release 11 (`a105de3a`) shows the same result.

**Ruling:** Install/update breakers in R12: **NONE**. Each item was reproduced on both R12 (`313bbd46f`) and R11 (`a105de3a`), with the same result on both. Hannah's rule: "if none break install or update, add to Plan 39".

## Triage

| Item | Class | First cause | R11 |
|---|---|---|---|
| Lifecycle migration/restart | fixture | journal omits the activation-lock binding added at `installer/core.py:435` | same |
| Pinokio stopped-update (14) | fixture composition | historical Agent lacks `astrid.sdk.timeline.commit`; paired with current Runtime | same |
| Pinokio activation (4) | stale double | mock rejects the existing `persist_choices=False` API (predates R11) | same TypeError |
| Pinokio integration, pending launch (2) | fixture | starts an unfinished update without authenticated custody; correctly refused (`installer/service.py:323`) | same |
| Pinokio integration, current Runtime (6) | fixture composition | historical Agent with current Runtime | same |
| Pinokio integration, retained Runtime (6) | stale expectation | Update-while-running is correctly refused (`custody.py:196`); the stop-first contract predates R11 (`07e906121`) | same |
| Retained-owner cleanup (secondary) | pre-existing compatibility refusal | legacy birth identity lacks boot/PID-namespace scope (Runtime `platform.py:637`) | same; the validator is byte-identical |
| Update recovery (3) + transaction authority (2) | stale exit expectation | deliberate recovery-only exit 3 (`installer/outcome.py:22`; rulings `7b1ce9367`, `53f3640f3`) | R12 post-state assertions pass when exit 3 is required |
| Upgrade fixtures (`busy_fixture` x10, `upgrade_release` x4) | environment | missing historical Runtime tree / `ASTRID_RUNTIME_REPO` unset | n/a |
| `c1_product_gaps` (1), `journey_plumbing` (1), `cross_client` (1) | stale test/env | see the part-1 triage | n/a |

## Plan 39 follow-ups

- Fix the fixtures to pair matching Agent and Runtime versions.
- Update the doubles and expectations to the documented contracts.
- Give the Lanes job the historical Runtime tree.
