import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
const { parseTimelineBundle } = await import(resolve(process.cwd(), 'src/tools/video-editor/data/typed/timelineBundle.ts'));
const item = (o: Record<string, unknown> = {}) => ({
  id: 'assetA:src:0', shape: 'interval', domain: 'source_seconds', extent: { start: 0, end: 1.5 },
  schemaRef: 'astrid.transcript_segment/v1', payload: { text: 'hello' },
  sourceArtifactRef: { assetId: 'assetA' },
  provenance: { adapterId: 'astrid.adaptTranscript', adapterVersion: '1' }, ...o,
});
const env = (o: Record<string, unknown> = {}) => ({
  schema_version: 1, itemsBySchemaRef: { 'astrid.transcript_segment/v1': [item()] }, ...o });
const refs = (rows: unknown[]) => ({ transcriptReferences: { schema: 'media.transcript.references/v1', associations: rows } });
const cases: Record<string, unknown> = {
  '1 valid': env(),
  '1b valid+assetId rows': env(refs([{ assetId: 'assetA', documentId: 'doc1' }])),
  '2 rows without assetId (R14 shape)': env(refs([{ documentId: 'doc1', mediaId: 'assetA', sourceId: 's1' }])),
  '3 fractional extent': env({ itemsBySchemaRef: { 'astrid.transcript_segment/v1': [item({ extent: { start: 0.1234567, end: 1.5000001 } })] } }),
};
const files = process.argv.slice(2);
for (const f of files) cases['file ' + f] = JSON.parse(readFileSync(f, 'utf8'));
for (const [name, v] of Object.entries(cases)) {
  try { parseTimelineBundle(v); console.log('OK   ', name); }
  catch (e) { console.log('FAIL ', name, '->', (e as Error).message); }
}
