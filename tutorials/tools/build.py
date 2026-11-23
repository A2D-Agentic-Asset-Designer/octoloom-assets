#!/usr/bin/env python3
"""Generate the Octoloom template tutorials (octoloom#253).

Usage: python3 tutorials/tools/build.py <path-to-octoloom-repo> [--no-shots] [ids...]
Reads media/templates (index.json, agent-network.yaml, exchange.json, README.md, brokers/*.agent)
and writes tutorials/<id>/README.md plus screenshots taken with the repo's headless harness
(.claude/skills/octoloom-screenshot/shot.mjs, needs `npm run build` first). Only template data,
no org data: URLs in screenshots are gateway.example.com.
"""
import json, os, re, subprocess, sys, shutil, tempfile
import yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scratch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)                      # tutorials/
ASSETS = 'https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials'
args = [a for a in sys.argv[1:] if not a.startswith('--')]
REPO = os.path.abspath(args[0]); ONLY = set(args[1:])
SHOTS = '--no-shots' not in sys.argv
T = os.path.join(REPO, 'media', 'templates')
INDEX = json.load(open(os.path.join(T, 'index.json')))['templates']
STYLE = {'v1': 'Probabilistic', 'v2': 'Deterministic'}
NODE = {'trigger': 'Trigger', 'generator': 'Generator (one LLM call with structured outputs)', 'subagent': 'Subagent (calls a tool or an agent and classifies the answer)',
        'router': 'Router (picks the next step from a condition)', 'orchestrator': 'Orchestrator (the LLM picks tools and agents in a loop)',
        'executor': 'Executor (runs a tool with fixed inputs, no LLM)', 'echo': 'Echo (the reply: completed, failed, rejected or input-required)'}

def variant(t):
    i = t['id']
    return 'governed' if i.endswith('-governed') else 'secured' if i.endswith('-secured') else 'idmc' if '-idmc-' in i else 'plain'

def base_id(t):
    return re.sub(r'-(governed|secured)$', '', t['id'])

def readme_parts(text):
    secs, cur = {}, '_head'
    for line in text.splitlines():
        m = re.match(r'^## (.+)', line)
        if m: cur = m.group(1).strip(); secs[cur] = []; continue
        secs.setdefault(cur, []).append(line)
    return {k: '\n'.join(v).strip() for k, v in secs.items()}

def try_prompts(section):
    out, cur = [], None
    for line in section.splitlines():
        m = re.match(r'^- \*\*(.+?)\*\*\s*$', line)
        if m: cur = {'prompt': m.group(1).strip(), 'see': ''}; out.append(cur); continue
        m = re.match(r'^\s+- You should see:\s*(.+)', line)
        if m and cur: cur['see'] = m.group(1).strip()
    return out

def clean(s):
    # Tutorials name the reply icon by what it opens: the Agent Network Tracer.
    return re.sub(r'\*\*[A-Z]{3}\*\* icon', '**Tracer** icon', s)

def secrets(ex):
    out, plain = [], []
    for g, x in (ex.get('metadata', {}).get('variables') or {}).items():
        if not isinstance(x, dict): continue
        items = x.items() if not ('default' in x or 'secret' in x) else [(None, x)]
        for n, d in items:
            if not isinstance(d, dict): continue
            k = f'{g}.{n}' if n else g
            (out if d.get('secret') else plain).append((k, d.get('description', ''), d.get('default', '')))
    return out, plain

def model(t):
    d = os.path.join(T, t['id'])
    y = yaml.safe_load(open(os.path.join(d, 'agent-network.yaml')))
    ex = json.load(open(os.path.join(d, 'exchange.json')))
    m = {'yaml': y, 'ex': ex, 'readme': open(os.path.join(d, 'README.md')).read(), 'dir': d}
    if t['version'] == 'v1':
        m['brokers'] = [(k, b.get('card', {}).get('name', k), b) for k, b in (y.get('brokers') or {}).items()]
        m['agents'] = [(k, a.get('card', {}).get('name', k), a.get('card', {}).get('description', '')) for k, a in (y.get('agents') or {}).items()]
        m['mcps'] = [(k, s.get('label', k), s.get('description', ''), [x['name'] for x in s.get('metadata', {}).get('tools', [])]) for k, s in (y.get('mcpServers') or {}).items()]
    else:
        r = y.get('registry') or {}
        m['brokers'] = [(k, b.get('interfaces', {}).get('a2a', {}).get('card', {}).get('name', k), b) for k, b in (y.get('brokers') or {}).items()]
        m['agents'] = [(k, a.get('info', {}).get('label', k), a.get('info', {}).get('description', '')) for k, a in (r.get('agents') or {}).items()]
        m['mcps'] = [(k, s.get('info', {}).get('label', k), s.get('info', {}).get('description', ''), [x.get('name') for x in (s.get('metadata', {}).get('tools') or s.get('metadata', {}).get('interfaces', {}).get('mcp', {}).get('tools') or [])]) for k, s in (r.get('mcps') or r.get('mcpServers') or {}).items()]
        flows = {}
        for k, b in (y.get('brokers') or {}).items():
            f = (b.get('implementation') or '').lstrip('./')
            if f and os.path.exists(os.path.join(d, f)): flows[k] = (f, open(os.path.join(d, f)).read())
        m['flows'] = flows
    return m

