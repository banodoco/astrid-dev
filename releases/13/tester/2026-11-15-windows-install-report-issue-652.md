# Astrid Release 13: Windows install report (issue #652, "Iridium Storm")

**Date:** 2026-11-15 · **Agent:** Claude Code (Claude Opus 5.5), driving PowerShell scripts · **Scope:** part 2 of `windows-tester-brief.md` only (install + build check + `doctor`).

> Written for a developer working on Linux, and for their coding agent. Every failure below comes with the exact error, the root cause, a way to reproduce it on Windows, and a suggested fix. The details that matter are Windows behaviours that never show up on Linux: `MAX_PATH`, how the certificate store fills, private DACLs, and Git not being present.

---

## 1. TL;DR

| | |
|---|---|
| Result | **Installed.** `Astrid installed: Release 13.` `doctor --json` → `healthy: true`, Runtime `running`, client/runtime schema compatible. |
| Build check | One line, exactly `9acb55b60e167ac53d0ad04350a66b792f44348f` ✅ |
| Attempts needed | 5. The 1st and 2nd failures were caused by the environment; the 3rd, 4th and 5th are **Astrid bugs on Windows**. |
| Blocking bugs found | **(B1)** paths over 260 chars in the agent archive · **(B2)** paths over 260 chars in the VibeComfy archive, even from a 4-char root · **(B3)** Git is required but not provided or documented |
| Other findings | (F1) on a fresh Windows, Python `urllib` fails TLS where `uv` succeeds · (F2) misleading failure text · (F3) the brief's "published release" was still Release 12 · (F4) the private-DACL check rejects redirected or mapped folders with a vague message |
| Not tested | Parts 3–5 (no GPU, no ComfyUI in this environment). Nothing was generated. |
| Host impact | None: the install ran inside a disposable Windows Sandbox. Autostart, command and skills were **off**. |

---

## 2. Environment

- **OS:** Windows 10 Pro 22H2, build 19045, x64. Windows PowerShell 5.1.19041.
- **Isolation:** Windows Sandbox (a fresh, disposable VM; local account `WDAGUtilityAccount`). Networking on, **vGPU off**. On Windows 10 the Sandbox vGPU does not expose CUDA (`nvcuda.dll` is absent and `nvidia-smi` cannot load NVML), so a GPU run is not possible there.
- **Pre-installed in the Sandbox:** nothing beyond stock Windows. **No Git, no Python, no Node.**
- **Brief deviations, all deliberate and on the tester's instructions:**
  - Flags `--autostart off --command off --skills off --skill-copies off`, without `--yes`. Explicit choices skip the prompt and the consent stop.
  - The bootstrap was run **from a local, pre-reviewed copy** of `install.ps1` (sha256 `EA581D5D7C2D02F9F062DC15AFFABE1F7C3E38D641984CECF4797F13AC58B3A9`), with `--manifest <local copy of the issue's MANIFEST_URL>`, instead of `irm | iex`.
  - Nothing was posted to GitHub by the agent, and no session export is attached.

---

## 3. Timeline

| # | `LOCALAPPDATA` | Result | Error (verbatim) | Cause |
|---|---|---|---|---|
| 1 | folder mapped from the host into the Sandbox | failed in 3 s | `Astrid directories require a protected owner/SYSTEM DACL.` | Environment (see F4) |
| 2 | Sandbox default `C:\Users\WDAGUtilityAccount\AppData\Local` | failed in 48 s | `urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1016)>` | Environment, fresh root store (see F1) |
| 3 | same | failed in 25 s | `FileNotFoundError: [Errno 2] No such file or directory: 'C:\\Users\\WDAGUtilityAccount\\AppData\\Local\\Astrid\\versions\\9acb55b6-6855dfa8-942799de\\a.unpack\\astrid-agent-9acb55b6…\\remotion\\artifacts\\banodoco-timeline-compos…'` | **B1** |
| 4 | `C:\A` (to shorten paths) | failed in 68 s | `FileNotFoundError: … 'C:\\A\\Astrid\\versions\\9acb55b6-6855dfa8-a31efc15\\v.unpack\\VibeComfy-dba38f86…\\docs\\handover\\unified-workflow-integrity-20260909\\evidence\\workflow-review-set-2026…'` | **B2** |
| 4b | `C:\A` + `LongPathsEnabled=1` (Sandbox only) | failed in 42 s | `Source staging operations require Git on PATH or a valid recorded Git executable.` (summary: `Failure: ValueError`) | **B3** |
| 5 | `C:\A` + LongPaths + MinGit 2.56.1 on `PATH` | **success in 360 s** | — | — |

