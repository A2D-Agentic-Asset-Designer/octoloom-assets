"""Version page (octoloom#301): the CHANGELOG by version, changes in plain words, contributors per change.

Contributors = the issue's creator and the implementer (author of the merged PR), from docs-src/contributors.json
(refresh: docs-src/changelog_page.py --refresh <repo>). Without an issue the contributor is amirkhan-ak-sf.
Issue numbers and names are not shown; the octoloom repo is private."""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'contributors.json')
NAMES = {'amirkhan-ak-sf': 'Amir Khan', 'jeffcock': 'George Jeffcock', 'burak-tas': 'Burak Tas', 'tommasobolis': 'Tommaso Bolis', 'gabrielmule': 'Gabriel Bustos Sölch'}
EARLY = ['gabrielmule', 'amirkhan-ak-sf']  # every change before 0.7.0


def vt(v):
    return tuple(int(x) for x in re.findall(r'\d+', v)[:3])
DEFAULT = 'amirkhan-ak-sf'
BOTS = {'claude', 'github-actions', 'dependabot'}


def person(login):
    return f'[{NAMES.get(login, login)}](https://github.com/{login})'


def refresh(changelog):
    nums = sorted({int(n) for n in re.findall(r'#(\d+)', open(changelog).read())})
    out = {}
    for n in nums:
        q = ('{repository(owner:"A2D-Agentic-Asset-Designer",name:"octoloom"){issueOrPullRequest(number:%d){__typename '
             '... on Issue{author{login} closedByPullRequestsReferences(first:5,includeClosedPrs:true){nodes{author{login} merged}}} '
             '... on PullRequest{author{login}}}}}' % n)
        try:
            d = json.loads(subprocess.run(['gh', 'api', 'graphql', '-f', 'query=' + q], capture_output=True, check=True, text=True).stdout)
            d = d['data']['repository']['issueOrPullRequest'] or {}
        except Exception:
            continue
        a = (d.get('author') or {}).get('login')
        impl = [p['author']['login'] for p in (d.get('closedByPullRequestsReferences') or {}).get('nodes', []) if p.get('merged')]
        if d.get('__typename') == 'PullRequest': impl = [a]
        out[str(n)] = {'type': d.get('__typename'), 'creator': a, 'impl': sorted(set(impl))}
    json.dump(out, open(CACHE, 'w'), indent=0, sort_keys=True)


def clean(t):
    t = re.sub(r'\bANT\b', 'Tracer', t)
    # drop credit parentheses and issue refs: "(#292; requested by ...)", "(#63)", "(#261, settles #256)"
    t = re.sub(r'\s*\((?:[^()]|\([^()]*\))*?(?:#\d+|reported|built|committed|requested|suggested|feedback)(?:[^()]|\([^()]*\))*\)', '', t)
    t = re.sub(r'\s*#\d+\b', '', t)
    t = re.sub(r'\(\s*[,;]?\s*\)', '', t)
    t = re.sub(r"\s*\((?:George|Burak|Tommaso|Bruno)[^)]*\)", '', t)
    t = re.sub(r'\s+([.,;:])(?=\s|$)', r'\1', t)
    return t.replace('**.**', '**').replace(' .**', '.**').strip()


def contributors(text, cache):
    logins = []
    for n in re.findall(r'#(\d+)', text):
        c = cache.get(n)
        if not c: continue
        for l in [c.get('creator')] + c.get('impl', []):
            if l and l not in BOTS and l not in logins: logins.append(l)
    for l in re.findall(r'https://github\.com/([A-Za-z0-9-]+)\)', text):
        if l in NAMES and l not in logins: logins.append(l)
    return logins or [DEFAULT]


def who(v, it, cache):
    return EARLY if vt(v) < (0, 7, 0) else contributors(it['text'] + ' '.join(it['sub']), cache)


def parse(changelog):
    vers, cur, item = [], None, None
    for line in open(changelog).read().splitlines():
        m = re.match(r'^## (\S+)', line)
        if m:
            cur = {'v': m.group(1), 'intro': [], 'items': []}; vers.append(cur); item = None; continue
        if cur is None: continue
        if re.match(r'^- ', line):
            item = {'text': line[2:], 'sub': []}; cur['items'].append(item)
        elif re.match(r'^\s{2,}- ', line) and item:
            item['sub'].append(line.strip()[2:])
        elif line.strip() and item and line.startswith('  '):
            item['text'] += ' ' + line.strip()
        elif line.strip() and not line.startswith('#'):
            if item: item = None
            cur['intro'].append(line.strip())
    return vers


def tag_dates(repo):
    try:
        out = subprocess.run(['git', '-C', repo, 'tag', '-l', 'v*', '--format=%(refname:short) %(creatordate:short)'],
                             capture_output=True, text=True, check=True).stdout
        return {l.split()[0][1:]: l.split()[1] for l in out.splitlines() if l.strip()}
    except Exception:
        return {}


def page(repo, released):
    changelog = os.path.join(repo, 'CHANGELOG.md')
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    dates = tag_dates(repo)
    vers = parse(changelog)
    everyone = {}
    for v in vers:
        for it in v['items']:
            for l in who(v['v'], it, cache): everyone[l] = everyone.get(l, 0) + 1
    o = ['<span class="ol-pill">Version</span>', '', '# Version history', '',
         f'<p class="lede">Every Octoloom release from the very first, newest first: what changed, in plain words, and who made it happen. '
         f'<b>{len(vers)} versions</b>, <b>{sum(len(v["items"]) for v in vers)} changes</b>.</p>', '',
         '## Contributors', '',
         'Everyone who suggested or built a change. A change counts for the person who filed the request and for the person who implemented it; '
         'a change without a request is credited to its implementer.', '',
         ' · '.join(person(l) for l, _ in sorted(everyone.items(), key=lambda x: -x[1])), '']
    for v in vers:
        tag = v['v']
        state = 'released' if tag in dates or tag == released else ('in development' if tag > released else 'released')
        meta = [dates[tag]] if tag in dates else []
        meta.append('in development' if state == 'in development' else 'released')
        o += [f'## {tag}', '', f'<span class="ol-ver-meta">{" · ".join(meta)}</span>', '']
        for p in v['intro']: o += [clean(p), '']
        if not v['items']: continue
        for it in v['items']:
            by = ', '.join(person(l) for l in who(v['v'], it, cache))
            o.append(f'- {clean(it["text"])}')
            for sub in it['sub']: o.append(f'    - {clean(sub)}')
            o += ['', f'    <span class="ol-by">:material-account-heart-outline: {by}</span>', '']
        o.append('')
    return '\n'.join(o)


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == '--refresh': refresh(os.path.join(sys.argv[2], 'CHANGELOG.md'))
