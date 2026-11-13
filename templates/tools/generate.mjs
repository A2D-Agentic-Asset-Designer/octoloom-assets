// Generates the Octoloom example templates from usecases.mjs + flows.mjs + a2d-ids.json.
// Output: ../<id>/ (agent-network.yaml, exchange.json, brokers/*.agent, README.md) and ../index.json.
// No credentials are written: the LLM key is the secret variable openai.apiKey with an empty default.
//
// Usage: node generate.mjs <yaml-module-path>
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { USECASES } from './usecases.mjs';
import { FLOWS } from './flows.mjs';
import { TRY } from './tryit.mjs';

const YAML = await import(pathToFileURL(process.argv[2] ?? 'yaml').href).catch(() => import('yaml'));
const here = path.dirname(new URL(import.meta.url).pathname);
const out = path.resolve(here, '..');
const ids = JSON.parse(fs.readFileSync(path.join(here, 'a2d-ids.json'), 'utf8'));
const A2D = 'https://www.a2d-ai.com/api/platform';
const AF = '68ef9520-24e9-4cf2-b2f5-620025690913';
const MODEL = 'gpt-5-mini';
const camel = (s) => s.replace(/[-_]+(\w)/g, (_, c) => c.toUpperCase());
// Quote date-like scalars (MCP protocolVersion) so the Agent Fabric parser keeps them as strings.
const dump = (o) => YAML.stringify(o, { lineWidth: 0, aliasDuplicateObjects: false }).replace(/: (\d{4}-\d{2}-\d{2})$/gm, ': "$1"');
const MODES = ['application/json', 'text/plain'];

// Built-in Agent Fabric policies used by the technical variants (configurations follow each policy's schema).
const POL = {
  // Not used here because the CLI already applies them to every connection: mcp-support, tracing,
  // agent-connection-telemetry, a2a card policies and (on brokers) user-context-propagation.
  rateLimit: (n) => ({ assetId: 'rate-limiting', version: '1.5.1', configuration: { rateLimits: [{ maximumRequests: n, timePeriodInMilliseconds: 60000 }], exposeHeaders: true } }),
  headers: (h) => ({ assetId: 'header-injection', version: '1.3.3', configuration: { inboundHeaders: h } }),
  mcpPii: { assetId: 'mcp-pii-detector', version: '1.0.1', configuration: { entities: ['Email', 'US SSN', 'Credit Card', 'Phone Number'], action: 'Log and mask' } },
  mcpSchema: { assetId: 'mcp-schema-validation', version: '1.3.0', configuration: { validateToolSchema: true } },
  a2aPii: { assetId: 'a-two-a-pii-detector', version: '1.0.2', configuration: { entities: ['Email', 'US SSN', 'Credit Card'], action: 'Log' } },
  a2aV1Pii: { assetId: 'a2a-v1-pii-detector', version: '1.0.0', configuration: { entities: ['Email', 'US SSN', 'Credit Card'], action: 'Log' } },
  logOut: { assetId: 'message-logging-outbound', version: '2.1.0', configuration: { loggingConfiguration: [{ itemName: 'Upstream calls', itemData: { message: '#[attributes.method ++ " " ++ attributes.requestPath]', level: 'INFO', firstSection: true, secondSection: false } }] } },
  prompt: (text) => ({ assetId: 'a-two-a-prompt-decorator', version: '1.0.2', configuration: { textDecorators: [{ text: `#['${text}']` }] } }),
};

