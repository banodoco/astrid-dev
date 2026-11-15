# W217 review: network_policy.py (socketpair + GuardedPopen), agent 8625a4638401fda892dcb29a38f125d6c9fce2cb

VERDICT: PASS

Diff reviewed: `git diff 401dbd78 8625a463 -- astrid/core/execution/network_policy.py`, plus the new test file. The review ran in a clean detached worktree at /tmp/w217/wt. Nothing tracked was edited, nothing was pushed, and nothing was dispatched.

| Check | Verdict |
|---|---|
| A. Reaching the unchecked connect | SAFE |
| B. Races, leaks, hangs | SAFE (two minor non-blocking notes) |
| C. Argument handling and the POSIX regression | SAFE |
| D. GuardedPopen | SAFE (pre-existing gaps noted, none introduced) |
| E. Evidence records | SAFE |
| F. Tests | SAFE for the regression, with missing negative tests listed |
| G. Side-by-side regression run | IDENTICAL, no BLOCK |

The Python (Windows) socketpair path cannot run on this Linux box. I reasoned about it from the code and exercised it by forcing `_kernel_socketpair` to return False. Everything ran on loopback in throwaway interpreters. Python is 3.13.18 and the scripts ran with `python3 -I`.

## G. Required regression check (run first)

The policy was installed with the real `install(policy, evidence)`. That runs `_patch_socket`, `_patch_redirects` and `_patch_native_descendants`. The policy was deny-all: allowed protocols tcp/udp/dns and no destinations.

Four runs were compared. "plain" is an unpatched interpreter. "base" is the policy at 401dbd78. "new" is 8625a463. "prev" is the failed recut 8e8e60b1. Ephemeral ports are normalised to PORT.

| Call | plain | base policy 401dbd78 | NEW policy 8625a463 | prev recut 8e8e60b1 |
|---|---|---|---|---|
| `socketpair()` | `[(AF_UNIX,SOCK_STREAM,0),(AF_UNIX,SOCK_STREAM,0)]` | same | **same** | `OSError 95` |
| `socketpair(AF_UNIX)` | `[(AF_UNIX,SOCK_STREAM,0)]*2` | same | **same** | not run (dies earlier) |
| `socketpair(AF_UNIX, SOCK_DGRAM)` | `[(AF_UNIX,SOCK_DGRAM,0)]*2` | same | **same** | |
| `socketpair(AF_UNIX, STREAM\|NONBLOCK\|CLOEXEC)` | `[(AF_UNIX,SOCK_STREAM,0)]*2` | same | **same** | |
| `socketpair(AF_INET)` | `OSError 95` | same | **same** | |
| `socketpair(family=,type=,proto=)` kwargs | ok, AF_UNIX/STREAM/0 | same | **same** | |
| `new_event_loop()`, `run_until_complete(sleep(0))`, `close()` | `ok` | `ok` | **`ok`** | `OSError 95` |
| `asyncio.run(co)` | `42` | `42` | **`42`** | `OSError 95` |
| `asyncio.run` with `run_in_executor` | `7` | `7` | **`7`** | `OSError 95` |
| `create_connection(("192.0.2.1", 9))` | `ConnectionRefusedError 111` (sandbox network, no policy) | `NetworkPolicyError ... denied dns destination 192.0.2.1` | **same as base** | same as base |
| loopback `connect` outside any pair | `connected` | `NetworkPolicyError ... denied tcp destination 127.0.0.1:PORT` | **same as base** | same as base |
| loopback `connect_ex` | `0` | `NetworkPolicyError ... denied tcp ...:PORT` | **same as base** | same as base |

Results of the diffs, after port normalisation:

- **`diff base new`, deny-all:** the only differing line is `socket.socketpair.__module__` (`socket` versus the policy module). That is the expected wrapper identity.
- **`diff base new`, with `allowed_destinations=["127.0.0.1"]`:** the same single line differs. The loopback connect returns `connected` and `connect_ex` returns `0` in both.
- **`diff plain new`:** the first nine lines (the socketpair and asyncio rows) are identical. The only other differences are the policy denials, which are the same under base.
- **`diff plain prev`:** the 8e8e60b1 wrapper fails with `OSError [Errno 95]`. It also prints `AttributeError: ... no attribute '_ssock'` noise from `BaseEventLoop.__del__`. This confirms the earlier defect and shows the corrected wrapper fixes it.

On POSIX no behavioural difference was found, so there is no BLOCK from G. The evidence file for the NEW run holds only the dns, tcp-denied and tcp-allowed records from the explicit calls. Creating event loops added no `local-socketpair` records.

## C. Argument handling and POSIX behaviour: SAFE

