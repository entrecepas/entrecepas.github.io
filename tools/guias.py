# -*- coding: utf-8 -*-
"""Genera las guías didácticas (PDF etiquetado/accesible) a partir de contenidos ya presentes en la web.
Uso: desde build.py -> guias.generar(ref, root)"""
import os, html

COMUN_NIVEL = 'Pensada para 3.º–4.º de ESO y Bachillerato; se puede adaptar a ciclos formativos y a divulgación con público adulto.'

G = [
 dict(id='viticultura-de-precision', archivo='guia_viticultura_de_precision.pdf', web='index.html',
  titulo='Viticultura de precisión: cada cepa cuenta', materias='Biología y Geología · Tecnología y Digitalización · Geografía', min='50',
  idea='Dentro de una misma parcela el suelo y las cepas cambian mucho; la viticultura de precisión mide esas diferencias para actuar donde hace falta.',
  objetivos=['Explicar por qué un viñedo no es uniforme y qué consecuencias tiene gestionarlo como si lo fuera.', 'Nombrar los cinco grandes objetivos de la viticultura de precisión: estimar la producción, vigilar la sanidad, conocer el viñedo, manejar el riego y decidir la vendimia.', 'Distinguir plataformas (satélite, dron, vehículo) y sensores (cámara convencional, térmica, hiperespectral).'],
  vocab=[('Variabilidad','Diferencias de suelo, vigor o producción dentro de una misma parcela.'), ('Vigor','Cuánto crece y cuánta hoja tiene una cepa.'), ('Sensor','Aparato que mide algo, como la luz o la temperatura.'), ('Mapa de zonas','Mapa que divide la parcela según una medida, por ejemplo el vigor.')],
  pasos=[('Antes (10 min)','Mira el vídeo de la portada de «Entre cepas» sin sonido y pide que cada pareja escriba qué ha visto en cada uno de los cuatro clips.'), ('Durante (25 min)','Reparte los cinco objetivos entre cinco grupos. Cada grupo lee la pestaña de su objetivo en la portada y prepara, en una cartulina, una pregunta que la tecnología ayuda a responder y una herramienta que usaría.'), ('Después (15 min)','Puesta en común: cada grupo presenta su objetivo en un minuto. Se construye en la pizarra un mapa que une objetivos, plataformas y sensores.')],
  debate=['Si dos zonas de una parcela son muy distintas, ¿tiene sentido tratarlas igual? ¿Cuándo sí?', '¿Qué ventajas y qué costes tiene medir cada cepa en lugar de la parcela entera?', '¿Qué decisiones debe seguir tomando una persona aunque haya mapas y sensores?'],
  evaluar=['Explica la idea de variabilidad con un ejemplo propio.', 'Relaciona al menos tres objetivos con una herramienta adecuada.', 'Argumenta con cuidado qué puede y qué no puede decidir la tecnología.'],
  ampl=['Dibuja un mapa de vigor de un patio o de un huerto escolar: ¿qué zonas serían «de vigor alto» y por qué?'],
  refs=['bra2010','tar2021','lau2021']),
 dict(id='racimos', archivo='guia_contar_racimos.pdf', web='racimos.html',
  titulo='¿Cuántos racimos hay? Lo que ve la cámara y lo que hay', materias='Matemáticas · Biología y Geología · Tecnología', min='50',
  idea='Una cámara solo cuenta lo que ve: las hojas esconden racimos, y por eso las estimaciones de producción deben tener en cuenta lo oculto.',
  objetivos=['Interpretar un porcentaje y una proporción a partir de datos reales (36 racimos ocultos de 126 en 20 cepas: 28,6 %).', 'Comparar el tiempo que tarda una persona y el que tarda una IA, y detectar qué parte de la comparación es una estimación.', 'Reconocer que un resultado de IA depende de lo que la imagen muestra.'],
  vocab=[('Oclusión','Cuando algo tapa a otra cosa y no se ve (las hojas tapan racimos).'), ('Racimo visible','Racimo que se ve en la foto con hojas.'), ('Estimación','Valor aproximado que se calcula con los datos disponibles.'), ('Detección','Marcar en una imagen dónde está un objeto, aquí un racimo.')],
  pasos=[('Antes (10 min)','Pregunta: «¿Cuántos racimos crees que tiene una cepa?». Anota las respuestas sin corregir. Explica qué es contar racimos y para qué sirve (Laurent et al., 2021).'), ('Jugar (20 min)','Cada estudiante juega el reto «¿Cuántos racimos hay?» en su móvil u ordenador, o en parejas. Al final anotan cuántas cepas quedaron a ±1 racimo y qué porcentaje de racimos estaba escondido.'), ('Después (20 min)','Calcula en clase el porcentaje de racimos ocultos de los resultados de todo el grupo y compáralo con el de los 20 racimos del conjunto de datos (28,6 %). Para la comparación de tiempos, usa los datos que muestra el reto: 2,5 ms por imagen para la IA (Jocher et al., 2026) y unos 15 minutos por cada cuatro cepas para una persona en el campo (Jaramillo et al., 2021). Discute qué hace posible cada tiempo y qué no mide.')],
  debate=['Si una cámara solo ve el 70 % de los racimos, ¿qué se podría hacer para estimar el total?', '¿Es justo comparar la velocidad de una persona y de una IA? ¿Qué se deja fuera?', '¿Qué pasaría si usásemos el recuento de la IA sin tener en cuenta los racimos ocultos?'],
  evaluar=['Calcula e interpreta correctamente un porcentaje a partir de dos cantidades.', 'Distingue «lo que se mide» de «lo que se estima».', 'Explica por qué la IA no cuenta lo que no ve.'],
  ampl=['Repite el reto otro día y compara tus resultados: ¿mejora tu estimación con la práctica?'],
  refs=['lau2021','jar2021','joc2026','ini2024','ini2021']),
 dict(id='mildiu', archivo='guia_detectar_mildiu.pdf', web='mildiu.html',
  titulo='¿Mildiu o no? Mirar con ojo de persona y con ojo de IA', materias='Biología y Geología · Física y Química · Tecnología', min='55',
  idea='El mildiu aparece primero como manchas muy pequeñas y pálidas; una IA puede ayudar a localizarlas, pero sus resultados son prometedores, no un problema resuelto.',
  objetivos=['Describir síntomas del mildiu en hoja: manchas de aceite en el haz y pelusilla blanquecina en el envés.', 'Interpretar medidas de acierto (exactitud y F1) y entender que un 86 % no significa «sin fallos».', 'Valorar por qué detectar pronto es difícil y por qué hace falta validar en condiciones reales.'],
  vocab=[('Mildiu','Enfermedad de la vid causada por un oomiceto.'), ('Haz y envés','Cara superior y cara inferior de la hoja.'), ('Exactitud (acierto)','Porcentaje de casos que el modelo clasifica bien.'), ('F1','Número entre 0 y 1 que resume si el modelo acierta y no se deja casos sin detectar.')],
  pasos=[('Antes (10 min)','Muestra las imágenes de síntomas de la sección «Antes» del reto y pide que describan qué cambia entre una hoja sana y una con mildiu.'), ('Jugar (20 min)','Cada estudiante juega la ronda de diez imágenes. Anotan sus aciertos y qué imágenes les costaron.'), ('Después (25 min)','Mira la sección «Después»: dónde estaba realmente el mildiu y dónde falla la IA. Comparad vuestras confusiones con las de la IA. Calculad el porcentaje de acierto del grupo y relacionadlo con las cifras de los artículos: un modelo de segmentación alcanzó el 86 % de acierto con F1 del 82 %, y otro enfoque el 91 % con F1 de 0,92 (Hernández et al., 2025).')],
  debate=['¿Por qué es más difícil acertar con mildiu en fase temprana?', 'Si un modelo acierta el 91 %, ¿en qué casos fallaría? ¿Qué error sería peor, dar la alarma sin necesidad o no verla?', '¿Quién debe tomar la decisión de tratar: la IA o una persona? ¿Por qué?'],
  evaluar=['Describe los síntomas del mildiu con vocabulario preciso.', 'Interpreta un porcentaje de acierto sin confundirlo con «nunca falla».', 'Razona sobre las limitaciones de una IA entrenada con ciertas imágenes.'],
  ampl=['Busca otra enfermedad o plaga del viñedo y plantea qué imágenes harían falta para entrenar una IA que la reconozca.'],
  refs=['her2025','her2024','pob2025d','ini2025b']),
 dict(id='peso', archivo='guia_peso_del_racimo.pdf', web='peso.html',
  titulo='¿Cuánto pesa este racimo? De la forma al peso', materias='Matemáticas · Biología y Geología', min='45',
  idea='Medir el área, el perímetro y la forma de un racimo en una foto permite estimar su peso sin cortarlo.',
  objetivos=['Entender que se puede predecir una magnitud (el peso) a partir de otras (área, perímetro, forma).', 'Interpretar un coeficiente R² como cuánto explica un modelo.', 'Reconocer desviaciones del modelo en los racimos más grandes.'],
  vocab=[('Regresión','Método para predecir un valor a partir de otros.'), ('R²','Cuánto de lo que varía lo explica el modelo; 1 sería perfecto.'), ('Circularidad','Medida de lo redondo que es un contorno.'), ('Perímetro','Longitud del contorno de una figura.')],
  pasos=[('Antes (10 min)','Plantea: «¿Podemos saber cuánto pesa algo solo mirándolo?». Cada estudiante estima el peso de tres objetos del aula y luego los pesa.'), ('Actividad (25 min)','Con papel cuadriculado, dibuja el contorno de cuatro hojas o piedras de distintos tamaños, calcula área y perímetro contando cuadros y relaciónalos con su peso.'), ('Después (10 min)','Lee cómo lo hizo el estudio: 359 racimos de Cabernet-Sauvignon, 13 medidas de forma y un modelo en el que área, perímetro y circularidad predijeron el peso con un R² ajustado de 0,824 (Poblete-Echeverría et al., 2025).')],
  debate=['¿Por qué el modelo falla más en los racimos más grandes?', '¿Qué otras magnitudes podrían ayudar a estimar el peso?'],
  evaluar=['Calcula área y perímetro de figuras sencillas.', 'Explica con palabras qué indica un R² de 0,82.'],
  ampl=['Representa en una gráfica área frente a peso con los datos de la clase y dibuja una recta que se ajuste.'],
  refs=['pob2025d','lau2021']),
 dict(id='enfermedades', archivo='guia_otras_enfermedades.pdf', web='enfermedades.html',
  titulo='¿Qué enfermedad es? Oídio y yesca', materias='Biología y Geología', min='45',
  idea='Cada enfermedad deja síntomas distintos, y una IA debe aprenderlos por separado; algunas se confunden con otras.',
  objetivos=['Diferenciar oídio (polvo blanquecino sobre hojas y racimos) de yesca (enfermedad de la madera que se delata en las hojas).', 'Entender que un parásito obligado solo crece sobre la planta viva.', 'Explicar por qué una IA entrenada para una enfermedad no sirve sin más para otra.'],
  vocab=[('Hongo','Organismo que se alimenta de otros seres vivos o de materia orgánica.'), ('Parásito obligado','Organismo que solo puede crecer sobre un huésped vivo.'), ('Síntoma','Cambio visible que produce la enfermedad.'), ('Atigrado','Aspecto de manchas entre los nervios de la hoja en la yesca.')],
  pasos=[('Antes (10 min)','Pide que describan qué síntomas esperan ver en una planta enferma. Anota las ideas.'), ('Actividad (25 min)','Con las fotos de la página del reto, completa una tabla: enfermedad, órgano afectado, síntoma visible, posible confusión.'), ('Después (10 min)','Debate: ¿qué necesitaría una IA para reconocer cada una?')],
  debate=['¿Por qué conviene detectar la yesca por las hojas si ataca la madera?', '¿Cómo se evitarían confusiones entre enfermedades parecidas?'],
  evaluar=['Completa la tabla con precisión.', 'Explica por qué cada enfermedad exige datos propios.'],
  ampl=['Investiga cómo se llama la enfermedad más habitual en el cultivo de tu zona.'],
  refs=['gad2012','del2021','mug1999','her2025']),
 dict(id='variedades', archivo='guia_variedades.pdf', web='variedades.html',
  titulo='¿Qué variedad es? Hojas, luz y carné de identidad', materias='Biología y Geología · Física y Química', min='50',
  idea='Las hojas de dos variedades pueden parecer iguales a simple vista, pero una cámara que capta más colores que los nuestros las distingue.',
  objetivos=['Explicar para qué sirve conocer la variedad de una cepa.', 'Relacionar la luz visible y la que no vemos con la información que aporta una cámara hiperespectral.', 'Interpretar un resultado de clasificación: 30 variedades, 1.200 muestras y puntuaciones de hasta 0,99 en validación cruzada.'],
  vocab=[('Variedad','Tipo de vid con características propias, como Tempranillo o Garnacha.'), ('Ampelografía','Estudio y descripción de las vides por su aspecto.'), ('Hiperespectral','Cámara que registra cientos de bandas de luz.'), ('Validación cruzada','Forma de comprobar un modelo repartiendo los datos en varios grupos.')],
  pasos=[('Antes (10 min)','Observa hojas de dos plantas parecidas y pide que describan diferencias.'), ('Actividad (25 min)','Con un prisma o una linterna y papeles de colores, explica que un objeto refleja unas luces más que otras; relaciónalo con la huella espectral de una hoja.'), ('Después (10 min)','Lee el estudio con 30 variedades y comenta qué significa «0,99» (Gutiérrez et al., 2018).')],
  debate=['¿Qué ventajas tiene reconocer la variedad sin análisis de ADN?', '¿Qué ocurriría si el modelo solo hubiera visto hojas de un viñedo?'],
  evaluar=['Explica qué es una huella espectral.', 'Interpreta una puntuación de 0,99 con cuidado.'],
  ampl=['Fotografía hojas de varias plantas y clasifícalas por rasgos visibles.'],
  refs=['gut2018a','gut2018b','tar2021']),
 dict(id='fases', archivo='guia_fases_de_la_vid.pdf', web='fases.html',
  titulo='¿En qué fase está la vid? Cuatro etapas, una foto', materias='Biología y Geología · Matemáticas', min='50',
  idea='Reconocer la fase del ciclo de la vid ayuda a decidir cuándo podar, tratar, regar o vendimiar; una IA aprendió a clasificarla con fotos.',
  objetivos=['Ordenar las cuatro etapas según la escala de Eichhorn y Lorenz: brotes e inflorescencias, floración, formación de bayas y maduración.', 'Interpretar acierto en validación y en test (97,4 % y 95,6 %).', 'Explicar por qué la floración es la etapa más difícil de clasificar.'],
  vocab=[('Fase fenológica','Etapa del ciclo anual de la planta.'), ('Escala E-L','Escala numérica que describe las fases de la vid.'), ('Validación y test','Dos conjuntos de imágenes para comprobar un modelo; el de test no se usa para entrenar.'), ('Inflorescencia','Conjunto de flores.')],
  pasos=[('Antes (10 min)','Ordena en la pizarra las cuatro etapas con las fotos de la página del reto.'), ('Actividad (25 min)','Jugad una ronda del reto: ocho fotos que hay que situar en la línea del tiempo de la escala E-L. Calcula el acierto del grupo, exacto y a una fase de distancia, y compáralo con el de la IA.'), ('Después (10 min)','Lee por qué la floración se confunde con etapas vecinas y comenta qué haría falta para mejorar (Íñiguez et al., 2025b).')],
  debate=['¿Por qué una foto en un día puede ser difícil de clasificar si el cambio es gradual?', '¿Qué decisiones del viñedo dependen de la fase?'],
  evaluar=['Ordena las etapas correctamente.', 'Interpreta porcentajes de acierto de dos conjuntos distintos.'],
  ampl=['Fotografía una misma planta cada semana durante un mes y describe sus cambios.'],
  refs=['ini2025b','coo1995','bag1952']),
 dict(id='sed', archivo='guia_estres_hidrico.pdf', web='sed.html',
  titulo='¿Qué cepa tiene sed? Ver la temperatura', materias='Física y Química · Biología y Geología', min='50',
  idea='Una planta con sed se calienta más; una cámara térmica puede ayudar a estimar su estado hídrico desde un vehículo en marcha.',
  objetivos=['Relacionar temperatura y evaporación en una planta.', 'Leer una imagen térmica y su escala de colores.', 'Interpretar un R² de 0,62 a 0,71 como un resultado útil pero limitado.'],
  vocab=[('Estado hídrico','Cuánta agua tiene disponible la planta.'), ('Térmica','Imagen en la que el color indica temperatura.'), ('Evaporación','Paso de agua líquida a vapor; enfría la hoja.'), ('Referencia','Medida que se considera el patrón con el que se compara.')],
  pasos=[('Antes (10 min)','Experimento: moja un paño y otro no, déjalos al sol y toca su temperatura. Relaciónalo con la hoja.'), ('Actividad (25 min)','Con las imágenes térmicas de la página del reto, identifica zonas más cálidas y propón hipótesis.'), ('Después (10 min)','Lee los resultados: cámaras térmicas a 5 km/h, R² de hasta 0,62 y 0,65 (Gutiérrez et al., 2018) y de hasta 0,71 (Gutiérrez et al., 2021).')],
  debate=['¿Qué otras causas podrían calentar una hoja además de la sed?', '¿Para qué serviría saber qué zonas necesitan más agua?'],
  evaluar=['Explica por qué una hoja con sed se calienta.', 'Lee una escala de colores de una imagen térmica.'],
  ampl=['Mide con un termómetro infrarrojo la temperatura de distintas superficies del patio y compáralas.'],
  refs=['gut2018a','gut2021','tar2021']),
 dict(id='color', archivo='guia_colores_que_no_vemos.pdf', web='color.html',
  titulo='Colores que no vemos: madurez de la uva con luz', materias='Física y Química · Biología y Geología', min='50',
  idea='La luz que no vemos esconde información sobre la composición de la uva antes de probarla.',
  objetivos=['Situar la luz visible en el espectro electromagnético, junto al infrarrojo.', 'Entender qué son los sólidos solubles y los antocianos.', 'Interpretar un R² de 0,92 y 0,83 como una predicción buena pero que depende de las condiciones del estudio.'],
  vocab=[('Espectro','Conjunto de colores o longitudes de onda de la luz.'), ('Infrarrojo','Luz que no vemos, de mayor longitud de onda que el rojo.'), ('Antocianos','Pigmentos que dan color a la uva tinta.'), ('Sólidos solubles','Medida relacionada con los azúcares de la uva.')],
  pasos=[('Antes (10 min)','Con un prisma o un CD, muestra el espectro visible y pregunta qué habrá «más allá» del rojo.'), ('Actividad (25 min)','Con el esquema del espectro de la página del reto, sitúa dónde mira cada cámara (400–1000 nm) y qué zonas no vemos.'), ('Después (10 min)','Lee el estudio con cámara a 5 km/h y Tempranillo: R² de 0,92 para sólidos solubles y de 0,83 para antocianos (Gutiérrez et al., 2019).')],
  debate=['¿Qué ventajas tiene medir la madurez sin cortar las uvas?', '¿Por qué los resultados de un viñedo pueden no valer para otro?'],
  evaluar=['Sitúa el visible y el infrarrojo en el espectro.', 'Explica por qué la luz informa de la composición.'],
  ampl=['Investiga qué otras cosas se miden con luz que no vemos (por ejemplo, el mando de la tele).'],
  refs=['gut2019','tej2026','hyp']),
]

