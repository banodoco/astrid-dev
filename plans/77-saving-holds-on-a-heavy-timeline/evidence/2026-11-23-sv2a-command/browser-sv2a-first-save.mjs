import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {lstat, mkdtemp, readFile, rm, statfs, writeFile} from 'node:fs/promises';
import {loadavg} from 'node:os';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {armFreeSpace} from './arm-free-space.mjs';
import {
  browserTape, canonicalFreeSpace, exactFreeSpaceDiff, exactOccurrences, freeSpacePointsMatch, wireCommits,
} from './reused-trace-helpers.mjs';

const [root, data, fixturePath, tuplePath, dist, distInventory, tools, output, mode, preflightPath] = process.argv.slice(2);
assert.equal(process.argv.length, 12);
assert.equal(mode, 'candidate');
process.umask(0o077);
const readJson = async location => JSON.parse(await readFile(location, 'utf8'));
const tuple = await readJson(tuplePath);
assert.equal(tuple.app, '148eaf381e3f02dc0f0d5dfc61e61ebf37dbc715');
assert.equal(tuple.agent, '5e301956dc49c8b9ba4d23a7ce96c6564bd74d2f');
assert.match(tuple.runtime, /^[a-f0-9]{40}$/);
const preflight = await readJson(preflightPath);
const {runtime_sha: runtimeSha, pid, start} = preflight;
assert.equal(runtimeSha, tuple.runtime);
assert(Number.isSafeInteger(pid) && pid > 0);
assert.match(start, /^\d+$/);
const candidate = {runtime_sha: runtimeSha, pid, start};
for (const file of ['save-1.json', 'browser-sv2a-first-save.json']) {
  await assert.rejects(lstat(path.join(output, file)), {code: 'ENOENT'});
}

const loadModule = location => import(pathToFileURL(location));
const {chromium} = await loadModule(process.env.SAVE_LOOP_PLAYWRIGHT);
const {publicSnapshot} = await loadModule(path.join(tools, 'scripts/save-loop/assert.mjs'));
const {runtimeRootForData, parseStat} = await loadModule(path.join(tools, 'scripts/save-loop/cpu.mjs'));
const {expectedFixtureIds, sameIds} = await loadModule(path.join(tools, 'scripts/save-loop/readiness.mjs'));
const fixture = await readJson(fixturePath);
const project = fixture.project_id;
const timeline = fixture.timeline_id;
const pin = {project, timeline,
  revision_id: 'authoring-parent-revision-5357f6c0f85f6b1edbe53275043432abf63a33f56582ae6f300b06519436acaa',
  publication_id: 'txn-45427064f4d34b9a840005c774956763',
  content_digest: 'sha256:75f9d65814ba3b48ca0d0422bf04f28a07178f25931a8c3bd57d582ff06cbaae'};
const target = {clip_id: 'fixture-video-0190', track_id: 'V6'};
const expectedStartSeconds = 191.3667;
assert(fixture.media.synthetic === true && fixture.variant === 'standard');
assert.equal(project, '042a5c0245af40818c4ea6f75d3a4206');
assert.equal(timeline, 'save-loop-heavy-1d4576fd');
const clips = expectedFixtureIds(fixture);
const tracks = [...fixture.tracks.visual, ...fixture.tracks.audio].map(track => track.id);
const occurrences = fixture.clips.shot_occurrences.map(item => item.occurrence_id);
assert(clips.length === 300 && tracks.length === 9 && occurrences.length === 10);

