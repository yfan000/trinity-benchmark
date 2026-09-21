# nemotron-3-ultra — pytorch@sophia, base arm

Input preparation. **FAIL** (correctness 0/2, completeness 2/2, usability 0/2, fatal; 1 of 9 requirements violated).

````
**File 1: `train_resnet50.py`** — Main distributed training script with checkpoint resume support

```python
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.utils.data.distributed import DistributedSampler
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.distributed import init_process_group, destroy_process_group
from torchvision import models, transforms, datasets
from torch.cuda.amp import GradScaler, autocast
import argparse


def ddp_setup():
    """
    Initialize the distributed process group.
    On Sophia (ALCF), launched via MPI; rank/world_size come from environment.
    """
    backend = "ccl" if torch.xpu.is_available() else "nccl"
    init_process_group(backend=backend)
    rank = int(os.environ["RANK"])
    local_rank = int(os.environ["LOCAL_RANK"])
    world_size = int(os.environ["WORLD_SIZE"])
    if torch.xpu.is_available():
        torch.xpu.set_device(local_rank)
    else:
        torch.cuda.set_device(local_rank)
    return rank, local_rank, world_size


def get_data_loaders(data_dir, batch_size, num_workers, world_size, rank):
    """
    Create train and validation data loaders with DistributedSampler.
    Assumes ImageNet-style layout: data_dir/train, data_dir/val
    """
    train_transform = transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    val_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    train_dataset = datasets.ImageFolder(os.path.join(data_dir, "train"), transform=train_transform)
    val_dataset = datasets.ImageFolder(os.path.join(data_dir, "val"), transform=val_transform)

    train_sampler = DistributedSampler(train_dataset, num_replicas=world_size, rank=rank, shuffle=True)
    val_sampler = DistributedSampler(val_dataset, num_replicas=world_size, rank=rank, shuffle=False)

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        sampler=train_sampler,
        num_workers=num_workers,
        pin_memory=True,
        drop_last=True,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        sampler=val_sampler,
        num_workers=num_workers,
        pin_memory=True,
        drop_last=False,
    )
    return train_loader, val_loader, train_sampler


def load_checkpoint(model, optimizer, scaler, checkpoint_path, device):
    """
    Load model, optimizer, scaler, epoch, and best accuracy from checkpoint.
    Returns (start_epoch, best_acc1).
    """
    if not os.path.isfile(checkpoint_path):
        raise FileNotFoundError(f"No checkpoint found at {checkpoint_path}")

    checkpoint = torch.load(checkpoint_path, map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"])
    optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
    if scaler is not None and "scaler_state_dict" in checkpoint:
        scaler.load_state_dict(checkpoint["scaler_state_dict"])
    start_epoch = checkpoint.get("epoch", 0) + 1
    best_acc1 = checkpoint.get("best_acc1", 0.0)
    print(f"[Rank {os.environ.get('RANK', 0)}] Loaded checkpoint from {checkpoint_path} (epoch {checkpoint.get('epoch', 0)}, best_acc1 {best_acc1:.2f})")
    return start_epoch, best_acc1


def save_checkpoint(model, optimizer, scaler, epoch, best_acc1, is_best, checkpoint_dir, rank):
    """
    Save checkpoint (only rank 0 writes to avoid corruption).
    """
    if rank != 0:
        return
    os.makedirs(checkpoint_dir, exist_ok=True)
    state = {
        "epoch": epoch,
        "model_state_dict": model.module.state_dict() if isinstance(model, DDP) else model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "best_acc1": best_acc1,
    }
    if scaler is not None:
        state["scaler_state_dict"] = scaler.state_dict()
    filename = os.path.join(checkpoint_dir, f"checkpoint_epoch_{epoch}.pt")
    torch.save(state, filename)
    if is_best:
        best_path = os.path.join(checkpoint_dir, "model_best.pt")
        torch.save(state, best_path)
    print(f"[Rank {rank}] Saved checkpoint to {filename}")


def validate(model, val_loader, criterion, device, rank):
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0
    with torch.no_grad():
        for images, targets in val_loader:
            images = images.to(device, non_blocking=True)
            targets = targets.to(device, non_blocking=True)
            outputs = model(images)
            loss = criterion(outputs, targets)
            total_loss += loss.item() * images.size(0)
            _, predicted = outputs.max(1)
            correct += predicted.eq(targets).sum().item()
            total += targets.size(0)
    avg_loss = total_loss / total if total > 0 else 0.0
    acc1 = 100.0 * correct / total if total > 0 else 0.0
    return avg_loss, acc1


def train_one_epoch(model, train_loader, criterion, optimizer, scaler, device, epoch, rank, use_amp):
    model.train()
    train_loader.sampler.set_epoch(epoch)
    running_loss = 0.0
    correct = 0
    total = 0
    for batch_idx, (images, targets) in enumerate(train_loader):
        images = images.to(device, non_blocking=True)
        targets = targets.to(device, non_blocking=True)

        optimizer.zero_grad(set_to_none=True)
        if use_amp:
            with autocast(device_type=device.type):
                outputs = model(images)
                loss = criterion(outputs, targets)
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            outputs = model(images)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

        running_loss += loss.item() * images.size(0)
        _, predicted = outputs.max(1)
        correct += predicted.eq(targets).sum().item()
        total += targets.size(0)

        if batch_idx % 50 == 0 and rank == 0:
            print(f"Epoch {epoch} Batch {batch_idx}/{len(train_loader)} Loss: {loss.item():.4f}")

    avg_loss = running_loss / total if total > 0 else 0.0
    acc1 = 100.0 * correct / total if total > 0 else 0.0
    return avg_loss, acc1


def main():
    parser = argparse.ArgumentParser(description="ResNet-50 mixed-precision training with checkpoint resume")
    parser.add_argument("--data-dir", type=str, required=True, help="Path to ImageNet-style dataset (train/val subdirs)")
    parser.add_argument("--checkpoint-dir", type=str, default="/eagle/MatGenome/bkowalski/pytorch_run/checkpoints",
                        help="Directory to read/write checkpoints")
    parser.add_argument("--resume", type=str, default="",
                        help="Checkpoint filename (in --checkpoint-dir) to resume from; empty = fresh start")
    parser.add_argument("--epochs", type=int, default=10, help="Total epochs to run")
    parser.add_argument("--batch-size", type=int, default=256, help="Per-GPU batch size")
    parser.add_argument("--lr", type=float, default=0.1, help="Initial learning rate")
    parser.add_argument("--momentum", type=float, default=0.9, help="SGD momentum")
    parser.add_argument("--weight-decay", type=float, default=1e-4, help="Weight decay")
    parser.add_argument("--num-workers", type=int, default=8, help="Data loader workers per process")
    parser.add_argument("--no-amp", action="store_true", help="Disable automatic mixed precision")
    args = parser.parse_args()

    rank, local_rank, world_size = ddp_setup()
    device = torch.device(f"xpu:{local_rank}" if torch.xpu.is_available() else f"cuda:{local_rank}")
    use_amp = not args.no_amp and (torch.cuda.is_available() or torch.xpu.is_available())

    # Model
    model = models.resnet50(weights=None).to(device)
    model = DDP(model, device_ids=[local_rank] if not torch.xpu.is_available() else None)

    # Loss, optimizer, scheduler, scaler
    criterion = nn.CrossEntropyLoss().to(device)
    optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=args.momentum, weight_decay=args.weight_decay)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)
    scaler = GradScaler() if use_amp else None

    # Data
    train_loader, val_loader, train_sampler = get_data_loaders(
        args.data_dir, args.batch_size, args.num_workers, world_size, rank
    )

    # Resume from checkpoint if provided
    start_epoch = 0
    best_acc1 = 0.0
    if args.resume:
        checkpoint_path = os.path.join(args.checkpoint_dir, args.resume)
        start_epoch, best_acc1 = load_checkpoint(model, optimizer, scaler, checkpoint_path, device)
        # Step scheduler to catch up
        for _ in range(start_epoch):
            scheduler.step()

    # Training loop
    for epoch in range(start_epoch, args.epochs):
        train_loss, train_acc = train_one_epoch(
            model, train_loader, criterion, optimizer, scaler, device, epoch, rank, use_amp
        )
        val_loss, val_acc = validate(model, val_loader, criterion, device, rank)
        scheduler.step()

        if rank == 0:
            print(f"Epoch {epoch}: Train Loss {train_loss:.4f} Acc {train_acc:.2f}% | Val Loss {val_loss:.4f} Acc {val_acc:.2f}%")

        is_best = val_acc > best_acc1
        best_acc1 = max(best_acc1, val_acc)
        save_checkpoint(model, optimizer, scaler, epoch, best_acc1, is_best, args.checkpoint_dir, rank)

    destroy_process_group()


if __name__ == "__main__":
    main()
```

