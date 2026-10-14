"""Vectorizacion de la mascara de cambio (raster -> poligonos)."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.utils.config import ensure_dir, load_config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Vectoriza el mapa de cambio de Gaza.")
    parser.add_argument("--config", default="configs/gaza.yaml", help="Ruta al YAML de configuracion.")
    parser.add_argument("--raster", default=None, help="GeoTIFF de cambio (por defecto el del YAML).")
    parser.add_argument("--min-area", type=float, default=20.0, help="Area minima en m2 para conservar un poligono.")
    parser.add_argument("--simplify", type=float, default=1.0, help="Tolerancia de simplificacion en unidades del CRS.")
    return parser.parse_args()


def vectorize_mask(raster_path: Path, out_path: Path, min_area: float, simplify: float) -> int:
    """Convierte una mascara binaria en poligonos y la guarda como GeoJSON."""
    import geopandas as gpd
    import rasterio
    from rasterio import features
    from shapely.geometry import shape

    with rasterio.open(raster_path) as src:
        mask = src.read(1)
        transform = src.transform
        crs = src.crs

    geometries = [
        shape(geom)
        for geom, value in features.shapes(mask.astype("uint8"), mask=mask.astype(bool), transform=transform)
        if value == 1
    ]
    if not geometries:
        print("[vectorize] No se encontraron pixeles de cambio.")
        return 0

    gdf = gpd.GeoDataFrame(geometry=geometries, crs=crs)
    gdf["area_m2"] = gdf.geometry.area
    gdf = gdf[gdf["area_m2"] >= min_area].copy()
    if simplify > 0:
        gdf["geometry"] = gdf.geometry.simplify(simplify, preserve_topology=True)

    ensure_dir(out_path.parent)
    gdf.to_file(out_path, driver="GeoJSON")
    return len(gdf)


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    root = Path(config["_repo_root"])

    raster_path = Path(args.raster) if args.raster else root / config["outputs"]["rasters"] / "cambio_gaza.tif"
    if not raster_path.exists():
        raise SystemExit(f"No existe {raster_path}. Ejecuta primero la inferencia.")

    out_path = root / config["outputs"]["vectors"] / "cambio_gaza.geojson"
    count = vectorize_mask(raster_path, out_path, args.min_area, args.simplify)
    print(f"[vectorize] {count} poligonos guardados en {out_path}")


if __name__ == "__main__":
    main()