def flow_nodes(text):
    out = []
    lines = text.splitlines()
    for i, l in enumerate(lines):
        mm = re.match(r'^(trigger|generator|subagent|router|orchestrator|executor|echo) (\w+):', l)
        if not mm: continue
        desc = ''
        for j in range(i + 1, min(i + 8, len(lines))):
            dm = re.match(r'^\s+(description|label):\s*"?(.+?)"?\s*$', lines[j])
            if dm and dm.group(1) == 'description': desc = dm.group(2); break
            if re.match(r'^\S', lines[j]): break
        out.append((mm.group(1), mm.group(2), desc))
    return out

def policies_of(text):
    return sorted(set(re.findall(r'name:\s*([a-z0-9][a-z0-9_-]*(?:pii|limit|validation|injection|decorator|guard|filter|sanitiz|enforcement|auth|jwt|spike|token|policy)[a-z0-9_-]*)', text)))

def targets(text):
    return sorted(set(re.findall(r'"(?:llm|a2a|mcp)://([\w.-]+)"', text)))

# ---------- screenshots ----------
def progress_texts(agent_text):
    """The working-update sentences (#302) along ONE run of a v2 flow: from the trigger, follow the transitions,
    and at a router take its first route (the happy path the first Try it prompt takes)."""
    blocks, cur = {}, None
    for line in agent_text.splitlines():
        h = re.match(r'^(\w+) (\w+):\s*$', line)
        if h: cur = f'{h.group(1)}.{h.group(2)}'; blocks[cur] = []; continue
        if cur and (line.startswith(' ') or not line.strip()): blocks[cur].append(line)
        elif line.strip(): cur = None
    def nxt(body):
        t = '\n'.join(body)
        m = re.search(r'target:\s*@(\w+\.\w+)', t) or re.search(r'transition to @(\w+\.\w+)', t)
        return m.group(1) if m else None
    node = next((k for k in blocks if k.startswith('trigger.')), None)
    out, seen = [], set()
    while node and node in blocks and node not in seen:
        seen.add(node)
        if node.startswith('echo.progress'):
            m = re.search(r'textPart\("([^"]+)"', '\n'.join(blocks[node]))
            if m: out.append(m.group(1))
        node = nxt(blocks[node])
    return out

