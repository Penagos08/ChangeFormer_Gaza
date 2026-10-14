# Orquesta el pipeline completo de ChangeFormer_Gaza.
# Uso:  powershell -ExecutionPolicy Bypass -File scripts\run_pipeline.ps1
param(
    [string]$Config = "configs/gaza.yaml",
    [int]$MaxItems = 4
)

$ErrorActionPreference = "Stop"

Write-Host "== 1/8 Descarga Sentinel-2 (antes) ==" -ForegroundColor Cyan
python -m src.data.download_sentinel2 --config $Config --period pre --max-items $MaxItems
if (-not $?) { throw "Fallo la descarga Sentinel-2 pre" }

Write-Host "== 2/8 Descarga Sentinel-2 (despues) ==" -ForegroundColor Cyan
python -m src.data.download_sentinel2 --config $Config --period post --max-items $MaxItems
if (-not $?) { throw "Fallo la descarga Sentinel-2 post" }

Write-Host "== 3/8 Descarga Sentinel-1 (SAR antes y despues) ==" -ForegroundColor Cyan
python -m src.data.download_sentinel1 --config $Config
if (-not $?) { throw "Fallo la descarga Sentinel-1" }

Write-Host "== 4/8 Descarga huellas de edificios (OSM) ==" -ForegroundColor Cyan
python -m src.data.footprints --config $Config
if (-not $?) { throw "Fallo la descarga de huellas" }

Write-Host "== 5/8 Inferencia con ChangeFormer ==" -ForegroundColor Cyan
python -m src.inference.infer_gaza --config $Config
if (-not $?) { throw "Fallo la inferencia" }

Write-Host "== 6/8 Vectorizacion del cambio ==" -ForegroundColor Cyan
python -m src.postprocess.vectorize --config $Config
if (-not $?) { throw "Fallo la vectorizacion" }

Write-Host "== 7/8 Cruce con huellas de edificios ==" -ForegroundColor Cyan
python -m src.postprocess.buildings_join --config $Config
if (-not $?) { throw "Fallo el cruce con edificios" }

Write-Host "== 8/8 Validacion con UNOSAT (opcional) ==" -ForegroundColor Cyan
if (Test-Path "data/external/unosat/unosat_gaza_damage.gdb") {
    python -m src.data.unosat --config $Config
    python -m src.postprocess.stats --config $Config
} else {
    Write-Host "Omitido: descarga el GDB de UNOSAT desde HDX y colocalo en data/external/unosat/." -ForegroundColor Yellow
}

Write-Host "Pipeline terminado. Revisa outputs/ y reports/." -ForegroundColor Green
