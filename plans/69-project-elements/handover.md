# Handover — Editing a real clip: project elements and practical fixes

[Plan](plan.md) · [Tasks](tasks.md) · [Inputs](inputs.md)

Written on 21 November 2026 by the Release 15 setup session, for the manager who runs this plan and then [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md) ([brief](../../releases/15/briefs/plans-69-77.md)). It is a dated snapshot: re-read heads with `git ls-remote` before acting.

## First actions

1. **Clone** `astrid-dev`, `astrid-app`, `astrid-agent` and `astrid-runtime` (all `banodoco` on GitHub). One worktree per branch.
2. **Check out `release/15/plan-69`** in the three product repositories and confirm the heads below, or newer ones whose history contains them.
3. **Create `run.yaml`** as [Plan 77's handover](../77-saving-holds-on-a-heavy-timeline/handover.md#runyaml) says, under this plan's `.otto/runs/<run-id>/`; the same bindings serve both plans.
4. **Record yourself** in the `Owner` line of [plan.md](plan.md) and the `Run start` line of [inputs](inputs.md#planning-evidence).
5. **Start PE-1 and PE-2** in parallel ([tasks](tasks.md)).

## Branches

| Repository | `release/15/plan-69` | Its `release/15/main` base | Pins |
| --- | --- | --- | --- |
| astrid-app | `5866b23bb` | `2ef94b4cf` | Agent `58c749cab`, Runtime `1046f4074` |
| astrid-agent | `58c749cab` | `04f3f1236` | Runtime `1046f4074` |
| astrid-runtime | `1046f4074` | `1758a6df9` | — |

- **What the base holds.** `release/15/main` is Release 15's main with `release/14/main` merged in on 21 November ([astrid-dev#1224](https://github.com/banodoco/astrid-dev/issues/1224)). Since then Agent `release/15/main` took R14-FIX-15 (`aac1ceb68`, astrid-agent#462); App R14-FIX-16 is not forwarded yet (it conflicts with Plan 59's save work; the Release 14 Lead is combining them). It does **not** hold Release 14's integration of Plans 59, 64 and 65, which has not landed in `release/14/main`. PE-3's first step, merging `release/15/main` in, brings whatever has been forwarded by then.
- **Merge, never rebase or force-push** ([Release workflow](../../skills/shared/workstreams/astrid-dev-release/SKILL.md#how-a-release-runs)).
- **The old branches** `release/14/plan-69` are superseded by these; do not push to them.

## Current Release 15 forward on 22 November

The Release 15 Lead landed the owner's forward after this handover was written. The current Runtime base is `2cf5890b7185450109254601b83d6dccb535bde4`, which contains `b51d4e56`. Agent's current base is `0982317814545d50c8d7e2c623d7f7086bba879b`. App's base remains `2ef94b4cf33d0818b642b0ef71fd9a64f58ddc18`. Recheck all three before relying on them. [Runtime #86](https://github.com/banodoco/astrid-runtime/pull/86) · [Agent #482](https://github.com/banodoco/astrid-agent/pull/482)

The forward invalidated the old exact landing comparison. Bring the current base into Plan 69 in Runtime, Agent and App order. Regenerate the contract projections and pins. The Runtime combined contract remains `0.2.15` with digest `sha256:2c6a76e17b4441398ab91e3e9d6283a719fd5b08807447db9dbf2ecc5e1339a2`. The owner-approved test changes pin that existing version in the two current timeline integration assertions. WC10 intentionally builds against a separate frozen `0.2.14` client and keeps its original values.

The host is arranging the exact paired Linux unit shards on separate machines after three cancellation cycles. Send the final Agent plan SHA before anyone runs candidate shards. Use the named selection and compare test IDs against the current Agent base. Obtain the exact Windows, Darwin, wheel and fast-check results from hosted CI. The previous Windows CIM, Darwin and test-gate evidence stays available as history. The current Agent base already carries matching RunPod model lock and recipe hashes, so [Agent #477](https://github.com/banodoco/astrid-agent/pull/477) closed as redundant.

## Running the tests

- **Agent:** a venv with `pip install -e '.[dev]'`, plus the Runtime at the pinned commit installed into the same venv (`pip install -e <runtime checkout at the pin>`); without it, imports fail with `No module named 'runtime_protocol'`. Element admission needs the renderer's pinned Node, v20.19.4 (`remotion/package.json`): set `ASTRID_NODE_EXECUTABLE` to it and run `npm ci` in `remotion/`. `pytest-xdist` is not in the dev extras, so do not pass `-n`.
- **Runtime:** a venv with `pip install -e '.[test]'`; `-n 4` works.
- **App:** `npm ci`, then `npx vitest run --config config/testing/vitest.config.ts <files>` and `npx tsc -p tsconfig.app.json --noEmit`.
- **Compare, do not count.** Run the same selection on the head and on its base (and, for a merge, on each parent), and look only at failures the head adds.

## Known failures

On 21 November, on these heads, with the setup above:

- **Agent:** `tests/packs/timeline/test_cli_parity.py::test_create_slug_names_the_new_timeline` and `::test_publish_requires_a_message` also fail on `release/15/main`. Three esbuild-discovery tests in `tests/core/test_project_packs.py` (`test_admission_compiles_when_bin_esbuild_is_a_js_shim`, `test_compiler_discovery_needs_no_bin_esbuild_and_forwards_windows_env`, `test_missing_esbuild_api_and_wrong_version_have_plain_fixes`) fail on `release/14/plan-69` itself with `KeyError: 'ASTRID_REMOTION_PROJECT_DIR'`; PE-1 decides whether that is the test's setup or a defect.
- **Runtime:** 22 cases across the timeline-commit test files fail the same on `release/15/main` (environment-dependent). `test_descriptor_reader_does_not_inherit_live_cas_proofs` is a strict xfail for [#1222](https://github.com/banodoco/astrid-dev/issues/1222) (PE-2).
- **App:** 7 to 9 failing cases and 9 to 11 `tsc` errors in the focused selection, each also present on `release/15/main` or `release/14/plan-69`. `src/tools/video-editor/runtime/admittedElement.realModule.test.ts` has two skips the skip registry does not declare, so the full `npm run test:app` refuses until they are declared.

## What the 21 November merge decided

- **Runtime:** two verify-once CAS designs met. Plan 59's (already on `release/15/main`, and in Release 14's integration) is kept; this plan's duplicate (`b2ea261`) and its API tests (`tests/test_cas_verification.py`) are dropped. PE-2 settles the one test left.
- **App:** `RemotionPreview.tsx` keeps both Release 15's `getCurrentFrame` and this plan's removal of the preview's element-readiness gate; `TimelineRenderer.tsx` takes both sides' imports.
- **Pins:** regenerated, never hand-merged.

## Pins

Regenerate with astrid-agent `scripts/regenerate_runtime_pins.py`, in order, from full SHAs:

```bash
python3 scripts/regenerate_runtime_pins.py --runtime-sha <runtime sha> --agent-sha <agent sha> --runtime-checkout <runtime> --app-checkout <app> --apply
```

It writes the Agent's two `runtime.lock.json` files and the App's `runtime.lock.json` and `public/install-manifest.json`. Commit the Agent's change first, then run it again with that Agent commit as `--agent-sha` for the App.

## Landing (PE-3, on the owner's go)

- **The owner's go first.** Landing into `release/15/main` needs it ([inputs](inputs.md#planning-evidence)). Ask once PE-1, PE-2 and R are done, then start Plan 77 without waiting; its branches already contain this plan's.
- **Order:** Runtime, then the Agent re-pinned to the landed Runtime merge commit, then the App re-pinned to both. Each PR names `Plan 69` in its title; the product repositories' `landing reference` check needs a plan or an astrid-dev issue named.
- **After:** set the plan 69 rows in [releases/15.md](../../releases/15.md#branches) to `merged` and run `python3 scripts/release_branches.py check 15`.


## Retained-history witness disposition

The current release base deliberately removed `tests/test_timeline_commit_ancestry.py` through Runtime `05d1ad88`, which reverted #62's retained-history optimization after reported import overhead. The host ruled to carry that deliberate removal on Plan 69. The original file passed all five cases on `c12a2d18`. With the original bytes restored only for the exact combined Runtime probe, `test_head_verification_after_an_unrelated_write_costs_the_same_at_3_and_30_entries` and `test_a_write_in_the_same_project_keeps_the_retained_history` observed 23 to 169 SQL statements and failed. `test_an_import_completes_while_a_commit_is_validating_and_does_not_force_a_rewalk` could not access the inherited `Film.provider` fixture. The two other cases passed. Record these inherited limits in the Plan 69 landing PRs.
