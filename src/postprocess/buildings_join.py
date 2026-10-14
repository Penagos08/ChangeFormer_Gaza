"""Cruce de los poligonos de cambio con las huellas de edificios.

Determina que edificios quedaron afectados segun la fraccion de su area cubierta
por el cambio detectado.

Uso:
    python -m src.postprocess.buildings_join --config configs/gaza.yaml
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.utils.config import ensure_dir, load_config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cruza cambio detectado con huellas de edificios.")
    parser.add_argument("--config", default="configs/gaza.yaml", help="Ruta al YAML de configuracion.")
    parser.add_argument("--coverage", type=float, default=0.30, help="Fraccion de area para marcar un edificio como afectado.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    root = Path(config["_repo_root"])
    crs = config["project"]["crs"]

    footprints_path = root / "data" / "raw" / "footprints" / "gaza_buildings.geojson"
    change_path = root / config["outputs"]["vectors"] / "cambio_gaza.geojson"
    for path in (footprints_path, change_path):
        if not path.exists():
            raise SystemExit(
                f"No existe {path}. Ejecuta la descarga de huellas y la inferencia antes de este paso."
            )

    import geopandas as gpd

    buildings = gpd.read_file(footprints_path).to_crs(crs)
    change = gpd.read_file(change_path).to_crs(crs)
    print(f"[buildings] {len(buildings)} huellas y {len(change)} poligonos de cambio.")

    change_union = change.geometry.union_all() if hasattr(change.geometry, "union_all") else change.geometry.unary_union

    building_area = buildings.geometry.area
    inter_area = buildings.geometry.intersection(change_union).area
    buildings["cobertura_cambio"] = (inter_area / building_area.replace(0, float("nan"))).fillna(0.0)
    buildings["afectado"] = buildings["cobertura_cambio"] >= args.coverage

    affected = buildings[buildings["afectado"]].copy()
    out_path = root / config["outputs"]["vectors"] / "edificios_afectados.geojson"
    ensure_dir(out_path.parent)
    affected.to_file(out_path, driver="GeoJSON")

    summary = {
        "huellas_totales": int(len(buildings)),
        "huellas_afectadas": int(len(affected)),
        "porcentaje_afectado": round(100.0 * len(affected) / max(len(buildings), 1), 2),
        "umbral_cobertura": args.coverage,
    }
    summary_path = root / config["outputs"]["reports"] / "edificios_resumen.json"
    ensure_dir(summary_path.parent)
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[buildings] Resumen: {summary}")


if __name__ == "__main__":
    main()
