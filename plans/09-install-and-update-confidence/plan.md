# 09 — Install and update confidence

[Final Release 16 programme review](../../releases/16/evidence/final-programme-review.md) records current dependencies, estimates and remaining decisions.

**Project:** Install and update confidence

**Goal:** Make installing and updating dependable on all three OSes: one update path, and a real hosted test for every install, update, rollback and removal route.

**Status:** queued

**Owner:** Unassigned

**Estimate:** 2–4 engineering days remaining implementation plus 1–1.5 incremental integration/qualification days; shared P09/P10/P29/P30 total 6–11 + 3–5, counted once, excluding existing P38/P93/P94/P31 work and venue waits.

**Waiting on:** Existing installer/update transaction is reusable; [SC-09](https://github.com/banodoco/astrid-dev/blob/52c40028c067047533e222a017c92ac17f8cf5ba/plans/09-install-and-update-confidence/evidence/release-16-scoping/SC-09.md) reconciles prior work. R16 residual: schema-changing lock handoff, lived-in rollback/retention, route/OS and removal evidence; coordinate P29/P30/P10/P38. Await scoped dispatch, not a replacement installer.

**Vision gaps:** [Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (primary).

**Contributing:** [Astrid development skill](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/start.md).

## Release 16: complete the existing installation lifecycle

Plans 09, 10, 29 and 30 retain their separate outcomes but form one residual programme. The shared transaction, installation resolver, outcome record, local adapter, managed Pinokio adapter and platform workers already exist. Preserve them and repair only demonstrated gaps. The [installation/update sense-check #2060](https://github.com/banodoco/astrid-dev/issues/2060) supplies the task dispositions; the current [task ledger](tasks.md) records their canonical R16 homes. Historical Release 1–14 instructions and pre-main/int promotion lanes are not current dispatch authority.

**End state:** a person can install, repair, update and remove Astrid through the appropriate supported route on Windows, macOS and Linux. An interrupted or failed update preserves the previous working selection and user data, provides a truthful next step, and can recover and subsequently complete an update. Removal keeps user data unless its separate removal is explicitly requested.

### Ownership and residual work

| Existing owner | Retained responsibility |
| --- | --- |
| P09 IU-1/13 | Existing installer transaction, selection, migration lock handoff, rollback/recovery and retained-version policy. No new transaction or lock registry. |
| P29 with P30 LA-1–7 | One installed-owner/paired-version decision, truthful outcome and existing hosted/local adapters; no new update state machine. |
| P30 UR-15 | Safe worker launch, observation, settlement and interrupted-job compatibility on systemd 249/252 as well as newer managers. Lowering a version check alone is insufficient. |
| P10 PIN-2–4 | Actual Pinokio engine actions, Stop/Quit safety, settlement and hosted/local native proof; consume the common transaction and P38 custody. |
| P35 / P38 | P35 owns durable user-state compatibility; P38 owns live process authority and the currently reserved upgrade lifecycle hunks. P09 consumes these joins. |
| P93 / P94 / H3 P67 | P93 owns pack admission/default delivery; P94 owns environment/model provisioning. H3 companion selection uses the existing pack group transaction. These are not second Astrid installers. |
| P31 / Release Lead | One candidate tuple, qualification register, effective publication protection and authorized publication. |

The existing P38 `38-08U` author owns its reserved `core`/CLI/backend/service/local-update/outcome joins; the existing contract oracle owns the bounded managed-update contract question on [board #2050](https://github.com/banodoco/astrid-dev/issues/2050). Do not dispatch a competing P09/P29/P30 writer over those functions. Their latest portable source results do not constitute native served-origin proof. Native cold continuation/rollback and a supported live R15 transition remain open. The [completed oracle follow-up](https://github.com/banodoco/astrid-dev/issues/2050#issuecomment-7225981241) distinguishes retained process authority from the added frozen-policy assumption. The Lead must resolve whether authenticated supervisor policy is trusted and prove the selected route. If the stronger boundary is retained, managed Update-now, old service-start and local-page job continuation still need a reachable consumer; the current refreshed-terminal/detached route does not cover them. A one-time manual R15 transition would be a specific owner-visible support exception, not the existing releases-9-and-earlier exception. Safe refusal is mandatory where authority is absent, but does not discharge a promised successful update route.

### Preservation and qualification

- Use the actually published R15 origin and the final R16 candidate, with full App/Agent/Runtime/pack/launcher identities. R15 is published and its required floor is 15 ([publication receipt](https://github.com/banodoco/astrid-dev/issues/1836#issuecomment-7174076695)); P31 owns fresh served-byte verification and any separately approved floor change.
- Retain an inventory of every genuinely published supported origin. Share fixtures only where source-backed state/transition equivalence preserves the original origin obligation; do not invent historical versions or silently drop a published cohort. Keep content assertions, default-removal tombstones, credentials, revoked grants, pending edits/imports, user packs and user-owned environments.
- Verify changed-schema lock transfer where the candidate changes schema; retain faithful changed-schema contract proof otherwise. Do not remove or bypass the installer lifetime lock. Same-schema success does not prove this seam.
- Version-owned product definitions cannot be overridden by stale legacy copies. Durable user state outside the version root remains authoritative in its own domain. Quarantine invalid optional inputs where permitted; missing required state remains a truthful failure. No general hostile-home cleanup, removal of unknown content, or claim that arbitrary corrupt data can never prevent safe startup.
- Preserve last-good selection until verification. Prune only owned, unneeded state under the accepted rollback window; never restore over newer work. Record automatic failed-update rollback, retained R0 handoff rollback and release roll-forward separately. Do not promise arbitrary post-success downgrade.
- Reuse the existing journey harness and measured per-volume space checks. Native proof covers each supported OS/owner/route difference, including fully local paired update and genuine Pinokio hosted/local actions. Stand-ins remain logic tests. An unqualified promised cell stays open; naming a limitation does not silently remove support.
- Each positive journey includes failure/refusal, preserved state, recovery/retry and subsequent successful operation. Qualify busy/unknown owner refusal, stale PID, Windows locked files/DACLs, interrupted workers, failed activation, insufficient space, no-manager/autostart-off paths where supported, repair and data-safe removal. Reuse evidence across the four projects without duplicating whole runs.

### Execution order and completion

Prepare origin fixtures, P31 records, P10 engine feasibility and P30 disjoint worker/paired-state work in parallel. Land only the affected P35/P38 producer-consumer joins before their dependent transaction work. Run one early installed vertical journey; integrate required P93/P94/default-pack readiness, then freeze one tuple and run the native matrix. Independent review and actual release acceptance are separate from source implementation or portable tests. IU-END contributes its verdict to P31; it does not publish another release.

**Remaining shared effort:** 6–11 engineering days for residual implementation, focused regressions and fixtures; 3–5 days for integration/native qualification and resulting bounded correction, conditional on the P38 contract and real engine capability. This is the four-plan total (9–16), not four additive estimates, and excludes P35/P38/P93/P94/P31 implementation. Independent release review is budgeted once at programme level. An unresolved upstream capability or required support change is outside this range.

**Outstanding owner boundary:** Windows R0-origin upgrade versus explicit permanent safe refusal (IU-7), if no prior accepted disposition can be recovered. Keep the [legacy conversion draft](legacy-conversion/plan.md) paused. Existing R0 retention/command decisions are recorded in [inputs](inputs.md); do not reopen them merely because an old task cell says pending. Any change to retained support or rollback policy requires the owner; ordinary shared implementation sequencing does not.

## History and next records

Original decisions, historical task IDs and evidence remain in [tasks](tasks.md), [inputs](inputs.md) and the [prior complete plan](https://github.com/banodoco/astrid-dev/blob/2b43946a85f63a0a114023e271baf4952ed209c2/plans/09-install-and-update-confidence/plan.md). The shared [Release 16 brief](../../releases/16.md) and [run board](../../releases/16/run.md) govern scope, current reservations and publication authority.
