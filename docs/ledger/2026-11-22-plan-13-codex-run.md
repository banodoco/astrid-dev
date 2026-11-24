Date: 2026-11-22
Kind: issue
Source: Plan 13 execution-host manager run and independent review
Resolved by: —

The independent review found eight defects after the first move, including a missed lint gate and growth-guard bypass; a helper also edited two scratch copies of existing tests despite the no-test-edits rule, then restored them and repeated proof with a plugin. Two final CI runs were cancelled, leaving no full-suite result, and “after the forward lands” was interpreted differently for a forward branch and the release branch. Update the manager and runner to require the unchanged lint gate, release-base guard, startup-import and patch-sensitivity probes before handoff; enforce no test edits in scratch as well as the checkout; persist cancelled CI as NO-RESULT with explicit qualification ownership; and name the exact branch and commit whose landing releases a dependency.
