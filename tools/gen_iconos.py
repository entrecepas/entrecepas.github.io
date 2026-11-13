"""Genera js/comparativas_iconos.js: pictogramas minimalistas propios (CC BY 4.0) para las comparativas."""
import json, math, os
G, O, V, C, S = '#54081F', '#E07A10', '#5E6619', '#FBF3E4', '#F3E6CC'
ST = f'stroke="{G}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"'
def p(d, fill='none', extra=''): return f'<path d="{d}" fill="{fill}" {ST} {extra}/>'
def c(x, y, r, fill='none', stroke=True): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" {ST if stroke else ""}/>'
def r(x, y, w, h, fill='none', rx=0, stroke=True, extra=''): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {ST if stroke else ""} {extra}/>'
def ln(d, col=G, w=3): return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
def poly(pts, fill, stroke=True): return f'<polygon points="{pts}" fill="{fill}" {ST if stroke else ""}/>'
def dots(n, y=106):
    x0 = 60 - (n - 1) * 8
    return ''.join(c(x0 + i * 16, y, 4, O, False) for i in range(n))
def barril(n):
    return (p('M30 22 C20 46 20 66 30 90 H90 C100 66 100 46 90 22Z', O) + ln('M26 38 H94') + ln('M22 56 H98') + ln('M26 74 H94') + c(60, 56, 5, C) + dots(n, 104))
