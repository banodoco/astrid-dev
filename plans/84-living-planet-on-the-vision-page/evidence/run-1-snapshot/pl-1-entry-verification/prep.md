# PL-1 entry repair verifier preparation

Prepared 2026-11-22 for frozen candidate `7f80225f63f4852dbe2463865e0f4a34af908472` in `worktrees/pl-1-entry-verify`.

Copied `worktrees/baseline/node_modules` into private `worktrees/pl-1-entry-verify.env/node_modules` (543 MB) and pointed only this verification worktree's `node_modules` symlink at that copy. Repository-vendor symlinks point into this candidate worktree's `vendor/` tree. No broken symlinks were found. The worktree source is clean at the candidate SHA. No compiler, test, build, or browser command has been run.

Reserved proof scope once the manager releases the heavy slot: unchanged original PublicAstridPlanet component test, the separate entry-boundary tests, scoped lint, focused entry assertions at test locations `:208` and `:338` on this frozen SHA, and laptop/phone poster-before/live-after capture with stage layout shift recorded. No extra entry assertions or broad suite are planned.
