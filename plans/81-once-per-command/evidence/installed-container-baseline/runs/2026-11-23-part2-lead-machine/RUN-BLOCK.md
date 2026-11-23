# Part 2: one installed three-arm run on the Lead machine

Execute once on one quiet CPU machine. Use all three arms in this one session; do not combine samples from separate machines or attempts. Numbers from the previous box and the Lead machine are not comparable. This is a stand-in ComfyUI on loopback, with npm omp, no GPU, pod or paid service; `--no-wait` measures through task admission, not generation completion. There is no real ComfyUI node-info answer. The committed wrapper adds `--timings` for `after` and `vc48` but not `before`, so the wall comparisons include that instrumentation asymmetry.

Each numbered step has one attempt. Stop at any failed command, missing object, nonempty target, mismatch, failed preflight, insufficient space or gate/command failure; retain and return what was produced. Do not retry, change a pin, mix results or stitch attempts. Wrapper-internal readiness and load-wait behavior remains the committed recipe. The run's qualification may fail even when collection completed; keep the raw evidence and report the exit status without interpretation.

The arm labels are fixed by the driver: `before` = stock base; `after` = Part 2; `vc48` = Part 1 landed. The resulting `after/before` and `vc48/before` ratios use the intended base. The fixed round order is before, after, vc48. Each of same-prompt, changed-prompt and timeline groups has one warmup per arm then five measured interleaved rounds (54 commands total). Prompts are `a red square on a plain background` and `a blue square on a plain background, variation {k}`; timeline edits add a three-second media layer at `3*k`. The recipe gates each command's start on one-minute load strictly below 1.0, with a 600-second wait limit and the timing lock. It never substitutes an ungated sample.

Attestation is **off** as ruled: identity evidence is the selected `current` pointer and requested/installed manifests, not byte-level Runtime attestation and not proof of which socket a command used. Preserve those reads independently. Recipe commit: `102ebc4679b688ce4521292961239e9af402c1c2`, `plans/81-once-per-command/evidence/installed-container-baseline/` (`run-ab-installed.sh`, `ab_run.py`, `ab_summary.py`, manifests and stand-in).

## 1. Reserve space and inspect the machine

Prior installed footprints were approximately 3.5 GiB before, 4.1 GiB landed and 3.5 GiB after, plus about 1.2 GiB for even one installer cache: a conservative 12.3 GiB peak estimate. The Lead requires at least **18 GiB free** (peak plus 50%) on `/root/codex` at the start, then at least **4 GiB free after each arm install**, with each arm’s disposable download cache removed immediately after its install. The reported 23 GiB passes the start check. Ensure no other heavy process or benchmark is running; stop if the machine is not quiet. The executor must inspect `top` output before proceeding.

```bash
set -euo pipefail
mkdir -p /root/codex/p81box
python3 - <<'PY'
import shutil
free = shutil.disk_usage('/root/codex/p81box').free
print('free bytes:', free, 'required:', 18 * 1024**3)
if free < 18 * 1024**3: raise SystemExit('STOP: insufficient free space')
PY
uptime
top -b -n 1 | sed -n '1,25p'
nproc
free -h
uname -a
```

## 2. Fetch and prove every requested commit

The checkout and run directories below must not exist. Exact object checks precede any install; use these explicit remote URLs or equivalent verified mirrors containing the same objects.

