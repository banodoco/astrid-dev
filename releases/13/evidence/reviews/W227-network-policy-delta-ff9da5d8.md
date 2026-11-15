# W227 review: network_policy.py `_program_name` delta, agent ff9da5d8021cbdd8180054c98aedb459bc79d9d7

VERDICT: PASS

Diff reviewed: `git diff 8625a463 ff9da5d8 -- astrid/core/execution/network_policy.py` and the +23-line test addition. I used a detached worktree at /tmp/w227/wt (now removed) and module copies in /tmp/w227 (`base_np.py` = 401dbd78, `mid_np.py` = 8625a463, `new_np.py` = ff9da5d8). Everything ran with `python3 -I` on loopback only. Nothing tracked was edited, nothing was pushed or dispatched. The fetched ref resolved to exactly ff9da5d8021cbdd8180054c98aedb459bc79d9d7.

| Check | Verdict |
|---|---|
| A. POSIX behaviour of `_program_name` | WIDENS, minor, and only inside the pre-existing name-only trust. Not blocking. |
| B. Windows semantics | SAFE (fails closed on every odd form). Pre-existing gaps listed. |
| C. Side-by-side regression run | IDENTICAL, no BLOCK |
| D. Tests | SAFE for the positive path. Negative tests are thin; list below. |

The only runtime change is `_program_name` (network_policy.py:291-299), used at :319 (`_local_media_tool`) and :341 (`_local_identity_tool`). `_local_process_probe` still uses `Path(tokens[0]).name.lower()` (:367, unchanged). The rest of the diff is typing only (`MutableMapping`, `socket.AddressFamily`). `check()` (:378-383) and `GuardedPopen` (:403-405) are byte-identical to 8625a463.

## A. `_program_name` versus `Path(token).name.lower()` on POSIX: WIDENS (minor)

Method: `diffA.py` ran both functions over about 70 hand-picked tokens, and `fuzz.py` ran an exhaustive concatenation of 14 fragments up to length 4 (82,740 command lists, media and git forms). I compared the allow decision of 8625a463 and ff9da5d8.

Result of the exhaustive run: 1365 inputs newly allowed, 115 newly denied, 81260 unchanged. Every newly allowed input contains a backslash or ends in `.exe` (case-insensitive). The script printed no other kind of widening. Every newly denied input ends in a trailing `/` or `/.` form.

Difference table (name returned by old / new, then effect on the allow decision):

| Input | Old name | New name | Effect |
|---|---|---|---|
| `ffprobe.exe`, `FFPROBE.EXE`, `/tmp/x/ffprobe.exe`, `PosixPath('ffprobe.exe')` | `ffprobe.exe` | `ffprobe` | widens (allowed now) |
| `ffmpeg.exe`, `git.exe`, `GIT.EXE` | `*.exe` | `ffmpeg` / `git` | widens |
| `x\ffprobe`, `..\ffprobe`, `\ffprobe`, `/tmp/a/b\ffprobe` | whole token or `b\ffprobe` | `ffprobe` | widens |
| `x\git` | `x\git` | `git` | widens |
| `C:\Tools\ffprobe.exe`, `C:/Tools/ffprobe.exe` | `...ffprobe.exe` | `ffprobe` | widens |
| `/tmp/x\ffprobe.exe` | `x\ffprobe.exe` | `ffprobe` | widens |
| `ffprobe/`, `ffprobe//`, `ffprobe/.`, `./ffprobe/.`, `git/`, `git/.` | `ffprobe` / `git` | `` or `.` | narrows (was allowed, now denied) |
| `/tmp/ffprobe\x` | `ffprobe\x` | `x` | both deny |
| `ffprobe.exe.exe` | `ffprobe.exe.exe` | `ffprobe.exe` | both deny (strips once) |
| `ffprobe.exe.bat`, `ffprobe.com`, `ffprobe.`, `ffprobe `, `ffprobe.exe.`, `ffprobe.exe:evil`, `ffprobe\t` | unchanged | unchanged | both deny |
| `ffprobe.exe/` , `.exe`, `/.exe`, `` (empty), `.`, `..`, `/` | various | `` / `.` / `..` | both deny |
| `ffprobe` case variants (`FFPROBE`) | `ffprobe` | `ffprobe` | same, allowed |
| `None`, `0`, `b'ffprobe'`, `['ffprobe']` | `TypeError` | `none`, `0`, `b'ffprobe'`, `['ffprobe']` | both deny. The old helper raised, but the callers pass `str(value)` tokens, so no input reaches it as a non-str. Note `b'ffprobe'` is `"b'ffprobe'"` after `str()`, denied in both. |

