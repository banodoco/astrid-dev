# W233: 15 unit failures on published agent 9814193a (CI run 43757233210)

## Overall verdict: (a) all intended, tests stale. One small UNINTENDED copy side effect noted (group B, `windows-upgrade-unsupported`), not data-affecting.

Nothing a user needs was dropped from the failure copy, and the staging check still rejects every damaged or foreign input before declaring a version. The cleanup of a rejected candidate cannot reach outside `<root>/versions/<candidate>`.

All 15 ids PASS at R12 main 0e1543e0 and at 401dbd78, and FAIL at 9814193a (local reproduction below).

## Which commits changed what (`git log 401dbd78..9814193a`)

One commit is responsible for all 15: **896544e95** "Installer: fresh Windows install without long-path support or late Git failure; honest failure messages" (found by a tester on a clean Windows 10 sandbox, astrid-dev issue 652). Its message says: "Print the real error, name the log, offer Settings only when a Runtime is running, and remove the candidate folder a failed prepare leaves behind."

- (a) Failure copy: `astrid/installer/outcome.py` and `cli.py` in 896544e95.
  - `REASONS["refused"]`: "the installer refused to continue; the message above says why." became "the installer could not continue."
  - `REASONS["error"]`: "the run stopped with an error; the message above says why." became "setup stopped with an error."
  - `CONSOLE_DETAILS`: "Details: shown above in this window (the installer log was not used)." became "Details: see the error in this window."
  - A failed first install now says "Setup did not finish; some downloaded files may remain." instead of "Nothing was installed."
  - `next_steps(..., runtime_running=)`: when no running Runtime was observed and the Next line names "Settings > Updates", it is replaced by "Next: run the same command again; if it fails again, send the error and install log to support."
  - `cli.py` now prints `<ExceptionType>: <message>` for any otherwise-unprinted failure (the real error replaces "the message above").
  - The commit updated the matching assertions in `tests/test_installer_outcome_copy.py` and `tests/test_installer_terminal_summary.py` and added new tests for them. It missed the same strings in `tests/test_update_from_field_states.py` and `tests/test_boundary_handoff.py`, which is why they are stale.
- (b) Candidate cleanup: `Backend.stage()` in `astrid/installer/backend.py`, commit 896544e95.
  - Lines 1339-1349 at 9814193a: `folder.mkdir(parents=True)`, then `try: return self._stage(...)`, then `except BaseException as failure: ... remove_pack_tree(folder)` (line 1346).
  - Code comment: "Only this newly created candidate is ours to remove; selection and the old Runtime have not changed during prepare."
  - Why: a failed prepare used to leave a half-built version folder behind.
  - Other 401..9814 commits that touch installer files (95b8130e8 TLS fallback, 9f0cd240e, 6317d661b, 64b518c5c, 2440ee36a) are not involved in these 15.

## Group results (priority order)

### 1. Installer schema and ACL, 9 ids (8 `test_installer_installed_schema` + `test_installer_acl::test_windows_staged_version_folder_is_a_protected_record_parent`): INTENDED, tests stale. No custody regression.

Why the tests fail: each does `candidate, = (state.root / "versions").iterdir()` (or the ACL test `(folder,) = ...`) after the rejected `stage()`, expecting the leftover half-built folder to inspect. It is now removed, so the unpack fails ("expected 1, got 0"). This matches the CI tracebacks and my local runs.

Does the check still hold: yes. For all 8 scenarios the same `ValueError` is raised, `services.json` and `profile.json` do not exist in the candidate when it is removed, `current` is never created, and no `service_declaration` / `source_checkout_digest` command ran. These are the same assertions the old tests made, now observed at removal time (see the patch).

What the cleanup removes:
- Only `remove_pack_tree(folder)`, where `folder = root / "versions" / new_version_id(manifest)`. `folder.mkdir(parents=True)` (no `exist_ok`) creates it on the line before the `try`. A pre-existing folder raises FileExistsError before the `try`, so it is never cleaned.
- `remove_pack_tree` (`astrid/installer/_pack_cleanup.py:32`) is `shutil.rmtree(path, onerror=retry)`. `rmtree` unlinks symlinks without following them. The retry handler chmods only on Windows and skips symlinks (its comment says "chmod would follow symlinks out of the tree"). On a failure that is not fixable it re-raises; `stage()` catches `OSError`, adds a note ("Partial installation remains at ..."), says so, and re-raises the original rejection.
- Nothing outside `<root>/versions/<candidate>` is named anywhere in the path. The data folder is never passed.

