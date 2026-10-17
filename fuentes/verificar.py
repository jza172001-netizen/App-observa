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
print('Todo en orden.' if not mal else f'{mal} problemas.')

# Revisión opcional de enlaces externos:  python verificar.py sitio --enlaces
if '--enlaces' in sys.argv:
    import urllib.request,concurrent.futures as cf
    urls=set()
    for r,_,fs in os.walk(OUT):
        for f in fs:
            if f.endswith('.html'):urls|={u if u.count('(')>=u.count(')') else u[:-1] for u in re.findall(r"https?://[^\s'\"<>]+",open(os.path.join(r,f),encoding='utf8').read())}
    urls={u.rstrip('.,;') for u in urls if not re.search(r'(fonts\.|cdnjs|jsdelivr|ytimg|youtube-nocookie|wa\.me|api\.|tile|openfreemap|amazonaws|arcgisonline|google\.com/maps|earth\.google|\$\{|\'\+)',u)}
    def ok(u):
        for m in ('HEAD','GET'):
            try:
                r=urllib.request.urlopen(urllib.request.Request(u,method=m,headers={'User-Agent':'Mozilla/5.0 ObservaRigor'}),timeout=20);return u,r.status
            except Exception as e:
                c=getattr(e,'code',None)
                if c in (403,429):return u,c
                last=c or str(e)[:40]
        return u,last
    with cf.ThreadPoolExecutor(12) as ex:res=list(ex.map(ok,sorted(urls)))
    rotos=[(u,c) for u,c in res if not (isinstance(c,int) and c<400) and c not in (403,429)]
    print(f'Enlaces externos revisados: {len(res)} · con problema: {len(rotos)}')
    for u,c in rotos:print('  ✗',c,u)

sys.exit(1 if mal else 0)
