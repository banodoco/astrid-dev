# Inputs — Releases defined and published from astrid-dev

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — on 8 Nov 2026 the owner asked for releases to be defined and published from astrid-dev, with CI and protection, as a new project that starts after Plan 29 ([planning session](https://claude.ai/code/session_011EzfVzreGCJJQnTuXpbib9)). Next: the owner answers the open decisions below and confirms the scope.

**Prior art:** read-only maps of the release number in the App, Agent, Runtime and Pinokio at App `915bfa84d87268038f396dc999dc2095683e5d8a`, plus two independent design reviews ([planning session](https://claude.ai/code/session_011EzfVzreGCJJQnTuXpbib9)). Key findings:
- The integer `release` is checked as an integer in every repository and persisted on users' disks, so switching the wire format would cost 8–12 days.
- On App `main`, `pin.mjs` added 1 on every pin run, which is how release went from 1 to 9 on 7 Nov.
- At least six consumers read the manifest from an App checkout or image, not from astrid.haus.
- The vision feed already publishes from astrid-dev to a generated-only branch, after testing with the App's parser.
- astrid-dev `main` and App `main` are unprotected, and every product repository is public.

**Approach:** astrid-dev release records, checked by CI with the App's existing manifest check, published like the vision feed. The App syncs one generated copy, so nothing in the Agent, Runtime or Pinokio changes. This replaces Plan 29's UR-8b (version helper, App PR #208), UR-8c (markdown log, astrid-dev PR #82) and UR-8d, and UR-8's tuple guard.

**Challenge:** Reviewed — two independent high-judgment reviews ([planning session](https://claude.ai/code/session_011EzfVzreGCJJQnTuXpbib9)). The first kept the App manifest as the source. The owner then asked for astrid-dev as the source, and the second review, briefed for the simplest reliable design, chose syncing a generated App copy over having astrid.haus serve the manifest at runtime. Proxying would add server code to the install path, make installs depend on GitHub at install time, and change five consumers. It also cut signatures, a separate go-check bot, version arithmetic and the markdown log.

**Review rounds:** Pending — recommend at most three. This is release and security work, and it moves the trust root for code users run into astrid-dev. Next: the owner confirms the number.

**Proof and limits:** see [plan.md](plan.md#completion). astrid-dev `main` protection is a prerequisite for the first publish. A release goes live within one sync interval plus a deploy.

## Owner decisions

Already decided (8 Nov 2026, recorded in [Plan 29's inputs](../29-update-and-release/inputs.md#owner-decisions), decisions 7–8):
- **Versions:** `major.minor.patch`, patch by default, minor or major only when the owner declares it. Release 10 is `0.0.10`.
- **Wire ordering:** the integer `release` stays the ordering key.
- **Required:** its own per-release decision with a reason, never implied by kind. Kind changes no behaviour for now.
- **History:** it starts at a legacy record for the release live when this plan starts, expected to be Release 10 = 0.0.10.
- **Hosted App deploys** are not releases.
- **Source:** astrid-dev defines and publishes each release. This replaces Plan 29 decision 9's "App manifest stays the source".

Open, each with a recommendation:
1. **Sync trigger:** a scheduled pull plus a manual run, with no new credential, or an instant push from astrid-dev, which needs an App write token. Recommend the scheduled pull.
2. **Who can approve a release:** only the owner in `CODEOWNERS`, or any maintainer. Recommend only the owner.
3. **Protection timing:** protect astrid-dev `main` now, since it's required before the first publish. App `main` follows, with a bypass for the sync. Recommend now.

## Source identities

Record exact base SHAs when each task starts. Land App work on `int/31-releases-from-astrid-dev`, and astrid-dev work by PR on `main`.