```bash
set -euo pipefail
ROOT=/root/codex/p81box/part2-once
mkdir "$ROOT"
mkdir "$ROOT/receipts"
git clone --no-checkout https://github.com/banodoco/astrid-dev.git "$ROOT/dev"
git -C "$ROOT/dev" fetch origin 102ebc4679b688ce4521292961239e9af402c1c2
git -C "$ROOT/dev" checkout --detach 102ebc4679b688ce4521292961239e9af402c1c2
git clone --no-checkout https://github.com/banodoco/astrid-agent.git "$ROOT/agent"
git -C "$ROOT/agent" fetch origin 8807f820eb47d6018db723511e024a0a123fbe95 bd94a6e11dd0e9fb5e488e66f349db564a8220a8
git clone --no-checkout https://github.com/banodoco/astrid-runtime.git "$ROOT/runtime"
git -C "$ROOT/runtime" fetch origin 3c28211f3cb7ac4867ad744d8cdeeb38dd4484c5 53a035ba7c04156dc45aa096f099b4c0224dfb14
git clone --no-checkout https://github.com/banodoco/VibeComfy.git "$ROOT/vibe"
git -C "$ROOT/vibe" fetch origin 48b5fa9e45630e1bc502651975ec0ef3a5e74c4c 675f5dc2658197318a95e0e1b7c5b232b17cd9d5
for sha in 8807f820eb47d6018db723511e024a0a123fbe95 bd94a6e11dd0e9fb5e488e66f349db564a8220a8; do git -C "$ROOT/agent" cat-file -e "$sha^{commit}"; git -C "$ROOT/agent" rev-parse "$sha^{commit}"; done
for sha in 3c28211f3cb7ac4867ad744d8cdeeb38dd4484c5 53a035ba7c04156dc45aa096f099b4c0224dfb14; do git -C "$ROOT/runtime" cat-file -e "$sha^{commit}"; git -C "$ROOT/runtime" rev-parse "$sha^{commit}"; done
for sha in 48b5fa9e45630e1bc502651975ec0ef3a5e74c4c 675f5dc2658197318a95e0e1b7c5b232b17cd9d5; do git -C "$ROOT/vibe" cat-file -e "$sha^{commit}"; git -C "$ROOT/vibe" rev-parse "$sha^{commit}"; done
git -C "$ROOT/vibe" checkout --detach 675f5dc2658197318a95e0e1b7c5b232b17cd9d5
# Make each requested commit reachable by a local ref and permit SHA fetches.
for item in \
  agent:8807f820eb47d6018db723511e024a0a123fbe95 \
  agent:bd94a6e11dd0e9fb5e488e66f349db564a8220a8 \
  runtime:3c28211f3cb7ac4867ad744d8cdeeb38dd4484c5 \
  runtime:53a035ba7c04156dc45aa096f099b4c0224dfb14 \
  vibe:48b5fa9e45630e1bc502651975ec0ef3a5e74c4c \
  vibe:675f5dc2658197318a95e0e1b7c5b232b17cd9d5; do
  repo=${item%%:*}; sha=${item#*:}
  git -C "$ROOT/$repo" branch "run-proof-$sha" "$sha"
  git -C "$ROOT/$repo" config uploadpack.allowAnySHA1InWant true
  git -C "$ROOT/$repo" config uploadpack.allowReachableSHA1InWant true
done
# Prove each exact object can be fetched by SHA through the local Git transport.
mkdir "$ROOT/fetch-proof"
for item in \
  agent:8807f820eb47d6018db723511e024a0a123fbe95 \
  agent:bd94a6e11dd0e9fb5e488e66f349db564a8220a8 \
  runtime:3c28211f3cb7ac4867ad744d8cdeeb38dd4484c5 \
  runtime:53a035ba7c04156dc45aa096f099b4c0224dfb14 \
  vibe:48b5fa9e45630e1bc502651975ec0ef3a5e74c4c \
  vibe:675f5dc2658197318a95e0e1b7c5b232b17cd9d5; do
  repo=${item%%:*}; sha=${item#*:}; proof="$ROOT/fetch-proof/$repo-$sha"
  git init -q "$proof"
  git -C "$proof" fetch --depth=1 --no-tags "file://$ROOT/$repo" "$sha"
  test "$(git -C "$proof" rev-parse 'FETCH_HEAD^{commit}')" = "$sha"
  printf '%s %s fetchable\n' "$repo" "$sha" | tee -a "$ROOT/receipts/fetch-proof.txt"
done
```

The exact tuples are:

| Driver arm | Agent | Runtime | VibeComfy |
| --- | --- | --- | --- |
| before | `8807f820eb47d6018db723511e024a0a123fbe95` | `3c28211f3cb7ac4867ad744d8cdeeb38dd4484c5` | `48b5fa9e45630e1bc502651975ec0ef3a5e74c4c` |
| after | locally generated trial commit on `bd94a6e11dd0e9fb5e488e66f349db564a8220a8` | `53a035ba7c04156dc45aa096f099b4c0224dfb14` | `675f5dc2658197318a95e0e1b7c5b232b17cd9d5` |
| vc48 | `bd94a6e11dd0e9fb5e488e66f349db564a8220a8` | `53a035ba7c04156dc45aa096f099b4c0224dfb14` | `48b5fa9e45630e1bc502651975ec0ef3a5e74c4c` |

## 3. Generate the trial pins locally, never push

