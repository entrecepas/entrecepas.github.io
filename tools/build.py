#!/usr/bin/env python3
"""Genera las páginas HTML estáticas de «Entre cepas» (cabecera/pie comunes) y comprueba marcadores.
Uso:  python3 tools/build.py            (borrador: deja pasar los marcadores PROVISIONAL)
      python3 tools/build.py --final    (falla si queda algún marcador o «a verificar» visible)
Todo el contenido visible está en este archivo para revisarlo de una vez.
Las cifras de los artículos salen de sus resúmenes; cada una lleva su referencia."""
import json, os, re, sys, html

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
FINAL = '--final' in sys.argv
TITULO = 'Entre cepas'
LEMA = 'Tú contra la IA en el viñedo'
AUTOR = 'Rubén Iñiguez Mangado'
SITE_URL = os.environ.get('SITE_URL', '').rstrip('/')  # p. ej. SITE_URL=https://usuario.github.io/entre-cepas python3 tools/build.py
DESC_SITIO = 'Retos interactivos para poner a prueba tu ojo contra la inteligencia artificial en el viñedo, con imágenes y datos reales de investigación del ICVV y la Universidad de La Rioja.'

# ---------------- referencias (una sola vez, se reutilizan) ----------------
def doi(d): return f'<a href="https://doi.org/{d}">doi:{d}</a>'
REF = {
 'ini2024': ('Íñiguez, R., Gutiérrez, S., Poblete-Echeverría, C., Hernández, I., Barrio, I. y Tardáguila, J. (2024). Deep learning modelling for non-invasive grape bunch detection under diverse occlusion conditions. <em>Computers and Electronics in Agriculture</em>, 226, 109421.', '10.1016/j.compag.2024.109421'),
 'ini2021': ('Íñiguez, R., Palacios, F., Barrio, I., Hernández, I., Gutiérrez, S. y Tardaguila, J. (2021). Impact of leaf occlusions on yield assessment by computer vision in commercial vineyards. <em>Agronomy</em>, 11, 1003.', '10.3390/agronomy11051003'),
 'coo1995': ('Coombe, B. G. (1995). Growth stages of the grapevine: adoption of a system for identifying grapevine growth stages. <em>Australian Journal of Grape and Wine Research</em>, 1(2), 104–110.', '10.1111/j.1755-0238.1995.tb00086.x'),
 'bag1952': ('Baggiolini, M. (1952). Les stades repères dans le développement annuel de la vigne et leur utilisation pratique. <em>Revue Romande d’Agriculture, de Viticulture et d’Arboriculture</em>, 8(1), 4–6.', None),
 'icvv2020': ('Instituto de Ciencias de la Vid y del Vino [ICVV] (2020, 16 de marzo). <em>Reportaje del Banco de Germoplasma de La Grajera en el suplemento Agro del periódico La Rioja</em>. ICVV (Gobierno de La Rioja, CSIC y Universidad de La Rioja).', None),
 'joc2026': ('Jocher, G., Qiu, J., Liu, M., Lyu, S., Akyon, F. C. y Kalfaoglu, M. E. (2026). Ultralytics YOLO26: Unified real-time end-to-end vision models. <em>arXiv</em>:2606.03748.', '10.48550/arXiv.2606.03748'),
 'pal2020': ('Palacios, F., Bueno, G., Salido, J., Diago, M. P., Hernández, I. y Tardaguila, J. (2020). Automated grapevine flower detection and quantification method based on computer vision and deep learning from on-the-go imaging using a mobile sensing platform under field conditions. <em>Computers and Electronics in Agriculture</em>, 178, 105796.', '10.1016/j.compag.2020.105796'),
 'jar2021': ('Jaramillo, J., Vanden Heuvel, J. y Petersen, K. H. (2021). Low-cost, computer vision-based, prebloom cluster count prediction in vineyards. <em>Frontiers in Agronomy</em>, 3, 648080.', '10.3389/fagro.2021.648080'),
 'ini2025a': ('Íñiguez, R., Poblete-Echeverría, C., Barrio, I., Hernández, I., Gutiérrez, S., Martínez-Cámara, E. y Tardáguila, J. (2025a). Impact of phenological and lighting conditions on early detection of grapevine inflorescences and bunches using deep learning. <em>Agriculture</em>, 15, 1495.', '10.3390/agriculture15141495'),
 'ini2025b': ('Íñiguez, R., Wolela, F., Gonzalez Pavez, M. I., Barrio, I., Tardáguila, J., Venter, T. y Poblete-Echeverría, C. (2025b). Artificial intelligence-driven classification method of grapevine major phenological stages using conventional RGB imaging. <em>OENO One</em>, 59(2).', '10.20870/oeno-one.2025.59.2.9306'),
 'pob2025': ('Poblete-Echeverría, C., Berry, A., Venter, T., Velez, S., Gonzalez Pavez, M. I. e Íñiguez, R. (2025a). Morphological image analysis for estimating grape bunch weight under different irrigation regimes in Cabernet-Sauvignon. <em>OENO One</em>, 59(2).', '10.20870/oeno-one.2025.59.2.9309'),
 'her2025': ('Hernández, I., Silva, R., Melo-Pinto, P., Gutiérrez, S. y Tardaguila, J. (2025). Early detection of downy mildew in vineyards using deep neural networks for semantic segmentation. <em>Biosystems Engineering</em>, 252, 15–31.', '10.1016/j.biosystemseng.2025.02.007'),
 'her2024b': ('Hernández, I., Gutiérrez, S. y Tardaguila, J. (2024a). Image analysis with deep learning for early detection of downy mildew in grapevine. <em>Scientia Horticulturae</em>, 331, 113155.', '10.1016/j.scienta.2024.113155'),
 'her2024': ('Hernández, I., Gutiérrez, S., Barrio, I., Íñiguez, R. y Tardaguila, J. (2024b). In-field disease symptom detection and localisation using explainable deep learning: use case for downy mildew in grapevine. <em>Computers and Electronics in Agriculture</em>, 226, 109478.', '10.1016/j.compag.2024.109478'),
 'her2021': ('Hernández, I., Gutiérrez, S., Ceballos, S., Íñiguez, R., Barrio, I. y Tardaguila, J. (2021). Artificial intelligence and novel sensing technologies for assessing downy mildew in grapevine. <em>Horticulturae</em>, 7(5), 103.', '10.3390/horticulturae7050103'),
 'oiv2019': ('OIV (2019). <em>Definición y principios generales de la OIV en materia de viticultura de precisión</em> (Resolución OIV-VITI 593-2019). Organización Internacional de la Viña y el Vino. <a href="https://www.oiv.int/es/node/3113">oiv.int/es/node/3113</a>', None),
 'tej2026': ('Tejada-González, A., Barrio, I., Poggi, L., Fernández-Novales, J., Martínez-Lapuente, L., Guadalupe, Z. y Diago, M. P. (2026). On-the-go hyperspectral imaging for monitoring grape maturity in Tempranillo: supporting adaptive harvest decisions. <em>OENO One</em>, 60(3), 9877.', '10.20870/oeno-one.2026.60.3.9877'),
 'hyp': ('HyperGrape (2025). <em>HyperGrape: desarrollando la aplicación de tecnologías no invasivas para monitorizar en tiempo real y a la entrada de bodega la composición de la uva</em> (PID2023-150555OB-I00). Universidad de La Rioja (grupo Televitis, ICVV); financiado por MICIU/AEI/10.13039/501100011033 y FEDER, UE. <a href="https://hypergrape.unirioja.es/">hypergrape.unirioja.es</a>', None),
 'del2021': ('Del Frari, G., Oliveira, H. y Boavida Ferreira, R. (2021). White rot fungi (Hymenochaetales) and esca of grapevine: insights from recent microbiome studies. <em>Journal of Fungi</em>, 7(9), 770.', '10.3390/jof7090770'),
 'mug1999': ('Mugnai, L., Graniti, A. y Surico, G. (1999). Esca (black measles) and brown wood-streaking: two old and elusive diseases of grapevines. <em>Plant Disease</em>, 83(5), 404–418.', '10.1094/PDIS.1999.83.5.404'),
 'ots1979': ('Otsu, N. (1979). A threshold selection method from gray-level histograms. <em>IEEE Transactions on Systems, Man, and Cybernetics</em>, 9(1), 62–66.', '10.1109/TSMC.1979.4310076'),
 'ges2011': ('Gessler, C., Pertot, I. y Perazzolli, M. (2011). <em>Plasmopara viticola</em>: a review of knowledge on downy mildew of grapevine and effective disease management. <em>Phytopathologia Mediterranea</em>, 50(1), 3–44.', 'https://doi.org/10.14601/Phytopathol_Mediterr-9360'),
 'gad2012': ('Gadoury, D. M., Cadle-Davidson, L., Wilcox, W. F., Dry, I. B., Seem, R. C. y Milgroom, M. G. (2012). Grapevine powdery mildew (<em>Erysiphe necator</em>): a fascinating system for the study of the biology, ecology and epidemiology of an obligate biotroph. <em>Molecular Plant Pathology</em>, 13(1), 1–16.', '10.1111/j.1364-3703.2011.00728.x'),
 'lau2021': ('Laurent, C., Oger, B., Taylor, J. A., Scholasch, T., Metay, A. y Tisseyre, B. (2021). A review of the issues, methods and perspectives for yield estimation, prediction and forecasting in viticulture. <em>European Journal of Agronomy</em>, 130, 126339.', '10.1016/j.eja.2021.126339'),
 'tar2021': ('Tardaguila, J., Stoll, M., Gutiérrez, S., Proffitt, T. y Diago, M. P. (2021). Smart applications and digital technologies in viticulture: a review. <em>Smart Agricultural Technology</em>, 1, 100005.', '10.1016/j.atech.2021.100005'),
 'bra2010': ('Bramley, R. G. V. (2010). Precision viticulture: managing vineyard variability for improved quality outcomes. En <em>Managing wine quality. Volume 1: Viticulture and wine quality</em> (cap. 12). Woodhead Publishing.', 'https://doi.org/10.1533/9781845699284.3.445'),
 'fer2023': ('Ferro, M. V. y Catania, P. (2023). Technologies and innovative methods for precision viticulture: a comprehensive review. <em>Horticulturae</em>, 9(3), 399.', '10.3390/horticulturae9030399'),
 'del2014': ('De la Fuente, M. (2014). The relevance of the yield prediction methods in vineyard management. <em>Bulletin de l’OIV</em>, 87(1001-1002-1003), 387–394.', None),
 'pob2025d': ('Poblete-Echeverría, C., Hernández, I., Íñiguez, R., Gutiérrez, S., Barrio, I. y Tardáguila, J. (2025b). Using artificial intelligence for automatic and fast detection of downy mildew symptoms in grapevine canopies. <em>European Journal of Agronomy</em>, 170, 127755.', '10.1016/j.eja.2025.127755'),
 'gut2018a': ('Gutiérrez, S., Diago, M. P., Fernández-Novales, J. y Tardaguila, J. (2018b). Vineyard water status assessment using on-the-go thermal imaging and machine learning. <em>PLoS ONE</em>, 13(2), e0192037.', '10.1371/journal.pone.0192037'),
 'gut2021': ('Gutiérrez, S., Fernández-Novales, J., Diago, M. P., Íñiguez, R. y Tardaguila, J. (2021). Assessing and mapping vineyard water status using a ground mobile thermal imaging platform. <em>Irrigation Science</em>.', '10.1007/s00271-021-00735-1'),
 'gut2018b': ('Gutiérrez, S., Fernández-Novales, J., Diago, M. P. y Tardaguila, J. (2018a). On-the-go hyperspectral imaging under field conditions and machine learning for the classification of grapevine varieties. <em>Frontiers in Plant Science</em>, 9, 1102.', '10.3389/fpls.2018.01102'),
 'gut2019': ('Gutiérrez, S., Tardaguila, J., Fernández-Novales, J. y Diago, M. P. (2019). On-the-go hyperspectral imaging for the in-field estimation of grape berry soluble solids and anthocyanin concentration. <em>Australian Journal of Grape and Wine Research</em>, 25, 127–133.', '10.1111/ajgw.12376'),
}
def ref(k): t, d = REF[k]; return f'{t} {doi(d)}' if d else t
def refs_ul(keys): return '<ul class="refs">' + ''.join(f'<li>{ref(k)}</li>' for k in keys) + '</ul>'

GLOSARIO = {
    'mildiu': 'Enfermedad de la vid causada por un organismo parecido a un hongo (Plasmopara viticola). Se ve como manchas amarillentas, «de aceite», en el haz de las hojas.',
    'aforo': 'Estimación de la cosecha que dará un viñedo antes de vendimiar, normalmente contando racimos.',
    'defoliación': 'Quitar hojas de la cepa. Aquí sirve para ver los racimos que las hojas tapaban.',
    'oclusión': 'Cuando algo tapa lo que queremos ver; aquí, las hojas tapando los racimos.',
    'viticultura de precisión': 'Según la OIV, un enfoque de gestión cíclico de las operaciones de campo, basado en herramientas de información y tecnología, que utiliza múltiples fuentes de datos relacionados con el viñedo para respaldar la toma de decisiones específicas para cada lugar, con el objetivo de optimizar los procesos de producción (OIV, 2019).',
}
_gl = {'n': 0}
def term(palabra, texto=None):
    _gl['n'] += 1; i = f'g{_gl["n"]}'
    return (f'<button type="button" class="term" aria-expanded="false" aria-controls="{i}">{texto or palabra}</button>'
            f'<span class="gloss" id="{i}" hidden><strong>{html.escape(palabra.capitalize())}:</strong> {GLOSARIO[palabra]}</span>')

# ---------------- iconos (SVG propios, decorativos) ----------------
S = 'fill="none" stroke="#54081F" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"'
ICONOS = {
 'racimo': f'<svg viewBox="0 0 48 48" aria-hidden="true" focusable="false"><g fill="#54081F"><circle cx="16" cy="18" r="5"/><circle cx="27" cy="18" r="5"/><circle cx="21" cy="26" r="5"/><circle cx="32" cy="26" r="5"/><circle cx="16" cy="34" r="5"/><circle cx="27" cy="34" r="5"/><circle cx="22" cy="42" r="4"/></g><path d="M22 13c0-5 3-8 8-8" {S} stroke="#5E6619"/></svg>',
 'hoja': f'<svg viewBox="0 0 48 48" aria-hidden="true" focusable="false"><path d="M24 6c8 4 15 4 18 9-1 8 1 12-4 17-3 5-8 8-14 12-6-4-11-7-14-12-5-5-3-9-4-17 3-5 10-5 18-9z" {S}/><circle cx="19" cy="22" r="3.5" fill="#E07A10"/><circle cx="29" cy="28" r="2.5" fill="#E07A10"/><circle cx="22" cy="32" r="2" fill="#E07A10"/></svg>',
 'fase': f'<svg viewBox="0 0 48 48" aria-hidden="true" focusable="false"><path d="M6 40h36" {S}/><path d="M12 40v-8m0 0c-3-1-4-4-4-6 3 0 4 2 4 6zm0 0c3-1 4-4 4-6-3 0-4 2-4 6z" {S}/><path d="M24 40V22" {S}/><circle cx="24" cy="18" r="4" {S}/><path d="M36 40V30" {S}/><g fill="#54081F"><circle cx="33" cy="26" r="3"/><circle cx="39" cy="26" r="3"/><circle cx="36" cy="22" r="3"/></g></svg>',
 'peso': f'<svg viewBox="0 0 48 48" aria-hidden="true" focusable="false"><path d="M8 40h32M24 10v30M12 16h24" {S}/><path d="M12 16l-6 12h12zM36 16l-6 12h12z" {S}/></svg>',
 'sed': f'<svg viewBox="0 0 48 48" aria-hidden="true" focusable="false"><path d="M24 6c8 10 12 16 12 22a12 12 0 0 1-24 0c0-6 4-12 12-22z" {S}/><path d="M18 30a6 6 0 0 0 6 6" {S} stroke="#E07A10"/></svg>',
 'variedad': f'<svg viewBox="0 0 48 48" aria-hidden="true" focusable="false"><path d="M14 8l4 6-6 2 4 6-6 2 6 8h-2" {S}/><path d="M34 8l-4 6 6 2-4 6 6 2-6 8" {S} stroke-dasharray="1 5"/><path d="M24 14v28" {S}/></svg>',
 'color': f'<svg viewBox="0 0 48 48" aria-hidden="true" focusable="false"><path d="M4 24h12l5-12 6 24 5-12h12" {S}/><g stroke-width="4" stroke-linecap="round"><path d="M8 40h6" stroke="#54081F"/><path d="M18 40h6" stroke="#E07A10"/><path d="M28 40h6" stroke="#5E6619"/><path d="M38 40h4" stroke="#768020"/></g></svg>',
}
def icono(k, disc=False): return f'<span class="icono{" disc" if disc else ""}">{ICONOS[k]}</span>'

def logo_svg():
    return ('<svg viewBox="0 0 48 48" aria-hidden="true" focusable="false">'
            '<path d="M4 14V4h10M34 4h10v10M44 34v10H34M14 44H4V34" fill="none" stroke="#54081F" stroke-width="4"/>'
            '<g fill="#54081F"><circle cx="17" cy="16" r="4.5"/><circle cx="27" cy="16" r="4.5"/><circle cx="22" cy="23" r="4.5"/>'
            '<circle cx="32" cy="23" r="4.5"/><circle cx="17" cy="30" r="4.5"/><circle cx="27" cy="30" r="4.5"/><circle cx="22" cy="37" r="4.5"/></g>'
            '<path d="M22 12c0-4 2-6 5-7" fill="none" stroke="#5E6619" stroke-width="3" stroke-linecap="round"/></svg>')

# ---------------- retos y próximos retos ----------------
PROX = [  # archivo, icono, verbo, pregunta, gancho
 ('peso.html', 'peso', 'Estimar', '¿Cuánto pesa este racimo?', 'Un racimo, una foto y una pregunta: ¿cuántos gramos crees que pesa?'),
 ('enfermedades.html', 'hoja', 'Reconocer', '¿Qué enfermedad es?', 'Oídio, yesca… otras amenazas del viñedo que también se aprenden a reconocer.'),
 ('variedades.html', 'variedad', 'Identificar', '¿Qué variedad es?', 'Tempranillo, Garnacha, Graciano… ¿distingues una variedad por su hoja?'),
 ('fases.html', 'fase', 'Reconocer', '¿En qué fase está la vid?', 'Brotes, flores, bayas verdes, uvas maduras: ¿sabrías decir en qué momento está la planta solo con una foto?'),
 ('sed.html', 'sed', 'Medir', '¿Qué cepa tiene sed?', 'Las plantas también sufren sequía. Una cámara térmica ve lo que el ojo no nota.'),
 ('color.html', 'color', 'Descubrir', 'Colores que no vemos', 'La luz que no percibimos esconde información sobre la uva antes de probarla.'),
]
JUGABLES = {'fases.html'}
LAB_PAGS = ['laboratorio.html', 'laboratorio-racimos.html', 'laboratorio-mildiu.html']
NAV = [('index.html', 'Inicio'), ('SUB', 'Juegos'), ('LAB', 'Laboratorio'), ('ciencia.html', 'La ciencia'), ('guia-didactica.html', 'Docentes'), ('creditos.html', 'Créditos')]
TODAS = ['index.html', 'juegos.html', 'racimos.html', 'mildiu.html'] + [p[0] for p in PROX] + ['laboratorio.html', 'laboratorio-racimos.html', 'laboratorio-mildiu.html', 'sube.html', 'ciencia.html', 'creditos.html', 'accesibilidad.html', 'guia-didactica.html', 'lenguaje-sencillo.html']

