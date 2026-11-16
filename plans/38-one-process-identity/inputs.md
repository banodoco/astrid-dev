# Inputs — One process identity for Agent and Runtime

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — on 9 Nov 2026 the owner (Hannah) asked for this plan in session https://claude.ai/code/session_011EzfVzreGCJJQnTuXpbib9. It is queued to start after release 12 is published to `main`, and its completion is every test in its area green on macOS, Linux and Windows. The open decisions below don't change that scope.

**Prior art:** an independent root-cause investigation and the Runtime worker's reproductions ([planning session](https://claude.ai/code/session_011EzfVzreGCJJQnTuXpbib9)), with each key line re-read by the planner. The source revisions:
- Agent `ff40f2c684fc7ce22e42a5cacda5c63a0c8800a9` (the release-12 candidate), `a105de3a4852cb61b9647dfe2c920118bd29f272` (`main`) and `72462b04fa036736eb7fc9cb654def5f4ea2158c`;
- Runtime `744cf24874ea851f95949a706725aba19d18222f` (the release-12 candidate), `4f5477cb0f5b03d28bec991a1fe34edcd8fc309f` (`main`) and `52ec0578963847693a0df758d9bc1d55325f518f`.

Findings:
- **Linux and Windows: the peer token.** The Agent's `_peer_token` is Darwin-only at all three Agent refs (`custody_broker.py:594-596`), and so are `current_process_audit_token` (`:605`) and `signal_audit_token` (`:677`). The host calls them on every OS, through `AuthenticatedCleanupActor.current()` (`generic_host.py:14761`) and `.private_peer(control)` (`:16146`).
- **History.** The Runtime copied the Agent broker on 2026-10-20 (`15676e61188c680bd98f88075dc2b4cb17ac424e`), then added Linux custody on 1 Nov (`91f4a54e157c95f357fb634b89c9f99b983a97af`, `ae36d688bb04a7535cbde92bc3b515290e61cca7`). Its broker dispatches per OS (`astrid_runtime/custody_broker.py:181-202`, `:254-258`). That was never ported back to the Agent.
- **The birth-id format.** The Runtime writes `proc-start-ticks:N;boot:..;pidns:..` on Linux (`runtime_protocol/platform.py:592`). The Agent writes `ps-lstart:` from `/bin/ps` on Linux (`custody_broker.py:1586-1606`) and `<boot>:<ticks>` in `process_group.py:258`. So the host-only peer check fails at `generic_host.py:15645`.
- **macOS and Linux: closure parity.** The Agent measures `runtime_protocol` and `astrid_runtime` when they sit beside `astrid/` (`astrid/core/source_identity.py:49-53`). The Runtime's `_COMPONENTS` (`runtime_protocol/verified_host_launch.py:34-40`) does not. Each side requires its own digest (`verified_host_launch.py:412-414`; `generic_host.py:15667-15672`). For an installed pair, no single digest satisfies both.
- **The test.** `tests/test_installed_pack_custody_spawn.py:89` pins `boot_manifest_hash` as the raw-file sha, not the canonical hash (`astrid/core/_shared/boot_manifest.py:217,421`).
- **The Runtime worker's runs.** macOS: `diag/darwin-custody-spawn` at `b76de0d`, final run 42601137756, macos-15, installed non-editable layout. Custody and `serve_control` pass. Then come "host-only boot input differs" (`generic_host.py:15663`; `:15126` at R10) and "host-only admitted import closure differs" (`:15668-15672`). With the Agent's digest, the Runtime refuses instead with "materialized source closure differs from reviewed components". This is identical at R10, R11 and R12. An earlier harness bug (cwd egg-info shadowing the installed dist) is fixed on Runtime `fix/darwin-custody-spawn-harness` `458784af`. Linux, in the worker's sandbox at R12: with `_peer_token` bypassed, the start fails at `generic_host.py:15645` (the birth format), and with the Agent's digest it fails earlier, at `verified_host_launch.py:412-414`. So Linux has three stacked bugs and macOS two. These run and branch ids are as reported by the worker; the planner did not fetch them.
- **CI at the release-12 candidate:**
  - Runtime run 42579496915: `darwin-native` fails the custody-spawn test, and `sandbox-process-control` ERRORs the four Linux boundary tests with "Linux pidfd custody is unavailable" (`astrid_runtime/custody_broker.py:1864`);
  - Runtime run 42586102206 shows the same;
  - Agent run 42583740849 was cancelled.

  The [test inventory](tasks.md#test-inventory) has the details.
- **User exposure today: none by default.** Only the Runtime launches `--host-control-fd` hosts (`runtime_protocol/local_worker_composition.py:373`, `local_execution_supervisor.py:1009`), no production code writes a `host_only_cpu` profile, and the App has no caller.
- **Reuse:**
  - `runtime_protocol.process_binding` (it calls itself "the one place" but switches only Linux);
  - `platform.process_identity` and `process_birth_matches`, which already accept the legacy `<boot>:<ticks>` form (`platform.py:617-623`);
  - the Agent's `runtime.lock.json` and `scripts/vendor_lock.py`, which vendor Runtime artifacts by SHA (CI `ci.yml:439`);
  - the Runtime's `DeclaredXfail` and skip registry (`tests/lanes.py`) and the Agent's xfail guard (`tests/lanes.py:247-250`).
- **Negative findings:**
  - `remote_worker_deployment.py:62` digests a deployment, not a source closure, so it is not a duplicate;
  - the Runtime never computes the boot-manifest hash; it validates an opaque `sha256:` (`local_execution_supervisor.py:159`).

**Approach:** each piece gets the one home that both sides can import under the verified-launch constraints, and each task deletes the copy it replaces.

- **Process identity and peer custody go in `runtime_protocol`.**
  - The Agent host already imports `runtime_protocol.platform`.
  - The installed-origin probe requires `runtime_protocol`, `runtime_protocol.platform` and `astrid_runtime` beside `astrid/` (`astrid/sdk/host_bootstrap.py:1173-1212`).
  - The verified mapping covers that whole root (`local_worker_composition.py:1422-1432`) and refuses anything outside it (`verified_host_launch.py:756`).
  - The host imports Runtime code only after `verify_installed_host_startup()` (`astrid/core/execution/__init__.py:3-6`).
- **Rejected homes:**
  - `astrid_runtime` is the Runtime's application package (CLI, bootstrap, owner broker), and the Agent should depend on the protocol, not the application;
  - the Agent is ruled out because `runtime_protocol` "intentionally has no dependency on Astrid" and the verifier never imports the host;
  - a new shared package would add a fourth distribution, with its own pin, lock and release-record field, which is a second mechanism next to Plan 31's three-SHA record.
- **The closure keeps two measurers by design.** `verified_host_launch.source_checkout_closure` is an "independent parity implementation; never imports the selected host" (`:171-172`). The host measures before any Runtime import (`source_identity.py:1`; `host_bootstrap.py:1180-1181`: "Even importing the measurement helper would execute unvalidated product code"). So the one home is the definition: a Runtime-owned data file with golden vectors, vendored to the Agent by `runtime.lock.json`.
- **The boot-manifest hash stays in the Agent.** The Agent writes the manifest and is already its only producer.

**Challenge:** Reviewed — two independent sources ([planning session](https://claude.ai/code/session_011EzfVzreGCJJQnTuXpbib9)) confirm the diagnosis. The first is the root-cause investigation, which proposed the provider shape, the closure parity and the 4–6 day core. The second is the Runtime worker's macOS CI and Linux sandbox reproductions, which confirmed the three stacked Linux bugs and the two macOS ones independently. The planner re-read every key line and accepted or changed the investigation's proposals:
- *accepted:* the provider in `process_binding`, with the Darwin primitives moved into `runtime_protocol`, SO_PEERPIDFD and pin-on-inherit;
- *changed:* "one shared definition or golden vectors" became both: a definition file that carries the vectors, because the two measurers must stay separate;
- *added at the owner's request:* the role-custody core as phase 2, the one-implementation guards, the three-OS job, and the inventory of every area test to turn green.

The estimate grows from 4–6 days to 10–13 because of those additions. An advisor critique of the task split is still worth doing before dispatch, as part of the ambiguity pass.

**Proof and limits:** see [plan.md](plan.md#completion). Limits:
- Backend-specific tests run on their own OS (D4).
- Windows host-only start may need a transport change beyond the provider (D6).
- Journals written by release 12 in the old Agent birth format fail closed after the update (D3).
- Run and branch ids from the Runtime worker are as reported.

**Review stops and rounds:** recommended; the owner confirms.
- **RS1 after the provider (P1, P2r), at most 2 rounds.** A1, A2, A3, L1, F1, C1 and C2 all build on that API and its closure file. A late finding would redo both brokers' imports and the vendored lock.
- **The final review (R), at most 3 rounds.** It is security, custody and cross-repository work.
- **The phase 2 review (R2), at most 2 rounds.**

**Ambiguity pass:** pending. There are X, S and T tasks, and other agents will run them, so N helpers run one per task group at the start, against the published release-12 heads, and list only real owner decisions.

## Duplicate inventory

Every parallel implementation found, by `git grep` at Agent `ff40f2c` and Runtime `744cf248`. Each is deleted by the task named.

| Piece | Copy | Task |
|---|---|---|
| Peer token | A `astrid/core/execution/custody_broker.py:594` `_peer_token` (Darwin-only); R `astrid_runtime/custody_broker.py:181` (dispatches); R `runtime_protocol/linux_process_binding.py:131` (Linux, kept as the backend); R `runtime_protocol/posix_handoff.py:41,66` (`SO_PEERCRED`, `LOCAL_PEERPID`) | A1, P1 |
| Own token and details | A `custody_broker.py:517-605` (`_AuditToken`, `_token_from_words`, `audit_token_details`, `current_process_audit_token`); R `astrid_runtime/custody_broker.py:89-253` (the same, with dispatch); R `platform.py:1682-1705` (Windows `handoff_token`, kept as the backend) | A1, P1 |
| Signal and resume | A `custody_broker.py:677-765` (`signal_audit_token`, `_resume_audit_token_once`, `_posix_spawn_setexec_suspended`); R `astrid_runtime/custody_broker.py:254-275` | A1, P1 |
| Darwin census and start time | A `custody_broker.py:153-253`, `:464-498` (`kinfo_proc` structs, `_darwin_process_records`, `_darwin_process_start`); R `platform.py:397-423` (`_read_darwin_process_info`, kept) | A1, P1 |
| Process identity | A `custody_broker.py:1568-1606` `default_process_identity` (`ps-lstart` on Linux); R `astrid_runtime/custody_broker.py:1659` (wrapper, folded); R `platform.py:529-603` (the home) | A1, P1 |
| Birth-id encoders and matchers | A `custody_broker.py:236` `_ps_lstart_birth`; A `process_group.py:135`, `:235-258` `process_birth_identity` (`<boot>:<ticks>`), `:264-282` `_zombie_birth_identity`; A `generic_host.py:16262` `_selected_birth_matches`; A `custody_broker.py:2914-2934` (translator); A `platform_helpers.py:116-170` (leader check); A `vibecomfy_engine_adapter.py:98-101`; A `astrid/core/generation/engine_custody.py:474-477`; A `astrid/core/generation/target_launch.py:133-139`; A `astrid/sdk/host_bootstrap.py:156` | A1, A2 |
| Qualification scripts reading `/proc/<pid>/stat` | A `scripts/installed_product_surface.py:545`, `scripts/m4_6_process_observer.py:364`, `scripts/native_service_adapter.py:396`, `scripts/pinokio_platform_adapter.py:544-633` | A2 (provider, or a listed stdlib reason) |
| Source-closure definition | A `astrid/core/source_identity.py:39-53`; R `runtime_protocol/verified_host_launch.py:34-40` | P2r, A3 |
| Boot-manifest hash | A `astrid/core/_shared/boot_manifest.py:217` (the home); R `tests/test_installed_pack_custody_spawn.py:89` (fixed in release 12) | E1 (keeps it fixed) |
| Role-custody ABI | 59 names (classes, methods, functions) defined in both A `astrid/core/execution/custody_broker.py` and R `astrid_runtime/custody_broker.py`, 23 of them identical (difflib ratio ≥ 0.995) (`RoleCustodyAuthority`, `RoleBoundCustodyBroker`, `AuthenticatedCleanupActor`, `RetainedChildActor`, `_send_frame`, `_read_frame`, `_atomic_owner_json`, `_append_owner_jsonl`, `_open_authority_scope_lock`, `_acquire_scope_admission`, `_read_owner_file`, `_incarnation`, …) | C1, C2 |
| Agent test pins in Runtime CI | R `.github/workflows/ci.yml:31` (`e425903f`), `:143` (`4866090e`), `tests/astrid-agent.pin` (`b05ac03a`) | E1 |
| Adjacent, not this plan | A `astrid/packs/runpod/pod_source_identity.py` and `scripts/pod_source_identity.py` are identical except one path line (git source-pair identity, not a closure) | an issue |

## Recurrence guard

**Choice:** a one-implementation test in each repository (G1, G2). It sits in the default unit lane on every OS, so it needs no new job. It fails when a peer-credential, process-identity, signalling or closure primitive appears outside its home.

**Why this one:** it is the simplest guard that would have caught the 1 Nov drift. The Agent's copy of `LOCAL_PEERTOKEN` and `proc_signal_with_audittoken` would have failed the Agent's test, so the Runtime's Linux custody, which landed that day, would have been the only implementation, and the Agent would have used it.

**What backs it up:**
- the closure vectors, which reach the Agent through `vendor_lock.py check`, already in Agent CI;
- the three-OS `host-spawn` job (E1), which catches behavioural drift between the pinned pair.

**Rejected:**
- an import-linter dependency, which is a new tool for a rule a test states;
- a release-time cross-repo job, which is slower and later than the per-PR test.

## Alignment with Plan 31

- **The landing matches Plan 31's model of a release.**
  - The Runtime merges first.
  - The Agent re-vendors through `vendor_lock.py update`, setting `runtime.lock.json` `source_commit`.
  - The Runtime's single `tests/astrid-agent.pin` names the Agent it tests against.
  - The release record carries both SHAs.
  - Plan 31's RL-1b `release-contract` already fails a record whose `runtime` differs from the Agent's lock. So consistency at release time is already enforced, and this plan adds no gate there.
- **Coordinate, not own.** If Plan 31 later derives the Runtime's test pin from the release record, that is Plan 31's choice. This plan only collapses the three hand-kept pins into one file.
- **No piece moves to Plan 31.** The conformance this plan needs runs per PR, which is earlier than release.

## Owner decisions

Decided (9 Nov 2026, [planning session](https://claude.ai/code/session_011EzfVzreGCJJQnTuXpbib9)):
- the scope and the queue position, after release 12 is published;
- completion is all green on three OSes, with no xfail, skip or manual lane;
- duplicates are deleted in the same change;
- there is a mechanical guard;
- Plan 31 alignment;
- review stops follow the new rule.

Open, each with a recommendation:
1. **D1 Phase 2 (the role-custody core) in this plan.** Recommend yes, as phase 2 after phase 1 publishes. It removes the largest remaining copy, and it carries no user-visible risk, because the formats don't change.
2. **D2 The closure includes the Runtime packages beside `astrid/`.** Recommend yes, which is the Agent's current rule. They execute inside the host.
3. **D3 Old-format journals after the update.** Recommend accepting fail-closed: journals with the old Agent birth format (`<boot>:<ticks>`) read as "unknown" and are never signalled. The update stops hosts first, and `process_birth_matches` already refuses to match unscoped births.
4. **D4 What "no skip" means.** Recommend this reading:
   - every provider-contract, guard, vector and host-spawn test runs on all three OSes;
   - a test of one backend's kernel API (Mach task-name ports, pidfd, Job Objects) runs on its own OS, in a blocking job;
   - each OS has its own backend test.
5. **D5 Review rounds.** Recommend RS1 at most 2, R at most 3 and R2 at most 2.
6. **D6 Windows host-only start.** Recommend keeping it in scope if E1 shows it needs a control-channel transport change beyond the provider (row E1.1, S, about +1–2 days).
7. **D7 Linux custody under a seccomp sandbox (no pidfd).** Recommend that it stays a named refusal here (L1) and that a fallback belongs to Plan 15.
8. **D8 Priority.** Recommend queuing it after Plans 31 and 30. User exposure is none by default, and it unblocks host-only CPU hosts on Linux and Windows.

## Source identities

- **Base:** each repository's `main` after release 12 is published. Record the exact SHAs at T0.
- **Donors:**
  - the Runtime diag branch `origin/diag/darwin-custody-spawn` (`d299966c6edcf931236a976f7978ae74259f38a7`) for `tests/test_diag_host_spawn.py`;
  - `fix/darwin-custody-spawn-harness` (`458784af`, as reported) for the harness fix, if release 12 does not already carry it.
- **Integration:** `int/38-one-process-identity` in the Runtime and the Agent. Only the Release skill moves either branch to `main`.
