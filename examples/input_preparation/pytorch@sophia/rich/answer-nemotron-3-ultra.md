# nemotron-3-ultra — pytorch@sophia, rich arm

Input preparation. **FAIL** (correctness 2/2, completeness 2/2, usability 0/2, fatal; 0 of 9 requirements violated).

````
train_resnet50.py
```python
import os
import argparse
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import CosineAnnealingLR
from torch.utils.data import DataLoader, DistributedSampler
from torch.utils.data.distributed import DistributedSampler
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.distributed import init_process_group, destroy_process_group
from torch.cuda.amp import GradScaler, autocast
import torchvision
from torchvision import transforms
import torchvision.models as models

def setup_distributed():
    """Initialize distributed training using environment variables set by MPI launcher."""
    init_process_group(backend="nccl", init_method="env://")
    local_rank = int(os.environ["LOCAL_RANK"])
    torch.cuda.set_device(local_rank)
    return local_rank

def cleanup_distributed():
    destroy_process_group()

def get_data_loaders(data_dir, batch_size, local_rank, world_size):
    """Create training data loader with distributed sampler."""
    transform = transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    train_dataset = torchvision.datasets.ImageFolder(root=data_dir, transform=transform)
    train_sampler = DistributedSampler(train_dataset, num_replicas=world_size, rank=local_rank, shuffle=True)
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        sampler=train_sampler,
        num_workers=8,
        pin_memory=True,
        drop_last=True,
    )
    return train_loader, train_sampler

def load_checkpoint(model, optimizer, scheduler, scaler, checkpoint_path, local_rank):
    """Load checkpoint if it exists."""
    start_epoch = 0
    if os.path.isfile(checkpoint_path):
        map_location = {"cuda:0": f"cuda:{local_rank}"}
        checkpoint = torch.load(checkpoint_path, map_location=map_location)
        model.load_state_dict(checkpoint["model_state_dict"])
        optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
        scheduler.load_state_dict(checkpoint["scheduler_state_dict"])
        scaler.load_state_dict(checkpoint["scaler_state_dict"])
        start_epoch = checkpoint["epoch"] + 1
        print(f"[Rank {local_rank}] Loaded checkpoint from epoch {checkpoint['epoch']}")
    else:
        print(f"[Rank {local_rank}] No checkpoint found at {checkpoint_path}, starting from scratch")
    return start_epoch

def save_checkpoint(model, optimizer, scheduler, scaler, epoch, checkpoint_path, local_rank):
    """Save checkpoint (only on rank 0)."""
    if local_rank == 0:
        torch.save({
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "scheduler_state_dict": scheduler.state_dict(),
            "scaler_state_dict": scaler.state_dict(),
        }, checkpoint_path)
        print(f"[Rank 0] Saved checkpoint at epoch {epoch}")

def main():
    parser = argparse.ArgumentParser(description="Distributed ResNet-50 training with mixed precision")
    parser.add_argument("--data-dir", type=str, default="/eagle/MatGenome/bkowalski/pytorch_run/imagenet_subset",
                        help="Path to training dataset (ImageFolder format)")
    parser.add_argument("--checkpoint-path", type=str, default="/eagle/MatGenome/bkowalski/pytorch_run/checkpoint.pt",
                        help="Path to checkpoint file for resume/save")
    parser.add_argument("--epochs", type=int, default=10, help="Total number of epochs")
    parser.add_argument("--batch-size", type=int, default=256, help="Batch size per GPU")
    parser.add_argument("--lr", type=float, default=0.1, help="Initial learning rate")
    parser.add_argument("--weight-decay", type=float, default=1e-4, help="Weight decay")
    parser.add_argument("--momentum", type=float, default=0.9, help="SGD momentum")
    args = parser.parse_args()

    local_rank = setup_distributed()
    world_size = int(os.environ["WORLD_SIZE"])
    device = torch.device(f"cuda:{local_rank}")

    torch.backends.cudnn.benchmark = True

    # Model
    model = models.resnet50(weights=None).to(device)
    model = DDP(model, device_ids=[local_rank], output_device=local_rank)

    # Mixed precision scaler
    scaler = GradScaler()

    # Optimizer and scheduler
    optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=args.momentum, weight_decay=args.weight_decay)
    scheduler = CosineAnnealingLR(optimizer, T_max=args.epochs)

    # Load checkpoint if exists
    start_epoch = load_checkpoint(model, optimizer, scheduler, scaler, args.checkpoint_path, local_rank)

    # Data
    train_loader, train_sampler = get_data_loaders(args.data_dir, args.batch_size, local_rank, world_size)

    # Loss
    criterion = nn.CrossEntropyLoss().to(device)

    # Training loop
    for epoch in range(start_epoch, args.epochs):
        train_sampler.set_epoch(epoch)
        model.train()
        running_loss = 0.0
        for i, (images, targets) in enumerate(train_loader):
            images = images.to(device, non_blocking=True)
            targets = targets.to(device, non_blocking=True)

            optimizer.zero_grad()
            with autocast():
                outputs = model(images)
                loss = criterion(outputs, targets)

            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

            running_loss += loss.item()

        scheduler.step()

        avg_loss = running_loss / len(train_loader)
        print(f"[Rank {local_rank}] Epoch {epoch+1}/{args.epochs} - Loss: {avg_loss:.4f}")

        # Save checkpoint at end of each epoch
        save_checkpoint(model, optimizer, scheduler, scaler, epoch, args.checkpoint_path, local_rank)

    cleanup_distributed()

if __name__ == "__main__":
    main()
```

This script is the primary input file: it defines the distributed training workflow, mixed-precision setup, checkpoint loading/saving, data loading with a distributed sampler, and the ResNet-50 model configuration matching the specified workload (100k images, batch size 256/GPU, 10 epochs). It reads the existing checkpoint from the working directory to resume training.
````
