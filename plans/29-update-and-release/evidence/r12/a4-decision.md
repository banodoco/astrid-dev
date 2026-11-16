# A4 navigation capture decision record

**Status: blocked; no waiver or product change.** A4 requires a zero-failure Direct Journey and a fail-closed credential scan of full raw request headers, observed response bodies, DOM, storage, cookies and outboxes. An incomplete capture or missing genuine request terminal is a failure. This requirement applies even if Release 12 is split.

## Evidence and boundary

[Diagnostic run 42954826041](https://github.com/banodoco/astrid-app/actions/runs/42954826041) joined a gated app-state request to an underlying `Fetch.failRequest` rejection across frame commit, with no observed CDP or Playwright terminal before timeout. The scan failed closed. The rejection detail and underlying disconnect were not observed. [Exact inputs and sanitized sequence](dj-protocol-42954826041.md).

[Local browser probes](a4-devtools/README.md) show a genuine pagehide request can begin after the navigation response, and a streaming response interrupted by navigation can lose its unread suffix. Durable CDP buffering recovered a completed body, not bytes the browser never received; an independent CDP session did not reproduce the CI missing-terminal case. [Supported-version/source comparison](a4-browser-lifecycle/README.md) found no compliant pin-only fix: Playwright 1.65 may infer `requestfailed` from document detachment without a CDP terminal, and tested pairs still lost an interrupted body. The exact cause of the CI omission remains unproved.

## Viable paths and consequences

1. **Browser/DevTools mechanism, recommended for preserving behavior:** demonstrate a mechanism or upstream repair that exposes actual cancellation for the missing-event interleaving and retains the complete original observed response through commit, including real pagehide traffic. Prove both counterexamples locally and then the exact release journey. No supported existing mechanism has been demonstrated; this may require browser ownership or a substantive dependency change and its scope and timing are unknown. Do not infer success from `route.abort()` resolution, document detachment, missing server traffic or an incomplete stream.
2. **App-owned navigation preparation:** coordinate all dirty settings/outbox and lifecycle owners, flush and acknowledge them, settle existing work and prevent new old-document scheduling before navigation, including cancellation recovery. This is a product lifecycle change requiring the release's product-behavior disposition and complete owner coverage; no such change is authorized or implemented here.

A proxy or refetch may help observe traffic but cannot prove a request it never saw or recover an interrupted original response. Reordering the current gate, widening a timeout, suppressing lifecycle work, or accepting inferred terminals does not satisfy the stated guarantee. Until a path is demonstrated and qualified, A4 and `A-FROZEN` remain blocked.
