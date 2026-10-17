"""Clústeres de Observa Rigor: cada uno organiza por PREGUNTA lo que ya está en las apps.
Genera sitio/clusters/index.html y sitio/clusters/<slug>/index.html. Lo llama construir.py."""
import os,html
E=html.escape
# tipo: adm judicial aca pre aud tes org (organización de la sociedad civil)
TIPO={'adm':'Oficial','jud':'Judicial y de control','aca':'Académica','pre':'Prensa','org':'Sociedad civil','tes':'Testimonio'}
C=[
{'s':'drogas','t':'Drogas: la cadena y la salud pública','i':'💊','q':'¿Por qué la persecución cae sobre el eslabón más pequeño y el mercado sigue igual?',
 'con':[('Brecha','La captura cae abajo','En 20 años, el 0,1 % de los capturados por drogas en Medellín era universitario. El Código Penal (art. 376) promete desarticular el tráfico; la captura recae en el último eslabón.'),
  ('Brecha','El mercado sigue en los mismos sitios','Muchas capturas y operativos repetidos en los mismos puntos (Centro, Barrio Antioquia, Provenza). Es lo que predice el efecto reemplazo, que sigue siendo hipótesis.'),
  ('Vacío','El consumo se mide con un dato de 2019','La última Encuesta Nacional de Consumo es de 2019. La Ley 1566 de 2012 ordena atender el consumo como salud pública, pero sin medición actual no se sabe si funciona.'),
  ('Hallazgo','Lo que se vende no es lo que dice ser','En 2021, Échele Cabeza analizó 2.868 sustancias: el 16 % de los tusibi contenía opioides (riesgo alto) y el 35 % del 2CB analizado no era 2CB. El riesgo de salud no lo mide ningún registro oficial.')],
 'apps':[('../../medellin/','Mapa de Medellín · cruces de microtráfico (comuna 10) y drogas sintéticas (comuna 14)'),('../../datos/#rentas','Rigor Datos · cannabis y drogas sintéticas')],
 'inv':[('org','Échele Cabeza (Corporación Acción Técnica Social) · Informe de análisis de sustancias 2021','https://www.echelecabeza.com/wp-content/uploads/2022/05/Informe_2021.pdf','2.868 sustancias analizadas; 395 en Medellín; mezclas del tusibi, pureza de la cocaína (41 % entre 25 y 50 %), precios y formas de compra. Reducción de riesgos para personas adultas.'),
  ('aca','CESED · Centro de Estudios sobre Seguridad y Drogas, Universidad de los Andes','https://cesed.uniandes.edu.co','Investigación sobre política de drogas, seguridad y mercados ilegales.'),
  ('org','Elementa DDHH','https://elementaddhh.org','Política de drogas con enfoque de derechos humanos.'),
  ('org','Dejusticia','https://www.dejusticia.org','Investigación jurídica sobre drogas, cárceles y derechos.'),
  ('adm','DANE · Encuesta Nacional de Consumo de Sustancias Psicoactivas 2019','https://www.dane.gov.co/files/investigaciones/boletines/encspa/bt-encspa-2019.pdf','La medición nacional más reciente del consumo.')]},
{'s':'economias','t':'Economías ilícitas y Estado paralelo','i':'💰','q':'¿Quién regula donde el Estado no llega, y con qué plata?',
 'con':[('Hallazgo','Lo ilícito pesa más del 8 % del PIB','Al menos $142 billones al año sumando rentas ilícitas medidas y corrupción; más del doble de toda la minería legal.'),
  ('Brecha','Sustitución normativa','En la Comuna 13 el comercio paga vacuna a quien manda en el barrio; en Santa Marta un grupo armado intentó imponer un paro armado en 2026. Quien cobra y protege no es el Estado.'),
  ('Brecha','El crédito legal no llega a la esquina','El crédito de bajo monto se creó para competirle al gota a gota; en la práctica, en municipios como Marinilla el gota a gota es lo que está a la mano (observación de campo, por medir).'),
  ('Hallazgo','99.097 familias en el programa de sustitución','Son solo las que entraron al PNIS; muestran cuánta gente vive de la coca por falta de alternativas.')],
 'apps':[('../../datos/#conclusion','Rigor Datos · todo lo ilícito en una cuenta'),('../../datos/#legal','País legal frente a país ilegal'),('../../medellin/','Mapa de Medellín · extorsión en la comuna 13')],
 'inv':[('aca','Centro de Valor Público, Universidad EAFIT · Economía de la cocaína','https://www.bluradio.com/regiones/antioquia/segun-estudio-cocaina-supero-al-petroleo-como-principal-producto-de-exportacion-en-colombia-rg10','La cocaína pesó 4,4 % del PIB en 2024.'),
  ('org','Fundación Ideas para la Paz (FIP)','https://ideaspaz.org','Seguridad, crimen organizado y sustitución de cultivos.'),
  ('org','Indepaz','https://indepaz.org.co','Masacres, líderes sociales y presencia de grupos armados.'),
  ('org','Fundación Paz y Reconciliación (Pares)','https://www.pares.com.co','Crimen organizado y subregistro de la extorsión.'),
  ('pre','InSight Crime','https://insightcrime.org/es/','Periodismo de investigación sobre crimen organizado en América Latina.')]},
{'s':'memoria','t':'Memoria y desaparición forzada','i':'🕯️','q':'¿Qué le debe el Estado a las familias que siguen buscando?',
 'con':[('Diferencia','La búsqueda avanza y depende de recursos','La JEP halló, identificó y entregó 7 cuerpos en La Escombrera desde 2024; la continuidad dependió de una orden judicial (Auto AI-48 de 2025) para garantizar la plata.'),
  ('Vacío','El catastro no refleja lo que la JEP protege','El suelo figura como rural común mientras es posible fosa común. Falta cruzar el polígono exacto con el número predial.'),
  ('Hallazgo','El Estado contrató explotación minera sobre ese suelo','En 2002 la Gobernación firmó contratos de explotación en La Escombrera y La Arenera. Falta saber qué obligaciones de cuidado tenían.')],
 'apps':[('../../medellin/','Mapa de Medellín · pestaña Memoria y cruce de La Escombrera'),('../../cumplimiento/','Hallazgos graves · La Escombrera')],
 'inv':[('jud','Jurisdicción Especial para la Paz (JEP)','https://www.jep.gov.co','Medidas cautelares y búsqueda en La Escombrera.'),
  ('adm','Unidad de Búsqueda de Personas dadas por Desaparecidas','https://ubpdbusquedadesaparecidos.co','Búsqueda humanitaria.'),
  ('adm','Centro Nacional de Memoria Histórica','https://www.centrodememoriahistorica.gov.co','Memoria de las operaciones en la Comuna 13.'),
  ('aca','Universidad de los Andes · Espacios de memoria: el caso de La Escombrera','https://cienciassociales.uniandes.edu.co/opca/articulo/espacios-de-memoria-el-caso-de-la-escombrera-en-medellin','Historia de las denuncias y de la búsqueda.'),
  ('org','Instituto Popular de Capacitación (IPC)','https://www.ipc.org.co','Derechos humanos en Medellín.')]},
{'s':'contratacion','t':'Contratación y corrupción','i':'⚖️','q':'¿Se escoge con competencia real a quien se le paga con plata pública?',
 'con':[('Brecha','La excepción pesa más que la regla','La Ley 1150 de 2007 hace de la licitación la regla; en el Oriente, buena parte de la plata se contrata a dedo.'),
  ('Brecha','Competencia de papel','En San Carlos, 55 de 57 procesos con competencia recibieron una sola oferta desde 2024.'),
  ('Hallazgo','El pico del año electoral','La Ceja firmó el 32,2 % de la plata del cuatrienio 2020–2023 en sus últimos seis meses; revisado, no son duplicados.')],
 'apps':[('../../contratacion/','Rigor Contratación · los 23 municipios del Oriente'),('../../cumplimiento/','Hallazgos graves · rutas de exigencia')],
 'inv':[('org','Transparencia por Colombia · Monitor Ciudadano de la Corrupción','https://transparenciacolombia.org.co','Índice de Percepción de la Corrupción y hechos de corrupción documentados.'),
  ('adm','SECOP II · datos abiertos','https://www.datos.gov.co/d/jbjy-vk9h','Todos los contratos electrónicos del Estado.'),
  ('pre','La Silla Vacía','https://www.lasillavacia.com','Periodismo de poder y verificación de datos.')]},
{'s':'narcocultura','t':'Narcocultura y redes','i':'📱','q':'¿Cómo el narcoestereotipo alimenta la demanda y el reclutamiento?',
 'con':[('Hipótesis','La aspiración empuja, la falta de opciones decide','Los jóvenes de un mismo barrio ven las mismas redes y no todos entran; quien entra suele ser quien además no tiene otra opción. Falta medirlo.'),
  ('Hallazgo','Una ética del triunfo rápido','Omar Rincón describió en 2009 la narcocultura como "una cultura del todo vale para salir de pobre", con la ostentación en el centro.'),
  ('Vacío','Nadie mide el contenido','Proponemos un análisis de contenido de redes con método escrito: muestra de publicaciones de una zona y categorías fijas (ostentación, dinero fácil, violencia, mujer como trofeo).')],
 'apps':[('../../noticias/','Noticias y videos · drogas y estructuras criminales')],
 'inv':[('aca','Omar Rincón · Narco.estética y narco.cultura en Narco.lombia (Nueva Sociedad 222, 2009)','https://nuso.org/articulo/narcoestetica-y-narcocultura-en-narcolombia/','El texto que fundó el estudio de la narcocultura en Colombia.'),
  ('aca','Revisión crítica del concepto de narcocultura (Redalyc)','https://www.redalyc.org/journal/185/18568993007/18568993007.epub','Discute los alcances y límites del concepto de Rincón.'),
  ('aca','Del paisano al parcero: el narcotráfico en la cultura medellinense, 1984–1995 (Universidad Nacional)','https://revistas.unal.edu.co/index.php/forum/article/view/115091','Lenguaje, música y literatura antes y después del narcotráfico en Medellín.')]},
{'s':'penal','t':'Sistema penal y seguridad','i':'🚔','q':'¿A quién captura el Estado, a quién no, y qué registra?',
 'con':[('Diferencia','La extorsión oficial mide la denuncia','El registro baja mientras la academia estima un subregistro de hasta tres veces.'),
  ('Hallazgo','Secuestro extorsivo: el más alto en una década','477 casos en 2025.'),
  ('Contradicción','Dos cifras oficiales de un mismo mes','Agosto de 2026: el Gobierno reportó −79 % en secuestro; los datos del Ministerio de Defensa, −58 %.')],
 'apps':[('../../medellin/','Mapa de Medellín · capas de seguridad y cruces'),('../../datos/#actual','Rigor Datos · gobierno actual')],
 'inv':[('org','Temblores ONG','https://www.temblores.org','Violencia policial y derechos humanos.'),
  ('org','Medellín Cómo Vamos','https://www.medellincomovamos.org','Calidad de vida y seguridad en Medellín.'),
  ('adm','MEData · datos abiertos de Medellín','https://medata.gov.co','Seguridad por comuna (SISC).')]}]
