# Fichas de conjuntos de datos (dataset cards)

Este directorio reune las fichas de descripcion de los conjuntos de datos del proyecto
**ChangeFormer_Gaza**, tanto las fuentes de entrada como el producto derivado. Cada ficha
sigue la plantilla de dataset card de Hugging Face y las recomendaciones de Gebru et al.
(2018, *Datasheets for Datasets*, arXiv:1803.09010).

Referencia de la plantilla: https://github.com/huggingface/huggingface_hub/tree/main/src/huggingface_hub/templates

---

## Sentinel-2 L2A de Gaza

Subconjunto de imagenes Sentinel-2 Nivel 2A (reflectancia de superficie) recortado al
area de interes de la Franja de Gaza en dos epocas, con bandas B02, B03, B04 y B08 a 10
metros. Es la entrada optica principal del modelo de deteccion de cambios.

- **Ficha completa:** [sentinel2_l2a_gaza.md](./sentinel2_l2a_gaza.md)
- **Autor de la ficha:** Jose David Penagos, Universidad Distrital Francisco Jose de Caldas
  (GitHub: [Penagos08](https://github.com/Penagos08)).

---

## Sentinel-1 GRD de Gaza

Subconjunto de imagenes Sentinel-1 GRD (SAR, banda C) con polarizaciones VV y VH, en dos
epocas, convertidas a decibelios. Aporta la capa de radar que atraviesa nubes y polvo,
complementaria a la optica.

- **Ficha completa:** [sentinel1_grd_gaza.md](./sentinel1_grd_gaza.md)
- **Autor de la ficha:** Jose David Penagos, Universidad Distrital Francisco Jose de Caldas
  (GitHub: [Penagos08](https://github.com/Penagos08)).

---

## Huellas de edificios de Gaza (OSM/HOTOSM)

Poligonos de edificios del area de Gaza extraidos de OpenStreetMap y HOTOSM, usados como
referencia pre-conflicto para contar cuantas estructuras quedaron afectadas.

- **Ficha completa:** [osm_buildings_gaza.md](./osm_buildings_gaza.md)
- **Autor de la ficha:** Jose David Penagos, Universidad Distrital Francisco Jose de Caldas
  (GitHub: [Penagos08](https://github.com/Penagos08)).

---

## UNOSAT Gaza Strip Comprehensive Damage Assessment

Evaluacion oficial de UNOSAT sobre dano y destruccion de estructuras en Gaza, con cuatro
categorias de dano. Se usa como conjunto de referencia para validar el cambio detectado.

- **Ficha completa:** [unosat_gaza_damage.md](./unosat_gaza_damage.md)
- **Autor de la ficha:** Jose David Penagos, Universidad Distrital Francisco Jose de Caldas
  (GitHub: [Penagos08](https://github.com/Penagos08)).

---

## xBD (xView2)

Conjunto de imagenes de muy alta resolucion con edificios anotados y cuatro niveles de
dano antes y despues de un desastre, usado para el ajuste fino del modelo. Licencia no
comercial.

- **Ficha completa:** [xbd_xview2.md](./xbd_xview2.md)
- **Autor de la ficha:** Jose David Penagos, Universidad Distrital Francisco Jose de Caldas
  (GitHub: [Penagos08](https://github.com/Penagos08)).

---

## Cambio y dano en Gaza (derivado)

Conjunto derivado que produce el pipeline: rasters de cambio y probabilidad, poligonos de
cambio, huellas de edificios afectados y metricas de validacion contra UNOSAT.

- **Ficha completa:** [gaza_change_detection.md](./gaza_change_detection.md)
- **Autor de la ficha:** Jose David Penagos, Universidad Distrital Francisco Jose de Caldas
  (GitHub: [Penagos08](https://github.com/Penagos08)).

---

Las fichas de los modelos estan en [`../model_cards/README.md`](../model_cards/README.md).
