/* Reto «¿En qué fase está la vid?» · datos en window.FASES (generado por tools/build.py) */
(function () {
  'use strict';
  var D = window.FASES; if (!D) return;
  var RONDA = 8, KEY = 'fases_mejor_v1';
  var $ = function (id) { return document.getElementById(id); };
  var ET = D.etapas, POS = {}; ET.forEach(function (e, i) { POS[e.el] = i; });
  var est = { ronda: [], i: 0, resp: [], guia: false, previas: [], hecho: false, tiempos: [], t0: 0, reloj: null };
  function arrancaReloj() { paraReloj(); est.t0 = Date.now(); var r = $('reloj'); r.textContent = '0:00'; est.reloj = window.setInterval(function () { r.textContent = window.EntreCepasVs.fmt((Date.now() - est.t0) / 1000); }, 1000); }
  function paraReloj() { if (est.reloj) { window.clearInterval(est.reloj); est.reloj = null; } }
  function anuncia(t) { $('estado').textContent = ''; setTimeout(function () { $('estado').textContent = t; }, 30); }
  function baraja(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function limpia(n) { while (n.firstChild) n.removeChild(n.firstChild); }
  function nombre(el) { return ET[POS[el]].n; }
  function nuevaRonda() {
    var etapas = baraja(ET.map(function (e) { return e.el; })).slice(0, RONDA);
    var r = etapas.map(function (el) {
      var l = D.fotos.filter(function (f) { return f.el === el; });
      var libres = l.filter(function (f) { return est.previas.indexOf(f.id) < 0; }); if (!libres.length) libres = l;
      return baraja(libres)[0];
    });
    est.previas = r.map(function (f) { return f.id; });
    return baraja(r);
  }
  function pic(f) {
    var p = document.createElement('picture'), s = document.createElement('source'); s.type = 'image/webp'; s.srcset = 'img/fases/' + f.id + '.webp'; p.appendChild(s);
    var im = document.createElement('img'); im.src = 'img/fases/' + f.id + '.jpg'; im.width = f.w; im.height = f.h; im.decoding = 'async';
    im.alt = 'Fotografía de una cepa en el viñedo. Tu tarea es decir en qué estado fenológico está; una descripción detallada aparece al comprobar la respuesta.';
    p.appendChild(im); return p;
  }
  function radios() { return document.querySelectorAll('#carril input[type=radio]'); }
  function sel() { var r = document.querySelector('#carril input:checked'); return r ? parseInt(r.value, 10) : null; }
  function barra() {
    var b = $('progreso-barra'); limpia(b);
    for (var k = 0; k < RONDA; k++) { var s = document.createElement('span'); s.className = k < est.i ? 'hecha' : (k === est.i ? 'actual' : ''); b.appendChild(s); }
    $('progreso').textContent = 'Foto ' + (est.i + 1) + ' de ' + RONDA;
  }
  function empezar() {
    est.guia = $('modo-guia').checked; est.i = 0; est.resp = []; est.tiempos = [];
    est.ronda = est.guia ? ET.map(function (e) { return { el: e.el }; }) : nuevaRonda();
    $('juego-intro').hidden = true; $('juego-fin').hidden = true; $('juego-juego').hidden = false; muestra();
  }
  function muestra() {
    var f = est.ronda[est.i], N = est.ronda.length; est.hecho = false;
    var b = $('progreso-barra'); limpia(b);
    for (var k = 0; k < N; k++) { var s = document.createElement('span'); s.className = k < est.i ? 'hecha' : (k === est.i ? 'actual' : ''); b.appendChild(s); }
    $('progreso').textContent = (est.guia ? 'Etapa ' : 'Foto ') + (est.i + 1) + ' de ' + N;
    $('carril').removeAttribute('tabindex'); $('feedback').hidden = true; $('siguiente').hidden = true; $('comprobar').hidden = false; $('comprobar').disabled = true;
    Array.prototype.forEach.call(radios(), function (r) { r.checked = false; r.disabled = false; r.parentNode.className = 'nodo'; });
    $('titulo-caso').textContent = est.guia ? 'Recorrido guiado' : 'Foto ' + (est.i + 1);
    limpia($('img-caso'));
    if (est.guia) {
      $('figura').hidden = true; $('linea').hidden = true; $('comprobar').hidden = true; resultado(f.el, null);
    } else {
      $('figura').hidden = false; $('linea').hidden = false; $('img-caso').appendChild(pic(f)); arrancaReloj();
    }
    anuncia((est.guia ? 'Etapa ' : 'Foto ') + (est.i + 1) + ' de ' + N + '.');
    var t = $('titulo-caso'); t.setAttribute('tabindex', '-1'); t.focus({ preventScroll: true }); window.irA($('juego-juego'));
  }
  function resultado(real, elegido) {
    var e = ET[POS[real]], dist = elegido === null ? null : Math.abs(POS[elegido] - POS[real]);
    est.resp[est.i] = elegido; est.hecho = true; if (elegido !== null) { est.tiempos[est.i] = (Date.now() - est.t0) / 1000; paraReloj(); }
    Array.prototype.forEach.call(radios(), function (r) {
      r.disabled = true; var v = parseInt(r.value, 10);
      if (v === real) r.parentNode.className = 'nodo correcto'; else if (v === elegido) r.parentNode.className = 'nodo errado';
    });
    $('comprobar').hidden = true; $('carril').tabIndex = 0;
    var fb = $('feedback'); fb.hidden = false; fb.className = 'resultado-paso' + (dist === 0 || dist === null ? '' : ' oculto');
    var cab = dist === null ? '' : (dist === 0 ? '✔ Exacto. ' : (dist === 1 ? '≈ Casi: estabas a una fase. ' : '✘ No era esa. '));
    $('fb-titulo').textContent = cab + (est.guia ? '' : 'Esta foto es de ') + 'E-L ' + e.el + ': ' + e.n + '.';
    $('fb-texto').textContent = e.desc;
    $('fb-pista').textContent = e.pista + (dist === null ? '' : ' El paso de una fase a otra es gradual, y a distancia hasta las personas expertas dudan entre fases vecinas.');
    $('siguiente').hidden = false; $('siguiente').textContent = est.i === est.ronda.length - 1 ? 'Ver el resultado' : (est.guia ? 'Siguiente etapa' : 'Siguiente foto');
    anuncia($('fb-titulo').textContent + ' ' + e.desc);
    $('siguiente').focus({ preventScroll: true }); window.verMin($('siguiente'));
  }
  function final() {
    $('juego-juego').hidden = true; $('juego-fin').hidden = false;
    var N = est.ronda.length, ex = 0, cerca = 0, i;
    $('bloque-vs').hidden = est.guia;
    if (!est.guia) {
      var tm = est.tiempos.reduce(function (a, b) { return a + b; }, 0) / est.tiempos.length;
      window.EntreCepasVs.pinta({ tmed: tm, unidad: 'por foto', ia: { s: 0.005, txt: '≈ 5 ms', nota: 'por foto (estimación propia)' }, cpu: { txt: '≈ 0,5 s', nota: 'por foto, medido en un ordenador de 2 núcleos' }, aviso: 'El estudio no publica el tiempo por imagen ni compara con personas: estas cifras son propias. Con la estimación para un ResNet-34 a 768 px en una GPU como la del estudio, y con la medida en un ordenador normal sin GPU. Eso sí: a la IA le pasa como a ti, confunde fases vecinas.' });
    }
    if (est.guia) {
      $('f-aciertos').textContent = '9 etapas'; $('f-aciertos-txt').textContent = 'repasadas en el recorrido guiado.'; $('f-cerca').textContent = ''; $('f-mejor').textContent = '';
      $('f-compartir').setAttribute('data-texto', 'En «Entre cepas» he repasado las etapas del ciclo de la vid, de la brotación a la maduración. ¿Sabrías reconocerlas en una foto?');
    } else {
      for (i = 0; i < N; i++) { var d = Math.abs(POS[est.resp[i]] - POS[est.ronda[i].el]); if (d === 0) ex++; if (d <= 1) cerca++; }
      $('f-aciertos').textContent = ex + ' de ' + N; $('f-aciertos-txt').textContent = 'fotos situadas en la fase exacta.';
      $('f-cerca').textContent = 'Si cuentas también las que quedaron a una fase de distancia, fueron ' + cerca + ' de ' + N + '. Fases vecinas se parecen mucho: el ciclo de la vid es continuo, y las etapas son una forma de ponerle marcas.';
      var mejor = null; try { mejor = parseInt(localStorage.getItem(KEY), 10); } catch (e) { mejor = null; } if (isNaN(mejor)) mejor = null;
      var nuevo = mejor === null || ex > mejor; if (nuevo) { try { localStorage.setItem(KEY, String(ex)); } catch (e2) { } mejor = ex; }
      $('f-mejor').textContent = (nuevo ? 'Nuevo récord en este navegador: ' : 'Tu mejor ronda en este navegador: ') + mejor + ' de ' + N + '.';
      $('f-compartir').setAttribute('data-texto', 'En «Entre cepas» he acertado la fase exacta de la vid en ' + ex + ' de ' + N + ' fotos (' + cerca + ' a una fase o menos). ¿Y tú?');
    }
    anuncia('Ronda terminada. ' + $('f-aciertos').textContent + ' ' + $('f-aciertos-txt').textContent);
    var h = $('titulo-final'); h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); window.irA($('juego-fin'));
  }
  $('empezar').addEventListener('click', empezar); $('otra').addEventListener('click', empezar);
  $('carril').addEventListener('change', function () {
    $('comprobar').disabled = sel() === null;

  });
  $('comprobar').addEventListener('click', function () { var v = sel(); if (v !== null) resultado(est.ronda[est.i].el, v); });
  $('siguiente').addEventListener('click', function () { if (est.i < est.ronda.length - 1) { est.i++; muestra(); } else final(); });
})();
