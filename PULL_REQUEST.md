# Pull request

**Titulo**

```
feat: pipeline abierto de deteccion de dano en Gaza con ChangeFormer
```

**Rama base:** `main`
**Rama de comparacion:** `feat/changeformer-gaza-pipeline`

**Enlace para abrirlo:**
https://github.com/Penagos08/ChangeFormer_Gaza/compare/main...feat/changeformer-gaza-pipeline

---

## Descripcion

Pipeline de codigo abierto para detectar dano en edificios e infraestructura en la Franja
de Gaza a partir de imagenes satelitales libres (Sentinel-2 y Sentinel-1), usando el modelo
de deteccion de cambios ChangeFormer. El repositorio incluye todo lo necesario para
descargar datos, preparar teselas, inferir, vectorizar resultados y validarlos contra la
referencia de UNOSAT.

## Contenido

- Descarga de Sentinel-2 L2A y Sentinel-1 GRD desde Microsoft Planetary Computer (STAC).
- Huellas de edificios de OpenStreetMap/HOTOSM y datos de UNOSAT.
- Preprocesamiento por teselas y alineacion de pares bitemporales.
- Wrapper de ChangeFormerV6 con pesos de LEVIR-CD (normalizacion 0.5, no ImageNet).
- Inferencia sobre Gaza con salida georreferenciada (raster de cambio y probabilidad).
- Postproceso: vectorizacion, cruce con edificios afectados y metricas frente a UNOSAT.
- Ajuste fino opcional con xBD (xView2) para el modelo especializado.
- Notebooks de exploracion y demo, y script de orquestacion `scripts/run_pipeline.ps1`.
- Fichas de modelos y de conjuntos de datos (model cards y dataset cards).

## Estructura

- `src/`: codigo del pipeline (data, models, inference, postprocess, train, utils).
- `configs/`: configuracion de Gaza y del modelo.
- `model_cards/`, `dataset_cards/`: fichas siguiendo Mitchell et al. (2019) y plantillas
  de Hugging Face.
- `notebooks/`, `scripts/`, `tests/`.

## Como ejecutar

1. Crear el entorno: `conda env create -f environment.yml`.
2. Activar: `conda activate changeformer-gaza`.
3. Configurar el AOI y las fechas en `configs/gaza.yaml`.
4. Ejecutar `scripts/run_pipeline.ps1`.

## Datos y licencias

- Copernicus Sentinel: acceso libre (CC BY-SA 3.0 IGO).
- OpenStreetMap: ODbL 1.0.
- UNOSAT: CC BY-SA.
- xBD (xView2): CC BY-NC-SA 4.0 (solo uso no comercial).
- ChangeFormer: MIT.

## Limitaciones

- Resultados preliminares, no validados en campo.
- Diferencia de resolucion y dominio entre xBD (muy alta resolucion, desastres naturales)
  y Sentinel-2 (10 m, conflicto): error de transferencia.
- El SAR complementario esta sujeto a ruido moteado y distorsiones geometricas.
- GPU local solo para inferencia; el entrenamiento se penso para la nube.

## Lista de verificacion

- [x] El codigo compila (`python -m compileall -q src tests conftest.py`).
- [x] Commits con prefijo semantico.
- [ ] Pruebas ejecutadas en el entorno conda (`pytest`).
- [ ] Verificacion de resultados con datos reales.
