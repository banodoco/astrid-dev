# No-rental H3 submission readiness rehearsal

Purpose: exercise the local H3 planning, Runtime Python package, recovery-path, installed-manifest and pinned-source gates before any RunPod claim. This procedure makes no RunPod claim and never calls `astrid machines claim`. The H3 dry run writes a local plan; source fetchability check writes only to a disposable data root and uses Git reads. These are deliberate local side effects, not provider spend.

## State at writing

No readiness step below has been run as part of this rehearsal. Do not mark the candidate ready from the historical generation attempt. On 2026-11-16, the first generation admission was blocked because the Runtime did not have `vibecomfy` available. A later admitted task (`53b1a5befd774a949aaebd2d0c8a3f7f`) failed before model preparation with:

```text
RunPod needs the installed release manifest at /home/user/work/h3/wt/environment.env/manifest.json to pin its bootstrap sources
```

The first retry also encountered an existing recovery receipt (`recovery receipt already exists; use resume=True or a new path`). The subsequent pre-admission retry was deliberately interrupted. Exact worker source fetchability has not been established. The local source venv at `environment.env` is not itself an installed Astrid release and does not contain the required manifest.

## 0. Bind commands to the real installed host

Use the interpreter and `astrid` executable belonging to the Agent installation that runs the selected Runtime's generic pack host, and the Runtime data root selected by that Runtime. Do not use a developer checkout, an unrelated venv, or ambient `PYTHONPATH` as evidence of installed readiness.

Set these shell variables to the already-installed paths for this host. This snippet does not inspect or print credential files:

```bash
ASTRID_BIN=/absolute/path/to/selected/astrid
ASTRID_PYTHON=/absolute/path/to/selected/python
ASTRID_RUNTIME_DATA_ROOT=/absolute/path/to/selected/runtime-data
ASTRID_PROJECT=minkhole
ASTRID_H3_INPUTS=/absolute/path/to/the/exact/h3-inputs.json
```

`ASTRID_H3_INPUTS` is the JSON object supplied to `--inputs-json` for the intended H3 entry, with the same request and asset map that the eventual operation will use. Keep creative input contents out of this report.

## 1. Run the H3 CPU planning preview

The documented H3 `--dry-run` normalizes the request, resolves prepare/compile bindings, and writes `plan.json` without submitting a local GPU or RunPod task ([H3 README](../../wt/environment/astrid/packs/h3_av/README.md)). Use a new disposable output directory so the plan does not collide with a real operation journal:

```bash
ASTRID_DRY_RUN_OUT="$(mktemp -d)/h3-dry-run"
ASTRID_RUNTIME_DATA_ROOT="$ASTRID_RUNTIME_DATA_ROOT" \
  "$ASTRID_BIN" generate video \
  --entry h3 \
  --placement runpod \
  --project "$ASTRID_PROJECT" \
  --inputs-json "$ASTRID_H3_INPUTS" \
  --out "$ASTRID_DRY_RUN_OUT" \
  --dry-run --json
```

Record the CLI exit code, returned readiness/plan status, and whether `plan.json` was written. Preserve the plan as local evidence if desired. A successful preview proves only request normalization and CPU planning/bindings. It does not prove the `vibecomfy` package is importable by the host, receipt recovery, manifest validity, media transfer, worker startup, live node schema, model availability, or GPU execution. The preview writes files under the temporary output directory; it is not a Runtime task or provider operation.

## 2. Check VibeComfy in the exact host Python

The generation error recommended `astrid doctor --json`; the setup documentation identifies this command as read-only for optional capability prerequisites. Run it through the selected installation, then check the same interpreter's import origin:

```bash
ASTRID_RUNTIME_DATA_ROOT="$ASTRID_RUNTIME_DATA_ROOT" \
  "$ASTRID_BIN" doctor --json

"$ASTRID_PYTHON" - <<'PY'
import importlib.util
import json
import sys

spec = importlib.util.find_spec("vibecomfy")
print(json.dumps({
    "python": sys.executable,
    "vibecomfy_available": spec is not None,
    "vibecomfy_origin": None if spec is None else spec.origin,
}, sort_keys=True))
PY
```

Pass evidence: doctor has no `packages:missing=vibecomfy` issue, and `vibecomfy_available` is `true` in the host's selected Python. If doctor or import is run from another Python, it does not qualify the host. Package presence does not establish the worker source pins or the worker's model cache.

## 3. Decide the recovery receipt before submission

For a new authorized operation, choose a new, unique SDK receipt path and a new, empty H3 `--out` directory. Do not reuse a path that already contains a receipt or journal. `--dry-run` cannot exercise `--recovery-path`; the SDK explicitly rejects recovery receipts on dry-run previews. Check only whether the receipt file itself already exists; `AdmissionReceipt` intentionally retains its sibling lock file after use, and lock-file existence alone does not mean the path is in use.

