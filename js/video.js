/* Vídeo de la portada: arranca solo la primera vez (sin sonido) cuando se ve en pantalla; el sonido se activa con los controles. */
(function () {
  'use strict';
  var v = document.getElementById('vp');
  if (!v) return;
  v.muted = true;
  var reducir = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reducir || !('IntersectionObserver' in window)) return;
  var hecho = false;
  v.addEventListener('play', function () { hecho = true; });
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (e.isIntersecting && !hecho) {
        hecho = true; io.disconnect();
        var p = v.play(); if (p && p.catch) p.catch(function () {});
      }
    });
  }, { threshold: 0.6 });
  io.observe(v);
})();
