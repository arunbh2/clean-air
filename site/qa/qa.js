// Clean Air QA: accessibility (axe), internal links and anchors, functional checks,
// reflow at 320 px, print, logo transparency, page weight and external requests.
// Run after `python3 site/build.py`:  cd site/qa && npm install && node qa.js
// Writes site/qa/report/qa-report.json and qa-report.md; exits non-zero on failures.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const DIST = path.resolve(__dirname, '..', 'dist');
const OUT = path.join(__dirname, 'report'); fs.mkdirSync(OUT, { recursive: true });
const AXE = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
const pages = fs.readFileSync(path.join(DIST, 'sitemap.txt'), 'utf8').trim().split('\n');
const url = p => 'file://' + path.join(DIST, p);
const results = { axe: {}, links: [], functional: [], reflow: [], print: [], logos: [], weight: {}, external: [] };
const fail = []; const pass = (name, ok, detail = '') => { results.functional.push({ name, ok, detail }); if (!ok) fail.push(name + ': ' + detail); };

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  const ids = {};
  // 1. axe + collect links and ids
  for (const p of pages) {
    await page.goto(url(p));
    await page.addScriptTag({ content: AXE });
    const r = await page.evaluate(async () => {
      const res = await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'] } });
      return res.violations.map(v => ({ id: v.id, impact: v.impact, help: v.help, nodes: v.nodes.length, sample: v.nodes[0] && v.nodes[0].target.join(' ') }));
    });
    if (r.length) results.axe[p] = r;
    const info = await page.evaluate(() => ({
      ids: [...document.querySelectorAll('[id]')].map(e => e.id),
      links: [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')),
      res: [...document.querySelectorAll('img[src],script[src],link[href]')].map(e => e.getAttribute('src') || e.getAttribute('href')),
      cutoff: document.body.innerText.includes('22 November 2026'),
      logoName: (document.querySelector('a.brand') || {}).getAttribute ? document.querySelector('a.brand').getAttribute('aria-label') : null,
      h1: document.querySelectorAll('h1').length,
    }));
    ids[p] = new Set(info.ids);
    results[p] = info;
  }
  // 2. internal links and anchors
  for (const p of pages) {
    for (const href of results[p].links) {
      if (/^(https?:|mailto:)/.test(href)) { results.external.push(href); continue; }
      const [file, hash] = href.split('#');
      const target = file ? path.normalize(path.join(path.dirname(p), file)) : p;
      if (!fs.existsSync(path.join(DIST, target))) { results.links.push({ page: p, href, problem: 'missing file' }); continue; }
      if (hash && target.endsWith('.html')) {
        if (!ids[target]) { const h = fs.readFileSync(path.join(DIST, target), 'utf8'); ids[target] = new Set([...h.matchAll(/id="([^"]+)"/g)].map(m => m[1])); }
        if (!ids[target].has(hash)) results.links.push({ page: p, href, problem: 'missing anchor' });
      }
    }
    for (const src of results[p].res) if (/^https?:/.test(src)) results.weight.externalResources = (results.weight.externalResources || []).concat([p + ' -> ' + src]);
  }
  // 3. functional checks
  pass('every page shows the research cutoff', pages.filter(p => p !== '404.html').every(p => results[p].cutoff));
  pass('every page has exactly one h1', pages.every(p => results[p].h1 === 1), pages.filter(p => results[p].h1 !== 1).join(', '));
  pass('home logo link named "Clean Air — home"', pages.every(p => results[p].logoName === 'Clean Air — home'));
  pass('no broken internal links or anchors', results.links.length === 0, results.links.length + ' problems');
  pass('no external scripts, styles or images', !results.weight.externalResources, (results.weight.externalResources || []).slice(0, 3).join('; '));
  // filters
  await page.goto(url('what-works/index.html'));
  const csv = fs.readFileSync(path.resolve(__dirname, '..', '..', 'research', 'data', 'interventions.csv'), 'utf8');
  const fundNow = (csv.match(/,Fund now,/g) || []).length;
  await page.selectOption('select[data-key="rec"]', 'Fund now');
  const shown = await page.locator('#int-list > li:not([hidden])').count();
  pass('intervention filter shows only "Fund now" items', shown === fundNow, `${shown} shown vs ${fundNow} in CSV`);
  await page.goto(url('organisations/index.html'));
  await page.selectOption('select[data-key="fn"]', 'delivery');
  const orgShown = await page.locator('#org-table tbody tr:not([hidden])').count();
  pass('organisation filter narrows the table', orgShown > 0 && orgShown < 21, `${orgShown} rows`);
  // citations resolve
  const claimsHtml = fs.readFileSync(path.join(DIST, 'evidence/claims.html'), 'utf8');
  const claimIds = new Set([...claimsHtml.matchAll(/<tr id="(C\d{3})"/g)].map(m => m[1]));
  let cites = 0, bad = 0;
  for (const p of pages) for (const h of results[p].links) { const m = h.match(/claims\.html#(C\d{3})$/); if (m) { cites++; if (!claimIds.has(m[1])) bad++; } }
  pass('every citation resolves to a claim', bad === 0 && cites > 300, `${cites} citations, ${bad} unresolved`);
  // keyboard: first Tab reaches skip link
  await page.goto(url('index.html')); await page.keyboard.press('Tab');
  const focused = await page.evaluate(() => document.activeElement.className + '|' + document.activeElement.textContent.trim());
  pass('first Tab focuses the skip link', focused.startsWith('skip|'), focused);
  const outline = await page.evaluate(() => getComputedStyle(document.activeElement).outlineStyle);
  pass('focused element shows an outline', outline !== 'none', outline);
  // 4. reflow at 320 px (equivalent to 400% zoom on a 1280 px screen)
  const mob = await browser.newPage({ viewport: { width: 320, height: 800 } });
  for (const p of pages) {
    await mob.goto(url(p));
    const o = await mob.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    if (o > 0) results.reflow.push({ page: p, overflow: o });
  }
  pass('no horizontal page scroll at 320 px', results.reflow.length === 0, results.reflow.map(r => r.page).slice(0, 5).join(', '));
  // text zoom 200%
  await mob.setViewportSize({ width: 640, height: 900 });
  await mob.goto(url('index.html')); await mob.evaluate(() => { document.documentElement.style.fontSize = '200%'; });
  const z = await mob.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  pass('home page has no horizontal scroll with text at 200%', z <= 0, `${z}px`);
  // 5. print
  for (const p of ['support/brief.html', 'what-works/smog-towers.html', 'index.html']) {
    await page.goto(url(p)); await page.emulateMedia({ media: 'print' });
    const navHidden = await page.evaluate(() => getComputedStyle(document.querySelector('.nav')).display === 'none');
    const pdf = path.join(OUT, 'print-' + p.replace(/\//g, '_') + '.pdf');
    await page.pdf({ path: pdf, format: 'A4' }); await page.emulateMedia({ media: 'screen' });
    results.print.push({ page: p, navHidden, bytes: fs.statSync(pdf).size });
  }
  pass('print hides navigation and produces a PDF', results.print.every(r => r.navHidden && r.bytes > 10000));
  // 6. logos: vector only, transparent background
  const logoDir = path.join(DIST, 'logo');
  for (const f of fs.readdirSync(logoDir)) {
    const s = fs.readFileSync(path.join(logoDir, f), 'utf8');
    results.logos.push({ file: f, raster: /<image|data:image/.test(s), background: /<rect/.test(s) });
  }
  pass('logos are pure vector with transparent backgrounds', results.logos.every(l => !l.raster && !l.background));
  // 7. weight
  let total = 0; const walk = d => fs.readdirSync(d).forEach(f => { const q = path.join(d, f); fs.statSync(q).isDirectory() ? walk(q) : (q.endsWith('.html') || q.endsWith('.css') || q.endsWith('.js') || q.endsWith('.svg')) && (total += fs.statSync(q).size); });
  walk(DIST);
  const home = fs.statSync(path.join(DIST, 'index.html')).size + fs.statSync(path.join(DIST, 'css/site.css')).size + fs.statSync(path.join(DIST, 'js/site.js')).size + fs.statSync(path.join(DIST, 'logo/logo-horizontal.svg')).size + fs.statSync(path.join(DIST, 'logo/logo-white.svg')).size;
  results.weight.homeBytes = home; results.weight.allHtmlCssJsSvgBytes = total;
  pass('home page under 150 KB including CSS, JS and logos', home < 150000, `${Math.round(home / 1024)} KB`);
  // axe summary
  const axeCount = Object.values(results.axe).reduce((n, v) => n + v.length, 0);
  pass('no axe WCAG 2.1 A/AA violations', axeCount === 0, axeCount + ' violation types across ' + Object.keys(results.axe).length + ' pages');
  await browser.close();
  results.external = [...new Set(results.external)].length;
  pages.forEach(p => delete results[p]);
  fs.writeFileSync(path.join(OUT, 'qa-report.json'), JSON.stringify(results, null, 2));
  const md = ['# QA report', '', `Pages checked: ${pages.length}`, '', '| Check | Result | Detail |', '|---|---|---|',
    ...results.functional.map(f => `| ${f.name} | ${f.ok ? 'pass' : '**FAIL**'} | ${f.detail} |`), '',
    `External links (source URLs, verified in Phase 2): ${results.external}`, '',
    '## axe violations', '', ...(Object.keys(results.axe).length ? Object.entries(results.axe).map(([p, v]) => `- ${p}: ` + v.map(x => `${x.id} (${x.impact}, ${x.nodes} nodes, e.g. ${x.sample})`).join('; ')) : ['None.'])];
  fs.writeFileSync(path.join(OUT, 'qa-report.md'), md.join('\n') + '\n');
  console.log(md.slice(0, 30).join('\n'));
  if (fail.length) { console.log('\nFAILURES:\n' + fail.join('\n')); process.exit(1); }
})();
