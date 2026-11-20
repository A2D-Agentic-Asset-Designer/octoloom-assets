"""Path 3 of the template tutorials: build the use case from a blank project, no code (octoloom#253).

Every step uses a form, a menu or a button of Octoloom: New Project (Blank + starter broker), the
canvas + menu (Empty entries), the inspector forms, the Problems fixes, the exchange.json form, the
card rows (Tools, Link to), the broker panels (v1) and the flow editor (v2). The screenshots are
staged states of the same project, built from the template data with the template id prefix removed.
"""
import copy, json, re
import yaml

PREFIX = re.compile(r'octo_[a-z0-9]+_')
AUTH = {'basic': 'Basic (username / password)', 'apiKey': 'API key', 'apikey-client-credentials': 'Client ID enforcement (client_id / client_secret headers)',
        'oauth2-client-credentials': 'OAuth 2.0 client credentials (bearer token)'}
KIND = {'trigger': 'Trigger', 'generator': 'Generator', 'subagent': 'Subagent', 'router': 'Router', 'orchestrator': 'Orchestrator', 'executor': 'Executor', 'echo': 'Reply'}


def slug(s, sep='-'):
    return re.sub(r'^%s+|%s+$' % (re.escape(sep), re.escape(sep)), '', re.sub(r'[^a-zA-Z0-9]+', sep, s.strip())).lower()


def camel(s):
    return re.sub(r'[-_]+(\w)', lambda m: m.group(1).upper(), s)


def dump(y):
    return yaml.safe_dump(y, sort_keys=False, allow_unicode=True, width=10000)


def code(s):
    s = str(s)
    return '``' + s + '``' if '`' in s else '`' + s + '`'


# ---------- AgentScript (read only, to describe the flow) ----------
def agent_blocks(text):
    """Top-level blocks of an .agent file as (key, dict). Procedures (->) are kept as text."""
    out = []
    for l in text.splitlines():
        if l.lstrip().startswith('#') and not l.startswith('  '):
            continue
        m = re.match(r'^(\w+)(?: (\w+))?:\s*$', l)
        if m:
            out.append([m.group(1) + (' ' + m.group(2) if m.group(2) else ''), []]); continue
        if out: out[-1][1].append(l)
    res = []
    for k, body in out:
        y = []
        for l in body:
            m = re.match(r'^(\s*(?:- )?)(\w+):\s*->\s*$', l)
            if m: y.append(f'{m.group(1)}{m.group(2)}: |'); continue
            m = re.match(r'^(\s*(?:- )?)(\w+):\s+(.+)$', l)
            if m and not re.match(r'^(".*"|\||\d+(\.\d+)?|true|false)$', m.group(3).strip()):
                y.append(f"{m.group(1)}{m.group(2)}: '{m.group(3).strip().replace(chr(39), chr(39) * 2)}'"); continue
            y.append(l)
        try:
            res.append((k, yaml.safe_load('\n'.join(y)) or {}))
        except Exception:
            res.append((k, {}))
    return res


def proc_target(s):
    m = re.search(r'transition to @(\w+)\.(\w+)', s or '')
    return f'{m.group(2)}' if m else None


def text_of(s):
    s = (s or '').strip()
    return '\n'.join(re.sub(r'^\| ?', '', x) for x in s.splitlines())


# ---------- the project, without template prefixes ----------
def stripped(t, m):
    """agent-network.yaml (dict), exchange.json (dict), flow (file, text) of the template, prefix removed, v2 broker key as the starter makes it."""
    raw = PREFIX.sub('', open(f"{m['dir']}/agent-network.yaml").read())
    y = yaml.safe_load(raw)
    ex = json.loads(PREFIX.sub('', json.dumps(m['ex'])))
    ex['name'] = ex['assetId'] = project_name(t)
    flow = None
    if t['version'] == 'v2':
        (bk, b), = y['brokers'].items()
        name = b['interfaces']['a2a']['card']['name']
        nk, nf = slug(name, '_'), f"brokers/{slug(name)}.agent"
        b['implementation'] = './' + nf
        y['brokers'] = {nk: b}
        f, x = next(iter(m['flows'].values()))
        x = PREFIX.sub('', x).replace(f'brokers://{bk}/', f'brokers://{nk}/')
        x = re.sub(r'^(# .*\n)+', '', x.split('\n', 1)[1] if x.startswith('# @dialect') else x)
        x = '# @dialect: AGENTFABRIC=1.0\n\n' + x.lstrip()
        x = re.sub(r'^trigger \w+:', f'trigger {camel(nk)}Trigger:', x, flags=re.M)
        flow = (nf, x)
    return y, ex, flow


def project_name(t):
    return re.sub(r'-v[12]$', '', t['assetId']) + '-scratch'


def broker_of(y, v):
    (bk, b), = y['brokers'].items()
    return bk, b, (b['card']['name'] if v == 'v1' else b['interfaces']['a2a']['card']['name'])


def starter_flow(bk, name):
    return f'''# @dialect: AGENTFABRIC=1.0

system:
  instructions: "You are the {name} agent."

config:
  agent_name: "{slug(name)}"
  default_llm: @llm.default

llm:
  default:
    target: "llm://openai_connection"
    kind: "OpenAI"
    model: "gpt-5-mini"

actions:

trigger {camel(bk)}Trigger:
  kind: "a2a"
  target: "brokers://{bk}/a2a"
  on_message: ->
    transition to @subagent.assistant

subagent assistant:
  description: "Answers the request."
  label: "Assistant"
  reasoning:
    instructions: ->
      | {{!@request.payload.message.parts[0].text}}
  on_exit: ->
    transition to @echo.done

echo done:
  kind: "a2a:status_update_event"
  state: "TASK_STATE_COMPLETED"
  message: a2a.message({{messageId: uuid(), parts: [a2a.textPart(@subagent.assistant.output)]}})
'''


def stage(y, v, upto):
    """Network after step `upto`: start, agents, mcps, conns, tools, links, final."""
    order = ['start', 'agents', 'mcps', 'conns', 'tools', 'links', 'final']
    n = order.index(upto)
    s = copy.deepcopy(y)
    bk, b, _ = broker_of(s, v)
    if v == 'v1':
        if n < order.index('links'):
            b['spec'].update({'instructions': ['You are a helpful broker. Route each request to the best agent or tool.'], 'links': [], 'tools': [], 'taskTimeoutSecs': 60})
            b['spec']['llm']['configuration'] = {'model': 'gpt-5-mini'}
            b['spec'].pop('policies', None)
        if n < order.index('agents'): s.pop('agents', None)
        if n < order.index('mcps'): s.pop('mcpServers', None)
        if n < order.index('conns'): s['connections'] = {k: c for k, c in s['connections'].items() if c.get('kind') == 'llm'}
        if n < order.index('tools'):
            for x in (s.get('mcpServers') or {}).values(): x.get('metadata', {}).pop('tools', None)
        if n < order.index('final'):
            for c in s.get('connections', {}).values(): c.get('spec', {}).pop('policies', None)
    else:
        r = s.setdefault('registry', {})
        if n < order.index('agents'): r.pop('agents', None)
        if n < order.index('mcps'): r.pop('mcps', None)
        if not r: s.pop('registry')
        if n < order.index('conns'): s['context']['connections'] = {k: c for k, c in s['context']['connections'].items() if c.get('kind') == 'llm'}
        if n < order.index('tools'):
            for x in (s.get('registry', {}).get('mcps') or {}).values(): x.get('metadata', {}).pop('tools', None)
        if n < order.index('final'):
            s['context'].pop('policies', None)
            b['interfaces']['a2a'].pop('policies', None)
            for c in s['context']['connections'].values(): c.pop('policies', None)
    return s


# ---------- what the reader fills in ----------
def entities(y, v):
    if v == 'v1':
        ag = [(k, a.get('label', k), a.get('description', ''), a.get('metadata', {}).get('platform', ''), a.get('card', {})) for k, a in (y.get('agents') or {}).items()]
        mc = [(k, s.get('label', k), s.get('description', ''), s.get('metadata', {}).get('tools') or []) for k, s in (y.get('mcpServers') or {}).items()]
        cs = [(k, c) for k, c in y['connections'].items() if c.get('kind') != 'llm']
    else:
        r = y.get('registry') or {}
        ag = []
        for k, a in (r.get('agents') or {}).items():
            ifs = a.get('metadata', {}).get('interfaces', {})
            ik = next(iter(ifs), 'a2a')
            ag.append((k, a.get('info', {}).get('label', k), a.get('info', {}).get('description', ''), a.get('metadata', {}).get('platform', ''), dict(ifs.get(ik, {}).get('card', {}), _iface=ik)))
        mc = [(k, s.get('info', {}).get('label', k), s.get('info', {}).get('description', ''), s.get('metadata', {}).get('tools') or []) for k, s in (r.get('mcps') or {}).items()]
        cs = [(k, c) for k, c in y['context']['connections'].items() if c.get('kind') != 'llm']
    return ag, mc, cs


def conn_url(c, v):
    return (c.get('spec') or {}).get('url') if v == 'v1' else c.get('url')


def conn_auth(c, v):
    return (c.get('spec') or {}).get('authentication') if v == 'v1' else c.get('authentication')


def conn_policies(c, v):
    if v == 'v1': return [('', p) for p in ((c.get('spec') or {}).get('policies') or [])]
    p = c.get('policies') or {}
    return [(d, x) for d in ('inbound', 'outbound') for x in (p.get(d) or [])]


