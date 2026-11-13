#!/usr/bin/env python3
"""Genera data/racimos.js y optimiza las imágenes a partir de 04_trabajo/paquete_racimos.
Uso: python3 tools/gen_racimos.py RUTA_PAQUETE_RACIMOS   (por defecto ../paquete_racimos)
No inventa datos: solo reorganiza las cajas y recuentos del paquete."""
import json, os, sys
from PIL import Image
pkg = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', '..', 'paquete_racimos')
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
out_img = os.path.join(root, 'img', 'racimos'); os.makedirs(out_img, exist_ok=True)

def solape(a, b):
    """Intersección / área de la caja menor (las cajas con hojas suelen ser más pequeñas que sin hojas)."""
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0])); iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    m = min((a[2]-a[0])*(a[3]-a[1]), (b[2]-b[0])*(b[3]-b[1]))
    return ix*iy/m if m else 0

def match(con, des):
    """Asignación óptima (húngara) de cada caja con hojas a una caja distinta de la imagen deshojada."""
    from scipy.optimize import linear_sum_assignment
    import numpy as np
    cost = np.zeros((len(con), len(des)))
    for i, c in enumerate(con):
        for j, d in enumerate(des):
            dist = (((c[0]+c[2])-(d[0]+d[2]))**2 + ((c[1]+c[3])-(d[1]+d[3]))**2) ** .5 / 1000
            cost[i, j] = -solape(c, d) + 0.05*dist
    r, c = linear_sum_assignment(cost)
    return {int(j): int(i) for i, j in zip(r, c)}

cepas, avisos = [], []
ids = [r['id'] for r in json.load(open(os.path.join(pkg, 'indice.json'), encoding='utf-8'))] if isinstance(json.load(open(os.path.join(pkg, 'indice.json'), encoding='utf-8')), list) else None
for fn in sorted(os.listdir(os.path.join(pkg, 'json'))):
    if ids is not None and fn[:-5] not in ids: continue
    d = json.load(open(os.path.join(pkg, 'json', fn), encoding='utf-8'))
    cid = d['id']; W, H = d['dimensiones_px']['con_hojas']
    box = lambda b: [b['x_min'], b['y_min'], b['x_max'], b['y_max']]
    con = [box(b) for b in d['cajas']['con_hojas']]; des = [box(b) for b in d['cajas']['deshojada']]
    m = match(con, des)
    nuevas = [j for j in range(len(des)) if j not in m]
    r = d['racimos']
    if len(nuevas) != r['aparecen_al_deshojar']:
        avisos.append(f"{cid}: emparejadas->nuevas {len(nuevas)} != aparecen_al_deshojar {r['aparecen_al_deshojar']}")
    cepas.append(dict(id=cid, w=W, h=H, con=con,
        des=[dict(b=des[j], oculto=(j in nuevas)) for j in range(len(des))],
        visibles=r['visibles_con_hojas'], deshojada=r['visibles_deshojada'], ocultos=r['aparecen_al_deshojar']))
    for nivel in ('con_hojas', 'deshojada'):
        src = os.path.join(pkg, 'imagenes', f'{cid}_{nivel}.jpg')
        im = Image.open(src).convert('RGB')
        im.save(os.path.join(out_img, f'{cid}_{nivel}.jpg'), quality=82, optimize=True, progressive=True)
        im.save(os.path.join(out_img, f'{cid}_{nivel}.webp'), quality=78, method=6)
tot_vis = sum(c['deshojada'] for c in cepas); tot_oc = sum(c['ocultos'] for c in cepas)
medio = sum(c['ocultos']/c['deshojada'] for c in cepas)/len(cepas)
meta = dict(n=len(cepas), porcentaje_agregado=round(100*tot_oc/tot_vis, 1), porcentaje_medio_por_cepa=round(100*medio, 1),
            total_deshojada=tot_vis, total_ocultos=tot_oc)
open(os.path.join(root, 'data', 'racimos.js'), 'w', encoding='utf-8').write(
    '// Generado por tools/gen_racimos.py. No editar a mano.\nwindow.RACIMOS = ' +
    json.dumps(dict(meta=meta, cepas=cepas), ensure_ascii=False, separators=(',', ':')) + ';\n')
print(meta); print('\n'.join(avisos) or 'emparejamiento coherente en las 20 cepas')
