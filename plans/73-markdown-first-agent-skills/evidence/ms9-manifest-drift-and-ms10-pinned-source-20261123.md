# Plan 73 — manifest-integrity rollback and pinned PR-only exercise source

**Disposition:** bounded regression repairs **PASS on GitHub-hosted Linux**, not migration approval, final MS-9/MS-11 acceptance, production rollback, or independent MS-10 completion.

## Exact source custody and receipts

- **Validated candidate SHA:** `7a61ae0c9308d6e782710629d323e44bf81c4d68`, on isolated `p73/recovery-ms8-validation-20261123-1`, draft [#1627](https://github.com/banodoco/astrid-dev/pull/1627) stacked over untouched #1390.
- **Hosted exact-head results:** [Documentation integrity 45244356796](https://github.com/banodoco/astrid-dev/actions/runs/45244356796), job `137937106933` **SUCCESS**; `vision-consumer-contract` **SUCCESS**; `review-intake` **SUCCESS**. Raw documentation log: **587/587 Python tests PASS**, **64/64 post-build view tests PASS**, targeted golden fixture PASS; built/checked generated skill packages, scripted MS10 rehearsal, MS11 negative matrix, guarded MS7/MS9 rollback and repository/generated-view checks PASS. Publishing and auto-merge skipped.
- **Rollback machine proof:** artifact `plan73-ms9-compat-rollback`, ID `14853961172` attached to run 45244356796, contains `ms9-compat-rollback.json` and `ms9-compat-rollback.md`. Independently inspected archive: `source_sha=7a61ae0c9308d6e782710629d323e44bf81c4d68`, `status=PASS`, **21/21 assertions PASS**, **12 command receipts**, `error=null`. All source and destination roots in the exercise were disposable.
- **D5 HOLD machine proof:** artifact `plan73-ms9-readiness-hold`, ID `14854155953`. Independently inspected exact SHA, **20** primary old-to-new source mappings with **zero missing/mismatched**, **14** retained historical authored `SKILL.md` manifests, **nine** retained aliases, **767 literal legacy-reference matches across protected scopes**, and **18 active-consumer files**. Readiness is `HOLD_PENDING_D5_AND_INDEPENDENT_ACCEPTANCE`. Not all 767 matches require rewriting.
- **Reproduce without acting on live sources:** `python3 scripts/ms9_compat_rollback.py --source-ref 7a61ae0c9308d6e782710629d323e44bf81c4d68 --output-dir <outside-checkout-directory>` on an available Linux host with Git, Bash, GNU sed and symlinks. It fetches the exact source into a detached disposable checkout, uses a temporary home and skill directory, and never modifies the original checkout's tracked files.

## Bug A: link snapshots did not guarantee instruction identity

**Bounded pre-fix reproduction:** a temporary legacy `skills/astrid-dev/SKILL.md` was hashed before migration; then its bytes were altered while the legacy link targets remained valid. The earlier disposable `restore_legacy_links` preflight checked link strings, directory custody and collisions, then restored the legacy link pointing at **changed instructions** without refusal. Thus a successful link-level rollback did not guarantee the original `SKILL.md` was restored.

**Fix on isolated branch:** `restore_legacy_links` now requires explicit `expected_legacy_hashes` and `expected_generated_hashes` for all expected manifests. It refuses incomplete snapshot keysets, missing or modified legacy instruction manifests, missing or modified generated manifests and previously covered foreign collisions **before unlinking any installed symlink**. The one legacy `shared` pseudo-package is intentionally reference-only and exempt from having a `SKILL.md`; every generated package requires one.

**New regression tests:** `test_legacy_manifest_content_drift_refused_before_mutation`, `test_generated_manifest_content_drift_refused_before_mutation`, `test_missing_legacy_manifest_refuses_before_mutation`, `test_incomplete_content_hash_snapshots_fail_closed`, and `test_shared_reference_only_legacy_folder_has_no_skill_manifest`. The original nine rollback-helper tests remain intact. The integrated exact-source exercise now additionally injects **both** legacy and generated content drift and proves refusal before mutation. The hosted suite has **14 rollback-helper tests**.

**Important limit:** these are `SKILL.md` byte digests, not cryptographic manifests of *every* linked helper, reference, asset or external dependency. Old link restoration is still multi-step and **non-atomic**; crash/power loss, in-flight noncooperating writers, source asset drift, cross-filesystem behavior and untested OSes remain NO-RESULT. The helper is for disposable evidence only, not an authorized production restore procedure.

## Bug B: pinned draft PR commit may be absent from a clean clone

**Bounded pre-fix reproduction:** using a temporary bare Git repository with main and a draft commit reachable only through `refs/pull/1627/head`, a clean `file://` clone could not check out that 40-character draft SHA (`fatal: unable to read tree`). Explicit `git fetch --no-tags origin pull/1627/head` fetched it; checking `FETCH_HEAD` against the source SHA and detaching at that exact SHA then succeeded.

**Fix in the proctor-only [fresh-agent client protocol](ms10-client-discovery-protocol-20261123.md):** fetch the explicit `pull/1627/head` ref, compare `git rev-parse FETCH_HEAD` to `SOURCE_SHA`, refuse a moving PR head or mismatch, and verify the detached checkout and clean initial working tree. Do not silently use default `main`, a newer PR head or any different SHA. The uncoached [actor brief](ms10-fresh-agent-assignment-20261123.md) was not given the evaluator's answer steps, earlier attempt scripts or scoring rubric.

**New regression tests:** `test_clean_clone_of_pr_only_head_needs_explicit_fetch` runs the local-bare-repository negative/positive fetch sequence without network, and `test_proctor_fetches_and_verifies_pinned_pr_head_before_checkout` ensures the proctor packet contains and orders the exact fetch/match/checkout instructions. The hosted suite has **seven packet tests**. A full independent agent or real Claude/Codex client session **was not performed**; genuine client selector, source-bound instruction load, implicit matching and retirement remain NO-RESULT.

## Gates and next ownership

The current authoritative old `skills/`, `sync.sh`, historical evidence, release instructions, `tasks.md`, original #1390 and project/main were not changed. The original technical RS1 **BLOCK** persists with only six bounded RS1.4–RS1.9 remediations adjudicated; prior reviewer credential and disputed review-round caveats remain. The unconfirmed old-manager retirement, D5 active-consumer handoff, MS7/MS9 source migration, independent uncoached MS10 with real-client discovery, integrated MS11 acceptance, final independent R, separate max-two-round Astra High sense check and explicit owner project-to-main GO remain open.

**No D5 cutover, legacy deletion, task checkmark, independent-review verdict or merge is claimed.**
