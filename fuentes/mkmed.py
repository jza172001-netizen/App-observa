s=open('live_med.html',encoding='utf8').read()
a=open('analisis.js',encoding='utf8').read().replace('__TEND__',open('tend.json').read())
old="{n:'Estación Villa',"
esc="{n:'La Escombrera',ll:[-75.6386,6.2588],k:'13',own:'ladera',r:1,s:['jep7','op34','ai48'],h:()=>'Vista desde la Comuna 13. Por casi dos décadas fue depósito de escombros y, según la JEP, una fosa común: desde diciembre de 2024 se hallaron 7 cuerpos, todos identificados y entregados a sus familias. Ubicación aproximada.'},\n "
s=s.replace(old,esc+old);i=s.rfind('</body>');s=s[:i]+'<script>\n'+a+'\n</script>\n<script>\n'+open('conclu.js',encoding='utf8').read()+'\n</script>\n<script>\n'+open('fx/fx.js',encoding='utf8').read()+'\n'+open('fx/pilotos.js',encoding='utf8').read()+'\n</script>\n'+s[i:]
s=s.replace('<body>','<body data-orn-nobottom>',1).replace('<div class="top">','<div class="top" data-orn-slot>',1)
MOB='<style>@media (max-width:820px){.giro{transform:scale(.62);transform-origin:left bottom;left:8px!important}.panel:not(.min)~.giro{display:none!important}.panel:not(.min)~.tira{display:none!important}.fab button,.fab a{width:38px!important;height:38px!important}.top .orn-in{background:rgba(13,9,25,.75);backdrop-filter:blur(8px)}}</style>'
i=s.rfind('</body>');s=s[:i]+MOB+'<script>'+open('fx/nav.js',encoding='utf8').read()+'</script>'+s[i:]
open('site/medellin/index.html','w',encoding='utf8').write(s)