def specs(t, m):
    tid, v = t['id'], t['version']
    rel = f'media/templates/{tid}'
    sp = []
    ver = t['version']
    sp.append({'name': 'new-project', 'view': 'newProject', 'size': '1300,1000', 'messages': [
        {'type': 'newProjectInit', 'version': ver, 'templates': '@json:media/templates/index.json#templates', 'source': 'bundled', 'folder': '/Users/demo/projects'},
        {'type': 'newProjectReadme', 'id': tid, 'text': clean(m['readme'])}],
        'after': f"[...document.querySelectorAll('.np-tab')].find(b => b.textContent.startsWith('{'Technical' if t['category']=='technical' else 'Use cases'}'))?.click(); setTimeout(() => {{ const c=[...document.querySelectorAll('.np-card2')]; const want={json.dumps(t['title'].replace(': governed',''))}; const pick=c.filter(b => b.querySelector('.np-ct')?.textContent===want); (pick[{1 if variant(t)=='governed' else 0}]||pick[0])?.click(); const el=pick[0]; let sc=el?.parentElement; while (sc && !(sc.scrollHeight>sc.clientHeight+4 && /auto|scroll/.test(getComputedStyle(sc).overflowY))) sc=sc.parentElement; if (el && sc) sc.scrollTop += el.getBoundingClientRect().top - sc.getBoundingClientRect().top - sc.clientHeight/3; document.scrollingElement.scrollTop=0; window.scrollTo(0,0); }}, 60)"})
    net = {'version': v}
    if v == 'v2':
        net['brokerFiles'] = {k: f for k, (f, _) in m['flows'].items()}
        net['brokerTargets'] = {k: targets(x) for k, (_, x) in m['flows'].items()}
        deps = {}
        for dd in m['ex'].get('dependencies') or []:
            if re.match(r'^(agent|mcp|llm)-metadata$', dd.get('classifier', '')): deps[dd['assetId']] = {'groupId': dd['groupId'], 'version': dd['version'], 'classifier': dd['classifier']}
        net['dependencies'] = deps
    sp.append({'name': 'canvas', 'view': 'network', 'size': '1500,900', 'messages': [
        {'type': 'doc', 'kind': 'network', 'fileName': 'agent-network.yaml', 'uri': f'file:///demo/{tid}/agent-network.yaml', 'text': f'@file:{rel}/agent-network.yaml', 'guidesSeen': ['v1', 'v2', 'agent'], 'network': net}]})
    if v == 'v2':
        for k, (f, x) in list(m['flows'].items())[:1]:
            conns = {c: ('llm' if 'openai' in c or 'llm' in c else 'mcp' if 'mcp' in c else 'a2a') for c in targets(x)}
            sp.append({'name': 'flow', 'view': 'agent', 'size': '1500,900', 'messages': [
                {'type': 'doc', 'kind': 'agent', 'fileName': os.path.basename(f), 'uri': f'file:///demo/{tid}/{f}', 'text': f'@file:{rel}/{f}', 'guidesSeen': ['v1', 'v2', 'agent'], 'agent': {'brokerKey': k, 'connections': conns}}]})
    tp = try_prompts(readme_parts(m['readme']).get('Try it', ''))
    if tp and m['brokers']:
        bk, bn, _ = m['brokers'][0]
        url = f'https://gateway.example.com/{bk}/'
        reply = tp[0]['see']
        uses = {bk: net.get('brokerTargets', {}).get(bk, [])}
        # #302: v2 flows send working updates before each step; with Live on the reply keeps them above the answer
        prog = progress_texts(m['flows'][bk][1]) if v == 'v2' and bk in m.get('flows', {}) else []
        steps = ([{'at': 1794500000600, 'state': 'submitted'}] + [{'at': 1794500001000 + i * 1200, 'state': 'working', 'text': x} for i, x in enumerate(prog)]) if prog else None
        st = {'chat:broker': bk, 'chat:target': 'deployed', 'chat:left': 'network', **({'chat:stream': True} if prog else {}), 'chat:convs': {bk: {'turns': [
            {'id': 1, 'role': 'user', 'text': tp[0]['prompt'], 'at': 1794500000000},
            {'id': 2, 'role': 'agent', 'text': reply, 'at': 1794500006000, **({'steps': steps} if steps else {}), 'reply': {'ok': True, 'text': '', 'state': 'completed', 'httpStatus': 200, 'ms': 6100, 'taskId': '7f3a9c1e-5b2d-4e8f-9a01-c2d3e4f5a6b7', 'contextId': 'c1'}}]}}}
        sp.append({'name': 'chat', 'view': 'chat', 'size': '1500,900', 'state': st, 'messages': [
            {'type': 'chatInit', 'dir': f'/tmp/{tid}', 'project': tid, 'version': v, 'network': f'@file:{rel}/agent-network.yaml',
             'brokers': [{'key': bk, 'name': bn, 'url': url, 'protocol': '1.0' if v == 'v2' else '0.3.0', 'skills': []}],
             'deployment': {'env': 'Sandbox', 'gateway': 'example-gateway', 'status': 'running', 'brokers': [{'key': bk, 'url': url, 'protocol': '1.0' if v == 'v2' else '0.3.0', 'ok': True, 'http': 200}]},
             'uses': uses, 'networkCtx': net}]})
    return sp

