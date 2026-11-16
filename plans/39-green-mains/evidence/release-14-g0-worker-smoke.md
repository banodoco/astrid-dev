# Release 14 G0 — worker smoke and coordinated submissions

16 November 2026. This records the canonical scripts and coordinated product
submissions for [G0](../tasks.md), under the
[Release 14 scope](../plan.md#release-14-scope). Implementation and local G0
acceptance and coordinated integration are complete in all three repositories.
All three PRs merged into `release/14/plan-39` on 16 November 2026; G0 is
complete. The merge receipts and current CI result are recorded below.

## Source and scope

- Base: `2770aa79e8d9325c7891294609c746963cc4776e`.
- Implementation: `5fb12b7908d0a0e771e989f9f1f1d51b993788df`, tree
  `71fc701d644a55480b65b80c3065cc36fd840855`.
- The original assignment authorized astrid-dev `p39/g0` only. The owner later
  explicitly authorized the coordinated Runtime/App submissions, then the three
  plan-branch merges after independent verification and record repair. Task
  branches were `p39/g0`; integration is into `release/14/plan-39` only.
  Neither `release/14/main` nor public `main` was promoted.
- Initial local validation: Linux, Python 3.13.5; fresh detached checkouts with
  only the proposed worker scripts copied into `scripts/worker-env/`. Runtime
  setup puts the Python venv, fetched Agent and Node 22 beside the checkout in
  `<checkout>.env/`, but `npm ci --prefix <checkout>/packages/typescript` writes
  `node_modules` **inside** the checkout at `packages/typescript/node_modules/`.
  That ignored dependency directory is setup output; the checkout is not wholly
  untouched. App setup likewise writes its ignored root `node_modules/`.
- Runtime validation base: `2537fed24385ec1c24f48a812e09af4bb63fb794`, the inspected
  `release/14/main` and `release/14/plan-39` head. Its Agent pin is
  `b05ac03a5bcab278bccf99d85b49f4037b5dec10`.
- App validation base: `0b6ef16152dc3fa11246ccc2007da630c66d1a1a`, the inspected
  `release/14/main` and `release/14/plan-39` head. Its manifest pins Agent
  `9814193a73f606719e81883a8be197d27dd361d4` and Runtime
  `6855dfa8df65cf8ae4c002b57134d6505493c17c`.
- Product tests, lockfiles and source are unchanged. The negative pin case used
  a separate throwaway Runtime worktree. No Plan 55 or Plan 38 test was edited.

The evidence-only follow-up carries the implementation proof forward: the four
script blobs below are unchanged. No full product CI or integrated release qualification
is claimed.

Git CLI push could not authenticate in this session. Publication uses the
connected GitHub API with a lease on the assigned astrid-dev branch's base; the uploaded
implementation tree is exactly the locally tested tree above. No source bytes
changed for that transport fallback.

## Reused work and changes

Plan 38 W0 was already merged in astrid-dev
[PR #210](https://github.com/banodoco/astrid-dev/pull/210), merge commit
`3e6dffdffc93c91c267b6496b9e900e77d01c862`. Runtime `int/38` contains its copies at
`74a1be1eb290bdb32541c0a238a2fc51d35401e1`; those original three script blobs
match the assigned astrid-dev base. That Runtime work was not yet merged into
the inspected Release 14 head. Neither inspected product release head has a
`scripts/worker-env/` directory. Plan 31 RL-0's App setup was absent.

- `runtime-setup.sh` retains W0's venv, dependency installs and exact Agent
  fetch. It adds an environment-local Node 22 via `npm install ... node@22` and
  `npm ci --include=dev` from `packages/typescript/package-lock.json`. Its exact
  local Node and compiler must run before it writes the setup receipt.
- `runtime-pytest.sh` exposes that Node and compiler on its cleared `PATH` and
  points `ASTRID_CHECKOUT` at the verified Agent. The old value was the Runtime
  directory, contrary to `tests/astrid_checkout.py`'s contract.
- `app-setup.sh` requires the first Node on `PATH` to be 20.19.x and runs
  `npm ci --legacy-peer-deps`, including the existing postinstall script.
- `smoke.sh app <file>` runs setup followed by `node --test <file>`.
  Agent/VC dispatch and failure handling remain the same. The README describes
  the prerequisites, commands and existing smoke exit convention.

## Focused proof

| Check | Observed result |
| --- | --- |
| Frozen base `smoke.sh runtime tests/test_platform.py` | PASS, exit 0; 70 passed, 1 existing Windows-only skip, 2 deselected; `ENV-PASS` |
| Candidate `bash scripts/worker-env/smoke.sh runtime tests/test_platform.py` | PASS, exit 0; same counts; `ENV-PASS` |
| Runtime smoke with a 40-character all-zero Agent pin | Expected refusal, exit 3; git reports `not our ref`; pytest is not reached |
| `tsc --version` and `node --version` from inside `runtime-pytest.sh` | PASS; Node `v22.23.5`, TypeScript `Version 5.9.3`, matching the Runtime lockfile; both executable paths are local to the prepared environment/checkout |
| Agent checkout from inside `runtime-pytest.sh` | PASS; `ASTRID_CHECKOUT` is the fetched Agent and its HEAD equals the pin |
| `bash scripts/worker-env/smoke.sh app scripts/installer/manifest.test.mjs`, Node 20.19.4/npm 10.8.2, with workspace proxy configured as below | PASS, exit 0; 4 tests passed, none skipped; `ENV-PASS` |
| Same App smoke with the workspace's Node 24.22.1 first on `PATH` | Expected refusal, exit 3, before npm or tests |
| Five `cmp` checks against the proposed local Runtime/App copies | PASS; every comparison silent, exit 0 |
| Agent/VC setup and pytest scripts versus the base | Byte-identical |
| Agent/VC smoke dispatch versus the base, using stub sibling commands | 8 comparisons passed: success, setup failure, test failure, and selector containing spaces, for each mode; same arguments, output and exit status |
| Real Agent setup and smoke on `ab95803ce28fa51eec937b4074f5ec0f0439b98a` | PASS, exit 0; one existing installer tool-probe test passed; `ENV-PASS` |
| Real VibeComfy setup and smoke on `dba38f8644c46f652376f2cd5112ea161e40f09b` | PASS, exit 0; `tests/test_scope.py`: 13 passed, no failures/errors/skips; `ENV-PASS` |
| Isolated failure probes using stubs | App npm exit 41 and Runtime compiler-version exit 42 each produce setup exit 3 |
| `bash -n env/runtime-setup.sh env/runtime-pytest.sh env/app-setup.sh env/smoke.sh` and `git diff --check` | PASS |

Runtime output:

```text
python=3.13.5
agent=b05ac03a5bcab278bccf99d85b49f4037b5dec10
node=v22.23.5
tsc=Version 5.9.3
70 passed, 1 skipped, 2 deselected in 1.39s
ENV-PASS runtime tests/test_platform.py
smoke_exit=0
```

The skip is the existing `test_windows_current_user_and_get_process_times_identity`
declaration. The deselections come from the unchanged Runtime pytest configuration;
no additional selector filter, skip or deselect was supplied.

Runtime environment probe command, with two temporary checks outside the product
repository that invoke the real tools and verify the actual checkout:

```bash
bash scripts/worker-env/runtime-pytest.sh -q -s \
  /workspace/scratch/0f74e42cf9ba/g0-validation/test_runtime_environment.py
```

```text
node --version: v22.23.5; tsc --version: Version 5.9.3; lockfile: 5.9.3
ASTRID_CHECKOUT: /workspace/scratch/0f74e42cf9ba/astrid-runtime.env/agent; Agent SHA: b05ac03a5bcab278bccf99d85b49f4037b5dec10
2 passed in 0.21s
```

App output:

```text
# tests 4
# suites 0
# pass 4
# fail 0
# cancelled 0
# skipped 0
# todo 0
ENV-PASS app scripts/installer/manifest.test.mjs
smoke_exit=0
```

## Environment repair and incomplete validation

The first App attempt installed dependencies successfully, then reported 2 passed
and 2 failed with `fetch failed`. A direct Node probe identified
`EAI_AGAIN: getaddrinfo EAI_AGAIN raw.githubusercontent.com`; curl through the
workspace's configured proxy returned HTTP 200. Node 20's fetch needed that same
proxy. The successful run used `undici` 6's `EnvHttpProxyAgent` in a temporary
preload, without stubbing responses or changing any product/test file:

```javascript
const { EnvHttpProxyAgent, setGlobalDispatcher } = require('./node20-proxy/node_modules/undici');
setGlobalDispatcher(new EnvHttpProxyAgent());
```

Node 20.19.x was prepared explicitly before App setup: the available bootstrap
npm installed the npm-distributed `node@20.19.4` and `npm@10.8.2` into the
validation-only prefix `/workspace/scratch/0f74e42cf9ba/g0-validation/app-node`,
outside the product checkout. Its `node_modules/.bin` was prepended to `PATH`.
The installed package manifests and executable versions confirm Node 20.19.4
and npm 10.8.2. `app-setup.sh` does not obtain or switch Node; it validates the
first executable on the caller's `PATH` and refuses a different version.

The exact rerun from the App checkout was:

```bash
PATH="/workspace/scratch/0f74e42cf9ba/g0-validation/app-node/node_modules/.bin:$PATH" \
NODE_OPTIONS="--require /workspace/scratch/0f74e42cf9ba/g0-validation/node20-proxy.cjs ${NODE_OPTIONS:-}" \
bash scripts/worker-env/smoke.sh app scripts/installer/manifest.test.mjs
```

The preload and its dependency are validation-only environment preparation, not
part of the canonical scripts or product copy requirements. Workers behind a
proxy need a working Node 20 fetch configuration. Dependency installation also
prints existing Supabase engine warnings (`>=22.0.0` while G0 requires 20.19.x);
the required four manifest checks pass. No dependency or engine policy changed.

An initial Runtime baseline attempt was discarded after an edit to the live
smoke script interrupted Bash's read of it (syntax error, exit 2). The baseline
was then exported from the immutable base commit to a separate directory and
rerun successfully. No product failure was inferred from the discarded attempt.

Before the separate plan-branch metadata fix, `python3 scripts/astrid_dev.py
check` exited 1 on both the untouched assigned base and the original G0
candidate, with byte-identical diagnostics:

```text
ERROR release-documents: releases/14.md: Branches row astrid-agent `release/14/plan-39`: duplicate repository and branch
ERROR release-documents: releases/14.md: Branches row astrid-runtime `release/14/plan-39`: duplicate repository and branch
ERROR release-documents: releases/14.md: Branches row astrid-app `release/14/plan-39`: duplicate repository and branch
ERROR release-documents: releases/14.md: Branches row astrid-dev `release/14/plan-39`: duplicate repository and branch
```

Those Release 14 document entries were outside G0. They were subsequently
fixed on the plan branch in `013e60390882ab9e697009f64bff2210a36391a1`; the
updated G0 branch incorporates that commit by merge. The historical failure
above is preserved, not represented as the current documentation result. The
follow-up below supplies real focused Agent and VibeComfy smoke runs as well.
No full product suite was run locally. No hosted worker-smoke or native
macOS/Windows worker-smoke proof is claimed.

## Follow-up: remaining smoke checks and review submission

After the owner's request to keep going, the real Agent and VibeComfy setups
were run against fresh source checkouts using the canonical scripts from
`f652b7361f80f43b1b14c5cb20b7aa722b59841c`. Both checkouts remained clean.

Agent source: `ab95803ce28fa51eec937b4074f5ec0f0439b98a`, the inspected
`release/14/main` head. The existing tool-probe selector exercises no provider
credentials or live services and is outside the excluded Plan 55/38 tests.

```bash
bash /workspace/scratch/0f74e42cf9ba/g0-validation/dev-followup/env/smoke.sh agent \
  tests/test_installer_platforms.py::test_ffmpeg_probe_checks_every_required_encoder_and_analysis_filter
```

```text
python=3.13.5
runtime=6855dfa8df65cf8ae4c002b57134d6505493c17c
vibecomfy=dba38f8644c46f652376f2cd5112ea161e40f09b
lifecycle=7f0b025e9391baac9f5c2fb7393617ea6fef0704
1 passed in 1.02s
ENV-PASS agent tests/test_installer_platforms.py::test_ffmpeg_probe_checks_every_required_encoder_and_analysis_filter
smoke_exit=0
```

VibeComfy source: `dba38f8644c46f652376f2cd5112ea161e40f09b`, matching the
Agent's pin. The scope-identity test file is outside the excluded test inventory.

```bash
bash /workspace/scratch/0f74e42cf9ba/g0-validation/dev-followup/env/smoke.sh vc tests/test_scope.py
```

```text
3.13.5 /workspace/scratch/0f74e42cf9ba/g0-validation/vc-smoke/vibecomfy/__init__.py
13 passed in 1.46s
ENV-PASS vc tests/test_scope.py
command exit: 0
```

[Draft PR #762](https://github.com/banodoco/astrid-dev/pull/762) targets
`release/14/plan-39` from `p39/g0`; it was unmerged at this earlier checkpoint. Its initial hosted
[Documentation integrity run](https://github.com/banodoco/astrid-dev/actions/runs/43918877531)
on `f652b7361f80f43b1b14c5cb20b7aa722b59841c` ran 417 validator tests and
failed three, all caused by the existing duplicate Release 14 branch entries:

- `test_check_docs.StrategyTests.test_real_strategy_passes`
- `test_golden.GoldenTests.test_real_tree_and_fixtures_match_golden_output`
- `test_views.ViewTests.test_legacy_vision_failure_is_the_only_error_line`

These exact three tests were rerun on both the untouched base
`2770aa79e8d9325c7891294609c746963cc4776e` and the candidate, using:

```bash
PYTHONPATH=scripts python3 -m unittest \
  test_check_docs.StrategyTests.test_real_strategy_passes \
  test_golden.GoldenTests.test_real_tree_and_fixtures_match_golden_output \
  test_views.ViewTests.test_legacy_vision_failure_is_the_only_error_line
```

Both runs exited 1 with the same three failures. Their full output is identical
after normalizing only the checkout path and elapsed time. No validator, golden
file or release record was changed to obtain a pass. This is confirmation of
pre-existing CI failures, not a green CI claim.

Authentication was also checked again: `gh auth status` reported no login and
Git had no credential helper; the connected GitHub API was authenticated as
`peteromallet` and successfully created the draft PR. That API remains the
working route for updates solely to `p39/g0`; CLI credentials do not block this
submission.

## Coordinated copies

These exact canonical blobs are now committed in the product submissions below.
Both products add the files, since the directories are absent on their unchanged
release-plan bases.

| Repository and destination | Canonical source | Git blob | Mode |
| --- | --- | --- | --- |
| Runtime `scripts/worker-env/runtime-setup.sh` | `env/runtime-setup.sh` | `b39e30fe340a804f1d23296ff8dea4ee428f3cd1` | 100644 |
| Runtime `scripts/worker-env/runtime-pytest.sh` | `env/runtime-pytest.sh` | `7ca73294e71c490a24ceba25131194292e94473a` | 100644 |
| Runtime `scripts/worker-env/smoke.sh` | `env/smoke.sh` | `1d5ac2b970b0407a8f8438c5fcdb8e4857d5b22e` | 100755 |
| App `scripts/worker-env/app-setup.sh` | `env/app-setup.sh` | `2361cfb7735fbd090d300d413e644cdb5b519d07` | 100644 |
| App `scripts/worker-env/smoke.sh` | `env/smoke.sh` | `1d5ac2b970b0407a8f8438c5fcdb8e4857d5b22e` | 100755 |

The literal smoke commands and all five `cmp` checks were repeated against
fresh checkouts of the published product commits. The old `int/38` branch was
not merged to obtain the files.

## Completed product submissions and exact-commit proof

The owner then requested the coordinated work end to end. The connected GitHub
API created only the two `p39/g0` product branches, each directly from its
previously validated `release/14/plan-39` base. Each published tree matches the
locally calculated tree, and each commit has exactly the intended base parent.
Fresh checkouts were fetched from GitHub for the following proof.

| Submission | Commit | Base | Product changes |
| --- | --- | --- | --- |
| [Runtime PR #52](https://github.com/banodoco/astrid-runtime/pull/52) | `dff3f116053d9e64e761509bfe35d77c1f6b96ad` | `2537fed24385ec1c24f48a812e09af4bb63fb794` | Three worker scripts only |
| [App PR #278](https://github.com/banodoco/astrid-app/pull/278) | `9dc7a313e90b85c0f855f20be2fd8d037436fe1c` | `0b6ef16152dc3fa11246ccc2007da630c66d1a1a` | Two worker scripts only |

At this submission checkpoint, both drafts targeted `release/14/plan-39` from `p39/g0` and linked the canonical
[astrid-dev PR #762](https://github.com/banodoco/astrid-dev/pull/762). They have
not been merged at that checkpoint. The canonical implementation and all four script blobs remain
unchanged from `d9f6abcec4bc05781adbd29529a5d421a5728f66`; this follow-up changes
only G0's task progress and evidence.

Runtime, from `/workspace/scratch/0f74e42cf9ba/g0-validation/runtime-submission`:

```text
$ bash scripts/worker-env/smoke.sh runtime tests/test_platform.py
python=3.13.5
agent=b05ac03a5bcab278bccf99d85b49f4037b5dec10
node=v22.23.5
tsc=Version 5.9.3
70 passed, 1 skipped, 2 deselected in 1.40s
ENV-PASS runtime tests/test_platform.py
smoke_exit=0
```

The same two external environment probes described above passed through this
commit's `runtime-pytest.sh` in 0.28s. They again verified the actual local Node
and compiler paths, lockfile TypeScript 5.9.3, and exact Agent checkout/pin.
Three literal canonical `cmp` checks, shell syntax and whitespace checks passed;
the checkout remained clean.

A separate throwaway worktree from `dff3f116053d9e64e761509bfe35d77c1f6b96ad`
used the same smoke command after setting only its Agent pin to 40 zeroes:

```text
fatal: remote error: upload-pack: not our ref 0000000000000000000000000000000000000000
ENV-FAIL setup (runtime)
smoke_exit=3
```

The negative case stopped before pytest. Its pin was restored and that
worktree is clean; no altered pin or test is part of any submission.

App, from `/workspace/scratch/0f74e42cf9ba/g0-validation/app-submission`, with
the same Node 20.19.4/npm 10.8.2 and external proxy preparation described above:

```text
$ bash scripts/worker-env/smoke.sh app scripts/installer/manifest.test.mjs
added 569 packages in 10s
# tests 4
# pass 4
# fail 0
# skipped 0
ENV-PASS app scripts/installer/manifest.test.mjs
command exit: 0
```

With actual Node 24.22.1 first on `PATH`, the same command again refused setup
with `ENV: expected Node 20.19.x first on PATH` and `ENV-FAIL setup (app)`, exit
3, before npm/tests. Both literal canonical `cmp` checks, shell syntax and
whitespace checks passed. The App checkout remained clean, including its
manifest and lockfile. The earlier Agent/VC smoke proof carries forward because
their source, inputs and the canonical scripts are unchanged.

### Completed hosted checks and integration review

The completed [Runtime CI run 43921815789](https://github.com/banodoco/astrid-runtime/actions/runs/43921815789)
failed five jobs. Its base comparison is
[run 43888599361](https://github.com/banodoco/astrid-runtime/actions/runs/43888599361)
at `2537fed24385ec1c24f48a812e09af4bb63fb794`. The completed jobs compare as
follows (F = failed, P = passed, S = skipped, X = xfailed, E = errors):

| Runtime job | G0 candidate | Untouched base |
| --- | --- | --- |
| unit (ubuntu-latest) | 77 F, 8440 P, 26 S, 13 X, 1010 E; 60 subtests passed | Same counts |
| sandbox-process-control | 82 F, 8355 P, 26 S, 13 X, 1014 E; 60 subtests passed | Same counts |
| portability-lifecycle (ubuntu-latest) | 7 F, 610 P, 45 S | Same counts |
| portability-lifecycle (macos-latest) | 8 F, 595 P, 59 S | Same counts |
| unit (macos-latest) | **74 F, 8339 P**, 130 S, 13 X, 1010 E; 60 subtests passed | **73 F, 8340 P**, otherwise same counts |

The one additional macOS failure is
`tests/test_p2_commit_phase_capture.py::test_live_watchdog_uses_real_handler_and_private_faulthandler_output`,
with `assert sampling["sample_total"] > 0` receiving zero samples. The
[candidate job](https://github.com/banodoco/astrid-runtime/actions/runs/43921815789/job/133490778712)
ran GitHub merge commit `d93c71648eb393a106a33de0bd7060aecddb4da2`; the
[base job](https://github.com/banodoco/astrid-runtime/actions/runs/43888599361/job/133373360363)
did not report that failure. There are no candidate-only error test IDs in
that comparison.

**Flakiness assessment: not confirmed flaky; likely scheduling-sensitive.**
The test holds a live request for a fixed 50 ms, then expects a background
sampler with a 20 ms interval to have observed it. It does not wait for a
sampling-completion signal. The test and capture helper are byte-identical
between base and G0. Two preceding stored macOS runs
([43883740374](https://github.com/banodoco/astrid-runtime/actions/runs/43883740374/job/133356183408)
and [43870457685](https://github.com/banodoco/astrid-runtime/actions/runs/43870457685/job/133309933790))
do not report this test failing either. Those observations support a timing
hypothesis, but do not establish its cause or justify claiming a proven flake.
The failure remains an explicit unresolved G1/Runtime triage item, not a
passing test or a waived assertion.

A targeted Linux diagnostic on the unchanged G0 Runtime commit passed this
one selector in 1.65s when pytest's temporary output was placed under `TMPDIR`:

```bash
bash scripts/worker-env/runtime-pytest.sh \
  --basetemp /workspace/scratch/0f74e42cf9ba/g0-validation/runtime-submission.env/tmp/watchdog-diagnostic \
  -q tests/test_p2_commit_phase_capture.py::test_live_watchdog_uses_real_handler_and_private_faulthandler_output
```

The initial diagnostic with the launcher's default sibling `basetemp` failed
an earlier helper precondition, `P2 phase sink must be a new file under TMPDIR`.
Only the diagnostic output directory was corrected; no test or source changed.
A Linux pass does not establish macOS flakiness. The required G0 platform smoke
is unaffected and remains passing.

Manager review: the G0 product changes are exactly the worker-script copies,
the current hosted CI does not call them, and no product/helper/test code in
the failing path changed. The independently verified G0 acceptance remains
valid. The extra broad-suite failure is retained for G1 triage; full Runtime
CI is explicitly red, and no release promotion is claimed by these task merges.

App's [Dockerfile Check run 43921978796](https://github.com/banodoco/astrid-app/actions/runs/43921978796)
finished successfully. App's existing Tests workflow accepts PR bases `main`
or `release/*/main`, so it did not run for this plan-branch submission. The four
required G0 manifest checks passed locally at the exact submitted commit.
Neither product's current CI invokes these new worker scripts; full-product
CI health is separate from G0's worker acceptance.

The completed astrid-dev
[Documentation integrity run 43922554303](https://github.com/banodoco/astrid-dev/actions/runs/43922554303)
passed: **417 validator tests, OK**, repository checks, refreshed-view
validation and the vision consumer contract. It tested GitHub's merge commit
`7f79ac2f5750d618b93d34cc6ad17bca5d7a9643`, combining G0 head
`3021fa07c1c887fc2137218a333417f0c39f7f20` with the separately corrected plan
base `013e60390882ab9e697009f64bff2210a36391a1`. The older runs on `f652b736`
and `d9f6abce` really did fail three of 417 tests; those are historical results
on the old metadata, not current blockers or changes made to tests by G0.

The owner independently verified G0's local proof and all five copy modes,
then authorized record corrections, manager review, marking all three PRs
ready and merging them as one coordinated batch into `release/14/plan-39`.
The owner also authorized concurrent wave-0 G1, SF3a and GL work, with manager
branch review and the existing plan review points; no outside verification is
required for every individual task. This authority supersedes the earlier
no-merge boundary for these plan-branch submissions. It does not authorize a
release/main promotion or edits to excluded Plan 55/38 tests.

Routes used: G0's N route, with an N helper for App implementation and dispatch
checks and a separate read-only helper for the merged-work audit and focused
source review. The review's one compiler-status finding was fixed and its
failure case checked. Exact inherited session model ID/effort was not exposed;
the available helper identity and this limitation are recorded in local run state.

## Coordinated integration completed

The manager reviewed the scripts, literal copies and modes, current records,
completed CI and exact-source proof. The astrid-dev task branch incorporated
current plan base `013e60390882ab9e697009f64bff2210a36391a1` by additive merge
in `9e5ca2beae40cc6f1489ab309c387e43a60abf6e`; its tree
`d59995f86156124637b466b0812e5880df93ef50` matches the locally checked tree.
`python3 scripts/astrid_dev.py check` and `git diff --check` passed. The new
[Documentation integrity run 43930646037](https://github.com/banodoco/astrid-dev/actions/runs/43930646037)
completed successfully, including documentation validation and the App vision
consumer contract. All three PRs were marked ready before the merge batch.

| Repository | PR | Reviewed head | Merge into `release/14/plan-39` |
| --- | --- | --- | --- |
| astrid-dev | [#762](https://github.com/banodoco/astrid-dev/pull/762) | `9e5ca2beae40cc6f1489ab309c387e43a60abf6e` | `60e944ce8c48a71d5ae2949cb6f68a52653acdab` |
| Runtime | [#52](https://github.com/banodoco/astrid-runtime/pull/52) | `dff3f116053d9e64e761509bfe35d77c1f6b96ad` | `e3a87af74bb47ad8012bacf011bce1261687d3ba` |
| App | [#278](https://github.com/banodoco/astrid-app/pull/278) | `9dc7a313e90b85c0f855f20be2fd8d037436fe1c` | `c23d0dfb59dc73394f47f11884df18c8102fc365` |

GitHub confirmed all three merges. Fresh git fetches verified all three plan
heads; Runtime and App merge trees have no diff from their reviewed task heads.
The five canonical copy comparisons were silent and all modes matched before
the batch. No script changed during record repair or integration, so the
independently verified exact-commit smoke proof carries forward unchanged.

Plan 38 W0 credits its reused delivery through G0. Plan 31 RL-0 and Plan 39 G0
are ticked with these receipts. Runtime's broad CI and the additional macOS
live-watchdog failure remain red/unresolved as described above; completing G0
does not claim otherwise. G1, SF3a and GL continue concurrently, with the next
owner checkpoint at the end of wave 0.