def cabecera(actual):
    li = ''
    for h, n in NAV:
        if h == 'SUB':
            activo = actual in ['juegos.html', 'racimos.html', 'mildiu.html'] + [p[0] for p in PROX]
            cur = lambda a: ' aria-current="page"' if a == actual else ''
            sub = f'<li><a href="juegos.html"{cur("juegos.html")}>Ver todos los juegos</a></li>'
            sub += f'<li><a href="racimos.html"{cur("racimos.html")}>¿Cuántos racimos hay?</a></li><li><a href="mildiu.html"{cur("mildiu.html")}>¿Mildiu o no?</a></li>'
            sub += ''.join(f'<li><a href="{a}"{cur(a)}>{q}{"" if a in JUGABLES else ' <span class="sr-only">(próximamente)</span>'}</a></li>' for a, _, _, q, _ in PROX)
            li += (f'<li><button type="button" class="sub-toggle" id="sub-toggle" aria-expanded="false" aria-controls="sub-menu"{" data-activo=\"1\"" if activo else ""}>{n}'
                   '<svg viewBox="0 0 10 10" aria-hidden="true"><path d="M1 3l4 4 4-4" fill="none" stroke="currentColor" stroke-width="2"/></svg></button>'
                   f'<ul class="sub" id="sub-menu" hidden>{sub}</ul></li>')
        elif h == 'LAB':
            activo = actual in LAB_PAGS
            cur = lambda a: ' aria-current="page"' if a == actual else ''
            sub = ''.join(f'<li><a href="{a}"{cur(a)}>{t}</a></li>' for a, t in [('laboratorio.html', 'Cómo funciona'), ('laboratorio-racimos.html', 'Contar racimos con IA'), ('laboratorio-mildiu.html', 'Detectar mildiu con IA')])
            li += (f'<li><button type="button" class="sub-toggle" id="lab-toggle" aria-expanded="false" aria-controls="lab-menu"{" data-activo=\"1\"" if activo else ""}>{n}'
                   '<svg viewBox="0 0 10 10" aria-hidden="true"><path d="M1 3l4 4 4-4" fill="none" stroke="currentColor" stroke-width="2"/></svg></button>'
                   f'<ul class="sub" id="lab-menu" hidden>{sub}</ul></li>')
        else:
            li += f'<li><a href="{h}"{" aria-current=\"page\"" if h == actual else ""}>{n}</a></li>'
    return f'''<a class="skip" href="#contenido">Saltar al contenido</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html">{logo_svg()}<span>{TITULO}</span></a>
    <button type="button" class="btn secundario nav-toggle" id="nav-toggle" aria-expanded="false" aria-controls="site-nav">Menú</button>
    <nav class="site-nav" id="site-nav" aria-label="Principal"><ul>{li}</ul></nav>
  </div>
</header>'''

def pie():
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div><p><strong>{TITULO}</strong> · {LEMA}</p>
      <p>Divulgación basada en investigación de la <a href="https://www.unirioja.es/">Universidad de La Rioja</a> y del <a href="https://www.icvv.es/">Instituto de Ciencias de la Vid y del Vino (ICVV)</a>. Obra de {AUTOR}.</p></div>
    <div><p><strong>Licencia</strong></p>
      <p>Contenidos bajo <a href="https://creativecommons.org/licenses/by/4.0/deed.es" rel="license">CC BY 4.0</a>. Código bajo licencia MIT. Detalles en <a href="creditos.html">Créditos</a>.</p></div>
    <div><p><strong>Más información</strong></p>
      <ul><li><a href="ciencia.html">La ciencia detrás</a></li><li><a href="creditos.html">Créditos y licencias</a></li><li><a href="accesibilidad.html">Declaración de accesibilidad</a></li><li><a href="lenguaje-sencillo.html">En lenguaje sencillo</a></li><li><a href="guia-didactica.html">Guía didáctica para docentes</a></li></ul>
      <p class="pie-compartir"><button type="button" class="btn secundario" data-compartir>Compartir esta web</button></p></div>
  </div>
</footer>'''

def meta_social(archivo, full, desc):
    u = lambda p: f'{SITE_URL}/{p}' if SITE_URL else p
    t = html.escape(full); d = html.escape(desc)
    m = (f'<meta property="og:type" content="website"><meta property="og:locale" content="es_ES"><meta property="og:site_name" content="{TITULO}">'
         f'<meta property="og:title" content="{t}"><meta property="og:description" content="{d}">'
         f'<meta property="og:image" content="{u("img/og.jpg")}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
         f'<meta property="og:image:alt" content="Entre cepas: Tú contra la IA en el viñedo. Ilustración de un viñedo visto desde arriba con un mapa de zonas.">'
         f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{t}"><meta name="twitter:description" content="{d}"><meta name="twitter:image" content="{u("img/og.jpg")}">')
    if SITE_URL:
        m += f'<link rel="canonical" href="{u("" if archivo == "index.html" else archivo)}"><meta property="og:url" content="{u("" if archivo == "index.html" else archivo)}">'
    return m

GUIA_DE = {'index.html': 'guia_viticultura_de_precision.pdf', 'racimos.html': 'guia_contar_racimos.pdf', 'mildiu.html': 'guia_detectar_mildiu.pdf', 'peso.html': 'guia_peso_del_racimo.pdf', 'enfermedades.html': 'guia_otras_enfermedades.pdf', 'variedades.html': 'guia_variedades.pdf', 'fases.html': 'guia_fases_de_la_vid.pdf', 'sed.html': 'guia_estres_hidrico.pdf', 'color.html': 'guia_colores_que_no_vemos.pdf'}

def pagina(archivo, titulo, descripcion, cuerpo, scripts=()):
    if archivo in GUIA_DE and archivo != 'index.html':
        cuerpo += f'<section class="bloque guia-barra" aria-label="Para docentes"><div class="wrap"><p>¿Eres docente? <a href="guias/{GUIA_DE[archivo]}" download>Descarga la guía didáctica de este tema (PDF)</a> o <a href="guia-didactica.html">mira todas las guías</a>.</p></div></section>'
    full = f'{titulo} · {TITULO}' if archivo != 'index.html' else f'{TITULO} · {LEMA}'
    sc = ''.join(f'<script src="{s}" defer></script>' for s in scripts)
    open(os.path.join(ROOT, archivo), 'w', encoding='utf-8').write(f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full)}</title>
<meta name="description" content="{html.escape(descripcion)}">
<meta name="author" content="{AUTOR}">
<meta name="theme-color" content="#54081F">
{meta_social(archivo, full, descripcion)}
<link rel="icon" href="img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="css/style.css">
<script src="js/common.js" defer></script><script src="js/voz.js" defer></script><script src="js/compartir.js" defer></script>{sc}
</head>
<body>
{cabecera(archivo)}
<main id="contenido">
{cuerpo}
</main>
{pie()}
</body>
</html>
''')

def cab_pagina(chip, icon, h1, lead, prox=False):
    return f'''<div class="cabecera-pagina"><div class="wrap">{icono(icon, prox)}<div><span class="chip{" prox" if prox else ""}">{chip}</span><h1>{h1}</h1><p class="lead">{lead}</p></div></div></div>'''

# ---------------- datos de los retos ----------------
d = json.loads(open(os.path.join(ROOT, 'data', 'racimos.js'), encoding='utf-8').read().split('=', 1)[1].rstrip(';\n'))
META = d['meta']; C37 = next(c for c in d['cepas'] if c['id'] == 'C_37')
fmt = lambda x: str(x).replace('.', ',')

def rects(boxes, clase):
    o = ''
    for b in boxes:
        a = f'x="{b[0]}" y="{b[1]}" width="{b[2]-b[0]}" height="{b[3]-b[1]}" rx="3"'
        o += f'<rect class="halo" {a}/><rect class="{clase}" {a}/>'
    return o

def foto(base, alt, cap, w, h, carpeta='img/mildiu', cls='foto-caja'):
    return (f'<figure class="{cls}"><picture><source type="image/webp" srcset="{carpeta}/{base}.webp"><img src="{carpeta}/{base}.jpg" alt="{alt}" width="{w}" height="{h}" loading="lazy"></picture>'
            f'<figcaption>{cap}</figcaption></figure>')

from PIL import Image as _PI
def _dim(base):
    with _PI.open(f'img/fotos/{base}.jpg') as im: return im.size
def pf(base, alt, extra='', lazy=True):
    w, h = _dim(base)
    return f'<picture><source type="image/webp" srcset="img/fotos/{base}.webp"><img src="img/fotos/{base}.jpg" alt="{alt}" width="{w}" height="{h}"{" loading=\"lazy\"" if lazy else ""}{extra}></picture>'
CRED = 'Foto: archivo Televitis (UR-ICVV).'
# Contacto: la dirección de correo se pasa por la variable de entorno CONTACTO_EMAIL; sin ella, se enlaza la ficha del autor en la UR.
_mail = os.environ.get('CONTACTO_EMAIL', '').strip()
CONTACTO = (f'<a href="mailto:{_mail}">{_mail}</a>' if _mail else
            '<a href="https://investigacion.unirioja.es/investigadores/148703/detalle">ficha del autor en el portal de investigación de la Universidad de La Rioja</a> (datos de contacto)')
CRH = 'Figura: equipo HyperGrape (Universidad de La Rioja).'
CRED_IA = 'Imagen generada con IA a partir de fotografías del archivo Televitis (UR-ICVV).'
def ff(base, alt, cap, cred=CRED, cls='foto-caja'):
    return f'<figure class="{cls}">{pf(base, alt)}<figcaption>{cap} <span class="cred">{cred}</span></figcaption></figure>'
def ff_ctx(base, w, h, alt, cap, cred, cls='foto-caja foto-ancha'):
    return f'<figure class="{cls}">{pic_ctx(base, alt, w, h)}<figcaption>{cap} <span class="cred">{cred}</span></figcaption></figure>'
def galeria(items):
    return '<div class="galeria">' + ''.join(ff(*i) for i in items) + '</div>'

def hero_cepa():
    w, h = C37['w'], C37['h']
    vis = rects(C37['con'], 'caja-v'); oc = rects([o['b'] for o in C37['des'] if o['oculto']], 'caja-h'); vd = rects([o['b'] for o in C37['des'] if not o['oculto']], 'caja-v')
    return f'''<figure class="hero-cepa" id="hero-cepa" data-vis="{C37['visibles']}" data-oc="{C37['ocultos']}" data-tot="{C37['deshojada']}">
  <div class="hc-lienzo" style="--pos:0%">
    <div class="hc-capa"><picture><source type="image/webp" srcset="img/racimos/C_37_con_hojas.webp"><img src="img/racimos/C_37_con_hojas.jpg" alt="Cepa de vid con hojas: entre ellas se ven pocos racimos de uva tinta." width="{w}" height="{h}" loading="lazy"></picture>
      <svg class="cajas hc-cajas" viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true">{vis}</svg></div>
    <div class="hc-capa hc-b" aria-hidden="true"><picture><source type="image/webp" srcset="img/racimos/C_37_deshojada.webp"><img src="img/racimos/C_37_deshojada.jpg" alt="" width="{w}" height="{h}"></picture>
      <svg class="cajas hc-cajas" viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true">{vd}{oc}</svg></div>
    <span class="hc-linea" aria-hidden="true"></span>
  </div>
  <p class="hc-control"><label for="hc-rango">Quita las hojas</label><input type="range" id="hc-rango" min="0" max="100" step="5" value="0" aria-valuetext="Cepa con hojas"></p>
  <figcaption id="hc-txt" aria-live="polite">Con hojas, una persona experta ve {C37['visibles']} racimos. ¿Cuántos esconden las hojas? Desliza para descubrirlo.</figcaption>
</figure>'''

def hero_img():
    w, h = C37['w'], C37['h']
    vis = rects(C37['con'], 'caja-v'); oc = rects([o['b'] for o in C37['des'] if o['oculto']], 'caja-h'); vd = rects([o['b'] for o in C37['des'] if not o['oculto']], 'caja-v')
    return f'''<figure class="hero-img">
  <div class="split" role="img" aria-label="Una misma cepa fotografiada con hojas (mitad izquierda) y sin hojas (mitad derecha). Con hojas se ven {C37['visibles']} racimos; al quitar las hojas aparecen {C37['ocultos']} más.">
    <div class="capa"><picture><source type="image/webp" srcset="img/racimos/C_37_con_hojas.webp"><img src="img/racimos/C_37_con_hojas.jpg" alt="" width="{w}" height="{h}"></picture>
      <svg class="cajas" viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true">{vis}</svg></div>
    <div class="capa capa-b"><picture><source type="image/webp" srcset="img/racimos/C_37_deshojada.webp"><img src="img/racimos/C_37_deshojada.jpg" alt="" width="{w}" height="{h}"></picture>
      <svg class="cajas" viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true">{vd}{oc}</svg></div>
    <span class="linea" aria-hidden="true"></span>
  </div>
  <figcaption><span><strong>Con hojas</strong><span class="leyenda-linea"></span>{C37['visibles']} racimos a la vista</span>
  <span><strong>Sin hojas</strong><span class="leyenda-linea disc"></span>{C37['ocultos']} racimos más, escondidos</span></figcaption>
</figure>'''

# ---------------- páginas ----------------
def objetivo(n, titulo, img, texto, retos):
    ya = any(r[2] for r in retos)
    chip = '<span class="chip">Juega ya</span>' if ya else '<span class="chip prox">Próximamente</span>'
    lis = ''.join(f'<li><a class="btn{"" if r[2] else " secundario"}" href="{r[0]}">{"Jugar: " if r[2] else "Próximamente: "}{r[1]}</a></li>' for r in retos)
    return f"""<li class="objetivo"><div class="foto">{img}</div><div class="cuerpo"><p class="num-obj" aria-hidden="true">{n}</p>{chip}<h3>{titulo}</h3>{texto}<ul class="retos-obj">{lis}</ul></div></li>"""

def pic_ctx(base, alt, w, h, carpeta='img/contexto', extra=''):
    return f'<picture><source type="image/webp" srcset="{carpeta}/{base}.webp"><img src="{carpeta}/{base}.jpg" alt="{alt}" width="{w}" height="{h}" loading="lazy"{extra}></picture>'

def mosaico():
    T = lambda base, alt: f'<span>{pf(base, alt, lazy=False)}</span>'
    return f"""<figure class="mosaico">
  <div class="m-grid">
    {T('quad_04_vinedo_aereo_dron_ladera', 'Vista aérea, tomada con un dron, de un viñedo en ladera con filas verdes y un pueblo al fondo.')}
    {T('mildiu_09_hoja_manchas_aceite_cepa', 'Hojas de vid con manchas amarillentas redondeadas, entre otras hojas verdes.')}
    <span>{pic_ctx('dron_termica_b', 'Imagen térmica aérea de un viñedo: las filas de cepas aparecen en tonos morados y el suelo, en naranja y amarillo.', 640, 512, extra=' fetchpriority="high"')}</span>
    {T('quad_08_plataforma_atardecer_ladera_a', 'Vehículo naranja con cámaras montadas en una plataforma, aparcado junto a un viñedo al atardecer.')}
    {T('produccion_01_cepa_racimos_cerca', 'Cepa con varios racimos de uva tinta bajo las hojas.')}
    {T('hyper_03_camara_hiperespectral_en_quad', 'Plataforma con una cámara hiperespectral montada sobre un vehículo entre las filas de un viñedo.')}
  </div>
  <figcaption>Mirar el viñedo con drones, cámaras y sensores. Fotografías e imagen térmica de dron: archivo Televitis (Universidad de La Rioja).</figcaption>
</figure>"""

def selector_objetivos():
    R = {a: q for a, i, v, q, g in PROX}
    L = lambda href, txt, jugar=False: f'<a class="btn{"" if jugar else " secundario"}" href="{href}">{"Jugar: " if jugar else ""}{txt}</a>'
    T = [
      ('produccion', 'Producción', 'racimo', pf('produccion_03_cepa_racimos_cinta_b', 'Cepa con racimos de uva tinta, con una cinta a rayas en el tronco.'), 'Estimar la producción',
        'Saber cuánta uva habrá antes de vendimiar orienta el manejo del viñedo, la elaboración y la venta (Laurent et al., 2021). Para estimarlo hay que contar racimos, y las hojas esconden muchos.',
        [L('racimos.html', '¿Cuántos racimos hay?', True), L('peso.html', R['peso.html'])]),
      ('sanidad', 'Sanidad', 'hoja', pf('mildiu_11_hojas_en_mano_manchas_aceite', 'Manos sostienen hojas de vid con manchas amarillentas causadas por el mildiu.'), 'Vigilar la sanidad',
        'El mildiu es una de las enfermedades más destructivas del viñedo, y vigilarlo a pie es laborioso y subjetivo (Poblete-Echeverría et al., 2025b). ¿Puede ayudar una cámara?',
        [L('mildiu.html', '¿Mildiu o no?', True), L('enfermedades.html', R['enfermedades.html'])]),
      ('vinedo', 'Viñedo', 'variedad', pf('quad_03_dron_en_vuelo_sobre_vinedo', 'Un dron en vuelo sobre un viñedo, con filas de cepas y un cielo nublado.'), 'Conocer y vigilar el viñedo',
        'Drones, satélites y sensores permiten vigilar la vid a lo largo del año (Tardaguila et al., 2021). Y la IA puede ayudar a reconocer la variedad (Gutiérrez et al., 2018a) o la fase del ciclo (Íñiguez et al., 2025b).',
        [L('variedades.html', R['variedades.html']), L('fases.html', R['fases.html'], True)]),
      ('riego', 'Riego', 'sed', pic_ctx('dron_termica_0129', 'Imagen térmica aérea de un viñedo: las cepas aparecen en tonos morados y los caminos, en naranja y amarillo.', 640, 512), 'Manejar bien el riego',
        'Las plantas también sufren sequía. Una cámara térmica, montada en un vehículo que avanza por el viñedo, permite estimar su estado hídrico (Gutiérrez et al., 2018b) y decidir cuánto y dónde regar.',
        [L('sed.html', R['sed.html'])]),
      ('vendimia', 'Vendimia', 'color', pf('vendimia_01_racimo_caja_tijeras', 'Racimo de uva tinta madura colgando de la cepa, con unas tijeras de vendimia y una caja de racimos al fondo.'), 'Decidir cuándo vendimiar',
        'La madurez se mide con muestras y análisis de laboratorio. Una cámara hiperespectral, que capta luz que no vemos, puede estimar azúcares, acidez o color en el propio viñedo (Tejada-González et al., 2026).',
        [L('color.html', R['color.html'])]),
    ]
    PRACT = {
      'produccion': 'Ajustar el aclareo, organizar la vendimia (personal, cajas, depósitos) y negociar la venta de la uva con datos, no a ojo.',
      'sanidad': 'Revisar antes los focos, tratar cuándo y dónde hace falta y evitar tratamientos innecesarios.',
      'vinedo': 'Programar poda en verde, tratamientos y riegos según la fase real de cada parcela, y confirmar qué variedad hay plantada.',
      'riego': 'Decidir cuánto y dónde regar, sectorizar el riego y ahorrar agua sin perder calidad de uva.',
      'vendimia': 'Elegir el día de vendimia de cada parcela y separar uvas de distinta calidad a la entrada de bodega.',
    }
    tabs = ''.join(f'<button type="button" role="tab" id="tab-{k}" aria-controls="pan-{k}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{icono(ic)}<span>{n}</span></button>' for i, (k, n, ic, _, _, _, _) in enumerate(T))
    pans = ''.join(f'<div class="panel{" activo" if i == 0 else ""}" role="tabpanel" id="pan-{k}" aria-labelledby="tab-{k}" tabindex="0"><div class="foto">{im}</div><div class="cuerpo"><h3>{t}</h3><p>{tx}</p><p class="practico"><strong>En el viñedo sirve para:</strong> {PRACT[k]}</p><p class="acciones">{"".join(ls)}</p></div></div>' for i, (k, n, ic, im, t, tx, ls) in enumerate(T))
    return f'<div class="selector"><div class="tabs" role="tablist" aria-label="Los cinco objetivos del viñedo de precisión">{tabs}</div><div class="paneles">{pans}</div></div>'

