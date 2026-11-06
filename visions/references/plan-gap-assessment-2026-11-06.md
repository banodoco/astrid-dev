# Plan → gap assessment (2026-11-06)

**Status: provisional review, not a maintained index or an approved change to plan scope.** This assessment reads the [current Astrid Dev plan queue](../../README.md), plan goals and initial [vision gaps](../README.md). A plan's **own `plan.md`** remains the source of truth for its relationship once that mapping is adopted. This snapshot should be retired or kept explicitly historical once the backlog is reconciled; do not manually maintain parallel plan-gap status tables.

## Interpretation

- **Direct:** the plan's accepted outcome would produce testable evidence toward the named gap. The outcome might only *partially* reduce the gap.
- **Enabler:** the plan improves the system's ability to deliver/verify later outcomes, but does **not by itself** demonstrate a gap's desired state.
- **Primary / supporting:** one strong closest relationship is preferred; supporting associations only count if actual evidence is relevant. Related work is not automatically a dependency.
- **Foundation:** `F-` gaps sit as cross-cutting gaps, separate from the four artistic principles. Platform reliability and safety are outcomes; **testing is their evidence**, not automatically a fifth principle.

## Current plan mapping

| Plan | Proposed classification | What its actual completion would show | Important limit |
| --- | --- | --- | --- |
| [01 — Installer consent](../../plans/01-installer-consent/plan.md) | Direct → **F-002** | People can choose and control supported install behavior | Doesn't establish universal sandbox safety |
| [02 — Consistent generation](../../plans/02-consistent-generation/plan.md) | Direct → **F-003** | Compatible pinned defaults/recipes and CPU/fixture readiness | **No real inference** established by this plan |
| [04 — Concurrent edits](../../plans/04-concurrent-edits/plan.md) | Direct → **F-002**; enabling LS-002 | Concurrent agent/user edits respect conflicts and preserve work | Doesn't implement agent workspace composition |
| [05 — Release fixes integration](../../plans/05-remaining-fixes/plan.md) | **Foundational enabler** for F-001 / F-003 | Accepted fixes are coherently integrated and proven on named candidates | Release bookkeeping is not independent product-level reliability proof |
| [06 — Packs v1.3](../../plans/06-packs/plan.md) | Direct → **F-004**; supporting LS-003 | Pack install/trust/update/rollback and cross-product contribution lifecycle | Not a universal live component workspace |
| [07 — Pinokio basic](../../plans/07-pinokio/plan.md) | Direct → **F-001** | Launcher install/start/stop/update/remove flows on specified OS paths | Queue says **active**; indicative evidence doesn't qualify full native engine behavior |
| [08 — Release 1 install/update](../../plans/08-release1-install-update/plan.md) | Direct → **F-001** (**already done, partial gap evidence**) | Five named hosted rows passed on the recorded R1 tuple | Not all platforms/browser/device/engine scenarios |
| [09 — Install/update confidence](../../plans/09-install-and-update-confidence/plan.md) | Direct → **F-001** | Real-path install/update/rollback/recovery coverage across declared supported OSes | Test matrix and supported modes must remain explicit |
| [10 — Pinokio qualification](../../plans/10-pinokio-qualification/plan.md) | Direct → **F-001**; supporting F-002 | Native engine stop/custody and fully-local safety qualification | Requires live/native proof beyond launcher fakes |
| [11 — Three.js as a pack](../../plans/11-threejs-pack/plan.md) | Direct → **F-004**; enables LS-003 | First-party Three.js behavior survives pack extraction | Not proof of a general 3D workspace or arbitrary component composability |
| [12 — Multiple inference routes](../../plans/12-multiple-inference-routes/plan.md) | Direct → **F-003** | Additional real supported inference route with model/task lifecycle | Doesn't establish every provider/hardware combination |
| [13 — Execution host refactor](../../plans/13-execution-host-refactor/plan.md) | **Foundational enabler** for F-003 / F-004 | Clearer maintained host modules without changing behavior | Refactoring alone is not proof of a new creator-facing capability |
| [14 — Repository cleanup](../../plans/14-repository-cleanup/plan.md) | **Foundational enabler** | Better source navigation, less duplicate/dead code, preserved evidence | Don't invent a vague 'clean code' vision gap to classify a cleanup plan |
| [15 — OpenShell safety](../../plans/15-openshell-safe-execution/plan.md) | Direct → **F-002**; supporting F-001 | Qualified user-selected full-stack sandbox/permissions on specified platforms | No claim of absolute security or automatic browser-extension isolation |
| [16 — Streamlined agent experience](../../plans/16-streamlined-agent-experience/plan.md) | Direct → **F-003** | Agent choice, account setup, readiness and execution work in one supported journey | No claim of Hivemind learning integration |
| [17 — VibeComfy extensibility](../../plans/17-vibecomfy-extensibility/plan.md) | Direct → **LS-003**; F-004 enabler | One creator workflow proves reusable pack abstractions without forking core | H3_AV proof may not establish arbitrary UI contributions |
| [18 — Extensible timeline](../../plans/18-timeline-editing/plan.md) | **Enabler / partial evidence → LS-003** | Editing primitives and one alternate view over shared media | Doesn't establish general full-stack pack composition; existing plan already labels LS-003 supporting |
| [19 — First-principles documentation](../../plans/19-first-principles-documentation/plan.md) | **Foundational enabler** for extension adoption | Humans/agents can discover the supported mental model and workflows | A clearer guide isn't proof that the capability works end-to-end |
| [20 — Zero to first image](../../plans/20-zero-to-first-image/plan.md) | Direct → **F-003** | One supported real image-generation journey reaches timeline | First image does not close AA-001 (sustained ambitious art) |
| [21 — Astrid website](../../plans/21-astrid-website/plan.md) | **Communication enabler** for vision / CA-001 | An approved public website journey explains the product and ambition | A website doesn't establish artistic challenge culture |
| [22 — Hivemind protocol](../../plans/22-hivemind-protocol/plan.md) | Direct → **CI-002** (**already mapped**) | One testable cross-dataset knowledge boundary | Protocol alone doesn't give agents continuous learning |
| [23 — Agent learning integration](../../plans/23-agent-learning-integration/plan.md) | Direct → **CI-001**, dependency on CI-002 (**already mapped**) | Real agent retrieves, learns locally and can propose shareable evidence | No automatic public contribution or model training |
| [24 — Liquid workspace](../../plans/24-liquid-workspace/plan.md) | Direct → **LS-001**; supporting LS-002, LS-003 (**already mapped**) | Real frontend components and agents share workspace operations | One music demo doesn't necessarily close every related gap |

