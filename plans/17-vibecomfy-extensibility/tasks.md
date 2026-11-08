# Tasks — Pack extension points: switch on the protocol and prove it

[Plan](plan.md) · [Inputs](inputs.md) · [Project status and owner](../../README.md)

Routes: `N` is the default, `X` very hard, `S` super hard ([run contract](../../skills/astrid-dev-shared/run-contract.md#routing-and-bindings)). An `X` lead delegates reading, mechanical edits and running checks to `N` helpers.

**Rules for every task:**
- Base: [Plan 32](../32-generation-placement-targets/plan.md)'s landed Agent head after T6b, which already declares the `generation.engine`, `generation.machine` and `vibecomfy.workflows` points and allows `side: agent`. The poms_packs base is `main` after [Plan 06](../06-packs/plan.md). Record both SHAs in [inputs.md](inputs.md) before P1.
- Line numbers below are at Agent `5eac07e3f`; re-check them on the base.
- **CPU only:** P4's live run is [Plan 34](../34-real-gpu-proof/plan.md)'s.
- Run only the named selectors, using `PYT` and `PYT_POD` from [Plan 33's tasks](../33-unblock-live-generation/tasks.md).
- Add no versions, priorities, point inheritance, per-contribution trust or entry-point discovery (see the plan's Deferred list).
- Start only on the owner's go.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| [P1](#p1-validation-in-the-install-transaction) Extension validation inside the install transaction, plus the owner-dependency rule | X | Plan 32 T6b | `astrid/core/pack/{transaction,validate}.py`, `astrid/core/extensions/registry.py` (call site only), and their tests | New nodes in `tests/core/pack/test_transaction.py` and `tests/core/extensions/test_registry.py`; `tests/core/extensions` green | [ ] |
| [P2](#p2-astrid-packs-extensions) `astrid packs extensions` lists points, contributions and problems | N | Plan 32 T6b | `astrid/core/pack/{cli_parser,cli_inspect}.py`, and their tests | New `tests/core/pack/test_cli_extensions.py` | [ ] |
| [P3](#p3-protocol-and-point-docs) Protocol and point docs | N | P1, P2 | New `docs/packs/extension-points.md`; `docs/packs/{README,creating-packs}.md` (links only) | The repository's docs check; every point and field documented | [ ] |
| [P4](#p4-the-sound-on-video-pack) The sound-on-video pack, local and RunPod on CPU fakes | N | P1 | New poms_packs `sound_on_video/` (pack, contribution, template, `finalize`, tests) | Install through the transaction; the pack's CPU tests on local and the RunPod fake | [ ] |
| R Review rounds (at most 2; Pending owner agreement) | S | P1–P4 | read-only | Rounds per the [run contract](../../skills/astrid-dev-shared/run-contract.md): findings become rows `R<round>.<n>` added directly below this one, each with route, scope, dependencies and proof; publishing or closing waits for them | [ ] |

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

## P3 Protocol and point docs

**Outcome:** one page, `docs/packs/extension-points.md`, that covers:
- what a point and a contribution are, and the file layout (`extensions/points/<name>.yaml`, `extensions/<point-id>/<key>.yaml`);
- the owner-dependency rule;
- install-time validation;
- the three points' fields.

It must say that the `vibecomfy.workflows` field `finalize` is not VibeComfy's template `finalize` (`templates.py:1381`). Link it from `docs/packs/README.md` and `creating-packs.md`. **Authority:** CPU only.

**Proof:** Step 0: name the Agent's docs or link check (`git grep -ln "docs/packs" -- scripts tests`) and run it. Every field in the three point YAML files appears in the page (a grep per field).

## P4 The sound-on-video pack

**Outcome:** a second, non-h3 composite pack proves the protocol from outside core.
- It contributes one `vibecomfy.workflows` entry that reuses the existing sound-effects template (VibeComfy `ready_templates/audio/hunyuan_video_foley.py`, which saves audio only).
- It adds a `finalize` of about 30 lines that muxes the generated audio onto the source video with ffmpeg.
- It exercises `ready_root`, `entries`, a media input and `finalize`, with no `build`. Its models, node pin and licence notice already exist.

**Authority:** CPU only; the live run is Plan 34's.

1. Create `sound_on_video/` in poms_packs:
   - `pack.yaml` with `dependencies.packs: [vibecomfy]`;
   - `extensions/vibecomfy.workflows/sound_on_video.yaml`;
   - a ready root with one template that reuses the sfx graph;
   - `finalize.py`;
   - `tests/`.

   Step 0: check whether the ready-root loader accepts a template that imports the VibeComfy one. If it does not, copy the graph and keep the same model rows and node pin.
2. Install it through `astrid packs add` (P1's validation runs).

**Proof:**
- In the poms_packs checkout, run the pack's own tests against the base Agent, using Plan 06 PK-16's harness command (`tests/integration/test_install_each_pack.py`, [Plan 06 tasks](../06-packs/tasks.md#pk-16-land-the-packs-in-poms_packs)).
- New `sound_on_video/tests/test_sound_on_video_cpu.py`:
  - a generate on Plan 33's stand-in ComfyUI (local) and through Plan 32 T5's RunPod CPU fake;
  - the output is a video with the generated audio track (`ffprobe` shows one video and one audio stream), from a lavfi source clip.
- `astrid packs extensions` lists the contribution.