CSS = '''
@page { size: A4; margin: 18mm 16mm 18mm 16mm; }
* { box-sizing: border-box; }
body { font-family: 'Inter', Arial, sans-serif; font-size: 10.5pt; line-height: 1.45; color: #1F1A17; }
h1 { font-family: 'DejaVu Serif', Georgia, serif; font-size: 22pt; color: #5A0F26; margin: 0 0 4pt; line-height: 1.15; }
h2 { font-size: 12.5pt; color: #5A0F26; margin: 14pt 0 4pt; border-bottom: 2px solid #5A0F26; padding-bottom: 2pt; }
.cab { background: #FBF3E6; border-left: 8px solid #5A0F26; padding: 10pt 12pt; margin-bottom: 8pt; }
.meta { font-size: 9.5pt; color: #3a302a; margin: 2pt 0; }
.idea { font-size: 12pt; font-weight: 600; margin: 8pt 0; }
ul, ol { margin: 3pt 0 3pt 16pt; padding: 0; } li { margin-bottom: 3pt; }
dl { margin: 3pt 0; } dt { font-weight: 700; } dd { margin: 0 0 3pt 0; }
.pie { margin-top: 14pt; font-size: 8.5pt; color: #3a302a; border-top: 1px solid #999; padding-top: 4pt; }
.refs li { font-size: 8.5pt; }
a { color: #5A0F26; }
'''

