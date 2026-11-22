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
