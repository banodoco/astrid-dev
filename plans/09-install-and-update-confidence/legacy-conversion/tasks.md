# Tasks — Convert a legacy Astrid installation to standalone

[Plan](plan.md) · [Inputs](inputs.md)

**Task ids:** `LC-0` … `LC-11`; `RS1` and `R` are bounded review stops, not implementation. **Critical path:** LC-0 → LC-1 → max(LC-2, LC-3) → RS1 → LC-4 → LC-5 → LC-6 → LC-8 → LC-9 → R → LC-11. LC-7 and LC-10 run in parallel where their contracts are stable. Task ordering is based on shared contract/output, not merely shared files. **Test inventory:** tracked baseline and proposed additions below. Re-check against the code at dispatch; no tests are run during planning.

Routes follow the skill exactly: **N = normal, including ordinary hard; X = very hard; S = super hard/data safety; T = small taste/editorial refinement.** The user's “hard” bucket maps to X only for genuinely very-hard coupled work. There is no separate ordinary-hard model band. Actual models and efforts are bound in a later run, not guessed here.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| LC-0 Freeze candidate and reuse Plan09/38 work; make narrow worker setup available | N | implementation start | Source record, Plan09 overlap; canonical `astrid-dev/env/` and corresponding product `scripts/worker-env/` only if missing | Exact pins/dirty-state/donor map; after authorized execution only, named setup smoke and inventory baseline once | [ ] |
| LC-1 Define truthful legacy recovery-admission contract | S | LC-0 | Agent installer admission and Runtime custody boundary contract; no live apply | Decision table covers mixed owner, authentic managed owner, offline realm and refusals; unchanged old guards; independent code-backed policy critique | [ ] |
| LC-2 Add minimal Runtime-owned continuous custody/handoff | S | LC-1 | Runtime admission/owner fence, existing bootstrap/boundary/broker APIs; shared identity owner preserved | Real owner stop/start under held admission; exact child binding; contender and helper/parent failure tests | [ ] |
| LC-3 Prepare complete pinned recovery installation | X | LC-1 | Agent `Backend.stage`/validation and version-owned recovery descriptor/bootstrap; dependency/tool pins | Archived/candidate-independent interpreter boots; full pack-host/chat and effective instructions; declared required capabilities | [ ] |
| RS1 Review custody and recovery prerequisites (at most 1 proposed round) | S | LC-2, LC-3 | read-only integrated boundary | Independent review against LC-1 policy; findings become RS1.n; protects data-changing integration | [ ] |
| LC-4 Reuse the existing transaction through a conversion adapter | X | RS1 | Agent `core.py:Installer` transaction dispatch, `transaction_context`; new `legacy_conversion.py` | Existing update tests unchanged; conversion uses same journal/engine; normal R0/source paths still refuse | [ ] |
| LC-5 Integrate rollback and fresh-process recovery | S | LC-4 | Existing Agent rollback/replay plus narrowly necessary Runtime restore/recovery hooks | Inject activation failure after real migration; full old-compatible recovery; exact-record interrupted replay; conflicting marker retained | [ ] |
| LC-6 Publish standalone selection and services without losing user state | X | LC-5 | Agent Backend registration/start/selection/identity and existing instruction/config consumers | Original root/realm/project/config remains; real authenticated Agent/service function; truthful candidate identity | [ ] |
| LC-7 Expose explicit conversion CLI and structured results | N | LC-4 | `cli.py:parser,main`, existing summary/status serializer; no new UI | Public entry reaches adapter only after admission; available/refused/failed/recovered/completed statuses; no success on preview | [ ] |
| LC-8 Qualify real native conversion, failure and concurrency matrix | S | LC-6, LC-7 | Narrow Agent/Runtime native integration fixtures and existing hosted lifecycle job | Public entry; lived-in old family; migration, service recovery, restart race and crash boundaries; exact pins/evidence | [ ] |
| LC-9 Verify editable timeline, project switch and instructions | N | LC-8 | Existing browser journey harness + one new conversion case; fixture data only | Connected and current; preserved timeline edit/reload/switch; actual chat instruction injection; no response interception | [ ] |
| LC-10 Refine conversion/refusal/recovery wording | T | LC-1, LC-7 | One CLI message family and setup doc passage only | Each message matches actual structured state and gives exact next action; no data reset/unsafe retry advice | [ ] |
| R Final integrated review (at most 2 proposed rounds) | S | LC-8, LC-9, LC-10 | read-only exact integrated candidate | Review policy, data preservation and actual proofs; findings become Rn.m; no blocking finding waived | [ ] |
| LC-11 Release handoff, then separately authorized real-machine acceptance | N | R | Existing release process and official installer invocation only | Official published tuple; successful real original timeline and services on standalone; retained recovery evidence | [ ] |

