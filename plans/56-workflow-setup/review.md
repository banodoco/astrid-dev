# Independent review — Workflow set-up

[Plan](plan.md) · [Inputs](inputs.md)

An Astra critique of the first draft of this plan, run on 15 November 2026 against astrid-agent `a91c35dfd` and VibeComfy `dba38f86`, briefed to build as little as possible and to check claims in code. Source reading only. Reproduced as written; line references to plan.md and inputs.md are to the first draft. What was accepted is in [inputs.md](inputs.md#planning-evidence).

Reviewed code at Astrid `a91c35dfd` and VibeComfy `dba38f86`. Offline, source inspection only; no generation, project execution, credentials, or environment changes. `A:` paths are relative to the supplied Astrid checkout; `V:` paths to `/home/user/banodoco/vibecomfy`.

1. Claims in inputs.md that need correction:

- `inputs.md:13`: an undeclared digest/size is not automatically fatal: `ComfyUIEngine.workflow_requirements` first fills them from pinned locks (`A:astrid/packs/vibecomfy/extensions/generation.engine/comfyui_engine.py:167-174`). The actual refusal is for fields still missing afterward (`A:astrid/core/generation/managed_preparation.py:300-303`). Counting incomplete authored rows does not establish the number of blocked workflows.
- `inputs.md:20-22`: readiness is not limited to the 15 lock entries. `get_known_node_packs` merges static definitions with rich lock entries (`V:vibecomfy/node_packs/_defs.py:474-478`). The false “core node” diagnosis is real, but applies when neither source resolves the class (`A:astrid/core/generation/asset_gaps.py:105-120`).
- `inputs.md:23`: “requirements installed” means declared `pack.pip_packages`, not arbitrary packs' `requirements.txt` or installation hooks. An unknown pack can have no dependency installation at all (`V:vibecomfy/node_packs/_install.py:221-233,985-987,1016-1034`). Extending this to arbitrary requirements is new behavior and new risk.
- `inputs.md:25`: “bundled entries only” is too narrow: alignment also accepts registered ready-template entries (`A:astrid/core/generation/asset_alignment.py:344-366`). There is already a combined node/model/restart report, `vibecomfy nodes reconcile` (`V:vibecomfy/commands/nodes.py:396-460,562-619`). It is not a complete target setup command.
- Also qualify the claimed absence of combined acquisition/restart handling: VibeComfy exposes `run --ensure-packs --ensure-models`, and embedded prerequisite preparation installs packs, reloads, then ensures models (`V:vibecomfy/commands/run.py:1029-1031`; `V:vibecomfy/runtime/session.py:1140-1224`). This is reusable orchestration, not approval to run generation during setup.
- `inputs.md:16`: no general content-identification index is a fair conclusion; “nothing identifies a file by content” is literally too broad. A specific legacy Flux VAE is identified by size and SHA (`V:vibecomfy/registry/models_loader.py:180-192`). Source receipts also already persist URL, observed hash and size (`V:vibecomfy/fetch.py:316-348`), although they are not a reverse index.
- `inputs.md:12,22` omit crucial limits: attached downloads require existing loader nodes and a same-machine target (`A:astrid/core/generation/asset_gaps.py:264-268,323-333`); Manager resolution is conditional, as detailed below. `inputs.md:15` is correct for Astrid's role matching; VibeComfy additionally handles separator-equivalent picker values, deliberately not arbitrary basename/case matches (`V:vibecomfy/model_assets.py:321-339`).

2. Existing pieces and task cuts:

- WS-3 should extend the existing requirements contract, not invent a second authority: `entries.requirements`, `ComfyUIEngine.workflow_requirements`, VibeComfy `resolve_referenced_assets` and `referenced_model_requirements` already expose models/nodes or resolved/unresolved model records (`A:astrid/core/generation/entries.py:985-996`; engine file above:149-177; `V:vibecomfy/model_assets.py:129-180,269-294`).
- Reuse `nodes reconcile`, `nodes install-plan`, `missing_packs_for_workflow`, and `inspect_pack_install_state` for diagnostics and installed-pack state (`V:vibecomfy/commands/nodes.py:236-263,396`; `V:vibecomfy/node_packs/_install.py:666,1151-1189`). Offline schema availability is not proof a class is loaded on the selected server; retain live `/object_info` validation.
- Keep WS-1 as a small reporting fix. Merge WS-2's confirmed local mapping into WS-5; both need the same scoped binding record. Offer only candidates the target's loader can actually use; filename, extension and size do not establish identity.
- Reduce WS-5 initially to declared/registry sources, explicit user URL or local-file mapping, and persisted confirmation. Defer header inference, global content indexing, fuzzy remote search and Civitai integration. Reuse authored `model_assets`, registry aliases and source receipts; add only the missing workflow/field-to-source binding.
- WS-4 should compose the existing installer and download paths. Resume support already exists in `A:astrid/core/generation/model_downloader.py:597-685`; attached downloads currently use temporary staging cleaned in `finally` (`asset_gaps.py:418-449`), so wiring durable resume there remains work. Fold WS-6 into command delivery; keep WS-7 focused on changed boundaries and failures.

3. Risk and minimum safeguard:

Approval to install a pinned repository authorizes executing third-party code with the user's privileges; it does not establish safety. Node import, dependency build/metadata hooks and later runtime execution can read or modify accessible files. A virtual environment isolates dependencies, not these privileges.

The ordinary failure is breaking the shared Python environment: incompatible NumPy/Transformers/OpenCV/CUDA dependencies can disable existing workflows. Pip replaces installed distributions, contradicting `plan.md:42`'s unconditional promise never to replace the person's files. A commit pin does not pin transitive Python artifacts.

The existing check is insufficient: it protects Torch by default plus configured names, compares versions, resolves again for actual installation, and detects some changes only afterward (`V:vibecomfy/node_packs/_install.py:943-982,1011-1042`). It provides neither rollback nor a guarantee that other installed packages remain compatible. The managed preparation path supplies additional base-package names; the standalone alignment invocation does not explicitly supply that list (`A:astrid/core/generation/managed_preparation.py:711,766`; `asset_alignment.py:486-491`).

Minimum automatic path: identify the actual ComfyUI root and interpreter; show the pinned code and complete dependency change set; refuse changes to existing distributions or existing pack checkouts. Resolve all packs together under constraints for the installed environment and install the approved artifacts, not a fresh floating resolution. Require explicit trust for code execution; a pip dry-run can itself invoke build metadata code and is not a sandbox.

If replacements are needed, the smallest scope is to leave that item manual. Supporting automatic replacements requires a restorable environment snapshot/clone and recovery evidence; `pip freeze` alone is not rollback. Do not turn this project into a general environment transaction manager.

4. What breaks a single plan/apply digest:

- Ordering: `_download_gaps` refuses absent loader classes; `workflow_asset_gaps` obtains model choices from observed schemas (`A:astrid/core/generation/asset_gaps.py:154-170,264-268`). Unknown custom loaders may also be skipped by static model extraction (`V:vibecomfy/model_assets.py:232-245`). “Every model from any workflow” cannot be promised before schema/declaration discovery.
- Installing pack files does not load the nodes. Stop at `restart_required`, let the owner restart an external server, then refresh `/object_info` and validate model names/folders. Managed alignment currently downloads known models first and only reports restart afterward (`A:astrid/core/generation/asset_alignment.py:581-610`). Installation success is not readiness.
- The attached digest is recomputed from the current missing-file plan (`A:astrid/core/generation/asset_gaps.py:348-351,452-475`). After a restart or partial success, that plan changes and the old digest fails. Persist the approved immutable actions separately from progress; completed actions must be verified and skipped. Newly discovered actions need another approval, so “one approval for any workflow” must be relaxed.
- Model publication is per-file; node cloning/pip/lock updates are separate mutations. Earlier downloads and package changes survive later failures, and the installer retains incomplete sentinels (`V:vibecomfy/node_packs/_install.py:1044-1082,1177-1181`). Report completed/failed/pending work and recover explicitly; never imply atomic rollback or that all failures leave nothing behind.
- Bind approval to workflow content, target/root/interpreter, destinations, source identities, node commits and dependency artifacts; check environment drift before applying. A repository-only digest cannot bind floating pip resolution. “Plan writes nothing” is already false for the reused hard-link probe (`A:astrid/core/generation/asset_gaps.py:334-338,375-391`); move probes to apply or narrow that promise.

5. Is the Manager resolver usable as assumed?

Not as a drop-in offline lookup. `resolve_pack` uses Comfy Registry, not Manager; `allow_remote_lookup=False` rejects named lookups before consulting its cache (`V:vibecomfy/registry/pack_resolver.py:592-653`). Manager support is in `resolve_missing_nodes`, which also attempts Registry and GitHub and exposes no equivalent offline/source allowlist (`:666-744`). This also exceeds D2's proposed Manager-only node search scope.

The Manager tier needs both `custom-node-map.json` and `custom-node-list.json`, retrieved over HTTP on cache misses; responses are cached to disk (`:962-994,1026-1031`). Offline operation needs compatible cached responses plus explicit prevention of uncached/fallback requests. A cold-cache transport error in the Manager tier is not caught by its `_BudgetExceeded`-only handler (`:697-705`). Cache writes also contradict a literal read-only plan.

Online compatibility is unproven by this review: tests supply synthetic class-to-slug maps and bare lists (`V:tests/test_pack_resolver.py:660-689`). The parser expects that shape; `_iter_records` does not unwrap a `custom_nodes` list, and `_first_string` ignores array-valued `files` (`V:vibecomfy/registry/pack_resolver.py:1300-1360,1508-1538`). Require a representative real cached Manager fixture and endpoint/schema verification before claiming coverage; no network was used here.

Even a successful Manager match is evidence, not an installable pin: its `PackRef` has no commit, and candidates are explicitly `runnable=False` (`:1353-1360,199-217`). Resolve and approve a full commit separately, preserving ambiguity and validating the advertised classes after loading.

6. The three most important corrections:

1. Shrink the project to one orchestration/reporting front door over existing contracts and helpers; merge WS-2/WS-5 and defer broad identification/search. Preserve explicit unknowns instead of promising complete discovery for any workflow.
2. Replace the atomic, one-approval story with install → restart → inspect → continue, immutable approved actions, and per-action progress. Narrow external-target support initially to a verified same-machine installation; the existing downloader already imposes this boundary.
3. Make dependency replacement a refusal/manual boundary for the first release. The current protected-package check is a useful guard, not sufficient protection for a person's existing ComfyUI; validate the Manager data path before making it a core dependency.
