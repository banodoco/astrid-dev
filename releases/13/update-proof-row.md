# Release 13 — the R1-update proof row

**Read this first.** No file in astrid-dev, the brief or the release skill defines a row called "R1-update". The phrase appears only in [decisions.md](decisions.md) (the schedule: "the App re-pin and the R1-update proof", Saturday 06:00 to 10:00, and "the R1-update row come at candidate time"). This page therefore builds the row from what the repository does define, and the manager must confirm the reading before the proof is run. The reading used:

> **R1-update** = the update leg of the Release-1 installed-lifecycle receipt ("Release-1 installed lifecycle receipt", Agent `.github/workflows/journey.yml`): a real long-lived install from a published earlier release is updated, through the product path, to the Release 13 candidate, and the receipt shows the update succeeded and the installed product works afterwards. Plan 08 names this "stand-in next-version updates on all three operating systems"; the R12 matrix rows that cover it are `direct-linux-r11-update`, `direct-macos-r11-update` and the `r0 handoff, then update` legs of `direct-linux`, `direct-macos` and `direct-windows`.

If the owner meant a narrower or different row, only section 3 changes. See "Decisions needed" at the end.

## 1. What the skill and the brief require

From the [release skill](../../skills/astrid-dev-release/SKILL.md) and the [brief](../13.md):

1. The installed Runtime, Agent and App are one tuple. Branches qualified separately do not qualify the tuple, so the update proof is on the **frozen tuple** (App re-pin commit from [app-repin-checklist.md](app-repin-checklist.md)), not on `main`s or older heads.
2. Install, update, rollback, keep-data uninstall, migration and update-bridge journeys keep their semantics. The frozen `POST /v1/update` contract (signatures, errors, stop payload, proxy policy, journal linkage) is unchanged, and lost-ack recovery does not send an update POST by itself.
3. The App update guard resolves actions, flushes guarded persistence and then starts one update: a failed or delayed save means no POST, a successful save means exactly one POST, and status GETs only observe.
4. Timeline persistence is qualified on the integrated tuple.
5. Step 0 of publishing: list the install states real users are in (diagnostics received, past releases, migrations) and have CI cover each from that real starting state. **A proof row is named after its literal starting state.** So the row is named for what it starts from, for example "R12 served (Agent `0e1543e0`) to R13 candidate", and each past release users may still run (R9, R10, R11, R12) needs its own named row or an explained omission.
6. Evidence must bind the actual candidate SHAs and the inner command result, not a wrapper status or a historical baseline. Prepared-only output is not live evidence.
7. After publishing, the owner checks the release through the normal App path on a real long-lived install with no custom commands. Plan 29 is not done until that passes. That step is the owner's, not CI's.
8. Gate item 1 of the brief: the 11-row matrix, App Tests and Direct Journey with 0 failures. The update rows are part of those 11 rows.

## 2. Preconditions

- The App re-pin commit exists and is pushed (checklist step 9). Candidate JSON needs its SHA.
- Agent `journey.yml` and the harness (`tests/journey_matrix.py`, `scripts/journey_hosted_update.py`) on the frozen Agent head must still contain the update rows. VERIFY by reading `tests/journey_matrix.py` at `<AGENT>` (`RELEASE1_JOB_IDS`); the version read for this draft was published R12 (`0e1543e0`), where `journey_matrix.py` could not be fetched by that path, so the row list below is taken from the R12 matrix verdicts in [plans/29-update-and-release/evidence/r12/matrix-42835188782.md](../../plans/29-update-and-release/evidence/r12/matrix-42835188782.md).
- No RunPod, GPU or paid resource is used by any step on this page. The workflow runs on GitHub-hosted runners (Linux, macOS, Windows).

## 3. The rows (per the R12 matrix; confirm against the frozen head)

| Row | Starting state | Update to | R12 result (history, not R13 evidence) |
|---|---|---|---|
| `direct-linux-r11-update` | served R11 | candidate | failed on the R11 baseline HOME; fixed by harness `b550ecadf`; unproven |
| `direct-macos-r11-update` | served R11 | candidate | green |
| `direct-linux` (R0 handoff, then update) | R0 via the pinned Release 9 installer | candidate | environment failure (FFmpeg download timeout), rerun only |
| `direct-macos` (R0 handoff, then update) | R0 | candidate | failed, chiptune not ready; fixed in Agent `b2dc24ddb` |
| `direct-windows` (R0 handoff, then update) | R0 | candidate | failed at `packs add` (read-only git objects); fixed in `989cd0f6c`. Windows may legitimately refuse the R0 upgrade (the Windows update-refusal rows) |
| `direct-linux-fresh` / `direct-macos-fresh` | fresh install, then Update now in the candidate's own hosted App build | candidate | fresh linux failed after the update (HOME); macOS green |
| `direct-linux-autostart-off` / `direct-macos-autostart-off` | autostart off | candidate | harness read a top-level `reason`; fixed by `b550ecadf` |
| `direct-linux-r9-install`, `direct-macos-r9-install` | R9 | candidate | green |

The R1-update proof for R13 is: **every update row above is green on the frozen tuple, with a named starting state, plus the evidence in section 5.** PENDING: the manager confirms which of these the owner calls "the R1-update row" (see decisions needed).

## 4. Commands

### 4a. Free local checks (a person or a worker may run these; none touches a paid resource)

Preflight that the dispatch inputs are right, from an astrid-app checkout at the re-pin commit:

```bash
node scripts/installer/pin.mjs --check
node scripts/installer/release-guard.mjs <APP_BASE> HEAD --pins
node --test scripts/installer/release.test.mjs
```

