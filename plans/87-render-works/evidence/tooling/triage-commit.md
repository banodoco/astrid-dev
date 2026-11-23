# Triage: timeline commit defects (G1-G3), release/14/main

Method: worktree HEAD is `release/14/fix-1238-stale-registry-asset` with uncommitted changes and no local `release/14/main`. All main line numbers come from `git show origin/release/14/main:./<path>` (origin tip 9f614dff7, "Merge pull request #400 ... legacy-basis"). Paths below are under `astrid/` in the repo. Nothing was checked out or edited.

Friction-log citations vs main:
- `sdk/timeline/sync.py:1075` and `:1166`: same lines on main. OK.
- `sdk/timeline/commit_session.py:603`: `def commit` on main, same line.
- `sdk/timeline_elements.py ~146-158` / `_settle_held_flight`: NOT on main. There is no `_settle_held_flight` anywhere on main. Lines 140-158 on main are `_matches`/`_clip` (element-update helpers, unrelated to the outbox). The replay mechanism on main is `TimelineSession.resolve_acknowledged` (`sdk/timeline/sync.py:762-781`), which is reached from `commit_session.py:674`. Inference: the friction cited a newer installed copy.
- Edit-D `Clip.nudge` path: `sdk/timeline/model.py:396-411` (nudge), `:299-321` (`on`, calls `self._tl.retime()` at :321). Timeline.retime is `sdk/timeline/reflow.py:370` ("Resolve every moment (after a VO change, a gap, an edit)").
- `packs/timeline/cli.py`: `_cmd_edit` at :2755, auto-sweep at :2864-2868, `_apply_edit` at :2897, `clip.set(...)` at :3037 and :3072, `clip.swap_asset` at :3048, `--no-sweep` check at :3137.

## G1 - edit patch folds unrelated rewrites

(a) Issues: none found for "retime", "nudge", "push=None", "reflow". Only #1246 touches the large-body failure (see G2).

(b) Code on main:
- `sdk/timeline/model.py:396-411`:
  ```
  def nudge(self, seconds: float = 0.0, *, frames: int = 0) -> "Clip":
      current = intent.on(self.data)
      if current:
          moment = mo.parse(current).with_offset(seconds=float(seconds), frames=int(frames))
          return self.on(moment)
  ```
  Moment clips go through `on()`, which calls `self._tl.retime()` (`model.py:321`). `retime` (`sdk/timeline/reflow.py:370`) resolves every moment in the timeline, so unrelated clips get rewritten. Inference: this is the source of the 353 `at` + 7 `hold` changes in friction edits item 5. Quoted from the code, not run.
- `sdk/timeline/commit_session.py:603` `commit(...)` is the entry point; `edits.py:546` is the only `"push"` handling found under `sdk/timeline` (plate push param). No code path on main was found that makes `set(push=None)` a no-op; not traced further.
- `packs/timeline/cli.py:3037-3048` applies `clip.set` and `clip.swap_asset` for `--set`/`--swap-asset`. Friction reports c34 retime even with `--no-sweep`. Inference: the retime comes from the per-clip mutation path (`retime`), not from the sweep at :2864-2868, since `--no-sweep` was passed.

## G2 - dry run reports CommitOutcomeUnknown; follow-up contradicts

(a) Issues: **#1246** (open, astrid-dev) "bug: a failed timeline commit can leave the timeline stuck with no supported way to clear it". Its body describes the same class: a 1.96 MB body, `Broken pipe` + `CommitOutcomeUnknown`, a left-behind in-flight record blocking later commits. It is a close match on symptoms; it is not specifically about dry runs. Related: **#1369** (open, astrid-dev, Release 15 observation): retry raises "in-flight request is immutable" when a flight is replaced between read and flush. Searches for "may or may not have been committed", "outcome unknown dry_run", "CommitOutcomeUnknown" returned no other issue. Hits #442/#1101/#1174 are unrelated PR text.

(b) Code (main):
- `sdk/timeline/sync.py:1001-1002`: `def _flush(self, *, idempotency_key=None, dry_run=False, via="python", prepare=None, release_conflict=False):`
- `sdk/timeline/sync.py:1075-1078`:
  ```
  result = _response(self.client.timelines.commit(
      self.project_id, self.timeline_id, body, idempotency_key=flight["key"],
  ))
  except Exception as exc:
  ```
