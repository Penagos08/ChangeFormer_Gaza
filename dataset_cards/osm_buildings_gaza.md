---
# Metadatos segun la especificacion de dataset card de Hugging Face
language:
  - en
license: odbl-1.0
pretty_name: Huellas de edificios de Gaza (OSM/HOTOSM)
tags:
  - geospatial
  - openstreetmap
  - buildings
  - footprints
  - vector
task_categories:
  - other
size_categories:
  - 10K<n<100K
configs:
  - config_name: default
    data_files: gaza_buildings.geojson
---

# Ficha de conjunto de datos: Huellas de edificios de Gaza

<!-- Resumen rapido del conjunto de datos -->

Poligonos de edificios del area de la Franja de Gaza extraidos de OpenStreetMap y del
equipo humanitario HOTOSM, usados como referencia pre-conflicto para cuantificar cuantas
estructuras quedaron afectadas por el cambio detectado.

## Detalles del conjunto de datos

### Descripcion

Conjunto vectorial de huellas de edificios (geometrias tipo Polygon o MultiPolygon)
dentro del bbox de Gaza. Se descarga con OSMnx filtrando la etiqueta `building=True`, y
se usa como capa base sobre la que se interseca el mapa de cambio para estimar la
proporcion de edificios afectados.

- **Curado por:** Comunidad OpenStreetMap y HOTOSM; extraccion para este proyecto por
  Jose David Penagos, Universidad Distrital Francisco Jose de Caldas.
- **Financiado por [opcional]:** [Informacion adicional necesaria]
- **Compartido por [opcional]:** OpenStreetMap / HOTOSM
- **Idioma(s) (PLN):** No aplica.
- **Licencia:** Open Database License (ODbL) 1.0, atribucion a OpenStreetMap contributors.

### Fuentes del conjunto de datos [opcional]

- **Repositorio:** https://www.openstreetmap.org/ y https://www.hotosm.org/
- **Articulo [opcional]:** Boeing, G. (2017). OSMnx: New Methods for Acquiring,
  Constructing, Analyzing, and Visualizing Complex Street Networks. Computers, Environment
  and Urban Systems.
- **Demo [opcional]:** `src/data/footprints.py`

## Usos

### Uso directo

Conteo y localizacion de estructuras, cruce espacial con poligonos de cambio y estimacion
de edificios afectados.

### Usos fuera de alcance

No es un censo catastral ni una fuente oficial de limites prediales. La calidad y
cobertura varian segun el mapeo voluntario y pueden estar incompletas en zonas de conflicto.

## Estructura del conjunto de datos

Archivo GeoJSON (`data/raw/footprints/gaza_buildings.geojson`) con columnas provenientes
de OSM, entre ellas `geometry`. Se reproyecta a EPSG:32636 antes del analisis.

## Creacion del conjunto de datos

### Justificacion de la curaduria

Se requiere una referencia de edificios previa al conflicto para atribuir el cambio
detectado a estructuras concretas.

### Datos de origen

#### Recoleccion y procesamiento

Descarga desde la API de Overpass mediante OSMnx (compatible con versiones 1.x y 2.x),
filtrado de geometrias poligonales, exportacion a GeoJSON (`src/data/footprints.py`).

#### Quienes producen los datos de origen

Mapeadores voluntarios de OpenStreetMap, incluidos equipos humanitarios de HOTOSM que
cartografiaron Gaza.

### Anotaciones [opcional]

No aplica.

#### Informacion personal y sensible

No contiene datos personales. Ubica infraestructura; su difusion debe considerar el
contexto humanitario.

## Sesgos, riesgos y limitaciones

- Cobertura y precision heterogeneas; trazados aproximados.
- Puede no reflejar cambios recientes del entorno construido.
- Licencia ODbL: los productos derivados pueden quedar sujetos a share-alike.

### Recomendaciones

Documentar la fecha de descarga, verificar completitud y considerar fuentes catastrales
o humanitarias complementarias.

## Citacion [opcional]

**APA:**

OpenStreetMap contributors. (2026). *OpenStreetMap* [Base de datos]. https://www.openstreetmap.org

## Glosario [opcional]

- **Huella:** contorno poligonal de un edificio.
- **ODbL:** licencia de base de datos abierta con clausula share-alike.
- **OSMnx:** libreria para descargar y analizar datos de OSM.

## Autores de la ficha [opcional]

Jose David Penagos, Universidad Distrital Francisco Jose de Caldas.

## Contacto de la ficha

GitHub: [Penagos08](https://github.com/Penagos08)
