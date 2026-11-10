# Plan 34 handoff — first GPU run, 10 November 2026

> **Superseded in part (10 Nov 2026, Hannah):** the generation work is now in **Release 12**, not a Release 13. Don't wait for Release 12 to publish, and don't treat the runner freeze as a stop: follow [releases/12.md](../../releases/12.md) and your tasks in [Track B](../../releases/12/generation.md)]. Where this file says "after release 12", "release 13" or "freeze", the release plan wins; everything else here stands.

## Goal and safe stopping point

Complete the first [full GPU validation](../../skills/astrid-dev-gpu-validate/SKILL.md): every default generation slot and h3_av, including RunPod HTTPS, local-managed on a pod, and the GPU-only checks. This run is **partial, not release qualification**. The owner directed packaging for another machine; start no new rentals during packaging. All 18 rented pods have been released. Independent final census at 16:41:15 UTC was empty.

Evidence branch was pushed at `1874afa`; the source of live results, every attempt/pod, focused fix proofs and artifact hashes is [evidence PR #260](https://github.com/banodoco/astrid-dev/pull/260), [run record](https://github.com/banodoco/astrid-dev/blob/plan34/gpu-validation-2026-11-10/validation/gpu/2026-11-10-cc084ebd9.md). Do not infer a GPU pass from a CPU fix, a successful install or a capacity claim.

## Recovery revisions

All SHAs below are Agent commits unless marked otherwise. The four candidate branches listed below are pushed. The packaging lead audited every owned clone/worktree with `git log --branches --not --remotes --oneline`; none had remaining unpushed commits. Never push `main` or `int/**`, and never force-push.

| Role | Exact revision | Recovery branch / status |
| --- | --- | --- |
| Launch base (Plan 32 last product change) | `cc084ebd9cf8d90d417ff302865d747652902390` | Original run identity |
| Final image proof | `26eeaff4f90fc5b91e25e0769477a9081deee5d3` | Exact successful image candidate |
| Latest fetched Plan 32 tracking head | `99724131d2c3eff11867a189986c4ba147e5a81b` | Test-only change relative to image candidate; no paid rerun required |
| TTS prompt integration donor | `37fb20008d49bb3402f82f02f727e03f60dc5101` | Contains prompt repair |
| Warm-receipt repair | `89d138765184d058fd05d77568a27fcc97268cde` | `plan34/fix-warm-receipt`; CPU proof, GPU reuse pending |
| Music / warm integration | `e9cb9e6b9bd54882375fa6413987630c8dbfd38f` | `plan34/candidate-e9cb9e6b9` |
| Plan 40 capacity donor | `0d50b1cf1b39f7e3e8b4f30e085e9135dc883053` | T6 waiting capacity |
| Capacity integration | `4367cc5e04776f354726696b20e000886909d27b` | `plan34/candidate-4367cc5e0`; live wait/claim proof |
| Safe failure diagnostics | `e0d95d7b859bd2e8d6f83124b4bc7f2828eb5c49` | `plan34/fix-failure-diagnostics` (fix N) |
| Diagnostics integration | `69d8cbc552211e4065bd4047e3859dea2ca049cd` | `plan34/candidate-69d8cbc55`; failed TTS and SFX attempts |
| Video T5-R1 donor | `c8f56c5829e5b5a4e7e8b09e12466a4e3916feb9` | Plan 40 GPU placement recovery guard repair |
| Video integration | `17acda421195bdd7e56ccacd5cf5718ba3c95030` | `plan34/candidate-17acda421`; 182 focused checks, no paid video inference |
| TTS prompt repair | `3f10f3b653cfab88c090d84e9d380e3be7fc6497` | `plan34/fix-tts-prompt`; included via integration donor |
| Runtime pin | `4f5477cb0f5b03d28bec991a1fe34edcd8fc309f` | Existing tested candidate pin |
| VibeComfy baseline | `e65f4941d09b1cb4d1dd5aae6171c73e648706f4` | Actual pod source on last SFX attempt |
| VibeComfy SFX repair | `af5cb429bb43b405ed8780e760760a645c7c3920` | [VibeComfy PR #166](https://github.com/banodoco/VibeComfy/pull/166); CPU-proven, GPU proof pending |
| runpod-lifecycle pin | `f2948817eeb94af8dee76be21f6d673724f1606e` | Existing tested candidate pin |

Earlier repair branches and their exact revisions are recorded once in PR #260. `plan34/candidate-sfx-af5` is pushed at `69d8cbc552211e4065bd4047e3859dea2ca049cd`; its controller manifest override was not an Agent source change, and the branch alone does not align the engine recipe. It is not a qualified af5cb429 GPU candidate. Plan 40 T9 has no accepted donor SHA yet.

## Task state and completed proof

| Task | State and remaining claim |
| --- | --- |
| G1 | Partial/deviation: orchestrator explicitly folded smoke into product G1/G2 because there was no prepare-only route. No isolated direct-VibeComfy smoke per slot is proved. |
| G2 | Partial: image.t2i, image.edit and audio.music passed real RunPod HTTPS inference. TTS and SFX failed; video and actual Matrix h3_av remain unrun. Separate local-managed and attached coverage remains unproved. |
| G3 | In progress: recorded and routed failures have CPU-tested pushed repairs; TTS root cause remains unknown and depends on Plan 40 T9 diagnostics. SFX repair needs consistent pins and GPU verification. |
| G4 | Not started: a complete second pass on a fixed integrated candidate remains due. |
| G5 | Not proved: checked models root equals fetch destination; second-pod volume reuse with zero fetch; immediate post-start polling; hundreds-of-MB HTTPS output. Same-pod warm reuse after its receipt repair is also not yet proved. |

Successful artifacts and exact task IDs are in the run record. Image t2i/edit passed on `26eeaff4`; music passed on `e9cb9e6b9`. The successful music MP3 passed ffprobe and full ffmpeg decoding. T6 was live-proven: one waiting SFX command acquired after two creates. Its subsequent doctor failure does not negate capacity wait/claim proof.

TTS on `69d8cbc55` failed with safe `category=input; code=input_rejected`; the exact rejected field is unknown. CPU capsule/binding validation and graph compilation did not reproduce it. SFX on the manifest-only af5 candidate failed `category=integrity; code=integrity_failed`; the pin mismatch is a likely cause, **not proved**. Both exact pods were released with GET404, account-list absence and empty census recorded.

## Budget and custody

The original balance was **$105.6454141266**. Final independently verified GraphQL balance at **2026-11-10 16:41:15 UTC** was **$102.5117504166**, an observed difference of **$3.1336637100**, including background storage and subject to billing lag; pods were `[]`. Do not reset the budget on the new machine: the whole run has a $24 cap and must stop renting/release everything at $20 observed spend.

Owner-approved static split: TTS $3, SFX $3, video $6 total across i2v/v2v/edit, total new exposure $12. Recalculate against the final original-to-current balance before any rental. Each isolated root owns its ledger/journal and watches only its own exact pod IDs; census before/after every rental. An unowned pod stops new claims and is reported; never release another owner's pod. No joint reservation is required by the owner's static-split decision.

## Exact next actions on the new machine

1. Enter through [Astrid contributor skill](../../skills/astrid-dev/SKILL.md), [GPU validation skill](../../skills/astrid-dev-gpu-validate/SKILL.md), and the [run contract](../../skills/astrid-dev-shared/run-contract.md). Read the committed record and the handoff PR, reconstruct isolated installed program versions and journals, and obtain `RUNPOD_API_KEY` without printing or writing its value. Fetch `origin int/32-one-generation-path` before every new paid cell; inspect moved code paths and rerun a passed cell only when affected.
2. Resume video on `plan34/candidate-17acda421`, one waiting generate at a time. Use committed, explicitly synthetic fixtures/request maps from PR #260; they cannot substitute for the requested actual Matrix excerpt (80.886–83.305 s). Their committed path is `validation/gpu/fixtures/plan34-synthetic` on the evidence branch; its README constructs portable request/asset-map inputs. Minimum observed video sizing: 32 GB GPU, approximately 53.5 GB model storage; choose a sufficient GPU without a geography filter.
3. Wait for the accepted Plan 40 **T9** SHA, merge it with fix N into a pushed candidate, then run TTS once. T9 owns keep-on-failure and a bounded allowlisted failure summary. The abandoned separate fix P must not be revived. If failure leaves the pod idle, inspect privately via the product's HTTPS machine access; record only exception class, stage, node/class, field/constraint. Release explicitly through `astrid machines release` within consented idle/paid limits. Never retain raw prompts, URLs, logs, stdout or keys.
4. Build a new SFX candidate with **both** install manifest and engine recipe pinned to VibeComfy `af5cb429bb43b405ed8780e760760a645c7c3920`. Verify bootstrapped pod VibeComfy HEAD is af5 before generation. `astrid/packs/runpod/managed_sources.py:43-50` reads `engine_recipe.load_recipe("comfyui", "linux-x86_64-cu130")`, whose Vibe pin is `astrid/packs/vibecomfy/pins.json:10`; also audit `astrid/packs/runpod/pins.json:15`. The last manifest-only attempt bootstrapped e65, so PR #166 is **not GPU-proven**. The attempted installer override was generated as `sfx-install-manifest.json` with its pin at JSON field `vibecomfy.sha` (line 119); the installer consumed it via `run-astrid install --manifest`. That generated local file is not a committed release manifest; reconstruct the override from a trusted current manifest, using the pinned revisions in the [SFX audit](https://github.com/banodoco/astrid-dev/blob/plan34/gpu-validation-2026-11-10/validation/gpu/2026-11-10-sfx-candidate.md).
5. Complete the remaining matrix and G5 cells, record exact revisions/output identity and release proof per cell. Reconcile every owned pod and account balance, update PR #260, then seek the required final review; do not claim qualification from this handoff.

Each cell uses **one waiting product command**, with no outer capacity rotation, geographic restriction, deadline or capacity timeout. The concrete invocation shape is below; create each JSON request from committed fixtures and obtain slot/mode names from the exact installed `astrid generate defaults --json` and `--help`. The per-cell caps are ceilings within the static split, not fresh budgets:

```sh
astrid generate video --entry h3 --mode i2v --inputs-json i2v.inputs.json --placement runpod --gpu 'RTX A6000' --consent paid --max-usd 3 --max-hourly-usd 1.2
astrid generate video --entry h3 --mode v2v --inputs-json v2v.inputs.json --placement runpod --gpu 'RTX A6000' --consent paid --max-usd 3 --max-hourly-usd 1.2
astrid generate video --entry h3 --mode video-edit --inputs-json video-edit.inputs.json --placement runpod --gpu 'RTX A6000' --consent paid --max-usd 3 --max-hourly-usd 1.2
astrid generate audio 'Hello from Astrid.' --entry audio/qwen3_tts_custom_voice --mode tts --placement runpod --gpu 'RTX 3090' --consent paid --max-usd 3 --max-hourly-usd 1.2
astrid generate audio --prompt 'Natural sounds matching the video.' --video-ref validation/gpu/fixtures/plan34-synthetic/synthetic-source.mp4 --entry audio/hunyuan_video_foley --mode sfx --placement runpod --gpu 'RTX 3090' --consent paid --max-usd 3 --max-hourly-usd 1.2
```

An inputs JSON for video contains `request` (the request file) and `asset_map` (asset IDs to fixture paths). Explicit mode is required; video defaults to v2v. Before running the three video commands, divide the aggregate $6 across the sequence in the root ledger; three independent $3 reservations would exceed that allocation. Use HTTPS only; SSH TCP22 is blocked. Do not use `h3_release.py`'s default SSH transport.

Focused CPU/integration proof to resume on the checkout (use the shared [worker environment](../../env/README.md), not an unavailable former-machine wrapper):

```sh
python -m pytest tests/integrations/test_dry_run_equals_live_run.py -m gpu
python -m pytest tests/core/generation/test_engine_recipe.py tests/core/generation/test_engine_cli.py
python scripts/check_docs.py
```

The requested audio/sfx and audio/tts GPU selectors currently collect no GPU cases (13 deselected); that is a coverage gap, not a pass. Reconcile the exact test inventory with the incoming T9 task and the run record rather than running the full suite speculatively.

## Reviews, owner decisions and follow-ups

Consequential fixes used a Terra critic: warm receipt re-checkpoint, prompt alias, safe failure diagnostics and the source-identity contract. The record contains their focused proof and accepted findings. TTS prompt repair has 10 new tests and SDK parity; diagnostics has 24 checks including a real CLI sentinel. Video integration had 182 focused checks. No final Plan 34 release review has been consumed or passed; the prior per-fix reviews do not satisfy it. A fresh reviewer must verify all incoming integration SHAs and paid evidence.

The orchestrator relayed these owner decisions on 10 November: product bootstrap rather than adapting retired `pod_session.py` (Plan 14 / astrid-dev #262); combined G1/G2 deviation; one waiting product generate without geography/deadline filters; static split above; Plan 40 T9 supersedes fix P; package now with no new rentals. Their durable authority is this handoff PR plus the corresponding run-record entries; local mailbox state is not required for recovery.

Follow-ups for filing/routing, not new work authorized by packaging:

- **Plan 29 (release/pins):** install manifest and engine recipe duplicate the VibeComfy pin and can silently disagree. Derive one from the other or enforce consistency at install. Include actual pod HEAD in qualification.
- **Plan 40 T9:** keep a failed job idle within consented limits and expose the bounded safe failure summary; donor pending. TTS GPU cause remains unresolved until that evidence exists.
- **Runtime:** orphaned isolated no-pod task after sandbox interruption stayed running in the task DB; cancellation/down did not reconcile it. Preserve facts and retire unused ledger reservation; no fabricated cleanup. This is not yet reproduced outside the sandbox child-process behavior.
- **Plan 20 P3.1:** fresh settings lack usable RunPod placement/default GPU onboarding; already routed.
- **GPU proof:** complete G1 isolation or obtain a durable explicit scope decision, local-managed/attached coverage, warm-volume second-pod zero-fetch, exact models-root proof, poll-after-start and large HTTPS artifact.
- **Test coverage:** restore executable GPU-marked audio/sfx and audio/tts parity cells; CPU deselection proves no GPU behavior.
- **H3 fixture:** acquire the actual requested Matrix excerpt through an authorized source; synthetic media is labelled and useful only for separate flow validation.

The attempted install-manifest was generated for this candidate and is reconstructed as described above; the committed SFX audit records the actual versions. Audio CLI forms above match the attempted product commands; T9 may change its optional diagnostic flags, so inspect its help before the TTS rerun.
