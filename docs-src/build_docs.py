import re
#!/usr/bin/env python3
"""Generate the Octoloom documentation site (octoloom#301) into docs/ and mkdocs.yml.

Usage: python3 docs-src/build_docs.py <path-to-octoloom-repo>

Sources (nothing is written by hand twice):
  - the Octoloom README (highlights, feature tour, getting started, reference sections)
  - src/model/guides.ts (EXPLAIN cards and the guided tours, the same texts as the in-app Explain button)
  - package.json (commands, settings, version)
  - templates/, tutorials/ and skills/ of this repo
The site is built and published by .github/workflows/docs.yml (MkDocs Material, GitHub Pages).
"""
import json, os, re, shutil, subprocess, sys, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ui_meta import SECTIONS, F, REF_SHOT, CARD_IMG, KEY_SHOT, SHOT_STEP, CARD_SHOT
import changelog_page
import usage_page

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOCS = os.path.join(ROOT, 'docs')
REPO = os.path.abspath(sys.argv[1])
RAW = 'https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main'
BLOB = 'https://github.com/A2D-Agentic-Asset-Designer/octoloom-assets/blob/main'
TREE = 'https://github.com/A2D-Agentic-Asset-Designer/octoloom-assets/tree/main'
SITE = 'https://a2d-agentic-asset-designer.github.io/octoloom-assets/'
MARKET = 'https://marketplace.visualstudio.com/items?itemName=octoloom.octoloom'

README = open(os.path.join(REPO, 'README.md')).read()
PKG = json.load(open(os.path.join(REPO, 'package.json')))
INDEX = json.load(open(os.path.join(REPO, 'media', 'templates', 'index.json')))['templates']
TUTS = os.path.join(ROOT, 'tutorials')
TPLS = os.path.join(ROOT, 'templates')
SKILLS = os.path.join(ROOT, 'skills')
UI = os.path.join(HERE, 'img', 'ui')
SHOTS = json.load(open(os.path.join(UI, 'index.json'))) if os.path.exists(os.path.join(UI, 'index.json')) else {}


def market_stats():
    """Install count etc. from the VS Code Marketplace (baked in; marketplace.js refreshes it live)."""
    try:
        req = urllib.request.Request('https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery',
            data=json.dumps({'filters': [{'criteria': [{'filterType': 7, 'value': 'octoloom.octoloom'}]}], 'flags': 914}).encode(),
            headers={'Content-Type': 'application/json', 'Accept': 'application/json;api-version=3.0-preview.1'})
        try:
            raw = urllib.request.urlopen(req, timeout=20).read()
        except Exception:  # local Python without CA certs: fall back to curl
            import subprocess
            raw = subprocess.run(['curl', '-s', '-X', 'POST', req.full_url, '-H', 'Content-Type: application/json',
                                  '-H', 'Accept: application/json;api-version=3.0-preview.1', '--data-binary', req.data.decode()],
                                 capture_output=True, check=True, timeout=30).stdout
        x = json.loads(raw)['results'][0]['extensions'][0]
        st = {t['statisticName']: t['value'] for t in x['statistics']}
        return {'installs': int(st.get('install', 0)), 'rating': st.get('averagerating', 0), 'ratings': int(st.get('ratingcount', 0)),
                'version': x['versions'][0]['version']}
    except Exception as e:
        print('marketplace stats unavailable:', e)
        return {'installs': 0, 'rating': 0, 'ratings': 0, 'version': PKG['version']}


MK = None
SHOT_CAP = {}
for _m in F.values():
    for _sh, _cap in _m.get('shots') or []: SHOT_CAP.setdefault(_sh, _cap)


def img(name, up, caption=None, theme_pair=True, cls=''):
    """A screenshot in light and dark (the one matching the site theme shows)."""
    alt = (caption or name).replace('"', "'")
    base = f'{up}assets/ui/{name}'
    c = f'{{ loading=lazy {cls}}}' if cls else '{ loading=lazy }'
    if theme_pair and os.path.exists(os.path.join(UI, f'{name}-dark.webp')):
        out = f'![{alt}]({base}-light.webp#only-light){c}\n![{alt}]({base}-dark.webp#only-dark){c}'
    else:
        out = f'![{alt}]({base}-light.webp){c}'
    if caption: out = f'<figure markdown>\n{out}\n<figcaption>{caption}</figcaption>\n</figure>'
    return out


CTL_DESC = {
    'Network': 'Open the Agent Network view of the deployed network', 'exchange.json': 'Open the Exchange asset form of this project',
    'Build & Deploy': 'Validate, build, publish and deploy this network', 'Save': 'Save the file (the YAML stays the source of truth)',
    'Collapse card': 'Collapse or expand the card body', 'Edit': 'Edit the linked agents or MCP servers of this broker',
    'Add to the network': 'Add a broker, agent, MCP server, LLM or policy', 'Auto layout': 'Arrange the cards automatically',
    'Zoom out': 'Zoom the canvas out', 'Zoom in': 'Zoom the canvas in', 'Fit to screen': 'Fit all cards into the view',
    'Hide the minimap': 'Show or hide the minimap', 'Overview': 'One row per agent network', 'Policies': 'Policy coverage per network',
    'Governance': 'Governance results per network', 'Authentication': 'Upstream authentication per connection',
    'Origins': 'Where the assets come from', 'Lifecycle': 'Validated, built, published, deployed', 'LLMs': 'LLM providers per network',
    'Code': 'YAML / AgentScript source view',
    'Use another URL': 'Chat with a broker at a different URL', 'Show raw JSON for every reply': 'Show the raw A2A JSON under each reply',
    'Running': 'Show only the running deployments', 'Not deployed': 'Show only the projects that are not deployed',
    'Copy URL': 'Copy the broker URL', 'Check status': 'Ask Agent Fabric for the deployment status',
    'Check deployment status': 'Ask Agent Fabric for the deployment status', 'Workspace report': 'Open the HTML report of all findings',
    'Unpublish from Exchange': 'Remove this version from Exchange', 'Undeploy': 'Stop the deployment (asks first)',
    'Show details': 'Show the full details', 'Setup gateways': 'Pick the Flex gateways to deploy to',
    'Setup & Connect': 'Connect Anypoint, A²D and IDMC', 'Reload the ruleset catalogs and projects': 'Read the rulesets and projects again',
    'Publish to Exchange': 'Publish the assets to Exchange', 'Projects & Deploy': 'The projects list with status lights',
    'Project': 'Project settings', 'Preview': 'Preview the result before you apply it', 'Open folder…': 'Open the project folder',
    'New Version': 'Bump the asset version', 'New project': 'Create a project from a template', 'JSON': 'Show the JSON source',
    'Hide the rulesets': 'Hide the rulesets column', 'Hide the findings': 'Hide the findings column', 'Hide explorer': 'Hide the flow explorer',
    'Governed services': 'The services the rulesets checked', 'Deploy': 'Deploy the network to Agent Fabric',
    'Configuration': 'Deployment settings: environment, gateway, variables', 'Canvas': 'Show the canvas', 'Cancel': 'Close without changes',
    'Add subagent': 'Add a subagent step to the flow', 'Add node': 'Add a step to the flow', 'Add a ruleset YAML file': 'Use a local ruleset file',
    'Unlock to edit': 'Unlock the generated file to edit it by hand', 'Select environment': 'Pick the Anypoint environment',
    'Revert': 'Undo the unsaved changes', 'Remove group': 'Remove this group', 'Re-check': 'Run the checks again',
    'Probabilistic': 'v1 networks: the LLM picks the next agent', 'Deterministic': 'v2 networks: an AgentScript flow decides',
    'Open in text editor': 'Open the file as text', 'Load the trace again': 'Reload the trace', 'Hide the tracer': 'Hide the tracer panel',
    'Form': 'Show the form view', 'Download and open': 'Download the asset and open it as a project',
    'Disconnect from Agent Fabric': 'Sign out of Anypoint', 'Disconnect from A²D': 'Remove the A²D API key',
    'Deployed': 'Show only deployed projects', 'Create from template': 'Create the project', 'Connect': 'Connect with these settings',
    'Cards': 'Show the results as cards', 'Rows': 'Show the results as rows', 'Browse…': 'Pick a folder', 'Back to the network': 'Return to the network canvas',
    'Any status': 'Filter by status', 'All': 'Show all', 'All styles': 'Show v1 and v2 networks', 'MCP': 'Show MCP servers', 'Visual': 'Visual canvas', 'Refresh': 'Read the data again', 'Send': 'Send the message to the broker',
}


