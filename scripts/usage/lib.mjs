// Pure helpers of the usage aggregation (octoloom#333). No network, no fs: tested with node --test.
// Privacy rules: only aggregates leave this module, never a machine id, IP, city or per-machine row,
// and every breakdown cell needs at least K distinct machines (smaller cells fold into "Other").

export const K = 5;
export const WINDOW_DAYS = 30;
export const TREND_WEEKS = 12;

/** The event catalog of the extension (ADR octoloom#324, TELEMETRY_EVENTS in src/model/telemetry.ts). */
export const EVENTS = ['activate', 'heartbeat', 'build', 'validate', 'publish', 'deploy', 'governance', 'create', 'feature', 'error'];
export const ACTIONS = ['build', 'validate', 'publish', 'deploy', 'governance'];
export const CONNECTIONS = ['anypoint', 'a2d', 'p4a', 'idmc'];

/** Field names that must never appear in the output (checked by the tests and before every write). */
export const FORBIDDEN_KEYS = /^(distinct_?id|machine_?id|\$?ip|.*city.*|.*postal.*|.*latitude.*|.*longitude.*|person.*|\$?session_?id)$/i;

const n = (v) => (Number.isFinite(Number(v)) ? Number(v) : 0);

/**
 * k-anonymity grouping: rows {key, machines, uses?} -> cells with >= k machines (sorted, biggest first),
 * plus one "Other" cell with the rest. "Other" itself is dropped when it has fewer than k machines.
 */
export function kAnon(rows, k = K, label = 'key') {
  const keep = [], rest = { machines: 0, uses: 0, cells: 0 };
  for (const r of rows) {
    const m = n(r.machines);
    if (!r.key || r.key === 'null' || m < k) { rest.machines += m; rest.uses += n(r.uses); rest.cells++; continue; }
    keep.push({ [label]: String(r.key), ...(r.name ? { name: String(r.name) } : {}), machines: m, ...(r.uses !== undefined ? { uses: n(r.uses) } : {}) });
  }
  keep.sort((a, b) => b.machines - a.machines || String(a[label]).localeCompare(String(b[label])));
  if (rest.cells && rest.machines >= k) keep.push({ [label]: 'Other', machines: rest.machines, ...(rows.some((r) => r.uses !== undefined) ? { uses: rest.uses } : {}) });
  return keep;
}

/** A count that is only published when it covers at least k machines; otherwise null ("fewer than 5"). */
export const atLeastK = (count, machines, k = K) => (n(machines) >= k ? n(count) : null);

/** Turns the raw query results (arrays of rows) into the public usage.json object. */
export function buildUsage(raw, refreshed = new Date().toISOString()) {
  const [a1, a7, a30, a90] = (raw.active?.[0] ?? []).map(n);
  const ev = Object.fromEntries((raw.events ?? []).map(([e, c]) => [e, n(c)]));
  const totals = {
    active: { day: a1 ?? 0, week: a7 ?? 0, month: a30 ?? 0, quarter: a90 ?? 0 },
    events: Object.fromEntries(['build', 'validate', 'publish', 'deploy', 'governance', 'create'].map((e) => [e, ev[e] ?? 0])),
  };
  const rows = (x, f) => (x ?? []).map(f);
  const countries = kAnon(rows(raw.countries, ([code, name, m]) => ({ key: code, name, machines: m })), K, 'code');
  const versions = kAnon(rows(raw.versions, ([v, m]) => ({ key: v, machines: m })), K, 'version');
  const os = kAnon(rows(raw.os, ([v, m]) => ({ key: v, machines: m })), K, 'os');
  const features = kAnon(rows(raw.features, ([id, uses, m]) => ({ key: id, uses, machines: m })), K, 'id');
  const templates = kAnon(rows(raw.templates, ([style, t, uses, m]) => ({ key: `${style}|${t}`, uses, machines: m })), K, 'key')
    .map(({ key, ...r }) => (key === 'Other' ? { style: 'other', template: 'Other', ...r } : { style: key.split('|')[0], template: key.split('|')[1], ...r }));
  const styles = { build: {}, create: {} };
  for (const [kind, style, uses, m, withPolicies, governed] of raw.styles ?? []) {
    if (!['build', 'create'].includes(kind) || !['v1', 'v2'].includes(style)) continue;
    styles[kind][style] = n(m) >= K ? { uses: n(uses), machines: n(m), ...(kind === 'build' ? { withPolicies: n(withPolicies), governed: n(governed) } : {}) } : null;
  }
  const outcomes = {};
  const byAction = {};
  for (const [e, outcome, c, m] of raw.outcomes ?? []) {
    if (!ACTIONS.includes(e)) continue;
    (byAction[e] ??= { machines: n(raw.actionMachines?.find((r) => r[0] === e)?.[1]), cells: {} }).cells[outcome || 'unknown'] = n(c);
  }
  for (const a of ACTIONS) outcomes[a] = byAction[a] && byAction[a].machines >= K ? byAction[a].cells : null;
  const c = (raw.connections?.[0] ?? []).map(n);
  const cm = c[CONNECTIONS.length] ?? 0;
  const connections = { machines: cm, ...Object.fromEntries(CONNECTIONS.map((x, i) => [x, atLeastK(c[i] ?? 0, cm) === null ? null : (c[i] ?? 0) >= K ? c[i] : null])) };
  const trends = rows(raw.trends, ([week, active, build, deploy, create]) => ({ week: String(week).slice(0, 10), active: n(active), build: n(build), deploy: n(deploy), create: n(create) }));
  const out = { schema: 1, refreshed, window: { days: WINDOW_DAYS, k: K, trendWeeks: TREND_WEEKS }, totals, countries, versions, platforms: { os }, features, templates, styles, outcomes, connections, trends };
  out.empty = totals.active.quarter === 0 && Object.values(totals.events).every((x) => x === 0);
  assertSafe(out);
  return out;
}