Real execution on POSIX (`runA.py`, deny-all policy installed with the real `install()`; scripts named as below in /tmp/w227/play print their own name):

- 8625a463: `./ffprobe` RAN; `./ffprobe.exe`, `./x\ffprobe`, `./..\ffprobe`, `./git.exe` DENIED.
- ff9da5d8: `./ffprobe` RAN (same as before); `./ffprobe.exe` RAN; `./x\ffprobe` RAN (a file whose real name contains a backslash); `./..\ffprobe` RAN; `./git.exe rev-parse HEAD` RAN. Still DENIED: `./ffprobe.exe.bat`, any media command with `https://` or `tcp://` in an argument, `./git.exe -c core.sshCommand=x rev-parse HEAD`, `./git.exe fetch`.
- A symlink `sub/ffprobe -> /bin/echo` RAN under both versions: the pre-existing name-only trust.
- `Popen("./ffprobe.exe -v error clip.mp4")` (string, no shell) fails with `FileNotFoundError`, because Popen executes the whole string as one program name. This is a denial by the OS, not by the policy, so it is no widening.

Answer to the question: yes. On POSIX, a provider-controlled file whose real name ends in `.exe` or contains a backslash before an `ffprobe`/`ffmpeg`/`git` component now passes `_local_media_tool` / `_local_identity_tool` and executes as a native child. It is a strict superset of what passed before. Old inputs that only differed by a trailing `/` or `/.` (nonsense forms for an executable) are now denied.

Separated from the pre-existing property: at 401dbd78 and 8625a463, any path whose last component is `ffprobe`, `ffmpeg` or `git` is already allowed by NAME only (`./ffprobe`, `/tmp/x/ffprobe`, a symlink, a bare name resolved through PATH). A party who can place a file with an arbitrary name in a directory the provider can name already had a trivial route: create a file called `ffprobe`. The delta adds no new capability in that situation: the same file, with the same contents, could have been named `ffprobe`. It only enlarges the set of acceptable names. It would matter only for a party who is constrained to produce a name ending in `.exe` or containing a backslash (for example a name taken from an archive entry or a remote filename), and who cannot also produce a plain `ffprobe`. That is a corner case, so I rate it minor.

Argument checks still bind identically. Only `tokens[0]` goes through the new helper. `network_prefixes` and the `"://" in token.lower()` test (:322-326) still scan `tokens[1:]`. The git branch still rejects `-c`, any `--config*`, and everything outside the four exact subcommand tuples, after the optional `-C <dir>` removal. I ran `./x\ffprobe -i tcp://127.0.0.1:1` (DENIED), `./ffprobe.exe https://example.com/x.mp4` (DENIED), `git.exe -c ...` and `git.exe fetch` (both DENIED). The check against `shell` and `executable` is unchanged (see B).

Minimal hardening (optional, not blocking): apply the backslash and `.exe` normalisation only when `os.name == "nt"`, so POSIX keeps the exact previous name rules:

```python
def _program_name(token):
    name = str(token)
    if os.name == "nt":
        name = name.replace("\\", "/")
    name = name.rsplit("/", 1)[-1].lower()
    return name[:-4] if os.name == "nt" and name.endswith(".exe") else name
```

The tests that pass `C:\...\ffprobe.exe` would then need to be marked Windows-only or monkeypatch `os.name`.

## B. Windows semantics (reasoned from code, not run natively)

