---
# Metadatos segun la especificacion de model card de Hugging Face
# https://github.com/huggingface/hub-docs/blob/main/modelcard.md
language:
  - en
license: mit
library_name: pytorch
pipeline_tag: image-segmentation
tags:
  - change-detection
  - remote-sensing
  - earth-observation
  - transformer
  - siamese-network
  - bitemporal
datasets:
  - levir-cd
metrics:
  - iou
  - f1
  - precision
  - recall
base_model: nvidia/segformer
---

# Ficha de modelo: ChangeFormerV6

<!-- Resumen rapido del modelo -->

ChangeFormerV6 es una red siamesa basada en transformers para deteccion de cambios
binaria en imagenes bitemporales. Compara dos imagenes de la misma zona (antes y
despues) y produce una mascara que indica, pixel a pixel, donde ocurrio un cambio.

## Detalles del modelo

### Descripcion del modelo

ChangeFormer combina un codificador jerarquico tipo transformer (encoder MiT, heredado
de SegFormer) con un decodificador tambien transformer que fusiona caracteristicas de
las dos imagenes en varias resoluciones. A diferencia de las arquitecturas
convolucionales puras, el mecanismo de atencion captura dependencias de largo alcance
entre las dos tomas, lo que mejora la deteccion en objetos de gran tamano y en cambios
de forma global. La version V6 usa una dimension de embedding de 256 y produce una
salida de dos clases (cambio / no cambio). En este proyecto se emplea como modelo base
preentrenado en LEVIR-CD y como punto de partida para el ajuste fino con xBD.

- **Desarrollado por:** Wele Gedara Chaminda Bandara y Vishal M. Patel (Universidad Johns Hopkins).
- **Financiado por [opcional]:** [Informacion adicional necesaria]
- **Compartido por [opcional]:** Repositorio oficial https://github.com/wgcban/ChangeFormer
- **Tipo de modelo:** Red siamesa transformer para segmentacion binaria de cambios.
- **Idioma(s) (PLN):** No aplica (modelo de vision por computador).
- **Licencia:** MIT, con la salvedad publicada por los autores de que el codigo se libera
  para fines no comerciales y de investigacion; para uso comercial debe contactarse a los autores.
- **Ajustado a partir de [opcional]:** SegFormer (encoder MiT), preentrenado en ADE20K.

### Fuentes del modelo [opcional]

- **Repositorio:** https://github.com/wgcban/ChangeFormer
- **Articulo:** Bandara, W. G. C. y Patel, V. M. (2022). ChangeFormer: A Transformer-Based
  Siamese Network for Change Detection. IGARSS. arXiv:2201.01293
- **Demo [opcional]:** `demo_LEVIR.py` en el repositorio oficial

## Usos

### Uso directo

Deteccion binaria de cambios entre dos imagenes aereas o satelitales alineadas
geometricamente, en formato de recortes de 256x256 pixeles. Es el motor de inferencia
del pipeline de ChangeFormer_Gaza para identificar cambios en el entorno construido.

### Uso posterior [opcional]

Ajuste fino con el dataset xBD (xView2) para especializar el modelo en daño a edificios,
y uso como capa intermedia dentro de sistemas mayores de evaluacion de daño, alerta
temprana o monitoreo humanitario.

### Usos fuera de alcance

No fue disenado para clasificar la severidad del dano, para estimar victimas, ni para
tareas medicas, legales o forenses. No debe usarse como unica fuente para decisiones que
afecten derechos de las personas. No esta pensado para imagenes SAR directamente ni para
resoluciones muy distintas a las de su entrenamiento.

## Sesgos, riesgos y limitaciones

- El modelo base se entreno en LEVIR-CD (imagenes aereas de EE. UU.), por lo que su
  desempeno puede degradarse en escenas con tipologias constructivas distintas, como las
  de Gaza.
- Detecta cambio generico, no destruccion; un edificio nuevo o una via nueva tambien
  cuentan como cambio.
- La deteccion depende de un co-registro geometrico preciso entre las dos tomas; errores
  de alineacion producen falsos positivos en los bordes.
- La nubosidad y el polvo, frecuentes en la region, degradan la entrada optica.
- Renderizar conclusiones a nivel de edificio exige el cruce con huellas y un umbral de
  cobertura, lo que introduce incertidumbre adicional.

### Recomendaciones

Los usuarios, tanto directos como posteriores, deben conocer los sesgos y limitaciones
del modelo. Dado que la deteccion de dano en contextos de conflicto es sensible, los
resultados deben presentarse como preliminares, acompanarse de metricas de incertidumbre
y, cuando sea posible, validarse con fuentes independientes como UNOSAT.

## Como empezar con el modelo

```python
import sys
sys.path.insert(0, "third_party/ChangeFormer")

from src.models.changeformer_wrapper import ChangeFormerWrapper

modelo = ChangeFormerWrapper(
    checkpoint="checkpoints/ChangeFormer_LEVIR/best_ckpt.pt",
    embed_dim=256,
    n_class=2,
    device="auto",
)
mascara = modelo.predict_mask(imagen_pre, imagen_post, threshold=0.5)
```

