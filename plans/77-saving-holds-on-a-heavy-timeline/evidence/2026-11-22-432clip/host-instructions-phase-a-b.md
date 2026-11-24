# Addendum 2 — after the seed stopped at 432 clips (Plan 77 host's decision, 22 November 2026, 18:04Z)

The Plan 77 host has decided: no resume, no reseed; 616 is off the table until the history read is fixed. Two phases follow, in this order. Return raw files and sha256 sums; do not interpret results.

## Phase A — read-only measurements on the live 432-clip project

The Runtime is warm and idle. In this phase: NO commit, NO restart, NO writes to the project, nothing killed, no change to the installed product. Put all outputs under `run/receipts/phaseA/`.

(a) A standalone authenticated SDK read of exactly the failing call, `list_timeline_commits`, as `fetch_bundle` makes it (limit 50, no cursor), with a client timeout of 900 s so it is not cut at 300 s. Timestamp start and end. Run it TWICE back to back (the second shows whether a warm memo helps). Record bytes returned and page count for each. Use the installed Python and SDK from a small script of your own in `run/`; if the 300 s limit is a constant inside the installed SDK, pass a longer timeout through the SDK's or client's own parameters or build the request with the same client class; do not edit installed files. If you cannot make the call without editing the product, stop and say so.

(b) During the FIRST read, py-spy against the Runtime PID. Install py-spy into a scratch virtual environment outside the stack (never into the product install). Take `py-spy dump --pid <pid>` at 10, 30, 60, 120 and 240 s after the read starts, and one `py-spy record -r 100 -d 300 -f raw --nonblocking -o <file> --pid <pid>` started with the read. Keep the raw file byte-for-byte and record its sha256. Rank the decodable records into self and inclusive time with the two rankers from astrid-app pull request 370, head 5b2c76a6a636d835700bc5f12b48848861dc30f5, `scripts/save-loop/diagnostics/rank-runtime-profile.py` (strict) and `rank-decoded-runtime-profile.py` (recovery; tolerates py-spy's invalid UTF-8). Get them with `git -C /root/codex/p77box/app fetch origin 5b2c76a6a636d835700bc5f12b48848861dc30f5` and `git show <sha>:<path> > run/tools/<name>`; do NOT change the worktree at `wt/`. Report the top 25 by inclusive and by self time, and the fraction of samples under `list_timeline_commits`, `_history_page`, `_verify_accepted_replay` and `jsonschema`.

(c) Runtime process CPU seconds from `/proc/<pid>/stat` before and after each read; the resource probe values (free -m, du of stack and temp, process count) at start and end.

(d) Record the commit count, the head, the clip, track and shot counts and the canonical document's size in bytes.

If the first read has not returned after 900 s, record that, keep the profile, skip the second read and go on to (c) and (d) with whatever read-only means still answer; if nothing answers, say so and continue to Phase B.

When Phase A is complete, write `run/receipts/phaseA/SUMMARY.md` listing every file with its sha256, then go straight on to Phase B without waiting.

## Phase B — safe stop and the authenticated backup, labelled 432

1. Clean safe stop of the Runtime and editor through the installed safe shutdown. Confirm no `-wal` or `-shm` files remain beside the realm database and that the three ports are closed.
2. At least 25 GiB free before the backup.
3. `doctor --root <realm> --admission-timeout 600` must pass first.
4. Record the realm UUID and the sha256 of `realm.sqlite3` before the backup.
5. Backup with the installed Python: `RealmStore(root, admission_timeout=600.0)` and `create_backup(store, <destination>, key_path=<support>/'backup-auth.key')`, exactly as the specification and addendum 1 say. Key custody as before: the support directory stays outside the stack; pass the key's PATH only; never open, print, copy or hash the key.
6. Verify the backup manifest's realm id. Then a verified restore into a unique inactive path, with matching realm id and database sha256.
7. Label everything 432, not 616: the backup directory name, the receipts and `run/receipts/READY.md`. READY.md states plainly that the project holds 432 clips because the single seed stopped on a 300 s read timeout, gives the tuple, the head, the counts, every path and every hash.

End with RUN-STATUS: DONE when READY.md is written, or RUN-STATUS: WAITING with one precise question if something stops you.
