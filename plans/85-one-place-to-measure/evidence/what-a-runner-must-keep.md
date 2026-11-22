# What a general runner must keep

From the hosting session of Plan 81 (`session_011EzfW2Ut856AFGZS8ZamHU`), 22 November 2026, 16:56 UTC, answering the Release 15 Lead's question for this plan. Its own account of what made its installed before-and-after result trustworthy.

1. **A load gate that fails closed.** Each timed command starts only when the one-minute load is below 1.0: it polls, and then the run fails; it never runs ungated. Load is recorded before and after every command, with a 30-second sampler. A run that missed the gate is working evidence only.
2. **Arms alternated in one session:** before, after and any variant in each round, one warm-up and five measured runs per arm, medians, and ratios against "before". Numbers from different sessions are never compared.
3. **A shared timing lock** held only during the timed command, not during setup or inventories, so several managers can interleave and a test inventory never starves a measurement.
4. **A stand-in ComfyUI** that serves the real node schemas for the default model, so the command reaches "task queued" with `--no-wait`; and the setting stated every time: installed build, CPU container, stand-in ComfyUI, shared machine. Not covered: a real ComfyUI's node-information answer, and GPU work.
5. **Isolated installs per arm:** its own home and configuration directories, program and data roots and door port, from the official installer, with the tuple recorded (installer, manifests, commits) and the installer's own pin-match check as the guard against a wrong arm.
6. **An untimed check first** (the version, the help flags, one untimed command per arm), then the timed run. The driver writes one record per command, flushed, and its own summary. A summary rebuilt by hand is labelled working evidence.
7. **Counts first.** Wall seconds on a shared machine are noisy, so they are paired with counts and stage timings. Where only the "after" arm can report stages, the asymmetry is stated.
8. **The reviewer re-runs it once** in a fresh, quiet session.

Still only on that session's machine at the time of writing, to be committed in its next evidence pull request: the timing wrapper (`timed-astrid.py`), the summary's test and recovery scripts, every manifest with its checksum, a short note on pinning a tuple for an "after" arm, the raw outputs behind both tables, the hashing probes and the attribution harness. The live installs (about 1.3 GB each) are not committed; the script reproduces them.
