difficulty: astra (review, read-only)

# Review M1, final check (a job attaches to the live claimed machine and never allocates) for rigour and robustness (read-only)

**Repo:** Astrid. **Clone:** `/home/user/wt/c-m1`. Review the diff `git diff 22e5a13e5 2ef923df5` (both commits exist in this clone). Do not edit, commit or push anything; write nothing except your report.

Read first (binding): `/home/user/wt/briefs/wave3/machines-design.md` (owner decisions O1–O8 and the spend-safety constraints) and `/home/user/wt/briefs/wave3/machines-plan.md` (row **M1**). The task brief the worker followed: `machines-m1.md, machines-m1-4.final.md (part b) and machines-m1-5.md (part c, with the manager's two rulings)`.

## What to look for
- **Money and custody safety:** can any path now rent a pod, extend a paid expiry, exceed the machine's budget cap, skip a release on host shutdown, or let a forgotten machine bill past its bounds? Can a job run on a lease that expired, ended, or belongs to a different owner epoch? Races between admission and expiry.
- **Correctness:** does the code do what the brief's outcome says, on every entry point (CLI, SDK, host operation, restart with a journalled lease)? Dead code or transitions left behind that the brief says to remove; shims; parallel paths.
- **Tests:** do the new tests fail without the change and prove the outcome, or do they test a fake? Was any test weakened, skipped or deleted beyond the conversions the brief allows (generate-time allocation, per-job consent, the consent flag, `--until-release`)? Check each listed conversion keeps its safety assertions.
- **Failure visibility:** is every new refusal one understandable line naming what to do?

You may run read-only checks: `git diff`, `git log`, `grep`, reading files, and these tests only: `tests/packs/runpod/test_job_on_claimed_machine.py tests/packs/runpod/test_failed_job_keeps_warm.py tests/packs/runpod/test_failure_receipt.py tests/packs/runpod/test_keep_warm_evidence.py tests/packs/runpod/test_target_selection.py tests/packs/runpod/test_generation_preparation.py tests/packs/runpod/test_acquisition_gates_provider_fields.py`, with `TMPDIR=$PWD/.tmp-tests PYTHONPATH="$PWD:/home/user/wt/vibecomfy-fe92ac7" /home/user/astrid-agent.env/venv/bin/python -m pytest -q <files> --basetemp=$PWD/.tmp-tests/pt`; delete `.tmp-tests` afterwards. Never call any RunPod endpoint and never run `astrid generate` or `astrid machines`. Never read `.env`, credential files or ~/.codex. Use your Luna sub-agents for reading, tracing and running the named tests, in parallel; keep your own effort for the judgment. Every sub-agent follows these same rules.

## Report
Findings ordered by severity: **blocking** (money, custody, a wrong outcome, a weakened test), **should fix**, **note**. For each: file and line, what is wrong, a concrete failing scenario, and the smallest fix. End with a verdict: merge, merge after the listed blocking fixes, or do not merge.

**This is a re-check.** Your earlier review (`machines-m1-review.log`) gave four findings. The manager accepted them all, and part c (`bf3dd2f09..2ef923df5`) addresses them. Confirm each one is closed:
1. no generation-time allocation path remains anywhere in `astrid/` (grep `acquire(`, `owner.select(`, `PaidRunConsent` on job paths);
2. the legacy-journal fallback is deleted, and the one-line refusal plus the release route are tested;
3. the restart test now goes through `TargetProviderBindings.get(job=True)` and asserts the unchanged expiry and cap, both timers re-armed, the old epoch refused, and an active lease that is not adopted;
4. the limit refusals name `astrid machines keep`.

Then review the deletions and conversions in part c: does each deleted test have live-path cover for money and custody, as its report claims? Report anything new at the same severities. Run the named tests once, as the merge proof. Keep it short: the verdict comes first, then findings.

**Specific to part c:** it deleted eight tests that covered only the deleted `RunPodGenerationPreparer`. Three of them were named by the manager. The other five are `test_ordinary_entry_and_raw_workflow_prepare_exact_claim_without_transform`, `test_unsupported_engine_or_undisclosed_limits_refuse_before_claim`, `test_source_validation_failure_happens_before_claim_or_offer`, `test_ambiguous_install_retains_cleanup_and_cannot_replay` and `test_preparation_expiry_never_admits_worker`. For each, find the live-path test (on `RunPodMachine.claim`, `prepare_retained_generation` or the host) that covers its money, custody or expiry concern, or name the gap as **blocking**. Note the worker's own "muddled" remark: a job after a failed preparation is refused as "no machine" before the more specific unresolved-preparation error. Rule whether that refusal is understandable or should name the unresolved preparation.
