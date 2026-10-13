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

## Cómo se construye y se publica
1. Editá las fuentes en `fuentes/` (la landing, noticias y nosotros se editan directo en `sitio/`).
2. `python fuentes/construir.py` regenera todas las páginas desde sus fuentes.
3. `python fuentes/verificar.py` revisa la sintaxis de cada script, los enlaces internos y que no se haya colado ninguna clave.
4. Subí los cambios a `main`: Vercel publica solo (carpeta raíz `sitio`).

## Motor de fuentes (fx.js)
- Cada fuente tiene tipo (administrativa, judicial, académica, prensa, audiovisual, testimonial, blog, redes) y solidez.
- Solo se cruza lo que tiene llave común: lugar, periodo y tema. Una fuente con llave parcial da contexto, no triangula.
- Independencia: si un medio repite a una entidad ("Procuraduría (vía El Tiempo)"), cuenta como una sola fuente.
- Las diferencias se nombran por tipo: contradicción, brecha, cobertura, tiempo, subregistro y vacío de información. Solo la contradicción y la brecha se presentan como hallazgo.

## Cruces estadísticos (conclu.js)
Correlación de Spearman con prueba de permutación (2.000 barajadas, semilla fija), mostrando el número de comunas de cada cruce. Correlación no es causa, y habla de comunas, no de personas.
