/* Bloque «¿Y la rapidez?»: tú frente a la IA. Compartido por los retos de mildiu y fases. */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  function h(tag, cls, txt) { var e = document.createElement(tag); if (cls) e.className = cls; if (txt !== undefined) e.textContent = txt; return e; }
  function limpia(n) { while (n.firstChild) n.removeChild(n.firstChild); }
  function chip(ul, cls, et, val, nota) { var li = h('li', cls); li.appendChild(h('span', 'c-et', et)); li.appendChild(h('span', 'c-num', val)); if (nota) li.appendChild(h('span', 'c-nota', nota)); ul.appendChild(li); }
  /* o: { tmed, unidad, ia: {s, txt, nota}, aviso } */
  window.EntreCepasVs = {
    fmt: function (sg) { var m = Math.floor(sg / 60), r = Math.floor(sg % 60); return m + ':' + (r < 10 ? '0' : '') + r; },
    pinta: function (o) {
      var C = window.COMPARATIVAS, d = C.datos(o.tmed, 0, o.ia.s);
      var ul = $('f-tiempos'); limpia(ul);
      chip(ul, 'c-tu', 'Tú', (o.tmed < 10 ? C.num(o.tmed, 1) : String(Math.round(o.tmed))) + ' s', o.unidad + ', de media');
      chip(ul, 'c-ia', 'La IA', o.ia.txt, o.ia.nota);
      var v = $('f-vs-txt'); limpia(v);
      var p0 = h('p', 'vs-intro', 'Mientras tú decidías una ' + (o.unidad === 'por foto' ? 'foto' : 'imagen') + ', la IA habría analizado unas ');
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
      } else if (IC) { $('f-vs-ico').innerHTML = IC; $('f-vs-ico').hidden = false; cap.textContent = ''; fig.hidden = false; $('f-vs').classList.add('con-foto'); }
      else { fig.hidden = true; $('f-vs').classList.remove('con-foto'); }
      $('f-aviso').textContent = o.aviso;
    }
  };
})();