def policy_def(x, ctxpol):
    """(asset id, configuration) of a policy entry: v1 {ref, configuration}, v2 binding {ref:{name: binding}} or inline {policy: …}."""
    if 'policy' in x: return x['policy']['ref']['name'], x['policy'].get('configuration') or {}
    name = x.get('ref', {}).get('name')
    if name in ctxpol: return ctxpol[name]['ref']['name'], ctxpol[name].get('configuration') or {}
    return name, x.get('configuration') or {}


def cfg_lines(cfg, ind='  '):
    def one(val):
        if isinstance(val, bool): return 'on' if val else 'off'
        if isinstance(val, dict):
            if set(val) == {'key', 'value'}: return f"`{val['key']}` = `{val['value']}`"
            return ', '.join(f"{k} `{x}`" for k, x in val.items())
        return code(val)
    out = []
    for k, val in cfg.items():
        if isinstance(val, list) and val and all(isinstance(x, str) for x in val):
            out.append(f"{ind}- **{k}**: " + ', '.join(code(x) for x in val))
        elif isinstance(val, list):
            out.append(f"{ind}- **{k}** (one entry each, **+**): " + '; '.join(one(x) for x in val))
        else:
            out.append(f"{ind}- **{k}**: {one(val)}")
    return out


POLICY_NAME = {'rate-limiting': 'Rate Limiting', 'header-injection': 'Header Injection', 'jwt-validation': 'JWT Validation', 'mcp-pii-detector': 'MCP PII Detector',
               'mcp-schema-validation': 'MCP Schema Validation', 'a-two-a-pii-detector': 'A2A PII Detector', 'a2a-v1-pii-detector': 'A2A v1 PII Detector',
               'a-two-a-prompt-decorator': 'A2A Prompt Decorator', 'response-timeout': 'Response Timeout', 'message-logging-outbound': 'Message Logging (outbound)'}


