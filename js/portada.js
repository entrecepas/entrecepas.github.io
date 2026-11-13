(function () {
  'use strict';
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.selector [role="tab"]'));
  if (!tabs.length) return;
  document.documentElement.classList.add('tabs-js');
  function activa(t, foco) {
    tabs.forEach(function (x) {
      var on = x === t;
      x.setAttribute('aria-selected', on ? 'true' : 'false');
      x.tabIndex = on ? 0 : -1;
      document.getElementById(x.getAttribute('aria-controls')).classList.toggle('activo', on);
    });
    if (foco) t.focus({ preventScroll: true });
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { activa(t, false); });
    t.addEventListener('keydown', function (e) {
      var j = null;
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') j = (i + 1) % tabs.length;
      else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') j = (i - 1 + tabs.length) % tabs.length;
      else if (e.key === 'Home') j = 0;
      else if (e.key === 'End') j = tabs.length - 1;
      if (j !== null) { e.preventDefault(); activa(tabs[j], true); }
    });
  });
})();
