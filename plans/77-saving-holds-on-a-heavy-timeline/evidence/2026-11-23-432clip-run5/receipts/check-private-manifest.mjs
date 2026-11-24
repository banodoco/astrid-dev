import { readFile } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { pathToFileURL } from 'node:url';
const [app, manifestPath, agent, runtime, agentSha, runtimeSha] = process.argv.slice(2);
const { checkManifest } = await import(pathToFileURL(`${app}/scripts/installer/pin.mjs`));
const reader = async (repo, sha, file) => {
  const selected = repo === 'banodoco/astrid-agent' && sha === agentSha ? agent : repo === 'banodoco/astrid-runtime' && sha === runtimeSha ? runtime : null;
  if (!selected) throw Error(`Unexpected source ${repo} ${sha}`);
  return execFileSync('git', ['--git-dir', selected, 'show', `${sha}:${file}`], {maxBuffer: 20*1024*1024});
};
console.log(await checkManifest(JSON.parse(await readFile(manifestPath, 'utf8')), reader));
