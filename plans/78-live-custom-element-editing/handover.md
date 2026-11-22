# Plan 78 handover

Updated 22 November 2026. [Plan](plan.md) · [Tasks and proof](tasks.md) · [Authority and owner decisions](inputs.md). The hosting Orchestrator owns this run; address the Release 15 Lead through the host. No release landing, publication or paid resource is authorized here.

## Done

- Agent `release/15/plan-78` is at `07e7cc0373f03d139d44de26eaa2c5fe6c8d03df`, based at `8807f820eb47d6018db723511e024a0a123fbe95`. LE-1 merged at `b491c3d4b50830292ff5af7720d1965aa5f70e6b`: one mixed commit and updated skills; 70 focused tests passed. A stale mixed request uses the existing atomic timeline guard and retry rules.
- LE-2a merged at `6d4868be916d75fa58ecb3229dd9eadb06c3a8e4`. The later reader-gate registry repair merged at `8ac4e7ec88a06d51dd12818410654ee66549b876`; exact head passed 28 focused tests and an isolated pack-add/reader/shot-commit probe. The cache key detects collection publication and removal. Separate limits: nested installed-pack edits [#1497](https://github.com/banodoco/astrid-dev/issues/1497), external mutation of an active managed root [#1496](https://github.com/banodoco/astrid-dev/issues/1496), and in-place Node Composition replacement [#1495](https://github.com/banodoco/astrid-dev/issues/1495).
- LE-2b Agent installer and manifest validation merged at `750d98af2ad7b8c2df0e77877935857e7c398789`; 44 focused tests passed against 35 at baseline. The motion pack pin is poms_packs commit `2379ab54aca522019ff4f869cfdf9375bdb56dfc`, `pack-tree-v1` digest `75234c10217e67ec0f111a4cb6be4a6252e172a9cd382506498d07ce1d241029`. The App pin and test are a patch, not an App landing: `/root/codex/plan78/run/app-motion-pin.patch`; its disposable-copy test passed 7 cases.
- [Agent baseline](evidence/tests/astrid-agent/8807f820/summary.md): 187 passed, four failed locally, two deselected by existing configuration. Three failures also appear in hosted run `45031908687`; the fourth, `test_move_reload_and_inverse_import_no_renderer`, passes hosted and fails locally because the isolated wrapper's safe path prevents its subprocess importing `tests.helpers`. The [Lead's hosted failing-ID list](../../releases/15/evidence/agent-ci-baseline-8807f820/) is the CI comparison baseline. The LE-2b baseline is [recorded separately](evidence/tests/astrid-agent/8807f820/le2b/summary.md).

## Live proof and recovery

LE-4 uses a disposable install at `/root/astrid-le4b`, isolated home `/root/codex/le4/isolated2/home`, data root `/root/codex/le4/isolated2/data`, Runtime port 19277, editor 15273, proxy 15274 and capture control 15275. The project is `868f2743c8c94caa8f28c1c82107f26c`, timeline `moderate4`; the editor URL is `http://127.0.0.1:15273/tools/video-editor?connect=1&project=868f2743c8c94caa8f28c1c82107f26c&timeline=moderate4`. Reports are `/root/codex/le4/run2/report.md` through `/root/codex/le4/run8/report.md`; run7's outcome is in `run6/report.md` and `run7/result.md` if `run7/report.md` is absent. These paths are machine-local; copy the final evidence into the plan record.

The owner explicitly instructed on 22 November that the chat use her existing Codex login folder via `CODEX_HOME`; no login files may be read, listed or copied. The first chat session was stopped before any edit; a second made the edit. After a container restart, process IDs are invalid. To restore the isolated stack only when needed, from `/root/codex/le4`:

```sh
source run4/setup-env.sh
export CODEX_HOME=/root/.codex ASTRID_RUNTIME_DOOR_PORT=19277
/root/astrid-le4b/versions/c12a8cf01762/py/bin/astrid-runtime up --profile astrid --data-root /root/codex/le4/isolated2/data --json
cd /root/codex/le4/isolated2/app
PORT=15273 VITE_ASTRID_DYNAMIC_PROXY_PORT=15274 ASTRID_APP_ACP_ENABLED=1 setsid nohup node scripts/dev-local-workspace.mjs --data-root /root/codex/le4/isolated2/data > /root/codex/le4/run8/editor-recovery.log 2>&1 < /dev/null &
```

The launcher starts its proxy. Reopen the editor only after a restart, checking health and the saved project head first; a new page cannot establish that the original page stayed open. The original live no-restart pack probe is in `run4/report.md`, on its original Runtime process: receipt `txn-8e216465a7a14875a48b8428ef0f6765`.

The second chat produced one new history row, seven clips retargeted to two admitted forks, and six titles at numeric times 10, 12, 14, 16, 18 and 20 seconds. History receipt `txn-1a909b6859274123bb4e3b592e9fb69b` points to head `authoring-parent-revision-539ca914f3ece4008c2c76179f5266a1405deaf53d5fa9961882433da8022bfc`. Prompt to history commit was 4 min 21.365 s; admission was reported within 3 min 55 s, exact time unknown. The earliest recorded after-edit DOM result was 5 min 43 s; the first after-still at 9 min 13 s is an upper bound, not first-render latency. `run8/report.md` records four same-page after-stills at 1.50, 3.50, 11.00 and 31.50 s; compare them with the before images and finalize the record with the host. The accepted receipt is in Runtime history; a separate accepted-response comparison was not captured. The four negative cases were recorded in `run2`, not repeated in this chat run. Do not mark LE-4 final until the host says its record is final.

## Next, in order

1. Finish and bind LE-4's prompt, pins, history/receipt, visual comparisons, timing and negative-case record to the exact candidate; resolve the separate response-receipt limitation with the host. The host performs live work.
2. Wait for the Lead's notice through the host that Plan 81 has landed. Release landing order is Plan 81, Plan 40, Plan 77, then Plan 78. Fetch and merge `release/15/main` into the plan branch with a merge commit, then rerun touched focused proof. The earlier temporary Plan 81 rehearsal had no textual conflicts and 70 tests passed, but is not this final merge.
3. When LE-4 is final and the candidate is fixed, update `/root/codex/plan78/run/review-brief.md` to the exact final range and send `READY: R` to the host. A separate reviewer who did none of the work gets at most two rounds; record and repair blocking findings before landing.
4. Tell the Lead through the host before dispatching the one integrated-head Agent CI run; only one Agent CI run may run across the release at a time. Compare all failure IDs against the Lead's hosted baseline, not only the local baseline. Retake the release headline measurement on the final candidate and record its method and result.
5. Apply and validate the App pin line only with the owner's go and the Lead's re-pin order; the host handles the App change. Make `tasks.md` accurate, then prepare the landing pull requests. Nothing lands in `release/15/main` without the owner's go through the host.

## Decisions and other lanes

- 21 November: the owner said “merge to main, add this plan to release 15”; approval covered the written plan, motion-pack pin and two-round review cap ([inputs](inputs.md#owner-decisions)).
- 22 November: “Yes, go on everything” was relayed by the host as the go on the exact motion-pack pin. “USE THE SAME ONE” authorized using the existing login folder via `CODEX_HOME` for the isolated chat stack only.
- The one existing assertion changed is `tests/core/pack/test_cli_manage.py:121`: before, “The pack is available after the host's next start.”; after, “The pack will be picked up by the running host.” The owner has not ratified that exact assertion by name; bring it through the host before landing.
- [#1433](https://github.com/banodoco/astrid-dev/issues/1433) owns admitted-element list/preview timeout behavior. In the rehearsal a scoped list waited about 28.8 s; profiling observed a history read and a list request waiting on the store mutex, but this does not establish a scaling law or all lock ownership. Four timeline-provider tests failed on the untouched local baseline; the hosted list confirms three, while the fourth is the local-only environment difference above. Leave those failures to their owning lanes.