def shoot(tid, sp, theme):
    tmp = tempfile.mkdtemp(prefix='octo-tut-')
    img = os.path.join(OUT, tid, 'img'); os.makedirs(img, exist_ok=True)
    files = []
    for s in sp:
        s = dict(s, themes=[theme])
        p = os.path.join(tmp, s['name'] + '.json'); json.dump(s, open(p, 'w')); files.append(p)
    subprocess.run(['node', os.path.join(REPO, '.claude/skills/octoloom-screenshot/shot.mjs'), *files], cwd=REPO, env=dict(os.environ, OUT=tmp), check=True, stdout=subprocess.DEVNULL)
    for s in sp:
        dst = os.path.join(img, s['name'] + '.png')
        shutil.copy(os.path.join(tmp, s['name'] + '.png'), dst)
        subprocess.run(['sips', '-Z', '1600', dst], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.rmtree(tmp)

# ---------- markdown ----------
def img(tid, name, alt):
    return f'![{alt}]({ASSETS}/{tid}/img/{name}.png)'

def tutorial(t, m, nxt, prev):
    tid, v = t['id'], t['version']
    rp = readme_parts(m['readme'])
    tp = try_prompts(rp.get('Try it', ''))
    sec, plain = secrets(m['ex'])
    var = variant(t)
    text = open(os.path.join(m['dir'], 'agent-network.yaml')).read()
    L = []
    L += [f"# Tutorial: {t['title']}", '',
          f"[All tutorials](../README.md) · [Getting started](../getting-started.md) · {STYLE[v]} network ({'Agent Network 2.0, AgentScript' if v=='v2' else 'Agent Network 1.0, LLM broker'}) · {'Use case' if t['category']=='usecase' else 'Technical'}{' · fully mocked' if t.get('mocked') else ''}{'' if var=='plain' else ' · ' + var.upper() if var=='idmc' else ' · ' + var}", '',
          f"> {t['summary']}", '',
          f"| Agents | MCP servers | A2A | Policies | Template id |", '|---|---|---|---|---|',
          f"| {t['agents']} | {t['mcps']} | {', '.join(t['protocols'])} | {len(t['policies'])} | `{tid}` |", '',
          'There are three ways to use this template:', '',
          '1. **[Just use it](#path-1-just-use-it)**: create the project, deploy it and chat with it in about 10 minutes.',
          '2. **[Learn step by step](#path-2-learn-step-by-step)**: the same steps, with what each part of the network does and how Octoloom shows it.',
          '3. **[Build it from scratch](#path-3-build-it-from-scratch)**: start from a blank project and build the same network yourself, no code, one screenshot per step.', '',
          '## Before you start', '',
          '- VS Code with **Octoloom for Agent Fabric** installed (Marketplace), version ' + ('0.9.27' if t.get('mocked') else '0.9.25') + ' or later.',
          '- An Anypoint organization with Agent Fabric, a connected app (client ID and secret), an environment and a Flex gateway.',
          ('- No OpenAI key: the LLM is an A²D LLM mock as well (`a2dLlm.url`), with scripted answers for the Try it prompts.' if t.get('mocked') else '- An OpenAI API key (or an OpenAI-compatible LLM gateway).'),
          ]
    if var == 'idmc':
        L.append('- An Informatica IDMC org with the four shared MCP services and an IDMC MCP client (see the template README, *IDMC setup*).')
    L += ['- Nothing else: ' + (('all agents, MCP servers and the LLM are public A²D mocks, so the network runs without any other system or key.' if t.get('mocked') else 'all agents and MCP servers are public A²D mocks, so the network runs without any other system.') if var != 'idmc' else 'the IDMC MCP servers are called with OAuth 2.0 client credentials.'), '',
          '## Path 1: Just use it', '',
          '1. **Home → Start → New ' + STYLE[v] + ' Network.** In the dialog pick **' + ('Technical' if t['category']=='technical' else 'Use cases') + '**, then the card **' + t['title'].replace(': governed','') + '**' + (' (the one with the policies chip)' if var=='governed' else '') + '. Choose a folder and click **Create**.',
          '2. **Deploy.** ' + clean(re.sub(r'^\d\. ', '', next((l for l in rp.get('Deploy in 3 steps', '').splitlines() if l.startswith('2.')), 'In Projects & Deploy, click Deploy.'))).strip()]
    for k, desc, _ in sec: L.append(f'   - `{k}`: {desc}')
    L += ['3. **Chat.** When the status light is green, click **Open chat** and paste:']
    for p in tp: L.append(f"   - `{p['prompt']}`")
    L += ['', 'Done. The rest of this page explains what you just ran.', '',
          '## Path 2: Learn step by step', '',
          '### Step 1. Connect Octoloom', '',
          'Open **Setup & Connect** (Octoloom side bar) and connect **Agent Fabric**: the connected app client ID and secret and the organization. Pick the environment. ' + ('A²D isn\'t needed: the mock URLs are already the defaults in `exchange.json`.' if var != 'idmc' else 'Also connect **IDMC** (Headless IDMC) if you want the IDMC palette tab.') + ' The Tooling list shows Node.js, Java and anypoint-cli-v4 with its agent-network plugin. Use **Install** or **Repair** on any red row.', '',
          '### Step 2. Create the project from the template', '',
          f"On **Home**, click **New {STYLE[v]} Network**. In **2 Start from**, choose **{'Technical' if t['category']=='technical' else 'Use cases'}** and click **{t['title'].replace(': governed','')}**. The right side shows the template README: what it contains, **Deploy in 3 steps** and **Try it**. Keep the suggested name `{t['assetId'].replace('-v1','').replace('-v2','')}` or type your own, pick the folder and click **Create**.", '',
          img(tid, 'new-project', f"New Project dialog with {t['title']} selected"), '',
          f"Octoloom writes `agent-network.yaml`, `exchange.json`, `README.md`{' and the broker flow in `brokers/`' if v=='v2' else ''}, and opens the canvas. Every id gets the template prefix `{t['prefix']}_`, so several templates can be deployed into one org side by side.", '',
          '### Step 3. Read the network on the canvas', '',
          img(tid, 'canvas', f"{t['title']} on the {STYLE[v]} network canvas"), '',
          'Each card is a part of `agent-network.yaml`. Click one to open it in the inspector on the right. Each change in the inspector is a change to the text, so the YAML stays the source of truth (**Code** view shows it).', '']
    for bk, bn, b in m['brokers']:
        L.append(f'- **Broker {bn}** (`{bk}`): ' + ('the LLM decides which agent or tool to call from its instructions.' if v=='v1' else 'its AgentScript flow decides every step.'))
        if v == 'v1':
            ins = (b.get('spec') or {}).get('instructions') or []
            if ins:
                L.append('  - Instructions:')
                for x in ins: L.append(f'    - {x}')
    for k, n, d in m['agents']: L.append(f'- **Agent {n}**: {d}')
    for k, n, d, tools in m['mcps']: L.append(f'- **MCP server {n}**: {d}' + (f" Tools: {', '.join('`'+x+'`' for x in tools if x)}." if tools else ''))
    L += ['', 'Try this on the canvas: use the zoom bar and the minimap, drag a card, or **Auto layout**. The layout is saved per file. **Minimize all** turns the cards into icon tiles. Click a connection line to see which broker uses which agent or tool.', '']
    n = 4
    if v == 'v2' and m['flows']:
        k, (f, x) = next(iter(m['flows'].items()))
        L += [f'### Step {n}. Follow the broker flow (AgentScript)', '',
              f"Double-click the broker card (or open `{f}`). The flow editor shows the AgentScript program that decides every step. The LLM only extracts fields and writes text, so the same input always takes the same branch.", '',
              img(tid, 'flow', f'{t["title"]} broker flow'), '', '| Step | Kind | What it does |', '|---|---|---|']
        for kind, name, desc in flow_nodes(x):
            d = desc or {'trigger': 'Starts the flow when an A2A message arrives at the broker.', 'echo': f'Ends the flow with the `{name}` reply.'}.get(kind) or NODE.get(kind, kind)
            if kind == 'echo' and name.startswith('progress') and not desc:
                d = 'Progress update (`TASK_STATE_WORKING`): tells the caller what comes next, then goes on to that step. With **Live** on, the chat shows it while the broker works.'
            L.append(f'| `{name}` | {NODE.get(kind, kind).split(" (")[0]} | {d} |')
        L += ['', 'Click a step to edit it in the inspector. **+ Step** adds a node, and **+ Step → Patterns** inserts whole shapes such as retry, human in the loop or a guardrail check. **Code** shows the `.agent` text with completion.', '']
        n += 1
    if t['policies'] or var == 'secured':
        L += [f'### Step {n}. See the {"policies" if var != "secured" else "secured connections"}', '']
        if t['policies']:
            L.append('This variant adds Agent Fabric policies. Open a broker or connection and look at its **Policies** section. Each policy folds open to show its configuration:')
            for p in t['policies']: L.append(f'- `{p}`')
            L.append('')
        if var == 'secured':
            sl = next((l for l in rp.get('_head', '').splitlines() if l.startswith('- Secured:')), '')
            L += [clean(sl[2:]) if sl else 'Every agent and MCP connection authenticates.', '',
                  'Open a connection card. Its **Authentication** section shows the kind (Basic, Client ID enforcement and so on). Names and client IDs are normal variables; passwords and secrets are **secret variables** that Octoloom asks for at deploy time and never stores.', '']
        L += ['Run **Governance** (shield icon in the canvas toolbar) to check the project against the Agent Fabric rulesets. It runs locally, and findings show on the cards with **Fix** where one exists.', '']
        n += 1
    L += [f'### Step {n}. Validate and build', '',
          'In the canvas toolbar, open the CLI menu: **Validate** does a dry run of build, publish and deploy and lists problems in the Problems panel (click one to jump to the card). **Build** repairs and packages the project locally with anypoint-cli-v4.', '']
    if plain:
        L += ['The variables of this template (in `exchange.json`, open it for the no-code form):', '', '| Variable | What | Default |', '|---|---|---|']
        for k, d, df in plain: L.append(f'| `{k}` | {d} | {"`"+str(df)+"`" if df else "(fill in)" if "ingressgw" in k else "—"} |')
        L.append('')
    n += 1
    L += [f'### Step {n}. Deploy', '',
          'Open **Projects & Deploy** and click **Deploy** on the project (or **Deploy…** on the canvas). Pick your gateway (the chips show its status and space), keep **Tracing**, **Wait until the network is ready** and **Publish before deploy** on, then enter the secrets. Nothing you type is stored:', '']
    for k, desc, _ in sec: L.append(f'- `{k}`: {desc}')
    if v == 'v1': L += ['', 'For a probabilistic network, also fill `ingressgw.url` in `exchange.json` (your ingress gateway base URL) before you deploy.']
    L += ['', 'The square status light goes from blue (deploying) to green (**Deployed and running**). The deployment box lists every broker URL; click one to copy it.', '']
    n += 1
    L += [f'### Step {n}. Chat with the broker', '',
          'Click **Open chat** on the deployment box. On the left is the network (the cards light up as they are called), and on the right is the conversation with its task states.' + (' **Live progress** (the antenna button next to Send) is on by default: while the broker works, the chat lists its progress updates (*' + '*, *'.join(progress_texts(next(iter(m['flows'].values()))[1])[:2]) + '*) and keeps them above the answer.' if v == 'v2' and m.get('flows') and progress_texts(next(iter(m['flows'].values()))[1]) else '') + ' Paste the prompts one at a time:', '',
          img(tid, 'chat', f'{t["title"]} in the broker chat'), '', ('*The LLM is a scripted A²D LLM mock, so the broker gives the same answer every time; the ids in the table are checked by a live deploy.*' if t.get('mocked') else '*The reply in the screenshot is an illustration: it shows what the broker answers. The real wording changes from run to run.*'), '', '| Prompt | You should see |', '|---|---|']
    for p in tp: L.append(f"| `{p['prompt']}` | {p['see'].replace('|', '/')} |")
    L += ['', clean(next((l for l in reversed(m['readme'].splitlines()) if l.startswith('The broker is')), '')), '']
    n += 1
    L += [f'### Step {n}. Trace a reply', '',
          'Under each reply, the **Tracer** icon opens the task in the **Agent Network Tracer**: a waterfall of every call the broker made (gateway, broker, LLM, A2A agents, MCP tools) on one time axis, coloured like the cards. Errors are red. Click a span to see its request and response. The **Network** view shows the same reply as a sequence of calls.', '']
    n += 1
    L += [f'### Step {n}. Share it (optional)', '',
          'The **Share** icon in the chat header opens the Share dialog. **A²D sessions** invites people by email to chat with this deployed broker and brings their passed / failed marks and comments back. **Local portal** generates a small web chat you can run or host anywhere.', '',
          *scratch.path3(t, m, lambda name, alt: img(tid, name, alt)),
          '## What you learned', '',
          f"- How a {STYLE[v].lower()} network is built: " + ('an LLM broker with instructions picks agents and MCP tools.' if v=='v1' else 'an AgentScript flow decides every step; the LLM extracts and writes text.'),
          '- How the canvas, the inspector and the code view edit the same YAML.',
          '- How to build the same network from a blank project with forms and menus only (Path 3).',
          *(['- How policies are attached and checked with Governance.'] if t['policies'] else []),
          *(['- How authenticated connections use variables and secret variables.'] if var=='secured' else []),
          '- How to validate, build, deploy, chat and trace with Octoloom.', '',
          '## Next', '']
    if prev: L.append(f"- Previous: [{prev['title']}](../{prev['id']}/README.md)")
    if nxt: L.append(f"- Next: [{nxt['title']}](../{nxt['id']}/README.md)")
    rel = [x for x in INDEX if base_id(x) == base_id(t) and x['id'] != tid]
    for x in rel: L.append(f"- Same use case, {variant(x) if variant(x)!='plain' else 'plain'} variant: [{x['title']}](../{x['id']}/README.md)")
    L += ['- [All tutorials](../README.md)', '', '---', f'Generated from the `{tid}` template (Octoloom `media/templates/{tid}`). Screenshots use fake data.', '']
    return '\n'.join(L)

ORDER_KEY = lambda t: ({'usecase': 0, 'technical': 1}[t['category']], 1 if t.get('mocked') else 0, {'plain': 0, 'governed': 1, 'secured': 2, 'idmc': 3}[variant(t)], t['title'])

def index_md():
    L = ['# Octoloom tutorials', '',
         'One tutorial for every template project in Octoloom for Agent Fabric. Each one gives you three paths:', '',
         '1. **Just use it**: import the template from **New Project**, deploy it and chat with it.',
         '2. **Learn step by step**: the same project, explained part by part (canvas, AgentScript flow, policies, deploy, chat, Tracer), with screenshots.',
         '3. **Build it from scratch**: start from a blank project and build the same network with forms, menus and buttons only (no code), one screenshot per step.', '',
         'New to Octoloom? Start with **[Getting started](getting-started.md)**, then pick a template. A good learning order is the smallest ones first: *Retail Returns* (deterministic) and *Customer Service* (probabilistic), then their governed and secured variants. No OpenAI key yet? The **Fully mocked** ones (*Hotel Concierge*, *Event Ticketing* and four more) use an A²D LLM mock, so you can deploy and chat with only an Anypoint org.', '']
    for v in ('v1', 'v2'):
        L += [f"## {STYLE[v]} networks ({'Agent Network 1.0' if v=='v1' else 'Agent Network 2.0, AgentScript'})", '',
              'An LLM broker reads its instructions and picks agents and MCP tools.' if v=='v1' else 'AgentScript flows decide every step: routers, gates, executors.', '',
              '| Tutorial | Kind | Agents | MCP | Policies |', '|---|---|---|---|---|']
        for t in sorted([x for x in INDEX if x['version'] == v], key=ORDER_KEY):
            k = 'Fully mocked' if t.get('mocked') else {'plain': 'Use case' if t['category']=='usecase' else 'Technical', 'governed': 'Governed', 'secured': 'Secured', 'idmc': 'IDMC'}[variant(t)]
            L.append(f"| [{t['title']}]({t['id']}/README.md) | {k} | {t['agents']} | {t['mcps']} | {len(t['policies'])} |")
        L.append('')
    L += ['---', 'The tutorials are generated from the bundled templates with `tutorials/tools/build.py` and updated when the templates change. Screenshots use fake data.', '']
    return '\n'.join(L)

def main():
    order = {v: sorted([x for x in INDEX if x['version'] == v], key=ORDER_KEY) for v in ('v1', 'v2')}
    for v, lst in order.items():
        for i, t in enumerate(lst):
            if ONLY and t['id'] not in ONLY: continue
            m = model(t)
            os.makedirs(os.path.join(OUT, t['id']), exist_ok=True)
            open(os.path.join(OUT, t['id'], 'README.md'), 'w').write(tutorial(t, m, lst[i + 1] if i + 1 < len(lst) else None, lst[i - 1] if i else None))
            if SHOTS: shoot(t['id'], specs(t, m) + scratch.specs3(t, m, specs(t, m)[1]['messages'][0]['network']), 'dark' if i % 2 == 0 else 'light')
            print('ok', t['id'])
    if not ONLY: open(os.path.join(OUT, 'README.md'), 'w').write(index_md())

main()
