/* Reto «Detectar mildiu» · datos en data/mildiu.js (generado por tools/gen_mildiu.py) */
(function () {
  'use strict';
  var D = window.MILDIU; if (!D) return;
  var ITEMS = D.items, RONDA = 10, KEY = 'mildiu_mejor_v1';
  var $ = function (id) { return document.getElementById(id); };
  var TXT = {
    avanzado: {
      que: 'Mildiu avanzado',
      desc: 'manchas amarillentas y pardas extendidas por varias hojas, con zonas secas.',
      pista: 'Las manchas amarillentas, «de aceite», en el haz de la hoja son el síntoma más reconocible. Cuando avanza, el tejido se seca y se oscurece.'
    },
    leve: {
      que: 'Mildiu en fase temprana',
      desc: 'manchas pequeñas y dispersas entre muchas hojas sanas, fáciles de pasar por alto.',
      pista: 'Al principio las manchas son diminutas. Por eso es tan difícil verlas entre tanta hoja, también para una persona experta y para una IA.'
    },
    sano: {
      que: 'Sin mildiu',
      desc: 'follaje sin manchas visibles.',
      pista: 'Una vegetación uniforme, sin manchas amarillentas ni zonas secas, es lo esperable en un viñedo sin síntomas.'
    },
    parecido: {
      que: 'Sin mildiu, pero se parece',
      desc: 'hojas con coloración rojiza o amarillenta que no es mildiu.',
      pista: 'No todo lo que cambia de color es mildiu: hojas rojizas o amarillentas pueden confundirse con los síntomas. Por eso hace falta experiencia (y validación en campo).'
    }
  };
  var NOMBRE = { avanzado: 'Mildiu avanzado', leve: 'Mildiu en fase temprana', sano: 'Sin mildiu', parecido: 'Se parece, pero no es mildiu' };
  var el = {
    intro: $('juego-intro'), play: $('juego-juego'), fin: $('juego-fin'), status: $('estado'), modoGuia: $('modo-guia'),
    progreso: $('progreso'), barra: $('progreso-barra'), titulo: $('titulo-caso'), figura: $('figura'), img: $('img-caso'),
    botones: $('botones-resp'), sin: $('resp-sin'), con: $('resp-con'), fb: $('feedback'), fbTit: $('fb-titulo'), fbTxt: $('fb-texto'),
    fbPista: $('fb-pista'), fbIA: $('fb-ia'), sig: $('siguiente'), pregunta: $('pregunta'), guia: $('guia')
  };
  var NS='http://www.w3.org/2000/svg';
  var est = { ronda: [], i: 0, resp: [], guia: false, previas: [], tiempos: [], t0: 0, reloj: null };
  function arrancaReloj() { paraReloj(); est.t0 = Date.now(); var r = $('reloj'); if (!r) return; r.textContent = '0:00'; est.reloj = window.setInterval(function () { r.textContent = window.EntreCepasVs.fmt((Date.now() - est.t0) / 1000); }, 1000); }
  function paraReloj() { if (est.reloj) { window.clearInterval(est.reloj); est.reloj = null; } }

  function anuncia(t) { el.status.textContent = ''; setTimeout(function () { el.status.textContent = t; }, 30); }
  function baraja(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function toma(cat, n) {
    var l = ITEMS.filter(function (x) { return x.cat === cat; });
    var libres = l.filter(function (x) { return est.previas.indexOf(x.id) < 0; });
    if (libres.length < n) libres = l;
    return baraja(libres).slice(0, n);
  }
  function nuevaRonda() {
    var r = [].concat(toma('avanzado', 2), toma('leve', 3), toma('sano', 3), toma('parecido', 2));
    est.previas = r.map(function (x) { return x.id; });
    return baraja(r);
  }
  function limpia(n) { while (n.firstChild) n.removeChild(n.firstChild); }
  function pic(it, alt) {
    var p = document.createElement('picture');
    var s = document.createElement('source'); s.type = 'image/webp'; s.srcset = 'img/mildiu/' + it.id + '.webp'; p.appendChild(s);
    var im = document.createElement('img'); im.src = 'img/mildiu/' + it.id + '.jpg'; im.alt = alt; im.width = it.w; im.height = it.h; im.decoding = 'async';
    p.appendChild(im); return p;
  }

  function empezar() {
    est.guia = el.modoGuia.checked; est.ronda = nuevaRonda(); est.i = 0; est.resp = []; est.tiempos = [];
    el.intro.hidden = true; el.fin.hidden = true; el.play.hidden = false; muestra();
  }
  function barra() {
    limpia(el.barra);
    for (var k = 0; k < RONDA; k++) { var s = document.createElement('span'); s.className = k < est.i ? 'hecha' : (k === est.i ? 'actual' : ''); el.barra.appendChild(s); }
    el.progreso.textContent = 'Imagen ' + (est.i + 1) + ' de ' + RONDA;
  }
  function muestra() {
    var it = est.ronda[est.i]; barra();
    el.fb.hidden = true; el.sig.hidden = true; el.fbIA.hidden = true;
    el.titulo.textContent = 'Imagen ' + (est.i + 1);
    limpia(el.img); quitaManchas(); $('ctl-manchas').hidden = true;
    if (est.guia) {
      el.figura.hidden = true; el.botones.hidden = true; el.pregunta.textContent = 'Recorrido guiado: sin imágenes, solo explicaciones y resultados.';
      respuesta(null);
    } else {
      el.figura.hidden = false; el.botones.hidden = false; el.sin.disabled = el.con.disabled = false;
      el.img.appendChild(pic(it, 'Recorte de una fotografía de la vegetación de un viñedo: hojas de distintos tonos, sobre todo verdes y amarillentas.'));
      el.pregunta.textContent = 'Mira con atención. ¿Ves mildiu en esta imagen?';
      arrancaReloj();
    }
    anuncia('Imagen ' + (est.i + 1) + ' de ' + RONDA + '.');
    el.titulo.setAttribute('tabindex', '-1'); el.titulo.focus({ preventScroll: true });
    window.irA($('juego-juego'));
  }
  function respuesta(v) { // v: 'mildiu' | 'sin' | null (guiado)
    var it = est.ronda[est.i], t = TXT[it.cat], ok = v === null ? null : (v === it.et);
    est.resp[est.i] = v; if (v !== null) { est.tiempos[est.i] = (Date.now() - est.t0) / 1000; paraReloj(); }
    el.sin.disabled = el.con.disabled = true;
    el.fb.hidden = false; el.fb.className = 'resultado-paso' + (ok === false ? ' oculto' : '');
    var cab = ok === null ? '' : (ok ? '✔ Acertaste. ' : '✘ No era esa. ');
    el.fbTit.textContent = cab + (it.et === 'mildiu' ? 'Esta imagen tiene mildiu.' : 'Esta imagen no tiene mildiu.');
    el.fbTxt.textContent = t.que + ': ' + t.desc;
    el.fbPista.textContent = t.pista;
    if (it.pred) { el.fbIA.hidden = false; el.fbIA.textContent = 'La IA dijo: ' + it.pred + ' (confianza ' + Math.round(it.conf * 100) + ' %).'; }
    if (!est.guia && it.les && it.les.length) pintaManchas(it);
    el.sig.hidden = false; el.sig.textContent = est.i === RONDA - 1 ? 'Ver el resultado' : 'Siguiente imagen';
    anuncia(el.fbTit.textContent + ' ' + el.fbTxt.textContent);
    el.sig.focus({ preventScroll: true }); window.verMin(el.sig);
  }
  function quitaManchas() { var o = document.getElementById('svg-manchas'); if (o) o.parentNode.removeChild(o); }
  function pintaManchas(it) {
    var svg = document.createElementNS(NS, 'svg'); svg.setAttribute('id', 'svg-manchas'); svg.setAttribute('viewBox', '0 0 ' + it.w + ' ' + it.h);
    svg.setAttribute('class', 'capa-manchas'); svg.setAttribute('aria-hidden', 'true'); svg.setAttribute('focusable', 'false');
    it.les.forEach(function (f) {
      var pts = []; for (var k = 0; k < f.length; k += 2) pts.push(f[k] + ',' + f[k + 1]);
      var h = document.createElementNS(NS, 'polygon'); h.setAttribute('points', pts.join(' ')); h.setAttribute('class', 'halo'); svg.appendChild(h);
      var m = document.createElementNS(NS, 'polygon'); m.setAttribute('points', pts.join(' ')); m.setAttribute('class', 'mancha'); svg.appendChild(m);
    });
    $('lienzo-m').appendChild(svg);
    $('ctl-manchas').hidden = false; var b = $('ver-manchas'); b.setAttribute('aria-pressed', 'true'); b.textContent = 'Ocultar manchas marcadas';
    $('cap-manchas').textContent = 'Imagen con ' + it.les.length + ' zonas de mildiu marcadas con línea discontinua.';
  }
  function siguiente() { if (est.i < RONDA - 1) { est.i++; muestra(); } else final(); }

  function final() {
    el.play.hidden = true; el.fin.hidden = false;
    var aciertos = 0, porCat = {}, i;
    for (i = 0; i < RONDA; i++) {
      var it = est.ronda[i], ok = est.resp[i] === it.et;
      var c = porCat[it.cat] = porCat[it.cat] || { n: 0, ok: 0 }; c.n++; if (ok) { c.ok++; aciertos++; }
    }
    var body = $('tabla-cuerpo'); limpia(body);
    ['avanzado', 'leve', 'sano', 'parecido'].forEach(function (k) {
      if (!porCat[k]) return;
      var tr = document.createElement('tr'), th = document.createElement('th'); th.scope = 'row'; th.textContent = NOMBRE[k]; tr.appendChild(th);
      var a = document.createElement('td'); a.textContent = porCat[k].n; tr.appendChild(a);
      var b = document.createElement('td'); b.textContent = est.guia ? '—' : porCat[k].ok; tr.appendChild(b); body.appendChild(tr);
    });
    $('bloque-vs').hidden = est.guia;
    if (!est.guia) {
      var tm = est.tiempos.reduce(function (a, b) { return a + b; }, 0) / est.tiempos.length;
      window.EntreCepasVs.pinta({ tmed: tm, unidad: 'por imagen', ia: { s: 0.2, txt: '≈ 0,2 s', nota: 'por imagen (estimación propia)' }, cpu: { txt: '≈ 4,5 s', nota: 'por imagen, medido en un ordenador de 2 núcleos' }, aviso: 'Los artículos no publican el tiempo por imagen, así que son cifras propias: la estimación con GPU es un orden de magnitud, y la medida sin GPU es de una prueba real con este modelo. Y ojo: rápido no es lo mismo que acertar, y la decisión final es siempre de una persona.' });
    }
    if (est.guia) {
      $('f-aciertos').textContent = '10 casos'; $('f-aciertos-txt').textContent = 'repasados en el recorrido guiado.'; $('f-mejor').textContent = '';
    } else {
      $('f-aciertos').textContent = aciertos + ' de ' + RONDA; $('f-aciertos-txt').textContent = 'imágenes bien clasificadas.';
      var mejor = null; try { mejor = parseInt(localStorage.getItem(KEY), 10); } catch (e) { mejor = null; }
      if (isNaN(mejor)) mejor = null;
      var nuevo = mejor === null || aciertos > mejor;
      if (nuevo) { try { localStorage.setItem(KEY, String(aciertos)); } catch (e) { /* sin almacenamiento */ } mejor = aciertos; }
      $('f-mejor').textContent = (nuevo ? 'Nuevo récord en este navegador: ' : 'Tu mejor ronda en este navegador: ') + mejor + ' de ' + RONDA + '.';
      var l = porCat.leve; $('f-leve').textContent = l ? 'Con mildiu en fase temprana acertaste ' + l.ok + ' de ' + l.n + '. ' + (l.ok < l.n ? 'Es lo más difícil: las manchas iniciales son diminutas.' : 'Buen ojo: es lo más difícil de ver.') : '';
    }
    $('f-compartir').setAttribute('data-texto', est.guia ? 'En «Entre cepas» he repasado diez imágenes reales de mildiu en viñedo. ¿Sabrías distinguir las hojas con mildiu de las sanas?' : 'En «Entre cepas» he acertado ' + aciertos + ' de ' + RONDA + ' imágenes reales de viñedo: ¿mildiu o no? ¿Y tú?');
    anuncia('Ronda terminada. ' + $('f-aciertos').textContent + ' ' + $('f-aciertos-txt').textContent);
    var h = $('titulo-final'); h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true });
    window.irA($('juego-fin'));
  }

  $('empezar').addEventListener('click', empezar);
  $('otra').addEventListener('click', empezar);
  el.sin.addEventListener('click', function () { respuesta('sin'); });
  el.con.addEventListener('click', function () { respuesta('mildiu'); });
  el.sig.addEventListener('click', siguiente);
  $('ver-manchas').addEventListener('click', function () {
    var o = document.getElementById('svg-manchas'); if (!o) return;
    var oculto = o.style.display === 'none'; o.style.display = oculto ? '' : 'none';
    this.setAttribute('aria-pressed', String(oculto)); this.textContent = oculto ? 'Ocultar manchas marcadas' : 'Mostrar manchas marcadas';
  });
})();
