# Astrid Release 13 (0.0.13)

**Required update.** It fixes problems that could keep a rented machine billing after a job, or lose a finished result. Existing installs on Release 12 or earlier are asked to update: the App shows a one-line "Update Astrid · Required" notice that expands to the reason and the update command.

## What's new

- **One generation path, local or on a rented GPU.** You can generate images (text-to-image, edit), audio (speech, sound effects, music) and h3 video (video-to-video, video edit, image-to-video). They run with your own ComfyUI or on a RunPod machine you rent and control. Every type was proven live on real GPUs.
- **Failures explain themselves.** A failed job returns a receipt that names the stage and the cause, collected before the machine is released, so you don't need SSH to find out what went wrong.
- **Safer machine lifetime.**
  - Releasing a machine no longer reports success while the pod is still running.
  - A failed preparation no longer kills a warm engine; only that job fails.
  - Finished outputs are written atomically, so a result can't be half-written or lost.
- **Faster warm jobs.** The full model re-hash on every job is off by default; full verification is opt-in.
- **h3 masked edits.** Temporal, start-frame, regional and strength masks are admitted and documented, with worked examples.
- **Local-first onboarding.** You can get to a first image without renting anything.
- **Windows.**
  - A fresh install works as a normal user.
  - Generation with your own ComfyUI works whether or not Windows long paths are enabled.
  - A missing ComfyUI node pack is reported with the exact install commands.
  - Updating from Release 12 is tested end to end.
- **Updates from older releases.** Updating from Releases 0, 9, 11 and 12 is tested on Linux and macOS, and from Release 12 on Windows.

## Known limits

- **Managed local engine:**
  - It refuses templates whose models have no fingerprint. The fix is the first item for 13.1.
  - It isn't offered on Windows.
- **RunPod:**
  - A warm job carries about 215 s of overhead per image. Speed work is planned for Release 14.
  - The engine snapshot on the network volume (P6) is wired up but doesn't save time yet.
- **h3 image-to-video** from a single image uses the reference route, as in Release 12. First-frame image-to-video was reverted.
- **The seed used** is reported only by `astrid generate --json`, not by `tasks show` or the stored receipt.
- **Cancelling an attached job** uses ComfyUI's global interrupt, so it can also stop another client's job on the same ComfyUI.
- **On macOS, an update or uninstall can rarely fail** with "Astrid couldn't finish". Nothing is lost and running it again works. The cause is a shutdown race that is also present in Release 12 (astrid-dev #685).
- **Untested paths:** CI doesn't yet generate against a real ComfyUI, and macOS with your own ComfyUI and RunPod from Windows haven't had real runs.

## Components

| Component | Commit |
|---|---|
| Agent | `9814193a73f606719e81883a8be197d27dd361d4` |
| Runtime | `6855dfa8df65cf8ae4c002b57134d6505493c17c` |
| VibeComfy | `dba38f8644c46f652376f2cd5112ea161e40f09b` |
| runpod-lifecycle | `7f0b025e9391baac9f5c2fb7393617ea6fef0704` (0.3.1.dev0) |
| App | PR #268 merge commit (manifest sha256 `29dc13cf…`) |
