"""Segunda capa de alertas: modalidades (Ley 1150), cierre de mandato 2020-23, oferente único, pagos, obras, multientidad -> contra.json + c/*.json"""
import json,re,collections,datetime as dt,os
C=json.load(open('contratos.json'));CI=json.load(open('ciudades.json'));D=json.load(open('contra.json'));X=json.load(open('extra.json'));K=json.load(open('cruces.json'))
c2m={v:k for k,v in CI.items() if v};dig=lambda s:re.sub(r'\D','',s or '');fe=lambda s:dt.date.fromisoformat(s[:10]) if s else None
nm=lambda u:(re.search(r'CO1\.NTC\.\d+',u.get('url','') if isinstance(u,dict) else (u or '')) or [None])[0]
def cat(m):
    l=(m or '').lower()
    if 'directa' in l:return 'directa'
    if 'gimen especial' in l:return 'regimen'
    if 'nima cuant' in l:return 'minima'
    if 'abreviada' in l or l=='subasta' or 'subasta inversa' in l:return 'abreviada'
    if 'rito' in l:return 'meritos'
    if 'licitaci' in l:return 'licitacion'
    return 'otra'
HOY=dt.date(2026,10,12);CORTE=HOY-dt.timedelta(days=90);G0,G1=dt.date(2026,1,31),dt.date(2026,6,21)
ent_x_doc=collections.defaultdict(set);n_x_doc=collections.Counter()
for r in C:
    if (r.get('tipodocproveedor') or '').upper()=='NIT':d=dig(r.get('documento_proveedor'));ent_x_doc[d].add(r.get('nombre_entidad'));n_x_doc[d]+=1
multi={d for d,e in ent_x_doc.items() if len(e)>=4 and n_x_doc[d]>=10}
cl=collections.Counter((r.get('nombre_entidad'),r.get('documento_proveedor'),(r.get('fecha_de_firma') or '')[:7]) for r in C if cat(r.get('modalidad_de_contratacion'))=='directa')
vd=sorted(float(r.get('valor_del_contrato') or 0) for r in C if cat(r.get('modalidad_de_contratacion'))=='directa');alto=vd[int(len(vd)*.99)]
por=collections.defaultdict(list)
for r in C:por[c2m.get(r.get('ciudad'))].append(r)
# curva de mandato 2020-2023 (SECOP I + II)
cur=collections.defaultdict(lambda:[[0,0] for _ in range(48)])
for s,key in((X['s2'],'ciudad'),(X['s1'],'municipio_entidad')):
    for x in s:
        m=c2m.get(x[key]) if key=='ciudad' else x[key]
        if not m:continue
        y,mo=int(x['m'][:4]),int(x['m'][5:7]);i=(y-2020)*12+mo-1
        if 0<=i<48:cur[m][i][0]+=int(x['n']);cur[m][i][1]+=float(x['v'] or 0)