def index():
    pills = ''.join(f'<li><a class="pill" href="{a}">{icono(i, True)}<span>{q} <span class="pill-prox">(próximamente)</span></span></a></li>' for a, i, v, q, g in PROX if a not in JUGABLES)
    pasos = [('1', 'Haz una foto'), ('2', 'Súbela'), ('3', 'La web la analiza'), ('4', 'Mira el resultado')]
    lab = ''.join(f'<li><span class="paso-num" aria-hidden="true">{n}</span><span>{t}</span></li>' for n, t in pasos)
    cuerpo = f"""<section class="hero hero-simple hero-reto hero-vdp">
  <div class="wrap">
    <div>
      <p class="kicker">Ciencia de la vid · Divulgación · ICVV</p>
      <h1>{TITULO}</h1>
      <p class="lema">{LEMA}</p>
      <p class="lead"><strong>¿Qué ve una máquina en un viñedo?</strong> La {term('viticultura de precisión')} usa cámaras, sensores e inteligencia artificial para medir las diferencias entre cepas y actuar solo donde hace falta. La IA cuenta racimos, detecta mildiu y reconoce la fase de la vid en segundos, pero no lo ve todo. <strong>Compruébalo tú.</strong></p>
      <p class="acciones"><a class="btn grande" href="juegos.html">Jugar (5 min)</a> <a class="enlace-suave" href="#obj-h">Qué es la viticultura de precisión</a></p>
    </div>
    <figure class="video-vp">
      <video id="vp" controls muted playsinline preload="metadata" width="1280" height="720" poster="video/entre_cepas_vp.jpg" aria-describedby="vp-trans">
        <source src="video/entre_cepas_vp.mp4" type="video/mp4">
        Tu navegador no puede reproducir el vídeo; abajo tienes su transcripción.
      </video>
      <details id="vp-trans" class="transcripcion"><summary>Transcripción del vídeo (37 s)</summary>
        <p>El vídeo no tiene locución, solo sonido ambiente; el texto de cada escena aparece en la propia imagen.</p>
        <ol>
          <li><strong>Un viñedo no es igual en todas partes.</strong> Vista desde arriba de una parcela: las cepas de la izquierda son pequeñas y amarillentas, y las de la derecha, grandes y de un verde intenso. Dentro de una misma parcela, las cepas crecen de forma distinta.</li>
          <li><strong>Recoger datos.</strong> Un dron sobrevuela las filas y un vehículo con cámaras y sensores recorre las calles. Ondas de luz van de cada equipo a las cepas: recogen datos de cada zona del viñedo.</li>
          <li><strong>De datos a mapas.</strong> La parcela se cubre con un mapa de colores, del amarillo (poco vigor) al verde oscuro (mucho vigor). De un vistazo se ve dónde crece más y dónde menos la vid.</li>
          <li><strong>Actuar donde hace falta.</strong> Un tractor recorre la parcela y riega las zonas amarillas, pero no las verde oscuro. Esas zonas se van recuperando: se actúa donde hace falta, con más agua o más cuidados en unas zonas y menos en otras.</li>
        </ol>
      </details>
    </figure>
  </div>
</section>

<section class="bloque prueba" aria-labelledby="prueba-h">
  <div class="wrap hero-reto-grid">
    <div>
      <h2 id="prueba-h">Pruébalo ahora: ¿cuántos racimos esconden las hojas?</h2>
      <p>Esta es una cepa real de La Rioja. Con hojas, una persona experta ve unos pocos racimos y la IA de <a class="enl-tv" href="https://televitis.unirioja.es/">Televitis</a> no encuentra ninguno. Desliza para quitar las hojas y mira lo que había.</p>
      <p class="acciones"><a class="btn" href="racimos.html">Jugar al reto de los racimos</a></p>
    </div>
    {hero_cepa()}
  </div>
</section>

<section class="cifras" aria-label="Tres datos de la investigación">
  <div class="wrap"><ul>
    <li><span class="cifra">28,6 %</span><span>de los racimos de las 20 cepas del reto estaban escondidos por las hojas</span></li>
    <li><span class="cifra">86 %</span><span>de acierto de la IA al localizar zonas con mildiu en el campo (Hernández et al., 2025)</span></li>
    <li><span class="cifra">95,6 %</span><span>de acierto de la IA al reconocer la fase de la vid en fotos nuevas (Íñiguez et al., 2025b)</span></li>
  </ul></div>
</section>

<section aria-labelledby="retos-h" id="retos" class="bloque">
  <div class="wrap">
    <h2 id="retos-h">Empieza aquí: una ruta de 15 minutos</h2>
    <ol class="ruta ruta-h">
      <li><span class="paso-num" aria-hidden="true">1</span><span><strong>Mira el vídeo</strong> de arriba (37 s): un viñedo no es igual en todas partes (Bramley, 2010), y la viticultura de precisión mide esas diferencias.</span></li>
      <li><span class="paso-num" aria-hidden="true">2</span><span><strong>Juega los retos</strong> (≈ 5 min cada uno) y compara tu ojo con la IA.</span></li>
      <li><span class="paso-num" aria-hidden="true">3</span><span><strong>Explora los cinco objetivos</strong> del viñedo de precisión.</span></li>
      <li><span class="paso-num" aria-hidden="true">4</span><span><strong>Prueba el Laboratorio</strong> y mira la IA analizando fotos reales.</span></li>
    </ol>
    {retos_grandes()}
  </div>
</section>

<section class="band band-fina" aria-label="Mensaje principal">
  <div class="narrow"><p class="lead">La inteligencia artificial puede ayudar mucho en el viñedo, pero ve lo que ve la cámara, depende de cuándo y cómo se mira, y siempre necesita la mirada de una persona.</p></div>
</section>

<section aria-labelledby="obj-h" class="bloque">
  <div class="wrap">
    <h2 id="obj-h">Cuidar el viñedo, cepa a cepa</h2>
    <p>Cinco objetivos en los que la tecnología ayuda a mirar mejor. Elige uno.</p>
    {selector_objetivos()}
  </div>
</section>

<section class="bloque lab-franja" aria-labelledby="lab-h">
  <div class="wrap">
    <h2 id="lab-h">Laboratorio: prueba la IA con tu foto</h2>
    <ol class="lab-pasos">{lab}</ol>
    <p><a class="btn" href="laboratorio.html">Probar con tu foto</a></p>
  </div>
</section>

<section aria-labelledby="mas" class="bloque">
  <div class="wrap">
    <h2 id="mas">Próximos retos</h2>
    <p>Todavía no se pueden jugar, pero ya puedes ver en qué consistirán y en qué investigación se apoyan.</p>
    <ul class="pills">{pills}</ul>
    <p class="mas-juegos"><a class="btn secundario" href="juegos.html">Ver todos los juegos</a></p>
  </div>
</section>

<section class="bloque" aria-label="Referencias"><div class="wrap capas"><details><summary>Referencias de esta página</summary><div>{refs_ul(['bra2010', 'lau2021', 'pob2025d', 'tar2021', 'gut2018a', 'gut2018b', 'ini2025b', 'tej2026'])}</div></details></div></section>

<section class="barra-fina" aria-label="Más información">
  <div class="wrap">
    <ul><li><a href="ciencia.html">La ciencia</a></li><li><a href="creditos.html">Créditos</a></li><li><a href="accesibilidad.html">Accesibilidad</a></li><li><button type="button" class="enlace-btn" data-compartir>Compartir</button></li></ul>
  </div>
</section>"""
    pagina('index.html', 'Inicio', DESC_SITIO, cuerpo, scripts=('js/portada.js', 'js/video.js', 'js/hero.js'))

def _fig_variabilidad():
    return f"""      <figure class="ctx-fig">
        <div class="par">{pic_ctx('var_dron_foto', 'Imagen aérea de un viñedo con filas de cepas verdes separadas por tierra marrón: las cepas de la izquierda están más separadas y las de la derecha, más densas.', 600, 800)}{pic_ctx('var_dron_mapa', 'Mapa de zonas en cinco tonos de verde, del amarillo claro al verde oscuro: el vigor aumenta de izquierda a derecha.', 600, 800)}</div>
        <ul class="leyenda-mapa" aria-label="Leyenda del mapa: vigor">
          <li><span class="sw" style="background:#ffffb2"></span>Vigor bajo</li>
          <li><span class="sw" style="background:#c2e699"></span></li>
          <li><span class="sw" style="background:#78c679"></span>Medio</li>
          <li><span class="sw" style="background:#31a354"></span></li>
          <li><span class="sw" style="background:#006837"></span>Vigor alto</li>
        </ul>
        <figcaption>La misma zona de un viñedo vista desde un dron (izquierda) y su mapa de vigor (derecha): dentro de una misma parcela, las cepas no son iguales. <span class="cred">Elaboración propia a partir de una imagen de dron de Televitis (Universidad de La Rioja), julio de 2024.</span></figcaption>
      </figure>"""

def _extra_ciencia():
    return f"""<h2>Cada cepa cuenta</h2>
<p>Dentro de una misma parcela hay mucha variabilidad (Bramley, 2010): por eso interesa mirar cada zona, e incluso cada cepa.</p>
{_fig_variabilidad()}
<h2>Con qué se mira el viñedo</h2>
<details open>
      <summary>¿Con qué herramientas se hace?</summary>
      <div>
      <p>Los datos se obtienen desde distintas plataformas: satélites, drones y vehículos que circulan entre las filas, o con sensores y cámaras manuales (Tardaguila et al., 2021). Los sensores incluyen cámaras de imagen convencional (RGB), térmicas, multiespectrales e hiperespectrales. Después, la inteligencia artificial ayuda a interpretar esas imágenes.</p>
      <ul class="herr">
        <li>{ff('quad_02_plataforma_quad_atardecer_b', 'Vehículo naranja con una plataforma de cámaras y sensores, aparcado junto a un viñedo.', 'Un vehículo equipado con diferentes sensores.')}</li>
        <li>{ff('campo_03_plataforma_entre_filas', 'Vista desde un vehículo con un mástil con cámara, entre dos filas de viñedo.', 'El vehículo recorre las filas del viñedo recopilando datos.')}</li>
        <li>{ff('campo_02_plataforma_mastil_camara_vertical', 'Mástil metálico con una cámara en lo alto, sobre un vehículo, junto a una fila de viñedo.', 'Una plataforma se puede equipar con múltiples sensores.')}</li>
        <li>{ff('insion_02_espectrometro_nir_fibra', 'Un pequeño espectrómetro negro unido por un cable de fibra naranja a un sensor metálico.', 'Un espectrómetro portátil, que mide la luz que refleja la uva.')}</li>
        <li>{ff('campo_05_camara_rgb_detalle', 'Primer plano de una cámara réflex negra sobre un trípode, con un viñedo desenfocado al fondo.', 'Una cámara convencional (RGB), como la que da las imágenes de los tres retos.', CRED_IA)}</li>
        <li>{ff('ia_01_esquema_red_neuronal', 'Esquema: una foto de una cepa sin hojas pasa por una red neuronal, dibujada como círculos unidos por líneas, y sale la misma foto con cajas amarillas sobre los racimos.', 'La inteligencia artificial convierte la foto en datos: aquí, dónde están los racimos.', 'Elaboración propia con un modelo de Televitis.')}</li>
      </ul></div>
    </details>
"""

def retos_grandes(detalle=False):
    FR = ('B_38_deshojada', 577) if detalle else ('B_33_deshojada', 572)
    FM = 'mildiu_12_hojas_enves_en_mano' if detalle else 'mildiu_02_hoja_decolorada_en_mano'
    def li(href, chip, h3, p, extra, foto_html, jug):
        return f'''<li class="reto-grande"><div class="foto">{foto_html}</div>
        <div class="cuerpo"><span class="chip">{chip}</span><h3>{h3}</h3><p>{p}</p>{extra}
          <a class="btn" href="{href}">Jugar<span class="sr-only"> {jug}</span></a></div></li>'''
    ex_r = ('<ul class="mini"><li><strong>Antes:</strong> por qué importa contar racimos.</li><li><strong>Jugar:</strong> cinco cepas, con y sin hojas.</li><li><strong>Después:</strong> qué hace la IA y qué no ve.</li></ul>' if detalle else '')
    ex_m = ('<ul class="mini"><li><strong>Antes:</strong> qué es el mildiu y qué síntomas buscar.</li><li><strong>Jugar:</strong> diez imágenes reales de viñedo.</li><li><strong>Después:</strong> dónde estaba y dónde falla la IA.</li></ul>' if detalle else '')
    r = li('racimos.html', f"{ICONOS['racimo']}Contar", '¿Cuántos racimos hay?', 'Calcula cuántos racimos hay en cinco cepas y comprueba cuántos escondían las hojas.', ex_r,
           f'<picture><source type="image/webp" srcset="img/racimos/{FR[0]}.webp"><img src="img/racimos/{FR[0]}.jpg" alt="Una cepa sin hojas, con todos sus racimos a la vista." width="1200" height="{FR[1]}" loading="lazy"></picture>', 'a contar racimos')
    m = li('mildiu.html', f"{ICONOS['hoja']}Detectar", '¿Mildiu o no?', f"Diez imágenes del viñedo: ¿ves el {term('mildiu')}? Después, comprueba dónde estaba exactamente.", ex_m,
           pf(FM, 'Manos sostienen hojas de vid con zonas decoloradas y pardas.'), 'a detectar mildiu')
    ex_f = ('<ul class="mini"><li><strong>Antes:</strong> las etapas de la escala E-L.</li><li><strong>Jugar:</strong> ocho fotos y una línea del tiempo.</li><li><strong>Después:</strong> qué distingue una IA de una persona.</li></ul>' if detalle else '')
    f = li('fases.html', f"{ICONOS['fase']}Reconocer", '¿En qué fase está la vid?', 'Brotes, flores, bayas verdes, uvas maduras: sitúa cada foto en la línea del tiempo del viñedo.', ex_f,
           '<picture><source type="image/webp" srcset="img/fases/el27_1.webp"><img src="img/fases/el27_1.jpg" alt="Cepa con hojas verdes y un racimo de bayas verdes pequeñas colgando." width="1000" height="666" loading="lazy"></picture>', 'a reconocer la fase de la vid')
    return f'<ul class="retos-grandes">{r}{m}{f}</ul>'

def juegos():
    prox = ''.join(f'<li><a class="prox-card" href="{a}">{icono(i, True)}<span class="chip prox">Próximamente</span><h3>{q}</h3><p>{g}</p><span class="mas">Saber más<span class="sr-only"> sobre «{q}»</span></span></a></li>' for a, i, v, q, g in PROX if a not in JUGABLES)
    cuerpo = cab_pagina('Juegos', 'racimo', 'Juegos', 'Retos para comparar tu ojo con el de la inteligencia artificial, con imágenes reales de viñedos de La Rioja.') + f'''
<section class="bloque" aria-labelledby="ya" id="ya"><div class="wrap">
  <h2 id="ya">Ahora te toca a ti: tres retos para jugar ya</h2>
  <p class="lead">Cada reto tiene tres partes: <strong>antes</strong>, para entender el problema; <strong>jugar</strong>, con imágenes reales de viñedos de La Rioja; y <strong>después</strong>, para ver qué hace la ciencia y dónde falla.</p>
  {retos_grandes(True)}
</div></section>
<section class="bloque" aria-labelledby="proximos" id="proximos"><div class="wrap">
  <h2 id="proximos">Y esto es solo el principio</h2>
  <p>La plataforma crecerá con la investigación. Estos son los próximos retos en los que ya se está trabajando: todavía no se pueden jugar, pero puedes ver en qué consistirán y en qué investigación se apoyan.</p>
  <ul class="prox-grid">{prox}</ul>
</div></section>'''
    pagina('juegos.html', 'Juegos', 'Todos los retos de Entre cepas: tres para jugar ya (contar racimos, detectar mildiu y reconocer la fase de la vid) y los próximos, con imágenes reales de viñedos de La Rioja.', cuerpo)

CAPA_RACIMOS = f'''<section class="bloque" aria-labelledby="antes">
  <div class="wrap capas">
    <h2 id="antes">Antes de jugar: el problema</h2>
    <p class="lead">Antes de la vendimia, bodegas y viticultores necesitan saber cuánta uva habrá. Y lo que más pesa en esa cuenta es el número de racimos por cepa.</p>
    <details>
      <summary>Por qué importa contar racimos</summary>
      <div><p>El número de racimos por cepa suele ser el componente que más explica la variación de la cosecha: la regla clásica le atribuye en torno al 60 %, aunque esa proporción cambia según el viñedo y no debe darse por supuesta (Laurent et al., 2021). Además, tras la floración el número de racimos ya no cambia, así que puede contarse con antelación (Laurent et al., 2021). Esa estimación previa se llama {term('aforo')}.</p></div>
    </details>
    <details>
      <summary>Para qué le sirve a la bodega y a quien cultiva</summary>
      <div><p>Saber con tiempo cuánta uva habrá es una información esencial para todo el sector: orienta el manejo del viñedo, la elaboración, la venta, la contabilidad y la estrategia de la añada (Laurent et al., 2021). A quien cultiva le permite, por ejemplo, aclarar racimos para favorecer la maduración y evitar cargar demasiado o demasiado poco las cepas; a la bodega, calcular el espacio, la maquinaria y el personal que necesitará durante la vendimia (De la Fuente, 2014).</p>
      {galeria([('produccion_04_fila_racimos_espaldera', 'Fila de cepas en espaldera con muchos racimos de uva tinta colgando.', 'Una fila de cepas cargada de racimos.'), ('produccion_05_fila_vinedo_con_bodega_al_fondo', 'Calle de césped entre dos filas de viñedo, con un edificio de bodega al fondo.', 'El viñedo y la bodega, cada uno con sus decisiones.')])}</div>
    </details>
    <details>
      <summary>Cómo se hacía</summary>
      <div><p>El método tradicional consiste en cortar y contar racimos de unas pocas cepas y extrapolar al resto de la parcela. Es un muestreo destructivo, lento y caro, y la muestra no recoge toda la variabilidad del viñedo (Íñiguez et al., 2024).</p>{galeria([('yo_01_fotografiando_racimos_2023', 'Una persona agachada junto a una cepa, muy cerca de sus racimos, como si los contara uno a uno.', 'Contar a mano los racimos de cada cepa es lento.')])}</div>
    </details>
    <details>
      <summary>Cómo se hace ahora</summary>
      <div><p>Se fotografían las cepas con cámaras convencionales y un modelo de inteligencia artificial, entrenado con imágenes en las que personas han marcado cada racimo, aprende a localizarlos. En un estudio en viñedos comerciales, el modelo (YOLOv4) logró un error de 1,12 racimos, con un R² de 0,83 en validación (Íñiguez et al., 2024).</p>{galeria([('campo_04_camara_tripode_vinedo', 'Una cámara réflex sobre un trípode, en el pasillo entre dos filas de viñedo con racimos.', 'Una cámara convencional basta para fotografiar las cepas.', CRED_IA), ('campo_01_plataforma_camara_mastil', 'Vehículo con un mástil y una cámara en lo alto, junto a una fila de viñedo.', 'Las cámaras también pueden ir montadas en un vehículo.')])}</div>
    </details>
    <details>
      <summary>¿Se pueden contar racimos antes de la floración?</summary>
      <div><p>Cuanto antes se sepa cuánta uva habrá, más margen hay para actuar. Por eso se ha probado a detectar inflorescencias (los racimos todavía en flor) y racimos jóvenes. En un estudio con 436 imágenes de seis variedades, tomadas antes de la floración y tras el cuajado, de día y de noche con un foco LED, el mejor resultado para los racimos se obtuvo tras el cuajado y con luz de día (F1 = 0,77; R² = 0,97), mientras que para las inflorescencias fue mejor de noche con luz artificial (F1 = 0,71; R² = 0,76) (Íñiguez et al., 2025a).</p>
      {ff_ctx('fig_inf_ec', 1400, 488, 'Dos fotografías de cepas: a la izquierda, antes de la floración, brotes largos con pequeñas inflorescencias entre las hojas; a la derecha, tras el cuajado, un racimo de bayas verdes entre el follaje.', 'Lo que hay que detectar: inflorescencias antes de la floración (izquierda) y racimos jóvenes tras el cuajado (derecha), pequeños y medio escondidos entre las hojas.', 'Elaboración propia a partir de Íñiguez et al. (2025a), con fotografías del archivo Televitis (Universidad de La Rioja).')}</div>
    </details>
    <details>
      <summary>El obstáculo: las hojas</summary>
      <div><p>Las hojas tapan racimos; a eso se le llama {term('oclusión')}. En un estudio con cinco viñedos de Tempranillo, al aumentar la oclusión la relación entre los píxeles de racimo en la foto y la cosecha bajó de un R² de 0,77 a uno de 0,63 (Íñiguez et al., 2021). Quitar hojas ({term('defoliación')}) es una práctica habitual en el viñedo, y aquí la usamos para ver qué escondían.</p>
      {ff_ctx('fig_oclusion_ec', 1400, 693, 'Dos cepas, cada una fotografiada con hojas (izquierda) y sin ellas (derecha), con cajas amarillas sobre los racimos que detecta un modelo: con hojas detecta 1 y 0 racimos; sin hojas, 6 en cada una.', 'La misma cepa con y sin hojas, con los racimos que detecta un modelo de Televitis: las hojas esconden la mayoría.', 'Elaboración propia a partir de Íñiguez et al. (2021), con fotografías del archivo Televitis (Universidad de La Rioja).')}</div>
    </details>
    <p class="cita">Más detalle y referencias completas en «Para saber más», al final de la página.</p>
  </div>
</section>'''