Compute the manifest hash the candidate JSON needs (check how `journey.yml`'s `automatic_candidate` step computes `manifest_sha256` before using this: VERIFY):

```bash
sha256sum public/install-manifest.json
```

### 4b. The hosted matrix dispatch (CI, free of GPU; the manager dispatches it)

The R12 shape, from [releases/12/decisions.md](../12/decisions.md): `journey.yml` on the harness branch for the release, `direct_only=true`, with all of these supplied, otherwise the run fails at config (run 601 did):

- `candidate`: JSON with `app`, `agent`, `runtime`, `pinokio`, `manifest_sha256`. `app` is the re-pin commit; `agent` and `runtime` are the manifest's; `pinokio` is the workflow's fallback unless the manifest names one (R12 used `d15c58b5`).
- `old_launcher_ref`: the constant `bbba620e3d89eeff8021417f365e6ea584203105`.
- `stopped_path_agent_ref`: must equal the candidate Agent SHA.
- `direct_only`: `true`; `row`: `direct` for all rows, or one row id to rerun just that row.

```bash
# Dispatch (ORCHESTRATOR: it starts a write action on CI, and it is the binding run; do not use it as a shakedown)
gh workflow run journey.yml --repo banodoco/astrid-agent --ref <HARNESS_BRANCH> \
  -f candidate='{"app":"<APP_REPIN_SHA>","agent":"<AGENT>","runtime":"<RUNTIME>","pinokio":"<PINOKIO_SHA>","manifest_sha256":"<SHA256>"}' \
  -f old_launcher_ref=bbba620e3d89eeff8021417f365e6ea584203105 \
  -f stopped_path_agent_ref=<AGENT> \
  -f direct_only=true -f row=direct

gh run list --repo banodoco/astrid-agent --workflow journey.yml --limit 3
gh run watch <RUN_ID> --repo banodoco/astrid-agent --exit-status
gh run view <RUN_ID> --repo banodoco/astrid-agent --json jobs --jq '.jobs[] | {name, conclusion}'
```

`<HARNESS_BRANCH>`: R12 used `harness/29-r12`; PENDING: the branch that holds the harness for R13 (or `r13/compose` if the harness moved into it). A rerun of a single row: the same dispatch with `row=direct-linux-r11-update` (or whichever row id).

### 4c. Fetch the per-row receipts (read-only)

```bash
curl -s "https://api.github.com/repos/banodoco/astrid-agent/actions/runs/<RUN_ID>/artifacts"
# then GET each artifact's archive_download_url (works through the session proxy with no token, per the R12 handoff)
```

For each update row, the receipt files to read are `verify-update.json`, `update-job-record.json`, `update-transaction.json`, `update-transaction-status.json`, `update-job-journal.log` and, on the hosted-update rows, `update-button.json` (names from the workflow's upload list). Record: the starting release and Agent SHA, the final `agent.sha`/`runtime.sha`, the candidate App SHA, the inner command result, and the host's effective HOME (the R12 `direct-linux-r11-update` fix depends on it).

### 4d. App-side journeys on the same commit (CI)

```bash
gh workflow run direct-journey.yml --repo banodoco/astrid-app --ref r13/app-repin
gh workflow run test.yml --repo banodoco/astrid-app --ref r13/app-repin   # push to the branch already starts it; dispatch only to rerun
```

`direct-journey.yml` with empty `agent_ref` and `runtime_ref` reads both from the manifest, so it proves the pinned tuple.

### 4e. Post-publish, owner only

ORCHESTRATOR ONLY / owner: on the owner's real long-lived Mac install, click Update now through the normal App path with no custom commands. Record the before and after release number and Agent SHA. Nothing here is automated, and nothing here uses RunPod.

### 4f. ORCHESTRATOR ONLY steps

None of the update proof needs a paid GPU or RunPod. The steps that are orchestrator-only are the writes and the owner-gated ones: the App branch push, the matrix dispatch (it is the binding run), the merges, and the post-publish owner check. The paid generation proof is a separate claim: **ORCHESTRATOR ONLY, paid** ([release-record.md](release-record.md) claim 9).

## 5. Evidence to record (so the row is not "green" by assertion)

File: `releases/13/evidence/update-proof/<run-id>.md`, one table row per starting state, each with:

| Field | Value |
|---|---|
| Row name (literal starting state) | PENDING |
| Starting release, Agent SHA, Runtime SHA | PENDING |
| Candidate App, Agent, Runtime SHAs and manifest sha256 | PENDING |
| Workflow run id and job id | PENDING |
| Result of the inner update command (not the wrapper) | PENDING |
| Post-update verification (`verify-update.json`): tuple installed equals candidate | PENDING |
| Data kept: projects and timelines present after the update | PENDING |
| Rollback exercised (one forced rollback, per the patch-release rule, if the manager keeps that bar) | PENDING |
| Failures, with the cited R12 run if called pre-existing (test lane Rule 0) | PENDING |

Nothing is filled in here. No run has been made.

## Decisions needed

1. Does "R1-update" mean the reading above (the update rows of the Release-1 installed-lifecycle matrix), or a single specific row, or the Plan 09 IU-15 update rows (the skill's patch-release text points to "Plan 09 IU-15; until it exists, the matrix's update rows")? Plan 09 IU-15 does not appear to be built, so the matrix update rows are the working definition.
2. Which past releases must have a named starting-state row (skill step 0): R9 and R11 are in the matrix already; R10 and R12 are not named as rows.
3. Whether Windows keeps its documented refusal of the R0 upgrade as a pass, and whether a forced rollback is required.
