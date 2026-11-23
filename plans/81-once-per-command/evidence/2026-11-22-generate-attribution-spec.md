# Attribution spec — every second of `generate` named

Read on 22 November 2026 at astrid-agent `315b8b7a9336ec3147b399f6bf6f168011d09b27` (`release/15/plan-81`), the unmerged gate on `p81/us-2` (`313618112`), and VibeComfy `e65f494` (not the pinned `799d90f6`; re-check VibeComfy lines at dispatch). Line numbers are from that head: re-check each at dispatch. Nothing was run; every statement below is from reading unless it cites the evidence JSON.

**Task ids:** `A-1` to `A-6`. **Critical path:** A-1, A-3, A-5, A-6. **Rules for every card:** no wire, schema or store change; no refusal moves; no existing test edited, skipped or weakened; timing code only observes (a stage wrapper never changes arguments, order or exceptions); nothing is kept for a later command.

## Why the residual is 60% today

- `astrid/sdk/command_timing.py:64` computes `other command work` as wall minus the sum of stages. It is a remainder, so "stages add up to wall" is true by construction.
- A stage's `seconds` is exclusive: `_advance` (`command_timing.py:26-29`) credits elapsed time only to the innermost active stage. `model registry` reports 0.05 s because its pack scan is credited to the nested `pack discovery` stage (`core/pack/discovery.py:366`).
- The collector starts at process start on Linux (`astrid/console.py:18`, `process_started_at`), so interpreter start and every import sit in the remainder.
- On the measured route (`generate workflow <file.py> --placement <url>`) the only generation stages are `workflow build` around `workflow_entries.prepare` (`sdk/generation.py:1976`), `model registry` (`:626`), `target check` around `select_generation_target` (`:1825`) and `pack discovery`. Everything in the table under A-3 runs untimed.
- The gate measures only that route. Its argv is in `tests/integrations/test_command_latency_budget.py:77-81` on `p81/us-2`. No `entry lookup` or `entry discovery` stage appears in any evidence JSON.

## Stage model (A-1 decides the code; this is the contract)