- **POSIX no-argument call.** `socketpair(*args, **kwargs)` is at network_policy.py:185-189. When `_kernel_socketpair()` is true (:158-161) it returns the original `socketpair` called with the same positional and keyword arguments with the arguments exactly as received. The `AF_INET` default exists only on `_loopback_pair` (:191), which POSIX never reaches. CPython's own default is `family=None`, which becomes `AF_UNIX` when it exists. Run G shows `socketpair()` is still AF_UNIX on both ends under the policy, so there is no regression on Linux or macOS.
- **Windows defaults.** The `_loopback_pair` defaults (AF_INET, SOCK_STREAM, 0) equal CPython's `_fallback_socketpair` defaults, which is what `socket.socketpair` is on Windows. asyncio calls `socket.socketpair()` with no arguments in `selector_events` and `proactor_events`, so its default call is unchanged on Windows.
- **Windows rejections.** With the kernel check forced to False, AF_UNIX, SOCK_DGRAM, `SOCK_STREAM|NONBLOCK|CLOEXEC` and proto=6 all raise `ValueError`. That matches the stdlib fallback, which also raises `ValueError` for family, type and proto. The `SOCK_*` flags do not exist on Windows. I know of no provider or asyncio caller that passes them there.
- **Windows kwargs.** `family=, type=, proto=` as keywords is accepted. Extra positional arguments raise `TypeError`, as the stdlib does.

## A. Can the unchecked connect reach anything but the listener's own address? SAFE

Evidence is network_policy.py:191-204. The only call to `originals[(socket.socket,"connect")]` is at :204.

- **Target.** `target = listener.getsockname()[:2]` (:199) comes from a listener the call just bound to the literal `("127.0.0.1", 0)` or `("::1", 0)` (:192, :197). The caller cannot change host or port.
- **Caller-controlled arguments.** The caller controls only family, type and proto, and :192-194 gate them.
  - Family must be the key of a two-entry dict. A non-AF_INET or non-AF_INET6 string or int gives `ValueError`, and an unhashable value gives `TypeError`.
  - Type must be SOCK_STREAM and proto must be 0.
  - There is no way to reach a wildcard bind such as 0.0.0.0, and no IPv4-mapped or dual-stack path.
  - For IPv6, `[:2]` drops flow info and scope id. The result is still `::1` and the port.
- **Normal connect guard.** It is unchanged (:221-223) and nothing is thread-local. A grep finds no `threading.local`.
- **Provider monkeypatching.** If a provider replaces `socket.socket` with a subclass, it does not reach the connect. The lookup key `(socket.socket,"connect")` then misses, so the call fails closed with `KeyError`. I reproduced this with `socket.socket = Evil`. A provider already running in-process can bypass the guard more directly, with `_socket.socket.connect(sock, addr)`, which I ran. This was true at 401dbd78 as well, and the module docstring says the hook is "not a sandbox". The change adds no new reach.

## B. Races, cleanup and hangs: SAFE

Reproduced with `_kernel_socketpair` forced to False.

- **Hostile peer connecting to the listener before the client.** A raw base-class socket (`_socket.socket`) connected to the listener right after `listen()`. `accept()` returned the hostile peer. The pair was rejected with `OSError [Errno 107] ENOTCONN` from `client.getpeername()`. The cause: the listener is closed in `finally` (:212-213) before verification (:214). Closing the listener resets the real client's un-accepted connection. So the wrong peer fails closed, though as `OSError(ENOTCONN)` rather than `ConnectionError`.
- **Spoofing the match.** To pass verification an attacker would need a source port equal to the client's port. That would be a duplicate 4-tuple, which TCP forbids. I judge the match unspoofable.
- **File descriptors.** The fd count returned to its baseline in the hostile-peer case. It also did so when the connect raised `ConnectionRefusedError`, and when the connect never completed and the SIGALRM interrupted `accept` (:209-211 closes the client, :212-213 closes the listener).
- **Hang risk.** If the non-blocking connect fails with any error other than BlockingIOError or InterruptedError, it propagates immediately, so there is no hang. If the connect silently never completes, `accept()` blocks indefinitely (I confirmed with an alarm after 2 seconds). This is identical to CPython's `_fallback_socketpair` (same structure, no timeout). It is not new and not exploitable. Nothing in the policy adds a wait.
- **Thread confusion.** I ran 4 threads spamming loopback connects while 300 pairs were built. All 21363 attempts were denied and 0 were allowed. 8 concurrent pairs also worked.
- **Minor note 1.** Verification (:214-217) is not inside a `try`. If `getpeername` or `getsockname` raises, as in the ENOTCONN case, `server` and `client` are not closed explicitly. CPython's fallback does close them in that case. They stay open only until the exception and its traceback are released, as I measured: 2 fds held while the exception was alive and 0 after it was released. This is low severity and fails closed. Fix: wrap the verification in `try/except: server.close(); client.close(); raise`.
- **Minor note 2.** The `ConnectionError("Unexpected peer connection")` branch itself is unreachable by a real race, because of the ENOTCONN behaviour above. It is defence in depth only.

## D. GuardedPopen: SAFE (nothing worse than the function wrapper)

Evidence is :364-401. Reproduced on both the new and the base module; both runs are `python3 -I`.

- **Check input.** `check(args, kwargs)` receives the positional tuple and keyword mapping exactly as the old wrapper did. The logic is moved verbatim.
- **Denied paths.** Each of these is denied (`NetworkPolicyError`):
  - `subprocess.Popen(list)`, `Popen(args=)`, `shell=True`, `executable=`, `env=`
  - `subprocess.run`, `call` and `check_output`, because `subprocess.run` looks `Popen` up as a global
  - `os.popen`
  - `asyncio.create_subprocess_exec`
  - a subclass created after install