def racimos():
    cuerpo = cab_pagina(f'{ICONOS["racimo"]}Contar', 'racimo', '¿Cuántos racimos hay?', 'Cinco cepas, cinco estimaciones. Después, quitamos las hojas y vemos cuántos racimos escondían.<span class="nace">Un reto basado en la <a href="https://investigacion.unirioja.es/documentos/696a8d27be3bb53a465a961c">tesis doctoral de Rubén Iñiguez Mangado</a> (Universidad de La Rioja – ICVV, 2025).</span>') + CAPA_RACIMOS + f'''
<section class="bloque" aria-labelledby="juega">
  <div class="wrap">
    <h2 id="juega">Ahora te toca a ti</h2>
    <div id="juego-intro">
      <ol class="tres">
        <li><h3>1. Cuenta</h3><p>Verás una cepa con hojas. Cuenta los racimos que veas y escribe tu cifra.</p></li>
        <li><h3>2. Comprueba</h3><p>Pulsa «Comprobar»: aparecen con línea continua los racimos que ve una cámara.</p></li>
        <li><h3>3. Quita las hojas</h3><p>Pulsa «Quitar las hojas» o arrastra el deslizador: con línea discontinua salen los que estaban escondidos.</p></li>
        <li><h3>4. Compárate</h3><p>Son cinco cepas. Al final, el marcador: lo que contaste tú, lo que contó la IA y lo que había de verdad, y cuánto tardas frente a ella.</p></li>
      </ol>
      <p class="ayuda">La pregunta tiene truco: ni tú ni la cámara podéis ver lo que tapan las hojas. Por eso se compara tu cifra con lo que ve la cámara y después con lo que había de verdad. Las cajas de «lo que ve una cámara» las marcaron personas expertas sobre la foto con hojas. Además, en cada cepa verás cuántos racimos contó la IA de Televitis en esa misma foto: tú, la IA y lo que había de verdad.</p>
      <div class="modo"><input type="checkbox" id="modo-desc" aria-describedby="modo-desc-ayuda"><label for="modo-desc"><strong>Modo descripción</strong>: sustituye las imágenes por descripciones en texto.</label></div>
      <p class="ayuda" id="modo-desc-ayuda">Pensado para quien no puede ver las imágenes. Con él, la pregunta cambia: calcula cuántos racimos hay en total, incluidos los que tapan las hojas.</p>
      <p><button type="button" class="btn grande" id="empezar">Empezar la ronda</button></p>
      <p class="nota">Sin límite de tiempo, pero se cuenta cuánto tardas por imagen para compararte con la IA al final. No se guarda nada fuera de tu navegador.</p>
    </div>

    <div id="juego-juego" hidden>
      <div class="juego-cab"><span class="progreso" id="progreso"></span><span class="reloj" aria-hidden="true">Tiempo: <span id="reloj">0:00</span></span><span class="progreso-barra" id="progreso-barra" aria-hidden="true"></span></div>
      <h3 id="titulo-cepa"></h3>
      <p id="pregunta"></p>
      <div class="escena" id="escena">
        <p class="escena-aviso" aria-hidden="true">En pantallas pequeñas, desliza la imagen hacia los lados para verla entera.</p>
        <div class="escena-scroll" id="escena-scroll" tabindex="0" role="group" aria-label="Imagen de la cepa, desplazable">
          <div class="lienzo" id="lienzo">
            <div class="capa" id="capa-a"><span id="img-a"></span><svg class="cajas" id="cajas-a" viewBox="0 0 1200 521" preserveAspectRatio="none" aria-hidden="true"></svg></div>
            <div class="capa capa-b" id="capa-b"><span id="img-b"></span><svg class="cajas" id="cajas-b" viewBox="0 0 1200 521" preserveAspectRatio="none" aria-hidden="true"></svg></div>
            <span class="divisor" aria-hidden="true"></span>
          </div>
        </div>
        <p class="escena-pie" id="escena-pie"></p>
      </div>
      <div class="descripcion" id="descripcion-cepa" hidden></div>

      <form class="respuesta" id="form-respuesta" novalidate>
        <label class="grande" for="respuesta" id="etiqueta-resp">¿Cuántos racimos hay en esta cepa?</label>
        <div class="stepper"><button type="button" id="menos" aria-label="Un racimo menos">−</button>
          <input id="respuesta" type="number" inputmode="numeric" min="0" max="99" step="1" aria-describedby="ayuda-resp"><button type="button" id="mas" aria-label="Un racimo más">+</button></div>
        <p class="ayuda" id="ayuda-resp">Escribe un número del 0 al 99. Tu mejor estimación vale.</p>
        <p class="ayuda" id="error-resp" role="alert" hidden>Escribe un número para poder comprobarlo.</p>
        <div class="acciones"><button type="submit" class="btn grande" id="comprobar">Comprobar</button></div>
      </form>

      <div id="revelacion" hidden>
        <p class="tu-respuesta" id="tu-respuesta"></p>
        <ul class="leyenda" id="leyenda">
          <li><svg viewBox="0 0 44 22" aria-hidden="true"><rect x="2" y="2" width="40" height="18" rx="2" fill="none" stroke="#fff" stroke-width="6"/><rect x="2" y="2" width="40" height="18" rx="2" fill="none" stroke="#54081F" stroke-width="3"/></svg>Línea continua: racimo que una cámara ve con hojas.</li>
          <li><svg viewBox="0 0 44 22" aria-hidden="true"><rect x="2" y="2" width="40" height="18" rx="2" fill="none" stroke="#E07A10" stroke-width="3" stroke-dasharray="7 5"/></svg>Línea discontinua: racimo que estaba escondido por las hojas.</li>
        </ul>
        <div class="comparador" id="comparador">
          <div class="botones">
            <button type="button" class="btn" id="quitar-hojas">Quitar las hojas</button>
            <button type="button" class="btn secundario" id="ver-con">Ver con hojas</button>
            <button type="button" class="btn secundario" id="ver-sin">Ver sin hojas</button>
          </div>
          <label for="rango"><span class="sr-only">Comparador: </span>Arrastra o usa las flechas del teclado para quitar las hojas poco a poco</label>
          <input type="range" id="rango" min="0" max="100" step="5" value="0" aria-valuetext="Imagen con hojas">
        </div>
        <div class="resultado-paso" id="paso-a" hidden><p class="num" id="paso-a-txt"></p></div>
        <div class="resultado-paso oculto" id="paso-b" hidden><p class="num" id="paso-b-txt"></p></div>
        <div class="resultado-paso" id="paso-c" hidden><p id="paso-c-txt"></p></div>
        <p><button type="button" class="btn grande" id="siguiente" hidden>Siguiente cepa</button></p>
      </div>
    </div>

    <div id="juego-fin" hidden>
      <h3 id="titulo-final">Resultado de la ronda</h3>
      <div class="final-grid">
        <div class="dato"><span class="grande" id="f-cerca"></span><span id="f-cerca-txt"></span></div>
        <div class="dato destacado"><span class="grande" id="f-pct"></span><span id="f-pct-txt"></span></div>
      </div>
      <h4 class="sub-res">Tus números</h4>
      <ul class="tres" id="f-resumen" aria-label="Resumen de la ronda"></ul>
      <div class="caja sirve"><h4>Si la IA ve menos, ¿para qué sirve?</h4><p>En estas fotos, la IA de Televitis encuentra menos racimos que una persona experta. Pero una persona necesita minutos por cepa y la IA, segundos: puede revisar todas las cepas de un viñedo, y no solo unas pocas. Por eso la investigación busca cuándo y cómo mirar para que las hojas tapen menos: contar antes de que crezcan, o después de deshojar (Íñiguez et al., 2021; Íñiguez et al., 2025a). La IA no sustituye a la persona: le da datos de todo el viñedo.</p></div>
      <h4 class="sub-res">¿Y la rapidez?</h4>
      <ul class="tiempos" id="f-tiempos" aria-label="Comparación de tiempos"></ul>
      <div class="vs" id="f-vs">
        <div class="vs-txt" id="f-vs-txt"></div>
        <figure class="vs-foto" id="f-vs-foto" hidden><div class="vs-ico" id="f-vs-ico" hidden></div><img id="f-vs-img" alt="" loading="lazy" width="600" height="400" hidden><figcaption id="f-vs-cap"></figcaption></figure>
      </div>
      <p class="aviso-ia" id="f-aviso"></p>
      <div class="tabla-wrap"><table class="tabla"><caption>Tus respuestas y los datos de cada cepa</caption>
        <thead><tr><th scope="col">Cepa</th><th scope="col">Tu respuesta</th><th scope="col">La IA contó</th><th scope="col">Racimos que ve una persona experta</th><th scope="col">Racimos que aparecen al deshojar</th><th scope="col">Racimos en total sin hojas</th></tr></thead>
        <tbody id="tabla-cuerpo"></tbody></table></div>
      <p class="nota" id="f-mejor"></p>
      <p class="acciones"><button type="button" class="btn" id="f-compartir" data-compartir>Compartir mi resultado</button></p>
      <p class="acciones"><button type="button" class="btn grande" id="otra">Jugar otra ronda</button><a class="btn grande secundario" href="mildiu.html">Pasar al reto del mildiu</a></p>
    </div>
    <p class="sr-only" id="estado" role="status" aria-live="polite" aria-atomic="true"></p>
  </div>
</section>

<section class="bloque" aria-labelledby="despues">
  <div class="wrap">
    <h2 id="despues">Después de jugar: qué hemos aprendido</h2>
    <ol class="ideas">
      <li><p><strong>Las hojas esconden racimos.</strong></p><p>Por eso la IA se usa pronto en la temporada, antes de que crezca la vegetación y tape los racimos (Íñiguez et al., 2025a). En ese estudio, el mejor resultado para bayas pequeñas llegó con luz de día, y para inflorescencias, con iluminación artificial nocturna: cuándo y cómo se mira importa.</p></li>
      <li><p><strong>Contar racimos no es saber los kilos.</strong></p><p>El peso se estima aparte, por ejemplo midiendo la forma y el tamaño del racimo en la foto (Poblete-Echeverría et al., 2025a).</p></li>
      <li><p><strong>La IA no sustituye a quien conoce el viñedo.</strong></p><p>Le da datos antes y de todas las cepas; la decisión sigue siendo de una persona.</p></li>
    </ol>
    <div class="caja" style="margin-top:2rem">
      <h3>Un dato de esta muestra</h3>
      <p class="lead">En las {META['n']} cepas de este reto, las hojas escondían <strong>{META['total_ocultos']} de {META['total_deshojada']} racimos ({fmt(META['porcentaje_agregado'])} %)</strong>.</p>
      <p class="nota">Ojo: son {META['n']} cepas elegidas para mostrar casos fáciles y difíciles, no una muestra representativa de un viñedo. Los «racimos en total sin hojas» son los etiquetados en la imagen sin hojas; no son un recuento de campo. «Racimos que aparecen al deshojar» son los que se ven sin hojas y no con ellas.</p>
    </div>
    <p style="margin-top:1.5rem"><a class="btn" href="juegos.html#proximos">Ver los próximos retos</a></p>
  </div>
</section>

<section class="bloque" aria-labelledby="saber">
  <div class="wrap capas">
    <h2 id="saber">Para saber más</h2>
    <p class="lead">Este reto nace de la <a href="https://investigacion.unirioja.es/documentos/696a8d27be3bb53a465a961c">tesis doctoral de Rubén Iñiguez Mangado</a> (Universidad de La Rioja – ICVV, 2025), sobre cómo estimar la cosecha del viñedo con inteligencia artificial y visión por computador, y de sus artículos: el efecto de las hojas (Íñiguez et al., 2021), el recuento de racimos con IA (Íñiguez et al., 2024) y su detección antes de la floración (Íñiguez et al., 2025a).</p>
    <details><summary>La misma cepa, tres miradas: la IA, una persona y la realidad</summary>
      <div><p>Esta es una de las cepas del reto. Con hojas, el modelo de detección de racimos de <a class="enl-tv" href="https://televitis.unirioja.es/">Televitis</a> encuentra 2 racimos y una persona experta marca 4. Al quitar las hojas aparecen 9. La IA no falla por «no saber» qué es un racimo: falla, como la persona, porque no puede ver lo que está tapado.</p>
      {ff_ctx('fig_tres_miradas_ec',1400,702,'Tres fotos de la misma cepa. Arriba a la izquierda, con hojas, la IA marca 2 racimos con cajas amarillas. Arriba a la derecha, la misma foto con 4 racimos marcados por una persona experta en blanco. Abajo, la cepa sin hojas con 9 racimos: los que estaban tapados, con línea discontinua amarilla. Al lado, las cifras 2, 4 y 9.','La IA y la persona experta miran la foto con hojas; la tercera imagen muestra lo que había.','Elaboración propia a partir de Íñiguez et al. (2024), con fotografías del archivo Televitis (Universidad de La Rioja) y un modelo de Televitis.')}</div></details>
    <details><summary>Las 20 cepas del reto, una a una</summary>
      <div><p>Si se suman las 20 cepas, el modelo encuentra 56 racimos en las fotos con hojas, una persona experta marca 90 y, sin hojas, había 126. En 16 de las 20 cepas la persona ve más racimos que la IA, y en ninguna la IA ve más que la persona. Y cuando la cepa tiene muchos racimos, los dos se quedan lejos de lo que había. Por eso la investigación no se queda en contar lo que se ve: busca cómo corregir lo que las hojas esconden (Íñiguez et al., 2021).</p>
      {ff_ctx('fig_20_cepas_ec',1400,560,'Gráfico de barras con las 20 cepas del reto ordenadas de menos a más racimos. Para cada cepa, una barra clara con los racimos que había sin hojas (de 2 a 11), una barra granate con los que veía una persona experta con hojas y una barra amarilla con los que encontró la IA con hojas. Totales: 126 reales, 90 de la persona experta y 56 de la IA. La IA no encontró ninguno en tres cepas.','Racimos por cepa: lo que había (barra clara), lo que vio una persona experta (granate) y lo que encontró la IA de Televitis (amarillo), siempre en la foto con hojas.','Elaboración propia con las imágenes y etiquetas del reto (Íñiguez et al., 2024) y un modelo de Televitis.')}
      <p>Estas fotos pueden haber servido para entrenar el modelo, así que sirven para ilustrar el problema de las hojas, no para medir su acierto.</p></div></details>
    <details><summary>Artículos de investigación en que se basa este reto</summary>
      <div>{refs_ul(['lau2021', 'jar2021', 'joc2026', 'del2014', 'ini2024', 'ini2021', 'ini2025a', 'pob2025'])}
      <p class="cita">Imágenes y etiquetas del reto: Íñiguez et al. (2024). Todas las clases de racimo del etiquetado original se agrupan aquí como «racimo». Más en <a href="ciencia.html">La ciencia detrás</a> y <a href="creditos.html">Créditos</a>.</p></div></details>
  </div>
</section>'''
    pagina('racimos.html', '¿Cuántos racimos hay?', 'Reto interactivo: estima cuántos racimos hay en cinco cepas con hojas y descubre cuántos escondían las hojas, con imágenes reales de investigación.', cuerpo, ('data/racimos.js', 'data/racimos_ia.js', 'data/comparativas_fotos.js', 'js/comparativas_iconos.js', 'js/comparativas.js', 'js/racimos.js'))

def bloque_vs():
    return """<div id="bloque-vs"><h4 class="sub-res">¿Y la rapidez?</h4>
      <ul class="tiempos" id="f-tiempos" aria-label="Comparación de tiempos"></ul>
      <div class="vs" id="f-vs">
        <div class="vs-txt" id="f-vs-txt"></div>
        <figure class="vs-foto" id="f-vs-foto" hidden><div class="vs-ico" id="f-vs-ico" hidden></div><img id="f-vs-img" alt="" loading="lazy" width="600" height="400" hidden><figcaption id="f-vs-cap"></figcaption></figure>
      </div>
      <p class="aviso-ia" id="f-aviso"></p></div>"""

