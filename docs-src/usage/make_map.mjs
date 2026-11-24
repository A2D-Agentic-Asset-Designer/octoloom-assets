// Builds docs-src/usage/world.svg (one <path data-c="ISO2"> per country) from world-atlas countries-110m
// (ISC, Natural Earth public-domain data) and the ISO numeric -> alpha-2 table of i18n-iso-countries (MIT).
import fs from 'node:fs';
const [, , topoPath, codesPath, out] = process.argv;
const topo = JSON.parse(fs.readFileSync(topoPath, 'utf8'));
const codes = JSON.parse(fs.readFileSync(codesPath, 'utf8')); // [[alpha2, alpha3, numeric], ...]
const num2a2 = Object.fromEntries(codes.map(([a2, , num]) => [String(num).padStart(3, '0'), a2]));
const { scale: [sx, sy], translate: [tx, ty] } = topo.transform;
const arcs = topo.arcs.map((a) => { let x = 0, y = 0; return a.map(([dx, dy]) => [(x += dx) * sx + tx, (y += dy) * sy + ty]); });
const W = 960, H = 470; // equirectangular, latitude clipped to [-58, 84]
const P = ([lon, lat]) => [((lon + 180) / 360) * W, ((84 - Math.max(-58, Math.min(84, lat))) / 142) * H];
const ring = (ids) => { const pts = []; for (const i of ids) { const a = i < 0 ? [...arcs[~i]].reverse() : arcs[i]; pts.push(...(pts.length ? a.slice(1) : a)); } return pts; };
const d = (rings) => rings.map((r) => { const pts = ring(r).map(P); let s = '', last = null;
  let px = null;
  for (const [x, y] of pts) { const k = `${x.toFixed(1)},${y.toFixed(1)}`; if (k === last) continue;
    // A ring that crosses the antimeridian jumps across the map: start a new subpath instead of a streak.
    s += (s && Math.abs(x - px) < W / 2 ? 'L' : 'M') + k; last = k; px = x; } return s + 'Z'; }).join('');
const paths = [];
for (const g of topo.objects.countries.geometries) {
  if (!g.type) continue;
  const polys = g.type === 'Polygon' ? [g.arcs] : g.arcs;
  const a2 = num2a2[String(g.id).padStart(3, '0')] ?? '';
  if (g.properties?.name === 'Antarctica') continue;
  paths.push(`<path data-c="${a2}"${a2 ? '' : ' class="nc"'} d="${polys.map(d).join('')}"><title>${(g.properties?.name ?? '').replace(/[<&"]/g, '')}</title></path>`);
}
fs.writeFileSync(out, `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" class="ol-map" role="img" aria-label="World map of Octoloom users by country">\n<!-- Countries: Natural Earth 1:110m (public domain) via world-atlas 2.0.2 (ISC, Mike Bostock); ISO codes: i18n-iso-countries (MIT). Generated for octoloom#334. -->\n${paths.join('\n')}\n</svg>\n`);
console.log('countries', paths.length, 'bytes', fs.statSync(out).size);
