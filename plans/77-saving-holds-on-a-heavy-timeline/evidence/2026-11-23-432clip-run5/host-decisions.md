
## From your host, 05:10Z 23 November: decision on the failed install

The install failed on a set-up fault, not on the product: `run4/stack/runtime.git` was cloned bare from /home/user/astrid-runtime, where commit 77c38d037f98f744bd8f41c15d95429c124a8003 exists only on the remote-tracking ref `refs/remotes/origin/release/15/fix-1491-verified-head`, so the mirror did not contain it. No restore, adoption or fixture was touched. I authorise ONE second attempt, in a NEW root, with the mirror built correctly. Leave `/root/codex/p77box/run4` exactly as it is: it is the record of attempt 1. Do not delete or reuse anything in it.

Attempt 2:
1. Leftover Git processes from attempt 1 (you named 5294, 5296, 5298, 5300): if any still exist and belong to that installer session, end them with a plain TERM and record their command lines and exit; if they are gone, record that.
2. New root: RUN5=/root/codex/p77box/run5 (must be absent; create it mode 700), STACK=$RUN5/stack, RECEIPTS=$RUN5/receipts. Everything the amendment says about run4 paths applies to run5.
3. Do NOT re-run the pin generation. Reuse `/root/codex/p77box/firstcut-432-reviewed-pins` as it is: verify both worktrees are clean, that `exact-tuple.txt` is unchanged (record its SHA-256 and its five lines), and take APP_SHA, AGENT_SHA, RUNTIME_SHA from it.
4. Build the private mirrors so that each provably contains its exact commit BEFORE the installer runs. For the Runtime: fetch `refs/remotes/origin/release/15/fix-1491-verified-head` from /home/user/astrid-runtime into a named branch in the new bare mirror (or fetch the commit by SHA from a source where it is reachable), then require `git --git-dir=$STACK/runtime.git rev-parse '77c38d037f98f744bd8f41c15d95429c124a8003^{commit}'` to print exactly that SHA. Same proof for the Agent mirror and the generated AGENT_SHA. If either proof fails, stop before the installer.
5. Then continue exactly as the amendment says from "immediately before the isolated installer command": `run4_space before_install 25` (its log goes in the new RECEIPTS), the manifest check, the install ONCE, and on through sections 2 to 6 with all the same stops. A refusal at adoption's final verification is still the result, with no retry. This second install attempt is the last: if it fails for any reason, stop and report.
6. In your RESULT.md, report attempt 1 and attempt 2 separately, and state plainly that attempt 1 failed in set-up before any product step, with the mirror cause above. Write SHA256SUMS for `run5/receipts` (and leave `run4/receipts/SHA256SUMS` as it is).
All other rules in your prompt stand (custody, no interpretation, heartbeats, do not stop for details of how to observe).

## From your host, 05:42Z: disposition of the stopped compiled build

Record it as it is: attempt 2 stopped at the compiled build in section 5; no browser observation; no further attempt, no restart, no resume. Do not start the Runtime again.

One last READ-ONLY step from the files that already exist (start no process, touch no realm), then finish:
1. From `run5/receipts/build.log` and the build script: the exact command that failed, the URL and endpoint it called, the timeout it used, and where port 38175 came from (which discovery or door record named it). Quote the lines.
2. From the Runtime's and services' own logs under `run5/stack` for the window 05:34:00Z to 05:36:30Z: what the Runtime logged (requests received on that port with their durations or absence, lock or verification activity, errors), and what the pack-host service logged for its five restarts and the chat service for `readiness_timeout` (first error of each, quoted, with timestamps). Redact any field named key_id or manifest_hmac; never open a key file.
3. From `adopt.json` and the adoption logs: the timestamps of adoption's own phases (materialize, final verification, the transport timeout) so the 843 s can be split.
Write these three as `run5/receipts/post-stop-log-extract.md` (raw quotes with file and line, no interpretation), add it to `run5/receipts/SHA256SUMS`, re-hash the signed backup directory's database file and the stopped source realm's database exactly as the runbook's section 6 says if it names them (if the runbook does not name a command for them, say so and skip), append a "Disposition" section to RESULT.md saying the above, and end `RUN-STATUS: DONE`.
