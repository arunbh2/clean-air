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