def path3(t, m, img, n0=1):
    """Markdown lines of Path 3."""
    v = t['version']
    y, ex, flow = stripped(t, m)
    bk, b, bname = broker_of(y, v)
    ag, mc, cs = entities(y, v)
    tid = t['id']
    L = ['## Path 3: Build it from scratch', '',
         f"Here you build the same network yourself, starting from a blank project. Every step uses a form, a menu or a button. You never import the template, and you never type YAML{' or AgentScript' if v == 'v2' else ''}. The names below are the template's names without the `{t['prefix']}_` prefix. You can use your own names, but keep them consistent.", '',
         '> The text fields take plain values. Where a value looks like `${group.name}`, type it as shown: it is a **variable** that `exchange.json` declares and that deploy fills in.', '']
    n = n0
    def step(title):
        nonlocal n
        L.extend([f'### Step 3.{n}. {title}', '']); n += 1

    step('Create a blank project with a starter broker')
    L += [f"Connect Octoloom first, as in [Path 2, Step 1](#step-1-connect-octoloom). Then, on **Home**, click **New {'Probabilistic' if v == 'v1' else 'Deterministic'} Network**. In **2 Start from**, choose **Blank** and turn on **Add a starter broker**.", '',
          f"- **Broker name**: `{bname if v == 'v2' else bk}`",
          f"- **Name**: `{project_name(t)}` (the Exchange asset id; a different name from the template, so both can live in one org)",
          '- **Parent folder**: pick a folder, then click **Create blank project**.', '',
          img('scratch-new', 'Blank project with a starter broker'), '',
          ('The starter broker is an LLM broker with an OpenAI LLM (`openai` provider, `openai-connection`) and default instructions. The LLM is already done.' if v == 'v1'
           else f"The starter broker `{bk}` has an OpenAI LLM connection (`openai_connection`, MuleSoft's published OpenAI LLM) and a flow `{flow[0]}` with a trigger, one subagent and the built-in `done` reply. The LLM is already done."), '']

    if t.get('mocked'):
        step('Switch the LLM to the A²D LLM mock')
        L += ["This template needs no OpenAI key: its LLM is an **A²D LLM mock** with scripted answers. Open the **Asset Palette** (Octoloom side bar), pick the **A²D** tab and the **LLMs** filter, then drag **Octoloom " + t['title'].replace(' (fully mocked)', '') + " LLM** onto the broker card.", '',
              ('- It adds the project LLM ' + ('(`llmProviders`)' if v == 'v1' else '(`registry.llms`)') + ' and a connection to the mock URL with the placeholder key `a2d-mock-key`, and switches the broker to the mock\'s first model. No Exchange dependency is added.'),
              "- Rename the variable group to `a2dLlm` in `exchange.json` (the template uses `${a2dLlm.url}` and `${a2dLlm.apiKey}`), and remove the starter OpenAI connection and its `openai` variables.", '']

    if ag:
        step('Add the agents')
        L += ['On the canvas, click **+** (Add to the network) → **Agent** → **Empty**. The new agent opens in the inspector on the right. Fill it in, then repeat for each agent:', '',
              img('scratch-add', 'The Add to the network menu with the Agent submenu'), '']
        for k, lab, desc, plat, card in ag:
            L.append(f"- **{lab}**")
            L.append(f"  - **Identity → Key**: `{k}`")
            if v == 'v1':
                L.append(f"  - **Label**: {lab} · **Description**: {desc}")
                if plat: L.append(f"  - **Metadata → Platform**: `{plat}` (or click its icon under **Agent framework**)")
                L.append(f"  - **Agent card**: **Name** {card.get('name', lab)}, **Description** as above, **URL** `{card.get('url', '')}`, **Protocol version** `0.3.0`")
            else:
                L.append(f"  - **Info → Label**: {lab} · **Description**: {desc}")
                if plat: L.append(f"  - **Metadata → Platform**: `{plat}` (or click its icon under **Agent framework**)")
                if card.get('_iface') == 'a2a':
                    url = (card.get('supportedInterfaces') or [{}])[0].get('url', '')
                    L.append(f"  - **Interface**: click `a2a` (A2A 1.0). **Agent card (A2A 1.x)**: **Name** {card.get('name', lab)}, **Description** as above, **Supported interfaces → URL** `{url}`, Binding `JSONRPC`, Protocol version `1.0`")
                else:
                    L.append(f"  - **Interface**: keep `a2a_v03` (A2A 0.3.0). **Agent card (A2A 0.3)**: **Name** {card.get('name', lab)}, **Description** as above, **URL** `{card.get('url', '')}`")
        L += ['', img('scratch-agent', 'An agent in the inspector'), '',
              'The card skills are optional. Once the agent has a connection (two steps on), the inspector offers **Read skills from the live agent**, which fills them from the running agent.', '']

    step('Add the MCP servers')
    L.append('Click **+** → **MCP server** → **Empty**, then fill in:')
    L.append('')
    for k, lab, desc, tools in mc:
        L.append(f"- **{lab}**: **Key** `{k}`, **Label** {lab}, **Description** {desc.rstrip('.')}" + (' · **Protocol version** `2025-06-18`' if v == 'v2' else '') + '. The transport is already Streamable HTTP on `/mcp`.')
    L.append('')

    step('Add the connections')
    L += ['A connection is the URL (and authentication) Agent Fabric uses to reach an agent or an MCP server. Click **+** → **Connection** → **Empty** once per ' + ('agent and MCP server' if ag else 'MCP server') + ', and fill in:', '',
          '| Key | Kind | ' + ('Target → Name' if v == 'v1' else 'Registry entry → Name') + ' | URL |', '|---|---|---|---|']
    for k, c in cs:
        L.append(f"| `{k}` | `{c.get('kind')}` | `{c.get('ref', {}).get('name')}` | `{conn_url(c, v)}` |")
    L += ['', img('scratch-conn', 'A connection in the inspector'), '']
    secured = [(k, c) for k, c in cs if (conn_auth(c, v) or {}).get('kind') not in (None, 'none')]
    if secured:
        L += ['These connections also authenticate. In **Authentication**, pick the kind and type the values exactly as shown. The values are variables, and the secret ones are asked for at deploy time:', '']
        for k, c in secured:
            a = conn_auth(c, v)
            vals = []
            for f, x in a.items():
                if f == 'kind': continue
                if f == 'token' and isinstance(x, dict):
                    vals.append(f"**Token → Token URL** `{x.get('url')}`" + (f", **Body encoding** `{x['bodyEncoding']}`" if x.get('bodyEncoding') else '')); continue
                if isinstance(x, dict) and 'value' not in x:
                    vals.append(f"**{f}** " + ', '.join(f'{a} `{b}`' for a, b in x.items())); continue
                vals.append(f"**{f}** `{x['value'] if isinstance(x, dict) else x}`" + (f" (header `{x['name']}`)" if isinstance(x, dict) and x.get('name') else ''))
            L.append(f"- `{k}`: **{AUTH.get(a['kind'], a['kind'])}**, " + ', '.join(vals))
        L.append('')

    step('Declare the variables')
    L += ['The Problems bar now shows **Variable ${…} is not declared in exchange.json** for each new variable. Click **Add to exchange.json** on each one.',
          '', 'Then open `exchange.json` (it opens as a form) and, under **Variables**, set the defaults:', '', '| Variable | Default |', '|---|---|']
    sec = []
    for g, x in (ex.get('metadata', {}).get('variables') or {}).items():
        for nme, d in (x.items() if isinstance(x, dict) and not ('default' in x) else [(None, x)]):
            if not isinstance(d, dict): continue
            key = f'{g}.{nme}' if nme else g
            if d.get('secret'): sec.append(key); continue
            L.append(f"| `{key}` | {'`' + str(d.get('default')) + '`' if d.get('default') not in ('', None) else '(your ingress gateway URL)' if 'ingressgw' in key else '(empty)'} |")
    L += ['', f"Leave the secret variables ({', '.join('`' + s + '`' for s in sec)}) empty: deploy asks for them and never stores them." if sec else '', '',
          img('scratch-vars', 'The exchange.json form with the variables'), '']
    if v == 'v2':
        L += ['Also click **Remove it** on any **declared but not used** variable that the Problems bar shows.', '']

    step('Declare the MCP tools')
    L += ['On each MCP server card, click the **Tools** row (or its pencil). Octoloom reads the tool list from the running server: tick the tools below. You can also type a name in **Add a tool by name…**.', '']
    for k, lab, desc, tools in mc:
        L.append(f"- **{lab}**: " + ', '.join(f"`{x.get('name')}`" for x in tools))
    L += ['', img('scratch-tools', 'The Tools row of an MCP server card'), '']

    if v == 'v1':
        sp = b['spec']
        step('Give the broker its agents and tools' if ag else 'Give the broker its tools')
        L += [f"Select the broker `{bk}`. In the inspector:", '',
              *([f"1. Click **Agents (0)**. In **Add existing agent…**, pick each agent and click **Add**: " + ', '.join(f"`{l['agent']['ref']['name']}`" for l in sp.get('links') or []) + '.'] if sp.get('links') else []),
              f"{'2' if sp.get('links') else '1'}. Click **MCP servers (0)**. Add each server with **Add existing MCP server…**, then tick its **Allowed tools**:"]
        for tl in sp.get('tools') or []:
            L.append(f"   - `{tl['mcp']['ref']['name']}`: " + ', '.join(f'`{a}`' for a in tl['mcp'].get('allowed') or []))
        L += ['', img('scratch-links', 'The MCP servers of the broker with their allowed tools'), '']
        step('Write the broker instructions')
        L += ['Back in the broker inspector, open **Instructions and limits**. Replace the default instruction with these entries, one per line:', '']
        for x in sp.get('instructions') or []: L.append(f'- {x}')
        L += ['', f"Set **Max number of loops** `{sp.get('maxNumberOfLoops', 25)}`, **Max consecutive errors** `{sp.get('maxConsecutiveErrors', 3)}` and **Task timeout (s)** `{sp.get('taskTimeoutSecs', 60)}`."]
        eff = ((sp.get('llm') or {}).get('configuration') or {}).get('openAI', {}).get('reasoningEffort')
        if eff: L.append(f"Under **Model parameters → OpenAI**, set **Reasoning effort** to `{eff}`. The broker then answers within the gateway timeout.")
        L += ['', f"Optionally, fill the broker's **Agent card (A2A 0.3.0)** description: *{b['card'].get('description', '')}*", '', img('scratch-broker', 'The broker instructions and limits'), '']
    else:
        step('Link the agents and MCP servers to the broker' if ag else 'Link the MCP servers to the broker')
        L += [f"Every {'agent and MCP' if ag else 'MCP'} card now has a **Broker** row with **Link to {bname}**. Click it on each card. Octoloom adds the matching actions to the broker flow: {'one per agent and ' if ag else ''}one per declared MCP tool.", '',
              img('scratch-link', 'Link to the broker on the agent and MCP cards'), '']
        blocks = agent_blocks(flow[1])
        bd = dict(blocks)
        acts = bd.get('actions') or {}
        need = [(a, x['inputs']) for a, x in acts.items() if isinstance(x, dict) and x.get('inputs')]
        if need:
            L.append('**Link to** also reads the required inputs from the tool schema. In the flow (next step), open **Connections** in the explorer and check that these actions show them under **Inputs** (one per line; type them if they are missing):')
            for a, ins in need: L.append(f"- `{a}`: " + ', '.join(f"`{k}: {t_}`" for k, t_ in ins.items()))
            L.append('')
        step('Build the broker flow')
        llm = (bd.get('llm') or {}).get('default') or {}
        L += [f"On the broker card (or in its inspector), click **Open broker flow**. Then set up the flow:", '',
              f"1. **Settings → Language Settings**: on the `default` model, set **Reasoning effort (OpenAI)** to `{llm.get('reasoning_effort', 'MINIMAL')}`.",
              f"2. **Settings → System Messages**: set the instructions to: *{(bd.get('system') or {}).get('instructions', '')}*",
              '3. Select the `assistant` subagent and delete it (trash icon). The trigger and the built-in `done` reply stay.',
              '4. Add the steps below in order. Select the step that comes before, click **Add node**, pick the kind and choose **Empty**, then set its **API name** in **General**. Octoloom wires each new step after the selected one, and you set the exact next step in the inspector.', '',
              img('scratch-flow-add', 'Add node in the flow editor'), '']
        nodes = [(k, x) for k, x in blocks if re.match(r'^(generator|subagent|router|orchestrator|executor|echo) ', k)]
        trig = next((x for k, x in blocks if k.startswith('trigger ')), {})
        L.append(f"Select the trigger and, under **Go to**, pick `{proc_target(trig.get('on_message'))}` once that step exists.")
        L.append('')
        for k, x in nodes:
            kind, name = k.split()
            L.append(f"#### {KIND[kind]} `{name}`")
            L.append('')
            row = []
            if x.get('label'): row.append(f"**Label** {x['label']}")
            if x.get('description'): row.append(f"**Description** {x['description']}")
            if row: L.append('- ' + ' · '.join(row))
            sysi = (x.get('system') or {}).get('instructions')
            if sysi: L += ['- **System instructions**:', '', *['  > ' + l for l in text_of(sysi).splitlines()], '']
            if kind == 'generator' and x.get('prompt'): L += ['- **Prompt**:', '', *['  > ' + l for l in text_of(x['prompt']).splitlines()], '']
            rs = x.get('reasoning') or {}
            if rs.get('instructions'): L += ['- **Reasoning instructions**:', '', *['  > ' + l for l in text_of(rs['instructions']).splitlines()], '']
            if rs.get('actions'): L.append('- **Actions** (**+ Add action…**): ' + ', '.join(f"`{str(a).replace('@actions.', '')}`" for a in rs['actions'].values()))
            if rs.get('max_number_of_loops'): L.append(f"- **Limits → Max loops**: `{rs['max_number_of_loops']}`")
            outs = ((x.get('outputs') or rs.get('outputs') or {}).get('properties') or {})
            if outs:
                L.append('- **Structured output** (**Add field** for each):')
                for f, d in outs.items():
                    L.append(f"  - `{f}` ({d.get('type', 'string')}): {d.get('description', '')}" + (f" · **Allowed values** {', '.join('`' + str(e) + '`' for e in d['enum'])}" if d.get('enum') else ''))
            if kind == 'router':
                for r in x.get('routes') or []:
                    L.append(f"- **Routes** (**+**): **Label** {r.get('label', '')} · **When** {code(r.get('when'))} · **Go to** `{str(r.get('target')).split('.')[-1]}`")
                if x.get('otherwise'): L.append(f"- **Otherwise → Go to**: `{str(x['otherwise'].get('target')).split('.')[-1]}`")
            if kind == 'executor':
                L.append('- **Steps (do)**: **Run action**')
                for l in (x.get('do') or '').splitlines():
                    l = l.strip()
                    mm = re.match(r'run @actions\.(\w+)', l)
                    if mm: L.append(f"  - **Action** `{mm.group(1)}`")
                    mm = re.match(r'with (\w+) = (.+)', l)
                    if mm: L.append(f"    - **Bind argument** `{mm.group(1)}` = {code(mm.group(2))}")
            if kind == 'echo':
                msg = str(x.get('message', ''))
                mm = re.search(r'textPart\((.*)\)\]\}\)\s*$', msg)
                arg = mm.group(1).strip() if mm else msg
                if re.fullmatch(r'"[^"]*"', arg): L.append(f"- **Message text**: {arg[1:-1]}")
                else: L.append(f"- **Use expression**, then **Message (expression)**: {code(arg)}")
                L.append('- **Task state**: `TASK_STATE_COMPLETED`')
            nx = proc_target(x.get('on_exit'))
            if nx: L.append(f"- **Next step (on exit) → Go to**: `{nx}`")
            L.append('')
        L += [img('scratch-flow', 'The finished broker flow'), '',
              f"When you are done, the flow matches the template's flow ([Path 2, Step 4](#step-4-follow-the-broker-flow-agentscript)). The built-in `done` reply isn't used by this use case. The Problems bar shows **echo done is not reachable from the trigger** as a warning, and you can leave it.", '']

    pol_b = (b.get('spec') or {}).get('policies') if v == 'v1' else [('inbound', x) for x in ((b['interfaces']['a2a'].get('policies') or {}).get('inbound') or [])]
    ctxpol = (y.get('context') or {}).get('policies') or {}
    pol_c = [(k, conn_policies(c, v)) for k, c in cs if conn_policies(c, v)]
    if pol_b or pol_c:
        step('Add the policies')
        L += ['Select the broker or connection, scroll to **Policies** and click **Add policy**. Pick the policy (search by name)' + (', choose the **Direction**' if v == 'v2' else '') + ' and set its **Configuration** fields. **Header Injection** has its own header list. Octoloom also adds each policy as an `exchange.json` dependency.', '']
        for x in (pol_b or []):
            d, p = x if v == 'v2' else ('', x)
            a, cfg = policy_def(p, ctxpol)
            L.append(f"- Broker `{bk}`: **{POLICY_NAME.get(a, a)}**" + (f' ({d})' if d else ''))
            L += cfg_lines(cfg)
        for k, ps in pol_c:
            for d, p in ps:
                a, cfg = policy_def(p, ctxpol)
                L.append(f"- Connection `{k}`: **{POLICY_NAME.get(a, a)}**" + (f' ({d})' if d else ''))
                L += cfg_lines(cfg)
        L += ['', img('scratch-policy', 'Policies on the broker'), '']
        if v == 'v2' and ctxpol:
            L += ['The template declares a policy once under `context.policies` and points to it from each connection. **Add policy** writes each policy on its connection instead. Both give the same result at runtime.', '']

    step('Validate, deploy and chat')
    L += ['Run **Validate** from the canvas CLI menu and fix anything in the Problems bar. Then follow Path 2 from [Validate and build](#step-%d-validate-and-build) onwards' % (4 if v == 'v1' else 5) + ': deploy (enter the secrets), wait for the green light, open the chat and send the same prompts. Your network answers like the template, because it is the same network, built by hand.', '']
    return L