// Secured variant (#31): authenticated connections with deploy-time secret variables, the LLM behind a
// configurable gateway URL, outbound message logging. A2D mocks ignore the credentials, so it still runs.
const SEC = (i) => (i % 2 === 0 ? 'basic' : 'apikey-client-credentials');
function secAuth(kind, g, vars) {
  if (kind === 'basic') {
    vars[g].username = { description: 'User name for Basic authentication', default: 'octoloom-demo', secret: false };
    vars[g].password = { description: 'Password (secret, entered at deploy time)', default: '', secret: true };
    return { kind: 'basic', username: `\${${g}.username}`, password: `\${${g}.password}` };
  }
  vars[g].clientId = { description: 'Client ID for Client ID Enforcement', default: 'octoloom-demo-client', secret: false };
  vars[g].clientSecret = { description: 'Client secret (secret, entered at deploy time)', default: '', secret: true };
  return { kind: 'apikey-client-credentials', clientId: { value: `\${${g}.clientId}`, name: 'client_id' }, clientSecret: { value: `\${${g}.clientSecret}`, name: 'client_secret' } };
}
const LLM_GW = { llmGateway: { url: { description: 'OpenAI-compatible LLM endpoint: api.openai.com or your LLM gateway in front of it', default: 'https://api.openai.com/v1', secret: false } } };

function skills(list) {
  return list.map((s) => ({ id: s.id, name: s.name, description: s.description, tags: s.tags, examples: s.examples }));
}

function exchange(u, vars, deps) {
  return JSON.stringify({
    main: 'agent-network.yaml', name: u.slug, classifier: u.version === 'v1' ? 'agent-network' : 'agentic-network',
    descriptorVersion: '1.0.0', apiVersion: 'v1', tags: ['octoloom-example'],
    metadata: { variables: vars }, dependencies: deps,
    groupId: '${organizationId}', assetId: u.slug, version: '1.0.0',
  }, null, 2) + '\n';
}

const policyDeps = (used) => [...new Map(used.map((p) => [p.assetId, p])).values()].map((p) => ({ classifier: 'schema', packaging: 'zip', groupId: AF, assetId: p.assetId, version: p.version }));

