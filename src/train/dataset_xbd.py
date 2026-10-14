"""Dataset xBD (xView2) para el ajuste fino de ChangeFormer.

xBD organiza las imagenes como pares antes/despues con etiquetas de 5 clases:
0 = fondo, 1 = sin dano, 2 = dano menor, 3 = dano mayor, 4 = destruido. Para la
deteccion de edificios destruidos se binariza la etiqueta: {2, 3, 4} pasan a la
clase 1 (cambio).

Referencia: Gupta et al. (2019), xBD, xView2 Challenge.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

DAMAGE_CLASSES = {2, 3, 4}


class XBDDataset:
    """Dataset de pares antes/despues de xBD.

    Se implementa con acceso diferido (import de torch dentro de __init__) para no
    exigir PyTorch al importar el modulo.
    """

    def __init__(self, root: str | Path, split: str = "train", img_size: int = 256, binary: bool = True):
        import torch
        from torch.utils.data import Dataset

        self._torch = torch
        self.img_size = img_size
        self.binary = binary
        root = Path(root) / split
        self.image_dir = root / "images"
        self.label_dir = root / "labels"
        if not self.image_dir.exists():
            raise FileNotFoundError(
                f"No existe {self.image_dir}. Descarga xBD desde https://xview2.org/dataset y coloca "
                f"la estructura train/val -> images/ + labels/ en {root.parent}."
            )
        self.post_images = sorted(self.image_dir.glob("*_post_disaster.png"))
        if not self.post_images:
            raise FileNotFoundError(f"No se encontraron imagenes *_post_disaster.png en {self.image_dir}.")

        class _Impl(Dataset):
            def __len__(inner) -> int:
                return len(self.post_images)

            def __getitem__(inner, index: int):
                return self._load(index)

        self._dataset = _Impl()

    def _load(self, index: int):
        from PIL import Image
        import torchvision.transforms.functional as TF

        post_path = self.post_images[index]
        pre_path = post_path.with_name(post_path.name.replace("_post_disaster", "_pre_disaster"))
        label_path = self.label_dir / post_path.name

        image_a = Image.open(pre_path).convert("RGB")
        image_b = Image.open(post_path).convert("RGB")
        label = Image.open(label_path) if label_path.exists() else None

        image_a = TF.resize(image_a, [self.img_size, self.img_size])
        image_b = TF.resize(image_b, [self.img_size, self.img_size])
        tensor_a = TF.normalize(TF.to_tensor(image_a), mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        tensor_b = TF.normalize(TF.to_tensor(image_b), mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])

        if label is not None:
            label = TF.resize(label, [self.img_size, self.img_size], interpolation=TF.InterpolationMode.NEAREST)
        label_array = np.array(label) if label is not None else np.zeros((self.img_size, self.img_size), np.uint8)
        if self.binary:
            target = np.isin(label_array, list(DAMAGE_CLASSES)).astype(np.int64)
        else:
            target = label_array.astype(np.int64)

        return {
            "A": tensor_a,
            "B": tensor_b,
            "L": self._torch.from_numpy(target),
            "name": post_path.name,
        }

    def as_dataset(self):
        return self._dataset