Task cards use source identities from inputs.md. X/S leads delegate bounded reading, mechanical edits and checks to N helpers, retaining design/judgment. The policy/contract and task ambiguities are resolved before downstream dispatch, not by inventing authority mid-run.

### Test inventory and worker commands

Verified **tracked** Agent files at the inspected base:

- `tests/test_installer_r0_entry.py`
- `tests/test_installer_transaction_authority.py`
- `tests/test_installer_backup.py`
- `tests/test_installer_pre_stop_recovery.py`
- `tests/test_installer_release0_rollback.py`
- `tests/test_installer_pinokio_custody.py`
- `tests/test_installer_candidate_validation.py`

Verified Runtime test paths at the pinned source:

- `tests/test_operator_upgrade.py`, `tests/test_operator_upgrade_recovery.py`
- `tests/test_runtime_upgrade.py`, `tests/test_v33_historical_backup_restore.py`
- `tests/test_bootstrap.py`, `tests/test_real_bootstrap.py`
- `tests/test_native_custody.py`, `tests/test_role_custody_authority.py`
- `tests/test_prepared_child_owner_custody.py`, `tests/test_retained_process_custody.py`
- `tests/test_profile_services.py`, `tests/test_service_stop.py`

These files define the candidate inventory; LC-0 narrows selectors by the exact symbols changed before running its one baseline. Do not run all files after every card. New tests below are **proposed additions**, not tests that already exist: Agent `tests/test_installer_legacy_conversion.py` and `tests/test_installer_legacy_conversion_native.py`; Runtime `tests/test_legacy_conversion_custody.py`. Prototype `test_installer_legacy_source_admission.py` and portable-adoption files are untracked donor research, not part of the official baseline. Browser selector is Pending LC-0: locate the existing journey harness and record a real selector before dispatch; do not invent one.

Workers call literal product-root commands, after LC-0 confirms/copies the canonical shared environment scripts:

```text
bash scripts/worker-env/agent-setup.sh
bash scripts/worker-env/agent-pytest.sh -q <card's explicit files/selectors>
bash scripts/worker-env/runtime-setup.sh
bash scripts/worker-env/runtime-pytest.sh -q <card's explicit files/selectors>
```

The placeholders above are command shapes, not executable acceptance commands. LC-0 fills each card with actual selectors from its candidate; the explicit file sets below are the initial choices. Fetch other public repositories by git at verified pins, never GitHub archives. Do not copy setup into the plan directory. Native Darwin proof runs on a declared macOS worker; Linux-only cloud proof is not a substitute. Exit 3 from shared setup is an environment problem, not a product failure. Planning performs none of these commands.

Load-bearing runs: one baseline inventory before first implementation; each card's focused proof after its change; LC-2/LC-3 shared boundary before LC-4; integrated full relevant suite once on hosted CI before R and promotion. Carry unchanged evidence forward; record actual inner exit status, source tree/pins and limitations. No broad local runs, xfails or weakened oracles.

### LC-0 — Source, reuse and environment record

Input: source table in inputs.md and current official manifests. Deliverable: actual candidate identities and a retained-change inventory, bounded existing-test selectors, exact donor dispositions, and a Plan09/38 overlap/merge-order agreement. Do not duplicate IU-1 transaction consolidation or IU-13 lock handoff if their implementation has landed. Scope canonical environment scripts only when the required literal script is missing from its attached repository; preserve the public-git pin rule. Before implementation: record base/ref/SHA, official manifest date, pin consistency, no implicit use of untracked prototypes. Proof: source record and narrowly named setup smoke per product; baseline only after execution start. No product contract changes; no pinned oracle is invalidated.

### LC-1 — Admission policy and supported incident class

Input: incident's sanitized unknown-loaded-code class, owner requirements and existing guards. Deliverable: a finite admissibility table and typed conversion source descriptor, distinct from normal installed `Version`. Minimum rows: current same-user authenticated live legacy owner with unknown startup provenance; offline legacy realm; authentic managed Pinokio; source checkout actively used for development; conflicting realm/path/UID/process birth; active uninterruptible work; unowned occupied program root; unmanaged restart authority. For each row define allowed evidence, forbidden inference, exact pre-stop refusal, and recovery prerequisite.

