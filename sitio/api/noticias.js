// Noticias en vivo: lee Google Noticias por tema y devuelve JSON con caché de 1 hora.
// Respuesta: {ok:true, items, actualizado} o {ok:false, error} con código 502 si falla la fuente.
const TEMAS={ddhh:'"derechos humanos" Colombia OR "desaparición forzada" OR "líderes sociales"',corrupcion:'corrupción Colombia contratación OR Procuraduría OR Contraloría',seguridad:'Medellín extorsión OR microtráfico OR "trata de personas" OR "gota a gota"',drogas:'Medellín tusi OR "drogas sintéticas" OR marihuana OR consumo',oriente:'Rionegro OR "La Ceja" OR Marinilla OR "El Peñol" OR Guarne Antioquia alcaldía',escombrera:'"La Escombrera" OR "Comuna 13" desaparecidos OR JEP OR buscadoras',desaparicion:'"desaparición forzada" OR "Unidad de Búsqueda" OR "madres buscadoras" Colombia',conflicto:'Antioquia "conflicto armado" OR masacre OR desplazamiento OR "líder social"',grupos:'"Oficina de Envigado" OR "La Terraza" OR "Los Chatas" OR Pachelly OR "La Mesa" OR "Clan del Golfo" Medellín OR Antioquia',economia:'Colombia desempleo OR informalidad OR pobreza OR desigualdad DANE',contratos:'Antioquia contrato OR contratación OR Contraloría OR Procuraduría alcaldía irregularidades'};
const {XMLParser}=require('fast-xml-parser');
const parser=new XMLParser({ignoreAttributes:false,attributeNamePrefix:'@',textNodeName:'#text',processEntities:true,htmlEntities:true});
const txt=v=>(v==null?'':typeof v==='object'?(v['#text']??''):String(v)).trim();
module.exports=async(req,res)=>{res.setHeader('Access-Control-Allow-Origin','*');
 try{const q=req.query||{};let t=TEMAS[q.t]||TEMAS.seguridad;
  if(q.t==='mun'&&q.m){const m=String(q.m).replace(/[^A-Za-zÁÉÍÓÚáéíóúÑñü .]/g,'').slice(0,40);if(m)t='"'+m+'" Antioquia alcaldía OR contrato OR Contraloría OR Procuraduría OR corrupción'}
  const u='https://news.google.com/rss/search?q='+encodeURIComponent(t+' when:30d')+'&hl=es-419&gl=CO&ceid=CO:es-419';
  const r=await fetch(u,{headers:{'User-Agent':'Mozilla/5.0 ObservaRigor'}});if(!r.ok)throw new Error('Google Noticias respondió '+r.status);
  const doc=parser.parse(await r.text());const ch=doc&&doc.rss&&doc.rss.channel;if(!ch)throw new Error('La respuesta no es un RSS válido');
  const lista=[].concat(ch.item||[]);
  const items=lista.slice(0,12).map(it=>{let ti=txt(it.title);const src=txt(it.source);if(src&&ti.endsWith(' - '+src))ti=ti.slice(0,-(src.length+3));return {t:ti,u:txt(it.link),f:txt(it.pubDate),s:src}}).filter(i=>i.t&&i.u);
  res.setHeader('Cache-Control','s-maxage=3600, stale-while-revalidate=86400');res.status(200).json({ok:true,actualizado:new Date().toISOString(),items})}
 catch(e){res.setHeader('Cache-Control','no-store');res.status(502).json({ok:false,error:String(e.message||e),items:[]})}};
