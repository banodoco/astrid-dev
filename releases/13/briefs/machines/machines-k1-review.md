difficulty: astra (review, read-only)

# Review K1 (a success after earlier failed jobs on a warm machine is checkpointed and returned) for rigour and robustness (read-only)

**Repo:** Astrid. **Clone:** `/home/user/wt/c-k1`. Review the diff `git diff 22e5a13e5 cf70c72f8` (both commits exist in this clone). Do not edit, commit or push anything; write nothing except your report.

Read first (binding): `/home/user/wt/briefs/wave3/machines-design.md` (owner decisions O1–O8 and the spend-safety constraints) and `/home/user/wt/briefs/wave3/machines-plan.md` (row (none: K1 is a live-finding card; the brief is binding)). The task brief the worker followed: `/home/user/wt/briefs/wave3/machines-k1.md (its live evidence is in live-s1/edit-failure/)`.

## What to look for
- **Money and custody safety:** can any path now rent a pod, extend a paid expiry, exceed the machine's budget cap, skip a release on host shutdown, or let a forgotten machine bill past its bounds? Can a job run on a lease that expired, ended, or belongs to a different owner epoch? Races between admission and expiry.
- **Correctness:** does the code do what the brief's outcome says, on every entry point (CLI, SDK, host operation, restart with a journalled lease)? Dead code or transitions left behind that the brief says to remove; shims; parallel paths.
- **Tests:** do the new tests fail without the change and prove the outcome, or do they test a fake? Was any test weakened, skipped or deleted beyond the conversions the brief allows (generate-time allocation, per-job consent, the consent flag, `--until-release`)? Check each listed conversion keeps its safety assertions.
- **Failure visibility:** is every new refusal one understandable line naming what to do?

You may run read-only checks: `git diff`, `git log`, `grep`, reading files, and these tests only: `tests/packs/runpod/test_warm_sequence_checkpoint.py tests/packs/runpod/test_failed_job_keeps_warm.py tests/packs/runpod/test_keep_warm_evidence.py tests/packs/runpod/test_failure_receipt.py tests/packs/runpod/test_machine.py`, with `TMPDIR=$PWD/.tmp-tests PYTHONPATH="$PWD:/home/user/wt/vibecomfy-fe92ac7" /home/user/astrid-agent.env/venv/bin/python -m pytest -q <files> --basetemp=$PWD/.tmp-tests/pt`; delete `.tmp-tests` afterwards. Never call any RunPod endpoint and never run `astrid generate` or `astrid machines`. Never read `.env`, credential files or ~/.codex. Use your Luna sub-agents for reading, tracing and running the named tests, in parallel; keep your own effort for the judgment. Every sub-agent follows these same rules.

## Report
Findings ordered by severity: **blocking** (money, custody, a wrong outcome, a weakened test), **should fix**, **note**. For each: file and line, what is wrong, a concrete failing scenario, and the smallest fix. End with a verdict: merge, merge after the listed blocking fixes, or do not merge.

## The manager's specific questions
1. The new verification window is bounded by 120 s and the original paid lease. Can verification now run past the paid expiry, or hold a job's custody after the lease ends? Is the window measured at the start of verification, or can a long `engines status` overrun it?
2. Does the checkpoint still refuse a truly changed installation, a different job or epoch, or an expired lease, with `install_unverified` in the message and the receipt?
3. The worker ruled out (b) and (c) and did not investigate (d). Is the evidence for (b) and (c) sound? Given `live-s1/edit-failure/` (213 s of execution, `done` at 1794500293.56, collection starting at 1794500294.75), is (a) consistent with the live timings?
4. `failure_receipt.py:build_receipt` now carries the reason: is that field covered by a test, and does it read as one understandable line?

Run the named tests once as the merge proof. The verdict comes first.
