---
# Metadatos segun la especificacion de model card de Hugging Face
language:
  - en
license: mit
library_name: pytorch
pipeline_tag: image-segmentation
tags:
  - change-detection
  - remote-sensing
  - earth-observation
  - building-damage
  - humanitarian
  - gaza
datasets:
  - xbd
metrics:
  - iou
  - f1
base_model: wgcban/ChangeFormer
---

# Ficha de modelo: ChangeFormer_Gaza

<!-- Resumen rapido del modelo -->

ChangeFormer_Gaza es la version ajustada (fine-tuned) del modelo ChangeFormerV6 para
la deteccion de cambio asociado a edificios destruidos en la Franja de Gaza. Parte de
los pesos de ChangeFormerV6 (LEVIR-CD) y se especializa con el dataset xBD (xView2) de
dano a edificios.

## Detalles del modelo

### Descripcion del modelo

Sobre la arquitectura siamesa transformer de ChangeFormerV6 se reemplaza la cabeza de
clasificacion binaria por una salida de dos clases (sin dano / dano severo). El ajuste
fino usa xBD, que etiqueta cada edificio con cinco categorias de dano (fondo, sin dano,
dano menor, dano mayor, destruido); para la tarea binaria las clases de dano menor, mayor
y destruido se agrupan en una sola clase de cambio. En este proyecto el modelo se entrena
en la nube (por ejemplo Google Colab) por la limitacion de la GPU local, y luego se
aplica sobre pares Sentinel-2 (antes/despues) de Gaza.

- **Desarrollado por:** Jose David Penagos, Universidad Distrital Francisco Jose de Caldas,
  a partir del modelo base de Bandara y Patel.
- **Financiado por [opcional]:** [Informacion adicional necesaria]
- **Compartido por [opcional]:** [Informacion adicional necesaria]
- **Tipo de modelo:** Red siamesa transformer ajustada para deteccion binaria de dano.
- **Idioma(s) (PLN):** No aplica.
- **Licencia:** MIT para el codigo; el uso de xBD impone la clausula no comercial
  CC BY-NC-SA 4.0 (ver limitaciones).
- **Ajustado a partir de [opcional]:** ChangeFormerV6 (LEVIR-CD), ver `changeformer_v6.md`.

### Fuentes del modelo [opcional]

- **Repositorio:** https://github.com/Penagos08/ChangeFormer_Gaza
- **Articulo [opcional]:** Bandara, W. G. C. y Patel, V. M. (2022). arXiv:2201.01293;
  xBD: Gupta, R. et al. (2019). CVPRW. arXiv:1911.09296
- **Demo [opcional]:** `notebooks/02_changeformer_gaza.ipynb`

## Usos

### Uso directo

Generar mapas binarios de cambio/dano sobre pares de imagenes Sentinel-2 de la Franja de
Gaza, tesela a tesela, con solape, para despues vectorizar y cruzar con huellas de edificios.

### Uso posterior [opcional]

Integracion en tableros de evaluacion de dano, estimacion de edificios afectados por
gobernacion y comparacion con evaluaciones internacionales (UNOSAT).

### Usos fuera de alcance

No determinar responsabilidades, identificar personas ni cuantificar victimas. No usar
como prueba legal sin verificacion en campo. No extrapolar a otras regiones o resoluciones
sin reentrenamiento y validacion.

## Sesgos, riesgos y limitaciones

- xBD proviene de imagenes comerciales de muy alta resolucion (~0.3-0.5 m) de Maxar,
  mientras que la inferencia en Gaza usa Sentinel-2 (10 m): la diferencia de resolucion
  es la principal fuente de error de transferencia.
- xBD es no comercial (CC BY-NC-SA 4.0), lo que restringe el uso comercial del modelo derivado.
- Los desastres de xBD incluyen huracanes, incendios, inundaciones, terremotos, tsunamis
  y explosion; los patrones de dano de conflicto armado difieren de los desastres naturales.
