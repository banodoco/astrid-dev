# Release 13 — release record

The publish-time record of what Release 13 is: the frozen tuple, its claims and their evidence, and what is left before publication. The [brief](../13.md) holds intent, [run.md](run.md) the live board, [decisions.md](decisions.md) the rulings, [tests.md](tests.md) the test gate and [deferred.md](deferred.md) what R13 does not fix. This record links to them and does not repeat them. Sections follow what the [release skill](../../skills/astrid-dev-release/SKILL.md) says a release must report (there is no release-record template in `templates/release/`).

**Status: PUBLISHED 20:54 UTC Sun 15 Nov 2026.** Agent main 959da732 (merge of 9814193a), Runtime main 6855dfa8, App main d7d48cfe; served manifest release 13, sha256 29dc13cf…; see section 0. Earlier status: Earlier status: Candidate A′ was frozen at 10:40 UTC Sun 15 Nov ([decisions.md:2281](decisions.md#L2281)); evidence below runs through 11:35 UTC Sun 15 Nov ([decisions.md:2286](decisions.md#L2286)). Nothing has been published.

Convention: `PENDING: <what fills it>` marks a value not yet known. Nothing below is a result unless it cites its evidence.

## 0. Final publish tuple (Sun 15 Nov, 20:40 UTC). This section supersedes sections 1, 2, 4 and 7 where they differ.

Sections 1 to 7 below describe candidate A′ as of 11:35 UTC. After that point, the candidate went through A″ and A‴, then Hannah held the publish for the Windows fixes ([decisions.md:2432](decisions.md#L2432)). The final tuple is ([decisions.md:2502](decisions.md#L2502)):

| Component | SHA |
|---|---|
| Agent | `9814193a73f606719e81883a8be197d27dd361d4`: PR #347 head `r13/compose-aprime`, tested as `int/r13-9814193a`. It is ff9da5d8 plus a merge of the advisor's `r14/windows-install` `29ca1469` |
| App | `7297d266564997c460a051a7eeb63a9f1ae2278c`: PR #268 head `r13/app-repin-8e0006f5`. The release guard passes |
| Install manifest | sha256 `29dc13cf7c8d9e7553b4fb8a3f357199bfc80885e55775c6aea6a91e0a163483`, release 13, required |
| Runtime | `6855dfa8df65cf8ae4c002b57134d6505493c17c`. On publish, Runtime main is fast-forwarded to it from `42ae24af` |
| VibeComfy / lifecycle | `dba38f86…` / `7f0b025e…`: unchanged |

**Identity (decided).** Version 0.0.13, a full release, a REQUIRED update with the compact card ([decisions.md:2303](decisions.md#L2303), [:2308](decisions.md#L2308), [:2340](decisions.md#L2340)). Hannah's go stands, so no further confirmation is needed.

**Gate on the final tuple:**

| Check | Run | Result |
|---|---|---|
| Whole-tree mypy, ruff and cycles, run as CI does (W228; tree identical to 9814193a) | local | exit 0 |
| Hosted fast checks: mypy baseline, import cycles, ruff, collection, boundary, windows-native, release wheels | CI 43757233210 | **GREEN** ([decisions.md:2532](decisions.md#L2532)); darwin native red as on every candidate since A″ |
| 8 unit shards vs R12, opt-in, installed wheel | CI 43757233210 | PENDING |
| Integration lanes | Lanes 43757233283 | PENDING |
| W227 POSIX equivalence of `_program_name` | local fuzz over 82,740 lists | PASS: 0 widened, 0 narrowed |
| Windows fresh-user install, long paths ON and OFF, with real generation | 43756890273 on 29ca1469 | **GREEN** ([decisions.md:2522](decisions.md#L2522)) |
| 14-row journey, including direct-windows-r12-update | 43757304537 | PENDING. The gate row direct-windows-r12-update is **GREEN** ([decisions.md:2536](decisions.md#L2536)) |
| linux-fresh capture rows | 43757315244, 43757326484 | PENDING |
| App checks by name (W218) | App 7297d266 | PENDING |

A macos-fresh uninstall failure that matches W224's shutdown-race signature gets one rerun. That race is present in R12's Runtime and is filed as astrid-dev #685. Any other red result blocks the publish.

**Publish order:**
1. Merge Agent PR #347.
2. Fast-forward Runtime main `42ae24af` to `6855dfa8`.
3. Merge App PR #268.
4. Wait for the deploy and confirm that `https://astrid.haus/install-manifest.json` serves release 13 with these SHAs.
5. Fast-forward the `int/*` branches.
6. Tell Hannah, with the release notes.

**Known limits added since section 6:**
- **Windows:**
  - Generation with your own ComfyUI works with long paths OFF (short VibeComfy runtime root).
  - The managed engine is not offered on Windows.
- **The macOS update and uninstall shutdown race** is rare and retryable, with no data lost (#685).
- **Managed-local refuses templates without fingerprints.** The fix is ml131, the first item for 13.1.
- **Coverage gaps:** no CI job generates against a real ComfyUI. macOS own-ComfyUI and Windows RunPod have had no real runs.
- **Follow-ups:** astrid-dev #669–#685.

## 1. Release identity

| Field | Value |
|---|---|
| Release number | 13 (served Release 12 + 1; `release-guard` requires exactly +1) |
| Version | **PENDING: owner decision.** The open question: is the version `0.0.13`? That is the default if R13 follows Releases 10 to 12, which are `0.0.N` (as recorded in the earlier draft of this record), but no rule in the release skill sets it and R13 is a full release, so Hannah confirms or names another. The install manifest has no version field, so where the version is stated is also to be confirmed |
| Kind | **PENDING: owner decision**, full or patch. The brief's [Publication](../13.md#publication) section is still "Not pinned" |
| Required update | **PENDING: owner decision** (whether R13 raises the `required` floor) |
| Built on | Published Release 12: Agent `0e1543e0da2215db9cb3320cfd1083174c3c62a9`, Runtime `42ae24aff8d2cb854f874ce134161077a3ba3641`, VibeComfy `e65f4941d09b1cb4d1dd5aae6171c73e648706f4`, lifecycle `f2948817eeb94af8dee76be21f6d673724f1606e` (astrid-app `public/install-manifest.json`, `release: 12`, read 13 Nov). R12 Agent `0e1543e0` is an ancestor of A′ |
| Cutoff | Hannah: 13:00 UTC Sun 15 Nov, "assuming nothing critical is broken" ([decisions.md:2146](decisions.md#L2146)); "ship asap, anything lagging into next" ([decisions.md:2269](decisions.md#L2269)) |
| Publication authority | **NOT GIVEN** (section 8) |

## 2. Exact candidate identity and tuple

**Candidate A′:** Agent `int/r13-f709407c` = `f709407cb10cc56bafebae51080832386bca3a44` on branch `r13/compose-aprime` (`r13/compose` untouched). It is candidate A `a91c35dfd63f8d5969714541a30afe25feb2d626` + merge of `r13/revert-h3first2` `8d88fc7ec` (merge commit `9a8a3b634`) + merge of `r13/machines-prepstop` `16dbe5b41` (merge commit `f709407cb`) ([decisions.md:2270](decisions.md#L2270), [:2281](decisions.md#L2281)). Verified in `/home/user/wt/c-aprime`: HEAD and both parents match, the worktree is clean, and the A→A′ diff touches only the h3 pack, `astrid/sdk/generation.py`, `managed_preparation.py` and tests; no pin file changes.

| Component | Repository | SHA | Source (verified at `f709407cb`) |
|---|---|---|---|
| Agent | banodoco/astrid-agent | `f709407cb10cc56bafebae51080832386bca3a44` | `int/r13-f709407c`, `origin/r13/compose-aprime` |
| Runtime | banodoco/astrid-runtime | `6855dfa8df65cf8ae4c002b57134d6505493c17c` | `runtime.lock.json` and `astrid/resources/runtime.lock.json` `source_commit`. Changed from R12 `42ae24aff` |
| VibeComfy | banodoco/VibeComfy | `dba38f8644c46f652376f2cd5112ea161e40f09b` | `astrid/packs/runpod/pins.json` and `astrid/packs/vibecomfy/pins.json` (vc-11 security pin, [decisions.md:1888](decisions.md#L1888)) |
| runpod-lifecycle | banodoco/runpod-lifecycle | `7f0b025e9391baac9f5c2fb7393617ea6fef0704`, version `0.3.1.dev0` | `astrid/packs/runpod/pins.json` |
| App | banodoco/astrid-app | PENDING: the re-pin commit on `main` ([app-repin-checklist.md](app-repin-checklist.md)) | |
| Install manifest | astrid-app `public/install-manifest.json` | PENDING: `schema_digest` (computed by `pin.mjs`) and manifest sha256 | |

The same Runtime, VibeComfy and lifecycle SHAs were in the Windows tester manifest ([decisions.md:2092](decisions.md#L2092), [:2169](decisions.md#L2169)). The manifest's `vibecomfy` and `lifecycle` blocks are generated by `pin.mjs` from `pins.json`, not typed by hand.

Included plans: Plan 32, Plan 40, Plan 20 (phase 4 included), Plan 34 ([brief](../13.md#included-plans)). Included pull requests: [evidence/open-prs.md](evidence/open-prs.md).

## 3. Claims and evidence

| # | Claim | Evidence | Qualification |
|---|---|---|---|
| C1 | All five generation types work on RunPod: image (t2i, edit), audio (tts, sfx, music) and h3 video (v2v, video-edit, i2v) | A's final live round: t2i ×3, edit, tts, sfx, music, h3 v2v, h3 video-edit and the claim-2 t2i passed ([decisions.md:2254](decisions.md#L2254)); outputs checked by eye and ear ([decisions.md:2239](decisions.md#L2239)). A′ recheck 5/5 PASS: h3 i2v, t2i straight after it, bike i2v (3 s), h3 video-edit, t2i; decoded streams MD5-identical to the earlier reference-route runs ([decisions.md:2286](decisions.md#L2286)) | edit, tts, sfx and music ran on A only. A′ differs from A in the h3 pack and `managed_preparation.py` (prepstop), so their A′ result rests on that small delta, not a rerun. The sfx input clip is all black, so sync is not exercised ([decisions.md:2239](decisions.md#L2239)) |
| C2 | The W142 release false-success is fixed: `machines release <stale-id>` no longer returns ok while the pod is live | `r13/machines-rel` `dcc99a752` merged into A; the release test passes 2/2 with the fix and fails 2/2 without it on a quiet box; Astra W148 APPROVE ([decisions.md:2206](decisions.md#L2206), [:2226](decisions.md#L2226)); Lanes on A: release binding[True] fixed ([decisions.md:2285](decisions.md#L2285)) | Deferred notes: [deferred.md](deferred.md#w148-notes-on-the-release-fix-deferred-cause-r13machines-rel-dcc99a752) |
| C3 | Prepstop: a failed preparation no longer kills a warm engine; a reused engine stays up and only the job fails | Cause and fix ([decisions.md:2243](decisions.md#L2243)); Astra W166 APPROVE ([decisions.md:2278](decisions.md#L2278)); two paired runs, 0 candidate-only failures ([decisions.md:2284](decisions.md#L2284)); live, t2i after h3 i2v passed on A′ ([decisions.md:2286](decisions.md#L2286)) | Thin proof: no test or live job runs a second full job after a real preparation failure ([deferred.md:238](deferred.md#L238)); W166's limits ([decisions.md:2278](decisions.md#L2278)) |
| C4 | h3 masked edits (temporal, start-frame, regional, strength) are admitted and documented | Dry runs ([decisions.md:2098](decisions.md#L2098), [evidence/h3dry/](evidence/h3dry/)); live T1–T5b masking round, all pipeline checks pass, on `a921b7dce` (an ancestor of A′) ([decisions.md:2124](decisions.md#L2124), [evidence/live/h3m/](evidence/live/h3m/)); worked examples and an admission test merged (`521e12dfc`, [decisions.md:2143](decisions.md#L2143)); h3 video-edit passed on A and A′ | The live masking round used a synthetic clip, so prompt adherence is unmeasured; the real-clip T2–T5b cells failed on A after the poisoning and were not in A′'s recheck ([decisions.md:2241](decisions.md#L2241)). [deferred.md:240](deferred.md#L240) ("never run live") predates the 20:45 round |
| C5 | The W3 per-job full model re-hash is off by default; full verification is opt-in | Hannah's ruling ([decisions.md:2084](decisions.md#L2084)); round 5 and 5b ([decisions.md:2116](decisions.md#L2116)); merged `6a6ab6f4d` → `cb1a336ea` with 0 candidate-only failures ([decisions.md:2157](decisions.md#L2157)); live, 0 files hashed on warm jobs ([decisions.md:2148](decisions.md#L2148)); test ruling ([deferred.md:200](deferred.md#L200)) | [deferred.md:74](deferred.md#L74) still says "default: full re-verification", which predates the ruling |
| C6 | Plan 20 phase 4 (local-first onboarding) is in R13 | Hannah pulls onboarding in ([decisions.md:1899](decisions.md#L1899)); merged `ec00046f3` → `8c0d7f03f`, 0 R12-passing ids failing ([decisions.md:2142](decisions.md#L2142)); Windows install → doctor → uninstall proof green ([decisions.md:2132](decisions.md#L2132), [:2173](decisions.md#L2173)) | No tester feedback yet (section 6) |
| C7 | No CI regression against published R12 | Section 4 | A′ CI and Lanes pending |

## 4. Focused checks and results

| Check | Head | Result |
|---|---|---|
| Binding CI comparison vs R12 (CI `43693935046`, Lanes `43693934998`) | A `a91c35df` | **Clean.** 0 regressions in all 8 unit shards; fast checks, boundary, release wheels, Windows native/installer PASS; darwin = R12; Lanes 0 regressions, one R12-old intermittent; one load-sensitive LTX catalog timeout deferred ([tests.md](tests.md#current-state-sat-14-nov-1200-utc-supersedes-the-older-comparison-below), [decisions.md:2285](decisions.md#L2285), [evidence/tests/agent/a91c35df/](evidence/tests/agent/a91c35df/), [deferred.md:170](deferred.md#L170)) |
| CI delta (CI `43705081374`) and Lanes delta (`43705081352`) | A′ `f709407c` | **PENDING** (units ~12:15, Lanes ~13:40 UTC, [decisions.md:2285](decisions.md#L2285)) |
| Revert proof W164 | `8d88fc7ec` | Faithful, 0 regressions ([decisions.md:2284](decisions.md#L2284)) |
| Prepstop proof W165 | `16dbe5b41` | 0 candidate-only failures in two paired runs ([decisions.md:2284](decisions.md#L2284)) |
| Final live round, 18 cells | A | 10/18 PASS; h3 i2v failed in preparation and poisoned the machine, so 8 later cells failed fast ([decisions.md:2241](decisions.md#L2241), [:2254](decisions.md#L2254), [evidence/live/final-A/](evidence/live/final-A/)) |
| Live recheck, 5 cells (`roundA2.sh`) | A′ | **5/5 PASS**, pod released, balance $77.64 ([decisions.md:2286](decisions.md#L2286)) |
| Windows install/uninstall CI proof | tester head `9acb55b6` | Green, run `43664846375` ([decisions.md:2173](decisions.md#L2173)) |
| App Tests, Direct Journey, `journey.yml` matrix, `release-guard`, `pin.mjs --check`, `vendor-lock` checks | App re-pin | PENDING: run on the App re-pin commit |

## 5. Review result

| Review | Range | Result |
|---|---|---|
| Astra W166 | prepstop `16dbe5b41` | APPROVE, with notes for R14 ([decisions.md:2278](decisions.md#L2278)) |
| W164 (test manager) | revert `8d88fc7ec` | Revert faithful, 0 regressions ([decisions.md:2284](decisions.md#L2284)) |
| Astra W148 | W142 fix `dcc99a752` | APPROVE ([decisions.md:2226](decisions.md#L2226)) |
| Merge review of the whole range `0e1543e0..f709407c`; redaction and log bundle (G3); pins and installer (G4) | | PENDING: no review file in [evidence/reviews/](evidence/reviews/) |

## 6. Unqualified claims and known limits

These go in the release notes ([run.md](run.md)).

- **P6 (engine snapshot on the volume) is not effective.** It is wired and on by default, but showed no live saving and its outcome is never recorded ([decisions.md:2254](decisions.md#L2254), [:2264](decisions.md#L2264)).
- **First-frame i2v is reverted.** Single-image h3 i2v uses the reference route as in R12; h3first2 moves to plan 54 ([decisions.md:2244](decisions.md#L2244), [deferred.md:169](deferred.md#L169)).
- **seed_used appears only in synchronous `generate --json`**, not in `tasks show` or a durable receipt. Seeding itself works ([decisions.md:2242](decisions.md#L2242), [deferred.md:166](deferred.md#L166)).
- **RunPod warm overhead is ~215 s per t2i** on A ([decisions.md:2279](decisions.md#L2279)). Speed work moves to R14, local-first; RunPod speed is out of its scope ([decisions.md:2282](decisions.md#L2282), astrid-dev#662).
- **Attached cancel uses ComfyUI's global `/interrupt`**, so it can stop another client's job ([deferred.md:237](deferred.md#L237)).
- **A′'s Lanes delta is pending at the time of the go**; the test manager says so plainly if it has not finished ([decisions.md:2278](decisions.md#L2278)).
- **No Windows tester feedback yet** (0 comments, [run.md](run.md)). The Windows CI install/uninstall proof is green ([decisions.md:2173](decisions.md#L2173)).
- Also unqualified: prepstop's second-job path (C3); h3 mask prompt adherence on a real clip (C4); edit, tts, sfx and music not rerun on A′ (C1).

## 7. Remaining authorized actions

**Publication needs Hannah's go, in the publishing session, naming the exact SHAs** (Agent `f709407cb10cc56bafebae51080832386bca3a44`, Runtime `6855dfa8df65cf8ae4c002b57134d6505493c17c`, VibeComfy `dba38f8644c46f652376f2cd5112ea161e40f09b`, lifecycle `7f0b025e9391baac9f5c2fb7393617ea6fef0704`, plus the App re-pin SHA). Not given as of 11:35 UTC. Her publish condition ([decisions.md:2269](decisions.md#L2269)): A's binding table clean (done), revert and prepstop proofs clean (done), A′ hosted fast checks and unit shards green (PENDING), A′ live recheck (done). Before the go she also sets version, kind and required update (section 1).

After the go, only the one publishing session acts, in the skill's order: confirm the served manifest is still release 12; merge Agent, then Runtime `6855dfa8` (changed from R12), then the App with the manifest; wait for the production deploy and the served-manifest canary; confirm `https://astrid.haus/install-manifest.json` serves release 13 with these SHAs; fast-forward each `int/<project>` (never forced); close the project through Manage; owner check on a real long-lived install; close included PRs. Each step is logged here with its run id.

After publish: R14 local-first speed ([decisions.md:2282](decisions.md#L2282)); the paused R13.1 RunPod cards ([decisions.md:2269](decisions.md#L2269)); the [deferred register](deferred.md).
