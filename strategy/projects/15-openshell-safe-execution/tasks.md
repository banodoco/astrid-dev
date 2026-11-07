# Tasks: sandboxed execution with OpenShell

[Plan](plan.md) · [Inputs](inputs.md) · [Status and owner](../../../README.md)

## Draft outline

No executable task IDs or assignments are established. After inspecting current source, scope bounded tasks, dependencies, routes, and explicit focused selectors; do not treat these intended outcomes as ready work.

- Reconcile PR #109 and merged dependencies; reuse and streamline setup, start/stop, account connection, and permission controls.
- Specify supported platforms, the in-sandbox app/backend processes, outside client surfaces and access, restricted defaults, and the actual isolation boundary. Preserve a stronger mode without host-folder or host-ComfyUI exceptions; disclose those exceptions when selected.
- Allow external inference only when selected and its service/network access is granted; explain that inference and sent data are outside local sandbox compute. Keep spend and external-service effects visible.
- Prove permitted agent/pack operations, cancellation, and restart. Check that forbidden host files, credentials, network destinations, and unapproved services remain inaccessible.
- Coordinate first use, account setup, and inference behavior with [onboarding](../20-zero-to-first-image/plan.md), [agent setup](../16-streamlined-agent-experience/plan.md), and [inference routing](../12-multiple-inference-routes/plan.md).

Historical full-suite results are evidence to assess, not a request to rerun broad suites. Shared execution and publication limits are in the [run contract](../../../skills/astrid-dev-shared/run-contract.md).
