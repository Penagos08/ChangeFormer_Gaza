---
# Metadatos segun la especificacion de dataset card de Hugging Face
language:
  - en
license: cc-by-sa-3.0-igo
pretty_name: Sentinel-1 GRD de Gaza (ChangeFormer_Gaza)
tags:
  - geospatial
  - remote-sensing
  - sentinel-1
  - sar
  - change-detection
  - earth-observation
task_categories:
  - image-segmentation
size_categories:
  - n<1K
configs:
  - config_name: default
    data_files: gaza_s1_pre.tif
---

# Ficha de conjunto de datos: Sentinel-1 GRD de Gaza

<!-- Resumen rapido del conjunto de datos -->

Subconjunto de imagenes Sentinel-1 GRD (radar de apertura sintetica, banda C) recortado
al area de interes de la Franja de Gaza, en dos epocas, usado como capa SAR complementaria
del modelo.

## Detalles del conjunto de datos

### Descripcion

Dos mosaicos SAR (antes y despues) con las polarizaciones VV y VH, a 10 metros,
reproyectados a EPSG:32636 y convertidos a decibelios (10*log10). El SAR atraviesa nubes
y polvo y es sensible a cambios en la estructura y la rugosidad de la superficie, por lo
que complementa a la capa optica cuando la nubosidad impide el uso de Sentinel-2.

- **Curado por:** Jose David Penagos, Universidad Distrital Francisco Jose de Caldas, a partir de datos de ESA.
- **Financiado por [opcional]:** [Informacion adicional necesaria]
- **Compartido por [opcional]:** Microsoft Planetary Computer
- **Idioma(s) (PLN):** No aplica.
- **Licencia:** Datos Copernicus Sentinel (terminos de datos de Copernicus / CC BY-SA 3.0 IGO).

### Fuentes del conjunto de datos [opcional]

- **Repositorio:** https://planetarycomputer.microsoft.com/ (coleccion `sentinel-1-grd`)
- **Articulo [opcional]:** Torres, R. et al. (2012). GMES Sentinel-1 mission. Remote Sensing of Environment.
- **Demo [opcional]:** `notebooks/01_exploracion.ipynb`

## Usos

### Uso directo

Capa de apoyo para deteccion de cambios en condiciones de nubosidad, y analisis de
retrodispersion (backscatter) sobre el entorno construido. Antecedente metodologico:
Scher y Van Den Hoek (2025) usaron InSAR de Sentinel-1 para monitorear dano en Gaza.

### Usos fuera de alcance

No reemplaza interpretacion optica de alta resolucion para severidad de dano. La
deteccion automatica de cambios estructurales finos exige co-registro cuidadoso.

## Estructura del conjunto de datos

GeoTIFF de 2 bandas (VV, VH) en float32 con valores en dB, perfil en EPSG:32636.
Archivos: `data/raw/sentinel1/gaza_s1_pre.tif` y `data/raw/sentinel1/gaza_s1_post.tif`.

## Creacion del conjunto de datos

### Justificacion de la curaduria

Aportar una fuente de observacion de la Tierra independiente del clima y sensible a la
estructura, esencial en una region con alta nubosidad.

### Datos de origen

#### Recoleccion y procesamiento

Busqueda en el catalogo STAC, filtrado por direccion orbital (descendente), recorte,
reproyeccion y agregacion temporal por mediana, seguida de conversion a dB
(`src/data/download_sentinel1.py`).

#### Quienes producen los datos de origen

Agencia Espacial Europea (ESA), programa Copernicus.

### Anotaciones [opcional]

No aplica.

#### Informacion personal y sensible

Imagenes de una zona poblada en conflicto; mismo tratamiento responsable que la capa optica.

## Sesgos, riesgos y limitaciones

- El SAR presenta ruido tipo moteado (speckle) y distorsiones geometricas (layover, sombra)
  que dificultan la interpretacion.
- La retrodispersion depende de la orientacion y la humedad, no solo de la presencia de edificios.
- La comparacion bitemporal exige geometria orbital consistente.

### Recomendaciones

Filtrar el moteado y verificar consistencia orbital antes de comparar. Combinar con
Sentinel-2 para interpretar los cambios.

## Citacion [opcional]

**APA:**

ESA. (2014-). *Copernicus Sentinel-1 (GRD)*. Programa Copernicus, Unión Europea.

## Glosario [opcional]

- **GRD:** Ground Range Detected, producto SAR detectado y proyectado a rango-terreno.
- **VV / VH:** polarizaciones vertical-vertical y vertical-horizontal.
- **dB:** escala logaritmica de retrodispersion.

## Autores de la ficha [opcional]

Jose David Penagos, Universidad Distrital Francisco Jose de Caldas.

## Contacto de la ficha

GitHub: [Penagos08](https://github.com/Penagos08)
