"""Carga de configuracion y utilidades comunes del proyecto."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]


def load_config(path: str | os.PathLike[str]) -> dict[str, Any]:
    """Carga un archivo YAML de configuracion y resuelve rutas relativas al repo."""
    config_path = Path(path)
    if not config_path.is_absolute():
        config_path = REPO_ROOT / config_path
    with open(config_path, "r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle)
    config["_config_path"] = str(config_path)
    config["_repo_root"] = str(REPO_ROOT)
    return config


def resolve_path(config: dict[str, Any], key_path: str) -> Path:
    """Devuelve una ruta absoluta a partir de una clave anidada tipo 'aoi.geojson'."""
    node: Any = config
    for key in key_path.split("."):
        node = node[key]
    path = Path(node)
    if not path.is_absolute():
        path = Path(config["_repo_root"]) / path
    return path


def ensure_dir(path: str | os.PathLike[str]) -> Path:
    """Crea el directorio si no existe y lo devuelve."""
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory
