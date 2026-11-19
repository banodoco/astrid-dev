# LS-12 split qualification checkpoint, 19 November at 17:07 UTC

The candidate is Agent [aacdcd86](https://github.com/banodoco/astrid-agent/commit/aacdcd86bfe09bcddac0f4d5941498c5126f74d8). Its destination and reference is [e3795656](https://github.com/banodoco/astrid-agent/commit/e379565641414bc183cd02edebab1cbf77617931).

**Darwin.** The two job logs report the same 55 primary pytest IDs. The only changed outcome was `tests/packs/test_audio_render.py::AudioRenderTest::test_rendered_mp4_contains_audio_stream`, which passed on the reference (log line 3624) and failed on the candidate (line 4145). The candidate traceback first surfaced a custody error in `astrid/core/execution/process_group.py:577` after the reconciliation budget expired at 1.356932s (lines 2187–2189). The renderer surfaced that error later. What prevented stabilization remains unknown. This is a different test from the historical ee0 persistent-capture timeout. [Reference job](https://github.com/banodoco/astrid-agent/actions/runs/44465854222/job/135363345893) · [Candidate job](https://github.com/banodoco/astrid-agent/actions/runs/44551401308/job/135655815146)

| CI job | Primary pass / fail / error | Pytest step exit | SHA-256 of original decoded job log |
| --- | --- | ---: | --- |
| Darwin reference | 42 / 12 / 1 | 1 | `5e4d5fc15a804d56d2b49c4f0c5432a4dc4c4652eac5e9bb16421965e700edde` |
| Darwin candidate | 41 / 13 / 1 | 1 | `b17c068710a64f6f355aed8b30e5907ba8d9e51b192093f000bf2b8a3d112365` |
| [Unit 5 reference](https://github.com/banodoco/astrid-agent/actions/runs/44465854222/job/135363346307) | 2,262 / 95 / 107 | 1 | `04c861c208f6136c3085d7ea3d44ba02bd7de3b8115f67d32259bd69bd15987e` |
| [Unit 5 candidate](https://github.com/banodoco/astrid-agent/actions/runs/44551401308/job/135655815415) | 2,263 / 95 / 107 | 1 | `c21a54e2a82b8aa12d5e8706ac64be483329e7b515439489b9b50bea7e341e46` |

Unit 5 had 2,463 common primary IDs and all had identical outcomes. One reference ID and two candidate IDs were outside the other side's shard 5. Full-suite coverage requires comparison across shards.

**Windows uninstrumented first job.** Both sides supplied 20 latency samples per caller and retained exit 0 for the latency and counter commands. The CLI median was 8.7806213s on e379 and 9.8669253s on aacd (+12.37%). The SDK median was 7.52306865s and 8.52851205s (+13.36%). Both changes are within the 15% same-OS tolerance. Both sides exceeded the absolute 5s budget. The separate Windows owned pack-verification phases and the macOS uninstrumented CLI still exceed their respective criteria. These ordinary meter counter runs do not supply the missing calibrated LS-2.1 controls. [Windows reference artifact](https://github.com/banodoco/astrid-agent/actions/runs/44548464348/artifacts/14554385969) · [Windows candidate artifact](https://github.com/banodoco/astrid-agent/actions/runs/44548464348/artifacts/14553196959) · [Owned phases and macOS proof](https://github.com/banodoco/astrid-agent/pull/361#issuecomment-7015881666)

The Linux reference reports CLI 6.75271198s and SDK 5.90438806s, with 20 samples per caller and command exits 0. The Linux candidate, CI and Lanes were still running at this checkpoint. [Linux reference artifact](https://github.com/banodoco/astrid-agent/actions/runs/44548464348/artifacts/14552914084) · [Linux candidate job](https://github.com/banodoco/astrid-agent/actions/runs/44548464348/job/135645371204)
