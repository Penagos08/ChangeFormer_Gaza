"""Teselado y reconstruccion de rasters para la inferencia por parches.

ChangeFormer espera entradas de 256x256. Como el AOI de Gaza es mucho mayor, se
divide en teselas, se infiere cada una y se reconstruye el mapa completo promediando
las zonas de solape.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

import numpy as np


@dataclass
class Tile:
    row: int
    col: int
    array: np.ndarray


def pad_to_multiple(array: np.ndarray, multiple: int) -> tuple[np.ndarray, tuple[int, int]]:
    """Rellena un arreglo HxWxC hasta que H y W sean multiplos de `multiple`.

    Devuelve el arreglo rellenado y la forma original (altura, anchura).
    """
    height, width = array.shape[:2]
    pad_h = (multiple - height % multiple) % multiple
    pad_w = (multiple - width % multiple) % multiple
    if pad_h == 0 and pad_w == 0:
        return array, (height, width)
    if array.ndim == 3:
        pad_width = ((0, pad_h), (0, pad_w), (0, 0))
    else:
        pad_width = ((0, pad_h), (0, pad_w))
    padded = np.pad(array, pad_width, mode="reflect")
    return padded, (height, width)


def iter_tile_slices(height: int, width: int, size: int, stride: int) -> Iterator[tuple[int, int, int, int]]:
    """Genera coordenadas (r0, c0, r1, c1) de teselas que cubren todo el raster."""
    row_starts = list(range(0, max(height - size, 0) + 1, stride))
    col_starts = list(range(0, max(width - size, 0) + 1, stride))
    if row_starts[-1] != height - size:
        row_starts.append(height - size)
    if col_starts[-1] != width - size:
        col_starts.append(width - size)
    for r0 in row_starts:
        for c0 in col_starts:
            yield r0, c0, r0 + size, c0 + size


def iter_tiles(array: np.ndarray, size: int, stride: int) -> Iterator[Tile]:
    """Itera las teselas de un arreglo HxW (o HxWxC)."""
    height, width = array.shape[:2]
    for r0, c0, r1, c1 in iter_tile_slices(height, width, size, stride):
        yield Tile(row=r0, col=c0, array=array[r0:r1, c0:c1])


def stitch_tiles(tiles: list[Tile], shape: tuple[int, int], tile_size: int) -> np.ndarray:
    """Reconstruye un raster promediando las predicciones en las zonas de solape.

    Parametros
    ----------
    tiles: lista de Tile con predicciones (HxW o HxWxC).
    shape: forma objetivo (altura, anchura) del raster original.
    """
    height, width = shape
    channels = None
    if tiles[0].array.ndim == 3:
        channels = tiles[0].array.shape[2]
        accumulator = np.zeros((height, width, channels), dtype=np.float64)
        counts = np.zeros((height, width, 1), dtype=np.float64)
    else:
        accumulator = np.zeros((height, width), dtype=np.float64)
        counts = np.zeros((height, width), dtype=np.float64)

    for tile in tiles:
        r0, c0 = tile.row, tile.col
        r1, c1 = r0 + tile.array.shape[0], c0 + tile.array.shape[1]
        accumulator[r0:r1, c0:c1] += tile.array
        if channels is not None:
            counts[r0:r1, c0:c1] += 1.0
        else:
            counts[r0:r1, c0:c1] += 1.0

    counts = np.maximum(counts, 1.0)
    return accumulator / counts


def align_pair(pre: np.ndarray, post: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Recorta dos arreglos a la menor forma comun para garantizar co-registro por pixel."""
    height = min(pre.shape[0], post.shape[0])
    width = min(pre.shape[1], post.shape[1])
    return pre[:height, :width], post[:height, :width]
