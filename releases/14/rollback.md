# Release 14 rollback — frozen-tuple runbook (DRAFT, NOT EXECUTED)

**Scope:** fix forward after a Release 14 publish problem, preserving user realms. An R13 deployment is a last resort. This runbook is a conditional operational proposal and **not** permission for this packet session to deploy or modify product refs.

**Authority:** The Release 14 Lead coordinates; **the owner approves and an authorized Railway/App operator performs the deployment**. Only an authorized publisher may change product `main` or produce a replacement deployment, and it needs the owner's go in that session ([release skill](../../skills/shared/workstreams/astrid-dev-release/SKILL.md#promote-or-publish)). The PUB-1 worker cannot execute any step below.

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

## 2. Response: fix forward

The [owner made Release 14 a required update](https://github.com/banodoco/astrid-dev/issues/796#issuecomment-7065093369). On a served-tuple mismatch or reported save/reopen failure, stop promotion, preserve the affected realm, drafts and logs, notify the Lead and owner, and prepare a qualified forward fix. The Lead coordinates; the owner authorizes publication and an authorized operator deploys it. Verify the frozen corrected tuple, served manifest and canary, and save/reopen a preserved fixture before resuming.

Restoring the R13 deployment is **last resort only**, requiring owner authorization and a verified operator and immutable image. It strands installations already updated to R14: they cannot rely on R13/R14 mixed-version compatibility. Do not downgrade installations or overwrite user data. Before publication capture the R13 deployment ID, image digest, served manifest bytes and SHA-256, and operator access and restoration evidence as described above. If a last-resort restore is authorized, verify those bytes, pins and canary after deployment, record the incident and explicitly communicate the impact on R14 users.

## 3. Data safety and qualification

FIX-17 must prove that the R13 App presents the required-update prompt and preserves drafts through update, and that an R14 install reopens R13-written realms including timelines, history and save queue. It must retain the Windows, macOS and Linux update rows and killed Windows update row. The former mixed-version rows fail by design and are no longer release gates. Preserve the original realm and drafts on any failure; do not direct users to delete projects or force an older Runtime to read an unsupported schema. Plans 59, 64 and 65 are in the combined Release 14 tuple and require qualification on the frozen SHAs.

Before publication, the Lead must confirm the last-resort R13 deployment evidence, operator access, the required FIX-17 receipts, and the full publication checklist. A forward fix requires its own qualified tuple and owner go.
