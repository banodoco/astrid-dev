import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import {createHash} from 'node:crypto';
import {lstat, open, readFile, writeFile} from 'node:fs/promises';
import path from 'node:path';
import {setTimeout as pause} from 'node:timers/promises';

const spy = process.env.SV3_PYSPY ?? '/home/user/codex-run/run/toolchain/py-spy-0.4.1/bin/py-spy';
const attachBanner = /^py-spy> Sampling process 100 times a second\. Press Control-C to exit\.$/m;
const attachTimeoutMs = 5_000;
const scopeLimitMs = 120_000;

const clock = () => {
  const monotonicMs = performance.now();
  return {monotonic_ms: monotonicMs, epoch_ms: performance.timeOrigin + monotonicMs};
};

export async function profileTwoSave({runtime, page, targetUrl, output, stem, cpu}) {
  const rawFile = `${stem}.speedscope.json`;
  const logFile = `${stem}-sampler.log`;
  const evidenceFile = `${stem}-profile.json`;
  const raw = path.join(output, rawFile);
  const logPath = path.join(output, logFile);
  const evidencePath = path.join(output, evidenceFile);
  for (const location of [raw, evidencePath]) {
    await assert.rejects(lstat(location), {code: 'ENOENT'});
  }
  const args = ['record', '--pid', String(runtime.pid), '--rate', '100', '--threads',
    '--idle', '--format', 'speedscope', '--output', raw];
  const record = {runtime, sampler: spy, version: '0.4.1', args, rate_hz: 100, threads: true,
    idle: true, native: false, raw_file: rawFile, sampler_log: logFile,
    boundary: 'just_before_pointerdown_through_scoped_http_200', attach_timeout_ms: attachTimeoutMs,
    scope_limit_ms: scopeLimitMs, runtime_cpu_before: await cpu()};
  const log = await open(logPath, 'wx', 0o600);
  record.spawn_requested = clock();
  const child = spawn(spy, args, {stdio: ['ignore', log.fd, log.fd]});
  let spawnError, exit, stopPromise, cap;
  const closed = new Promise(resolve => {
    child.once('error', error => { spawnError = error.code ?? error.name; });
    child.once('close', (code, signal) => {
      exit = {code, signal, spawn_error: spawnError ?? null, observed: clock()};
      resolve(exit);
    });
  });
  const running = () => spawnError === undefined && !exit && child.exitCode === null && child.signalCode === null;

  function stop(reason) {
    if (stopPromise) return stopPromise;
    record.stop_reason = reason;
    record.stop_requested = clock();
    page.off('response', afterResponse);
    clearTimeout(cap);
    if (running()) {
      record.sigint_sent = child.kill('SIGINT');
    }
    stopPromise = (async () => {
      const cpuAfter = cpu().catch(() => null);
      let terminated = await Promise.race([closed, pause(10_000, null, {ref: false})]);
      if (!terminated && running()) {
        record.sigterm_sent = child.kill('SIGTERM');
        terminated = await Promise.race([closed, pause(2_000, null, {ref: false})]);
      }
      if (!terminated && running()) {
        record.sigkill_sent = child.kill('SIGKILL');
        terminated = await Promise.race([closed, pause(2_000, null, {ref: false})]);
      }
      record.sampler_exit = terminated ?? {outcome: 'exit_timeout'};
      record.runtime_cpu_after = await cpuAfter;
      if (record.runtime_cpu_after !== null) {
        record.runtime_cpu_delta = record.runtime_cpu_after - record.runtime_cpu_before;
      }
      const logText = await readFile(logPath, 'utf8');
      const counts = /\bSamples:\s*(\d+)\s+Errors:\s*(\d+)/.exec(logText);
      record.sampling_sample_count = counts ? Number(counts[1]) : null;
      record.sampling_error_count = counts ? Number(counts[2]) : null;
      record.sampler_diagnostics = logText.split(/\r?\n/).filter(line => line.trim() &&
        /error|permission|failed|denied|lagging|out of date|inaccurate/i.test(line) &&
        !/\bSamples:\s*\d+\s+Errors:\s*\d+/.test(line)).slice(0, 30);
      const bytes = await readFile(raw).catch(error => {
        if (error?.code !== 'ENOENT') throw error;
        return null;
      });
      if (bytes) {
        record.raw_sha256 = createHash('sha256').update(bytes).digest('hex');
        record.raw_bytes = bytes.length;
        try {
          const profile = JSON.parse(bytes);
          assert(String(profile.$schema).includes('speedscope') && Array.isArray(profile.shared?.frames) &&
            profile.profiles.length > 0 && profile.profiles.every(thread => thread.type === 'sampled' &&
              Array.isArray(thread.samples) && thread.samples.length === thread.weights?.length));
          record.raw_sampled_profiles = profile.profiles.length;
          record.raw_stack_samples = profile.profiles.reduce((total, thread) => total + thread.samples.length, 0);
        } catch (error) { record.raw_error_kind = error?.name ?? 'Error'; }
      }
      record.complete = Boolean(record.attach_observed && record.pointerdown_requested && record.http_200 &&
        reason === 'scoped_http_200' && record.sigint_sent && record.sampler_exit.code === 0 &&
        record.sampling_sample_count > 0 && record.sampling_error_count !== null && record.raw_stack_samples > 0);
      await writeFile(evidencePath, JSON.stringify(record, null, 2) + '\n', {flag: 'wx', mode: 0o600});
      return record;
    })();
    return stopPromise;
  }

  function afterResponse(response) {
    if (response.url() !== targetUrl || response.request().method() !== 'POST' || response.status() !== 200) return;
    record.http_200 = clock();
    const reason = record.pointerdown_requested ? 'scoped_http_200' : 'http_200_before_pointerdown';
    void stop(reason).catch(() => {});
  }

  try {
    page.on('response', afterResponse);
    cap = setTimeout(() => { void stop('scope_timeout').catch(() => {}); }, scopeLimitMs);
    await log.close();
    const deadline = performance.now() + attachTimeoutMs;
    while (running() && !stopPromise && performance.now() < deadline) {
      if (attachBanner.test(await readFile(logPath, 'utf8')) && running() && !stopPromise) {
        record.attach_observed = clock();
        break;
      }
      await Promise.race([closed, pause(20)]);
    }
  } catch (error) { record.attach_error_kind = error?.code ?? error?.name ?? 'Error'; }
  if (!record.attach_observed) {
    record.attach_error = record.attach_error_kind ?? (running() ? 'sampling_banner_timeout' : 'sampler_exited_before_banner');
    await stop('attach_failed');
  }
  return {
    attached: Boolean(record.attach_observed),
    evidenceFile,
    beforePointerdown() {
      if (!record.attach_observed || !running() || stopPromise) {
        record.attach_error ??= 'sampler_ended_before_pointerdown';
        throw new Error('Runtime sampler is unavailable before pointerdown');
      }
      record.pointerdown_requested = clock();
      return record.pointerdown_requested;
    },
    stop,
  };
}