def head(t,desc,rel):
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><title>{E(t)} · Observa Rigor</title><meta name="description" content="{E(desc)}"><meta property="og:title" content="{E(t)} · Observa Rigor"><meta property="og:description" content="{E(desc)}"><meta name="theme-color" content="#0A0716">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🧭</text></svg>"><link href="https://fonts.googleapis.com/css2?family=Anton&family=Manrope:wght@400;600;800&family=Playfair+Display:ital,wght@1,800&display=swap" rel="stylesheet">
<style>:root{{--bg:#0A0716;--bg2:#120C22;--txt:#F7F3FF;--suave:#B4ABC8;--sol:#FFC93C;--rosa:#FF4F8B;--grad:linear-gradient(115deg,#FFC93C,#FF8A3D 45%,#FF4F8B);color-scheme:dark;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}*{{box-sizing:inherit}}body{{margin:0;background:var(--bg);color:var(--txt);font-family:Manrope,system-ui,sans-serif;line-height:1.55}}.wrap{{max-width:1050px;margin:0 auto;padding:0 18px}}a{{color:var(--sol)}}
nav{{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:rgba(10,7,22,.88);backdrop-filter:blur(10px);border-bottom:1px solid rgba(255,255,255,.08)}}nav .wrap{{display:flex;align-items:center;gap:8px;padding:12px 18px}}nav b{{font-family:Anton,sans-serif;letter-spacing:.04em}}
h1,h2{{font-family:Anton,Impact,sans-serif;font-weight:400;text-transform:uppercase;line-height:1.03}}h1{{font-size:clamp(2.2rem,6vw,4rem);margin:34px 0 8px;text-shadow:0 2px 0 #3a2457,0 4px 0 #2a1a40,0 10px 22px rgba(0,0,0,.6)}}h2{{font-size:clamp(1.5rem,3.6vw,2.2rem);margin:30px 0 8px}}.grad{{font-family:'Playfair Display',serif;font-style:italic;text-transform:none;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}}
.kick{{color:var(--sol);font-size:.75rem;font-weight:800;letter-spacing:.18em;text-transform:uppercase}}.lead{{color:var(--suave);font-size:1.05rem;max-width:70ch}}.q{{font-size:1.25rem;font-weight:800;padding:16px 18px;border-radius:16px;background:linear-gradient(135deg,rgba(255,201,60,.12),rgba(255,79,139,.12));border-left:4px solid var(--sol)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:14px;margin:18px 0}}.card{{display:block;text-decoration:none;color:inherit;background:var(--bg2);border:1px solid rgba(255,255,255,.09);border-radius:20px;padding:18px;transition:border-color .2s,transform .2s}}a.card:hover{{border-color:rgba(255,201,60,.5);transform:translateY(-3px)}}.card .ic{{font-size:2rem}}.card h3{{margin:6px 0}}.card p{{color:var(--suave);margin:0}}
.con{{background:var(--bg2);border-radius:16px;padding:14px 16px;margin:10px 0;border:1px solid rgba(255,255,255,.08)}}.tag{{display:inline-block;font-size:.66rem;font-weight:800;padding:2px 9px;border-radius:99px;background:#9aa0ff;color:#0B0814;margin-bottom:6px}}.tag.Brecha,.tag.Contradicción{{background:var(--rosa)}}.tag.Hallazgo{{background:#7CF7B0}}.tag.Hipótesis,.tag.Vacío{{background:var(--sol)}}.con b{{display:block}}.con p{{margin:4px 0 0;color:var(--suave)}}
.src{{display:block;text-decoration:none;color:inherit;padding:12px 0;border-bottom:1px solid rgba(255,255,255,.08)}}.src small{{display:inline-block;font-size:.66rem;font-weight:800;padding:1px 8px;border-radius:8px;background:rgba(255,255,255,.1);margin-right:6px}}.src b{{color:var(--sol)}}.src p{{margin:4px 0 0;color:var(--suave);font-size:.9rem}}
.ap{{border:2px dashed rgba(255,255,255,.2);border-radius:18px;padding:18px;color:var(--suave)}}.ap a.wa{{display:inline-block;margin-top:10px;padding:11px 16px;border-radius:12px;background:#25D366;color:#06210f;font-weight:800;text-decoration:none}}footer{{padding:30px 0 60px;color:var(--suave);font-size:.85rem}}</style></head><body><nav><div class="wrap"><b><a href="{rel}" style="color:inherit;text-decoration:none">OBSERVA RIGOR</a></b></div></nav><div class="wrap">'''
FOOT='</div><footer><div class="wrap">Observa Rigor · Lo que no se mide, no se exige.</div></footer></body></html>'
def build(OUT):
    os.makedirs(os.path.join(OUT,'clusters'),exist_ok=True)
    idx=head('Clústeres','Las preguntas que investiga Observa Rigor, con conclusiones, datos, investigaciones de referencia y aportes.','../')
    idx+='<p class="kick" style="margin-top:30px">Clústeres</p><h1>Empezá por una <span class="grad">pregunta</span></h1><p class="lead">Cada clúster reúne lo que sabemos sobre un problema: la pregunta, las conclusiones redactadas como deber, los datos de nuestras apps, las investigaciones serias que lo estudian y, pronto, los aportes de quienes viven el problema.</p><div class="grid">'
    idx+=''.join(f'<a class="card" href="{c["s"]}/"><span class="ic">{c["i"]}</span><h3>{E(c["t"])}</h3><p>{E(c["q"])}</p></a>' for c in C)+'</div>'+FOOT
    open(os.path.join(OUT,'clusters','index.html'),'w',encoding='utf8').write(idx)
    for c in C:
        h=head(c['t'],c['q'],'../../')
        h+=f'<p class="kick" style="margin-top:30px"><a href="../">Clústeres</a> · {c["i"]}</p><h1>{E(c["t"])}</h1><p class="q">{E(c["q"])}</p>'
        h+='<h2>Lo que sabemos</h2>'+''.join(f'<div class="con"><span class="tag {k}">{k}</span><b>{E(t)}</b><p>{E(d)}</p></div>' for k,t,d in c['con'])
        h+='<h2>Míralo en los datos</h2><div class="grid">'+''.join(f'<a class="card" href="{u}"><h3>{E(t)} →</h3></a>' for u,t in c['apps'])+'</div>'
        h+='<h2>Investigaciones y fuentes de referencia</h2><p class="lead">Organizaciones y estudios serios que trabajan este tema. Cada uno con su tipo de fuente.</p>'+''.join(f'<a class="src" href="{u}" target="_blank" rel="noopener"><small>{TIPO[tp]}</small><b>{E(t)} →</b><p>{E(d)}</p></a>' for tp,t,u,d in c['inv'])
        h+=f'<h2>Aportes</h2><div class="ap"><b>Muy pronto: aportes moderados.</b><p>Vas a poder contar lo que ves en tu territorio. Cada aporte entra como señal, pasa por moderación y no se publica con nombres de personas ni datos que ubiquen a nadie. Mientras tanto, escribinos.</p><a class="wa" target="_blank" rel="noopener" href="https://wa.me/573113866341?text={__import__("urllib.parse").parse.quote("Hola, Observa Rigor 👋 Quiero aportar al clúster: "+c["t"]+" 📌")}">💬 Aportar por WhatsApp</a></div>'
        os.makedirs(os.path.join(OUT,'clusters',c['s']),exist_ok=True)
        open(os.path.join(OUT,'clusters',c['s'],'index.html'),'w',encoding='utf8').write(h+FOOT)
    print('  ✓ clusters/ (%d clústeres)'%len(C))
if __name__=='__main__':import sys;build(sys.argv[1] if len(sys.argv)>1 else 'sitio')
