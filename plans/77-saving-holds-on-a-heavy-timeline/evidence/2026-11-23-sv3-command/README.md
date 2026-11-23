# Plan 77 SV-3 measurement package

Status: static checks only. This package has not been run. It is the measurement successor to the SV-2a command
package (`../2026-11-23-sv2a-command/`), adapted to work on a copy of the retained sandbox data.

## Entry point

```
SV3_SIGNED_BACKUP=<canonical signed backup directory> \
SV3_RUNTIME_REF=<a ref in the candidate mirror that resolves to the Runtime SHA> \
  bash run-sv3-overlay.sh <candidate Runtime SHA> <approved package.sha256 digest>
```

Optional: `SV3_REPETITIONS` (default 3, one to nine). `SV3_STATIC_DRY_RUN=1` prints the fixed inputs and exits.
`SV3_TRACE=1` is refused, because the trace witness and trace verdict of SV-2a are not ported.

The Runtime SHA is an argument, not a value in the package. The approval covers the SHA and the package digest. The
tree is recorded in `candidate-tree.txt`. A commit SHA fixes its tree, so the approval covers the tree as well.

`package-digest.txt` holds the SHA-256 of `package.sha256`. That file lists the eight command inputs.

## What a run does

1. Checks identity. The package digest is compared, then `sha256sum -c` runs. The ref must resolve to the SHA in the
   mirror, and the retained base `77c38d03` must match. The dependency and contract diff against `77c38d03` must be
   empty. The retained program manifest, the App commit, the browser tooling commit and the stopped prior stack are
   checked as in SV-2a.
2. Takes the signed-backup and owner stat inventories, and the owner lock, as in SV-2a.
3. Archives the candidate source, verifies its git tree and records the file digests. Inventories the retained
   program before and after.
4. Makes one pristine copy of `direct-data` (about 521 MB) under `$out/pristine-data`. The original is only read.
5. For each repetition, copies the pristine data to `$out/work-data-<n>` and runs everything against that copy:
   - `prepare` rebases the copy's `catalog.json` and `source-profiles/astrid.json` (see the next section);
   - `up`, then the preview, then one headless browser session (`browser-sv3-measure.mjs`);
   - the Agent step (not established, see below);
   - an idle-safe `down` with three attempts, then the port and owner-exit checks;
   - the Runtime log and pack-host log byte deltas, and `pack-host.json`;
   - removal of the work copy, only after the stack stopped idle-safe.
6. Combines the repetitions into `measurements.jsonl` and `summary.tsv`.
7. Cleanup records the boundaries, the exit state, a privacy scan and `SHA256SUMS`. It removes the pristine copy.
   It stops only PIDs the script started, then TERM and KILL of whatever listens on ports 2400 and 17500.

Receipts go to `run/evidence/plan-77/round7-acceptance/sv3-measure-<SHA>/`.

## Data root and copy: where paths resolve

Verified by reading the SV-2a verify script, the overlay driver and the helper `runtimeRootForData`:

- Support root `= <data>/runtime`. Realm root `= <support>/realms/<realm>`. Discovery `= <support>/discovery.json`.
  The overlay checks `paths.runtime_support` against the support root, and the preview takes `--data-root`. All of
  these follow the data root argument, so a copy resolves the same way.
- `catalog.json` and `source-profiles/astrid.json` store **absolute** `data_root` paths of the original stack. The
  overlay and `verify-overlay.py` compare them to the support root. Without a rewrite the copy would be refused.
  `prepare` therefore rewrites the copy only: it replaces the original support prefix, then fails if any reference to
  the original data root remains. `rebase.json` records the digests before and after. A synthetic self-test in the
  scratchpad gave zero residual references and the expected candidate profile.
- **Deviation:** `runtimeRootForData` (quick-indicator `scripts/save-loop/cpu.mjs`) requires the data root to sit
  inside the owned stack root. A copy under `$out` fails that check. The driver replaces it with `runtimeIdentity()`:
  discovery `pid` and `runtime_instance_id`, `/proc/<pid>/stat` start time, and the proxy health (`status ok`,
  `workspace.v1`, the same instance). The stack ownership marker is no longer checked for the copy.

Not established:

- Runtime-internal absolute references beyond `catalog.json` and the source profile, such as paths inside the realm
  SQLite files or the content store. The rebase checks only the two JSON files. A copied Runtime may still refuse or
  write to the original path. Only a run can show this.
- Whether the Runtime or the preview keeps a lock or lookup keyed to the stack root rather than the data root.
- That the preview's `dev-local-workspace.mjs --data-root <copy>` serves the copy's realm (not run).

## Per-repetition scenarios (browser-sv3-measure.mjs)

One fresh headless profile per repetition, one browser session:

