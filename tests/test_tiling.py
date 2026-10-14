"""Pruebas del teselado y la reconstruccion de rasters."""

import numpy as np

from src.data.tiling import align_pair, iter_tile_slices, pad_to_multiple, stitch_tiles, Tile


def test_pad_to_multiple_no_change():
    array = np.zeros((256, 512, 3), dtype=np.float32)
    padded, original = pad_to_multiple(array, 256)
    assert padded.shape == array.shape
    assert original == (256, 512)


def test_pad_to_multiple_pads():
    array = np.ones((300, 300, 3), dtype=np.float32)
    padded, original = pad_to_multiple(array, 256)
    assert padded.shape[0] % 256 == 0
    assert padded.shape[1] % 256 == 0
    assert original == (300, 300)


def test_iter_tile_slices_covers_all():
    slices = list(iter_tile_slices(512, 512, 256, 256))
    assert len(slices) == 4
    assert slices[0] == (0, 0, 256, 256)
    assert slices[-1] == (256, 256, 512, 512)


def test_iter_tile_slices_overlap_edges():
    slices = list(iter_tile_slices(300, 300, 256, 256))
    assert slices[-1][2] == 300 and slices[-1][3] == 300


def test_stitch_tiles_roundtrip():
    original = np.arange(256 * 256, dtype=np.float32).reshape(256, 256)
    tiles = [Tile(row=0, col=0, array=original)]
    result = stitch_tiles(tiles, (256, 256), 256)
    assert np.allclose(result, original)


def test_stitch_tiles_averages_overlap():
    tile_a = Tile(row=0, col=0, array=np.full((2, 2), 1.0))
    tile_b = Tile(row=0, col=1, array=np.full((2, 2), 3.0))
    result = stitch_tiles([tile_a, tile_b], (2, 3), 2)
    assert result.shape == (2, 3)
    assert np.isclose(result[0, 1], 2.0)


def test_align_pair():
    pre = np.zeros((10, 12, 3))
    post = np.zeros((8, 12, 3))
    aligned_pre, aligned_post = align_pair(pre, post)
    assert aligned_pre.shape == aligned_post.shape == (8, 12, 3)
