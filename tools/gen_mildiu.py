#!/usr/bin/env python3
"""Genera data/mildiu.js y optimiza las imágenes a partir de 04_trabajo/paquete_mildiu.
Uso: python3 tools/gen_mildiu.py RUTA_PAQUETE_MILDIU   (por defecto ../paquete_mildiu)
Si el CSV trae predicciones del modelo (columnas prediccion_modelo/confianza con valores reales),
se incluyen; si ponen «a verificar» o están vacías, el juego NO muestra predicción (nunca se inventa)."""
import csv, json, os, sys
from PIL import Image
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
pkg = sys.argv[1] if len(sys.argv) > 1 else os.path.join(root, '..', 'paquete_mildiu')
out = os.path.join(root, 'img', 'mildiu'); os.makedirs(out, exist_ok=True)
CAT = {'mildiu_avanzado': 'avanzado', 'mildiu_leve': 'leve', 'sano': 'sano', 'parecido_no_mildiu': 'parecido'}
LES = json.load(open(os.path.join(root,'tools','lesiones.json'))) if os.path.exists(os.path.join(root,'tools','lesiones.json')) else {}
items = []
for r in csv.DictReader(open(os.path.join(pkg, 'paquete_mildiu.csv'), encoding='utf-8-sig')):
    fid = r['archivo'].rsplit('.', 1)[0]
    im = Image.open(os.path.join(pkg, 'imagenes', r['archivo'])).convert('RGB')
    im.save(os.path.join(out, fid + '.jpg'), quality=82, optimize=True, progressive=True)
    im.save(os.path.join(out, fid + '.webp'), quality=78, method=6)
    pred = r.get('prediccion_modelo', '').strip(); conf = r.get('confianza', '').strip()
    real = pred and 'verificar' not in pred.lower() and conf
    items.append(dict(id=fid, w=im.size[0], h=im.size[1], et='mildiu' if r['etiqueta_real'] == 'mildiu' else 'sin',
                      cat=CAT[r['categoria']], les=[[c for pt in poly for c in pt] for poly in LES.get(fid, [])], pred=pred if real else None, conf=float(conf) if real else None))
open(os.path.join(root, 'data', 'mildiu.js'), 'w', encoding='utf-8').write(
    '// Generado por tools/gen_mildiu.py. No editar a mano.\nwindow.MILDIU = ' + json.dumps(dict(items=items), ensure_ascii=False, separators=(',', ':')) + ';\n')
from collections import Counter
print(len(items), Counter(i['cat'] for i in items), 'con predicción:', sum(1 for i in items if i['pred']))
