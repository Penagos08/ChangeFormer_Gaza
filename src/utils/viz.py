"""Utilidades de visualizacion de resultados de deteccion de cambios."""

from __future__ import annotations

from pathlib import Path

import numpy as np


def save_comparison(
    image_a: np.ndarray,
    image_b: np.ndarray,
    mask: np.ndarray,
    out_path: str | Path,
    title: str = "",
) -> Path:
    """Guarda una figura con imagen antes, despues y mascara superpuesta.

    Parametros
    ----------
    image_a, image_b: arreglos HxWx3 en rango 0-1.
    mask: arreglo HxW booleano (True = cambio).
    """
    import matplotlib.pyplot as plt

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    overlay = image_b.copy()
    overlay[mask] = overlay[mask] * 0.4 + np.array([1.0, 0.0, 0.0]) * 0.6
    overlay = np.clip(overlay, 0, 1)

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    axes[0].imshow(image_a)
    axes[0].set_title("Antes")
    axes[1].imshow(image_b)
    axes[1].set_title("Despues")
    axes[2].imshow(overlay)
    axes[2].set_title("Cambio detectado")
    for axis in axes:
        axis.axis("off")
    if title:
        fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path