- El modelo hereda los sesgos del modelo base y no modela la severidad del dano.

### Recomendaciones

Declarar la incertidumbre y la resolucion de las imagenes de entrada. Acompanar cada mapa
con las metricas de validacion frente a UNOSAT. No usar los resultados como evidencia
oficial.

## Como empezar con el modelo

```bash
# Ajuste fino (idealmente en GPU en la nube)
python -m src.train.finetune_xbd --config configs/gaza.yaml \
    --dataset-root data/external/xbd --epochs 50
```

```python
from src.models.changeformer_wrapper import ChangeFormerWrapper

modelo = ChangeFormerWrapper(
    checkpoint="checkpoints/ChangeFormer_xBD/best_ckpt.pt",
    embed_dim=256,
    n_class=2,
    device="auto",
)
```

## Detalles de entrenamiento

### Datos de entrenamiento

xBD (xView2): 850,736 edificios, 45,361 km2, 6 tipos de desastre, 15 paises,
22,068 imagenes de 1024x1024. Ver `dataset_cards/xbd_xview2.md`.

### Procedimiento de entrenamiento

#### Preprocesamiento [opcional]

Pares antes/despues redimensionados a 256x256; etiquetas remuestreadas con vecino mas
cercano; binarizacion de clases {dano menor, mayor, destruido} a la clase 1;
normalizacion con media y desviacion 0.5.

#### Hiperparametros de entrenamiento

- **Regimen de entrenamiento:** fp32, AdamW, tasa de aprendizaje 1e-4, decaimiento de
  peso 1e-4, tamano de lote 8, 50 epocas. Perdida de entropia cruzada con peso de clase
  [1.0, 6.0] mas una componente Dice.

#### Velocidades, tamanos y tiempos [opcional]

[Informacion adicional necesaria] (depende del hardware de nube empleado).

## Evaluacion

### Datos, factores y metricas de prueba

#### Datos de prueba

Conjunto de validacion de xBD y, para Gaza, el cruce espacial con las etiquetas de dano
de UNOSAT (`dataset_cards/unosat_gaza_damage.md`).

#### Factores

Tipo de desastre del conjunto de prueba; resolucion de la imagen; densidad de edificios;
presencia de nubes.

#### Metricas

IoU, F1, precision y recall para la clase de cambio; recall espacial frente a UNOSAT y
tolerancia en metros.

### Resultados

[Informacion adicional necesaria] hasta ejecutar el ajuste fino y la validacion.

#### Resumen

Se reporta el mejor checkpoint segun F1 de validacion al final del entrenamiento.

## Consideraciones eticas

El modelo se aplica sobre un contexto de conflicto. Su uso debe ser humanitario y
transparente. Debe explicitarse que se trata de un analisis preliminar basado en imagenes
de resolucion media y no validado en campo.

## Citacion [opcional]

**BibTeX:**

```bibtex
@inproceedings{bandara2022changeformer,
  title={ChangeFormer: A Transformer-Based Siamese Network for Change Detection},
  author={Bandara, Wele Gedara Chaminda and Patel, Vishal M.},
  booktitle={IGARSS 2022},
  pages={2075--2078},
  year={2022}
}
```

**APA:**

Penagos, J. D. (2026). *ChangeFormer_Gaza* [modelo ajustado]. Universidad Distrital
Francisco Jose de Caldas. Basado en Bandara y Patel (2022).

## Glosario [opcional]

- **Ajuste fino:** reentrenamiento de un modelo preentrenado en un dominio especifico.
- **xBD:** dataset de dano a edificios del reto xView2.

## Mas informacion [opcional]

Modelo base: `model_cards/changeformer_v6.md`.

## Autores de la ficha [opcional]

Jose David Penagos, Universidad Distrital Francisco Jose de Caldas.

## Contacto de la ficha

GitHub: [Penagos08](https://github.com/Penagos08)
