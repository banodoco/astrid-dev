# Release 12, Track A — Fixes

[Release 12](../12.md) · [Track B: Generation](generation.md) · Reference only: [Plan 29 handoff](../../plans/29-update-and-release/handoff.md) and [evidence](../../plans/29-update-and-release/evidence/r12/)

This page gives the **P29 manager** its orders. It is binding, together with [releases/12.md](../12.md). The Plan 29 handoff and brief are reference only, for SHAs, evidence and lessons; don't follow their gate, next steps or freeze text. This is a working brief, frozen when Release 12 becomes Final. State as of 10 Nov 2026.

## START HERE — P29 manager

- **Your tasks:** rows A1–A7 below, in order. A4 runs in parallel from the start.
- **First:** push a test commit to `scratch/p29-push-test` ([how-to](../12.md#how-to-tools-every-manager-uses)); run `smoke.sh agent` once.
- **Do now:** A0, A1 and A4 in parallel.
- **You may push:**
  - Agent `r12/cand-next` and `cand/29-r12`;
  - App `cand/29-r12` and `release12/candidate-manifest`;
  - the harness branch `harness/29-r12`.

  Push by full GitHub URL, adding commits only, never force.
- **You may dispatch:** early Direct Journey runs, Checkpoint A's runs (App Tests, Direct Journey, matrix, Agent CI) and the final round.
- **You message:** only the orchestrator, using the labels in [hand-offs](../12.md#hand-offs-all-via-mailboxes) (`A-CAND`, `A-FROZEN`, `MERGED`, `GATE-GREEN`, `PUBLISHED`).
- **Never:**
  - push `int/**` or any `main`;
  - merge VibeComfy;
  - land the CI-trigger prep;
  - weaken, skip or delete a test;
  - call a fix "drift" without trace evidence;
  - move `cand/29-r12` after `A-FROZEN` without the orchestrator's OK.
- **While waiting:** `RUN-STATUS: WAITING <label> from <sender>`.
- **How-to:** tests, comparisons, dispatch, artifacts and disk are covered by [How-to](../12.md#how-to-tools-every-manager-uses); commands are in [Commands](#commands) below. Need CI logs or traces? Post `NEED-ARTIFACTS repo=<r> run=<id>`.
- **You're done when** you have posted `GATE-GREEN` with the full tuple. The orchestrator publishes. Then end `WAITING PUBLISHED from orchestrator`, and fix anything the publish turns up.

## Where it stands

| Area | State |
|---|---|
| **Agent** | `cand/29-r12` = `313bbd46f`. `r12/cand-next` = `733ac5a43` adds five fixes (personal-pack snapshots, ready-marker fence, schema cache, Windows read-only cleanup, HOME in the update job and handoff launcher), **not yet proven**. Base failures are recorded in [agent-comparison.md](../../plans/29-update-and-release/evidence/r12/agent-comparison.md) |
| **App** | `cand/29-r12` = `8cfe10ce7` (Direct Journey rounds 3–6). The last early Direct Journey had 2 failures open: `:1264` (a seed helper uses the retired save route) and `:649` (Runtime restart, the draft survives) |
| **Harness** | `harness/29-r12` = `b550ecadf` |
| **Matrix** | The last full run was 4 of 11 green; each failing row has a root cause and a fix or a rerun ([verdicts](../../plans/29-update-and-release/evidence/r12/matrix-42835188782.md)) |
| **Reviews** | Rounds 1–3 done; round 3's blockers are fixed in `733ac5a43` |
| **Not yet adopted** | The Windows pack-exchange recovery fix: donor `plan32/r12-windows-recovery-donor` `26380e3a` repairs a bug from `35c170e39`, where crash recovery can delete the previous generation |

## Tasks

| # | Task | Depends on | Done when |
|---|---|---|---|
| A0 | **Make Agent CI measurable before the freeze:** fix the three collection errors that stop the unit shards on `main` and the candidate (see CI [42799672641](https://github.com/banodoco/astrid-agent/actions/runs/42799672641)); add `-rA` output, or a junit artifact, to the candidate's `ci.yml` unit jobs. P32 fixes only errors caused by generation code | — | One CI run on the candidate produces test ids that `baseline-diff.py` can read |
| A1 | Into `r12/cand-next`, merge `--no-ff`: the Windows donor `26380e3a` (check it against `989cd0f6c`; compare both parents). **A1b:** make the Agent's engine-recipe VibeComfy pin checked against, or derived from, the install manifest's pin at install. When `VIBECOMFY-RELEASE` arrives, set the Agent pin to it | — | Both merged; focused proof passes; every `tests/test_installer_*.py` runs |
| A2 | **One** before/after comparison on that head, against the recorded base, R11 and R10. Run `env/cmp-run.sh` once per commit, in parallel, then `baseline-diff.py` ([method](../../plans/29-update-and-release/evidence/r12/agent-comparison.md)). The recorded base run used Runtime `9fc53b77`; `agent-setup.sh` takes the Runtime from each commit's `runtime.lock.json`, so if the lock differs, rerun the base too | A1 | No new failures. Any regression against R11 or R10 is fixed, then A2 is rerun once |
| A3 | Push to `cand/29-r12`; run review round 4 on `313bbd46f..cand` (an Astra worker; see How-to); fix blockers; post `A-CAND`. Dispatch Checkpoint A's Agent CI and matrix right away, in parallel with the review | A0, A2, `VIBECOMFY-RELEASE` pinned (A1b) | No open blocker |
| A4 | Direct Journey round 7 onward (`:1264`, `:649`), then early Direct Journey runs until 0 failures. Diagnose each failure from its trace | — | Direct Journey 0 |
| **Checkpoint A** | Re-pin commit #1 (fixes-only tuple), then App Tests, Direct Journey, the full matrix, and **one Agent CI run** on the Agent candidate. Push `release12/candidate-manifest`, the manifest with the agreed pins, for P34 to install | A3, A4 | All green, including the Windows rows, which are the donor's native proof. Post `A-FROZEN agent=<sha> app=<sha> ci-run=<id>`. After this, `cand/29-r12` doesn't move |
| A5 | **Merge** after `CHECKPOINT-B`: fast-forward Agent `cand/29-r12` to `FINAL-B7`, which is built on `A-FROZEN`, so no new merge is made. Merge `plan20/staging-app` into App `cand/29-r12` `--no-ff` | `CHECKPOINT-B` | Post `MERGED` |
| A6 | Re-pin commit #2: the final Agent SHA, VibeComfy, the Runtime and a regenerated vendor lock. Then `vendor-lock.mjs check`, the runtime lock check, `cliSurfaceVerbs.test.ts`, `pin.mjs --check` and `release-guard`. Then the final round ([gate](../12.md#gate-final-tuple)) | A5 | Gate holds. Post `GATE-GREEN` |
| A7 | Hand over for publish: post `GATE-GREEN` with every full SHA (Agent, App, Runtime, harness, the VibeComfy, ComfyUI and lifecycle pins, and the manifest sha256). The **orchestrator** gets Hannah's in-session go and publishes with the Release skill. P29 fixes anything the publish turns up | A6 | `PUBLISHED` |

## Commands

All from the relevant checkout's root. Worked example: App commit `ecd0b0cf1` (a re-pin to Agent `313bbd46f`), and the vendor-lock dry run on `r12/app-vendor-lock-313bbd46`.

| Step | Command |
|---|---|
| Re-pin the manifest | `node scripts/installer/pin.mjs` with the final Agent and Runtime SHAs. Read the script's usage header first; check with `node scripts/installer/pin.mjs --check` |
| Vendor lock | `node scripts/vendor-lock.mjs update config/astrid-cli-surface/vendor.lock.json --producer astrid-producer`, then `node scripts/vendor-lock.mjs check config/astrid-cli-surface/vendor.lock.json --producer astrid-producer` |
| Runtime lock check | `node scripts/vendor-lock.mjs check runtime.lock.json --producer runtime-producer` |
| Release guard | `node scripts/installer/release-check.mjs origin/main --candidate` |
| CLI surface test | `npx vitest run --config config/testing/vitest.config.ts src/integrations/runtime/cliSurfaceVerbs.test.ts` |
| App Tests / Direct Journey / App lanes | Dispatch `test.yml`, `direct-journey.yml` and `lanes.yml` on astrid-app with `{"ref":"cand/29-r12"}` |
| Matrix | Dispatch astrid-agent `journey.yml` on `harness/29-r12` with `direct_only=true` and the `candidate` input, frozen JSON: `{"app":<40-hex>,"agent":<40-hex>,"runtime":<40-hex>,"pinokio":<40-hex>,"manifest_sha256":<64-hex>,"artifacts":{"public/install":<sha256>,"public/install.sh":<sha256>,"public/install.ps1":<sha256>}}`, all read from the App candidate. `journey.yml`'s automatic step builds the same shape |
| Agent CI | Dispatch astrid-agent `ci.yml` with `{"ref":"cand/29-r12"}` |

**If Hannah splits (H4):** skip A5. A6 becomes a fixes-only re-pin and the gate without item 5. Then A7.
