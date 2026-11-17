# H3 RunPod pilot runbook

Portable procedure for an operator on a separate machine. This is based on the successful installed H3 pilot recorded in [`cost.md`](cost.md), [`rehearsal.md`](rehearsal.md), and the `stage-*` logs in this directory. Commands below are templates: replace paths, project, media, target settings, deadline, volume, and cost limits with values authorized for the new run. Do not reuse this run's receipt, output directory, pod ID, or deadline.

**Paid boundary:** all steps through the no-rental rehearsal are local/read-only except Astrid project/media imports. `astrid machines claim` and a non-dry-run `generate video` can incur provider charges. Run them only under the operation's explicit budget and deadline. Do not make a second claim if the first is pending or allocated.

## 1. Install the exact release into an isolated home

Use a fresh program/data/home root, the selected installed Runtime, and a manifest copied from the matching release install manifest. Preserve the complete manifest, including `schema_version` and `tools`. Set source SHAs to full lowercase commits from the release/approved candidate. The successful pilot used:

| Source | Pinned commit |
| --- | --- |
| Agent | `5ae4e172d4ae2a26f2c374ff08de8832b4a8cd85` |
| Runtime | `6855dfa8df65cf8ae4c002b57134d6505493c17c` |
| VibeComfy | `dba38f8644c46f652376f2cd5112ea161e40f09b` |
| runpod-lifecycle | `9f88ef7640bc664f697112d966ecefa123d44340` |

Successful installed Agent directory was `.../stage-program/versions/5ae4e172-6855dfa8-b6833d04`; its `manifest.json` and Python/CLI were used for *all* rehearsal and generation commands. Do not substitute the source checkout or an unrelated venv: RunPod bootstrap requires the installed release manifest.

For local candidate commits, follow [`local-source-install.md`](../../astrid-agent/docs/setup/local-source-install.md): use committed scratch clones, add `repo` as an absolute local directory or `file://` URL, and retain each exact full `sha`. A remote Git URL is not supported in `repo`. For published commits, omit `repo` and let the installer fetch the pinned archive. Do not use uncommitted worktree edits; the installer reads `git archive` at the commit. A typical isolated install, with manifest served from localhost, is:

The installer needs access to `codeload.github.com` for pinned tool source archives, including Oh My Pi. That host was blocked in this cloud session during a later install even though the pilot's earlier installation succeeded. Where the operator's authorized network permits Git access, the documented exact local-source override can instead name a clean local Git checkout at the manifest's full pinned commit; the installer uses `git archive` for that commit and checks its pinned build inputs. Select this only when the host authorizes that source and transport. Do not disable TLS or bypass a network refusal.

```sh
# Terminal A, from the directory containing local-install-manifest.json
python -m http.server 17605 --bind 127.0.0.1

# Terminal B: the ordinary installer transaction, isolated from the operator's existing install
curl -fsSL https://astrid.haus/install | \
  ASTRID_INSTALL_MANIFEST_URL=http://127.0.0.1:17605/local-install-manifest.json sh -s -- \
  --root /absolute/path/to/pilot/program \
  --data-root /absolute/path/to/pilot/data --managed-by pinokio
```

Use a fresh HOME/XDG home for the install service as required by the host setup. The pilot used the installer's `--managed-by pinokio` option to stage without registering a shared login service, and ran its Runtime under an external supervisor. With variables set to the installed version, isolated home and data root, and a free door port, its equivalent launch is:

```sh
python3 - <<'PY'
import os
names = ('PATH', 'HOME', 'XDG_CONFIG_HOME', 'XDG_DATA_HOME', 'XDG_STATE_HOME', 'TMPDIR',
         'RUNPOD_API_KEY', 'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'NO_PROXY',
         'http_proxy', 'https_proxy', 'all_proxy', 'no_proxy', 'SSL_CERT_FILE',
         'SSL_CERT_DIR', 'REQUESTS_CA_BUNDLE', 'CURL_CA_BUNDLE')
env = {name: os.environ[name] for name in names if name in os.environ}
py = os.environ['ASTRID_PYTHON']
os.execve(py, [py, '-I', '-m', 'astrid_runtime', 'run', '--profile', 'astrid',
               '--data-root', os.environ['ASTRID_RUNTIME_DATA_ROOT'],
               '--source-manifest', os.environ['ASTRID_PROFILE'],
               '--door-port', os.environ['ASTRID_DOOR_PORT']], env)
PY
```