Use a shallow local checkout with no remote after fetching; this avoids a partial clone whose missing objects make the installer's Git fetch fail. Install only VibeComfy's ordinary CPU Python dependencies for the generator. The generated commit SHA depends on commit metadata; its **tree must equal** `6d88c6f75c62f664293db167bfafb178f4073764`. The reference shallow commit is `58bf34ffed0e4d378112e2389616cd80caae4f19`; regenerate and compare the tree, do not assume its object exists remotely.

```bash
set -euo pipefail
ROOT=/root/codex/p81box/part2-once
git init "$ROOT/trial-agent"
git -C "$ROOT/trial-agent" fetch --depth=1 https://github.com/banodoco/astrid-agent.git bd94a6e11dd0e9fb5e488e66f349db564a8220a8
git -C "$ROOT/trial-agent" checkout --detach FETCH_HEAD
python3 -m venv "$ROOT/generator-venv"
"$ROOT/generator-venv/bin/python" -m pip install -e "$ROOT/vibe"
(cd "$ROOT/trial-agent" && "$ROOT/generator-venv/bin/python" scripts/vibecomfy_pin.py 675f5dc2658197318a95e0e1b7c5b232b17cd9d5 --checkout "$ROOT/vibe")
git -C "$ROOT/trial-agent" add astrid/packs/runpod/pins.json astrid/packs/runpod/recipe.linux-cu130.json astrid/packs/vibecomfy/environment.windows-nvidia.json astrid/packs/vibecomfy/extensions/generation.engine/comfyui.yaml astrid/packs/vibecomfy/pins.json astrid/packs/vibecomfy/recipe.windows-cu130.json
test "$(git -C "$ROOT/trial-agent" write-tree)" = 6d88c6f75c62f664293db167bfafb178f4073764
git -C "$ROOT/trial-agent" -c user.name='Local trial' -c user.email='local-trial@example.invalid' commit -m 'Set local trial VibeComfy pins'
test "$(git -C "$ROOT/trial-agent" rev-parse HEAD^)" = bd94a6e11dd0e9fb5e488e66f349db564a8220a8
test -z "$(git -C "$ROOT/trial-agent" remote)"
git -C "$ROOT/trial-agent" branch local-trial HEAD
git -C "$ROOT/trial-agent" bundle create "$ROOT/receipts/trial.bundle" local-trial
sha256sum "$ROOT/receipts/trial.bundle" > "$ROOT/receipts/bundle-sha256.txt"
git -C "$ROOT/trial-agent" config uploadpack.allowAnySHA1InWant true
git -C "$ROOT/trial-agent" config uploadpack.allowReachableSHA1InWant true
trial_sha=$(git -C "$ROOT/trial-agent" rev-parse HEAD)
trial_proof="$ROOT/fetch-proof/trial-$trial_sha"
git init -q "$trial_proof"
git -C "$trial_proof" fetch --depth=1 --no-tags "file://$ROOT/trial-agent" "$trial_sha"
test "$(git -C "$trial_proof" rev-parse 'FETCH_HEAD^{commit}')" = "$trial_sha"
printf 'trial-agent %s fetchable\n' "$trial_sha" | tee -a "$ROOT/receipts/fetch-proof.txt"
git -C "$ROOT/trial-agent" diff HEAD^ HEAD > "$ROOT/receipts/trial-pin.diff"
git -C "$ROOT/trial-agent" rev-parse HEAD HEAD^{tree} > "$ROOT/receipts/trial-identity.txt"
```

All seven local fetch proofs use shallow fetches, and must pass before any install; return `fetch-proof.txt`. A failed proof stops the run.

The six expected paths are precisely the six arguments to `git add` above. The tree check covers all files, including the generated digests. Never push the trial commit.

## 4. Create and hash the three manifests

Start from the committed npm-omp and candidate manifests. The baseline and landed Agent recipes already pin old VibeComfy. Both Runtime versions declare schema digest `sha256:2c6a76e17b4441398ab91e3e9d6283a719fd5b08807447db9dbf2ecc5e1339a2`. Paths and the locally generated commit are machine-specific, so record the generated manifest hashes; do not reuse an old absolute-path manifest.

