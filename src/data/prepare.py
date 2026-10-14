"""Lectura y preparacion de pares de imagenes antes/despues."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from src.data.tiling import align_pair


def read_raster(path: str | Path) -> tuple[np.ndarray, dict]:
    """Lee un GeoTIFF y devuelve (array CxHxW, perfil de rasterio)."""
    import rasterio

    with rasterio.open(path) as dataset:
        array = dataset.read()
        profile = dataset.profile.copy()
    return array, profile


def _to_rgb_zero_one(bands: np.ndarray, percentile: float = 98.0) -> np.ndarray:
    """Convierte las 3 primeras bandas a RGB float 0-1 con estiramiento por percentil."""
    rgb = np.transpose(bands[:3], (1, 2, 0)).astype(np.float32)
    upper = np.percentile(rgb, percentile) if rgb.size else 1.0
    rgb = rgb / max(float(upper), 1e-6)
    return np.clip(rgb, 0, 1)


def load_sentinel_pair(config: dict) -> tuple[np.ndarray, np.ndarray, dict]:
    """Carga el par Sentinel-2 antes/despues y lo prepara como RGB normalizado.

    Devuelve (pre_rgb, post_rgb, profile) con pre y post alineados pixel a pixel.
    """
    root = Path(config["_repo_root"])
    pre_path = root / "data" / "raw" / "sentinel2" / "gaza_s2_pre.tif"
    post_path = root / "data" / "raw" / "sentinel2" / "gaza_s2_post.tif"

    if not pre_path.exists() or not post_path.exists():
        raise SystemExit(
            "Faltan las imagenes Sentinel-2. Ejecuta primero:\n"
            "  python -m src.data.download_sentinel2 --config configs/gaza.yaml --period pre\n"
            "  python -m src.data.download_sentinel2 --config configs/gaza.yaml --period post"
        )

    pre_bands, profile = read_raster(pre_path)
    post_bands, _ = read_raster(post_path)

    pre_rgb = _to_rgb_zero_one(pre_bands)
    post_rgb = _to_rgb_zero_one(post_bands)
    pre_rgb, post_rgb = align_pair(pre_rgb, post_rgb)
    return pre_rgb, post_rgb, profile
