# W22: boundary ratchet and provider neutrality

Checkout: `/home/user/wt/agent-compose` at `913c6b8fff8c63aeb05cb1b5ae160463f6d5e641`. The two requested tests were run once each through `/home/user/astrid-dev/env/agent-pytest.sh`, serially, with `-q -rA -o faulthandler_timeout=300`. Both failed. Full failure output is saved in [boundary-test.log](boundary-test.log) and [provider-neutrality-test.log](provider-neutrality-test.log). No source or baseline was changed.

## What the tests count

`test_core_pack_boundary_ratchet_holds` runs `scripts/check_core_pack_boundary.py --check`. It scans Python under `astrid/core`, `astrid/sdk`, and top-level `astrid/*.py`. Findings are AST imports/constants: `pack_import`, `capability_id`, `dynamic_pack_import`, `repo_pack_path`, and exact `pack_name_literal`. It counts `(file, kind, value)` multiplicities; the checked-in baseline has no line numbers. The 73 rows identify current source occurrences added since the R12 checkout; the guard baseline stores no line numbers, so the R12 comparison disambiguates repeated identical values where possible. For repeated literals that were already present in R12, the guard itself cannot identify a unique historical line.

`test_provider_and_engine_mentions_in_core_do_not_grow` scans every `astrid/core/**/*.py` file and counts case-insensitive substring occurrences of `runpod` and `comfy`, including comments, docstrings, identifiers, and string values. It has only aggregate limits, with no per-file or per-line baseline.

## Failures and totals

- Boundary ratchet: failed; 73 excess AST findings.
- Provider neutrality: failed at `runpod: 306` vs limit `303` (+3), and `comfy: 1206` vs limit `1184` (+22).

| Owner | Crossings | Class (a) | Class (b) |
|---|---:|---:|---:|
| machines lane | 25 | 0 | 25 |
| engine lane | 39 | 0 | 39 |
| test manager | 9 | 0 | 9 |

Fix class total: **(a) 0**, **(b) 73**. The placement type/resolution code already exists in generation, but it still uses provider/pack-name string constants and does not give the scanner a neutral interface. The other direct imports and literals are used; no unused import or literal was found among these excesses.

## Provider-neutrality growth and overlap

The static limits are the original limits added with the test (`ebdc2504`): 303 `runpod`, 1184 `comfy`. The current excesses are therefore +3 and +22. Comparing current counts with the W11 reported run (`f9214240`: 306/1203), `runpod` is unchanged and `comfy` grew by 3. A baseline-relative diff gives net +3 `runpod` occurrences (six additions in `astrid/core/contracts/errors.py` and `astrid/core/machines_cli.py`, offset by three removals in generation code) and +22 `comfy` occurrences across generation files. Those file/term totals are the finest attribution the substring test supports; it cannot say which 3 or 22 source occurrences cross the limit.

The W11-to-W22 net `comfy` additions are in engine code (including `engine_contracts.py`, `engine_platforms.py`, and `engine_runner.py`, offset by removals in `engine_runner_target.py`). They are not boundary findings. Some boundary findings contain provider/engine text, but the provider test has no per-line baseline, so its aggregate excess cannot be mapped to those same lines. The counts are related to the same broad source scope, but the test evidence does **not** show that its over-limit mentions are the boundary guard’s lines.

## Class (b) groups for release-manager design pass

- **neutral placement vocabulary/API** — 44 crossings.
- **neutral machine operation/capability dispatch API** — 19 crossings.
- **neutral setup phase/reserved command vocabulary** — 6 crossings.
- **neutral engine pin/resource registry** — 2 crossings.
- **engine contribution/resource discovery API** — 1 crossings.
- **neutral execution failure receipt hook** — 1 crossings.

A single interface per group should remove the listed direct core dependencies. The machine CLI/SDK paths, engine placement handling, failure receipt, pin/resource declarations, and setup vocabulary are separate design questions; combine them only if the release manager chooses a common neutral facade.

## Machines Lane crossings

