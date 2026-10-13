"""Contratos SECOP II firmados desde 2024 en los 23 municipios del Oriente antioqueño -> contratos.json"""
import urllib.request, urllib.parse, json
C = json.load(open('ciudades.json'))
cities = [v for v in C.values() if v]
W = "departamento='Antioquia' AND fecha_de_firma>='2024-01-01' AND ciudad in(" + ",".join("'%s'" % c for c in cities) + ")"
S = "nombre_entidad,nit_entidad,ciudad,orden,modalidad_de_contratacion,tipo_de_contrato,valor_del_contrato,fecha_de_firma,fecha_de_inicio_del_contrato,fecha_de_fin_del_contrato,dias_adicionados,tipodocproveedor,documento_proveedor,proveedor_adjudicado,estado_contrato,urlproceso,id_contrato,objeto_del_contrato"
out, off = [], 0
while True:
    u = "https://www.datos.gov.co/resource/jbjy-vk9h.json?" + urllib.parse.urlencode({"$select": S, "$where": W, "$limit": 50000, "$offset": off, "$order": "id_contrato"})
    r = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "ObservaRigor/1.0"}), timeout=300))
    out += r; off += len(r); print(off)
    if len(r) < 50000: break
json.dump(out, open('contratos.json', 'w'), ensure_ascii=False)
print(len(out), 'contratos')
