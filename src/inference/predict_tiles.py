"""Inferencia de ChangeFormer por teselas sobre un par de rasters completos."""

from __future__ import annotations

import numpy as np

from src.data.tiling import Tile, iter_tile_slices, pad_to_multiple, stitch_tiles
from src.models.changeformer_wrapper import ChangeFormerWrapper


def predict_change_map(
    pre_rgb: np.ndarray,
    post_rgb: np.ndarray,
    model: ChangeFormerWrapper,
    tile_size: int = 256,
    stride: int = 256,
    threshold: float = 0.5,
) -> tuple[np.ndarray, np.ndarray]:
    """Genera el mapa de cambio completo.

    Devuelve (mascara_bool, probabilidad) con las dimensiones originales del raster.
    """
    pre_padded, (height, width) = pad_to_multiple(pre_rgb, tile_size)
    post_padded, _ = pad_to_multiple(post_rgb, tile_size)
    pad_h, pad_w = pre_padded.shape[0], pre_padded.shape[1]

    prob_tiles: list[Tile] = []
    total = 0
    for r0, c0, r1, c1 in iter_tile_slices(pad_h, pad_w, tile_size, stride):
        patch_a = pre_padded[r0:r1, c0:c1]
        patch_b = post_padded[r0:r1, c0:c1]
        prob = model.predict_proba(patch_a, patch_b)
        prob_tiles.append(Tile(row=r0, col=c0, array=prob))
        total += 1
        if total % 20 == 0:
            print(f"[infer] {total} teselas procesadas...")

    full_prob = stitch_tiles(prob_tiles, (pad_h, pad_w), tile_size)
    full_prob = full_prob[:height, :width]
    mask = full_prob >= threshold
    print(f"[infer] Teselas totales: {total}. Pixeles marcados como cambio: {int(mask.sum())}.")
    return mask, full_prob


def save_change_map(mask: np.ndarray, prob: np.ndarray, profile: dict, out_raster, out_prob=None) -> None:
    """Guarda la mascara binaria y, opcionalmente, la probabilidad como GeoTIFF."""
    import rasterio
    from pathlib import Path

    out_raster = Path(out_raster)
    out_raster.parent.mkdir(parents=True, exist_ok=True)

    profile = dict(profile)
    profile.update(count=1, dtype="uint8", compress="lzw")
    with rasterio.open(out_raster, "w", **profile) as dst:
        dst.write(mask.astype("uint8"), 1)

    if out_prob is not None:
        out_prob = Path(out_prob)
        out_prob.parent.mkdir(parents=True, exist_ok=True)
        profile_prob = dict(profile)
        profile_prob.update(dtype="float32")
        with rasterio.open(out_prob, "w", **profile_prob) as dst:
            dst.write(prob.astype("float32"), 1)
