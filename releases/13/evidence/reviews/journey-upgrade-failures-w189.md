**There are two distinct failures.** Four A′ rows expose an upgrade regression: the candidate pack host refuses the boot manifest left by Release 9, so candidate startup fails. The two Release 11 rows stop earlier at an R12-specific harness guard and do not test the upgrade. A″’s completed failed row hits the same guard.

The [row-by-row evidence file](/tmp/w189-first-failure-context.txt) contains 25 lines of context on each side of the first exception or guard failure. One unrelated registration-output line is omitted.

| Row | First failure and classification | Context |
|---|---|---|
| A′ `direct-linux` | Candidate `install --update` after a successful R0 → R9 handoff: **`BootManifestDrift: boot manifest disagrees with live registry/fixtures`**. The installer exits 1 and records rollback to Release 9. **Upgrade regression.** | [Linux handoff](/tmp/w189-first-failure-context.txt:1) |
| A′ `direct-macos` | Same `BootManifestDrift` during candidate `install --update`; exit 1 and rollback to Release 9. **Upgrade regression.** | [macOS handoff](/tmp/w189-first-failure-context.txt:55) |
| A′ `direct-linux-r9-install` | Candidate plain `install` over Release 9: same `BootManifestDrift`; the harness reports **`install-bootstrap.log: exit 1`**. **Upgrade regression.** | [Linux R9 install](/tmp/w189-first-failure-context.txt:109) |
| A′ `direct-macos-r9-install` | Same boot-manifest exception and **`install-bootstrap.log: exit 1`** during candidate plain install. **Upgrade regression.** | [macOS R9 install](/tmp/w189-first-failure-context.txt:163) |
| A′ `direct-linux-r11-update` | **`release11-then-update requires the candidate to be Release 12, not 13`**. The receipt marks the Release 11 install and subsequent checks `not-run`. **Harness constraint.** | [Linux R11 guard](/tmp/w189-first-failure-context.txt:217) |
| A′ `direct-macos-r11-update` | Same Release 12 guard, before installation. **Harness constraint.** | [macOS R11 guard](/tmp/w189-first-failure-context.txt:271) |
| A″ `direct-macos-r11-update` | Same Release 12 guard. This is the only A″ failed row present in the job listing I checked; it does not establish whether A″ has the four boot-manifest failures. | [A″ macOS R11 guard](/tmp/w189-first-failure-context.txt:325) |

For the four installer failures, the stored manifest has `profile_order=['pip_embedded', 'checkout_server']` and populated profile and fixture digests; the candidate computes an empty profile order and empty profile and fixture digests, with a different registry digest. The exception is wrapped as **`generic Astrid pack boot manifest could not be composed; restart Astrid`**. The installer then reports that the service stopped while starting. The two handoff receipts explicitly record `start: 9`, `target: 13`, `still: 9`, and `kind: rolled-back`.

The R12 Linux baseline diverges at the same commands:

- **R0 handoff:** R12 candidate `install --update` exited 0 and reported “Astrid updated: Release 9 → Release 12.” A′ exited 1 during candidate pack-host startup.
- **R9 install:** The same candidate plain `install` over Release 9 reached “Startup: running and ready” on R12 and recorded a 9 → 12 transition. A′ failed service readiness.
- **R11 update:** R12 passed the release guard and reported “Astrid updated: Release 11 → Release 12.” A′ is rejected by the guard before Release 11 is installed.

The candidate’s relevant changes are Agent commits `9f00e2ae2` and `a26030e78`, which removed the two boot profiles. In A′, [boot_manifest.py:25](https://github.com/banodoco/astrid-agent/blob/f709407cb10cc56bafebae51080832386bca3a44/astrid/core/_shared/boot_manifest.py#L25) sets an empty default order, while [boot_manifest.py:388](https://github.com/banodoco/astrid-agent/blob/f709407cb10cc56bafebae51080832386bca3a44/astrid/core/_shared/boot_manifest.py#L388) rejects an existing different stamp. The candidate reaches that comparison through [dispatch.py:740](https://github.com/banodoco/astrid-agent/blob/f709407cb10cc56bafebae51080832386bca3a44/astrid/core/gateway/dispatch.py#L740). The needed product fix is a controlled migration or regeneration of a recognized older derived boot manifest during upgrade, with rollback and same-version drift detection preserved.

Separately, update the R12 harness’s [Release 11 target constant](https://github.com/banodoco/astrid-agent/blob/1940a2fe11d8b131320dcf1c32dcfb69af288aef/scripts/journey_version_jumps.py#L65) and [admission check](https://github.com/banodoco/astrid-agent/blob/1940a2fe11d8b131320dcf1c32dcfb69af288aef/scripts/journey_version_jumps.py#L1303) to admit and verify the intended Release 13 candidate. Until that journey runs past admission, the Release 11 → 13 upgrade remains unproven.

The observed exception is a **pack-host boot-manifest** mismatch, not the RunPod managed-source pin refusal. The Runtime commit resolves through the requested GitHub API, and its archive URL returned HTTP 200. The R0 handoffs completed before candidate update, so the old-launcher and stopped-path inputs are not the observed failure point. These observations do not independently prove every candidate pin is correct.

A minimal offline reproduction should stamp a scratch support root using the older release’s `compose_profile_handoff`, then invoke A′’s composition against the same manifest; the second call should raise `BootManifestDrift`. This isolates the persisted-manifest boundary without a provider call. **I did not run that two-version reproduction.** No GitHub writes, provider calls, reruns, or tracked-file edits were made.