// ─────────────────────────────── v1 (Probabilistic) ───────────────────────────────
function v1(u, technical, secured) {
  const rec = ids[u.id];
  const R = (k) => `${u.prefix}_${k}`;
  const b = R(u.broker.key);
  const vars = { ingressgw: { url: { description: 'Ingress gateway base URL (the broker is served under it)', default: '', secret: false } }, openai: { apiKey: { description: 'OpenAI API key (secret, injected at deploy time)', default: '', secret: true } }, ...(secured ? LLM_GW : {}) };
  const used = [];
  const pol = (p) => (used.push(p), { ref: { name: p.assetId, namespace: AF }, configuration: p.configuration });
  const net = {
    schemaVersion: '1.0.0',
    label: `${u.title}${technical ? ' (governed)' : secured ? ' (secured)' : ''}`,
    brokers: {
      [b]: {
        card: { protocolVersion: '0.3.0', name: b, description: u.summary, url: `\${ingressgw.url}/${b}`, version: '1.0.0', capabilities: { streaming: false, pushNotifications: false, stateTransitionHistory: false }, defaultInputModes: MODES, defaultOutputModes: MODES, skills: skills(u.broker.skills) },
        spec: {
          llm: { ref: { name: R('openai') }, configuration: { model: MODEL } },
          instructions: u.broker.instructions,
          links: u.agents.map((a) => ({ agent: { ref: { name: R(a.key) } } })),
          tools: u.mcps.map((m) => ({ mcp: { ref: { name: R(m.key) }, allowed: m.tools.map((t) => t.name) } })),
          maxNumberOfLoops: 25, maxConsecutiveErrors: 3, taskTimeoutSecs: 90,
          ...(technical || secured ? { policies: [pol(POL.rateLimit(60))] } : {}),
        },
      },
    },
    llmProviders: { [R('openai')]: { label: 'OpenAI', description: 'OpenAI LLM provider', metadata: { platform: 'OpenAI', models: [MODEL] } } },
    connections: {
      'openai-connection': { kind: 'llm', ref: { name: R('openai') }, spec: { url: secured ? '${llmGateway.url}/' : 'https://api.openai.com/v1/', configuration: { apiKey: '${openai.apiKey}', timeout: 600000 } } },
    },
    mcpServers: {},
    agents: {},
  };
  for (const [i, m] of u.mcps.entries()) {
    const v = camel(m.key);
    vars[v] = { url: { description: `${m.name} (A2D mock) base URL`, default: `${A2D}/${rec.mcps[m.key]}/`, secret: false } };
    net.connections[`${m.key}-connection`] = { kind: 'mcp', ref: { name: R(m.key) }, spec: { url: `\${${v}.url}`, ...(secured ? { authentication: secAuth(SEC(i + 1), v, vars) } : {}), ...(technical ? { policies: i % 2 === 0 ? [pol(POL.mcpPii)] : [pol(POL.mcpSchema), pol(POL.headers([{ key: 'x-octoloom-source', value: u.slug }]))] } : {}) } };
    net.mcpServers[R(m.key)] = { label: m.name, description: m.description, metadata: { transport: { kind: 'streamableHttp', path: '/mcp' }, tools: m.tools.map((t) => ({ name: t.name, description: t.description, inputSchema: { type: 'object', properties: Object.fromEntries(Object.entries(t.input).map(([k, [type, description]]) => [k, { type, description }])), required: t.required } })) } };
  }
  for (const [i, a] of u.agents.entries()) {
    const v = camel(a.key);
    const url = `${A2D}/${rec.agents[a.key]}/a2a`;
    vars[v] = { url: { description: `${a.name} (A2D mock, A2A 0.3.0) URL`, default: url, secret: false } };
    net.connections[`${a.key}-connection`] = { kind: 'agent', ref: { name: R(a.key) }, spec: { url: `\${${v}.url}`, ...(secured ? { authentication: secAuth(SEC(i), v, vars) } : {}), ...(technical ? { policies: i % 2 === 0 ? [pol(POL.a2aPii)] : [pol(POL.headers([{ key: 'x-correlation-source', value: b }])), pol(POL.prompt('Answer concisely and never include personal data.'))] } : {}) } };
    net.agents[R(a.key)] = { label: a.name, description: a.description, metadata: { platform: a.platform, protocol: 'a2a' }, card: { name: a.name, description: a.description, url: `\${${v}.url}`, protocolVersion: '0.3.0', version: '1.0.0', capabilities: { streaming: false, pushNotifications: false }, defaultInputModes: MODES, defaultOutputModes: MODES, skills: skills(a.skills) } };
  }
  return { files: { 'agent-network.yaml': dump(net), 'exchange.json': exchange(u, vars, policyDeps(used)) }, policies: [...new Set(used.map((p) => p.assetId))] };
}