- `sdk/timeline/sync.py:1166`: `raise CommitOutcomeUnknown(exc, key=_display_key(flight)) from exc  # Keep the durable flight byte-for-byte retryable.` The branch above it (lines 1079-1165) handles only `status in {conflict, refused, invalid}`. Nothing checks `dry_run` before line 1166.
- `sdk/timeline/sync.py:107-122`: `CommitOutcomeUnknown.__init__` calls `present_failure(failure, unknown=True)`.
- `sdk/timeline/_commit_wording.py:46-48`: headline "No reply could be verified; this edit may or may not have been committed"; fix "Call tl.commit() again with no arguments to confirm the saved request; the edit is not re-run blindly." Generic, with no dry-run branch.
- Why the follow-up says "in-flight request is immutable" (inference, from reading code): a dry-run flight is persisted with `body["dry_run"] = True` (`sync.py:1017`). `tl.commit()` with no args calls `flush(dry_run=False)` (`commit_session.py:603` default). `_flight_body` (`sync.py:1295-1315`) requires `body.get("dry_run", False) == dry_run` (line 1310) and raises "in-flight request is immutable; retry its original payload and key" (line 1314). So the wording's advised call can never match a dry-run flight.

(c) Small local fix: plausible but design-dependent. Inference: a dry run never commits, so clearing `state["flight"]` on a dry-run transport failure should be safe, since the flight is only a marker over `state["pending"][:count]` and `del state["pending"][...]` runs only on the ack path (`sync.py:1195`). A fix would sit before line 1166: under `self.outbox.locked()`, when `dry_run`, set `state["flight"] = None`, write, then raise a `TimelineEditError`/`WorkspaceClientError` with "dry run did not reach the Runtime; nothing was saved; retry". Wording branch in `_commit_wording.py` would also need a dry-run variant. Owner decision needed on whether dry runs should keep a retryable flight.
Tests that pin CommitOutcomeUnknown (the path is `~/Developer/astrid-release-src/wt-r14-fix-1238/tests`; the same 8 files exist on main under `../tests`):
- `tests/sdk/test_timeline_sync.py:206` (`match="No reply could be verified"`, lost-ack non-dry commit)
- `tests/sdk/test_timeline_open_commit_v2.py:598`
- `tests/sdk/test_timeline_commit_wording_runtime.py:196`
- `tests/sdk/test_timeline_clash_back_runtime.py:641`
- `tests/sdk/test_timeline_editing_acceptance_runtime.py:169`, `:1199`
- `tests/timeline/test_audio_import_runtime.py:140`
- `tests/timeline/test_function_media_replay.py:98`, `:171`
- `tests/editing_conformance/test_timeline_clash_back_acceptance_runtime.py:574`, `:818`
No test covers `dry_run=True` with a transport failure (not verified exhaustively; grep for `dry_run` + `CommitOutcomeUnknown` found none).

## G3 - one shared outbox per timeline

(a) Issues: **#1246** covers the stuck-flight symptom and the manual outbox-file edit. **#1369** covers the retry/replace race. No issue found for the per-process outbox or the stale `head`.

(b) Code (main):
- Default path: `sdk/timeline/sync.py:407-422`:
  ```
  explicit_outbox = outbox_path is not None
  if outbox_path is None:
      name = hashlib.sha256(request_bytes(scope)).hexdigest() + ".json"
      outbox_path = resolve_runtime_data_root() / "timeline-outbox" / name
  session = cls(client, Outbox(outbox_path), identity, project_id, timeline_id)
  session._explicit_outbox = explicit_outbox
  ```
  `scope = {**identity, "project_id": ..., "timeline_id": ...}` (`sync.py:416`). So one file per (actor identity, project, timeline), shared by every session of that actor. Confirmed.
- Per-process outbox IS supported: `outbox_path=` at `Timeline.open` (`sdk/timeline/commit_session.py:310-311`, `sync.py:407`). Passing it sets `_explicit_outbox`, which switches pending/flight listing from `actors="all"` to `"self"` (`commit_session.py:648`, `:685`, `:898-899`). The friction's workaround is the intended route.
- Stale head: `sync.py:423-445` reads and writes `state["base"]` under the lock; `Timeline.open(...).head` was not traced. Inference: the head reflects the shared outbox's `base`, so a held sibling flight leaves it stale.
- Sibling-replay path: `commit_session.py:674` calls `resolve_acknowledged` (`sync.py:762`), which reads `state["acknowledged"][key]` from the shared outbox. Inference: with `actors="all"`, one agent can replay another's acknowledged key. Not proven.

## Facts for the owner
- Main has no `_settle_held_flight`; the friction's `timeline_elements.py:146-158` cite is stale.
- The `dry_run` gap at `sync.py:1166` and the generic wording at `_commit_wording.py:46-48` are the only small G2 change points found.