| File:line | Kind | Token | Introducing commit | Subject | Fix | Shared interface |
|---|---|---|---|---|---|---|
| `astrid/core/execution/generic_host.py:2912` | `pack_name_literal` | `setup` | `e862934c` | Merge PR #330 (fix/r12-n3) into fix/r12-autostart | (b) | neutral setup phase/reserved command vocabulary |
| `astrid/core/execution/generic_host.py:2920` | `pack_name_literal` | `setup` | `e862934c` | Merge PR #330 (fix/r12-n3) into fix/r12-autostart | (b) | neutral setup phase/reserved command vocabulary |
| `astrid/core/execution/generic_host.py:6439` | `pack_name_literal` | `local` | `e75a5a8ee` | Plan 32 T5c+T5d: which machine ran a job; warm reuse cleared when the pod dies | (b) | neutral placement vocabulary/API |
| `astrid/core/execution/generic_host.py:6439` | `pack_name_literal` | `local` | `e75a5a8ee` | Plan 32 T5c+T5d: which machine ran a job; warm reuse cleared when the pod dies | (b) | neutral placement vocabulary/API |
| `astrid/core/execution/generic_host.py:12549` | `pack_name_literal` | `local` | `1ae020677` | Carry resolved placement into managed generation | (b) | neutral placement vocabulary/API |
| `astrid/core/execution/generic_host.py:12847` | `pack_name_literal` | `local` | `2ac650593` | Prepare managed engines on the trusted host before worker launch | (b) | neutral placement vocabulary/API |
| `astrid/core/execution/generic_host.py:7210` | `pack_import` | `astrid.packs.runpod.failure_receipt` | `09724310a` | Receipt: not_collected marker, RunPod-only wiring, stage-forcing journeys | (b) | neutral execution failure receipt hook |
| `astrid/core/execution/machine_run.py:23` | `pack_name_literal` | `local` | `b6c17c8fc` | Plan 32 T5: RunPod as a remote machine through generation.machine | (b) | neutral placement vocabulary/API |
| `astrid/core/machines_cli.py:23` | `pack_import` | `astrid.packs.runpod.machine` | `e75a5a8ee` | Plan 32 T5c+T5d: which machine ran a job; warm reuse cleared when the pod dies | (b) | neutral machine operation/capability dispatch API |
| `astrid/core/machines_cli.py:96` | `pack_import` | `astrid.packs.runpod.target_selection` | `7d8239a64` | Add machine keep CLI with paid cap | (b) | neutral machine operation/capability dispatch API |
| `astrid/core/machines_cli.py:134` | `pack_import` | `astrid.packs.runpod.target_selection` | `7d8239a64` | Add machine keep CLI with paid cap | (b) | neutral machine operation/capability dispatch API |
| `astrid/core/machines_cli.py:212` | `pack_import` | `astrid.packs.runpod.target_selection` | `c0f505d4d` | Add paid manual RunPod machine claims | (b) | neutral machine operation/capability dispatch API |
| `astrid/core/machines_cli.py:244` | `pack_import` | `astrid.packs.runpod.target_selection` | `c0f505d4d` | Add paid manual RunPod machine claims | (b) | neutral machine operation/capability dispatch API |
| `astrid/core/machines_cli.py:329` | `pack_import` | `astrid.packs.runpod.target_selection` | `4960d98d2` | Complete fresh RunPod machine setup | (b) | neutral machine operation/capability dispatch API |
| `astrid/core/machines_cli.py:348` | `pack_import` | `astrid.packs.runpod` | `748625413` | Add guided RunPod machine setup | (b) | neutral machine operation/capability dispatch API |
| `astrid/core/machines_cli.py:349` | `pack_import` | `astrid.packs.runpod.worker_owner` | `a284d16a6` | Fix generation-side F401 and I001 lint findings | (b) | neutral machine operation/capability dispatch API |
| `astrid/core/machines_cli.py:520` | `pack_name_literal` | `setup` | `748625413` | Add guided RunPod machine setup | (b) | neutral setup phase/reserved command vocabulary |
| `astrid/core/machines_cli.py:553` | `pack_name_literal` | `setup` | `748625413` | Add guided RunPod machine setup | (b) | neutral setup phase/reserved command vocabulary |
| `astrid/core/machines_cli.py:71` | `pack_name_literal` | `runpod` | `8f2a12303` | Bind machine release to requested pod through retained owner | (b) | neutral placement vocabulary/API |
| `astrid/core/machines_cli.py:217` | `pack_name_literal` | `runpod` | `c0f505d4d` | Add paid manual RunPod machine claims | (b) | neutral placement vocabulary/API |
| `astrid/core/machines_cli.py:295` | `pack_name_literal` | `runpod` | `4960d98d2` | Complete fresh RunPod machine setup | (b) | neutral placement vocabulary/API |
| `astrid/core/machines_cli.py:335` | `pack_name_literal` | `runpod` | `748625413` | Add guided RunPod machine setup | (b) | neutral placement vocabulary/API |
| `astrid/core/machines_cli.py:353` | `pack_name_literal` | `runpod` | `748625413` | Add guided RunPod machine setup | (b) | neutral placement vocabulary/API |
| `astrid/core/machines_cli.py:457` | `pack_name_literal` | `runpod` | `3ce1c9709` | Preserve unrestricted setup and protect provider errors | (b) | neutral placement vocabulary/API |
| `astrid/core/machines_cli.py:455` | `capability_id` | `runpod.setup` | `3ce1c9709` | Preserve unrestricted setup and protect provider errors | (b) | neutral machine operation/capability dispatch API |

