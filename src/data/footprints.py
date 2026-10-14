"""Descarga de huellas de edificios (OpenStreetMap / HOTOSM) para la Franja de Gaza.

Estas huellas actuan como referencia pre-conflicto sobre la cual se cuantifican
las estructuras afectadas por el cambio detectado.

Uso:
    python -m src.data.footprints --config configs/gaza.yaml
"""

from __future__ import annotations

import argparse
from pathlib import Path

from src.utils.config import ensure_dir, load_config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Descarga huellas de edificios de Gaza (OSM).")
    parser.add_argument("--config", default="configs/gaza.yaml", help="Ruta al YAML de configuracion.")
    return parser.parse_args()


def download_osm_footprints(bbox: list[float]):
    """Descarga edificios desde OSM, compatible con varias versiones de osmnx."""
    import osmnx as ox

    min_lon, min_lat, max_lon, max_lat = bbox
    tags = {"building": True}

    try:
        # osmnx >= 2.0
        gdf = ox.features_from_bbox(bbox=(min_lon, min_lat, max_lon, max_lat), tags=tags)
    except TypeError:
        # osmnx 1.x
        gdf = ox.features_from_bbox(max_lat, min_lat, max_lon, min_lon, tags)

    # Conservar solo geometrias poligonales (edificios).
    gdf = gdf[gdf.geometry.type.isin(["Polygon", "MultiPolygon"])].copy()
    gdf = gdf.reset_index()
    return gdf


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    bbox = config["aoi"]["bbox_wgs84"]

    print("[footprints] Descargando edificios desde OpenStreetMap...")
    gdf = download_osm_footprints(bbox)
    print(f"[footprints] {len(gdf)} huellas descargadas.")

    out_path = Path(config["_repo_root"]) / "data" / "raw" / "footprints" / "gaza_buildings.geojson"
    ensure_dir(out_path.parent)
    gdf.to_file(out_path, driver="GeoJSON")
    print(f"[footprints] Guardado en {out_path}")


if __name__ == "__main__":
    main()
