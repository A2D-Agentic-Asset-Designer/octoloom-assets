#!/usr/bin/env node
// Daily usage aggregation (octoloom#333): queries PostHog EU server-side, keeps only aggregates (k >= 5)
// and writes docs/assets/usage.json plus the monthly copy docs/assets/usage/YYYY-MM.json.
// Env: POSTHOG_QUERY_KEY (secret, read-only, project-scoped), POSTHOG_PROJECT_ID, POSTHOG_HOST (default EU).
// A failed query leaves the previous files untouched and exits with code 1. Nothing secret is ever logged.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { QUERIES, buildUsage, changed, validSchema } from './lib.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const OUT = process.env.USAGE_OUT ?? path.join(ROOT, 'docs', 'assets', 'usage.json');
const HOST = process.env.POSTHOG_HOST ?? 'https://eu.posthog.com';
const KEY = process.env.POSTHOG_QUERY_KEY;
const PROJECT = process.env.POSTHOG_PROJECT_ID;

async function query(name, q) {
  const ctl = new AbortController();
  const t = setTimeout(() => ctl.abort(), 60_000);
  try {
    const r = await fetch(`${HOST}/api/projects/${encodeURIComponent(PROJECT)}/query/`, {
      method: 'POST', signal: ctl.signal,
      headers: { 'content-type': 'application/json', authorization: `Bearer ${KEY}` },
      body: JSON.stringify({ query: { kind: 'HogQLQuery', query: q } }),
    });
    if (!r.ok) throw new Error(`query ${name}: HTTP ${r.status}`);
    const j = await r.json();
    if (!Array.isArray(j.results)) throw new Error(`query ${name}: no results`);
    return j.results;
  } finally { clearTimeout(t); }
}

async function main() {
  if (!KEY || !PROJECT) throw new Error('POSTHOG_QUERY_KEY and POSTHOG_PROJECT_ID must be set');
  const raw = {};
  for (const [name, q] of Object.entries(QUERIES)) raw[name] = await query(name, q);
  const usage = buildUsage(raw);
  const errs = validSchema(usage);
  if (errs.length) throw new Error(`usage.json schema: ${errs.join(', ')}`);
  const prev = fs.existsSync(OUT) ? JSON.parse(fs.readFileSync(OUT, 'utf8')) : null;
  if (!changed(prev, usage)) { console.log('usage: no change'); return; }
  fs.mkdirSync(path.join(path.dirname(OUT), 'usage'), { recursive: true });
  const text = JSON.stringify(usage, null, 2) + '\n';
  fs.writeFileSync(OUT, text);
  fs.writeFileSync(path.join(path.dirname(OUT), 'usage', `${usage.refreshed.slice(0, 7)}.json`), text);
  const t = usage.totals;
  console.log(`usage: written (active day/week/month ${t.active.day}/${t.active.week}/${t.active.month}, countries ${usage.countries.length}, empty ${usage.empty})`);
}

main().catch((e) => { console.error('usage aggregation failed:', e.message); process.exit(1); });