## Engine Lane crossings

| File:line | Kind | Token | Introducing commit | Subject | Fix | Shared interface |
|---|---|---|---|---|---|---|
| `astrid/core/generation/asset_alignment.py:272` | `pack_name_literal` | `local` | `593b33283` | Engine receipts: one freshness check at every admission boundary; old custody handles kept | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/asset_alignment.py:105` | `pack_name_literal` | `local` | `993fd926e` | Readers of an installed engine build their plan from its receipt | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/canonical_pins.py:1` | `repo_pack_path` | `(multiline docstring; full AST string in crossings.tsv)` | `c4ee7ff13` | Pins: one canonical declaration (runpod/pins.json) with a check against every literal copy | (b) | neutral engine pin/resource registry |
| `astrid/core/generation/canonical_pins.py:18` | `repo_pack_path` | `astrid/packs/runpod/pins.json` | `c4ee7ff13` | Pins: one canonical declaration (runpod/pins.json) with a check against every literal copy | (b) | neutral engine pin/resource registry |
| `astrid/core/generation/cli.py:739` | `pack_import` | `astrid.packs.runpod` | `3bcd524e3` | Add machine phase timing, shared verified fetch, and local failure receipt | (b) | neutral machine operation/capability dispatch API |
| `astrid/core/generation/cli.py:777` | `pack_import` | `astrid.packs.runpod.machine` | `a284d16a6` | Fix generation-side F401 and I001 lint findings | (b) | neutral machine operation/capability dispatch API |
| `astrid/core/generation/cli.py:810` | `pack_import` | `astrid.packs.runpod.machine` | `80bbf6904` | Keep verified RunPod machines after failed jobs | (b) | neutral machine operation/capability dispatch API |
| `astrid/core/generation/cli.py:504` | `pack_name_literal` | `local` | `edf9b5928` | Plan 32 T4g: the local run path is complete (align modes, --job form, progress) | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/engine_bootstrap.py:36` | `repo_pack_path` | `astrid/packs/wan2gp/extensions/generation.engine/wan2gp.yaml` | `a45dd06c4` | Plan 32 T2b: one base engine keyed comfyui | (b) | engine contribution/resource discovery API |
| `astrid/core/generation/engine_endpoint.py:367` | `pack_name_literal` | `local` | `593b33283` | Engine receipts: one freshness check at every admission boundary; old custody handles kept | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/engine_local_server.py:49` | `pack_name_literal` | `local` | `39fa9ed23` | Plan 32 T4g: move the server start-or-reuse out of the bootstrap closure | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/engine_local_server.py:53` | `pack_name_literal` | `local` | `993fd926e` | Readers of an installed engine build their plan from its receipt | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/engine_local_server.py:55` | `pack_name_literal` | `local` | `993fd926e` | Readers of an installed engine build their plan from its receipt | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/engine_readiness.py:747` | `pack_name_literal` | `local` | `993fd926e` | Readers of an installed engine build their plan from its receipt | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/engine_startup.py:180` | `pack_name_literal` | `local` | `593b33283` | Engine receipts: one freshness check at every admission boundary; old custody handles kept | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/managed_preparation.py:156` | `pack_name_literal` | `local` | `993fd926e` | Readers of an installed engine build their plan from its receipt | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/managed_preparation.py:158` | `pack_name_literal` | `local` | `993fd926e` | Readers of an installed engine build their plan from its receipt | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/managed_preparation.py:267` | `pack_name_literal` | `local` | `2ac650593` | Prepare managed engines on the trusted host before worker launch | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/managed_preparation.py:354` | `pack_name_literal` | `local` | `993fd926e` | Readers of an installed engine build their plan from its receipt | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/managed_preparation.py:356` | `pack_name_literal` | `local` | `993fd926e` | Readers of an installed engine build their plan from its receipt | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/placement.py:227` | `pack_import` | `astrid.packs.runpod.machine` | `e75a5a8ee` | Plan 32 T5c+T5d: which machine ran a job; warm reuse cleared when the pod dies | (b) | neutral machine operation/capability dispatch API |
| `astrid/core/generation/placement.py:23` | `pack_name_literal` | `local` | `cef4da11e` | Plan 32 T3: add frozen Placement and its resolution tests | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/placement.py:67` | `pack_name_literal` | `local` | `cef4da11e` | Plan 32 T3: add frozen Placement and its resolution tests | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/placement.py:80` | `pack_name_literal` | `local` | `cef4da11e` | Plan 32 T3: add frozen Placement and its resolution tests | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/placement.py:135` | `pack_name_literal` | `local` | `cd27ed9d7` | Plan 32 T3b: one placement decision site; explicit local never reaches attached ComfyUI | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/placement.py:150` | `pack_name_literal` | `local` | `cef4da11e` | Plan 32 T3: add frozen Placement and its resolution tests | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/placement.py:151` | `pack_name_literal` | `local` | `cef4da11e` | Plan 32 T3: add frozen Placement and its resolution tests | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/placement.py:166` | `pack_name_literal` | `local` | `cd27ed9d7` | Plan 32 T3b: one placement decision site; explicit local never reaches attached ComfyUI | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/placement.py:244` | `pack_name_literal` | `local` | `cef4da11e` | Plan 32 T3: add frozen Placement and its resolution tests | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/placement.py:26` | `pack_name_literal` | `runpod` | `cef4da11e` | Plan 32 T3: add frozen Placement and its resolution tests | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/placement.py:101` | `pack_name_literal` | `runpod` | `e26c4bd09` | fix(generation): recognize mapped RunPod placement for recovery | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/placement.py:103` | `pack_name_literal` | `runpod` | `e26c4bd09` | fix(generation): recognize mapped RunPod placement for recovery | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/placement.py:103` | `pack_name_literal` | `runpod` | `e26c4bd09` | fix(generation): recognize mapped RunPod placement for recovery | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/placement.py:225` | `pack_name_literal` | `runpod` | `e75a5a8ee` | Plan 32 T5c+T5d: which machine ran a job; warm reuse cleared when the pod dies | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/settings.py:204` | `pack_name_literal` | `runpod` | `ee3015a5a` | Plan 32 T6d: default entries are data; generation settings document in the Runtime | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/settings.py:204` | `pack_name_literal` | `runpod` | `ee3015a5a` | Plan 32 T6d: default entries are data; generation settings document in the Runtime | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/settings.py:205` | `pack_name_literal` | `runpod` | `ee3015a5a` | Plan 32 T6d: default entries are data; generation settings document in the Runtime | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/settings.py:205` | `pack_name_literal` | `runpod` | `ee3015a5a` | Plan 32 T6d: default entries are data; generation settings document in the Runtime | (b) | neutral placement vocabulary/API |
| `astrid/core/generation/targets.py:301` | `pack_name_literal` | `local` | `993fd926e` | Readers of an installed engine build their plan from its receipt | (b) | neutral placement vocabulary/API |

