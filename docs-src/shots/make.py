#!/usr/bin/env python3
"""Screenshots for the docs site (octoloom#301): renders Octoloom webviews with fake data (the
octoloom-screenshot specs of the Octoloom repo), numbers every control that has a tooltip and crops
the canvas cards. Output: docs-src/img/ui/*.webp + *.json (read by build_docs.py).

Usage: python3 docs-src/shots/make.py <octoloom repo>   (run `npm run build` there first; needs Chrome + Pillow)
"""
import html as H, json, os, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

REPO = os.path.abspath(sys.argv[1])
HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(os.path.dirname(HERE), 'img', 'ui')
TMP = '/tmp/octo-docs-shots'
SPECS = os.path.join(REPO, '.claude', 'skills', 'octoloom-screenshot', 'specs')
CH = os.environ.get('CHROME', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')

# spec name -> annotate? (numbered controls)
SHOTS = {
    'welcome': 1, 'welcome-update': 0, 'coverage-map': 1,
    'new-project': 1, 'new-project-readme': 0, 'new-project-blank': 0, 'new-project-idmc': 0,
    'exchange-import': 1, 'projects-new-exchange': 0,
    'projects-deploy': 1, 'deploy-form': 1, 'deploy-auth': 0, 'run-local-vars': 0, 'projects-explain': 0,
    'setup-connect': 1, 'setup-connect-update': 0, 'setup-connect-idmc': 0,
    'assets-llm': 1, 'assets-a2d-llm': 0, 'assets-idmc': 0, 'assets-error-detail': 0, 'assets-idmc-hdm': 0,
    'network-v2': 1, 'network-v1': 1, 'network-v2-context': 0, 'broker-protected': 0, 'policies-fold': 0, 'policy-picker': 0,
    'network-problems-fix': 0, 'network-v1-exchange-llm': 0, 'network-mcp-url': 0, 'network-fab-tip': 0,
    'agent-flow': 1, 'agent-patterns': 0,
    'code-yaml': 1, 'code-find': 0,
    'exchange-locked': 1, 'exchange-unlocked': 0,
    'chat-progress': 1, 'chat-auth': 0, 'chat-network': 0, 'chat-network-sequence': 0, 'chat-trace': 1, 'chat-trace-colors': 0,
    'chat-share-a2d': 0, 'chat-share-web': 0, 'chat-share-a2d-review': 0, 'chat-narrow': 0,
    'tracer': 1, 'tracer-mini': 0,
    'governance': 1, 'governance-fix-all': 0,
    'explain-anything': 0, 'explain-guide': 0, 'explain-docs': 0,
}
# Quick Starts (docs only): the onboarding tab at each journey step after the four prerequisites
SHOTS.update({f'qs-{j}-{k}': 0 for j, n in (('beginner', 9), ('advanced', 10), ('expert', 11)) for k in range(4, n)})
# canvas card crops: (spec, css selector, output name)
CROPS = [
    ('network-v2', '.nc.k-broker', 'card-broker'), ('network-v2', '.nc.k-agent', 'card-agent'),
    ('network-v2', '.nc.k-mcp', 'card-mcp'), ('network-v2', '.nc.k-llm', 'card-llm'),
    ('policies-fold', '.inspector', 'card-policy'),
    ('agent-flow', '.nc.k-trigger', 'card-trigger'), ('agent-flow', '.nc.k-generator', 'card-generator'),
    ('agent-flow', '.nc.k-subagent', 'card-subagent'), ('agent-flow', '.nc.k-router', 'card-router'),
    ('agent-flow', '.nc.k-executor', 'card-executor'), ('agent-flow', '.nc.k-echo', 'card-echo'),
    ('agent-flow', '.explorer', 'flow-explorer'), ('network-v2', '.topbar', 'toolbar-network'),
    ('agent-flow', '.topbar', 'toolbar-flow'), ('network-v2', '.fab-col', 'canvas-fabs'),
    ('network-v2', '.problems', 'problems-bar'), ('network-v2', '.xb-btn', 'explain-button'),
]

BOTTOM = {'.xb-btn', '.problems'}

PROBE = r"""()=>{
 const W=innerWidth,Hh=innerHeight, out=[], seen=new Set();
 const skip=/\b(nc-chip|nc-pill|ctr-row|ctr-span|nc-tile|nc-eye|nc-sec-fold|nc-ok|nc-fw|nc-model|nc-edit-btn|chat-split|mc-item|tracer-row|port|ex-item)\b/;
 for (const e of document.querySelectorAll('button,[role=button],[title],[data-explain],.seg > *')) {
   const r=e.getBoundingClientRect(); if (r.width<6||r.height<6||r.x<0||r.y<0||r.x>W-4||r.y>Hh-4) continue;
   const cls=(e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className)||'';
   if (skip.test(cls)) continue;
   if (e.tagName==='DIV' && /\bnc\b/.test(cls)) continue;
   if (!['BUTTON','A','LABEL'].includes(e.tagName) && !/btn|chip|fab|seg|tab|dot|pill/.test(cls) && !e.closest('.seg')) continue;
   const st=getComputedStyle(e); if (st.visibility==='hidden'||+st.opacity===0) continue;
   let t=(e.getAttribute('title')||e.getAttribute('aria-label')||'').trim(); const txt=(e.textContent||'').replace(/\s+/g,' ').trim();
   if (!t && !txt) continue; if (txt.length>40 && !t) continue;
   const key=(t||txt).split('\n')[0]; if (seen.has(key)) continue; seen.add(key);
   out.push({t, txt: txt.slice(0,40), x:r.x, y:r.y, w:r.width, h:r.height});
 }
 const crops={}; for (const s of SELS) { const e=document.querySelector(s); if (e){const r=e.getBoundingClientRect(); crops[s]=[r.x,r.y,r.width,r.height];} }
 return {W, H:Hh, controls: out, crops};
}"""


def dump(name, size, sels, extra=0):
    page = os.path.join(TMP, f'{name}-light.html')
    if not os.path.exists(page): page = os.path.join(TMP, f'{name}.html')
    w, h = size.split(',')
    size = f'{w},{int(h) + extra}'
    src = open(page).read()
    js = PROBE.replace('SELS', json.dumps(sels))
    inj = ("<script>setTimeout(()=>{let r;try{r=(" + js + ")()}catch(e){r={err:String(e)}}"
           "const p=document.createElement('pre');p.id='__out';p.textContent=JSON.stringify(r);document.body.appendChild(p)},2600)</script></body>")
    probe = page.replace('.html', '.probe.html'); open(probe, 'w').write(src.replace('</body>', inj))
    out = subprocess.run([CH, '--headless=new', '--disable-gpu', '--allow-file-access-from-files', '--hide-scrollbars',
                          f'--window-size={size}', '--virtual-time-budget=6000', '--dump-dom', 'file://' + probe],
                         capture_output=True, text=True, timeout=120).stdout
    m = re.search(r'<pre id="__out">(.*?)</pre>', out, re.S)
    r = json.loads(H.unescape(m.group(1))) if m else None
    want = int(h)
    if r and 'H' in r and r['H'] != want and extra == 0:  # dump-dom's viewport is shorter than --screenshot's
        r2 = dump(name, f'{w},{h}', sels, want - r['H'])
        # the controls line up with the taller probe, but the canvas cards are fitted to the first layout
        # pass (the same one the screenshot draws them in), so the card crops keep the first probe's rects
        # the floating, bottom-anchored parts (Explain button, problems bar) follow the taller viewport
        if r2: r2['crops'] = {k: (v if k in BOTTOM else r.get('crops', {}).get(k, v)) for k, v in r2.get('crops', {}).items()}
        return r2
    return r


def font(sz):
    for f in ('/System/Library/Fonts/SFNSRounded.ttf', '/System/Library/Fonts/Helvetica.ttc', '/Library/Fonts/Arial Bold.ttf'):
        if os.path.exists(f):
            try: return ImageFont.truetype(f, sz)
            except Exception: pass
    return ImageFont.load_default()


def save(im, path, maxw=1800):
    if im.width > maxw: im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    im.convert('RGB').save(path, 'WEBP', quality=86, method=6)


def annotate(png, controls, scale, out):
    im = Image.open(png).convert('RGB'); d = ImageDraw.Draw(im); f = font(int(11 * scale))
    rad = int(9 * scale); placed = []
    for i, c in enumerate(controls, 1):
        cx = (c['x'] + c['w']) * scale - rad * 0.4; cy = c['y'] * scale + rad * 0.4
        cx = min(max(cx, rad + 2), im.width - rad - 2); cy = min(max(cy, rad + 2), im.height - rad - 2)
        for (px, py) in placed:
            if abs(px - cx) < rad * 1.9 and abs(py - cy) < rad * 1.9: cy += rad * 2.0
        placed.append((cx, cy))
        d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(2, 42, 192), outline=(255, 255, 255), width=max(2, int(scale)))
        s = str(i); tw = d.textlength(s, font=f)
        d.text((cx - tw / 2, cy - rad * 0.62), s, fill='white', font=f)
    save(im, out)