I = {}
I['parpadeo'] = p('M12 60 Q60 18 108 60 Q60 102 12 60Z', C) + c(60, 60, 17, V) + c(60, 60, 7, G, False) + ln('M32 36 L26 26') + ln('M60 28 V16') + ln('M88 36 L94 26')
I['latido'] = p('M60 100 C16 70 12 38 34 28 C47 23 57 31 60 40 C63 31 73 23 86 28 C108 38 104 70 60 100Z', G) + ln('M14 62 H42 L50 44 L62 80 L70 58 H106', C, 4)
I['luz-sol'] = c(30, 60, 17, O) + ''.join(ln(f'M{30+24*math.cos(a):.0f} {60+24*math.sin(a):.0f} L{30+30*math.cos(a):.0f} {60+30*math.sin(a):.0f}', O, 3) for a in [i*math.pi/4 for i in range(8)]) + ln('M56 60 H86', O, 3).replace('fill="none"', 'fill="none" stroke-dasharray="3 6"') + c(100, 60, 11, V)
I['cancion-pop'] = f'<ellipse cx="38" cy="88" rx="13" ry="9" fill="{G}"/><ellipse cx="82" cy="78" rx="13" ry="9" fill="{G}"/>' + ln('M50 88 V34', G, 4) + ln('M94 78 V26', G, 4) + poly('50,34 94,26 94,40 50,48', G, False)
I['huevo-duro'] = p('M60 16 C88 16 100 56 100 74 C100 96 82 106 60 106 C38 106 20 96 20 74 C20 56 32 16 60 16Z', C) + c(60, 76, 17, O) + ln('M44 50 C46 44 50 40 54 38', S, 4)
I['tortilla'] = c(60, 60, 46, C) + c(60, 60, 35, '#F0B04A') + ln('M60 60 L94 48') + ln('M60 60 L88 82') + ''.join(c(x, y, 3, C, False) for x, y in [(44, 48), (50, 74), (38, 64), (66, 40), (72, 66)])
I['partido-futbol'] = c(60, 60, 40, C) + poly('60,44 75,55 69,72 51,72 45,55', G) + ln('M60 44 V22') + ln('M75 55 L96 48') + ln('M69 72 L82 90') + ln('M51 72 L38 90') + ln('M45 55 L24 48')
I['iss'] = c(60, 120, 56, V) + ln('M44 38 H76', G, 4) + r(52, 30, 16, 16, C, 2) + r(12, 24, 30, 28, O, 2) + r(78, 24, 30, 28, O, 2) + ln('M27 24 V52', G, 2) + ln('M93 24 V52', G, 2)
I['pelicula-maraton'] = r(16, 50, 88, 50, G, 4) + f'<g transform="rotate(-9 16 48)">' + r(16, 32, 88, 16, C, 3) + ''.join(poly(f'{x},32 {x+10},32 {x+4},48 {x-6},48', G, False) for x in [26, 48, 70, 92]) + '</g>' + poly('52,62 52,88 76,75', C)
I['vuelo-nueva-york'] = f'<ellipse cx="44" cy="96" rx="28" ry="6" fill="{S}"/><g transform="rotate(-25 60 58)">' + p('M12 58 Q12 50 28 50 H98 Q110 54 110 58 Q110 62 98 66 H28 Q12 66 12 58Z', C) + p('M56 50 L40 20 H52 L80 50Z', G) + p('M56 66 L40 96 H52 L80 66Z', G) + p('M20 52 L14 38 H24 L32 52Z', G) + '</g>'
I['dia-entero'] = p('M60 20 A40 40 0 0 0 60 100Z', O) + p('M60 20 A40 40 0 0 1 60 100Z', G) + c(78, 44, 2.5, C, False) + c(88, 66, 2, C, False) + c(74, 82, 2.5, C, False) + c(40, 60, 8, '#F8D58E')
I['apolo-11'] = c(60, 66, 42, S) + c(44, 80, 8, '#D9C6A3') + c(78, 86, 6, '#D9C6A3') + c(84, 62, 5, '#D9C6A3') + ln('M52 52 V16', G, 3) + r(52, 16, 28, 16, O, 1)
I['fermentacion'] = p('M36 16 H84 C84 56 76 68 60 70 C44 68 36 56 36 16Z', C) + p('M40 36 H80 C79 56 74 64 60 66 C46 64 41 56 40 36Z', G, '') + ln('M60 70 V98') + ln('M42 100 H78') + c(52, 52, 3, C, False) + c(66, 46, 2.5, C, False) + c(60, 58, 2, C, False)
I['juegos-olimpicos'] = poly('42,12 60,50 78,12', V) + ln('M42 12 L60 50 L78 12', G, 3) + c(60, 76, 26, O) + poly('60,60 64,72 76,72 66,80 70,92 60,85 50,92 54,80 44,72 56,72', C, False)
I['tour-francia'] = c(32, 78, 22) + c(88, 78, 22) + ln('M32 78 L56 78 L46 48 H78 L56 78') + ln('M78 48 L88 78') + ln('M40 44 H54') + ln('M72 40 H86 L78 48') + c(56, 78, 4, O, False)
I['mundial-futbol'] = p('M38 18 H82 V44 C82 60 72 68 60 68 C48 68 38 60 38 44Z', O) + ln('M38 26 C22 26 22 50 40 52') + ln('M82 26 C98 26 98 50 80 52') + ln('M60 68 V84') + r(40, 84, 40, 14, G, 2)
I['camino-santiago'] = p('M60 100 L20 52 C30 22 90 22 100 52Z', O) + ''.join(ln(f'M60 100 L{x} {y}') for x, y in [(34, 36), (47, 28), (60, 26), (73, 28), (86, 36)]) + ln('M48 100 H72')
I['ciclo-vid'] = p('M60 14 L72 34 L92 32 L82 50 L98 66 L76 68 L60 92 L44 68 L22 66 L38 50 L28 32 L48 34Z', V) + ln('M60 92 V40', C, 2) + ln('M60 68 L40 56', C, 2) + ln('M60 68 L80 56', C, 2) + ''.join(c(x, y, 5, G, False) for x, y in [(86, 90), (98, 90), (92, 100), (80, 100), (104, 100), (92, 80)])
I['viaje-marte'] = c(78, 78, 30, O) + c(70, 86, 4, G, False) + c(88, 70, 3, G, False) + c(86, 92, 3, G, False) + '<g transform="translate(36 38) rotate(40)">' + p('M0 -22 C10 -10 10 8 6 16 H-6 C-10 8 -10 -10 0 -22Z', C) + poly('-6,10 -14,22 -6,16', G) + poly('6,10 14,22 6,16', G) + c(0, -6, 4, V) + p('M-4 16 L0 28 L4 16Z', O, '') + '</g>'
I['embarazo'] = r(42, 44, 36, 54, C, 9) + r(44, 38, 32, 10, G, 3) + p('M52 38 C52 22 68 22 68 38Z', O) + ln('M42 62 H52') + ln('M42 74 H52') + ln('M42 86 H52') + r(44, 70, 32, 26, '#F8D58E', 8, False)
I['empire-state'] = r(34, 72, 52, 26, G, 1) + r(43, 52, 34, 20, G, 1) + r(52, 36, 16, 16, G, 1) + ln('M60 36 V10', G, 3) + ''.join(r(x, y, 4, 6, O, 0, False) for x in [40, 52, 64, 76] for y in [80, 90]) + r(48, 58, 4, 6, O, 0, False) + r(68, 58, 4, 6, O, 0, False)
I['elefanta'] = c(30, 52, 22, S) + c(90, 52, 22, S) + c(60, 54, 27, S) + ln('M60 62 V86 C60 100 46 100 46 88', G, 8) + c(50, 48, 3.5, G, False) + c(70, 48, 3.5, G, False)
I['crianza-rioja'] = barril(2)
I['torre-eiffel'] = ln('M60 10 L46 54 L32 98', G, 4) + ln('M60 10 L74 54 L88 98', G, 4) + ln('M48 50 H72', G, 4) + ln('M40 74 H80', G, 4) + ln('M42 98 Q60 68 78 98', G, 4) + ln('M60 10 V4', G, 3)
I['reserva-elcano'] = barril(3)
xs = list(range(44, 80, 8))
def curva(x): t = (x - 32) / 56; return (1 - t) ** 2 * 30 + 2 * t * (1 - t) * 76 + t * t * 30
I['grado-golden-gate'] = r(28, 26, 8, 62, O, 1) + r(84, 26, 8, 62, O, 1) + r(6, 76, 108, 6, G, 1) + ln('M32 30 Q60 76 88 30', G, 3) + ln('M6 74 L32 30') + ln('M114 74 L88 30') + ''.join(ln(f'M{x} {curva(x):.0f} V76', G, 2) for x in xs)
I['gran-reserva-cristo'] = barril(5)
I['burj-khalifa'] = p('M60 4 L63 28 L68 28 L70 50 L76 50 L78 72 L86 72 L88 100 H32 L34 72 L42 72 L44 50 L50 50 L52 28 L57 28Z', G) + ln('M60 30 V96', C, 2) + ln('M46 52 H74', C, 2) + ln('M38 74 H82', C, 2)
I['canal-panama'] = poly('26,70 94,70 84,86 36,86', G) + r(46, 50, 28, 20, C, 2) + r(32, 58, 12, 12, O, 1) + r(76, 58, 12, 12, O, 1) + ln('M58 50 V38') + ln('M8 98 Q18 90 28 98 T48 98 T68 98 T88 98 T108 98', V, 4)
I['opera-sidney'] = p('M18 92 C18 52 34 32 50 28 C44 50 42 72 42 92Z', C) + p('M42 92 C44 58 58 34 82 24 C76 50 74 72 76 92Z', C) + p('M76 92 C78 64 90 48 104 44 C100 62 98 76 100 92Z', C) + r(12, 92, 100, 8, G, 1)
I['piramide-taj-mahal'] = p('M60 20 L102 94 H18Z', O) + ln('M32 72 H88', G, 2) + ln('M42 54 H78', G, 2) + ln('M24 84 H96', G, 2) + c(96, 24, 9, '#F8D58E', False)
I['universidad-rioja'] = poly('60,26 108,48 60,70 12,48', G) + p('M34 60 V80 C34 92 86 92 86 80 V60 L60 70Z', V) + ln('M100 52 V80', O, 3) + c(100, 84, 4, O, False)
I['vida-larga'] = r(28, 12, 64, 8, G, 2) + r(28, 100, 64, 8, G, 2) + p('M34 20 H86 L66 60 L86 100 H34 L54 60Z', C) + poly('44,30 76,30 62,52 58,52', O, False) + poly('42,100 60,76 78,100', O, False) + ln('M60 60 V76', O, 2)
def torre(cx, top):
    return poly(f'{cx-8},100 {cx-6},{top+26} {cx},{top} {cx+6},{top+26} {cx+8},100', G) + c(cx, top - 4, 3.5, O, False) + r(cx - 1.5, top + 36, 3, 9, C, 0, False) + r(cx - 1.5, top + 54, 3, 9, C, 0, False)