**Queue status at this review:** Plan 08 is marked `done`, Plan 07 `active`; the others above are queued in the draft README. These statuses are reported from the queue, not independently requalified. No product code/tests were run for this classification.

## What this reveals

1. **Infrastructure dominates the near-term queue.** Many plans improve supported-environment reliability, trustworthy operation or creative execution. These are not secondary in importance, just different in kind from the four artistic principles.
2. **Three artistic/community gaps have no direct plan:** [AA-001](../gaps/AA-001-sustained-creative-work.md) (sustained ambitious finished art), [CA-001](../gaps/CA-001-creative-challenge-culture.md) (ongoing artistic challenges/critique) and [CA-002](../gaps/CA-002-contributor-ownership.md) (real contributor ownership). This may be an intentional sequencing choice; the map makes it visible rather than forcing unrelated plans to masquerade as progress.
3. **Existing vision gaps still matter independently:** [LS-002](../gaps/LS-002-agent-workspace-control.md) and [LS-003](../gaps/LS-003-full-stack-contributions.md) have partial or proposed work, not proven closure.
4. **Plan 08 is the first useful manual reconciliation example.** Its accepted five-row result can update F-001 to *partially evidenced* without implying F-001 is fully closed.
5. **'Testing' should be expressed as qualified confidence.** Real-platform coverage is F-001's closure evidence. More candidate cross-cutting outcomes such as performance under large projects, accessibility across input/device modes and supported deployment-cost predictability deserve **investigation**, not automatically invented gaps without an observed baseline.

## Suggested next documentation step (not carried out by this assessment)

Review and adopt mappings in each plan's own `plan.md` with `**Vision gaps:**` (primary/supporting) or `**Vision role:** Foundational enabler`. Keep the current queue/status unchanged; do not add reverse plan lists to gap documents. For old completed plans, first compare their **actual** evidence to the new gap closure criteria. Only then update gap assessments, with source identity and a reviewer. Once mappings are adopted, this assessment remains a dated historical artifact, not a live index.

See the [gap format and reassessment procedure](../gaps.md).
