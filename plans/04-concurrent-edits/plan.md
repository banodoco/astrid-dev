# 04 — Refined concurrent editing

> **Draft reconciliation:** The dated Release 16 proposal below supersedes conflicting historical scope or dependency wording for review only. Existing statuses, decisions and delivery authority remain the historical record until the owner accepts a change.

**Project:** Refined concurrent editing

**Goal:** Keep users in control: agent edits must respect user edits, surface conflicts, and retry safely without silently overwriting changes.

**Status:** queued

**Owner:** Unassigned

**Estimate:** TBD

**Waiting on:** —

**Vision gaps:** [Trustworthy user control](../../vision/gaps/F-002-safe-user-control.md) (primary).

**Contributing:** [Astrid development skill](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/start.md).

Complete the retained concurrent-editing behavior so agent edits respect user edits, surface conflicts, and retry safely without silently overwriting changes. The project remains queued; this plan does not authorize execution.

## Goal and scope

- **Included:** validate the retained Agent, App, and Runtime work as one exact tuple; repair only demonstrated in-scope failures; then compose and promote reviewed candidates after generation integration.
- **Deferred:** full SDK/UI suites and unrelated baseline failures.
- **Build on:** retained concurrent-editing work and the promoted generation tuple. Exact historical SHAs, evidence limits, and branch rules are in [inputs.md](inputs.md).

## Sequence

Run [CE-FINAL](tasks.md#ce-final) and, only for a demonstrated failure, [CE-REPAIR](tasks.md#ce-repair-only-if-required); then complete the existing [CE-END](tasks.md#ce-end) review. After generation integration is promoted, [compose](tasks.md#ce-compose) once on frozen current bases, [review](tasks.md#ce-review), and [promote](tasks.md#ce-promote) the same immutable heads. Dependencies and exact proof are in [tasks.md](tasks.md).

## Completion boundary

Completion means the exact retained tuple passes the scoped checks, required outcomes have no blocking END-review findings, and the reviewed composed candidates are promoted under the existing authority. Proof must cover seven SDK nodes, the unchanged eight-case hosted wrapper, real hosted outcomes, SDK guarantees, and the cooperative limit. This does not claim full-suite coverage or establish future candidate results from historical evidence. The [shared run contract](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/shared/run-contract.md) and the actual product repositories' release policies govern execution and publication; this plan grants neither.

## Read next

- [tasks.md](tasks.md): task index, routes, dependencies, selectors, and acceptance.
- [inputs.md](inputs.md): retained source identities, evidence provenance, and branch policy.
- [Project queue](../../README.md): current status, owner, and estimate.

## Proposed Release 16 reconciliation — 25 November 2026

Draft pending independent review and owner scope agreement; preserve existing task progress and accepted decisions. Source: [SYN-01 original](https://github.com/banodoco/astrid-dev/blob/4259785be40565ba940ecb076ca8c9889742d7cf/releases/16/evidence/scoping/SYN-01.md).

retain original two-writer/no-overwrite/no-blocking acceptance and cooperative limit. P63 implements demonstrated residuals; no second queue, merger or separate publisher. Richer collaboration remains later.
