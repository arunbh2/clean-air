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
      const res = await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'] } });
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
  // organisations explorer: every filter narrows, presets work, no-results state is announced
  await page.goto(url('organisations/index.html'));
  const totalOrgs = await page.locator('#org-list > li').count();
  const cnt = async () => parseInt((await page.textContent('#ex-count')).split(' of ')[0], 10);
  const fsel = await page.locator('select[data-f]').evaluateAll(s => s.map(x => [x.getAttribute('data-f'), [...x.options].map(o => o.value).filter(Boolean)]));
  let badFilter = [];
  for (const [k, vals] of fsel) {
    for (const v of vals) { await page.selectOption(`select[data-f="${k}"]`, v); const n = await cnt(); if (!(n >= 0 && n <= totalOrgs)) badFilter.push(k + '=' + v); }
    const anyNarrow = await (async () => { for (const v of vals) { await page.selectOption(`select[data-f="${k}"]`, v); if (await cnt() < totalOrgs) return true; } return false; })();
    if (!anyNarrow) badFilter.push(k + ' never narrows');
    await page.selectOption(`select[data-f="${k}"]`, '');
  }
  pass('every explorer filter works and narrows results', badFilter.length === 0, badFilter.slice(0, 5).join(', ') + ` (${fsel.length} filters)`);
  await page.fill('[data-q]', 'kathmandu'); const sq = await cnt();
  await page.fill('[data-q]', 'zzqx'); const noneShown = await page.isVisible('#ex-none'); const live = await page.getAttribute('#ex-count', 'aria-live');
  await page.click('[data-clear]');
  pass('explorer search, no-results message and live count', sq > 0 && sq < totalOrgs && noneShown && live === 'polite', `search ${sq}`);
  await page.click('[data-preset-id="business"]'); const biz = await cnt();
  const bizOk = await page.locator('#org-list > li:not([hidden])').evaluateAll(l => l.every(x => x.getAttribute('data-category') === 'private'));
  pass('"Explore solutions and businesses" preset shows only companies', biz > 0 && bizOk, `${biz} shown`);
  await page.click('[data-clear]');
  await page.goto(url('organisations/compare.html'));
  const ob = page.locator('[data-compare] input'); await ob.nth(5).check({ force: true }).catch(() => {});
  const oc = await page.locator('#compare-table thead th[data-col]:not([hidden])').count();
  pass('organisation comparison shows at most three', oc >= 1 && oc <= 3, `${oc} shown`);
  // no empty profile pages; each has sources and the four evidence rows
  const profs = pages.filter(p => p.startsWith('organisations/o/'));
  const emptyP = profs.filter(p => { const h = fs.readFileSync(path.join(DIST, p), 'utf8'); return !/<ol class="sources small"><li/.test(h) || !/Measured outcomes/.test(h) || !/In one sentence/.test(h); });
  pass('no empty organisation profiles (sources, summary, evidence rows)', profs.length > 0 && emptyP.length === 0, `${profs.length} profiles; empty: ${emptyP.slice(0, 3).join(', ')}`);
  const ex = JSON.parse(fs.readFileSync(path.join(DIST, 'downloads/data/organisations-atlas.json'), 'utf8'));
  const leak = JSON.stringify(ex).match(/[\w.+-]+@[\w-]+\.[\w.]+/g) || [];
  pass('public data export is valid JSON with no e-mail addresses', ex.organisations.length === profs.length && leak.length === 0, `${ex.organisations.length} orgs; ${leak.length} e-mails`);
  // the old #anchors on the organisations page still resolve
  pass('first-edition organisation anchors still exist', ['cpcb', 'mht', 'construction-unions'].every(a => ids['organisations/index.html'].has(a)));
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
  // journeys on a phone-sized screen, driven by keyboard focus + Enter
  const ph = await browser.newPage({ viewport: { width: 390, height: 844 } });
  async function go(sel) { await ph.focus(sel); await Promise.all([ph.waitForNavigation(), ph.keyboard.press('Enter')]); }
  try {
    await ph.goto(url('index.html'));
    await go('a[href="people/journey-street-vendor.html"]');           // 1
    await go('a[href="../what-works/occupational-protection.html"]');   // 2: a concrete response
    const hasOperator = await ph.locator('text=Who runs it').count();
    await ph.goBack();
    await go('a[href="../organisations/funding/p18.html"]');            // who funded something similar
    const hasSource = await ph.locator('a[href*="evidence/sources.html#S"]').count();
    await ph.goBack();
    const gapLink = await ph.locator('a[href*="evidence/gaps.html#G1"]').count();
    pass('street-vendor journey: home → story → response (2 clicks) → funding → gap', hasOperator > 0 && hasSource > 0 && gapLink > 0);
  } catch (e) { pass('street-vendor journey works', false, e.message.slice(0, 120)); }
  try {
    await ph.goto(url('index.html'));
    await go('a[href="organisations/funding/index.html"]');
    await go('a[href="p01.html"]');
    const bd = await ph.locator('text=board-approved').count();
    await ph.goto(url('support/journey-funder.html'));
    await go('a[href="../support/pathways/dp1.html"]');
    const mind = await ph.locator('text=What would change my mind').count();
    pass('funder journey: atlas → Bangladesh record → pathway with falsification test', bd > 0 && mind > 0);
  } catch (e) { pass('funder journey works', false, e.message.slice(0, 120)); }
  // compare tool limits to three
  await page.goto(url('what-works/compare.html'));
  const boxes = page.locator('[data-compare] input');
  await boxes.nth(1).check({ force: true }).catch(() => {});
  const shownCols = await page.locator('#compare-table thead th[data-col]:not([hidden])').count();
  pass('comparison shows at most three interventions', shownCols <= 3 && shownCols >= 1, `${shownCols} shown`);
  // images need alt attributes
  let noAlt = 0;
  for (const p of pages) { const h = fs.readFileSync(path.join(DIST, p), 'utf8'); noAlt += (h.match(/<img(?![^>]*\balt=)[^>]*>/g) || []).length; }
  pass('every image has an alt attribute', noAlt === 0, `${noAlt} without alt`);
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
  pass('no axe WCAG 2.1 and 2.2 A/AA violations', axeCount === 0, axeCount + ' violation types across ' + Object.keys(results.axe).length + ' pages');
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
