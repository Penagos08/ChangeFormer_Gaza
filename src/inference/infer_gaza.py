"""Pipeline de inferencia completo para la Franja de Gaza.

Carga el par Sentinel-2 antes/despues, ejecuta ChangeFormer por teselas, guarda
el mapa binario de cambio y una figura de comparacion.

Uso:
    python -m src.inference.infer_gaza --config configs/gaza.yaml
"""

from __future__ import annotations

import argparse
from pathlib import Path

from src.data.prepare import load_sentinel_pair
from src.inference.predict_tiles import predict_change_map, save_change_map
from src.models.changeformer_wrapper import ChangeFormerWrapper
from src.utils.config import ensure_dir, load_config
from src.utils.viz import save_comparison


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inferencia de cambio en Gaza con ChangeFormer.")
    parser.add_argument("--config", default="configs/gaza.yaml", help="Ruta al YAML de configuracion.")
    parser.add_argument("--checkpoint", default=None, help="Ruta a los pesos (sobreescribe el YAML).")
    parser.add_argument("--max-preview", type=int, default=1, help="Numero de figuras de vista previa.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)

    tiling = config["tiling"]
    inference = config["inference"]
    model_cfg = config["model"]

    print("[infer] Cargando par Sentinel-2 antes/despues...")
    pre_rgb, post_rgb, profile = load_sentinel_pair(config)
    print(f"[infer] Dimensiones del raster: {pre_rgb.shape[:2]}")

    checkpoint = args.checkpoint or model_cfg["checkpoint"]
    model = ChangeFormerWrapper(
        checkpoint=checkpoint,
        embed_dim=model_cfg["embed_dim"],
        n_class=model_cfg["n_class"],
        device=inference["device"],
    )

    mask, prob = predict_change_map(
        pre_rgb,
        post_rgb,
        model,
        tile_size=tiling["size"],
        stride=tiling["stride"],
        threshold=inference["threshold"],
    )

    root = Path(config["_repo_root"])
    raster_dir = ensure_dir(root / config["outputs"]["rasters"])
    out_raster = raster_dir / "cambio_gaza.tif"
    out_prob = raster_dir / "cambio_gaza_prob.tif"
    save_change_map(mask, prob, profile, out_raster, out_prob)
    print(f"[infer] Mapa de cambio guardado en {out_raster}")

    if args.max_preview > 0:
        maps_dir = ensure_dir(root / config["outputs"]["maps"])
        save_comparison(pre_rgb, post_rgb, mask, maps_dir / "vista_previa_gaza.png", title="Gaza: cambio detectado")
        print(f"[infer] Figura de vista previa en {maps_dir / 'vista_previa_gaza.png'}")


if __name__ == "__main__":
    main()
