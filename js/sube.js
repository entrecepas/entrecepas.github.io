(function () {
  'use strict';
  var f = document.getElementById('sube-foto'); if (!f) return;
  var form = document.getElementById('sube-form'), tarea = form.getAttribute('data-tarea');
  var vista = document.getElementById('sube-vista'), img = document.getElementById('sube-img'), msg = document.getElementById('sube-msg');
  var res = document.getElementById('sube-res'), cv = document.getElementById('sube-canvas'), txt = document.getElementById('sube-txt');
  var btn = document.getElementById('sube-ok');
  var url = null, ortP = null, sesiones = {};
  var MEAN = [0.485, 0.456, 0.406], STD = [0.229, 0.224, 0.225];

  var origen = null, marcado = null, verMarcas = true;
  var tog = document.createElement('button'); tog.type = 'button'; tog.className = 'btn secundario'; tog.id = 'sube-toggle'; tog.hidden = true;
  tog.setAttribute('aria-pressed', 'true'); tog.textContent = 'Ocultar las marcas de la IA';
  if (res) res.appendChild(tog);
  function guardaMarcado() { try { marcado = cv.getContext('2d').getImageData(0, 0, cv.width, cv.height); verMarcas = true; tog.hidden = !origen; tog.setAttribute('aria-pressed', 'true'); tog.textContent = 'Ocultar las marcas de la IA'; } catch (e) { tog.hidden = true; } }
  tog.addEventListener('click', function () {
    var c = cv.getContext('2d'); verMarcas = !verMarcas;
    if (verMarcas && marcado) c.putImageData(marcado, 0, 0); else if (origen) c.drawImage(origen, 0, 0, cv.width, cv.height);
    tog.setAttribute('aria-pressed', String(verMarcas)); tog.textContent = verMarcas ? 'Ocultar las marcas de la IA' : 'Ver las marcas de la IA';
  });
  function aviso(t) { msg.hidden = false; msg.textContent = t; }
  function cargaOrt() {
    if (ortP) return ortP;
    ortP = new Promise(function (ok, ko) {
      var s = document.createElement('script'); s.src = 'js/vendor/ort/ort.wasm.min.js';
      s.onload = function () { ort.env.wasm.wasmPaths = new URL('js/vendor/ort/', document.baseURI).href; ort.env.wasm.numThreads = 1; ok(ort); };
      s.onerror = function () { ko(new Error('ort')); }; document.head.appendChild(s);
    });
    return ortP;
  }
  var propio = null; // ArrayBuffer de un modelo cargado por la persona usuaria
  function sesion(nombre) {
    if (propio) { if (!sesiones._propio) sesiones._propio = cargaOrt().then(function (o) { return o.InferenceSession.create(propio, { executionProviders: ['wasm'] }); }); return sesiones._propio; }
    if (!sesiones[nombre]) sesiones[nombre] = cargaOrt().then(function (o) { return o.InferenceSession.create('models/' + nombre + '.onnx', { executionProviders: ['wasm'] }); });
    return sesiones[nombre];
  }
  function existe(u) {
    var get = function () { return fetch(u, { headers: { Range: 'bytes=0-0' } }).then(function (r) { return r.ok; }, function () { return false; }); };
    return fetch(u, { method: 'HEAD' }).then(function (r) { return r.ok ? true : get(); }, get);
  }
  function pausa() { return new Promise(function (r) { setTimeout(r, 0); }); }

  var ejemplo = false;
  var mp = document.getElementById('sube-modelo');
  if (mp) mp.addEventListener('change', function () {
    var a = mp.files && mp.files[0], st = document.getElementById('sube-modelo-estado');
    if (!a) return;
    st.textContent = 'Cargando el modelo…';
    a.arrayBuffer().then(function (buf) {
      propio = buf; delete sesiones._propio;
      return sesion(tarea);
    }).then(function () {
      f.disabled = false; st.textContent = 'Modelo «' + a.name + '» cargado en tu navegador. Ya puedes elegir una foto propia y analizarla.';
    }).catch(function () { propio = null; delete sesiones._propio; st.textContent = 'No he podido abrir ese archivo como modelo ONNX. Revisa el formato.'; });
  });
  if (location.protocol !== 'file:') existe('models/' + (tarea === 'racimos' ? 'racimos' : 'mildiu') + '.onnx').then(function (ok) {
    var n = document.getElementById('sube-nota-modelo'); if (!ok && n) { n.hidden = false; f.disabled = true; }
  });
  Array.prototype.forEach.call(document.querySelectorAll('[data-ejemplo]'), function (b) {
    b.addEventListener('click', function () {
      if (url && !ejemplo) URL.revokeObjectURL(url);
      f.value = ''; url = b.getAttribute('data-ejemplo'); ejemplo = true;
      if (res) res.hidden = true; msg.hidden = true;
      img.src = url; img.alt = 'Foto de ejemplo: ' + b.textContent; vista.hidden = false;
      form.requestSubmit ? form.requestSubmit() : btn.click();
    });
  });
  f.addEventListener('change', function () { ejemplo = false; img.alt = 'Vista previa de la foto que has elegido';
    if (url && !ejemplo) URL.revokeObjectURL(url); url = null;
    if (res) res.hidden = true; msg.hidden = true;
    var a = f.files && f.files[0];
    if (!a || a.type.indexOf('image/') !== 0) { vista.hidden = true; return; }
    url = URL.createObjectURL(a); img.src = url; vista.hidden = false;
  });

  function leerImagen() {
    return new Promise(function (ok, ko) {
      var im = new Image(); im.onload = function () { ok(im); }; im.onerror = ko; im.src = url;
    });
  }

  /* ---------- Mildiu: segmentación por teselas (U-Net, 224×224) ---------- */
  function mildiu(im) {
    var L = 1280, k = Math.min(1, L / Math.max(im.naturalWidth, im.naturalHeight));
    var W = Math.round(im.naturalWidth * k), H = Math.round(im.naturalHeight * k);
    cv.width = W; cv.height = H; var c = cv.getContext('2d', { willReadFrequently: true });
    c.drawImage(im, 0, 0, W, H);
    var base = c.getImageData(0, 0, W, H), out = c.createImageData(W, H); out.data.set(base.data);
    var t = Math.max(64, Math.round(Math.max(W, H) / 6)), th = 0.95, marcados = 0;
    var tc = document.createElement('canvas'); tc.width = tc.height = 224; var tx = tc.getContext('2d', { willReadFrequently: true });
    var tiles = []; for (var y = 0; y < H; y += t) for (var x = 0; x < W; x += t) tiles.push([x, y]);
    var t0 = performance.now();
    return sesion('mildiu').then(function (s) {
      var i = 0;
      function paso() {
        if (i >= tiles.length) return Promise.resolve();
        var x0 = tiles[i][0], y0 = tiles[i][1], w = Math.min(t, W - x0), h = Math.min(t, H - y0); i++;
        aviso('Analizando… ' + Math.round(i / tiles.length * 100) + ' %');
        tx.clearRect(0, 0, 224, 224); tx.drawImage(cv, x0, y0, w, h, 0, 0, 224, 224);
        var d = tx.getImageData(0, 0, 224, 224).data, a = new Float32Array(3 * 224 * 224);
        for (var p = 0; p < 224 * 224; p++) for (var ch = 0; ch < 3; ch++) a[ch * 224 * 224 + p] = (d[p * 4 + ch] / 255 - MEAN[ch]) / STD[ch];
        var fe = {}; fe[s.inputNames[0]] = new ort.Tensor('float32', a, [1, 3, 224, 224]);
        return s.run(fe).then(function (r) {
          var t = r[s.outputNames[0]], pr = t.data, N = 224 * 224;
          if (t.dims.length === 4 && t.dims[1] === 2) { var q2 = new Float32Array(N); for (var z = 0; z < N; z++) { var e0 = Math.exp(pr[z]), e1 = Math.exp(pr[N + z]); q2[z] = e1 / (e0 + e1); } pr = q2; }
          else { var fuera = false; for (var z2 = 0; z2 < N; z2 += 997) if (pr[z2] < 0 || pr[z2] > 1) { fuera = true; break; } if (fuera) { var q1 = new Float32Array(N); for (var z3 = 0; z3 < N; z3++) q1[z3] = 1 / (1 + Math.exp(-pr[z3])); pr = q1; } }
          for (var yy = 0; yy < h; yy++) for (var xx = 0; xx < w; xx++) {
            var q = pr[Math.min(223, Math.floor(yy * 224 / h)) * 224 + Math.min(223, Math.floor(xx * 224 / w))];
            if (q > th) { var o = ((y0 + yy) * W + x0 + xx) * 4; out.data[o] = out.data[o] * .55 + 255 * .45; out.data[o + 1] = out.data[o + 1] * .55; out.data[o + 2] = out.data[o + 2] * .55 + 200 * .45; marcados++; }
          }
        }).then(pausa).then(paso);
      }
      return paso();
    }).then(function () {
      c.putImageData(out, 0, 0);
      var pct = marcados / (W * H) * 100, ms = Math.round(performance.now() - t0);
      txt.textContent = (pct < 0.5 ? 'No se ven señales claras de mildiu en esta foto. ' : 'La IA marca en rosa las zonas que podrían tener mildiu: ' + pct.toFixed(1).replace('.', ',') + ' % de la imagen. ') +
        'Ha tardado ' + (ms / 1000).toFixed(1).replace('.', ',') + ' s en tu dispositivo. Es una ayuda para mirar, no un diagnóstico: la decisión es de una persona.';
      cv.setAttribute('aria-label', 'Tu foto con las zonas sospechosas de mildiu marcadas en rosa');
    });
  }

  /* ---------- Racimos: detector YOLO (ONNX) ---------- */
  function racimos(im) {
    var S = 640, W = im.naturalWidth, H = im.naturalHeight, r = Math.min(S / W, S / H), nw = Math.round(W * r), nh = Math.round(H * r), px = Math.floor((S - nw) / 2), py = Math.floor((S - nh) / 2);
    var tc = document.createElement('canvas'); tc.width = tc.height = S; var tx = tc.getContext('2d', { willReadFrequently: true });
    tx.fillStyle = 'rgb(114,114,114)'; tx.fillRect(0, 0, S, S); tx.drawImage(im, px, py, nw, nh);
    var d = tx.getImageData(0, 0, S, S).data, a = new Float32Array(3 * S * S);
    for (var p = 0; p < S * S; p++) { a[p] = d[p * 4] / 255; a[S * S + p] = d[p * 4 + 1] / 255; a[2 * S * S + p] = d[p * 4 + 2] / 255; }
    var K = Math.min(1, 1280 / Math.max(W, H)); cv.width = Math.round(W * K); cv.height = Math.round(H * K);
    var c = cv.getContext('2d'); c.drawImage(im, 0, 0, cv.width, cv.height);
    var t0 = performance.now();
    return sesion('racimos').then(function (s) {
      return s.run({ [s.inputNames[0]]: new ort.Tensor('float32', a, [1, 3, S, S]) });
    }).then(function (o) {
      var t = o[Object.keys(o)[0]], dm = t.dims, v = t.data, cajas = [], umbral = 0.25;
      if (dm[2] === 6) { // NMS integrado: [1,N,6] x1,y1,x2,y2,conf,cls
        for (var i = 0; i < dm[1]; i++) { var b = v.subarray(i * 6, i * 6 + 6); if (b[4] >= umbral) cajas.push([b[0], b[1], b[2], b[3], b[4]]); }
      } else { // [1, 4+nc, N] cx,cy,w,h,scores…
        var nc = dm[1] - 4, N = dm[2];
        for (var j = 0; j < N; j++) {
          var m = 0; for (var q = 0; q < nc; q++) m = Math.max(m, v[(4 + q) * N + j]);
          if (m >= umbral) { var cx = v[j], cy = v[N + j], w = v[2 * N + j], h = v[3 * N + j]; cajas.push([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, m]); }
        }
        cajas.sort(function (u, w2) { return w2[4] - u[4]; });
        var keep = [];
        cajas.forEach(function (b) {
          for (var k = 0; k < keep.length; k++) {
            var e = keep[k], ix = Math.max(0, Math.min(b[2], e[2]) - Math.max(b[0], e[0])), iy = Math.max(0, Math.min(b[3], e[3]) - Math.max(b[1], e[1])), I = ix * iy;
            if (I / ((b[2] - b[0]) * (b[3] - b[1]) + (e[2] - e[0]) * (e[3] - e[1]) - I) > 0.45) return;
          }
          keep.push(b);
        });
        cajas = keep;
      }
      c.lineWidth = Math.max(5, cv.width / 180); c.strokeStyle = '#FFD21F'; c.font = 'bold ' + Math.max(20, cv.width / 40) + 'px Inter,sans-serif'; c.fillStyle = '#FFD21F';
      cajas.forEach(function (b, n) {
        var x1 = (b[0] - px) / r * K, y1 = (b[1] - py) / r * K, x2 = (b[2] - px) / r * K, y2 = (b[3] - py) / r * K;
        c.strokeRect(x1, y1, x2 - x1, y2 - y1); c.fillText(String(n + 1), x1 + 4, y1 + Math.max(16, cv.width / 55));
      });
      var ms = Math.round(performance.now() - t0);
      txt.textContent = 'La IA ha contado ' + cajas.length + (cajas.length === 1 ? ' racimo' : ' racimos') + ' visibles en tu foto (' + (ms / 1000).toFixed(1).replace('.', ',') + ' s). Los racimos tapados por las hojas no se pueden contar desde una foto, así que el recuento real puede ser mayor.';
      cv.setAttribute('aria-label', 'Tu foto con ' + cajas.length + ' racimos marcados con cajas amarillas');
    });
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!url) { aviso('Primero elige una foto o prueba con una de ejemplo.'); return; }
    btn.disabled = true; res.hidden = true;
    if (location.protocol === 'file:') { aviso('Para analizar fotos, la web tiene que abrirse desde su dirección de internet o con el archivo ABRIR_WEB.bat (el navegador no deja cargar los modelos desde un archivo abierto directamente).'); btn.disabled = false; return; }
    var modelo = tarea === 'racimos' ? 'racimos' : 'mildiu';
    (propio ? Promise.resolve(true) : existe('models/' + modelo + '.onnx')).then(function (ok) {
      if (!ok) {
        var E = ejemplo && window.LAB_EJEMPLOS && window.LAB_EJEMPLOS[url];
        if (!E) { aviso('En esta versión en línea, el análisis de fotos propias no está disponible: los modelos de IA no se publican. Prueba con las fotos de ejemplo de arriba para ver el resultado.'); return; }
        return new Promise(function (ok2, ko2) { var im = new Image(); im.onload = function () { cv.width = im.naturalWidth; cv.height = im.naturalHeight; cv.getContext('2d').drawImage(im, 0, 0); var o = new Image(); o.onload = function () { origen = o; guardaMarcado(); }; o.src = url; cv.setAttribute('aria-label', E.aria); txt.textContent = E.txt; msg.hidden = true; res.hidden = false; res.scrollIntoView({ block: 'nearest' }); ok2(); }; im.onerror = ko2; im.src = E.img; });
      }
      aviso('Cargando el modelo de IA (la primera vez tarda unos segundos)…');
      return leerImagen().then(function (im) { origen = im; return (tarea === 'racimos' ? racimos : mildiu)(im); }).then(function () { guardaMarcado(); msg.hidden = true; res.hidden = false; res.scrollIntoView({ block: 'nearest' }); });
    }).catch(function () { aviso('No he podido analizar la foto en este dispositivo. Prueba con otra foto o con otro navegador.'); })
      .then(function () { btn.disabled = false; });
  });
})();
