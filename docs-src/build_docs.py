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
import json, os, re, shutil, subprocess, sys

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


def card(e, level='###'):
    out = [f'{level} {e["title"]}', '', e['what'], '', f'**When to use it:** {e["when"]}', '']
    if e.get('examples'):
        out += ['**Examples:**', ''] + [f'- {x}' for x in e['examples']] + ['']
    if e.get('snippet'):
        lang = 'yaml' if re.match(r'^\s*[\w-]+:\s', e['snippet']) and 'transition to' not in e['snippet'] and '->' not in e['snippet'] else 'text'
        out += [f'```{lang}', e['snippet'], '```', '']
    return '\n'.join(out)


def home(version):
    hl = readme_section('Highlights')
    rows = [l for l in hl.splitlines() if l.startswith('| **')]
    cards = []
    for r in rows:
        m = re.match(r'\| \*\*(.+?)\*\* \| (.+) \|$', r)
        if m: cards.append(f'-   **{m.group(1)}**\n\n    ---\n\n    {m.group(2)}')
    intro = README.split('## Highlights')[0]
    intro = re.sub(r'(?s)^.*?</p>\s*', '', intro, count=1) if '</p>' in intro else intro
    intro = re.sub(r'(?s)<h1.*?</h1>|<p[^>]*>.*?</p>', '', intro)
    intro = re.sub(r'(?m)^</?div.*$|^<img.*$|^---\s*$', '', intro)
    intro = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', intro).strip()
    return f'''---
hide:
  - navigation
  - toc
---

<div class="hero" markdown>

![Loomi, the Octoloom octopus](assets/loomi.png){{ .hero-logo }}

# Octoloom for Agent Fabric

**Design, govern, deploy and observe MuleSoft Agent Fabric agent networks, visually, in VS Code.**

[Get it on the Marketplace]({MARKET}){{ .md-button .md-button--primary }}
[Getting started](getting-started.md){{ .md-button }}
[Tutorials](tutorials/index.md){{ .md-button }}

<small>Version {version}</small>

</div>

{intro}

![Deterministic network canvas with the inspector]({RAW}/screenshots/network-v2.png)

## Where to start

<div class="grid cards" markdown>

-   :material-rocket-launch: **[Getting started](getting-started.md)**

    ---

    A 20-minute tour: install, connect, create a project from a template, deploy and chat.

-   :material-school: **[Tutorials](tutorials/index.md)**

    ---

    One per template ({len(INDEX)}), each with three paths: *Just use it*, *Learn step by step* and *Build it from scratch*.

-   :material-view-grid: **[Templates](catalog/index.md)**

    ---

    Ready-to-run agent networks: use cases, governed, secured, fully mocked and Informatica IDMC.

-   :material-book-open-variant: **[Features](features/index.md)**

    ---

    Every view of Octoloom, what it does and how to use it, with screenshots.

-   :material-gesture-tap-button: **[UI reference](reference/index.md)**

    ---

    Every button, card, canvas and panel: what it is, when to use it, examples. The same texts as the in-app **Explain** button.

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
    tour = readme_section('Feature tour')
    pages, nav = [], []
    idx = ['# Features', '', 'Every view of Octoloom, in the order you meet them. Each page ends with the buttons and components of that view, as the **Explain** button describes them.', '']
    for title, body in sections(tour, 3):
        s = slug(title)
        md = [f'# {title}', '', site_links(body, 'features/'), '']
        keys = FEATURE_EXPLAIN.get(s, [])
        if keys:
            md += ['## Buttons and components', '', 'The same text as the in-app **Explain** button (click the floating info button, then the item).', '']
            md += [card(E[k]) for k in keys if k in E]
        write(f'features/{s}.md', '\n'.join(md))
        first = re.sub(r'\s+', ' ', re.sub(r'!\[[^\]]*\]\([^)]*\)', '', body).strip().split('\n\n')[0])
        idx.append(f'- **[{title.replace("`", "")}]({s}.md)**: {first[:220]}{"…" if len(first) > 220 else ""}')
        nav.append((title.replace('`', ''), f'features/{s}.md'))
    write('features/index.md', '\n'.join(idx))
    return nav


def reference(E, G):
    nav, used = [], set()
    idx = ['# UI reference', '', 'Every button, card, canvas and panel of Octoloom: what it is, when to use it and examples. '
           'These are the texts of the in-app **Explain** button: click the floating info button in any Octoloom editor, then click the item.', '']
    for gid, title, intro, keys in GROUPS:
        md = [f'# {title}', '', intro, '']
        for k in keys:
            if k in E: md.append(card(E[k], '##')); used.add(k)
        write(f'reference/{gid}.md', '\n'.join(md))
        idx.append(f'- **[{title}]({gid}.md)**: ' + ', '.join(E[k]['title'] for k in keys if k in E))
        nav.append((title, f'reference/{gid}.md'))
    rest = [k for k in E if k not in used]
    if rest:
        write('reference/more.md', '\n'.join(['# More', ''] + [card(E[k], '##') for k in rest]))
        nav.append(('More', 'reference/more.md')); idx.append('- **[More](more.md)**')
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
    write('reference/index.md', '\n'.join(idx))
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
           'Every upstream is a public A²D mock, so a template deploys and answers without any backend of yours.', '',
           '| Kind | What it is |', '|---|---|',
           '| Use case | A business network: agents, MCP servers and an LLM broker or an AgentScript flow. |',
           '| Governed | The same use case with built-in Agent Fabric gateway policies. |',
           '| Secured | A use case whose agents, MCP servers or LLM need authentication (client credentials, API key, OAuth 2.0). |',
           '| Fully mocked | The LLM is an A²D LLM mock too: deploy and chat without an OpenAI key. |',
           '| Informatica IDMC | Uses Informatica IDMC MCP servers (needs an IDMC org). |', '']
    nav = []
    for v in ('v1', 'v2'):
        lst = [t for t in INDEX if t['version'] == v]
        idx += [f'## {style[v]}', '', '| Template | Kind | Agents | MCP | Policies | Tutorial |', '|---|---|---|---|---|---|']
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
        write(f'tutorials/{t["id"]}.md', fix(open(p).read()))
        nav[t['version']].append((t['title'], f'tutorials/{t["id"]}.md'))
    write('tutorials/index.md', fix(open(os.path.join(TUTS, 'README.md')).read()))
    gs = open(os.path.join(TUTS, 'getting-started.md')).read()
    gs = re.sub(r'\]\(README\.md\)', '](tutorials/index.md)', gs)
    gs = re.sub(r'\]\(([\w-]+)/README\.md\)', r'](tutorials/\1.md)', gs)
    write('getting-started.md', site_links(gs, ''))
    return [('Probabilistic (v1)', nav['v1']), ('Deterministic (v2)', nav['v2'])]


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
        write(f'about/{rel}', f'# {title}\n\n' + readme_section(title))


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
    if os.path.isdir(DOCS): shutil.rmtree(DOCS)
    os.makedirs(os.path.join(DOCS, 'assets'))
    shutil.copy(os.path.join(REPO, 'media', 'octoloom.png'), os.path.join(DOCS, 'assets', 'loomi.png'))
    shutil.copy(os.path.join(HERE, 'extra.css'), os.path.join(DOCS, 'assets', 'extra.css'))
    version = PKG['version']
    write('index.md', home(version))
    tut = tutorials()
    nav = [('Home', 'index.md'), ('Getting started', 'getting-started.md'),
           ('Tutorials', [('All tutorials', 'tutorials/index.md')] + tut),
           ('Templates', [('All templates', 'catalog/index.md')] + templates()),
           ('Features', [('Overview', 'features/index.md')] + features(E)),
           ('UI reference', [('Overview', 'reference/index.md')] + reference(E, G))]
    sk = skills()
    if sk: nav.append(('Skills', [('Overview', 'skills/index.md')] + sk))
    ref_pages(); team()
    nav.append(('About', [('Requirements', 'about/requirements.md'), ('Privacy and security', 'about/privacy.md'),
                          ('Known limitations', 'about/limitations.md'), ('Meet the Octoloomies', 'team.md')]))
    yml = f'''# Generated by docs-src/build_docs.py (octoloom#301). Edit the generator, not this file.
site_name: Octoloom for Agent Fabric
site_description: Design, govern, deploy and observe MuleSoft Agent Fabric agent networks, visually, in VS Code.
site_url: {SITE}
repo_url: https://github.com/A2D-Agentic-Asset-Designer/octoloom-assets
repo_name: octoloom-assets
edit_uri: ""
copyright: Octoloom for Agent Fabric {version}
theme:
  name: material
  logo: assets/loomi.png
  favicon: assets/loomi.png
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      accent: light blue
      toggle:
        icon: material/weather-night
        name: Dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: indigo
      accent: light blue
      toggle:
        icon: material/weather-sunny
        name: Light mode
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.top
    - navigation.indexes
    - navigation.footer
    - search.suggest
    - search.highlight
    - content.code.copy
    - toc.follow
extra_css:
  - assets/extra.css
markdown_extensions:
  - admonition
  - attr_list
  - md_in_html
  - tables
  - toc:
      permalink: true
  - pymdownx.details
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
