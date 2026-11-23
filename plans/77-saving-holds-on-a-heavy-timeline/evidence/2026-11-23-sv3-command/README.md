# Plan 77 SV-3 measurement package

Status: static checks only. This package has not been run. It measures the save path on a COPY of the retained
sandbox data. The original is only read. It is the measurement successor to `../2026-11-23-sv2a-command/`.

## Purpose and the head_busy context

This package measures the editor's save timing for the candidate Runtime SHA, which is a parameter. The candidate is
the fix for the `head_busy` refusal that Plan 78 traced to the pack host's idle claim poll. Therefore:

- S0 and every scenario S1 to S4 must run WITH the pack host polling, as in a normal install. The package does not
  start, stop or alter the pack host.
- `pack-host.json` records whether the pack host polled during the repetition: its status, `claim_lines` and
  `log_growth_bytes` (the byte delta of `service-pack-host.log`). A repetition whose delta is empty reads
  `pack host not polling`. Such a repetition does not count as evidence for the candidate.

## Entry point

```
SV3_SIGNED_BACKUP=<canonical signed backup directory> \
SV3_RUNTIME_REF=<a ref in the candidate mirror that resolves to the Runtime SHA> \
  bash run-sv3-overlay.sh <candidate Runtime SHA> <approved package.sha256 digest>
```

Optional: `SV3_REPETITIONS` (default 3, one to nine). `SV3_STATIC_DRY_RUN=1` prints the fixed inputs and exits.
`SV3_TRACE=1` is refused, because the trace witness and trace verdict of SV-2a are not ported.

The Runtime SHA is an argument and is not in the package. The approval covers the SHA and the package digest. The
tree is written to `candidate-tree.txt`. A commit SHA fixes its tree, so the approval covers the tree too.
`package-digest.txt` holds the SHA-256 of `package.sha256`, which lists the eight command inputs.

The SV-2a diagnostics variable `ASTRID_RUNTIME_TIMELINE_DIAGNOSTICS` is not set in this package. It was removed
on purpose after the SV-2a run.

## What a run does

1. Checks identity. The package digest is compared and `sha256sum -c` runs. The ref must resolve to the SHA, and the
   retained base `77c38d03` must match. The dependency and contract diff against `77c38d03` must be empty. The
   retained program manifest, the App commit, the browser tooling commit and the stopped prior stack are checked.
2. Takes the signed-backup and owner stat inventories and the owner lock write, as in SV-2a.
3. Archives the candidate source, verifies its git tree and records the file digests. Inventories the retained
   program before and after.
4. Audits the original data for links (`pristine-copy-audit.json`). It fails on a symlink that resolves outside the
   tree, or on a regular file whose hard links are not all inside the tree. Then makes one pristine copy under
   `$out/pristine-data`. Free space must stay at 16 GiB or more.
5. For each repetition, copies the pristine data to `$out/work-data-<n>` and runs everything against that copy.
   `prepare` rebases the copy's `catalog.json` and `source-profiles/astrid.json` (see the next section). Then `up`,
   the preview, one headless browser session (`browser-sv3-measure.mjs`), the Agent step (not established, see below),
   an idle-safe `down` with three attempts, the port and owner-exit checks, the runtime and pack-host log deltas,
   `pack-host.json`, and removal of the work copy when the stack stopped idle-safe.
6. Combines the repetitions into `measurements.jsonl` and `summary.tsv`.
7. Cleanup records the boundaries, a privacy scan and `SHA256SUMS`, and removes the pristine copy. It stops only PIDs
   the script started (TERM, then KILL after 10 s), then TERM and KILL of whatever listens on ports 2400 and 17500.
   If the driver dies, it TERMs the Chrome PIDs that `pgrep -f -- "--user-data-dir=<profile>/"` finds, waits 5 s, KILLs
   any left, checks again, and fails the run if any remain.

Receipts go to `run/evidence/plan-77/round7-acceptance/sv3-measure-<SHA>/`.

## Data root and copy: where paths resolve

Verified by reading the SV-2a verify script, the overlay driver and the helper `runtimeRootForData`:

- Support root `= <data>/runtime`. Realm root `= <support>/realms/<realm>`. Discovery `= <support>/discovery.json`.
  The overlay checks the support root, and the preview takes `--data-root`. Both follow the data root argument, so a
  copy resolves the same way.
- `catalog.json` and `source-profiles/astrid.json` store **absolute** `data_root` paths of the original stack.
  Without a rewrite the copy would be refused. `prepare` therefore rewrites the copy only, replaces the original
  support prefix, and fails if any reference to the original data root remains. `rebase.json` records the digests
  before and after. A synthetic self-test in the scratchpad gave zero residual references.
