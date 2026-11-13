/* Escuchar esta página: usa la voz del propio navegador (Web Speech API). Sin servicios externos. */
(function () {
  'use strict';
  if (!('speechSynthesis' in window) || !window.SpeechSynthesisUtterance) return;
  var main = document.getElementById('contenido'); if (!main) return;
  var synth = window.speechSynthesis, cola = [], activo = false, pausado = false, voz = null;

  var bar = document.createElement('div');
  bar.className = 'voz'; bar.setAttribute('role', 'group'); bar.setAttribute('aria-label', 'Escuchar esta página');
  bar.innerHTML = '<button type="button" class="btn secundario" id="voz-play">Escuchar esta página</button>' +
    '<button type="button" class="btn secundario" id="voz-pausa" hidden>Pausar</button>' +
    '<button type="button" class="btn secundario" id="voz-stop" hidden>Parar</button>' +
    '<span id="voz-estado" class="sr-only" role="status" aria-live="polite"></span>';
  main.insertBefore(bar, main.firstChild);
  var $ = function (id) { return document.getElementById(id); };
  var play = $('voz-play'), pausa = $('voz-pausa'), stop = $('voz-stop'), est = $('voz-estado');

  function elige() {
    var vs = synth.getVoices();
    voz = vs.filter(function (v) { return /^es[-_]ES/i.test(v.lang); })[0] || vs.filter(function (v) { return /^es/i.test(v.lang); })[0] || null;
  }
  elige(); if (synth.onvoiceschanged !== undefined) synth.onvoiceschanged = elige;

  function texto() {
    var c = main.cloneNode(true);
    var q = c.querySelectorAll('.voz, script, style, svg, [hidden], [aria-hidden="true"], .sr-only, .escena, #juego-juego, #juego-fin, form');
    for (var i = 0; i < q.length; i++) if (q[i].parentNode) q[i].parentNode.removeChild(q[i]);
    var ds = c.querySelectorAll('details:not([open])');
    for (i = 0; i < ds.length; i++) { var s = ds[i].querySelector('summary'); ds[i].innerHTML = ''; if (s) ds[i].appendChild(s); }
    var t = (c.innerText || c.textContent || '').replace(/\s+/g, ' ').trim();
    return t.match(/[^.!?¡¿:;]+[.!?:;]?\s*/g) || [t];
  }
  function lee() {
    if (!cola.length || !activo) { fin(); return; }
    var u = new SpeechSynthesisUtterance(cola.shift());
    u.lang = 'es-ES'; if (voz) u.voice = voz; u.rate = 1;
    u.onend = lee; u.onerror = function () { fin(); };
    synth.speak(u);
  }
  function fin() { activo = false; pausado = false; synth.cancel(); play.hidden = false; pausa.hidden = true; stop.hidden = true; pausa.textContent = 'Pausar'; }
  play.addEventListener('click', function () {
    synth.cancel(); cola = texto(); activo = true;
    play.hidden = true; pausa.hidden = false; stop.hidden = false; est.textContent = 'Leyendo la página en voz alta.';
    lee(); pausa.focus();
  });
  pausa.addEventListener('click', function () {
    if (pausado) { synth.resume(); pausado = false; pausa.textContent = 'Pausar'; } else { synth.pause(); pausado = true; pausa.textContent = 'Seguir'; }
  });
  stop.addEventListener('click', function () { fin(); est.textContent = 'Lectura detenida.'; play.focus(); });
  window.addEventListener('pagehide', function () { synth.cancel(); });
})();