def mildiu():
    cuerpo = cab_pagina(f'{ICONOS["hoja"]}Detectar', 'hoja', '¿Mildiu o no?', 'Diez imágenes de viñedo. Decide si hay mildiu, como lo haría una persona experta.<span class="nace">Un reto basado en la <a href="https://investigacion.unirioja.es/documentos/681cec665afe3d4f3517e8d6">tesis doctoral de Inés Hernández</a> (Universidad de La Rioja – ICVV, 2025).</span>') + f'''
<section class="bloque" aria-labelledby="antes">
  <div class="wrap capas">
    <h2 id="antes">Antes de jugar: el problema</h2>
    <p class="lead">El {term('mildiu')} (<em>Plasmopara viticola</em>) es una de las enfermedades más destructivas de la vid (Gessler et al., 2011; Poblete-Echeverría et al., 2025b). Detectarlo a tiempo permite tratar justo cuando hace falta y evitar pérdidas.</p>
    <details>
      <summary>Qué es el mildiu</summary>
      <div><div class="duo">{ff('mildiu_05_cepa_completa_con_manchas', 'Cepa con hojas verdes y varias hojas amarillentas con manchas, en un viñedo.', 'Una cepa con mildiu: las manchas aparecen repartidas entre las hojas.')}
      <div><p>El mildiu lo causa <em>Plasmopara viticola</em>, un microorganismo parecido a un hongo (un oomiceto) que vive dentro de los tejidos verdes de la vid, y que se propaga con tiempo húmedo y templado (Gessler et al., 2011). Es una de las enfermedades más destructivas de las zonas vitivinícolas: reduce la cosecha y la calidad de la uva (Poblete-Echeverría et al., 2025b).</p>
      <p>Puede afectar a hojas, brotes y racimos.</p></div></div></div>
    </details>
    <details>
      <summary>Qué es una mancha de aceite</summary>
      <div><div class="duo">{ff('mildiu_01_hoja_mancha_aceite_en_mano', 'Una mano sostiene una hoja de vid con zonas amarillentas y translúcidas.', 'Manchas de aceite en el haz de una hoja.')}
      <div><p>Es el síntoma más reconocible en el haz de la hoja: una zona amarillenta y como translúcida, parecida a una gota de aceite sobre papel. Con el tiempo, el tejido se oscurece y se seca (Gessler et al., 2011; Hernández et al., 2024a).</p></div></div>
      {galeria([('mildiu_19_mancha_aceite_primer_plano', 'Primer plano de una hoja de vid verde con una mancha amarillenta redonda, rodeada de otras hojas con gotas de agua.', 'Una mancha de aceite en primer plano, en una hoja de la cepa.'), ('mildiu_03_hojas_manchas_aceite_amarillas', 'Hojas de vid con manchas amarillas, algunas con el centro pardo.', 'Varias manchas en la misma cepa.'), ('mildiu_15_hoja_necrosis_avanzada', 'Hoja de vid con grandes zonas amarillas y pardas, con el tejido seco.', 'Mildiu avanzado: el tejido se seca y se rompe.')])}</div>
    </details>
    <details>
      <summary>La pelusilla blanca: esporulación</summary>
      <div><div class="duo">{ff('mildiu_17_hoja_enves_esporulacion_en_mano', 'Una mano sostiene una hoja de vid dada la vuelta, con una película blanquecina en el envés.', 'El envés de una hoja con mildiu, con la película blanquecina.')}
      <div><p>Si el ambiente es húmedo, por el envés de la mancha aparece una pelusilla blanquecina. Es la esporulación: el organismo produce las estructuras con las que se propaga a otras hojas (Gessler et al., 2011; Hernández et al., 2024a).</p></div></div>
      {ff('mildiu_20_hoja_haz_enves', 'Dos hojas de vid juntas: a la izquierda el haz, con manchas amarillas de aceite; a la derecha el envés, con una pelusilla blanquecina sobre las manchas.', 'Una misma enfermedad vista por las dos caras: manchas de aceite en el haz (izquierda) y pelusilla blanquecina en el envés (derecha).')}</div>
    </details>
    <details>
      <summary>El mildiu también ataca a los racimos</summary>
      <div>{galeria([('mildiu_04_racimo_joven_afectado', 'Racimo joven con bayas verdes y partes marchitas de color oscuro.', 'Un racimo joven afectado.'), ('mildiu_06_racimo_afectado_en_cepa', 'Racimo de bayas verdes con zonas secas y oscuras, colgando de la cepa.', 'En la cepa, algunas partes del racimo se secan.')])}
      <p>Además de las hojas, la enfermedad puede afectar a los racimos jóvenes (Gessler et al., 2011). Este reto se centra en las hojas: detectar sus síntomas es clave porque suelen ser la primera señal de la enfermedad (Hernández et al., 2024a, 2024b).</p></div>
    </details>
    <details>
      <summary>Qué síntomas buscar</summary>
      <div><div class="duo">{foto('det_inicial', 'Detalle de hojas de vid con manchas pequeñas, pálidas y amarillentas.', 'Primeras manchas: pequeñas, pálidas y fáciles de confundir con otros cambios de color.', 570, 514)}
      <p>Al principio las manchas son muy pequeñas y muy pálidas, por eso cuesta tanto verlas entre tantas hojas (Hernández et al., 2024a). Detectar los síntomas en las hojas es clave porque suelen ser la primera señal de la enfermedad. En el juego, al responder verás marcadas las zonas con mildiu.</p></div></div>
    </details>
    <details>
      <summary>No confundir: el oídio</summary>
      <div>{galeria([('oidio_01_hoja_haz_en_mano', 'Una mano sostiene una hoja de vid con una capa blanquecina difusa en la superficie.', 'Oídio en una hoja.'), ('oidio_04_racimo_bayas_verdes', 'Racimo de bayas verdes con aspecto polvoriento, grisáceo.', 'Oídio en un racimo.'), ('oidio_06_bayas_detalle_polvo_a', 'Bayas verdes en detalle, cubiertas por un polvillo grisáceo.', 'Detalle del polvillo sobre las bayas.')])}
      <p>El oídio (<em>Erysiphe necator</em>) es otra enfermedad importante de la vid, causada por un hongo. Se reconoce por un polvillo ceniciento en hojas y racimos (Gadoury et al., 2012). No es lo mismo que el mildiu, y distinguirlas bien forma parte del trabajo de quien vigila el viñedo.</p></div>
    </details>
    <details>
      <summary>Cómo se hacía</summary>
      <div><p>Tradicionalmente, una persona experta recorre el viñedo y mira las hojas, o se hacen análisis en laboratorio. Es un método laborioso, subjetivo y que exige personal cualificado (Hernández et al., 2021, 2024a).</p></div>
    </details>
    <details>
      <summary>Cómo se hace ahora</summary>
      <div><p>Se fotografía la vegetación, a mano o desde un vehículo en marcha, y redes neuronales buscan los síntomas. En campo, un modelo que localiza zonas con síntomas alcanzó un 86 % de acierto y una puntuación F1 del 82 % al clasificar zonas con y sin síntomas (Hernández et al., 2025). Otro enfoque, que clasifica trozos de imagen y los recorre con una ventana deslizante (EfficientNetV2S), logró un 91 % de acierto y un F1 de 0,92 (Hernández et al., 2024b), y permite ver en qué zonas «se fija» la IA para decidir.</p></div>
    </details>
    <details>
      <summary>Los límites</summary>
      <div><p>Los síntomas iniciales son diminutos, la luz cambia de una foto a otra y algunas hojas con colores raros se parecen al mildiu. Los propios artículos presentan estos resultados como prometedores, no como un problema resuelto, y hablan de validar en condiciones reales (Hernández et al., 2024a, 2024b, 2025).</p></div>
    </details>
  </div>
</section>

<section class="bloque" aria-labelledby="juega">
  <div class="wrap juego-mildiu">
    <h2 id="juega">Ahora te toca a ti</h2>
    <div id="juego-intro">
      <ol class="tres">
        <li><h3>Mira</h3><p>Verás 10 imágenes del viñedo: algunas sanas, otras con mildiu y otras que engañan.</p></li>
        <li><h3>Decide</h3><p>Pulsa «Con mildiu» o «Sin mildiu».</p></li>
        <li><h3>Aprende</h3><p>Después de cada imagen, te explicamos qué había y qué síntomas mirar.</p></li>
      </ol>
      <div class="modo"><input type="checkbox" id="modo-guia" aria-describedby="modo-guia-ayuda"><label for="modo-guia"><strong>Recorrido guiado sin imágenes</strong></label></div>
      <p class="ayuda" id="modo-guia-ayuda">Para quien no puede ver las imágenes: en lugar de jugar, repasas 10 casos con una descripción en texto y su resultado. Las descripciones son generales para cada tipo de caso.</p>
      <p><button type="button" class="btn grande" id="empezar">Empezar la ronda</button></p>
      <p class="nota">Sin límite de tiempo, pero se cuenta cuánto tardas por imagen para compararte con la IA al final. No se guarda nada fuera de tu navegador.</p>
    </div>

    <div id="juego-juego" hidden>
      <div class="juego-cab"><span class="progreso" id="progreso"></span><span class="reloj" aria-hidden="true">Tiempo: <span id="reloj">0:00</span></span><span class="progreso-barra" id="progreso-barra" aria-hidden="true"></span></div>
      <h3 id="titulo-caso" class="sr-only"></h3>
      <p id="pregunta"></p>
      <figure class="figura-juego" id="figura"><span class="lienzo-m" id="lienzo-m"><span id="img-caso"></span></span><figcaption class="sr-only" id="cap-manchas"></figcaption></figure>
      <p class="ctl-manchas" id="ctl-manchas" hidden><button type="button" class="btn secundario" id="ver-manchas" aria-pressed="true">Ocultar manchas marcadas</button> <span class="nota" id="leyenda-manchas">Las zonas rodeadas con línea discontinua las marcaron a mano las personas que etiquetaron la imagen; no es una predicción de la IA.</span></p>
      <div class="botones-resp" id="botones-resp">
        <button type="button" class="btn btn-dash" id="resp-sin">Sin mildiu</button>
        <button type="button" class="btn" id="resp-con">Con mildiu</button>
      </div>
      <div class="resultado-paso" id="feedback" hidden>
        <p class="num" id="fb-titulo"></p><p id="fb-texto"></p><p id="fb-pista" class="nota"></p><p class="estado-ia" id="fb-ia" hidden></p>
      </div>
      <p><button type="button" class="btn grande" id="siguiente" hidden>Siguiente imagen</button></p>
    </div>

    <div id="juego-fin" hidden>
      <h3 id="titulo-final">Resultado de la ronda</h3>
      <div class="final-grid"><div class="dato"><span class="grande" id="f-aciertos"></span><span id="f-aciertos-txt"></span></div><div class="dato" id="f-ia-caja" hidden><span class="grande" id="f-ia"></span><span id="f-ia-txt"></span></div></div>
      <p class="cita">Cómo decide la IA: el modelo de detección de mildiu de Televitis marca, píxel a píxel, las zonas que cree enfermas; aquí cuenta como «tiene mildiu» si marca al menos el 1 % de la imagen. Algunas de estas imágenes pueden haber servido para entrenarlo, así que su acierto aquí es orientativo, no una medida.</p>
      <p id="f-leve"></p>
      <div class="tabla-wrap"><table class="tabla"><caption>Resultados por tipo de imagen</caption>
        <thead><tr><th scope="col">Tipo</th><th scope="col">Imágenes</th><th scope="col">Tus aciertos</th><th scope="col">Aciertos de la IA</th></tr></thead><tbody id="tabla-cuerpo"></tbody></table></div>
      {bloque_vs()}
      <p class="nota" id="f-mejor"></p>
      <p class="acciones"><button type="button" class="btn" id="f-compartir" data-compartir>Compartir mi resultado</button></p>
      <p class="acciones"><button type="button" class="btn grande" id="otra">Jugar otra ronda</button><a class="btn grande secundario" href="racimos.html">Ir al reto de los racimos</a></p>
    </div>
    <p class="sr-only" id="estado" role="status" aria-live="polite" aria-atomic="true"></p>
  </div>
</section>

<section class="bloque" aria-labelledby="despues">
  <div class="wrap">
    <h2 id="despues">Después de jugar: qué hemos aprendido</h2>
    <ol class="ideas">
      <li><p><strong>Detectar pronto es lo difícil.</strong></p><p>Las manchas iniciales son diminutas y se pierden entre las hojas. Si te costaron, estás en buena compañía: es el reto de la investigación.</p></li>
      <li><p><strong>No todo lo que cambia de color es mildiu.</strong></p><p>Una IA, como una persona, puede confundir síntomas parecidos; por eso se entrena con muchos ejemplos etiquetados por personas expertas.</p></li>
      <li><p><strong>La IA ayuda a mirar, la persona decide.</strong></p><p>Localizar los síntomas en todo el viñedo permite tratar solo donde hace falta, pero hay que validar los resultados en campo.</p></li>
    </ol>
    <div class="caja" style="margin-top:2rem"><h3>Qué no hemos hecho aquí</h3>
      <p>En este reto no se ejecuta ningún modelo de IA: las imágenes y su etiqueta proceden del trabajo de las personas que las recogieron y etiquetaron, y los porcentajes de acierto de arriba son los que publican los artículos con sus propios datos de prueba, no los de estas imágenes.</p></div>
    <p style="margin-top:1.5rem"><a class="btn" href="juegos.html#proximos">Ver los próximos retos</a></p>
  </div>
</section>

<section class="bloque" aria-labelledby="saber">
  <div class="wrap capas">
    <h2 id="saber">Para saber más</h2>
    <p class="lead">Este reto nace de la <a href="https://investigacion.unirioja.es/documentos/681cec665afe3d4f3517e8d6">tesis doctoral de Inés Hernández</a> (Universidad de La Rioja – ICVV, 2025) y de sus artículos.</p>
    <details><summary>¿Y cómo se estudia el mildiu en el laboratorio?</summary>
      <div><p>Antes de salir al campo, las investigadoras de <a class="enl-tv" href="https://televitis.unirioja.es/">Televitis</a> inocularon discos de hoja de vid con el patógeno y los fotografiaron día tras día. Así se puede ver cuándo aparecen los primeros síntomas y entrenar a la IA con ejemplos controlados (Hernández et al., 2024a). Con ese aprendizaje, el modelo ya puede mirar una foto de campo:</p>
      {ff_ctx('fig_mapa_ec',1400,480,'Tres imágenes de la misma cepa con hojas: la foto, una máscara en la que las zonas que la IA da por enfermas aparecen en rosa sobre fondo oscuro, y la foto con esas zonas superpuestas, sobre todo en dos hojas con manchas.','La IA no responde «sano» o «enfermo» para toda la foto: dibuja, zona a zona, dónde cree que hay mildiu.','Elaboración propia a partir de Hernández et al. (2024a), con una fotografía del archivo Televitis (Universidad de La Rioja) y un modelo de Televitis.')}
      <p>Fíjate en que marca las zonas con manchas, y en que al principio apenas hay nada que marcar: por eso detectar pronto es tan difícil (Hernández et al., 2024a). Esta imagen puede haber formado parte del entrenamiento del modelo, así que sirve para ilustrar, no para medir su acierto.</p></div></details>
    <details><summary>¿Y en el campo? Una persona experta frente a la IA</summary>
      <div><p>En el viñedo, las manchas son mucho más pequeñas respecto a toda la cepa. En estas imágenes, la columna central es lo que marcó una persona experta y la de la derecha, lo que predijo el modelo. Se parecen, pero no son idénticas: la IA ayuda a mirar y la persona valida. Algunas de estas fotos pueden haber servido para entrenar el modelo, así que no son una prueba de su acierto.</p>
      {ff_ctx('fig_campo_ec',1400,1412,'Tres filas, una por foto de viñedo con hojas: a la izquierda la foto; en el centro, las zonas con síntomas marcadas a mano en amarillo; a la derecha, las zonas que predice la IA en rosa. Se parecen, pero no coinciden del todo.','Cada fila es una foto: imagen (izquierda), síntomas marcados a mano por una persona (centro) y predicción de la IA (derecha).','Elaboración propia a partir de Hernández et al. (2025), con fotografías del archivo Televitis (Universidad de La Rioja) y un modelo de Televitis.')}
      
      <p>También se ha probado con detectores tipo YOLO, que marcan con cajas las hojas con síntomas en cepas completas (Poblete-Echeverría et al., 2025b).</p>
      </div></details>
    <details open><summary>Artículos de investigación en que se basa este reto</summary>
      <div>{refs_ul(['pob2025d', 'her2025', 'her2024', 'her2024b', 'her2021', 'ges2011', 'gad2012'])}
      <p class="cita">Las imágenes son fotografías de viñedo de <a class="enl-tv" href="https://televitis.unirioja.es/">Televitis</a> (Universidad de La Rioja, ICVV); los recortes se han preparado para este juego. Más en <a href="creditos.html">Créditos</a>.</p></div></details>
  </div>
</section>'''
    pagina('mildiu.html', '¿Mildiu o no?', 'Reto interactivo: decide si diez imágenes de viñedo tienen mildiu y aprende qué síntomas buscar, con imágenes reales de investigación.', cuerpo, ('data/mildiu.js', 'data/mildiu_ia.js', 'data/comparativas_fotos.js', 'js/comparativas_iconos.js', 'js/comparativas.js', 'js/vs.js', 'js/mildiu.js'))