Recommended new policy: user-authorized recovery transfers custody of their data, not trust in previously loaded code. The supported entry verifies current workspace/process identity and exclusion, then replaces code only with independently pinned candidate/recovery installations. Missing admission evidence is not filled by rewriting profiles or changing `managed_by`. Authentic managed Pinokio installations remain on their normal existing route and are not silently converted through this incident adapter. An active development checkout is refused; supporting intentional development-to-installed conversion requires its own accepted policy, not an inference from this request. The contract must make the actual incident class feasible or explicitly return a design blocker before LC-2/3; offline-only passing does not close this card's end-user outcome. LC-1 cannot choose D4 on the owner's behalf.

Scope: `backend.py:source_checkout_ownership,preflight_stop`, `cli.py:main` entry dispatch, Runtime owner/custody contract docs; LC-1 defines the interface, LC-2 implements it. Focused proof: proposed admission table cases in `tests/test_installer_legacy_conversion.py`; existing `tests/test_installer_r0_entry.py` and `tests/test_installer_candidate_validation.py` remain unchanged. **Makes untrue:** only the proposed statement that *all* standalone legacy recovery entries are unavailable; ordinary update/source refusals are not changed. No existing pinned test/fixture/oracle may be relaxed; re-check against code at dispatch and list any actual contradiction before changing it. Authority: design/fixture only until policy reviewed; no live stop.

### LC-2 — Continuous custody using the existing Runtime

Input: accepted LC-1 policy. Deliverable: a Runtime-owned operation/lease consumed by the installer, using existing installer/bootstrap mutexes, realm admission fence, owner.lock, authenticated birth-checked stop, process identity and role custody. Acquire the admission fence before stop; acquire owner lock only after the identified owner exits; retain exclusion through backup/migration and startup; bind the launched child's identity/realm/health before release. A compatible recovery bootstrap consumes a controlled inherited fence through the same broker, not a raw user-supplied FD flag. Changing the selected realm or lock inode invalidates the operation. Account for manager/client restart authority explicitly.

Scope: `astrid_runtime/operator_upgrade.py` fence/operator entry, `astrid_runtime/bootstrap.py` and `runtime_protocol` boundary/custody implementations resolved at LC-0; keep Plan38's canonical identity provider. The proposed version-scoped `Legacy31RecoveryBoundary` in plan.md is part of this interface: the old pinned binary is not assumed to understand a new flag or custody contract. The new conversion helper and verified old pair must have distinct truthful identities, explicit per-child environment and normal bootstrap publication. Do not introduce another global journal, identity parser or unchecked environment override. Focused proof: `tests/test_legacy_conversion_custody.py` (new), `tests/test_native_custody.py`, `tests/test_prepared_child_owner_custody.py`, `tests/test_retained_process_custody.py`, `tests/test_bootstrap.py`. Cases include contender before/after stop, PID reuse, wrong root/fd, parent/helper death before/after ready, lost lease, safe refusal with old owner unchanged. **Makes untrue:** the current inability to lend a *verified* held admission lease to this installer operation; no arbitrary FD/caller assertion becomes authority. Enumerate exact existing fixture/oracle lines at dispatch before changing the public boundary. No process identity or wire-schema change unless the contract explicitly requires and reviews it.

### LC-3 — Candidate-independent full recovery installation

Input: LC-1 version-family contract and official historical pair. Deliverable: complete staged recovery program identity and readiness evidence, including interpreter/base/dependencies, tools, Agent/Runtime/generated-client pins and version-owned service declarations. Reuse `Backend.stage` and candidate validation; avoid copying the mixed live `.pth` environment. Candidate preparation failure occurs before any source stop. Preserve configuration and effective instructions through a version-appropriate adapter without overwriting originals. Optional capability omissions must be declared; a capability needed by the user's timeline cannot be silently dropped.

Focused proof: Agent `tests/test_installer_candidate_validation.py`, `tests/test_installer_release0_rollback.py`, Runtime `tests/test_profile_services.py`, `tests/test_service_stop.py`, and new conversion-native recovery fixture. Prove boot with original source interpreter unavailable, genuine pack-host/chat connection, root/nested instructions consumed, and required timeline/render tool resolution without paid inference. Test missing libpython, old CLI options and wrong release identity. **Makes untrue:** reuse of the arbitrary retained venv as the sole recovery source for this new route; normal update recovery expectations remain. Any existing recovery test that changes must retain its original route assertion. Do not claim an actual release tuple when Python/uv/tool versions differ.

### RS1 — Review admission, custody and recovery contract

One proposed round by an independent high-judgment reviewer, exact integrated candidate, read-only. Must inspect code and native evidence, not summaries. Resolve LC-1's live incident class, source-versus-custody distinction, continuous fence handoff and full recovery preparation. Later data-changing cards depend on this stop because a bad assumption would invalidate all transaction work. Remaining blockers become scoped RS1.n cards or an explicit plan blocker; no extra rounds silently added.

