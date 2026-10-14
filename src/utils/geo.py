"""Utilidades geoespaciales y de normalizacion."""

from __future__ import annotations

from pathlib import Path

import numpy as np

# ChangeFormer normaliza sus entradas con media y desviacion 0.5 (rango final -1 a 1),
# segun datasets/data_utils.py del repositorio oficial.
CHANGEFORMER_MEAN = 0.5
CHANGEFORMER_STD = 0.5


def normalize_changeformer(array: np.ndarray) -> np.ndarray:
    """Normaliza un arreglo HxWxC (RGB, rango 0-1) al rango -1..1 que espera ChangeFormer."""
    return (array - CHANGEFORMER_MEAN) / CHANGEFORMER_STD


def read_rgb(path: str | Path) -> np.ndarray:
    """Lee un GeoTIFF y devuelve un arreglo HxWxC normalizado a 0-1 usando las 3 primeras bandas."""
    import rasterio

    with rasterio.open(path) as dataset:
        bands = dataset.read()
        profile = dataset.profile
    # bands: (C, H, W) -> (H, W, C)
    array = np.transpose(bands[:3], (1, 2, 0)).astype(np.float32)
    array = np.clip(array, 0, None)
    max_value = np.percentile(array, 99) if array.max() > 0 else 1.0
    array = array / max(max_value, 1e-6)
    return np.clip(array, 0, 1)


def to_uint8(array: np.ndarray) -> np.ndarray:
    """Convierte un arreglo flotante en rango 0-1 a uint8 (0-255)."""
    return (np.clip(array, 0, 1) * 255).astype(np.uint8)
