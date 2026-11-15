/* Portada: deslizador para quitar las hojas a una cepa real. */
(function () {
  'use strict';
  var fig = document.getElementById('hero-cepa'); if (!fig) return;
  var r = document.getElementById('hc-rango'), lz = fig.querySelector('.hc-lienzo'), t = document.getElementById('hc-txt');
  var vis = +fig.dataset.vis, oc = +fig.dataset.oc, tot = +fig.dataset.tot, ultimo = null;
  function act() {
    var v = parseInt(r.value, 10); lz.style.setProperty('--pos', v + '%');
    r.setAttribute('aria-valuetext', v === 0 ? 'Cepa con hojas' : (v === 100 ? 'Cepa sin hojas' : v + ' % sin hojas'));
    var estado = v >= 60 ? 'fin' : 'ini';
    if (estado !== ultimo) {
      ultimo = estado;
      t.textContent = estado === 'fin'
        ? 'Sin hojas aparecen ' + oc + ' racimos más: había ' + tot + '. Con hojas, una persona experta veía ' + vis + ' y la IA de Televitis no vio ninguno. Eso es lo que la cámara no ve.'
        : 'Con hojas, una persona experta ve ' + vis + ' racimos. ¿Cuántos esconden las hojas? Desliza para descubrirlo.';
    }
  }
  r.addEventListener('input', act); act();
})();
