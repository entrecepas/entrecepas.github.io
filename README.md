# Entre cepas · Tú contra la IA en el viñedo

> **Versión de demostración en línea.** Los modelos de IA (carpeta `models/`) siguen en fase de pruebas y se publicarán aquí cuando estén listos. En el Laboratorio se muestran resultados calculados de antemano sobre las fotos de ejemplo, y quien tenga su propio modelo en ONNX puede cargarlo para analizar sus fotos en el navegador.

Web de divulgación científica sobre viticultura de precisión e inteligencia artificial, basada en la investigación del grupo Televitis (Universidad de La Rioja – ICVV). Autor: Rubén Iñiguez Mangado.

Tiene tres retos para jugar (contar racimos, detectar mildiu y reconocer la fase de la vid), seis retos próximos con su base científica, un Laboratorio que analiza fotos con modelos de IA y guías didácticas descargables para docentes.

## Cómo abrirla

**Desde internet:** abre la dirección publicada de la web.

**Desde esta carpeta (Windows):** haz doble clic en `ABRIR_WEB.bat`. Se abre el navegador en `http://localhost:8000`. Cierra la ventana negra para terminar. Necesita Python instalado.

**Desde esta carpeta (macOS o Linux):** en un terminal, dentro de esta carpeta, ejecuta `python3 -m http.server 8000` y abre `http://localhost:8000`.

Si abres `index.html` con doble clic, los juegos y las páginas funcionan, pero el Laboratorio no: el navegador no deja cargar los modelos de IA desde un archivo abierto directamente.

## Qué hay en cada carpeta

| Carpeta o archivo | Contenido |
|---|---|
| `*.html` | Las 19 páginas de la web (generadas, no se editan a mano) |
| `css/`, `js/` | Estilos y comportamiento. `js/vendor/` tiene las librerías de terceros |
| `data/` | Datos de los retos (cepas, imágenes de mildiu, créditos de comparativas) |
| `img/` | Fotografías (archivo Televitis), figuras de elaboración propia e iconos |
| `models/` | Modelos de IA en formato ONNX (Televitis): `racimos.onnx` y `mildiu.onnx` |
| `video/` | Vídeo de la portada y su imagen de vista previa |
| `guias/` | Nueve guías didácticas en PDF accesible, una por tema |
| `capturas/` | Capturas de pantalla de la web |
| `tools/` | Scripts en Python que generan las páginas y las guías |

## Cómo regenerar las páginas

```
python3 tools/build.py            # genera las 19 páginas
python3 tools/build.py --final    # igual, pero falla si queda texto provisional
SITE_URL=https://ejemplo.org python3 tools/build.py   # añade enlaces canónicos, sitemap.xml y robots.txt
```

Las guías en PDF se generan con `tools/guias.py` (necesita Playwright).

## Privacidad

No hay cookies, analítica ni servidor propio. Las fotos que se suben al Laboratorio se analizan en el propio navegador y no se envían a ningún sitio. Los récords de los juegos se guardan solo en el navegador de quien juega.

## Accesibilidad

Diseñada para cumplir WCAG 2.1 AA: uso completo con teclado, textos alternativos, resultados anunciados a lectores de pantalla, recorridos guiados en texto para quien no ve las imágenes, sin límites de tiempo y respeto a la preferencia de reducir movimiento. Comprobada con axe-core en las 19 páginas, a 1280 y 390 px de ancho. Detalles en `accesibilidad.html`.

## Licencias

- Textos, fotografías y figuras propias: CC BY 4.0, salvo que se indique otra cosa en `creditos.html`.
- Código de la web: MIT.
- Modelos de IA: grupo de investigación Televitis (Universidad de La Rioja). Prototipos de investigación.
- Librerías de terceros incluidas: ONNX Runtime Web 1.20.1 (MIT, Microsoft) y qrcode-generator 1.4.4 (MIT, Kazuhiko Arase).

## Contacto

Rubén Iñiguez Mangado · Televitis, Universidad de La Rioja – ICVV · https://investigacion.unirioja.es/investigadores/148703/detalle
