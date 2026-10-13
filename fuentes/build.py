"""Base geosocial de Medellín por comuna -> base.json (datos separados de la lógica)."""
import json, statistics, urllib.parse, urllib.request
import pandas as pd

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"
S = "https://www.medellin.gov.co/servidormapas/rest/services/"

def q(path, where="1=1", fields="*", geo=False, simp=None, page=1000):
    out, off = [], 0
    while True:
        p = {"where": where, "outFields": fields, "returnGeometry": str(geo).lower(), "outSR": 4326,
             "f": "geojson" if geo else "json", "resultOffset": off, "resultRecordCount": page}
        if simp: p["maxAllowableOffset"] = simp
        r = urllib.request.Request(S + path + "/query?" + urllib.parse.urlencode(p), headers={"User-Agent": UA})
        fs = json.load(urllib.request.urlopen(r, timeout=120)).get("features", [])
        out += fs
        if len(fs) < page: return out
        off += page

def cod(x):
    s = str(x).strip()
    try: return str(int(float(s)))
    except ValueError: return s
if __name__ == "__main__":
    comunas = q("ServiciosCatastro/Base_Catastral/MapServer/0", fields="comuna,nombre", geo=True, simp=0.0002)
    C = {cod(f["properties"]["comuna"]): {"nombre": f["properties"]["nombre"]} for f in comunas}

    for lay, key in [(1, "ipm"), (2, "imcv")]:
        for f in q("estadisticas/VC_Indicadores_ECV/MapServer/%d" % lay, fields="codigo,i_2024,i_2014"):
            a = f["attributes"]; k = cod(a["codigo"])
            if k in C: C[k][key] = a["i_2024"]; C[k][key + "_2014"] = a["i_2014"]

    zge = {}
    for f in q("ServiciosCatastro/Base_Catastral/MapServer/12", fields="comuna,valor_m2"):
        a = f["attributes"]; zge.setdefault(cod(a["comuna"]), []).append(a["valor_m2"])
    for k, v in zge.items():
        if k in C: C[k]["suelo_m2"] = int(statistics.median(v))

    for f in q("mapas_nacionales/VC_Catastro/MapServer/4", fields="comuna,poblacion_aprox"):
        a = f["attributes"]; k = cod(a["comuna"])
        if k in C: C[k]["poblacion"] = C[k].get("poblacion", 0) + (a["poblacion_aprox"] or 0)

    for f in q("salud_protec_soc/VM_Evol_ViolenciaGenero/MapServer/9", fields="comuna,tasa_2021,casos_2021"):
        a = f["attributes"]; k = cod(a["comuna"])
        if k in C: C[k]["vg_tasa_2021"] = a["tasa_2021"]

    for f in q("ccio_ind_turism/VC_Turismo/MapServer/0", fields="cod_comuna"):
        k = cod(f["attributes"]["cod_comuna"])
        if k in C: C[k]["atractivos"] = C[k].get("atractivos", 0) + 1

    cap = pd.read_csv("captura.csv", usecols=["fecha_hecho", "cantidad", "articulo_penal", "codigo_comuna"], dtype=str)
    cap = cap[cap.articulo_penal.str.startswith("376", na=False)]
    cap["anio"] = cap.fecha_hecho.str[:4].astype(int)
    cap["cantidad"] = pd.to_numeric(cap.cantidad, errors="coerce").fillna(1)
    for k, v in cap.groupby("codigo_comuna").cantidad.sum().items():
        if cod(k) in C: C[cod(k)]["cap376"] = int(v)
    for k, v in cap[cap.anio >= 2019].groupby("codigo_comuna").cantidad.sum().items():
        if cod(k) in C: C[cod(k)]["cap376_19"] = int(v)

    cr = pd.read_csv("consolidado_cantidad_casos_criminalidad_en_comunas_por_anio.csv", dtype=str)
    cr["Cantidad_casos"] = pd.to_numeric(cr.Cantidad_casos, errors="coerce")
    for conducta, key in [("Extorsión", "extorsion"), ("Homicidio", "homicidio")]:
        sub = cr[cr.Conducta.str.contains(conducta, na=False)]
        y = sub.Fecha_hecho.max()
        for k, v in sub[sub.Fecha_hecho == y].groupby("Codigo_comuna").Cantidad_casos.sum().items():
            if cod(k) in C: C[cod(k)][key] = int(v); C[cod(k)][key + "_anio"] = y

    for k, c in C.items():
        p = c.get("poblacion") or 0
        if p: c["cap376_x1000"] = round(c.get("cap376_19", 0) / p * 1000, 2)

    for f in comunas:
        f["properties"] = {"k": cod(f["properties"]["comuna"]), **C[cod(f["properties"]["comuna"])]}
    json.dump({"type": "FeatureCollection", "features": comunas}, open("base.json", "w"),
              ensure_ascii=False, separators=(",", ":"))
    for k in sorted(C, key=lambda x: int(x)): print(k, C[k])