- **Deviation:** `runtimeRootForData` (quick-indicator `scripts/save-loop/cpu.mjs`) requires the data root to sit
  inside the owned stack root, so a copy under `$out` fails. The driver's `runtimeIdentity()` replaces it: discovery
  `pid` and `runtime_instance_id`, the `/proc/<pid>/stat` start time, and the proxy health (`status ok`,
  `workspace.v1`, the same instance).

Not established:

- Runtime-internal absolute references beyond the two JSON files, such as paths inside the realm SQLite files or the
  content store. A copied Runtime may still refuse or write to an original path. Only a run can show this.
- Whether the Runtime or preview keys anything to the stack root rather than the data root.
- The original-data boundary: the listing is recursive (`%y %P %s %T@ %m %i`). A change in any line fails the run.
  On the base Runtime only `workspace adopt` reads `adopt-journal.json` (`workspace_adopt.py:240`), and this package
  never calls it. The copy keeps that file unchanged, and the original is not touched.

## Scenarios per repetition (browser-sv3-measure.mjs)

Order: S0, cold, S1, S2, S2o, S3, S3o, S4, then the Agent step. One fresh headless profile, one browser session.

- **S0.** Page load is the first browser action. It ends when the editor is writable. Recorded: navigation to writable
  in ms, and the status and body of `GET .../verified-head` (route family `timeline.verified_head.v1`, path
  `getTimelineVerifiedHead` in `client.ts`). A refusal is HTTP 409 or reason `head_busy`.
- **cold.** One sequential drag, checked against the expected start `191.3667`.
- **S1** one sequential drag. **S2** two sequential drags, with 200 ms from Saved to the next drag. **S3** ten
  sequential drags, with 150 ms from Saved. **S4** five sequential drags, each waited to Saved.
- **S2o and S3o** (overlapped). The next edit is released 150 ms after the previous release, WITHOUT waiting for
  Saved. After the chain the driver waits, bounded at 180 s, until the requests have responded and the badge is
  saved or refused. It then waits 2 s and reads the public head. If the editor coalesces edits, the POST count is
  recorded and the timings are not attributed to drags. Overlap is not established. The predicted start of each
  edit is the previous planned destination, and the editor's rendered projection may not match it (see the drag plan).

Each drag records: `release_to_post_ms`, `post_to_200_ms`, `response_to_saved_ms`, `release_to_saved_ms`
(the sum of the first three), `post_to_saved_ms`, `http_status`, `refusal` (reason, body code and badge), the network
POST count, and `failed` with the failed phase and reason. A refusal or non-2xx response does NOT abort the
repetition. The driver records it and continues with the next drag. A sequential drag after a failure uses the
reset path (`prepareOverlapped`) and keeps the last verified head. Every non-2xx response on an `/api/runtime` route is
kept in `non_2xx_runtime`. The POST counts are recorded, not asserted.

### Prepare, arm and reset protocol

Matches `browser-two-save-profile.mjs` for every sequential drag:

- The first drag of the session needs an idle tape (`!armed` and no pointer). Each later drag needs the previous drag's
  arm and released pointer (`armed && pointer.up`), and the previous counts (one requested, responded and succeeded).
  It then consumes both: `armed=false`, `pointer=null`, counts reset. `armFreeSpace` needs `armed=false`, so the
  arm of the next drag succeeds only after the consume.
- The overlapped and reset paths (`prepareOverlapped`) consume the previous arm and pointer and reset the counts
  without checking the earlier counts. Whether the tape accepts a drag released while a save is in flight is NOT
  established by any receipt.

### Drag path plan (the real distances)

From the prior two-save receipts (`candidate-two-save-profile-20261123-retry/browser-two-save-profile.json`) and the
helper `planFreeSpace` (`reused-trace-helpers.mjs`):

- The pinned clip is 4 s long. The zoom is 32 px per second. The canonical span start went 187.2 s, then 189.3 s, then
  191.3667 s. Both saves moved the clip RIGHT, by 67 px and 66 px, about 2.07 s each.
- `planFreeSpace` always plans a rightward move: `dx = max(18, ceil(clip.right - x0) + 2)` pixels from the clip's
  centre, and the driver asserts `desiredStart > span.start`. The target is the lane's last clip. So the direction
  CANNOT alternate with this tape. A leftward move would land on the 36 earlier clips in the lane.
