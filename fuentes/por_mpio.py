"""Archivo de contratos con banderas de riesgo por municipio -> c/<cod>.json; suma cruces a contra.json"""
import json, re, collections, datetime as dt, os
C = json.load(open('contratos.json')); CI = json.load(open('ciudades.json')); X = json.load(open('cruces.json')); D = json.load(open('contra.json'))
dig = lambda s: re.sub(r'\D', '', s or ''); fe = lambda s: dt.date.fromisoformat(s[:10]) if s else None
directa = lambda r: 'directa' in (r.get('modalidad_de_contratacion') or '').lower()
G0, G1 = dt.date(2026, 1, 31), dt.date(2026, 6, 21)
c2m = {v: k for k, v in CI.items() if v}
cl = collections.Counter((r.get('nombre_entidad'), r.get('documento_proveedor'), (r.get('fecha_de_firma') or '')[:7]) for r in C if directa(r))
vd = sorted(float(r.get('valor_del_contrato') or 0) for r in C if directa(r)); alto = vd[int(len(vd) * .99)]
MO = {'Contratación directa': 'Directa', 'Contratación Directa (con ofertas)': 'Directa con ofertas', 'Contratación régimen especial': 'Régimen especial', 'Contratación régimen especial (con ofertas)': 'Régimen especial con ofertas', 'Mínima cuantía': 'Mínima cuantía', 'Licitación pública': 'Licitación pública'}
os.makedirs('../geo/site2/contratacion/c', exist_ok=True)
por = collections.defaultdict(list)
for r in C: por[c2m.get(r.get('ciudad'))].append(r)
for m, rs in por.items():
    if not m: continue
    ents = sorted({(r.get('nombre_entidad') or '').strip().title() for r in rs}); ei = {e: i for i, e in enumerate(ents)}
    out, nm, ns = [], 0, 0
    for r in rs:
        v = float(r.get('valor_del_contrato') or 0); d = dig(r.get('documento_proveedor')); nat = (r.get('tipodocproveedor') or '').upper() != 'NIT'
        f, i, fin, ad = fe(r.get('fecha_de_firma')), fe(r.get('fecha_de_inicio_del_contrato')), fe(r.get('fecha_de_fin_del_contrato')), float(r.get('dias_adicionados') or 0)
        fl = ''
        if directa(r): fl += 'D'
        if directa(r) and f and G0 <= f <= G1: fl += 'G'
        if ad > 0 and i and fin and (fin - i).days - ad > 0 and ad / ((fin - i).days - ad) >= .5: fl += 'P'
        if directa(r) and cl[(r.get('nombre_entidad'), r.get('documento_proveedor'), (r.get('fecha_de_firma') or '')[:7])] >= 3: fl += 'R'
        if d in X['multas']: fl += 'M'; nm += 1
        if d in X['siri']: fl += 'S'; ns += 1
        if directa(r) and v >= alto: fl += 'A'
        u = r.get('urlproceso'); u = u.get('url') if isinstance(u, dict) else u
        out.append({'e': ei[(r.get('nombre_entidad') or '').strip().title()], 'p': ('Persona natural ···' + d[-4:]) if nat else (r.get('proveedor_adjudicado') or '').strip()[:70],
                    'mo': MO.get(r.get('modalidad_de_contratacion'), r.get('modalidad_de_contratacion')), 't': r.get('tipo_de_contrato'), 'v': round(v), 'f': (r.get('fecha_de_firma') or '')[:10],
                    'ad': int(ad), 'o': (r.get('objeto_del_contrato') or '')[:150], 'u': u, 'fl': fl})
    out.sort(key=lambda x: -x['v'])
    cod = D['municipios'][m]['cod']
    json.dump({'ent': ents, 'c': out}, open(f'../geo/site2/contratacion/c/{cod}.json', 'w'), ensure_ascii=False, separators=(',', ':'))
    D['municipios'][m]['cruces'] = {'multas': nm, 'siri': ns}
D['alto'] = round(alto); D['fuentes_cruce'] = {'multas': X['n_multas'], 'siri': X['n_siri']}
json.dump(D, open('contra.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('umbral alto valor directa:', round(alto), '| archivos:', len(os.listdir('../geo/site2/contratacion/c')))
print(sorted(((os.path.getsize('../geo/site2/contratacion/c/' + f) // 1024, f) for f in os.listdir('../geo/site2/contratacion/c')))[-3:])