## Test Manager crossings

| File:line | Kind | Token | Introducing commit | Subject | Fix | Shared interface |
|---|---|---|---|---|---|---|
| `astrid/core/hivemind/executors/search/run.py:178` | `pack_name_literal` | `setup` | `3e551fde` | worker-env setup also fetches runpod-lifecycle at its pin | (b) | neutral setup phase/reserved command vocabulary |
| `astrid/omp_agent.py:39` | `pack_name_literal` | `setup` | `3e551fde` | worker-env setup also fetches runpod-lifecycle at its pin | (b) | neutral setup phase/reserved command vocabulary |
| `astrid/sdk/generation.py:313` | `pack_import` | `astrid.packs.runpod.target_selection` | `16ffaa601` | Wait for RunPod capacity within explicit paid policy | (b) | neutral machine operation/capability dispatch API |
| `astrid/sdk/generation.py:377` | `pack_import` | `astrid.packs.runpod.target_selection` | `d3c440236` | Add explicit paid keep for owned RunPod leases | (b) | neutral machine operation/capability dispatch API |
| `astrid/sdk/generation.py:389` | `pack_import` | `astrid.packs.runpod.target_selection` | `c0f505d4d` | Add paid manual RunPod machine claims | (b) | neutral machine operation/capability dispatch API |
| `astrid/sdk/generation.py:1140` | `pack_import` | `astrid.packs.runpod.target_selection` | `16ffaa601` | Wait for RunPod capacity within explicit paid policy | (b) | neutral machine operation/capability dispatch API |
| `astrid/sdk/generation.py:356` | `capability_id` | `runpod.claim` | `c0f505d4d` | Add paid manual RunPod machine claims | (b) | neutral machine operation/capability dispatch API |
| `astrid/sdk/invocation.py:3415` | `capability_id` | `runpod.claim` | `c0f505d4d` | Add paid manual RunPod machine claims | (b) | neutral machine operation/capability dispatch API |
| `astrid/sdk/invocation.py:3413` | `pack_name_literal` | `runpod` | `c0f505d4d` | Add paid manual RunPod machine claims | (b) | neutral placement vocabulary/API |
