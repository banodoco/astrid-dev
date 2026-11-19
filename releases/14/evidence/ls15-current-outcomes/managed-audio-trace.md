# Managed-audio shutdown failure on the current LS-15 candidate

The managed-audio capability case reached the end of its drive and failed while closing the host. The first exception printed for this case is `CustodyUnresolved` at `astrid/core/generation/retained_preparation.py:209`. The retained preparation's `close()` saw `self.uncertain`. The captured stderr also reports a failed Comfy target `/queue` request during managed preparation release. The log does not identify the HTTP status, a transport exception, or the earlier operation that set the uncertainty flag. [Original integration job](https://github.com/banodoco/astrid-agent/actions/runs/44535565116/job/135599925333)

| Evidence | Identity |
| --- | --- |
| Agent checkout | `978fb66c13aa45ec49d60d838aef1574929b74dd` |
| Hosted execution | Run `44535565116`, attempt 1, job `135599925333`, integration shard 3 of 4 |
| Pytest node | `tests/integrations/test_runpod_slot_path_cpu.py::test_capability_reaches_generation_on_each_target[audio/music-local-managed]` |
| Node ID SHA-256 | `14665fda54ee4b559b6193fa3f07941d7ec97d1aad2541b9ac84bbf3c68a366e` |
| Original job log | 9,805,141 bytes, SHA-256 `9a61afa08f0912ba05de3040706379e9fd541061124f9d73087a3077e207c8b8` |
| Recorded outcome | FAILED at line 2860. Pytest exited 1. |

The GitHub job-log download and retained raw file have the same SHA-256. The existing comparison records the destination PASS and this candidate FAIL for the exact node ID. [Integration 3 comparison](integration3-outcomes.json.gz)

## Exception chain

| Original log lines | Operation and observed exception |
| --- | --- |
| 41251–41277 | The release adapter called `resource.close()`, then `self.managed.close()`. `RetainedPreparation.close()` raised `CustodyUnresolved` for unresolved prompt custody. |
| 41279–41315 | Resident release encountered its stored `_release_error` and raised `ResidentProtocolError` at `resident_sessions.py:641`. |
| 41317–41436 | The host called `managed_tool_session.close(reason="host_shutdown")`. The managed session wrapped the release failure in `SessionCapacityError` at `managed_tool_session.py:543`. |
| 41438–41580 | During `slot.shutdown()`, the slot raised `CleanupUncertainError` from `errors[0]` at `generic_host.py:7630`. Pytest printed its type as `custody_broker.CustodyError`. |
| 41582–41769 | Exiting `_drive` at test line 549 called `host.shutdown()` at test helper line 287. Outer host shutdown propagated that slot failure through the same aggregate raise. |
| 41770–41808 | The sole captured stream block is stderr. It records two Git checkouts, then queued, running and succeeded progress, followed by the owned-cleanup failure at line 41808. |

## Original traceback and captured stderr

The excerpt preserves every line of this pytest failure section, including its four explicit cause boundaries and captured stream. Numbers on the left refer to the original job log. Runner timestamp prefixes and trailing whitespace are omitted. Process addresses use stable object aliases. Temporary-directory and Python standard-library prefixes are shortened. Repository paths and source line numbers retain their original spelling.

