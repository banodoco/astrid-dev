# Frozen second-freeze installed measurement — 23 November 2026

The independent reviewer ran the committed three-arm driver on the frozen heads. It exited 0 with 54 command records: nine warmups and five measured commands per arm in each of three groups (45 measured). Each command's recorded one-minute load at admission was 0.4536–0.9995 on the shared four-vCPU box. Arm order was fixed. Generation timings were enabled for the candidate arms and not the published arm, so their instrumentation overhead differs.

| Arm | Agent | Runtime | VibeComfy |
|---|---|---|---|
| before | `c0ad6b54aadd21630d98bb5039613e37efe92a8f` | `5120462d67479dc4719406d0d34440edb616ace1` | `48b5fa9e45630e1bc502651975ec0ef3a5e74c4c` |
| after | `705298cd7da2ba9c7378998b4fe5c0ee28438f81` (local pin-bump on `b5c30e616e788308e9b6152adbc7064f2000db47`) | `72b129e5a2296dc58360a9896cc65fab9db4ad0c` | `950023c8846233f0006aac100d26b76711c42515` |
| vc48 | `b5c30e616e788308e9b6152adbc7064f2000db47` | `72b129e5a2296dc58360a9896cc65fab9db4ad0c` | `48b5fa9e45630e1bc502651975ec0ef3a5e74c4c` |

All arms used npm `@oh-my-pi/pi-coding-agent@18.12.6`. This was a CPU container with a loopback stand-in ComfyUI and `--no-wait`; generation wall time ends at task admission. It does not cover a real ComfyUI node-info answer or GPU execution. Attestation was **off**. The reviewer's independent reads of each installation's `current` pointer and selected manifest are in `identity.json`; they identify the configured pins, not byte-level source attestation or proof of the socket used by each command.

| Group | Before median | After median | vc48 median | After / before | vc48 / before |
|---|---:|---:|---:|---:|---:|
| Same-prompt generate | 14.682 s | 5.662 s | 10.780 s | 0.386 | 0.734 |
| Changed-prompt generate | 15.177 s | 6.108 s | 11.057 s | 0.402 | 0.729 |
| Timeline edit | 1.159 s | 1.125 s | 1.090 s | 0.971 | 0.940 |

The vc48 arm is the Release 15 landing candidate: its generation medians are approximately 27% lower than before in this setting. The after arm additionally includes PR #182's memo, which is held for later repair. The candidate Agent commits differ in generated pin files, so the arm difference is descriptive and does not by itself establish a causal share. Earlier `ab-run-*` tables are historical and measure their recorded earlier tuples.

`summary-ab.json`, `records.jsonl`, and `console.log` are copied unchanged from the reviewer's `measured/` directory; `identity.json` and `sha256.txt` are copied unchanged from the reviewer's parent evidence directory. `records.jsonl` contains 54 command records and a completion marker. The supplied `sha256.txt` is the reviewer's broader inventory and refers to paths in the original review workspace. No measurement was rerun to create this record.
