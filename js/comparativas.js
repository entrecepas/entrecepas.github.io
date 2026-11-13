/* Comparativas humor-científicas: tú vs. la IA. Duraciones aproximadas, en segundos. */
(function () {
  'use strict';
  var IA_S = 0.0025; // YOLO26s, 2,5 ms/imagen en GPU T4 con TensorRT, 640 px, solo el modelo (Jocher et al., 2026)
  var D = 86400, A = 365 * D;
  // [duración en segundos, "lo que ..." (completa la frase «más o menos…»)]
  var HITOS = [
    [0.3, 'lo que dura un parpadeo', 'parpadeo'],
    [0.8, 'lo que dura un latido del corazón', 'latido'],
    [500, 'lo que tarda la luz del Sol en llegar a la Tierra (unos 8 minutos)', 'luz-sol'],
    [210, 'lo que dura una canción pop', 'cancion-pop'],
    [600, 'lo que se tarda en cocer un huevo duro', 'huevo-duro'],
    [2700, 'lo que se tarda en hacer una tortilla de patata', 'tortilla'],
    [5400, 'lo que dura un partido de fútbol', 'partido-futbol'],
    [5520, 'lo que tarda la Estación Espacial Internacional en dar una vuelta a la Tierra (unos 92 minutos)', 'iss'],
    [7200, 'lo que dura una película o un maratón de élite', 'pelicula-maraton'],
    [28800, 'lo que dura un vuelo de Madrid a Nueva York', 'vuelo-nueva-york'],
    [D, 'lo que dura un día entero', 'dia-entero'],
    [8 * D, 'lo que duró el viaje de Apolo 11 a la Luna y de vuelta (unos 8 días)', 'apolo-11'],
    [10 * D, 'lo que dura la fermentación alcohólica de un vino tinto', 'fermentacion'],
    [16 * D, 'lo que duran unos Juegos Olímpicos enteros', 'juegos-olimpicos'],
    [21 * D, 'lo que dura un Tour de Francia', 'tour-francia'],
    [29 * D, 'lo que dura un Mundial de fútbol', 'mundial-futbol'],
    [33 * D, 'lo que se tarda en hacer el Camino de Santiago francés a pie', 'camino-santiago'],
    [180 * D, 'lo que dura el ciclo de la vid desde la brotación hasta la vendimia', 'ciclo-vid'],
    [210 * D, 'lo que dura un viaje a Marte (unos 7 meses)', 'viaje-marte'],
    [270 * D, 'lo que dura un embarazo humano', 'embarazo'],
    [410 * D, 'lo que se tardó en construir el Empire State (410 días)', 'empire-state'],
    [660 * D, 'lo que dura la gestación de una elefanta', 'elefanta'],
    [2 * A, 'lo que envejece un vino de crianza de Rioja', 'crianza-rioja'],
    [2.2 * A, 'lo que se tardó en construir la Torre Eiffel', 'torre-eiffel'],
    [3 * A, 'lo que envejece un reserva de Rioja, o lo que duró la vuelta al mundo de Elcano', 'reserva-elcano'],
    [4 * A, 'lo que dura un Grado en Enología, o lo que se tardó en construir el Golden Gate', 'grado-golden-gate'],
    [5 * A, 'lo que envejece un gran reserva de Rioja, o lo que se tardó en construir el Cristo Redentor', 'gran-reserva-cristo'],
    [6 * A, 'lo que se tardó en construir el Burj Khalifa', 'burj-khalifa'],
    [10 * A, 'lo que se tardó en excavar el canal de Panamá o el de Suez', 'canal-panama'],
    [14 * A, 'lo que se tardó en construir la Ópera de Sídney', 'opera-sidney'],
    [20 * A, 'lo que se tardó en construir la Gran Pirámide de Guiza o el Taj Mahal', 'piramide-taj-mahal'],
    [34 * A, 'los años que lleva existiendo la Universidad de La Rioja (desde 1992)', 'universidad-rioja'],
    [80 * A, 'lo que dura una vida humana larga', 'vida-larga'],
    [140 * A, 'lo que llevan las obras de la Sagrada Familia (desde 1882)', 'sagrada-familia'],
    [180 * A, 'lo que se tardó en construir la catedral de Notre-Dame de París', 'notre-dame'],
    [534 * A, 'el tiempo que ha pasado desde que Colón llegó a América', 'colon']
  ];
  var UNIDADES = [[1, '1 segundo'], [10, '10 segundos'], [60, '1 minuto'], [600, '10 minutos'], [3600, '1 hora'], [D, '1 día'], [7 * D, '1 semana'], [30 * D, '1 mes'], [A, '1 año']];

  function num(x, dec) { var s = x.toFixed(dec); return s.replace('.', ','); }
  function dur(s) {
    if (s < 120) { var q = Math.round(s); return q + (q === 1 ? ' segundo' : ' segundos'); }
    if (s < 7200) return Math.round(s / 60) + ' minutos';
    if (s < 2 * D) return Math.round(s / 3600) + ' horas';
    if (s < 60 * D) return Math.round(s / D) + ' días';
    if (s < 2 * A) return Math.round(s / (30 * D)) + ' meses';
    if (s < 10 * A) return num(s / A, 1) + ' años';
    return Math.round(s / A).toLocaleString('es-ES') + ' años';
  }
  function miles(n) { return Math.round(n).toLocaleString('es-ES'); }

  function elige(R) {
    var mejores = [], mejor = null;
    UNIDADES.forEach(function (u) {
      var B = R * u[0];
      HITOS.forEach(function (h) {
        var d = Math.abs(Math.log(B / h[0]));
        var c = { u: u, B: B, h: h, d: d };
        if (d < 0.3) mejores.push(c);
        if (!mejor || d < mejor.d) mejor = c;
      });
    });
    return mejores.length ? mejores[Math.floor(Math.random() * mejores.length)] : mejor;
  }

  function datos(tmedS, mediaRacimos, iaS) {
    var R = tmedS / (iaS || IA_S), c = elige(R);
    return {
      ts: Math.max(1, Math.round(tmedS)), media: mediaRacimos, nIA: Math.round(R),
      iaTxt: c.u[1], humTxt: dur(c.B), id: c.h[2], frase: c.h[1],
      rel: c.B < c.h[0] * 0.9 ? 'casi' : (c.B > c.h[0] * 1.1 ? 'algo más de' : 'justo')
    };
  }
  window.COMPARATIVAS = { datos: datos, miles: miles, num: num, hitos: HITOS, elige: elige, iaSegundos: IA_S };
})();
