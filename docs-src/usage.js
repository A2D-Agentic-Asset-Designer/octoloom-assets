// Usage page of the docs site (octoloom#334). Reads assets/usage.json (aggregates only, k >= 5, written by the
// usage Action, octoloom#333) and paints stat cards, the world map, bars and the weekly trend.
// No third-party code, no tracking, no cookies. All labels go in with textContent.
(function () {
  var NAMES = {
    'agentNetwork.build': 'Build', 'agentNetwork.deploy': 'Deploy', 'agentNetwork.publish': 'Publish', 'agentNetwork.validate': 'Validate',
    'agentNetwork.newProject': 'New project', 'agentNetwork.openChat': 'Chat', 'agentNetwork.governance': 'Governance',
    'agentNetwork.governanceReport': 'Governance report', 'agentNetwork.coverageMap': 'Coverage map', 'agentNetwork.runLocal': 'Run locally',
    'agentNetwork.quickStart': 'Quick Start', 'agentNetwork.welcome': 'Home', 'agentNetwork.openFromExchange': 'Open from Exchange',
    'agentNetwork.openVisual': 'Open canvas', 'agentNetwork.openText': 'Open as text', 'agentNetwork.undeploy': 'Undeploy',
    'agentNetwork.unpublish': 'Unpublish', 'agentNetwork.status': 'Deployment status', 'agentNetwork.checkGateway': 'Check gateway',
  };
  var CONN = { anypoint: 'Agent Fabric', a2d: 'A²D', p4a: 'P4A', idmc: 'Headless IDMC' };
  function fmt(n) { return n === null || n === undefined ? '–' : Math.round(n).toLocaleString('en-US'); }
  function get(o, p) { return p.split('.').reduce(function (a, k) { return a == null ? a : a[k]; }, o); }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined) e.textContent = text; return e; }
  function label(id) { return NAMES[id] || id.replace(/^agentNetwork\./, '').replace(/([a-z])([A-Z])/g, '$1 $2').replace(/^./, function (c) { return c.toUpperCase(); }); }

  var tip;
  function bindTip(node, text) {
    node.setAttribute('tabindex', '0');
    node.setAttribute('aria-label', text);
    function show(ev) {
      tip.textContent = text; tip.hidden = false;
      var r = node.getBoundingClientRect(), x = ev && ev.clientX !== undefined ? ev.clientX : r.left + r.width / 2, y = ev && ev.clientY !== undefined ? ev.clientY : r.top;
      tip.style.left = Math.min(window.innerWidth - 220, x + 12) + 'px'; tip.style.top = (y + 14) + 'px';
    }
    node.addEventListener('pointermove', show); node.addEventListener('focus', show);
    node.addEventListener('pointerleave', function () { tip.hidden = true; }); node.addEventListener('blur', function () { tip.hidden = true; });
  }

  function bars(host, rows) {
    host.textContent = '';
    if (!rows.length) { host.appendChild(el('p', 'ol-u-none', 'No group of at least 5 machines yet.')); return; }
    var max = Math.max.apply(null, rows.map(function (r) { return r.value; })) || 1;
    rows.forEach(function (r) {
      var row = el('div', 'ol-u-bar');
      row.appendChild(el('span', 'ol-u-bar-l', r.label));
      var track = el('span', 'ol-u-bar-t'); var fill = el('i'); fill.style.width = Math.max(1.5, (r.value / max) * 100) + '%'; track.appendChild(fill);
      row.appendChild(track);
      row.appendChild(el('b', 'ol-u-bar-v', fmt(r.value)));
      bindTip(row, r.label + ': ' + fmt(r.value) + (r.unit ? ' ' + r.unit : ''));
      host.appendChild(row);
    });
  }

  function map(root, countries) {
    var svg = root.querySelector('.ol-map'); if (!svg) return;
    var by = {}; var max = 0;
    countries.forEach(function (c) { if (c.code !== 'Other') { by[c.code] = c; max = Math.max(max, c.machines); } });
    svg.querySelectorAll('path[data-c]').forEach(function (p) {
      var c = by[p.getAttribute('data-c')];
      var t = p.querySelector('title'); var name = t ? t.textContent : p.getAttribute('data-c');
      if (c) {
        var step = Math.min(4, Math.floor((Math.log(c.machines) / Math.log(Math.max(max, 2))) * 5 - 0.0001));
        p.setAttribute('class', 'ol-c' + Math.max(0, step));
        if (t) t.textContent = name + ': ' + fmt(c.machines) + ' machines';
        bindTip(p, name + ': ' + fmt(c.machines) + ' machines');
      }
    });
  }

  function table(root, key, rows) {
    var tb = root.querySelector('[data-u-table="' + key + '"] tbody'); if (!tb) return;
    tb.textContent = '';
    rows.forEach(function (cells) { var tr = el('tr'); cells.forEach(function (c) { tr.appendChild(el('td', '', c)); }); tb.appendChild(tr); });
    tb.parentNode.hidden = !rows.length;
  }

  function trend(host, rows) {
    host.textContent = '';
    if (rows.length < 2) { host.appendChild(el('p', 'ol-u-none', 'The trend appears after two weeks of data.')); return; }
    var NS = 'http://www.w3.org/2000/svg', W = 640, H = 160, P = 28;
    var svg = document.createElementNS(NS, 'svg'); svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H); svg.setAttribute('class', 'ol-u-line');
    svg.setAttribute('role', 'img'); svg.setAttribute('aria-label', 'Active machines per week');
    var max = Math.max.apply(null, rows.map(function (r) { return r.active; })) || 1;
    var x = function (i) { return P + (i * (W - 2 * P)) / (rows.length - 1); }, y = function (v) { return H - P - (v / max) * (H - 2 * P); };
    var base = document.createElementNS(NS, 'line'); base.setAttribute('x1', P); base.setAttribute('x2', W - P); base.setAttribute('y1', H - P); base.setAttribute('y2', H - P); base.setAttribute('class', 'ol-u-axis'); svg.appendChild(base);
    var path = document.createElementNS(NS, 'path');
    path.setAttribute('d', rows.map(function (r, i) { return (i ? 'L' : 'M') + x(i).toFixed(1) + ',' + y(r.active).toFixed(1); }).join(''));
    svg.appendChild(path);
    rows.forEach(function (r, i) {
      var hit = document.createElementNS(NS, 'rect'); var w = (W - 2 * P) / Math.max(1, rows.length - 1);
      hit.setAttribute('x', x(i) - w / 2); hit.setAttribute('y', 0); hit.setAttribute('width', w); hit.setAttribute('height', H); hit.setAttribute('class', 'ol-u-hit');
      svg.appendChild(hit);
      bindTip(hit, 'Week of ' + r.week + ': ' + fmt(r.active) + ' active machines');
    });
    var last = rows[rows.length - 1];
    var lbl = document.createElementNS(NS, 'text'); lbl.setAttribute('x', x(rows.length - 1) - 4); lbl.setAttribute('y', y(last.active) - 8); lbl.setAttribute('text-anchor', 'end'); lbl.textContent = fmt(last.active);
    svg.appendChild(lbl);
    host.appendChild(svg);
  }

  function paint(root, u) {
    tip = root.querySelector('.ol-u-tip');
    var empty = !u || u.empty;
    root.querySelector('.ol-u-empty').hidden = !empty;
    root.classList.toggle('is-empty', !!empty);
    if (!u) return;
    var v = {
      active: u.totals.active, events: u.totals.events, styles: u.styles,
      build: { withPolicies: ((get(u, 'styles.build.v1.withPolicies') || 0) + (get(u, 'styles.build.v2.withPolicies') || 0)) || null,
               governed: ((get(u, 'styles.build.v1.governed') || 0) + (get(u, 'styles.build.v2.governed') || 0)) || null },
      refreshed: new Date(u.refreshed).toISOString().slice(0, 10),
    };
    root.querySelectorAll('[data-u]').forEach(function (e) { var x = get(v, e.getAttribute('data-u')); e.textContent = typeof x === 'string' ? x : fmt(x); });
    map(root, u.countries || []);
    table(root, 'countries', (u.countries || []).map(function (c) { return [c.name || c.code, fmt(c.machines)]; }));
    bars(root.querySelector('[data-u-bars="features"]'), (u.features || []).slice(0, 12).map(function (f) { return { label: f.id === 'Other' ? 'Other' : label(f.id), value: f.machines, unit: 'machines' }; }));
    bars(root.querySelector('[data-u-bars="templates"]'), (u.templates || []).slice(0, 12).map(function (t) { return { label: t.template + (t.style === 'other' ? '' : ' (' + t.style + ')'), value: t.uses, unit: 'projects' }; }));
    var cm = (u.connections || {}).machines || 0;
    bars(root.querySelector('[data-u-bars="connections"]'), Object.keys(CONN).filter(function (k) { return u.connections && u.connections[k] != null; }).map(function (k) { return { label: CONN[k], value: u.connections[k], unit: 'of ' + fmt(cm) + ' machines' }; }));
    trend(root.querySelector('[data-u-trend]'), u.trends || []);
    table(root, 'trends', (u.trends || []).map(function (t) { return [t.week, fmt(t.active), fmt(t.build), fmt(t.deploy), fmt(t.create)]; }));
  }

  function load() {
    var root = document.getElementById('ol-usage'); if (!root) return;
    // usage.json sits next to this script (docs/assets), whatever the page depth.
    var me = document.querySelector('script[src*="assets/usage.js"]');
    var url = new URL('usage.json', me ? me.src : location.href);
    fetch(url.href, { cache: 'no-cache' }).then(function (r) { return r.ok ? r.json() : null; }).then(function (u) { paint(root, u); }).catch(function () { paint(root, null); });
  }
  if (window.document$) window.document$.subscribe(load); else document.addEventListener('DOMContentLoaded', load);
})();
