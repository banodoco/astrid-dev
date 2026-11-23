# Tooling friction

- Brief names Agent clone `astrid-agent`, actual clone is `agent-src`; discovered with rg/worktree inventory. Skill symlinks require canonical path for relative documents.

- Source checkout identities change during fix development: product render returned `identity_mismatch: An older Astrid is still running. Restart it after its running tasks finish.` Correct route is finalize source then restart source stack, preserving copied data.

- Passing --astrid to the App couples the UI browser source to the Agent checkout, losing legacy am-* components after their managed-pack extraction. Supported split: omit --astrid/unset ASTRID_CHECKOUT for App, keep explicit SourceProfile selecting Agent worktree for Runtime. No App code change.
- Full candidate validation is stricter than timing-only validation: retained334microsecond occurrence overrun is rejudged when at/bound retime. Exact15-frameplan cannot silentlyrounditaway.

- Capture-only global visibility CSS hides embedded media documents in Playwright screenshots. Rejected those shots; retain normal player screenshots and mask editor chrome only during image comparison. First complete capture also hit URL constant shadowing in metadata after all20 seeks; corrected helper.

- Pause harness initially refused internal-revision refs; fixed exact pinned internal-revision→shot mapping without broadening allowed clip keys. Corrected live dryrun then refused stale head before any commit: concurrent external version38 deleted r6-sfx-wah-clip. Root/subagents issued no publication. Preserved readback/diff and restored original stack under user data-safety rule.
