# Release 10 field failure: a first-principles review

Read-only review, 8 Nov 2026. Sources: astrid-agent `origin/main` 72462b04, astrid-runtime `origin/main` 21df9bfb, astrid-app `origin/main` 1db36e66 (the App working tree was 150 files behind main, so I read main), and astrid-dev at f36fd1e. Each claim is tagged **[verified]** (read in code), **[inferred]** (follows from verified code but was not run), or **[unverified]**.

---

## 0. What actually happened, in one paragraph

Hannah's Mac was an R0 install. Some time ago it did the copy-only R0→R1 handoff, which landed on a Release 1 candidate. That left a handoff journal in phase `complete`, a selection whose `data_root` still points at R0, and an extra `r1_data_root` field. Since then, every `install`/`--update` enters `boundary_handoff.handle()` first. That function sees `complete`, re-verifies the *old handoff candidate*, prints "Astrid is using …-r1", and returns True. The CLI then prints "R0 to R1 handoff handled" and exits 0. The update code is never reached. The App reads the live Runtime's identity (release 1) and the served manifest (release 10), so it correctly says an update is available. Release 1 cannot update itself, so the App sends her to the command. That command is the path that silently does nothing. The proof never started from this state, because the leg named `release0-to-release1` starts from a fresh Release 9. Separately, an R0-era Runtime is running again against the retained R0 data and failing with `database or disk is full`.

### Verified chain

| Step | Where | Status |
|---|---|---|
| `install`/`update`/`rollback` call `handle()` before journal replay, staging, update-job admission and `Installer.run` | `astrid/installer/cli.py:631-655` | verified |
| A `complete` journal, with no rollback and no policy change, calls `validate_active` → `verify(candidate)` → `say(...)` → `return True` | `boundary_handoff.py:310-314` | verified |
| On True the CLI prints the "handoff handled" summary and returns 0 | `cli.py:643-655` | verified |
| `validate_active` requires `current` to equal the *handoff* candidate's pointer. Even a successful later update would make every later run fail with "R1 handoff selection changed" | `boundary_handoff.py:184-191` | verified (consequence inferred) |
| The Update-now worker (`--update-job`) is admitted at `cli.py:715`, after `handle()`. A click-launched worker on a handed-off machine therefore exits 0 without `record_success`/`record_failure` | `cli.py:715-716`, `update_job.py:2309` | verified (what reconcile then shows: unverified) |
| The Release 10 Runtime's eligibility check requires `daemon.support_root == selected.data_root/"runtime"` and `selected.realm_root == daemon.root`. After handoff, `data_root` and `realm_root` are R0's and the daemon is R1, so Update now would be refused on every handed-off machine even after it reaches Release 10 | `astrid_runtime/update.py:262-266`, `boundary_handoff.py:_records` | verified in code (not run) |
| Nothing outside the handoff modules reads `r1_data_root`. The normal update path takes `data` from `selection.data_root`, which is R0. **Just deleting the early return would run the update against the R0 data root** | `cli.py:556`, `git grep r1_data_root` | verified (consequence inferred) |
| A test enshrines the bug: "A completed rerun selects only R1… `assert handoff.handle(...)`" with `len(runtime_calls) == 1` | `tests/test_boundary_handoff.py:210-212` | verified |
| The App line comes from reason `self-update-unavailable`, its fallback when a Runtime reports no `self_update` (Release 1 predates it). It cannot say *why* | `client.ts:210`, `updateOperation.ts:19-30`, `UpdateResolutionActions.tsx:18,77` | verified |
| The summary never names a release: not before, after or target | `cli.py:_print_run_summary` | verified |

### Proof gap, verified

