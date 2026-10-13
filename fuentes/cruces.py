"""Cruza contratistas del Oriente con Multas SECOP I (4n4q-k399) y antecedentes SIRI de la Procuraduría (iaeu-rcn6) -> cruces.json"""
import urllib.request, urllib.parse, json, re
def q(ds, p): return json.load(urllib.request.urlopen(urllib.request.Request(f"https://www.datos.gov.co/resource/{ds}.json?" + urllib.parse.urlencode(p), headers={"User-Agent": "ObservaRigor/1.0"}), timeout=300))
def todo(ds, sel):
    out, off = [], 0
    while True:
        r = q(ds, {"$select": sel, "$limit": 50000, "$offset": off}); out += r; off += len(r)
        if len(r) < 50000: return out
dig = lambda s: re.sub(r'\D', '', s or '')
C = json.load(open('contratos.json')); docs = {dig(r.get('documento_proveedor')) for r in C} - {''}
M = todo('4n4q-k399', 'documento_contratista,nombre_entidad,municipio,valor_sancion,fecha_de_firmeza,ruta_de_proceso')
S = todo('iaeu-rcn6', 'numero_identificacion,sanciones,tipo_inhabilidad,duracion_anos,duracion_mes,fecha_efectos_juridicos,autoridad')
mul, siri = {}, {}
for m in M:
    d = dig(m.get('documento_contratista'))
    if d in docs: mul.setdefault(d, []).append({'e': (m.get('nombre_entidad') or '')[:60], 'v': m.get('valor_sancion'), 'f': (m.get('fecha_de_firmeza') or '')[:10], 'u': (m.get('ruta_de_proceso') or {}).get('url') if isinstance(m.get('ruta_de_proceso'), dict) else m.get('ruta_de_proceso')})
for s in S:
    d = dig(s.get('numero_identificacion'))
    if d in docs: siri.setdefault(d, []).append({'s': (s.get('sanciones') or '')[:60], 't': s.get('tipo_inhabilidad'), 'a': s.get('duracion_anos'), 'f': s.get('fecha_efectos_juridicos'), 'q': (s.get('autoridad') or '')[:50]})
json.dump({'multas': mul, 'siri': siri, 'n_multas': len(M), 'n_siri': len(S)}, open('cruces.json', 'w'), ensure_ascii=False)
print(len(docs), 'contratistas;', len(M), 'multas;', len(S), 'registros SIRI;', len(mul), 'con multas;', len(siri), 'con SIRI')