I['sagrada-familia'] = torre(28, 30) + torre(48, 12) + torre(72, 12) + torre(92, 30)
I['notre-dame'] = r(22, 28, 28, 72, G, 1) + r(70, 28, 28, 72, G, 1) + r(50, 52, 20, 48, G, 1) + c(60, 70, 9, C) + p('M54 100 V88 C54 80 66 80 66 88 V100Z', C) + ''.join(r(x, 22, 6, 6, G, 0, False) for x in [22, 32, 44, 70, 80, 92]) + r(31, 40, 10, 16, C, 5) + r(79, 40, 10, 16, C, 5)
I['colon'] = p('M20 78 H100 C94 94 80 100 60 100 C40 100 26 94 20 78Z', G) + ln('M60 78 V16', G, 3) + p('M60 22 C86 28 90 48 86 64 H60Z', C) + p('M60 26 C40 32 34 50 36 64 H60Z', C) + ln('M74 40 V54', O, 3) + ln('M67 47 H81', O, 3) + poly('60,14 76,10 60,6', O, False) + ln('M6 108 Q16 102 26 108 T46 108 T66 108 T86 108 T106 108', V, 4)
ids = ["parpadeo","latido","luz-sol","cancion-pop","huevo-duro","tortilla","partido-futbol","iss","pelicula-maraton","vuelo-nueva-york","dia-entero","apolo-11","fermentacion","juegos-olimpicos","tour-francia","mundial-futbol","camino-santiago","ciclo-vid","viaje-marte","embarazo","empire-state","elefanta","crianza-rioja","torre-eiffel","reserva-elcano","grado-golden-gate","gran-reserva-cristo","burj-khalifa","canal-panama","opera-sidney","piramide-taj-mahal","universidad-rioja","vida-larga","sagrada-familia","notre-dame","colon"]
assert set(ids) == set(I), set(ids) ^ set(I)
# el cráter de la luna lleva relleno oscuro suave
I['apolo-11'] = I['apolo-11'].replace('fill="none" stroke="#54081F" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/><circle cx="78"', 'fill="#D9C6A3" stroke="#54081F" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/><circle cx="78"')
out = {k: f'<svg viewBox="0 0 120 120" aria-hidden="true" focusable="false"><defs><clipPath id="cp-ico"><circle cx="60" cy="60" r="58"/></clipPath></defs><circle cx="60" cy="60" r="58" fill="{S}"/><g clip-path="url(#cp-ico)">{v}</g></svg>' for k, v in I.items()}
root = os.path.join(os.path.dirname(__file__), '..')
open(os.path.join(root, 'js', 'comparativas_iconos.js'), 'w', encoding='utf-8').write('/* Pictogramas propios, generados con tools/gen_iconos.py (CC BY 4.0) */\nwindow.COMPARATIVAS_ICONOS = ' + json.dumps(out, ensure_ascii=False) + ';\n')
print(len(out))
