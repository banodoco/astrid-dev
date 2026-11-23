# Plan 73 — disposable compatibility and rollback receipt

**Status:** bounded **PASS on Linux**, not D5, MS-9 completion, automatic product rollback or independent-client acceptance.

## Immutable execution

- Source: `9d04210cf4dd68e80fe8005b4e28f340c15b8380`, isolated [draft #1627](https://github.com/banodoco/astrid-dev/pull/1627), stacked over unchanged #1390.
- [Exact-head documentation job](https://github.com/banodoco/astrid-dev/actions/runs/45224001045/job/137865495306) succeeded: 575 unit tests, generated build/check, 64 post-build view tests, MS-10 scripted rehearsal, MS-11 negative matrix, MS-7/MS-9 HOLD report, repository checks and regenerated views all passed.
- Machine-readable proof: GitHub Actions artifact **`plan73-ms9-compat-rollback` ID `14841713879`** on [run 45224001045](https://github.com/banodoco/astrid-dev/actions/runs/45224001045). It contains `ms9-compat-rollback.json` and `ms9-compat-rollback.md`. Independently inspected: **17/17 assertions passing**, **12 command receipts** (11 ordinary success exits and one deliberate nonzero refusal), `error=null`, exact source SHA above.
- Reproduction: `python3 scripts/ms9_compat_rollback.py --source-ref 9d04210cf4dd68e80fe8005b4e28f340c15b8380 --output-dir <outside-checkout>` on Linux with Git, Bash, GNU sed and symlink support. The runner fetches its source commit locally into a detached temporary Git checkout; never point it at a real client's installed skill root.

## Observed transitions and rollback limitation

| Stage | Measured outcome |
| --- | --- |
| Initial `bash sync.sh` install in temporary root | **15** legacy symlink entries; **14** readable original `SKILL.md` files |
| Generated `skills build/check` and `install --dry-run` | Success; no old link changed in dry-run |
| Generated `skills install` | **14** generated skill symlinks; no leftover old `astrid-dev` or `shared` link |
| Repeated generated install | Exactly the same 14 link targets; foreign entry unchanged |
| Old `sync.sh --dry-run` on the generated layout | **Expected nonzero** with `foreign symlink` conflicts; no mutation. **This is NOT a rollback procedure.** |
| Inject a foreign collision before restoration | Guarded restoration refused the entire preflight without changing any installed links |
| Remove fixture-only collision; restore snapshot | All **15** original links and their targets, all original instruction hashes and the unrelated foreign file returned unchanged |
| Legacy installer after restoration | Dry-run zero exit; original authored skill sources and original checkout tracked status unchanged |

The restoration helper validates exact recorded generated targets, authored source paths and all destination collisions before mutation. It then changes several symlinks; **the operation is not atomic**, is unsafe to assume under hostile concurrent writes, interruption or power loss, and must not be used as an unattended production rollback. A D5 owner ruling must specify freeze/custody, snapshot capture and a supported rollback/client-reload procedure.

## Consumer classification correction

The first inventory at this source listed 78 active-reference matches across 19 files because the new test runner itself was treated as an active consumer. Its old-command strings are evidence fixtures, not live dependencies. The subsequent commit classifies `scripts/ms9_compat_rollback.py` (and other scripted MS-10/11 runners) under protected test/fixture review, **without dropping their references from the inventory**. Check the newest exact-head artifact for revised counts.

## Continuing gates

No real Claude/Codex session or picker, Windows/macOS client, fresh independent agent, D5 cutover, MS-9 old-source deletion, integration or release publication was performed. Original RS1 remains **BLOCK** with only the six bounded remediations adjudicated; final R, the separate max-two-round Astra High sense check and owner project-to-main GO remain outstanding. No tests weakened or canonical task rows changed.