# --- próximos retos: contenido por página ---
PROX_INFO = {
 'fases.html': dict(
   que='<p>Saber en qué fase está la vid ayuda a decidir cuándo podar, tratar, regar o vendimiar. Hasta ahora lo hacen personas expertas observando la planta. Un estudio las agrupó en cuatro etapas, según la escala de Eichhorn y Lorenz (E-L) (Coombe, 1995): desarrollo de brotes e inflorescencias (E-L 12–18), floración (E-L 19–26), formación de bayas (E-L 27–33) y maduración (E-L 35–38) (Íñiguez et al., 2025b).</p>',
   cien='<p>En ese estudio se entrenaron tres modelos de IA (ResNet-34, YOLOv11-Clasificación y Vision Transformer) para clasificar fotografías del viñedo en esas cuatro etapas, con 4.381 imágenes. ResNet-34 llegó a un 97,4 % de acierto en validación y un 95,6 % en test. La etapa más difícil fue la floración, que se confundía con las vecinas por su parecido visual (Íñiguez et al., 2025b).</p>' + ff_ctx('fig_fases_etapas_ec', 1400, 520, 'Cuatro fotos de cepas del ICVV ordenadas de abril a septiembre sobre una línea del tiempo: brotes e inflorescencias (E-L 12–18), floración (E-L 19–26, destacada en amarillo como la etapa que más confundía la IA), formación de bayas con racimos verdes (E-L 27–33) y maduración con uva tinta (E-L 35–38).', 'Las cuatro etapas del estudio. La floración, entre los brotes y las primeras bayas, fue la que más confundía la IA.', 'Elaboración propia a partir de Íñiguez et al. (2025b), con fotografías del archivo Televitis (Universidad de La Rioja).'),
   tesis='<p class="lead">Este reto nace de la <a href="https://investigacion.unirioja.es/documentos/696a8d27be3bb53a465a961c">tesis doctoral de Rubén Iñiguez Mangado</a> (Universidad de La Rioja – ICVV, 2025), sobre cómo estimar la cosecha del viñedo con inteligencia artificial y visión por computador. Saber en qué fase está la vid es el primer paso: dice qué se puede contar en cada momento, de las inflorescencias a los racimos maduros (Íñiguez et al., 2025b).</p>',
   idea='Te enseñaremos una foto y tendrás que decir en cuál de las cuatro etapas está la vid.', refs=['ini2025b', 'coo1995', 'pal2020', 'icvv2020'],
   extra_html=f'''<h2>Las cuatro etapas, en imágenes</h2>
  <p>Estas fotografías siguen a varias cepas de la colección de variedades del Instituto de Ciencias de la Vid y del Vino (ICVV), en la Finca Institucional de La Grajera (Logroño), con más de 500 variedades (ICVV, 2020), a lo largo de la campaña. Cada una lleva el nombre de su estado. Fíjate en cómo cambia la planta de una etapa a la siguiente: a veces el cambio es evidente y a veces es muy sutil.</p>
  <h3>1. Desarrollo de brotes e inflorescencias (E-L 12–18)</h3>
  {galeria([('seg_10_R03', 'Cepa con brotes jóvenes de hojas pequeñas y un tronco rugoso.', 'Racimos visibles.'), ('seg_12_G02', 'Cepa con brotes largos de hojas verde claro.', 'Inflorescencias separadas.'), ('seg_14_T03', 'Cepa con brotes largos y hojas abiertas, con zarcillos.', 'Inflorescencias separadas.'), ('seg_16_S09', 'Cepa con muchas hojas verdes y brotes que ya llegan al alambre.', 'Botones florales separados.')])}
  <h3>2. Floración (E-L 19–26)</h3>
  {galeria([('seg_17_T03', 'Cepa con hojas verdes y racimos todavía pequeños entre ellas.', 'Inicio de floración.'), ('seg_17_M04', 'Dos cepas con mucha hoja bajo un cielo azul.', 'Inicio de floración.'), ('seg_17_V08', 'Cepa con hojas verdes muy densas.', 'Final de floración.'), ('seg_17_S09', 'Brotes altos con hojas verdes y zarcillos bajo un cielo azul.', 'Final de floración.')])}
  <h3>3. Formación de bayas (E-L 27–33)</h3>
  {galeria([('seg_18_M04', 'Cepa con hojas verdes y pequeños racimos de bayas verdes que cuelgan bajo ellas.', 'Cuajado.'), ('seg_18_T03', 'Cepa con hojas grandes y un racimo de bayas verdes entre ellas.', 'Cuajado.'), ('seg_19_V08', 'Cepa muy frondosa con racimos de bayas verdes a la izquierda.', 'Baya tamaño guisante.'), ('seg_20_S09', 'Hojas verdes y un racimo de bayas verdes en la parte baja.', 'Baya tamaño guisante.')])}
  <h3>4. Maduración (E-L 35–38)</h3>
  {galeria([('seg_21_M04', 'Cepa con hojas verdes y varios racimos de uva oscura colgando.', 'Envero.'), ('seg_22_G02', 'Cepa con hojas oscuras y racimos de uva tinta a la izquierda.', 'Envero.'), ('seg_22_R03', 'Cepa frondosa con racimos de bayas rosadas al fondo.', 'Envero.'), ('seg_22_V08', 'Cepa con hojas y racimos de uva blanca de color verde dorado.', 'Maduración del fruto.')])}
  <p class="cita">El paso entre etapas es gradual y el estado de cada fotografía se ha asignado por su aspecto, no por una medición de cada cepa. Entre estados hay correspondencias aproximadas con la escala E-L (Coombe, 1995).</p>
  <h3>Y en plena floración, hasta las flores se cuentan</h3>
  <p>Cuando la inflorescencia está abierta, la visión por computador también puede segmentarla y contar sus flores, un dato que ayuda a prever la cosecha mucho antes de que haya uvas (Palacios et al., 2020).</p>
'''),
 'peso.html': dict(
   que='<p>Contar racimos no basta para prever la cosecha: también importa cuánto pesa cada uno. Pesarlos a mano es lento y obliga a cortar el racimo.</p>',
   cien='<p>Un estudio analizó imágenes de 359 racimos de Cabernet-Sauvignon con distintos riegos y extrajo 13 medidas de forma. Con un modelo de regresión por pasos, el área, el perímetro y la circularidad predijeron el peso (R² ajustado = 0,824), con desviaciones en los racimos más grandes (Poblete-Echeverría et al., 2025a).</p>',
   idea='Verás un racimo, estimarás su peso y lo compararás con el real.', refs=['pob2025'],
   extra_html=f'''<h2>De la foto al peso</h2>
  <p>El método fotografía cada racimo sobre un fondo claro con una referencia de tamaño conocido, mide su silueta (área, perímetro, circularidad…) con un programa y la relaciona con el peso real del racimo en una balanza (Poblete-Echeverría et al., 2025a).</p>
  {ff_ctx('fig_peso_ec', 1400, 520, 'Esquema de tres pasos: 1, pesar el racimo en una balanza; 2, fotografiarlo sobre un fondo claro con una referencia de tamaño de 5 centímetros; 3, medir la forma de su silueta (área, perímetro y circularidad) para estimar el peso.', 'El flujo de trabajo: pesar el racimo, fotografiarlo y medir su forma para estimar su peso.', 'Elaboración propia a partir de Poblete-Echeverría et al. (2025a).')}''',
   fotos=[('peso_01_balanza_laboratorio', 'Un racimo de uva tinta sobre una balanza de laboratorio, con el peso visible en la pantalla.', 'Pesar un racimo en el laboratorio: el dato que luego se intenta estimar solo con una foto.'), ('produccion_09_cinco_racimos_tamanos', 'Cinco racimos de uva tinta de distintos tamaños, colocados en fila sobre un papel.', 'Cada racimo es distinto: tamaño, forma y peso.')]),
 'sed.html': dict(
   que='<p>El estado hídrico de la vid afecta al rendimiento y a la calidad de la uva, y el riego es clave para un viñedo sostenible. Medirlo suele requerir una cámara de presión y mucho trabajo planta a planta.</p>',
   cien='<p>Cámaras térmicas montadas en un vehículo que avanza a 5 km/h estiman la sed de la vid con aprendizaje automático. En un trabajo, los modelos alcanzaron valores de R² de hasta 0,62 en validación cruzada y 0,65 en predicción (Gutiérrez et al., 2018b). En otro, dos índices térmicos llegaron a R² de hasta 0,71 frente a la medida de referencia (Gutiérrez et al., 2021).</p>',
   idea='Te mostraremos imágenes térmicas y tendrás que decir qué zona sufre más estrés.', refs=['gut2018a', 'gut2021'],
   fotos=[('@dron_termica', 'Imagen térmica aérea de un viñedo en colores del morado al amarillo: las cepas y el suelo tienen temperaturas distintas.', 'Imagen térmica tomada con un dron: los colores indican la temperatura.', 'Foto: archivo Televitis (Universidad de La Rioja), julio de 2024.'), ('@dron_termica_0108', 'Imagen térmica aérea de un viñedo con filas de cepas moradas y un camino anaranjado.', 'Otra zona del mismo vuelo: las filas más calientes aparecen en tonos más claros.', 'Foto: archivo Televitis (Universidad de La Rioja), julio de 2024.'), ('quad_01_plataforma_quad_atardecer_a', 'Vehículo naranja con una plataforma de cámaras y sensores junto a un viñedo.', 'Las cámaras pueden recorrer las filas montadas en un vehículo.'), ('ia_camara_presion', 'Una cámara de presión: una caja azul con un manómetro y una tapa metálica de la que sale el peciolo de una hoja de vid, delante de un viñedo.', 'Cámara de presión: mide el estado hídrico de una hoja, pero hay que hacerlo planta a planta.', CRED_IA), ('ia_plataforma_termica_recoloreada', 'Vista desde el vehículo de dos filas de viñedo con las hojas coloreadas del morado al amarillo, como en una imagen térmica, y la plataforma de cámaras al frente.', 'Ilustración: una fotografía real de la plataforma, recoloreada para sugerir cómo «ve» una cámara térmica. No es una imagen térmica real.', CRED_IA)]),
 'enfermedades.html': dict(
   que='<p>El mildiu no es la única amenaza. El <strong>oídio</strong>, causado por el hongo <em>Erysiphe necator</em>, cubre de un polvo blanquecino hojas y racimos; es un parásito que solo crece sobre la planta viva (Gadoury et al., 2012). Y la <strong>yesca</strong> (<em>esca</em>, en inglés) es una enfermedad de la madera, asociada a varios hongos, entre ellos <em>Fomitiporia mediterranea</em>, <em>Phaeomoniella chlamydospora</em> y <em>Phaeoacremonium minimum</em> (Del Frari et al., 2021).</p><p>La yesca ataca la cepa por dentro, pero a menudo se delata en las hojas, que se llenan de manchas entre los nervios con un aspecto «atigrado» (en inglés, <em>tiger stripes</em>) (Mugnai et al., 1999; Del Frari et al., 2021).</p>',
   cien='<p>La base del reto del mildiu, una red neuronal que marca sobre la imagen las zonas con síntomas, se describe en Hernández et al. (2025). La idea es extender este tipo de herramientas a otras enfermedades, aunque cada una tiene síntomas distintos que la IA debe aprender por separado, y algunas se confunden fácilmente con otras.</p>',
   idea='Te enseñaremos una hoja o una cepa y tendrás que decir qué le pasa: oídio, mildiu, yesca u otra cosa.', refs=['gad2012', 'del2021', 'mug1999', 'her2025'],
   fotos=[('oidio_02_hoja_brote_polvo_blanco', 'Hoja y brote de vid cubiertos por un polvo blanquecino.', 'Oídio en una hoja y un brote.'), ('oidio_05_racimo_bayas_polvo', 'Racimo de bayas verdes cubiertas de un polvo grisáceo.', 'Oídio en un racimo.'), ('madera_07_hojas_atigradas_g', 'Hojas de vid verdes con zonas rojizas y pardas entre los nervios y en los bordes.', 'Yesca: hojas con manchas «atigradas» entre los nervios.'), ('madera_09_hoja_atigrada_cercana_i', 'Primer plano de una hoja con el borde seco y zonas rojizas entre nervios verdes.', 'Yesca vista de cerca: los nervios siguen verdes y el resto se tiñe.')]),
 'variedades.html': dict(
   que='<p>Reconocer la variedad de una cepa es clave para el viticultor y para la bodega. La ampelografía clásica lo hace observando la forma de la hoja, el color de los brotes y otros rasgos; también se usan análisis de ADN en laboratorio. Pero las hojas de dos variedades pueden parecer casi iguales a simple vista.</p>',
   cien='<p>Un estudio fotografió con una cámara hiperespectral, desde un vehículo en marcha, hojas de 30 variedades en un viñedo de La Rioja. Con 1.200 muestras espectrales, los modelos clasificaron las variedades con puntuaciones de hasta 0,99 en validación cruzada (Gutiérrez et al., 2018a). Es decir: la hoja, vista con una cámara que capta más colores que los nuestros, funciona como un «carné de identidad» de la variedad.</p>',
   idea='Te enseñaremos una hoja y tendrás que adivinar de qué variedad es, a ver si ganas a la máquina.', refs=['gut2018b', 'icvv2020'],
   extra_html=f'''<h2>Seis variedades, seis hojas</h2>
  <p>Estas fotografías son de seis variedades, tres blancas y tres tintas, de la colección de variedades del Instituto de Ciencias de la Vid y del Vino (ICVV) en la Finca Institucional de La Grajera (Logroño), que reúne más de 500 variedades (ICVV, 2020), en la misma época del año. Fíjate en el tamaño de las hojas, en la profundidad de sus cortes (los lóbulos), en el color y en el borde dentado: son los rasgos que la ampelografía lleva siglos mirando.</p>
  {galeria([('seg_20_V08', 'Hojas de vid de color verde claro con bordes dentados y un racimo de bayas verdes.', 'Verdejo (blanca).'), ('seg_19_S09', 'Hojas verdes y un racimo pequeño de bayas verdes.', 'Sauvignon blanc (blanca).'), ('seg_19_R03', 'Hojas verdes de borde dentado y racimos verdes pequeños en la parte baja.', 'Riesling (blanca).'), ('seg_20_T03', 'Hojas oscuras de lóbulos marcados y un racimo de uva tinta.', 'Tempranillo (tinta).'), ('seg_21_G02', 'Hojas verdes y racimos de uva tinta colgando.', 'Garnacha (tinta).'), ('seg_20_M04', 'Hojas verdes grisáceas con racimos de bayas verdes a los lados.', 'Merlot (tinta).')])}'''),
 'color.html': dict(
   que='<p>Antes de vendimiar, bodegas y técnicos necesitan saber cómo va la maduración: azúcar, color… Normalmente se toman muestras y se analizan en laboratorio.</p>',
   cien='<p>Una cámara hiperespectral (400–1000 nm) montada en un vehículo a 5 km/h midió, en el propio viñedo, los sólidos solubles totales (R² de 0,92 en predicción) y los antocianos, los pigmentos del color (R² de 0,83), de uvas Tempranillo. Con ellos se elaboraron mapas de cómo cambia la maduración (Gutiérrez et al., 2019).</p>',
   idea='Verás cómo se ve el viñedo con «ojos» que captan más colores que los nuestros.', refs=['gut2019', 'tej2026', 'hyp'],
   fotos=[],
   extra_html=f'''<h2>El proyecto HyperGrape</h2>
  <p class="logo-proy"><a href="https://hypergrape.unirioja.es/"><img src="img/logo_hypergrape.png" alt="Logotipo del proyecto HyperGrape (abre su web)" width="220" height="47" loading="lazy"></a></p>
  <p>La imagen hiperespectral combina fotografía y espectroscopía: en lugar de tres colores (rojo, verde y azul), registra cientos de bandas de luz, incluidas algunas que el ojo no ve, y cada punto de la imagen tiene así su propia «huella» espectral (Tardaguila et al., 2021; Ferro y Catania, 2023).</p>
  <div class="galeria">{ff('hyper_08_espectro_electromagnetico_vis_nir_swir', 'Esquema del espectro electromagnético con las zonas visible, infrarrojo cercano e infrarrojo de onda corta.', 'El espectro: nuestros ojos solo ven una pequeña parte.', 'Figura: proyecto HyperGrape (Universidad de La Rioja).')}{ff('hyper_09_hipercubo_ejemplo', 'Imagen de una muestra con varios gráficos de espectros asociados a cada zona.', 'Un hipercubo: cada punto de la imagen tiene un espectro.', 'Figura: proyecto HyperGrape (Universidad de La Rioja).')}</div>
  <p><a class="enl-hg" href="https://hypergrape.unirioja.es/">HyperGrape</a> es un proyecto del grupo de investigación <a class="enl-tv" href="https://televitis.unirioja.es/">Televitis</a>, de la Universidad de La Rioja y el Instituto de Ciencias de la Vid y del Vino (ICVV), con María Paz Diago como investigadora principal. Está financiado por el Ministerio de Ciencia, Innovación y Universidades (AEI) y los fondos FEDER de la Unión Europea. Su objetivo es desarrollar tecnologías no invasivas (imagen hiperespectral, multiespectral y RGB) para monitorizar en tiempo real la composición de la uva, tanto en campo como a la entrada de bodega (<a class="enl-hg" href="https://hypergrape.unirioja.es/">HyperGrape</a>, 2025).</p>
  <p>En el viñedo, las cámaras viajan montadas en un vehículo todoterreno que recorre las filas. Trabajan en el visible y el infrarrojo cercano (300–1400 nm) y en el infrarrojo de onda corta (de 1400 nm en adelante), luz que permite ver características de plantas y racimos invisibles para el ojo humano (<a class="enl-hg" href="https://hypergrape.unirioja.es/">HyperGrape</a>, 2025).</p>
  <h3>Así «ve» una cámara hiperespectral</h3>
  <p>Esta imagen no es una fotografía normal: es una vista del infrarrojo de onda corta (900–1700 nm) representada en falso color, y por eso los colores no son los reales. En ella se puede marcar qué píxeles corresponden a racimos y separarlos del resto.</p>
  <div class="galeria pasos">{ff('hyper_12_swir_cepa_original', 'Imagen en falso color de una cepa vista en el infrarrojo, con hojas de tono azul claro, la madera marrón y varios racimos de color azul oscuro colgando.', '1. La imagen hiperespectral, en falso color.', CRH)}{ff('hyper_13_swir_mascara_racimos', 'Imagen en blanco y negro donde las zonas blancas tienen la forma de los racimos y el resto es negro.', '2. Una máscara: lo blanco es lo que corresponde a racimos.', CRH)}{ff('hyper_14_swir_racimos_segmentados', 'La misma imagen en falso color con los racimos cubiertos de azul intenso, que marca las zonas detectadas.', '3. El resultado: los racimos marcados sobre la imagen.', CRH)}</div>
  <p>Al marcar los racimos se puede calcular el espectro solo de las uvas, y relacionarlo con su composición (Tejada-González et al., 2026).</p>
  <figure class="foto-caja foto-ancha">{pf('hyper_01_esquema_hipercubo_segmentacion', 'Esquema: capas de una imagen hiperespectral de una cepa, una máscara con la silueta de los racimos y una curva de reflectancia entre 400 y 1700 nanómetros.')}<figcaption>De la imagen a los datos: se marcan los racimos en la imagen hiperespectral y se calcula su espectro, es decir, cuánta luz refleja la uva en cada longitud de onda. <span class="cred">Figura: proyecto HyperGrape (Universidad de La Rioja).</span></figcaption></figure>
  <div class="galeria">{ff('hyper_04_uvas_en_bandeja_mesa_seleccion', 'Uvas tintas en una bandeja sobre la mesa de selección de una bodega.', 'En la bodega, las uvas pasan por la mesa de selección.', 'Foto: proyecto HyperGrape (Universidad de La Rioja).')}{ff('hyper_05_camara_sobre_mesa_seleccion', 'Una cámara montada sobre una estructura metálica encima de la mesa de selección de una bodega.', 'Una cámara situada sobre la mesa mira las uvas que pasan.', 'Foto: proyecto HyperGrape (Universidad de La Rioja).')}</div>
  <p>La misma idea se lleva a la entrada de bodega, donde las cámaras miran los racimos que llegan (<a class="enl-hg" href="https://hypergrape.unirioja.es/">HyperGrape</a>, 2025). El trabajo se centra en Tempranillo (Tejada-González et al., 2026).</p>
  <p>Ya hay resultados publicados: en Tempranillo tinto, los modelos estimaron azúcares, pH, acidez total y ácido málico con R² de predicción de entre 0,93 y 0,98, y los parámetros de color, con valores de entre 0,81 y 0,89 (Tejada-González et al., 2026).</p>'''),
}

FASES_EL = [  # código E-L, nombre corto, qué se ve, pista, nº de fotos
 (4, 'Brotación', 'Yemas hinchadas y primeros brotes verdes, con hojas diminutas, sobre madera todavía desnuda.', 'Ves la madera vieja casi desnuda y solo puntitos verdes: la planta acaba de despertar.'),
 (9, 'Primeras hojas', 'Brotes de pocos centímetros con dos o tres hojas ya separadas.', 'Hay hojas pequeñas, pero aún no forman una pared verde ni se ven flores.'),
 (12, 'Brotes de 10 cm', 'Brotes largos con cinco hojas o más, y las inflorescencias empiezan a verse.', 'Los brotes ya son largos y las hojas grandes; entre ellas asoman los racimos diminutos de flores.'),
 (17, 'Inflorescencias', 'Brotes con muchas hojas y racimos florales bien desarrollados, con las flores todavía cerradas y separadas.', 'Se ven racimos de botones verdes, todavía sin abrir.'),
 (19, 'Inicio de floración', 'Las primeras flores empiezan a abrirse: caen los primeros capuchones.', 'Los racimos florales siguen verdes pero las primeras flores se abren.'),
 (23, 'Plena floración', 'La mitad de los capuchones ya han caído: los racimos tienen muchas flores abiertas.', 'Hay muchas flores abiertas, con las puntas amarillentas de los estambres.'),
 (27, 'Cuajado', 'Las flores han dado paso a bayas diminutas y verdes que empiezan a crecer.', 'Ya no hay flores: cuelgan racimos de bayas verdes y pequeñas.'),
 (35, 'Envero', 'Las bayas empiezan a ablandarse y a cambiar de color.', 'Las bayas dejan de ser verdes: aparecen tonos rosados, rojizos y morados mezclados.'),
 (38, 'Maduración', 'Las bayas están maduras, oscuras en las variedades tintas, listas para vendimiar.', 'Los racimos son grandes y de un morado casi negro.'),
]
FASES_N = {4: 4, 9: 4, 12: 4, 17: 4, 19: 4, 23: 4, 27: 4, 35: 4, 38: 4}

