# Tasks — Run a release branch locally

[Plan](plan.md) · [Inputs](inputs.md)

**Routes** follow the [run contract](../../skills/shared/run-contract.md#routing-and-bindings). `N` covers everything below very hard, ordinary hard work included (Haiku or Luna). `X` is very hard (Sonnet or Terra). `S` is the review (Opus or Astra). **Task ids:** `RB-1` … `RB-9` and `R`, listed in run order. **Critical path:** RB-3 → RB-6 → R → RB-7. RB-2, RB-4, RB-5, RB-8 and RB-9 change different parts of the tool and run beside it. **Test inventory:** astrid-app `scripts/installer/manifest.test.mjs` (pin.mjs) is the one existing test file affected. The RB-3 fixture is new and lives beside the tool. No Agent or Runtime tests change.

**How the X task runs:** the X worker writes its N split first, launches the independent N helpers at once, and checks what they return against the code. It keeps the decisions and the final edit, and reports how many N helpers it launched. Every task adds commits only, and brings in a newer base by merging it ([run contract](../../skills/shared/run-contract.md#scope-source-identity-and-state)). Task work goes on a task branch `p61/<task id>`, cut from the plan branch `release/14/plan-61` in astrid-app or astrid-dev, and lands there by pull request. The plan branch is merged into `release/14/main` only by RB-7. Tool commits touch only the tool's paths.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| RB-1 One script, committed. Done in `1412e9ffc` (on `release/14/plan-61` as `aceeb7d00`): the index and the working tree no longer disagree, and it calls `pin.mjs`, not `manifest.mjs`. | N | — | `scripts/astrid-release/` | At `1412e9ffc`: `bash -n` passes on `astrid-release` and `realm-snapshot.sh`; `grep manifest.mjs` finds nothing | [x] |
| RB-2 The door port comes from the install. Once a program exists, read the door from the installed version's `version.json`; never re-pick it. Otherwise the "does the install match" check sees a new port and stages a second full program for nothing. The code is in `1412e9ffc`; this task is its proof. Done in `0bce7312` (R14-P61-01). | N | — | the tool: port selection, the install-match check | A second start and an `update` with nothing moved both log "already matches" and run no installer | [x] |
| RB-3 The realm: a snapshot copy, one path, attached by the Runtime. First run only, with the stack stopped. **(1)** Keep `catalog.json` as `catalog.json.pre-realm-snapshot`, then remove `catalog.json`, `instance.lock` and `discovery.json`: the installer's empty-realm selection and the stale owner records. Remove them only when no process of the stack is alive and the lock's pid is dead. **(2)** Snapshot into `data/runtime/realms/<id>`. Take a read-only SQLite `backup()` of the live `realm.sqlite3`. Make `cp -c -R` APFS clones of the realm's other entries, skipping `owner.lock`, `staging/`, `-wal` and `-shm`. Never copy the live data root's `runpod/`: it holds claim journals, `https-token` and managed sources, and a copied `claim.json` makes two owners of one pod. **(3)** Run `workspace attach --data-root <data> --realm-root <data>/runtime/realms/<id> --realm-id <id> --source-manifest <program>/versions/<current>/profile.json --json` with the stack's own Python, and require `configured_attach`. The Runtime writes the catalog and the source profile (`astrid_runtime/workspace.py:140-215`). **(4)** The one hand edit left: set `realm_id` and `realm_root` in the installer record and drop `foreground` ([#817](https://github.com/banodoco/astrid-dev/issues/817)). **(5)** Run `PRAGMA integrity_check` and `workspace inspect`, start, and self-check: the projects list and every timeline. If the branch's Runtime refuses the copy's schema, stop and report; never hand-migrate. Status: committed in `36c3c6f6a`, with the fixture `scripts/astrid-release/test-realm-snapshot.sh`. The fixture passed in `0bce7312` (R14-P61-01), including the wrong-id refusal. The hosted Release 13 copy attached and its existing timeline played in [the installed run](#installed-certification-on-19-november-2026). | X | — | the tool: the realm step, `realm-snapshot.sh`; README "The realm" | The fixture below passes, including the wrong-id refusal; in RB-6 a fresh first run attaches the copy, and an existing timeline loads | [x] |
| RB-4 The README tells the truth. It gives the disk need, about 10 GB in practice (program 3.6 GB, isolated home 3.6 GB, editor 0.7 GB, plus twice the realm database), and the tool's disk floor agrees with it. It says the realm copy is point-in-time and one-way. It says that the `astrid` on PATH stays the live install (`--command off`; use `HOME=<root>/home <root>/program/run-astrid`), and that GPU jobs use the stack's own RunPod setup and claims, so any machine must be released before the root is deleted. It says the way back is `stop`, that the fallback applies to the App and Agent only, and that timeline-composition is not switched. It says that `update` refuses across changed pins and prints the rebuild steps, and that `astrid-runtime restart` and `down` and the installer's `--update` are not for the stack. It says that the first start can need a guarded retry. It drops any "consistency check" promise: `pin.mjs --check` is the check. Done in `0bce7312` (R14-P61-01). | N | — | `scripts/astrid-release/README.md`; the disk floor in the tool | Each claim names the script line that does it; a reader finds none without one | [x] |
| RB-5 `pin.mjs` never overwrites its input. The change adds two flags, `--in <manifest>` and `--out <file>`; `--check` already existed. `--in` without `--out` refuses. The code and the tests are in `1412e9ffc`; this task is their run. | N | — | `scripts/installer/pin.mjs`; `manifest.test.mjs` | The `--in`/`--out` case passes; `--in X` alone exits non-zero and leaves `X` byte-identical; run with the App's pinned Node 20 | [x] |
| RB-8 `update` across changed pins refuses, and the tool never deletes the data. When the derived manifest differs, refuse before stopping anything. Print the three rebuild steps: `stop`; `cp -c -R <root>/data ~/astrid-release/<slug>.data-<YYYYMMDD-HHMM>`; delete the root and run again. Say that edits carry over only by attaching the kept clone's realm in RB-3 step (3), and only when its `SELECT version FROM runtime_schema WHERE id=1` (read-only) equals `SCHEMA_VERSION` in the new Runtime's `runtime_protocol/store.py`. Never remove `<root>/program` alone once `data/runtime/source-profiles/astrid.json` exists, because the retained-profile guard then blocks every reinstall. A first-run installer retry, before any realm copy, removes `program/` and `data/` together. Once `state/realm-id` exists, the tool deletes neither. `36c3c6f6a` adds the `data/` clone before destructive steps and the clearer refusal. Not the installer's `--update` ([#825](https://github.com/banodoco/astrid-dev/issues/825)). Not "remove `program/` and reinstall": refused by the retained-profile guard (`backend.py:1028-1044`, called at `cli.py:962`), and it runs no migration. Done in `0bce7312` (R14-P61-01). | N | — | the tool: the install step, the retry loop, the refusal text | With a moved Agent pin: `update` exits non-zero, prints the three steps, and leaves the root's file list and the stack's processes unchanged; a forced first-run network retry removes `program/` and `data/` together | [x] |
| RB-9 Name the first-start failure. The first start on a fresh copy fails once with "accepted commit inputs changed during verification", and the second start succeeds. It is not the data: 10 of 10 starts in scratch, through a different launch path, reached READY. A tracer on a later start of the stack saw one Runtime, 185 "tracer armed" lines, no version change and no raise, because the failure happens only on the first start of a fresh copy. So trace the first start of a fresh copy, in the stop window, through the real launch path (`astrid-runtime up` → the installer's `start_foreground` → `run`, with its `verify` loop beside it). The log tells the case apart: two starters at once, the Runtime's own connection writing during a read, another connection committing, the file touched from outside, or the inode replaced. Until a cause is fixed, keep the retry as a guarded net: that exact message only, at most 2 retries, a WARNING with the count, and each failed log tail kept. Delete the retry when the cause is fixed. If the cause is in the Runtime, delete it when the fix is pinned. | N | — | read-only on the Runtime; a tracer in the stack's program, removed afterwards; the tool's retry | The trace names the refusing call and the case; either the retry is deleted with the cause fixed, or the cause is written up for an issue and the retry stays guarded | [ ] The bounded retry shipped on the plan branch in [#311](https://github.com/banodoco/astrid-app/pull/311). Three fresh hosted copies started with zero retries. The packet records this accepted outcome. The historical root cause remains unknown. |
| RB-6 One real run, on a Mac with a live install: every item in [Completion](plan.md#completion), in order. It is a fresh first run. It needs about 10 GB free, and about 5 GiB free before the fresh-clone part. Check the live install before and after by the hashes and database facts in Completion. | N | RB-2 to RB-5, RB-8 | read-only on product code; evidence in the run record below | Each Completion item has its command and output in the run record; durations are recorded as information | [x] Hosted packet scope complete on the #318 editor landing. See the [run record](#installed-certification-on-19-november-2026) for the permitted stable-pin omission and the post-RB-7 replay. |
| R One review round of the tool, before it lands in the release branch (D3). The review covers the tool at the commit RB-6 ran, plus RB-9's outcome. Findings become rows `R.<n>` below this one. | S | RB-6, RB-9 | read-only | No blocker left open; each finding has a row or a recorded reason | [x] Independent R graded the tool A with zero blocking findings. The Lead signed off after ordinary integrated Tests passed on `aa5c228b`. [Integrated Tests](https://github.com/banodoco/astrid-app/actions/runs/44616793002) |
| RB-7 Land the plan in the release branch. **Already done on 17 November (D1, D2):** astrid-app `release/14/plan-61` is cut from `release/14/main` with the tool cherry-picked (`aceeb7d00`, `cf383fc0e`); Plan 59's branch gives the tool's paths back in `4eb6fb350`; astrid-dev `release/14/plan-61` is cut with the contributor section on it ([#834](https://github.com/banodoco/astrid-dev/pull/834)); both Branches rows are in the brief; #283 and #832 are closed. **Left:** after RB-6 and R, merge the current `release/14/main` into each plan branch (never rebase), rerun `manifest.test.mjs`, the RB-3 fixture and one `update` with nothing moved, check each conflict fix by its delta, and get hosted CI green on the exact head (a plan branch passes the `landing reference` check by its name). Then the plan manager merges `release/14/plan-61` into `release/14/main` in astrid-app and in astrid-dev, and sets both rows to `merged`. The tool reaches `main` with Release 14. | N | RB-6, R, D3 | astrid-app: the tool's paths; astrid-dev: the release skill and the ledger entry | `git log origin/release/14/main..origin/release/14/plan-61 --stat` lists only the tool's paths (astrid-app) and the skill and ledger files (astrid-dev); the reruns pass; CI is green; a fresh clone at that branch runs the start | [ ] |

## RB-3 detail

**Starting N split (3):**
1. Read the Runtime's `workspace attach` and `workspace inspect` (`astrid_runtime/workspace.py:140-215`) at the Agent head's pinned Runtime. Report exactly which files attach writes, and which the tool must remove first.
2. Build the fixture. It is a small data root shaped like a live one, made with the stack's own Python under `env -i` and a scratch HOME: `workspace create`, then `cp -c -R` of the realm, then `workspace attach` on a second data root, then `workspace inspect`. Give the realm a database in WAL mode with an uncheckpointed write, one media file, `owner.lock`, `staging/`, and a sibling `runpod/` with a `claim.json`. The check script asserts:
   - `PRAGMA integrity_check` is `ok`;
   - the uncheckpointed write is present;
   - the media is byte-identical;
   - the skipped files and `runpod/` are absent;
   - `workspace inspect` names the realm id;
   - attach with a wrong `--realm-id` fails with "workspace identity mismatch";
   - the source tree's hashes are unchanged.
3. After the X edit, run the fixture and report.

The X worker writes the step and its messages from split 1, and judges the fixture result.

## Run record

Filled in by RB-6: date, the commits that ran, each Completion item's command and output, and the live-install checks before and after.

### Installed certification on 19 November 2026

The original hosted macOS harness completed on the accepted editor merge. Its native command record, browser traces, screenshots and before/after snapshots are retained in the [installed artifact](https://github.com/banodoco/astrid-app/actions/runs/44610924453/artifacts/14572779092). [Hosted Mac job](https://github.com/banodoco/astrid-app/actions/runs/44610924453/job/135866997143) · [Workflow run](https://github.com/banodoco/astrid-app/actions/runs/44610924453)

The runner used macOS 26.7.2 (25G332), arm64, Node 20.19.4 and Python 3.11.9. Commands below use `$HARNESS` for the checked-out #310 repository, `$TOOL` for the #311 tool checkout, `$PROOF` for the evidence directory, `$STACK` for the disposable plan stack and `$FRESH_CHECKOUT` for the clean plan clone. Recorded exits are the original command exits. Browser and database outputs below are field projections.

| Component | Actual immutable source |
| --- | --- |
| Harness #310 | `3c99c7aa7f9a0079b5075351f6271239714c4bc4` |
| Release tool #311 | `d72ee39ded70346e5b22d952fba985c8a137b622` |
| Installed editor, release/14/plan-61 | `4b47c75243443b1844f6712f31303dea509b5935` |
| Installed Agent, release/14/main | `ae929cdae7460c36cfbfd95599019a4c45f42e1c` |
| Installed Runtime | `2537fed24385ec1c24f48a812e09af4bb63fb794` |
| Live Release 13 Agent | `9814193a73f606719e81883a8be197d27dd361d4` |
| Live Release 13 Runtime | `6855dfa8df65cf8ae4c002b57134d6505493c17c` |

Every archived `heads.tsv` agrees on the editor and Agent. The installed manifests identify the Runtime. On six starts the tool reported that the editor’s runtime.lock.json names 6855dfa8df65 while the Agent locks install 2537fed24385. The installed results apply to the tuple above. The actual project was `4da6b9443996465faeafd4a367d82005`, realm `7c3bf16a-ccec-482c-954f-7bde8e0113a1`, and timeline `61616161-6161-4161-8161-616161616161`.

#### 1. Stop the half-built install

```text
$ bash $TOOL/scripts/astrid-release/astrid-release stop release/14/plan-61
Owned stack process census after stop: []
exit 0
```

#### 2. Start on the copied realm

```text
$ bash $TOOL/scripts/astrid-release/astrid-release release/14/plan-61
[release] READY: release release/14/plan-61
workspace attach: configured_attach
exit 0
```

#### 3. Play the existing long-lived timeline

```text
$ node $HARNESS/scripts/astrid-release/hosted-browser.mjs $STACK $PROOF play
PASS  mode=play  frameBefore=0  framePlaying=23
head before=txn-34e57f19c39941ce965ed42562d16a1f
head after=txn-34e57f19c39941ce965ed42562d16a1f
exit 0
```

#### 4. Edit once and verify it survives restart

```text
$ bash $TOOL/scripts/astrid-release/astrid-release stop release/14/plan-61
[]
exit 0
```

```text
$ bash $TOOL/scripts/astrid-release/astrid-release release/14/plan-61
[release] READY: release release/14/plan-61
exit 0
```

```text
$ node $HARNESS/scripts/astrid-release/hosted-browser.mjs $STACK $PROOF edit
PASS  mode=edit  frameBefore=0  framePlaying=24
head before=txn-34e57f19c39941ce965ed42562d16a1f
head after=txn-ee9afe6738cd4cd587413f2ba9a9bd24
exit 0
```

```text
$ bash $TOOL/scripts/astrid-release/astrid-release stop release/14/plan-61
[]
exit 0
```

```text
$ bash $TOOL/scripts/astrid-release/astrid-release release/14/plan-61
[release] READY: release release/14/plan-61
exit 0
```

```text
$ node $HARNESS/scripts/astrid-release/hosted-browser.mjs $STACK $PROOF verify-edit
PASS  mode=verify-edit  frameBefore=0  framePlaying=24
head before=txn-ee9afe6738cd4cd587413f2ba9a9bd24
head after=txn-ee9afe6738cd4cd587413f2ba9a9bd24
exit 0
```

The copied database’s read-only `SELECT count(*) FROM timeline_commit_history` returned **7 before editing, 8 after editing and 8 after restart**. Schema version was 33 at all three observations. The new publication and document revision persisted.

- Before — `txn-34e57f19c39941ce965ed42562d16a1f`, `authoring-parent-revision-c9298e19acdd3c2108ad9c250653e48c81a03c117c21831338fd7727a2095e3a`
- After edit — `txn-ee9afe6738cd4cd587413f2ba9a9bd24`, `authoring-parent-revision-0181d9cfe07db56d171862cb963f895eaa90ccb2edfcba249eb720154191497e`
- After restart — `txn-ee9afe6738cd4cd587413f2ba9a9bd24`, `authoring-parent-revision-0181d9cfe07db56d171862cb963f895eaa90ccb2edfcba249eb720154191497e`

#### 5. Update while both pins are unchanged

```text
$ bash $TOOL/scripts/astrid-release/astrid-release update release/14/plan-61
[release] app: unchanged (4b47c7524344 on release/14/plan-61)
[release] agent: unchanged (ae929cdae746 on release/14/main)
exit 0
```

The before/after process comparison reports `unchanged=true`, empty identity differences and empty capture errors on both sides. The raw before/after process listings are retained. The comparison covers the long-lived service identities, with transient subprocess observations recorded separately.

#### 6. Update after an Agent or Runtime pin moves

Not exercised in the real run: resolved branch heads did not move. Both Agent/Runtime refusal injections remain executed in release.test.mjs on this hosted Mac. The plan permits this named outcome while branch heads stay fixed.

#### 7. Refuse an update over tracked editor changes

```text
$ bash $TOOL/scripts/astrid-release/astrid-release update release/14/plan-61
[release] STOP: Editor source in $STACK/editor has changes; not overwriting.
exit 1
```

The workflow checked the stack after the expected refusal.

#### 8. Repeat fresh first starts

```text
$ bash $TOOL/scripts/astrid-release/astrid-release release/14/plan-61
[release] READY: release release/14/plan-61
workspace attach: configured_attach
exit 0
```

```text
$ node $HARNESS/scripts/astrid-release/hosted-browser.mjs $STACK $PROOF play
PASS  mode=play  frameBefore=0  framePlaying=25
head before=txn-34e57f19c39941ce965ed42562d16a1f
head after=txn-34e57f19c39941ce965ed42562d16a1f
exit 0
```

```text
$ bash $TOOL/scripts/astrid-release/astrid-release stop release/14/plan-61
exit 0
```

```text
$ bash $FRESH_CHECKOUT/scripts/astrid-release/astrid-release release/14/plan-61
[release] READY: release release/14/plan-61
workspace attach: configured_attach
exit 0
```

```text
$ node $HARNESS/scripts/astrid-release/hosted-browser.mjs $STACK $PROOF play
PASS  mode=play  frameBefore=0  framePlaying=24
head before=txn-34e57f19c39941ce965ed42562d16a1f
head after=txn-34e57f19c39941ce965ed42562d16a1f
exit 0
```

```text
$ bash $TOOL/scripts/astrid-release/astrid-release stop release/14/plan-61
exit 0
```

Fresh copies 1 and 2 used the tool at `d72ee39d`. Copy 3 used the ordinary tool in a new plan clone at `4b47c752`. All three started with zero failed attempts and zero retries. Four original RB-9 startup tests passed, including the exact retry guard, stale-log refusal and two-retry ceiling. The historical failure did not recur in this run. All ten archived chat-model timeout observations recorded zero kills on this run.

#### 9. Stop before negative attachment

```text
$ bash $TOOL/scripts/astrid-release/astrid-release stop release/14/plan-61
Owned stack process census after stop: []
exit 0
```

#### 10. Preserve the live Release 13 install

The complete before and after snapshots compare equal. All nine file hashes match at both endpoints and the intermediate snapshots. The following lists the original `shasum -a 256` results once, as both outputs were identical. The fixture directory names are shortened as above.

```text
$ shasum -a 256 "$HOME/Library/Application Support/Astrid Runtime/runtime/realms/7c3bf16a-ccec-482c-954f-7bde8e0113a1/cas/sha256/45/1fd5616d1078c3499cb18899fa8338c761e85fb04c16e4ea0e7ff7d7a3fe5e" "$HOME/Library/Application Support/Astrid Runtime/runtime/realms/7c3bf16a-ccec-482c-954f-7bde8e0113a1/cas/sha256/8e/9e423b6cbd62a3970f375d15dfef438410e11009ea4f4b989d2a1c7e3011d6" $HOME/.astrid/astrid.env $HOME/.local/share/astrid-install.json $HOME/.local/share/astrid/install.json $HOME/Library/LaunchAgents/haus.astrid.runtime.plist $HOME/.local/share/astrid/versions/9814193a-6855dfa8-50d47d22/manifest.json $HOME/.local/share/astrid/versions/9814193a-6855dfa8-50d47d22/version.json $HOME/.local/share/astrid/current
799b3c0da8855e6bca893154f4e346180a225e7bd2e130c3f2b087755811f0c9  $HOME/.astrid/astrid.env
f4cd62bc351b402a0634f273ca75ef00a665a2621325a13f52a097553cd6cb68  $HOME/.local/share/astrid-install.json
f73706b6f8dffadda6ea9d1e69130777e4e69753498eee92b3bbed7769cfcd9c  $HOME/.local/share/astrid/current
5c358b8385f12add5c9f777339e0d639917c68978238f96390bb8a3872586768  $HOME/.local/share/astrid/install.json
7ef7ef9f8bc20c753b9ac713da8719803f0163a7069f5ad11f7b5998d5677110  $HOME/.local/share/astrid/versions/9814193a-6855dfa8-50d47d22/manifest.json
e9949e2a1ce9fbe8c11a88837fe45039c90d04540aaac58b31cb114be8a45889  $HOME/.local/share/astrid/versions/9814193a-6855dfa8-50d47d22/version.json
451fd5616d1078c3499cb18899fa8338c761e85fb04c16e4ea0e7ff7d7a3fe5e  $HOME/Library/Application Support/Astrid Runtime/runtime/realms/7c3bf16a-ccec-482c-954f-7bde8e0113a1/cas/sha256/45/1fd5616d1078c3499cb18899fa8338c761e85fb04c16e4ea0e7ff7d7a3fe5e
8e9e423b6cbd62a3970f375d15dfef438410e11009ea4f4b989d2a1c7e3011d6  $HOME/Library/Application Support/Astrid Runtime/runtime/realms/7c3bf16a-ccec-482c-954f-7bde8e0113a1/cas/sha256/8e/9e423b6cbd62a3970f375d15dfef438410e11009ea4f4b989d2a1c7e3011d6
fa6a9878fc663219cc7e3c6d6d08f912cce8416889385e13ac8f34e36ae36a45  $HOME/Library/LaunchAgents/haus.astrid.runtime.plist
exit 0
```

```text
$ shasum -a 256 "$HOME/Library/Application Support/Astrid Runtime/runtime/realms/7c3bf16a-ccec-482c-954f-7bde8e0113a1/cas/sha256/45/1fd5616d1078c3499cb18899fa8338c761e85fb04c16e4ea0e7ff7d7a3fe5e" "$HOME/Library/Application Support/Astrid Runtime/runtime/realms/7c3bf16a-ccec-482c-954f-7bde8e0113a1/cas/sha256/8e/9e423b6cbd62a3970f375d15dfef438410e11009ea4f4b989d2a1c7e3011d6" $HOME/.astrid/astrid.env $HOME/.local/share/astrid-install.json $HOME/.local/share/astrid/install.json $HOME/Library/LaunchAgents/haus.astrid.runtime.plist $HOME/.local/share/astrid/versions/9814193a-6855dfa8-50d47d22/manifest.json $HOME/.local/share/astrid/versions/9814193a-6855dfa8-50d47d22/version.json $HOME/.local/share/astrid/current
All nine digests match the preceding list.
exit 0
```

The live runtime PID and start time were `12157 Thu Nov 19 20:50:41 2026` before and after. Launchd reported `state = running; runs = 1; pid = 12157; last exit code = (never exited)`. Live `timeline_commit_history` remained 7, schema 33, and runtime epoch 1. The live head remained `txn-34e57f19c39941ce965ed42562d16a1f`, revision `authoring-parent-revision-c9298e19acdd3c2108ad9c250653e48c81a03c117c21831338fd7727a2095e3a`. No listed file was absent.

#### 11. First run from a fresh plan clone

```text
$ git clone --depth 1 --single-branch --branch release/14/plan-61 https://github.com/banodoco/astrid-app.git $FRESH_CHECKOUT
exit 0
```

```text
$ git -C $FRESH_CHECKOUT rev-parse HEAD
4b47c75243443b1844f6712f31303dea509b5935
exit 0
```

The third fresh start above used this clone and played the copied timeline. Completion 11’s explicit post-RB-7 repetition remains with RB-7.

#### Refusal cases

```text
$ bash $TOOL/scripts/astrid-release/astrid-release release/14/p61-mistyped-fd50fd13cb704c8da41830a0a58be6a1
[release] STOP: Neither the App nor the Agent has a branch named release/14/p61-mistyped-fd50fd13cb704c8da41830a0a58be6a1 (typo?). Nothing was done.
exit 1
```

```text
$ bash $TOOL/scripts/astrid-release/astrid-release release/14/plan-61
[release] STOP: macOS only.
exit 1
```

The non-Mac probe substitutes only `uname` at the actual entry point on this hosted Mac.

```text
$ python3 scripts/astrid-release/hosted-negative.py
PASS: mode=ro refusal before attach; source database bytes unchanged.
Inner refusal exit 1; native negative proof step succeeded.
```

```text
$ $STACK/program/versions/3ee4bff802be/py/bin/python -I -m astrid_runtime workspace attach --data-root $PROOF/wrong-id-data --realm-root $STACK/data/runtime/realms/7c3bf16a-ccec-482c-954f-7bde8e0113a1 --realm-id 99999999-9999-4999-8999-999999999999 --source-manifest $STACK/program/versions/3ee4bff802be/profile.json --json
"error": "workspace identity mismatch: expected 99999999-9999-4999-8999-999999999999, observed 7c3bf16a-ccec-482c-954f-7bde8e0113a1",
exit 1
```

```text
$ $STACK/program/versions/3ee4bff802be/py/bin/python -X utf8 -I $TOOL/scripts/astrid-release/workspace-attach.py workspace attach --data-root $PROOF-schema-negative/selection --realm-root $PROOF-schema-negative/7c3bf16a-ccec-482c-954f-7bde8e0113a1 --realm-id 7c3bf16a-ccec-482c-954f-7bde8e0113a1 --source-manifest $STACK/program/versions/3ee4bff802be/profile.json --json
Runtime doctor exit 1; the negative clone was refused.
exit 1
```

The schema-negative database SHA-256 remained `96caf6dd54934f76a84a9e41e95441630974e95f648c96d94f61c9d0c8ebcd2a`; no catalog was published.

The minimum observed free space was 85.44 GiB. The run reported no disk-related omissions. All five retained browser reports show advancing frames and zero page errors. They also record HTTP 503 on the local update-status endpoint. The packet keeps the original failed certification and its two timeout kills, and the separate diagnostic run and its three timeout kills, as their own evidence.

### Independent review R on 19 November 2026

The independent reviewer graded the tool A in one round, with no blocking finding. Executable tool and harness blobs in the two reviewed PRs match their integrated versions. The reviewer independently ran the four original startup controls and both moved-pin controls on `aa5c228b` with Node 20.19.4. All six passed. The initial local fixture selected a Python shim and stopped before exercising the tool. It passed with the system interpreter, as did the original hosted fixture. The installed proof covers the isolated live-control hashes, read-only copy, stored edit, process identity, unchanged update and refusal cases. The local update-status endpoint returned HTTP 503 during playback. Its availability is outside this release-tool acceptance. Ordinary integrated Tests passed on `aa5c228b`. All 1,436 App files and the SDK file matched the earlier exact native receipt by file and count, with 20,886 App and 335 SDK passes. Integrated Vitest emitted file-level results. Node, installer, boundary and Darwin test names and outcomes matched their references. R is signed off. RB-7 retains the two release-branch syncs and post-landing fresh clone. [Integrated Tests](https://github.com/banodoco/astrid-app/actions/runs/44616793002) · [Installed Mac job](https://github.com/banodoco/astrid-app/actions/runs/44610924453/job/135866997143)

### RB-7 integration, 19 November 2026

App sync #317 at `e44b5836` contains the current release main and plan head `aa5c228b`. The 43 release-sync paths and 26 new plan paths were disjoint relative to `67428177`. Against release main, 17 editor source/test paths are the union of the accepted #314 and #318 repairs to the C4 installed edit. Fifteen resulting blobs match the accepted PRs. The other two preserve the exact #314 line changes over the release-main versions of `useTimelinePersistence.ts` and `useTimelineSave.ts`. These repairs were authorized by the hosted packet and its Lead decisions. The remaining changes are the tool, installer helpers, ignore file and proof workflows. The dev plan head already contains its release main and adds only the ledger entry and release-skill instructions. [C4 acceptance](https://github.com/banodoco/astrid-dev/issues/796#issuecomment-7013916661) · [Installed confirmation](https://github.com/banodoco/astrid-dev/issues/966#issuecomment-7022318629) · [Dev draft](https://github.com/banodoco/astrid-dev/pull/1010)

The preceding sync stopped at a 422 after Keep, with eleven unexecuted serial journey cases. On the refreshed head all 59 journey IDs matched the certified destination, including attempt counts and expected outcomes. The conflict case passed, and all eleven serial cases ran. The manifest, realm and unchanged-update fixtures passed. The exact native comparison recorded 20,886 destination and 21,145 candidate App passes, and 335 SDK passes on each side. Ordinary [source Tests](https://github.com/banodoco/astrid-app/actions/runs/44620977921) passed. The independent comparison traced four missing positional IDs and fifteen rebound titles to retained source cases, a timestamp in a parameterized title, and the deliberate #292 track-label behavior. The source and approved release main have identical blobs for the four affected files. The sync landed on plan-61 at `71258577` with reviewed tree `f4da2694`. [App #320](https://github.com/banodoco/astrid-app/pull/320) and [dev #1010](https://github.com/banodoco/astrid-dev/pull/1010) are the paired release-branch drafts. [Plan-head Tests](https://github.com/banodoco/astrid-app/actions/runs/44630601739) and the [real unchanged update](https://github.com/banodoco/astrid-app/actions/runs/44630605193) are booked. The fresh-clone C11 check follows both landings. [New journey](https://github.com/banodoco/astrid-app/actions/runs/44620992954) · [App/SDK native comparison](https://github.com/banodoco/astrid-app/actions/runs/44621203141) · [Manifest, realm and unchanged-update fixtures](https://github.com/banodoco/astrid-app/actions/runs/44620993199)

### Earlier evidence

On 18 November 2026, [App #302](https://github.com/banodoco/astrid-app/pull/302) (R14-P61-01) merged into astrid-app `release/14/plan-61` at `0bce7312`. The Lead graded round two A after rebuilt probes verified all eight round-one items. The release cases passed 31/31, the pinned Runtime cases passed 10/10, and the native macOS realm suite reported `passed=36 failed=0` (run `44307575039`, job `134813021197`). [Lead DONE](https://github.com/banodoco/astrid-dev/issues/796#issuecomment-6980328306)

Checked on 17 November 2026, late evening, from a scratch clone of astrid-app `release/14/plan-61` at `cf383fc0e` with Node 20.19.4, while the plan moved to its own branch. This is not RB-6, and it touched neither the running stack nor the live install:
- `bash -n scripts/astrid-release/astrid-release` and `bash -n scripts/astrid-release/realm-snapshot.sh`: both pass.
- `scripts/astrid-release/test-realm-snapshot.sh`: `passed=35 failed=0`. It ends with a shell "Terminated" line, which is the fixture stopping its own background writer process.
- `node --test scripts/installer/manifest.test.mjs`: 6 tests, 6 pass, 0 fail, including "--in without --out refuses instead of overwriting its input". That is RB-5's proof.
- `git diff --stat origin/release/14/main..origin/release/14/plan-61` lists seven files, all the tool's: `.gitignore`, the four files under `scripts/astrid-release/`, `manifest.test.mjs` and `pin.mjs`.
- On `release/14/plan-59`, after commit `4eb6fb350`, `git diff origin/release/14/main -- scripts .gitignore` is empty.

Recorded before RB-6, 17 November 2026: a stack from astrid-app `release/14/plan-59` at `1412e9ffc` (Agent `cce5d69a`, Runtime `519b4047`, ports 2400, 17500 and 17501) ran on a copy of a real realm, beside the live install (Agent `9814193a`, Runtime `6855dfa8`, door 17340). A browser check passed at `http://127.0.0.1:2400/tools/video-editor?entry=editor`, with the "Almost Ready" timeline, 5 timelines, clips and a preview frame. The first start failed once with "accepted commit inputs changed during verification", and the guarded retry started it. The realm step of that run was the hand catalog edit, not `workspace attach`. A later tracer run on a non-first start saw one Runtime, 185 "tracer armed" lines, no version change and no raise. The preview banner fix is `158186d8`.

## Issues to file

Found while building the tool. Eight were filed on 17 November 2026, six as issues and two as comments on [#739](https://github.com/banodoco/astrid-dev/issues/739). [#825](https://github.com/banodoco/astrid-dev/issues/825), the stop probe, followed after the failed `update`. They are follow-ups, not part of this plan's finish, except where a task names one.

**Still to file, the owner's call (drafts; not filed):**
- **Runtime: one timeline that cannot be verified at startup stops the whole Runtime, with no stack trace.** `runtime_protocol/service.py:3055-3066` lets `ProtocolError` escape, and `astrid_runtime/cli.py:471` prints only its text. Wanted: the traceback in `runtime.log`; that one timeline read-only, with a reason; the rest of the Runtime starts. A test is included. RB-9's trace may add to it.
- **Installer: a retained managed source profile blocks reinstall over a kept workspace.** Every installer run except doctor calls `source_checkout_ownership` first (`cli.py:962`). With no `program/current`, it loads the retained `data/runtime/source-profiles/astrid.json` and requires its paths to be Git checkout roots (`backend.py:1028-1044`, `runtime_protocol/source_identity.py:53-59`). A managed profile never passes, so the installer's own reinstall-over-kept-workspace branch (`core.py:768-771`) is unreachable. "Uninstall keeps the workspace, run the line again" hits the same wall, because uninstall leaves the profile. Wanted: a retained profile that carries `runtime_environment` or `service_declaration`, or whose paths lie under the recorded program root, is treated as managed and passes. RB-8 works around it.
- **App: onboarding "Open my local editor" and the copied agent instructions hardcode port 5180.** They should use the port the page was served from. Reported from the stack run, which serves the editor on its own port. The code was not read for this plan.
- RunPod pins for live work, in [Plan 62](../62-one-manifest-one-stack/tasks.md#issues-to-file).

**Filed:**
- [#825](https://github.com/banodoco/astrid-dev/issues/825) on macOS, update, restart and uninstall of an autostart-off installation fail with "launchd service configuration is malformed" whenever another Astrid is loaded for the same user. It links #818, #815 and #817. RB-8 avoids it, and Plan 62's V0 is its fix.
- [#815](https://github.com/banodoco/astrid-dev/issues/815) `--managed-by pinokio` means two things, and `--update` is hidden from `--help`.
- [#739 comment](https://github.com/banodoco/astrid-dev/issues/739#issuecomment-6955510571): on a release plan branch, "which commit of each repository" has four unchecked owners that disagree, and nothing checks them on plan branches.
- [#816](https://github.com/banodoco/astrid-dev/issues/816) one command that answers "is this Astrid ready, including rendering".
- [#817](https://github.com/banodoco/astrid-dev/issues/817) a supported way to start a second installation on a copy of an existing workspace. It would delete RB-3's hand edit of the installer record and the installer's empty realm.
- [#818](https://github.com/banodoco/astrid-dev/issues/818) a second installation is isolated only by a fake HOME, because the launchd label and the install record ignore `--root`.
- [#819](https://github.com/banodoco/astrid-dev/issues/819) `dev-local-workspace.mjs` chooses the data root five ways.
- [#739 comment](https://github.com/banodoco/astrid-dev/issues/739#issuecomment-6955511950): the release's repository list omits repositories that already carry release branches (timeline-composition), so `release_branches.py check` cannot see them.
- [#820](https://github.com/banodoco/astrid-dev/issues/820) timeline-composition is vendored twice, linked only by a hand-edited version constant.
