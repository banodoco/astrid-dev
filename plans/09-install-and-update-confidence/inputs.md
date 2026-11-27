# Inputs: Install and update confidence

[Final Release 16 programme review](../../releases/16/evidence/final-programme-review.md) records current dependencies, estimates and remaining decisions.

[Plan](plan.md) · [Tasks](tasks.md)

## Current Release 16 evidence — 27 November 2026

The owner retains P09/P10/P29/P30 in the 18-project release. The current residual programme is in [P09](../09-install-and-update-confidence/plan.md), with per-ID dispositions in [tasks](tasks.md). [installation/update sense-check #2060](https://github.com/banodoco/astrid-dev/issues/2060) was read in full with its subsequent comments (none at the review snapshot); it is a source investigation, not a native proof receipt. Historical bases and publication commands below are provenance only.

Refreshed independent source heads: Agent R16 integration `4a2bad187f12e7b0d1ba5bd1164b4a076787516a`; Runtime R16 integration `55a541a7ab904873e63510e581a60742e1b83fb8`; published App `cc1d48f016fde55ad6b0609c619d8a4bcec56823`; Pinokio `1e4c1e77f0d2b1ed322d0112d5f40103c998c5eb`. These are not a frozen integrated R16 tuple. [R15 publication](https://github.com/banodoco/astrid-dev/issues/1836#issuecomment-7174076695) and the App source manifest identify release/required floor 15; fresh HTTP bytes and post-live owner confirmation remain distinct P31 evidence.

[P38 continuation handoff](https://github.com/banodoco/astrid-dev/issues/2050#issuecomment-7225429126) identifies draft Runtime #133 `ccfdacc3559e7cb219f1cac1fadc150d957122bf` and Agent #697 `8da74aa9821cb27caec7a3eec7a30e17733f5284`. It reports portable proof for authored deferred/cold fixes, not native systemd served-origin qualification. The [completed oracle follow-up](https://github.com/banodoco/astrid-dev/issues/2050#issuecomment-7225981241) corrects the broad impossibility inference: stock systemd does not supply the proposed frozen-definition compare-stop, but that is not identical to the canonical retained-owner requirement. The Lead must decide the supervisor-policy boundary and demonstrate its complete protocol; any reduced R15 primary action requires its exact product disposition. Current authored terminal/detached continuation does not implement managed Update-now/old service-start/local-page job consumption. No native positive is claimed. All shared-function reservations and original negative proofs remain intact.

Plans 52, 53 and 85 are excluded by the present owner instruction. Necessary measurements, product qualification and original regressions remain under existing retained owners and infrastructure; this evidence update does not reinstate the removed projects.

**Recovered recorded choices:** the preserved [#178 inputs at `5c1f139`](https://github.com/banodoco/astrid-dev/blob/5c1f1393d8b435ba16722359840704d0c95d3003/plans/29-update-and-release/inputs.md) explicitly record decision 18 (local `npm run update`, hosted curl) and decision 19 (R0 rollback offered only until the first successful post-handoff update, then retained R0 code/plist/version may be pruned). The PR was closed/unmerged; this is a recovered decision record, not proof that its implementation landed or a publication go. Do not ask the same policy question solely because main retains an older “pending” cell. Preserve user content/newer work and current P35/P38 authority; only a proposed change to that policy requires a fresh owner decision.


## Starting code

The source plan records `pre-main` as the intended base and destination for each repository. These are historical rules, not verified live refs. Freeze each current head at IU-0. No full base or donor SHAs were recorded in the source plan; record them at start. The exact Plan 08 verified heads and reusable donor commits must be recovered from its existing run evidence. Do not treat the R1 stand-in update as proof of a real released-version migration.

| Repository | Starting branch + SHA | Retained work / donor SHAs / unpublished changes | Verified predecessor output | Candidate branch | Intended destination |
|---|---|---|---|---|---|
| astrid-agent | `pre-main`; exact SHA TBD at IU-0 | Plan 08 update step and stand-in generator; exact commits/custody TBD at start | Plan 08 verified head; exact identity TBD | Fresh create-only candidate name recorded at execution | `pre-main` |
| astrid-runtime | `pre-main`; exact SHA TBD at IU-0 | Plan 08 update step if applicable; exact commits/custody TBD at start | Plan 08 verified head; exact identity TBD | Fresh create-only candidate name recorded at execution | `pre-main` |
| astrid-app | `pre-main`; exact SHA TBD at IU-0 | Plan 08 update step if applicable; exact commits/custody TBD at start | Plan 08 verified head; exact identity TBD | Fresh create-only candidate name recorded at execution | `pre-main` |

No dirty-work custody is specified in the source plan; establish and record custody at start rather than assuming a clean tree. Confirm branches and existing run state before use. Plan 01's `cli.py`/`backend.py` overlap is a sequencing dependency: IU-1 coordinates with Plan 01 I-02 and whichever lands second rebases as required.

## References and evidence

| Source | What it establishes | Identity or link | Limits / missing information |
|---|---|---|---|
| Plan 08 Release 1 | Verified predecessor output, five-row gate, and update step | [Plan 08](../08-release1-install-update/plan.md), [inputs](../08-release1-install-update/inputs.md), [tasks](../08-release1-install-update/tasks.md) | Exact run heads/donor commits must be recovered; stand-in update is not a real version migration. |
| Plan 01 installer consent | Shared installer-file sequence | [Plan 01](../01-installer-consent/plan.md), task I-02 | Exact branch/file state must be reconciled at start. |
| Per-OS coverage baseline | Path × OS matrix classified real, mocked, or absent | IU-0, to be recorded at start | No baseline exists in this plan yet; define the supported-path rows from this plan's scope and record evidence per Linux, macOS, and Windows. |
| Runtime CLI schema and installer/service routes | Contract, update entry points, platform-specific behaviors named in scope | Source paths and line references in the original plan: `astrid/installer/local_update.py`, `update_job.py`, `app_update.py`, `custody.py`, `service.py` (~110–127 and ~972–983) | Source identities are not frozen; inspect at task start. |

## Constraints

Preserve user data and the last working version on failed or unsupported operations. Use real hosted tests for supported user paths; mocked coverage does not satisfy the OS/path matrix. Pinokio remains in Plan 07 and pack install/update/rollback remains in Plan 06 PK-9. Follow the shared [run contract](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/shared/run-contract.md) for identity, routes, checks, review, and publication. No plan authorizes execution; preserve existing authority and review limits.

The separately paused [legacy-to-standalone conversion draft](legacy-conversion/inputs.md) records the mixed-owner incident, the independent design critique, and its unresolved recovery-admission policy. Its proposed extension does not change the authority or prior evidence of this plan.

## Phase 2: upgrade-safe installed state

| Source | What it establishes | Identity or link | Limits |
|---|---|---|---|
| User incident, 12 Nov | R1 (Agent `7247ea92`, Runtime `9fc53b77`) → R12 update fails: `PackValidationError: external pack id 'hivemind' conflicts with a core pack`, pack host exit 1, rollback | Sanitized install.log traceback; R12 Agent `0e1543e0` `astrid/core/pack/ownership.py:43` | One machine; the affected group is derived from code, not measured |
| Release lineage | Login provisions a managed Hivemind in R1, R9 and R10; core Hivemind plus the fatal conflict exist in R2–R8, R11 and R12; R2–R8 were a parallel line merged at R11 | App `public/install-manifest.json` history; Agent `auth.py`, `source_setup.py`, `discovery.py` and `ownership.py` at each release SHA | — |
| CI reproduction without login | R1 → R12 updates cleanly when no managed Hivemind exists | astrid-agent `scratch/r12-r1-update-repro` `377b7af1`, run 43214297253 | Seeded data only |
| Reviews | Category, flaws and minimal design; R12 sign-in depends on the legacy checkout; dirty or deleted legacy copies also fail | Astra rounds 1–3, 14 Luna probes, Fable review (12 Nov); Fable reproduced the failure and confirmed a set-aside restores the host | Read-only reviews; the credential-store continuity of a new helper is unverified |


## Proposed Release 16 scope reconciliation (25 November 2026)

This is a proposed scoping amendment from [SYN-01](https://github.com/banodoco/astrid-dev/blob/4259785be40565ba940ecb076ca8c9889742d7cf/releases/16/evidence/scoping/SYN-01.md); scope, execution and publication remain subject to the existing independent reviews and owner decisions. Existing task progress, accepted decisions and historical evidence remain unchanged. Where historical sequencing differs, the following describes the proposed R16 task-level sequencing; it does not change existing delivery authority.

**D-SYN-1 — proposed, not accepted:**

Adopt a bounded R16 gate: every **effective required status on the exact candidate** must pass; every retained positive/negative release journey must pass; no known harm, supported-path failure, new/lost failure, or unclassified failure may be accepted. Build a complete executed inventory against the actually served predecessor, with repository, job family, OS/architecture, selector/configuration and full test identity. Combine shards within each job family; shard is provenance, not identity. Preserve duplicate/subtest accounting explicitly. Missing/skipped/cancelled/not-collected cases, newly quarantined cases and absent proof are not passes. Formerly-red disappearing cases need a documented removal/equivalence decision, just as formerly-green missing cases do.

An **actually executed, nonrequired inherited red** may remain only with a named, evidence-backed nonharm classification, owner acceptance, and a later owner/task. Candidate-equal or old does not mean harmless. In particular, the latest #2002 descriptor and occurrence-precondition groups remain unclassified until investigated. No change to assertions, required names, gates, bypass rules or job selection merely to produce this result. P91's full green cleanup remains R17. If the actual protection or owner policy instead demands all jobs green, that is binding: fund the minimum required repairs or hold R16. Record this choice in P31 inputs and remove contradictory literal all-green wording only through the approved canonical amendment.

P31 stays in R16. RL-3 visible 0.1.0 and final review precede the first authorized Final transition. Keep the legacy integer for order and required floor; semantic display is a validated mapping. Carry forward the **actual published floor** (15 in the actual R15 publication, rechecked against served bytes before candidate freeze); minor does not mean required. Floor 16 needs an explicit reason and mixed-version/migration proof. Preserve RL-3's primary-UI fallback **“an earlier version”** for unmapped legacy releases, with exact legacy integer in diagnostics/records; do not invent public semantic versions. P58's existing record reader/generator is the only strategy/publication record home.

**D-SYN-4 — proposed, not accepted:**

Keep Windows, macOS, Linux and genuine Pinokio hosted/local; RunPod remains experimental with mandatory consent, cost and cleanup safety. Use the [proposed SYN support and negative matrix](https://github.com/banodoco/astrid-dev/blob/4259785be40565ba940ecb076ca8c9889742d7cf/releases/16/evidence/scoping/SYN-01.md#7-exact-support-negative-and-preservation-matrix) with the task/owner mapping in [the release acceptance record](../../releases/16.md#proposed-support-and-negative-acceptance). Select one maintainable managed Windows route after ER-0 compares the existing Portable adapter and recipe by actual provenance, custody and rollback work. Linux stays; existing Apple Silicon/MPS support does not promise managed macOS provisioning. No universal BF16 or literal `sm_89` requirement; prove the actual operator/dtype and compatible wheel on each representative cell.

Retain P38's minimal common role ABI C1/C2/R2 because one-home role authority is in the requested outcome and owner-requested source history. Reconcile the still-open D1 wording explicitly. Design/inventory can start early; landing follows the internal phase-one checkpoint. If the reviewed source proves that outcome requires a substantially larger redesign, request an owner scope decision before dispatching that expansion. It never gates independent lanes merely to create concurrency.

P52/P53/P85 are excluded by the current owner decision. Preserve retained product qualification and measurement with existing infrastructure; do not recreate their project or administration gates in this programme.

The proposed transition depends on D-SYN-1/4, an actual origin inventory, per-volume peak-space accounting and operation/lifetime-lock handoff. Quarantine optional packs and refuse missing required packs; preserve defaults, tombstones and credentials. Rollback after new work requires explicit preservation. The required floor is the actual published floor, not an assumed historical 14. Bootstrap refusal may leave bounded owned tool/cache/log preparation unless moved earlier: source currently writes before validating pins; it cannot be described as literally zero filesystem writes.
