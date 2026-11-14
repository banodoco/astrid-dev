# Release 13 — App re-pin checklist

How to re-pin astrid-app to the Release 13 Agent and Runtime tuple. **Nothing here has been run.** This draft was written from astrid-app `main` at `237b28be935af49c23464fa6ca1cf30db67ebaa0` (read-only, through the GitHub tools, 13 Nov 2026), from the [release skill](../../skills/astrid-dev-release/SKILL.md) and from the Release 12 record ([plan 29 handoff](../../plans/29-update-and-release/handoff.md), section 3 step 5, and [releases/12/decisions.md](../12/decisions.md)). `releases/12` has no release record of its own, only decisions, so those are the sources for the previous re-pin. Where a path or command could not be confirmed from the App's files it is marked VERIFY.

Placeholders: `<AGENT>` is the frozen Agent SHA, `<RUNTIME>` is the Runtime SHA that the Agent's `runtime.lock.json` names (expected to stay `42ae24aff8d2cb854f874ce134161077a3ba3641`), `<APP_BASE>` is astrid-app `main` as served.

## Who runs it, and when

- Lane: skill lane 3, the Agent/Runtime installer tuple. It does not authorize a deployment, tag or publication.
- When: After the freeze, because the pin names the frozen Agent SHA ([run.md](run.md)).
- Who: the release manager, or a worker it briefs. The branch push and the later merge are write actions on astrid-app: ORCHESTRATOR ONLY (a push needs the destination named, and the merge to `main` needs the owner's go in the publishing session).
- No GPU or RunPod is needed for any step here.

## 0. Preconditions (stop if any is false)

1. The Agent head `<AGENT>` is frozen, its CI comparison against R12 is clean, and the SHA is on GitHub (the pin tools read it from `raw.githubusercontent.com`, so it must be pushed).
2. Look at the Agent's `runtime.lock.json`: `source_commit` must be a full 40-character SHA, and the Runtime at that SHA must have `contract/manifest.json`. Expected `<RUNTIME>` is `42ae24aff...` (G5: no Runtime change in R13). If it differs, the Runtime moved: do step 6 as well, and the release record needs the Runtime review.
3. The Agent's `astrid/packs/runpod/pins.json` has full 40-character `sources.vibecomfy.revision` and `sources.lifecycle.revision`, plus `repository` and `version` for lifecycle (pin.mjs refuses otherwise). Verify VibeComfy `d3850831265c54bb811808c2bc85c53ef5ac7ec9` and the lifecycle candidate `7f0b025e9391baac9f5c2fb7393617ea6fef0704` against the frozen head; PENDING: final lifecycle version and confirmation ([decisions.md:1737](decisions.md#L1737), [decisions.md:1322](decisions.md#L1322), [offline evidence:58](evidence/cells/foleybind-bug-evidence-pack.md#L58)).
4. Nobody else is mid-publish and the served release is still 12: `curl -s https://astrid.haus/install-manifest.json` shows `"release": 12`, agent `0e1543e0da2215db9cb3320cfd1083174c3c62a9`. If not, re-base on the served tuple and renumber (skill: one publisher at a time).
5. Work on a branch of astrid-app cut from `<APP_BASE>`, for example `r13/app-repin`. Never commit to `main`. Never force-push.

VibeComfy candidate chain: cells-vc-6 `46251c8c`, -7 `ae7dd067`, -8 `8d64b083`, -9 `f3e95d1c`, -10 `d3850831`. The vc10 pin includes the LTX i2v LoRA and text-encoder digests and FLF model identities from unauthenticated Hugging Face HEAD reads; the earlier i2v checkpoint metadata is in [vc7-ltx-metadata.txt](evidence/cells/vc7-ltx-metadata.txt). Verify the final pinned template revisions, digests and sizes, rather than copying individual model digests into the App manifest ([decisions.md:1737](decisions.md#L1737)). PENDING: verify the chain at freeze; the cells-log ref is unavailable locally.

## 1. Files that change

| File | Changed by | Why |
|---|---|---|
| `public/install-manifest.json` | `node scripts/installer/pin.mjs <AGENT>` for `agent.sha`, `runtime.sha`, `runtime.schema_digest`, `vibecomfy`, `lifecycle`; **`release` by hand** | The installed tuple. `pin.mjs` never writes `release` |
| `runtime.lock.json` (repo root) | `node scripts/vendor-lock.mjs update runtime.lock.json --producer <runtime checkout>`, only if `<RUNTIME>` differs from the current `source_commit` | The vendored Runtime client and schema; `release-guard --pins` requires `manifest.runtime.sha` to equal its `source_commit` |
| `config/astrid-cli-surface/vendor.lock.json` and `config/astrid-cli-surface/cli-surface.json` | `node scripts/vendor-lock.mjs update config/astrid-cli-surface/vendor.lock.json --producer <agent checkout>` | The App's copy of the Agent CLI surface. Rule from the R12 handoff: **every Agent re-pin regenerates the vendor lock in the same commit** |
| `public/install`, `public/install.sh`, `public/install.ps1` | Not touched unless the bootstrap is meant to change. These are part of the tuple: any change needs the same release +1 | Bootstraps are served byte for byte |
| `src/integrations/runtime/**`, `vendor/timeline-schema/**` | Only as a side effect of the Runtime `vendor-lock.mjs update` | Generated from the Runtime |

Do not edit these by hand: the tools check hashes and a hand edit shows as "edited locally".

## 2. Steps

All commands run from the astrid-app checkout root, Node 20.19.x (`.nvmrc`).

1. **Branch.** `git switch -c r13/app-repin <APP_BASE>`; confirm `git status` is clean.
2. **Pin the Agent and everything it names.**
   `node scripts/installer/pin.mjs <AGENT>`
   This reads `runtime.lock.json` and `astrid/packs/runpod/pins.json` at `<AGENT>` and the Runtime contract at `<RUNTIME>`, and rewrites `agent.sha`, `runtime.sha`, `runtime.schema_digest`, `vibecomfy` and `lifecycle` in `public/install-manifest.json`. It needs network access to `raw.githubusercontent.com`.
3. **Bump `release` by exactly 1** in `public/install-manifest.json`: `12` to `13` (the manifest read on 13 Nov says `release: 12`; if the served release moved, use served + 1). Do this by editing the one number.
4. **Update the floor only if the owner decided on a required update.** Bump `release` first, then:
   `node scripts/installer/pin.mjs <AGENT> --require "<reason>"`
   (`--require` sets `required.release` to the manifest's own release; the guard refuses a floor set before the bump). Skip this step if no required update was decided. The proposed floor of 13 was ruled moot ([decisions.md:1766](decisions.md#L1766)); PENDING: confirm the final manifest floor at freeze.
5. **Re-vendor the Agent CLI surface.** Check out the Agent at exactly `<AGENT>` (a clone you already have is fine; it must be at HEAD `<AGENT>` and clean, the tool refuses otherwise):
   1. Edit `config/astrid-cli-surface/vendor.lock.json` so `source_commit` is `<AGENT>`.
   2. `node scripts/vendor-lock.mjs update config/astrid-cli-surface/vendor.lock.json --producer <path to agent checkout>`
   This copies verified bytes, regenerates `cli-surface.json`, the `producer_version` and the file hashes.
6. **Re-vendor the Runtime, only if the Runtime moved** (same procedure): set `source_commit` in `runtime.lock.json` to `<RUNTIME>`, check the Runtime out at it, and run `node scripts/vendor-lock.mjs update runtime.lock.json --producer <path to runtime checkout>`. If the Runtime did not move, skip, and the check in step 7 proves it.
7. **Run the checks, in this order, before any push** (the R12 order, plus the CI ones):

   | Check | Command | Proves |
   |---|---|---|
   | Manifest coherence | `node scripts/installer/pin.mjs --check` | `runtime.sha` equals the Agent's lock; `vibecomfy` and `lifecycle` equal the Agent's `pins.json`; `schema_digest` equals the Runtime contract digest; no `runpod` block |
   | Agent vendor lock | `node scripts/vendor-lock.mjs check config/astrid-cli-surface/vendor.lock.json --producer <agent checkout>` | Vendored CLI surface matches the pinned Agent bytes |
   | Runtime vendor lock | `node scripts/vendor-lock.mjs check runtime.lock.json --producer <runtime checkout>` | Vendored Runtime files match the pinned Runtime |
   | Release guard with pins | `node scripts/installer/release-guard.mjs <APP_BASE> HEAD --pins` | Tuple changed, release is exactly base + 1; App lock agrees with the manifest; pin coherence again |
   | Installer unit tests | `node --test scripts/installer/release.test.mjs` | The guard and pin logic |
   | CLI surface test | `cliSurfaceVerbs.test.ts` through vitest (VERIFY the file path with `git grep -l cliSurfaceVerbs`; run only that file, not the full suite) | The vendored CLI verbs are consistent. This is where a new machines/generate verb would fail |
   | Types | `npx tsc -p tsconfig.app.json --noEmit` (VERIFY the project that `npm run` uses; the R12 re-pin ran `tsc`) | Regenerated TypeScript compiles |

   Do not run the full App suite locally; that runs on CI.
8. **One commit.** The R12 rule: the manifest pin, the release bump and both lock regenerations are **one** App commit, so a single SHA names the tuple. Commit message names `<AGENT>`, `<RUNTIME>`, the release number and the trailers the session requires.
9. **Push the branch (ORCHESTRATOR ONLY)** to astrid-app as `r13/app-repin` (or the `int/**` branch the manager names). CI that runs on push: `Tests` (`release-guard`, `vitest`, `boundary`, which re-checks both vendor locks against the pinned producers), `Direct Journey` and `three-products` (they read the Agent and Runtime from the manifest). Open a PR into `main` only when the manager says so: the release-guard job also runs on pull requests.
10. **Qualifying round on that one commit** (CI, no paid steps): App Tests, Direct Journey, App lanes (`lanes.yml`) and the 11-row `journey.yml` matrix, whose App candidate is this commit. The run ids go into [release-record.md](release-record.md) claims 3 to 8. The matrix dispatch is in [update-proof-row.md](update-proof-row.md). Any new App commit after this point invalidates these runs for the exact-head claims; redo them.

## 3. What happens at publish (not part of the re-pin)

Done only by the publishing session, with the owner's go naming the SHAs: merge Agent, then Runtime (no-op if unchanged), then App; the App merge triggers the production deployment (`Reigh / production`); the `Served manifest canary` runs only after that deployment succeeds, and runs `node scripts/installer/served-manifest.mjs <deployed-sha>`, which compares the served `agent.sha`, `runtime.sha`, `runtime.schema_digest` and `release` and the three bootstrap files with the deployed commit. A canary seen before the deployment shows as skipped. Then confirm `https://astrid.haus/install-manifest.json` serves release 13 and the exact SHAs. Running the canary script by hand is read-only and safe: `node scripts/installer/served-manifest.mjs <deployed-sha>`.

## 4. Known traps

- `release` forgotten: the guard fails with "install tuple changed ... requires release 13".
- `release` bumped with no tuple change: the guard fails the other way. The tuple includes the three bootstrap files.
- `--require` before the bump: refused.
- Agent re-pinned without regenerating `config/astrid-cli-surface`: the `boundary` job and `cliSurfaceVerbs.test.ts` fail. R12 had this twice.
- Agent SHA not pushed yet, or a short SHA: `pin.mjs` reads a 40-character SHA from GitHub and fails with HTTP 404.
- The manifest copies the frozen Agent pins: verify lifecycle and VibeComfy at `<AGENT>` before accepting the generated manifest.
- Stale App `main`: if another project published in the meantime, the base moves; re-base and renumber, never race.
- `Direct Journey` and `Tests` read the pins from the manifest; there is no separate place to set the Agent SHA for them.
- Nothing in astrid-app was changed to produce this checklist.