// ─────────────────────────────── v2 (Deterministic) ───────────────────────────────
function v2(u, technical, secured) {
  const rec = ids[u.id];
  const f = FLOWS[u.id];
  const R = (k) => `${u.prefix}_${k}`;
  const b = R(u.broker.key);
  const file = u.broker.key.replace(/_/g, '-');
  const vars = { openai: { apiKey: { description: 'OpenAI API key (secret, injected at deploy time)', default: '', secret: true } }, ...(secured ? LLM_GW : {}) };
  const used = [];
  const decl = {};
  const bind = (key, p) => (used.push(p), (decl[key] = { ref: { name: p.assetId, namespace: AF }, configuration: p.configuration }), { ref: { name: key } });
  const inline = (p) => (used.push(p), { policy: { ref: { name: p.assetId, namespace: AF }, configuration: p.configuration } });
  const net = {
    agentNetwork: '2.0.0',
    info: { label: `${u.title}${technical ? ' (governed)' : secured ? ' (secured)' : ''}`, version: 'v1', description: u.summary },
    registry: { agents: {}, mcps: {}, llms: { [R('openai')]: { info: { label: 'OpenAI' }, metadata: { platform: 'OpenAI', models: [MODEL] } } } },
    context: { connections: {} },
    brokers: {},
  };
  for (const a of u.agents) {
    const url = `${A2D}/${rec.agents[a.key]}/a2a`;
    const card = { name: a.name, description: a.description, version: '1.0.0', capabilities: { pushNotifications: false }, defaultInputModes: MODES, defaultOutputModes: MODES, skills: skills(a.skills) };
    net.registry.agents[R(a.key)] = { info: { label: a.name, description: a.description }, metadata: { platform: a.platform, interfaces: a.proto === '1.0' ? { a2a: { card: { ...card, supportedInterfaces: [{ url, protocolBinding: 'JSONRPC', protocolVersion: '1.0' }] } } } : { a2a_v03: { card: { ...card, url, protocolVersion: '0.3.0' } } } } };
  }
  for (const m of u.mcps) net.registry.mcps[R(m.key)] = { info: { label: m.name, description: m.description }, metadata: { protocolVersion: '2025-06-18', transport: { kind: 'streamableHttp', path: '/mcp' }, tools: m.tools.map((t) => ({ name: t.name, description: t.description, inputSchema: { type: 'object', properties: Object.fromEntries(Object.entries(t.input).map(([k, [type, description]]) => [k, { type, description }])), required: t.required } })) } };
  for (const [i, a] of u.agents.entries()) {
    const v = camel(a.key);
    vars[v] = { url: { description: `${a.name} (A2D mock, A2A ${a.proto}) URL`, default: `${A2D}/${rec.agents[a.key]}/a2a`, secret: false } };
    net.context.connections[`${a.key}_connection`] = { kind: 'a2a', ref: { name: R(a.key) }, url: `\${${v}.url}`, ...(secured ? { authentication: secAuth(SEC(i), v, vars), policies: { outbound: [bind('log_upstream', POL.logOut)] } } : {}), ...(technical ? { policies: { inbound: i % 2 === 0 ? [a.proto === '1.0' ? bind('a2a_v1_pii', POL.a2aV1Pii) : bind('a2a_pii', POL.a2aPii)] : [inline(POL.headers([{ key: 'x-correlation-source', value: b }]))] } } : {}) };
  }
  for (const [i, m] of u.mcps.entries()) {
    const v = camel(m.key);
    vars[v] = { url: { description: `${m.name} (A2D mock) base URL`, default: `${A2D}/${rec.mcps[m.key]}/`, secret: false } };
    net.context.connections[`${m.key}_connection`] = { kind: 'mcp', ref: { name: R(m.key) }, url: `\${${v}.url}`, ...(secured ? { authentication: secAuth(SEC(i + 1), v, vars), policies: { outbound: [bind('log_upstream', POL.logOut)] } } : {}), ...(technical ? { policies: { inbound: i % 2 === 0 ? [bind('mcp_pii', POL.mcpPii), bind('mcp_schema', POL.mcpSchema)] : [bind('mcp_pii', POL.mcpPii), inline(POL.headers([{ key: 'x-octoloom-source', value: u.slug }]))] } } : {}) };
  }
  net.context.connections.openai_connection = { kind: 'llm', ref: { name: R('openai') }, url: secured ? '${llmGateway.url}' : 'https://api.openai.com/v1', authentication: { kind: 'apiKey', apiKey: '${openai.apiKey}' } };
  net.brokers[b] = { kind: 'AgentScript', implementation: `./brokers/${file}.agent`, interfaces: { a2a: { card: { name: u.broker.name, description: u.summary, version: '1.0.0', capabilities: { streaming: true, pushNotifications: false }, defaultInputModes: ['text/plain'], defaultOutputModes: ['text/plain'], skills: skills(u.broker.skills) }, ...(technical || secured ? { policies: { inbound: [bind('rate_limit', POL.rateLimit(30))] } } : {}) } } };
  if (Object.keys(decl).length) net.context.policies = decl;

  const actions = Object.entries(f.actions).map(([k, a]) => a.a2a
    ? `  ${k}:\n    target: "a2a://${a.a2a}_connection"\n    kind: "a2a:send_message"`
    : `  ${k}:\n    target: "mcp://${a.mcp}_connection"\n    kind: "mcp:tool"\n    tool_name: "${a.tool}"${a.inputs ? `\n    inputs:\n${Object.entries(a.inputs).map(([n, t]) => `      ${n}: ${t}`).join('\n')}` : ''}`).join('\n');
  const agent = `# @dialect: AGENTFABRIC=1.0
# ${u.title}: ${u.summary}
# Upstreams are A2D mocks; see README.md for test prompts.

system:
  instructions: "${f.system.replace(/"/g, "'")}"

config:
  agent_name: "${file}"
  default_llm: @llm.default

llm:
  default:
    target: "llm://openai_connection"
    kind: "OpenAI"
    model: "${MODEL}"

actions:
${actions}

trigger ${camel(u.broker.key)}Trigger:
  kind: "a2a"
  target: "brokers://${b}/a2a"
  on_message: ->
    transition to ${f.start}

${f.body.trim()}
`;
  return { files: { 'agent-network.yaml': dump(net), 'exchange.json': exchange(u, vars, policyDeps(used)), [`brokers/${file}.agent`]: agent }, policies: [...new Set(used.map((p) => p.assetId))] };
}