Set `HOME`/`XDG_*` to the install's isolated home, and export `ASTRID_PYTHON`, `ASTRID_PROFILE`, `ASTRID_RUNTIME_DATA_ROOT`, and `ASTRID_DOOR_PORT` before launching. The supervisor must keep the Runtime alive. Values from the allowlist remain only in process environment data: never inspect `.env` or credential files, echo secrets, or put them in command arguments or logs. Verify the installed Runtime and generic host are ready using Astrid/Runtime status surfaces before proceeding.

**Proves:** the selected installed package set and its installed release manifest are the actual host environment. **Does not prove:** provider credentials work, a volume is visible in the account, a claim will allocate, or a GPU workload will succeed. The host's service environment matters: the first staged claim failed to confirm the volume because its service lacked proxy/certificate trust; the log showed TLS certificate verification errors. The safe fix was to restart only the staged Runtime with allowlisted inherited proxy/trust settings plus the existing API key. The retry then confirmed the volume. Do not “fix” this by weakening TLS verification.

## 2. Create the project and import with Astrid

Use the installed CLI connected to the intended Runtime and data root. For this installed CLI, the exact project/import command forms are:

```sh
export ASTRID_RUNTIME_DATA_ROOT=/absolute/path/to/pilot/data
"$ASTRID_BIN" projects create minkhole --name Minkhole --select --json
"$ASTRID_BIN" timelines import --project minkhole --name 'Approved rough cut' \
  /absolute/path/to/approved-rough-cut.astrid --json
"$ASTRID_BIN" timelines import --project minkhole --name 'Original matrix scene reference' \
  /absolute/path/to/original-matrix-scene-reference.astrid --json
"$ASTRID_BIN" timelines assets --project minkhole '<returned-timeline-id>'
"$ASTRID_BIN" media list --project minkhole --json
```

Use fresh project slug or select an existing authorized project; don't run `projects create` a second time on an existing slug. Import the approved timeline/source and its reference via Astrid CLI/SDK only; do not copy media into Runtime internals or create authoring records by hand. Retain the exact JSON receipts and resolved IDs. The successful staged run used `minkhole`, imported `approved-rough-cut.astrid` and `original-matrix-scene-reference.astrid`, and received timeline IDs `5802f72b36d24693b2da6fdb5c8d1080` and `87369ec4ada74ae781ec56d23baa57dc`.

After import, list timeline assets and project media, then use `astrid media open --project minkhole --materialize --cache-root /absolute/path/to/pilot/media-cache --max-bytes <sufficient-limit> --json '<returned-media-id-or-opening-reference>'` to resolve/read the needed media through Astrid. Use the returned handle in the input asset map. The successful imported Matrix media handle was `sha256:aa84f8370736f6fd295f4c8037654a118864060d6b15134625ab9aa88e64f092`. Preserve the approved source interval, target line/profile/parameters, and request identity exactly; only repin the media handle if importing into a new workspace changes its ID. Keep imports and request artifacts in the run evidence directory.

**Proves:** the Astrid project contains the imported authoring records/media and the selected handle resolves through Astrid. **Does not prove:** a provider worker can fetch or decode the asset. Check the imported media's size/hash using Astrid's media open/read interface when the workflow requires exact identity.

## 3. Configure and confirm the network volume

Use `astrid machines setup --help` from the installed CLI. Review the selected account's existing volume and placement first; do not create/resize/delete one for this procedure. Configure the approved existing volume, datacenter, GPU, and immutable image digest with the setup command's `--volume`, `--datacenter`, `--gpu`, `--image`, and budget options, then inspect the resulting preferences through Astrid. Example shape (values are illustrative; replace with owner-approved values):

```sh
export ASTRID_RUNTIME_DATA_ROOT=/absolute/path/to/pilot/data
"$ASTRID_BIN" machines setup \
  --volume '<existing-volume-id-or-name>' \
  --datacenter '<approved-datacenter>' \
  --gpu '<qualified-gpu>' \
  --budget-usd '<authorized-global-budget>' \
  --image '<approved-image@sha256:digest>' \
  --json
```

The staged pilot selected existing 300 GB volume `2z2dlu1v8g` (`storage`), mounted at `/workspace`, in `EUR-NO-1`; image `runpod/base@sha256:820c605eaaa276de20a0d77993fb0846d54e180efff5de67d46341ed399b5a7f`, RTX 5090, hourly ceiling $2, total cap $3. The `stage-volume-setup.log` result records these preferences and successful provider lookup. They are historical values, not defaults for another account.

