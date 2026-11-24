/** Enable the tape once, after its caller has proved the exact public head and plan. */
export function armFreeSpace({x, y, clipId, trackId}) {
  const tape = window.__p77DispatchTrace;
  const hit = document.elementFromPoint(x, y);
  const clip = hit?.closest('.clip-action[data-row-id][data-clip-id]');
  if (!tape || tape.armed || tape.pointer || tape.omitted || !tape.fullWritable()
      || tape.counts['app:timeline_commit'].requested || clip?.dataset.clipId !== clipId
      || clip?.dataset.rowId !== trackId || hit.closest('button, [data-no-clip-drag], [data-resize-edge]')) {
    return false;
  }
  tape.armed = true;
  return true;
}
