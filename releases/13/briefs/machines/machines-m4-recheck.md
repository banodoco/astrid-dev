difficulty: astra (review, read-only)

# Review M4, re-check after card 4 (a claim has a lifetime and an idle time; the cap bounds both) for rigour and robustness (read-only)

**Repo:** Astrid. **Clone:** `/home/user/wt/c-m4`. Review the diff `git diff 1d4471866 0d152b373` (both commits exist in this clone). Do not edit, commit or push anything; write nothing except your report.

Read first (binding): `/home/user/wt/briefs/wave3/machines-design.md` (owner decisions O1–O8 and the spend-safety constraints) and `/home/user/wt/briefs/wave3/machines-plan.md` (row **M4**). The task brief the worker followed: `/home/user/wt/briefs/wave3/machines-m4-4.md (card 4)`.

## What to look for
- **Money and custody safety:** can any path now rent a pod, extend a paid expiry, exceed the machine's budget cap, skip a release on host shutdown, or let a forgotten machine bill past its bounds? Can a job run on a lease that expired, ended, or belongs to a different owner epoch? Races between admission and expiry.
- **Correctness:** does the code do what the brief's outcome says, on every entry point (CLI, SDK, host operation, restart with a journalled lease)? Dead code or transitions left behind that the brief says to remove; shims; parallel paths.
- **Tests:** do the new tests fail without the change and prove the outcome, or do they test a fake? Was any test weakened, skipped or deleted beyond the conversions the brief allows (generate-time allocation, per-job consent, the consent flag, `--until-release`)? Check each listed conversion keeps its safety assertions.
- **Failure visibility:** is every new refusal one understandable line naming what to do?

You may run read-only checks: `git diff`, `git log`, `grep`, reading files, and these tests only: `tests/core/test_machines_claim.py tests/test_setup_skill_branches.py tests/packs/runpod/test_target_selection.py tests/core/generation/test_cli.py tests/packs/runpod/test_warm_session.py tests/packs/runpod/test_machine.py tests/packs/runpod/test_owner_retry_gate.py`, with `TMPDIR=$PWD/.tmp-tests PYTHONPATH="$PWD:/home/user/wt/vibecomfy-a8a7be7" /home/user/astrid-agent.env/venv/bin/python -m pytest -q <files> --basetemp=$PWD/.tmp-tests/pt`; delete `.tmp-tests` afterwards. Never call any RunPod endpoint and never run `astrid generate` or `astrid machines`. Never read `.env`, credential files or ~/.codex. Use your Luna sub-agents for reading, tracing and running the named tests, in parallel; keep your own effort for the judgment. Every sub-agent follows these same rules.

## Report
Findings ordered by severity: **blocking** (money, custody, a wrong outcome, a weakened test), **should fix**, **note**. For each: file and line, what is wrong, a concrete failing scenario, and the smallest fix. End with a verdict: merge, merge after the listed blocking fixes, or do not merge.

**This is a re-check.** Your review (`machines-m4-review.log`) gave seven findings, all accepted, and card 4 (`1d4471866..0d152b373`) addresses them, along with the 429 owner's three conditions: the 1 s floor is only on the owner's recovery timers; cooldown, Retry-After and back-off still win; and a consecutive-429 test covers release and in-flight-create recovery. Confirm each one is closed. Above all, check finding 1: the expiry persisted before the paid POST. Can any path still bill past min(cap, start + lifetime): slow readiness, an acquisition retry, recovery after a crash mid-acquisition? Then review its twelve test conversions (listed in `machines-m4-4.log`'s final report): each must keep its money, custody and release assertions. Card 4's own proof passed 411. **Do not rerun the whole six-file set.** Run only `tests/packs/runpod/test_owner_retry_gate.py`, `tests/core/test_machines_claim.py` and `tests/test_setup_skill_branches.py`, plus the named tests you need for a specific doubt. The verdict comes first, then findings.
