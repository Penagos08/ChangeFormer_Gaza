"""Descarga de imagenes Sentinel-1 GRD (SAR) desde el Microsoft Planetary Computer.

El SAR es la capa complementaria del proyecto: atraviesa nubes y polvo, frecuentes
en Gaza, y es sensible a cambios estructurales. Se guardan las polarizaciones VV/VH
convertidas a decibelios.

Uso:
    python -m src.data.download_sentinel1 --config configs/gaza.yaml
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from src.data.stac_utils import load_stack, search_items, write_raster
from src.utils.config import ensure_dir, load_config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Descarga Sentinel-1 GRD de Gaza.")
    parser.add_argument("--config", default="configs/gaza.yaml", help="Ruta al YAML de configuracion.")
    return parser.parse_args()


def _download_period(config: dict, period_name: str, epsg: int) -> Path:
    s1 = config["sentinel1"]
    bbox = config["aoi"]["bbox_wgs84"]
    period = s1[period_name]

    query = {}
    if s1.get("orbit_state"):
        query["sat:orbit_state"] = {"eq": s1["orbit_state"]}

    print(f"[sentinel1] Buscando imagenes {period_name} entre {period['start']} y {period['end']}...")
    items = search_items(
        collection=s1["collection"],
        bbox=bbox,
        datetime_range=f"{period['start']}/{period['end']}",
        query=query,
    )
    if not items:
        raise SystemExit(
            "No se encontraron imagenes Sentinel-1. Revisa fechas o la direccion orbital."
        )

    print(f"[sentinel1] {len(items)} item(s) encontrados; usando agregacion temporal.")
    mosaic = load_stack(
        items=items,
        assets=list(s1["polarization"]),
        bbox=bbox,
        epsg=epsg,
        resolution=s1["resolution"],
        aggregate="median",
    )

    # Convertir potencia lineal a dB, evitando el logaritmo de cero.
    data = np.asarray(mosaic.values, dtype=np.float32)
    db = 10.0 * np.log10(np.clip(data, 1e-6, None))
    mosaico_db = mosaic.copy(data=db)

    out_path = Path(config["_repo_root"]) / "data" / "raw" / "sentinel1" / f"gaza_s1_{period_name}.tif"
    ensure_dir(out_path.parent)
    write_raster(mosaico_db, out_path)
    print(f"[sentinel1] Guardado en {out_path}")
    return out_path


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    epsg = int(str(config["project"]["crs"]).split(":")[1])
    _download_period(config, "pre", epsg)
    _download_period(config, "post", epsg)


if __name__ == "__main__":
    main()