For a genuinely new receipt path, the read-only disposition check is:

```bash
ASTRID_NEW_RECEIPT=/absolute/path/to/a/new-operation/admission.recovery.json
test ! -e "$ASTRID_NEW_RECEIPT" || { echo "receipt path already exists; choose a different new path" >&2; exit 1; }
```

If an invocation already has a receipt, do not delete or overwrite it. Resume with the exact same project, inputs, execution request, recovery path, and H3 output directory. The SDK validates the same request digest and Runtime realm before recovering the admission (`docs/reference/sdk.md`, “Exact admission recovery”; `astrid/sdk/recovery.py`).

For a new, separately authorized operation, the CLI shape is below. It creates an admission and may execute against the paid target; it is **not** part of this no-rental rehearsal:

```bash
ASTRID_RUNTIME_DATA_ROOT="$ASTRID_RUNTIME_DATA_ROOT" \
  "$ASTRID_BIN" generate video \
  --entry h3 --placement runpod --project "$ASTRID_PROJECT" \
  --inputs-json "$ASTRID_H3_INPUTS" \
  --out /absolute/path/to/a-new-empty-h3-operation-directory \
  --recovery-path /absolute/path/to/a-new-unique-runtime-admission.recovery.json \
  --json
```

CLI interface discrepancy: the H3 skill says to resume via `astrid generate video ... --resume` (`astrid/packs/h3_av/docs/SKILL.md:63-68`), but this checkout's parser adds `--resume` only when the modality spec has `audio_modes` (`astrid/core/generation/cli.py:241-242`); the video spec has no `audio_modes` (`:20-22`). Thus H3 video `--resume` is not exposed by the current CLI parser. The public `GenerationFacade.video()` SDK method does accept `resume` and `recovery_path` (`astrid/sdk/generation.py:2352-2375`), so the supported SDK path for an already-authorized same-request resume is:

```bash
ASTRID_RUNTIME_DATA_ROOT="$ASTRID_RUNTIME_DATA_ROOT" "$ASTRID_PYTHON" - <<'PY'
from pathlib import Path

from astrid.sdk.client import AstridClient
from astrid.sdk.generation import GenerationFacade

with AstridClient.open_from_launcher() as client:
    result = GenerationFacade().video(
        entry="h3",
        placement="runpod",
        project="minkhole",
        request="/absolute/path/to/the/same-request.json",
        asset_map="/absolute/path/to/the/same-asset-map.json",
        out="/absolute/path/to/the/same-h3-operation-directory",
        client=client,
        recovery_path=Path("/absolute/path/to/the/existing-runtime-admission.recovery.json"),
        resume=True,
        wait=True,
    )
    print({"ok": result.ok, "task_id": getattr(result, "task_id", None)})
PY
```

Use the exact same request, asset map, execution request, project, `out`, and receipt path as the original admission. If this is an intentional new operation, create new empty paths and omit `resume`; a receipt collision is a stop condition until the old admission is reconciled or a genuinely new operation is authorized. The resume SDK call is also an actual Runtime recovery/observation operation, not part of no-rental rehearsal.

## 4. Validate the installed release manifest and resolve exact pins

Run `_pins()` with the same installed Python from step 2. It is a read-only internal helper: it derives the manifest path as `Path(sys.prefix).parent / "manifest.json"`, reads the installed manifest, checks Runtime SHA against the Agent's `runtime.lock.json`, checks the exact canonical lifecycle repo/SHA/version, and checks the optional VibeComfy SHA against the selected recipe. It returns four source identities. Do not construct a minimal hand-written manifest in the venv to bypass the installed-release boundary.

```bash
"$ASTRID_PYTHON" - <<'PY'
from astrid.packs.runpod.managed_sources import _installed_manifest_path, _pins

print(f"manifest={_installed_manifest_path()}")
for source, (repository, revision) in sorted(_pins().items()):
    print(f"{source}\t{repository}\t{revision}")
PY
```

Pass evidence: the manifest path exists and `_pins()` returns all four identities without raising `ManagedSourcesError`. Retain the four path/repository/full-commit rows. Do not print the full release manifest; it contains unrelated installation metadata. This check does not prove those commits are fetchable or that the managed source cache is clean.

The required identities are `src/astrid-agent`, `src/astrid-runtime`, `src/runpod-lifecycle`, and `src/VibeComfy`. The installed manifest provides Agent and Runtime repo/commit fields; Runtime must match `runtime.lock.json`. Lifecycle is taken from the Agent's canonical pin. VibeComfy is taken from the H3 ComfyUI engine recipe; if present in the manifest, its SHA must match that canonical revision.