- **S0.** Page load is the first browser action. It ends at `fullWritable` (the editor's own ready wait) and
  the verified-head observation. Recorded: navigation to writable in ms, the status and body of
  `GET .../verified-head` (route family `timeline.verified_head.v1`, path `getTimelineVerifiedHead` in
  `client.ts`), and whether it was a refusal (HTTP 409 or `head_busy`).
- **cold.** One drag of the pinned clip to free space. The first drag is checked against the expected start,
  `191.3667`.
- **S1** one drag. **S2** two drags, 200 ms gap. **S3** ten drags, 150 ms gap. **S4** five drags, each waited to Saved.
  Each warm scenario ends with a 2 s settle.

For every commit POST: release to POST, POST to response, response to Saved (the source's definition), HTTP status
and any refusal with its reason text, taken from the response body. Every non-2xx response on any `/api/runtime`
route is kept in `non_2xx_runtime`. The POST count is checked against the network recorder: 19 per repetition
(1 + 1 + 2 + 10 + 5).

Destination and alternation come from `canonicalFreeSpace` and `planFreeSpace`. The SV-2a receipts show that
alternation is inherited: the prior two-save run moved the clip from 191.3667 to 189.3 and back to 191.3667
(`candidate-two-save-profile-20261123-retry/browser-two-save-profile.json`). Only two saves were observed, so the
behaviour over ten or more saves is not established.

### Deviations from the brief

- **Gap.** S2 and S3 gap from Saved, not from release. The next drag starts only after the previous POST is Saved,
  and the 200 ms or 150 ms gap is applied after that. Overlapping in-flight saves are not exercised. The planning
  reads the verified head, and the browser helper's `prepareSave` contract is written for one save at a time.
  Overlap is not established.
- **Counts.** `prepareSave` resets the tape counts per drag. The source resets them once only and its check only
  holds for two saves.
- **Helpers.** `drag()` in `lib.mjs` is not used. The geometry-checked sequence from the SV-2a driver covers it.
- **Sampler.** The Runtime sampler from the two-save driver is not used, because it is a profiler and not part of
  the timing path.

## Not included

- **Save while a generation runs.** Dropped by decision. The `head_busy` refusals seen earlier came from the pack
  host's idle claim poll, not from a running task. No local no-cost generation exists. Where a scenario could be
  added: a new entry in the `scenarios` array of `browser-sv3-measure.mjs`, with a generation start step before the
  drag.

## Pack host and logs

The script does not start, stop or alter the pack host. Per repetition it records:

- `service-pack-host-delta.txt`, the byte delta of `service-pack-host.log` from the offset before `up`;
- `runtime-log-delta.txt`, the same for `runtime.log`;
- `pack-host.json`, with the delta size in bytes, the number of lines mentioning `claim`, and the `pgrep -fa pack`
  count of lines that also mention `host`. It is a count only, with no group or owner assertion. An empty delta is
  recorded as `pack host not polling`.

## Agent authoring commit

Not established, so the step writes `agent-commit: not established` and does not fail. The files read do not settle:

- the interpreter (the retained `program/versions/4b62ab1a6521/py/bin/python` or the installed Agent),
- the working directory,
- how the Runtime door is found for a copied data root,
- the key name of the receipt id.

The stub `agent_commit()` in the script carries these as its TODO. The documented invocation is
`python3 -m astrid timelines edit <timeline> --project <project> --clip parent/clip:<id> --on <seconds>
--idempotency-key sv3-<n> --json`. The clip, project and timeline are in `fixture.json` and the driver constants. Its
value (`fixture-video-0190`, `042a5c02...`, `save-loop-heavy-1d4576fd`) is not used yet.

## Processes, ports and paths: what is kept and what is dropped

Kept from SV-2a: TERM then KILL of PIDs the script started (`stop_pid`, with a 10 s watchdog). Fallback TERM and KILL
of listeners on 2400 and 17500. The health answer through 2400 (`status ok`, `workspace.v1`, the instance). Port-closed
checks on 2400, 17500 and 17501. Owner-exit check. The Runtime `down` with idle-safe. The lock write.

Dropped: process-group proofs, `group-live`, group members in `preview-after`, the trace witness, the trace verdict,
the `pkill` of Chrome by profile path. In its place, a read-only count of Chrome processes on the profile path
(`chrome-residue.txt`). That count fails the repetition if it is not zero, and nothing is killed.

The SV-2a process setting `ASTRID_RUNTIME_TIMELINE_DIAGNOSTICS=1` is NOT set here, so the Runtime runs with production settings and no trace.

## Unverified assumptions (not confirmed by any receipt)

- `setsid --wait` forwards TERM to the preview launcher, and the launcher stops its own detached children. If not,
  the port fallback is what stops them.
- The Runtime's `down` returns `status stopped` and `idle.safe true` on the copy, as it did on the original.
- The browser helpers `observeRequests`, `wireCommits`, `publicSnapshot`, `canonicalFreeSpace` and
  `planFreeSpace` behave the same on a copied data root. They read through the origin, so they should.
- The `jq` filters in `combine_outputs` were compiled and run on sample lines, with the rename fix applied. The per-
  repetition filter runs on a sample receipt. The full rep receipt was not produced by a run.
- The pack host is registered and polling during a run. That is recorded, not asserted.
- `pgrep -fa pack` counts only the pack-host processes. The count is taken without a group or owner check.

## Static checks run for this change

`bash -n run-sv3-overlay.sh`; `node --check` on the driver, `arm-free-space.mjs` and `reused-trace-helpers.mjs`; the
Python AST parse of `verify-overlay.py`, `overlay-direct.py` and `overlay-guard/sitecustomize.py`; the JSON parse of
`approved-input.json`; `jq` compilation of the combiner filters; and a synthetic rebase self-test in the scratchpad.
Nothing was run as a package, and no product process was started.

## Review notes added by the lane host

- `runtime/adopt-journal.json` is copied unchanged and still names the original realm paths (three occurrences). Whether the Runtime reads it at start is not established; if it does, the copy could touch the original realm directory, which the original-data boundary listing would show.
- S2 (two edits) and S3 (ten edits) wait for Saved between drags, so they measure sequential saves, not overlapping edits. If the Runtime or editor should be measured with edits released while a save is in flight, say so and the gap/count logic changes; the POST count assertion in the script (19) then has to be dropped.
- The signed backup and the original `direct-data` are only read; the original-data listing before/after is compared at cleanup.