**Why needed:** This is the complete training script that implements distributed ResNet-50 training with mixed precision (AMP), checkpoint saving/loading for resume, cosine-annealing LR schedule, and validation. It reads the checkpoint from the working directory and resumes epoch, optimizer, scaler, and best-accuracy state. Designed for Sophia's Intel GPUs (uses `ccl` backend when XPU available, falls back to `nccl`).

---

**File 2: `launch_train.sh`** — Launch wrapper (not a scheduler script; sets env vars and invokes the Python entry point)

```bash
#!/usr/bin/env bash
# Launch script for distributed ResNet-50 training on Sophia (ALCF)
# Intended to be called from within an MPI allocation (e.g., mpirun, srun, or pbsdsh)
# Sets required environment variables for torch.distributed and oneCCL

set -euo pipefail

# ── User-configurable ──────────────────────────────────────────────
DATA_DIR="/eagle/MatGenome/bkowalski/pytorch_run/imagenet_subset_100k"
CHECKPOINT_DIR="/eagle/MatGenome/bkowalski/pytorch_run/checkpoints"
RESUME_CHECKPOINT=""   # e.g., "checkpoint_epoch_3.pt" to resume; empty = fresh start
EPOCHS=10
BATCH_SIZE=256
LR=0.1
NUM_WORKERS=8
# ────────────────────────────────────────────────────────────────────

# Detect MPI-provided ranks
export RANK=${PMI_RANK:-${OMPI_COMM_WORLD_RANK:-0}}
export WORLD_SIZE=${PMI_SIZE:-${OMPI_COMM_WORLD_SIZE:-1}}
export LOCAL_RANK=${MPI_LOCALRANKID:-${OMPI_COMM_WORLD_LOCAL_RANK:-0}}
export MASTER_ADDR=${MASTER_ADDR:-$(hostname -i | awk '{print $1}')}
export MASTER_PORT=${MASTER_PORT:-29500}

# oneCCL / XPU settings for Sophia (Intel PVC)
export CCL_ATL_TRANSPORT=mpi
export SYCL_PI_LEVEL_ZERO_USE_IMMEDIATE_COMMANDLISTS=1
export ZE_FLAT_DEVICE_HIERARCHY=COMPOSITE

# Ensure checkpoint directory exists
mkdir -p "${CHECKPOINT_DIR}"

# Invoke training script
exec python train_resnet50.py \
    --data-dir "${DATA_DIR}" \
    --checkpoint-dir "${CHECKPOINT_DIR}" \
    --resume "${RESUME_CHECKPOINT}" \
    --epochs "${EPOCHS}" \
    --batch-size "${BATCH_SIZE}" \
    --lr "${LR}" \
    --num-workers "${NUM_WORKERS}"
```

**Why needed:** Provides the exact launch-time configuration (dataset path, checkpoint directory, resume filename, hyperparameters) and sets the MPI/oneCCL environment variables required for `torch.distributed` initialization on Sophia. It is sourced/invoked by the job script (not written here) and ensures the Python script receives consistent arguments and environment across all ranks.
````
