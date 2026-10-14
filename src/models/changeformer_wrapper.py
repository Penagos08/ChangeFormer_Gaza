"""Envoltura de ChangeFormer para inferencia sobre pares antes/despues.

Carga el modelo oficial definido en `third_party/ChangeFormer` (submodulo git),
sus pesos preentrenados y expone una interfaz simple que recibe imagenes RGB en
rango 0-1 y devuelve la probabilidad de cambio por pixel.

Referencia: Bandara y Patel (2022), ChangeFormer, IGARSS. arXiv:2201.01293.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

from src.utils.config import REPO_ROOT

CHANGEFORMER_ROOT = REPO_ROOT / "third_party" / "ChangeFormer"
STATE_DICT_KEYS = ("model_G_state_dict", "state_dict", "model")


def _add_changeformer_to_path() -> None:
    """Inserta el repositorio oficial en sys.path para importar su red."""
    root = str(CHANGEFORMER_ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)


def _extract_state_dict(checkpoint: dict) -> dict:
    """Extrae el diccionario de pesos de un checkpoint de ChangeFormer."""
    for key in STATE_DICT_KEYS:
        if isinstance(checkpoint, dict) and key in checkpoint:
            return checkpoint[key]
    # Si el checkpoint es directamente el state_dict
    if isinstance(checkpoint, dict) and all(hasattr(v, "shape") for v in checkpoint.values()):
        return checkpoint
    raise KeyError(
        f"No se encontro el state_dict en el checkpoint. Claves disponibles: {list(checkpoint.keys())}"
    )


def resolve_device(device: str = "auto") -> str:
    """Resuelve el dispositivo de computo."""
    import torch

    if device == "auto":
        return "cuda" if torch.cuda.is_available() else "cpu"
    return device


class ChangeFormerWrapper:
    """Interfaz de alto nivel para ChangeFormerV6."""

    def __init__(
        self,
        checkpoint: str | Path | None = None,
        embed_dim: int = 256,
        n_class: int = 2,
        device: str = "auto",
    ) -> None:
        import torch

        self.device = resolve_device(device)
        self.n_class = n_class
        self.embed_dim = embed_dim
        self.net = self._build_model(embed_dim)
        if checkpoint is not None:
            self.load_checkpoint(checkpoint)
        self.net.to(self.device)
        self.net.eval()
        print(f"[ChangeFormer] Modelo listo en {self.device} (embed_dim={embed_dim}).")

    def _build_model(self, embed_dim: int):
        _add_changeformer_to_path()
        from models.ChangeFormer import ChangeFormerV6

        return ChangeFormerV6(embed_dim=embed_dim)

    def load_checkpoint(self, checkpoint: str | Path) -> None:
        import torch

        path = Path(checkpoint)
        if not path.is_absolute():
            path = REPO_ROOT / path
        if not path.exists():
            raise FileNotFoundError(
                f"No existe el checkpoint {path}. Descarga los pesos ChangeFormerV6 (LEVIR-CD) "
                "y ajusta 'model.checkpoint' en configs/gaza.yaml."
            )
        checkpoint_data = torch.load(str(path), map_location=self.device)
        state_dict = _extract_state_dict(checkpoint_data)
        self.net.load_state_dict(state_dict)
        print(f"[ChangeFormer] Pesos cargados desde {path}.")

    def _prepare_batch(self, image_a: np.ndarray, image_b: np.ndarray):
        """Convierte pares RGB (H,W,3 en 0-1) en tensores NCHW normalizados (-1..1)."""
        import torch

        def to_tensor(image: np.ndarray):
            array = np.transpose(image[:, :, :3], (2, 0, 1)).astype(np.float32)
            array = (array - 0.5) / 0.5
            return torch.from_numpy(array).unsqueeze(0)

        return to_tensor(image_a).to(self.device), to_tensor(image_b).to(self.device)

    def predict_proba(self, image_a: np.ndarray, image_b: np.ndarray) -> np.ndarray:
        """Devuelve un mapa HxW con la probabilidad de cambio (clase 1)."""
        import torch

        tensor_a, tensor_b = self._prepare_batch(image_a, image_b)
        with torch.no_grad():
            logits = self.net(tensor_a, tensor_b)[-1]
            probabilities = torch.softmax(logits, dim=1)
        change_prob = probabilities[0, 1].cpu().numpy().astype(np.float32)
        return change_prob

    def predict_mask(
        self,
        image_a: np.ndarray,
        image_b: np.ndarray,
        threshold: float = 0.5,
    ) -> np.ndarray:
        """Devuelve una mascara binaria booleana (True = cambio)."""
        prob = self.predict_proba(image_a, image_b)
        return prob >= threshold
