# Release 12 VibeComfy CI baseline evidence

Recorded 10 November 2026 for Release 12. Candidate `release12/vibecomfy`
is `8d065a8fef3dd602d5462e27d8eca088cf4e8262`; the compared VibeComfy
`main` revision is `e65f4941d09b1cb4d1dd5aae6171c73e648706f4`. These
findings are routed here for CI triage; VibeComfy's own workflows are outside
the three-repository scope stated in Plan 39, so their eventual owner and scope
need confirmation rather than being assumed by this record.

| Check | Candidate first failure | Base first failure | Evidence and cause |
| --- | --- | --- | --- |
| canonical-parity | [Run 42888944335, job 130084618962](https://github.com/banodoco/VibeComfy/actions/runs/42888944335/job/130084618962) | [Run 42553833451, job 128955055526](https://github.com/banodoco/VibeComfy/actions/runs/42553833451/job/128955055526) | `root-clean` finds tracked `candidate-dependencies.json` and `vendor` missing from the Makefile root allowlist on both revisions. |
| test | [Run 42888944320, job 130084618824](https://github.com/banodoco/VibeComfy/actions/runs/42888944320/job/130084618824) | [Run 42553833097, job 128955053947](https://github.com/banodoco/VibeComfy/actions/runs/42553833097/job/128955053947) | `pip install` cannot find `runpod-lifecycle>=0.3.1.dev0,<0.4`. |
| browser-boot | [Run 42888944320, job 130084619101](https://github.com/banodoco/VibeComfy/actions/runs/42888944320/job/130084619101) | [Run 42553833097, job 128955053701](https://github.com/banodoco/VibeComfy/actions/runs/42553833097/job/128955053701) | The same dependency installation failure. |

The committed lifecycle wheel is configured under `tool.uv.sources`, while the
Makefile's editable install uses pip, which does not use that uv source and
searches the index. Both runs used Python 3.14.4; the logs do not establish the
Python version as the cause. The relevant workflow, Makefile and dependency
configuration are unchanged between these revisions. A repair should preserve
the checks and verify the committed dependency rather than skip them.

These comparisons establish only the **first** failures as present on the
base. The substantive parity, test and browser steps did not execute, so they
do not establish complete CI parity or a passing candidate. No workflows were
rerun for this investigation.