- `journey_matrix.py`: the two "upgrade" rows are leg `release0-to-release1`, but `execute_release0_to_release1` bootstraps a **fresh Release 9** (`journey_version_jumps.py:688-760`). Plan 29 decision 13 re-aimed them there ("re-aimed to installed Release 9 … no new CI row"). The handed-off state is the one real pre-R1 users are in, and it is now proven by no row.
- `journey_fresh_update.py:146-147` and `:126-127` **require** the start state to have no handoff evidence ("Fresh update baseline has R0 boundary handoff state" is a failure). The proof explicitly excludes the field's population.
- The harness *does* assert `installed_release(version) == target_release` (`journey_version_jumps.py:765`). It has its own handoff-aware data-root resolver (`journey_data_roots.selection`). **The test knows the truth the product doesn't.** The post-condition lives in CI, not in the product, so it never ran on a real machine.

### Diagnostics, verified (`astrid_runtime/diagnostics.py`)

| Label shown | What it actually is |
|---|---|
| `B1 identity: …release=1` | the selection record's `identity`, not the live Runtime |
| `Last update result: No update has run yet.` | `update-transaction.json`'s result. The handoff never writes one, so a machine that has been "updated" by handoff and run `--update` many times says "no update has run" |
| `Installer transaction log:` | the last 80 lines of `~/Library/Logs/Astrid Runtime/install.log`, cut mid-JSON |
| `Retained back-end copies: 8258571708 bytes` | the size of the whole `program_root/versions`, current version included. I found no code that prunes old versions (grep: no prune/retain logic in `core.py`/`backend.py`) **[verified absence by grep]** |
| `Runtime log tail (runtime.log)` | one log file shared by the R0 and R1 Runtimes, so the R0 traceback appears under the R1 Runtime's report |
| `Runtime support state: ready (healthy=True)`, `issues: []` | true for R1 while the R0 Runtime logs `SQLITE_FULL` and R1's `pack-host` has restarted 16 times. **A health signal that says OK while broken is the same class of bug as exit 0 that did nothing.** |

### Two Runtimes and disk-full

| Claim | Status |
|---|---|
| Instance `4dd8d3b7` serves the R0 data root from `versions/1ad318d0…/a` (R0-era layout); R1 serves from `versions/7247ea92…/py/…` | verified (diagnostics) |
| Both share `realm_id d8b536dd…`, `actor_id`, and door port `17340` | verified (diagnostics) |
| The handoff disables and boots out the R0 launchd label (`r0_stop._disable_and_stop`). The R0 plist, R0 version and R0 data are deliberately kept for rollback | verified |
| `owner_lock` is per realm *root*, and the R1 copy has a different root with the same realm id, so nothing stops two owners of one realm | verified (code) |
| *What* restarted R0 (an old launcher, a skill copy, the old command shim, a rollback attempt) | **unverified** |
| Whether the disk is really full or only the R0 database cannot grow | **unverified**. The diagnostics record no free space, which is itself a gap |
| Why `pack-host` restarted 16 times (`last_exit 1`) | **unverified**. Disk-full on the shared volume is plausible |
| On macOS the backup uses an APFS clone and skips the free-space check (`backend.py:880-884`) | verified |

So these belong to the same story. The handoff deliberately leaves a second complete, runnable installation, and nothing ever retires it. Nothing ever prunes versions either. Storage grows, a second owner of the same realm can come back, and health reports the survivor as fine.

---

## 1. Root causes as a system

**Q1. Why could an update report success without updating?**
Exit status and summary are produced *per branch*: each early return calls `_print_run_summary(result_note=...)` with its own prose and returns 0. Nothing at the end of a run checks the user's actual request ("be on release N") against the observed world. Success was defined as "this branch didn't raise", not "the goal state holds". The handoff module answered its own question ("is the handoff consistent?") and the CLI reported that as the answer to `--update`.

**Q2. Why could the App and the installer disagree?**
They read different sources of truth:
- the App reads the *live Runtime identity* (release 1) against the *served manifest* (10);
- the installer reads the *handoff journal*, which pins the handoff candidate as permanently correct (`validate_active`);
- the Release 10 Runtime reads `selection.data_root` (R0);
- the harness reads `journey_data_roots` (R1 if present).

That is four resolvers of "what is installed and where", and only the harness one is right for this state.