/** Throws when a forbidden field name appears anywhere in the object. */
export function assertSafe(o, path = '') {
  if (Array.isArray(o)) return o.forEach((x, i) => assertSafe(x, `${path}[${i}]`));
  if (o && typeof o === 'object') for (const [k, v] of Object.entries(o)) {
    if (FORBIDDEN_KEYS.test(k)) throw new Error(`forbidden field in usage output: ${path}.${k}`);
    assertSafe(v, `${path}.${k}`);
  }
}

/** Minimal schema check of usage.json (the page relies on these fields). */
export function validSchema(u) {
  const errs = [];
  if (u?.schema !== 1) errs.push('schema');
  if (typeof u?.refreshed !== 'string' || Number.isNaN(Date.parse(u.refreshed))) errs.push('refreshed');
  for (const k of ['day', 'week', 'month', 'quarter']) if (typeof u?.totals?.active?.[k] !== 'number') errs.push(`totals.active.${k}`);
  for (const k of ['countries', 'versions', 'features', 'templates', 'trends']) if (!Array.isArray(u?.[k])) errs.push(k);
  for (const k of ['styles', 'outcomes', 'connections', 'platforms']) if (typeof u?.[k] !== 'object' || u[k] === null) errs.push(k);
  if (typeof u?.empty !== 'boolean') errs.push('empty');
  return errs;
}

/** True when the data changed (the refresh date alone is not a change). */
export function changed(prev, next) {
  if (!prev) return true;
  const strip = ({ refreshed, ...r }) => JSON.stringify(r);
  return strip(prev) !== strip(next);
}

// ------------------------------------------------------------------ HogQL
/** Event name without the "<publisher>.<extension>/" prefix that VS Code's TelemetryLogger adds. */
const E = "replaceRegexpOne(event, '^.*/', '')";
const IN = `${E} in (${EVENTS.map((e) => `'${e}'`).join(', ')})`;
const W = `timestamp > now() - interval ${WINDOW_DAYS} day`;
const S = (p) => `toString(properties.${p})`;
const TRUE = (p) => `${S(p)} in ('true', '1')`;

export const QUERIES = {
  active: `select uniqExactIf(distinct_id, timestamp > now() - interval 1 day), uniqExactIf(distinct_id, timestamp > now() - interval 7 day), uniqExactIf(distinct_id, ${W}), uniqExact(distinct_id) from events where ${E} = 'heartbeat' and timestamp > now() - interval 90 day`,
  events: `select ${E} as e, count() from events where ${IN} and ${W} group by e`,
  countries: `select properties.$geoip_country_code as c, any(properties.$geoip_country_name), uniqExact(distinct_id) from events where ${IN} and ${W} group by c`,
  versions: `select ${S('extVersion')} as v, uniqExact(distinct_id) from events where ${IN} and ${W} group by v`,
  os: `select ${S('os')} as v, uniqExact(distinct_id) from events where ${IN} and ${W} group by v`,
  features: `select ${S('id')} as id, count(), uniqExact(distinct_id) from events where ${E} = 'feature' and ${W} group by id`,
  templates: `select ${S('style')} as s, ${S('template')} as t, count(), uniqExact(distinct_id) from events where ${E} = 'create' and ${W} group by s, t`,
  styles: `select ${E} as e, ${S('style')} as s, count(), uniqExact(distinct_id), countIf(${S('policies')} in ('1-3', '4+')), countIf(${TRUE('governed')}) from events where ${E} in ('build', 'create') and ${W} group by e, s`,
  outcomes: `select ${E} as e, ${S('outcome')} as o, count(), uniqExact(distinct_id) from events where ${E} in (${ACTIONS.map((a) => `'${a}'`).join(', ')}) and ${W} group by e, o`,
  actionMachines: `select ${E} as e, uniqExact(distinct_id) from events where ${E} in (${ACTIONS.map((a) => `'${a}'`).join(', ')}) and ${W} group by e`,
  connections: `select ${CONNECTIONS.map((c) => `countIf(${c} in ('true', '1'))`).join(', ')}, count() from (select distinct_id, ${CONNECTIONS.map((c) => `argMax(${S(c)}, timestamp) as ${c}`).join(', ')} from events where ${E} = 'heartbeat' and ${W} group by distinct_id)`,
  trends: `select toStartOfWeek(timestamp, 1) as w, uniqExactIf(distinct_id, ${E} = 'heartbeat'), countIf(${E} = 'build'), countIf(${E} = 'deploy'), countIf(${E} = 'create') from events where ${IN} and timestamp > now() - interval ${TREND_WEEKS} week group by w order by w`,
};
