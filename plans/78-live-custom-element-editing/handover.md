# Plan 78 handover

Updated 23 November 2026. [Plan](plan.md) · [Tasks and proof](tasks.md) · [Authority and owner decisions](inputs.md). The hosting Orchestrator owns this run; address the Release 15 Lead through the host. The Lead controls landing after confirming its gate in writing; publication and paid resources remain with the owner.

## Done

- Agent `release/15/plan-78` is pushed at `c5f6054656cf98c783444cb2e5ae1bd13eeec0b8`, based at `8807f820eb47d6018db723511e024a0a123fbe95`. LE-1 merged at `b491c3d4b50830292ff5af7720d1965aa5f70e6b`: one mixed commit and updated skills; 70 focused tests passed. A stale mixed request uses the existing atomic timeline guard and retry rules.
- LE-2a merged at `6d4868be916d75fa58ecb3229dd9eadb06c3a8e4`. The later reader-gate registry repair merged at `8ac4e7ec88a06d51dd12818410654ee66549b876`; exact head passed 28 focused tests and an isolated pack-add/reader/shot-commit probe. The earlier collection-state key is removed in the narrowed local candidate. Separate limits: nested installed-pack edits [#1497](https://github.com/banodoco/astrid-dev/issues/1497), external mutation of an active managed root [#1496](https://github.com/banodoco/astrid-dev/issues/1496), and in-place Node Composition replacement [#1495](https://github.com/banodoco/astrid-dev/issues/1495).
- LE-2b Agent installer and manifest validation merged at `750d98af2ad7b8c2df0e77877935857e7c398789`; 44 focused tests passed against 35 at baseline. The motion pack pin is poms_packs commit `2379ab54aca522019ff4f869cfdf9375bdb56dfc`, `pack-tree-v1` digest `75234c10217e67ec0f111a4cb6be4a6252e172a9cd382506498d07ce1d241029`. The App pin and test are a patch, not an App landing: [evidence/app-motion-pin.patch](evidence/app-motion-pin.patch); its disposable-copy test passed 7 cases.
- [Agent baseline](evidence/tests/astrid-agent/8807f820/summary.md): 187 passed, four failed locally, two deselected by existing configuration. Three failures also appear in hosted run `45031908687`; the fourth, `test_move_reload_and_inverse_import_no_renderer`, passes hosted and fails locally because the isolated wrapper's safe path prevents its subprocess importing `tests.helpers`. The [Lead's hosted failing-ID list](../../releases/15/evidence/agent-ci-baseline-8807f820/) is the CI comparison baseline. The LE-2b baseline is [recorded separately](evidence/tests/astrid-agent/8807f820/le2b/summary.md).

## Review and current gates

Two independent review rounds found 17 findings; ten concerned registry generation tracking and update-path default-pack publication. On 23 November the host adopted the narrower scope requested by the Lead: clear and rediscover once on a miss, and publish release defaults only on fresh install, preserving truthful recovery reporting. [Tasks](tasks.md) records the cases, the changed run-added assertions and the Lead's authorization for a third full round. Deferred limits: warm alias-to-exact [#1538](https://github.com/banodoco/astrid-dev/issues/1538), removed-pack cache [#1542](https://github.com/banodoco/astrid-dev/issues/1542), nested edits [#1497](https://github.com/banodoco/astrid-dev/issues/1497), managed-root changes [#1496](https://github.com/banodoco/astrid-dev/issues/1496), Node Composition replacement [#1495](https://github.com/banodoco/astrid-dev/issues/1495), and update policy [#1525](https://github.com/banodoco/astrid-dev/issues/1525).