**Q3. Why could the proof pass while the field failed?**
The matrix was generated from what CI can construct cheaply: fresh installs and fresh Release 9. It was not generated from the states real installs are in. The leg name (`release0-to-release1`) claimed coverage its body no longer had. The decisive post-condition lived only in the harness. No real long-lived install ran the candidate before the manifest went public.

### Missing invariants

| # | Invariant | Today |
|---|---|---|
| I1 | **Exit 0 from install/update ⇒ the observed live release equals the target** (or the run says, with a non-zero exit, that it did not update and why) | absent in the product; present only in CI |
| I2 | **One resolver of the installation** (program root, active data root, service label, selected version, live identity), used by installer, Runtime, diagnostics and harness | four resolvers; `data_root` means R0 on handed-off machines |
| I3 | **Every install state has a defined update transition** (an exhaustive, total function) | the handoff's `complete` is a sink |
| I4 | **A finished migration is not a permanent authority.** Once the handoff completes, the install is an ordinary direct install | the journal stays authoritative forever (`validate_active` on every run) |
| I5 | **At most one live Runtime per realm per user** | per-root lock only; two run today |
| I6 | **Storage is bounded and space is checked before work** | no version pruning; no space check on macOS |
| I7 | **Health and diagnostics report the user-relevant truth first** (live release, last outcome, other runtimes, disk) | headline fields are the record, not the live state, and mislabelled |

---

## 2. Prevention by construction: the elegant core

Of the candidates named in the brief, here is what each one buys:

- **A post-condition on every run (I1)** turns *every* future bug of this class from silent to loud, whatever its cause. It is the highest leverage and the smallest change. It does not make the update *work*.
- **One source of truth (I2) plus retiring the handoff (I4)** makes *this* state updatable, and removes the trap that a naive fix would hit (updating against R0). It also fixes Update now on these machines.
- **An explicit state model (I3)** is what makes I1 testable for every state and stops a new sink appearing silently.
- **"No early return can skip the work"** follows from I1: any early return that doesn't reach the target must report "not updated" and exit non-zero, so it can no longer pretend. It does not need to be a separate rule.

**The core is three mechanisms:** the receipt (I1), the resolver with normalisation (I2+I4), and the state enumeration that drives tests (I3). The rest (one Runtime per realm, disk) attaches to the resolver and the receipt.

### M1. The run receipt: an observed post-condition, one renderer
- **What:** `settle(request, before, resolver) -> Outcome`, called exactly once at the end of every install/update/repair/recovery run, including every path that returns today. Where a recovery is safe to continue, the update continues in the same run; otherwise it reports `not-updated`.
- **How:** it re-resolves the installation, probes the live Runtime health identity at the *resolved active* data root, and compares it with the request's target (the manifest release for `--update`; "selected = live, healthy" for repair).
- **Outcomes:** `updated(from, to)`, `already-current(r)`, `repaired(r)`, `not-updated(reason, still=r, target=t)`, `failed(reason, still=r)`, `rolled-back(still=r)`.
  - Exit code 0 only for the first three.
  - `not-updated` exits 3; `failed` and `rolled-back` exit 1.
- **One record:** it writes `last-run.json` (typed schema, shared with the Runtime and the App). The terminal summary, the diagnostics headline and the App's "Last result" render this one record.
- **Reasons** are an enum: `self-update-too-old`, `disk-space`, `busy`, `needs-repair`, `other-runtime-running`, `windows-upgrade-unsupported`, `installer-bug`, … Each has one line of copy.
- **Where:** new `astrid/installer/outcome.py` (~100 lines), wired into `cli.py`. The CLI's `try/except` boundary already exists (`cli.py:773-797`), so this is the single exit.
- **Deletes:** the `result_note` free text, the five scattered `_print_run_summary(...)`/`return 0` early exits, and `RECOVERED_PREVIOUS_VERSION`'s return-0 path.
- **Effect on 8 Nov:** her run would have printed "Astrid did not update" and exited 3. The App, reading `last-run.json`, would have said so too.

