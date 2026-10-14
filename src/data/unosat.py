"""Preparacion del dataset de referencia de UNOSAT.

UNOSAT publica las evaluaciones de dano como File Geodatabase (GDB) en HDX.
La descarga es manual (requiere aceptar terminos en data.humdata.org); este modulo
toma el GDB descargado, detecta su capa y lo convierte a GeoJSON para el cruce de
validacion.

Uso:
    python -m src.data.unosat --config configs/gaza.yaml
"""

from __future__ import annotations

import argparse
from pathlib import Path

from src.utils.config import ensure_dir, load_config, resolve_path

HDX_HINT = (
    "Descarga el GDB de UNOSAT desde https://data.humdata.org (busca "
    "'UNOSAT Gaza Strip Comprehensive Damage Assessment'), descomprimelo y "
    "apunta la clave 'unosat.gdb_path' del YAML a la carpeta .gdb."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convierte el GDB de UNOSAT a GeoJSON.")
    parser.add_argument("--config", default="configs/gaza.yaml", help="Ruta al YAML de configuracion.")
    return parser.parse_args()


def find_layer(gdb_path: Path, layer: str | None) -> str:
    """Devuelve el nombre de la capa a leer dentro del GDB."""
    import fiona

    layers = fiona.listlayers(str(gdb_path))
    if not layers:
        raise SystemExit(f"El GDB {gdb_path} no contiene capas.")
    if layer and layer in layers:
        return layer
    print(f"[unosat] Capas encontradas: {layers}. Usando '{layers[0]}'.")
    return layers[0]


def main() -> None:
    args = parse_args()
    config = load_config(args.config)

    gdb_path = resolve_path(config, "unosat.gdb_path")
    if not gdb_path.exists():
        raise SystemExit(f"No existe {gdb_path}.\n{HDX_HINT}")

    import geopandas as gpd

    layer = find_layer(gdb_path, config["unosat"].get("layer"))
    print(f"[unosat] Leyendo capa '{layer}' de {gdb_path}...")
    gdf = gpd.read_file(gdb_path, layer=layer)
    gdf = gdf.to_crs(config["project"]["crs"])
    print(f"[unosat] {len(gdf)} registros de dano.")

    out_path = Path(config["_repo_root"]) / config["unosat"]["vector_path"]
    ensure_dir(out_path.parent)
    gdf.to_file(out_path, driver="GeoJSON")
    print(f"[unosat] Guardado en {out_path}")


if __name__ == "__main__":
    main()
