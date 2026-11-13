/* Compartir: panel con compartir del móvil, copiar enlace, redes y código QR (se genera en el navegador; sin servicios externos). */
(function () {
  'use strict';
  var dlg = null, ultimo = null;
  function url() { return (document.querySelector('link[rel=canonical]') || {}).href || location.href.split('#')[0]; }
  function texto(btn) { return (btn && btn.getAttribute('data-texto')) || 'Entre cepas: ¿puedes contar racimos y detectar mildiu mejor que una inteligencia artificial? Retos con datos reales de viñedos de La Rioja.'; }
  function cargaQR(cb) {
    if (window.qrcode) return cb();
    var s = document.createElement('script'); s.src = 'js/vendor/qrcode.js'; s.onload = cb; document.head.appendChild(s);
  }
  function pintaQR(cont, u) {
    cargaQR(function () {
      var q = window.qrcode(0, 'M'); q.addData(u); q.make();
      cont.innerHTML = q.createSvgTag({ cellSize: 6, margin: 4, scalable: true });
      var svg = cont.querySelector('svg'); if (svg) { svg.setAttribute('role', 'img'); svg.setAttribute('aria-label', 'Código QR con el enlace de la web'); svg.style.width = '100%'; svg.style.height = 'auto'; }
    });
  }
  function enlaces(u, t) {
    var e = encodeURIComponent, tu = e(t + ' ' + u);
    return [
      ['WhatsApp', 'https://wa.me/?text=' + tu],
      ['Telegram', 'https://t.me/share/url?url=' + e(u) + '&text=' + e(t)],
      ['X', 'https://twitter.com/intent/tweet?text=' + e(t) + '&url=' + e(u)],
      ['Facebook', 'https://www.facebook.com/sharer/sharer.php?u=' + e(u)],
      ['LinkedIn', 'https://www.linkedin.com/sharing/share-offsite/?url=' + e(u)],
      ['Correo', 'mailto:?subject=' + e('Entre cepas') + '&body=' + tu]
    ];
  }
  function crea() {
    dlg = document.createElement('dialog'); dlg.className = 'dlg-compartir'; dlg.setAttribute('aria-labelledby', 'dlg-c-h');
    dlg.innerHTML = '<form method="dialog"><h2 id="dlg-c-h">Compartir</h2><p class="dlg-c-texto"></p>' +
      '<p><button type="button" class="btn" data-c-nativo hidden>Compartir desde el móvil</button> <button type="button" class="btn secundario" data-c-copiar>Copiar enlace</button></p>' +
      '<p class="dlg-c-estado" role="status" aria-live="polite"></p>' +
      '<ul class="dlg-c-redes"></ul>' +
      '<div class="dlg-c-qr"><div class="qr" data-c-qr></div><p>Escanea el código con el móvil para abrir la web.</p></div>' +
      '<p class="dlg-c-cierra"><button class="btn secundario" value="cerrar">Cerrar</button></p></form>';
    document.body.appendChild(dlg);
    dlg.addEventListener('close', function () { if (ultimo) ultimo.focus(); });
    dlg.querySelector('[data-c-copiar]').addEventListener('click', function () {
      var u = url(), est = dlg.querySelector('.dlg-c-estado');
      function ok() { est.textContent = 'Enlace copiado.'; }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(u).then(ok, function () { est.textContent = 'No se ha podido copiar. Copia la dirección del navegador.'; });
      else { var i = document.createElement('input'); i.value = u; document.body.appendChild(i); i.select(); try { document.execCommand('copy'); ok(); } catch (e) { est.textContent = 'Copia la dirección del navegador.'; } i.remove(); }
    });
    var nat = dlg.querySelector('[data-c-nativo]');
    if (navigator.share) { nat.hidden = false; nat.addEventListener('click', function () { navigator.share({ title: 'Entre cepas', text: dlg.__t, url: url() }).catch(function () {}); }); }
  }
  function abre(btn) {
    if (!dlg) crea();
    ultimo = btn; var u = url(), t = texto(btn); dlg.__t = t;
    dlg.querySelector('.dlg-c-texto').textContent = t;
    dlg.querySelector('.dlg-c-estado').textContent = '';
    dlg.querySelector('.dlg-c-redes').innerHTML = enlaces(u, t).map(function (x) { return '<li><a class="btn secundario" href="' + x[1] + '" target="_blank" rel="noopener noreferrer">' + x[0] + '<span class="sr-only"> (se abre en una pestaña nueva)</span></a></li>'; }).join('');
    pintaQR(dlg.querySelector('[data-c-qr]'), u);
    if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', '');
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-compartir]'); if (b) { e.preventDefault(); abre(b); }
  });
  window.entreCepasCompartir = abre;
})();