def controls_table(shot, E_titles=None):
    ctl = SHOTS.get(shot, {}).get('controls') or []
    if not ctl: return ''
    rows = ['| # | Control | What it does |', '|---|---|---|']
    for c in ctl:
        t, txt = c['title'] or '', c['text'] or ''
        pre = t.split(':')[0].split('(')[0].strip() if ':' in t else ''
        name = pre if pre and len(pre) <= 40 else (txt if txt and len(txt) <= 32 else (t.split('(')[0].strip()[:40] or txt))
        name = re.sub(r'\d+\s*·\s*\d+\s*nets?$', '', name).strip()
        what = t if t and t != name else ''
        m = re.match(r'^(.*?[a-z…])([A-Z][a-z].*)$', name)
        if m and ' ' in name and not what: name, what = m.group(1), m.group(2)
        if not what: what = CTL_DESC.get(name, '')
        what = what.replace('|', '/').replace('\n', ' ')
        rows.append(f'| <span class="ol-n">{c["n"]}</span> | **{name.replace("|", "/")}** | {what} |')
    return '\n'.join(rows)


def indent(block, n=4):
    """A block inside a list item (so the screenshot belongs to that step)."""
    return '\n'.join((' ' * n + l) if l else l for l in block.split('\n'))


def annotated(shot, up, caption):
    if not SHOTS.get(shot, {}).get('controls'): return img(shot, up, caption)
    return img(f'{shot}-annot', up, caption) + '\n\n' + controls_table(shot)


def explain():
    out = '/tmp/octoloom-docs-guides.cjs'
    subprocess.run(['npx', 'esbuild', 'src/model/guides.ts', '--bundle', '--format=cjs', '--platform=node',
                    '--outfile=' + out, '--log-level=error'], cwd=REPO, check=True)
    js = subprocess.run(['node', '-e', f'const g=require({json.dumps(out)});process.stdout.write(JSON.stringify({{E:g.EXPLAIN,G:g.GUIDES}}))'],
                        check=True, capture_output=True, text=True).stdout
    return json.loads(js)


def clean(s):
    # The reply / project icon that opens the Agent Network Tracer is named by what it opens.
    s = re.sub(r'\*\*[A-Z]{3}\*\* (icon|button)', r'**Tracer** \1', s)
    s = re.sub(r'\bThe \*\*[A-Z]{3}\*\* icon', 'The **Tracer** icon', s)
    s = re.sub(r'\b' + 'A' + 'NT' + r' (icon|button)\b', r'Tracer \1', s)
    return s


