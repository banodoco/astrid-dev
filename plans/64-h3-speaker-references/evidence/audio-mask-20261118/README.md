# SR-5 pinned audio-mask CPU diagnostic — 2026-11-18

The diagnostic ran the actual pinned VideoHelperSuite loader, Comfy ImageToMask and CropMask methods, and the motion pack's `MiniMaxH3SetAVNoiseMask` on CPU PyTorch 2.10.0+cpu. It used import-only shims for unused UI/server dependencies and bypassed the motion pack's runtime compatibility precheck. No GPU or model inference ran.

- ComfyUI: `6bfaacc67c2103481e5f0c84d75257cd0581d86a`.
- VideoHelperSuite: `4ee72c065db22c9d96c2427954dc69e7b908444b`.
- H3 motion pack: `361624fb406b63eb6694442eac6c895fc1533a70`; `existing_video_extension.py` SHA-256 `787910aaf84e4b9a3dc9837ebc1cb47c7068b58098d9275b2771c1b10a532b15`.

Commands, with the pinned source trees and motion file at the paths referenced by the scripts:

```sh
python make-mask-probe.py
python real-node-diagnostic.py
```

The first command makes a four-frame 16-bit lossless artifact. The second loaded it through the pinned VHS implementation and mask methods, checked four values and `[4,1,1]` shape, then checked the actual motion-node audio mask resampling to `[1,1,2,7]` and retention of the existing video mask. See `diagnostic.log`. Container bytes can vary across encodes; the decoded values are the proof.

This diagnostic proves the exercised loader and tensor method behavior only. It does not prove Comfy executor, schema registration, final managed graph binding or inference quality; those remain separate claims. Durable focused tests must not depend on these temporary source checkouts.
