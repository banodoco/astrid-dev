# Independent pre-publication review — four POSIX prerequisites

**Verdict: NO BLOCKER for this bounded card on the supported Linux/macOS/Windows targets.** Full K1a remains incomplete; formal RS1 remains **0/1**.

Reviewed exact Agent range `cd778822a9a5fab273144ca367cfdd94a20889e3..16ef29bf8cd9d9df82c6f2a892feff3dffc44d70`, independently resolved tree `f155b695df8c89b375e761ae1a4f51470c41bc85`. Read the manager card, complete diff, before/after logs and exits, AST comparison, platform-selection evidence, source fixtures and registry. No source edits, test reruns, workflow actions or remote changes; this report is the sole write. Diff whitespace check passes.

## Scope and coverage

Exactly four function-level gates change: default VibeComfy runtime-root host placement; real O_NOFOLLOW lock refusal; the POSIX `fcntl` probe for simulated Windows transaction-lock retention; and a fake installed launcher's POSIX shebang. All assertions, parameters and neighboring tests remain unchanged. Only the now-unused `sys` import in the runtime-root file is removed. The authorized exception to literal body equality is `fcntl = pytest.importorskip("fcntl")` becoming function-local `import fcntl`; the binding used by the existing assertions is unchanged.

The `fcntl` import remains **inside that single marked function**. Importing/collecting the module on Windows does not import `fcntl`; the existing registry applies the unavailable `posix_native` skip before test execution. The `windows` fixture simulates Windows transaction behavior by changing product-module objects, not the actual host registry's `os.name`. Its native POSIX lock probe retains the same four-rename and journal/backup-retirement assertions. No module mark was introduced, so other Windows tests keep their selection.

The existing POSIX lane is default-on for Linux/macOS and unavailable on Windows. As with earlier cards, eligibility does not imply macOS CI execution: the dedicated Darwin job's expression selects Darwin/Remotion/Chrome/Codex lanes, not ordinary POSIX tests. Both before and after these four cases remain in the ordinary Linux selection. Raw evidence records **4 passed before and after**, exits **0/0**. This is not a native Windows or macOS run.

## O_NOFOLLOW capability boundary

The old condition is a capability check (`hasattr(os, "O_NOFOLLOW")`), whereas `posix_native` is an OS check. They are **not universally equivalent for every Unix/Python build**. The equivalence is justified only for the supported ordinary Linux and macOS CPython targets, where the real flag exists, and Windows, where it does not. The retained evidence observes Linux CPython 3.12.14 with `O_NOFOLLOW=131072`.

Independently checked primary documentation: [CPython os constants](https://docs.python.org/3.12/library/os.html#os.O_NOFOLLOW) explicitly makes extension availability depend on the C library; [Apple's Mac OS X open(2)](https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man2/open.2.html) defines O_NOFOLLOW and its symlink-refusal behavior. This supports the card's limited platform claim, not a blanket statement that every `os.name == "posix"` runtime has the flag. No supported-target mismatch was established, so this distinction is not a blocker. If supported targets later include a POSIX build lacking the flag, this test's native-path premise must be revisited; its current body can also receive ELOOP from the fallback and is not itself a capability attestation.

The neighboring tests that deliberately remove O_NOFOLLOW still exist and are unchanged. No actual symlink/permission failure is hidden by a new fallback or expectation change.

## Ownership and remaining work

These bodies test path placement, filesystem lock refusal/retention and launcher argument dispatch. They do not modify or prove Plan 38 process identity/peer custody/source-closure parity or Plan 55 warm session/transport/budget behavior. No excluded owned contract change was found.

“Complete” can describe this four-gate card only. The full scanner, other direct skips and Plan 38 hold remain separate and are not waived. No concrete remaining regression risk required an additional test in this review.
