# Observa Rigor

Observatorio de la ineficacia normativa: mide la distancia entre lo que la norma promete y lo que pasa, con fuentes públicas cruzadas.

## Estructura
- `sitio/` — la página publicada en Vercel (raíz del proyecto en Vercel: `sitio`).
  - `index.html` landing · `medellin/` mapa 3D · `contratacion/` Rigor Contratación · `datos/` Rigor Datos · `noticias/` · `cumplimiento/` Hallazgos graves · `nosotros/`
  - `api/noticias.js` y `api/contratos.js` — funciones en vivo (Google Noticias y SECOP II).
- `fuentes/` — scripts y datos que arman el sitio.
  - Contratación: `bajar.py` → `contratos.json` (no se sube por tamaño; se regenera), `bajar2.py`, `bajar3.py`, `analizar2.py`, `cruces.py`.
  - Medellín: `live_med.html` + `analisis.js` + `conclu.js` + `fx/fx.js` + `fx/pilotos.js` + `fx/nav.js` → `mkmed.py`.
  - Rigor Datos y Cumplimiento: `fx/datos.html`, `fx/cumplimiento.html`.

## Reglas del método
Cada dato con su fuente y su tipo; solo se cruza lo que tiene llave común (lugar, periodo, tema); las conclusiones se redactan como deberes, no como causas; "alerta de riesgo", nunca "corrupción"; personas naturales ocultas.
