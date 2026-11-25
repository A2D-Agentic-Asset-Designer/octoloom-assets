"""Usage and "Data we collect" pages of the docs site (octoloom#334).

- Usage: static page that reads docs/assets/usage.json (written by the usage Action, octoloom#333) in the
  browser with usage.js. Aggregates only (k >= 5); no tracking, third-party JS or CDN; the world map is the
  committed SVG docs-src/usage/world.svg.
- Data we collect: generated from the extension's catalog so it can't drift: telemetry.json at the Octoloom
  repo root when it exists (octoloom#330), otherwise TELEMETRY_EVENTS in src/model/telemetry.ts.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))

PURPOSE = {
    'activate': 'Octoloom started (once per VS Code session).',
    'heartbeat': 'The machine used Octoloom today (at most once per UTC day), with which connections are set up.',
    'build': 'Build ran: success or failure, network style, how many policies (as a range) and whether it is governed.',
    'validate': 'Validate ran: success, failure or cancelled.',
    'publish': 'Publish to Exchange ran: success or failure.',
    'deploy': 'Deploy ran: success, failure or cancelled, and whether it also published.',
    'governance': 'A governance check ran: conforms, violations or error, and how many rulesets (as a range).',
    'create': 'A project was created: network style and the template id from the public catalog (or blank).',
    'feature': 'An Octoloom command was used (at most once per command per UTC day). Only the command id.',
    'error': 'A guarded action failed: the action and the error class name (for example deploy:SourceError), never the message.',
}
PROP_DESC = {
    'outcome': 'result', 'style': 'v1 (Probabilistic) or v2 (Deterministic)', 'policies': 'number of policies as a range',
    'governed': 'project has governance', 'autopublish': 'deploy also published', 'rulesets': 'number of rulesets as a range',
    'template': 'catalog template id, blank, or other', 'id': 'contributed Octoloom command id', 'action': 'the action that failed',
    'code': 'action:ErrorClass', 'anypoint': 'connected to Agent Fabric', 'a2d': 'connected to A²D', 'p4a': 'connected to P4A',
    'idmc': 'connected to Headless IDMC',
}
COMMON = [
    ('extVersion', 'Octoloom version (semver only)'), ('vscodeVersion', 'VS Code version (semver only)'),
    ('os', 'win, mac, linux or other'), ('uiKind', 'desktop or web'),
    ('remoteName', 'none, ssh, wsl, container, codespaces or other (never the host name)'),
    ('country', 'derived by PostHog from the IP address, which is then discarded'),
]
NEVER = ['names of projects, agents, brokers or files', 'file paths, file contents or project files',
         'URLs, host names, gateway or environment names', 'organization ids, user names or e-mail addresses',
         'API keys, tokens or credentials', 'error messages or stack traces', 'chat messages or prompts',
         'the IP address (discarded after the country lookup) and anything finer than the country',
         'a user profile: events are anonymous (no person profiles)']


def catalog(repo):
    """[(event, [(prop, type/values)])] from telemetry.json or TELEMETRY_EVENTS; source label."""
    tj = os.path.join(repo, 'telemetry.json')
    if os.path.exists(tj):
        d = json.load(open(tj))
        ev = d.get('events', d)
        out = []
        for name, spec in ev.items():
            props = spec.get('properties', spec) if isinstance(spec, dict) else {}
            out.append((name, [(k, v if isinstance(v, str) else v.get('type', '') if isinstance(v, dict) else '') for k, v in props.items() if k not in ('purpose', 'classification')]))
        return out, 'telemetry.json'
    src = open(os.path.join(repo, 'src', 'model', 'telemetry.ts')).read() if os.path.exists(os.path.join(repo, 'src', 'model', 'telemetry.ts')) else ''
    m = re.search(r'export const TELEMETRY_EVENTS = \{(.*?)\n\}', src, re.S)
    if not m:
        return [], None
    consts = dict(re.findall(r'const (\w+) = e\(([^)]*)\);', src))
    consts.update({k: v for k, v in re.findall(r'export const (\w+_BUCKETS) = \[([^\]]*)\]', src)})
    def split_top(body):
        parts, depth, cur = [], 0, ''
        for ch in body:
            if ch in '({[': depth += 1
            if ch in ')}]': depth -= 1
            if ch == ',' and depth == 0: parts.append(cur); cur = ''
            else: cur += ch
        if cur.strip(): parts.append(cur)
        return [x.strip() for x in parts if x.strip()]
    def vals(spec):
        spec = spec.strip()
        if spec == 'BOOL': return 'boolean'
        if spec in consts: return ' · '.join(x.strip(" '") for x in consts[spec].split(','))
        b = re.match(r"e\(\.\.\.(\w+)\)", spec)
        if b: return {'ERROR_ACTIONS': '', 'FEATURE_IDS': ''}.get(b.group(1), ' · '.join(x.strip(" '") for x in consts.get(b.group(1), '').split(',')))
        if spec.startswith('e('): return ' · '.join(x.strip(" '") for x in spec[2:-1].split(','))
        return ''
    out = []
    body = m.group(1)
    for line in [l.strip().rstrip(',') for l in body.splitlines() if re.match(r'\s*\w+: \{', l)]:
        name, rest = line.split(':', 1)
        inner = rest.strip()[1:-1]
        props = []
        for part in split_top(inner):
            k, spec = part.split(':', 1)
            props.append((k.strip(), vals(spec)))
        out.append((name.strip(), props))
    return out, 'src/model/telemetry.ts'


def data_page(repo):
    cat, src = catalog(repo)
    rows = []
    for name, props in cat:
        ps = '<br>'.join(f'`{k}`: {PROP_DESC.get(k, "")}' + (f' ({t})' if t else '') for k, t in props) or 'common properties only'
        rows.append(f'| `{name}` | {PURPOSE.get(name, "")} | {ps} |')
    note = '' if src == 'telemetry.json' else '\n!!! note "Source"\n    This list is generated from the extension\'s event catalog. The machine-readable `telemetry.json` that ships in the extension ships with the release that starts sending.\n'
    return f'''<span class="ol-pill">About</span>

# Data we collect

Octoloom can send **anonymous usage counts** to help improve the extension: which actions run, whether they work, and on which versions. This page lists every event and every property. Nothing else is sent. The public [Usage](usage.md) page shows the totals.
{note}
## How it works

- **Off when VS Code telemetry is off.** Octoloom sends through VS Code's own telemetry logger, so VS Code's `telemetry.telemetryLevel` always wins.
- **Its own switch.** The setting `agentNetwork.telemetry.enabled` turns Octoloom's usage counts off, whatever VS Code's setting is.
- **Anonymous.** Events carry VS Code's anonymous machine id and no person profile. They are not linked to an Anypoint, A²D, P4A or IDMC account.
- **Small.** At most 100 events per VS Code session; the daily ping and each command at most once per day.
- **Only fixed values.** Every property is a fixed value, a yes/no or a range. Free text can't be sent: the extension drops it before sending.

## Events

| Event | Why | Properties |
|---|---|---|
{chr(10).join(rows)}

Every event also carries these common properties:

| Property | Value |
|---|---|
{chr(10).join(f"| `{k}` | {v} |" for k, v in COMMON)}

## Never collected

{chr(10).join(f"- {x}" for x in NEVER)}

## Where the data goes

- **Processor:** PostHog Cloud **EU** (servers in the EU). The project discards the IP address after the country lookup and keeps no person profiles.
- **Retention:** raw events for **1 year**. After that only monthly aggregates are kept (counts, no machine ids).
- **Public numbers:** the [Usage](usage.md) page shows only totals, and countries or other breakdowns only when they cover at least **5 machines**; smaller groups are shown as *Other*.

## Turn it off

- In VS Code: **Settings → Telemetry → Telemetry Level → off** (`"telemetry.telemetryLevel": "off"`), which turns off telemetry of all extensions; or
- only for Octoloom: `"agentNetwork.telemetry.enabled": false` in your settings (search **@tag:telemetry** in the Settings editor).

## Deletion

Raw events are **deleted automatically after 1 year**. On our current PostHog plan the events of a single machine can't be deleted earlier, so we don't offer deletion on request. Turning telemetry off (above) stops every further event at once. No IP address and no person profile is stored, so the events are not linked to you.
'''


def usage_page():
    svg = open(os.path.join(HERE, 'usage', 'world.svg')).read()
    svg = re.sub(r'<!--.*?-->\n', '', svg, flags=re.S)
    return f'''---
hide:
  - toc
---

<span class="ol-pill">Community</span>

# Usage

How Octoloom is used, in totals. The numbers come from the anonymous usage counts described in [Data we collect](data-we-collect.md): only aggregates, and only groups of at least **5 machines** (smaller groups are shown as *Other*). Installs come from the VS Code Marketplace.

<div class="ol-usage" id="ol-usage" markdown="0">
<p class="ol-u-empty" hidden><b>No data yet.</b> The numbers appear here once the first release that sends anonymous usage counts is in use. Until then, see the Marketplace installs below.</p>
<div class="ol-stats">
<div class="ol-stat"><b data-u="active.day">–</b><span>Active machines today</span></div>
<div class="ol-stat"><b data-u="active.week">–</b><span>This week</span></div>
<div class="ol-stat"><b data-u="active.month">–</b><span>Last 30 days</span></div>
<a class="ol-stat" href="https://marketplace.visualstudio.com/items?itemName=octoloom.octoloom"><b class="ol-installs" data-fallback="">–</b><span>Marketplace installs</span></a>
</div>

<h2 id="countries">Where Octoloom is used</h2>
<div class="ol-u-map">{svg}</div>
<div class="ol-u-legend" aria-hidden="true"><span>fewer</span><i></i><span>more machines</span></div>
<table class="ol-u-table" data-u-table="countries"><thead><tr><th>Country</th><th>Machines (30 days)</th></tr></thead><tbody></tbody></table>

<h2 id="networks">Networks built</h2>
<div class="ol-stats">
<div class="ol-stat"><b data-u="styles.build.v1.uses">–</b><span>Probabilistic (v1) builds</span></div>
<div class="ol-stat"><b data-u="styles.build.v2.uses">–</b><span>Deterministic (v2) builds</span></div>
<div class="ol-stat"><b data-u="build.withPolicies">–</b><span>Builds with policies</span></div>
<div class="ol-stat"><b data-u="build.governed">–</b><span>Governed builds</span></div>
<div class="ol-stat"><b data-u="events.deploy">–</b><span>Deploys</span></div>
</div>

<h2 id="features">Most-used features</h2>
<div class="ol-u-bars" data-u-bars="features"></div>

<h2 id="templates">Popular templates</h2>
<div class="ol-u-bars" data-u-bars="templates"></div>

<h2 id="connections">Connections</h2>
<div class="ol-u-bars" data-u-bars="connections"></div>

<h2 id="trends">Weekly trend</h2>
<div class="ol-u-trend" data-u-trend></div>
<table class="ol-u-table" data-u-table="trends"><thead><tr><th>Week</th><th>Active machines</th><th>Builds</th><th>Deploys</th><th>Projects created</th></tr></thead><tbody></tbody></table>

<p class="ol-u-meta">Last refresh: <span data-u="refreshed">–</span> · groups below 5 machines are shown as Other · <a href="../data-we-collect/">What we collect</a></p>
<div class="ol-u-tip" role="tooltip" hidden></div>
</div>
'''
