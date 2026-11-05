# 04 — Refined concurrent editing

**Start here:** read [AGENTS.md](../../AGENTS.md), choose a workflow in the [skills guide](../../skills/README.md), follow the [run contract](../../skills/astrid-dev-shared/run-contract.md), and look up terms in the [glossary](../../docs/glossary.md).

Complete the retained concurrent-editing behavior so agent edits respect user edits, surface conflicts, and retry safely without silently overwriting changes. The project remains queued; this plan does not authorize execution.

## Goal and scope

- **Included:** validate the retained Agent, App, and Runtime work as one exact tuple; repair only demonstrated in-scope failures; then compose and promote reviewed candidates after generation integration.
- **Deferred:** full SDK/UI suites and unrelated baseline failures.
- **Build on:** retained concurrent-editing work and the promoted generation tuple. Exact historical SHAs, evidence limits, and branch rules are in [inputs.md](inputs.md).

## Sequence

Run [CE-FINAL](tasks.md#ce-final) and, only for a demonstrated failure, [CE-REPAIR](tasks.md#ce-repair-only-if-required); then complete the existing [CE-END](tasks.md#ce-end) review. After generation integration is promoted, [compose](tasks.md#ce-compose) once on frozen current bases, [review](tasks.md#ce-review), and [promote](tasks.md#ce-promote) the same immutable heads. Dependencies and exact proof are in [tasks.md](tasks.md).

## Completion boundary

Completion means the exact retained tuple passes the scoped checks, required outcomes have no blocking END-review findings, and the reviewed composed candidates are promoted under the existing authority. Proof must cover seven SDK nodes, the unchanged eight-case hosted wrapper, real hosted outcomes, SDK guarantees, and the cooperative limit. This does not claim full-suite coverage or establish future candidate results from historical evidence. The shared [run contract](../../skills/astrid-dev-shared/run-contract.md) and [initiative handoff](../MANAGER.md) retain execution and publication authority.

## Read next

- [tasks.md](tasks.md): task index, routes, dependencies, selectors, and acceptance.
- [inputs.md](inputs.md): retained source identities, evidence provenance, and branch policy.
- [Project queue](../../README.md): current status, owner, and estimate.
