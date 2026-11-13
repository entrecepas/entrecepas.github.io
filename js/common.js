/* Comportamiento común: menú móvil y glosario emergente. Sin dependencias. */
(function () {
  document.documentElement.classList.add('js');
  var reducido = function () { return window.matchMedia('(prefers-reduced-motion: reduce)').matches; };
  /* irA: lleva el principio del elemento a la parte alta de la pantalla; verMin: solo lo justo para verlo entero */
  window.irA = function (el) { if (el && el.scrollIntoView) el.scrollIntoView({ behavior: reducido() ? 'auto' : 'smooth', block: 'start' }); };
  window.verMin = function (el) { if (el && el.scrollIntoView) el.scrollIntoView({ behavior: reducido() ? 'auto' : 'smooth', block: 'nearest' }); };
  var btn = document.getElementById('nav-toggle');
  var nav = document.getElementById('site-nav');
  if (btn && nav) {
    var mq = window.matchMedia('(max-width: 52rem)');
    var sync = function () {
      if (mq.matches) { nav.hidden = btn.getAttribute('aria-expanded') !== 'true'; }
      else { nav.hidden = false; }
    };
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!open));
      sync();
    });
    nav.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && mq.matches && btn.getAttribute('aria-expanded') === 'true') {
        btn.setAttribute('aria-expanded', 'false'); sync(); btn.focus();
      }
    });
    (mq.addEventListener ? mq.addEventListener('change', sync) : mq.addListener(sync));
    sync();
  }
  [['sub-toggle', 'sub-menu'], ['lab-toggle', 'lab-menu']].forEach(function (ids) {
    var st = document.getElementById(ids[0]), sm = document.getElementById(ids[1]);
    if (!(st && sm)) return;
    var cierra = function () { st.setAttribute('aria-expanded', 'false'); sm.hidden = true; };
    st.addEventListener('click', function () {
      var open = st.getAttribute('aria-expanded') === 'true';
      [['sub-toggle', 'sub-menu'], ['lab-toggle', 'lab-menu']].forEach(function (o) { var t = document.getElementById(o[0]), m = document.getElementById(o[1]); if (t && m && t !== st) { t.setAttribute('aria-expanded', 'false'); m.hidden = true; } });
      st.setAttribute('aria-expanded', String(!open)); sm.hidden = open;
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !sm.hidden) { cierra(); st.focus(); } });
    document.addEventListener('click', function (e) { if (!sm.hidden && !sm.parentNode.contains(e.target)) cierra(); });
    sm.addEventListener('focusout', function (e) { if (e.relatedTarget && !sm.parentNode.contains(e.relatedTarget)) cierra(); });
  });
  document.addEventListener('click', function (e) {
    var t = e.target.closest && e.target.closest('button.term');
    if (!t) return;
    var box = document.getElementById(t.getAttribute('aria-controls'));
    if (!box) return;
    var open = t.getAttribute('aria-expanded') === 'true';
    t.setAttribute('aria-expanded', String(!open));
    box.hidden = open;
  });
})();

/* Fuente de las imágenes propias: etiqueta discreta (hover/foco/toque). Las figuras de artículos ("et al.") mantienen su cita visible. */
(function () {
  'use strict';
  var n = 0;
  document.querySelectorAll('figure').forEach(function (fig) {
    var cred = fig.querySelector('figcaption .cred');
    if (!cred || /et al\./.test(cred.textContent)) return;
    if (!/(archivo|proyecto|equipo|Elaboración propia|ilustrativa)/.test(cred.textContent)) return;
    n++;
    var id = 'fuente-' + n;
    cred.id = id; cred.classList.add('cred-flot');
    fig.classList.add('con-fuente');
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'fuente'; b.setAttribute('aria-label', 'Fuente de la imagen'); b.setAttribute('aria-expanded', 'false'); b.setAttribute('aria-controls', id);
    b.textContent = 'i';
    b.addEventListener('click', function () {
      var on = fig.classList.toggle('fuente-on'); b.setAttribute('aria-expanded', on ? 'true' : 'false');
    });
    fig.addEventListener('keydown', function (e) { if (e.key === 'Escape' && fig.classList.contains('fuente-on')) { fig.classList.remove('fuente-on'); b.setAttribute('aria-expanded', 'false'); b.focus(); } });
    fig.insertBefore(b, fig.firstChild);
    var cap = fig.querySelector('figcaption');
    if (cap && !cap.textContent.trim()) cap.hidden = true;
  });
})();
