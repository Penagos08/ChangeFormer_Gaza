"""Pruebas de carga de configuracion y utilidades."""

from pathlib import Path

import numpy as np

from src.utils.config import REPO_ROOT, load_config, resolve_path
from src.utils.geo import normalize_changeformer, to_uint8


def test_load_config_has_expected_sections():
    config = load_config("configs/gaza.yaml")
    for section in ("project", "aoi", "sentinel2", "model", "tiling", "outputs"):
        assert section in config
    assert config["_repo_root"] == str(REPO_ROOT)


def test_resolve_path_is_absolute():
    config = load_config("configs/gaza.yaml")
    path = resolve_path(config, "aoi.geojson")
    assert path.is_absolute()
    assert isinstance(path, Path)


def test_normalize_changeformer_range():
    array = np.array([[[0.0, 0.5, 1.0]]], dtype=np.float32)
    normalized = normalize_changeformer(array)
    assert np.isclose(normalized.min(), -1.0)
    assert np.isclose(normalized[0, 0, 1], 0.0)


def test_to_uint8():
    array = np.array([0.0, 0.5, 1.0], dtype=np.float32)
    result = to_uint8(array)
    assert result.dtype == np.uint8
    assert result.tolist() == [0, 127, 255]