const inventory = new Map((await readFile(distInventory, 'utf8')).trim().split('\n').map(line => {
  const match = /^([a-f0-9]{64})  \.\/(.+)$/.exec(line);
  assert(match);
  return [match[2], match[1]];
}));
const origin = 'http://127.0.0.1:2400';
const projectKey = '/v1/projects/' + encodeURIComponent(project);
const timelineKey = projectKey + '/timelines/' + encodeURIComponent(timeline);
const scopedProject = '/api/runtime' + projectKey;
const scopedTimeline = '/api/runtime' + timelineKey;
const commitRoute = scopedTimeline + '/commit';
const commitUrl = origin + commitRoute;
const url = new URL('/tools/video-editor', origin);
url.searchParams.set('connect', '1');
url.searchParams.set('project', project);
url.searchParams.set('timeline', timeline);
const runtimeHealthUrl = origin + '/api/runtime/v1/health';
const runtime = await runtimeRootForData(root, data, runtimeHealthUrl);
assert.deepEqual(runtime, {pid: candidate.pid, start: candidate.start});
const ticks = Number(execFileSync('getconf', ['CLK_TCK'], {encoding: 'utf8'}).trim());
assert(Number.isFinite(ticks) && ticks > 0);
async function cpu() {
  const sample = parseStat(await readFile(`/proc/${runtime.pid}/stat`, 'utf8'));
  assert.equal(sample.start, runtime.start, 'Runtime process changed');
  return sample.cpu / ticks;
}

const browserParent = process.env.P77_R7_BROWSER_TMP;
assert(/^\/tmp\/sl-p77-r7-[A-Za-z0-9]+$/.test(browserParent));
const diskPaths = [data, output, browserParent];
const diskFloorBytes = 16n * 1024n ** 3n;
async function diskFree() {
  return Promise.all(diskPaths.map(async location => {
    const sample = await statfs(location, {bigint: true});
    return {path: location, bytes_available: Number(sample.bavail * sample.bsize)};
  }));
}
function assertDiskFree(readings) {
  assert(readings.every(entry => entry.bytes_available >= Number(diskFloorBytes)), 'Free disk fell below 16 GiB');
}

const clock = () => {
  const monotonicMs = performance.now();
  return {monotonic_ms: monotonicMs, epoch_ms: performance.timeOrigin + monotonicMs};
};
const headSummary = head => ({revision: head.headRevision, publication: head.publicationId,
  content_digest: head.content_digest, active_heads: head.headCount, clips: head.clipIds.length,
  occurrences: head.payload.occurrences.length});
function verifyScopedHead(snapshot, expected) {
  assert.equal(snapshot.headRevision, expected.revision_id);
  assert.equal(snapshot.publicationId, expected.publication_id);
  assert.equal(snapshot.content_digest, expected.content_digest);
  assert.equal(snapshot.headCount, 1);
  assert(sameIds(snapshot.clipIds, clips) && exactOccurrences(snapshot, occurrences));
}
function bounded(ms, action) {
  let timer;
  return Promise.race([action(), new Promise((_, reject) => {
    timer = setTimeout(() => reject(new Error('Observation deadline')), ms);
  })]).finally(() => clearTimeout(timer));
}
const writeReceipt = (name, receipt) => writeFile(path.join(output, `${name}.json`),
  JSON.stringify(receipt, null, 2) + '\n', {flag: 'wx', mode: 0o600});

async function verifyServedAsset(context, route) {
  const name = route.slice(1);
  const digest = bytes => createHash('sha256').update(bytes).digest('hex');
  const response = await context.request.get(origin + route, {timeout: 10_000});
  const expected = inventory.get(name);
  assert(response.ok() && expected && digest(await response.body()) === expected);
  assert.equal(digest(await readFile(path.join(dist, name))), expected);
}

function observeRequests(page) {
  const events = new Map();
  page.on('request', request => {
    const target = new URL(request.url());
    if (target.origin !== origin) return;
    const route = target.pathname;
    events.set(request, {route, method: request.method(), kind: request.resourceType(), started: clock(),
      ...(target.searchParams.has('limit') ? {limit: target.searchParams.get('limit')} : {}),
      ...(target.searchParams.has('cursor') ? {has_cursor: true} : {})});
  });
  page.on('response', response => {
    const event = events.get(response.request());
    if (event) Object.assign(event, {status: response.status(), headers: clock()});
  });
  page.on('requestfinished', request => {
    const event = events.get(request);
    if (event) event.finished = clock();
  });
  page.on('requestfailed', request => {
    const event = events.get(request);
    if (event) event.failed = clock();
  });
  const rows = () => [...events.values()];
  return {rows, posts: () => rows().filter(row => row.method === 'POST' && row.route === commitRoute)};
}

