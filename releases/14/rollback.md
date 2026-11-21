# Release 14 rollback — frozen-tuple runbook (DRAFT, NOT EXECUTED)

**Scope:** restore the last known good Release 13 **served App + installer manifest** after a Release 14 publish problem, without erasing a user's realm. This runbook is a conditional operational proposal and **not** permission for this packet session to deploy or modify product refs.

**Authority:** The Release 14 Lead coordinates; **the owner approves and an authorized Railway/App operator performs the hosted rollback**. Only an authorized publisher may change product `main` or produce a replacement deployment, and it needs the owner's go in that session ([release skill](../../skills/shared/workstreams/astrid-dev-release/SKILL.md#promote-or-publish)). The PUB-1 worker cannot execute any step below.

## 1. Last-known-good Release 13 identity (immutable source)

| Component | Last-known-good source / value | Verification |
|---|---|---|
| Hosted App source | `de7dd1e668aa6dcf3cbce013c701fa7c76615f99` | [R13 App commit](https://github.com/banodoco/astrid-app/commit/de7dd1e668aa6dcf3cbce013c701fa7c76615f99) |
| Immutable R13 manifest | [`public/install-manifest.json` at that App SHA](https://github.com/banodoco/astrid-app/blob/de7dd1e668aa6dcf3cbce013c701fa7c76615f99/public/install-manifest.json) | `schema_version: 1`, `release: 13` and `required.release: 13` |
| R13 installed Agent (manifest) | `9814193a73f606719e81883a8be197d27dd361d4` | Not the same as Agent `main` baseline |
| R13 published Agent source/CI baseline | `959da7326c982a9197b5d6e2a4489f45e1deef0e` | For per-ID testing, **not** the installer pin |
| R13 installed Runtime | `6855dfa8df65cf8ae4c002b57134d6505493c17c` | Manifest identity |
| Runtime schema | `sha256:9628bb5fd6e1dbbec392dd39f2e01031622dcf52d7ccff7cd1f0ad10743dcb1c` | Manifest identity |
| R13 installed VibeComfy | `dba38f8644c46f652376f2cd5112ea161e40f09b` | Manifest identity |
| R13 lifecycle | `7f0b025e9391baac9f5c2fb7393617ea6fef0704`, `0.3.1.dev0` | Manifest identity |
| R13 public canary | [run 44891402290](https://github.com/banodoco/astrid-app/actions/runs/44891402290) succeeded on the R13 App SHA | Canary proves served-manifest check then; reverify at time of rollback |

**Must capture before allowing R14 publish (BLOCKING):** the **exact active Railway deployment ID/image digest** that currently serves App `de7dd1e6`; the full R13 manifest bytes with SHA-256; current response bytes/headers from `https://astrid.haus/install-manifest.json`; evidence that the operator has permission to redeploy that immutable deployment; and a non-destructive rehearsal or provider-documented restoration action. Place a redacted receipt in `releases/14/evidence/` or link an access-controlled operational record. **These deployment identifiers and rollback permissions have not been verified by PUB-1; do not invent them.**

## 2. Stop and decide immediately on either trigger

1. **Served-tuple mismatch after publication:** the public `https://astrid.haus/install-manifest.json` is not the exact Lead-frozen release/Agent/Runtime/VibeComfy/schema tuple after the App deployment completes, or the served-manifest canary disagrees with that tuple.
2. **Save and reopen failure reported:** a normal edit that claimed to save does not persist on reopen, including an R13-to-R14 update or either mixed-version web/install state. Preserve the user-visible error, original realm and exact paired versions before attempting recovery.

For either trigger: the Lead declares a publication incident on the Release 14 mailbox, **stops further promotion/install advertising**, names the failing tuple, checks for an existing publisher, preserves manifests, job logs and user data, and asks the owner for the restore go. Do not suppress the failing assertion or treat a failed save as harmless.

## 3. Restore the served R13 App and manifest (operator only)

1. Identify the approved **last-good immutable R13 Railway deployment** from the pre-publish capture. Verify its built App SHA and embedded `public/install-manifest.json` byte digest. Do not select an arbitrary earlier deployment by timestamp.
2. Using the Railway deployment rollback/redeploy mechanism **only if the operator has verified it restores that exact image and manifest**, redeploy the immutable R13 build to the production service. Follow [App's hosted deployment guide](https://github.com/banodoco/astrid-app/blob/de7dd1e668aa6dcf3cbce013c701fa7c76615f99/docs/structure_detail/deployment_and_migration_guide.md) for what the hosted image contains. It builds with `npm run build:hosted` and runs on Railway; a local build itself is **not** a deployment.
3. **If no trusted immutable R13 image or safe restoration mechanism exists:** stop, keep the incident BLOCKED, and seek an explicitly approved **forward** corrective deployment built from and verified against the R13 App source plus its exact R13 manifest. Do **not** reset, force-push, or rewrite a shared `main`; do not mutate the installer release number without passing the release guard. The Lead/owner must authorize any production Git change separately.
4. After the platform confirms the rollback, fetch the public manifest and compare exact required values and **whole-file SHA-256** against the preserved R13 bytes. Verify `release == 13`, `required.release == 13`, the R13 Agent/Runtime/VibeComfy SHAs, lifecycle and schema digest. Confirm no R14 manifest remains on an alternate domain/cache edge. Run/observe the served-manifest canary against the restored deployment, and perform a small hosted App load and read-only reopen check on a preserved fixture.
5. Record the deployment ID, source SHA/image digest, manifest SHA-256, canary run, URL, time, operator, authorization and result in the incident evidence. Keep the frozen R14 evidence and branches intact for causal investigation and a separately qualified forward fix.

**No Git history rewrite or silent installer downgrade.** Installed clients may already hold the R14 code and a newer locally saved realm; restoring the hosted site does not automatically roll back any local user installation. Protect those versions and data separately.

## 4. Data safety and mixed-version checks

The [FIX-17 Release 13-to-14 matrix](packets/R14-FIX-17.md) must run **before** initial publication, including:

- Release 14 App versus a still-unupdated Release 13 Agent/Runtime install: an edit, save, reopen and one accurately explained rejected save;
- Release 13 App versus a realm written by Release 14: open, inspect its save queue and reopen;
- Windows/macOS/Linux update over a seeded R13 realm, **including save/reload after update** and a killed Windows update recovered on R13.

These rows are expected **evidence of compatibility, not a substitute for production restore verification**. The [owner's new combined-tuple ruling](https://github.com/banodoco/astrid-dev/issues/796#issuecomment-7063263106) specifically warns that Runtime's edited timeline save schema may not be backward compatible; a mixed row must prove it on the final merged schema. No green mixed-version receipt has been asserted by this packet.

When a reported save/reopen fails, preserve the original realm, its version, logs and drafts; **do not direct the user to delete a project, overwrite history or force an older Runtime to parse unsupported new schema**. FIX-16 offers a safe explicit copy-out or discard-and-reload decision for refused saves. Already-updated installations require their own supported recovery plan or a separately qualified forward fix, rather than an automatic R13 installer downgrade.

## 5. Closing the incident / resuming R14

The owner and Lead decide after comparing the public manifest and a real saved/reopened fixture. Announce which public tuple is served, what happens to R13 and R14 installed users, and what remains blocked. A subsequent R14 publication **again** needs exact frozen SHAs, the full release gates, a new owner go in the publishing session and the App-last deploy/canary order. No evidence from an invalidated tuple is silently reused.

**Pre-publication checklist:** [ ] immutable R13 deployment and restore mechanism confirmed; [ ] manifest bytes/digest captured; [ ] operator/owner authority established; [ ] FIX-17 both mixed rows pass twice on the final frozen tuple; [ ] full publication checklist signed off. If any are missing, keep publication **BLOCKED**.
