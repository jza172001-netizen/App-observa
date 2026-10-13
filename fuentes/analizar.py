"""Alertas de riesgo en contratación (SECOP II, Oriente antioqueño, desde 2024) -> contra.json"""
import json, unicodedata, collections, datetime as dt
C = json.load(open('contratos.json')); CI = json.load(open('ciudades.json')); G = json.load(open('ant_mpios.json'))
n2 = lambda s: unicodedata.normalize('NFD', s or '').encode('ascii', 'ignore').decode().upper().strip()
ciudad_a_mpio = {v: k for k, v in CI.items() if v}
fecha = lambda s: dt.date.fromisoformat(s[:10]) if s else None
val = lambda r: float(r.get('valor_del_contrato') or 0)
directa = lambda r: (r.get('modalidad_de_contratacion') or '').lower().startswith('contrataci') and 'directa' in (r.get('modalidad_de_contratacion') or '').lower()
G0, G1 = dt.date(2026, 1, 31), dt.date(2026, 6, 21)  # Ley de Garantías 2026 (4 meses antes de la 1.ª vuelta hasta la 2.ª vuelta)
def natural(r): return (r.get('tipodocproveedor') or '').upper()!='NIT'
def nombre_prov(r):
    d = r.get('documento_proveedor') or ''
    return ('Persona natural ···' + d[-4:]) if natural(r) else (r.get('proveedor_adjudicado') or 'Sin nombre').strip()[:60]
def medir(rs):
    v = sum(map(val, rs)) or 1; n = len(rs)
    vd = sum(val(r) for r in rs if directa(r)); nd = sum(1 for r in rs if directa(r))
    prov = collections.Counter()
    for r in rs: prov[(r.get('documento_proveedor'), nombre_prov(r))] += val(r)
    top = prov.most_common(5); top3 = sum(x[1] for x in top[:3]) / v
    pr = 0
    for r in rs:
        a, i, f = float(r.get('dias_adicionados') or 0), fecha(r.get('fecha_de_inicio_del_contrato')), fecha(r.get('fecha_de_fin_del_contrato'))
        if a > 0 and i and f and (f - i).days - a > 0 and a / ((f - i).days - a) >= .5: pr += 1
    cl = collections.Counter((r.get('nombre_entidad'), r.get('documento_proveedor'), (r.get('fecha_de_firma') or '')[:7]) for r in rs if directa(r))
    fr = sum(1 for k, c in cl.items() if c >= 3)
    ga = [r for r in rs if directa(r) and fecha(r.get('fecha_de_firma')) and G0 <= fecha(r.get('fecha_de_firma')) <= G1]
    return {'n': n, 'valor': round(v), 'pd_v': round(vd / v * 100, 1), 'pd_n': round(nd / max(n, 1) * 100, 1), 'top3': round(top3 * 100, 1),
            'top': [{'p': k[1], 'v': round(x)} for k, x in top], 'prorrogas': pr, 'pr_pct': round(pr / max(n, 1) * 100, 1),
            'fracc': fr, 'gar_n': len(ga), 'gar_v': round(sum(map(val, ga)))}
def alertas(m, n, mun=False):
    a = []
    if m['pd_v'] >= 60: a.append('directa')
    if n >= 30 and m['top3'] >= 40: a.append('concentracion')
    if m['pr_pct'] >= 8: a.append('prorrogas')
    if m['fracc'] >= (10 if mun else 5): a.append('repetidos')
    if m['gar_n'] >= 5: a.append('garantias')
    return a
porM = collections.defaultdict(list)
for r in C: porM[ciudad_a_mpio.get(r.get('ciudad'))].append(r)
out = {'municipios': {}, 'periodo': 'Contratos firmados entre el 1 de enero de 2024 y la fecha de consulta', 'consulta': dt.date.today().isoformat(), 'total': len(C)}
for f in G['features']:
    if 'ORIENTE' not in n2(f['properties']['SUBREGION']): continue
    nom = f['properties']['MPIO_NOMBR']
    k = next((o for o in CI if n2(o) == n2(nom)), None)
    rs = porM.get(k, [])
    m = medir(rs) if rs else None
    ent = collections.defaultdict(list)
    for r in rs: ent[(r.get('nombre_entidad') or '').strip()].append(r)
    E = []
    for en, er in sorted(ent.items(), key=lambda x: -sum(map(val, x[1]))):
        me = medir(er); me['nombre'] = en.title(); me['alertas'] = alertas(me, len(er)); me['nit'] = er[0].get('nit_entidad'); E.append(me)
    out['municipios'][k or nom.title()] = {'cod': f['properties']['COD_MPIO'], 'datos': m, 'alertas': (alertas(m, len(rs), True) if m else [])+(['publicacion'] if len(rs) < 100 else []),
                                            'pocos': len(rs) < 100, 'ciudad_secop': CI.get(k), 'entidades': E[:12]}
    f['properties'] = {'n': k or nom.title(), 'cod': f['properties']['COD_MPIO']}
G['features'] = [f for f in G['features'] if 'n' in f['properties']]
json.dump(out, open('contra.json', 'w'), ensure_ascii=False, separators=(',', ':'))
json.dump(G, open('oriente_geo.json', 'w'), ensure_ascii=False, separators=(',', ':'))
for k, v in sorted(out['municipios'].items(), key=lambda x: -(x[1]['datos'] or {}).get('pd_v', 0))[:23]:
    d = v['datos'] or {}
    print(k, d.get('n'), d.get('pd_v'), d.get('top3'), d.get('pr_pct'), d.get('fracc'), d.get('gar_n'), v['alertas'], 'POCOS' if v['pocos'] else '')
