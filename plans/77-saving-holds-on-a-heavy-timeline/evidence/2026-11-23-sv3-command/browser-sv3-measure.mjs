// SV-3 measurement driver: one fresh browser profile per repetition, scenarios S0, cold, S1-S4.
// Static-checked only in this package. Adapted from browser-sv2a-first-save.mjs (SV-2a) and the save
// timing code of browser-two-save-profile.mjs. The trace witness, the trace verdict and the Runtime
// sampler are not used here.
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
await assertNoReceipt('browser-sv3-measure.json');

async function assertNoReceipt(name) {
  await assert.rejects(lstat(path.join(output, name)), {code: 'ENOENT'});
}

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

// Identity of the one live owner, checked from the copied data root's discovery record, the proxy health and
// the owner's /proc start time. This replaces runtimeRootForData, which requires the data root to sit inside the
// owned stack root and therefore rejects the work copy (see README, deviations).
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
  return {pid, start, instance};
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
  return {reason: typeof reason === 'string' ? reason : (reason === null ? null : JSON.stringify(reason).slice(0, 200)),
    body_code: typeof (json?.code ?? json?.error?.code) === 'string' ? (json?.code ?? json?.error?.code) : null,
    excerpt: text.slice(0, 300)};
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

// The geometry observer closes over these containers. Refill them from each verified head.
// prepareSave(move, expected): expected is 0 before the first drag of the session and 1 after any earlier drag,
// whose counts are then one requested, responded and succeeded. Counts and the pointer are reset here.
function initializeTape(install, args) {
  const span = {};
  const siblings = [];
  install({...args, freeSpace: {span, siblings}});
  const tape = window.__p77DispatchTrace;
  if (!tape) return;
  tape.prepareSave = (move, expected) => {
    const count = tape.counts['app:timeline_commit'];
    if (!tape.fullWritable() || tape.omitted || tape.armed || count.requested !== expected ||
        count.responded !== expected || count.succeeded !== expected || count.failed ||
        (expected ? !Number.isFinite(tape.pointer?.up) : tape.pointer)) return false;
    Object.assign(span, move.span);
    siblings.splice(0, siblings.length, ...move.siblings);
    tape.pointer = null;
    tape.counts['app:timeline_commit'] = {requested: 0, responded: 0, succeeded: 0, failed: 0};
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

async function obtainPublicHead(page, label, receipt) {
  const interval = receipt[label] = {start: clock()};
  try { return await bounded(120_000, () => publicSnapshot(page, origin, fixture)); }
  finally { interval.end = clock(); }
}

function isScopedRead(row) {
  return row.method === 'GET' && (row.route === scopedProject || row.route.startsWith(scopedProject + '/') ||
    row.route === '/api/runtime/v1/projects/selection');
}

// One drag to free space, geometry-checked as in the SV-2a driver, then one Saved wait and one accepted head check.
// Each drag is a full save cycle. The next drag is not started until this one is Saved (see README, deviations).
async function dragOnce({page, head, index, cold, hasPrior, expectedCas, commitRequests, recorder, browserTimeOrigin,
  refusals, drags}) {
  const receipt = {index, cold, baseline: headSummary(head)};
  const postsBefore = recorder.posts().length;
  let phase = 'identity_before_drag';
  let diskWatch, diskCheck, diskStop;
  try {
    await runtimeIdentity();
    assert.equal(await page.evaluate(() => performance.timeOrigin), browserTimeOrigin, 'Editor document changed');
    phase = 'exact_head_geometry';
    const move = canonicalFreeSpace(head, clips, tracks);
    assert(!move.issue, move.issue);
    assert.deepEqual(move.target, target);
    if (cold) assert.equal(move.span.start_seconds, expectedStartSeconds);
    receipt.target = move.target;
    receipt.canonical = {span: move.span, siblings: move.siblings};
    Object.assign(expectedCas, {headRevision: head.headRevision, publicationId: head.publicationId});
    commitRequests.clear();
    assert(await page.evaluate(({move, expected}) => window.__p77DispatchTrace.prepareSave(move, expected),
      {move, expected: hasPrior ? 1 : 0}));
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
    assertDiskFree(receipt.disk_before);
    receipt.load_1m = loadavg()[0];
    phase = 'arm_single_pointer';
    assert.equal(commitRequests.size, 0);
    assert(await page.evaluate(armFreeSpace, {x: x0, y, clipId: move.target.clip_id, trackId: move.target.track_id}));
    phase = 'final_pointer_guard';
    receipt.observed_at_gesture = await currentGeometry();
    checkGeometry(receipt.observed_at_gesture);
    assert.equal(recorder.posts().length, postsBefore);
    assert.equal(commitRequests.size, 0);
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
    receipt.pointerdown = clock();
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
    receipt.observed_drag = {omitted: moved.omitted, path_points: moved.path.length};
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
    const handoff = tape.rows.findLast(row => row.phase === 'handoff-ready' && row.at <= pointer.up);
    await recorder.settle();
    const postRow = recorder.posts().at(-1);
    const refused = response?.status !== 200 || tape.badge?.kind === 'refused';
    if (refused) {
      refusals.push({index, cold, http_status: response?.status ?? null, reason: postRow?.body?.reason ?? null,
        body_code: postRow?.body?.body_code ?? null, badge_kind: tape.badge?.kind ?? null, badge: tape.badge});
    }
    const posts = recorder.posts().length - postsBefore;
    receipt.save = {
      release_to_post_ms: request ? request.at - pointer.up : null,
      post_to_200_ms: response && request ? response.at - request.at : null,
      response_to_saved_ms: saved && response ? saved.at - response.at : null,
      http_status: response?.status ?? null,
      last_pre_release_handoff_ms: handoff ? handoff.at - pointer.up : null,
      post_count_driver: requests.length,
      post_count_network: posts,
      badge: tape.badge,
      commit_count: tape.count,
    };
    if (settleFailure) throw settleFailure;
    assert(!tape.omitted && requests.length === 1 && response?.status === 200 && saved && tape.badge.state === 'saved');
    assert.deepEqual(tape.count, {requested: 1, responded: 1, succeeded: 1, failed: 0});
    assert.equal(posts, 1, 'one commit POST expected for this drag');

    phase = 'accepted_public_head';
    const after = await obtainPublicHead(page, 'accepted_public_proof', receipt);
    receipt.public_after = headSummary(after);
    const [commit] = commitRequests.values();
    receipt.commit_wire = [...commitRequests.values()];
    assert(commitRequests.size === 1 && commit.status === 200 &&
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
    receipt.start_before_s = move.span.start_seconds;
    assert.equal(await page.evaluate(() => performance.timeOrigin), browserTimeOrigin, 'Editor document changed');
    await cpu();
    clearInterval(diskWatch);
    await diskCheck;
    assert(!diskStop);
    phase = 'verified';
    return {after, save: receipt.save};
  } catch (error) {
    receipt.error_phase = phase;
    receipt.error_kind = error?.name ?? 'Error';
    throw error;
  } finally {
    clearInterval(diskWatch);
    await diskCheck;
    if (diskStop) receipt.disk_stop = diskStop;
    receipt.phase = phase;
    drags.push(receipt);
  }
}

const profile = await mkdtemp(path.join(browserParent, 'profile-'));
const receipt = {mode, tuple, runtime_sha: runtimeSha, data_root: data, candidate: {pid, start, instance},
  disk_floor_bytes: Number(diskFloorBytes), node_time_origin: performance.timeOrigin, load_1m_start: loadavg()[0],
  scenarios: [], drags: [], s0: null, refusals: []};
// Scenario order is fixed: cold (one save), then S1 to S4. Each warm scenario ends with a 2 s settle.
const scenarios = [
  {name: 'cold', warm: false, drags: 1, gap_ms: 0},
  {name: 'S1', warm: true, drags: 1, gap_ms: 0},
  {name: 'S2', warm: true, drags: 2, gap_ms: 200},
  {name: 'S3', warm: true, drags: 10, gap_ms: 150},
  {name: 'S4', warm: true, drags: 5, gap_ms: 0},
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
  // S0: the page load is the first browser action. It ends when the editor is writable and the verified-head
  // route has answered.
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
  for (const scenario of scenarios) {
    phase = `scenario_${scenario.name}`;
    const result = {name: scenario.name, warm: scenario.warm, drags: [], n_posts: 0, settle_ms: 2000};
    const postsBefore = recorder.posts().length;
    for (let i = 0; i < scenario.drags; i += 1) {
      const drags = [];
      const outcome = await dragOnce({page, head, index: i, cold: scenario.name === 'cold' && i === 0,
        hasPrior: sessionDrags > 0, expectedCas, commitRequests, recorder, browserTimeOrigin,
        refusals: receipt.refusals, drags});
      sessionDrags += 1;
      head = outcome.after;
      result.drags.push({...outcome.save, scenario: scenario.name, index: i});
      receipt.drags.push(...drags);
      if (i < scenario.drags - 1) await sleep(scenario.gap_ms);
    }
    await sleep(2000);
    result.n_posts = recorder.posts().length - postsBefore;
    assert.equal(result.n_posts, scenario.drags, `scenario ${scenario.name} commit POST count`);
    receipt.scenarios.push(result);
  }
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
  if (recorder) await recorder.settle();
  receipt.timeline_commit_posts = recorder?.posts().length ?? 0;
  receipt.non_2xx_runtime = (recorder?.rows() ?? []).filter(row => row.route?.startsWith('/api/runtime') &&
    !(row.status >= 200 && row.status < 300) && row.status !== undefined)
    .map(row => ({method: row.method, route: row.route, status: row.status, body: row.body ?? null}));
  receipt.refusal_count = receipt.refusals.length + (receipt.s0?.refusal ? 1 : 0) +
    receipt.non_2xx_runtime.filter(row => row.status === 409 || row.body?.reason === 'head_busy').length;
  receipt.requests = recorder?.rows() ?? [];
  const expectedPosts = scenarios.reduce((sum, item) => sum + item.drags, 0);
  if (receipt.phase === 'verified' && (receipt.context_close_error || !receipt.profile_removed ||
      receipt.timeline_commit_posts !== expectedPosts)) {
    receipt.phase = 'cleanup_proof_failed';
    process.exitCode = 1;
  }
  await writeReceipt('browser-sv3-measure', receipt);
}
