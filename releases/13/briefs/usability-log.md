# Usability log: what a real agent would trip over (batch 6, 12 Nov)

Each item: what happened, what an agent following the skill would do, and the elegant fix.

1. **No project on a fresh install** (13:46 UTC). The first `generate` refused with "project is required for generation; pass --project <project> or select a current project". The RunPod skill and the generate examples never mention creating one.
   - **Workaround:** `astrid projects create setup --name Setup --select`.
   - **Elegant fix:** generate works with no ceremony. Either a default project exists from install, or `generate` uses one automatically and says so.
2. **Settings declared again on every generate.** The GPU list (redundant: already saved), `--max-hourly-usd`, `--max-usd` (alongside the saved `--budget-usd`), `--preparation-seconds`, `--execution-seconds` and `--idle-seconds` (required, no defaults), and `--consent paid` on every run.
   - **Owner (12 Nov):** "we shouldn't have to declare things over and over"; `--consent paid` is "just bureaucracy ... they've already rented the machine".
3. **No way to see the account balance from the product.** The batch uses `curl` against the RunPod GraphQL API for its $67.41 floor.
4. **Naming.** `machines setup` configures RunPod only; the generate path says `--placement runpod`. Two names for one thing today.
5. **A content-free heartbeat.** The `generate` CLI prints "Still following RunPod task …: [Nm] running waiting=-" every minute. It says the same during a 13-minute stock wait ("no stock yet" is only in the host log) and during engine setup. It should say the phase: waiting for a GPU (attempt N, datacenter), the machine starting, setting up the engine, downloading models, running, collecting outputs. That belongs in M7 (`machines show`) and the generate wait line.
6. **A volume pins an empty datacenter.** No 5090 or 4090 in EUR-NO-1 for 13 minutes while EU-RO-1 had 5090s. The CLI never said so (M6 plus the wait line).
- Bug: `generate --inputs-json FILE --edit IMG` drops the edit image (refused: requires image_ref); `--inputs-json` replaces rather than merges the CLI inputs. Found 12 Nov batch 6.
7. **A successful run's engine logs are not captured.** For t2i only the `run` record comes back ("the ComfyUI server owns its logs; VibeComfy did not capture them"). This breaks the owner rule: logs for every generation, including successes.
8. **The machine is warm but the engine is cold.** A t2i job took 6m38s with no downloads: 15 s host preparation, 4m17s on the pod (ComfyUI start, model check, loading at least 7.3 GB from the network volume, then generation), 54 s collecting one PNG, 24 s reset. The reset restarts ComfyUI, so every job on a warm machine reloads its models. Keep ComfyUI and its loaded models between jobs, and reset only the job's files. Also check the 54 s collection.
