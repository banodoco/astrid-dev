# Release 14 G0 — canonical worker scripts

16 November 2026. This is the astrid-dev portion of [G0](../tasks.md), under the
[Release 14 scope](../plan.md#release-14-scope). The product copies still need
coordinated submissions; G0 is not marked complete.

## Source and scope

- Base: `2770aa79e8d9325c7891294609c746963cc4776e`.
- Implementation: `5fb12b7908d0a0e771e989f9f1f1d51b993788df`, tree
  `71fc701d644a55480b65b80c3065cc36fd840855`.
- Authorized destination: astrid-dev `p39/g0` only. No product branch, release
  branch or `main` was pushed or merged.
- Local validation: Linux, Python 3.13.5; fresh detached product checkouts with
  only the proposed worker scripts copied into `scripts/worker-env/`.
- Runtime checkout: `2537fed24385ec1c24f48a812e09af4bb63fb794`, the inspected
  `release/14/main` and `release/14/plan-39` head. Its Agent pin is
  `b05ac03a5bcab278bccf99d85b49f4037b5dec10`.
- App checkout: `0b6ef16152dc3fa11246ccc2007da630c66d1a1a`, the inspected
  `release/14/main` and `release/14/plan-39` head. Its manifest pins Agent
  `9814193a73f606719e81883a8be197d27dd361d4` and Runtime
  `6855dfa8df65cf8ae4c002b57134d6505493c17c`.
- Product tests, lockfiles and source are unchanged. The negative pin case used
  a separate throwaway Runtime worktree. No Plan 55 or Plan 38 test was edited.

The evidence-only follow-up carries the implementation proof forward: the four
script blobs below are unchanged. No full CI or integrated release qualification
is claimed.

Git CLI push could not authenticate in this session. Publication uses the
connected GitHub API with a lease on the assigned branch's base; the uploaded
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

`python3 scripts/astrid_dev.py check` exits 1 on both the untouched base worktree
and this candidate, with byte-identical diagnostics:

```text
ERROR release-documents: releases/14.md: Branches row astrid-agent `release/14/plan-39`: duplicate repository and branch
ERROR release-documents: releases/14.md: Branches row astrid-runtime `release/14/plan-39`: duplicate repository and branch
ERROR release-documents: releases/14.md: Branches row astrid-app `release/14/plan-39`: duplicate repository and branch
ERROR release-documents: releases/14.md: Branches row astrid-dev `release/14/plan-39`: duplicate repository and branch
```

Those Release 14 document entries are outside G0 and remain unchanged. Full
Agent and VibeComfy product smoke runs were not performed: their unchanged
helpers and the stubbed dispatch comparisons establish the narrower wrapper
claim only. No hosted, macOS or Windows validation was performed.

## Required coordinated copies

Copy these exact canonical blobs into later product submissions. Both products
need additions, since the directories are absent on the inspected release heads.
The local validation copies do not constitute a remote submission.

| Repository and destination | Canonical source | Git blob | Mode |
| --- | --- | --- | --- |
| Runtime `scripts/worker-env/runtime-setup.sh` | `env/runtime-setup.sh` | `b39e30fe340a804f1d23296ff8dea4ee428f3cd1` | 100644 |
| Runtime `scripts/worker-env/runtime-pytest.sh` | `env/runtime-pytest.sh` | `7ca73294e71c490a24ceba25131194292e94473a` | 100644 |
| Runtime `scripts/worker-env/smoke.sh` | `env/smoke.sh` | `1d5ac2b970b0407a8f8438c5fcdb8e4857d5b22e` | 100755 |
| App `scripts/worker-env/app-setup.sh` | `env/app-setup.sh` | `2361cfb7735fbd090d300d413e644cdb5b519d07` | 100644 |
| App `scripts/worker-env/smoke.sh` | `env/smoke.sh` | `1d5ac2b970b0407a8f8438c5fcdb8e4857d5b22e` | 100755 |

After coordinated copying, repeat the literal smoke commands and `cmp` checks
on each product submission's exact head. Do not merge the old `int/38` branch
wholesale just to obtain its three files.

Routes used: G0's N route, with an N helper for App implementation and dispatch
checks and a separate read-only helper for the merged-work audit and focused
source review. The review's one compiler-status finding was fixed and its
failure case checked. Exact inherited session model ID/effort was not exposed;
the available helper identity and this limitation are recorded in local run state.