```bash
set -euo pipefail
ROOT=/root/codex/p81box/part2-once
TOOL="$ROOT/dev/plans/81-once-per-command/evidence/installed-container-baseline"
mkdir "$ROOT/manifests"
TRIAL=$(git -C "$ROOT/trial-agent" rev-parse HEAD)
python3 - "$ROOT" "$TOOL" "$TRIAL" <<'PY'
import json,sys
from pathlib import Path
root,tool,trial=Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3]
base=json.loads((tool/'manifest-omp-npm.json').read_text())
candidate=json.loads((tool/'manifest-candidate-vc48.json').read_text())
digest='sha256:2c6a76e17b4441398ab91e3e9d6283a719fd5b08807447db9dbf2ecc5e1339a2'
for name,src,agent,runtime,vibe in [
 ('before',base,'8807f820eb47d6018db723511e024a0a123fbe95','3c28211f3cb7ac4867ad744d8cdeeb38dd4484c5','48b5fa9e45630e1bc502651975ec0ef3a5e74c4c'),
 ('vc48',candidate,'bd94a6e11dd0e9fb5e488e66f349db564a8220a8','53a035ba7c04156dc45aa096f099b4c0224dfb14','48b5fa9e45630e1bc502651975ec0ef3a5e74c4c'),
 ('after',candidate,trial,'53a035ba7c04156dc45aa096f099b4c0224dfb14','675f5dc2658197318a95e0e1b7c5b232b17cd9d5')]:
 m=json.loads(json.dumps(src)); m['agent']={'sha':agent,'repo':str(root/('trial-agent' if name=='after' else 'agent'))}; m['runtime'].update(sha=runtime,schema_digest=digest); m['vibecomfy']['sha']=vibe
 assert m['tools']['omp']['source']=='@oh-my-pi/pi-coding-agent@18.12.6'
 (root/'manifests'/f'{name}.json').write_text(json.dumps(m,indent=2)+'\n')
PY
sha256sum "$ROOT"/manifests/*.json | tee "$ROOT/receipts/manifest-sha256.txt"
```

## 5. Install the three arms and perform untimed pin/version preflight

Use the same installer as the committed recipe. Install in the fixed order below, once each, then remove that arm's disposable download cache and stop if less than 4 GiB remains. The installer starts local services; this is preflight, not a timed sample. The Lead's 18 GiB start rule includes the staged-install peak.

```bash
set -euo pipefail
ROOT=/root/codex/p81box/part2-once
TOOL="$ROOT/dev/plans/81-once-per-command/evidence/installed-container-baseline"
mkdir "$ROOT/installs"
command -v ss >/dev/null 2>&1 || { echo "STOP: ss is required for port checks" >&2; exit 1; }
for port in 17340 17341 17342 18188; do
  if ss -H -ltn "sport = :$port" | grep -q .; then echo "STOP: port $port occupied"; exit 1; fi
done
curl -fsS -o "$ROOT/receipts/install.sh" https://astrid.haus/install
printf '%s  %s\n' c268a5fae7ff318414745cee7bfcec13b6d7a81434f7aaa10d218ffe28248fff "$ROOT/receipts/install.sh" | sha256sum -c -
for arm in before after vc48; do
  case "$arm" in before) suffix=; door=17340;; after) suffix=-after; door=17341;; vc48) suffix=-vc48; door=17342;; esac
  h="$ROOT/installs/home$suffix"; program="$ROOT/installs/program$suffix"; data="$ROOT/installs/data$suffix"
  mkdir -p "$h" "$data"
  ( export HOME="$h" XDG_DATA_HOME="$h/.local/share" XDG_STATE_HOME="$h/.local/state" XDG_CONFIG_HOME="$h/.config" XDG_CACHE_HOME="$h/.cache" ASTRID_RUNTIME_DOOR_PORT="$door"
    unset ASTRID_PREPARED_CONNECTION ASTRID_RUNTIME_ENDPOINT ASTRID_RUNTIME_LAUNCHER ASTRID_RUNTIME_CREDENTIAL ASTRID_RUNTIME_DATA_ROOT || true
    sh "$ROOT/receipts/install.sh" --manifest "$ROOT/manifests/$arm.json" --root "$program" --data-root "$data" --yes --autostart off --command on --skills off --skill-copies off </dev/null > "$ROOT/receipts/install-$arm.log" 2>&1
    selected=$(python3 "$TOOL/runtime_attestation.py" --selected "$program/current")
    python3 - "$ROOT/manifests/$arm.json" "$selected/manifest.json" <<'PY2'
import json,sys
want,got=(json.load(open(p)) for p in sys.argv[1:])
for key in ('agent','runtime','vibecomfy','lifecycle'):
 if want[key]['sha'] != got[key]['sha']: raise SystemExit(f'STOP: {key} pin mismatch')
PY2
    "$program/run-astrid" --version > "$ROOT/receipts/version-$arm.txt" 2>&1
  )
  python3 - "$h/.cache" <<'PY2'
import shutil,sys
from pathlib import Path
p=Path(sys.argv[1])
if p.is_dir(): shutil.rmtree(p)
PY2
  python3 - "$ROOT" "$arm" <<'PY2'
import shutil,sys
free=shutil.disk_usage(sys.argv[1]).free
print(sys.argv[2], 'free bytes:', free)
if free < 4*1024**3: raise SystemExit('STOP: less than 4 GiB free after install')
PY2
done
```

