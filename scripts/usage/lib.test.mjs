// node --test scripts/usage/*.test.mjs  (octoloom#333)
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { kAnon, buildUsage, validSchema, assertSafe, changed, QUERIES, K } from './lib.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));

test('k-anonymity: 4 machines go to Other, 5 stay', () => {
  const out = kAnon([{ key: 'CH', machines: 5 }, { key: 'DE', machines: 4 }, { key: 'FR', machines: 3 }], K, 'code');
  assert.deepEqual(out, [{ code: 'CH', machines: 5 }, { code: 'Other', machines: 7 }]);
});

test('k-anonymity: an Other with fewer than 5 machines is dropped too', () => {
  assert.deepEqual(kAnon([{ key: 'CH', machines: 9 }, { key: 'DE', machines: 4 }], K, 'code'), [{ code: 'CH', machines: 9 }]);
  assert.deepEqual(kAnon([{ key: null, machines: 2 }], K, 'code'), []);
});

const RAW = {
  active: [[6, 12, 30, 40]],
  events: [['build', 50], ['deploy', 20], ['create', 9]],
  countries: [['CH', 'Switzerland', 20], ['DE', 'Germany', 6], ['IS', 'Iceland', 1], ['LU', 'Luxembourg', 4]],
  versions: [['0.9.30', 25], ['0.9.29', 3]],
  os: [['mac', 18], ['win', 9], ['linux', 3]],
  features: [['agentNetwork.build', 40, 12], ['agentNetwork.undeploy', 2, 1]],
  templates: [['v2', 'v2-retail-returns', 8, 6], ['v1', 'blank', 3, 2]],
  styles: [['build', 'v2', 30, 10, 12, 4], ['build', 'v1', 20, 3, 1, 0], ['create', 'v2', 8, 6, 0, 0]],
  outcomes: [['build', 'ok', 45, 10], ['build', 'fail', 5, 3], ['deploy', 'ok', 20, 2]],
  actionMachines: [['build', 10], ['deploy', 2]],
  connections: [[20, 6, 2, 1, 25]],
  trends: [['2026-11-16', 10, 30, 10, 5], ['2026-11-23', 12, 20, 10, 4]],
};

test('buildUsage: aggregates only, k >= 5 in every breakdown', () => {
  const u = buildUsage(RAW, '2026-11-24T03:00:00.000Z');
  assert.deepEqual(validSchema(u), []);
  assert.equal(u.empty, false);
  // IS (1) and LU (4) are below k each; together 5 machines, so they show only as Other.
  assert.deepEqual(u.countries, [{ code: 'CH', name: 'Switzerland', machines: 20 }, { code: 'DE', name: 'Germany', machines: 6 }, { code: 'Other', machines: 5 }]);
  assert.deepEqual(u.features, [{ id: 'agentNetwork.build', machines: 12, uses: 40 }]);
  assert.equal(u.styles.build.v1, null);
  assert.equal(u.styles.build.v2.withPolicies, 12);
  assert.equal(u.outcomes.deploy, null);
  assert.deepEqual(u.outcomes.build, { ok: 45, fail: 5 });
  assert.equal(u.connections.anypoint, 20);
  assert.equal(u.connections.p4a, null);
  assert.deepEqual(u.templates, [{ style: 'v2', template: 'v2-retail-returns', machines: 6, uses: 8 }]);
});

test('no field named like distinct_id, ip or city anywhere in the output', () => {
  const text = JSON.stringify(buildUsage(RAW));
  assert.doesNotMatch(text, /distinct_?id|"\$?ip"|city|postal|latitude/i);
  assert.throws(() => assertSafe({ countries: [{ code: 'CH', distinct_id: 'x' }] }), /forbidden/);
  assert.throws(() => assertSafe({ a: { $geoip_city_name: 'x' } }), /forbidden/);
  for (const q of Object.values(QUERIES)) assert.doesNotMatch(q, /city|postal|latitude|\$ip/i);
});

test('no data yet: an empty project gives a valid file with empty = true', () => {
  const u = buildUsage({});
  assert.deepEqual(validSchema(u), []);
  assert.equal(u.empty, true);
  assert.deepEqual(u.countries, []);
});

test('changed() ignores the refresh date', () => {
  const a = buildUsage(RAW, '2026-11-24T03:00:00.000Z');
  const b = buildUsage(RAW, '2026-11-25T03:00:00.000Z');
  assert.equal(changed(a, b), false);
  assert.equal(changed(null, b), true);
  assert.equal(changed(a, buildUsage({ ...RAW, active: [[7, 12, 30, 40]] })), true);
});

test('a PostHog error leaves the previous file untouched and fails the run', async () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'usage-'));
  const out = path.join(dir, 'usage.json');
  fs.writeFileSync(out, '{"schema":1,"keep":true}\n');
  // A local server that answers every query with HTTP 500.
  const http = await import('node:http');
  const srv = http.createServer((_, res) => { res.statusCode = 500; res.end('{}'); });
  await new Promise((r) => srv.listen(0, '127.0.0.1', r));
  const host = `http://127.0.0.1:${srv.address().port}`;
  const r = await new Promise((resolve) => {
    import('node:child_process').then(({ spawn }) => {
      const p = spawn(process.execPath, [path.join(HERE, 'aggregate.mjs')], { env: { ...process.env, POSTHOG_HOST: host, POSTHOG_QUERY_KEY: 'test-key', POSTHOG_PROJECT_ID: '1', USAGE_OUT: out } });
      let err = ''; p.stderr.on('data', (d) => (err += d));
      p.on('close', (code) => resolve({ code, err }));
    });
  });
  srv.close();
  assert.equal(r.code, 1);
  assert.match(r.err, /HTTP 500/);
  assert.doesNotMatch(r.err, /test-key/);
  assert.equal(fs.readFileSync(out, 'utf8'), '{"schema":1,"keep":true}\n');
});

test('missing credentials fail without writing', () => {
  const r = spawnSync(process.execPath, [path.join(HERE, 'aggregate.mjs')], { env: { PATH: process.env.PATH, USAGE_OUT: path.join(os.tmpdir(), 'never.json') } });
  assert.equal(r.status, 1);
  assert.equal(fs.existsSync(path.join(os.tmpdir(), 'never.json')), false);
});