### M2. One installation resolver, and finishing the handoff
- **Resolver:** `Installation.resolve(home) -> State`.
  - `kind` ∈ {`r0`, `handoff(phase)`, `handoff-rolled-back`, `direct`, `pinokio`, `source`, `fully-local`}.
  - Fields: `program_root`, `active_data_root`, `service_label`, `selected_version`, `live_runtimes[]`, `free_bytes`, `astrid_bytes{versions, backups, retained_r0, workspace}`.
  - Where: new `astrid/installer/installation.py` (~150 lines). The CLI, `update_job`, `support`/diagnostics and the harness (`journey_data_roots` becomes a call into it) all use it.
- **Normalise once:** on the first run that sees a `complete` journal, and at the end of a successful handoff:
  - rewrite marker and selection so `data_root` is the R1 root and `realm_root` is the R1 realm;
  - keep the R0 root as `retained_r0_data_root` (provenance only);
  - rename the journal to `astrid-r1-handoff.completed.json` (an archive, not an authority).

  After that, a handed-off install *is* a direct install. The ordinary update path works, and the Runtime's eligibility check (`update.py:262-266`) passes without any Runtime change, because `data_root` now names the live root.
- **Deletes:**
  - the `complete` branch of `handle()`;
  - `validate_active` as a per-run gate (it runs once, inside normalisation);
  - `apply_completed_policy` and its CLI branch (~85 lines), because choice changes use the normal path;
  - the R1 special case in `journey_data_roots`;
  - the "Astrid is using …-r1; R0 is retained…" lines.
- **Rollback (owner decision):** after normalisation, `--rollback` should be available only until the first successful post-handoff update. After that the retained R0 data is an old backup, not a switch-back target. That is also what lets the R0 copy, the R0 plist and the R0 version be pruned (M4b).
- **Order matters:** M2 must land with M1. Without M2, M1 makes the failure loud. M2 without M1 leaves the next sink silent. Deleting the early return without M2 updates against R0 (§0).

### M3. The state model is the test matrix
- **Enumeration:** `INSTALL_STATES` lives in `installation.py`.
  - States: every `kind`, each handoff phase (`stopping`…`rolled_back`), `pending-transaction(step)`, `direct(release)` for each published release that may still exist, and `handed-off(release)`.
  - Orthogonal conditions: autostart off, command off, another Runtime live, low disk, Windows, Pinokio stale claim.
- **Transition table:** `UPDATE_TRANSITION: dict[kind, Callable]` with a test asserting it covers `INSTALL_STATES` exhaustively. Adding a state without a transition fails CI.
- **Property (§3):** for every state and target, the run ends in `updated(target)`, or in `not-updated`/`failed` with a reason from the enum. It never exits 0 with live ≠ target.

### M4. Same story, attached to M2/M1
- **a. One live Runtime per realm (I5).**
  - The Runtime takes a per-user lock keyed by `realm_id` (next to the installer lock), not by realm root. A second start refuses: "Another Astrid is already running this workspace from <root>."
  - The resolver lists *all* live runtimes it can find (discovery files under the active root and any retained root). The receipt fails `other-runtime-running` if there is more than one.
  - Where: Runtime start path (`runtime_protocol` owner lock; ~30 lines) plus the resolver.
  - Normalisation also removes R0-era launchers once rollback is no longer offered.
- **b. Bounded storage and a space check (I6).**
  - **Retention, at the end of a successful `settle`:** keep the current version and the previous version (the rollback target). Keep the retained R0 data/version/plist only while rollback is offered, and say what was freed in the summary. Where: `installation.py` or `core.py`, ~40 lines.
  - **Preflight:** before staging, require `free ≥ estimated(new version + backup) + margin` on every OS, including macOS clones. Otherwise refuse with `disk-space` and the exact bytes.
- **c. Health tells the truth (I7).** The Runtime maps `sqlite3.OperationalError: database or disk is full` to `support.issues += ["disk-full"]` and health `degraded`. Any service with restarts above a threshold becomes an issue. Where: the Runtime store transaction wrapper and support (~20 lines).

---