function initializeTape(install, args) {
  // The geometry observer closes over these containers. Fill them after verifying the retained public head.
  const span = {};
  const siblings = [];
  install({...args, freeSpace: {span, siblings}});
  const tape = window.__p77DispatchTrace;
  if (!tape) return;
  tape.prepareSave = move => {
    const count = tape.counts['app:timeline_commit'];
    if (!tape.fullWritable() || tape.omitted || tape.armed || tape.pointer ||
        count.requested || count.responded || count.succeeded || count.failed) return false;
    Object.assign(span, move.span);
    siblings.push(...move.siblings);
    return true;
  };
}

function pointStaysOnSource(point, expected) {
  const row = expected.source_row;
  return Boolean(point?.in_source_row && point.hit_row === expected.hit_row &&
    point.scroll_left === expected.scroll_left && point.scroll_top === expected.scroll_top && row &&
    JSON.stringify(point.source_row) === JSON.stringify(row) &&
    point.viewport.width === expected.viewport.width && point.viewport.height === expected.viewport.height &&
    point.x > row.left && point.x < row.right && point.y > row.top && point.y < row.bottom);
}

async function obtainPublicHead(page, receipt, label) {
  const interval = receipt[label] = {start: clock()};
  try { return await bounded(120_000, () => publicSnapshot(page, origin, fixture)); }
  finally { interval.end = clock(); }
}

