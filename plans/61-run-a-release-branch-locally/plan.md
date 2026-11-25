# Run a release branch locally

**Project:** Run a release branch locally

**Goal:** A developer runs the whole Astrid stack at one release or plan branch on a copy of their own work, isolated from their live install, and stops it with one command.

**Status:** paused

**Owner:** Hannah

**Estimate:** About a day of engineering, plus one real run.

**Waiting on:** Release 15 for the remaining real-stack run and follow-up work; the single-branch tool shipped with Release 14.

**Start:** [Astrid contributor skill](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision role:** Foundational enabler — lets contributors and the owner try a release or plan branch of the whole stack on a copy of their real work before it ships, without claiming a new creator-facing capability.

## Status as of 17 November 2026, late evening

**Where the work is.** The owner decided on 17 November that the tool goes on its own plan branch, which is merged into the release branch, and that this plan is in Release 14 and on `main` ([D1 and D2](inputs.md#owner-decisions)). Both are done. [handover.md](handover.md) is the entry point for the next manager.

**Works.** The `release/14/plan-59` stack runs isolated on a copy of the owner's realm:
- the stack: Agent `cce5d69a`, Runtime `519b4047`, ports 2400, 17500 and 17501, in `~/astrid-release/release-14-plan-59`;
- the live install beside it, untouched: Agent `9814193a`, Runtime `6855dfa8`, door 17340. Both builds are labelled "Release 13".

A browser check passed at `http://127.0.0.1:2400/tools/video-editor?entry=editor`. It showed the "Almost Ready" timeline, 5 timelines, clips and a preview frame. The preview banner bug that the check found is fixed, and the fix is Plan 59's (`158186d8`, on `release/14/plan-59`). The stack was built with the earlier tool commit `1412e9ffc`, before the realm step used `workspace attach`.

**Where the code is.**
- astrid-app `release/14/plan-61`, pushed, head `cf383fc0e2668fe25c4a24f77c1a0b438a3a9fca`. It was cut on 17 November from `release/14/main` at `0b6ef16152dc3fa11246ccc2007da630c66d1a1a`. Two commits were cherry-picked with `-x`: `aceeb7d00` (from `1412e9ffc`, the tool) and `cf383fc0e` (from `36c3c6f6a`: `workspace attach`, a clone of `data/` before any destructive step, a clearer `update` refusal and the realm fixture). The diff against `release/14/main` lists only the tool's paths: `scripts/astrid-release/`, `scripts/installer/pin.mjs`, `scripts/installer/manifest.test.mjs` and one `.gitignore` line. **It is not merged into `release/14/main`**: RB-7 does that, after the RB-6 proofs and the review.
- astrid-app `release/14/plan-59`: one commit, `4eb6fb350ddced8547dabca69ee825514b4367e2`, returns those same paths to their `release/14/main` state, so Plan 59 does not land the tool a second time. The banner fix stays. Nothing was reverted or rewritten.
- The tool calls its own copy of `pin.mjs`, found relative to the script (`$SCRIPT_DIR/../installer/pin.mjs`), and reads only the target branch's `public/install-manifest.json` and `runtime.lock.json` with `git show`. So it works from a checkout of `release/14/plan-61` against any branch, including `release/14/plan-59`, which no longer has `--in` and `--out`.
- astrid-dev `release/14/plan-61`, cut at `abafc66e539cb64f679c9083f134e5a288bfd205` from `release/14/main`. [astrid-dev #834](https://github.com/banodoco/astrid-dev/pull/834) brought the contributor section onto it, in the release skill at its path on that branch, with a ledger entry.
- Closed: [astrid-app #283](https://github.com/banodoco/astrid-app/pull/283) (the tool against `main`), its branch `tool/astrid-release` deleted, and [astrid-dev #832](https://github.com/banodoco/astrid-dev/pull/832) (replaced by #834).

**Proven on `release/14/plan-61` on 17 November, from a scratch clone, Node 20.19.4:**
- `bash -n` passes on `astrid-release` and `realm-snapshot.sh`.
- `scripts/astrid-release/test-realm-snapshot.sh` reports `passed=35 failed=0`.
- `node --test scripts/installer/manifest.test.mjs` reports 6 pass, 0 fail.

**Not proven yet:** `workspace attach` on the real stack, the `data/` clone backup, an edit surviving a restart, `update` after a branch move, a fresh-clone run (it needs about 5 GiB free), the cause of the first-start failure, and a hosted CI run of `release/14/plan-61`.

**Next:**
1. The owner approves one stop window for those proofs (RB-6, RB-9), announced first, with each stop under 2 minutes. Until then the running stack is left alone.
2. The owner files, or declines, the three drafted issues ([tasks](tasks.md#issues-to-file)).
3. The owner decides D3, and D4 when it matters.
4. After RB-6 and the review (R), RB-7 merges `release/14/plan-61` into `release/14/main` in astrid-app and astrid-dev. The tool reaches `main` when Release 14 publishes.

**Who decides.** The owner decides D3 and D4, the stop window, the issues and every merge into a product `main` ([decisions](inputs.md#owner-decisions)). D1 and D2 are decided. The plan manager, once named, runs the tasks and lands the plan in `release/14/main` through its plan branch. The Release 14 Lead keeps the release's brief and board.

## What the first run found

- **The preview banners.** Two bare, unstyled `<div role=status>` banners sat in the preview as in-flow flex items and took about 53% of its width. They are now an absolutely positioned overlay strip (`158186d8`, App `PreviewPanel`).
- **The canvas note.** It says the timeline has no saved output size and the theme declares a 1920×1080 canvas. It is informational, and it shows on `release/14/plan-59` only, since `f3619a18a`.
- **Why `?entry=editor`.** The welcome and connect dialog comes from welcome state stored in the browser, and its Continue only switches to a local connection screen. The URL opens the editor directly. The editor talks only to the stack's own proxy, 17500, which forwards to the stack's door, 17501. It never talks to the live 17340.
- **The first-start failure.** The first start of a fresh copy fails once with "accepted commit inputs changed during verification", and a guarded retry (at most 2) starts it.
  - A tracer on a later start saw one Runtime, 185 "tracer armed" lines, no version change and no raise.
  - A review could not reproduce it in 10 starts in scratch.
  - It happens only on the first start of a fresh copy. The cause is unknown (RB-9).
- **Where the tool landed.** The owner first asked for the tool on `main`, and [astrid-app #283](https://github.com/banodoco/astrid-app/pull/283) went against `main`. On 17 November she decided it goes on its own branch, `release/14/plan-61`, which is merged into the release branch and reaches `main` at publication (D2). #283 is closed.

## Lessons

- Do not test tool changes on the stack the owner is using: two restarts happened without notice.
- Give notice before any stop, and keep each stop under 2 minutes.
- Fixtures first; the real stack last.
- With about 3 GiB free and swap near full, run one heavy job at a time.
- Agents run long steps in the foreground and report only what finished.
- Something other than the agent that built a check verifies it. Several "running" claims were wrong.

## Outcome and scope

**The one idea.** A stack is an install made from one manifest: the exact commit of each component, written by the App's `scripts/installer/pin.mjs` and put on disk by the installer (`public/install --manifest`). This plan adds no second format and no new concept. It makes the tool that already exists, `scripts/astrid-release/astrid-release` in astrid-app, run once, safely and truthfully, for one branch. Moving a built stack to new commits while keeping its data is not in this plan: the installer cannot do it yet beside a live Astrid ([#825](https://github.com/banodoco/astrid-dev/issues/825), and the retained-profile guard in [tasks](tasks.md#issues-to-file)). Everything beyond one branch is [Plan 62](../62-one-manifest-one-stack/plan.md): one stack, switching by branch or manifest, going back, local and live work, RunPod pins and the contributor text.

When this plan is done, on macOS:

1. `astrid-release release/14/plan-59` builds the stack in `~/astrid-release/release-14-plan-59`, copies the realm, starts, and ends READY. READY means the Runtime reports `rendering.render` available, the editor page answers, and Runtime health through the editor is `ok`. It prints the editor URL and the stop command.
2. **Which commits run.** The App and Agent heads are the branch's. Either of the two falls back loudly when it lacks the branch: `release/NN/plan-PP` → `release/NN/main` → `main`, one `FELL BACK` line each. The Runtime, VibeComfy and runpod-lifecycle come from the Agent's own pins (`runtime.lock.json`, `pins.json`). **timeline-composition is not switched at all**: it is the tarball the App and the Agent vendor ([#820](https://github.com/banodoco/astrid-dev/issues/820)).
3. **The realm copy.** The stack opens on a snapshot copy of the developer's realm, taken once, on the first run (RB-3). The plan's realm step attaches it with the Runtime's own `workspace attach`, leaving one hand edit, the installer record's two realm fields ([#817](https://github.com/banodoco/astrid-dev/issues/817)). That step is committed on `release/14/plan-61` (`cf383fc0e`, from `36c3c6f6a`) but not yet run on the real stack. The run that passed used the earlier hand edit of the catalog. An existing long-lived timeline, such as an "Almost Ready" edit, opens, plays and can be edited. Edits stay in the copy. Nothing copies back. **The first start on a fresh copy fails once** with "accepted commit inputs changed during verification", and a guarded retry (at most 2) starts it. The cause is not explained (RB-9).
4. **`update`.** With nothing moved, it runs no installer and no restart. When the derived manifest is unchanged, for example because only App code moved, it checks out the new App commit and restarts with no installer run. **When the Agent or Runtime commits change, it refuses before touching anything** and prints the rebuild steps (RB-8):
   1. `astrid-release stop <branch>`.
   2. Keep the data: `cp -c -R <root>/data ~/astrid-release/<slug>.data-<YYYYMMDD-HHMM>`, an APFS clone that costs almost no disk.
   3. Delete the root and run again. The realm is copied again from live.

   The edits on the old copy carry over only by attaching the kept clone's realm in place of a new snapshot, and only when its workspace schema equals the new Runtime's. The kept-data update waits for [#825](https://github.com/banodoco/astrid-dev/issues/825) and the retained-profile guard. Removing only `<root>/program` and reinstalling does not work: the installer refuses whenever a managed source profile is retained in the data (`backend.py:1028-1044`, called at `cli.py:962`). `update` also refuses, before stopping anything, when the stack's editor clone has tracked changes.
5. **`status`** shows what each repository resolves to and whether the stack runs. When the heads moved since the build, it says so and names `update`.
6. **`stop`** ends only processes under the stack's root. Going back to normal means `stop`: the live install was never changed.
7. **The live install is untouched**, proven by hashes and database facts, not sizes and times (see [Completion](#completion)). That covers its Runtime, data root, ports (`:2222`, `:17340`, `:17336`, `:17391`) and login service. **The `astrid` on your PATH stays the live install**, because the stack is installed with `--command off`. Commands for the stack run through `HOME=<root>/home <root>/program/run-astrid`, and that includes GPU jobs, which use the stack's own RunPod setup and claims.

**Following the branch is explicit.** Nothing watches the remote: a push reaches the stack at the next `update`. An automatic follow is refused, because it restarts under someone who is editing a timeline.

**What "latest" means per layer:**

| Layer | Runs from | A change shows up |
| --- | --- | --- |
| Editor (App) | the stack's own clone, `<root>/editor`, served by Vite | Edits in that clone show at once, by hot reload. Pushes to the branch show at `update`. |
| Agent, Runtime, VibeComfy, runpod-lifecycle | the installed program, `<root>/program/versions/<id>/` (not editable) | A push that moves these pins makes `update` refuse and print the rebuild steps (RB-8); the kept-data update waits for #825. The Runtime and VibeComfy move only when the Agent's pins name a new commit. Local edits never show. |
| timeline-composition | the tarballs vendored in the App and the Agent | Only when it is re-vendored and committed there. |
| Realm | the copy taken at the first run | Never re-synced. For a fresh copy: the rebuild steps. |

**Out of scope here; moved to Plan 62:**
- one stack instead of one per branch;
- `use <branch | manifest>` and `back`, and moving a stack to new commits with its data;
- the App commit inside the manifest;
- local `repo` pins and live checkouts;
- `status` per component with RunPod pins;
- RunPod's pin check;
- the contributor section that replaces the older routes. A first section for this tool is written, in the release skill on astrid-dev `release/14/plan-61` ([#834](https://github.com/banodoco/astrid-dev/pull/834)).

**Refused:**
- Windows and Linux, refused by name: the realm copy relies on APFS clones, and Linux developers' RunPod need is Plan 62's Agent issue.
- `--managed-by pinokio` ([#815](https://github.com/banodoco/astrid-dev/issues/815)).
- The tool deleting `<root>/program` or `<root>/data` once a realm copy exists. A rebuild replaces both, and it is the developer's, by the printed steps, after the data is cloned.
- Calling `astrid-runtime restart` or `down`, or the installer's `--update` or `--uninstall`, on the stack. The #825 probe guards them (`runtime_lifecycle.py:87`, `:102`, `core.py:692`; read from the code, not run). The tool keeps its own start and stop.
- Copying the realm back.
- A second realm path.

## Existing work and decision

**Reused as is:**
- the installer, with `--manifest`, for a fresh install. Its hidden `--update` is the intended in-place path, and the code says a failed update rolls itself back (Agent `astrid/installer/core.py:577-606`). It is not usable yet on a stack beside a live install ([#825](https://github.com/banodoco/astrid-dev/issues/825)). Its reinstall over a kept workspace (`core.py:768-771`, `backend.py:738-746`) is refused whenever a managed source profile is retained (`backend.py:1028-1044`, called at `cli.py:962`), so that route is unreachable today;
- `pin.mjs` as the one manifest writer;
- the App's `dev-local-workspace.mjs` as the launcher;
- the Runtime's `workspace attach` for the realm, and its capability list for readiness;
- the tool's own isolation: a fake HOME, an explicit data root, its own ports, autostart, command and skills off.

**Going back** is not a command here. A stack runs one branch's heads; Plan 62's `back` comes after #825.

**The realm is a snapshot copy, one path, attached by the Runtime.** The tool takes a read-only SQLite backup of the live database and APFS clones of the rest. It removes the installer's empty-realm selection and the stale owner records, `instance.lock` and `discovery.json`. Then it runs the Runtime's `workspace attach`, which checks the realm id and writes the catalog and source profile itself (`astrid_runtime/workspace.py:140-215`). One hand edit remains, the installer record's `realm_id` and `realm_root`, because no supported writer exists ([#817](https://github.com/banodoco/astrid-dev/issues/817)). Adopt is not used: it refuses a destination that already has a workspace. The Runtime's own backup of a 2 GB realm would not fit beside the stack on the development Mac we measured. The clones plus the database copy cost about 14 MB.

The evidence and the reviews are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

Critical path: RB-3 → RB-6 → R → RB-7 ([tasks](tasks.md)). RB-2, RB-4, RB-5, RB-8 and RB-9 run beside it. Nothing spends money.

Where the work stands is in [Status](#status-as-of-17-november-2026-late-evening), at the top, and in the [handover](handover.md).

## Interfaces and handoff

**Consumes:**
- the App and Agent branch heads (`git ls-remote`);
- the Agent's `runtime.lock.json` and `pins.json` at that head, through `pin.mjs`;
- the App's `public/install` at the App head;
- the live realm database, opened read-only;
- the live media, cloned copy-on-write;
- the Runtime's `workspace attach` and `workspace inspect` from the stack's own program.

The tool passes no `ASTRID_*` variable into the stack, `ASTRID_ENV_FILE` included, so the stack gets no live keys. The live `~/.astrid/astrid.env` is never copied. RB-6 still hashes it before and after.

**Produces:**
- an isolated install at `~/astrid-release/<slug>`; its `program/versions/<id>/manifest.json` is the pin set for every component except the App;
- `state/heads.tsv`, the refs and the App and Agent commits it built from. Plan 62's V3 folds the App commit into the manifest and removes this file.

### How to run it

You need:
- a Mac with git, `sqlite3`, `python3`, and Node on PATH that meets the App's `engines`;
- a live Astrid install, for the copy of your work;
- about 10 GB free disk in practice: the program 3.6 GB, the isolated home 3.6 GB (its uv cache), the editor clone 0.7 GB, plus twice your realm database.

Until Release 14 publishes, the tool is on astrid-app `release/14/plan-61`: run it from a checkout of that branch, naming the branch to try as the argument. Use the editor URL with `?entry=editor`.

```sh
git clone https://github.com/banodoco/astrid-app.git && cd astrid-app && git checkout release/14/plan-61   # the tool's branch, until Release 14 publishes
scripts/astrid-release/astrid-release stop   release/14/plan-59   # clears a half-built run's processes, if any
scripts/astrid-release/astrid-release        release/14/plan-59   # build, copy the realm, start; ends READY with the editor URL
scripts/astrid-release/astrid-release status release/14/plan-59
scripts/astrid-release/astrid-release update release/14/plan-59   # when the branch moved; refuses with the rebuild steps if the Agent or Runtime moved
scripts/astrid-release/astrid-release stop   release/14/plan-59   # back to normal; files stay
```

**If a rebuild fails after the root was deleted:** the live install is untouched and the dated data clone still holds the edits. `stop` clears the half-built root's processes, and a second run starts from a fresh copy of live. To keep the edits, attach the kept clone's realm, same schema only.

To reclaim the disk, first release any RunPod machine the stack claimed (`<root>/program/run-astrid machines status` shows none). Its claim journal lives in `<root>/data/runpod/`, and deleting that orphans a paid pod. Then delete `~/astrid-release/<slug>`, and any dated data clone you no longer need.

**Record edits, made on 17 November.** The planning pull request that brought this plan to `main` added Plan 61's line to the Release 14 brief and the Branches rows for astrid-app and astrid-dev `release/14/plan-61` (role `plan 61`, State `open`, with their cut SHAs). The plan manager sets each row to `merged` when RB-7 lands it.

The issues found while building the tool are listed in [tasks](tasks.md#issues-to-file).

## Completion

One real run (RB-6), on a Mac with a live install, evidence pasted into the [run record](tasks.md#run-record):

- [ ] `stop` clears any half-built run, including a Runtime the installer started on an empty realm.
- [ ] A fresh first run ends READY and prints the launch line. `workspace attach` reports `configured_attach`, and `workspace inspect` names the copied realm.
- [ ] An existing long-lived timeline from the live realm opens on the copy and plays.
- [ ] **An edit survives a restart.** Read `SELECT count(*) FROM timeline_commit_history` on the copy while stopped (read-only), make one edit in the stack editor, then `stop` and start again. The edit is there, and the count is one higher, both before and after the restart.
- [ ] `update` with nothing moved prints `unchanged` and runs no installer and no restart.
- [ ] `update` after a moved Agent or Runtime commit refuses before touching anything and prints the rebuild steps. If the branch did not move during the run, record it as not exercised, by name.
- [ ] A tracked change in the editor clone makes `update` refuse, with the stack still running.
- [ ] The first-start failure is either explained (RB-9) or recorded with its count of retries and each failed log tail.
- [ ] `stop` leaves no process of the stack running.
- [ ] **Throughout, the live install is untouched.** Take `shasum -a 256` before and after a full run of:
  - every file under the live realm's `cas/`;
  - the live `~/.astrid/astrid.env`;
  - `~/.local/share/astrid-install.json`;
  - the live login service plist;
  - the live `versions/<current>/manifest.json`.

  Also compare the live Runtime's pid and start time, and its launchd job state. The live Runtime writes its database all the time, so compare facts there, not bytes. Read with `mode=ro`: the head publication ids, the `timeline_commit_history` count and `runtime_epoch`.
- [ ] After RB-7, the same first run works from a fresh clone of astrid-app at `release/14/plan-61`, after cloning the old `data/` aside and deleting the root. It needs about 5 GiB free first.

Negative cases:
- A mistyped branch stops before anything is touched.
- A non-Mac machine is refused by name.
- A live realm database that cannot be opened read-only is refused.
- `workspace attach` with a wrong realm id is refused ("workspace identity mismatch").
- If the branch's Runtime refuses the copied realm's schema, the run stops and reports it. Nothing is hand-migrated.

The plan lands in `release/14/main` through its plan branches in astrid-app and astrid-dev. It reaches `main` only when Release 14 is published.
