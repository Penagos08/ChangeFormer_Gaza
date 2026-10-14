"""Comparacion del cambio detectado contra el dataset de referencia de UNOSAT.

Genera metricas de exactitud espacial: que proporcion de los danos reportados por
UNOSAT queda cubierta por el modelo (recall) y que proporcion de las detecciones
del modelo coincide con UNOSAT (precision).

Uso:
    python -m src.postprocess.stats --config configs/gaza.yaml
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.utils.config import ensure_dir, load_config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Metricas contra UNOSAT.")
    parser.add_argument("--config", default="configs/gaza.yaml", help="Ruta al YAML de configuracion.")
    parser.add_argument("--tolerance", type=float, default=20.0, help="Distancia de tolerancia en metros.")
    return parser.parse_args()


def _load_reference(config: dict, root: Path):
    import geopandas as gpd

    path = root / config["unosat"]["vector_path"]
    if not path.exists():
        raise SystemExit(
            f"No existe {path}. Descarga el GDB desde HDX y ejecuta "
            "'python -m src.data.unosat --config configs/gaza.yaml'."
        )
    return gpd.read_file(path).to_crs(config["project"]["crs"])


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    root = Path(config["_repo_root"])
    crs = config["project"]["crs"]

    import geopandas as gpd

    reference = _load_reference(config, root)
    change_path = root / config["outputs"]["vectors"] / "cambio_gaza.geojson"
    if not change_path.exists():
        raise SystemExit("Falta el GeoJSON de cambio. Ejecuta la vectorizacion primero.")
    change = gpd.read_file(change_path).to_crs(crs)

    reference_points = reference.geometry.representative_point()
    change_union = change.geometry.union_all() if hasattr(change.geometry, "union_all") else change.geometry.unary_union

    buffer = change_union.buffer(args.tolerance)
    recall_hits = reference_points.within(buffer).sum()
    recall = float(recall_hits) / max(len(reference_points), 1)

    precision_hits = 0
    ref_union = reference.geometry.union_all() if hasattr(reference.geometry, "union_all") else reference.geometry.unary_union
    for geom in change.geometry:
        if geom.representative_point().distance(ref_union) <= args.tolerance:
            precision_hits += 1
    precision = float(precision_hits) / max(len(change), 1)

    metrics = {
        "referencia_features": int(len(reference)),
        "detecciones_modelo": int(len(change)),
        "recall_unosat": round(recall, 4),
        "precision_unosat": round(precision, 4),
        "tolerancia_m": args.tolerance,
    }

    reports_dir = ensure_dir(root / config["outputs"]["reports"])
    (reports_dir / "metricas_unosat.json").write_text(
        json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    lines = [
        "# Metricas contra UNOSAT",
        "",
        f"- Referencias de dano (UNOSAT): {metrics['referencia_features']}",
        f"- Detecciones del modelo: {metrics['detecciones_modelo']}",
        f"- Recall (danos cubiertos): {metrics['recall_unosat']:.2%}",
        f"- Precision (detecciones confirmadas): {metrics['precision_unosat']:.2%}",
        f"- Tolerancia espacial: {metrics['tolerancia_m']} m",
    ]
    (reports_dir / "metricas_unosat.md").write_text("\n".join(lines), encoding="utf-8")
    print("[stats] " + " | ".join(lines[2:]))


if __name__ == "__main__":
    main()
