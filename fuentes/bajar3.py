"""Serie anual 2020-2023 por municipio y modalidad (SECOP I + II) -> anual.json"""
import json,urllib.request,urllib.parse
U="https://www.datos.gov.co/resource/";q=lambda ds,p:json.load(urllib.request.urlopen(urllib.request.Request(U+ds+".json?"+urllib.parse.urlencode(p),headers={"User-Agent":"ObservaRigor/1.0"}),timeout=300))
CI=json.load(open('ciudades.json'));inn=",".join("'%s'"%v for v in CI.values() if v);mi=",".join("'%s'"%k for k in CI)
A={'s2':q('jbjy-vk9h',{"$select":"ciudad,date_extract_y(fecha_de_firma) as y,modalidad_de_contratacion as m,count(*) as n,sum(valor_del_contrato) as v","$where":f"departamento='Antioquia' AND fecha_de_firma between '2020-01-01' and '2023-12-31T23:59:59' AND ciudad in({inn})","$group":"ciudad,y,m","$limit":50000}),
 's1':q('f789-7hwg',{"$select":"municipio_entidad,anno_firma_contrato as y,modalidad_de_contratacion as m,count(*) as n,sum(cuantia_contrato) as v","$where":f"departamento_entidad='Antioquia' AND anno_firma_contrato in('2020','2021','2022','2023') AND municipio_entidad in({mi})","$group":"municipio_entidad,y,m","$limit":50000})}
json.dump(A,open('anual.json','w'),ensure_ascii=False);print(len(A['s2']),len(A['s1']))