async function saveOnce({page, head, commitRequests, recorder, browserTimeOrigin, receipt}) {
  let phase = 'runtime_identity_before_save';
  let diskWatch, diskCheck, diskStop;
  try {
    receipt.runtime_before_save = await runtimeRootForData(root, data, runtimeHealthUrl);
    assert.deepEqual(receipt.runtime_before_save, runtime);
    phase = 'exact_head_geometry';
    assert.equal(recorder.posts().length, 0);
    assert.equal(commitRequests.size, 0);
    assert.equal(await page.evaluate(() => performance.timeOrigin), browserTimeOrigin, 'Editor document changed');
    const move = canonicalFreeSpace(head, clips, tracks);
    assert(!move.issue, move.issue);
    assert.deepEqual(move.target, target);
    assert.equal(move.span.start_seconds, expectedStartSeconds);
    receipt.baseline = headSummary(head);
    receipt.target = move.target;
    receipt.canonical = {span: move.span, siblings: move.siblings};
    assert(await page.evaluate(geometry => window.__p77DispatchTrace.prepareSave(geometry), receipt.canonical));
    const plan = await page.evaluate(async () => {
      const tape = window.__p77DispatchTrace;
      const preliminary = tape.planFreeSpace({scroll: true});
      if (preliminary.issue) return preliminary;
      await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
      return tape.planFreeSpace({scroll: false});
    });
    receipt.geometry = plan;
    assert(!plan.issue, plan.issue);
    assert(plan.x1 > plan.x0 && plan.desired_start_seconds > move.span.start_seconds);
    phase = 'before_pointer_geometry';
    const {x0, x1, y} = plan;
    await page.mouse.move(x0, y);
    const currentGeometry = () => page.evaluate(({x0, x1, y}) => {
      const tape = window.__p77DispatchTrace;
      return {source: tape.freeSpacePoint(x0, y), destination: tape.freeSpacePoint(x1, y),
        projection: tape.planFreeSpace({scroll: false}), writable: tape.fullWritable()};
    }, {x0, x1, y});
    const checkGeometry = observed => {
      assert(observed.writable && !observed.projection.issue && observed.projection.x0 === x0 &&
        observed.projection.x1 === x1 && observed.projection.y === y &&
        Math.abs(observed.projection.desired_start_seconds - plan.desired_start_seconds) < 1e-6 &&
        freeSpacePointsMatch(observed.source, plan.source) && freeSpacePointsMatch(observed.destination, plan.destination));
    };
    receipt.observed_before_down = await currentGeometry();
    checkGeometry(receipt.observed_before_down);
    phase = 'disk_before_move';
    receipt.disk_before = await diskFree();
    receipt.disk_before_human = execFileSync('df', ['-h', '--', ...diskPaths], {encoding: 'utf8', timeout: 3_000}).trim();
    assertDiskFree(receipt.disk_before);
    receipt.load_1m_gesture = loadavg()[0];
    phase = 'arm_single_pointer';
    assert.equal(commitRequests.size, 0);
    assert(await page.evaluate(armFreeSpace, {x: x0, y, clipId: move.target.clip_id, trackId: move.target.track_id}));
    phase = 'final_pointer_guard';
    receipt.observed_at_gesture = await currentGeometry();
    checkGeometry(receipt.observed_at_gesture);
    assert.equal(recorder.posts().length, 0);
    assert.equal(commitRequests.size, 0);
    receipt.disk_at_gesture = await diskFree();
    assertDiskFree(receipt.disk_at_gesture);
    await cpu();
    const watchDisk = async () => {
      let space;
      try {
        space = await diskFree();
        assertDiskFree(space);
      } catch (error) {
        diskStop = {at: clock(), error_kind: error?.name ?? 'Error', free: space ?? null};
        void page.close().catch(() => {});
      }
    };
    diskWatch = setInterval(() => {
      if (!diskCheck && !diskStop) diskCheck = watchDisk().finally(() => { diskCheck = null; });
    }, 500);
    receipt.reads_pending_at_gesture = recorder.rows().filter(row =>
      isScopedRead(row) && !row.finished && !row.failed).map(row => row.route);
    phase = 'pointerdown_scope';
    receipt.pointerdown_requested = clock();
    await page.mouse.down();
    receipt.observed_down = await page.evaluate(() => window.__p77DispatchTrace.pointer?.freeSpaceDown ?? null);
    assert(freeSpacePointsMatch(receipt.observed_down, plan.source));
    phase = 'pointermove_geometry';
    await page.mouse.move((x0 + x1) / 2, y, {steps: 4});
    await page.mouse.move(x1, y, {steps: 6});
    const moved = await page.evaluate(() => {
      const tape = window.__p77DispatchTrace;
      return {pointer: tape.pointer, omitted: tape.omitted, path: tape.rows.filter(row =>
        row.phase === 'pointermove' && row.at >= tape.pointer?.down).map(row => row.geometry)};
    });
    receipt.observed_drag = moved;
    assert(moved.pointer && !moved.pointer.cancelled && !moved.pointer.freeSpacePathInvalid &&
      !moved.omitted && moved.path.length > 0);
    let past = x0;
    for (const point of moved.path) {
      assert(point.x >= past && point.x <= x1 && point.y === y && pointStaysOnSource(point, plan.source));
      past = point.x;
    }
    assert(freeSpacePointsMatch(moved.pointer.freeSpaceMove, plan.destination));
    phase = 'pointerup_geometry';
    await page.mouse.up();
    const pointer = await page.evaluate(() => window.__p77DispatchTrace.pointer);
    receipt.observed_up = pointer?.freeSpaceUp ?? null;
    assert(Number.isFinite(pointer?.up) && freeSpacePointsMatch(receipt.observed_up, plan.destination));
    receipt.release = {monotonic_ms: pointer.up, epoch_ms: browserTimeOrigin + pointer.up};

    phase = 'save_settlement';
    let settleFailure;
    try {
      await page.waitForFunction(() => {
        const tape = window.__p77DispatchTrace;
        const response = tape.rows.find(row => row.at >= tape.pointer.up && row.phase === 'fetch-response' &&
          row.endpoint === 'timeline_commit' && row.status === 200);
        return (response && tape.rows.some(row => row.at >= response.at && row.phase === 'badge' && row.state === 'saved')) ||
          tape.readBadge().kind === 'refused';
      }, null, {timeout: 90_000, polling: 100});
    } catch (error) { settleFailure = error; }
    const tape = await page.evaluate(() => {
      const trace = window.__p77DispatchTrace;
      return {rows: trace.rows, badge: trace.readBadge(), count: trace.counts['app:timeline_commit'], omitted: trace.omitted};
    });
    const scoped = tape.rows.filter(row => row.at >= pointer.up && row.endpoint === 'timeline_commit');
    const requests = scoped.filter(row => row.phase === 'fetch-request');
    const [request] = requests;
    const response = scoped.find(row => row.phase === 'fetch-response' && row.request === request?.request);
    const saved = response && tape.rows.find(row => row.at >= response.at && row.phase === 'badge' && row.state === 'saved');
    const browserClock = row => row ? {monotonic_ms: row.at, epoch_ms: browserTimeOrigin + row.at} : null;
    const phases = new Set(['schedule', 'capture-called', 'capture-resolved', 'capture-rejected', 'handoff-ready',
      'outbox-append-start', 'outbox-append-persisted', 'pump-enter', 'pump-record-read', 'pump-ready-for-dispatch',
      'fetch-request', 'fetch-response', 'badge']);
    const handoff = tape.rows.findLast(row => row.phase === 'handoff-ready' && row.at <= pointer.up);
    receipt.save = {gesture_to_post_ms: request ? request.at - pointer.up : null,
      post_to_response_ms: response && request ? response.at - request.at : null,
      response_to_saved_ms: saved ? saved.at - response.at : null, http_status: response?.status ?? null,
      post: browserClock(request), http_200: response?.status === 200 ? browserClock(response) : null,
      saved: browserClock(saved), badge: tape.badge, commit_count: tape.count,
      last_pre_release_handoff_ms: handoff ? handoff.at - pointer.up : null,
      editor_trace: tape.rows.filter(row => row.at >= pointer.up && phases.has(row.phase) &&
        (!row.endpoint || row.endpoint === 'timeline_commit')).map(row => ({phase: row.phase,
        ms_after_release: row.at - pointer.up, status: row.status, state: row.state}))};
    if (settleFailure) throw settleFailure;
    assert(!tape.omitted && requests.length === 1 && response?.status === 200 && saved && tape.badge.state === 'saved');
    assert.deepEqual(tape.count, {requested: 1, responded: 1, succeeded: 1, failed: 0});

    phase = 'accepted_public_head';
    const after = await obtainPublicHead(page, receipt, 'accepted_public_proof');
    receipt.public_after = headSummary(after);
    const [commit] = commitRequests.values();
    receipt.save.commit_wire = [...commitRequests.values()];
    assert(recorder.posts().length === 1 && commitRequests.size === 1 && commit.status === 200 &&
      commit.outcome === 'accepted' && commit.exactCas && commit.exactAcceptedCas && commit.receipt);
    assert(after.headRevision !== head.headRevision && after.publicationId !== head.publicationId);
    verifyScopedHead(after, {revision_id: commit.receipt.revision, publication_id: commit.receipt.publication,
      content_digest: commit.receipt.content_digest});
    const afterClip = after.payload.config.clips.find(clip => clip.id === move.target.clip_id);
    assert(afterClip?.track === move.target.track_id && afterClip.at > move.span.start_seconds &&
      afterClip.at + move.span.duration_seconds < plan.visible_time_bounds_seconds[1] &&
      Math.abs(afterClip.at - plan.desired_start_seconds) <= 2 / plan.pixels_per_second + 0.002);
    assert(exactFreeSpaceDiff(head, after, {clip: move.target.clip_id, to_seconds: afterClip.at}));
    receipt.accepted = headSummary(after);
    receipt.accepted_start_s = afterClip.at;
    assert.equal(await page.evaluate(() => performance.timeOrigin), browserTimeOrigin, 'Editor document changed');
    await cpu();
    clearInterval(diskWatch);
    await diskCheck;
    assert(!diskStop);
    phase = 'verified';
  } catch (error) {
    receipt.error_phase = phase;
    receipt.error_kind = error?.name ?? 'Error';
    throw error;
  } finally {
    clearInterval(diskWatch);
    await diskCheck;
    if (diskStop) receipt.disk_stop = diskStop;
    receipt.phase = phase;
    receipt.commit_wire = [...commitRequests.values()];
    receipt.wire_request = recorder.posts()[0] ?? null;
    receipt.timeline_commit_posts = recorder.posts().length;
    await writeReceipt('save-1', receipt);
  }
}

