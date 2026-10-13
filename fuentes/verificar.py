"""Revisa el sitio antes de publicar: sintaxis de cada script, claves filtradas y enlaces internos.
Uso:  python verificar.py [carpeta_sitio]"""
import os,re,subprocess,sys,tempfile
OUT=sys.argv[1] if len(sys.argv)>1 else 'sitio';mal=0
for r,_,fs in os.walk(OUT):
    for f in fs:
        p=os.path.join(r,f)
        if f.endswith(('.html','.js')):
            s=open(p,encoding='utf8').read()
            if re.search(r'(ghp_|github_pat_|vcp_)[A-Za-z0-9_]{20,}',s):print('✗ posible clave en',p);mal+=1
            bloques=re.findall(r'<script>(.*?)</script>',s,re.S) if f.endswith('.html') else [s]
            for i,b in enumerate(bloques):
                with tempfile.NamedTemporaryFile('w',suffix='.js',delete=False,encoding='utf8') as t:t.write(b)
                if subprocess.run(['node','--check',t.name],capture_output=True).returncode:print('✗ error de sintaxis en',p,'script',i+1);mal+=1
                os.unlink(t.name)
            if f.endswith('.html'):
                for h in re.findall(r'href="(/[a-z]+/)',s):
                    if not os.path.exists(os.path.join(OUT,h.strip('/'),'index.html')):print('✗ enlace roto',h,'en',p);mal+=1
print('Todo en orden.' if not mal else f'{mal} problemas.');sys.exit(1 if mal else 0)