Reproduction at 9814193a in my scratch tree (`/home/user/wt/r13-tests/runs/w233/repro-cleanup-scenarios.py`, run as a test in the scratch worktree). It uses the real `stage()` and the 8 scenarios: source/wheel x missing/symlink/mismatch, wheel fifo (foreign object), foreign guarded directory. Just before the removal I spied on `remove_pack_tree` and planted hostile entries inside the candidate: a symlink to an outside directory, a symlink to a data file, and a hardlink to a data file. Result for every one of the 8:
- exactly 1 removal call, on a direct child of `versions/`;
- after it, the data-folder file (bytes unchanged), the outside directory behind the directory symlink, the symlink target `outside/identical-schema.json` (symlink-source and symlink-wheel), the other version `versions/old`, and `install.json` are all present and unchanged;
- the cache files hardlinked into the candidate are unchanged. The one exception is wheel-mismatch: the test's own damage writes through the hardlink, and the files were already changed before cleanup, verified by a pre-removal check;
- `current` is never created; only the candidate folder is gone.
- The "foreign" scenario is a monkeypatched `os.geteuid` (not a real foreign owner), and "foreign object" is a FIFO created inside the candidate venv. Both are inside the candidate and are deleted with it. A real file owned by someone else in a directory we cannot write fails with `PermissionError`, which is reported ("Partial installation remains") and nothing else is touched. I ran as root here, so that last path is by reading the code, not by test.