## 5. Exercise exact source fetchability in an isolated data root

`ensure_managed_sources()` is the same resolver RunPod preparation calls. It fetches a missing pin with `git fetch --depth=1 <repository> <full-sha>`, checks out detached, verifies `HEAD`, and requires a clean tree. It writes under `<data-root>/runpod/sources`; set a fresh temporary `ASTRID_RUNTIME_DATA_ROOT` so it cannot change the selected Runtime's real cache.

```bash
ASTRID_PREFLIGHT_ROOT="$(mktemp -d)"
trap 'rm -rf "$ASTRID_PREFLIGHT_ROOT"' EXIT

ASTRID_RUNTIME_DATA_ROOT="$ASTRID_PREFLIGHT_ROOT" \
  "$ASTRID_PYTHON" - <<'PY'
import subprocess

from astrid.packs.runpod.managed_sources import (
    _pins,
    ensure_managed_sources,
)

pins = _pins()
root = ensure_managed_sources()
for relative, (repository, expected) in sorted(pins.items()):
    checkout = root / relative
    actual = subprocess.run(
        ["git", "-C", str(checkout), "rev-parse", "HEAD"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    dirty = subprocess.run(
        ["git", "-C", str(checkout), "status", "--porcelain", "--untracked-files=all"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    print(f"{relative}\t{repository}\texpected={expected}\tactual={actual}\tclean={not bool(dirty)}")
    if actual != expected or dirty:
        raise SystemExit(f"source identity check failed: {relative}")
print(f"managed_source_root={root}")
PY
```

This creates and removes only the temporary preflight source cache. It makes Git network reads to the manifest/canonical repositories, but does not contact RunPod, read provider credentials, admit a task, or start a pod. Pass evidence is four exact `actual=expected` full SHA rows with `clean=True` and exit code 0. A fetch failure means no source-fetchability proof; preserve the error and stop before renting. If the installed manifest's Agent commit is unpublished, its configured repository must make that exact commit fetchable. Do not substitute a branch head or loosen the pin check.

## 6. Readiness decision and evidence boundary

Only after steps 1–5 pass should the request be considered preflight-ready for a separately authorized paid operation. Save command lines, exit codes, sanitized stdout/stderr, manifest path, four source identity rows, and the exact dry-run plan location. Keep request text, media contents, credential references, and credentials out of shared evidence.

These checks do not qualify a RunPod image/template, watchdog acknowledgement, volume mount, GPU memory, ComfyUI node schema, model download throughput/cache, inference, or output readback. Those require the actual paid worker path. No paid command is part of this rehearsal; the first such boundary is the separately authorized `astrid machines claim` or a generation command that claims a machine.

## 7. Staged installed Runtime rehearsal (2026-11-16)

This run used the installed staged Agent and its Runtime data root, not the source venv:

```text
CLI=/home/user/work/h3/run/pilot/stage-program/versions/5ae4e172-6855dfa8-b6833d04/py/bin/astrid
PYTHON=/home/user/work/h3/run/pilot/stage-program/versions/5ae4e172-6855dfa8-b6833d04/py/bin/python
ASTRID_RUNTIME_DATA_ROOT=/home/user/work/h3/run/pilot/stage-data
PROJECT=minkhole
INPUTS=/home/user/work/h3/run/pilot/stage-pika-inputs.json
```

The staged Runtime was restarted by `runpod_api` after the imports and media read completed. Its new instance ID was `5c3cd68624774ac49e87da481362529d`; Runtime health and the generic host readiness file were reported healthy/ready. The installed CLI and Python remained the paths above.

### Entry dry-run

Exact command:

```bash
ASTRID_RUNTIME_DATA_ROOT=/home/user/work/h3/run/pilot/stage-data \
  /home/user/work/h3/run/pilot/stage-program/versions/5ae4e172-6855dfa8-b6833d04/py/bin/astrid \
  generate video --entry h3 --placement runpod --project minkhole \
  --inputs-json /home/user/work/h3/run/pilot/stage-pika-inputs.json \
  --out /home/user/work/h3/run/pilot/rehearsal-evidence/stage-pika-dry-run-output \
  --dry-run --json
```

Exit code was `0`; result `status` was `ready`, `issues` and `fixes` were empty, and target state was `pending_host_readiness`. The plan resolved the source media hash to `aa84f8370736f6fd295f4c8037654a118864060d6b15134625ab9aa88e64f092`, the imported Astrid media handle, and exact source range `81.05` to `84.299` seconds. It measured 78 frames at 24/1 fps with audio and conformed the prefix to 1024×576 at 24 fps. Evidence: [`entry-dry-run.stdout`](rehearsal-evidence/entry-dry-run.stdout), [`entry-dry-run.stderr`](rehearsal-evidence/entry-dry-run.stderr), [`entry-dry-run.exit`](rehearsal-evidence/entry-dry-run.exit). The JSON contains the request prompt; keep it local and do not paste it into shared summaries.

