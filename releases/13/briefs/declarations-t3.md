difficulty: sol (S); full access; use Luna sub-agents

# T2+T3: one model-declaration shape, everywhere; the music template fixed; the 37 legacy templates migrated or unlisted; the corpus check green

**Repo:** VibeComfy. **Clone:** `/home/user/wt/c-vcmusic` (branch `r13/music-declaration` from `r13/models-root` `e4118ccf`). It already holds an uncommitted diff from the previous worker: the music template fixed, a regression test in `tests/test_models_root_resolution.py`, and a corpus check in `tests/test_ready_templates.py`. Continue from it. Astrid, read-only: `/home/user/wt/c-b6`.

**Use your Luna sub-agents** for the per-template work (reading source workflows, classifying each asset), call-site searches and running checks, in parallel. Keep your own effort for the design and judgment.

## Design (decided)
- **One record everywhere:** `{name, subdir, url, sha256, size_bytes}`, relative to the models directory. `target_path` stays only for files that live inside a custom-node pack.
  - Today there are five shapes: bare filename strings in templates; `{name,url,directory}` in source JSON; `{name,url,subdir}` in `model_assets.py` about 500-547; `{path,destination,bytes,sha256}` in Astrid's `packs/runpod/models.lock.json`; and `target_path`.
  - Make preparation accept exactly the one record; a bare string or a missing `subdir` refuses with a clear message.
- **No silent guess.** `model_assets.py` about 547 ends in `_CLASS_TYPE_SUBDIRS.get(class_type, "checkpoints")`; delete the `checkpoints` default so an unknown placement refuses.
  - Derivation from the consuming node is allowed only when a template is authored or ported, where a person sees the result. Never at preparation.
- **Migrate the 37 templates with filename-only requirements, without guessing,** in this order:
  1. Regenerate from the source workflow's `properties.models` where the record exists (`porting/convert.py` about 791-824 preserves it).
  2. Else take placement from VibeComfy's model registry entries (`registry/models_loader.py` about 44-80).
  3. Anything left is no longer listed as ready (say exactly how ready status is expressed) until a person declares it.
  - `audio/hunyuan_foley_v2a` (the SFX cell's template) is among the 37: make sure it ends fully declared, and say how.
- **The corpus check passes with NO allowlist.**
- **Astrid's lock:** report, don't change. Say how Astrid's lock row should become the same record (`destination` = `subdir/name`), with exact file:line, for a follow-up Astrid task.

## Suites
- The template, ready-template, model-assets, fetch and prepared tests, plus `tests/test_models_root_resolution.py`. Compare against `e4118ccf` and report differences only. Pre-existing failures: the template index, frame-count binding and packaged-install helper tests.
- Python `/home/user/astrid-agent.env/venv/bin/python`, `PYTHONPATH="$PWD"`.
- List every template changed and every template unlisted, with the reason.

## Rules (verbatim, all apply)
- do not push or commit;
- never weaken, skip or delete a test;
- no RunPod or paid services; package registries, GitHub and Hugging Face reads are allowed;
- no `.env`, credential files or ~/.codex;
- start no long-lived services (loopback test servers inside tests are fine);
- if /tmp is not writable, use `TMPDIR=$PWD/.tmp-tests` and delete it afterwards;
- ruff must not rise (Astrid only);
- no AI model or product names;
- stop after three failed attempts;
- Python `/home/user/astrid-agent.env/venv/bin/python` with `PYTHONPATH as stated in this brief`;
- other Codex workers run in parallel on this machine, so use your own `TMPDIR` under your clone for pytest (`--basetemp=$PWD/.tmp-tests/pt`) and delete it at the end;
- return the diff and the before/after test results.

## Manager review of pass 1 (continue from the working-tree diff in c-vcmusic; don't start over)
Pass 1 is good: 30 templates declared, 18 moved to drafts, the corpus check green with no allowlist, and the SFX and music templates fully declared. Finish:
1. **The two emitter regressions.**
   - `tests/test_porting_emitter.py::test_canonical_emitter_rebuild_preserves_exact_materialized_input_alias[video/ltx2_3_i2v]` ("canonical first-build semantic digest differs from admitted candidate"): find the cause. Your declaration change probably altered the emitted canonical output, so the admitted candidate digest needs regenerating with the repository's own tooling, not a hand-edited literal. Say which.
   - `test_canonical_emitter_does_not_infer_over_retained_motion_prompt_target`: it resolves `video/ltx2_3_runexx_motion_transfer_dwpose` through ready discovery, but that template is now a draft. Point the test at the draft location or a fixture while keeping every assertion, and explain.
2. **An Astrid dependency on an unlisted template.** Astrid's catalog uses `video/ltx2_3_runexx_first_last_frame` (Astrid `astrid/core/model_catalog/models.yaml:841`, `astrid/packs/vibecomfy/src/dimensional_ltx.py:21`) for LTX 2.3's `flf` mode.
   - Try hard to declare that template's models from a real source: the LTX model registry entries, the source workflow, or the HF repos the LTX ready templates already declare.
   - If it truly cannot be declared, leave it a draft and write the exact Astrid change in `astrid-follow-up.txt`: the `flf` mode shows as unavailable, with the reason. Don't touch Astrid.
3. Run the suites once more and report the counts against `e4118ccf`.

**Explicit rule (12 Nov):** you must not call `api.runpod.io`, `rest.runpod.io` or any RunPod endpoint, and must not run any `astrid generate` or `astrid machines` command. The network proxy would act on a real paid account.
