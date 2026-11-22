Date: 2026-11-22
Kind: issue
Source: Plan 78 run
Resolved by: —

The Agent worker setup completed but did not provision the Node version and Remotion dependencies required by the named element-placement tests. The initial baseline therefore reported fixture failures before reaching the behavior under test. Extend the shared Agent environment smoke/setup to install the renderer's pinned Node and locked Remotion compiler when a named test needs them, and report toolchain readiness before starting the baseline.