function isScopedRead(row) {
  return row.method === 'GET' && (row.route === scopedProject || row.route.startsWith(scopedProject + '/') ||
    row.route === '/api/runtime/v1/projects/selection');
}

const traceFaults = new Set(['trace_connection_rebound', 'bounded_output_overflow', 'trace_output_failure',
  'transaction_scope_mismatch', 'unknown_sql_attempt', 'unknown_trace_event']);
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

async function readTraceEnvelopes(tracePath) {
  const info = await lstat(tracePath);
  assert(info.isFile() && !info.isSymbolicLink() && (info.mode & 0o077) === 0);
  assert(info.size > 0 && info.size <= 2_100_000);
  // The last element is empty or a line still being written; only newline-terminated lines are parsed.
  const lines = (await readFile(tracePath, 'utf8')).split('\n').slice(0, -1).filter(Boolean);
  return lines.map(line => JSON.parse(line));
}

async function requireTraceWitness(context) {
  const tracePath = process.env.P77_SV2A_TRACE_PATH;
  assert.equal(tracePath, path.join(output, 'timeline-memo-trace.jsonl'));
  const route = scopedTimeline + '/commits?limit=1';
  const beforeRead = clock();
  const response = await context.request.get(origin + route, {
    headers: {'Cache-Control': 'no-cache'}, maxRedirects: 0, timeout: 120_000,
  });
  assert.equal(response.status(), 200, 'Authenticated history witness failed');
  const history = await response.json();
  const completedRead = clock();
  assert.deepEqual(history.head, {revision_id: pin.revision_id, publication_id: pin.publication_id});
  assert.equal(history.items.length, 1);
  assert.equal(history.items[0].revision_id, pin.revision_id);
  assert.equal(history.items[0].publication_id, pin.publication_id);
  // request_started does not flush, so poll the trace file for a bounded time for the history request scope.
  const deadline = performance.now() + 10_000;
  let marker, scope, seen;
  for (;;) {
    let envelopes = [];
    try { envelopes = await readTraceEnvelopes(tracePath); }
    catch (error) { if (error?.code !== 'ENOENT') throw error; }
    const events = envelopes.flatMap(item => item.events);
    for (const item of envelopes) {
      assert.equal(item.schema, 'timeline-memo-provenance-v1');
      assert.equal(item.overflow, false);
      assert.equal(item.unknown, false);
    }
    assert(!events.some(event => traceFaults.has(event.kind)), 'Trace holds a rebound, overflow or unknown event');
    assert(!events.some(event => event.kind === 'request_scope_started' && event.route === 'timeline_commit_post'),
      'A commit request scope exists before the save');
    if (envelopes.length) {
      marker = events[0];
      assert.equal(marker.kind, 'trace_runtime_source');
      assert.equal(marker.pid, candidate.pid);
      assert.equal(marker.module_file, preflight.module_proofs.runtime_protocol.file);
      assert.equal(marker.module_file, path.join(preflight.archive, 'runtime_protocol/__init__.py'));
    }
    const scopes = events.filter(event => event.kind === 'request_scope_started' && event.route === 'timeline_history_get');
    seen = {envelopes: envelopes.length, events: events.length, history_scopes: scopes.length};
    assert(scopes.length <= 1, 'More than one history request scope before the save');
    if (scopes.length) { [scope] = scopes; break; }
    if (performance.now() > deadline) break;
    await sleep(250);
  }
  if (!scope) {
    await writeReceipt('trace-witness-failure', {route, http_status: 200, before_read: beforeRead,
      completed_read: completedRead, seen, reason: 'No request_scope_started witness for timeline_history_get within 10 s. ' +
      'Nothing was navigated or written.'});
    throw new Error('Trace request witness absent');
  }
  return {route, http_status: 200, head: history.head, before_read: beforeRead,
    completed_read: completedRead, trace_schema: 'timeline-memo-provenance-v1', marker, request_scope: scope, seen};
}

