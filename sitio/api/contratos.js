// Contratación en vivo: últimos 30 días de un municipio en el SECOP II (datos.gov.co, jbjy-vk9h). Caché de 24 horas.
// Respuesta: {ok:true, desde, hasta, n, v, nd, vd} o {ok:false, error} con código 400/502.
module.exports=async(req,res)=>{res.setHeader('Access-Control-Allow-Origin','*');
 const c=String((req.query||{}).c||'').replace(/[^A-Za-zÁÉÍÓÚáéíóúÑñü .]/g,'').slice(0,40).trim();
 if(!c){res.status(400).json({ok:false,error:'Falta el municipio (parámetro c)'});return}
 try{const d=new Date(Date.now()-30*864e5).toISOString().slice(0,10),hoy=new Date().toISOString().slice(0,10);
  const w=encodeURIComponent("departamento='Antioquia' AND ciudad='"+c+"' AND fecha_de_firma>='"+d+"' AND fecha_de_firma<='"+hoy+"T23:59:59'");
  const r=await fetch('https://www.datos.gov.co/resource/jbjy-vk9h.json?$select=modalidad_de_contratacion as m,count(*) as n,sum(valor_del_contrato) as v&$where='+w+'&$group=modalidad_de_contratacion&$limit=50');
  if(!r.ok)throw new Error('datos.gov.co respondió '+r.status);const a=await r.json();if(!Array.isArray(a))throw new Error('Respuesta inesperada de datos.gov.co');
  let n=0,v=0,nd=0,vd=0;a.forEach(x=>{const k=+x.n||0,s=+x.v||0;n+=k;v+=s;if(/directa/i.test(x.m||'')){nd+=k;vd+=s}});
  res.setHeader('Cache-Control','s-maxage=86400, stale-while-revalidate=172800');res.status(200).json({ok:true,fuente:'SECOP II (jbjy-vk9h), fecha de firma',desde:d,hasta:hoy,n,v,nd,vd})}
 catch(e){res.setHeader('Cache-Control','no-store');res.status(502).json({ok:false,error:String(e.message||e)})}};