This proves request normalization and CPU planning for the selected H3 entry. It does not prove live Runtime admission or a RunPod task: installed SDK source sets `check_runtime=not dry_run and not is_remote_target` in `astrid/sdk/generation.py`, and the resulting plan explicitly remains `pending_host_readiness`.

### Same-host VibeComfy and Runtime capability

The same installed Python reported `vibecomfy` importable from the staged version's `site-packages/vibecomfy/__init__.py`. The installed Runtime capability view was read through `AstridClient` / its workspace transport `list_capabilities(limit=100)` and filtered to `vibecomfy.run`: status `ready`, required resource `gpu`, no unavailable reason. Evidence: [`installed-package-and-pins.stdout`](rehearsal-evidence/installed-package-and-pins.stdout) and [`capability-view.json`](rehearsal-evidence/capability-view.json). `astrid generate list --json` also showed the H3 local entry unavailable for attached local generation because no local ComfyUI target was attached; this is distinct from the ready `vibecomfy.run` capability used by Runtime-hosted generation. Evidence: [`generation-list.json`](rehearsal-evidence/generation-list.json).

`astrid doctor --json` did return `healthy: false`: the installed Remotion renderer's `node_modules` is missing. The staged H3 `after_outputs` hook directly imports and calls `h3_av.shared.compose.compose_candidate` and `h3_av.shared.verify.verify_candidate` (`astrid/packs/h3_av/extensions/vibecomfy.workflows/hooks.py:209-227`); these H3 modules use subprocess/ffprobe and no H3 Python source references Remotion. This supports that the missing renderer package is outside the H3 compose/verify code path. The overall doctor warning remains real and this rehearsal does not claim generic Runtime health or paid worker success from the `vibecomfy.run` row alone.

### Fresh receipt disposition

Candidate receipt path for a future separately authorized operation: `/home/user/work/h3/run/pilot/rehearsal-evidence/stage-pika-operation.recovery.json`. At rehearsal time it did not exist; its parent directory existed and was writable. An exclusive sibling probe file was created, written, fsynced, and removed. Evidence: [`fresh-receipt.json`](rehearsal-evidence/fresh-receipt.json). No actual recovery receipt was created; dry-run does not exercise AdmissionReceipt locking, freeze, or replay semantics. This establishes only fresh-path disposition and basic filesystem writability.

### Installed pins and managed source fetchability

Using the installed Python, `_installed_manifest_path()` returned `/home/user/work/h3/run/pilot/stage-program/versions/5ae4e172-6855dfa8-b6833d04/manifest.json`; it existed. `_pins()` returned all four installed source identities without error. Then `ensure_managed_sources()` ran with `ASTRID_RUNTIME_DATA_ROOT=/home/user/work/h3/run/pilot/rehearsal-evidence/source-root`, isolating its Git checkouts under `source-root/runpod/sources`. Exit code was `0`; all four checkouts were clean and `git rev-parse HEAD` exactly matched the manifest/canonical pin:

| Managed source | Exact pinned commit | Result |
| --- | --- | --- |
| `src/VibeComfy` | `dba38f8644c46f652376f2cd5112ea161e40f09b` | exact, clean |
| `src/astrid-agent` | `5ae4e172d4ae2a26f2c374ff08de8832b4a8cd85` | exact, clean |
| `src/astrid-runtime` | `6855dfa8df65cf8ae4c002b57134d6505493c17c` | exact, clean |
| `src/runpod-lifecycle` | `9f88ef7640bc664f697112d966ecefa123d44340` | exact, clean |

Evidence: [`installed-package-and-pins.stdout`](rehearsal-evidence/installed-package-and-pins.stdout), [`managed-sources.stdout`](rehearsal-evidence/managed-sources.stdout), and [`managed-sources.exit`](rehearsal-evidence/managed-sources.exit). `ensure_managed_sources()` made Git network reads and wrote only this isolated source cache. It did not contact RunPod or admit a task.

### Evidence boundary

The rehearsal confirms staged package importability, a ready `vibecomfy.run` capability, successful H3 CPU planning, a fresh writable recovery-path location, installed pin consistency, and fetchability of the exact four source commits. It did not create a real AdmissionReceipt, submit a provider claim, invoke provider APIs, download models, start a GPU worker, or execute inference/composition/verification. A live H3 generation remains unproved and would cross the paid-operation boundary.
