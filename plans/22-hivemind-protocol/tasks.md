# Tasks — Hivemind protocol

[Plan](plan.md) · [Inputs](inputs.md). **Draft task breakdown only:** no work is started or authorized. Assign routes, owners, exact source identities and focused commands at the implementation start, not from stale assumptions.

| ID | Proposed task and bounded output | Dependency | Proof required |
| --- | --- | --- | --- |
| HP-1 | Current-state audit + decision note: proposed entries/links/scopes/access against existing resource/revision/evidence structures; choose stable ids, exact references, privacy/custody and migration strategy | None | Mapping table, unresolved contracts and selected source SHAs |
| HP-2 | Versioned protocol schema with `find/inspect/contribute` semantics, error/access model, six relation categories and fixtures | HP-1 | Small positive/negative schema and idempotency fixtures; no invented trust from links |
| HP-3 | Minimal local/private dataset implementation/prototype with independent store, access policies and exact references | HP-2 | Local create/find/inspect/contribute, restart, denied read/write and no implicit outbound sync |
| HP-4 | Banodoco adapter or staged migration pilot preserving existing accepted-head search and editorial decisions | HP-1, HP-2 | Rehearsed disposable test, source/revision round trip, rejected/withdrawn invisibility and recovery evidence |
| HP-5 | One additional dataset interoperability proof with private-sanitized evidence | HP-3, HP-4 | Cross-dataset references resolve under permission; private content stays local; revoked/missing links fail safely |
| HP-6 | Agent decision-quality evaluation and limited source-custody/privacy hardening | HP-4, HP-5 | Compare no-knowledge/raw-search/protocol use on scoped creative questions; human review of relevance and failures |

No assumption that the October 29 sample counts, migration results, IP exposure claim, HTTP/MCP surfaces or link-tagger evaluation are verified current findings. Re-check each. No full ingestion at scale until a separate scoped plan exists.
