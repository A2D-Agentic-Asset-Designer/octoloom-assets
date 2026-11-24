// Template filters on the catalog page (octoloom#322): the same Level / Industry / Needs / Time chips as the
// New Project dialog. Facets are baked into #ol-tf by build_docs.py; cards and table rows are matched by link.
(function () {
  function init() {
    var box = document.getElementById('ol-tf');
    if (!box || box.dataset.ready) return;
    box.dataset.ready = '1';
    var labels = JSON.parse(box.dataset.labels), facets = JSON.parse(box.dataset.facets);
    var keys = ['level', 'industry', 'needs', 'time'], sel = {};
    var idOf = function (el) {
      var a = el.querySelector('a[href]');
      if (!a) return null;
      var m = a.getAttribute('href').replace(/\/?(index\.html)?(#.*)?$/, '').match(/([\w-]+?)(?:\.html|\.md)?$/);
      return m && facets[m[1]] ? m[1] : null;
    };
    var items = [];
    document.querySelectorAll('.md-content .grid.cards > ul > li, .md-content table tbody tr').forEach(function (el) {
      var id = idOf(el);
      if (id) items.push({ el: el, id: id });
    });
    var ids = Object.keys(facets);
    var match = function (id, skip) {
      return keys.every(function (k) { return k === skip || !sel[k] || facets[id][k].indexOf(sel[k]) >= 0; });
    };
    var status = document.createElement('p');
    status.className = 'ol-tf-status';
    status.setAttribute('aria-live', 'polite');
    function render() {
      while (box.firstChild) box.removeChild(box.firstChild);
      keys.forEach(function (k) {
        var counts = {};
        ids.forEach(function (id) { if (match(id, k)) facets[id][k].forEach(function (v) { counts[v] = (counts[v] || 0) + 1; }); });
        var row = document.createElement('div');
        row.className = 'ol-tf-row';
        row.setAttribute('role', 'group');
        row.setAttribute('aria-label', labels[k][0]);
        var l = document.createElement('span');
        l.className = 'ol-tf-label';
        l.textContent = labels[k][0];
        row.appendChild(l);
        var chips = document.createElement('span');
        chips.className = 'ol-tf-chips';
        row.appendChild(chips);
        labels[k][1].forEach(function (o) {
          if (!counts[o[0]] && sel[k] !== o[0]) return;
          var b = document.createElement('button');
          b.type = 'button';
          b.className = 'ol-tf-chip' + (sel[k] === o[0] ? ' on' : '');
          b.setAttribute('aria-pressed', sel[k] === o[0] ? 'true' : 'false');
          b.textContent = o[1] + ' ';
          var n = document.createElement('span');
          n.className = 'ol-tf-n';
          n.textContent = String(counts[o[0]] || 0);
          b.appendChild(n);
          b.addEventListener('click', function () { sel[k] = sel[k] === o[0] ? undefined : o[0]; render(); });
          chips.appendChild(b);
        });
        box.appendChild(row);
      });
      var any = keys.some(function (k) { return sel[k]; });
      var shown = ids.filter(function (id) { return match(id); }).length;
      items.forEach(function (it) { it.el.hidden = !match(it.id); });
      status.textContent = any ? shown + ' of ' + ids.length + ' templates match. ' : '';
      if (any) {
        var c = document.createElement('button');
        c.type = 'button';
        c.className = 'ol-tf-clear';
        c.textContent = 'Clear filters';
        c.addEventListener('click', function () { sel = {}; render(); });
        status.appendChild(c);
      }
      box.appendChild(status);
    }
    render();
  }
  if (window.document$ && window.document$.subscribe) window.document$.subscribe(init);
  else document.addEventListener('DOMContentLoaded', init);
})();
