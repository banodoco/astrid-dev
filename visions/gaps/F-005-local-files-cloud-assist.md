# F-005 — Local projects can't yet use a coherent cloud agent, generation and rendering service

**Applies to:** [Local-first, cloud-capable](../principles.md#local-first-cloud-capable) · [Eliminate needless technical wrangling](../principles.md#eliminate-needless-technical-wrangling) · [In the creator's control](../principles.md#in-the-creators-control) · [A Tool for Artistic Ambition](../pillars/artistic-ambition.md) · **Assessment:** Open; remote routes exist but an integrated cloud-assisted local-files workflow has not been qualified.

## Desired state

A creator keeps **the Astrid project database and durable files on their own machine**, while consenting to an optional cloud agent session, remote image/video generation and remote video rendering. The agent handles provider selection, setup and execution within approved permissions and budgets; inputs sent to remote services are explicit and scoped. Results come back as correct editable files/operations in the same local workspace, with progress, cancellation, retry, recoverability and cleanup.

## Current state

Astrid Agent has local orchestration and selected provider/RunPod generation routes; [documented execution paths](https://github.com/banodoco/astrid-agent/blob/main/docs/reference/where-things-run.md) distinguish provider APIs from local and RunPod inference. [Reigh Worker Orchestrator](https://github.com/banodoco/reigh-worker-orchestrator) documents RunPod worker and fal/Wavespeed API orchestration, but [the satellite-disposition review](https://github.com/banodoco/astrid-agent/blob/main/tools/astrid-rename/satellites.md) marks that repository deprecated, with current deployment unverified. None of this establishes **an end-to-end Astrid cloud-agent + generation + render product** retaining local file/database authority.

## Gap

No supported integration has demonstrated secure, consented cloud-agent execution and remote generation/rendering as a coherent local-files Astrid workflow. The task/result protocol, permissions, provider choice, remote temporary-file handling, cost controls, local result reconciliation, crash/stop recovery and artifact provenance must be qualified.

## Closure evidence

With one approved provider/configuration and a declared local project, a user or their agent launches remote work (including image generation and a video render), watches status and costs, cancels/retries as appropriate, and receives correctly linked editable local artifacts with the **local database still authoritative**. A qualification report covers data actually transmitted, permissions, cleanup, non-success paths, security boundaries and retention. Offline/unsupported cases are identified honestly.

## Sources and reassessment

[Plan 25 — cloud-assisted Astrid V1](../../plans/25-cloud-assist-v1/plan.md) · [F-003 — creative execution](F-003-creative-execution.md) · [F-001 — platform reliability](F-001-platform-reliability.md). This gap is about a **specific local-data/remote-execution product boundary**, not all inference-provider plumbing.