- **Subclassing.** The old function wrapper made `class X(subprocess.Popen)` fail with `TypeError: function() argument 'code' must be code, not str`. I reproduced that on 401dbd78. The new class fixes it.
- **Not covered, same as the old wrapper.** These bypass the guard and did so before:
  - a `Popen` captured before install (`from subprocess import Popen`), which ran a command
  - a subclass created before install (my `PreSub`)
  - `subprocess.Popen.__mro__[1].__init__(...)`, which is one step easier to reach than before but was already reachable through the closure
  - the strict startup path installs the policy before `asyncio` is imported, so `asyncio.windows_utils.Popen` would subclass the guard. I cannot verify this on Windows.
- **Side effects.** `__name__` and `__qualname__` are set to `Popen`, but `__module__` is the policy module. As a result, `pickle.dumps(subprocess.Popen)` raises `PicklingError`, and an instance created before install is not `isinstance(..., subprocess.Popen)`. The old function wrapper made `isinstance` raise `TypeError` outright. No stderr noise appeared when a denied `Popen` was garbage-collected, so there is no `__del__` problem. Optional hardening: `GuardedPopen.__module__ = "subprocess"`.
- **Uninstall.** There is no uninstall function. The policy lasts for the life of the child process, and the tests restore through `originals`. After restoring, `subprocess.Popen is original` is True. A subclass created while patched stays guarded.
- **Pre-existing gap, not caused by this change.** `check` reads `shell` and `executable` from `kwargs` only. Positional `shell` and `executable` bypass the guard. Both the base and the new module print `POSITIONAL_SHELL_BYPASS` for `Popen("ffprobe -x ; echo POSITIONAL_SHELL_BYPASS", -1, None, None, None, None, None, True, True)`. That is the ffprobe prefix for `_local_media_tool` with `shell=True` passed as the 9th positional argument. A separate fix should read the positional arguments via `inspect.signature`. It is out of scope for this diff.

## E. Evidence records: SAFE

- **Records.** On the Windows path every successful pair records one `tcp` event at :218 with `allowed=True` and `detail="local-socketpair"` (verified: 1 event per pair, 2000 pairs gave 2000 events of about 146 bytes). On POSIX nothing is recorded, because no connect happens (checked in run G).
- **Failure path.** A pair that fails verification, or fails earlier, leaves no record even though the unchecked connect ran. That is a minor evidence gap.
- **Volume.** `_EVENTS` is an unbounded list, as before. The existing denial paths already record each attempt without bound, so a provider could always make it large. 2000 loops give about 290 KB of JSON. The events are written once at exit by `_write_evidence`. The host treats child evidence as diagnostic only and ignores it for settlement (generic_host.py:10288-10357). I found no new size limit or denial of service.

## F. Tests (tests/core/execution/test_network_policy_popen_class.py, 183 lines)

I ran the file in an isolated package copy with a fresh pytest (the repo's conftest needs jsonschema, which is not installed here). All 10 tests pass on 8625a463. Run against the 8e8e60b1 wrapper, `test_posix_socketpair_and_asyncio_are_untouched_under_the_guard` fails with `OSError: [Errno 95]` from `socket.socketpair`. So the new POSIX test does catch the previous defect.

Covered:
- the ordinary connect guard still denies a loopback connect, in `test_every_other_connect_is_still_refused` and `test_nested_and_concurrent_pairs_leave_no_state`
- the pair is recorded exactly once
- unsupported arguments raise `ValueError`
- a subclass of the guard is checked
- POSIX `socketpair()` gives an AF_UNIX pair, and `new_event_loop()` and `asyncio.run` work

Missing negative tests (not blocking):
1. A hostile peer on the ephemeral port, to show verification rejects it and closes the sockets. My race reproduction above covers this.
2. A cleanup test: after a failed pair, assert no fds leak, including when connect raises and when verification fails.
3. A connect from another thread while a pair is under construction (the existing tests only probe after).
4. The POSIX test asserts only `left.family`. It does not check the right end, the type or proto. It also has no test that explicit arguments such as `socketpair(AF_UNIX, SOCK_DGRAM)` pass through unchanged.
5. The Windows-path `ValueError` test covers only `AF_INET, SOCK_DGRAM`. There is none for AF_UNIX, flags or proto.
6. Popen: no tests for `subprocess.run`, `check_output` or `asyncio.create_subprocess_exec`, for the captured-class gap, or for restoring the originals.

`tests/test_windows_posix_guard.py` contains no `network_policy` or `socketpair` references, and `tests/test_windows_mechanics.py` is unchanged by the branch.

## Minimal fixes (none required for PASS)

- Close `server` and `client` if the verification calls raise (:214-217).
- Set `GuardedPopen.__module__ = "subprocess"`.
- Add the missing negative tests above.
- Separately, handle positional `shell` and `executable` in `check`.

Scratch artifacts are in /tmp/w217: the worktree `wt`, the module copies `base`, `new` and `old`, and the `out_*.txt` run outputs.
