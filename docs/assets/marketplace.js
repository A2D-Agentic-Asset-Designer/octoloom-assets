// Live VS Code Marketplace numbers for the docs (octoloom#301). Falls back to the numbers baked in at build time.
(function () {
  var ID = 'octoloom.octoloom';
  var MARKET = 'https://marketplace.visualstudio.com/items?itemName=' + ID;
  function fmt(n) { return Math.round(n).toLocaleString('en-US'); }
  function paint(s) {
    document.querySelectorAll('.ol-installs').forEach(function (e) { if (s.install) e.textContent = fmt(s.install); });
    document.querySelectorAll('.ol-rating').forEach(function (e) { if (s.averagerating) e.textContent = s.averagerating.toFixed(1); });
    document.querySelectorAll('.ol-ratings').forEach(function (e) { if (s.ratingcount) e.textContent = fmt(s.ratingcount); });
    document.querySelectorAll('.ol-version').forEach(function (e) { if (s.version) e.textContent = s.version; });
  }
  function pill() {
    var inner = document.querySelector('.md-header__inner');
    if (!inner || inner.querySelector('.ol-mk')) return;
    var a = document.createElement('a');
    a.className = 'ol-mk'; a.href = MARKET; a.title = 'Octoloom on the VS Code Marketplace';
    a.innerHTML = '<span class="ol-mk-l">Marketplace</span><span class="ol-mk-v"><span class="ol-installs">' +
      (document.querySelector('.ol-installs') ? document.querySelector('.ol-installs').dataset.fallback : '') + '</span> installs</span>';
    var search = inner.querySelector('.md-search');
    inner.insertBefore(a, search);
  }
  var cache = null;
  function load() {
    pill();
    if (cache) return paint(cache);
    try {
      var c = JSON.parse(sessionStorage.getItem('ol-mk') || 'null');
      if (c && Date.now() - c.at < 3600e3) { cache = c; return paint(c); }
    } catch (e) {}
    fetch('https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json;api-version=3.0-preview.1' },
      body: JSON.stringify({ filters: [{ criteria: [{ filterType: 7, value: ID }] }], flags: 914 })
    }).then(function (r) { return r.json(); }).then(function (d) {
      var x = d.results[0].extensions[0], s = { at: Date.now(), version: x.versions[0].version };
      x.statistics.forEach(function (t) { s[t.statisticName] = t.value; });
      cache = s; try { sessionStorage.setItem('ol-mk', JSON.stringify(s)); } catch (e) {}
      paint(s);
    }).catch(function () {});
  }
  if (window.document$) window.document$.subscribe(load); else document.addEventListener('DOMContentLoaded', load);
})();
