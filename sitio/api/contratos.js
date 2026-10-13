// Contratación en vivo: últimos 30 días de un municipio en el SECOP II (datos abiertos). Caché de 24 horas.
module.exports=async(req,res)=>{try{const c=String((req.query||{}).c||'').replace(/[^A-Za-zÁÉÍÓÚáéíóúÑñü .]/g,'').slice(0,40);if(!c)throw new Error('falta municipio');
 const d=new Date(Date.now()-30*864e5).toISOString().slice(0,10),hoy=new Date().toISOString().slice(0,10);
 const w=encodeURIComponent("departamento='Antioquia' AND ciudad='"+c+"' AND fecha_de_firma>='"+d+"' AND fecha_de_firma<='"+hoy+"T23:59:59'");
 const u='https://www.datos.gov.co/resource/jbjy-vk9h.json?$select=modalidad_de_contratacion as m,count(*) as n,sum(valor_del_contrato) as v&$where='+w+'&$group=modalidad_de_contratacion&$limit=50';
 const r=await (await fetch(u)).json();let n=0,v=0,nd=0,vd=0;(Array.isArray(r)?r:[]).forEach(x=>{const k=+x.n,s=+(x.v||0);n+=k;v+=s;if(/directa/i.test(x.m||'')){nd+=k;vd+=s}});
 res.setHeader('Cache-Control','s-maxage=86400, stale-while-revalidate=172800');res.status(200).json({desde:d,hasta:hoy,n,v,nd,vd})}catch(e){res.status(200).json({error:String(e)})}};