**Proves:** Astrid accepted/persisted the selected setup preferences and (if the setup result confirms it) could read the volume from the authenticated account. **Does not prove:** GPU capacity or a successful mount. If volume confirmation fails, inspect sanitized Runtime host logs for network/TLS errors, correct service proxy/trust inheritance, then repeat the read-only/setup confirmation. Do not issue a claim while volume identity is unknown.

## 4. No-rental rehearsal: do every gate before the paid boundary

Set `ASTRID_BIN`, `ASTRID_PYTHON`, `ASTRID_RUNTIME_DATA_ROOT`, project, and exact input JSON to the installed host values. Use fresh temporary output and receipt paths. Follow the full commands and evidence meanings in [`rehearsal.md`](rehearsal.md), especially its staged rehearsal section:

1. Run `astrid generate video ... --dry-run --json` for the exact H3 entry and inputs. In the successful run it exited 0, returned `ready`, resolved the exact source hash/range `[81.05,84.299)`, and planned 78 input frames at 24 fps. A dry run proves CPU planning/normalization only; it does not perform Runtime admission.
2. Check `vibecomfy` using the *same installed Python* as the Runtime host. Also read the Runtime capability view through Astrid and confirm `vibecomfy.run` is `ready`. The staged view was ready with required GPU resource. `astrid doctor` still reported missing Remotion `node_modules`; tracing the H3 `after_outputs` path showed it directly calls H3 compose/verify and those modules do not use Remotion. Keep that global doctor warning in the report; don't turn it into a generic healthy claim.
3. Choose a fresh unique output path and recovery path. Confirm the recovery path does not exist and its parent permits a create/write/fsync/remove probe. A successful check is only a filesystem disposition check. Dry-run does **not** create or exercise an AdmissionReceipt, lock, or replay.
4. Use the installed Python to call `astrid.packs.runpod.managed_sources._pins()` and `ensure_managed_sources()` against an isolated temporary data root. Check all four actual `git rev-parse HEAD` values equal the installed pinned full SHAs and all worktrees are clean. Successful staged run fetched all four exact commits; see `rehearsal-evidence/managed-sources.stdout` for the identities. This proves source fetchability from that network and installed-manifest consistency, not worker bootstrap or provider admission.

Stop on any failure or unexplained difference. Do not manufacture a manifest in the venv to pass the check. The working local source venv lacked an installed release manifest and failed RunPod bootstrap. Earlier VibeComfy absence and reuse of a recovery receipt also blocked admission. A new distinct operation needs its own fresh receipt/output paths; the video CLI did not expose `--resume` in this build even though the H3 skill text mentioned it. Do not try a new operation on an old receipt path.

## 5. One bounded waiting claim (paid boundary)

Before claim, record a fresh UTC clock check, provider quote/placement, empty machine list, existing volume confirmation, and the explicit maximum hourly rate, total cap, hard cumulative stop threshold, and UTC deadline. The timeout must be short and bounded. Use the installed CLI and Astrid only; never call provider APIs directly. Example syntax from the successful wait, with all values replaced by current authorized values:

```sh
"$ASTRID_BIN" machines claim \
  --gpu '<qualified-gpu>' \
  --max-hourly-usd '<hourly-limit>' \
  --max-usd '<claim-cap>' \
  --deadline '<absolute-UTC-deadline>' \
  --for 30m --capacity-timeout 30m \
  --consent paid --json
```

The successful staged claim used RTX 5090, $2/hour ceiling, $2.30 claim cap, 30-minute capacity wait, and existing volume. Astrid reported allocation `s4u2c594zyrro1` at 20:44:25Z, provider rate $1.39/hour, and `self_stop: true`; the claim task succeeded after 7m40s. Capacity waiting itself was recorded as not creating pod charges. Monitor claim state and Runtime host logs; do not start another claim while this one is pending/allocated. On allocation, record pod ID, allocation time, effective provider expiry, hourly rate, watchdog/self-stop acknowledgement, and cumulative estimate. If no allocation before deadline, verify no machine remains and end the attempt. If allocated but watchdog acknowledgement is missing, follow the approved immediate-release policy; do not leave the pod unattended.

Maintain the *stricter* cumulative unfinished-candidate threshold independently of provider claim cap. In the historical run, prior estimated spend was $0.2931 and owner required release once cumulative spend reached $2.40 without a finished candidate, despite $2.30 claim cap. Recompute this from the new run's authorized budget; do not copy historical numbers.

## 6. Submit one exact H3 request

Only after the claim succeeds and readiness is confirmed, use the installed CLI, the exact reviewed request/input JSON, and fresh output/recovery paths. This is a paid action. The successful command shape was:

