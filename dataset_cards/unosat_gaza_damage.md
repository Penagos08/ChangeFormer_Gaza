---
# Metadatos segun la especificacion de dataset card de Hugging Face
language:
  - en
license: cc-by-sa-4.0
pretty_name: UNOSAT Gaza Strip Comprehensive Damage Assessment
tags:
  - geospatial
  - humanitarian
  - building-damage
  - reference
  - gaza
task_categories:
  - other
size_categories:
  - 100K<n<1M
configs:
  - config_name: default
    data_files: unosat_gaza_damage.gdb
---

# Ficha de conjunto de datos: UNOSAT Gaza Strip Comprehensive Damage Assessment

<!-- Resumen rapido del conjunto de datos -->

Evaluacion oficial de dano y destruccion de estructuras en la Franja de Gaza elaborada
por UNOSAT a partir de imagenes satelitales de muy alta resolucion. Se usa como conjunto
de referencia (ground truth) para validar el cambio detectado por el modelo.

## Detalles del conjunto de datos

### Descripcion

Base de datos geografica (File Geodatabase) con puntos o poligonos de daño clasificados
en cuatro categorias: destruido, severamente dañado, moderadamente dañado y posiblemente
dañado. La evaluacion compara imagenes recientes contra una linea base de mayo de 2023 y
revisiones intermedias. En la edicion de abril de 2025 (producto UNOSAT 4130, publicado
el 7 de mayo de 2025) se identificaron 70,436 estructuras destruidas, 18,588 severamente
dañadas, 51,962 moderadamente dañadas y 33,500 posiblemente dañadas, para un total de
174,486 estructuras (cerca del 70 % de las estructuras de la Franja) y 258,201 unidades
habitacionales dañadas.

- **Curado por:** United Nations Satellite Centre (UNOSAT, UNITAR).
- **Financiado por [opcional]:** [Informacion adicional necesaria]
- **Compartido por [opcional]:** UNOSAT / HDX (OCHA).
- **Idioma(s) (PLN):** No aplica.
- **Licencia:** Creative Commons Attribution Share-Alike (CC BY-SA).

### Fuentes del conjunto de datos [opcional]

- **Repositorio:** https://unosat.org/products/4130 y https://data.humdata.org
- **Articulo [opcional]:** Ver documentacion de UNOSAT y el trabajo de Scher y Van Den Hoek
  (2025), arXiv:2506.14730, que valida contra UNOSAT.
- **Demo [opcional]:** `src/data/unosat.py`

## Usos

### Uso directo

Referencia para calcular recall y precision espacial del modelo de deteccion de cambio, y
para consultas humanitarias sobre dano a estructuras.

### Usos fuera de alcance

No usar como base legal ni como censo catastral. No es una validacion en terreno; es
interpretacion de imagenes.

## Estructura del conjunto de datos

File Geodatabase con capa(s) de daño; cada registro incluye una categoria de daño
(destruido, severo, moderado, posible) y geometria. En este proyecto se convierte a GeoJSON
(`data/external/unosat/unosat_gaza_damage.geojson`) y se reproyecta a EPSG:32636.

## Creacion del conjunto de datos

### Justificacion de la curaduria

Se necesita una referencia independiente y reconocida internacionalmente para evaluar la
calidad del modelo en Gaza.

### Datos de origen

#### Recoleccion y procesamiento

Analisis visual de imagenes de muy alta resolucion comparando epocas; los cambios se
documentan manualmente en datos vectoriales por analistas. Descarga manual desde HDX (se
aceptan terminos), seguida de conversion y reproyeccion en `src/data/unosat.py`.

#### Quienes producen los datos de origen

Analistas de UNOSAT (UNITAR) con imagenes satelitales comerciales.

### Anotaciones [opcional]

#### Proceso de anotacion

Interpretacion visual por analistas; clasificacion en cuatro niveles de daño.

#### Informacion personal y sensible

Ubica infraestructura dañada en una zona de conflicto. Su uso debe ser humanitario y
respetuoso de los principios de proteccion.

## Sesgos, riesgos y limitaciones

- Evaluacion preliminar no validada en terreno; puede subestimar el daño visible.
- Solo se detecta daño significativo a la integridad estructural; el daño menor puede no verse.
- Depende de la calidad e iluminacion de las imagenes fuente.
- Sirve como referencia aproximada, no como verdad absoluta pixel a pixel.

### Recomendaciones

Usar una tolerancia espacial al comparar (por ejemplo 20 m) y reportar las limitaciones
junto con las metricas.

## Citacion [opcional]

**APA:**

UNOSAT. (2025). *Gaza Strip Comprehensive Damage Assessment* [Producto 4130]. United
Nations Satellite Centre (UNITAR). https://unosat.org/products/4130

## Glosario [opcional]

- **GDB:** File Geodatabase de Esri.
- **Recall / precision:** proporciones de dano cubierto por el modelo y de detecciones
  confirmadas por la referencia.

## Autores de la ficha [opcional]

Jose David Penagos, Universidad Distrital Francisco Jose de Caldas.

## Contacto de la ficha

GitHub: [Penagos08](https://github.com/Penagos08)