## Detalles de entrenamiento

### Datos de entrenamiento

LEVIR-CD: 637 pares de imagenes aereas de muy alta resolucion (0.5 m) de 1024x1024
pixeles, recortadas a 256x256, con anotaciones binarias de cambio de edificios. Los
autores inicializan parte del codificador con un modelo preentrenado en segmentacion RGB
(ADE20K) para acelerar la convergencia.

### Procedimiento de entrenamiento

#### Preprocesamiento [opcional]

Redimensionado a 256x256, aumentos con volteos horizontal y vertical, recorte aleatorio
con escalado, desenfoque gaussiano y variacion de color. Normalizacion con media y
desviacion de 0.5 (rango final -1 a 1).

#### Hiperparametros de entrenamiento

- **Regimen de entrenamiento:** precision simple (fp32), 200 epocas, optimizador con
  tasa de aprendizaje ajustada linealmente, tamano de lote 8. Ver `scripts/` del
  repositorio oficial para los valores exactos.

#### Velocidades, tamanos y tiempos [opcional]

[Informacion adicional necesaria] (no publicada en el articulo original).

## Evaluacion

### Datos, factores y metricas de prueba

#### Datos de prueba

Conjunto de prueba de LEVIR-CD, complementado en este proyecto con el cruce espacial
frente a las etiquetas de dano de UNOSAT para la Franja de Gaza (ver
`dataset_cards/unosat_gaza_damage.md`).

#### Factores

Resolucion espacial, estacionalidad y cobertura nubosa de las imagenes; densidad y
tipologia del entorno construido; grado de alineacion bitemporal.

#### Metricas

F1 e IoU son las metricas estandar para segmentacion binaria de cambios; se
complementan con precision y recall, y con el cruce espacial contra datos de referencia.

### Resultados

El articulo original reporta resultados estado del arte en LEVIR-CD, DSIFN-CD y CDD.
En este repositorio los pesos base de LEVIR-CD se usan como punto de partida y su
desempeno especifico en Gaza se documenta en `reports/metricas_unosat.md`.

#### Resumen

[Informacion adicional necesaria] hasta ejecutar el pipeline completo sobre Gaza.

## Impacto ambiental

Las emisiones de carbono pueden estimarse con la calculadora de impacto de aprendizaje
automatico (Lacoste et al., 2019). Los datos de entrenamiento originales no estan
documentados en el articulo.

- **Tipo de hardware:** [Informacion adicional necesaria]
- **Horas de uso:** [Informacion adicional necesaria]
- **Proveedor de nube:** [Informacion adicional necesaria]
- **Region de computo:** [Informacion adicional necesaria]
- **Carbono emitido:** [Informacion adicional necesaria]

## Especificaciones tecnicas [opcional]

### Arquitectura y objetivo

Encoder jerarquico tipo transformer (MiT) compartido por una red siamesa, con un
decodificador transformer que fusiona caracteristicas multiescala. Funcion de perdida de
entropia cruzada (o perdida combinada segun la configuracion). Dimension de embedding 256.

### Infraestructura de computo

[Informacion adicional necesaria]

#### Hardware

GPU con al menos 4 GB de memoria para inferencia por recortes; se requiere una GPU mayor
para entrenamiento.

#### Software

Python, PyTorch, torchvision, einops, ttach. Ver `requirements.txt` del repositorio oficial.

## Consideraciones eticas

Este modelo opera sobre imagenes de zonas afectadas por un conflicto armado. El uso de
detecciones automaticas de destruccion debe respetar el derecho internacional humanitario
y los principios de proteccion de datos. Los mapas derivados no deben emplearse para
señalar individuos ni para fines militares. La incertidumbre debe declararse de forma
explicita.

## Citacion [opcional]

**BibTeX:**

```bibtex
@inproceedings{bandara2022changeformer,
  title={ChangeFormer: A Transformer-Based Siamese Network for Change Detection},
  author={Bandara, Wele Gedara Chaminda and Patel, Vishal M.},
  booktitle={IGARSS 2022 - 2022 IEEE International Geoscience and Remote Sensing Symposium},
  pages={2075--2078},
  year={2022}
}
```

**APA:**

Bandara, W. G. C. y Patel, V. M. (2022). *ChangeFormer: A Transformer-Based Siamese
Network for Change Detection*. IGARSS 2022. arXiv:2201.01293.

## Glosario [opcional]

- **Cambio binario:** clasificacion por pixel entre "cambio" y "no cambio".
- **Red siamesa:** arquitectura con dos ramas que comparten pesos y procesan cada imagen.
- **IoU:** interseccion sobre union, metrica de solapamiento entre prediccion y verdad.
- **MiT:** Mixed Transformer, encoder jerarquico usado por SegFormer.

## Mas informacion [opcional]

Ficha base del proyecto: `model_cards/README.md`. Modelo ajustado derivado:
`model_cards/changeformer_gaza.md`.

## Autores de la ficha [opcional]

Jose David Penagos, Universidad Distrital Francisco Jose de Caldas.

## Contacto de la ficha

GitHub: [Penagos08](https://github.com/Penagos08)
