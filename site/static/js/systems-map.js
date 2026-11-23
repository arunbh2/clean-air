// The web of dirty air: progressive enhancement for the systems map and guided journeys.
// Without this file the diagram shows the whole web and every box and arrow links to "Every link as text".
// Loaded only on systems-map pages, so the rest of the site is unaffected.
(function () {
  'use strict';
  // ---------- guided journeys: one step at a time ----------
  var jlist = document.querySelector('[data-journey]');
  if (jlist) {
    var steps = Array.prototype.slice.call(jlist.querySelectorAll('.j-step'));
    var nav = document.querySelector('[data-journey-nav]'), cur = 0, all = false;
    var count = nav.querySelector('[data-jcount]');
    function showStep() {
      steps.forEach(function (s, i) { s.hidden = !all && i !== cur; });
      count.textContent = all ? 'All ' + steps.length + ' steps' : 'Step ' + (cur + 1) + ' of ' + steps.length;
      nav.querySelector('[data-jprev]').disabled = all || cur === 0;
      nav.querySelector('[data-jnext]').disabled = all || cur === steps.length - 1;
      nav.querySelector('[data-jall]').textContent = all ? 'One step at a time' : 'Show all steps';
    }
    nav.hidden = false;
    nav.querySelector('[data-jprev]').addEventListener('click', function () { if (cur > 0) { cur--; showStep(); steps[cur].querySelector('h2').focus(); } });
    nav.querySelector('[data-jnext]').addEventListener('click', function () { if (cur < steps.length - 1) { cur++; showStep(); steps[cur].querySelector('h2').focus(); } });
    nav.querySelector('[data-jall]').addEventListener('click', function () { all = !all; showStep(); });
    steps.forEach(function (s) { s.querySelector('h2').setAttribute('tabindex', '-1'); });
    showStep();
  }

  // ---------- the map ----------
  var dataEl = document.getElementById('map-data');
  if (!dataEl) return;
  var D = JSON.parse(dataEl.textContent);
  var svg = document.querySelector('.map-svg'), panel = document.getElementById('map-panel');
  var vp = document.querySelector('[data-viewport]'), ctl = document.querySelector('[data-map-controls]');
  var N = {}, E = {}, L = {}, LV = {};
  D.nodes.forEach(function (n) { N[n.node_id] = n; });
  D.edges.forEach(function (e) { E[e.edge_id] = e; });
  D.loops.forEach(function (l) { L[l.loop_id] = l; });
  D.levers.forEach(function (l) { LV[l.lever_id] = l; });
  var nodeEls = {}, edgeEls = {};
  svg.querySelectorAll('.node').forEach(function (el) { nodeEls[el.getAttribute('data-id')] = el; });
  svg.querySelectorAll('.edge').forEach(function (el) { edgeEls[el.getAttribute('data-id')] = el; });
  document.documentElement.classList.add('js-map');
  svg.classList.add('simple');
  ctl.hidden = false; document.querySelector('[data-zoom]').hidden = false;

  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function rel(u) { return u.replace(/^.*\/systems-map\//, ''); }
  function claimList(cs) {
    if (!cs.length) return '<p>No claim supports this connection; it is a reasoned hypothesis.</p>';
    return '<ul>' + cs.map(function (c) {
      return '<li>' + esc(c.text) + ' <a class="cite" href="../evidence/claims.html#' + c.claim_id + '">' + c.claim_id + '</a> <span class="muted small">' + esc(c.verification_label) + '</span></li>';
    }).join('') + '</ul>';
  }
  function clearMarks() {
    svg.classList.remove('focus');
    svg.querySelectorAll('.on, .lever-target, .path-on').forEach(function (el) { el.classList.remove('on', 'lever-target', 'path-on'); });
  }
  function mark(edgeIds, cls) {
    svg.classList.add('focus');
    edgeIds.forEach(function (id) {
      var e = E[id]; if (!e) return;
      edgeEls[id].classList.add(cls || 'on'); nodeEls[e.from].classList.add('on'); nodeEls[e.to].classList.add('on');
    });
  }
  var calm = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function show(htmlStr) { panel.innerHTML = htmlStr + '<p class="sans small"><button type="button" class="btn-clear" data-close>Close details</button></p>'; var r = panel.getBoundingClientRect(); if (r.top > window.innerHeight - 80) panel.scrollIntoView({ block: 'nearest', behavior: calm ? 'auto' : 'smooth' }); }

  function showNode(id) {
    var n = N[id]; clearMarks();
    var outs = D.edges.filter(function (e) { return e.from === id; }), ins = D.edges.filter(function (e) { return e.to === id; });
    mark(outs.concat(ins).map(function (e) { return e.edge_id; }));
    nodeEls[id].classList.add('on');
    function li(e, other) {
      return '<li><button type="button" class="linkish" data-edge="' + e.edge_id + '">' + esc(N[other].label) + '</button> <span class="muted small">' + esc(e.evidence_strength) + (e.relation_kind === 'reasoned_hypothesis' ? ', hypothesis' : '') + '</span></li>';
    }
    show('<h3>' + esc(n.label) + '</h3><p>' + esc(n.explanation) + '</p>' +
      (outs.length ? '<h4>Leads to</h4><ul>' + outs.map(function (e) { return li(e, e.to); }).join('') + '</ul>' : '') +
      (ins.length ? '<h4>Comes from</h4><ul>' + ins.map(function (e) { return li(e, e.from); }).join('') + '</ul>' : '') +
      '<p class="sans small"><a href="' + rel(n.url) + '">Full entry with evidence</a></p>');
  }
  function showEdge(id) {
    var e = E[id]; clearMarks(); mark([id]);
    var lev = e.levers.map(function (l) { return '<li><button type="button" class="linkish" data-lev="' + l + '">' + esc(LV[l].name) + '</button> <span class="muted small">evidence it works: ' + esc(LV[l].effectiveness_rating) + '</span></li>'; }).join('');
    show('<h3>' + esc(N[e.from].label) + ' → ' + esc(N[e.to].label) + '</h3><p>' + esc(e.mechanism) + '</p>' +
      '<p><strong>Evidence that this connection exists: ' + esc(e.evidence_strength) + '.</strong> ' + esc(e.why_this_rating) + '</p>' +
      '<p class="sans small">' + esc(e.relation_label) + ' · ' + esc(e.order) + ' effect · ' + esc(e.geography) + '</p>' +
      '<p class="sans small"><strong>Uncertainty:</strong> ' + esc(e.uncertainty) + '</p>' + claimList(e.claims) +
      (lev ? '<h4>Levers that could weaken it</h4><ul>' + lev + '</ul>' : '') +
      (e.loops.length ? '<p class="sans small">Part of loop ' + e.loops.map(function (l) { return '<button type="button" class="linkish" data-loopbtn="' + l + '">' + l + '</button>'; }).join(', ') + '</p>' : '') +
      '<p class="sans small"><a href="links.html#' + id + '">Full entry</a></p>');
  }
  function showLoop(id) {
    var l = L[id]; clearMarks(); mark(l.edges, 'on');
    show('<h3>Loop ' + l.loop_id + ': ' + esc(l.title) + '</h3><p>' + esc(l.why_feedback) + '</p><ol>' +
      l.edges.map(function (x) { var e = E[x]; return '<li>' + esc(N[e.from].label) + ' → ' + esc(N[e.to].label) + ' <span class="muted small">' + esc(e.evidence_strength) + (e.relation_kind === 'reasoned_hypothesis' ? ', hypothesis' : '') + '</span></li>'; }).join('') +
      '</ol><p><strong>Loop as a whole:</strong> ' + esc(l.loop_confidence) + ' (not studied end to end). ' + l.measured_links + ' of ' + l.links + ' links measured.</p><p class="muted small">' + esc(l.caveats) + '</p><p class="sans small"><a href="' + rel(l.url) + '">Loop page</a></p>');
  }
  function showLever(id) {
    var l = LV[id]; clearMarks(); mark(l.targets, 'lever-target');
    var orgs = l.documented_organisations.map(function (o) { return esc(o.name) + ' (' + esc(o.role) + ')'; }).join('; ');
    var fund = l.funding_records.map(function (p) { return esc(p.title) + ': ' + esc(p.amount) + ', ' + esc(p.stage_in_source); }).concat(
      l.funding_links.map(function (f) { return esc(f.funder) + ' → ' + esc(f.recipient) + ': ' + esc(f.amount) + ', ' + esc(f.stage_in_source); })).join('; ');
    show('<h3>' + esc(l.name) + '</h3><p><strong>Could weaken:</strong> ' + l.targets.map(function (t) { return esc(N[E[t].from].label) + ' → ' + esc(N[E[t].to].label); }).join('; ') + '. ' + esc(l.could_change) + '</p>' +
      '<p><strong>Evidence that it works: ' + esc(l.effectiveness_rating) + '.</strong> ' + esc(l.effectiveness_reason) + ' Recommendation: ' + esc(l.recommendation) + '.</p>' +
      '<p class="sans small"><strong>Who could act:</strong> ' + l.roles.map(function (r) { return esc(r.role) + ': ' + esc(r.institution); }).join('; ') + '</p>' +
      '<p class="sans small"><strong>Documented doing related work:</strong> ' + (orgs || 'none linked yet') + '</p>' +
      '<p class="sans small"><strong>Funded related work:</strong> ' + (fund || 'no verified record linked') + '</p>' +
      '<p class="sans small"><strong>What could go wrong:</strong> ' + esc(l.risks) + '</p><p class="sans small"><strong>Unproven:</strong> ' + esc(l.unproven) + '</p>' +
      '<p class="muted small">Highlighted links could be weakened. This does not mean they are removed or that any loop is broken.</p><p class="sans small"><a href="' + rel(l.url) + '">Lever page</a></p>');
  }

  // path finder: up to three shortest simple paths over published edges
  function paths(from, to, hyp) {
    var adj = {}; D.edges.forEach(function (e) { if (!hyp && e.relation_kind === 'reasoned_hypothesis') return; (adj[e.from] = adj[e.from] || []).push(e); });
    var out = [], queue = [[from, []]], maxLen = 7;
    while (queue.length && out.length < 3) {
      var item = queue.shift(), at = item[0], via = item[1];
      if (via.length >= maxLen) continue;
      (adj[at] || []).forEach(function (e) {
        if (out.length >= 3) return;
        var seen = via.some(function (x) { return E[x].from === e.to; }) || e.to === from;
        if (seen) return;
        var p = via.concat([e.edge_id]);
        if (e.to === to) out.push(p); else queue.push([e.to, p]);
      });
    }
    return out;
  }
  function showPaths(from, to, hyp) {
    clearMarks();
    if (!from || !to || from === to) { show('<p>Choose two different parts of the map.</p>'); return; }
    var ps = paths(from, to, hyp);
    if (!ps.length) { show('<h3>No checked pathway found yet</h3><p>No mapped connection leads from ' + esc(N[from].label) + ' to ' + esc(N[to].label) + (hyp ? '' : ' using measured links. Try including unmeasured hypotheses') + '.</p>'); return; }
    ps.forEach(function (p) { mark(p, 'path-on'); });
    show('<h3>Possible mapped pathways</h3><p class="muted small">A possible mapped pathway, not a causal proof or prediction. Each step has its own evidence.</p>' + ps.map(function (p, i) {
      return '<h4>Route ' + (i + 1) + '</h4><ol>' + p.map(function (x) { var e = E[x]; return '<li><button type="button" class="linkish" data-edge="' + x + '">' + esc(N[e.from].label) + ' → ' + esc(N[e.to].label) + '</button> <span class="muted small">' + esc(e.evidence_strength) + (e.relation_kind === 'reasoned_hypothesis' ? ', hypothesis' : '') + '</span></li>'; }).join('') + '</ol>';
    }).join(''));
  }

  // controls
  var selFrom = ctl.querySelector('[data-from]'), selTo = ctl.querySelector('[data-to]'), selLev = ctl.querySelector('[data-lever]'), selPop = ctl.querySelector('[data-pop]');
  var opts = D.nodes.slice().sort(function (a, b) { return a.label.localeCompare(b.label); }).map(function (n) { return '<option value="' + n.node_id + '">' + esc(n.label) + '</option>'; }).join('');
  selFrom.innerHTML = '<option value="">Choose</option>' + opts; selTo.innerHTML = '<option value="">Choose</option>' + opts;
  selLev.innerHTML += D.levers.map(function (l) { return '<option value="' + l.lever_id + '">' + esc(l.name.length > 70 ? l.name.slice(0, 68) + '…' : l.name) + '</option>'; }).join('');
  selPop.innerHTML += D.groups.map(function (g) { return '<option value="' + g.id + '">' + esc(g.label) + '</option>'; }).join('');
  var viewBtn = ctl.querySelector('[data-view]');
  viewBtn.addEventListener('click', function () {
    var whole = svg.classList.toggle('simple') === false;
    viewBtn.setAttribute('aria-pressed', String(whole)); viewBtn.textContent = whole ? 'Show key connections only' : 'Show the whole web';
  });
  function highlightNodes(test, label) {
    clearMarks(); var hit = [];
    Object.keys(nodeEls).forEach(function (id) { if (test(N[id], nodeEls[id])) { nodeEls[id].classList.add('on'); hit.push(N[id].label); } });
    if (hit.length) { svg.classList.add('focus'); svg.classList.remove('simple'); viewBtn.setAttribute('aria-pressed', 'true'); viewBtn.textContent = 'Show key connections only'; }
    show('<h3>' + esc(label) + '</h3><p>' + hit.length + ' parts highlighted: ' + hit.map(esc).join('; ') + '.</p>');
  }
  ctl.querySelector('[data-sys]').addEventListener('change', function (ev) {
    var v = ev.target.value; if (!v) { clearMarks(); return; }
    var s = D.systems.filter(function (x) { return x.system_id === v; })[0];
    highlightNodes(function (n) { return n.system_id === v; }, s.title);
  });
  selPop.addEventListener('change', function (ev) {
    var v = ev.target.value; if (!v) { clearMarks(); return; }
    highlightNodes(function (n) { return n.populations.indexOf(v) > -1; }, 'Parts of the map documented for: ' + ev.target.selectedOptions[0].textContent);
  });
  ctl.querySelector('[data-find]').addEventListener('click', function () { showPaths(selFrom.value, selTo.value, ctl.querySelector('[data-hyp]').checked); });
  ctl.querySelector('[data-loop]').addEventListener('change', function (ev) { if (ev.target.value) showLoop(ev.target.value); else clearMarks(); });
  ctl.querySelector('[data-four]').addEventListener('change', function (ev) {
    var v = ev.target.value; if (!v) { clearMarks(); return; }
    var ls = D.levers.filter(function (l) { return l.four_is.indexOf(v) > -1; }); clearMarks();
    mark([].concat.apply([], ls.map(function (l) { return l.targets; })), 'lever-target');
    show('<h3>Levers that depend on ' + esc(v) + '</h3><p class="muted small">An illustration of prerequisites from the World Bank\'s 4Is framework, not a prediction. If ' + esc(v.toLowerCase()) + ' is missing, these levers are unlikely to work as intended.</p><ul>' +
      ls.map(function (l) { return '<li><button type="button" class="linkish" data-lev="' + l.lever_id + '">' + esc(l.name) + '</button> <span class="muted small">' + esc(l.job) + '; evidence it works: ' + esc(l.effectiveness_rating) + '</span></li>'; }).join('') +
      '</ul><p class="sans small"><a href="../what-works/four-is.html">The 4Is explained</a></p>');
  });
  selLev.addEventListener('change', function (ev) { if (ev.target.value) showLever(ev.target.value); else clearMarks(); });
  ctl.querySelector('[data-reset]').addEventListener('click', function () {
    clearMarks(); ctl.querySelectorAll('select').forEach(function (s) { s.value = ''; });
    panel.innerHTML = '<p class="muted sans">Select a box or an arrow to see what it means and the evidence behind it.</p>'; resetView();
  });

  svg.addEventListener('click', function (ev) {
    var a = ev.target.closest('a'); if (!a) return;
    ev.preventDefault();
    if (a.classList.contains('node')) showNode(a.getAttribute('data-id')); else if (a.classList.contains('edge')) showEdge(a.getAttribute('data-id'));
  });
  panel.addEventListener('click', function (ev) {
    var b = ev.target.closest('button'); if (!b) return;
    if (b.hasAttribute('data-close')) { clearMarks(); panel.innerHTML = '<p class="muted sans">Details closed.</p>'; return; }
    if (b.getAttribute('data-edge')) showEdge(b.getAttribute('data-edge'));
    if (b.getAttribute('data-lev')) { selLev.value = b.getAttribute('data-lev'); showLever(b.getAttribute('data-lev')); }
    if (b.getAttribute('data-loopbtn')) showLoop(b.getAttribute('data-loopbtn'));
  });
  document.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape' && svg.classList.contains('focus')) { clearMarks(); panel.innerHTML = '<p class="muted sans">Details closed.</p>'; }
  });

  // zoom inside the bounded viewport: the diagram keeps a readable minimum width and the viewport scrolls natively
  // (touch, trackpad, arrow keys when focused). The mouse wheel is never hijacked.
  var zf = 1;
  function apply() { svg.style.width = zf === 1 ? '' : 'max(100%, ' + Math.round(1100 * zf) + 'px)'; }
  function resetView() { zf = 1; apply(); vp.scrollLeft = 0; vp.scrollTop = 0; }
  document.querySelector('[data-zoom]').addEventListener('click', function (ev) {
    var z = ev.target.getAttribute('data-z');
    if (z === 'in') zf = Math.min(2.4, zf * 1.25); else if (z === 'out') zf = Math.max(0.6, zf / 1.25); else if (z === 'reset') return resetView();
    apply();
  });
  var dragMoved = false;
  // deep links from loop and lever pages: index.html#map?loop=L1 is not used; instead read ?loop= or ?lever=
  var q = new URLSearchParams(location.search);
  if (q.get('loop') && L[q.get('loop')]) { ctl.querySelector('[data-loop]').value = q.get('loop'); showLoop(q.get('loop')); }
  if (q.get('lever') && LV[q.get('lever')]) { selLev.value = q.get('lever'); showLever(q.get('lever')); }
})();