Successful run, final summary (verbatim):
```
Startup: running and ready.
Sign-in autostart: not registered.
Command/PATH: off; no owned command/PATH changes were needed.
Skill destinations: no target changes were reported.
Astrid installed: Release 13.
```
`doctor --json` (excerpt): `"healthy": true`, `"catalog_present": true`, `"discovery_present": true`, `runtimeClientCompatibility.compatible: true` (`workspace.v1`, schema `sha256:9628bb5f…`), `executor_skips.count: 0`, `packQuarantine.count: 0`.

---

## 4. Blocking bugs

### B1: `MAX_PATH` overflow when extracting the agent archive

- **Where:** `astrid/installer/tools.py` → `source()` (l.383) → `fetch_archive()` (l.221–222) → `extract()` (l.203, `target.open("wb")`). Called from `backend.py` `stage()` l.1338 (agent).
- **Why:** the longest entry in `astrid-agent@9acb55b6` is **178 chars**:
  `astrid-agent-9acb55b60e167ac53d0ad04350a66b792f44348f/remotion/artifacts/banodoco-timeline-composition-a5908fac2b43c5d7b17a45cd4687d7caccf1806451e1f081aee3e912fe64ca89.tgz.sha256`
  The staging prefix `%LOCALAPPDATA%\Astrid\versions\<agent8>-<runtime8>-<id8>\a.unpack\` comes to `76 + len(username)` chars with the default `C:\Users\<username>\AppData\Local`.
  **Total = 254 + len(username).** Without long-path support Windows allows at most 259, so **any Windows user whose name has more than 5 characters fails.** Most users will hit this.
- **Why it is invisible on Linux:** `PATH_MAX` there is 4096.
- **Reproduce:** a fresh Windows 10/11, a user name of 6 or more characters, `LongPathsEnabled=0` (the default), run the installer.
- **Suggested fixes (any of these):**
  1. In `extract()`, open targets through extended-length paths: `"\\\\?\\" + str(target.resolve())` on Windows.
  2. Drop the archive's top folder (`astrid-agent-<40 hex>/`, 53 chars) when unpacking, and shorten `a.unpack`.
  3. Don't ship the 64-hex digest inside the file name under `remotion/artifacts/`.
  4. Add a preflight that computes the longest destination path from the tar index and fails early with a clear message.

### B2: `MAX_PATH` overflow in the VibeComfy archive, even from a 4-char root

- **Where:** `backend.py` `stage()` l.1350 (`source("vibecomfy", …, folder / "v", …)`), then the same `extract()` path.
- **Why:** entries under `VibeComfy-dba38f8644c46f652376f2cd5112ea161e40f09b/docs/handover/unified-workflow-integrity-20260909/evidence/workflow-review-set-…` pass 260 even with `LOCALAPPDATA=C:\A`. **No user-side workaround exists without admin.**
- **Workaround used:** `HKLM\SYSTEM\CurrentControlSet\Control\FileSystem\LongPathsEnabled=1` (Python 3.11 is long-path aware). This **needs admin**, which contradicts the brief's "No admin rights are needed".
- **Suggested fixes:** the `\\?\` approach from B1; or exclude `docs/` (and other non-runtime folders) from the VibeComfy archive or extraction; or install VibeComfy from a wheel or sdist instead of a repo tarball.

### B3: Git is required, but neither provided nor documented

- **Message:** `Source staging operations require Git on PATH or a valid recorded Git executable.` → `Failure: ValueError`.
- **Context:** the manifest pins `uv`, `python`, `bun`, `node` and `ffmpeg` with Windows assets and sha256, but **not Git**. `windows-tester-brief.md` ("You need: …") and the setup skill don't list Git as a prerequisite. The check runs **after** about 70 s of downloads and staging.
- **Workaround used:** official **MinGit 2.56.1 64-bit** (sha256 `4a92850b6e917da4fd010669b614b55dccf5b0ec333a534cc4be4700dfefdafd`, signed by Johannes Schindelin), with its `cmd\` folder added to `PATH` for the installer process only, plus `git config --global core.longpaths true`.
- **Suggested fixes:** add a pinned `tools.git` (MinGit zip + sha256) to the manifest, like node/bun/ffmpeg. At minimum, check for Git in the bootstrap preflight and document it.

---

## 5. Other findings

### F1: on a fresh Windows, TLS fails in Python `urllib` but not in `uv`
- `uv` downloaded fine because it bundles its own roots. The Python downloader (`tools.py` `download()` l.162, `urllib.request.urlopen`) uses the Windows **ROOT store**, which Windows fills **lazily** (Automatic Root Certificates Update). On a fresh machine the root for `codeload.github.com` was not there yet.
- **Who it affects:** fresh installs, Windows Sandbox and VMs, and corporate machines where automatic root updates are disabled.
- **Workaround used:** one PowerShell `Invoke-WebRequest -Method Head` per host (github.com, codeload.github.com, nodejs.org, huggingface.co, pypi.org, astrid.haus, raw.githubusercontent.com). This makes CryptoAPI fetch the roots. **No verification was disabled.**
- **Suggested fix:** use [`truststore`](https://pypi.org/project/truststore/) (`truststore.inject_into_ssl()`). It verifies through the OS chain engine, which fetches missing roots. Alternatively, fall back to a `certifi` bundle on `SSLCertVerificationError`.

### F2: failure text can mislead
- The final message says `Details: shown above in this window (the installer log was not used).`, but `%LOCALAPPDATA%\Astrid Runtime\logs\install.log` **did** contain the full traceback.
- It also says `Next: open astrid.haus > Settings > Updates > Download diagnostics` after a **failed first install**, when the Runtime is not running and astrid.haus cannot connect.
- `Nothing was installed.` was printed while partial `Astrid\versions\<…>` folders from the failed attempt were still on disk. They were removed by a later run.

### F3: the brief and the published release disagree
- At test time (about 15:05 UTC), `https://astrid.haus/install-manifest.json` was **Release 12** (agent `0e1543e0da2215db9cb3320cfd1083174c3c62a9`).
- The brief says to install "the published release" and to *remove* `ASTRID_INSTALL_MANIFEST_URL`, but then requires agent `9acb55b6…`. Followed literally, the build check fails.
- The issue's `{{MANIFEST_URL}}` (Release 13, `astrid-dev@dd3ad1bf…/tester/install-manifest.json`) is **never referenced in the brief**. We used it through `--manifest`.

