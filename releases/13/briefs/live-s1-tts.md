# Fix: TTS fails loading its model (transformers 5 config attribute)

You are a Codex worker with full access. Deploy Luna sub-agents (as many as are useful) for all reading, searching and mechanical checks. You judge and write the fix.

## What happened (live, Release 13 Stage 1, RunPod RTX 5090, 12 Nov 15:56 UTC)
The TTS cell (Qwen3 TTS CustomVoice 0.6B through the `ComfyUI-QwenTTS` custom node, `AILab_Qwen3TTSCustomVoice`) prepared fine. Node restore and the existing declared patch passed. It then failed when the node loaded its model:
```
AttributeError: 'Qwen3TTSTalkerConfig' object has no attribute 'pad_token_id'
  ComfyUI-QwenTTS/AILab_QwenTTS.py:572 _custom_voice_generate -> _load_model("CustomVoice", ...)
```
The engine runs `transformers==5.22.1`, from Astrid's lock `astrid/packs/runpod/requirements.linux-cu130.lock:3498`. The node's pin is in `astrid/packs/runpod/pins.json` (`comfyui-qwentts`) and in the recipe `recipe.linux-cu130.json`.
The full failure bundle is in `/home/user/wt/briefs/wave3/live-s1/tts-failure/` (`logs/engine-error.json` has the traceback). Earlier work: Astrid declares recipe source patches to VibeComfy (Astrid `dd5bc822`, VibeComfy `c7a47e36`). The QwenTTS node already has one declared patch, so reuse that mechanism; don't invent another.

## Your clones
- Astrid: `/home/user/wt/c-ttsfix-ag`, branch `r13/ttsfix-ag` at `f9214240` (the Stage 1 candidate).
- VibeComfy: `/home/user/wt/c-ttsfix-vc`, branch `r13/ttsfix-vc` at `a8a7be7c`, if the change needs VibeComfy.

## Outcome
1. **The cause, named:** which code reads `pad_token_id` from that config, why transformers 5 no longer supplies it, and where the node's bundled config class should define it.
2. **One structural fix, chosen in this order:**
   1. **An upstream node commit that supports transformers 5.** Check the node's upstream history. If one exists, re-pin the node to it.
   2. **Otherwise, extend the node's existing declared patch,** so the bundled config sets the attribute, matching what upstream transformers 4 used to default.

   Don't downgrade transformers for the whole engine: other nodes in the same environment rely on 5.x. If you believe a downgrade is right after all, stop and report why.
3. **A CPU proof with no weights:** with `transformers==5.22.1` installed in a throwaway venv under your clone, construct the node's bundled talker config, and follow the same attribute path `_load_model` uses as far as it goes without weights. It shows the `AttributeError` before the fix and none after. Make it a test in the repository that owns the patch, if the patch mechanism has a test home; otherwise a script under `tests/` that the test collects.
4. **Check for the same class of break elsewhere.** List any other config attribute the node, or the rest of the node's model code, reads that transformers 5 dropped. Fix it in the same patch, so the next GPU run doesn't find the next missing attribute.

## Proof
- The CPU proof fails before and passes after.
- The test files of the declared-patch mechanism and pins checks pass, with no new failures against the base. Name them: in Astrid, `tests/` files that cover `pins.json`, the recipe and declared patches; in VibeComfy, the patch tests.
- Ruff in Astrid does not rise: `python -m scripts.reshape.compare_ruff_baseline`, baseline 2117.

## Rules
- Do not commit or push. Leave changes in the working trees.
- Never weaken, skip or delete a test. If an existing test pins the old behaviour on purpose, stop and report it.
- **No RunPod or paid services of any kind:** no calls to api.runpod.io, rest.runpod.io or any RunPod endpoint, no `astrid generate`, no `astrid machines`. The network proxy injects a real key, so a call spends real money. Package registries, GitHub and Hugging Face reads are allowed; config JSON from Hugging Face is fine, weights are not needed.
- No `.env`, credential files or `~/.codex`.
- **No full test suites,** only named test files. The machine has 4 CPUs shared with other workers, and about 3.5 GB of disk is free. Keep the throwaway venv small and delete it at the end. Use `TMPDIR=$PWD/.tmp-tests`.
- Python for repository tests: `/home/user/astrid-agent.env/venv/bin/python` with `PYTHONPATH=$PWD`.
- No AI model or product names in code or comments. Stop after three failed attempts at the same thing, and report.

## Return
The cause in two sentences, which fix path you took and why, the diff summary for each repository, before and after results, and the list from outcome 4.