function readme(u, t, technical, policies, secured, exchangeJson) {
  const v1 = u.version === 'v1';
  const vars = JSON.parse(exchangeJson).metadata?.variables ?? {};
  const flat = Object.entries(vars).flatMap(([g, o]) => Object.entries(o).map(([k, d]) => ({ key: `${g}.${k}`, ...d })));
  const secrets = flat.filter((x) => x.secret);
  const ask = flat.filter((x) => !x.secret && !x.default);
  const tries = TRY[u.id] ?? u.broker.skills.flatMap((s) => s.examples).map((p) => ({ p, see: '' }));
  const gov = technical
    ? [{ p: 'My email is jane.doe@example.com and my phone is +41 79 123 45 67. ' + tries[0].p, see: 'Same answer as the first prompt. The PII detector policies log the email and phone number; on the MCP connections with the MCP PII detector they are masked before the tool sees them. Check the policy logs in Anypoint Monitoring.' },
       { p: 'Send the first prompt more than 30 times within a minute', see: `The broker answers HTTP 429 (Too Many Requests) once the rate limit of ${v1 ? 60 : 30} requests per minute is reached.` }]
    : secured ? [{ p: tries[0].p, see: `Same answer as the plain variant: the A²D mocks accept any credentials. The Tracer shows each authenticated upstream call${v1 ? '' : ', and the outbound Message Logging policy writes one log line per call'}.` }] : [];
  const code = (x) => '`' + x + '`';
  return `# ${u.title}${technical ? ' (governed)' : secured ? ' (secured)' : ''}

${u.summary}

- Style: ${v1 ? 'Probabilistic (Agent Network 1.0): the LLM broker picks agents and tools from its instructions.' : 'Deterministic (Agent Network 2.0): an AgentScript flow in `brokers/` decides each step.'}
- Agents: ${u.agents.map((a) => `${a.name} (A2A ${a.proto}, ${a.platform})`).join(', ')}
- MCP servers: ${u.mcps.map((m) => `${m.name} (${m.tools.map((x) => x.name).join(', ')})`).join('; ')}
${technical ? `- Policies (Agent Fabric built-ins): ${policies.join(', ')}. They are declared in agent-network.yaml and listed as \`schema\` dependencies in exchange.json.\n` : ''}${secured ? `- Secured: every agent and MCP connection authenticates (Basic or Client ID enforcement, alternating). User names and client ids are variables, passwords and client secrets are secret variables asked for at deploy time. The LLM URL is the variable \`llmGateway.url\` (api.openai.com by default, or your LLM gateway).${v1 ? '' : ' Upstream calls are logged with the outbound Message Logging policy.'} Policies: ${policies.join(', ')}.\n` : ''}
All agents and MCP servers are public A2D mocks, so the network runs without any other system. No credentials are stored in this template.