def fases_juego():
    import json
    dims = {l.split(',')[0]: l.strip().split(',')[1:] for l in open(os.path.join(ROOT, 'img/fases/dims.txt'))}
    etapas = [dict(el=e, n=n, desc=d, pista=p) for e, n, d, p in FASES_EL]
    fotos = [dict(id=k, el=int(k[2:4]), w=int(v[0]), h=int(v[1])) for k, v in sorted(dims.items())]
    data = json.dumps(dict(etapas=etapas, fotos=fotos), ensure_ascii=False)
    nodos = ''.join(f'<span class="nodo"><input type="radio" name="etapa" id="et-{e}" value="{e}"><label for="et-{e}"><span class="cod">E-L {e}</span><span class="nom">{n}</span></label></span>' for e, n, d, p in FASES_EL)
    return f"""<div class="juego-fases" id="juego-fases">
  <h2 id="juega">Ahora te toca a ti</h2>
  <div id="juego-intro">
    <ol class="tres">
      <li><h3>Mira</h3><p>Verás 8 fotos de cepas hechas a lo largo de la campaña.</p></li>
      <li><h3>Sitúa</h3><p>Elige el estado fenológico en la línea del tiempo, de la brotación a la maduración.</p></li>
      <li><h3>Aprende</h3><p>Te decimos en qué estado estaba y qué rasgos mirar. Acertar a un estado de distancia ya tiene mérito.</p></li>
    </ol>
    <p class="ayuda">El juego usa nueve estados de la escala E-L, de la brotación (E-L 4) a la maduración (E-L 38); el estudio de referencia los agrupa en cuatro grandes etapas (Íñiguez et al., 2025b). En este reto no se ejecuta ningún modelo: tu respuesta se compara con el estado anotado por personas expertas, y tu tiempo, con una estimación del tiempo de un modelo de IA.</p>
    <div class="modo"><input type="checkbox" id="modo-guia" aria-describedby="modo-guia-ayuda"><label for="modo-guia"><strong>Recorrido guiado sin imágenes</strong></label></div>
    <p class="ayuda" id="modo-guia-ayuda">Para quien no puede ver las imágenes: repasas los nueve estados con una descripción en texto, en orden.</p>
    <p><button type="button" class="btn grande" id="empezar">Empezar la ronda</button></p>
    <p class="nota">Sin límite de tiempo, pero se cuenta cuánto tardas por foto para compararte con la IA al final. No se guarda nada fuera de tu navegador. Las fotos son del archivo de Televitis, de varias cepas y fechas.</p>
  </div>
  <div id="juego-juego" hidden>
    <div class="juego-cab"><span class="progreso" id="progreso"></span><span class="reloj" aria-hidden="true">Tiempo: <span id="reloj">0:00</span></span><span class="progreso-barra" id="progreso-barra" aria-hidden="true"></span></div>
    <h3 id="titulo-caso" class="sr-only"></h3>
    <figure class="figura-juego" id="figura"><span id="img-caso"></span></figure>
    <fieldset class="linea-tiempo" id="linea"><legend>Elige el estado fenológico (escala E-L)</legend>
      <div class="carril" id="carril">{nodos}</div>
    </fieldset>
    <p><button type="button" class="btn grande" id="comprobar" disabled>Comprobar</button></p>
    <div class="resultado-paso" id="feedback" hidden><p class="num" id="fb-titulo"></p><p id="fb-texto"></p><p id="fb-pista" class="nota"></p></div>
    <p><button type="button" class="btn grande" id="siguiente" hidden>Siguiente foto</button></p>
  </div>
  <div id="juego-fin" hidden>
    <h3 id="titulo-final">Resultado de la ronda</h3>
    <div class="final-grid"><div class="dato"><span class="grande" id="f-aciertos"></span><span id="f-aciertos-txt"></span></div></div>
    <p id="f-cerca"></p>
    {bloque_vs()}
    <p class="nota" id="f-mejor"></p>
    <p class="acciones"><button type="button" class="btn" id="f-compartir" data-compartir>Compartir mi resultado</button></p>
    <p class="acciones"><button type="button" class="btn grande" id="otra">Jugar otra ronda</button><a class="btn grande secundario" href="juegos.html">Ver todos los retos</a></p>
  </div>
  <p class="sr-only" id="estado" role="status" aria-live="polite" aria-atomic="true"></p>
  <script>window.FASES = {data};</script>
  <h2 style="margin-top:2rem">Después de jugar: qué hemos aprendido</h2>
  <ol class="ideas">
    <li><p><strong>Los estados vecinos se parecen.</strong></p><p>El ciclo de la vid es continuo y la escala E-L le pone marcas. Por eso confundir dos estados seguidos es normal, también para una IA: en el estudio, la floración fue la etapa que más se confundía con sus vecinas (Íñiguez et al., 2025b).</p></li>
    <li><p><strong>La foto importa.</strong></p><p>De lejos y con hojas, las flores y las bayas pequeñas apenas se ven. Qué se fotografía, desde dónde y cuándo cambia lo que pueden reconocer una persona y una máquina.</p></li>
    <li><p><strong>Saber la fase ayuda a decidir.</strong></p><p>Tratamientos, riego, deshojado o vendimia dependen del momento del ciclo. Una IA que reconozca la fase en fotos permitiría seguirla en todo el viñedo, y no solo en unas pocas cepas.</p></li>
  </ol>
</div>"""

def galeria_prox(info):
    its = []
    for f in info.get('fotos', []):
        base, alt, cap = f[0], f[1], f[2]; cred = f[3] if len(f) > 3 else CRED
        if base.startswith('@'):
            its.append(f'<figure class="foto-caja">{pic_ctx(base[1:], alt, 640 if base[1:].startswith('dron_termica') else 1000, 512 if base[1:].startswith('dron_termica') else 570)}<figcaption>{cap} <span class="cred">{cred}</span></figcaption></figure>')
        else:
            its.append(ff(base, alt, cap, cred))
    return '<div class="galeria">' + ''.join(its) + '</div>' if its else ''

def proximos():
    for a, i, v, q, g in PROX:
        info = PROX_INFO[a]
        cuerpo = cab_pagina(v, i, q, g + (f'<span class="nace">Un reto basado en la <a href=\"https://investigacion.unirioja.es/documentos/696a8d27be3bb53a465a961c\">tesis doctoral de Rubén Iñiguez Mangado</a> (Universidad de La Rioja – ICVV, 2025).</span>' if a == 'fases.html' else '')) + f'''
<section class="bloque"><div class="wrap narrow capas">
  <h2>El problema</h2>{info['que']}
  {fases_juego() if a == 'fases.html' else ''}
  <h2>Lo que dice la investigación</h2>{info['cien']}
  {galeria_prox(info)}
  {info.get('extra_html', '')}
  {'' if a == 'fases.html' else '<div class="caja discontinua"><h3>Así será el juego</h3><p>' + info['idea'] + '</p></div>'}
  <h2 style="margin-top:2rem">Para saber más</h2>{info.get('tesis', '')}{refs_ul(info['refs'])}
  <p class="vol"><a class="btn secundario" href="juegos.html">Ver todos los retos</a> <a class="btn" href="racimos.html">Jugar ahora a otro reto</a></p>
</div></section>'''
        pagina(a, q, f'{q} {g}', cuerpo, scripts=(('data/comparativas_fotos.js', 'js/comparativas_iconos.js', 'js/comparativas.js', 'js/vs.js', 'js/fases.js') if a == 'fases.html' else ()))

def ciencia():
    cuerpo = cab_pagina('La ciencia detrás', 'fase', 'La ciencia detrás', 'Cómo aprende una IA a mirar un viñedo, qué puede hacer, qué no, y los artículos de donde sale todo.') + f'''
<section class="bloque"><div class="narrow capas">
  <h2>Cómo aprende una IA a ver</h2>
  <p>Una red neuronal no «entiende» un viñedo: aprende patrones a partir de ejemplos. Para enseñarle a encontrar racimos, personas expertas marcan con una caja cada racimo en miles de fotos. Para enseñarle a ver el mildiu, otras personas señalan las zonas con síntomas.</p>
  <p>Después se comprueba con fotos que el modelo no ha visto, para medir cuánto acierta de verdad. Si las fotos de entrenamiento y las de la prueba son muy parecidas, el resultado engaña; por eso los artículos usan conjuntos separados y distintos viñedos.</p>
  <h2>Qué puede hacer</h2>
  <p>Revisar muchas cepas de forma rápida y repetible, localizar racimos o síntomas, y entregar datos de todo el viñedo, no solo de unas pocas plantas. Eso permite decidir antes y con más información.</p>
  <h2>Qué no puede hacer</h2>
  <p>Ver lo que la cámara no ve: si una hoja tapa un racimo, el modelo no lo cuenta. Tampoco funciona igual con cualquier luz, en cualquier fase de la planta o con síntomas muy parecidos. Los artículos lo miden y lo dicen: por ejemplo, la detección temprana de racimos e inflorescencias depende de la fase y de la iluminación (Íñiguez et al., 2025a). Y siempre hace falta validar en campo y que una persona decida.</p>
  <h2>Quién investiga</h2>
  <p>Detrás de los retos hay personas del grupo de investigación <a class="enl-tv" href="https://televitis.unirioja.es/">Televitis</a>, de la <a href="https://www.unirioja.es/">Universidad de La Rioja</a> y del <a href="https://www.icvv.es/">Instituto de Ciencias de la Vid y del Vino (ICVV)</a>. Estas son algunas de ellas:</p>
  <ul class="personas">
    <li><h3>Rubén Iñiguez Mangado</h3><p class="rol">Investigador posdoctoral del ICVV · Autor de esta web</p><p>Doctor en Enología, Viticultura y Sostenibilidad por la Universidad de La Rioja (2025), con mención internacional. Desarrolló en el ICVV su <a href="https://investigacion.unirioja.es/documentos/696a8d27be3bb53a465a961c">tesis sobre cómo estimar la cosecha del viñedo con inteligencia artificial y visión por computador</a>, que aporta <a href="https://www.unirioja.es/una-tesis-desarrolla-nuevas-herramientas-de-inteligencia-artificial-para-prever-con-precision-la-cantidad-de-uva-que-producira-un-vinedo/">nuevas herramientas para prever la cantidad de uva de un viñedo</a>. Es primer autor de los estudios de recuento de racimos y de fases de la vid en que se basan los retos.</p></li>
    <li><h3>María Paz Diago</h3><p class="rol">Profesora Titular de Viticultura (Universidad de La Rioja) · Investigadora del ICVV</p><p>Doctora en Ciencias Agrarias y Alimentarias y Master of Science en Viticultura y Enología por la Universidad de California, Davis. En el ICVV investiga la viticultura de precisión y las tecnologías no invasivas, y es investigadora principal de <a class="enl-tv" href="https://televitis.unirioja.es/">Televitis</a> y del proyecto <a class="enl-hg" href="https://hypergrape.unirioja.es/">HyperGrape</a>. Dirige el Departamento de Agricultura y Alimentación de la Universidad de La Rioja.</p></li>
    <li><h3>Inés Hernández</h3><p class="rol">Doctora por la Universidad de La Rioja (2025)</p><p>Desarrolló en el ICVV su tesis, <a href="https://investigacion.unirioja.es/documentos/681cec665afe3d4f3517e8d6">«Artificial intelligence and non-invasive sensing technologies for early detection of downy mildew in grapevine»</a>, un método con IA y visión artificial para <a href="https://www.unirioja.es/un-nuevo-metodo-basado-en-la-ia-y-la-vision-artificial-permite-detectar-el-mildiu-en-el-vinedo/">detectar el mildiu en el viñedo</a>. Es primera autora de los artículos en que se basa el reto del mildiu y suma 16 artículos y 9 comunicaciones a congresos.</p></li>
    <li><h3>Javier Tardáguila</h3><p class="rol">Catedrático de Viticultura de Precisión (Universidad de La Rioja) · Fundador de Televitis</p><p>Doctor por la Universidad de Padua (Italia) e investigador del ICVV. Trabaja en viticultura de precisión, robótica y tecnologías emergentes. Ha liderado varios proyectos europeos, como NoPest, que buscó nuevas soluciones contra las enfermedades causadas por hongos. Mantiene una intensa transferencia de tecnología con bodegas y empresas.</p></li>
  </ul>
  <h3>El resto del equipo</h3>
  <ul class="personas personas-mini">
    <li><h4>Juan Fernández-Novales</h4><p class="rol">Investigador del ICVV</p><p>Con una larga trayectoria investigadora, es especialista en espectroscopía NIR e imagen hiperespectral en el sector agroalimentario. Analiza datos espectrales y desarrolla modelos para la viticultura de precisión. Es además profesor ayudante doctor del área de Ingeniería Agroforestal de la Universidad de La Rioja.</p></li>
    <li><h4>Ignacio Barrio</h4><p class="rol">Investigador del ICVV</p><p>Investigador predoctoral FPI, matemático e ingeniero informático. Aplica ciencia de datos para estimar la composición de la uva sin tocarla, en el proyecto HyperGrape, y es coautor de más de 20 artículos.</p></li>
    <li><h4>Aitana Tejada</h4><p class="rol">Investigadora del ICVV</p><p>Investigadora predoctoral FPI y graduada en Enología. Prepara su tesis sobre el uso de sensores hiperespectrales para analizar la composición de la uva, y es primera autora del estudio en que se basa «Colores que no vemos» (Tejada-González et al., 2026).</p></li>
    <li><h4>Wenchao Sheng</h4><p class="rol">Investigadora del ICVV</p><p>Investigadora predoctoral y graduada en Enología. Prepara su tesis sobre la detección de residuos de pesticidas en la uva con sensores hiperespectrales.</p></li>
  </ul>
  <p>La investigación se hace también en colaboración con otras universidades: con el profesor titular Salvador Gutiérrez, del <a href="https://www.ugr.es/universidad/organizacion/entidades/departamento-ciencias-computacion-inteligencia-artificial">Departamento de Ciencias de la Computación e Inteligencia Artificial</a> de la Universidad de Granada, y con el profesor Carlos Poblete-Echeverría, de la <a href="https://www.su.ac.za/en/faculties/agrisciences">Facultad de AgriSciences de Stellenbosch University</a> (Sudáfrica). La lista completa de autoras, autores y colaboraciones está en <a href="creditos.html">Créditos</a>.</p>
  {_extra_ciencia()}
  <h2>Glosario</h2>
  <dl class="glosario">{''.join(f'<dt>{k.capitalize()}</dt><dd>{v}</dd>' for k, v in GLOSARIO.items())}
    <dt>Exactitud (acierto)</dt><dd>Porcentaje de casos que el modelo clasifica bien.</dd>
    <dt>F1</dt><dd>Número entre 0 y 1 que resume si el modelo acierta y no se deja casos sin detectar. Cuanto más cerca de 1, mejor.</dd>
    <dt>R²</dt><dd>Cuánto de lo que varía lo explica el modelo. 1 sería perfecto; 0 sería como no saber nada.</dd>
    <dt>Etiquetar</dt><dd>Marcar en una imagen lo que queremos que el modelo aprenda a reconocer.</dd>
  </dl>
  <h2>Artículos citados</h2>
  {refs_ul(['bra2010', 'tar2021', 'fer2023', 'lau2021', 'jar2021', 'del2014', 'ini2024', 'ini2021', 'ini2025a', 'ini2025b', 'pob2025', 'pob2025d', 'ges2011', 'gad2012', 'oiv2019', 'tej2026', 'hyp', 'del2021', 'mug1999', 'her2025', 'her2024', 'her2024b', 'her2021', 'pal2020', 'gut2018a', 'gut2021', 'gut2018b', 'gut2019'])}
</div></section>'''
    pagina('ciencia.html', 'La ciencia detrás', 'Cómo aprende una inteligencia artificial a mirar un viñedo, qué puede y qué no puede hacer, glosario y referencias de los artículos científicos.', cuerpo)

def creditos():
    cuerpo = cab_pagina('Créditos', 'variedad', 'Quién está detrás', 'Autoría, investigación, datos, licencias y cómo se ha hecho esta web.') + f'''
<section class="bloque"><div class="narrow capas">
  <h2>Autoría</h2>
  <p><strong>{AUTOR}</strong>, investigador posdoctoral del grupo Televitis, de la Universidad de La Rioja y del Instituto de Ciencias de la Vid y del Vino (ICVV): idea, textos, diseño y desarrollo de la web.</p>
  <h2>Dónde se investiga</h2>
  <p>Los retos salen de la investigación del grupo <a class="enl-tv" href="https://televitis.unirioja.es/">Televitis</a>, de la <a href="https://www.unirioja.es/">Universidad de La Rioja</a> y del <a href="https://www.icvv.es/">Instituto de Ciencias de la Vid y del Vino (ICVV)</a>. El ICVV es un centro de investigación mixto del Consejo Superior de Investigaciones Científicas (CSIC), el Gobierno de La Rioja y la Universidad de La Rioja, y en su colección de variedades de la Finca de La Grajera (Logroño) se tomaron muchas de las fotos de esta web. Las personas del grupo se presentan en <a href="ciencia.html">La ciencia</a>.</p>
  <h2>Colaboraciones</h2>
  <ul class="lista-simple">
    <li><strong>Salvador Gutiérrez</strong>, profesor titular del Departamento de Ciencias de la Computación e Inteligencia Artificial de la Universidad de Granada. Autor de los trabajos sobre estado hídrico, variedades y color, y codirector de la tesis de Inés Hernández.</li>
    <li><strong>Carlos Poblete-Echeverría</strong>, profesor de Viticultura Digital y Gestión del Agua en el Departamento de Viticultura y Enología de Stellenbosch University (Sudáfrica), donde coordina el grupo de Agricultura Digital del South African Grape and Wine Research Institute (SAGWRI). Autor del estudio sobre el peso del racimo y coautor de los de fases y recuento de racimos.</li>
  </ul>
  <h2>Investigación y datos</h2>
  <p>Todo lo que aquí se juega y se cuenta sale de estos estudios, con estas personas como autoras:</p>
  <ul class="lista-simple">
    <li><strong>Contar racimos:</strong> Rubén Iñiguez, Salvador Gutiérrez, Carlos Poblete-Echeverría, Inés Hernández, Ignacio Barrio, Javier Tardáguila, Fernando Palacios y Eduardo Martínez-Cámara.</li>
    <li><strong>Detectar mildiu:</strong> Inés Hernández (primera autora de los artículos de referencia), Rui Silva, Pedro Melo-Pinto, Salvador Gutiérrez, Ignacio Barrio, Rubén Iñiguez, Sara Ceballos y Javier Tardaguila.</li>
    <li><strong>Fases de la vid:</strong> Rubén Iñiguez, Fikile Wolela, María Ignacia González Pavez, Ignacio Barrio, Javier Tardáguila, Talitha Venter y Carlos Poblete-Echeverría.</li>
    <li><strong>Peso del racimo:</strong> Carlos Poblete-Echeverría, Anke Berry, Talitha Venter, Sergio Velez, María Ignacia González Pavez y Rubén Iñiguez.</li>
    <li><strong>Estado hídrico, variedades y colores:</strong> Salvador Gutiérrez, María-Paz Diago, Juan Fernández-Novales, Rubén Iñiguez y Javier Tardaguila.</li>
  </ul>
  <p>Los modelos de inteligencia artificial que se ejecutan en el Laboratorio y los que ilustran las figuras «Elaboración propia» son del grupo de investigación <a class="enl-tv" href="https://televitis.unirioja.es/">Televitis</a> (Universidad de La Rioja). Son prototipos de investigación.</p>
  <p>Las referencias completas, con su DOI, están en <a href="ciencia.html">La ciencia detrás</a>.</p>
  <h2>Imágenes</h2>
  <p>El vídeo de la portada se ha hecho con cuatro clips generados con Gemini (Google) a partir de descripciones escritas por el autor; el montaje, los fundidos y el texto los ha preparado el autor con ayuda de herramientas de IA. No muestra datos reales.</p>
  <p>En cada imagen, el icono ⓘ muestra su fuente al pasar el cursor, al enfocarlo con el teclado o al tocarlo; las figuras de artículos publicados llevan su cita a la vista.</p>
  <p>Todas las fotografías reales son de <a class="enl-tv" href="https://televitis.unirioja.es/">Televitis</a> (grupo de investigación de la Universidad de La Rioja y del ICVV): unas las ha tomado el autor de la web en el viñedo y otras proceden de la base de datos del grupo. Las imágenes generadas con IA se listan más abajo. Las figuras «Elaboración propia» se han hecho para esta web con fotografías y modelos de Televitis, a partir de los artículos que citan. Gracias al grupo <a class="enl-tv" href="https://televitis.unirioja.es/">Televitis</a> por los datos, las imágenes y las conversaciones que hay detrás de esta web. La única persona identificable en las imágenes es el autor, que ha firmado la autorización de uso de su imagen.</p>
  <p>Las manchas de mildiu marcadas en el juego proceden de las máscaras de segmentación de las personas que etiquetaron las imágenes.</p>
  <p>Las imágenes de dron (visible y térmica, julio de 2024), las fotografías de campo, de plataformas y de enfermedades son del archivo de <a class="enl-tv" href="https://televitis.unirioja.es/">Televitis</a> (Universidad de La Rioja). Las imágenes de cámaras hiperespectrales y de la mesa de selección proceden del proyecto <a class="enl-hg" href="https://hypergrape.unirioja.es/">HyperGrape</a> (grupo <a class="enl-tv" href="https://televitis.unirioja.es/">Televitis</a>, Universidad de La Rioja – ICVV; financiado por el Ministerio de Ciencia, Innovación y Universidades, AEI y FEDER-UE).</p>
  <h2>Imágenes generadas con inteligencia artificial</h2>
  <p>Estas son todas las imágenes generadas con IA de la web:</p>
  <ul class="lista-simple">
    <li>Con Gemini (Google), a partir de fotografías reales del archivo de <a class="enl-tv" href="https://televitis.unirioja.es/">Televitis</a>: la cámara de presión, la plataforma con colores que simulan una imagen térmica y la cámara sobre un trípode en el viñedo (en La ciencia aparece también recortada).</li>
    <li>Con ChatGPT (OpenAI), a partir de descripciones del autor: las cuatro ilustraciones de «Así funciona» del Laboratorio.</li>
    <li>Con Gemini (Google), a partir de descripciones del autor: los cuatro clips del vídeo de la portada.</li>
  </ul>
  <p>Ninguna se usa como dato ni en los juegos: todas las imágenes de los retos y de las enfermedades son fotografías reales.</p>
  <h2>Licencias</h2>
  <p>Los textos, el diseño y el resto de contenidos de esta web se publican bajo <a href="https://creativecommons.org/licenses/by/4.0/deed.es" rel="license">Creative Commons Atribución 4.0 Internacional (CC BY 4.0)</a>; el código, bajo licencia MIT. Los artículos científicos citados mantienen sus propias licencias; consulta cada uno en su enlace.</p>
  <h2>Probada con personas reales</h2>
  <p>Antes de la entrega, unas 20 personas probaron la web y dieron su opinión: 6 viticultores, 6 jóvenes sin relación con el sector, 6 investigadores del ámbito de la viticultura (entre ellos, del grupo <a class="enl-tv" href="https://televitis.unirioja.es/">Televitis</a>) y 2 investigadores de otras áreas, como la química. Sus comentarios se incorporaron a esta versión.</p>
  <h2>Cómo se hizo</h2>
  <p>Los pictogramas de las comparativas de los retos y las figuras «Elaboración propia» se han hecho para esta web (CC BY 4.0).</p>
  <p>La idea, la selección de datos y la revisión científica son de {AUTOR}, que asume la autoría y la responsabilidad final del contenido. Para redactar textos y desarrollar el código se usaron herramientas de inteligencia artificial generativa (Claude, de Anthropic) como apoyo. Ninguna cifra, referencia o resultado ha sido inventado: salen de los artículos y datos citados. La accesibilidad se ha comprobado con herramientas automáticas y pruebas manuales; los detalles están en la <a href="accesibilidad.html">declaración de accesibilidad</a>.</p>
</div></section>'''
    pagina('creditos.html', 'Créditos', 'Autoría, investigación, datos, licencias (CC BY 4.0) y transparencia sobre cómo se ha hecho Entre cepas.', cuerpo)