def main():
    os.makedirs(OUTDIR, exist_ok=True); os.makedirs(TMP, exist_ok=True)
    only = set(filter(None, os.environ.get('ONLY', '').split(',')))  # ONLY=a,b re-renders just these views
    todo = {n: a for n, a in SHOTS.items() if not only or n in only}
    specs = []
    for n in todo:  # every view in both themes
        own = os.path.join(HERE, 'specs', f'{n}.json')  # docs-only specs (no change in the extension repo)
        sp = json.load(open(own if os.path.exists(own) else os.path.join(SPECS, f'{n}.json'))); sp['themes'] = ['dark', 'light']
        if sp.get('messagesFile'): sp['messagesFile'] = os.path.join(SPECS, sp['messagesFile'])
        f = os.path.join(TMP, f'spec-{n}.json'); json.dump(sp, open(f, 'w')); specs.append(f)
    subprocess.run(['node', '.claude/skills/octoloom-screenshot/shot.mjs', *specs], cwd=REPO, check=True,
                   env={**os.environ, 'OUT': TMP}, stdout=subprocess.DEVNULL)
    idx = os.path.join(OUTDIR, 'index.json')
    index = json.load(open(idx)) if only and os.path.exists(idx) else {}
    for n, ann in todo.items():
        spec = json.load(open(os.path.join(TMP, f'spec-{n}.json')))
        size = spec.get('size') or '1500,900'
        themes = spec.get('themes') or ['dark']
        sels = sorted({s for (sp, s, _) in CROPS if sp == n})
        info = dump(n, size, sels) if (ann or sels) else None
        entry = {'size': size, 'themes': themes}
        for th in themes:
            png = os.path.join(TMP, f'{n}-{th}.png' if len(themes) > 1 else f'{n}.png')
            save(Image.open(png), os.path.join(OUTDIR, f'{n}-{th}.webp'))
            if ann and info and info.get('controls'):
                ctl = info['controls'][:28]
                scale = Image.open(png).width / info['W']
                if abs(Image.open(png).height / scale - info['H']) > 2: print('  viewport mismatch', n, info['H'])
                annotate(png, ctl, scale, os.path.join(OUTDIR, f'{n}-annot-{th}.webp'))
                entry['controls'] = [{'n': i, 'title': c['t'], 'text': c['txt']} for i, c in enumerate(ctl, 1)]
            if info and info.get('crops'):
                for (sp, sel, cname) in CROPS:
                    if sp != n or sel not in info['crops']: continue
                    x, y, w, h = info['crops'][sel]; im = Image.open(png); sc = im.width / info['W']; pad = 8
                    box = (max(0, int((x - pad) * sc)), max(0, int((y - pad) * sc)), min(im.width, int((x + w + pad) * sc)), min(im.height, int((y + h + pad) * sc)))
                    save(im.crop(box), os.path.join(OUTDIR, f'{cname}-{th}.webp'), maxw=1200)
        index[n] = entry
        print(n, len(entry.get('controls', [])), 'controls')
    index = {n: index[n] for n in SHOTS if n in index}
    json.dump(index, open(idx, 'w'), indent=1, ensure_ascii=False)


main()
