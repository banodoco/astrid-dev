# Releases

One row per published Astrid release, in release order. The log is add-only: a row is written once, from `pin.mjs --release` output, after the canary passes, and is never edited afterwards. The App manifest (`public/install-manifest.json`) is what the product acts on; this log records what shipped. The steps are in the [release skill](../skills/astrid-dev-release/SKILL.md).

- **App commit** is the merge commit that published the release. Later hosted App deploys are not releases.
- **Pinokio** is informational only; `—` means the manifest does not record it.
- **Required** is `no`, or the reason an update is required. It is never implied by the kind.
- **Projects** links the plans that shipped in the release.

| Release | Version | Kind | Date | App commit | Agent | Runtime | Pinokio | Required | Projects | Owner go |
|---|---|---|---|---|---|---|---|---|---|---|
| 9 | 0.0.9 | legacy | 2026-11-07 | 915bfa84d87268038f396dc999dc2095683e5d8a | 709492fa5f4850b9caf0cea4a4c543023b73fa0a | f4c7a4623c84da077daac3e3a9366fc2e6a55051 | — | no | [Plan 01](01-installer-consent/plan.md) | Owner decision 9, 8 Nov 2026 |
