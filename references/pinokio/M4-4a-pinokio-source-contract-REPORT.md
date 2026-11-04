# M4-4a Pinokio source-contract report

## Result

Exit-0 research deliverable: `PINOKIO-ENGINE-CONTRACT.md` records the
source-backed internal request/event boundary and a clearly labelled proposed
B/Q wrapper seam. It does not claim a product command exists, a daemon is
running, an app/action executed, or any acceptance/release result.

## Retrieval and custody

- Client ref recorded in `work/ORCHESTRATOR.md`: `5be43718701c448b43daf0ce51d8935f170065bb`.
- Daemon ref recorded in `work/ORCHESTRATOR.md`: `add4a674ad1ba95bb62ec427fce519fe5bf0e9bf`.
- The client commit is addressable at the canonical upstream repository
  `pinokiocomputer/pterm`; the root/task label says `pinokiopterm`. The exact
  SHA and four requested files match there. The daemon is
  `pinokiocomputer/pinokiod` at the exact requested SHA.
- Retrieval method: six `curl --fail --silent --show-error --location` reads
  from exact commit-addressed `raw.githubusercontent.com` URLs; no branch,
  tag, clone, install, daemon, Pinokio launch, action invocation, or update/
  stop action was performed.
- Source manifest: pterm `endpoint.js` (`https://github.com/pinokiocomputer/pterm/blob/5be43718701c448b43daf0ce51d8935f170065bb/endpoint.js`, SHA-256 `7f9020f0bfcb07ae52d541f1c1ef074f17b8f56b1f9922efe99d9306ffb85db5`), `rpc.js` (`https://github.com/pinokiocomputer/pterm/blob/5be43718701c448b43daf0ce51d8935f170065bb/rpc.js`, `27e1eda8e6755248deb9ce5816bac082029b7e3dd793632633b0db5dcb5a5a3e`), `script.js` (`https://github.com/pinokiocomputer/pterm/blob/5be43718701c448b43daf0ce51d8935f170065bb/script.js`, `0fc5f343aebb7419241974857cf63a15871bb26b08cca9d1817c99508b373b32`), `target.js` (`https://github.com/pinokiocomputer/pterm/blob/5be43718701c448b43daf0ce51d8935f170065bb/target.js`, `2afa27f8bd26ea39d9ffecabca00c34e98c8bf1aae125db4640372984720bb0e`); pinokiod `server/socket.js` (`https://github.com/pinokiocomputer/pinokiod/blob/add4a674ad1ba95bb62ec427fce519fe5bf0e9bf/server/socket.js`, `d40871a7e50ae9dae1f920d860de5b64b5e9b5d064d88556b79d27c29a07bbc6`) and `kernel/api/index.js` (`https://github.com/pinokiocomputer/pinokiod/blob/add4a674ad1ba95bb62ec427fce519fe5bf0e9bf/kernel/api/index.js`, `acdd39ce8c058d42e7555b029c8798aa3173062e33c3249773a25b239dfc58a7`).
- Downloaded source is confined to this task folder under
  `evidence/src/{pterm,pinokiod}`. No files outside this task folder were
  removed or modified.
- Local evidence hashes and exact source URLs/line ranges are in
  `PINOKIO-ENGINE-CONTRACT.md`.

## Findings

- `pterm` resolves a control plane and app/ref target, then sends WebSocket JSON
  requests. The source-backed URI request schema and app/script resolution are
  documented with exact lines in contract sections 1–2.
- `pinokiod` routes URI requests and method requests to `kernel.api.process`.
  The socket calls `process(...).catch(...)` without awaiting a terminal result.
- The daemon emits queue/info, start/stream/result, error/control, stop, and
  disconnect events along the internal listener path. Queue admission is not
  action settlement.
- `kernel.api.stop` performs engine-owned tracked cleanup and emits disconnect,
  but the six files do not define B/Q ownership, busy/unknown refusal semantics,
  immutable action hashing, or a general task readback API.
- pterm exits code 0 on both `stop` and `disconnect`; its stop helper also ends
  on any callback packet or an 800 ms timer. The contract therefore classifies a
  disconnect/timeout without prior terminal evidence as unknown, never success.

## Limitations / precise NEEDS

The source can establish only the internal boundary at these pinned commits. It
cannot establish the deployed version, installed app identity, immutable
`pinokio/update.js` or `pinokio/stop.js` bytes, real execution, busy/unknown
refusal, timeout recovery, or owned cleanup postconditions. Those are listed as
explicit owner inputs in contract section 8. No upstream command is claimed;
the proposed wrapper is labelled derived and requires owner implementation and
independent postcondition evidence.

## Preservation and scope

The failed-but-safe sibling report
`../M4-4a-pinokio-engine-stop-controls/REPORT.md` was read for preservation
checking and left unchanged. No Pinokio, Agent, Runtime, App, Q adapter,
contract, workflow, or central checkout was changed. No tests, daemon, install,
hosted run, acceptance, or release claim was made. The host supervisor owns
`last.txt` and `exit`.
