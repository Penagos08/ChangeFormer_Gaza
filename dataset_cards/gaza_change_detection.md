---
# Metadatos segun la especificacion de dataset card de Hugging Face
language:
  - en
license: other
pretty_name: Cambio y dano en Gaza (ChangeFormer_Gaza)
tags:
  - geospatial
  - remote-sensing
  - change-detection
  - building-damage
  - gaza
  - derived
task_categories:
  - image-segmentation
size_categories:
  - n<1K
configs:
  - config_name: default
    data_files: cambio_gaza.tif
---

# Ficha de conjunto de datos: Cambio y dano en Gaza (derivado)

<!-- Resumen rapido del conjunto de datos -->

Conjunto derivado que produce el pipeline de ChangeFormer_Gaza: rasters y vectores de
cambio sobre la Franja de Gaza, mas las huellas de edificios afectados y las metricas de
validacion contra UNOSAT.

## Detalles del conjunto de datos

### Descripcion

Es el resultado integrado del proyecto. Contiene: (1) el raster binario de cambio y su
mapa de probabilidad; (2) los poligonos de cambio vectorizados; (3) las huellas de
edificios intersectadas con el cambio; y (4) las metricas de validacion espacial frente a
UNOSAT. La deteccion proviene del modelo documentado en `model_cards/changeformer_gaza.md`,
aplicado sobre el par Sentinel-2 antes/despues.

- **Curado por:** Jose David Penagos, Universidad Distrital Francisco Jose de Caldas.
- **Financiado por [opcional]:** [Informacion adicional necesaria]
- **Compartido por [opcional]:** [Informacion adicional necesaria]
- **Idioma(s) (PLN):** No aplica.
- **Licencia:** Obra derivada; combina datos Copernicus (CC BY-SA 3.0 IGO) y OpenStreetMap
  (ODbL 1.0). Se recomienda compartir bajo CC BY-SA 4.0 con la debida atribucion. Los pesos
  derivados de xBD quedan sujetos a CC BY-NC-SA 4.0.

### Fuentes del conjunto de datos [opcional]

- **Repositorio:** https://github.com/Penagos08/ChangeFormer_Gaza
- **Articulo [opcional]:** Scher, C. y Van Den Hoek, J. (2025). arXiv:2506.14730
- **Demo [opcional]:** `notebooks/02_changeformer_gaza.ipynb`

## Usos

### Uso directo

Analisis humanitario y academico del dano al entorno construido en Gaza; base para mapas
y tableros; insumo para estimaciones por gobernacion.

### Usos fuera de alcance

No usar como evidencia legal, censo, ni para decisiones sobre personas. No es una
validacion en terreno.

## Estructura del conjunto de datos

- `outputs/rasters/cambio_gaza.tif`: mascara binaria (uint8, 0/1) georreferenciada.
- `outputs/rasters/cambio_gaza_prob.tif`: probabilidad de cambio (float32).
- `outputs/vectors/cambio_gaza.geojson`: poligonos de cambio.
- `outputs/vectors/edificios_afectados.geojson`: huellas intersectadas con `cobertura_cambio`.
- `reports/edificios_resumen.json` y `reports/metricas_unosat.md`: resumenes y metricas.

## Creacion del conjunto de datos

### Justificacion de la curaduria

Ofrecer un producto abierto, reproducible y auditable del cambio/dano en Gaza usando
unicamente imagenes libres.

### Datos de origen

#### Recoleccion y procesamiento

Pipeline `scripts/run_pipeline.ps1`: descarga Sentinel-2 y Sentinel-1, descarga huellas OSM,
inferencia por teselas, vectorizacion, cruce con edificios y validacion con UNOSAT
(`src/`).

#### Quienes producen los datos de origen

Derivado por este proyecto a partir de datos de ESA (Copernicus), OpenStreetMap/HOTOSM y UNOSAT.

### Anotaciones [opcional]

Las "etiquetas" son la salida del modelo mas el cruce con huellas; la referencia de
validacion es UNOSAT (`unosat_gaza_damage.md`).

#### Informacion personal y sensible

Ubica infraestructura dañada en una zona de conflicto; su difusion debe ser responsable.

## Sesgos, riesgos y limitaciones

- Hereda las limitaciones del modelo y de las fuentes de entrada.
- Error de transferencia por la diferencia de resolucion entre xBD y Sentinel-2.
- Resultados preliminares, no validados en campo.
- Mezcla de licencias: revisar condiciones antes de reutilizar.

### Recomendaciones

Acompanar los mapas con las metricas de validacion y las advertencias de incertidumbre.

## Citacion [opcional]

**APA:**

Penagos, J. D. (2026). *Cambio y dano en Gaza (ChangeFormer_Gaza)* [Conjunto de datos
derivado]. Universidad Distrital Francisco Jose de Caldas.

## Glosario [opcional]

- **Cobertura de cambio:** fraccion del area de un edificio solapada por el cambio detectado.
- **Vectorizacion:** conversion de una mascara raster en poligonos.

## Autores de la ficha [opcional]

Jose David Penagos, Universidad Distrital Francisco Jose de Caldas.

## Contacto de la ficha

GitHub: [Penagos08](https://github.com/Penagos08)
