// Progressive enhancement: filters and print button. Content is fully usable without JavaScript.
document.querySelectorAll('[data-filter-for]').forEach(function (box) {
  var target = document.getElementById(box.getAttribute('data-filter-for'));
  if (!target) return;
  var items = target.tagName === 'TABLE' ? target.querySelectorAll('tbody tr') : target.children;
  var count = document.getElementById(box.getAttribute('data-filter-for') + '-count');
  box.hidden = false;
  function apply() {
    var shown = 0;
    Array.prototype.forEach.call(items, function (el) {
      var ok = true;
      box.querySelectorAll('select').forEach(function (s) {
        var v = s.value, key = s.getAttribute('data-key'), have = el.getAttribute('data-' + key) || '';
        if (v && have.indexOf(v) === -1) ok = false;
      });
      el.hidden = !ok; if (ok) shown++;
    });
    if (count) count.textContent = 'Showing ' + shown + ' of ' + items.length;
  }
  box.addEventListener('change', apply); apply();
});
document.querySelectorAll('[data-print]').forEach(function (b) { b.addEventListener('click', function () { window.print(); }); });
// Compare up to three interventions: toggles table columns; without JS three defaults show.
(function () {
  var box = document.querySelector('[data-compare]');
  if (!box) return;
  box.hidden = false;
  var status = document.getElementById('compare-status');
  function apply() {
    var picked = Array.prototype.filter.call(box.querySelectorAll('input'), function (i) { return i.checked; }).map(function (i) { return i.value; });
    document.querySelectorAll('#compare-table [data-col]').forEach(function (c) { c.hidden = picked.indexOf(c.getAttribute('data-col')) === -1; });
    box.querySelectorAll('input').forEach(function (i) { i.disabled = !i.checked && picked.length >= 3; });
    if (status) status.textContent = 'Comparing ' + picked.length + ' of up to 3';
  }
  box.addEventListener('change', apply); apply();
})();
// Open a closed <details> when a link targets something inside it (keeps old #anchors working).
(function () {
  function openFor(hash) {
    if (!hash || hash.length < 2) return;
    var el = document.getElementById(decodeURIComponent(hash.slice(1)));
    if (!el) return;
    for (var p = el.parentElement; p; p = p.parentElement) if (p.tagName === 'DETAILS') p.open = true;
    el.scrollIntoView();
  }
  openFor(location.hash); window.addEventListener('hashchange', function () { openFor(location.hash); });
})();
// Organisations explorer: search, filters, presets, chunked display. Without JS every card is listed.
(function () {
  var form = document.querySelector('[data-explorer]');
  var list = document.getElementById('org-list');
  if (!form || !list) return;
  form.hidden = false;
  var mf = form.querySelector('[data-more-filters]'); if (mf && window.innerWidth >= 768) mf.open = true;
  var cards = Array.prototype.slice.call(list.children), PAGE = window.innerWidth < 600 ? 10 : 24, limit = PAGE;
  var q = form.querySelector('[data-q]'), sels = form.querySelectorAll('select[data-f]');
  var count = document.getElementById('ex-count'), active = document.getElementById('ex-active');
  var more = document.getElementById('ex-more'), none = document.getElementById('ex-none');
  var presetCat = '';
  function match(card) {
    var text = q.value.trim().toLowerCase();
    if (text && card.getAttribute('data-search').indexOf(text) === -1) return false;
    if (presetCat && presetCat.split('|').indexOf(card.getAttribute('data-category')) === -1) return false;
    for (var i = 0; i < sels.length; i++) {
      var v = sels[i].value, k = sels[i].getAttribute('data-f'); if (!v) continue;
      var have = card.getAttribute('data-' + k) || '';
      var parts = k === 'domain' || k === 'fn' ? have.split('|') : have.split(' ');
      if (k === 'funding' || k === 'status' || k === 'ev' || k === 'category') parts = [have];
      if (parts.indexOf(v) === -1) return false;
    }
    return true;
  }
  function apply(resetLimit) {
    if (resetLimit) limit = PAGE;
    var hits = cards.filter(match);
    cards.forEach(function (c) { c.hidden = true; });
    hits.slice(0, limit).forEach(function (c) { c.hidden = false; });
    count.textContent = hits.length + ' of ' + cards.length + ' organisations match' + (hits.length > limit ? ' (showing ' + limit + ')' : '');
    more.hidden = hits.length <= limit;
    none.hidden = hits.length !== 0;
    var labels = [];
    if (presetCat) labels.push(document.querySelector('[data-preset-id].on strong').textContent);
    if (q.value.trim()) labels.push('Search: "' + q.value.trim() + '"');
    sels.forEach(function (s) { if (s.value) labels.push(s.parentNode.firstChild.textContent.trim() + ': ' + s.options[s.selectedIndex].text); });
    active.textContent = labels.length ? 'Active: ' + labels.join(' · ') : '';
  }
  form.addEventListener('input', function () { apply(true); });
  form.addEventListener('change', function () { apply(true); });
  more.addEventListener('click', function () { limit += PAGE; apply(false); });
  form.querySelector('[data-clear]').addEventListener('click', function () {
    q.value = ''; sels.forEach(function (s) { s.value = ''; }); presetCat = '';
    document.querySelectorAll('[data-preset-id]').forEach(function (p) { p.classList.remove('on'); p.setAttribute('aria-pressed', 'false'); });
    apply(true); q.focus();
  });
  document.querySelectorAll('[data-preset]').forEach(function (p) {
    p.setAttribute('role', 'button'); p.setAttribute('aria-pressed', 'false');
    p.addEventListener('click', function (e) {
      if (p.getAttribute('data-preset-id') === 'money') return; // follows the link to the funding page
      e.preventDefault();
      var on = !p.classList.contains('on');
      document.querySelectorAll('[data-preset-id]').forEach(function (x) { x.classList.remove('on'); x.setAttribute('aria-pressed', 'false'); });
      presetCat = on ? p.getAttribute('data-preset') : '';
      if (on) { p.classList.add('on'); p.setAttribute('aria-pressed', 'true'); }
      apply(true);
      document.getElementById('explorer').scrollIntoView();
      count.focus && count.setAttribute('tabindex', '-1');
    });
    p.addEventListener('keydown', function (e) { if (e.key === ' ') { e.preventDefault(); p.click(); } });
  });
  apply(true);
})();