## 3. Testing: derive the matrix from real states

1. **Hermetic, on every Agent PR: `tests/test_update_from_every_state.py`.**
   - Parametrise over `INSTALL_STATES × {target newer, target equal}`.
   - Build each state with the existing fake backend from `tests/test_boundary_handoff.py` (`case`, `mark_completed_handoff`).
   - Fake health returns the selected version's identity, so the post-condition is real.
   - Assert the property in M3, and assert the summary's first line matches the outcome.
   - Cost: seconds. This test alone would have caught 8 Nov.
   - Rewrite `test_boundary_handoff.py:210-212`, which currently asserts the bug.
2. **Fixtures from the field.**
   - Diagnostics gain a redacted machine section: selection, marker, journal phase, pointer, versions list, live runtimes, free space.
   - `scripts/fixture_from_diagnostics.py` turns a report into a fixture directory that (1) loads.
   - First fixture: `handed-off-release1-r0-live-disk-full` (Hannah's).
   - Every field failure adds one fixture. That is the regression ledger.
3. **One journey leg from the real start state.**
   - Re-aim the existing macOS/Linux `release0-to-release1` legs, with no new row (that respects Plan 29's constraint): R0 fixture (`tests/fixtures/release0` already exists) → install with a pinned old candidate → handoff `complete` → `install --update` with the candidate.
   - Keep the existing harness assertion `installed_release == target`, plus the receipt's `updated` outcome.
   - Rename legs after their literal start state (`r0-handoff-then-update`, `release9-then-update`), so a name cannot claim coverage the body lacks.
   - Drop the `journey_fresh_update` precondition that *forbids* handoff state, or make that state a parameter.
4. **Field canary before publish.**
   - Before the App merge that serves the manifest, run the candidate on at least one real, long-lived install: the owner's Mac, or a dev's daily machine that is in the most common field state. Use `curl …/install | sh -s -- --update --manifest <candidate manifest>` (`--manifest` already exists).
   - Paste the receipt ("Release 1 → Release 11, exit 0") into the release record. `plans/releases.md` gains a "field receipt" column.
   - The release skill's publish step 1 ("Owner's go") gains: *no go without a field receipt from a real install in each field state the release claims to update.*
5. **Minimum proof for "existing users can update".**
   - A list of the field states known to exist (from diagnostics received, owner knowledge, and the published releases in `plans/releases.md`).
   - For each state, a passing receipt on the exact candidate (hermetic for all, journey for the top two, field for at least one).
   - A state without a receipt goes in the release notes and gets a specific App refusal line. It never gets the generic one.

---

## 4. Communication

**One vocabulary:** release numbers, "your projects", "this computer". Never R0/R1/handoff/B1/C2/realm/back-end copy in user copy. Every message has three parts: **what happened** (with numbers), **is my work safe**, and **the one next action**. Copy is generated from the M1 outcome and reason, so the App, the terminal and the diagnostics cannot disagree.

### 4a. App, Settings › Updates (proposed copy, exact)

| State | Title | Body | Actions |
|---|---|---|---|
| Up to date | **Astrid is up to date** | You have Release 10, the latest. | Check again |
| Update available, one click | **Release 11 is ready** | You have Release 10. Updating takes a few minutes and keeps your projects. Astrid will restart, then this page reloads. | **Update now** · Copy instructions for your agent |
| Needs one command (installed release predates in-app update) | **Release 10 is ready** | You have Release 1. Releases before 10 can't update from this page, so this one update needs a command. After it, future updates are one click here. | **Copy command** · Copy instructions for your agent |
| ↳ under the command | | Open Terminal, paste the command, press Return. It takes a few minutes. When it says "Astrid updated", come back and select Check again. | |
| Needs one command (reason reported by Astrid) | **Release 11 is ready** | This Astrid can't update from this page: {reason line}. Run the command below instead. It keeps your projects. | Copy command · Copy instructions for your agent |
| Last update did nothing (receipt `not-updated`) | **The last update didn't install anything** | Astrid is still Release 1; Release 10 is available. This is a problem in Astrid, not something you did. Your projects are safe. Send the diagnostics file to support so we can fix it. | **Download diagnostics** · Copy command (try again) |
| Update failed, restored | **The update to Release 11 didn't finish** | Astrid went back to Release 10 and your projects are unchanged. Reason: {reason line}. | **Try again** · Download diagnostics |
| Disk full | **Not enough disk space to update** | Astrid needs about {need} free and {free} is free. Old Astrid versions are using {versions}; the next successful update removes the ones it no longer needs. Free up space, then try again. | Try again · Download diagnostics |
| Disk full while running (health `disk-full`) | **Your disk is full** | Astrid can't save changes until there is more free space. Your existing projects are safe. Free up at least 2 GB, then restart Astrid. | Download diagnostics |
| Needs repair | **Astrid needs a quick repair** | Something on this computer is out of step with Release {r}. The repair command fixes it and keeps your projects. | **Copy repair command** · Copy instructions for your agent |
| Two Astrids running | **Two copies of Astrid are running** | An older copy of Astrid started again alongside this one. Run the repair command to stop it; it keeps your projects. | Copy repair command · Download diagnostics |

**Implementation note:** add `self-update-too-old` to the App reason union. Derive it when `self_update !== true` and `installedRelease < FIRST_SELF_UPDATE_RELEASE` (10). Delete the duplicated generic literal in `UpdateResolutionActions.tsx:18`; the client message table is the one copy. "Last result" reads the M1 record (via diagnostics or status), not `update-transaction.json`.

### 4b. Installer terminal summary (proposed copy, exact)

The first line is the outcome. Choices and the "Way back" line move to the log unless the user changed a choice.

**Updated:**
```
Astrid updated: Release 1 → Release 10.
Your projects were kept. Astrid is running — reload astrid.haus to continue.
Freed 6.9 GB of old Astrid versions.
```

**Already current:**
```
Astrid is already up to date (Release 10). Nothing was changed.
```

**Did nothing. This is what the installer must print when an update installs nothing** (exit 3):
```
Astrid did NOT update. It is still Release 1; Release 10 is available.
Why: the updater stopped early after checking an earlier storage move on this computer. This is a bug in Astrid, not something you did.
Your projects are safe — nothing was changed.
Next: send the diagnostics to support: open astrid.haus › Settings › Updates › Download diagnostics.
Details: ~/Library/Logs/Astrid Runtime/install.log
```
Rule: whenever `live release ≠ target` at settle, the first word is "Astrid did NOT update", followed by both numbers, a `Why:` line (from the reason enum; `installer-bug` when no reason was set) and a non-zero exit. No branch can opt out, because the summary is produced only by `settle`.

**Failed and restored** (exit 1):
```
Astrid did NOT update: the new version didn't start.
Astrid went back to Release 10 and is running. Your projects are unchanged.
Next: run the same command again. If it fails twice, send the diagnostics to support.
Details: ~/Library/Logs/Astrid Runtime/install.log
```

**Disk** (exit 3):
```
Astrid did NOT update: not enough disk space.
It needs about 2.1 GB free; 1.3 GB is free. Astrid is still Release 10 and your projects are unchanged.
Next: free up space, then run the same command again.
```

**Another Runtime running** (exit 3):
```
Astrid did NOT update: two copies of Astrid are running for the same workspace.
Next: run the repair command:  curl -fsSL https://astrid.haus/install | sh
```

### 4c. Diagnostics file layout

**Top, for a human. One line, then a short table, computed by the same classifier as the App and terminal:**
```
Astrid diagnostics · 2026-11-08 22:31 · Mac (darwin arm64)
SUMMARY: NOT OK — Release 1 is running and Release 10 is available, but the last update installed nothing. Two Astrid back-ends are running for one workspace, and the older one can't write (disk or database full).

Running release        1   (expected 10)
Available release      10
App release            10
Last update            2026-11-08 21:58 · --update · Release 1 → 1 · NOT UPDATED (installer-bug) · exit 3
Back-ends running      2   ← should be 1
  · Release 1   ~/Library/Application Support/Astrid Runtime-r1   pid 1273   healthy   (selected)
  · Release 0   ~/Library/Application Support/Astrid Runtime      pid ?      DISK FULL (not selected)
Disk                   1.3 GB free of 494 GB
Astrid storage         versions 8.3 GB (11 versions; 2 needed) · old workspace copy 3.1 GB · workspace 2.0 GB
Problems               pack-host restarted 16 times (last exit 1)
```
(Free space, version count and old-workspace size are illustrative; the current report doesn't collect them.)

**Below a `--- Raw detail ---` rule:** the redacted machine records (selection, marker, journal phase, `current`, versions list), the health JSON, `install.log` tail and `runtime.log` tail. Each has a true label, and each Runtime's log tail sits under its own data root. Rename "Installer transaction log" to "Installer log (install.log, last 80 lines)", and "Retained back-end copies" to "Program versions on disk". Drop "B1".

---

## 5. Elegance: the one to three mechanisms, where they live, and what to delete

| # | Mechanism | Lives in | Size | Deletes |
|---|---|---|---|---|
| 1 | **Run receipt**: `settle()` → `Outcome`, `last-run.json` (typed and shared), the only summary renderer, exit codes 0/1/3 | Agent `astrid/installer/outcome.py` (new); `cli.py` single exit. Runtime `diagnostics.py` headline reads it. App `resolveUpdate.ts`/`AstridUpdatesSection.tsx` read it via status | ~100 Agent + ~40 Runtime + ~40 App | `result_note`; five early-return summaries in `cli.py`; return-0 recovery path; choice-recovery lines from the default summary; the generic duplicated App literal |
| 2 | **One resolver + normalising the finished handoff** | Agent `astrid/installer/installation.py` (new); used by `cli.py`, `update_job.py`, `support.py`, `scripts/journey_data_roots.py` | ~150 | `handle()`'s `complete` branch; per-run `validate_active`; `apply_completed_policy` and its CLI branch (~85); harness R1 special case; "R0 retained" output |
| 3 | **State enumeration as test matrix**: `INSTALL_STATES`, exhaustive `UPDATE_TRANSITION`, and the every-state property test, fed by field fixtures | `installation.py` + `tests/test_update_from_every_state.py` + `scripts/fixture_from_diagnostics.py`; re-aimed and renamed journey legs | ~60 + ~150 test | the "baseline must have no handoff state" guard in `journey_fresh_update.py`; the bug-enshrining assertion in `test_boundary_handoff.py:210-212` |

Attached, not separate mechanisms: a realm-id lock in the Runtime (~30 lines), retention at settle plus a space preflight on all OSes (~40), and `disk-full`/restart-storm health issues (~20). Process: a field receipt as a precondition of the owner's go in `skills/astrid-dev-release/SKILL.md` (one bullet), and legs named after their literal start state.

**Net effect:** the Agent installer shrinks. Roughly −85 (completed-policy) −40 (early-return summaries and handoff `complete` handling) against +250 for the two new modules. That replaces four resolvers with one and branch-specific prose with one renderer. Per the house rule, the replacement and the deletion land in the same PR.

### Order of work
1. M1 and M2 in one Agent PR, with the hermetic every-state test and Hannah's fixture.
2. The Runtime health and diagnostics headline, and the App reason and copy.
3. The re-aimed journey leg and the field-canary rule.

Until step 1 ships, the App should not tell handed-off machines to run the command. It cannot detect them today, so the copy fix waits for M1/M2.

### Flags (not derailing)
- `cli.py:main()` is about 450 lines with nested early returns. That is how a sink could hide; the receipt makes it safe, but the function is still far over the 300-line guide.
- `update_job.py` is 2,449 lines.
- **No safe user-side workaround found** for Hannah. `--rollback` then `--update` would hit "The previous R1 copy is retained … preserve it before retrying" (`boundary_handoff.py:320`), and it risks stranding R1 work. Don't advise it. She needs the fixed installer.