def write(rel, text):
    p = os.path.join(DOCS, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w').write(clean(text).rstrip() + '\n')


def sections(text, level):
    """Split markdown by headings of one level: [(title, body)]."""
    out, cur, buf = [], None, []
    h = '#' * level + ' '
    for line in text.splitlines():
        if line.startswith(h) and not line.startswith(h + '#'):
            if cur is not None: out.append((cur, '\n'.join(buf).strip()))
            cur, buf = line[len(h):].strip(), []
        elif cur is not None:
            buf.append(line)
    if cur is not None: out.append((cur, '\n'.join(buf).strip()))
    return out


def readme_section(title):
    for t, b in sections(README, 2):
        if re.sub(r'<[^>]+>', '', t).strip() == title: return b
    raise SystemExit(f'README section missing: {title}')


def slug(t):
    t = re.sub(r'`|\(|\)|:|&|²', lambda m: '2' if m.group(0) == '²' else '', t.lower())
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')


def site_links(md, here):
    """Point links into this repo at the site pages. `here` is the page folder relative to docs/."""
    up = '../' * here.count('/') if here else ''
    def rep(m):
        url = m.group(1)
        mm = re.match(re.escape(BLOB) + r'/tutorials/(README\.md|getting-started\.md|([\w-]+)/README\.md)$', url)
        if mm:
            if mm.group(1) == 'README.md': return f']({up}tutorials/index.md)'
            if mm.group(1) == 'getting-started.md': return f']({up}getting-started.md)'
            return f']({up}tutorials/{mm.group(2)}.md)'
        return m.group(0)
    md = re.sub(r'\]\(https://octoloom\.a2d-ai\.com/start/(?:([\w-]+)/)?\)', lambda m: f']({up}start/{m.group(1) or "index"}.md)', md)
    return re.sub(r'\]\((https://github\.com/[^)\s]+)\)', rep, md)


# ---------------------------------------------------------------- pages

FEATURE_EXPLAIN = {
    'welcome-page': ['welcome', 'welcomeTutorials', 'octoloomVersion'],
    'coverage-map': ['coverage', 'coverageKpis', 'coverageOrigins', 'coverageTable', 'coverageDetail'],
    'new-project-from-templates': ['newProject'],
    'agent-network-from-exchange': ['exchangeImport'],
    'network-canvas-agent-network-yaml': ['networkCanvas', 'broker', 'agent', 'mcp', 'llm', 'connection', 'inspector', 'canvasTools', 'problems'],
    'broker-llm-provider': ['llm'],
    'llm-authentication-api-key-or-oauth-2-0-jwt': ['llm', 'connection'],
    'policies-and-p4a': ['policy'],
    'broker-flow-editor-brokers-agent': ['flowCanvas', 'trigger', 'generator', 'router', 'subagent', 'orchestrator', 'executor', 'echo', 'flowOutline', 'patterns'],
    'code-view-yaml-agentscript-json': ['codeView', 'tbVisualCode'],
    'asset-editor-exchange-json': ['exchangeEditor', 'tbExchangeJson'],
    'asset-palette-agent-fabric-and-a2d': ['palette', 'llmFromExchange'],
    'projects-deploy': ['projects', 'pjBuild', 'pjPublish', 'pjRunLocal', 'pjSetupGateways', 'pjUndeploy', 'pjUnpublish', 'pjRemove', 'validate', 'preDeploy', 'deployForm'],
    'setup-connect': ['setupConnect'],
    'governance-rulesets-for-brokers-agents-and-mcp-servers': ['governance', 'ruleset', 'governanceReport'],
    'minimize-to-icons': ['minimize'],
    'explain-anything': ['explainAnything'],
    'broker-chat': ['chat', 'chatNetwork', 'chatTrace', 'chatAuth', 'chatPortal', 'errorDetail'],
    'agent-network-tracer': ['tracer'],
}

GROUPS = [
    ('flow-nodes', 'Broker flow nodes', 'The steps of an AgentScript flow (`brokers/*.agent`), as cards on the broker canvas.',
     ['trigger', 'generator', 'router', 'subagent', 'orchestrator', 'executor', 'echo']),
    ('network-components', 'Network components', 'The cards of the network canvas (`agent-network.yaml`).',
     ['broker', 'agent', 'mcp', 'llm', 'connection', 'policy']),
    ('canvases-editors', 'Canvases and editors', 'The editors, the canvas tools and the panels around them.',
     ['networkCanvas', 'flowCanvas', 'inspector', 'canvasTools', 'flowOutline', 'problems', 'codeView', 'exchangeEditor', 'minimize', 'patterns', 'toolbar']),
    ('toolbar-buttons', 'Toolbar buttons', 'The buttons at the top of every Octoloom editor.',
     [k for k in ['tbVisualCode', 'tbExplorer', 'tbOpenNetwork', 'tbNetworkSettings', 'tbPreview', 'tbNewVersion', 'tbCommitVersion', 'tbBumpPatch', 'tbExchangeJson', 'tbBuildDeploy', 'tbSave']]),
    ('projects-deploy', 'Projects & Deploy buttons', 'The project card in the side bar: build, validate, publish, deploy, run locally.',
     ['projects', 'validate', 'pjBuild', 'pjPublish', 'pjRunLocal', 'pjSetupGateways', 'pjUndeploy', 'pjUnpublish', 'pjRemove', 'preDeploy', 'deployForm']),
    ('side-bar-home', 'Side bar, Home and New project', 'Setup & Connect, the Asset Palette, Home, the Coverage map and the New Project dialog.',
     ['setupConnect', 'palette', 'llmFromExchange', 'welcome', 'welcomeTutorials', 'octoloomVersion', 'coverage', 'coverageKpis', 'coverageOrigins', 'coverageTable', 'coverageDetail', 'newProject', 'exchangeImport']),
    ('chat-tracer', 'Chat, Share and Tracer', 'Talk to a deployed broker, share it and see what it did.',
     ['chat', 'chatNetwork', 'chatTrace', 'chatAuth', 'chatPortal', 'errorDetail', 'tracer']),
    ('governance', 'Governance', 'Local compliance checks with rulesets.', ['governance', 'ruleset', 'governanceReport']),
    ('help', 'Help', 'The floating Explain button and the guided tours.', ['explainAnything']),
]


def card(e, level='###', up='../', key=None, shot=False):
    out = [f'{level} {e["title"]}', '']
    pic = CARD_IMG.get(key) if key else None
    full = cap = None
    if shot and key and not pic:
        full = KEY_SHOT.get(key)
        if not full and key in CARD_SHOT: full, cap = CARD_SHOT[key]
    if pic and os.path.exists(os.path.join(UI, f'{pic}-light.webp')):
        out += ['<div class="grid" markdown>', '', img(pic, up, None), '', f'{e["what"]}\n\n**When to use it:** {e["when"]}', '', '</div>', '']
    else:
        out += [e['what'], '', f'**When to use it:** {e["when"]}', '']
        # A whole view is too wide to sit beside the text: it goes right under it (#349).
        if full and os.path.exists(os.path.join(UI, f'{full}-light.webp')):
            out += [img(full, up, cap or SHOT_CAP.get(full, e['title'])), '']
    if e.get('examples'):
        out += ['**Examples and details:**', ''] + [f'- {x}' for x in e['examples']] + ['']
    if e.get('snippet'):
        lang = 'yaml' if re.match(r'^\s*[\w-]+:\s', e['snippet']) and 'transition to' not in e['snippet'] and '->' not in e['snippet'] else 'text'
        out += ['??? note "In the file"', '', f'    ```{lang}'] + ['    ' + l for l in e['snippet'].splitlines()] + ['    ```', '']
    return '\n'.join(out)


def home(version):
    hl = readme_section('Highlights')
    rows = [l for l in hl.splitlines() if l.startswith('| **')]
    cards = []
    for r in rows:
        m = re.match(r'\| \*\*(.+?)\*\* \| (.+) \|$', r)
        if m: cards.append(f'-   **{m.group(1)}**\n\n    ---\n\n    {m.group(2)}')
    mk = MK
    n_v1 = sum(1 for t in INDEX if t['version'] == 'v1'); n_v2 = len(INDEX) - n_v1
    def tile(slug_, title, shot, text):
        return (f'-   **[{title}](features/{slug_}.md)**\n\n    ![{title}](assets/ui/{shot}-light.webp){{ loading=lazy }}\n\n    {text}\n')
    tour = [
        ('new-project-from-templates', 'Start from a template', 'new-project', f'{len(INDEX)} ready-to-run networks, every upstream mocked.'),
        ('network-canvas-agent-network-yaml', 'Design on the canvas', 'network-v2', 'Brokers, agents, MCP servers and LLMs as cards; the YAML stays in sync.'),
        ('broker-flow-editor-brokers-agent', 'Write broker flows', 'agent-flow', 'AgentScript flows: steps, branches, replies and live progress.'),
        ('governance-rulesets-for-brokers-agents-and-mcp-servers', 'Govern locally', 'governance', 'Rulesets from Agent Fabric, P4A and your org, with Fix all.'),
        ('projects-deploy', 'Build, publish, deploy', 'projects-deploy', 'Validate, build, publish to Exchange and deploy to your gateways.'),
        ('broker-chat', 'Chat and trace', 'chat-progress', 'Talk to the broker over A2A and see every call it made.'),
        ('agent-network-tracer', 'Agent Network Tracer', 'tracer', 'The path each task took through the flow, from the logs.'),
        ('coverage-map', 'Coverage map', 'coverage-map', 'Policy, auth and governance coverage of every network.'),
        ('setup-connect', 'Setup & Connect', 'setup-connect', 'Connections, CLI tools and theme in one place.'),
    ]
    return f'''---
hide:
  - navigation
  - toc
---

<div class="hero" markdown>

![Loomi, the Octoloom octopus](assets/loomi.png){{ .hero-logo }}

<span class="ol-pill">VS Code extension for Agent Fabric</span>

# Octoloom for Agent Fabric

<p class="lede"><strong>Design, govern, deploy and observe agent networks, visually, in VS Code.</strong>
Octoloom turns <code>agent-network.yaml</code> and AgentScript <code>.agent</code> flows into canvases, checks them with governance rulesets on your machine,
deploys them with the Anypoint CLI and lets you chat with the deployed broker and trace every call. Meet Loomi, the octopus who weaves your agents together.</p>

<div class="ol-stats">
<a class="ol-stat" href="{MARKET}"><b class="ol-installs" data-fallback="{mk['installs']:,}">{mk['installs']:,}</b><span>Marketplace installs</span></a>
<a class="ol-stat" href="{MARKET}&ssr=false#review-details"><b><span class="ol-rating">{mk['rating']:.1f}</span> ★</b><span><span class="ol-ratings">{mk['ratings']}</span> ratings</span></a>
<div class="ol-stat"><b class="ol-version">{mk['version']}</b><span>Latest version</span></div>
<a class="ol-stat" href="catalog/"><b>{len(INDEX)}</b><span>Templates ({n_v1} v1 · {n_v2} v2)</span></a>
<a class="ol-stat" href="tutorials/"><b>{len(INDEX)}</b><span>Tutorials</span></a>
</div>

[Install from the Marketplace]({MARKET}){{ .md-button .md-button--primary }}
[Getting started](getting-started.md){{ .md-button }}
[Features](features/index.md){{ .md-button }}
[Templates](catalog/index.md){{ .md-button }}

</div>

![The deterministic network canvas with the inspector](assets/ui/network-v2-light.webp#only-light)
![The deterministic network canvas with the inspector](assets/ui/network-v2-dark.webp#only-dark)

## Tour of Octoloom

<div class="grid cards" markdown>

{chr(10).join(tile(*t) for t in tour)}
</div>

## Where to start

<div class="grid cards" markdown>

-   :material-microsoft-visual-studio-code: **[Install from the VS Code Marketplace]({MARKET})**

    ---

    Search **Octoloom** in the Extensions view, or open the Marketplace page. Version {mk['version']}, {mk['installs']:,} installs.

-   :material-rocket-launch: **[Getting started](getting-started.md)**

    ---

    A 20-minute tour: install, connect, create a project from a template, deploy and chat.

-   :material-school: **[Tutorials](tutorials/index.md)**

    ---

    One per template, each with three paths: *Just use it*, *Learn step by step* and *Build it from scratch*.

-   :material-view-grid: **[Templates](catalog/index.md)**

    ---

    Ready-to-run agent networks: use cases, governed, secured, fully mocked and Informatica IDMC.

-   :material-gesture-tap-button: **[UI reference](reference/index.md)**

    ---

    Every button, card, canvas and panel on a screenshot, with what it does. The same texts as the in-app **Explain** button.

-   :material-robot: **[Skills for your AI assistant](skills/index.md)**

    ---

    Skills that teach Claude Code, Cursor and others to build agent networks the way the templates are built.

</div>

## Highlights

<div class="grid cards" markdown>

{chr(10).join(cards)}

</div>
'''


def features(E):
    tour = dict((slug(t), (t, b)) for t, b in sections(readme_section('Feature tour'), 3))
    nav = []
    idx = ['<span class="ol-pill">Using Octoloom</span>', '', '# Features', '',
           '<p class="lede"><strong>Every view of Octoloom, with screenshots.</strong> Each page says what the view is for, why you use it, '
           'where to find it and how to use it step by step. Every numbered control is explained under its screenshot.</p>', '']
    for sec, slugs in SECTIONS:
        idx += [f'## {sec}', '', '<div class="grid cards" markdown>', '']
        sub = []
        for s_ in slugs:
            if s_ not in tour: continue
            title, body = tour[s_]; m = F.get(s_, {})
            shots = m.get('shots') or []
            first = shots[0][0] if shots else None
            md = [f'<span class="ol-pill">{sec}</span>', '', f'# {m.get("nav") or title}', '']
            if m.get('what'): md += [f'<p class="lede"><strong>{m["what"]}</strong> {m.get("why", "")}</p>', '']
            if m.get('where'): md += [f'!!! info "Where to find it"', f'    {m["where"]}', '']
            if first: md += [annotated(first, '../', shots[0][1]) if SHOTS.get(first, {}).get('controls') else img(first, '../', shots[0][1]), '']
            # Every other screenshot sits next to the step it shows, never in a section of its own (#347).
            how = m.get('how') or []
            at = {}
            for sh, cap in shots[1:]:
                st = SHOT_STEP.get(sh, 0)
                at.setdefault(st if 0 <= st <= len(how) else 0, []).append((sh, cap))
            for sh, cap in at.get(0, []): md += [img(sh, '../', cap), '']
            if how:
                md += ['## How to use it', '']
                for i, x in enumerate(how, 1):
                    md += [f'{i}. {x}', '']
                    for sh, cap in at.get(i, []): md += [indent(img(sh, '../', cap)), '']
            md += ['## In detail', '', site_links(re.sub(r'!\[[^\]]*\]\([^)]*\)\s*', '', body), 'features/'), '']
            keys = FEATURE_EXPLAIN.get(s_, [])
            if keys:
                md += ['## Buttons and components', '', 'The same text as the in-app **Explain** button (click the floating **i**, then the item).', '']
                md += [card(E[k], '###', '../', k, shot=True) for k in keys if k in E]
            write(f'features/{s_}.md', '\n'.join(md))
            thumb = f'![{m.get("nav", title)}](../assets/ui/{first}-light.webp){{ loading=lazy }}' if first else ''
            idx += [f'-   **[{m.get("nav") or title}]({s_}.md)**', '', f'    {thumb}', '', f'    {m.get("what", "")}', '']
            sub.append((m.get('nav') or title.replace('`', ''), f'features/{s_}.md'))
        idx += ['</div>', '']
        nav.append((sec, sub))
    write('features/index.md', '\n'.join(idx))
    return nav


def reference(E, G):
    nav, used = [], set()
    idx = ['<span class="ol-pill">UI reference</span>', '', '# UI reference', '',
           '<p class="lede"><strong>Every button, card, canvas and panel of Octoloom, on a screenshot.</strong> What it is, when to use it and examples: '
           'the texts of the in-app <b>Explain</b> button. The file syntax is folded under <i>In the file</i>, for when you need it.</p>', '',
           '<div class="grid cards" markdown>', '']
    for gid, title, intro, keys in GROUPS:
        md = ['<span class="ol-pill">UI reference</span>', '', f'# {title}', '', f'<p class="lede">{intro}</p>', '']
        shots = REF_SHOT.get(gid, [])
        for sh in shots[:1]:
            md += [annotated(sh, '../', SHOT_CAP.get(sh, '')), '']
        for k in keys:
            if k not in E: continue
            md.append(card(E[k], '##', '../', k)); used.add(k)
            sh = KEY_SHOT.get(k)
            if sh and sh not in shots[:1] and not CARD_IMG.get(k): md += [img(sh, '../', SHOT_CAP.get(sh, E[k]['title'])), '']
        for sh in shots[1:]:
            if not any(KEY_SHOT.get(k) == sh for k in keys): md += [f'## {SHOT_CAP.get(sh, sh)}', '', annotated(sh, '../', SHOT_CAP.get(sh, '')), '']
        write(f'reference/{gid}.md', '\n'.join(md))
        sh0 = (REF_SHOT.get(gid) or [None])[0]
        th = f'![{title}](../assets/ui/{sh0}-light.webp){{ loading=lazy }}' if sh0 else ''
        idx += [f'-   **[{title}]({gid}.md)**', '', f'    {th}', '', '    ' + ', '.join(E[k]['title'] for k in keys if k in E), '']
        nav.append((title, f'reference/{gid}.md'))
    # Everything not in a group (the Quick Start entry) lives on the Quick Starts pages, not on a "More" page.
    rest = [k for k in E if k not in used and k not in QS_KEYS]
    if rest: print('  Explain entries on no page:', rest)
    # guided tours
    md = ['# Guided tours', '', 'Each canvas shows a short tour the first time you open it (*Don\'t show again* hides it). '
          'Replay it with **Guide** in the toolbar or **Start the guide** on the Explain button.', '']
    for g in G.values():
        md += [f'## {g["title"]}', ''] + [f'{i}. **{s["title"]}**: {s["body"]}' for i, s in enumerate(g['steps'], 1)] + ['']
    write('reference/guided-tours.md', '\n'.join(md))
    nav.append(('Guided tours', 'reference/guided-tours.md')); idx.append('- **[Guided tours](guided-tours.md)**: the first-time tour of each canvas')
    # commands and settings
    write('reference/commands.md', '# Commands\n\n' + readme_section('Commands'))
    write('reference/settings.md', '# Settings\n\n' + readme_section('Settings'))
    nav += [('Commands', 'reference/commands.md'), ('Settings', 'reference/settings.md')]
    idx += ['- **[Commands](commands.md)**: every command in the command palette', '- **[Settings](settings.md)**: every `agentNetwork.*` setting']
    idx.insert(idx.index('<div class="grid cards" markdown>') + 2, '')
    # close the card grid before the plain list items
    out, closed = [], False
    for l in idx:
        if not closed and l.startswith('- **['): out += ['</div>', '']; closed = True
        out.append(l)
    write('reference/index.md', '\n'.join(out))
    return nav


KIND = {'usecase': 'Use case', 'technical': 'Technical'}


def tkind(t):
    i = t['id']
    if t.get('mocked'): return 'Fully mocked'
    if '-idmc-' in i: return 'Informatica IDMC'
    if i.endswith('-governed'): return 'Governed'
    if i.endswith('-secured'): return 'Secured'
    return 'Use case'


def templates():
    style = {'v1': 'Probabilistic (Agent Network 1.0)', 'v2': 'Deterministic (Agent Network 2.0, AgentScript)'}
    idx = ['# Templates', '',
           f'Octoloom ships **{len(INDEX)} ready-to-run templates**. Open one with **New Project** (Home → *New Probabilistic / Deterministic Network* → *Use cases* or *Technical*). '
           'Every upstream is a public A²D mock, so a template deploys and answers without any backend of yours. '
           'You need an Anypoint organization with Agent Fabric, a gateway and a connected app: see [Before you start](../start/index.md).', '',
           '| Kind | What it is |', '|---|---|',
           '| Use case | A business network: agents, MCP servers and an LLM broker or an AgentScript flow. |',
           '| Governed | The same use case with built-in Agent Fabric gateway policies. |',
           '| Secured | A use case whose agents, MCP servers or LLM need authentication (client credentials, API key, OAuth 2.0). |',
           '| Fully mocked | The LLM is an A²D LLM mock too: deploy and chat without an OpenAI key. |',
           '| Informatica IDMC | Uses Informatica IDMC MCP servers (needs an IDMC org). |', '']
    nav = []
    idx[0:0] = ['<span class="ol-pill">Templates</span>', '']
    for v in ('v1', 'v2'):
        lst = [t for t in INDEX if t['version'] == v]
        idx += [f'## {style[v]}', '', '<div class="grid cards" markdown>', '']
        for t in lst:
            th = f'{RAW}/tutorials/{t["id"]}/img/canvas.png'
            idx += [f'-   **[{t["title"]}]({t["id"]}.md)**', '', f'    ![{t["title"]}]({th}){{ loading=lazy }}', '',
                    f'    <small>{tkind(t)} · {t.get("agents", 0)} agents · {t.get("mcps", 0)} MCP · {len(t.get("policies") or [])} policies</small>', '',
                    f'    {t.get("summary", "")}', '']
        idx += ['</div>', '', '| Template | Kind | Agents | MCP | Policies | Tutorial |', '|---|---|---|---|---|---|']
        sub = []
        for t in lst:
            idx.append(f'| [{t["title"]}]({t["id"]}.md) | {tkind(t)} | {t.get("agents", 0)} | {t.get("mcps", 0)} | {len(t.get("policies") or [])} | [Tutorial](../tutorials/{t["id"]}.md) |')
            src = os.path.join(TPLS, t['id'], 'README.md')
            body = open(src).read() if os.path.exists(src) else open(os.path.join(REPO, 'media', 'templates', t['id'], 'README.md')).read()
            body = re.sub(r'^# .*\n', '', body, count=1)
            img = os.path.join(TUTS, t['id'], 'img')
            shots = []
            for f, cap in (('canvas.png', 'The network canvas'), ('flow.png', 'The broker flow (AgentScript)'), ('chat.png', 'Chat with the deployed broker')):
                if os.path.exists(os.path.join(img, f)): shots.append(f'![{cap}]({RAW}/tutorials/{t["id"]}/img/{f})\n<small>{cap}</small>\n')
            pol = ', '.join(p if isinstance(p, str) else p.get('name', '') for p in (t.get('policies') or [])) or 'none'
            files = f'{TREE}/templates/{t["id"]}' if os.path.isdir(os.path.join(TPLS, t['id'])) else None
            md = [f'# {t["title"]}', '', f'> {t.get("summary", "")}', '',
                  '| | |', '|---|---|', f'| Style | {style[v]} |', f'| Kind | {tkind(t)} |',
                  f'| Agents / MCP servers | {t.get("agents", 0)} / {t.get("mcps", 0)} |',
                  f'| A2A protocol | {", ".join(t.get("protocols") or [])} |', f'| Policies | {pol} |',
                  f'| Asset prefix | `{t.get("prefix", "")}` |',
                  f'| Tutorial | [{t["title"]}: tutorial](../tutorials/{t["id"]}.md) |']
            if files: md.append(f'| Files | [templates/{t["id"]}]({files}) |')
            md += ['', '\n'.join(shots), body]
            write(f'catalog/{t["id"]}.md', '\n'.join(md))
            sub.append((t['title'], f'catalog/{t["id"]}.md'))
        idx.append('')
        nav.append((style[v].split(' (')[0], sub))
    write('catalog/index.md', '\n'.join(idx))
    return nav


# The Quick Start prerequisites of the extension (media/onboarding/steps), one page each (#349).
PREREQ = [('account', 'Anypoint account'), ('gateway', 'Small Managed Omni Gateway'), ('connected-app', 'Connected app Octoloom-CA'),
          ('connect-anypoint', 'Connect Octoloom to Agent Fabric'), ('connect-a2d', 'Connect to A²D (optional)'), ('connect-p4a', 'Connect to P4A (optional)')]
CORE_PREREQ = PREREQ[:4]


def prereqs():
    ob = os.path.join(REPO, 'media', 'onboarding')
    if not os.path.isdir(os.path.join(ob, 'steps')): return []
    out = os.path.join(DOCS, 'assets', 'onboarding'); os.makedirs(out, exist_ok=True)
    for f in os.listdir(ob):
        if f.endswith('.png'): shutil.copyfile(os.path.join(ob, f), os.path.join(out, f))
    vids = os.path.join(ob, 'videos')
    if os.path.isdir(vids):
        os.makedirs(os.path.join(out, 'videos'), exist_ok=True)
        for f in os.listdir(vids):
            if f.endswith(('.mp4', '.png')): shutil.copyfile(os.path.join(vids, f), os.path.join(out, 'videos', f))
    nav, idx = [], ['<span class="ol-pill">Get started</span>', '', '# Before you start', '',
                    '<p class="lede"><strong>What every tutorial needs, step by step.</strong> The same steps as the <b>Quick Start</b> tabs on the Octoloom Home page. '
                    'Do the first four once; A²D and P4A only for the tutorials that use them.</p>', '']
    for i, (slug_, title) in enumerate(PREREQ, 1):
        p = os.path.join(ob, 'steps', f'{slug_}.md')
        if not os.path.exists(p): continue
        md = open(p).read()
        md = re.sub(r'!\[([^\]]*)\]\(\.\./videos/([\w-]+)\.mp4\)',
                    lambda m: f'<video controls muted playsinline preload="none" poster="../../assets/onboarding/videos/{m.group(2)}.png" '
                              f'src="../../assets/onboarding/videos/{m.group(2)}.mp4" aria-label="{m.group(1)}" style="width:100%"></video>', md)
        md = re.sub(r'\]\(\.\./([\w-]+\.png)\)', r'](../assets/onboarding/\1)', md)
        # In-app wording: the step list and its buttons are not on this page.
        md = re.sub(r' ?This step ticks itself off[^.]*\.', '', md)
        md = re.sub(r'^# .*\n', f'<span class="ol-pill">Before you start · {i} of {len(PREREQ)}</span>\n\n# {title}\n', md, count=1)
        nxt = PREREQ[i] if i < len(PREREQ) else None
        md += '\n\n---\n\n' + (f'**Next:** [{nxt[1]}]({nxt[0]}.md)' if nxt else '**Next:** [pick a tutorial](../tutorials/index.md)') + '\n'
        write(f'start/{slug_}.md', md)
        idx.append(f'{i}. [{title}]({slug_}.md)')
        nav.append((title, f'start/{slug_}.md'))
    write('start/index.md', '\n'.join(idx))
    return [('Overview', 'start/index.md')] + nav


# Quick Starts: the three onboarding journeys of the extension (src/model/onboarding.ts), one page each,
# every step with its screenshot of the onboarding tab and of the Octoloom view it opens.
QS_KEYS = {'welcomeQuickStart'}
QS = [('beginner', 'Beginner', '~30 min', 'walk', 'Anypoint',
       'Pick a fully mocked template, learn the canvas, run a Deterministic network locally, then deploy it to your Omni Gateway and chat with it. No LLM key needed.',
       [('beginner-style', 'A fully mocked template', ['new-project']), ('canvas', 'Learn the canvas', ['network-v2']),
        ('run-local', 'Run it locally (Deterministic)', ['run-local-vars']), ('deploy', 'Deploy to your Omni Gateway', ['deploy-form']),
        ('chat', 'Chat and trace', ['chat-progress', 'chat-trace'])]),
      ('advanced', 'Advanced', '~45 min', 'run', 'Anypoint and A²D',
       'Connect A²D, build a use-case network from A²D mock agents and MCP servers, deploy it, then chat, trace and share it in an A²D session.',
       [('connect-a2d', 'Connect to A²D', []), ('advanced-template', 'A use-case network', ['new-project']),
        ('advanced-a2d', 'Build with A²D mocks', ['assets-a2d-llm']), ('deploy', 'Deploy to your Omni Gateway', ['deploy-form']),
        ('advanced-share', 'Chat, trace and share', ['chat-progress', 'chat-share-a2d'])]),
      ('expert', 'Expert', '~60 min', 'climb', 'Anypoint, A²D and P4A',
       'Connect A²D and P4A, start from a governed or secured technical template, add P4A and Agent Fabric policies, validate governance and check the Coverage map.',
       [('connect-a2d', 'Connect to A²D', []), ('connect-p4a', 'Connect to P4A', []), ('expert-template', 'A technical network', ['new-project']),
        ('expert-policies', 'Agent Fabric and P4A policies', ['policy-picker']), ('expert-governance', 'Validate the governance', ['governance']),
        ('expert-coverage', 'Deploy and check the coverage', ['coverage-map'])])]
QS_TPL = {'beginner': lambda t: bool(t.get('mocked')) or 'fully mocked' in (t.get('summary') or '').lower(),
          'advanced': lambda t: t['category'] == 'usecase', 'expert': lambda t: t['category'] == 'technical'}


def step_md(slug_, up):
    p = os.path.join(REPO, 'media', 'onboarding', 'steps', f'{slug_}.md')
    md = open(p).read()
    md = re.sub(r'!\[([^\]]*)\]\(\.\./videos/([\w-]+)\.mp4\)',
                lambda m: f'<video controls muted playsinline preload="none" poster="{up}assets/onboarding/videos/{m.group(2)}.png" '
                          f'src="{up}assets/onboarding/videos/{m.group(2)}.mp4" aria-label="{m.group(1)}" style="width:100%"></video>', md)
    md = re.sub(r'\]\(\.\./([\w-]+\.png)\)', rf']({up}assets/onboarding/\1)', md)
    md = re.sub(r' ?This step ticks itself off[^.]*\.', '', md)
    md = md.replace('**Templates for this journey** below', '**Templates for this journey** in the tab (listed at the end of this page)')
    md = re.sub(r'^# .*\n', '', md, count=1)
    return re.sub(r'^(#+) ', lambda m: '#' * (len(m.group(1)) + 2) + ' ', md, flags=re.M)


def quick_starts(E):
    if not os.path.isdir(os.path.join(REPO, 'media', 'onboarding', 'steps')): return []
    nav = [('Overview', 'quick-starts/index.md')]
    idx = ['<span class="ol-pill">Get started</span>', '', '# Quick Starts', '',
           '<p class="lede"><strong>Three guided journeys, from your first network to governed production.</strong> '
           'The same journeys as the <b>Quick Start</b> cards on the Octoloom Home page: each opens as its own Octoloom tab with the steps on the left, '
           'the page of the step on the right, short videos and buttons that open the right view. Every journey starts with the four '
           '<a href="../start/index.md">prerequisites</a>.</p>', '',
           img('welcome', '../', 'Home → Quick Start: the Beginner, Advanced and Expert cards'), '',
           '<div class="grid cards" markdown>', '']
    for jid, level, time, icon, needs, text, steps in QS:
        n = len(CORE_PREREQ) + len(steps)
        idx += [f'-   **[{level}]({jid}.md)** · {time}', '', f'    ![{level}](../assets/ui/qs-{jid}-{len(CORE_PREREQ)}-light.webp){{ loading=lazy }}', '',
                f'    {text}', '', f'    <small>{n} steps · needs {needs}</small>', '']
    idx += ['</div>', '', '| Journey | Time | Needs | Steps | Templates |', '|---|---|---|---|---|']
    for jid, level, time, icon, needs, text, steps in QS:
        tl = [t for t in INDEX if QS_TPL[jid](t)]
        idx.append(f'| [{level}]({jid}.md) | {time} | {needs} | {len(CORE_PREREQ) + len(steps)} | {len(tl)} |')
    e = E.get('welcomeQuickStart')
    if e: idx += ['', '## How the Quick Start tab works', '', card(e, '###')]
    write('quick-starts/index.md', '\n'.join(idx))
    for jid, level, time, icon, needs, text, steps in QS:
        n = len(CORE_PREREQ) + len(steps)
        md = [f'<span class="ol-pill">Quick Start · {level} · {time}</span>', '', f'# {level} journey', '', f'<p class="lede">{text}</p>', '',
              f'**Needs:** {needs}. **Steps:** {n}. Open it in VS Code with **Home → Quick Start → {level}**, or *Octoloom: Quick Start* in the Command Palette.', '',
              '## The journey at a glance', '']
        allsteps = [(s_, t, None) for s_, t in CORE_PREREQ] + steps
        for i, (s_, t, _) in enumerate(allsteps, 1):
            md.append(f'{i}. [{t}](#{i}-{slug(t)})')
        md += ['', f'## Steps 1–{len(CORE_PREREQ)}: the prerequisites', '',
               'Every journey starts with the same four steps. Each is explained step by step, with videos, under **Before you start**:', '']
        for i, (s_, t) in enumerate(CORE_PREREQ, 1):
            md += [f'### {i}. {t}', '', f'See [{t}](../start/{s_}.md).', '']
        for k, (s_, t, shots) in enumerate(steps):
            i = len(CORE_PREREQ) + k + 1
            md += [f'### {i}. {t}', '', img(f'qs-{jid}-{i - 1}', '../', f'{level} onboarding tab, step {i} of {n}: {t}'), '', step_md(s_, '../'), '']
            for sh in shots:
                md += [img(sh, '../', SHOT_CAP.get(sh) or t), '']
        tl = [t for t in INDEX if QS_TPL[jid](t)]
        md += ['## Templates for this journey', '', f'The {level} tab lists these templates; click one to create the project right in the tab.', '',
               '| Template | Style | Agents | MCP | Tutorial |', '|---|---|---|---|---|']
        for t in sorted(tl, key=lambda t: (t['version'] != 'v2', t['title'])):
            md.append(f'| [{t["title"]}](../catalog/{t["id"]}.md) | {"Deterministic" if t["version"] == "v2" else "Probabilistic"} | {t.get("agents", 0)} | {t.get("mcps", 0)} | [Tutorial](../tutorials/{t["id"]}.md) |')
        nxt = {'beginner': ('advanced', 'Advanced'), 'advanced': ('expert', 'Expert')}.get(jid)
        md += ['', '---', '', f'**Next:** [the {nxt[1]} journey]({nxt[0]}.md)' if nxt else '**Next:** [pick a tutorial](../tutorials/index.md)', '']
        write(f'quick-starts/{jid}.md', '\n'.join(md))
        nav.append((level, f'quick-starts/{jid}.md'))
    return nav


def prereq_line(up='../'):
    links = ' · '.join(f'[{t}]({up}start/{s_}.md)' for s_, t in CORE_PREREQ)
    return f'- **Not set up yet?** The Quick Start prerequisites, step by step with pictures: {links}.'


def tutorials():
    def fix(md, page_dir_is_tutorials=True):
        md = re.sub(r'\]\(\.\./README\.md\)', '](index.md)', md)
        md = re.sub(r'\]\(\.\./getting-started\.md\)', '](../getting-started.md)', md)
        md = re.sub(r'\]\(\.\./([\w-]+)/README\.md\)', r'](\1.md)', md)
        md = re.sub(r'\]\(([\w-]+)/README\.md\)', r'](\1.md)', md)
        md = re.sub(r'\]\(getting-started\.md\)', '](../getting-started.md)', md)
        return site_links(md, 'tutorials/')
    nav = {'v1': [], 'v2': []}
    for t in INDEX:
        p = os.path.join(TUTS, t['id'], 'README.md')
        if not os.path.exists(p): continue
        body = fix(open(p).read())
        if os.path.isdir(os.path.join(REPO, 'media', 'onboarding', 'steps')):
            if '](../start/' not in body.split('## Path 1')[0]:
                body = re.sub(r'(## Before you start\n\n(?:- .*\n)+)', lambda m: m.group(1) + prereq_line() + '\n', body, count=1)
        write(f'tutorials/{t["id"]}.md', body)
        nav[t['version']].append((t['title'], f'tutorials/{t["id"]}.md'))
    ti = fix(open(os.path.join(TUTS, 'README.md')).read())
    grid = ['', '## Pick a tutorial', '', '<div class="grid cards" markdown>', '']
    for t in INDEX:
        if not os.path.exists(os.path.join(TUTS, t['id'], 'README.md')): continue
        th = f'{RAW}/tutorials/{t["id"]}/img/canvas.png'
        grid += [f'-   **[{t["title"]}]({t["id"]}.md)**', '', f'    ![{t["title"]}]({th}){{ loading=lazy }}', '',
                 f'    <small>{"Probabilistic (v1)" if t["version"] == "v1" else "Deterministic (v2)"} · {tkind(t)}</small>', '']
    grid += ['</div>', '']
    ti = re.sub(r'^(# .*\n)', r'<span class="ol-pill">Tutorials</span>\n\n\1', ti, count=1)
    write('tutorials/index.md', ti + '\n'.join(grid))
    gs = open(os.path.join(TUTS, 'getting-started.md')).read()
    gs = re.sub(r'\]\(README\.md\)', '](tutorials/index.md)', gs)
    gs = re.sub(r'\]\(([\w-]+)/README\.md\)', r'](tutorials/\1.md)', gs)
    write('getting-started.md', site_links(gs, ''))
    return [('Probabilistic', nav['v1']), ('Deterministic', nav['v2'])]


def skills():
    if not os.path.isdir(SKILLS): return []
    nav = []
    readme = open(os.path.join(SKILLS, 'README.md')).read()
    readme = re.sub(r'\]\(\.?/?([\w-]+)/SKILL\.md\)', r'](\1.md)', readme)
    readme = re.sub(r'\]\(\.\./tutorials/getting-started\.md\)', '](../getting-started.md)', readme)
    readme = re.sub(r'\]\(\.\./(templates|tutorials)/?(README\.md)?\)', lambda m: f']({TREE}/{m.group(1)})', readme)
    readme = re.sub(r'\]\(\.\./([^)]+)\)', lambda m: f']({BLOB}/{m.group(1)})', readme)
    for d in sorted(os.listdir(SKILLS)):
        f = os.path.join(SKILLS, d, 'SKILL.md')
        if not os.path.exists(f): continue
        text = open(f).read()
        fm = re.match(r'(?s)^---\n(.*?)\n---\n', text)
        desc = ''
        if fm:
            m = re.search(r'(?m)^description:\s*(.+)$', fm.group(1)); desc = (m.group(1).strip().strip('"\'') if m else '')
            text = text[fm.end():]
        text = re.sub(r'\]\(\.\./([\w-]+)/SKILL\.md\)', r'](\1.md)', text)
        head = [f'!!! tip "Use this skill"', f'    {desc}' if desc else '', '',
                f'    Source: [`skills/{d}/SKILL.md`]({BLOB}/skills/{d}/SKILL.md) · [raw]({RAW}/skills/{d}/SKILL.md). '
                f'Copy the folder into `.claude/skills/` of your project (or `~/.claude/skills/`).', '']
        body = text.lstrip()
        if body.startswith('# '):
            first, _, rest = body.partition('\n'); body = first + '\n\n' + '\n'.join(head) + rest
        else:
            body = f'# {d}\n\n' + '\n'.join(head) + body
        write(f'skills/{d}.md', body)
        nav.append((d, f'skills/{d}.md'))
    write('skills/index.md', readme)
    return nav


def team():
    t = readme_section('Meet the Octoloomies') if 'Meet the Octoloomies' in README else ''
    write('team.md', '# Meet the Octoloomies\n\n' + t)


def ref_pages():
    for title, rel in (('Requirements', 'requirements.md'), ('Privacy and security', 'privacy.md'), ('Known limitations', 'limitations.md')):
        body = readme_section(title)
        # The README links the event catalog next to itself; on the site it is published under assets (#347).
        if os.path.exists(os.path.join(REPO, 'telemetry.json')):
            shutil.copyfile(os.path.join(REPO, 'telemetry.json'), os.path.join(DOCS, 'assets', 'telemetry.json'))
            body = body.replace('](telemetry.json)', '](../assets/telemetry.json)')
        write(f'about/{rel}', f'# {title}\n\n' + body)


def nav_yaml(items, ind=2):
    out = []
    for title, x in items:
        t = json.dumps(title, ensure_ascii=False)
        if isinstance(x, list):
            out.append(' ' * ind + f'- {t}:'); out += nav_yaml(x, ind + 4)
        else:
            out.append(' ' * ind + f'- {t}: {x}')
    return out


def main():
    data = explain()
    E, G = data['E'], data['G']
    # docs/assets/usage.json and docs/assets/usage/ are written by the usage Action (octoloom#333), not by this
    # generator: keep them across the regeneration.
    keep = {}
    for rel in ('assets/usage.json', 'assets/usage'):
        p_ = os.path.join(DOCS, rel)
        if os.path.exists(p_):
            tmp = os.path.join(ROOT, '.usage-keep-' + os.path.basename(rel)); shutil.rmtree(tmp, ignore_errors=True)
            (shutil.copytree if os.path.isdir(p_) else shutil.copy)(p_, tmp); keep[rel] = tmp
    if os.path.isdir(DOCS): shutil.rmtree(DOCS)
    os.makedirs(os.path.join(DOCS, 'assets'))
    for rel, tmp in keep.items():
        shutil.move(tmp, os.path.join(DOCS, rel))
    shutil.copy(os.path.join(REPO, 'media', 'octoloom.png'), os.path.join(DOCS, 'assets', 'loomi.png'))
    shutil.copy(os.path.join(HERE, 'extra.css'), os.path.join(DOCS, 'assets', 'extra.css'))
    shutil.copy(os.path.join(HERE, 'marketplace.js'), os.path.join(DOCS, 'assets', 'marketplace.js'))
    shutil.copy(os.path.join(HERE, 'usage.js'), os.path.join(DOCS, 'assets', 'usage.js'))
    if os.path.isdir(UI): shutil.copytree(UI, os.path.join(DOCS, 'assets', 'ui'), ignore=shutil.ignore_patterns('index.json'))
    global MK
    MK = market_stats()
    version = PKG['version']
    write('index.md', home(version))
    tut = tutorials()
    pre = prereqs()
    qs = quick_starts(E)
    nav = [('Get started', [('Introduction', 'index.md'), ('Getting started', 'getting-started.md')]
                           + ([('Before you start', pre)] if pre else []) + ([('Quick Starts', qs)] if qs else [])
                           + [('Install from the Marketplace', MARKET)]),
           ('Using Octoloom', [('All features', 'features/index.md')] + features(E)),
           ('UI reference', [('Overview', 'reference/index.md')] + reference(E, G)),
           ('Templates', [('All templates', 'catalog/index.md')] + templates()),
           ('Tutorials', [('All tutorials', 'tutorials/index.md')] + tut)]
    sk = skills()
    if sk: nav.append(('Skills for AI assistants', [('Overview', 'skills/index.md')] + sk))
    ref_pages(); team()
    req = open(os.path.join(DOCS, 'about', 'requirements.md')).read()
    write('about/requirements.md', req + '\n\n' + img('setup-connect', '../', 'Setup & Connect → Tooling checks every requirement and installs what is missing'))
    # Public usage (octoloom#334): aggregates written by the usage Action (#333), and what telemetry collects.
    write('usage.md', usage_page.usage_page())
    write('data-we-collect.md', usage_page.data_page(REPO))
    nav.append(('About', [('Requirements', 'about/requirements.md'), ('Privacy and security', 'about/privacy.md'),
                          ('Usage', 'usage.md'), ('Data we collect', 'data-we-collect.md'),
                          ('Known limitations', 'about/limitations.md'), ('Meet the Octoloomies', 'team.md')]))
    write('version.md', changelog_page.page(REPO, MK.get('version') or version))
    nav.append(('Version', [('Version history', 'version.md')]))
    yml = f'''# Generated by docs-src/build_docs.py (octoloom#301). Edit the generator, not this file.
site_name: Octoloom for Agent Fabric
site_description: Design, govern, deploy and observe MuleSoft Agent Fabric agent networks, visually, in VS Code.
site_url: {SITE}
repo_url: https://github.com/A2D-Agentic-Asset-Designer/octoloom-assets
repo_name: octoloom-assets
edit_uri: ""
copyright: 'Octoloom for Agent Fabric {version} · <a href="{MARKET}">VS Code Marketplace</a>'
theme:
  name: material
  custom_dir: docs-src/overrides
  logo: assets/loomi.png
  favicon: assets/loomi.png
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: custom
      accent: custom
      toggle:
        icon: material/weather-night
        name: Dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: custom
      accent: custom
      toggle:
        icon: material/weather-sunny
        name: Light mode
  features:
    - navigation.sections
    - navigation.top
    - navigation.indexes
    - navigation.footer
    - search.suggest
    - search.highlight
    - content.code.copy
    - toc.follow
    - navigation.instant
    - content.tabs.link
  font:
    text: Play
    code: JetBrains Mono
extra_css:
  - assets/extra.css
extra_javascript:
  - assets/marketplace.js
  - assets/usage.js
extra:
  version: "{version}"
  installs: "{MK['installs']:,}"
  marketplace: {MARKET}
  social:
    - icon: material/microsoft-visual-studio-code
      link: {MARKET}
      name: Octoloom on the VS Code Marketplace
    - icon: fontawesome/brands/github
      link: https://github.com/A2D-Agentic-Asset-Designer/octoloom-assets
      name: octoloom-assets on GitHub
markdown_extensions:
  - admonition
  - attr_list
  - md_in_html
  - tables
  - toc:
      permalink: true
  - pymdownx.details
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.superfences
  - pymdownx.highlight
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg
plugins:
  - search
nav:
''' + '\n'.join(nav_yaml(nav)) + '\n'
    open(os.path.join(ROOT, 'mkdocs.yml'), 'w').write(yml)
    print('docs written:', sum(len(f) for _, _, f in os.walk(DOCS)), 'files')


main()
