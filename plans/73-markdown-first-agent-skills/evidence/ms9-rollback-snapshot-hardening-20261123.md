# Plan 73 — rollback snapshot integrity and MS10 client-provenance hardening

**Disposition:** bounded repair **PASS** on the isolated Plan 73 recovery branch; **NOT** a D5 cutover, production rollback mechanism, independently instructed MS10 acceptance or final R.

## Source, reproduction and test receipt

- **Repaired source:** `f451491dde969837c063f9a566e15661161227be` on `p73/recovery-ms8-validation-20261123-1`, in [draft #1627](https://github.com/banodoco/astrid-dev/pull/1627) stacked on unchanged #1390.
- **Hosted exact-source proof:** [run 45232479692](https://github.com/banodoco/astrid-dev/actions/runs/45232479692), documentation job `137895394809` **SUCCESS**, plus vision-consumer **SUCCESS**, review-intake **SUCCESS**. Raw job logs report **580/580 Python unit tests PASS**, **64/64 post-build view tests PASS**, targeted golden fixture PASS, scripted MS10 rehearsal PASS, bounded MS11 negative matrix PASS, guarded MS7/MS9 rollback rehearsal PASS, repository checks and refreshed generated views PASS.
- **Latest rollback JSON/Markdown:** artifact `plan73-ms9-compat-rollback`, ID **14846853959** on that run, independently read. JSON records `source_sha=f451491dde969837c063f9a566e15661161227be`, `status=PASS`, **17/17 assertions true**, **12 command receipts**, `error=null`.
- **Latest D5-readiness JSON/Markdown:** artifact `plan73-ms9-readiness-hold`, ID **14847169785**, independently read. Exact source SHA matches; readiness **`HOLD_PENDING_D5_AND_INDEPENDENT_ACCEPTANCE`**, **20/20** primary source mappings present, no mapped source missing/mismatched, **765** literal references across multiple authority classes and **18 active-consumer files**. Counts include protected historical and test records, **not 765 instructions to rewrite**.
- **Local reproduction:** a small disposable Python fixture extracted the original `restore_legacy_links` preflight behavior. When its recorded `generated` map contained one owned link but the destination also contained a second symlink into `.generated/skills/`, the original helper removed the recorded generated link, restored the old link and **left the additional generated link in place**, producing an incomplete restoration with no refusal. This local fixture is a bounded reproducer, **not a full native checkout test**.

## Exact repair

Only the **disposable rollback exercise helper** `scripts/ms9_compat_rollback.py` was changed. Before any symlink mutation it now:

1. Refuses a symlinked or non-directory destination (matching the safe installation destination policy).
2. Refuses empty legacy or generated snapshots.
3. Scans installed destination entries for additional symlinks that resolve into this checkout's generated package tree but are **absent from the expected generated-link snapshot**; refuses before deleting/restoring anything.
4. Continues to preserve unrelated foreign links outside the generated tree, and requires exact recorded names, raw targets, old source paths and collision-free restoration.

Regression coverage was added to `scripts/test_ms9_compat_rollback.py`:

- `test_unrecorded_owned_generated_link_fails_before_any_mutation`
- `test_unknown_foreign_symlink_is_preserved_during_restore`
- `test_empty_rollback_snapshots_fail_closed`
- `test_symlinked_destination_is_refused`

All **nine** rollback helper tests (the five original plus these four) passed in the exact-head 580-test Linux inventory. Existing negative, foreign-collision and golden-view assertions were retained.

## MS10 independently instructed exercise readiness

The fresh-agent actor still receives only [its uncoached assignment](ms10-fresh-agent-assignment-20261123.md) and `agent/README.md`. The [proctor-only evaluator protocol](ms10-client-discovery-protocol-20261123.md) has been strengthened: a client displaying a matching skill name is not enough, especially when repository/user/admin/plugin scopes can contain **same-name skills**. Require the **actual installed source path**, its **content hash** tied to the exact checkout and an **actual client trace** showing the file being loaded. If client APIs or tools cannot expose that provenance, report **NO-RESULT** for source-bound discovery.

A fifth packet-contract test, `test_proctor_requires_selected_source_identity_not_just_skill_name`, passed with the hosted suite. These are **instructions and tests, not execution by a fresh independent agent**. Actual Codex/Claude CLI skill selection, explicit/implicit invocation and source loading remain unperformed in this manager environment.

## Safety boundaries and outstanding decisions

**Rollback is still non-atomic.** A failed symlink creation, malicious concurrent writer, process interruption, power loss or user-home permissions change after preflight could cause a partial result. The helper is **not** a supported production rollback command. The legacy `sync.sh` installer remains **not** an automatic rollback after generated-skill installation. D5 must specify a coordinated freeze, verified target snapshot, real client behavior, reversible transition procedure and owner decision before live migration.

The original independent RS1 technical verdict remains **BLOCK**, with only the six bounded RS1.4–RS1.9 fixes adjudicated; reviewer credential and round-count caveats persist. MS-7 live consumer owner decisions, D5, MS-9 legacy source deletion, genuine independent MS-10 agent and client discovery, integrated MS-11, formal independent final R, separate maximum-two-round whole-project Astra High sense check and explicit owner project-to-main GO remain outstanding. Old manager retirement acknowledgment is still inaccessible. No canonical task checkmarks, legacy sources, product repos, release instructions or protected main refs were modified.

**This document records pre-cutover preparation and intentionally makes no approval claim.**
