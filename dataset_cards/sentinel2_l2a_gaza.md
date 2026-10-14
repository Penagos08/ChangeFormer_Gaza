---
# Metadatos segun la especificacion de dataset card de Hugging Face
language:
  - en
license: cc-by-sa-3.0-igo
pretty_name: Sentinel-2 L2A de Gaza (ChangeFormer_Gaza)
tags:
  - geospatial
  - remote-sensing
  - sentinel-2
  - multispectral
  - change-detection
  - earth-observation
task_categories:
  - image-segmentation
size_categories:
  - n<1K
configs:
  - config_name: default
    data_files: gaza_s2_pre.tif
---

# Ficha de conjunto de datos: Sentinel-2 L2A de Gaza

<!-- Resumen rapido del conjunto de datos -->

Subconjunto de imagenes Sentinel-2 Nivel 2A (reflectancia de superficie) recortado al
area de interes de la Franja de Gaza, en dos epocas (antes y despues del conflicto),
usado como entrada optica del modelo ChangeFormer_Gaza.

## Detalles del conjunto de datos

### Descripcion

El conjunto consiste en dos mosaicos georreferenciados (uno "antes" y uno "despues") de
las bandas B02 (azul), B03 (verde), B04 (rojo) y B08 (infrarrojo cercano), a 10 metros de
resolucion, reproyectados a UTM zona 36N (EPSG:32636). Cada mosaico se compone combinando
varias escenas de la misma epoca mediante la mediana temporal, con el fin de reducir nubes
y sombras. El area de interes es la Franja de Gaza (bbox 34.20-34.60 E, 31.20-31.60 N).

- **Curado por:** Jose David Penagos, Universidad Distrital Francisco Jose de Caldas, a partir de datos de ESA.
- **Financiado por [opcional]:** [Informacion adicional necesaria]
- **Compartido por [opcional]:** Microsoft Planetary Computer (acceso a los datos originales)
- **Idioma(s) (PLN):** No aplica.
- **Licencia:** Datos Copernicus Sentinel, de acceso libre y abierto (terminos de datos de
  Copernicus / CC BY-SA 3.0 IGO).

### Fuentes del conjunto de datos [opcional]

- **Repositorio:** https://planetarycomputer.microsoft.com/ (coleccion `sentinel-2-l2a`)
- **Articulo [opcional]:** Drusch, M. et al. (2012). Sentinel-2: ESA's Optical
  High-Resolution Mission for GMES Operational Services. Remote Sensing of Environment.
- **Demo [opcional]:** `notebooks/01_exploracion.ipynb`

## Usos

### Uso directo

Entrada optica para deteccion de cambios con modelos siameses. Analisis multiespectral
basico (indices de vegetacion, agua, construccion) sobre Gaza.

### Usos fuera de alcance

No sirve para identificar personas, vehiculos o actividades. La resolucion de 10 metros
impide el analisis a nivel de edificio individual sin apoyo de otras fuentes.

## Estructura del conjunto de datos

Cada mosaico es un GeoTIFF de 4 bandas (B02, B03, B04, B08), en uint16 (reflectancia
escalada), con perfil geografico en EPSG:32636. Archivos de salida:
`data/raw/sentinel2/gaza_s2_pre.tif` y `data/raw/sentinel2/gaza_s2_post.tif`.

## Creacion del conjunto de datos

### Justificacion de la curaduria

Se necesita una base optica libre, sin credenciales y reproducible para alimentar el
modelo de deteccion de cambios en una zona con acceso restringido.

### Datos de origen

#### Recoleccion y procesamiento

Busqueda en el catalogo STAC de Microsoft Planetary Computer, filtrado por
`eo:cloud_cover < 15`, recorte al bbox, reproyeccion a EPSG:32636, remuestreo a 10 m y
agregacion temporal por mediana (`src/data/download_sentinel2.py`).

#### Quienes producen los datos de origen

Agencia Espacial Europea (ESA) dentro del programa Copernicus.

### Anotaciones [opcional]

No aplica; las etiquetas de cambio se generan en la ficha
`gaza_change_detection.md`.

#### Informacion personal y sensible

El conjunto contiene imagenes satelitales de una zona poblada en conflicto. Aunque no
incluye datos personales directos, puede revelar informacion sobre infraestructura y
asentamientos; su uso debe ser responsable.

## Sesgos, riesgos y limitaciones

- Nubosidad y sombras frecuentes en la region reducen la disponibilidad de pixeles validos.
- La mediana temporal puede suavizar cambios finos.
- La resolucion de 10 m es insuficiente para dano estructural detallado.
- La reflectancia de superficie puede variar por aerosoles y polvo.

### Recomendaciones

Verificar la proporcion de pixeles validos por tesela y complementar con SAR
(`sentinel1_grd_gaza.md`) cuando la cobertura optica sea pobre.

## Citacion [opcional]

**APA:**

ESA. (2015-). *Copernicus Sentinel-2 (procesado L2A)*. Programa Copernicus, Unión Europea.

## Glosario [opcional]

- **L2A:** producto de reflectancia de superficie corregido atmosféricamente.
- **STAC:** SpatioTemporal Asset Catalog.
- **Mediana temporal:** agregacion pixel a pixel del valor medio de una serie temporal.

## Autores de la ficha [opcional]

Jose David Penagos, Universidad Distrital Francisco Jose de Caldas.

## Contacto de la ficha

GitHub: [Penagos08](https://github.com/Penagos08)
