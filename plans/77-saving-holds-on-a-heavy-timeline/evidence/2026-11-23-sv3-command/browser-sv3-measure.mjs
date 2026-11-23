// SV-3 measurement driver: one fresh browser profile per repetition.
// Scenario order per repetition: S0 (page load), cold, S1, S2, S2o, S3, S3o, S4.
// Adapted from browser-sv2a-first-save.mjs (geometry, public head) and browser-two-save-profile.mjs (the
// prepare/arm/reset protocol and per-save timing). The trace witness, the trace verdict and the Runtime sampler are not used.
// Static-checked only in this package.
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
const {runtime_sha: runtimeSha, pid, start, instance} = preflight;
assert.equal(runtimeSha, tuple.runtime);
assert(Number.isSafeInteger(pid) && pid > 0);
assert.match(start, /^\d+$/);
assert.match(instance, /^[a-f0-9]+$/);
await assert.rejects(lstat(path.join(output, 'browser-sv3-measure.json')), {code: 'ENOENT'});

const loadModule = location => import(pathToFileURL(location));
const {chromium} = await loadModule(process.env.SAVE_LOOP_PLAYWRIGHT);
const {publicSnapshot} = await loadModule(path.join(tools, 'scripts/save-loop/assert.mjs'));
const {parseStat} = await loadModule(path.join(tools, 'scripts/save-loop/cpu.mjs'));
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
const verifiedHeadRoute = scopedTimeline + '/verified-head';
const commitRoute = scopedTimeline + '/commit';
const commitUrl = origin + commitRoute;
const url = new URL('/tools/video-editor', origin);
url.searchParams.set('connect', '1');
url.searchParams.set('project', project);
url.searchParams.set('timeline', timeline);
const runtimeHealthUrl = origin + '/api/runtime/v1/health';

// Identity of the one live owner, from the copied data root's discovery record, the proxy health and the owner's
// /proc start time. runtimeRootForData is not used: it requires the data root inside the owned stack root.
async function runtimeIdentity() {
  const discovery = JSON.parse(await readFile(path.join(data, 'runtime/discovery.json'), 'utf8'));
  assert.equal(discovery.pid, pid, 'discovery pid changed');
  assert.equal(discovery.runtime_instance_id, instance, 'discovery instance changed');
  const sample = parseStat(await readFile(`/proc/${pid}/stat`, 'utf8'));
  assert.equal(sample.start, start, 'Runtime process changed');
  const health = await fetch(runtimeHealthUrl, {headers: {accept: 'application/json'}, cache: 'no-store',
    redirect: 'manual', signal: AbortSignal.timeout(3000)});
  assert(health.ok && !health.redirected, 'proxy health did not respond');
  const body = await health.json();
  assert(body.status === 'ok' && body.protocol === 'workspace.v1' && body.runtime_instance_id === instance);
}

