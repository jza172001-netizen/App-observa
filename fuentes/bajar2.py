"""Fuentes nuevas: pagos SECOP II, oferentes por proceso, SECOP I y II 2020-2023 por mes -> extra.json"""
import json,urllib.request,urllib.parse,re
U="https://www.datos.gov.co/resource/"
def q(ds,p):return json.load(urllib.request.urlopen(urllib.request.Request(U+ds+".json?"+urllib.parse.urlencode(p),headers={"User-Agent":"ObservaRigor/1.0"}),timeout=300))
def todo(ds,p):
    o,off=[],0
    while True:
        r=q(ds,{**p,"$limit":50000,"$offset":off});o+=r;off+=len(r)
        if len(r)<50000:return o
CI=json.load(open('ciudades.json'));cs=[v for v in CI.values() if v];inn=",".join("'%s'"%c for c in cs)
nm=lambda u:(re.search(r'CO1\.NTC\.\d+',u.get('url','') if isinstance(u,dict) else (u or '')) or [None])[0]
X={}
P=todo('jbjy-vk9h',{"$select":"id_contrato,valor_pagado,valor_facturado,justificacion_modalidad_de,es_grupo","$where":f"departamento='Antioquia' AND fecha_de_firma>='2024-01-01' AND ciudad in({inn})","$order":"id_contrato"})
X['pagos']={r['id_contrato']:[float(r.get('valor_pagado') or 0),float(r.get('valor_facturado') or 0),(r.get('justificacion_modalidad_de') or '')[:60],r.get('es_grupo')] for r in P}
R=todo('p6dx-8zbt',{"$select":"urlproceso,proveedores_unicos_con,respuestas_al_procedimiento,modalidad_de_contratacion","$where":f"departamento_entidad='Antioquia' AND fecha_de_publicacion_del>='2023-06-01' AND ciudad_entidad in({inn})"})
X['ofertas']={}
for r in R:
    k=nm(r.get('urlproceso'))
    if k:X['ofertas'][k]=max(X['ofertas'].get(k,0),int(float(r.get('proveedores_unicos_con') or 0)),int(float(r.get('respuestas_al_procedimiento') or 0)))
X['s2']=q('jbjy-vk9h',{"$select":"ciudad,date_trunc_ym(fecha_de_firma) as m,count(*) as n,sum(valor_del_contrato) as v","$where":f"departamento='Antioquia' AND fecha_de_firma between '2020-01-01' and '2023-12-31T23:59:59' AND ciudad in({inn})","$group":"ciudad,m","$limit":50000})
mi=",".join("'%s'"%k for k in CI)
X['s1']=q('f789-7hwg',{"$select":"municipio_entidad,date_trunc_ym(fecha_de_firma_del_contrato) as m,count(*) as n,sum(cuantia_contrato) as v","$where":f"departamento_entidad='Antioquia' AND fecha_de_firma_del_contrato between '2020-01-01' and '2023-12-31T23:59:59' AND municipio_entidad in({mi})","$group":"municipio_entidad,m","$limit":50000})
X['s1mod']=q('f789-7hwg',{"$select":"municipio_entidad,modalidad_de_contratacion,count(*) as n,sum(cuantia_contrato) as v","$where":f"departamento_entidad='Antioquia' AND anno_firma_contrato in('2020','2021','2022','2023') AND municipio_entidad in({mi})","$group":"municipio_entidad,modalidad_de_contratacion","$limit":50000})
json.dump(X,open('extra.json','w'),ensure_ascii=False)
print(len(X['pagos']),'pagos',len(X['ofertas']),'procesos',len(X['s2']),'s2',len(X['s1']),'s1',len(X['s1mod']),'s1mod')
