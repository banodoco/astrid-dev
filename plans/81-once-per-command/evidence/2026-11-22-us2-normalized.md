# US-2 normalized source timing — 22 November 2026

Three independent runs used five fresh commands per group against a real local Runtime and stand-in ComfyUI. Agent test candidate `4a9c717523bb0f715760cd5f9896f544545bf02d`, Python 3.13.18 and pinned Node 20.19.4 ran on a shared four-vCPU Linux container. The Runtime was run from source; this is not an installed-machine baseline. The [accompanying JSON](2026-11-22-us2-normalized.json) records each trial's source identity, UTC times, load, exact CLI argument vectors, per-stage medians, request counts, exits and cleanup status.

| Trial | Same prompt median | Changed prompt median | Timeline edit median |
| --- | ---: | ---: | ---: |
| 1 | 19.734898832 s | 19.500388890 s | 4.134065821 s |
| 2 | 19.992197032 s | 19.825609389 s | 4.076406457 s |
| 3 | 19.547200156 s | 19.493019164 s | 4.031231798 s |

Each run executed `python -m pytest -p evidence_plugin -s -q -m integration tests/integrations/test_command_latency_budget.py::test_command_latency_budget` in its own isolated environment. All 45 timed commands succeeded. Stage names were normalized to Runtime request templates, and object-request durations and counts were accumulated per command before medians. The previously committed original ceiling fixture was not changed; its values remain 20.518135564 s, 20.013684696 s and 4.204190760 s. The owner's ceiling-setting decision remains open.

In each trial the report-only visualization returned a renderer lease failure, not a successful render. The worker's process scans reported cleanup clear. Separate real-delay checks have proved representative categories; complete physical coverage of every observed stage remains open. The earlier unnormalized calibration and its failing rerun are recorded [separately](2026-11-22-us2-source-calibration.md).
