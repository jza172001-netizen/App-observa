"""Construye todas las páginas de Observa Rigor desde sus fuentes.
Uso:  python construir.py [carpeta_fuentes] [carpeta_sitio]
Por defecto: fuentes/ y sitio/ (estructura del repositorio)."""
import json,os,re,sys
SRC=sys.argv[1] if len(sys.argv)>1 else 'fuentes'; OUT=sys.argv[2] if len(sys.argv)>2 else 'sitio'
rd=lambda p:open(os.path.join(SRC,p),encoding='utf8').read()
def wr(p,s):
    p=os.path.join(OUT,p);os.makedirs(os.path.dirname(p),exist_ok=True);open(p,'w',encoding='utf8').write(s);print('  ✓',p)
NAV=rd('fx/nav.js');FX=rd('fx/fx.js')
def con_nav(s):
    i=s.find('// Menú lateral común')
    if i>=0:j=s.find('</script>',i);return s[:i]+NAV+s[j:]
    k=s.rfind('</body>');return s[:k]+'<script>'+NAV+'</script>'+s[k:]
print('Medellín')
s=rd('live_med.html')
esc="{n:'La Escombrera',ll:[-75.6386,6.2588],k:'13',own:'ladera',r:1,s:['jep7','op34','ai48'],h:()=>'Vista desde la Comuna 13. Por casi dos décadas fue depósito de escombros y, según la JEP, una fosa común: desde diciembre de 2024 se hallaron 7 cuerpos, todos identificados y entregados a sus familias. Ubicación aproximada.'},\n "
s=s.replace("{n:'Estación Villa',",esc+"{n:'Estación Villa',",1)
s=s.replace('<body>','<body data-orn-nobottom>',1).replace('<div class="top">','<div class="top" data-orn-slot>',1)
MOB='<style>@media (max-width:820px){.giro{transform:scale(.62);transform-origin:left bottom;left:8px!important}.panel:not(.min)~.giro{display:none!important}.panel:not(.min)~.tira{display:none!important}.fab button,.fab a{width:38px!important;height:38px!important}.top .orn-in{background:rgba(13,9,25,.75);backdrop-filter:blur(8px)}}</style>'
js=[rd('analisis.js').replace('__TEND__',rd('tend.json')),rd('conclu.js'),FX+'\n'+rd('fx/pilotos.js'),rd('memoria.js')]
k=s.rfind('</body>');s=s[:k]+''.join('<script>\n'+j+'\n</script>\n' for j in js)+MOB+'<script>'+NAV+'</script>'+s[k:]
wr('medellin/index.html',s)
print('Contratación')
c=rd('contra_app.html').replace('__DATOS__',rd('contra_out.json')).replace('__GEO__',rd('oriente_geo.json'))
wr('contratacion/index.html',con_nav(c))
print('Rigor Datos y Hallazgos graves')
wr('datos/index.html',con_nav(rd('fx/datos.html').replace('__FX__',FX)))
wr('cumplimiento/index.html',con_nav(rd('fx/cumplimiento.html')))
print('Clústeres')
import importlib.util as _u;_sp=_u.spec_from_file_location('clusters',os.path.join(SRC,'clusters.py'));_m=_u.module_from_spec(_sp);_sp.loader.exec_module(_m);_m.build(OUT)
for _r,_d,_f in os.walk(os.path.join(OUT,'clusters')):
    for _x in _f:
        if _x=='index.html':_p=os.path.join(_r,_x);wr(os.path.relpath(_p,OUT),con_nav(open(_p,encoding='utf8').read()))
print('Landing, nosotros y noticias (se editan directo en el sitio; aquí solo se actualiza el menú)')
for p in ['index.html','nosotros/index.html','noticias/index.html']:
    f=os.path.join(OUT,p);wr(p,con_nav(open(f,encoding='utf8').read()))
print('Metadatos para buscadores y redes')
META={'index.html':('Observa Rigor · Observatorio de la ineficacia normativa','Medimos si la ley se cumple en Colombia, con fuentes públicas cruzadas: contratación, seguridad, drogas, desaparición forzada y economías ilícitas.'),
 'medellin/index.html':('Medellín comuna por comuna · Observa Rigor','Mapa 3D de Medellín que cruza seguridad, pobreza, plata pública y memoria, con fuentes verificables y conclusiones por comuna.'),
 'contratacion/index.html':('Rigor Contratación · Oriente antioqueño','Diez alertas de riesgo en la contratación pública de los 23 municipios del Oriente antioqueño, con datos del SECOP.'),
 'datos/index.html':('Rigor Datos · Observa Rigor','Economías ilícitas, empleo, desigualdad, corrupción y seguridad en Colombia: datos oficiales cruzados con academia y prensa.'),
 'cumplimiento/index.html':('Hallazgos graves · Observa Rigor','Hallazgos con deber legal, entidad obligada y evidencia cruzada, y las respuestas de las entidades.'),
 'noticias/index.html':('Noticias y videos · Observa Rigor','Derechos humanos, conflicto, drogas y corrupción en Medellín, el Oriente y Colombia, actualizado cada hora.'),
 'nosotros/index.html':('Quiénes somos · Observa Rigor','Servicios, método, planes y equipo de Observa Rigor.')}
for p,(t,d) in META.items():
    f=os.path.join(OUT,p);x=open(f,encoding='utf8').read();x=re.sub(r'<!--meta-or-->.*?<!--/meta-or-->','',x,flags=re.S)
    m='<!--meta-or--><meta name="description" content="'+d+'"><meta property="og:title" content="'+t+'"><meta property="og:description" content="'+d+'"><meta property="og:type" content="website"><meta property="og:locale" content="es_CO"><meta name="theme-color" content="#0A0716"><!--/meta-or-->'
    x=re.sub(r'<html(?![^>]*lang)','<html lang="es"',x,count=1);x=x.replace('</head>',m+'</head>',1);open(f,'w',encoding='utf8').write(x)
print('Listo.')