### LC-4 — Minimal conversion adapter over the transaction

Input: reviewed contracts. Deliverable: new `legacy_conversion.py` plus the minimum extraction of `core.py:Installer._run_update_transaction` and `transaction_context` so normal update and conversion share durable phases. Preserve standalone release0/source guards on normal dispatch; no fake `Version`, manager marker or fabricated current pointer. Journal conversion kind, exact root/realm, actual original selection/profile/service bytes, candidate, prepared recovery identity and Runtime custody operation. Reuse core rollback/recover callback structure; one journal owns progress.

Focused proof: `tests/test_installer_transaction_authority.py`, `tests/test_installer_pre_stop_recovery.py`, `tests/test_installer_r0_entry.py`, and new `tests/test_installer_legacy_conversion.py`. Normal paths pass unchanged; public conversion path refuses prior to mutation when any prerequisite is absent. **Makes untrue:** transaction dispatch only knows ordinary/Pinokio update; only new-kind fixtures added. Existing R0 journal/entry refusal assertions remain. Re-check actual journal oracle lines at dispatch, preserve old-record recovery semantics and reject unknown future kinds.

### LC-5 — Same-path rollback and durable replay

Input: LC-4 journal and reviewed held-custody/recovery contracts. Deliverable: conversion recovery callbacks wired into existing `rollback_transaction`/`recover_transaction`; no second recovery engine. Prepare recovery before stop. On Darwin use the existing `Backend.backup` clone producer under established quiescence, explicitly not an authenticated-RPC backup; validate the canonical database, complete media/support inventory and selected realm before treating the clone as verified. Retain the separately created authenticated user backup as additional evidence, not the source of fabricated custody. Refactor `Backend.restore`'s existing clone-consumption path for conversion so verified contents can be restored while the realm directory and owner.lock inodes remain held and unchanged; journal staging/retention and crash replay without replacing the fenced root. Ordinary restore continues to use its existing behavior. This is the chosen path; do not also build a parallel Runtime-backup transport. Recovery starts the prepared compatible program with its truthful release/manager and own service bootstrap, then verifies readiness before releasing custody. Never discard post-activation user writes to make rollback pass; record the failure state and refuse unsafe restoration.

Fresh-process replay validates operation, selection, capsule and exact known publications under the qualified locks. If a marker conflicts or exact target exit/service drain is unproved, retain it and report `recovery_required`. Extend an existing broker receipt only for a demonstrated acceptance gap; no general exit-receipt framework is a default deliverable. Focused proof: `tests/test_installer_backup.py`, `tests/test_installer_pre_stop_recovery.py`, Runtime `tests/test_operator_upgrade_recovery.py`, `tests/test_v33_historical_backup_restore.py`, new native conversion fixtures. Inject failure before stop, after stop, after backup, after schema write, after start, before selection commit and before release; exercise fresh replay. **Makes untrue:** new conversion records become recoverable; no old unknown record or unrelated marker becomes deletable. List any current realm-replacement oracle that must change before editing it; preserve its data/history guarantees.

### LC-6 — Standalone publication with preserved state

Input: successful transaction/recovery integration. Deliverable: complete LC-4's shared activation/rollback callbacks using existing `Backend.register,start,persist_identity` and selection writers; this is not a second publication mechanism. Change only program-version/location and management identity fields needed for standalone. Preserve data-root path, selected realm/project identifiers and all unrelated selection/catalog fields; service command paths change to the prepared program but user env/config values and semantic instruction precedence remain. Journal original selection/profile/service bytes so rollback restores them exactly where their semantics are unchanged. Preserve project/timeline/media references, credential values and instruction/skill files. Stage program separately; no workspace selection command issued by users/agents outside the installer. Audit real manager/watchers through supported stop/fence APIs, not broad process killing.

Focused proof: Agent `tests/test_installer_candidate_validation.py`, `tests/test_installer_transaction_authority.py`, Runtime `tests/test_profile_services.py`, `tests/test_service_stop.py`, new native conversion fixtures. Real startup and restart, pack operation, chat connect plus deterministic instruction injection, no secrets in diagnostics, exact-state before/after inventory. **Makes untrue:** conversion switches only the selected program management to standalone after readiness; normal Pinokio identity remains genuine on its own route. Source/profile mismatch tests remain refusals, not rewritten expectations.

### LC-7 — Explicit public command and structured outcome

