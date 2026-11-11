# G3: one failure receipt, fetched like an output

**Status: design only. Implementation is blocked on H10.** This design assumes the recommended answer: yes, a redacted, size-capped bundle may come back, local-only, about 256 KB. [§9](#9-if-h10-is-no) says what changes if the answer is no. Task: [releases/13.md G3](../13.md). Added by the orchestrator: a shared phase-timing block ([§4](#4-phase-timing-shared-by-success-and-failure)).

All code references are to Agent `release12/gen-candidate` `1439ccc63bf8d9ed5422ac1f95ffdd6158560e1e`. That commit is the merge of `plan32/r12-error-contract` `e1731b9e` (confirmed: second parent of `1439ccc6`; it adds the `generation_failed` fallback at `astrid/packs/runpod/failure_diagnostics.py:130-134`).

## 1. What happens today

**Failure path (the 4 KB tail).**
- On a non-zero exit, the pod-side job command pipes `failure_diagnostics.py` itself, as source, through the pod Python against `result.json` (`astrid/packs/runpod/machine.py:397-401`). This prints one `astrid-generation-failure:` frame.
- The controller reads only `tail -c 4097` of the job's stdout (`machine.py:763-773`). It parses the frame with `parse_frame`, which rejects anything over `MAX_FRAME_BYTES = 4096` (`failure_diagnostics.py:17,204-221`). It then raises `MachineError("remote generation failed (exit N; category=…; code=…)")` (`machine.py:774-780`).
- **The allowlist:** `CODES` maps about 25 codes to categories (`failure_diagnostics.py:18-31`). The only facts that survive are `node_id`, `node_class`, `field` and `constraint`. `node_class` and `field` must be in fixed sets (`:32-50`), and `node_id` must appear in the submitted graph (`:61-70,138-162`). Anything else becomes `unknown` or `generation_failed` (`:73-74,130-135`).
- **Why TTS said "field unknown":** no TTS node class or TTS-specific input name is in `FACT_ALLOW` (`:34-44`), so the field was dropped.
- `host_summary` and `safe_stored_summary` revalidate the frame before it reaches the lease journal and the CLI (`:77-102`; `astrid/packs/runpod/worker_owner.py:543-608`). The CLI prints one `Failure: …` line (`astrid/core/generation/cli.py:715-735`).
- Preparation failures carry raw remote stderr tails in exception text: `[-800:]` (`astrid/packs/runpod/remote_placement.py:493-497,524-536`). `host_summary` then drops that text before the journal.

**Success path (verified-manifest fetch).**
- The job command ends with `manifest_command(out)` (`machine.py:403`; script at `remote_placement.py:299-325`). The script writes `wrapper-manifest.json` with a sha256 and size for each file, and prints `WRAPPER_MANIFEST_SHA256=`.
- `fetch` downloads the manifest and checks it against the printed digest. It then downloads each file over the same pod-agent HTTPS `ops.get`, rejecting unsafe paths and any digest or size mismatch (`machine.py:781-812`; `_HttpsOps.get`, `remote_placement.py:903-904`).
- Failures have no such path.

**Release and keep-after-failure (Plan 40 T9).**
- `run_on_machine` calls `claim` outside the `try` block, then `start`/`poll`/`fetch`, and always calls `release(lease, success, failure=, stage=)` in `finally` (`astrid/core/execution/machine_run.py:67-117`).
- On a failure, `release` registers a failure observation and switches to a bounded transport (`ops.bounded`, `FAILURE_VERIFY_SECONDS = 120`) that a paid-expiry release can abort (`machine.py:868-908,180`; `worker_owner.py:610-634`; `remote_placement.py:770-772`). It stops the exact job (`machine.py:911-923`) and decides safe or unsafe (`:926-963`).
- If the machine is safe, the in-place reset runs (`:966-972`) and the lease settles `idle` with the bounded summary (`:976-997`). If not, `note_failed_job` runs and the exact pod is released (`:983-1013`).
- Preparation failures inside `claim` settle or release at `machine.py:579-619`.
- **Correction to the finding:** "a kept machine preserves the evidence" is only partly true. The reset that precedes warm retention deletes the run folder and the agent job folder, and truncates `runtime-data/**/*.log` (`astrid/packs/runpod/pod_reset.py:213-233,320`). Only the engine's own log, under the engine root, is not covered by that sweep (`astrid/core/generation/engine_custody.py:662,835`). So collection has to come before the reset, not only before release.

## 2. The eight stages: where each fails and what exists then

| Stage (enum) | Where it fails | Machine / pod agent? | Evidence at that moment |
|---|---|---|---|
| `no_machine` | `lease_owner.acquire` (`astrid/packs/runpod/generation.py:110-112`); offer and capacity refusals (`astrid/packs/runpod/target_selection.py:40-91,557,609-622`); a pinned machine that is not live (`machine.py:540-546`); acquire failing before `on_acquired` (`machine.py:613-619`) | none | exception class, fixed offer reason (`target_selection.py:66-74`), gate name (`astrid/packs/runpod/worker_preparation.py:42-49`). **Local only** |
| `boot` | `connect_claimed_for_preparation` (`remote_placement.py:935-962`, called at `generation.py:131`); storage pin (`generation.py:144-152`); `ensure_pod_ready` (`generation.py:173-175`, `machine.py:220-235`); the pod-side `exit 75` "not ready" (`machine.py:384-386`) | pod exists; agent may be unreachable | pod id, gate. Collection is attempted only if the agent answers |
| `install` | `_bootstrap`/`_install` jobs (`remote_placement.py:543-630`); engine not ready at `start_engine` (`astrid/packs/vibecomfy/actions/run/run.py:754-770`) | yes | job folder stdout/stderr; engine install receipt `.astrid-engine/install.json` (`astrid/core/generation/engine_local_endpoint.py:30`) with the failed step and code (`astrid/core/generation/engine_runner.py:836-853`) |
| `model_download` | pod-side align, inside the job (`run.py:983-993`); codes `missing_model`/`download_failed` (`failure_diagnostics.py:27`) | yes | progress phase `align`, `result.json`, job stderr |
| `workflow_validation` | entry/listing check `exit 3` (`machine.py:394-396`); pod-side input checks giving `input_rejected` (the TTS case) | yes | `result.json` issues, submitted graph |
| `execution` | `run`/`finalize` phases (`run.py:775,996`); non-zero `astrid generate` (`machine.py:397-401`) | yes | `result.json`, job stderr, engine log |
| `output_collection` | missing result or manifest, `DigestMismatch` (`machine.py:781-809`) | yes | run folder (the pod is unsafe on a digest mismatch, `machine.py:959-962`) |
| `release` | reset failure (`machine.py:966-972`), settlement (`:988-997`), exact release (`:1003-1013`, `:597-611`) | yes / going | fixed release-reason literals only. **No collection**: this stage updates a receipt or writes one locally |

**How a job failure gets its stage.** Facts are taken in this order:

1. The controller step that raised. Today's stage names are kept as `phase`: `claim`, `preparation`, `start`, `poll`, `fetch`, `execution`, `reset`, `cancel` (`failure_diagnostics.py:89-90`). They are refined by the last `RemoteRun.note` step: `bootstrap`, `install`, `selection`, `job`, `fetch`, `reset` (`remote_placement.py:350-351`; `machine.py:681,696,811,1072`).
2. The pod exit code: 75 means `boot`, 3 means `workflow_validation`.
3. The diagnostic category: `input` means `workflow_validation`; `model` means `model_download`; `installation`, `health` or `dependency` means `install`.
4. The last progress phase, copied on each poll (`machine.py:715-743`; phases at `astrid/core/generation/progress.py:16`): `align` means `model_download`, `start_engine` means `install`.
5. Otherwise, `execution`.

## 3. `failure-receipt.json` schema (v1)

Local path: `<runtime data root>/generation/failures/<task_id>/failure-receipt.json`, with the fetched bundle in `files/` beside it. The root is `resolve_runtime_data_root()` (`astrid/sdk/storage_root.py:152`), the same root the RunPod journal uses (`target_selection.py:256-260`), so the host and the CLI find the same folder. Failures with no admitted task use `local-<uuid>`. The newest 20 receipts are kept and older ones pruned; receipts never leave the machine.

```json
{
  "schema": "astrid.generation.failure-receipt.v1",
  "receipt_id": "…", "outcome": "failed",
  "stage": "workflow_validation",
  "stage_basis": "pod_exit|diagnostic|progress|controller_step",
  "phase": "fetch",
  "cause": {"code": "input_rejected", "category": "input", "exception": "MachineError",
            "node_id": "12", "node_class": "…", "field": "…", "constraint": "enum", "exit_code": 1},
  "message": "The pod rejected the workflow before it ran: node 12, field 'speaker' (enum).",
  "identity": {"task_id": "…", "attempt_id": "…", "invocation_id": "…", "placement": "runpod",
               "machine_id": "…", "lease": "<operation_id>", "generation": 3, "gpu": "…",
               "warm": true, "run_id": "…", "remote_job_id": "…", "pod_source_digest": "…"},
  "timing": { "…": "see §4" },
  "machine": {"after": "kept|released|none|unknown", "release_reason": "unsafe_job_state",
              "release_at": 0, "cost_usd": 0.0},
  "collection": {"state": "fetched|local_only|unreachable|timed_out|aborted_by_release|over_cap|digest_mismatch|withheld_by_policy",
                 "bundle_manifest_sha256": "…", "bytes": 0, "cap_bytes": 262144},
  "files": [{"name": "engine-log-tail.txt", "path": "files/engine-log-tail.txt", "bytes": 0,
             "sha256": "…", "truncated": true, "source_bytes": 0}],
  "redaction": {"policy": "astrid.failure-redaction.v1",
                "pod": {"secret": 0, "url": 0, "prompt": 0, "lines_dropped": 0},
                "local": {"secret": 0, "url": 0, "prompt": 0},
                "workflow_strings_replaced": 0}
}
```

- `cause` keeps today's validated facts: it is built by `host_summary`, never from exception text.
- `message` comes from a fixed table keyed by `(stage, code)`, with only `cause` facts filled in.
- `machine.*` uses the journal row that `lease_row` already exposes (`machine.py:1166-1208`).
- `release_reason` is one of the existing literals.
- Cancelled runs write no receipt.

## 4. Phase timing, shared by success and failure

One block, `astrid.generation.phase-timing.v1`, appears in two places: inside `failure-receipt.json`, and in `terminal["machine"]["timing"]` for every job. `terminal["machine"]` is already set at claim and success (`astrid/core/execution/generic_host.py:7035-7043`) and already copied into the attempt receipt on both outcomes (`generic_host.py:10711-10712`). Success therefore needs no new file.

All values are UTC epoch seconds plus derived durations. Each phase is `null` when it did not happen.

| Phase | Start | End | Exists today? |
|---|---|---|---|
| quote to claim (waiting for stock) | the capacity wait loop is entered | `claimed_at` | **Start not recorded.** It must be stamped at the loop entry (`target_selection.py:579`). The create attempt is stamped `last_create_started_at`/`authorized_at` before the POST (`target_selection.py:805-813`). `claimed_at` exists (`target_selection.py:895`), but it keeps an old value on a re-used record, so the receipt must use this invocation's own stamp |
| paid clock | `lease.started_at` = `authorized_at` (`worker_owner.py:405,419-427`) | `ended_at` (`worker_owner.py:857`) | yes |
| preparation | lease saved `preparing` after acquire (`generation.py:117-129`) | `save(state="prepared")` (`generation.py:181`) | **No timestamps.** Add `at` to `RemoteRun.note` (`remote_placement.py:350-351`); bootstrap and install then get times for free (`:589,630`) |
| execution | `_checkpoint(... "running")` (`machine.py:694`) | poll sees `exited` (`machine.py:709-710`) | **No timestamps.** Stamp both checkpoints. Pod phases (`align`, `run`, …) need an `at` key in `write_progress` (`progress.py:20-33`) and in `PROGRESS_KEYS` (`machine.py:51`), so model download and run split cleanly |
| collection / fetch | fetch or collection start | `note("fetch","done")` (`machine.py:811`) or collection end | stamp |
| idle | `settle` sets `idle_expires_at` (`worker_owner.py:572-573`) | the next claim's reuse, or `ended_at` | Idle ends after this job's receipt is written. So the next job records `idle_before_s` (warm reuse), and the ended-lease row (`worker_owner.py:857-861`) records the final idle span |

## 5. The pod-side failure folder

A new standard-library-only `failure_bundle.py` is shipped the same way `failure_diagnostics.py` is (`machine.py:399-401`) and run with one `ops.exec`. That is the same channel `fetch` already uses for `tail` (`machine.py:768`). It writes `RUNS_ROOT/<run_id>/failure/`; preparation uses `RUNS_ROOT/prep-<operation_id>/failure/`. The existing reset sweep already removes run folders (`pod_reset.py:157,216-219`), and an unsafe release deletes the pod, so no new cleanup is needed.

| File | Source | Cap |
|---|---|---|
| `error-tail.txt` | job folder `stderr`, the one `_run_job` already tails (`remote_placement.py:524-525`) | 32 KiB |
| `engine-log-tail.txt` | `<engine root>/runtime/out/sessions/comfyui/comfy.log` (`engine_custody.py:662,835`); slice 1 must confirm this is the live server's log on the pod | 128 KiB |
| `node-error.json` | `result.json` issues/node errors (today read by `read_result`, `failure_diagnostics.py:189-201`), with redacted values | 32 KiB |
| `workflow.redacted.json` | the submitted graph (`job.json` `execution.source`, `failure_diagnostics.py:174-186`), structure only | 48 KiB |
| `install-receipt.json` | `.astrid-engine/install.json` (install stage only) | 8 KiB |
| `collector.json` | exit code, last phase, redaction counts, truncation facts | 8 KiB |
| `wrapper-manifest.json` | the existing `manifest_command` (`remote_placement.py:322-325`) | n/a |

- Redaction runs before truncation, so a redaction token is never split.
- Tails cut at line boundaries, and any line over 2 KiB is shortened.
- The total cap is 256 KiB. The engine tail gives way first.

## 6. Redaction rules (`astrid.failure-redaction.v1`)

The same function runs on the pod and again on the controller after the fetch. The controller pass adds what only the controller knows: the HTTPS token file and the provider credential value, which the product already holds and resolves itself.

1. **Keys and tokens.**
   - Exact-value replacement of every environment value whose name matches `KEY|TOKEN|SECRET|PASSWORD|AUTH|CREDENTIAL|COOKIE`, plus the pod's prepared-connection owner token (`pod_reset.py:271`).
   - Patterns: `Bearer …`, `Authorization: …`, `hf_…`, `sk-…`, `AKIA…`, and any letter-and-digit run of 32 characters or more, except `sha256:<hex>` digests.
2. **URLs.** Every `scheme://…` becomes `<url>`; IPv4/IPv6 literals become `<ip>`. Pod paths under `/root/astrid` are kept: they are fixed and useful.
3. **Prompt text.**
   - Every string in `job.json` `bindings` and `inputs` (`machine.py:664-668`) of 4 characters or more is replaced wherever it appears. This includes its JSON-escaped form and each line of 8 characters or more.
   - Any log line containing 32 or more consecutive characters of one of these strings is dropped whole.
   - Strings under 4 characters are not matched; that limit is stated in `collector.json`.
4. **The workflow without prompt text.**
   - Kept: node ids, `class_type`, input names, link edges, numbers and booleans.
   - Kept as strings: model-file names (`*.safetensors|ckpt|pt|pth|bin|gguf|onnx`, no whitespace), and values of a small field allowlist (`sampler_name`, `scheduler`, `*_name` loaders, `type`, `mode`, `weight_dtype`, `device`).
   - Every other string becomes `{"redacted": "string", "len": n}`. Any value equal to a binding or input is always redacted.

## 7. Fetch reuse and ordering

**No new transport.**
- Lift the body of `machine.py:791-812` into `_fetch_verified(ops, remote_dir, destination, manifest_digest)`. Success calls it on `out/`; failure calls it on `failure/`.
- Before any `ops.get`, the failure call also refuses any manifest whose sizes break the §5 caps (`collection.state = over_cap`).
- A bundle digest mismatch is treated like an output mismatch: the pod becomes unsafe and is released (`machine.py:959-962`).

**Ordering.** Collection is a step on the release path, so no job-path release can skip it.
- **Job-path failures**, including fetch-branch failures, which raise into `finally` (`machine_run.py:102-117`): collection goes in `_release_impl` after the exact job stop (`machine.py:911-923`) and before the remote safety checks, the reset (`:966`) and `owner.release` (`:1003`).
- **Preparation failures:** collection goes first in `claim`'s `except` block, before `_finish` (`machine.py:583`) and before the settle and release calls (`:597-611`). The bundle travels on the exception as `exc.failure_bundle`, as `release_identity` already does (`machine.py:616`).
- `run_on_machine` gains a `try` around `claim` and writes the receipt after `release` returns, so `machine.after` is final. It is optional, gated by signature checks like `failure`/`stage` (`machine_run.py:110-117`).

**Timeouts.**
- Collection uses the existing bounded transport and abort event.
- `FAILURE_VERIFY_SECONDS` grows by a `COLLECT_SECONDS = 45` slice, always clipped to the paid expiry (`machine.py:901-907`).
- A paid-expiry or explicit release aborts collection (`collection.state = aborted_by_release`). Money rules win.

**If collection fails** (timeout, agent unreachable, over cap):
- Settlement and release go ahead exactly as today. "Unsafe release still has priority over a diagnostic read/write" (`machine.py:983-987`).
- A receipt is still written, with the controller-side `cause`, timing and `collection.state`.
- If receipt writing itself fails, it is logged by exception class and never masks the original error, matching `cli.py:734-735`.

## 8. The command, tests, slices

**Command: `astrid generate failure [TASK_ID] [--json]`.** It prints the newest receipt, or the one for `TASK_ID`.
- It is a new subparser of the `astrid generate` parser, beside `describe` and `release` (`cli.py:193-330`), dispatched in `_main` (`cli.py:516-560`). `failure` collides with no existing modality.
- Why not `astrid machines …` (`astrid/core/machines_cli.py:473-537`): `no_machine` receipts have no machine.
- `_kept_failure` (`cli.py:715-735`) adds one line on every RunPod failure: `Receipt: astrid generate failure <task_id>`.
- If `cli-surface.json` covers `generate` verbs, regenerate it with `scripts/gen_cli_surface.py`.

**Forced failures on CPU.**
- Base: `tests/integrations/test_remote_machine_cpu.py`. It uses a real Runtime, host, lease owner and HTTPS transport, with only provider HTTP and the pod agent faked (`:1-10,64`).
- Each stage gets one case: the fake offer refuses, or the wait times out (`no_machine`); the agent never answers (`boot`); the install job exits 1 with a failed install receipt (`install`); progress `align` plus `download_failed` (`model_download`); `exit 3`, and an `input_rejected` result naming a non-allowlisted TTS field (`workflow_validation`); a non-zero run with an engine log (`execution`); a manifest digest mismatch (`output_collection`); the reset exits non-zero (`release`).
- Each case asserts: receipt stage and code, files with digests, the machine kept or released as today, collection before reset and release (call-order spy), and a sentinel secret, URL and prompt absent from every file.
- Unit tests for the redactor and caps sit beside `tests/packs/runpod/test_failure_diagnostics.py`. Its existing tests stay unchanged, because the frame and journal contract does not change.
- **Live proof (no separate spend):** the Phase 2 TTS diagnosis run on a real pod. It is the one run that proves the real `comfy.log` path, real node-error shapes, redaction on real logs, and collection within budget. `boot` and `no_machine` stay CPU-only.

**Slices (most mechanical first).**

| Slice | Route |
|---|---|
| 1. Timing stamps (§4) and `_fetch_verified` refactor, no behavior change | N |
| 2. Receipt schema writer and `astrid generate failure` (local-only stages work at once) | N |
| 3. Pod `failure_bundle.py`, redactor and caps, with unit tests | X (redaction is data safety) |
| 4. Collection in `_release_impl` and `claim`, with budget and ordering, plus the CPU stage matrix | S (paid custody and ordering) |
| 5. Live check folded into Phase 2 TTS | manager GPU duty |

Slices 1 and 2 do not depend on H10 and can start before it is answered.

## 9. If H10 is no

- No bundle leaves the pod: `collection.state = withheld_by_policy`, and `files` is empty. Slices 1, 2 and 4's ordering and timing work all stay.
- The structural facts get richer instead, so a cause is still named without SSH:
  - **(a)** `field` and `node_class` are authorized against the submitted graph's own input names and class types, as `node_id` already is (`failure_diagnostics.py:61-70,138-162`), not against the fixed list. This alone would have named the TTS field.
  - **(b)** The pod exit code, last phase, the install receipt's failed step id and code, and the release reason are added.
  - **(c)** A pod-side classifier maps a few fixed log signatures (CUDA out of memory, a node pack that failed to import, a missing node class, a refused download) to new `CODES` entries. Only the enum crosses.
- The pod folder moves out of the run folder to `/root/astrid/failures/<run_id>/` (newest 5 kept), so it survives the reset on a kept machine for private operator inspection. The receipt names that pod path.
- Causes that live only in log text (a custom node's traceback) stay unnamed.

## Rulings (orchestrator, 11 Nov 2026)

- **Collection runs before the reset.** This is a hard requirement: the reset before a machine goes idle deletes the run and job folders and truncates every log (`pod_reset.py:213-233`), so collection after it finds nothing.
- **Releases outside the job path win.** A paid-expiry timer, `astrid machines release` or host shutdown aborts collection; the receipt records collection as aborted.
- **A failure-bundle digest mismatch is treated like an output mismatch:** the machine is marked unsafe and released.
- **Retention:** 20 local receipts and 5 pod folders.
- **Redaction rule** goes to Hannah with H10, as written above.
- **Graph-checked field and node names** are built now under either H10 answer; the orchestrator confirms with Hannah before merge.