Safe: yes. This is a deliberate, safe cleanup of our own just-created folder. The ACL test fails for the same reason (it inspects the removed folder's DACL after the fact).

### 4. Pinokio, 1 id (`test_pinokio_install_saves_explicit_skill_policy`): INTENDED side effect; the test stub is stale. The skill policy is still saved.

- Failure: `assert 1 == 3`. Captured output at 9814193a: `AttributeError: 'types.SimpleNamespace' object has no attribute 'env'`, then "Astrid was NOT installed: setup stopped with an error."
- Cause: commit 896544e95 added `cli._download_manifest()`, which reads `current(root).env.get("ASTRID_GIT_EXECUTABLE")` before the manifest download. The test stubs `cli.current` as `SimpleNamespace(python=python)` with no `env`. A real `Version` always has `env`, so users do not hit this.
- Policy still saved: the "Your choice: Astrid skills are off ..." and "Your choice: skills are copies ..." lines are printed, and with the stub given `env={}` the whole test passes, including `saved["skills"] is False` and `saved["skill_copies"] is True` in the selection file (my scratch run).
- Side note, not part of the 15: four other tests in that file fail in the CI log (they are bucketed preexisting) and again locally after my stub fix; they are outside this card.

### 2 and 3. Failure copy, 5 ids (`test_update_from_field_states` x4, `test_boundary_handoff` x1): INTENDED, tests stale. Nothing a user needs was dropped. One minor unintended wording case.

Test mismatches:
- `test_each_reason_has_its_own_next_step[error|installer-bug|windows-upgrade-unsupported]`: the default `Outcome(..., runtime_running=False)` now gives the fallback Next line rather than the Settings line (these three reasons' Next lines contain "Settings > Updates").
- `test_every_non_zero_outcome_ends_with_next_and_details`: fails only on the console line text, `"Details: shown above in this window (the installer log was not used)."` is now `"Details: see the error in this window."`.
- `test_cli_handled_handoff_refuses_policy_change...`: the card summarised the CI message wrongly. The full output still starts with "Astrid couldn't finish. Your work is kept. The R0 to R1 handoff is copy-only and cannot apply setup choice changes (autostart). Nothing was changed; ..." at ALL three SHAs. Only the reason line changed.

Every non-zero outcome still ends with a `Next:` line and a `Details:` line (checked for every reason, kinds failed/not-updated/rolled-back, plus fresh install and console). "Astrid did NOT update", "Astrid is still Release N" (or, for a fresh install, "Astrid was NOT installed"), and for not-updated "Your projects are safe — nothing was changed." are all kept. What was dropped is only the phrase "the message above says why" from the `refused`/`error` reason lines, which is replaced by actually printing the real error (cli.py) and naming the log. The handoff refusal still plainly says "Nothing was changed" and "Astrid did NOT update".

The unintended side effect: for `windows-upgrade-unsupported`, when no running Runtime was observed, the specific Next ("this Windows version can't be upgraded this way. Open astrid.haus > Settings > Updates > Download diagnostics ...") is replaced by the generic "run the same command again; if it fails again, send the error and install log to support." The reason line still says "upgrading from an earlier Windows version isn't supported yet.", so the user is told what happened, but "run the same command again" cannot help for a permanent unsupported state. The blanket substitution matches on the text "Settings > Updates". Code fix (not a test change): in `next_steps()`, `astrid/installer/outcome.py`, give that reason a Settings-free action instead of the generic fallback, for example in the same `if not runtime_running` branch:
`if reason == "windows-upgrade-unsupported": action = "Next: this Windows version can't be upgraded this way. Send the install log to support."`
(or limit the substitution to `reason in {None, "error", "installer-bug"}`). This is a copy decision for the owner; it does not affect data.

## User-visible copy comparison

R12 main 0e1543e0 and 401dbd78 are byte-identical for every scenario below. Scenario: `Outcome(kind, 1, 1, 2, reason, "update", log)`, with no observed running Runtime unless stated. Lines are separated by " | ".

| Scenario | R12 main = 401dbd78 | 9814193a |
|---|---|---|
| failed / `error` | Astrid did NOT update: the run stopped with an error; the message above says why. \| Astrid is still Release 1. \| Next: open astrid.haus > Settings > Updates > Download diagnostics, and send it to support. \| Details: LOG | Astrid did NOT update: setup stopped with an error. \| Astrid is still Release 1. \| Next: run the same command again; if it fails again, send the error and install log to support. \| Details: LOG (the real `Type: message` is also printed above it) |
| failed / `installer-bug` | ...the installer finished without installing the new release. This is a bug in Astrid, not something you did. \| Astrid is still Release 1. \| Next: open astrid.haus > Settings > Updates > Download diagnostics, and send it to support. \| Details: LOG | same first two lines; Next: run the same command again; if it fails again, send the error and install log to support. \| Details: LOG |
| failed / `windows-upgrade-unsupported` | ...upgrading from an earlier Windows version isn't supported yet. \| Astrid is still Release 1. \| Next: this Windows version can't be upgraded this way. Open astrid.haus > Settings > Updates > Download diagnostics to see what is installed. \| Details: LOG | same first two lines; Next: run the same command again; if it fails again, send the error and install log to support. (flagged above) |
| failed / `refused` | Astrid did NOT update: the installer refused to continue; the message above says why. \| Astrid is still Release 1. \| Next: fix what the message above names, then run the same command again. \| Details: LOG | Astrid did NOT update: the installer could not continue. \| Astrid is still Release 1. \| Next: fix what the message above names, then run the same command again. \| Details: LOG |
| not-updated / `error` | Astrid did NOT update. It is still Release 1; Release 2 is available. \| Why: the run stopped with an error; the message above says why. \| Your projects are safe — nothing was changed. \| Next: (Settings line) \| Details: LOG | same, with Why: setup stopped with an error. and the generic Next above |
| rolled-back / `error` | Astrid did NOT update: the new version didn't start. \| Astrid went back to Release 1. Your projects are unchanged. \| Run the same command again. If it fails twice, do the next step. \| Next: (Settings line) \| Details: LOG | same, with the generic Next |
| fresh install failed / `error` | Astrid was NOT installed: the run stopped with an error; the message above says why. \| Nothing was installed. \| Next: (Settings line) \| Details: LOG | Astrid was NOT installed: setup stopped with an error. \| Setup did not finish; some downloaded files may remain. \| Next: run the same command again; if it fails again, send the error and install log to support. \| Details: LOG |
| console (no log) | ... \| Details: shown above in this window (the installer log was not used). | ... \| Details: see the error in this window. |
| failed / `error` with a running Runtime observed (`runtime_running=True`, new only) | n/a | Next: open astrid.haus > Settings > Updates > Download diagnostics, and send it to support. (Settings advice kept when the App can show it) |
| handoff refusal (`--autostart on`, R0 -> R1) | Astrid couldn't finish. Your work is kept. \| The R0 to R1 handoff is copy-only and cannot apply setup choice changes (autostart). Nothing was changed; rerun without those flags, or change them after the handoff. \| Astrid did NOT update: the installer refused to continue; the message above says why. \| Astrid is still Release 0. \| Next: fix what the message above names, then run the same command again. \| Details: LOG | identical except line 3: "Astrid did NOT update: the installer could not continue." |

## Local reproduction (single pytest process per tree, only the 15 ids)

Venv `/tmp/w233/venv` (9814193a and 401dbd78, via PYTHONPATH; same Runtime pin 6855dfa8, VibeComfy per `scripts/ci_install_vibecomfy.py`) and `/tmp/w233/venv-r12` (R12 main, Runtime pin 42ae24af). Worktrees: `/tmp/w233/wt`, `/tmp/w233/wt-401`, `/tmp/w233/wt-r12`.

| id | R12 0e1543e0 | 401dbd78 | 9814193a | 9814193a + patch |
|---|---|---|---|---|
| schema [missing-source] | pass | pass | FAIL | pass |
| schema [missing-wheel] | pass | pass | FAIL | pass |
| schema [symlink-source] | pass | pass | FAIL | pass |
| schema [symlink-wheel] | pass | pass | FAIL | pass |
| schema [mismatch-source] | pass | pass | FAIL | pass |
| schema [mismatch-wheel] | pass | pass | FAIL | pass |
| foreign_object | pass | pass | FAIL | pass |
| foreign_guarded_directory | pass | pass | FAIL | pass |
| field_states next_step[error] | pass | pass | FAIL | pass |
| field_states next_step[installer-bug] | pass | pass | FAIL | pass |
| field_states next_step[windows-upgrade-unsupported] | pass | pass | FAIL | pass |
| field_states every_non_zero_outcome | pass | pass | FAIL | pass |
| boundary_handoff refuses_policy_change | pass | pass | FAIL | pass |
| pinokio saves_explicit_skill_policy | pass | pass | FAIL | pass |
| acl staged_version_folder_is_a_protected_record_parent | pass | pass | FAIL | pass |

Totals: 15 passed at R12, 15 passed at 401dbd78, 15 failed at 9814193a, 15 passed at 9814193a with the patch. I also ran the whole `test_each_reason_has_its_own_next_step` parametrization (19 params) with the patch: 19 passed.

Process note: while building the copy capture I accidentally ran a whole-file import of `test_boundary_handoff` (81 tests) once at R12 and once at 401dbd78 in my scratch worktrees, then killed a third run at 9814193a. These were in scratch trees only; nothing shared was touched.

## Appendix: tests-update patch (NOT applied, awaiting ruling)

`/home/user/wt/r13-tests/runs/w233/tests-update.patch` (diff against 9814193a, made and proven in `/tmp/w233/wt`, never applied to a shared checkout). It touches only tests:
- Installer schema and ACL tests: a spy on `remove_pack_tree` reads the candidate at removal time (no services.json / profile.json, source schema bytes, DACL protected, manifest private) and asserts `versions/` is then empty and `current` absent. The check keeps its strength and also now proves the cleanup.
- `test_each_reason_has_its_own_next_step`: loops `runtime_running` True and False; the old expectations hold when a Runtime is running, and the generic Next is expected otherwise. The console details line is updated. Note this encodes the `windows-upgrade-unsupported` fallback; if the owner takes the code fix above, change that one expectation instead.
- Handoff test: the reason line `... the installer could not continue.`
- Pinokio test: the `current` stub gets `env={}`.

## Other files
- Evidence, scratch: `/tmp/w233/copyB.{r12,401,9814}.txt` (copy table source), `/tmp/w233/copyC.{r12,401,9814}.txt` (handoff output).
- Reproduction script: `/home/user/wt/r13-tests/runs/w233/repro-cleanup-scenarios.py`.