# ---------- screenshots ----------
def specs3(t, m, net_base):
    v = t['version']
    y, ex, flow = stripped(t, m)
    bk, b, bname = broker_of(y, v)
    ag, mc, cs = entities(y, v)
    tid = t['id']
    uri = f'file:///demo/{project_name(t)}/agent-network.yaml'
    net = {'version': v}
    if v == 'v2':
        net['brokerFiles'] = {bk: flow[0]}
        net['brokerTargets'] = {bk: ['openai_connection']}
        net['dependencies'] = net_base.get('dependencies', {})
    def doc(upto, targets=None, extra=None):
        nn = copy.deepcopy(net)
        if v == 'v2' and targets is not None: nn['brokerTargets'] = {bk: targets}
        return {'type': 'doc', 'kind': 'network', 'fileName': 'agent-network.yaml', 'uri': uri, 'text': dump(stage(y, v, upto)), 'guidesSeen': ['v1', 'v2', 'agent'], 'network': nn, **(extra or {})}
    sel = lambda i: {'type': 'select', 'id': i}
    S = '1500,900'
    setter = "const setv=(el,v)=>{if(!el)return;const s=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set;s.call(el,v);el.dispatchEvent(new Event('input',{bubbles:true}));};"
    sp = [{'name': 'scratch-new', 'view': 'newProject', 'size': '1300,1000', 'messages': [
        {'type': 'newProjectInit', 'version': v, 'templates': '@json:media/templates/index.json#templates', 'source': 'bundled', 'folder': '/Users/demo/projects'}],
        'after': setter + "[...document.querySelectorAll('.np-tab')].find(b=>b.textContent.startsWith('Blank'))?.click(); setTimeout(()=>{document.querySelector('.np-blank .sw')?.click(); setTimeout(()=>{const f=[...document.querySelectorAll('.np-field')]; setv(f.find(x=>x.querySelector('span')?.textContent==='Broker name')?.querySelector('input'), %s); setv(f.find(x=>x.querySelector('span')?.textContent==='Name')?.querySelector('input'), %s); },80);},80)" % (json.dumps(bname if v == 'v2' else bk), json.dumps(project_name(t)))}]
    sp.append({'name': 'scratch-add', 'view': 'network', 'size': S, 'messages': [doc('start')],
               'after': "setTimeout(()=>{const b=document.querySelector('button[title=\"Add to the network\"]'); const r=b.getBoundingClientRect(); b.dispatchEvent(new MouseEvent('click',{bubbles:true,clientX:r.x+r.width/2,clientY:r.y+r.height/2})); setTimeout(()=>{const s=[...document.querySelectorAll('.submenu .menu-item')].find(x=>x.querySelector('.mi-label')?.textContent==='Agent'); s?.click();},80);},150)"})
    if ag: sp.append({'name': 'scratch-agent', 'view': 'network', 'size': S, 'messages': [doc('agents'), sel(f'agent-{ag[0][0]}')]})
    if cs:
        c0 = next((k for k, c in cs if (conn_auth(c, v) or {}).get('kind') not in (None, 'none')), cs[0][0])
        sp.append({'name': 'scratch-conn', 'view': 'network', 'size': S, 'messages': [doc('conns'), sel(f'connection-{c0}')],
                   'after': "setTimeout(()=>{const s=[...document.querySelectorAll('.inspector .fsection-t')].find(x=>x.textContent==='Authentication'); if(s) s.closest('.fsection').scrollIntoView({block:'center'});},250)"})
    sp.append({'name': 'scratch-vars', 'view': 'exchange', 'size': '1400,1000', 'messages': [
        {'type': 'doc', 'kind': 'exchange', 'fileName': 'exchange.json', 'uri': f'file:///demo/{project_name(t)}/exchange.json', 'text': json.dumps(ex, indent=2), 'guidesSeen': ['v1', 'v2', 'agent'], 'network': {'version': v, 'description': ''}}],
        'after': "setTimeout(()=>{const s=[...document.querySelectorAll('.fsection-t, h2, h3, .ex-h')].find(x=>/^Variables/.test(x.textContent)); s?.scrollIntoView({block:'start'});},200)"})
    if mc:
        k0, _, _, tools0 = mc[0]
        sp.append({'name': 'scratch-tools', 'view': 'network', 'size': S, 'messages': [doc('tools'), {'type': 'mcpTools', 'key': k0, 'tools': [{'name': x.get('name'), 'description': x.get('description', '')} for x in tools0]}],
                   'after': "setTimeout(()=>{const c=[...document.querySelectorAll('.nc.k-mcp')][0]; const r=[...(c?.querySelectorAll('.nc-row')||[])].find(x=>x.querySelector('.nc-label')?.textContent==='Tools'); r?.querySelector('.nc-edit-btn')?.dispatchEvent(new MouseEvent('click',{bubbles:true}));},200)"})
    if v == 'v1':
        sp.append({'name': 'scratch-links', 'view': 'network', 'size': S, 'messages': [doc('links'), sel(f'broker-{bk}')],
                   'after': "setTimeout(()=>{[...document.querySelectorAll('.inspector button')].find(x=>x.textContent.trim().startsWith('MCP servers ('))?.click();},250)"})
        sp.append({'name': 'scratch-broker', 'view': 'network', 'size': S, 'messages': [doc('links'), sel(f'broker-{bk}')],
                   'after': "setTimeout(()=>{const s=[...document.querySelectorAll('.inspector .fsection-t')].find(x=>x.textContent==='Instructions and limits'); const f=s?.closest('.fsection'); if(f&&!f.classList.contains('open')) f.querySelector('.fsection-h').click(); setTimeout(()=>f?.scrollIntoView({block:'start'}),100);},250)"})
    else:
        sp.append({'name': 'scratch-link', 'view': 'network', 'size': S, 'messages': [doc('tools', ['openai_connection'])]})
        conns = {k: c['kind'] for k, c in y['context']['connections'].items()}
        nodes = [k for k, _ in agent_blocks(flow[1]) if re.match(r'^(generator|subagent|router|orchestrator|executor|echo) ', k)]
        trig = re.search(r'^trigger (\w+):', flow[1], re.M).group(1)
        start = starter_flow(bk, bname).replace('subagent assistant:', 'REMOVED').split('REMOVED')[0].replace('    transition to @subagent.assistant\n', '').replace('  on_message: ->\n', '') + 'echo done:\n  kind: "a2a:status_update_event"\n  state: "TASK_STATE_COMPLETED"\n  message: a2a.message({messageId: uuid(), parts: [a2a.textPart("Done")]})\n'
        adoc = lambda text: {'type': 'doc', 'kind': 'agent', 'fileName': flow[0].split('/')[-1], 'uri': f'file:///demo/{project_name(t)}/{flow[0]}', 'text': text, 'guidesSeen': ['v1', 'v2', 'agent'], 'agent': {'brokerKey': bk, 'connections': conns}}
        sp.append({'name': 'scratch-flow-add', 'view': 'agent', 'size': S, 'messages': [adoc(start), sel(f'trigger-{trig}')],
                   'after': "setTimeout(()=>{const b=[...document.querySelectorAll('button')].find(x=>x.textContent.trim()==='Add node'); const r=b.getBoundingClientRect(); b.dispatchEvent(new MouseEvent('click',{bubbles:true,clientX:r.x+10,clientY:r.y+10})); setTimeout(()=>{[...document.querySelectorAll('.submenu .menu-item')].find(x=>x.querySelector('.mi-label')?.textContent==='Generator')?.click();},80);},250)"})
        pick = next((k for k in nodes if k.startswith('router ')), nodes[0])
        sp.append({'name': 'scratch-flow', 'view': 'agent', 'size': S, 'messages': [adoc(flow[1]), sel(pick.replace(' ', '-'))]})
    has_pol = bool((b.get('spec') or {}).get('policies')) if v == 'v1' else bool(b['interfaces']['a2a'].get('policies'))
    if has_pol:
        sp.append({'name': 'scratch-policy', 'view': 'network', 'size': S, 'messages': [doc('final', [x for x in net_base.get('brokerTargets', {}).values()][0] if v == 'v2' else None), sel(f'broker-{bk}')],
                   'after': "setTimeout(()=>{const r=document.querySelector('.xb-root'); if(r) r.style.display='none'; document.querySelector('.inspector .pol-item .pol-fold')?.click(); setTimeout(()=>{document.querySelector('.inspector .pol-item')?.closest('.fsection')?.scrollIntoView({block:'start'});},100);},250)"})
    return sp
