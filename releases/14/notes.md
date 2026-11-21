# Release 14 — stability and reliable creative work (DRAFT)

**Status: NOT PUBLISHED.** This draft is conditional on the frozen tuple, Release 14 qualification and the owner's explicit publication approval. Do not present these as shipped features until the Lead has verified the exact resulting product commits. This is an **optional update**: Release 13 installs are not required to upgrade, and Release 14 must remain compatible with supported Release 13 states.

Release 14 focuses on making ordinary creative work dependable: installs and updates that preserve existing projects, edits that save or refuse clearly, and generation that retains usable evidence when something fails. The release also incorporates the approved Plans 59, 64 and 65 creative work **only to the extent it lands and passes the combined Release 14 gates**.

## Intended changes since Release 13

- **Windows paths and installation:** shorter result/manifest names and installation paths, tested path-length budgets, and the Windows Runtime permissions behavior ([#671](https://github.com/banodoco/astrid-dev/issues/671), [#672](https://github.com/banodoco/astrid-dev/issues/672), [#673](https://github.com/banodoco/astrid-dev/issues/673), [#674](https://github.com/banodoco/astrid-dev/issues/674)).
- **Startup and dependencies:** VibeComfy workflow/node-loading cleanup, verified certificate handling without disabling TLS, restartable model downloads and clearer installer browser control ([#676](https://github.com/banodoco/astrid-dev/issues/676), [#721](https://github.com/banodoco/astrid-dev/issues/721), [#722](https://github.com/banodoco/astrid-dev/issues/722), [#723](https://github.com/banodoco/astrid-dev/issues/723)). Do not describe the TLS change as accepting unverified certificates.
- **Editing and save behavior:** targeted repairs for long-lived timelines that previously refused simple edits or duplicated validation against untouched historical content ([#839](https://github.com/banodoco/astrid-dev/issues/839), [#842](https://github.com/banodoco/astrid-dev/issues/842)); a rejected save must stop and explain, offering **“Copy my change out”** or an explicit **“Discard and reload the saved version”** rather than silently overwriting work (FIX-16). A fix is a shipped claim only after it lands and passes the original saved/reopened journeys.
- **Failure handling and recovery:** work on durable retry/failure evidence ([#926](https://github.com/banodoco/astrid-dev/issues/926)), the host activation/abort race tracked in [#905](https://github.com/banodoco/astrid-dev/issues/905), and the too-early “Saved” state tracked in [#966](https://github.com/banodoco/astrid-dev/issues/966). **#905 and #966 remain open at draft time**; do not call them fixed unless the Lead links a landed commit and passing reproducer.
- **Error envelope:** CLI and MCP errors include the literal JSON field `"code": null` where no code is available. Consumers must not treat absent `code` and an explicit null as the same wire representation.
- **Creative work on the combined candidate:** Plans 59 (Into the Minkhole), 64 (H3 speaker references) and 65 (H3 output sizing) were added to this release by the [21 November owner decision](https://github.com/banodoco/astrid-dev/issues/796#issuecomment-7063263106). Final notes will name **only the demonstrated creator-visible capabilities**, after their reviewed changes land and real outputs pass.

## Updating an existing installation

Release 14 is **opt-in**, not a required update. Use the normal update path from a supported Release 13 installation; keep the existing project/realm and verify an edit survives save, reload and reopen. The completed FIX-17 update matrix must test fresh installs on Windows, macOS and Linux, update-over-R13, a killed Windows update, and both live-web/mixed-version states. The owner personally runs the final Windows update on a real Release 13 installation, including one local generation, cancel and retry.

There is no instruction here to delete user data, recreate a project, reset an installation, or take a test-only shortcut around a refused save.

## Known limitations and explicit non-claims

- The **Plan 39 inherited red-test ceiling remains visible**. The release may qualify only with the authorized per-ID comparison; new failures, missing IDs or regressions are not acceptable. A green summary total alone proves nothing.
- **Speed work moves to Release 15.** Release 14 makes no performance, warm-start or under-one-second claim ([decision](https://github.com/banodoco/astrid-dev/issues/796#issuecomment-7061778603)).
- **Scene-by-reference moves to Release 15**; Release 14's save-refusal card does not implement scene-by-reference ([decision](https://github.com/banodoco/astrid-dev/issues/796#issuecomment-7061951208)).
- The four Release 13→14 test differences (two Hyperframes public-service renders, a middle-shot duration check, and external process adoption) require FIX-18 causal disposition. No test is skipped, deleted, or relaxed simply to announce the release.
- A change to the Runtime timeline save contract is not automatically backward compatible. Release 14 App writing to an **unupdated R13 install** and R13 App reading an **R14-written realm** both require the FIX-17 mixed-version rows to pass. Do not claim these cases pass before that result.
- The final rented RunPod generation, teardown receipt and owner-run real Windows checks are pending in [the publication checklist](evidence/publication-checklist.md).

## Maintainer sign-off (not user-facing release copy)

Before changing this draft to final, link the reviewed Agent, Runtime, VibeComfy and App SHAs, the exact App manifest and schema digest, per-ID/job diff versus published Release 13, the two same-day FIX-17 matrix passes, owner Windows/local generation receipt, Lead rented generation output/cost/empty census, rollback readiness and served-manifest canary. Confirm each issue above actually landed. Release manager and owner alone decide the publish; a draft PR is not permission.
