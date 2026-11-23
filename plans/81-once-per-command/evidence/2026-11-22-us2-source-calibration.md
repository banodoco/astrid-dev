# US-2 source calibration — 22 November 2026

Agent plan base `95b700fdf4b269a406bb057b521abb5922ce16ef`; test candidate `0f2b07cb0990621402418c13edc543c393eac928`. Agent's locked Runtime `0af5af11d71016fa08f65058c558c56a47e9b5a7`; VibeComfy `799d90f619a6723d0b376b7e77aef09c244a0821`; lifecycle `9f88ef7640bc664f697112d966ecefa123d44340`. Shared four-vCPU Linux container, Python 3.13.18, Node 20.19.4; Runtime runs from a checkout, ComfyUI is a stand-in. These are provisional source figures, not installed-Astrid evidence.

Each group used five fresh processes. Calibration load average at start was approximately 0.79/1.64/1.33, rising to roughly 2. Candidate-check load was approximately 4.50/3.38/2.46. Other work shares this machine. Run commands used the task worktree and its isolated setup:

```sh
PYTEST_ADDOPTS='-rA -m integration' bash /root/codex/plan-81/astrid-dev/env/agent-pytest.sh tests/integrations/test_command_latency_budget.py
```

The calibration was a precommit measurement of the same test path; the candidate check was on the named commit. Exact per-stage results and report-only visualization outcomes are in [the accompanying JSON](2026-11-22-us2-source-calibration.json).

| Group | Calibration median | Candidate median | Result against initial ceiling |
| --- | ---: | ---: | --- |
| Repeated prompt | 20.518135564 s | 20.207610304 s | Below |
| Changed prompt | 20.013684696 s | 20.701176700 s | Above by 0.687492004 s |
| Timeline edit | 4.204190760 s | 3.953441957 s | Below |

Calibration start-to-ready was 2.119151091 s; candidate check was 2.016306070 s. Both one-frame visualization observations failed: the renderer lease channel closed after 65.39 s and 68.95 s respectively. This is a reported failure, not a successful visualization measurement. Initial calibration test completed (exit 0); candidate gate failed (exit 1) on changed-prompt ceiling. No ceiling was raised. Real per-stage delay injection proof remains incomplete. Owner-machine US-0 remains the authoritative installed baseline.