s1mod=collections.defaultdict(lambda:collections.Counter())
for x in X['s1mod']:s1mod[x['municipio_entidad']][cat(x['modalidad_de_contratacion'])]+=float(x['v'] or 0)
os.makedirs('out/c',exist_ok=True);tot=collections.Counter()
for m,info in D['municipios'].items():
    rs=por.get(m,[]);mod=collections.defaultdict(lambda:[0,0]);grp=[0,0];comp=[0,0];nE=nX=nV=nU=0;out=[]
    ents=sorted({(r.get('nombre_entidad') or '').strip().title() for r in rs});ei={e:i for i,e in enumerate(ents)}
    for r in rs:
        v=float(r.get('valor_del_contrato') or 0);c=cat(r.get('modalidad_de_contratacion'));mod[c][0]+=1;mod[c][1]+=v
        p=X['pagos'].get(r.get('id_contrato'),[0,0,'',None]);d=dig(r.get('documento_proveedor'));nat=(r.get('tipodocproveedor') or '').upper()!='NIT'
        nombre=('Persona natural ···'+d[-4:]) if nat else (r.get('proveedor_adjudicado') or '').strip()[:70]
        es_g=bool(re.search(r'CONSORCIO|UNI[OÓ]N TEMPORAL',(r.get('proveedor_adjudicado') or '').upper())) or str(p[3]).lower()=='si'
        if es_g:grp[0]+=1;grp[1]+=v
        f,i,fin,ad=fe(r.get('fecha_de_firma')),fe(r.get('fecha_de_inicio_del_contrato')),fe(r.get('fecha_de_fin_del_contrato')),float(r.get('dias_adicionados') or 0)
        of=X['ofertas'].get(nm(r.get('urlproceso')))
        fl=''
        if c=='directa':fl+='D'
        if c=='directa' and f and G0<=f<=G1:fl+='G'
        if ad>0 and i and fin and (fin-i).days-ad>0 and ad/((fin-i).days-ad)>=.5:fl+='P'
        if c=='directa' and cl[(r.get('nombre_entidad'),r.get('documento_proveedor'),(r.get('fecha_de_firma') or '')[:7])]>=3:fl+='R'
        if d in K['multas']:fl+='M'
        if d in K['siri']:fl+='S'
        if c=='directa' and v>=alto:fl+='A'
        if c in('licitacion','abreviada','meritos'):
            comp[0]+=1
            if of==1:fl+='U';comp[1]+=1;nU+=1
        if v>0 and max(p[0],p[1])>v*1.02:fl+='X';nX+=1
        if (r.get('tipo_de_contrato')=='Obra') and ((r.get('estado_contrato')=='Suspendido') or (fin and fin<CORTE and r.get('estado_contrato') not in('Cerrado','terminado') and p[0]<v*.5)):fl+='E';nE+=1
        if not nat and d in multi:fl+='V';nV+=1
        u=r.get('urlproceso');u=u.get('url') if isinstance(u,dict) else u
        out.append({'e':ei[(r.get('nombre_entidad') or '').strip().title()],'p':nombre,'mo':r.get('modalidad_de_contratacion'),'t':r.get('tipo_de_contrato'),'v':round(v),'pg':round(p[0]),'f':(r.get('fecha_de_firma') or '')[:10],'fn':(r.get('fecha_de_fin_del_contrato') or '')[:10],'es':r.get('estado_contrato'),'of':of,'g':1 if es_g else 0,'ad':int(ad),'o':(r.get('objeto_del_contrato') or '')[:150],'u':u,'fl':fl})
    out.sort(key=lambda x:-x['v'])
    if rs:json.dump({'ent':ents,'c':out},open(f"out/c/{info['cod']}.json",'w'),ensure_ascii=False,separators=(',',':'))
    cu=cur.get(m);vt=sum(x[1] for x in cu) if cu else 0;nt=sum(x[0] for x in cu) if cu else 0
    cierre={'curva':[[a,round(b)] for a,b in cu],'n':nt,'v':round(vt),'nd':round(sum(x[1] for x in cu[46:])/vt*100,1) if vt else None,'s2':round(sum(x[1] for x in cu[42:])/vt*100,1) if vt else None} if cu else None
    info['modalidades']={k:[a,round(b)] for k,(a,b) in mod.items()};info['grupos']=[grp[0],round(grp[1])];info['secop1_mod']={k:round(v) for k,v in s1mod.get(m,{}).items()}
    info['competidos']=comp;info['n2']={'U':nU,'X':nX,'E':nE,'V':nV};info['cierre']=cierre
    al=set(info.get('alertas',[]))
    if comp[0]>=10 and comp[1]/comp[0]>=.6:al.add('unico')
    if nE>=3:al.add('obras')
    if nX>=3:al.add('pagos')
    if cierre and nt>=200 and ((cierre['nd'] or 0)>=12.5 or (cierre['s2'] or 0)>=25):al.add('cierre')
    info['alertas']=sorted(al);tot.update(al)
    print(f"{m:22} comp {comp} U{nU} X{nX} E{nE} V{nV} cierreND {cierre and cierre['nd']} s2 {cierre and cierre['s2']} n {nt} {sorted(al)}")
D['alto']=round(alto);D['periodo_mandato']='Contratos firmados entre el 1 de enero de 2020 y el 31 de diciembre de 2023 (SECOP I + SECOP II)'
json.dump(D,open('out/contra.json','w'),ensure_ascii=False,separators=(',',':'));print(tot)
