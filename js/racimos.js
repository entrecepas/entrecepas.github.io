/* Reto A · ¿Cuántos racimos hay? · datos en data/racimos.js (generado por tools/gen_racimos.py) */
(function () {
  'use strict';
  var D = window.RACIMOS;
  if (!D) return;
  var CEPAS = D.cepas, META = D.meta;
  var NS = 'http://www.w3.org/2000/svg';
  var RONDA = 5;
  var KEY = 'racimos_mejor_v1';
  var DESC = {
    B_33: 'Follaje muy abundante, verde y amarillento, que ocupa casi todo el encuadre; el tronco asoma por abajo.',
    B_38: 'Follaje verde y denso sobre un fondo claro; el tronco horizontal se ve en la parte baja.',
    C_09: 'Hojas grandes verdes y amarillas, con huecos de luz y sombra entre ellas.',
    C_11: 'Hojas verdes con bordes rojizos que cubren casi toda la cepa; zonas oscuras entre ellas.',
    C_16: 'Hojas verdes y ocres; a la izquierda hay un hueco con fondo blanco y abajo el tronco.',
    C_18: 'Hojas amarillentas y verdes, de aspecto otoñal, repartidas por todo el encuadre.',
    C_25: 'Vegetación dispersa: sarmientos y hojas con mucho fondo blanco visible y una cinta roja y blanca a la izquierda.',
    C_31: 'Hojas rojizas y verdes con huecos; un tronco retorcido en el centro y fondo blanco.',
    C_35: 'Follaje irregular: hojas secas pardas a la izquierda y hojas verdes a la derecha; un cartel con número abajo.',
    C_37: 'Vegetación muy densa de hojas verdes y rojizas que cubre casi todo el encuadre.',
    C_39: 'Hojas verdes y pardas con fondo claro a la izquierda; densidad de hojas media.',
    C_40: 'Hojas grandes anaranjadas y verdes, muy juntas, que tapan buena parte de la cepa.',
    D_20: 'Hojas de aspecto otoñal con huecos de luz; un cartel amarillo con número en el centro.',
    D_25: 'Vegetación escasa: sarmientos finos, pocas hojas y fondo blanco; un cartel amarillo abajo.',
    E_08: 'Follaje oscuro con zonas de sombra y un cartel amarillo con número a la izquierda.',
    E_42: 'Follaje sombrío con hojas anaranjadas en el centro y un cartel abajo a la derecha.',
    E_44: 'Densidad media de hojas: algunas secas y pardas, otras verdes a la izquierda; un cartel amarillo abajo.',
    F_09: 'Vegetación escasa: se ven sarmientos y pocas hojas; una cinta roja y blanca a la izquierda.',
    F_26: 'Hojas verdes sobre fondo blanco con densidad media-baja; un cartel amarillo abajo.',
    F_50: 'Hojas verdes y sarmientos sobre fondo blanco; una cinta roja y blanca a la izquierda.'
  };

  var $ = function (id) { return document.getElementById(id); };
  var el = {
    intro: $('juego-intro'), play: $('juego-juego'), fin: $('juego-fin'), status: $('estado'),
    modoDesc: $('modo-desc'), empezar: $('empezar'),
    progreso: $('progreso'), barra: $('progreso-barra'), pregunta: $('pregunta'), tituloCepa: $('titulo-cepa'),
    escena: $('escena'), escenaScroll: $('escena-scroll'), lienzo: $('lienzo'), pie: $('escena-pie'), desc: $('descripcion-cepa'),
    capaA: $('img-a'), capaB: $('img-b'), svgA: $('cajas-a'), svgB: $('cajas-b'),
    form: $('form-respuesta'), input: $('respuesta'), menos: $('menos'), mas: $('mas'), comprobar: $('comprobar'),
    revelacion: $('revelacion'), pasoA: $('paso-a'), pasoB: $('paso-b'), pasoC: $('paso-c'),
    comparador: $('comparador'), rango: $('rango'), quitar: $('quitar-hojas'), ponerHojas: $('ver-con'), verSin: $('ver-sin'),
    siguiente: $('siguiente'), leyenda: $('leyenda')
  };

  var estado = { ronda: [], i: 0, resp: [], tiempos: [], t0: 0, reloj: null, modoTexto: false, previas: [] };
  function fmt(sg) { var m = Math.floor(sg / 60), r = Math.floor(sg % 60); return m + ':' + (r < 10 ? '0' : '') + r; }
  function arrancaReloj() { paraReloj(); estado.t0 = Date.now(); var r = $('reloj'); r.textContent = '0:00'; estado.reloj = window.setInterval(function () { r.textContent = fmt((Date.now() - estado.t0) / 1000); }, 1000); }
  function paraReloj() { if (estado.reloj) { window.clearInterval(estado.reloj); estado.reloj = null; } }

  function anuncia(txt) { el.status.textContent = ''; window.setTimeout(function () { el.status.textContent = txt; }, 30); }
  function plural(n, s, p) { return n + ' ' + (n === 1 ? s : p); }
  function reducido() { return window.matchMedia('(prefers-reduced-motion: reduce)').matches; }
  function aleat(a) { return a[Math.floor(Math.random() * a.length)]; }
  function baraja(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }

  /* Elige 5 cepas mezclando fáciles, intermedias y difíciles, de menos a más oculta. */
  function nuevaRonda() {
    var libres = function (arr) { var l = arr.filter(function (c) { return estado.previas.indexOf(c.id) < 0; }); return l.length ? l : arr; };
    var f = CEPAS.filter(function (c) { return c.ocultos === 0; });
    var m = CEPAS.filter(function (c) { return c.ocultos >= 1 && c.ocultos <= 2; });
    var d = CEPAS.filter(function (c) { return c.ocultos >= 3; });
    var r = [];
    r.push(aleat(libres(f)));
    baraja(libres(m)).slice(0, 2).forEach(function (c) { r.push(c); });
    var dd = baraja(libres(d)).slice(0, 2).sort(function (a, b) { return a.ocultos - b.ocultos; });
    dd.forEach(function (c) { r.push(c); });
    estado.previas = r.map(function (c) { return c.id; });
    return r;
  }

  function pic(id, nivel, alt, w, h) {
    var p = document.createElement('picture');
    var s = document.createElement('source'); s.type = 'image/webp'; s.srcset = 'img/racimos/' + id + '_' + nivel + '.webp'; p.appendChild(s);
    var im = document.createElement('img'); im.src = 'img/racimos/' + id + '_' + nivel + '.jpg'; im.alt = alt; im.width = w || 1200; im.height = h || 521; im.decoding = 'async';
    p.appendChild(im); return p;
  }
  function rect(svg, b, clase) {
    var h = document.createElementNS(NS, 'rect'); h.setAttribute('class', 'halo');
    var r = document.createElementNS(NS, 'rect'); r.setAttribute('class', clase);
    [h, r].forEach(function (x) { x.setAttribute('x', b[0]); x.setAttribute('y', b[1]); x.setAttribute('width', b[2] - b[0]); x.setAttribute('height', b[3] - b[1]); x.setAttribute('rx', 3); svg.appendChild(x); });
  }
  function limpia(n) { while (n.firstChild) n.removeChild(n.firstChild); }

  function posTxt(b, c) {
    var cx = (b[0] + b[2]) / 2 / c.w, cy = (b[1] + b[3]) / 2 / c.h;
    var h = cx < 0.34 ? 'a la izquierda' : (cx > 0.66 ? 'a la derecha' : 'en el centro');
    var v = cy < 0.4 ? 'arriba' : (cy > 0.65 ? 'abajo' : 'a media altura');
    return v + ' ' + h;
  }
  function listaPos(boxes, c) {
    var t = boxes.map(function (b) { return posTxt(b, c); });
    return t.join('; ');
  }

  /* ---------- flujo ---------- */
  function empezar() {
    estado.modoTexto = el.modoDesc.checked;
    estado.ronda = nuevaRonda(); estado.i = 0; estado.resp = []; estado.tiempos = [];
    el.intro.hidden = true; el.fin.hidden = true; el.play.hidden = false;
    muestraCepa();
  }

  function pintaBarra() {
    limpia(el.barra);
    for (var k = 0; k < RONDA; k++) {
      var s = document.createElement('span');
      s.className = k < estado.i ? 'hecha' : (k === estado.i ? 'actual' : '');
      el.barra.appendChild(s);
    }
    el.progreso.textContent = 'Cepa ' + (estado.i + 1) + ' de ' + RONDA;
  }

  function muestraCepa() {
    var c = estado.ronda[estado.i];
    var _nueva = true;
    pintaBarra();
    el.revelacion.hidden = true; el.pasoA.hidden = el.pasoB.hidden = el.pasoC.hidden = true;
    el.form.hidden = false; el.input.disabled = false; el.comprobar.disabled = false; el.menos.disabled = el.mas.disabled = false;
    el.input.value = '';
    el.lienzo.style.setProperty('--pos', '0%'); el.lienzo.classList.remove('comparando');
    el.rango.value = 0; actualizaRango();
    limpia(el.svgA); limpia(el.svgB); limpia(el.capaA); limpia(el.capaB);
    el.lienzo.style.setProperty('--ratio', c.w + ' / ' + c.h);
    [el.svgA, el.svgB].forEach(function (sv) { sv.setAttribute('viewBox', '0 0 ' + c.w + ' ' + c.h); });
    el.tituloCepa.textContent = 'Cepa ' + (estado.i + 1);
    var etiqueta = $('etiqueta-resp');
    if (estado.modoTexto) {
      el.escena.hidden = true; el.desc.hidden = false;
      el.desc.innerHTML = '';
      var p = document.createElement('p'); p.textContent = 'Descripción de la imagen: ' + DESC[c.id];
      var q = document.createElement('p'); q.textContent = 'Entre las hojas se distinguen ' + plural(c.visibles, 'racimo', 'racimos') + ': ' + listaPos(c.con, c) + '.';
      el.desc.appendChild(p); el.desc.appendChild(q);
      etiqueta.textContent = '¿Cuántos racimos crees que hay en total, contando los que las hojas puedan tapar?';
      el.pregunta.textContent = 'Lee la descripción y calcula cuántos racimos hay en total.';
    } else {
      el.escena.hidden = false; el.desc.hidden = true;
      el.capaA.appendChild(pic(c.id, 'con_hojas', 'Fotografía de una cepa con hojas, sobre fondo claro. ' + DESC[c.id], c.w, c.h));
      el.pie.textContent = 'Cepa con hojas. Cuenta los racimos que veas.';
      etiqueta.textContent = '¿Cuántos racimos hay en esta cepa?';
      el.pregunta.textContent = 'Mira la imagen y escribe cuántos racimos crees que hay.';
    }
    arrancaReloj();
    anuncia('Cepa ' + (estado.i + 1) + ' de ' + RONDA + '.');
    el.tituloCepa.setAttribute('tabindex', '-1'); el.tituloCepa.focus({ preventScroll: true });
    window.irA($('juego-juego'));
  }

  function lee() { var v = parseInt(el.input.value, 10); return isNaN(v) ? null : Math.max(0, Math.min(99, v)); }
  function paso(d) { var v = lee(); v = v === null ? (d > 0 ? 1 : 0) : v + d; v = Math.max(0, Math.min(99, v)); el.input.value = v; anuncia(v + (v === 1 ? ' racimo' : ' racimos')); }

  function comprobar(ev) {
    ev.preventDefault();
    var v = lee();
    if (v === null) { anuncia('Escribe un número antes de comprobar.'); $('error-resp').hidden = false; el.input.focus(); return; }
    $('error-resp').hidden = true;
    var c = estado.ronda[estado.i];
    estado.resp[estado.i] = v;
    estado.tiempos[estado.i] = (Date.now() - estado.t0) / 1000; paraReloj();
    el.form.hidden = true;
    el.revelacion.hidden = false;
    var tu = $('tu-respuesta'); tu.textContent = 'Tu respuesta: ' + plural(v, 'racimo', 'racimos') + '.';
    if (estado.modoTexto) {
      el.comparador.hidden = true; el.leyenda.hidden = true;
      el.pasoA.hidden = false; $('paso-a-txt').textContent = 'Lo que puede ver una cámara: ' + plural(c.visibles, 'racimo', 'racimos') + '.' + (nIA(c) === null ? '' : ' La IA de Televitis contó ' + plural(nIA(c), 'racimo', 'racimos') + ' en esta foto.');
      revelaB(c);
      el.siguiente.focus({ preventScroll: true });
    } else {
      el.comparador.hidden = false; el.leyenda.hidden = false;
      c.con.forEach(function (b) { rect(el.svgA, b, 'caja-v'); });
      el.capaB.appendChild(pic(c.id, 'deshojada', 'La misma cepa sin hojas: los racimos quedan a la vista.', c.w, c.h));
      c.des.forEach(function (o) { rect(el.svgB, o.b, o.oculto ? 'caja-h' : 'caja-v'); });
      el.pasoA.hidden = false; $('paso-a-txt').textContent = 'Esto es lo que puede ver una cámara: ' + plural(c.visibles, 'racimo', 'racimos') + '.' + (nIA(c) === null ? '' : ' La IA de Televitis contó ' + plural(nIA(c), 'racimo', 'racimos') + '.');
      el.pie.textContent = 'Con hojas. Cajas continuas: racimos visibles para una cámara.';
      el.quitar.hidden = false; el.siguiente.hidden = true;
      anuncia('Tu respuesta: ' + v + '. ' + $('paso-a-txt').textContent + ' Pulsa «Quitar las hojas» para ver qué escondían.');
      el.quitar.focus({ preventScroll: true });
    }
  }

  function actualizaRango() {
    var v = parseInt(el.rango.value, 10);
    el.lienzo.style.setProperty('--pos', v + '%');
    el.lienzo.classList.toggle('comparando', v > 0 && v < 100);
    el.rango.setAttribute('aria-valuetext', v === 0 ? 'Imagen con hojas' : (v === 100 ? 'Imagen sin hojas' : v + ' % sin hojas, el resto con hojas'));
  }
  function mueve(a, cb) {
    var ini = parseInt(el.rango.value, 10);
    if (reducido() || ini === a) { el.rango.value = a; actualizaRango(); if (cb) cb(); return; }
    var t0 = null, dur = 900;
    function f(t) {
      if (t0 === null) t0 = t; var k = Math.min(1, (t - t0) / dur); var e = k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
      el.rango.value = Math.round(ini + (a - ini) * e); actualizaRango();
      if (k < 1) requestAnimationFrame(f); else if (cb) cb();
    }
    requestAnimationFrame(f);
  }

  function revelaB(c) {
    el.pasoB.hidden = false;
    $('paso-b-txt').textContent = 'Al quitar las hojas aparecen ' + plural(c.ocultos, 'racimo', 'racimos') + ' más' + (c.ocultos === 0 ? '' : ' (' + c.deshojada + ' en total).');
    if (estado.modoTexto && c.ocultos > 0) {
      var ocultos = c.des.filter(function (o) { return o.oculto; }).map(function (o) { return o.b; });
      $('paso-b-txt').textContent += ' Los ocultos estaban: ' + listaPos(ocultos, c) + '.';
    }
    el.pasoC.hidden = false;
    var m = c.ocultos === 0 ? 'Esta cepa era fácil: las hojas no escondían nada.' :
      (c.ocultos >= 3 ? 'Las hojas escondían ' + c.ocultos + ' racimos: ni tú ni la cámara podíais verlos.' :
        'Las hojas escondían ' + plural(c.ocultos, 'racimo', 'racimos') + ' que no se veían desde fuera.');
    $('paso-c-txt').textContent = m;
    el.siguiente.hidden = false;
    el.siguiente.textContent = estado.i === RONDA - 1 ? 'Ver el resultado' : 'Siguiente cepa';
    anuncia($('paso-b-txt').textContent + ' ' + m);
  }

  function quitar() {
    var c = estado.ronda[estado.i];
    el.quitar.disabled = true;
    mueve(100, function () {
      el.quitar.hidden = true; el.quitar.disabled = false;
      el.pie.textContent = 'Sin hojas. Línea continua: racimos que ya se veían. Línea discontinua: racimos que estaban ocultos.';
      revelaB(c);
      el.siguiente.focus({ preventScroll: true });
    });
  }

  function siguiente() {
    if (estado.i < RONDA - 1) { estado.i++; muestraCepa(); }
    else final();
  }

  function h(tag, cls, txt) { var e = document.createElement(tag); if (cls) e.className = cls; if (txt !== undefined) e.textContent = txt; return e; }
  function chip(ul, cls, etiqueta, valor, nota) {
    var li = h('li', cls); li.appendChild(h('span', 'c-et', etiqueta)); li.appendChild(h('span', 'c-num', valor)); if (nota) li.appendChild(h('span', 'c-nota', nota)); ul.appendChild(li);
  }
  function nIA(c) { var I = window.RACIMOS_IA && window.RACIMOS_IA[c.id]; return I ? I.n : null; }
  function pintaResumen(resp, vis, des, ia) {
    var ul = $('f-resumen'); limpia(ul);
    chip(ul, 'c-tu', 'Tú contaste', String(resp), 'racimos en total');
    if (ia !== null) chip(ul, 'c-ia', 'La IA contó', String(ia), 'racimos (modelo de Televitis)');
    chip(ul, 'c-cam', 'Una persona experta veía', String(vis), 'racimos en las fotos con hojas');
    chip(ul, 'c-real', 'Había de verdad', String(des), 'al quitar las hojas');
  }
  function pintaTiempos(tmed, media) {
    var C = window.COMPARATIVAS, d = C.datos(tmed, media);
    var ul = $('f-tiempos'); limpia(ul);
    chip(ul, 'c-tu', 'Tú', (tmed < 10 ? C.num(tmed, 1) : String(Math.round(tmed))) + ' s', 'por cepa, de media');
    chip(ul, 'c-ia', 'La IA', '2,5 ms', 'por imagen, en un ordenador potente (Jocher et al., 2026)');
    chip(ul, 'c-campo', 'Una persona en el campo', '≈ 4 min', 'por cepa: 15 min por cada 4 cepas (Jaramillo et al., 2021)');
    var v = $('f-vs-txt'); limpia(v);
    var p0 = h('p', 'vs-intro', 'Mientras tú terminabas una cepa, la IA habría analizado unas ');
    p0.appendChild(h('strong', 'rojo', C.miles(d.nIA))); p0.appendChild(document.createTextNode(' imágenes.')); v.appendChild(p0);
    v.appendChild(h('p', 'vs-intro', 'Para que te hagas una idea:'));
    var big = h('p', 'vs-big', 'Si la IA tardara ');
    big.appendChild(h('mark', 'm-ia', d.iaTxt)); big.appendChild(document.createTextNode(', tú tardarías ')); big.appendChild(h('mark', 'm-tu', d.humTxt)); big.appendChild(document.createTextNode('.'));
    v.appendChild(big);
    var q = h('p', 'vs-hito', d.rel + ' '); q.appendChild(h('strong', '', d.frase)); q.appendChild(document.createTextNode('.')); v.appendChild(q);
    var fig = $('f-vs-foto'), F = window.COMPARATIVAS_FOTOS && window.COMPARATIVAS_FOTOS[d.id], IC = window.COMPARATIVAS_ICONOS && window.COMPARATIVAS_ICONOS[d.id];
    var cap = $('f-vs-cap'); limpia(cap); $('f-vs-ico').hidden = true; $('f-vs-img').hidden = true;
    if (F) {
      $('f-vs-img').src = F.src; $('f-vs-img').alt = F.alt; $('f-vs-img').hidden = false;
      cap.appendChild(document.createTextNode(F.alt + '. Foto: ' + F.autor + (F.licencia ? ' (' + F.licencia + ')' : '') + '. '));
      if (F.url) { var a = h('a', '', 'Fuente'); a.href = F.url; a.rel = 'noopener'; cap.appendChild(a); }
      fig.hidden = false; $('f-vs').classList.add('con-foto');
    } else if (IC) {
      $('f-vs-ico').innerHTML = IC; $('f-vs-ico').hidden = false; cap.textContent = '';
      fig.hidden = false; $('f-vs').classList.add('con-foto');
    } else { fig.hidden = true; $('f-vs').classList.remove('con-foto'); }
    $('f-aviso').textContent = 'Eso sí: la IA solo cuenta lo que se ve. Detrás de las hojas hay racimos que solo una persona (o quitar las hojas) puede descubrir.';
  }

  function final() {
    el.play.hidden = true; el.fin.hidden = false;
    var r = estado.ronda, n = r.length, i;
    var cerca = 0, sumOc = 0, sumDes = 0, sumVis = 0, sumResp = 0, cercaTotal = 0;
    var cuerpo = $('tabla-cuerpo'); limpia(cuerpo);
    for (i = 0; i < n; i++) {
      var c = r[i], v = estado.resp[i];
      if (Math.abs(v - c.visibles) <= 1) cerca++;
      if (Math.abs(v - c.deshojada) <= 1) cercaTotal++;
      sumOc += c.ocultos; sumDes += c.deshojada; sumVis += c.visibles; sumResp += v;
      var tr = document.createElement('tr');
      var th = document.createElement('th'); th.scope = 'row'; th.textContent = 'Cepa ' + (i + 1); tr.appendChild(th);
      [v, (nIA(c) === null ? '—' : nIA(c)), c.visibles, c.ocultos, c.deshojada].forEach(function (x) { var td = document.createElement('td'); td.textContent = x; tr.appendChild(td); });
      cuerpo.appendChild(tr);
    }
    pintaTiempos(estado.tiempos.reduce(function (a, b) { return a + b; }, 0) / n, sumResp / n);
    var pct = sumDes ? Math.round(100 * sumOc / sumDes) : 0;
    var primario = estado.modoTexto ? cercaTotal : cerca;
    $('f-cerca').textContent = primario + ' de ' + n;
    $('f-cerca-txt').textContent = estado.modoTexto
      ? 'cepas en las que tu estimación quedó a ±1 racimo de los que había al quitar las hojas.'
      : 'cepas en las que tu respuesta quedó a ±1 racimo de lo que ve una cámara.';
    $('f-pct').textContent = pct + ' %';
    $('f-pct-txt').textContent = 'de los racimos de estas cinco cepas (' + sumOc + ' de ' + sumDes + ') estaban escondidos por las hojas.';
    var sumIA = 0, hayIA = true; r.forEach(function (c) { var k = nIA(c); if (k === null) hayIA = false; else sumIA += k; });
    pintaResumen(sumResp, sumVis, sumDes, hayIA ? sumIA : null);
    $('f-compartir').setAttribute('data-texto', 'En «Entre cepas» he contado racimos en ' + n + ' cepas y mi respuesta quedó a ±1 racimo en ' + primario + ' de ' + n + '. Detrás de las hojas se escondía un ' + pct + ' % de los racimos. ¿Puedes hacerlo mejor?');
    // mejor ronda (solo en este navegador)
    var mejor = null; try { mejor = parseInt(window.localStorage.getItem(KEY), 10); } catch (e) { mejor = null; }
    if (isNaN(mejor)) mejor = null;
    var nuevo = mejor === null || primario > mejor;
    if (nuevo) { try { window.localStorage.setItem(KEY, String(primario)); } catch (e) { /* sin almacenamiento: no pasa nada */ } mejor = primario; }
    $('f-mejor').textContent = (nuevo ? 'Nuevo récord en este navegador: ' : 'Tu mejor ronda en este navegador: ') + mejor + ' de ' + n + '.';
    anuncia('Ronda terminada. ' + $('f-cerca').textContent + ' ' + $('f-cerca-txt').textContent);
    var h = $('titulo-final'); h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true });
    window.irA(el.fin);
  }

  /* ---------- eventos ---------- */
  el.empezar.addEventListener('click', empezar);
  $('otra').addEventListener('click', function () { estado.modoTexto = el.modoDesc.checked; empezar(); });
  el.menos.addEventListener('click', function () { paso(-1); });
  el.mas.addEventListener('click', function () { paso(1); });
  el.form.addEventListener('submit', comprobar);
  el.quitar.addEventListener('click', quitar);
  el.rango.addEventListener('input', actualizaRango);
  el.verSin.addEventListener('click', function () { mueve(100); });
  el.ponerHojas.addEventListener('click', function () { mueve(0); });
  el.siguiente.addEventListener('click', siguiente);
})();