def doc(g, ref, titulo_web, url_base):
    li = lambda xs, tag='ul': f'<{tag}>' + ''.join(f'<li>{x}</li>' for x in xs) + f'</{tag}>'
    voc = '<dl>' + ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in g['vocab']) + '</dl>'
    pasos = ''.join(f'<li><strong>{k}.</strong> {v}</li>' for k, v in g['pasos'])
    refs = '<ul class="refs">' + ''.join(f'<li>{ref(k)}</li>' for k in g['refs']) + '</ul>'
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Guía didáctica: {g['titulo']} · {titulo_web}</title><style>{CSS}</style></head><body>
<header class="cab"><p class="meta">Guía didáctica · {titulo_web}</p><h1>{g['titulo']}</h1>
<p class="meta"><strong>Nivel:</strong> {COMUN_NIVEL}</p><p class="meta"><strong>Materias:</strong> {g['materias']} · <strong>Duración orientativa:</strong> {g['min']} minutos</p></header>
<p class="idea">Idea clave: {g['idea']}</p>
<h2>Qué aprenderá el alumnado</h2>{li(g['objetivos'])}
<h2>Vocabulario</h2>{voc}
<h2>Secuencia sugerida</h2><ol>{pasos}</ol>
<h2>Preguntas para el debate</h2>{li(g['debate'])}
<h2>Cómo evaluar</h2>{li(g['evaluar'])}
<h2>Para ampliar</h2>{li(g['ampl'])}
<h2>Referencias</h2>{refs}
<p class="pie">Material de {titulo_web}, de Rubén Iñiguez Mangado (Universidad de La Rioja / Instituto de Ciencias de la Vid y del Vino, ICVV). Licencia CC BY 4.0. Los datos y cifras proceden de las investigaciones citadas; si la actividad usa el reto en línea, el enlace es {url_base}{g['web']}. Las cifras de los artículos son resultados de investigación en condiciones concretas y no deben generalizarse.</p>
</body></html>'''

def generar(ref, root, titulo_web, site_url=''):
    from playwright.sync_api import sync_playwright
    out = os.path.join(root, 'guias'); os.makedirs(out, exist_ok=True)
    base = (site_url + '/') if site_url else ''
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        for g in G:
            pg.set_content(doc(g, ref, titulo_web, base), wait_until='load')
            pg.pdf(path=os.path.join(out, g['archivo']), format='A4', print_background=True, tagged=True, outline=True, prefer_css_page_size=True)
        b.close()
    return [(g['id'], g['titulo'], g['archivo'], g['materias'], g['min'], g['idea']) for g in G]