```text
2860 | tests/integrations/test_runpod_slot_path_cpu.py::test_capability_reaches_generation_on_each_target[audio/music-local-managed] FAILED [ 74%]
41238 | _ test_capability_reaches_generation_on_each_target[audio/music-local-managed] _
41239 |
41240 | self = <astrid.core.execution.managed_tool_session.ManagedToolSession object at <object-1>>
41241 |
41242 |     def _fence_and_release_locked(self, *, reason: str) -> Mapping[str, Any] | None:
41243 |         active = self._active
41244 |         if active is None:
41245 |             self._generation += 1
41246 |             return
41247 |         try:
41248 |             fenced = self._fence_locked(reason=reason)
41249 |             if isinstance(fenced, Mapping) and fenced.get("ok") is False:
41250 |                 raise RuntimeError("managed session fence was not verified")
41251 | >           evidence = self._call_adapter(active.adapter, "release", reason=reason)
41252 |                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
41253 |
41254 | astrid/core/execution/managed_tool_session.py:536:
41255 | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
41256 | astrid/core/execution/managed_tool_session.py:569: in _call_adapter
41257 |     return operation(**{name: value})
41258 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
41259 | astrid/core/execution/resident_concurrency.py:189: in release
41260 |     result = super().release(reason=reason)
41261 |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
41262 | astrid/core/execution/resident_sessions.py:658: in release
41263 |     resource.close()
41264 | astrid/packs/vibecomfy/resident.py:167: in close
41265 |     self.managed.close()
41266 | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
41267 |
41268 | self = <astrid.core.generation.retained_preparation.RetainedPreparation object at <object-2>>
41269 |
41270 |     def close(self):
41271 |         if self.closed:
41272 |             return
41273 |         if self.uncertain:
41274 | >           raise CustodyUnresolved("retained managed readiness has unresolved prompt custody")
41275 | E           astrid.core.generation.engine_contracts.CustodyUnresolved: retained managed readiness has unresolved prompt custody
41276 |
41277 | astrid/core/generation/retained_preparation.py:209: CustodyUnresolved
41278 |
41279 | The above exception was the direct cause of the following exception:
41280 |
41281 | self = <astrid.core.execution.managed_tool_session.ManagedToolSession object at <object-1>>
41282 |
41283 |     def _fence_and_release_locked(self, *, reason: str) -> Mapping[str, Any] | None:
41284 |         active = self._active
41285 |         if active is None:
41286 |             self._generation += 1
41287 |             return
41288 |         try:
41289 |             fenced = self._fence_locked(reason=reason)
41290 |             if isinstance(fenced, Mapping) and fenced.get("ok") is False:
41291 |                 raise RuntimeError("managed session fence was not verified")
41292 | >           evidence = self._call_adapter(active.adapter, "release", reason=reason)
41293 |                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
41294 |
41295 | astrid/core/execution/managed_tool_session.py:536:
41296 | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
41297 | astrid/core/execution/managed_tool_session.py:569: in _call_adapter
41298 |     return operation(**{name: value})
41299 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
41300 | astrid/core/execution/resident_concurrency.py:189: in release
41301 |     result = super().release(reason=reason)
41302 |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
41303 | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
41304 |
41305 | self = <astrid.core.execution.resident_concurrency.ConcurrentResidentAdapter object at <object-3>>
41306 |
41307 |     def release(self, *, reason):
41308 |         from . import generic_host as core
41309 |
41310 |         self._fenced.set()
41311 |         if self._release_error is not None:
41312 | >           raise ResidentProtocolError("resident release remains unproved") from self._release_error
41313 | E           astrid.core.execution.resident_sessions.ResidentProtocolError: resident release remains unproved
41314 |
41315 | astrid/core/execution/resident_sessions.py:641: ResidentProtocolError
41316 |
41317 | The above exception was the direct cause of the following exception:
41318 |
41319 | self = <astrid.core.execution.generic_host.GenericPackHost object at <object-4>>
41320 |
41321 |     def shutdown(self) -> None:
41322 |         """Stop the host and every currently owned capability process."""
41323 |         with self.managed_tool_session._lock:
41324 |             self._shutdown.set()
41325 |         self._claim_loop_wake.set()
41326 |         cancel_waits = getattr(self.client, "cancel_waits", None)
41327 |         if callable(cancel_waits):
41328 |             cancel_waits()
41329 |         self.warm_holds.close()
41330 |         errors: list[BaseException] = []
41331 |         # Fence every serving slot before any session release can block or
41332 |         # report uncertainty. A failed release must not leave a sibling live.
41333 |         for slot in self._claim_slots:
41334 |             with slot.managed_tool_session._lock:
41335 |                 slot._shutdown.set()
41336 |         if self._handoff_accounting_owner is self:
41337 |             self._local_engine_idle.close()
41338 |         for slot in self._claim_slots:
41339 |             try:
41340 |                 slot.shutdown()
41341 |             except Exception as exc:
41342 |                 errors.append(exc)
41343 |                 slot._latch_cleanup_uncertainty(str(exc))
41344 |                 self._latch_cleanup_uncertainty(str(exc))
41345 |         with self._process_lock:
41346 |             bridges = tuple(self._child_bridges)
41347 |         for bridge in bridges:
41348 |             try:
41349 |                 bridge.revoke()
41350 |             except BaseException as exc:
41351 |                 errors.append(exc)
41352 |         with self._renderer_setup_lock:
41353 |             renderer_owner = self._remotion_host_session
41354 |             if renderer_owner is not None:
41355 |                 try:
41356 |                     renderer_owner.close()
41357 |                 except BaseException as exc:
41358 |                     errors.append(exc)
41359 |                     self._latch_cleanup_uncertainty(str(exc))
41360 |         adapter = self.managed_tool_session.current_adapter
41361 |         if isinstance(adapter, (_ManagedTaskAdapter, ResidentPackAdapter)):
41362 |             # The current CPU attempt retains its admission token until its
41363 |             # own finally has stopped and verified the original command and
41364 |             # released its session. Closing MTS here would clear that token
41365 |             # while release still correctly rejects a live command census.
41366 |             if isinstance(adapter, _ManagedTaskAdapter):
41367 |                 adapter.fence(reason="host_shutdown")
41368 |             # Resident dispatch observes _shutdown through its existing job
41369 |             # cancellation guard. Let its finalizer retain the token until
41370 |             # native stop and cancellation are proved, then close the owner.
41371 |             owner = self._handoff_accounting_owner
41372 |             deadline = time.monotonic() + 5.0
41373 |             with owner._handoff_condition:
41374 |                 while (owner._handoff_observation_known
41375 |                        and owner._handoff_active_attempts != 0):
41376 |                     remaining = deadline - time.monotonic()
41377 |                     if remaining <= 0:
41378 |                         break
41379 |                     owner._handoff_condition.wait(timeout=remaining)
41380 |                 complete = (owner._handoff_observation_known
41381 |                             and owner._handoff_active_attempts == 0)
41382 |             with self._process_lock:
41383 |                 complete = complete and not self._active_processes
41384 |             if not complete:
41385 |                 self._latch_cleanup_uncertainty("CPU attempt cleanup remains unresolved")
41386 |                 # Do not abandon retained originals when the adapter is poisoned.
41387 |                 # No new observation/admission is allowed on this failure path.
41388 |                 from astrid.core.execution.process_group import contain_retained_handles
41389 |                 cleanup_deadline = time.monotonic() + 2.0
41390 |                 with self._process_lock:
41391 |                     retained = tuple(self._active_processes | self._host_lifetime_processes)
41392 |                 for process in retained:
41393 |                     if getattr(process, "_astrid_task_scope", False):
41394 |                         _task_scope.stop(process, 0.2)
41395 |                         continue
41396 |                     contain_retained_handles(process, cleanup_deadline=cleanup_deadline,
41397 |                                              first_error=(getattr(process, "_astrid_tree_uncertain", None)
41398 |                                                           or "CPU attempt cleanup remains unresolved"))
41399 |                 graph = getattr(self, "_native_engine_graph", None)
41400 |                 if graph is not None:
41401 |                     try:
41402 |                         graph.abort()
41403 |                     except BaseException as exc:
41404 |                         errors.append(exc)
41405 |                 raise CleanupUncertainError("CPU attempt cleanup remains unresolved")
41406 |         try:
41407 | >           self.managed_tool_session.close(reason="host_shutdown")
41408 |
41409 | astrid/core/execution/generic_host.py:7607:
41410 | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
41411 | astrid/core/execution/managed_tool_session.py:471: in close
41412 |     self._fence_and_release_locked(reason=reason)
41413 | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
41414 |
41415 | self = <astrid.core.execution.managed_tool_session.ManagedToolSession object at <object-1>>
41416 |
41417 |     def _fence_and_release_locked(self, *, reason: str) -> Mapping[str, Any] | None:
41418 |         active = self._active
41419 |         if active is None:
41420 |             self._generation += 1
41421 |             return
41422 |         try:
41423 |             fenced = self._fence_locked(reason=reason)
41424 |             if isinstance(fenced, Mapping) and fenced.get("ok") is False:
41425 |                 raise RuntimeError("managed session fence was not verified")
41426 |             evidence = self._call_adapter(active.adapter, "release", reason=reason)
41427 |             if not isinstance(evidence, Mapping) or evidence.get("ok") is not True:
41428 |                 raise RuntimeError("managed session release was not verified")
41429 |         except Exception as exc:
41430 |             # Keep the slot poisoned and occupied.  Admitting a replacement
41431 |             # after an unverified release would make the old process an
41432 |             # orphan and violates the single-resource contract.
41433 | >           raise SessionCapacityError("managed session release was not verified") from exc
41434 | E           astrid.core.execution.managed_tool_session.SessionCapacityError: managed session release was not verified
41435 |
41436 | astrid/core/execution/managed_tool_session.py:543: SessionCapacityError
41437 |
41438 | The above exception was the direct cause of the following exception:
41439 |
41440 | self = <astrid.core.execution.generic_host.GenericPackHost object at <object-5>>
41441 |
41442 |     def shutdown(self) -> None:
41443 |         """Stop the host and every currently owned capability process."""
41444 |         with self.managed_tool_session._lock:
41445 |             self._shutdown.set()
41446 |         self._claim_loop_wake.set()
41447 |         cancel_waits = getattr(self.client, "cancel_waits", None)
41448 |         if callable(cancel_waits):
41449 |             cancel_waits()
41450 |         self.warm_holds.close()
41451 |         errors: list[BaseException] = []
41452 |         # Fence every serving slot before any session release can block or
41453 |         # report uncertainty. A failed release must not leave a sibling live.
41454 |         for slot in self._claim_slots:
41455 |             with slot.managed_tool_session._lock:
41456 |                 slot._shutdown.set()
41457 |         if self._handoff_accounting_owner is self:
41458 |             self._local_engine_idle.close()
41459 |         for slot in self._claim_slots:
41460 |             try:
41461 | >               slot.shutdown()
41462 |
41463 | astrid/core/execution/generic_host.py:7540:
41464 | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
41465 |
41466 | self = <astrid.core.execution.generic_host.GenericPackHost object at <object-4>>
41467 |
41468 |     def shutdown(self) -> None:
41469 |         """Stop the host and every currently owned capability process."""
41470 |         with self.managed_tool_session._lock:
41471 |             self._shutdown.set()
41472 |         self._claim_loop_wake.set()
41473 |         cancel_waits = getattr(self.client, "cancel_waits", None)
41474 |         if callable(cancel_waits):
41475 |             cancel_waits()
41476 |         self.warm_holds.close()
41477 |         errors: list[BaseException] = []
41478 |         # Fence every serving slot before any session release can block or
41479 |         # report uncertainty. A failed release must not leave a sibling live.
41480 |         for slot in self._claim_slots:
41481 |             with slot.managed_tool_session._lock:
41482 |                 slot._shutdown.set()
41483 |         if self._handoff_accounting_owner is self:
41484 |             self._local_engine_idle.close()
41485 |         for slot in self._claim_slots:
41486 |             try:
41487 |                 slot.shutdown()
41488 |             except Exception as exc:
41489 |                 errors.append(exc)
41490 |                 slot._latch_cleanup_uncertainty(str(exc))
41491 |                 self._latch_cleanup_uncertainty(str(exc))
41492 |         with self._process_lock:
41493 |             bridges = tuple(self._child_bridges)
41494 |         for bridge in bridges:
41495 |             try:
41496 |                 bridge.revoke()
41497 |             except BaseException as exc:
41498 |                 errors.append(exc)
41499 |         with self._renderer_setup_lock:
41500 |             renderer_owner = self._remotion_host_session
41501 |             if renderer_owner is not None:
41502 |                 try:
41503 |                     renderer_owner.close()
41504 |                 except BaseException as exc:
41505 |                     errors.append(exc)
41506 |                     self._latch_cleanup_uncertainty(str(exc))
41507 |         adapter = self.managed_tool_session.current_adapter
41508 |         if isinstance(adapter, (_ManagedTaskAdapter, ResidentPackAdapter)):
41509 |             # The current CPU attempt retains its admission token until its
41510 |             # own finally has stopped and verified the original command and
41511 |             # released its session. Closing MTS here would clear that token
41512 |             # while release still correctly rejects a live command census.
41513 |             if isinstance(adapter, _ManagedTaskAdapter):
41514 |                 adapter.fence(reason="host_shutdown")
41515 |             # Resident dispatch observes _shutdown through its existing job
41516 |             # cancellation guard. Let its finalizer retain the token until
41517 |             # native stop and cancellation are proved, then close the owner.
41518 |             owner = self._handoff_accounting_owner
41519 |             deadline = time.monotonic() + 5.0
41520 |             with owner._handoff_condition:
41521 |                 while (owner._handoff_observation_known
41522 |                        and owner._handoff_active_attempts != 0):
41523 |                     remaining = deadline - time.monotonic()
41524 |                     if remaining <= 0:
41525 |                         break
41526 |                     owner._handoff_condition.wait(timeout=remaining)
41527 |                 complete = (owner._handoff_observation_known
41528 |                             and owner._handoff_active_attempts == 0)
41529 |             with self._process_lock:
41530 |                 complete = complete and not self._active_processes
41531 |             if not complete:
41532 |                 self._latch_cleanup_uncertainty("CPU attempt cleanup remains unresolved")
41533 |                 # Do not abandon retained originals when the adapter is poisoned.
41534 |                 # No new observation/admission is allowed on this failure path.
41535 |                 from astrid.core.execution.process_group import contain_retained_handles
41536 |                 cleanup_deadline = time.monotonic() + 2.0
41537 |                 with self._process_lock:
41538 |                     retained = tuple(self._active_processes | self._host_lifetime_processes)
41539 |                 for process in retained:
41540 |                     if getattr(process, "_astrid_task_scope", False):
41541 |                         _task_scope.stop(process, 0.2)
41542 |                         continue
41543 |                     contain_retained_handles(process, cleanup_deadline=cleanup_deadline,
41544 |                                              first_error=(getattr(process, "_astrid_tree_uncertain", None)
41545 |                                                           or "CPU attempt cleanup remains unresolved"))
41546 |                 graph = getattr(self, "_native_engine_graph", None)
41547 |                 if graph is not None:
41548 |                     try:
41549 |                         graph.abort()
41550 |                     except BaseException as exc:
41551 |                         errors.append(exc)
41552 |                 raise CleanupUncertainError("CPU attempt cleanup remains unresolved")
41553 |         try:
41554 |             self.managed_tool_session.close(reason="host_shutdown")
41555 |         except BaseException as exc:
41556 |             errors.append(exc)
41557 |         with self._process_lock:
41558 |             active = tuple(self._active_processes | self._host_lifetime_processes)
41559 |         for process in active:
41560 |             try:
41561 |                 _terminate_process_group(process, grace_seconds=1.0)
41562 |             except BaseException as exc:
41563 |                 errors.append(exc)
41564 |         graph = getattr(self, "_native_engine_graph", None)
41565 |         if graph is not None:
41566 |             try:
41567 |                 graph.abort()
41568 |             except BaseException as exc:
41569 |                 errors.append(exc)
41570 |         if self._handoff_accounting_owner is self and self._target_bindings is not None:
41571 |             try:
41572 |                 self._target_bindings.close()
41573 |             except BaseException as exc:
41574 |                 errors.append(exc)
41575 |         if errors:
41576 |             self._latch_cleanup_uncertainty("; ".join(str(error) for error in errors))
41577 | >           raise CleanupUncertainError("host graph cleanup remains unresolved") from errors[0]
41578 | E           astrid.core.execution.custody_broker.CustodyError: host graph cleanup remains unresolved
41579 |
41580 | astrid/core/execution/generic_host.py:7630: CustodyError
41581 |
41582 | The above exception was the direct cause of the following exception:
41583 |
41584 | capability = ('audio', 'music'), target_kind = 'local-managed'
41585 | align_mode = 'check'
41586 | tmp_path = PosixPath('<pytest-temp>/test_capability_reaches_genera0')
41587 | monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at <object-6>>
41588 | real_runtime = <function real_runtime.<locals>.start at <object-7>>
41589 | tuple_sources = PosixPath('<pytest-temp>/retained-bootstrap0')
41590 |
41591 |     @pytest.mark.parametrize(
41592 |         "capability,target_kind,align_mode",
41593 |         [pytest.param(c, t, "check", id=f"{'/'.join(c)}-{t}",
41594 |                       # CPU cannot verify the 1.9GB pinned turbo LoRA hash h3's validate step re-hashes (Plan 34; as the TTS local cell).
41595 |                       marks=[pytest.mark.gpu] if (c, t) == (("video", "h3"), "local-managed") else [])
41596 |          for t in TARGET_KINDS for c in CAPABILITIES]
41597 |         + [pytest.param(("audio", mode), target, "trust", id=f"audio/{mode}-{target}-trust")
41598 |            for mode in ("tts", "sfx") for target in ("local-managed", "attached")])
41599 |     # Slow on purpose: the video/h3 cells measured 267-304 s on hosted Lanes; the suite default is 120 s.
41600 |     @pytest.mark.timeout(600)
41601 |     def test_capability_reaches_generation_on_each_target(capability, target_kind, align_mode, tmp_path, monkeypatch,
41602 |                                                           real_runtime, tuple_sources):
41603 |         composed = set()
41604 |         if capability == ("video", "h3"):
41605 |             # The job directory (and the candidate composed in it) is removed when the run ends; hash it first.
41606 |             import hashlib, shutil
41607 |             real_rmtree = shutil.rmtree
41608 |             def hashing_rmtree(path, *args, **kwargs):
41609 |                 if Path(path).name.startswith("astrid-job-"):
41610 |                     composed.update(hashlib.sha256(f.read_bytes()).hexdigest()
41611 |                                     for f in Path(path).rglob("*.composed.*") if "compose" in f.parts)
41612 |                 return real_rmtree(path, *args, **kwargs)
41613 |             monkeypatch.setattr(shutil, "rmtree", hashing_rmtree)
41614 |         if capability == ("video", "h3"):
41615 |             import subprocess
41616 |             source = tmp_path / "source.mp4"
41617 |             subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
41618 |                             "color=c=blue:s=1024x576:r=24", "-f", "lavfi", "-i", "sine=frequency=440:duration=3",
41619 |                             "-frames:v", "57", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest",
41620 |                             str(source)], check=True, timeout=120)
41621 |             request = json.loads(H3_REQUEST.read_text())
41622 |             assets = tmp_path / "assets.json"
41623 |             assets.write_text(json.dumps({request["media"][0]["asset"]["id"]: str(source), "source": str(source)}))
41624 |             h3_classes = set(json.loads((Path(__file__).resolve().parents[1]
41625 |                                          / "fixtures/h3_cpu/object_info_h3_runpod_graph_closure.json").read_text()))
41626 |             h3_classes |= _h3_built_classes(H3_REQUEST, json.loads(assets.read_text()), tmp_path)
41627 |             def call(facade, controls, tmp):
41628 |                 return facade.video(entry="h3", request=str(H3_REQUEST), asset_map=str(assets), **controls)
41629 |             drive = dict(extra_classes=h3_classes, call=call, machine_identity=True, h3_output=True)
41630 |         else:
41631 |             drive = dict(call=_capability_call(capability))
41632 |         if align_mode == "trust":
41633 |             drive["trusted_inventory"] = True
41634 |             call = drive["call"]
41635 |             drive["call"] = lambda facade, controls, tmp: call(facade, {**controls, "align": "trust"}, tmp)
41636 |         red = _RED.get((capability, target_kind)) if align_mode == "check" else None
41637 |         if red and red[0] != "result":
41638 |             # Checked inventory refusal, with its remaining owner recorded in _RED
41639 |             with pytest.raises(Exception) as caught:
41640 |                 with _drive(capability, tmp_path, monkeypatch, real_runtime, tuple_sources, target_kind=target_kind, **drive):
41641 |                     pass
41642 |             assert type(caught.value).__name__ == red[0] and red[1] in str(caught.value), repr(caught.value)[:2000]
41643 |             return
41644 | >       with _drive(capability, tmp_path, monkeypatch, real_runtime, tuple_sources, target_kind=target_kind,
41645 |                     **drive) as (client, project_id, provider, result):
41646 |
41647 | tests/integrations/test_runpod_slot_path_cpu.py:549:
41648 | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
41649 | <python-3.11-stdlib>/contextlib.py:144: in __exit__
41650 |     next(self.gen)
41651 | tests/integrations/test_runpod_slot_path_cpu.py:287: in _drive
41652 |     host.shutdown()
41653 | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
41654 |
41655 | self = <astrid.core.execution.generic_host.GenericPackHost object at <object-5>>
41656 |
41657 |     def shutdown(self) -> None:
41658 |         """Stop the host and every currently owned capability process."""
41659 |         with self.managed_tool_session._lock:
41660 |             self._shutdown.set()
41661 |         self._claim_loop_wake.set()
41662 |         cancel_waits = getattr(self.client, "cancel_waits", None)
41663 |         if callable(cancel_waits):
41664 |             cancel_waits()
41665 |         self.warm_holds.close()
41666 |         errors: list[BaseException] = []
41667 |         # Fence every serving slot before any session release can block or
41668 |         # report uncertainty. A failed release must not leave a sibling live.
41669 |         for slot in self._claim_slots:
41670 |             with slot.managed_tool_session._lock:
41671 |                 slot._shutdown.set()
41672 |         if self._handoff_accounting_owner is self:
41673 |             self._local_engine_idle.close()
41674 |         for slot in self._claim_slots:
41675 |             try:
41676 |                 slot.shutdown()
41677 |             except Exception as exc:
41678 |                 errors.append(exc)
41679 |                 slot._latch_cleanup_uncertainty(str(exc))
41680 |                 self._latch_cleanup_uncertainty(str(exc))
41681 |         with self._process_lock:
41682 |             bridges = tuple(self._child_bridges)
41683 |         for bridge in bridges:
41684 |             try:
41685 |                 bridge.revoke()
41686 |             except BaseException as exc:
41687 |                 errors.append(exc)
41688 |         with self._renderer_setup_lock:
41689 |             renderer_owner = self._remotion_host_session
41690 |             if renderer_owner is not None:
41691 |                 try:
41692 |                     renderer_owner.close()
41693 |                 except BaseException as exc:
41694 |                     errors.append(exc)
41695 |                     self._latch_cleanup_uncertainty(str(exc))
41696 |         adapter = self.managed_tool_session.current_adapter
41697 |         if isinstance(adapter, (_ManagedTaskAdapter, ResidentPackAdapter)):
41698 |             # The current CPU attempt retains its admission token until its
41699 |             # own finally has stopped and verified the original command and
41700 |             # released its session. Closing MTS here would clear that token
41701 |             # while release still correctly rejects a live command census.
41702 |             if isinstance(adapter, _ManagedTaskAdapter):
41703 |                 adapter.fence(reason="host_shutdown")
41704 |             # Resident dispatch observes _shutdown through its existing job
41705 |             # cancellation guard. Let its finalizer retain the token until
41706 |             # native stop and cancellation are proved, then close the owner.
41707 |             owner = self._handoff_accounting_owner
41708 |             deadline = time.monotonic() + 5.0
41709 |             with owner._handoff_condition:
41710 |                 while (owner._handoff_observation_known
41711 |                        and owner._handoff_active_attempts != 0):
41712 |                     remaining = deadline - time.monotonic()
41713 |                     if remaining <= 0:
41714 |                         break
41715 |                     owner._handoff_condition.wait(timeout=remaining)
41716 |                 complete = (owner._handoff_observation_known
41717 |                             and owner._handoff_active_attempts == 0)
41718 |             with self._process_lock:
41719 |                 complete = complete and not self._active_processes
41720 |             if not complete:
41721 |                 self._latch_cleanup_uncertainty("CPU attempt cleanup remains unresolved")
41722 |                 # Do not abandon retained originals when the adapter is poisoned.
41723 |                 # No new observation/admission is allowed on this failure path.
41724 |                 from astrid.core.execution.process_group import contain_retained_handles
41725 |                 cleanup_deadline = time.monotonic() + 2.0
41726 |                 with self._process_lock:
41727 |                     retained = tuple(self._active_processes | self._host_lifetime_processes)
41728 |                 for process in retained:
41729 |                     if getattr(process, "_astrid_task_scope", False):
41730 |                         _task_scope.stop(process, 0.2)
41731 |                         continue
41732 |                     contain_retained_handles(process, cleanup_deadline=cleanup_deadline,
41733 |                                              first_error=(getattr(process, "_astrid_tree_uncertain", None)
41734 |                                                           or "CPU attempt cleanup remains unresolved"))
41735 |                 graph = getattr(self, "_native_engine_graph", None)
41736 |                 if graph is not None:
41737 |                     try:
41738 |                         graph.abort()
41739 |                     except BaseException as exc:
41740 |                         errors.append(exc)
41741 |                 raise CleanupUncertainError("CPU attempt cleanup remains unresolved")
41742 |         try:
41743 |             self.managed_tool_session.close(reason="host_shutdown")
41744 |         except BaseException as exc:
41745 |             errors.append(exc)
41746 |         with self._process_lock:
41747 |             active = tuple(self._active_processes | self._host_lifetime_processes)
41748 |         for process in active:
41749 |             try:
41750 |                 _terminate_process_group(process, grace_seconds=1.0)
41751 |             except BaseException as exc:
41752 |                 errors.append(exc)
41753 |         graph = getattr(self, "_native_engine_graph", None)
41754 |         if graph is not None:
41755 |             try:
41756 |                 graph.abort()
41757 |             except BaseException as exc:
41758 |                 errors.append(exc)
41759 |         if self._handoff_accounting_owner is self and self._target_bindings is not None:
41760 |             try:
41761 |                 self._target_bindings.close()
41762 |             except BaseException as exc:
41763 |                 errors.append(exc)
41764 |         if errors:
41765 |             self._latch_cleanup_uncertainty("; ".join(str(error) for error in errors))
41766 | >           raise CleanupUncertainError("host graph cleanup remains unresolved") from errors[0]
41767 | E           astrid.core.execution.custody_broker.CustodyError: host graph cleanup remains unresolved
41768 |
41769 | astrid/core/execution/generic_host.py:7630: CustodyError
41770 | ----------------------------- Captured stderr call -----------------------------
41771 | Note: switching to '1ba0ac3ad4fe69fa0b4966cc41e6852224013f97'.
41772 |
41773 | You are in 'detached HEAD' state. You can look around, make experimental
41774 | changes and commit them, and you can discard any commits you make in this
41775 | state without impacting any branches by switching back to a branch.
41776 |
41777 | If you want to create a new branch to retain commits you create, you may
41778 | do so (now or later) by using -c with the switch command. Example:
41779 |
41780 |   git switch -c <new-branch-name>
41781 |
41782 | Or undo this operation with:
41783 |
41784 |   git switch -
41785 |
41786 | Turn off this advice by setting config variable advice.detachedHead to false
41787 |
41788 | Note: switching to '6bfaacc67c2103481e5f0c84d75257cd0581d86a'.
41789 |
41790 | You are in 'detached HEAD' state. You can look around, make experimental
41791 | changes and commit them, and you can discard any commits you make in this
41792 | state without impacting any branches by switching back to a branch.
41793 |
41794 | If you want to create a new branch to retain commits you create, you may
41795 | do so (now or later) by using -c with the switch command. Example:
41796 |
41797 |   git switch -c <new-branch-name>
41798 |
41799 | Or undo this operation with:
41800 |
41801 |   git switch -
41802 |
41803 | Turn off this advice by setting config variable advice.detachedHead to false
41804 |
41805 | [0s] queued  waiting=-
41806 | [0s] running  waiting=-
41807 | [20s] succeeded 90%  waiting=-
41808 | generic host claim failed (1 consecutive): HostError: owned cleanup incomplete: managed preparation release: comfy target /queue request failed
```
