# Composable project-delivery relationships

**Project:** Composable project-delivery relationships

**Goal:** An agent can trace Astrid's existing project-delivery records through one validated relationship model and reuse them for a second read-only path, without duplicating sources or changing current outputs.

**Status:** active

**Owner:** Plan 72 completion-run manager (one whole-project manager session, named in the Run start in inputs.md; owner-authorized 24 November 2026)

**Estimate:** About 2–3 engineering days remain for the completion run; the candidate code exists and passes on current `main`.

**Waiting on:** nothing to start: the completion run's cards are in [tasks.md](tasks.md#completion-run-owner-go-24-november-2026). Then the final review R, the owner's project-wide sense check and the owner's go to merge the project branch into `main`. On 24 November the owner moved this plan from Release 16 to the astrid-dev-only route ([D6](inputs.md#owner-decisions)).

**Run route:** astrid-dev-only

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md), [Plan workstream](../../skills/shared/workstreams/astrid-dev-plan/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above own the catalog facts; priority stays in [priority.md](../priority.md). [Inputs](inputs.md) · [Tasks](tasks.md).

**Vision role:** Foundational enabler — a shared internal interpretation of existing delivery records and relationships. It does not itself provide [CA-003](../../vision/gaps/CA-003-vision-experiments-progress.md)'s public evidence-trail proof or [CA-005](../../vision/gaps/CA-005-parallel-contribution.md)'s real concurrent-contributor proof.

## Outcome and scope

The development workspace already describes a path from vision elements and their **goals** (the authored aspirations), through gaps and projects, to selected releases and their issue fixes. Today the connections are read and interpreted by several purpose-specific parsers and exporters. **Make that existing path one explicitly testable, read-only composition of canonical records and typed relationships.** An independent agent can inspect each supported relationship, its source and its validation result, then answer where a goal's related project work appears in recorded release plans. The same foundation can answer a small different question, such as which frozen issues a release lists, without a second record model.

**Included:**

- One tiny shared relationship mechanism: references with stable, namespaced identities; typed links; deterministic collection and traversal; source provenance; and structural integrity validation. Keep domain-specific meaning in its existing readers.
- Adapt the existing vision/goal, gap, project and release readers to expose their already-authored connections, retaining primary/supporting relationships and the foundational-enabler exception. A goal is the existing aspiration, not a new parallel kind of vision content.
- Express the current **project-delivery composition** as a traversable view over those links, including real negative/unknown cases. Project membership in a release is based on authored release briefs, not implied by a plan's status.
- Prove reuse with one small **Issue → Release** read-only traversal of a release's authored/frozen issue records. An untriaged label or issue outside that record is not proof of shipment.
- Integrate structural checking with [the existing check registry](../../scripts/checks.py), and reuse [the existing generated-view machinery](../../scripts/views.py) and [public vision exporter](../../scripts/export_public_vision.py) rather than creating another publication path.
- Preserve today's public feed shape (including schemaVersion 1), primary gap/project classification, authored source ownership, existing status/authority rules and current check verdicts except for separately justified new relationship-integrity refusals.

**Not included:**

- A generic pipeline DSL, workflow scheduler, agent orchestrator, database/graph store, new schema or universal execution state machine.
- A second complete operational pipeline; the issue-to-release path is deliberately a narrow composability test.
- A new evidence envelope, experiment record, approval workflow, issue-label bot, status, release-publishing gate or automatic gap closure.
- A public, evidence-backed vision-to-execution narrative: [Plan 44](../44-vision-execution-trail/plan.md) owns that outcome. [Plan 31](../31-releases-from-astrid-dev/plan.md) owns publication; [Plan 52](../52-issue-intake/plan.md) owns issue intake; [Plan 53](../53-vision-aspirations/plan.md) owns authored vision-goal meaning.
- Product-repository changes, App UI changes, migration of every historical free-form evidence link, or declarations for imagined future pipelines.

**Scope guard:** A relationship may be emitted only from a canonical, parseable source. Unknown, ambiguous or unproven associations remain unknown. Human review decides the meaning of evidence; checks validate structure only.

## Existing work and decision

This is **an extension, not a replacement, of [Plan 48](../48-one-record-model/plan.md)**: it delivered shared record readers in [records.py](../../scripts/records.py), the [check registry](../../scripts/checks.py), declared [views](../../scripts/views.py), generated catalog and extension guide. It expressly did not build the proposed universal evidence envelope. Current domain owners include [vision_subject.py](../../scripts/vision_subject.py) for authored goal IDs, [gap_relationships.py](../../scripts/gap_relationships.py) for primary/supporting goal references, [project_contract.py](../../scripts/project_contract.py) for project-to-gap links, and [records.py](../../scripts/records.py) for release brief and issue-list parsing. The [public exporter](../../scripts/export_public_vision.py) consumes these contracts today.

The missing piece is **a small shared way to represent and traverse links across these readers**, not another place to store them. Competing approaches and source identities are in [inputs.md](inputs.md). The requester chose this intermediate outcome on 20 November 2026; the scope proposal [#1064](https://github.com/banodoco/astrid-dev/pull/1064) and Release 15 placement [#1071](https://github.com/banodoco/astrid-dev/pull/1071) merged. Candidate code and evidence exist, but independent critique, authorized run custody, release integration and acceptance remain open. See [inputs](inputs.md) and [tasks](tasks.md).

## Sequence and readiness

1. **Baseline and contract:** inventory actual readers and consumers on the execution base; pin existing feed, views, checks, classifications and failure fixtures. Design the smallest typed reference/link contract with a clear supported/unsupported list.
2. **Shared layer and domain adapters:** add the relationship module; expose existing goal, gap, project, release and frozen-issue links without migrating their canonical records. Perform one **RS1 design review stop** before downstream checks/views depend on the contract.
3. **First composition and validation:** make the current delivery relationships traversable; add integrated structural checks; migrate only duplicate interpretation that the shared layer truly replaces.
4. **Reuse proof and completion:** implement the separate Issue → Release read-only query, verify identical existing public outputs and old verdicts, document extension points, remove redundant code and complete **one final review round**.

Task routes, dependencies, exact test inventory, load-bearing proof and review gates are in [tasks.md](tasks.md). Implementation must begin only after the scope is accepted, a named owner records a run start, and actual base/dependency SHAs and release destination are pinned. The current code may move in parallel, especially Plan 53 and the vision-goals changes; re-check these contracts at dispatch. No implementation PR or release assignment is authorized by this planning PR.

## Interfaces and handoff

**Consumes:** canonical Markdown from `vision/`, `plans/*/plan.md` and `releases/*.md`; authored release issue snapshots; the existing source parsers; the `astrid_dev.py check/list/sync` registry and exporter. Live GitHub issue labels may provide triage context but must not silently become evidence that an issue shipped.

**Produces:** a small importable relationship contract (proposed home `scripts/relationships.py`), domain adapters, one concrete project-delivery composition (proposed `scripts/project_delivery.py` only if it avoids another layer), one registry-backed integrity check, focused negative fixtures and a short extension explanation. Their exact names/API remain subject to RS1. Plan 44 may later consume this projection, but this project promises no Plan 44 artifact or public redesign.

**Handoff contract:** give the next project the exact integrated astrid-dev SHA, the supported record and relation kinds, sources/provenance and explicit unsupported cases, plus native passing and failing test receipts. No task or release may infer publication authority from these links.

## Completion

At one reviewed, exact integrated astrid-dev commit:

1. A fixture and real-repository probe resolve **goal → gap → project → recorded release contribution** from the actual authoring sources, with primary/supporting links preserved and no false claim that a completed project closes its gap.
2. A distinct fixture/query resolves **frozen issue → release** using the same reference/link primitives without creating a parallel record, persistent graph or second workflow engine. Missing and merely proposed issue links remain unknown.
3. Negative fixtures reject duplicate identity, unknown target, wrong endpoint kinds, wrong primary cardinality and contradictory authored links, with source-specific diagnostics; structurally valid but strategically questionable relationships remain for human review.
4. The fixed-revision public vision JSON is byte-identical, including schemaVersion 1; generated public views and plan classifications are unchanged except documented, authorized mechanical outputs such as the new check listing. Existing golden failures and current acceptance/release protections retain their verdicts.
5. The relevant focused suites, full `python3 -m unittest discover -s scripts -p "test_*.py"`, `python3 scripts/astrid_dev.py check` and view synchronization checks pass at the candidate and existing negative controls are demonstrably still caught. Report exact original and final revisions, commands, environments, raw exits and any unrelated failures.
6. An independent architecture stop and final review accept the smallest sound solution, including removed duplicate logic, explicit unsupported cases, limits and handoff to later pipelines.

Completion does not mark CA-003 or CA-005 closed, publish a release, authorize downstream work or activate a second pipeline.