```sh
ASTRID_RUNTIME_DATA_ROOT="$ASTRID_RUNTIME_DATA_ROOT" \
  "$ASTRID_BIN" generate video \
    --entry h3 --mode v2v \
    --inputs-json "$H3_INPUTS" \
    --placement runpod --project "$ASTRID_PROJECT" \
    --out "$FRESH_OUTPUT_DIR" \
    --recovery-path "$FRESH_RECOVERY_PATH" \
    --json
```

The operation must preserve the source interval, source media handle, target line/profile/settings, and generation parameters from the reviewed dry-run. Record the task ID and admission timestamp immediately. Monitor Astrid task status, preparation journal, and sanitized host pack-host log. Preparation reaching `start_engine` means selected-model alignment and integrity verification completed; it does not mean generation or output verification succeeded. In the pilot, core models were reported cached, the Pika LoRA was fetched, `trust_unchanged=true`, and verification reported trusted records/witnesses with `hashed=0, skipped=14`. The logs exposed no measured transfer byte count; the LoRA's declared locked size was not a measured transferred-byte value.

Enforce the authorized model-preparation cutoff and cumulative cost threshold. If a host-side submission/bootstrap error occurs, or a required cutoff is reached, release promptly under the approved policy. Do not silently retry with a new task/receipt. A retry is a new paid action requiring fresh paths and explicit authorization.

## 7. Read back, verify, release, and reconcile

Wait for the Astrid task to finish, then retrieve task outputs/logs/media through Astrid SDK/CLI. Read the H3 composition and verification artifacts; require `verified`, expected frame count/duration, audio coverage, protected-prefix evidence, and output identity/hash. The successful run's raw graph emitted 248 frames including 39 context frames; H3 composed a 240-frame, 10.0-second, 24 fps candidate with 48 kHz audio coverage and preserved the source prefix [0,3.25s]. Candidate SHA-256 was `6837b0a200c0a0139348802ccfb59d36cd15e92b3c8d458146cc65f341d64af5`. The Matroska container had an `.mp4` suffix; inspect media metadata rather than assuming the suffix. Verification establishes technical checks, not subjective/taste approval or transcript correctness.

Release through Astrid's machine release capability/CLI with `"$ASTRID_BIN" machines release --json '<exact-machine-id>'`; use the exact allocated machine ID and preserve the network volume. Then confirm via Astrid that the machine is ended/absent, release result succeeded, account listing succeeded and reports absent, and the volume remains. The successful release terminated `s4u2c594zyrro1`; exact GET returned 404, account list confirmed absence, volume was preserved, and Astrid estimated $0.5918 for that pod. Record release result, timestamps, pod state, and estimate. Reconcile provider billing separately if required: Astrid's estimate is not a billing statement.

## What went wrong and how it was resolved

- Source checkout/venv was not an installed release; worker bootstrap rejected its missing installed manifest. Use the installer's managed copy and its manifest.
- Early admission failed because `vibecomfy` was missing from the Runtime Python. The successful staged version contained the exact pinned package; verify same-host import and capability before claim.
- A retry reused an existing recovery receipt and was refused before admission. Use a fresh unique receipt/output path for a distinct operation. The CLI's video `--resume` discrepancy is documented in [`rehearsal.md`](rehearsal.md); don't rely on it.
- The first staged volume confirmation failed because the Runtime service lacked proxy/certificate trust. The log showed TLS verification errors. The Runtime was safely restarted with approved inherited proxy/cert settings and the existing key passed only through an in-memory environment allowlist; volume confirmation then succeeded. Never disable TLS verification or expose credential values.
- Readiness and dry-run did not imply paid success. Only the admitted task proved model preparation, worker execution, H3 composition/verification, and returned artifact. Release confirmation was separately required.

## Historical evidence map

- Installed-host dry run, receipt disposition, package/capability checks, exact pins and source fetch: [`rehearsal.md`](rehearsal.md), [`rehearsal-evidence/`](rehearsal-evidence/).
- Claim: [`stage-wait-retry1.log`](stage-wait-retry1.log).
- Generation and output: [`stage-generation.log`](stage-generation.log), [`composition-open.json`](composition-open.json), [`rehearsal-evidence/final-h3-composition.json`](rehearsal-evidence/final-h3-composition.json), [`rehearsal-evidence/final-h3-verification.json`](rehearsal-evidence/final-h3-verification.json).
- Release and cost timeline: [`stage-release.log`](stage-release.log), [`cost.md`](cost.md).
