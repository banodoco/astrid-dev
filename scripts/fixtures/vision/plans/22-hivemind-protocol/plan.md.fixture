# 22 — Hivemind protocol: local and collective knowledge

**Start here:** read [Astrid development skill](../../skills/astrid-dev/SKILL.md), use the [shared run contract](../../skills/astrid-dev-shared/run-contract.md), and inspect [tasks](tasks.md) and [inputs](inputs.md). Current status, owner and estimate are in the [project queue](../../README.md).

**Vision gaps:** [CI-002 — Independently owned, interoperable Hiveminds](../../vision/gaps/CI-002-federated-knowledge.md) (primary). This plan provides the protocol and dataset proof; routine agent use is addressed separately.

## Goal and scope

Turn the [October 29 Hivemind protocol proposal](protocol-proposal.md) into a **bounded, testable interoperable protocol and Banodoco proving-ground increment**. Independently owned datasets (local/private/team/community) should be able to record findings, link to each other, retain conditions and evidence, and exchange permitted knowledge without surrendering ownership.

The proposal is a *design input*, not a settled spec. Resolve its differences from [current Hivemind](https://github.com/banodoco/hivemind) before writing migrations or claiming compatibility.

**Included in proposed scope:** (1) record/identity/access and typed-link contract; (2) `find`, `inspect`, `contribute` behavior; (3) a local/private dataset proof; (4) Banodoco mapping and staged migration/adapter decision; (5) one second dataset able to exchange references or sanitized evidence; (6) privacy/security and source-custody checks; (7) decision-quality evaluation.

**Deferred:** indexing all possible sources, automatically publishing user work, arbitrary pack execution, replacing Astrid Runtime, default continuous agent integration across every workflow, and a large unqualified migration. Astrid-native, routine agent use is a separate [Plan 23](../23-agent-learning-integration/plan.md).

## Starting point and constraints

Banodoco Hivemind currently documents `resources` with immutable `resource_revisions` and an accepted head, `search`/`get_item`, and distinct contribution operations. The proposed protocol instead describes immutable dataset-prefixed entries/links/scopes/access, six link relations and three operations. **Do not assume these are already identical or that a compatibility-view migration is safe.** Investigate source identity, retention, privacy/deletion policy, conflicting methods, reported vs observed evidence and federation boundaries before choosing a cutover.

## Proposed sequence

1. **Reconcile the contract.** Freeze source, audit the actual implementation, decide record identities, revisions, scopes, access and relation semantics. Specify incompatibilities and chosen migration/adapter path.
2. **Prove a minimal local dataset.** Explicit local ownership, permission-aware `find/inspect/contribute`, idempotency and no implicit external writes.
3. **Prove Banodoco compatibility.** Preserve effective existing search and editorial authority; rehearse changes on disposable fixtures, test rollback and source-custody behavior.
4. **Prove one federation edge.** A private/local dataset can reference or submit an approved, sanitized receipt to a separate dataset; denied access does not leak data.
5. **Measure usefulness.** A real agent task receives more accurate, applicable guidance than raw search/no knowledge; contradictions and stale advice remain inspectable.

See [tasks.md](tasks.md) for proposed bounded work and non-goals. Split follow-on implementation projects only if independent outputs and owners emerge; do not silently broaden this plan.

## Completion

A versioned protocol/spec with fixtures and implementations for the limited proof; independently owned datasets exchange an authorized reference, source/revision/evidence survives; existing Banodoco behavior is preserved or intentionally migrated with evidence; documented security/privacy negatives pass; a real decision-quality comparison is recorded. Unproven or deferred features are explicitly named.

**Authorization:** Draft only. Owner go, actual branch/SHAs, dependencies, scoped checks and acceptance are still required before code changes, testing, or publication. This document does not override Hivemind's own source/roadmap authority.