- Each drag moves the clip right by about half its width plus 2 px, which is about 2.07 s at this zoom. A repetition
  makes 31 drags (1 + 1 + 2 + 2 + 10 + 10 + 5), so the clip drifts about 64 s to the right.
- Room: before each plan the driver scrolls the clip into the centre of the view (`planFreeSpace({scroll: true})`), so
  the clip keeps room to its right. The tape does not clamp the move to the timeline's duration. Whether the timeline
  or the editor clamps the move at its end is NOT established.
- The SV-2a receipts show the start 191.3667 at the SV-2a head. The earlier README line "191.3667 to 189.3 and back"
  was wrong. The prior run did not return to 191.3667 by a leftward move.

## Measurements and summary

`summary.tsv` keeps the original columns (`scenario, repetition, n_posts, release_to_post_ms, post_to_200_ms,
200_to_saved_ms, refusals`) and adds `n_drags, failed_drags, release_to_saved_ms, post_to_saved_ms, mode, notes`.

- Per scenario and repetition: medians over the mapped drags.
- Per scenario across repetitions (`all`): the median and the maximum of `release_to_saved_ms`, and the gate line.
  The gate is PASS when the median is at most 2000 ms and the maximum is at most 4000 ms. It is computed on
  `release_to_saved_ms` (the headline number). The cold scenario is reported on its own line.
- One `pack-host` row per repetition, from `pack-host.json`.
- One `S0` row per repetition, with the page-ready time and the verified-head status.

## Not included

- **Save while a generation runs.** Dropped by decision. The `head_busy` refusals came from the pack host's idle claim
  poll, not from a running task. No local no-cost generation exists. Where a scenario could be added: a new entry in
  the `scenarios` array of `browser-sv3-measure.mjs`, with a generation start step before the drag.

## Agent authoring commit

Not established, so the step writes `agent-commit: not established` and does not fail. The files read do not settle
the interpreter (the retained `program/versions/4b62ab1a6521/py/bin/python` or the installed Agent), the working
directory, the door discovery for a copied data root, or the receipt id key. The stub `agent_commit()` carries these as
its TODO. The documented invocation is `python3 -m astrid timelines edit <timeline> --project <project> --clip
parent/clip:<id> --on <seconds> --idempotency-key sv3-<n> --json`, with the clip, project and timeline in `fixture.json`.

## Processes, ports and paths

Kept from SV-2a: TERM and then KILL of PIDs the script started, the owner lock, the health answer through 2400, the
port-closed checks on 2400, 17500 and 17501, the owner-exit check, and an idle-safe `down`.

Dropped: process-group proofs, `group-live`, the trace witness, the trace verdict and the sampler.

Chrome: the driver's PIDs are checked by the profile-path pattern. The cleanup TERMs them, waits 5 s, KILLs any left,
and fails the run if any remain (see the cleanup step above).

## Unverified assumptions (not confirmed by any receipt)

- `setsid --wait` forwards TERM to the preview launcher, which stops its own detached children. Otherwise the port
  fallback is what stops them.
- The Runtime's `down` returns `stopped` and `idle.safe` on the copy.
- The browser helpers (`observeRequests`, `wireCommits`, `publicSnapshot`, `canonicalFreeSpace`, `planFreeSpace`)
  behave on a copied data root.
- Overlapped edits are accepted by the tape, and the editor's rendered projection matches the predicted start.
- The pack host polls during every repetition. The package records this and does not assert it.
- The `jq` filters were compiled and run on sample lines only. The full repetition receipt has not been produced by a run.

## Static checks for this change

`bash -n run-sv3-overlay.sh`; `node --check` on the driver, `arm-free-space.mjs` and `reused-trace-helpers.mjs`; the
Python AST parse of `verify-overlay.py`, `overlay-direct.py` and `overlay-guard/sitecustomize.py`; the JSON parse of
`approved-input.json`; `jq` compilation and sample runs of the combiner and the per-repetition filters; and a
synthetic rebase self-test in the scratchpad. Nothing was run as a package, and no product process was started.

## First run attempt, 23 November 2026

The first run of this package (head `08fb5ba0`, candidate `f2da02e1dcf02439ee149f1412310c72aa4bf0bb`) stopped in repetition 1 before any measurement: `browser-sv3-measure.mjs` imports `reused-trace-helpers.mjs`, which needs `P77_SV2A_TRACE_TOOLS` (the trace-tools worktree) at import time, and this package had dropped that variable and its identity check along with the trace. The fix restores `trace_helpers` in `approved-input.json`, the HEAD and clean-tree checks of the trace-tools worktree, and the variable for the browser process. Nothing else changed.