The pushed candidate has the narrowed repairs and the loader-call and media-registry compatibility fixes. Its 53-file module comparison against `0cde50ac` found zero regressions, zero failures without a baseline and zero missing tests: baseline 875 passed, 60 failed, six deselected; candidate 903 passed, 48 failed, six deselected. The classifier counted 49 pre-existing failing IDs and 12 fixed, with pytest subtest reporting accounting for the difference in counts. The two extra reader-module files also match baseline (105 passed and one pre-existing failure). Local evidence: `/root/codex/plan78/run/r22-final3-diff/summary.md` and `/root/codex/plan78/run/third-review-handoff.md`. Frozen Plan 81 rehearsal at this candidate had no conflicts and 259 passed, four known local baseline failures, two CI-lane deselections. The host has been asked to dispatch the independent third review.

The original [live proof](live-proof.md) is useful evidence but does not satisfy the final candidate and heavy-fixture gates. The host repeats LE-4 last on the final candidate, after merging landed Plan 81 and Plan 77's first cut: heavy fixture first, moderate only if heavy cannot load. The repeat needs a sanitized chat/tool trace, before/after history and receipt commands, navigation and timing evidence, and exact installed revisions for each negative case.

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

The second chat produced one new history row, seven clips retargeted to two admitted forks, and six titles at numeric times 10, 12, 14, 16, 18 and 20 seconds. History receipt `txn-1a909b6859274123bb4e3b592e9fb69b` points to head `authoring-parent-revision-539ca914f3ece4008c2c76179f5266a1405deaf53d5fa9961882433da8022bfc`. Prompt to history commit was 4 min 21.365 s; admission was reported within 3 min 55 s, exact time unknown. The earliest recorded after-edit DOM result was 5 min 43 s; the first after-still at 9 min 13 s is an upper bound, not first-render latency. `run8/report.md` records four same-page after-stills at 1.50, 3.50, 11.00 and 31.50 s; compare them with the before images and finalize the record with the host. The accepted receipt is in Runtime history; a separate accepted-response comparison was not captured. The four negative cases were recorded in `run2`, not repeated in this chat run. LE-4 remains open for the final-candidate repeat described above.

## Next, in order

1. The Lead authorised a third full round on 23 November 2026 because two rounds each found a fresh set of blockers. The host dispatches a fresh reviewer on `c5f60546`; resolve its findings through the host.
2. When the Lead reports Plan 81 landed, merge `release/15/main` into the plan branch and rerun touched proof. Landing order is Plan 81, Plan 40, Plan 77, then Plan 78; merge Plan 77's first cut before the final live proof.
3. The host repeats the final LE-4 proof. Tell the Lead before dispatching one final integrated-head Agent CI run; only one Agent CI run may run across the release at a time. Compare failure IDs against the Lead's hosted baseline and retake the headline measurement.
4. The Lead decides the App manifest re-pin and Plan 78 App landing after the Agent side lands. Make `tasks.md` accurate, prepare landing PRs, and obtain the Lead's written gate decision through the host. Release publication remains the owner's decision.

## Decisions and other lanes

- 23 November, relayed by the host: “TRUST THE RLEASE 15 LEAED ON ALL SUCH DECISIONS FROM NOW ON”. The Lead decides the landing gate, that assertion and App pin timing; publication, paid resources, rented machines, and the owner's live installs and media remain with the owner.
- 21 November: the owner said “merge to main, add this plan to release 15”; approval covered the written plan, motion-pack pin and two-round review cap ([inputs](inputs.md#owner-decisions)).
- 22 November: “Yes, go on everything” was relayed by the host as the go on the exact motion-pack pin. “USE THE SAME ONE” authorized using the existing login folder via `CODEX_HOME` for the isolated chat stack only.
- The Lead approved the one existing assertion change at `tests/core/pack/test_cli_manage.py:121`. Before: “The pack is available after the host's next start.” Final: “The pack is installed. Host refresh is pending.” Round two requested this evidence-only wording.
- [#1433](https://github.com/banodoco/astrid-dev/issues/1433) owns admitted-element list/preview timeout behavior. In the rehearsal a scoped list waited about 28.8 s; profiling observed a history read and a list request waiting on the store mutex, but this does not establish a scaling law or all lock ownership. Four timeline-provider tests failed on the untouched local baseline; the hosted list confirms three, while the fourth is the local-only environment difference above. Leave those failures to their owning lanes.
