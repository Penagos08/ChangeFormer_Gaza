"""Ajuste fino de ChangeFormerV6 con el dataset xBD.

Pensado para ejecutarse en una GPU en la nube (por ejemplo Google Colab), ya que
la GPU local del proyecto es demasiado modesta para entrenar. Optimiza una perdida
de entropia cruzada con pesos de clase y guarda el mejor checkpoint segun el F1.

Uso:
    python -m src.train.finetune_xbd --config configs/gaza.yaml \
        --dataset-root data/external/xbd --epochs 50
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from src.models.changeformer_wrapper import STATE_DICT_KEYS, _add_changeformer_to_path, resolve_device
from src.train.dataset_xbd import XBDDataset
from src.utils.config import ensure_dir, load_config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ajuste fino de ChangeFormer con xBD.")
    parser.add_argument("--config", default="configs/gaza.yaml", help="Ruta al YAML de configuracion.")
    parser.add_argument("--dataset-root", default=None, help="Raiz del dataset xBD (sobreescribe el YAML).")
    parser.add_argument("--pretrained", default=None, help="Pesos preentrenados de partida.")
    parser.add_argument("--epochs", type=int, default=None)
    parser.add_argument("--batch-size", type=int, default=None)
    parser.add_argument("--lr", type=float, default=None)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--device", default="auto")
    return parser.parse_args()


def _dice_loss_from_logits(logits, target, eps: float = 1e-6):
    import torch

    prob = torch.softmax(logits, dim=1)[:, 1]
    target = target.float()
    intersection = (prob * target).sum()
    return 1 - (2 * intersection + eps) / (prob.sum() + target.sum() + eps)


def _metrics(logits, target):
    import torch

    pred = torch.argmax(logits, dim=1)
    tp = ((pred == 1) & (target == 1)).sum().item()
    fp = ((pred == 1) & (target == 0)).sum().item()
    fn = ((pred == 0) & (target == 1)).sum().item()
    iou = tp / max(tp + fp + fn, 1)
    f1 = 2 * tp / max(2 * tp + fp + fn, 1)
    return iou, f1


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    ft = config["finetune"]
    model_cfg = config["model"]

    dataset_root = args.dataset_root or ft["dataset_root"]
    epochs = args.epochs or ft["epochs"]
    batch_size = args.batch_size or ft["batch_size"]
    lr = args.lr or ft["lr"]
    output_dir = Path(args.output_dir or ft["output_dir"])
    if not output_dir.is_absolute():
        output_dir = Path(config["_repo_root"]) / output_dir
    ensure_dir(output_dir)

    import torch
    from torch.utils.data import DataLoader

    device = resolve_device(args.device)

    train_set = XBDDataset(dataset_root, split="train", img_size=ft["img_size"]).as_dataset()
    val_set = XBDDataset(dataset_root, split="val", img_size=ft["img_size"]).as_dataset()
    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True, num_workers=ft["num_workers"])
    val_loader = DataLoader(val_set, batch_size=batch_size, shuffle=False, num_workers=ft["num_workers"])
    print(f"[finetune] train={len(train_set)} val={len(val_set)} device={device}")

    _add_changeformer_to_path()
    from models.ChangeFormer import ChangeFormerV6

    net = ChangeFormerV6(embed_dim=model_cfg["embed_dim"])
    if args.pretrained:
        checkpoint = torch.load(args.pretrained, map_location="cpu")
        for key in STATE_DICT_KEYS:
            if isinstance(checkpoint, dict) and key in checkpoint:
                net.load_state_dict(checkpoint[key])
                break
        print(f"[finetune] Pesos iniciales cargados de {args.pretrained}")
    net.to(device)

    weight = torch.tensor([1.0, 6.0], device=device)
    criterion = torch.nn.CrossEntropyLoss(weight=weight)
    optimizer = torch.optim.AdamW(net.parameters(), lr=lr, weight_decay=1e-4)

    best_f1 = -1.0
    for epoch in range(1, epochs + 1):
        net.train()
        running = 0.0
        for batch in train_loader:
            a, b, target = batch["A"].to(device), batch["B"].to(device), batch["L"].to(device)
            optimizer.zero_grad()
            logits = net(a, b)[-1]
            loss = criterion(logits, target) + _dice_loss_from_logits(logits, target)
            loss.backward()
            optimizer.step()
            running += loss.item()
        train_loss = running / max(len(train_loader), 1)

        net.eval()
        ious, f1s = [], []
        with torch.no_grad():
            for batch in val_loader:
                a, b, target = batch["A"].to(device), batch["B"].to(device), batch["L"].to(device)
                logits = net(a, b)[-1]
                iou, f1 = _metrics(logits, target)
                ious.append(iou)
                f1s.append(f1)
        val_iou = float(np.mean(ious)) if ious else 0.0
        val_f1 = float(np.mean(f1s)) if f1s else 0.0
        print(f"[finetune] epoca {epoch:03d} loss={train_loss:.4f} val_iou={val_iou:.4f} val_f1={val_f1:.4f}")

        if val_f1 > best_f1:
            best_f1 = val_f1
            torch.save({"model_G_state_dict": net.state_dict()}, output_dir / "best_ckpt.pt")
            print(f"[finetune] Nuevo mejor F1={best_f1:.4f}; checkpoint guardado.")

    print(f"[finetune] Terminado. Mejor F1 de validacion: {best_f1:.4f}")


if __name__ == "__main__":
    main()
