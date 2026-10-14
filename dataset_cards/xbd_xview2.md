---
# Metadatos segun la especificacion de dataset card de Hugging Face
language:
  - en
license: cc-by-nc-sa-4.0
pretty_name: xBD (xView2) - Building Damage Assessment
tags:
  - geospatial
  - remote-sensing
  - building-damage
  - disaster-response
  - change-detection
task_categories:
  - image-segmentation
size_categories:
  - 10K<n<100K
configs:
  - config_name: default
    data_files: ""
---

# Ficha de conjunto de datos: xBD (xView2)

<!-- Resumen rapido del conjunto de datos -->

xBD es un conjunto de imagenes satelitales de muy alta resolucion con anotaciones de
edificios y niveles de dano antes y despues de un desastre. Se usa en este proyecto como
datos de ajuste fino del modelo ChangeFormer_Gaza. Requiere registro y aceptacion de
terminos para su descarga.

## Detalles del conjunto de datos

### Descripcion

xBD contiene pares de imagenes antes/despues junto con poligonos de edificios y una
categoria de dano por edificio: 1 (sin dano), 2 (dano menor), 3 (dano mayor) y 4
(destruido), ademas de fondo (0). Cubre seis tipos de desastre natural en quince paises.
La descripcion oficial reporta 850,736 edificios, 45,361 km2 de superficie y 22,068
imagenes de 1024x1024 pixeles. En este proyecto las clases 2, 3 y 4 se agrupan en una
unica clase binaria de cambio.

- **Curado por:** Defense Innovation Unit (DIU) y colaboradores HADR.
- **Financiado por [opcional]:** [Informacion adicional necesaria]
- **Compartido por [opcional]:** xView2 challenge.
- **Idioma(s) (PLN):** No aplica.
- **Licencia:** CC BY-NC-SA 4.0 (no comercial, share-alike).

### Fuentes del conjunto de datos [opcional]

- **Repositorio:** https://xview2.org/dataset
- **Articulo:** Gupta, R., Goodman, B., Patel, N., Hosfelt, R., Sajeev, S., Heim, E.,
  Doshi, J., Lucas, K., Choset, H. y Gaston, M. (2019). *Creating xBD: A Dataset for
  Assessing Building Damage from Satellite Imagery*. CVPR Workshops. arXiv:1911.09296
- **Demo [opcional]:** `notebooks/02_changeformer_gaza.ipynb`

## Usos

### Uso directo

Ajuste fino supervisado de modelos de deteccion de cambio y evaluacion de localizacion y
dano a edificios.

### Usos fuera de alcance

Uso comercial (prohibido por la licencia). No usar como referencia catastral ni para
geolocalizar personas.

## Estructura del conjunto de datos

Estructura esperada en este proyecto: `data/external/xbd/{train,val}/images/*.png` con
pares `*_pre_disaster.png` y `*_post_disaster.png`, y etiquetas en `labels/`. Las etiquetas
usan la codificacion de cinco clases descrita arriba.

## Creacion del conjunto de datos

### Justificacion de la curaduria

xBD es el conjunto de referencia mas amplio y reconocido para evaluacion de dano a
edificios con imagenes antes/despues, lo que permite transferir aprendizaje al caso de Gaza.

### Datos de origen

#### Recoleccion y procesamiento

Imagenes de muy alta resolucion del Maxar Open Data Program, anotadas por analistas
expertos; los poligonos y las categorias de dano se revisaron para consistencia.
En este proyecto se redimensionan a 256x256 y se binarizan las etiquetas.

#### Quienes producen los datos de origen

Analistas expertos contratados por el proyecto xView2, sobre imagenes de Maxar.

### Anotaciones [opcional]

#### Proceso de anotacion

Localizacion de edificios y asignacion de nivel de dano por analistas, con enfasis en
cambios sobre el terreno entre las imagenes antes y despues.

#### Informacion personal y sensible

Las imagenes pueden mostrar zonas afectadas; no contiene datos personales directos.

## Sesgos, riesgos y limitaciones

- Dominio de desastres naturales (no conflicto armado), lo que limita la transferencia a Gaza.
- Alta resolucion (~0.3-0.5 m) distinta de Sentinel-2 (10 m).
- Concentracion geografica y tipologias constructivas distintas de las de Gaza.
- Licencia no comercial.

### Recomendaciones

Evaluar la transferencia entre dominios y considerar reentrenamiento o adaptacion de
dominio. Respetar la licencia no comercial.

## Citacion [opcional]

**BibTeX:**

```bibtex
@inproceedings{gupta2019xbd,
  title={Creating xBD: A Dataset for Assessing Building Damage from Satellite Imagery},
  author={Gupta, Ritwik and Goodman, Bryce and Patel, Nirav and Hosfelt, Ricky and Sajeev, Sandra and Heim, Eric and Doshi, Jigar and Lucas, Keane and Choset, Howie and Gaston, Matthew},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops},
  pages={10--17},
  year={2019}
}
```

**APA:**

Gupta, R. et al. (2019). *Creating xBD: A Dataset for Assessing Building Damage from
Satellite Imagery*. CVPR Workshops. arXiv:1911.09296

## Glosario [opcional]

- **HADR:** Humanitarian Assistance and Disaster Recovery.
- **Share-alike:** clausula que obliga a licenciar los derivados bajo la misma licencia.

## Autores de la ficha [opcional]

Jose David Penagos, Universidad Distrital Francisco Jose de Caldas.

## Contacto de la ficha

GitHub: [Penagos08](https://github.com/Penagos08)