### F4: the private-DACL check gives no detail
- `Initialize-PrivateDirectory` in `install.ps1` (l.39–65) rejects any `LOCALAPPDATA` on a folder whose ACL the process cannot control (here, a Sandbox mapped folder; folder redirection or network profiles likely hit it too). That makes sense, but the message doesn't name the path or the reason.
- **Suggestion:** include the path, the observed owner/SDDL, and one line on supported locations.

---

## 6. Network seen during the successful run
Sampled every 10 s, so short connections may not appear: GitHub (archives and releases), astral.sh / python-build-standalone via `uv`, PyPI, and `bun` → Cloudflare-fronted npm registry (`104.16.x.34`). Also Windows certificate validation, and normal Windows background traffic. Nothing unexpected.

## 7. Not done / not tested
- Parts 3–6 (ComfyUI scan, model downloads, cells A–H, doctor bundle). The environment has no usable GPU and no ComfyUI.
- `--autostart on`, `--command on` and `--skills on` paths, `--update`, and `--uninstall`.

## 8. Checklist for your coding agent
1. `astrid/installer/tools.py` `extract()`: on Windows use `\\?\` absolute paths, or strip the top-level `<repo>-<sha>/` folder.
2. Shorten the staging dirs (`a.unpack`, `v.unpack`, the `versions/<8>-<8>-<8>` scheme), or stage under a short root.
3. Add a tar-index preflight: fail early if any destination path is 260 chars or more and `LongPathsEnabled` is 0.
4. Exclude non-runtime folders from the VibeComfy archive (at least `docs/handover/**`).
5. Manifest: add `tools.git` (MinGit, pinned and hashed) and use it in source staging. Otherwise preflight Git in `install.ps1` before any download.
6. TLS: `truststore.inject_into_ssl()` early in `python -m astrid install`.
7. Fix the F2 texts. Point to `install.log` when it exists.
8. Brief: reconcile "published release" with `{{AGENT_SHA}}`, use `{{MANIFEST_URL}}` explicitly, list Git, and say that long paths may need admin.
9. Test idea: a GitHub Actions `windows-latest` job running as a user with a long name and `LongPathsEnabled=0`, with Git removed from `PATH`, plus a Windows Sandbox `.wsb` smoke test.
