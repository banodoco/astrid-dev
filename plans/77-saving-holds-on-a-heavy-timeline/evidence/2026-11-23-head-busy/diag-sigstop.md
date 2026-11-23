# run9 SIGSTOP experiment: does the pack host's idle claim poll cause head_busy?

Stack: /root/codex/le4/isolated3. Runtime PID 543 (instance 2a4eb62990164f8ab879979ac6770fc3, unchanged at every check). Pack host = child 554 (generic_host --service, parent 543). Chat = child 555. Process state checked with ps before and after every signal; 554 was never left stopped (final state Ssl).

Scripts: /root/codex/le4/run9/claude/hist-detail-claude.py (history read, SDK Timeline.open path); /root/codex/le4/run9/diag/open-read.py (Timeline.open, reports exception type and details). Fixture: /root/codex/le4/run4/fixture/generate.py with LE4_PANELS. Note: no editor read script exists under run8; the open-path read here is the SDK Timeline.open call the editor reopen path uses (store.py:480/517).

## A. diag-sigstop-1 (10 titles, one commit)
- 14:51:11-14:51:18 project + timeline created, generate.py LE4_PANELS=10 -> ok, receipt txn-dfbfed99d42a402f983e170cc77260b3 (diag-sigstop-1.log in diag/sigstop1-create.log).
- 14:51:21 read 1 (no pause): REFUSED, TimelineEditError "accepted commit inputs changed during verification (conflict)", elapsed 3.9 s; runtime.log warnings at 14:51:22.874 and 14:51:23.829 "moved total_changes, files, files[WAL]".
- 14:51:25 read 2 (no pause): OPEN_OK, elapsed 4.0 s (lucky pass, likely replay memo; this weakens the 10-title case).
- 14:51:46.193 kill -STOP 554. 14:51:46.203 read start (paused). 14:51:48.100 read rc=0, OPEN_OK, elapsed 1.9 s. 14:51:48.107 kill -CONT 554 (rc=0).
- 14:54:39 read after CONT: history read REFUSED head_busy (1 of 2 attempts); the second attempt raised the same TimelineEditError (conflict).
- 10-title case is confounded by the earlier lucky pass; not used for the verdict.

## B. diag-sigstop-2 (40 titles, one commit) - main case
- 14:52:19-14:52:37 project + timeline created, generate.py LE4_PANELS=40 -> ok, receipt txn-592d43246f1c4cccba5a52e296d61c6e.
- Outside window (no pause), 14:52:42 and 14:53:02, two attempts each:
  - history read: REFUSED head_busy (status refused, reason head_busy, conflicts [], base/current null) x2
  - open read: REFUSED after 10.0 s and 11.5 s, "accepted commit inputs changed during verification", details reason head_busy x2
- Inside window (pack host paused):
  - watchdog CONT armed 14:53:35.153 (fires at +18 s if the manual CONT did not run)
  - 14:53:35.157 kill -STOP 554; ps state Tsl
  - 14:53:35.169 history read start; 14:53:42.969 rc=0 OPEN_OK (elapsed 7.8 s)
  - 14:53:42.975 open read start; 14:53:44.291 rc=0 OPEN_OK (elapsed 0.84 s)
  - 14:53:44.300 kill -CONT 554 (rc=0); ps state Ssl. Stop duration 9.1 s (within 20 s).
- After CONT, 14:53:48 and 14:54:10, two attempts each:
  - history read: REFUSED head_busy x2
  - open read: REFUSED after 10.3 s and 11.5 s, head_busy x2
- Health (step 4): 14:52:52 check (60 s after the first CONT) and 14:54:26 registration rewrite (generic-host.ready.json, status ready); astrid packs status lists astrid_motion (effective_status experimental, install_tier default). Runtime 543, pack host 554, chat 555 all Ssl; PIDs and instance id unchanged.

## Verdict
CONFIRMED for the 40-title project (diag-sigstop-2): the verified history read and the open-path read are refused with head_busy outside the pause (2 of 2 each), pass only while the pack host is stopped (history 7.8 s, open 0.84 s), and are refused again after SIGCONT (2 of 2 each). Pack host stopped 9.1 s, never left stopped.

Caveat: the 10-title project (diag-sigstop-1) passed once before the pause (memo-like), so its paused pass is not independent evidence; its post-CONT read was refused. The result is one 40-title project with a single pause, so it is a strong indication, not a proof of every timing edge. The pass inside the window is consistent with the claim-poll writer (total_changes moved by temp-table writes) but this experiment does not directly observe the writer.

## Notes on the first 60 s health check
Background wait ran 14:51:50-14:52:52. Output at 14:52:52: 543/554/555 Ssl, same PIDs. packs status listed astrid_motion. No "pack refresh not acknowledged" check was repeated beyond this.
