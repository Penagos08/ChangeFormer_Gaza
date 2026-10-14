"""Descarga de imagenes Sentinel-2 L2A desde el Microsoft Planetary Computer.

Uso:
    python -m src.data.download_sentinel2 --config configs/gaza.yaml --period pre
    python -m src.data.download_sentinel2 --config configs/gaza.yaml --period post
"""

from __future__ import annotations

import argparse
from pathlib import Path

from src.data.stac_utils import load_stack, search_items, sort_by_cloud, write_raster
from src.utils.config import ensure_dir, load_config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Descarga Sentinel-2 L2A de Gaza.")
    parser.add_argument("--config", default="configs/gaza.yaml", help="Ruta al YAML de configuracion.")
    parser.add_argument("--period", choices=["pre", "post"], default="pre", help="Epoca a descargar.")
    parser.add_argument("--max-items", type=int, default=4, help="Numero maximo de items a combinar.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)

    s2 = config["sentinel2"]
    bbox = config["aoi"]["bbox_wgs84"]
    period = s2[args.period]
    epsg = int(str(config["project"]["crs"]).split(":")[1])

    print(f"[sentinel2] Buscando imagenes {args.period} entre {period['start']} y {period['end']}...")
    items = search_items(
        collection=s2["collection"],
        bbox=bbox,
        datetime_range=f"{period['start']}/{period['end']}",
        query={"eo:cloud_cover": {"lt": s2["max_cloud_cover"]}},
    )
    if not items:
        raise SystemExit(
            "No se encontraron imagenes para esa epoca. Ajusta las fechas o el maximo de nubosidad."
        )

    items = sort_by_cloud(items)[: args.max_items]
    print(f"[sentinel2] {len(items)} item(s) seleccionados, el menos nuboso: "
          f"{items[0].properties.get('eo:cloud_cover')}% de nubes")

    # Planetary Computer nombra los activos como B02, B03, B04, B08
    assets = [b.upper() for b in s2["bands"]]

    mosaic = load_stack(
        items=items,
        assets=assets,
        bbox=bbox,
        epsg=epsg,
        resolution=s2["resolution"],
        aggregate="median",
    )

    out_path = Path(config["_repo_root"]) / "data" / "raw" / "sentinel2" / f"gaza_s2_{args.period}.tif"
    ensure_dir(out_path.parent)
    write_raster(mosaic, out_path)
    print(f"[sentinel2] Guardado en {out_path}")


if __name__ == "__main__":
    main()
