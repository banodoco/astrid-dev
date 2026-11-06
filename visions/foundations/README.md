# Shared foundations

These are **cross-cutting outcomes that make Astrid's four [vision principles](../vision.md) achievable**, not additional artistic principles. A foundational gap may support several principles or no single one directly.

| Gap | Desired outcome |
| --- | --- |
| [F-001 — Reliability across supported environments](gaps/F-001-platform-reliability.md) | Install, run, update, stop and recover safely on declared supported OS, machines and interfaces |
| [F-002 — Trustworthy user control and operation](gaps/F-002-safe-user-control.md) | Consent, isolation, concurrency and recoverable actions preserve people's work and control |
| [F-003 — Dependable end-to-end creative execution](gaps/F-003-creative-execution.md) | Supported generation/agent paths reliably produce usable creative results |
| [F-004 — Dependable extension lifecycle](gaps/F-004-pack-lifecycle.md) | Packs and their contributions can be installed, validated, updated, disabled and rolled back without corrupting work |

A **test suite** is a method of demonstrating an outcome, not necessarily its own vision gap. For F-001, for example, evidence is a stated platform/device matrix with successful *real* install/run/update/recovery routes, not a generic claim that tests passed.

Keep foundation gaps few, coherent and independently assessable. Do not invent a new gap for every refactor, build task or CI job. Plans can reference a foundation gap as primary and a vision gap as supporting, or identify themselves as **foundational enablers** when they do not independently establish a user-facing outcome.

See the [gap contract](../gaps.md) and [provisional review of the current plan queue](../references/plan-gap-assessment-2026-11-06.md). The assessment is a time-stamped review, **not** a second maintained plan registry.