`_program_name` splits on both separators (`\` is folded to `/`), lowercases, and strips one trailing `.exe`.

| Input | Name | Allowed as media / git tool? | What Windows resolves |
|---|---|---|---|
| `C:\Tools\ffprobe.exe` | `ffprobe` | yes | that exact file |
| `ffprobe.EXE`, `FFPROBE.exe` | `ffprobe` | yes | same NTFS file (case-insensitive) |
| `git.exe` | `git` | yes (subject to the subcommand tuples) | same file as bare `git`, since CreateProcess appends `.exe` to an extension-less name |
| `C:\x\git.exe.bat` | `git.exe.bat` | no | would run cmd.exe, but never reaches it |
| `ffprobe.exe.exe` | `ffprobe.exe` | no (strips only once) | |
| 8.3 short name `FFPROB~1.EXE` | `ffprob~1` | no | fails closed, whatever it resolves to |
| `ffprobe.exe:evil` (alternate data stream) | `ffprobe.exe:evil` | no | |
| `ffprobe.exe.`, `ffprobe.exe ` (trailing dot or space) | unchanged | no | Windows would strip them and run `ffprobe.exe`, but the policy denies, so this is fail-closed |
| `C:ffprobe.exe` (drive-relative) | `c:ffprobe` | no | The old helper on Windows would have returned `ffprobe.exe` or `ffprobe`; now denied (narrower) |
| UNC `\\srv\share\ffprobe.exe` | `ffprobe` | yes | runs a binary over SMB |

Does the OS resolve any allowed form to a different binary than the named tool? For local names, no: `ffprobe` and `ffprobe.exe` resolve to the same file, because CreateProcess appends `.exe` to a name without an extension. So on Windows the delta is equivalence-preserving. It makes the rule match the real file name, which the old rule could not (the old rule only matched an extension-less `ffprobe`, which is not what a resolved Windows path looks like).

Pre-existing gaps that remain, none widened beyond what the old extension-less spelling already allowed:
1. UNC and remote paths: `\\srv\share\ffprobe` (old, no extension) resolved to `\\srv\share\ffprobe.exe` and was already allowed. The new rule adds the `.exe` spelling only. That is a name-only trust problem (a network-hosted binary), not caused by this delta.
2. String commands are split on whitespace (:313). A path with spaces and no quotes could be resolved by CreateProcess's "try each prefix" rule to a different file than the first token. Provider code normally passes lists; this is unchanged.
3. A token containing embedded quotes (`evil.exe" "\ffprobe`) is judged by its last separator component, while CreateProcess parses the quoted first token differently. I could not confirm an exploitable form; it is the same class as before and the old extension-less spelling had it too. Optional hardening: deny tokens that contain `"` or whitespace in `tokens[0]` for list commands.

Is the allow decision still made on what Popen executes? `check()` at :378-383 is unchanged. It reads `command = args[0] if args else kwargs.get("args", "")`, and it takes `shell` and `executable` from `kwargs` only. I re-ran `pos.py` and `pos2.py`: `Popen("ffprobe -x ; echo POSITIONAL_SHELL_BYPASS", -1, None, None, None, None, None, True, True)` and `Popen([...], -1, "/bin/echo")` print the bypass marker on 401dbd78, 8625a463 and ff9da5d8 alike. The positional form is thus a pre-existing gap, not widened. With the new `.exe` spelling the same bypass is reachable with `ffprobe.exe` as the prefix, but the bare `ffprobe` prefix already reached it, so nothing new is reachable. Keyword `shell=True` and keyword `executable=` stay DENIED. A separate fix should read the positional arguments through `inspect.signature` (carried over from W217).

## C. Side-by-side regression run: IDENTICAL

Harness: `runG.py` (same calls as the W217 check G, plus `create_subprocess_exec`), policy installed with the real `install()`, four interpreters: plain, base 401dbd78, mid 8625a463, new ff9da5d8, in deny-all mode and in `allowed_destinations=["127.0.0.1"]` mode. Stderr was empty in all eight runs.

Outputs in the new run (deny-all):
```
socketpair()                                    [AF_UNIX,STREAM,0] x2
socketpair(AF_UNIX)                             [AF_UNIX,STREAM,0] x2
socketpair(AF_UNIX, SOCK_DGRAM)                 [AF_UNIX,DGRAM,0] x2
socketpair(AF_UNIX, STREAM|NONBLOCK|CLOEXEC)    [AF_UNIX,STREAM,0] x2
socketpair(AF_INET)                             OSError 95
socketpair(family=,type=,proto=)                [AF_UNIX,STREAM,0] x2
new_event_loop/run_until_complete/close         ok
asyncio.run(co)                                 42
asyncio.run + run_in_executor                   7
asyncio.create_subprocess_exec(/bin/true)       NetworkPolicyError (native descendant denied)
create_connection(192.0.2.1:9)                  NetworkPolicyError (denied tcp destination)
loopback connect (outside pair)                 NetworkPolicyError (denied tcp ...:PORT)
loopback connect_ex                             NetworkPolicyError (denied tcp ...:PORT)
socketpair x50 then loop                        ok
```
Diffs, after port normalisation:
- new versus mid (8625a463): no difference in either mode (the socket code did not change at runtime).
- new versus base (401dbd78): the only line is `socketpair.__module__` (`socket` versus the policy module), the expected wrapper identity.
- new versus plain: the first nine lines are identical (the socketpair and asyncio rows). The remaining differences are only policy denials: `create_subprocess_exec`, the non-loopback `create_connection`, and the loopback connect and `connect_ex` outside a pair (all allowed in the plain interpreter, denied by the policy). In loopback-allowed mode the loopback rows are also identical to plain.

No behavioural difference from the plain interpreter beyond the policy denials, so there is no BLOCK from C.

## D. Tests: SAFE for the positive path; negative coverage is thin

The pytest module is not installed here, so I replayed the new assertions by hand in `tests_emul.py`. On ff9da5d8 every assertion holds. On 8625a463 the positive cases fail (`ffprobe.exe`, `FFPROBE.EXE`, `...\ffprobe.exe`, `ffmpeg.exe`, and the git case: `False` versus `True`). So the positive tests do pin the new `.exe` and path behaviour.

Pinned now: `ffprobe`, `ffprobe.exe`, `FFPROBE.EXE`, `/usr/bin/ffprobe`, `C:\Program Files\ffmpeg\bin\ffprobe.exe`, `ffmpeg.exe` allowed; `ffprobe.exe.bat`, `notffprobe.exe`, `ffprobe.com`, `curl.exe` denied; `ffprobe.exe` with an `https://` argument denied; `git.exe` path equals `git` for `rev-parse HEAD`.

Missing negative tests (none blocking):
1. `ffprobe.exe.exe` (one strip only), `git.exe.bat`, `ffprobe.exe:evil`, `ffprobe.exe.` and `ffprobe.exe ` (trailing dot or space), `ffprobe.` and the 8.3 form `FFPROB~1.EXE`.
2. `.exe` alone, empty string, `/`, `ffprobe/`, `ffprobe/.` (the now-narrower forms), and a non-str element.
3. A backslash POSIX file name (`x\ffprobe`) pinned either way. The delta makes it allowed, so a test should record that as intended, or the helper should be made Windows-only.
4. The git test asserts `_local_identity_tool(windows) == _local_identity_tool(command)`. That passes if both are False. Assert `is True`, and add `git.exe fetch`, `git.exe -c x=y rev-parse HEAD` and `git.exe -C dir status --porcelain --untracked-files=all` negatives and positive.
5. `ffmpeg.exe` with `rtmp://`, `tcp:` and `udp:` arguments (only `https://` is exercised).
6. A Popen-level test through `check()` that an executable called `ffprobe.exe` is allowed and recorded as `local-media-tool:`, and that `shell=True` or `executable=` with `ffprobe.exe` stays denied.
7. A UNC path (`\\srv\share\ffprobe.exe`) pinned as allowed or denied, so a later change in that decision is deliberate.

## Recommended changes

None required for PASS. Optional, in order of value: (1) make the backslash and `.exe` normalisation Windows-only so POSIX behaviour is exactly unchanged; (2) add the negative tests above; (3) separately, read positional `shell` and `executable` in `check()`; (4) consider denying UNC and quote-bearing `tokens[0]`.

Scratch artifacts: /tmp/w227 (`diffA.py`, `fuzz.py`, `runA.py`, `runG.py`, `pos.py`, `tests_emul.py`, `out_*.txt`, module copies).