const ticks = Number(execFileSync('getconf', ['CLK_TCK'], {encoding: 'utf8'}).trim());
assert(Number.isFinite(ticks) && ticks > 0);
async function cpu() {
  const sample = parseStat(await readFile(`/proc/${pid}/stat`, 'utf8'));
  assert.equal(sample.start, start, 'Runtime process changed');
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
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
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

// Reduce a non-2xx body to the fields the receipts need. The body is local Runtime output, kept short.
function refusalFields(text) {
  let json = null;
  try { json = JSON.parse(text); } catch { json = null; }
  const reason = json?.reason ?? json?.error?.reason ?? json?.error?.code ?? json?.code ?? json?.error ?? null;
  const code = json?.code ?? json?.error?.code ?? null;
  return {reason: typeof reason === 'string' ? reason : (reason === null ? null : JSON.stringify(reason).slice(0, 200)),
    body_code: typeof code === 'string' ? code : null, excerpt: text.slice(0, 300)};
}

function observeRequests(page) {
  const events = new Map();
  const bodies = [];
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
    if (!event) return;
    const status = response.status();
    Object.assign(event, {status, headers: clock()});
    if (!(status >= 200 && status < 300) && event.route.startsWith('/api/runtime')) {
      bodies.push(response.text()
        .then(text => Object.assign(event, {body: refusalFields(text)}))
        .catch(error => Object.assign(event, {body: {unreadable: error?.name ?? 'Error'}})));
    }
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
  return {rows, posts: () => rows().filter(row => row.method === 'POST' && row.route === commitRoute),
    settle: () => Promise.allSettled(bodies)};
}

// Arm and reset protocol, matching browser-two-save-profile.mjs (prepareSave) for every drag:
// - prepareSave(move, expected): the first drag of the session needs an idle tape (not armed, no pointer). Every later
//   drag needs the previous drag's arm and released pointer, and the previous counts (one requested, responded and
//   succeeded). It consumes both: armed=false, pointer=null, counts reset. armFreeSpace then needs armed=false.
// - prepareOverlapped(move): for a drag released while an earlier save may still be in flight, and after a failed drag.
//   It consumes the previous arm and pointer and resets the counts (armFreeSpace needs requested===0). It does not
//   check the earlier counts, so it is the path where the protocol is NOT established by a receipt.
function initializeTape(install, args) {
  const span = {};
  const siblings = [];
  install({...args, freeSpace: {span, siblings}});
  const tape = window.__p77DispatchTrace;
  if (!tape) return;
  const consume = move => {
    Object.assign(span, move.span);
    siblings.splice(0, siblings.length, ...move.siblings);
    tape.armed = false;
    tape.pointer = null;
    tape.counts['app:timeline_commit'] = {requested: 0, responded: 0, succeeded: 0, failed: 0};
    return true;
  };
  tape.prepareSave = (move, expected) => {
    const count = tape.counts['app:timeline_commit'];
    if (!tape.fullWritable() || tape.omitted || count.requested !== expected || count.responded !== expected ||
        count.succeeded !== expected || count.failed ||
        (expected ? !(tape.armed && Number.isFinite(tape.pointer?.up)) : (tape.armed || tape.pointer))) return false;
    return consume(move);
  };
  tape.prepareOverlapped = move => {
    if (!tape.fullWritable() || tape.omitted || !(tape.armed && Number.isFinite(tape.pointer?.up))) return false;
    return consume(move);
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

async function obtainPublicHead(page, label, receipt) {
  const interval = receipt[label] = {start: clock()};
  try { return await bounded(120_000, () => publicSnapshot(page, origin, fixture)); }
  finally { interval.end = clock(); }
}

function isScopedRead(row) {
  return row.method === 'GET' && (row.route === scopedProject || row.route.startsWith(scopedProject + '/') ||
    row.route === '/api/runtime/v1/projects/selection');
}

// Predicted move for an overlapped drag: the clip's start after the previous, in-flight drag. Span and siblings
// are unchanged, the target is unchanged. Whether the editor's rendered projection agrees is NOT established.
function predictMove(move0, startSeconds) {
  const span = {...move0.span, start_seconds: startSeconds, end_seconds: startSeconds + move0.span.duration_seconds};
  return {...move0, span};
}

// One drag: prepare, plan, arm, press, move, release. Returns the release and the plan. Does not wait for Saved.
async function gesture({page, move, plan0, prepareKind, record, cold, expectedCas, head, commitRequests}) {
  let phase = 'identity_before_drag';
  let diskWatch, diskCheck, diskStop;
  try {
    await runtimeIdentity();
    assert.equal(await page.evaluate(() => performance.timeOrigin), record.browserTimeOrigin, 'Editor document changed');
    phase = 'exact_head_geometry';
    assert(!move.issue, move.issue);
    if (cold) assert.equal(move.span.start_seconds, expectedStartSeconds);
    record.target = move.target;
    record.start_before_s = move.span.start_seconds;
    Object.assign(expectedCas, {headRevision: head.headRevision, publicationId: head.publicationId});
    phase = 'prepare';
    const prepared = prepareKind.kind === 'strict'
      ? await page.evaluate(({move, expected}) => window.__p77DispatchTrace.prepareSave(move, expected),
        {move, expected: prepareKind.expected})
      : await page.evaluate(move => window.__p77DispatchTrace.prepareOverlapped(move), move);
    record.prepare = prepared ? prepareKind.kind : 'refused_by_tape';
    assert(prepared, 'tape refused the prepare step');
    const plan = await page.evaluate(async () => {
      const tape = window.__p77DispatchTrace;
      const preliminary = tape.planFreeSpace({scroll: true});
      if (preliminary.issue) return preliminary;
      await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
      return tape.planFreeSpace({scroll: false});
    });
    record.geometry = plan;
    assert(!plan.issue, plan.issue);
    assert(plan.x1 > plan.x0 && plan.desired_start_seconds > move.span.start_seconds);
    record.dx_px = plan.dx;
    record.pixels_per_second = plan.pixels_per_second;
    record.planned_start_s = plan.desired_start_seconds;
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
    checkGeometry(await currentGeometry());
    phase = 'disk_before_move';
    assertDiskFree(await diskFree());
    record.load_1m = loadavg()[0];
    phase = 'arm_single_pointer';
    assert(await page.evaluate(armFreeSpace, {x: x0, y, clipId: move.target.clip_id, trackId: move.target.track_id}));
    phase = 'final_pointer_guard';
    checkGeometry(await currentGeometry());
    assertDiskFree(await diskFree());
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
    phase = 'pointerdown';
    await page.mouse.down();
    const down = await page.evaluate(() => window.__p77DispatchTrace.pointer?.freeSpaceDown ?? null);
    assert(freeSpacePointsMatch(down, plan.source));
    phase = 'pointermove_geometry';
    await page.mouse.move((x0 + x1) / 2, y, {steps: 4});
    await page.mouse.move(x1, y, {steps: 6});
    const moved = await page.evaluate(() => {
      const tape = window.__p77DispatchTrace;
      return {pointer: tape.pointer, omitted: tape.omitted, path: tape.rows.filter(row =>
        row.phase === 'pointermove' && row.at >= tape.pointer?.down).map(row => row.geometry)};
    });
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
    assert(Number.isFinite(pointer?.up) && freeSpacePointsMatch(pointer.freeSpaceUp, plan.destination));
    record.release_monotonic_ms = pointer.up;
    record.up = pointer.up;
    record.release_epoch_ms = record.browserTimeOrigin + pointer.up;
    phase = 'released';
    return {up: pointer.up, plan, move};
  } catch (error) {
    record.failed_phase = phase;
    throw error;
  } finally {
    clearInterval(diskWatch);
    await diskCheck;
    if (diskStop) record.disk_stop = diskStop;
  }
}

// Waits, bounded, until the requests after `up` have responded and the badge is saved or refused. Returns the rows.
async function settle(page, up, minRequests, timeoutMs) {
  await page.waitForFunction(({up, minRequests}) => {
    const tape = window.__p77DispatchTrace;
    const rows = tape.rows.filter(row => row.at >= up && row.endpoint === 'timeline_commit');
    const requests = rows.filter(row => row.phase === 'fetch-request').length;
    const responses = rows.filter(row => row.phase === 'fetch-response').length;
    const badge = tape.readBadge();
    return requests >= minRequests && responses >= requests && (badge.state === 'saved' || badge.kind === 'refused');
  }, {up, minRequests}, {timeout: timeoutMs, polling: 100});
}

// Attribution of the requests after the first release, in order. If the POST count differs from the drag count, the
// requests are NOT attributed to drags: the editor may have coalesced edits, and only the counts are recorded.
async function attribute(page, ups, recorder, postsStart) {
  const observed = await page.evaluate(first => {
    const tape = window.__p77DispatchTrace;
    const rows = tape.rows.filter(row => row.at >= first);
    return {
      badge: tape.readBadge(), count: tape.counts['app:timeline_commit'], omitted: tape.omitted,
      requests: rows.filter(row => row.phase === 'fetch-request' && row.endpoint === 'timeline_commit')
        .map(row => ({at: row.at, request: row.request})),
      responses: rows.filter(row => row.phase === 'fetch-response' && row.endpoint === 'timeline_commit')
        .map(row => ({at: row.at, request: row.request, status: row.status})),
      saved: rows.filter(row => row.phase === 'badge' && row.state === 'saved').map(row => row.at),
      refusedBadge: rows.filter(row => row.phase === 'badge' && row.state !== 'saved').map(row => row.at),
    };
  }, ups[0]);
  const posts = recorder.posts().slice(postsStart);
  const mapped = observed.requests.length === ups.length;
  const out = ups.map((up, k) => {
    if (!mapped) return {mapped: false};
    const request = observed.requests[k];
    const response = observed.responses.find(row => row.request === request.request);
    const saved = response ? observed.saved.find(at => at >= response.at) : undefined;
    const post = posts[k];
    return {mapped: true, request, response, saved,
      post_status: post?.status ?? null, refusal_body: post?.body ?? null};
  });
  return {observed: {requests: observed.requests.length, responses: observed.responses.length,
    badge: observed.badge, count: observed.count, omitted: observed.omitted}, posts: posts.length, attributed: out};
}

function timingFrom(up, attributed, browserTimeOrigin) {
  if (!attributed.mapped) return {mapped: false};
  const {request, response, saved} = attributed;
  return {
    mapped: true,
    release_to_post_ms: request ? request.at - up : null,
    post_to_200_ms: response && request ? response.at - request.at : null,
    response_to_saved_ms: saved !== undefined && response ? saved - response.at : null,
    http_status: response?.status ?? null,
    release_to_saved_ms: (saved !== undefined && response && request) ? (request.at - up) + (response.at - request.at) + (saved - response.at) : null,
    post_to_saved_ms: (saved !== undefined && response && request) ? (response.at - request.at) + (saved - response.at) : null,
    release_epoch_ms: browserTimeOrigin + up,
  };
}

const profile = await mkdtemp(path.join(browserParent, 'profile-'));
const receipt = {mode, tuple, runtime_sha: runtimeSha, data_root: data, candidate: {pid, start, instance},
  disk_floor_bytes: Number(diskFloorBytes), node_time_origin: performance.timeOrigin, load_1m_start: loadavg()[0],
  scenarios: [], s0: null, refusals: [], non_2xx_runtime: [], failed_drags: 0};
// Order per repetition. Overlapped scenarios release the next edit without waiting for Saved.
const scenarios = [
  {name: 'cold', mode: 'sequential', warm: false, drags: 1, gap_ms: 0},
  {name: 'S1', mode: 'sequential', warm: true, drags: 1, gap_ms: 0},
  {name: 'S2', mode: 'sequential', warm: true, drags: 2, gap_ms: 200},
  {name: 'S2o', mode: 'overlapped', warm: true, drags: 2, gap_ms: 150},
  {name: 'S3', mode: 'sequential', warm: true, drags: 10, gap_ms: 150},
  {name: 'S3o', mode: 'overlapped', warm: true, drags: 10, gap_ms: 150},
  {name: 'S4', mode: 'sequential', warm: true, drags: 5, gap_ms: 0},
];
let context, recorder;
let phase = 'browser_launch';
try {
  await runtimeIdentity();
  context = await chromium.launchPersistentContext(profile, {executablePath: process.env.SAVE_LOOP_CHROME,
    headless: true, viewport: {width: 1700, height: 1500}, args: ['--disable-gpu', '--no-first-run',
      '--disk-cache-size=1', '--media-cache-size=1', '--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE 127.0.0.1']});
  const page = context.pages()[0] ?? await context.newPage();
  recorder = observeRequests(page);
  const expectedCas = {headRevision: pin.revision_id, publicationId: pin.publication_id};
  const commitRequests = wireCommits(page, commitUrl, fixture, expectedCas, true);
  const tapeConfig = {timelineKey, projectKey, clipId: target.clip_id, trackId: target.track_id,
    warmScope: pin, compiledFixture: {clips, tracks}};
  await page.addInitScript({content: `(${initializeTape})(${browserTape}, ${JSON.stringify(tapeConfig)});`});
  // S0: page load is the first browser action. It ends when the editor is writable.
  phase = 'S0_page_load';
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
  const writableValue = await writable.jsonValue();
  await recorder.settle();
  const openingRows = recorder.rows();
  const verifiedHead = openingRows.find(row => row.method === 'GET' && row.route === verifiedHeadRoute);
  receipt.s0 = {
    navigation_to_writable_ms: (writableValue.time_origin + writableValue.monotonic_ms) - receipt.navigation.epoch_ms,
    opening_runtime_cpu_seconds: (await cpu()) - openingCpu,
    verified_head: verifiedHead ? {status: verifiedHead.status ?? null,
      requested_ms: verifiedHead.started.epoch_ms - receipt.navigation.epoch_ms,
      completed_ms: verifiedHead.finished ? verifiedHead.finished.epoch_ms - receipt.navigation.epoch_ms : null,
      body: verifiedHead.body ?? null} : null,
    refusal: Boolean(verifiedHead && (verifiedHead.status === 409 || verifiedHead.body?.reason === 'head_busy')),
    reads_pending_at_writable: openingRows.filter(row => isScopedRead(row) && !row.finished && !row.failed).map(row => row.route),
  };
  const browserTimeOrigin = writableValue.time_origin;
  receipt.writable = writableValue;
  phase = 'authoring_route';
  assert(openingRows.some(row => row.method === 'GET' && row.route === verifiedHeadRoute && row.status === 200));
  assert(!openingRows.some(row => row.method === 'GET' && row.route === scopedTimeline + '/commits'));
  phase = 'compiled_bytes';
  const scripts = openingRows.filter(row => row.kind === 'script');
  assert(!scripts.some(row => /^\/(src|@vite|node_modules)\//.test(row.route)));
  const bundle = scripts.find(row => /^\/assets\/[\w.-]+\.js$/.test(row.route) && row.status === 200);
  assert(bundle);
  await verifyServedAsset(context, bundle.route);
  receipt.compiled_asset = bundle.route;
  phase = 'original_public_proof';
  let head = await obtainPublicHead(page, 'initial_public_proof', receipt);
  verifyScopedHead(head, pin);
  receipt.original = headSummary(head);

  let sessionDrags = 0;
  let lastOk = true;
  for (const scenario of scenarios) {
    phase = `scenario_${scenario.name}`;
    const result = {name: scenario.name, mode: scenario.mode, warm: scenario.warm, drags: [], settle_ms: 2000};
    const postsBefore = recorder.posts().length;
    const expectedCas = {headRevision: head.headRevision, publicationId: head.publicationId};
    if (scenario.mode === 'sequential') {
      for (let i = 0; i < scenario.drags; i += 1) {
        const record = {index: i, mode: 'sequential', cold: scenario.name === 'cold' && i === 0, browserTimeOrigin,
          failed: false, lastOk_before: lastOk};
        const prepareKind = lastOk ? {kind: 'strict', expected: sessionDrags > 0 ? 1 : 0} : {kind: 'reset'};
        const postsStart = recorder.posts().length;
        let timing = {mapped: false};
        try {
          const move = canonicalFreeSpace(head, clips, tracks);
          commitRequests.clear();
          const g = await gesture({page, move, plan0: null, prepareKind, record, cold: record.cold, expectedCas, head,
            commitRequests});
          sessionDrags += 1;
          await settle(page, g.up, 1, 90_000);
          const tape = await attribute(page, [g.up], recorder, postsStart);
          timing = timingFrom(g.up, tape.attributed[0], browserTimeOrigin);
          record.attribution = {observed: tape.observed, posts: tape.posts};
          if (!timing.mapped || timing.http_status !== 200) throw new Error(`commit not accepted (status ${timing.http_status ?? 'none'})`);
          phase = 'accepted_public_head';
          const after = await obtainPublicHead(page, 'accepted_public_proof', record);
          const [commit] = commitRequests.values();
          assert(commit && commit.status === 200 && commit.outcome === 'accepted' && commit.exactCas && commit.exactAcceptedCas && commit.receipt);
          verifyScopedHead(after, {revision_id: commit.receipt.revision, publication_id: commit.receipt.publication,
            content_digest: commit.receipt.content_digest});
          assert(exactFreeSpaceDiff(head, after, {clip: move.target.clip_id,
            to_seconds: after.payload.config.clips.find(clip => clip.id === move.target.clip_id).at}));
          record.accepted_start_s = after.payload.config.clips.find(clip => clip.id === move.target.clip_id).at;
          head = after;
          lastOk = true;
        } catch (error) {
          record.failed = true;
          record.failed_reason = String(error?.message ?? error).slice(0, 300);
          record.error_kind = error?.name ?? 'Error';
          lastOk = false;
          sessionDrags += 1;
          const post = recorder.posts()[postsStart];
          if (post?.body) record.refusal = post.body;
          if (post && post.status && post.status !== 200) record.refusal = {...(post.body ?? {}), http_status: post.status};
          try {
            const refreshed = await bounded(60_000, () => publicSnapshot(page, origin, fixture));
            if (refreshed.headRevision !== head.headRevision) head = refreshed;
          } catch { /* keep the last verified head */ }
          receipt.failed_drags += 1;
        }
        Object.assign(record, timing);
        record.post_count_network = recorder.posts().length - postsStart;
        if (record.refusal || record.failed) receipt.refusals.push({scenario: scenario.name, index: i, ...(record.refusal ?? {}),
          failed_reason: record.failed_reason ?? null});
        result.drags.push(record);
        if (i < scenario.drags - 1) await sleep(scenario.gap_ms);
      }
      await sleep(2000);
    } else {
      // Overlapped chain: each edit is released without waiting for Saved. Attribution and Saved are read afterwards.
      const ups = [];
      const chainPostsStart = recorder.posts().length;
      const move0 = canonicalFreeSpace(head, clips, tracks);
      assert(!move0.issue, move0.issue);
      let predicted = move0.span.start_seconds;
      for (let i = 0; i < scenario.drags; i += 1) {
        const record = {index: i, mode: 'overlapped', cold: false, browserTimeOrigin, failed: false};
        const prepareKind = {kind: 'overlapped'};
        const move = predictMove(move0, predicted);
        try {
          const g = await gesture({page, move, plan0: null, prepareKind, record, cold: false, expectedCas, head,
            commitRequests});
          ups.push(g.up);
          predicted = g.plan.desired_start_seconds;
          sessionDrags += 1;
        } catch (error) {
          record.failed = true;
          record.failed_reason = String(error?.message ?? error).slice(0, 300);
          record.error_kind = error?.name ?? 'Error';
          receipt.failed_drags += 1;
        }
        result.drags.push(record);
        if (i < scenario.drags - 1) await sleep(scenario.gap_ms);
      }
      if (ups.length) {
        phase = `settle_${scenario.name}`;
        try { await settle(page, ups[0], 1, 180_000); }
        catch (error) { receipt.overlap_settle_error = error?.name ?? 'Error'; }
        await sleep(2000);
        const tape = await attribute(page, ups, recorder, chainPostsStart);
        result.posts_observed_by_tape = tape.observed.requests;
        result.coalesced = tape.observed.requests !== ups.length;
        let k = 0;
        for (const record of result.drags) {
          if (record.failed || record.up === undefined) continue;
          const timing = timingFrom(ups[k], tape.attributed[k], browserTimeOrigin);
          Object.assign(record, timing);
          record.attribution_mapped = timing.mapped;
          k += 1;
        }
        // Coalesced or dropped drags keep null timings (attribution_mapped false) and are only counted.
        head =await bounded(120_000, () => publicSnapshot(page, origin, fixture));
        result.accepted_after_chain = headSummary(head);
      }
      await sleep(2000);
      lastOk = result.drags.every(record => !record.failed);
    }
    result.posts_network = recorder.posts().length - postsBefore;
    result.n_drags = result.drags.length;
    result.n_failed = result.drags.filter(record => record.failed).length;
    receipt.scenarios.push(result);
  }
  phase = 'verified';
} catch (error) {
  receipt.error_phase = phase;
  receipt.error_kind = error?.name ?? 'Error';
  receipt.error_message = String(error?.message ?? error).slice(0, 300);
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
  if (recorder) await recorder.settle();
  receipt.timeline_commit_posts = recorder?.posts().length ?? 0;
  receipt.non_2xx_runtime = (recorder?.rows() ?? []).filter(row => row.route?.startsWith('/api/runtime') &&
    row.status !== undefined && !(row.status >= 200 && row.status < 300))
    .map(row => ({method: row.method, route: row.route, status: row.status, body: row.body ?? null}));
  receipt.refusal_count = receipt.refusals.length + (receipt.s0?.refusal ? 1 : 0) +
    receipt.non_2xx_runtime.filter(row => row.status === 409 || row.body?.reason === 'head_busy').length;
  receipt.requests = recorder?.rows() ?? [];
  await writeReceipt('browser-sv3-measure', receipt);
}
