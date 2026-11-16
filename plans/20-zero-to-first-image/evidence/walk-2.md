[Plan](../plan.md) · [Tasks](../tasks.md) · [Inputs](../inputs.md) · [Walk 1](walk-1.md) · [Walk 2r](walk-2r.md)

Committed by the planning session from the phase 4 manager's message of 14 Nov 2026 (`session_011EzfW4R5yz8EETVbzZaLCF`). The walker's text follows unchanged, except that HTML entities from the message transport are decoded (`&gt;` → `>`).

---

# P4.9 walk 2: the new path on CPU against the fake ComfyUI

Evidence folder: `/home/user/wt/p4-9-evidence/` (`cmdlog.txt` has start times; `out-*.txt` has each command's full output).
`L` = `/home/user/wt/p4-9-evidence/launcher.sh` (walk 1's launcher, `p4-0` -> `p4-9`, plus `TMPDIR`, see deviation D5).

## 1. Versions
- Candidate SHA `3490f1b253fdbb0bd45001e4d4b09431530e3ede` (checkout clean; only ignored `__pycache__/` and `astrid.egg-info/` present, both pre-existing).
- VibeComfy `dba38f8644c46f652376f2cd5112ea161e40f09b`; Runtime `6855dfa8df65cf8ae4c002b57134d6505493c17c`; lifecycle `7f0b025e` (sanctioned env only).
- Python 3.13.18. `vibecomfy` 2.8.0 registered with `pip install --no-deps` (P4.0.13 route).

## Known deviations (setup rows, not counted)
- D1 No installer run (P4.0.3: `codeload.github.com` 403). Launcher `L` stands in for `run-astrid`.
- D2 `astrid-runtime workspace create --source-manifest runtime-profile/astrid.json` (walk 1's profile, paths repointed), then `up --wait --door-port 17341`. Port 17340 is still held by walk 1's Runtime (realm `p4-0-walk`, pid 9143, still alive): `door_port_taken`. I did not stop it; I used another door port. `--hosted-origin off` is refused with `--wait` ("up --wait requires the browser door"), so the door points at astrid.haus; the "Connected" check was not possible.
- D3 Fake: walk 1's fake, changed: the three model folders start empty and are real directories reported by `/internal/folder_paths`; loader choices in `/object_info` now follow the folder contents (the first version did not, row A5a); `POST /_test/simulate_download` writes three stand-in files; `/history/<id>` and `/view` added so a run can finish (walk 1's fake 404ed there). Fake is in `fake/fake_comfyui.py`. Nothing here is verified against a real ComfyUI.
- D4 No fake file server for the models: `fetch-models` only fetches `https://huggingface.co` sources (plan text, section 3 row A5), so a local server could not be used without routing around it.
- D5 `TMPDIR=/home/user/wt/p4-9-evidence/tmp` added to the launcher after P4.9.1.
- D6 "Asked" rows: none were needed for Run A/B besides the ones taken as the skill recommends: use the ComfyUI at `http://127.0.0.1:8188` (yes), the default's download (yes at the plan; apply not run, see A5), first image (yes), save the workflow as an entry (answer 2, yes).

## 2. Run A (the default, `qwen-image-2.1-turbo`, slot `image.t2i`)
First skill step 15:22:06Z (`runA-skillstart.txt`).

| # | Command | Start (UTC) | Outcome |
|---|---|---|---|
| A1 | `L generate defaults --json` | 15:22:06 | exit 0, 26 s (first call; Runtime host starting). `image.t2i` = `qwen-image-2.1-turbo`, `ready: true`, `reason: required model roles present (model bytes unverified)` while the fake's model folders were EMPTY (P4.9.3). |
| A2 | `L generate targets --json` | 15:22:32 | `status: ready`, attached `http://127.0.0.1:8188`, `location: local`, `owner: human`; placement `source: discovery` before anything was saved. |
| A3 | `L generate scan --json` | 15:22:34 | found `http://127.0.0.1:8188`, `workflows: ["my_portrait_custom.json"]`, `workflows_detail: [{"modified": null, "name": "my_portrait_custom.json"}]`; error for port 8000 only. |
| A4 | `L generate settings set placement http://127.0.0.1:8188` | 15:22:41 | `placement is now {"endpoint": "http://127.0.0.1:8188", "kind": "attached"} (was the built-in default); restore: astrid generate settings unset placement` |
| A5a | `L generate fetch-models qwen-image-2.1-turbo t2i --comfy-url http://127.0.0.1:8188` (first fake) | 15:22:44 | `Missing models for qwen-image-2.1-turbo/t2i on your ComfyUI at http://127.0.0.1:8188:` then `Nothing can be downloaded.` Fake artifact: its `/object_info` ignored the empty folders (file `out-A5a-...`). |
| A5 | same command, fake fixed | 15:23:06 | exit 0 (3 s). Plan below. |
| A5-apply | `--apply e5c37dca...` | not run | A real run would pull 16.10 GiB from huggingface.co, which the brief forbids; no local source can be substituted (D4). Not run, so no refusal text exists to quote. Code: a non-HF source is shown as `its source is not https://huggingface.co/, so Astrid will not fetch it` in the plan (`astrid/core/generation/asset_gaps.py`). |
| (sim) | `curl -X POST 127.0.0.1:8188/_test/simulate_download` | 15:23:10 | the fake lists the three stand-in files. Not an Astrid command. |
| A6 | `L generate image --entry qwen-image-2.1-turbo --inputs-json work/inputs-a.json --json` | 15:23:15 | printed `Created and selected project "My first project" for this generation.`; task stayed `queued waiting=-` for 5 min, never admitted (P4.9.1). |
| A6b | same, after `astrid-runtime down`/`up` | 15:29 | queued, 100 s, no admission. |
| A6c | same plus `--placement http://127.0.0.1:8188` | 15:31 | queued, 90 s, no admission. |
| A6d | same, after `TMPDIR` fix (D5) | 15:37:20 | **admitted: fake log `POST /prompt` 1408 bytes (~15:37:22Z)**, then `POST /queue` x4, then `GET /history` 404 (fake limit) -> run failed. |
| A6e | same, fake gains `/history` | 15:38:00 | exit 0, `succeeded`; `POST /prompt` 1408 bytes. Result has `"open_url": "https://astrid.haus/tools/video-editor?project=a15b3e4df2154f26bcfc81a518db523f"`, `image_paths`, `seed_used`. No project notice (printed once, in A6). |

The plan (A5), exact:
```
Missing models for qwen-image-2.1-turbo/t2i on your ComfyUI at http://127.0.0.1:8188:
  qwen_image_2.1_turbo_int8_convrot.safetensors  6.76 GiB (7256787829 bytes)  -> /home/user/wt/p4-9-evidence/fake/models/diffusion_models  (from https://huggingface.co/Comfy-Org/Qwen-Image-2.1/resolve/aacf31a6.../diffusion_models/qwen_image_2.1_turbo_int8_convrot.safetensors, SHA-256 8144a018...)
  qwen3vl_8b_int8_convrot.safetensors  8.71 GiB (9350798360 bytes)  -> .../text_encoders  (from https://huggingface.co/Comfy-Org/Qwen-Image-2.1/resolve/aacf31a6.../text_encoders/qwen3vl_8b_int8_convrot.safetensors, SHA-256 8bfd0f6e...)
  qwen_image_2.1_vae_bf16.safetensors  0.63 GiB (675509688 bytes)  -> .../vae  (from https://huggingface.co/Comfy-Org/Qwen-Image-2.1/resolve/aacf31a6.../vae/qwen_image_2.1_vae_bf16.safetensors, SHA-256 bb21f747...)
Total: 16.10 GiB (17283095877 bytes); free space: 21.67 GiB (23265157120 bytes), and 1.00 GiB (1073741824 bytes) more is kept free as a margin.
Nothing has been written. ComfyUI is not restarted and nothing else on it is changed.
To download exactly this, run: astrid generate fetch-models qwen-image-2.1-turbo t2i --comfy-url http://127.0.0.1:8188 --apply e5c37dcac172ab8f98a45a3f8422170ce9cb4e88dad95b0330c0b37d9720af6d
```
(Full URLs and hashes are in `out-A5-plan.txt`.) The plan digest is `e5c37dcac172ab8f98a45a3f8422170ce9cb4e88dad95b0330c0b37d9720af6d`.

## 3. Run B (the person's saved workflow)
Start 15:38:21Z.

| # | Command | Start | Outcome |
|---|---|---|---|
| B1 | `curl -fsS "http://127.0.0.1:8188/userdata/workflows%2Fmy_portrait_custom.json" -o workB/workflow.json` | 15:38:21 | ok |
| B2 | `L generate describe workB/workflow.json --placement http://127.0.0.1:8188` | 15:38:22 | exit 0: inputs `model`, `seed` (default null), `node:3.filename_prefix`. (Walk 1: no `seed`, P4.0.7.) |
| B3 | `L generate workflow workB/workflow.json --placement http://127.0.0.1:8188 --inputs-json workB/inputs.json --json` (`{"model": "tiny-cpu-test.safetensors"}`) | 15:38:44 | **admitted: `POST /prompt` 338 bytes**, `succeeded`, `open_url` present (same project URL). Posted node 2: `AstridCustomSampler {"cfg": 1.0, "model": ["1", 0], "seed": 232778650, "steps": 4}`. **Seed is not 7.** Result `seed_used: 0`. |
| B4 | same with `{"seed": 7}` in inputs | 15:38:55 | exit 2, `status: blocked`, `code: input_rejected`, `message: unsupported entry inputs: seed` (describe in B2 had listed `seed`). |
| C1 | `L generate workflow workB/workflow.json --as-entry p49-my-portrait --dry-run --json` | 15:39:20 | `would_save_entry: p49-my-portrait`, `written: false`; inputs `model`, `node:3.filename_prefix` (no `seed`, unlike B2). |
| C2 | `L generate workflow workB/workflow.json --as-entry p49-my-portrait --no-run` | 15:39:20 | `{"entry": "p49-my-portrait", "ran": false, "replaced": false, "saved": true}`. **Wall time 7.76 s** (`wall-asentry.txt`). |

The pin step (`defaults set`) after C2 was not run (not asked for in the brief).

## 4. Minutes and command counts, against walk 1

| | Walk 1 (Run A, user's workflow) | Walk 2 Run A (default) | Walk 2 Run B (saved workflow) |
|---|---|---|---|
| First skill step to admission, measured | about 4 min (12:17:36 to 12:21:56) | 15.3 min (15:22:06 to ~15:37:22), of which ~14 min is P4.9.1 | about 0.5 min (15:38:21 to ~15:38:45) |
| Same, without the P4.9.1 wedge (estimate, not measured) | - | about 1.5 min (task created 15:23:34; the first A6 would have admitted within seconds) | - |
| Skill-path commands, clean path | 21 | 6 (defaults, targets, scan, settings set, fetch-models plan, image); +1 for the apply, which was not run | 3 (curl, describe, workflow) |
| Skill-path commands, as issued | 21 | 11 Astrid calls (A1-A5a, A5, A6, A6b, A6c, A6d, A6e), plus about 8 diagnostic commands | 3 |

Walk 1's 21 commands included `--as-entry` dry-run, `settings checkout/checkin`, a failed `--inputs` guess, project creation and the `pip install`; walk 2 needed none of those (project auto-created, `settings set` is one command, vibecomfy was pre-registered).

## 5. Places the skill made me guess (skill line quoted)
1. "Run every Astrid command ... through the launcher. It needs no PATH entry." and the `run-astrid` path. No installer ran here, so I used `L`. Not a skill gap, a sandbox one.
2. "If their ComfyUI is not running, ask the user to start it." Not needed.
3. "If its models are missing from their ComfyUI, show the download plan." The `defaults` output said `ready: true, required model roles present (model bytes unverified)` with empty model folders. I could not tell "missing" from that output; I ran the plan on the task's say-so. See P4.9.3.
4. "`generate fetch-models ENTRY t2i --comfy-url URL`": `t2i` is the mode, never named. I read it from the slot `image.t2i`. Fine, but unstated.
5. "`--inputs-json /absolute/path/inputs.json`": the skill never says what goes in the file. I used `{"prompt": "a lighthouse keeper"}` (from walk 1) and `{"model": "tiny-cpu-test.safetensors"}`; for the saved workflow the needed `model` input only shows in `describe`.
6. "its saved seed is kept": the skill promises the saved seed; it was not kept (P4.9.4).
7. "WORKFLOW ... the workflow's scan name": the scan name here was `my_portrait_custom.json`; the skill says to percent-encode it, fine. `workflows_detail.modified` is null in the fake, so "most recently edited first" could not be checked.
8. Setup step 4 says `generate scan --json` after `targets`; the generation skill step 2 runs the scan first. Order differs between the two skills (harmless).
9. "`--placement URL`" is shown for the saved-workflow commands but not for `generate image`; both worked (placement resolves from discovery or settings).

## 6. Walk-1 findings
- P4.0.1 (no checkout route in the skill): not changed, still present for a source checkout (the skill's only install line is `curl ... | sh`); not reachable here.
- P4.0.3 (proxy 403): not reachable, installer not run.
- P4.0.4 (no `run-astrid`): not reachable (no installer).
- P4.0.5 (preinstall script from `main`): still present in the skill text (step 1).
- P4.0.6 (`--help` census lists only `generate image`/`video`): still present; `--help` Generation block shows `generate image`, `generate video` only.
- P4.0.7 (`describe` ignored custom node inputs): partly fixed. With `--placement`, describe now lists `seed` (B2). But `--as-entry --dry-run` (C1) still omits it, and the run rejects it (B4); see P4.9.4.
- P4.0.8 (nvidia-smi check): not reached.
- P4.0.9 (egg-info in the checkout): `astrid.egg-info/` and `__pycache__/` are present in the checkout (ignored). I did not create them (pre-existing from the manager's build); same nuisance.
- P4.0.11 (data root): still needed `ASTRID_RUNTIME_DATA_ROOT`; not retested without it.
- P4.0.12 (source profile): still needed a hand-made source-profile JSON for `workspace create`.
- P4.0.13 (`packages:missing=vibecomfy`): worked around the same way (pre-registered); not retested without.
- P4.0.14 (no project): fixed. A project "My first project" was created by the first `generate image`, and the one-line notice `Created and selected project "My first project" for this generation.` printed once.
- P4.0.15 (needs `--placement`): fixed for the settings route: `generate image` ran without `--placement` (A6d/A6e) after A4 (and discovery already resolved the same endpoint before it).
- P4.0.16 (`location: local`, `owner: human` labels): still present (A2).
- P4.0.17 (`control_after_generate` shape): the fake uses the stock shape (option on `seed`); dry-run is `ready` and the run admits. Whether a real ComfyUI matches is for Plan 34.
- P4.0.18 (saved seed 7 lost): still present, see P4.9.4.
- P4.0.19, P4.0.20, P4.0.21 (fake artifacts): fixed in the fake. P4.0.25, P4.0.26 (older ComfyUI, release endpoints): not reached; the fake serves core nodes and 200 on `/queue` and `/api/free`.
- P4.0.22-24 (installer): not reachable.
- `open_url` after a finished generation: present in both runs. The skill's last step ("Give that link once, and say: the new image is in the gallery at the bottom of the editor (the "Open Gallery" tab)") is text in the skill; the CLI result carries only the URL, not the sentence.

## 7. New findings
- **P4.9.1 A stale temp directory from another Astrid run wedges the pack host silently, so every generation sits `queued` forever.** Evidence: A6/A6b/A6c: `[10s] queued waiting=-; current executor occupancy: registered host occupancy is unavailable or reports no active task`, then `Still following task ...: [4m 0s] queued`. Cause (found by running the host in the foreground with `faulthandler`, `host-once.out`): `generic_host.py` `_recover_terminal_requests` (line ~14202) scans `Path(tempfile.gettempdir()).glob("astrid-attempt-*")` when no attempt root is set, finds `/tmp/astrid-attempt-cp95sr10/fail-request.json` (left by walk 1's failed run at 12:21:55, a different realm), and loops forever on `self.client.task(...)` for a task this Runtime does not have (`_shutdown.wait(delay)` retry), before it ever claims work. The host then never polls, `executors.last_seen_at` stays at its registration time (15:28:51), and the Runtime admits new tasks with `waiting_reason = capability_unavailable` (realm.sqlite3). Nothing is logged; the task output says only `waiting=-`. A person whose earlier run crashed, or who has two Astrid installs, would hit this. Fix direction: scope the scan to this realm/support root, skip files whose task is unknown (NotFound) instead of retrying forever, and say so in the log. Workaround: `TMPDIR` pointing at an empty folder (D5); I did not delete walk 1's directory. Costs: about 14 min of this walk.
- **P4.9.2 `astrid-runtime up --wait` cannot run when another Runtime holds door port 17340 and `--hosted-origin off` is refused with `--wait`.** Evidence: `door_port_taken` ... `stop that one first (astrid-runtime down)`; `up --wait requires the browser door; enable --hosted-origin`. Needed `--door-port 17341`. A second realm on one machine is rare; walk 1's leftover Runtime caused it. Minor.
- **P4.9.3 `generate defaults` says `ready: true` for a default whose model files are absent.** Evidence: A1 `image.t2i ... "ready": true, "reason": "required model roles present (model bytes unverified)"` while `GET /models/diffusion_models`, `/models/text_encoders`, `/models/vae` all returned `[]` and the plan (A5) listed 16.10 GiB of missing files. (Walk 1's `list` said `ready: false`.) The skill's "If its models are missing from their ComfyUI, show the download plan" gives the agent no cue; it depends on which command it reads. Not checked here: whether a real ComfyUI's `/object_info` choices produce a `ready: false` (the fake's loaders listed no choices at that moment, so `_resolve_roles` should have failed; I did not read why `defaults` still said ready).
- **P4.9.4 The saved workflow's seed is not kept, and `seed` is offered by `describe` but refused by the run.** Evidence: B3 posted `seed: 232778650` for a saved `widgets_values [7, "fixed", 4, 1.0]` (`seed_used: 0`); B4 `{"seed": 7}` -> `unsupported entry inputs: seed`; C1 dry-run inputs omit `seed` while B2 lists it. Code: `prepare_execution_bindings(saved_ui=True)` keeps the seed only if `node.inputs.get("control_after_generate") == "fixed"` (`entries.py:897-905`), but the converted node (posted prompt) has no `control_after_generate` input, because the schema declares it as an option of `seed` (stock ComfyUI shape, from my knowledge of `/object_info`; not verified against a real server). So the skill's "its saved seed is kept" does not hold for this shape. Same as P4.0.18.
- **P4.9.5 The first `generate image` is the only place the project notice appears and it comes before the JSON.** Evidence: line 1 of `out-A6a-...`: `Created and selected project "My first project" for this generation.`; later runs print nothing. It was in the same stream as `--json` output, so a JSON parser on that output would trip on the first line. Minor; the notice went to the mixed `2>&1` capture, so I cannot say which stream.
- P4.9.6 (fake note, not a product finding) A first fake whose `/object_info` ignored the empty folders made `fetch-models` print a header and `Nothing can be downloaded.` with no files (A5a). With a real ComfyUI the lists follow the folders.

## 8. What still needs Plan 34's real run
- A real ComfyUI: `/object_info` shapes (`control_after_generate`, loader choices), `/models`, `/internal/folder_paths`, `/userdata` with real `modified` times, `/history`, `/queue`, `/api/free`, and the real image output.
- A real `fetch-models --apply` from huggingface.co (16.10 GiB; hash check, hard-link, atomic rename, free-space check, the non-writable folder refusal). Not run here.
- The real installer (`run-astrid`, tools stage, PyPI/GitHub downloads), the astrid.haus "Connected" check and the editor opening `open_url`.
- A second Astrid on the same machine (P4.9.1, P4.9.2) and a clean `/tmp`.
- `nvidia-smi`, managed engine and RunPod paths: not reached; nothing remote was called.

Servers stopped at the end: the fake (port 8188), this walk's Runtime (`astrid-runtime down`) and its pack host. Walk 1's Runtime (pid 9143) and host (pid 21539) are still running; I did not touch them. `/tmp/astrid-attempt-cp95sr10` (walk 1's leftover) is untouched.
