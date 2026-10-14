# ChangeFormer_Gaza

Detección de edificios e infraestructura destruida en la Franja de Gaza mediante
teledetección e inteligencia artificial geoespacial de código abierto, con
[ChangeFormer](https://github.com/wgcban/ChangeFormer) (Bandara y Patel, IGARSS 2022)
como modelo de detección de cambios.

Este proyecto es reproducible y público. Toma como entrada imágenes satelitales
libres (Sentinel-2 óptico y Sentinel-1 SAR), las compara con un modelo transformer
siames en pares *antes/después*, y produce mapas vectorizados de cambio que luego
se cruzan con huellas de edificios y con las etiquetas de daño de UNOSAT para
estimar cuántas estructuras resultaron afectadas.

## Motivación

La Franja de Gaza ha sufrido una destrucción masiva de su entorno construido. La
verificación sobre el terreno es peligrosa y costosa, por lo que el análisis de
imágenes satelitales se convirtió en la principal herramienta para cuantificar el
daño. UNOSAT, a partir de imágenes ópticas de muy alta resolución, identificó unos
174 486 edificios dañados hacia abril de 2025 (70 % del total de estructuras). El
trabajo académico de Scher y Van Den Hoek con InSAR de Sentinel-1 logró detectar
el 92,5 % de las etiquetas de UNOSAT con apenas un 1,2 % de falsos positivos.

Inspirados en esos antecedentes, este repositorio propone un flujo abierto, sin
dependencia de imágenes comerciales, que cualquiera puede ejecutar y auditar.

## Fuentes de datos

Todas son de acceso libre y no requieren credenciales, salvo el dataset de
entrenamiento xBD.

| Dato | Fuente | Uso |
|------|--------|-----|
| Sentinel-2 L2A | Microsoft Planetary Computer (STAC) | entrada óptica RGB+NIR a ChangeFormer |
| Sentinel-1 GRD | Microsoft Planetary Computer (STAC) | capa SAR complementaria (VV/VH) |
| Huellas de edificios | OpenStreetMap / HOTOSM vía OSMnx | conteo de estructuras afectadas |
| Etiquetas de daño | UNOSAT sobre HDX (GDB) | validación y referencia |
| xBD / xView2 | xview2.org (registro) | ajuste fino del modelo |

## Arquitectura del pipeline

```
Sentinel-2 (pre)  ─┐
                   ├─► recorte AOI, co-registro, teselado 256x256
Sentinel-2 (post) ─┘        │
                             ▼
                    ChangeFormer (siames)  ──►  máscara binaria de cambio
                             │
Sentinel-1 (pre/post) ───────┘ (capa de apoyo)
                             ▼
              vectorización   ──►   cruce con huellas de edificios
                             ▼
                    cruce con UNOSAT  ──►  métricas (precision / recall)
                             ▼
                  mapas, GeoJSON y reporte en `outputs/`
```

## Estructura del repositorio

```
ChangeFormer_Gaza/
├── configs/            # parámetros del proyecto y del modelo
├── data/
│   └── aoi/            # área de interés (GeoJSON)
├── src/
│   ├── data/           # descarga y preparación de datos
│   ├── models/         # envoltura de ChangeFormer
│   ├── inference/      # inferencia por teselas y mosaico
│   ├── train/          # ajuste fino con xBD
│   ├── postprocess/    # vectorización, cruce con edificios, métricas
│   └── utils/          # utilidades geoespaciales y de visualización
├── third_party/        # submódulo ChangeFormer (código oficial)
├── notebooks/          # exploración y demo
├── scripts/            # ejecución del pipeline completo
├── tests/              # pruebas básicas
└── outputs/            # resultados (no versionados)
```

## Instalación

Requiere un entorno conda con Python 3.10 (PyTorch no publica ruedas estables
para Python 3.14, que es la versión del sistema anfitrión de desarrollo).

```bash
conda env create -f environment.yml
conda activate changeformer-gaza

# Clonar el modelo oficial dentro del repositorio
git submodule update --init --recursive
```

Descarga los pesos preentrenados de ChangeFormerV6 (LEVIR-CD) y colócalos en
`checkpoints/ChangeFormer_LEVIR/best_ckpt.pt`. Ver enlaces en `third_party/ChangeFormer`.

## Uso

```bash
# 1. Descargar imágenes antes/después y huellas de edificios
python -m src.data.download_sentinel2 --config configs/gaza.yaml --period pre
python -m src.data.download_sentinel2 --config configs/gaza.yaml --period post
python -m src.data.download_sentinel1 --config configs/gaza.yaml
python -m src.data.footprints      --config configs/gaza.yaml

# 2. Inferencia con ChangeFormer y post-proceso
python -m src.inference.infer_gaza --config configs/gaza.yaml
python -m src.postprocess.buildings_join --config configs/gaza.yaml
python -m src.postprocess.stats          --config configs/gaza.yaml

# o todo de una vez
pwsh scripts/run_pipeline.ps1
```

El ajuste fino con xBD está pensado para ejecutarse en Google Colab por la
limitación de GPU local: ver `notebooks/02_changeformer_gaza.ipynb`.

## Resultados esperados

- `outputs/rasters/cambio_gaza.tif` — máscara binaria de cambio georreferenciada.
- `outputs/rasters/cambio_gaza_prob.tif` — probabilidad de cambio por píxel.
- `outputs/vectors/cambio_gaza.geojson` — polígonos de cambio.
- `outputs/vectors/edificios_afectados.geojson` — huellas intersectadas.
- `outputs/maps/vista_previa_gaza.png` — figura de comparación antes/después/predicción.
- `reports/edificios_resumen.json` — conteo de edificios afectados.
- `reports/metricas_unosat.md` — métricas de precisión y recall frente a UNOSAT.

## Limitaciones

- Los pesos preentrenados de ChangeFormer provienen de LEVIR-CD y detectan cambio
  binario genérico, no severidad de daño. La semántica de "destruido" depende del
  ajuste fino con xBD y del cruce con UNOSAT.
- Gaza presenta nubosidad frecuente; por eso el SAR es parte del diseño y no un
  complemento opcional.
- La GPU de desarrollo (NVIDIA MX330, 2 GB) solo permite inferencia por teselas;
  el entrenamiento debe hacerse en la nube.
- Los resultados son preliminares y no sustituyen la verificación en campo.

## Referencias

- Bandara, W. G. C. y Patel, V. M. (2022). *ChangeFormer: A Transformer-Based
  Siamese Network for Change Detection*. IGARSS. arXiv:2201.01293.
- Scher, C. y Van Den Hoek, J. (2025). *Active InSAR monitoring of building
  damage in Gaza during the Israel-Hamas War*. arXiv:2506.14730.
- Gupta, R. et al. (2019). *Creating xBD: A Dataset for Assessing Building
  Damage from Satellite Imagery*. CVPRW.
- UNOSAT. *Gaza Strip Comprehensive Damage Assessment*. https://unosat.org/
- Microsoft Planetary Computer. https://planetarycomputer.microsoft.com/

## Licencia

MIT. Ver `LICENSE`.