## Deploy in 3 steps

1. **Setup & Connect**: connect Agent Fabric (connected app client ID and secret, organization). A²D is not needed: the mock URLs are already the defaults in \`exchange.json\`.
2. ${ask.length ? `In \`exchange.json\`, fill in ${ask.map((x) => `${code(x.key)} (${x.description.replace(/\s*\(.*\)$/, '').toLowerCase()})`).join(', ')}. ` : ''}In **Projects & Deploy**, click **Deploy** on this project (or **Build & Deploy** in the editor) and pick your gateway. Octoloom asks for each secret variable; nothing you type is stored:
${secrets.map((x) => `   - ${code(x.key)}: ${x.key === 'openai.apiKey' ? 'your OpenAI API key (required)' : x.description.replace(/\s*\(.*\)$/, '')}${x.key === 'openai.apiKey' ? '' : ' (any value works with the A²D mocks)'}`).join('\n')}
3. When the status light turns green (**Deployed and running**), click **Open chat** and paste a prompt below. The **ANT** icon under a reply opens the task in the Agent Network Tracer, with each agent and tool call.

## Try it

${[...tries, ...gov].map((x) => `- **${x.p}**${x.see ? `\n  - You should see: ${x.see}` : ''}`).join('\n')}
${v1 ? '\nThe broker is probabilistic: the LLM picks the agents and tools, so the wording and the order of the calls can change between runs. The ids and numbers come from the mocks and stay the same.\n' : '\nThe broker is deterministic: the branches are fixed in the flow in `brokers/` (open the `.agent` file to see them). The LLM only reads the ids from your prompt and writes the reply text, so the same input takes the same branch.\n'}`;
}

const index = [];
for (const u of USECASES) {
  for (const mode of ['plain', 'governed', ...(u.secured ? ['secured'] : [])]) {
    const technical = mode === 'governed';
    const secured = mode === 'secured';
    const id = mode === 'plain' ? u.id : `${u.id}-${mode}`;
    const base = id.replace(/^v[12]-/, '').replace(/-(governed|secured)$/, '');
    // Registry entries become org-wide Exchange assets, so their ids carry a per-template prefix.
    // The extension replaces it with the user's project prefix when a template is instantiated.
    const prefix = `octo_${base.split('-').map((w) => w[0]).join('')}${u.version.slice(1)}${technical ? 'g' : secured ? 's' : ''}`;
    const t = { ...u, prefix, slug: id.replace(/^v[12]-/, '') + (u.version === 'v1' ? '-v1' : '-v2') };
    const r = u.version === 'v1' ? v1(t, technical, secured) : v2(t, technical, secured);
    const dir = path.join(out, id);
    fs.rmSync(dir, { recursive: true, force: true });
    for (const [f, c] of Object.entries({ ...r.files, 'README.md': readme(u, t, technical, r.policies, secured, r.files['exchange.json']) })) {
      fs.mkdirSync(path.dirname(path.join(dir, f)), { recursive: true });
      fs.writeFileSync(path.join(dir, f), c);
    }
    index.push({
      id, version: u.version, category: mode === 'plain' ? 'usecase' : 'technical', title: mode === 'plain' ? u.title : `${u.title}: ${mode}`,
      summary: technical ? `${u.summary} Adds built-in policies: ${r.policies.join(', ')}.` : secured ? `${u.summary} Secured: authenticated connections (Basic, Client ID enforcement) with secret variables, the LLM behind a gateway URL${u.version === 'v2' ? ', outbound message logging' : ''}.` : u.summary,
      agents: u.agents.length, mcps: u.mcps.length, protocols: [...new Set(u.agents.map((a) => a.proto))], policies: r.policies,
      files: Object.keys(r.files).concat('README.md'), assetId: t.slug, prefix,
    });
  }
}
fs.writeFileSync(path.join(out, 'index.json'), JSON.stringify({ schema: 1, templates: index }, null, 2) + '\n');
console.log(index.length, 'templates');