1. Each timing row keeps `stage` and `seconds` with today's meaning (**self time**, exclusive of nested stages). Self times plus the remainder still sum to wall, so existing consumers and the two pinned assertions in `tests/sdk/test_command_timings_paths.py` are untouched.
2. Each row gains `total_seconds` (**inclusive**: stage exit minus stage entry) and `parent` (the enclosing stage's name, or `null`). A reader ranks by `total_seconds` at depth 0 and drills down by `parent`.
3. The `--timings` text view prints depth-0 stages by `total_seconds`, children indented under them, then the remainder with its share of wall. A stage name that occurs more than once in a command prints once with its count and summed time.
4. The remainder keeps the name `other command work` and gains nothing else. It is bounded by the gate (A-5), not hidden.
5. Start-up is three named rows written by the collector from stamps, not by `stage()`: `interpreter start` (process start to `astrid.console` entry), `gateway imports` (console entry to `_GATEWAY_IMPORTED_MONO`, `core/gateway/__init__.py:24`), `command dispatch` (that stamp to the generation `main`, `core/generation/cli.py:952`). Where the process start is unavailable (`process_started_at` returns its fallback), `interpreter start` is omitted and the JSON says `"start": "command entry"`.
6. Lazy imports are attributed to the stage that first triggers them. That is accepted for the stage table; the import table from `-X importtime` (A-4) is the authority on import cost. No import hook is added to product code.

## Cards

| Task / outcome | Route | Depends on | Scope | Focused proof | Size |
| --- | --- | --- | --- | --- | --- |
| A-1 Stages report inclusive time and their parent, and occurrences are countable. Contract points 1 to 4 above | X | — | astrid-agent `astrid/sdk/command_timing.py` (`TimingCollector._advance`, `snapshot`, `stage`), the two text printers at `astrid/core/generation/cli.py:962-965` and `astrid/core/gateway/dispatch.py:612-614`; new tests beside `tests/sdk/test_command_timings_paths.py` | New tests: a 0.3 s child inside a 0.5 s parent reports parent `seconds` about 0.2, `total_seconds` about 0.5, child `parent` equal to the parent's name, each within 10%; sum of all `seconds` plus the remainder equals the collector's wall within 1 ms; a stage entered three times yields three rows. Every existing test in `tests/sdk/test_command_timings_paths.py`, `tests/integrations/test_command_timing_cli.py` and `tests/core/generation/test_cli_timings_opt_in.py` passes unchanged | 5 h |
| A-2 Start-up is named: `interpreter start`, `gateway imports`, `command dispatch` (contract point 5) | N | A-1 | astrid-agent `astrid/console.py` (stamp at module entry), `astrid/core/gateway/__init__.py` (`main`, near 72-80: pass the stamps on), `astrid/sdk/command_timing.py` (`TimingCollector.__init__` accepts named marks), `astrid/core/generation/cli.py:957` | New test in a fresh process: `astrid generate image x --dry-run --json --timings` on a machine with no Runtime carries the three rows, each finite and non-negative, and their sum is within 10% of (generation `main` entry minus process start) measured by the test. With process start unavailable (monkeypatched fallback) the first row is absent and `"start": "command entry"` is present | 3 h |
| A-3 Every block on both routes is a named stage. The table below is the starting list; the worker then runs the A-4 profile and adds stages until the remainder is under 10% of wall on each route. A wrapper only wraps: no argument, order or exception change | X | A-1 | astrid-agent `astrid/sdk/generation.py`, `astrid/core/generation/cli.py`, `astrid/core/generation/backends/comfy_target.py`, `astrid/core/generation/backends/vibecomfy.py`, `astrid/core/generation/availability.py`, `astrid/sdk/invocation.py`, `astrid/sdk/workspace_client.py` | New test `tests/sdk/test_generation_stage_coverage.py`: with the Runtime client and ComfyUI faked as in `tests/sdk/test_generation_target.py`, one `generate workflow` and one `generate image` run to admission each report every stage name in the table for its route, with `parent` as listed. `tests/sdk/test_generation_target.py::test_attached_default_binds_live_models_and_admits_one_canonical_workflow` and `::test_explicit_unqualified_keeps_input_validation_before_probe` pass unchanged | 8 h |
| A-4 The profiles, as a repeatable script and one evidence run from source. Method below. No product code | N | A-3 for the stage runs; the import and cProfile runs can start at once | astrid-dev `plans/81-once-per-command/evidence/` (script `attribution/run.sh`, `attribution/rank.py`, outputs); reuse the standing-up steps in `plans/81-once-per-command/handover.md` | The four output files named in the method exist for both routes; `rank.py` rerun on the saved raw files reproduces the tables byte for byte | 5 h |
| A-5 The gate cannot pass vacuously and covers both routes. Changes listed below | X | A-1, A-3 | astrid-agent, on top of `p81/us-2`: `tests/integrations/test_command_latency_budget.py`, `tests/integrations/command_latency_budgets.py`, `tests/integrations/command_latency_baseline.json`, `tests/integrations/command_latency_template_baseline.json` | The seven assertions listed under "Gate changes"; the delay test fails naming the stage for each new stage; a 1.5 s sleep with no stage active fails on the remainder bound, not only on the ceiling | 6 h |
| A-6 The attribution table, recorded. One run from source in the container; the same script on an installed Astrid with a real ComfyUI when the machine exists (that run is US-0's first baseline) | N | A-4, A-5 | astrid-dev `plans/81-once-per-command/evidence/2026-11-XX-attribution.md` and `.json` | Acceptance below | 3 h |

### A-3 instrumentation points

Stage names are literal. "Parent" is the enclosing stage a reader should see; `—` means depth 0. Lines are at `315b8b7a9`.

| Stage name | Wrap | File and line | Route | Parent |
| --- | --- | --- | --- | --- |
| `argument parsing` | `parser.parse_args` and the input reads before the client opens | `core/generation/cli.py:628` (in `_main`, `:586`) | both | — |
| `Runtime connection` | `_open_client()`; today's launcher, lock, handshake and host stages become its children | `core/generation/cli.py:544` (workflow), `:812` (image) | both | — |
| `workflow snapshot` | `_snapshot_generation_workflow` entry (it calls `load_bundle`, `sdk/generation.py:182`) | `sdk/generation.py:1544` and `:1974` | workflow; image when the candidate is a ready template | — / `candidate preparation` |
| `source retention` | `_retain_generation_source`; `retain_source` | `sdk/generation.py:1556`; `:1834`, called at `:1964` and `:1980` | both | as above |
| `workflow inputs` | `attached_comfy_url` and `resolve_workflow_inputs` together | `sdk/generation.py:1559-1561` | workflow | — |
| `placement` | each `resolve_placement` + `validate_placement` | `sdk/generation.py:1641`, `:1791` | both | — |
| `generation settings` | `generation_settings.read` | `sdk/generation.py:1718` | both | — |
| `default selection` | `generation_defaults.dispatch_ids` | `sdk/generation.py:1720` | both | — |
| `candidate qualification` | the loop that calls `require_model_available` / `require_entry_available` | `sdk/generation.py:1759-1778` | both | — |
| `availability declaration` | body of `availability_declaration` | `core/generation/availability.py:21` | both | whichever stage calls it |
| `candidate preparation` | the body of one pass of the candidate loop, with the candidate id in the JSON row as `detail` | `sdk/generation.py:1846-2031` | both | — |
| `workflow build` | unchanged (`prepare`, `build_entry`, `_prepare_catalog_target_workflow`) | `sdk/generation.py:1900`, `:1949`, `:1976` | both | `candidate preparation` |
| `model registry` | add the untimed load | `core/generation/backends/vibecomfy.py:518` | image, catalog candidate | `workflow build` |
| `entry needs` | `draft_entry` | `sdk/generation.py:1983` | workflow | `candidate preparation` |
| `target node list` | `workflow_entries.target_schema`; `_capture_model_resolution` | `sdk/generation.py:1966`, `:1993`; `core/generation/backends/vibecomfy.py:525` | both | `candidate preparation` / `workflow build` |
| `ComfyUI <METHOD> <path>` | every request, named like the Runtime requests | `core/generation/backends/comfy_target.py:217` (`request_json`) and the `endpoint_transport.object_info` branch at `:269` | both | whichever stage calls it |
| `workflow emission` | `emit_bundle` | `sdk/generation.py:2001`, `:2131` | both | `candidate preparation` / `bundle materialisation` |
| `approval compile` | `bundle.compile(schema_provider=schema)`, and `load_bundle` at `:2007` | `sdk/generation.py:2003`, `:2009` | both | `candidate preparation` |
| `readiness description` | from `target_record` to the `readiness_envelope` call | `sdk/generation.py:2050-2092` | both | — |
| `bundle materialisation` | the `TemporaryDirectory` block up to the `self.workflow(` call | `sdk/generation.py:2127-2185` | both | — |
| `object import` | `_import_generation_member` | `sdk/generation.py:127` | both | whichever stage calls it |
| `invocation` | the `self.workflow(...)` call that admits | `sdk/generation.py:2186` | both | — |
| `capability registries` | `sdk_module._load_registries` | `sdk/invocation.py:4507` | both | `invocation` |
| `capability lookup` | `sdk_module.get_capability` | `sdk/invocation.py:4530` | both | `invocation` |
| `admission preflight` | `_vibecomfy_invocation_preflight` (re-reads the three objects, reloads the bundle, compiles the API form) | `sdk/workspace_client.py:1036` | both | `invocation` |
| `entry lookup`, `entry discovery`, `pack discovery` | unchanged | `core/generation/cli.py:740`; `sdk/generation.py:1731`, `:1744-1745`, `:1751` | image | — |

`entry lookup` appears on `generate image` only with `--entry` or `--model` (`cli.py:740`, `generation.py:1731`) or when a pinned default is not among the candidates (`:1751`). Plain `generate image "prompt"` shows `entry discovery` and `pack discovery` instead. The gate therefore needs both forms (A-5).

### A-4 profile method

Stand up a Runtime and a stand-in ComfyUI as in the handover, run one warm-up command, then for each route take five fresh processes of each of these. Routes: `W` = `generate workflow <ready_templates/image/qwen_image_2_1_turbo.py> --placement <url> --project <id> --prompt <text> --no-wait --json`; `I` = `generate image <text> --placement <url> --project <id> --no-wait --json`; `E` = `I` plus `--entry <the fixture's image entry>`.

1. **Stages:** the command with `--timings`. Output `stages-<route>.json`: per stage the median of `seconds`, of `total_seconds`, and the count.
2. **Imports:** `python -X importtime -m astrid generate ...` with stderr to `importtime-<route>-<n>.log`. `rank.py` sums the self microseconds by top-level package and by module, takes the median across the five runs, and writes the top 25 of each with their share of the un-profiled wall. From source and installed are separate tables: an installed Astrid runs the `astrid` console (`astrid.console:main`), so use that interpreter with `-X importtime -c "from astrid.console import main; main()"`.
3. **Functions:** `python -m cProfile -o cprofile-<route>-<n>.prof -m astrid generate ...`. `rank.py` loads each with `pstats`, and writes two tables of the top 40: by `tottime` (self) and by `cumtime`, each row with calls, seconds, and **share of that profiled run's total**. cProfile slows the command unevenly, so the ranked table reports shares, and converts to seconds only by multiplying the share by the un-profiled median wall from step 1. The two walls are printed side by side so the inflation is visible.
4. **Children and waits:** `py-spy record --subprocesses --format speedscope --rate 100 -o pyspy-<route>.json -- astrid generate ...`, once per route, if `py-spy` installs in the environment. This is the only view of the launcher `connect` subprocess and of time blocked in I/O. If it cannot be installed or lacks ptrace permission, record that in the note and go on without it: the stage rows for the launcher and the Runtime requests then stand as the only account of child and wait time.
5. **The ranked table** (`attribution.md`): one row per depth-0 stage in descending `total_seconds`, with count, share of wall, its three largest children, and beside it the top three cProfile `cumtime` functions whose share is consistent with it. Then the remainder row with its share. Then the import table.

Installed differences to record, not to assume: source identity is stamped (`runtime_protocol/startup_identity.py:17`), so the launcher and `pack host source identity` rows should shrink; `/object_info` is a real request; pack roots include whatever the install adds.

### A-5 gate changes

1. **Groups.** Keep `same` and `changed` (workflow route). Add `image_same`, `image_changed` (route `I`) and `image_entry` (route `E`), five fresh processes each, each to its own admitted task. Distinct task receipts are asserted across all generation groups.
2. **Remainder bound.** For every group: median `other command work` divided by median wall is at most 0.10. This assertion is independent of the ceiling and has its own message naming the group, the remainder in seconds and its share.
3. **Outer wall.** For every group: the sum of all `seconds` plus the remainder is within 10% of the wall the test measured around the subprocess (`command_sample`, `command_latency_budgets.py:57`). This catches time before the collector starts or after it stops.
4. **Required stages.** `image_same` and `image_changed` report `entry discovery`; `image_entry` reports `entry lookup`; every generation group reports `candidate preparation`, `target node list`, `workflow emission`, `approval compile`, `invocation` and `admission preflight`. A missing name fails with the group and the name.
5. **Counts for every stage,** not only Runtime requests: `summarize` (`command_latency_budgets.py:65`) records the per-command count of each stage name. Recorded in the baseline; asserted as "may not rise". Today's values to expect on the workflow route, from `2026-11-22-us2-exact-gate.json`: `POST /v1/handshake` 2, `GET /v1/health` 2, `GET /v1/app-state/user/{key}` 4, `GET /v1/objects/{digest}` 9, `POST /v1/projects/{id}/objects` 3, `POST /v1/tasks` 1.
6. **ComfyUI requests.** The stand-in server counts requests by path; the report carries the count of `/object_info` per command for each group, and it may not rise.
7. **Delay proof.** `test_budget_names_each_delayed_stage` covers each new stage name, and its remainder case must fail on assertion 2 even when the ceiling is not exceeded.

The new groups' initial ceilings are their calibration medians, set the same way as the existing three; that is the owner's pending ceiling decision, not a new one. Do not lower the 10% bound to make a first run pass: add stages (A-3) until it holds.

### A-6 acceptance

- The remainder is under 10% of wall on `W`, `I` and `E`, by the gate.
- Every row has a name from this spec or one added under A-3 and listed in the evidence note.
- The note names the largest depth-0 stage on each route, its largest child, the largest self-time function, and the import total with its largest package.
- The note states for each figure whether it is from source in the container or from an installed Astrid with a real ComfyUI, and gives the count of `/object_info` requests per command.

## Parallel work and shared files

| File | Cards |
| --- | --- |
| `astrid/sdk/command_timing.py` | A-1, then A-2 (sequential) |
| `astrid/core/generation/cli.py` | A-1 (printer, 962-965), A-2 (957), A-3 (544, 628, 812): one worker, or merge A-1 first |
| `astrid/sdk/generation.py` | A-3; also F-1, F-2, F-3, F-4 in the fixes spec |
| `astrid/core/generation/availability.py`, `backends/vibecomfy.py` | A-3; also F-2, F-3 |
| `tests/integrations/command_latency_*` | A-5 only |

Order: A-1 first (half a day). Then A-2, A-3 and the import and cProfile halves of A-4 side by side. A-5 after A-3. A-6 last. With the fixes spec in the same two days: land A-3 before F-1 to F-4, or give both to one worker, because they edit the same lines of `sdk/generation.py`; the fixes are small and rebase easily onto A-3. About 30 hours of work, two days of wall time with two workers.
