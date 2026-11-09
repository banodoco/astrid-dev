# Tasks — Pack extension points: switch on the protocol and prove it

[Plan](plan.md) · [Inputs](inputs.md) · [Project status and owner](../../README.md)

Routes: `N` is the default, `X` very hard, `S` super hard ([run contract](../../skills/astrid-dev-shared/run-contract.md#routing-and-bindings)). An `X` lead delegates reading, mechanical edits and running checks to `N` helpers.

**Rules for every task:**
- Base: phase 1 (V rows, IMG's standalone half) starts from VibeComfy's pin once Plan 32 T6b-2 has fixed the `vibecomfy.workflows` shape. Phase 2 starts from [Plan 32](../32-generation-placement-targets/plan.md)'s landed Agent head after T6b, which already declares the `generation.engine`, `generation.machine` and `vibecomfy.workflows` points and allows `side: agent`. The poms_packs base is `main` after [Plan 06](../06-packs/plan.md). Record both SHAs in [inputs.md](inputs.md) before P1.
- Line numbers below are at Agent `5eac07e3f` (P rows) and Agent `ff40f2c68` or VibeComfy `e65f494` (the family rows, 9 Nov); re-check them on the base.
- **CPU only:** the live runs of IMG, S2 and h3 are [Plan 34](../34-real-gpu-proof/plan.md)'s.
- Run only the named selectors, using `PYT` and `PYT_POD` from [Plan 33's tasks](../33-unblock-live-generation/tasks.md).
- Add no version ranges, priorities, point inheritance or per-contribution or per-variant trust (see the plan's Deferred list). Raising `vibecomfy.workflows` to `version: 2, min_supported: 1` uses the existing fields and is in scope (A1). **Entry-point discovery is now in scope (owner, 9 Nov), but only for pinned distributions:** Astrid loads `load_plugins(only=<pinned dists>, drop_ins=False)` and lists unpinned entry points without loading them.
- Start only on the owner's go.

Phase 1 is VibeComfy alone; phase 2 is Astrid. Estimate: about 15–18 days (inferred): phase 1 about 7, phase 2 about 9.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| [V1](#v1-the-family-contract-in-vibecomfy) The family contract: `register_workflows`, entries with optional `variants`, `request` and `route`, the family registry with origin, `file` and `file_map` inputs, `needs` as objects, `load_plugins(only=, drop_ins=)` | X | Plan 32 T6b-2's final shape | VibeComfy `vibecomfy/extras.py` (`PluginAPI`, `load_plugins`), `vibecomfy/entries.py` (`_validate`, `load_entry`), new `vibecomfy/families.py` (registry and types only) | New `tests/test_workflow_families.py`: a fixture distribution's entry point registers; strict keys; a variant-less entry is a one-variant family; drop-ins are not executed under `only` | [ ] |
| [V5](#v5-selection-describe-and-the-plan-envelope) Selection, describe, the plan envelope and the refusal shape; VibeComfy's router rules become built-in `image` and `video` families | X | V1 | `vibecomfy/families.py` (`select`, `describe`, `plan_envelope`, `RequestError`), `vibecomfy/router/{_core,_rules}.py`, `vibecomfy/ops/{image,video}.py` (`pick` callers), the `vibecomfy entries` command, and their tests | New `tests/test_family_selection.py` (inline fixture below); `tests/test_router*.py` green against the built-in families; grep: no `register_route(` rule left in `_rules.py` | [ ] |
| V2 `vibecomfy run --entry ID --input k=v --file k=path --files k=@map.json [--variant V] [--dry-run]`; `build` replaces the bundle path before `load_bundle` (`commands/run.py` ~374); media staging lifted from Astrid (`local_server_engine.py:341-355`); `after_outputs` runs on `execute_once()`'s result; `--dry-run` prints V5's envelope | X | V1, V5 | VibeComfy `vibecomfy/commands/run.py`, and its tests | A fake ComfyUI runs a fake family; the dry run names the variant and reason; `after_outputs` rewrites the output; a raise exits 1 | [ ] |
| V3 `vibecomfy.media`: probe (promoted from `runtime/session.py` ~4630), stream coverage, mux, splice, sample digest, and `preserved_outside_mask`, lifted from h3's `compose.py` and `verify.py` (about 400 of its 1,398 lines) | N | none | New VibeComfy `vibecomfy/media.py`, and its tests | lavfi clips and two generated PNGs; `preserved_outside_mask` fails when one unmasked pixel changes | [ ] |
| V4 Authoring docs ("write a family": entry, variants, `when`, route, build, `after_outputs`, describe, dry run) and a release | N | V1–V3, V5 | VibeComfy docs | Docs check; the image family's entry in the docs is the one IMG ships | [ ] |
| [IMG](#img-the-image-family) The image family: txt2img, img2img, inpaint, outpaint behind one entry, as a native plugin plus a thin pack | N | V1–V3, V5 (standalone half); A2, A4 (Astrid half) | New poms_packs `image_family/` (plugin, entry, two new templates, optional `after_outputs`, tests) | Standalone and Astrid dry runs pick each variant with its reason; runs on a fake ComfyUI, local and the RunPod fake | [ ] |
| [P1](#p1-validation-in-the-install-transaction) Extension validation inside the install transaction, plus the owner-dependency rule | X | Plan 32 T6b | `astrid/core/pack/{transaction,validate}.py`, `astrid/core/extensions/registry.py` (call site only), and their tests | New nodes in `tests/core/pack/test_transaction.py` and `tests/core/extensions/test_registry.py`; `tests/core/extensions` green | [ ] |
| [P2](#p2-astrid-packs-extensions) `astrid packs extensions` lists points, contributions and problems | N | Plan 32 T6b | `astrid/core/pack/{cli_parser,cli_inspect}.py`, and their tests | New `tests/core/pack/test_cli_extensions.py` | [ ] |
| A1 The mirror: a thin pack's contribution carries `plugin: {distribution, version, sha256}` instead of `ready_root`; `astrid packs add` installs that exact wheel (a digest mismatch is quarantined); Astrid-pack contributions are forwarded to `register_workflows`; `vibecomfy.workflows` goes to `version: 2, min_supported: 1` with V1's optional fields; T6d's `default_for` moves into an Astrid-only sibling field; `prepare` and `finish` delegate to VibeComfy | S | V1, V2, P1 | `astrid/packs/vibecomfy/extensions/points/workflows.yaml`, the `vibecomfy` pack's contribution loader, `astrid/core/pack/transaction.py` (wheel install step), and their tests | Pinned plugins load; unpinned ones are listed with reason `unpinned` and not loaded; a digest mismatch is refused; a version-1 contribution still loads | [ ] |
| A2 `requirements()` adds `extra.plugins[{dist, version, sha256}]` and `validate_extra` allows it; the machine's `claim` installs the wheel before the pod-side `generate`; `machine_custody` includes plugin digests; installed (non-built-in) packs ship to the pod | X | A1 | Agent generation requirements and the RunPod machine contribution, and their tests | `PYT_POD test_remote_machine_cpu.py`: h3 through the plugin; a warm pod with a different plugin is not reused | [ ] |
| [A4](#a4-family-routing-through-generate) Family routing through `generate`: `list`, `describe` and `--dry-run` project V5's output; `generate image/video` with no entry uses the kind's default family; delete Astrid's mode inference | X | A1, V5, Plan 32 T6d | `astrid/sdk/generation.py` (`_infer_image_mode`, `_infer_video_mode`, `_EXPLICIT_ONLY_IMAGE_MODES`, the default resolution), `astrid/core/generation/{entries,cli}.py` (`describe_entry`, `--variant`, `--input`, `--file`), `astrid/packs/generation/docs/SKILL.md` (one section on families), and their tests | See [A4](#a4-family-routing-through-generate) | [ ] |
| H1 New repo `banodoco/vibecomfy-h3`: the h3-specific code (request v1 and v2, Character Swap, spec, masks, static regions, timing, builders, trios, `measure_h3_source_av`) on `vibecomfy.media`, as distribution `vibecomfy-h3` with entry point `vibecomfy.plugins: h3 = vibecomfy_h3:register`. It declares variants (`source_free`, `source_backed_v2v`, `extension_context`, `character_swap`; `audio_only` is refused as today) with `route` wrapping `branch_for`, puts its planner's timing, trim, previews and ignored fields under the envelope's `details`, and its compose and verify in `after_outputs` returning evidence | X | V1–V3, V5, Plan 32 done | The new repository | The four h3 test files pass; `vibecomfy run --entry h3 --dry-run` on the Matrix fixture names `extension_context` and its reason; the run on a fake ComfyUI | [ ] |
| A3 `h3_av` slimmed to its pin and SKILL; code and the `astrid h3` CLI (`cli.py`) deleted; `describe_entry`'s h3 special case (`entries.py:447`) deleted | N | H1, A2 | `astrid/packs/h3_av/**`, `astrid/core/generation/entries.py` (`describe_entry`) | Generate on local, attached and the RunPod fake; the h3 grep finds only the pin; `astrid h3` is an unknown command | [ ] |
| [S2](#s2-sound-on-video-as-a-native-plugin) Sound on video as a native plugin plus a thin pack: the foley template plus `vibecomfy.media` mux (replaces the earlier Astrid-only P4) | N | V1–V3, A2 | New poms_packs `sound_on_video/` | Standalone and Astrid runs, local and the RunPod fake; ffprobe shows one video and one audio stream | [ ] |
| [P3](#p3-protocol-point-and-family-docs) Protocol, point and family docs | N | P1, P2, A1, A4 | New `docs/packs/extension-points.md`; `docs/packs/{README,creating-packs}.md` (links only) | The repository's docs check; every point and field documented | [ ] |
| C1 Move the run site, bundle staging and media upload into VibeComfy; lift the `_t9_child_dispatch` stub out of `run.py` (follow-up, Plan 32 review, 9 Nov, at 7209ffcc7; Medium) | X | V2, A2 | Agent `astrid/packs/vibecomfy/actions/run/run.py` (1,220 lines; stub at 572-675 and 985-999, which reads an env var, `exec`s a fixture file and imports `astrid.packs.h3_av`), `core/generation/local_job.py:18,66`, `core/execution/machine_run.py:27`, `packs/runpod/machine.py:468,512-513` | The run site, bundle staging and media upload become VibeComfy's (V2 already lifts media staging); the Astrid side keeps a thin call. The h3 CPU stub moves to a test fixture, so no h3 code or `exec` is left on the generic run action. Proof: the Agent run action contains no `h3_av` import and no `exec`; generate on local, attached and the RunPod fake still passes | [ ] |
| R Review rounds (at most 3; Pending owner agreement) | S | all rows above | read-only | Rounds per the [run contract](../../skills/astrid-dev-shared/run-contract.md): findings become rows `R<round>.<n>` added directly below this one, each with route, scope, dependencies and proof; publishing or closing waits for them | [ ] |

**Critical path:** V1 → V5 → V2 → A1 → A2 → A3 → R. V3 runs alongside V1; H1 runs alongside A1 and A2 once V3 and V5 land; P1 must land before A1; A4 waits for Plan 32 T6d as well.

**Shared surfaces:** V1 and V5 both change the family contract, so V5 waits for V1. A1 and A4 both change how Astrid reads entries, so A4 waits for A1. A4 and Plan 32 T6d both change default resolution in `sdk/generation.py`, so A4 waits for T6d.

## P1 Validation in the install transaction

**Outcome:** a pack whose extension points or contributions do not parse fails `astrid packs add` loudly, before the swap, instead of at first use. **Authority:** CPU only.

**Delegate to N helpers:** reading the transaction flow, the test nodes and the checks. The lead keeps where in the transaction the check sits and what counts as a failure.

1. In `install_group` (`transaction.py:988`), run the extension registry's parse on the *staged* candidate before the swap. A quarantined or incompatible contribution, or a broken point, refuses the install with the registry's existing one-line fix (`registry.py` ~443-600, `problems()` at 508).
2. **Owner-dependency rule** (`validate.py`): contributing to `<owner>.<point>` requires `<owner>` in `dependencies.packs`, the same rule the import policy uses for `api` (`astrid/pack_imports.py:157-160`). Core packs (`generation`, `vibecomfy`) count as present.
3. Contributions inherit their pack's trust; there is no per-contribution trust.

**Proof:**
- New nodes:
  - `tests/core/pack/test_transaction.py::test_install_refuses_quarantined_contribution_before_swap`;
  - `tests/core/pack/test_transaction.py::test_install_refuses_contribution_without_owner_dependency`;
  - `tests/core/extensions/test_registry.py::test_staged_candidate_parse_reports_problems_without_activation`.
- These existing nodes stay green: `PYT tests/core/pack/test_transaction.py tests/core/extensions`.

## P2 `astrid packs extensions`

**Outcome:** a read-only command that lists points (owner, version, cardinality), contributions (pack, key, scope) and problems (quarantined, shadowed, disabled), with `--json`. Step 0: find the subcommand pattern in `cli_parser.py` (`list` at ~136, `inspect` at ~165) and put the command beside `inspect`. **Authority:** CPU only.

**Proof:** new `tests/core/pack/test_cli_extensions.py`:
- the three Plan 32 points are listed;
- a broken fixture contribution appears under problems with its fix;
- `--json` round-trips.

## P3 Protocol, point and family docs

**Outcome:** one page, `docs/packs/extension-points.md`, that covers:
- what a point and a contribution are, and the file layout (`extensions/points/<name>.yaml`, `extensions/<point-id>/<key>.yaml`);
- the owner-dependency rule;
- install-time validation;
- the three points' fields, including `vibecomfy.workflows` version 2 (variants, `when`, `route`, `request`);
- how Astrid shows a family (`generate list`, `describe`, `--dry-run`), linking to VibeComfy's "write a family" page (V4) rather than repeating it.

It must say that the post-output hook is `after_outputs`, not VibeComfy's template `finalize` (`templates.py:1381`). Link it from `docs/packs/README.md` and `creating-packs.md`. **Authority:** CPU only.

**Proof:** Step 0: name the Agent's docs or link check (`git grep -ln "docs/packs" -- scripts tests`) and run it. Every field in the three point YAML files appears in the page (a grep per field).

## V1 The family contract in VibeComfy

**Outcome:** a plugin can register a family of workflows in one call, and standalone VibeComfy users get the same contract Astrid mirrors. **Authority:** CPU only.

1. `PluginAPI.register_workflows(ready_root, entries, build=None, after_outputs=None, route=None, *, name)` (`extras.py:27-52`). It records origin: distribution and version, or the drop-in path.
2. The entry keeps today's keys `{id, kind, modes, bundle, needs, binds, defaults}` (`entries.py:49-68`) and gains three optional ones:
   - `variants`: an ordered list of `{id, mode, bundle, when, summary, inputs, defaults}`. `mode` must be in the kind's mode set (`entries.py:57`), and `modes` is derived from the variants. A variant's `bundle` and `inputs` may be omitted only when the family has a `build`;
   - `request`: a JSON Schema;
   - `inputs`: `[{name, type, required, description}]`, with `file` and `file_map` types (moved here from Astrid core).
3. `when` takes only `present`, `absent` and `equals`. Anything else is refused at registration, naming the key.
4. `load_plugins(only=<dists>, drop_ins=False)`.

## V5 Selection, describe and the plan envelope

**Outcome:** one routing mechanism, readable by an agent, replaces the three that exist today. **Authority:** CPU only.

1. `select(entry, inputs) -> {variant, reason}`. An explicit `variant` wins. Otherwise `route` runs, if there is one, and then the `when` tests in order; the first match wins. If nothing matches, or the inputs don't fit an explicit variant, a `RequestError` is raised.
2. `RequestError(code, field, fix)`, lifted from h3's `H3RequestError` (`h3_av/shared/request.py:18-26`).
3. `describe(entry) -> {id, kind, request | inputs, selection: "explicit variant, then route, then when in order", variants: [{id, mode, when | route_summary, summary, inputs, defaults}]}`.
4. `plan_envelope(...)`: the keys listed in the plan, with `details` taken from `build`'s `plan`.
5. **Router burn-down** (owner decision 1): re-express the six rules in `router/_rules.py:53-70` as variants of built-in `image` and `video` families, using `equals: {model: ...}` and a fallback. `router.pick` (`_core.py:74-94`) then selects over those families; `list_routes` and `describe_route` read them. `register_route` leaves `PluginAPI` (`extras.py:43-46`). Step 0: `git grep -n "register_route\|router.pick\|from vibecomfy.router"`, and check the known public plugins.

**Inline fixture** for `tests/test_family_selection.py`:

```yaml
id: image
kind: image
variants:
  - {id: inpaint,  mode: inpaint,  bundle: image/fx_inpaint,  when: {present: [image, mask]}, summary: Repaint the masked area}
  - {id: outpaint, mode: outpaint, bundle: image/fx_outpaint, when: {present: [image, expand]}, summary: Extend the canvas}
  - {id: img2img,  mode: i2i,      bundle: image/fx_i2i,      when: {present: [image]}, summary: Restyle an image}
  - {id: txt2img,  mode: t2i,      bundle: image/fx_t2i,      summary: Generate from a prompt}
```

**Proof** (new nodes):
- `{prompt}` selects `txt2img`, `{prompt, image}` selects `img2img`, `{prompt, image, mask}` selects `inpaint`, and `{prompt, image, expand}` selects `outpaint`; each reason names the matched test;
- `{prompt, mask}` (no image) with `variant: inpaint` is refused with `field: image`;
- `describe` round-trips through JSON;
- a `route` hook overrides `when`, and its reason is kept;
- an unknown `when` key is refused at registration.

## IMG The image family

**Outcome:** the owner's example, written as a third party would write it: one agent-facing entry, four variants, chosen by intent. **Authority:** CPU only; the live run, and inpaint and outpaint quality, are Plan 34's.

1. Step 0: VibeComfy `e65f494` has `image/z_image` and `image/z_image_img2img`, but no inpaint or outpaint ready template; there are only the `edit/` Flux 2 and Qwen edit graphs. Add two templates on the z_image model, using core ComfyUI nodes (`InpaintModelConditioning` or `SetLatentNoiseMask`, and `ImagePadForOutpaint`), so no new model is needed. If z_image cannot inpaint, use the existing `edit/` model and record that.
2. The plugin `image_family` registers the V5 fixture with the real bundles. `outpaint` binds `expand.{left,right,top,bottom}` to `ImagePadForOutpaint`. It needs no Python, apart from an optional `after_outputs` for `inpaint` that returns `preserved_outside_mask` evidence (V3).
3. Add a thin Astrid pack that pins the plugin (A1).

**What the author writes:** two templates, one entry of about 15 lines and an optional `after_outputs` of about 10. **What they get for free:** discovery, describe, routing with reasons, input validation and refusals, the dry-run plan, file staging, every placement, the default slots and pinned install.

**Proof:**
- Standalone: `vibecomfy run --entry image --dry-run` with each input set from the V5 fixture names the right variant. Each variant runs on a fake ComfyUI. Preservation evidence fails when the fake changes an unmasked pixel.
- Through Astrid (after A4): `astrid generate image --entry image --input prompt=... --file image=a.png --file mask=m.png --dry-run --json` names `inpaint` and its reason. Each variant runs locally and through the RunPod CPU fake.

## A4 Family routing through `generate`

**Outcome:** Astrid has one route per kind, and the choice it makes is the family's. **Authority:** CPU only.

1. `astrid generate list`, `describe --json` and `--dry-run --json` return V5's describe and plan envelope without reshaping them. Add `--variant`, plus `--input k=v` and `--file k=path`, matching V2.
2. Default resolution, owner decision 2: the request's entry, otherwise the kind's default family. That family selects a variant, and then a user's `(kind, mode)` pin for that variant's mode, if there is one, replaces the family (Plan 32 T6d's pins and `default_for` are kept). Today's inference rules become the `when` tests of the built-in `image` and `video` families (V5): `image_ref` means `i2i`, and `image_ref` with `image_end_ref` means `flf`.
3. **Delete:** `_infer_image_mode` (`sdk/generation.py:388-398`), `_EXPLICIT_ONLY_IMAGE_MODES` (402-404) and `_infer_video_mode` (451-466).

**Proof:**
- New nodes show that `generate image` with and without `image_ref`, and `generate video` with `image_ref` and `image_end_ref`, resolve the same modes as before through the built-in families.
- A user pin on `image.inpaint` wins after routing.
- `describe --entry image --json` equals VibeComfy's `describe` output.
- Grep: no `_infer_image_mode`, `_infer_video_mode` or `_EXPLICIT_ONLY_IMAGE_MODES`.

## S2 Sound on video as a native plugin

**Outcome:** a second non-h3 family proves `after_outputs` and the mux helper from outside core. It replaces the earlier P4, which wrote the same pack Astrid-only.
- It is a one-variant family: the variant-less entry form, proving backward compatibility.
- It reuses the existing sound-effects template (VibeComfy `ready_templates/audio/hunyuan_video_foley.py`, which saves audio only).
- Its `after_outputs` of about 10 lines calls `vibecomfy.media.mux` to put the generated audio onto the source video.
- It exercises a ready root, entries, a media input and `after_outputs`, with no `build`. Its models, node pin and licence notice already exist.

**Authority:** CPU only; the live run is Plan 34's.

1. Create `sound_on_video/` in poms_packs:
   - the plugin (an entry point that registers one entry);
   - a thin pack that pins it, with `dependencies.packs: [vibecomfy]`;
   - `tests/`.

   Step 0: check whether the ready-root loader accepts a template that imports the VibeComfy one. If it does not, copy the graph and keep the same model rows and node pin.
2. Install it through `astrid packs add` (P1's validation runs).

**Proof:**
- In the poms_packs checkout, run the pack's own tests against the base Agent, using Plan 06 PK-16's harness command (`tests/integration/test_install_each_pack.py`, [Plan 06 tasks](../06-packs/tasks.md#pk-16-land-the-packs-in-poms_packs)).
- New `sound_on_video/tests/test_sound_on_video_cpu.py`:
  - a standalone `vibecomfy run --entry sound_on_video` on a fake ComfyUI;
  - a generate on Plan 33's stand-in ComfyUI (local) and through Plan 32 T5's RunPod CPU fake;
  - the output is a video with the generated audio track (`ffprobe` shows one video and one audio stream), from a lavfi source clip.
- `astrid packs extensions` lists the contribution.

## Notes

- Rows V1–V4, H1, A1–A3 and S2 came from the 9 Nov Opus investigation, read at VibeComfy `e65f494` (the pin) and `e2905d0` (main), and Agent `origin/t6b1` `8c454ac07` and int/32 `7639a9569`. V5, IMG and A4, and the variant changes to V1, V2, H1 and A3, come from the owner's later 9 Nov direction ([inputs.md](inputs.md#owner-direction-9-nov-later)).
- Standalone VibeComfy's own remote RunPod binding runs `after_outputs` on the client, not the pod. Document this in V4.
- Multi-pass requests, and variants that chain workflows, stay out of scope.
- Owner questions are listed once, in [inputs.md](inputs.md#open-owner-decisions).