## 6. Run the committed driver once

This one invocation rechecks selected manifests, then runs the complete session. Do not run a separate timed invocation or repeat on failure. `ASTRID_RUNTIME_SOURCE_REPO` is provided for provenance; byte attestation is disabled explicitly. The freshly staged services may hold their own door ports; the stand-in port 18188 must still be free. Set no connection overrides.

```bash
set -euo pipefail
ROOT=/root/codex/p81box/part2-once
TOOL="$ROOT/dev/plans/81-once-per-command/evidence/installed-container-baseline"
command -v ss >/dev/null 2>&1 || { echo "STOP: ss is required for port checks" >&2; exit 1; }
if ss -H -ltn "sport = :18188" | grep -q .; then echo "STOP: port 18188 occupied"; exit 1; fi
export IB="$ROOT/installs" EVIDENCE_DIR="$ROOT/receipts/run"
export BEFORE_MANIFEST="$ROOT/manifests/before.json" CANDIDATE_MANIFEST="$ROOT/manifests/after.json" VC48_MANIFEST="$ROOT/manifests/vc48.json"
export ASTRID_AB_ATTEST=off ASTRID_RUNTIME_SOURCE_REPO="$ROOT/runtime"
export ARMS='before after vc48' SAMPLES=5 LOAD_MAX=1.0 LOAD_WAIT_SECONDS=600
unset ASTRID_PREPARED_CONNECTION ASTRID_RUNTIME_ENDPOINT ASTRID_RUNTIME_LAUNCHER ASTRID_RUNTIME_CREDENTIAL ASTRID_RUNTIME_DATA_ROOT || true
if "$TOOL/run-ab-installed.sh" --run; then status=0; else status=$?; fi
printf '%s\n' "$status" > "$ROOT/receipts/driver-exit.txt"
echo "Driver exit: $status. Stop on nonzero; retain and return all available receipts."
```

## 7. Record and return receipts, including on failure

Do not launch another sample. Read each available regular `current` pointer and selected manifest with the committed helper; preserve tuple/pin reads and the requested manifests, driver exit, `records.jsonl`, `summary-ab.json`, `console.log`, load samples and all raw evidence. A missing file is a failed/incomplete run, never a reason to rerun. Capture machine description and hash all returned files. Return `/root/codex/p81box/part2-once/receipts/` as a folder to the orchestrator, without interpreting the result.

```bash
set -euo pipefail
ROOT=/root/codex/p81box/part2-once
TOOL="$ROOT/dev/plans/81-once-per-command/evidence/installed-container-baseline"
{ nproc; free -h; uname -a; uptime; df -h "$ROOT"; } > "$ROOT/receipts/machine.txt"
for pair in 'before:' 'after:-after' 'vc48:-vc48'; do
  arm=${pair%%:*}; suffix=${pair#*:}; program="$ROOT/installs/program$suffix"
  if [ -f "$program/current" ]; then
    cp "$program/current" "$ROOT/receipts/current-$arm.txt"
    selected=$(python3 "$TOOL/runtime_attestation.py" --selected "$program/current")
    cp "$selected/manifest.json" "$ROOT/receipts/selected-$arm.json"
  else echo "missing current: $arm" >> "$ROOT/receipts/incomplete.txt"; fi
done
cp -R "$ROOT/manifests" "$ROOT/receipts/manifests"
(cd "$ROOT/receipts" && find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS)
```

The trial commit is regenerated and verified by tree; its locally created bundle, bundle checksum, trial identity and pin diff are included in the receipts.
