"""Drive `timelines transcripts refresh --use-source <whisper>` in-process (no network, no runtime) and save a draft."""
import json, sys
from argparse import Namespace
from pathlib import Path
from astrid.sdk.media_transcript import transcript_document_id
from astrid.sdk.timeline import words as W
from astrid.sdk.timeline_checkout import Checkout
from astrid.packs.timeline import cli_working

out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
PROJECT = "project-1"; MEDIA_A = "sha256:" + "a" * 64
whisper = W.default_source_order()[0]
doc = {"document_id": transcript_document_id(PROJECT, MEDIA_A, whisper), "version": 2,
       "content": {"schema": "media.transcript/v1", "media_id": MEDIA_A, "source_id": whisper,
                   "segments": [{"id": "seg", "words": [{"id": "word:0", "start": 0.0, "end": 0.5, "text": "hi"}]}]}}
clip = {"id": "c1", "track": "vo", "asset": "a", "at": 0.0, "from": 0.0, "to": 4.0, "speed": 1.0}
bundle = {"project_id": PROJECT,
          "placements": [{"shot_id": "s1", "occurrence_id": "occ-0", "at_ms": 0, "duration_ms": 4000}],
          "parent": {"clips": [], "tracks": [{"id": "vo", "kind": "vo"}],
                     "registry": {"assets": {"a": {"media_id": MEDIA_A}}},
                     # the App-authored envelope the Agent edits in place (seeded: what a real project holds)
                     "config": {"bundle": {"schema_version": 1, "itemsBySchemaRef": {}}}},
          "shots": {"s1": {"internal_timeline": {"clips": [clip], "tracks": [{"id": "vo", "kind": "vo"}],
                                                  "registry": {"assets": {"a": {"media_id": MEDIA_A}}}}}}}
draft_path = out / "draft.checkout.json"
working = Checkout(bundle, path=draft_path)
Checkout.open = classmethod(lambda cls, project, ref, client: working)
cli_working.working_copy = lambda parsed, create: (working, True)
W.load_timeline_transcripts = lambda client, project, bundle, **kw: {MEDIA_A: {whisper: doc}}
args = Namespace(client=object(), project="project-1", ref="cut", shot=None, run_missing=False, placement=None,
                 dry_run=False, draft=None, use_source=whisper, use_document=None)
print("rc", cli_working._cmd_transcripts_refresh(args))
saved = json.loads(draft_path.read_text())
b = saved["parent"]["config"]["bundle"]
(out / "parent_config_bundle.json").write_text(json.dumps(b, indent=2))
print(json.dumps(b, indent=2))
