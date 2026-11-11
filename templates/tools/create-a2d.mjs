// Creates fresh A2D mock assets for every use case (idempotent: skips ids already in a2d-ids.json).
// Usage: A2D_KEY=... node create-a2d.mjs   (the key is never written anywhere)
import fs from 'node:fs';
import { USECASES } from './usecases.mjs';

const BASE = 'https://www.a2d-ai.com/api/platform-mcp/mcp';
let sid, seq = 1, inited = false;
async function rpc(method, params, notify) {
  const body = { jsonrpc: '2.0', method, ...(params !== undefined ? { params } : {}) };
  if (!notify) body.id = seq++;
  const r = await fetch(BASE, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json, text/event-stream', Authorization: 'Bearer ' + process.env.A2D_KEY, 'MCP-Protocol-Version': '2025-06-18', ...(sid ? { 'Mcp-Session-Id': sid } : {}) }, body: JSON.stringify(body) });
  const s = r.headers.get('mcp-session-id'); if (s) sid = s;
  if (notify) return;
  const t = await r.text(); let m;
  if ((r.headers.get('content-type') || '').includes('event-stream')) { for (const l of t.split(/\r?\n/)) if (l.startsWith('data:')) { try { const x = JSON.parse(l.slice(5)); if (x.id === body.id) m = x; } catch {} } } else m = JSON.parse(t);
  if (!m) throw new Error(method + ': no response');
  if (m.error) throw new Error(method + ': ' + JSON.stringify(m.error));
  return m.result;
}
async function call(name, args = {}) {
  if (!inited) { await rpc('initialize', { protocolVersion: '2025-06-18', capabilities: {}, clientInfo: { name: 'octoloom-templates', version: '1' } }); await rpc('notifications/initialized', undefined, true); inited = true; }
  const r = await rpc('tools/call', { name, arguments: args });
  const txt = (r.content || []).map((c) => c.text).join('');
  if (r.isError) throw new Error(name + ': ' + txt);
  if (r.structuredContent) return r.structuredContent;
  try { return JSON.parse(txt); } catch { return txt; }
}

const IDS = new URL('./a2d-ids.json', import.meta.url);
const ids = fs.existsSync(IDS) ? JSON.parse(fs.readFileSync(IDS, 'utf8')) : {};
const save = () => fs.writeFileSync(IDS, JSON.stringify(ids, null, 2) + '\n');
const A2D_PLATFORM = (p) => (/mulesoft/i.test(p) ? 'mulesoft' : /agentforce/i.test(p) ? 'agentforce' : 'other');

const only = process.argv[2];
for (const u of USECASES) {
  if (only && u.id !== only) continue;
  const rec = (ids[u.id] ??= { project: undefined, agents: {}, mcps: {} });
  if (rec.project === undefined) {
    // A2D projects need a user-bound key; skip grouping when the key is an org token.
    try {
      const p = await call('create_project', { name: `Octoloom example: ${u.title} (${u.version === 'v1' ? 'Probabilistic' : 'Deterministic'})`, description: `${u.summary} Mock upstreams for the Octoloom ${u.id} template.` });
      rec.project = (p.project ?? p).id;
    } catch (e) { rec.project = null; console.log('project skipped:', String(e.message).slice(0, 80)); }
    save();
  }
  for (const m of u.mcps) {
    if (rec.mcps[m.key]) continue;
    const s = (await call('design_mcp_server', { name: `Octoloom ${m.name}`, type: 'mock', description: m.description, protocol_version: '2025-06-18' })).server;
    for (const [i, t] of m.tools.entries()) {
      const properties = Object.fromEntries(Object.entries(t.input).map(([k, [type, description]]) => [k, { type, description }]));
      const scen = t.cases.map(([field, value, json], j) => ({ name: `${t.name} ${value}`, condition: { field, operator: '===', value }, response: JSON.stringify(json), responseType: 'json' }));
      scen.push({ name: `${t.name} default`, condition: { field: t.required[0], operator: 'exists' }, response: JSON.stringify(t.fallback), responseType: 'json' });
      await call('add_mcp_tool', { server_id: s.id, name: t.name, description: t.description, input_schema: { type: 'object', properties, required: t.required }, mock_scenarios: scen, sort_order: i });
    }
    await call('update_mcp_server', { id: s.id, status: 'published', provider_organization: 'Octoloom examples' });
    if (rec.project) await call('add_asset_to_project', { project_id: rec.project, asset_type: 'mcp_server', asset_id: s.id });
    rec.mcps[m.key] = s.id; save();
    console.log('mcp', u.id, m.key, s.id);
  }
  for (const a of u.agents) {
    if (rec.agents[a.key]) continue;
    const c = (await call('design_agent_card', { name: a.name, description: a.description, platform: A2D_PLATFORM(a.platform), protocol_version: a.proto, type: 'mock', version: '1.0.0' })).agentCard;
    for (const [i, k] of a.skills.entries()) await call('add_agent_skill', { card_id: c.id, skill_id: k.id, name: k.name, description: k.description, tags: k.tags, examples: k.examples, sort_order: i });
    for (const [kw, text] of a.replies) await call('add_mock_scenario', { scope_type: 'agent_card', scope_id: c.id, scenario: { name: kw, condition: { field: 'text', operator: 'contains', value: kw }, response: text, responseType: 'text' } });
    await call('add_mock_scenario', { scope_type: 'agent_card', scope_id: c.id, scenario: { name: 'default', condition: { field: 'text', operator: 'exists' }, response: a.fallback, responseType: 'text' } });
    await call('update_agent_card', { id: c.id, status: 'published' });
    if (rec.project) await call('add_asset_to_project', { project_id: rec.project, asset_type: 'agent_card', asset_id: c.id });
    rec.agents[a.key] = c.id; save();
    console.log('agent', u.id, a.key, a.proto, c.id);
  }
}
console.log('done');