def _paso_img(n, alt):
    base = f'img/lab/paso{n}'
    if os.path.isfile(os.path.join(ROOT, base + '.jpg')):
        w = h = 800
        try:
            from PIL import Image as _I
            w, h = _I.open(os.path.join(ROOT, base + '.jpg')).size
        except Exception: pass
        webp = f'<source type="image/webp" srcset="{base}.webp">' if os.path.isfile(os.path.join(ROOT, base + '.webp')) else ''
        return f'<picture>{webp}<img src="{base}.jpg" alt="{alt}" width="{w}" height="{h}" loading="lazy"></picture>'
    return ''

def laboratorio():
    pasos = [
        ('1', 'Haz una foto en el campo', 'Con el móvil, a una cepa o a una hoja.', 'Una persona con una gorra hace una foto con el móvil a una cepa de vid en un viñedo.', 'viñedo'),
        ('2', 'Súbela a la plataforma', 'Eliges qué quieres analizar: racimos o mildiu.', 'Una mano sube la foto desde el móvil a una pantalla con el logotipo de la web.', 'subir'),
        ('3', 'La web la analiza', 'Un modelo de inteligencia artificial la examina en unos segundos, en tu propio dispositivo.', 'Una imagen de cepa con cuadrículas y destellos, como si una lupa digital la examinara.', 'analizar'),
        ('4', 'Recibe el resultado', 'Cajas sobre la foto, un número y una explicación en lenguaje claro.', 'Una foto de cepa con recuadros sobre los racimos y un número grande con el recuento.', 'resultado'),
    ]
    items = ''
    nota_ia = ''
    for n, t, d_, alt, _ in pasos:
        im = _paso_img(n, alt)
        items += f'<li class="paso-lab"><span class="paso-num" aria-hidden="true">{n}</span><div class="paso-img{" vacio" if not im else ""}">{im}</div><h3>{t}</h3><p>{d_}</p></li>'
    cuerpo = cab_pagina('Laboratorio', 'racimo', 'Prueba la IA con tu foto', 'Sube una foto de tu viñedo y descubre qué es capaz de ver la inteligencia artificial, y qué no.') + f'''
<section class="bloque"><div class="wrap">
  <h2>Así funciona, en cuatro pasos</h2>
  <ol class="pasos-lab">{items}</ol>
  {nota_ia}
  <h2>Elige qué quieres probar</h2>
  <div class="eleccion">
    <a class="prox-card" href="laboratorio-racimos.html">{icono('racimo')}<h3>Contar racimos</h3><p>La IA marca los racimos que ve en una foto de cepa y te dice cuántos son. Recuerda: solo cuenta los que se ven.</p><span class="mas">Probar</span></a>
    <a class="prox-card" href="laboratorio-mildiu.html">{icono('hoja')}<h3>Detectar mildiu</h3><p>La IA señala las zonas de una hoja o de una cepa que podrían tener mildiu. La decisión final siempre es de una persona.</p><span class="mas">Probar</span></a>
  </div>
  <p class="ayuda">Tus fotos se quedan en tu navegador y no se envían a ningún sitio. El análisis se hace en tu propio dispositivo. Es un prototipo de investigación: puede equivocarse, sobre todo con fotos de móvil.</p>
</div></section>'''
    pagina('laboratorio.html', 'Laboratorio', 'Sube una foto de viñedo y comprueba qué ve la inteligencia artificial.', cuerpo, scripts=('data/lab_ejemplos.js', 'js/sube.js'))

def _lab_tarea(archivo, tarea, chip_t, h1, lead, previsto, consejos, icon):
    EJ = {'racimos': [('img/racimos/B_33_deshojada.jpg', 'Cepa sin hojas'), ('img/racimos/C_37_con_hojas.jpg', 'Cepa con hojas'), ('img/racimos/F_09_deshojada.jpg', 'Otra cepa sin hojas')],
          'mildiu': [('img/mildiu/rm_02.jpg', 'Mildiu avanzado'), ('img/mildiu/rm_10.jpg', 'Mildiu inicial'), ('img/mildiu/rm_19.jpg', 'Hojas sanas')]}
    ejemplos = ' '.join(f'<button type="button" class="btn secundario" data-ejemplo="{src}">{t}</button>' for src, t in EJ[tarea])
    cuerpo = cab_pagina('Laboratorio', icon, h1, lead) + f'''
<section class="bloque"><div class="narrow">
  <form id="sube-form" data-tarea="{tarea}" novalidate>
    <div class="resultado-paso" id="sube-nota-modelo" hidden>
      <p>Esta es la versión de demostración en línea. Los modelos de IA de Televitis siguen en fase de pruebas y se publicarán aquí cuando estén listos, para que cualquiera pueda analizar sus propias fotos. Mientras tanto, puedes ver el resultado real de los modelos sobre las fotos de ejemplo.</p>
      <details class="dev"><summary>Para desarrolladores: cargar un modelo propio</summary><div>
      <p><label for="sube-modelo">Si tienes tu propio modelo en formato ONNX, cárgalo y analiza tus fotos. Se queda en tu navegador, como las fotos.</label><br><input type="file" id="sube-modelo" accept=".onnx"></p>
      <p class="ayuda" id="sube-modelo-estado" role="status" aria-live="polite"></p>
      <details><summary>Qué modelo sirve</summary><div>{'<p>Un detector tipo YOLO (Ultralytics) exportado a ONNX, con entrada de 640 × 640 píxeles en RGB y valores de 0 a 1. Se aceptan las dos salidas habituales: [1, 4 + clases, N] o [1, N, 6] con la supresión de duplicados ya incluida.</p>' if tarea == 'racimos' else '<p>Un modelo de segmentación exportado a ONNX, con entrada de 224 × 224 píxeles en RGB normalizada como ImageNet. La salida puede ser un canal de probabilidad de mildiu o dos canales (fondo y mildiu). La foto se analiza por trozos y se marcan las zonas con probabilidad mayor de 0,95.</p>'}</div></details>
      </div></details>
    </div>
    <p class="ejemplos" id="sube-ejemplos"><strong>¿No tienes una foto a mano?</strong> Prueba con una del archivo de Televitis:<br>{ejemplos}</p>
    <p><label for="sube-foto"><strong>1. Elige una foto</strong></label><br><input type="file" id="sube-foto" accept="image/*"></p>
    <figure id="sube-vista" hidden><img id="sube-img" alt="Vista previa de la foto que has elegido"><figcaption>Tu foto, solo en tu navegador.</figcaption></figure>
    <p><button type="submit" class="btn grande" id="sube-ok">2. Analizar con IA</button></p>
  </form>
  <div id="sube-msg" role="status" aria-live="polite" class="resultado-paso" hidden></div>
  <figure id="sube-res" hidden><canvas id="sube-canvas" role="img" aria-label="Resultado del análisis"></canvas><figcaption id="sube-txt"></figcaption></figure>
  <h2>Lo que verás</h2>
  {previsto}
  <h2>Cómo hacer una buena foto</h2>
  {consejos}
  <p class="ayuda">Tu foto se queda en tu navegador: el análisis se hace en tu propio dispositivo y no se envía a ningún sitio. Es un prototipo de investigación: puede equivocarse, sobre todo con fotos distintas a las de entrenamiento ({'cepas fotografiadas de frente, con cámara fija' if tarea == 'racimos' else 'fotos de campo de alta resolución'}).</p>
  <p style="margin-top:1.5rem"><a class="btn secundario" href="laboratorio.html">Volver al laboratorio</a></p>
</div></section>'''
    pagina(archivo, chip_t, f'{h1}: sube una foto y mira qué ve la inteligencia artificial.', cuerpo, scripts=('data/lab_ejemplos.js', 'js/sube.js'))

def lab_tareas():
    _lab_tarea('laboratorio-racimos.html', 'racimos', 'Contar racimos con IA', 'Contar racimos con IA', 'Sube una foto de una cepa y mira cuántos racimos cuenta la inteligencia artificial.',
        '<ul class="lista-simple"><li>Cajas continuas sobre los racimos que se ven en tu foto.</li><li>El número total de racimos detectados.</li><li>Cuánto ha tardado la IA en tu dispositivo.</li><li>Un recordatorio: los racimos tapados por las hojas no se pueden contar desde la foto.</li></ul>',
        '<ul class="lista-simple"><li>Una sola cepa por foto, vista de frente.</li><li>Con buena luz y sin contraluz.</li><li>Lo bastante cerca para que los racimos se vean, pero con la cepa entera en el encuadre.</li></ul><p class="ayuda">Son consejos orientativos.</p>', 'racimo')
    _lab_tarea('laboratorio-mildiu.html', 'mildiu', 'Detectar mildiu con IA', 'Detectar mildiu con IA', 'Sube una foto de una hoja o de una cepa y mira si la inteligencia artificial ve señales de mildiu.',
        '<ul class="lista-simple"><li>Las zonas sospechosas marcadas sobre tu foto.</li><li>Un aviso claro: «posible mildiu» o «no se ve mildiu».</li><li>Cuánto ha tardado la IA en tu dispositivo.</li><li>Un recordatorio: la IA ayuda a mirar, pero la decisión es de una persona.</li></ul>',
        '<ul class="lista-simple"><li>Enfoca la hoja con buena luz y sin sombras duras.</li><li>Incluye el haz (la cara de arriba), donde aparecen las manchas de aceite.</li><li>Evita fotos movidas o con la hoja mojada.</li></ul><p class="ayuda">Son consejos orientativos.</p>', 'hoja')


def guia_didactica():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import guias
    gs = guias.generar(ref, ROOT, TITULO, SITE_URL)
    items = ''.join(f'''<li class="guia-item"><div><h3>{t}</h3><p>{idea}</p><p class="meta-guia"><strong>Materias:</strong> {mat} · <strong>Duración:</strong> {mn} min</p></div>
      <p><a class="btn" href="guias/{arch}" download>Descargar PDF<span class="sr-only"> de «{t}»</span></a></p></li>''' for _, t, arch, mat, mn, idea in gs)
    cuerpo = cab_pagina('Para docentes', 'variedad', 'Guía didáctica', 'Una guía de una o dos páginas por tema, lista para usar en el aula con los retos de la web.') + f'''
<section class="bloque"><div class="wrap narrow">
  <h2>Cómo usar las guías</h2>
  <p>Cada guía propone una secuencia de <strong>antes, jugar y después</strong>, vocabulario, preguntas para el debate y criterios para evaluar. Está pensada para 3.º–4.º de ESO y Bachillerato y se puede adaptar a otros niveles. Todas las cifras proceden de las investigaciones citadas en cada guía.</p>
  <p>Son PDF etiquetados, con título e idioma, para que se puedan leer con lector de pantalla. Se pueden copiar, adaptar y compartir (CC BY 4.0), citando la autoría.</p>
  <ul class="guias">{items}</ul>
</div></section>'''
    pagina('guia-didactica.html', 'Guía didáctica', 'Guías didácticas descargables para docentes: una por tema, con actividades, vocabulario y preguntas de debate.', cuerpo)


def lenguaje_sencillo():
    cuerpo = cab_pagina('Resumen', 'racimo', 'En pocas palabras', 'Qué es esta web y qué puedes hacer en ella, en lenguaje sencillo.') + '''
<section class="bloque"><div class="wrap narrow sencillo">
  <h2>¿Qué es esta web?</h2>
  <p>Es una web para jugar y aprender.</p>
  <p>Habla de cómo se cuida un viñedo con ayuda de cámaras y de inteligencia artificial (IA).</p>
  <h2>¿Qué es la inteligencia artificial?</h2>
  <p>Es un programa de ordenador que aprende a hacer una tarea con muchos ejemplos.</p>
  <p>Aquí aprende a mirar fotos de viñedo.</p>
  <h2>¿Qué puedes hacer?</h2>
  <ul>
    <li>Contar racimos de uva en una foto.</li>
    <li>Decir si una hoja tiene mildiu. El mildiu es una enfermedad de la vid.</li>
    <li>Decir en qué momento del año está la vid: con brotes, con flores o con uvas.</li>
    <li>Subir tu propia foto para que la IA la mire. La foto no sale de tu móvil u ordenador.</li>
    <li>Comparar lo que tú ves con lo que ve la IA.</li>
  </ul>
  <h2>¿Qué debes recordar?</h2>
  <p>La IA ayuda mucho, pero solo ve lo que ve la cámara.</p>
  <p>Siempre hace falta una persona que mire y decida.</p>
  <h2>¿Cuánto tiempo necesitas?</h2>
  <p>Cada juego dura unos 5 minutos.</p>
  <p><a class="btn" href="racimos.html">Contar racimos</a> <a class="btn" href="mildiu.html">¿Mildiu o no?</a> <a class="btn" href="fases.html">¿En qué fase está la vid?</a></p>
</div></section>'''
    pagina('lenguaje-sencillo.html', 'En pocas palabras', 'Resumen de Entre cepas en lenguaje sencillo: qué es la web, qué puedes hacer y qué debes recordar.', cuerpo)

def sube():
    open(os.path.join(ROOT, 'sube.html'), 'w', encoding='utf-8').write('<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url=laboratorio.html"><title>Laboratorio</title><link rel="canonical" href="laboratorio.html"></head><body><p><a href="laboratorio.html">Ir al laboratorio</a></p></body></html>')

def accesibilidad():
    cuerpo = cab_pagina('Accesibilidad', 'variedad', 'Declaración de accesibilidad', 'Qué se ha hecho para que Entre cepas se pueda usar sin barreras, y cómo avisarnos si encuentras alguna.') + f'''
<section class="bloque"><div class="narrow capas">
  <h2>Qué se ha hecho</h2>
  <ul class="lista-simple">
    <li>Se ha diseñado para cumplir las pautas WCAG 2.1 de nivel AA.</li>
    <li>Todo se puede usar solo con el teclado, con el foco siempre visible y un enlace para saltar al contenido.</li>
    <li>Las imágenes tienen texto alternativo; en los retos, descripciones que no revelan la respuesta.</li>
    <li>Los resultados se anuncian a los lectores de pantalla.</li>
    <li>Nada depende solo del color: se usan líneas continuas y discontinuas, iconos y texto.</li>
    <li>No hay límites de tiempo: los retos miden cuánto tardas solo para compararlo con la IA, sin cuenta atrás. Se respeta la preferencia de reducir movimiento.</li>
    <li>El texto es ampliable hasta el 200 % sin perder contenido; los botones miden al menos 44 × 44 píxeles.</li>
    <li>Hay un modo descripción (racimos) y recorridos guiados en texto (mildiu y fases de la vid) para quien no puede ver las imágenes.</li>
    <li>En el Laboratorio, el resultado del análisis de tu foto se da también en texto y se anuncia a los lectores de pantalla.</li>
    <li>Un glosario explica los términos técnicos.</li>
    <li>Cada página tiene un botón «Escuchar esta página» que la lee en voz alta con la voz de tu navegador (no sustituye a un lector de pantalla).</li>
  </ul>
  <h2>Cómo se ha comprobado</h2>
  <p>Con la herramienta automática axe-core en todas las páginas, en pantalla de ordenador y de móvil, sin incidencias detectadas, y comprobando que no aparece desplazamiento horizontal de la página.</p>
  <h2>Limitaciones conocidas</h2>
  <p>Las pruebas automáticas no detectan todos los problemas, y todavía no se ha probado con lectores de pantalla reales. Si encuentras una barrera, cuéntanoslo.</p>
  <h2>Contacto</h2>
  <p>Rubén Iñiguez Mangado, <a class="enl-tv" href="https://televitis.unirioja.es/">Televitis</a>, Universidad de La Rioja e Instituto de Ciencias de la Vid y del Vino (ICVV): {CONTACTO}.</p>
</div></section>'''
    pagina('accesibilidad.html', 'Declaración de accesibilidad', 'Declaración de accesibilidad de Entre cepas: qué se ha hecho para cumplir WCAG 2.1 AA, cómo se ha comprobado y cómo comunicar una incidencia.', cuerpo)

# --- fotos de las comparativas (opcionales): img/comparativas/<id>.jpg + data/comparativas_creditos.csv ---
import csv
_fotos = {}
_csv = os.path.join(ROOT, 'data', 'comparativas_creditos.csv')
if os.path.exists(_csv):
    for _r in csv.DictReader(open(_csv, encoding='utf-8')):
        _f = os.path.join(ROOT, 'img', 'comparativas', _r['archivo'] or '')
        if _r['archivo'] and os.path.isfile(_f) and _r['autor'].strip() and _r['descripcion_alt'].strip():
            _fotos[_r['id']] = {'src': 'img/comparativas/' + _r['archivo'], 'alt': _r['descripcion_alt'].strip(), 'autor': _r['autor'].strip(), 'licencia': _r['licencia'].strip(), 'url': _r['url_fuente'].strip()}
open(os.path.join(ROOT, 'data', 'comparativas_fotos.js'), 'w', encoding='utf-8').write('window.COMPARATIVAS_FOTOS = ' + json.dumps(_fotos, ensure_ascii=False) + ';\n')
print('Fotos de comparativas con crédito completo:', len(_fotos))

index(); juegos(); racimos(); mildiu(); proximos(); laboratorio(); lab_tareas(); sube(); ciencia(); creditos(); accesibilidad(); guia_didactica(); lenguaje_sencillo()
open(os.path.join(ROOT, 'img', 'favicon.svg'), 'w', encoding='utf-8').write(logo_svg().replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', 1))

malos = []
for a in TODAS:
    t = open(os.path.join(ROOT, a), encoding='utf-8').read()
    if re.search(r'PROVISIONAL|PLACEHOLDER|a verificar|lorem', t, re.I): malos.append(a)
if malos:
    print(('ERROR' if FINAL else 'AVISO') + ': marcadores sin resolver en: ' + ', '.join(malos))
    if FINAL: sys.exit(1)
if SITE_URL:
    pubs = [p for p in TODAS if p != 'sube.html']
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{SITE_URL}/{"" if p == "index.html" else p}</loc></url>\n' for p in pubs) + '</urlset>\n')
    open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8').write(f'User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n')
print('Páginas generadas:', len(TODAS))