const profile = await mkdtemp(path.join(browserParent, 'profile-'));
const receipt = {mode, tuple, runtime, candidate, disk_floor_bytes: Number(diskFloorBytes), node_time_origin: performance.timeOrigin,
  load_1m_start: loadavg()[0], saves: []};
let context, recorder;
let phase = 'browser_launch';
try {
  context = await chromium.launchPersistentContext(profile, {executablePath: process.env.SAVE_LOOP_CHROME,
    headless: true, viewport: {width: 1700, height: 1500}, args: ['--disable-gpu', '--no-first-run',
      '--disk-cache-size=1', '--media-cache-size=1', '--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE 127.0.0.1']});
  phase = 'trace_witness';
  receipt.trace_witness = await requireTraceWitness(context);
  await writeReceipt('trace-before-save', receipt.trace_witness);
  const page = context.pages()[0] ?? await context.newPage();
  recorder = observeRequests(page);
  const expectedCas = {headRevision: pin.revision_id, publicationId: pin.publication_id};
  const commitRequests = wireCommits(page, commitUrl, fixture, expectedCas, true);
  const tapeConfig = {timelineKey, projectKey, clipId: target.clip_id, trackId: target.track_id,
    warmScope: pin, compiledFixture: {clips, tracks}};
  await page.addInitScript({content: `(${initializeTape})(${browserTape}, ${JSON.stringify(tapeConfig)});`});
  phase = 'opening';
  const openingCpu = await cpu();
  receipt.navigation = clock();
  await page.goto(url.href, {waitUntil: 'commit', timeout: 120_000});
  const navMs = performance.now() - receipt.navigation.monotonic_ms;
  const writable = await page.waitForFunction(() => {
    const tape = window.__p77DispatchTrace;
    if (!tape?.fullWritable()) return false;
    tape.watchBadge();
    return {monotonic_ms: performance.now(), time_origin: performance.timeOrigin};
  }, null, {timeout: Math.max(1, 900_000 - Math.ceil(navMs))});
  receipt.writable = await writable.jsonValue();
  receipt.writable_observed = clock();
  receipt.opening_runtime_cpu_seconds = (await cpu()) - openingCpu;
  const browserTimeOrigin = receipt.writable.time_origin;
  const openingRows = recorder.rows();
  receipt.reads_pending_at_writable = openingRows.filter(row => isScopedRead(row) && !row.finished && !row.failed).map(row => row.route);
  phase = 'authoring_route';
  assert(openingRows.some(row => row.method === 'GET' && row.route === scopedTimeline + '/verified-head' && row.status === 200));
  assert(!openingRows.some(row => row.method === 'GET' && row.route === scopedTimeline + '/commits'));
  phase = 'compiled_bytes';
  const scripts = openingRows.filter(row => row.kind === 'script');
  assert(!scripts.some(row => /^\/(src|@vite|node_modules)\//.test(row.route)));
  const bundle = scripts.find(row => /^\/assets\/[\w.-]+\.js$/.test(row.route) && row.status === 200);
  assert(bundle);
  await verifyServedAsset(context, bundle.route);
  receipt.compiled_asset = bundle.route;
  phase = 'original_public_proof';
  const head = await obtainPublicHead(page, receipt, 'initial_public_proof');
  verifyScopedHead(head, pin);
  receipt.original = headSummary(head);
  phase = 'save_1';
  const saveReceipt = {ordinal: 1, runtime, candidate, browser_time_origin: browserTimeOrigin};
  receipt.saves.push(saveReceipt);
  await saveOnce({page, head, commitRequests, recorder, browserTimeOrigin, receipt: saveReceipt});
  assert.equal(recorder.posts().length, 1);
  phase = 'verified';
} catch (error) {
  receipt.error_phase = phase;
  receipt.error_kind = error?.name ?? 'Error';
  process.exitCode = 1;
} finally {
  receipt.phase = phase;
  receipt.stopped = clock();
  try { await context?.close(); }
  catch (error) {
    receipt.context_close_error = error?.name ?? 'Error';
    process.exitCode = 1;
  }
  finally { await rm(profile, {recursive: true, force: true}); }
  receipt.profile_removed = await lstat(profile).then(() => false, error => error?.code === 'ENOENT');
  receipt.timeline_commit_posts = recorder?.posts().length ?? 0;
  receipt.requests = recorder?.rows() ?? [];
  if (receipt.phase === 'verified' && (receipt.context_close_error || !receipt.profile_removed || receipt.timeline_commit_posts !== 1)) {
    receipt.phase = 'cleanup_proof_failed';
    process.exitCode = 1;
  }
  await writeReceipt('browser-sv2a-first-save', receipt);
}
