# Sanitizer and selection policy

We sanitize every staged text file by replacing home and scratchpad absolute paths with `~`, removing email addresses, and flattening local absolute Markdown links into plain source references so the paths do not become broken links. Files are refused if they contain credential-looking prefixes with at least eight token characters, a credential carried in an authorization header, or an exact value read in memory from the local Wavespeed, Replicate, or GitHub token files. Secret values are never written to this bundle.

Included: 132 files (1950846 staged bytes).
Skipped: 0 files (0 source bytes).
Refused: 0 files (0 source bytes).
Missing exact requested files: 0.
Selection excludes `codex/*.log`, all video and audio, and large PNG sets. Selected JPEGs are downscaled/re-encoded below 300 KB. `sfx/` contributes only `FRICTION.md` and `SOURCES.md`.