Input: LC-4 adapter contract. Deliverable: proposed conversion mode in `cli.py:parser,main` and existing summary/result surface; finalized command spelling is a small implementation choice, not permission to add a UI. Preserve ordinary `--update` behavior. Route conversion admission before ordinary source/R0 dispatch without catching and ignoring their errors. Emit `converting` only as progress/journal state; terminal results distinguish refused without stop, recovered, recovery_required and completed. Include exact log path and retained backup location without secret values.

Focused proof: Agent `tests/test_installer_r0_entry.py` plus proposed `tests/test_installer_legacy_conversion.py` CLI cases. A command ending in refusal must not report success or open an empty workspace. Reuse the current installer's browser-opening success behavior; LC-9 tests that existing behavior after readiness. **Makes untrue:** new explicit command is available for admitted source class; existing help/message golden fixtures may gain only the new command/result family. Re-check and enumerate exact strings at dispatch before modifying their tests.

### LC-8 — Native public-entry acceptance matrix

Input: exact integrated Agent/Runtime candidate, fixture source/recovery pins, LC-6/7. Deliverable: narrow native macOS integration rows through the actual public installer entry and source policy, not direct backend calls. Include lived-in authentic legacy and the mixed-provenance incident shape, complete media/documents/credentials/instructions, selected timeline and watcher/manager conditions. Real services, real migration, real locks and actual process exits; no fake admission, release labels or daemon identity.

Focused proof: proposed Agent `tests/test_installer_legacy_conversion_native.py`, Runtime `tests/test_legacy_conversion_custody.py`, plus relevant existing operator/recovery/service selectors pinned in LC-0. Real tests cover all LC-5 durable cuts and competing starts; unsupported admission refuses before stop. **Makes untrue:** no existing mocked test becomes native proof merely by renaming it. Explicitly record observer/environment substitutions; do not suppress EPERM or fabricate discovery to make cleanup pass. Integration success on clean offline data alone is insufficient.

### LC-9 — Browser and Agent user journey

Input: LC-8 qualified native fixture and exact hosted/client candidate. Deliverable: one existing-harness journey that opens the preserved project/timeline, confirms current standalone identity and Connected, makes a reversible edit on fixture data, reloads it and switches projects. A real chat connect must load retained root/project instructions; use a deterministic no-spend provider boundary, not a health-only assertion. The personal original tab with drafts is untouched during qualification.

Scope: existing App journey harness and Agent instruction-delivery fixture selected at LC-0, with only the narrow conversion case added. Focused proof selector is Pending LC-0 discovery; do not dispatch until its real path and command are filled. **Makes untrue:** none in the hosted compatibility contract; no response rewriting, legacy write fence removal or read-only preview counted as editing. If the current editor still fails on the candidate, give that product defect a separate scoped card rather than quietly broadening this plan.

### LC-10 — Taste pass on one message family

Input: LC-7 structured outcomes and actual failures. Deliverable: concise command/refusal/recovery wording in existing CLI summaries and one setup-document passage. Explain what happened, whether the old installation still runs, what data remains, and the exact supported next step. Avoid promising “updated” when recovery merely restored the old release. No new workflow, consent policy or state semantics in this task. Proof: reviewer compares every message with its actual structured state; targeted existing message snapshots only if the changed text is pinned. No blanket screenshot suite. Exact affected message oracle lines recorded before edits.

### R — Integrated review

At most two proposed rounds, agreed at run start, on exact integrated pins after focused tests and hosted relevant suite. Independent reviewer checks original requirements, minimal reuse, guard preservation, full failure recovery, fresh replay and actual browser/instruction evidence. Findings become separate routed cards. Stop early if no blockers; unresolved blockers after the budget go to the accountable advisor/owner, not another unbounded round. Publication waits.

### LC-11 — Official delivery and actual machine outcome

Input: reviewed release candidate and separate explicit publication/live-apply authority. Deliverable: ordinary official release inclusion and installer path, then real incident acceptance. Re-fetch/read official installer and manifest, preserve original verified backup, capture pre-state without secrets, invoke only supported conversion, inspect printed logs and `service-<name>.log` on failure, and verify current standalone identity, original selected data root, actual timeline editing/project switch and Agent instructions. If browser requests local-network permission, tell the user to choose Allow. Do not treat Connected alone as completion.

This card is a required end-user closure step but is not authorized by the planning request. No automatic publication, PR, release number or live mutation is implied. Focused proof: exact installed tuple and actual UI/API outcome with preserved project identity. No broad extra tests or cleanup. If official publication is unavailable, deliver reviewed source as incomplete and keep the live-update task open; do not relabel a local patched installer as official.
