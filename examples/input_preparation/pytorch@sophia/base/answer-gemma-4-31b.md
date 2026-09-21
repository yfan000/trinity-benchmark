# gemma-4-31b — pytorch@sophia, base arm

Input preparation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 9 requirements violated).

````
**resnet_train.py**
```python
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms, models
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.distributed import init_process_group, destroy_process_group
from torch.utils.data.distributed import DistributedSampler
from torch.cuda.amp import GradScaler, autocast

def setup(rank, world_size):
    os.environ['MASTER_ADDR'] = 'localhost'
    os.environ['MASTER_PORT'] = '12355'
    torch.cuda.set_device(rank)
    init_process_group(backend='nccl', rank=rank, world_size=world_size)

def cleanup():
    destroy_process_group()

def train():
    # Configuration
    working_dir = "/eagle/MatGenome/bkowalski/pytorch_run"
    checkpoint_path = os.path.join(working_dir, "checkpoint.pth")
    batch_size = 256
    epochs = 10
    subset_size = 100000

    # MPI/Distributed Setup
    rank = int(os.environ["RANK"])
    world_size = int(os.environ["WORLD_SIZE"])
    setup(rank, world_size)

    # Data Loading
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    
    full_dataset = datasets.ImageFolder(root='/eagle/MatGenome/bkowalski/pytorch_run/data', transform=transform)
    subset_dataset = Subset(full_dataset, range(subset_size))
    sampler = DistributedSampler(subset_dataset, num_replicas=world_size, rank=rank)
    train_loader = DataLoader(subset_dataset, batch_size=batch_size, sampler=sampler)

    # Model, Optimizer, and Scaler for Mixed Precision
    model = models.resnet50().cuda(rank)
    model = DDP(model, device_ids=[rank])
    optimizer = optim.SGD(model.parameters(), lr=0.1, momentum=0.9)
    scaler = GradScaler()
    start_epoch = 0

    # Restart Logic
    if os.path.exists(checkpoint_path):
        checkpoint = torch.load(checkpoint_path, map_location=f'cuda:{rank}')
        model.module.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        scaler.load_state_dict(checkpoint['scaler_state_dict'])
        start_epoch = checkpoint['epoch']
        if rank == 0:
            print(f"Resuming from epoch {start_epoch}")

    criterion = nn.CrossEntropyLoss().cuda(rank)

    for epoch in range(start_epoch, epochs):
        sampler.set_epoch(epoch)
        model.train()
        for images, targets in train_loader:
            images, targets = images.cuda(rank), targets.cuda(rank)
            
            optimizer.zero_grad()
            with autocast():
                output = model(images)
                loss = criterion(output, targets)
            
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

        if rank == 0:
            torch.save({
                'epoch': epoch + 1,
                'model_state_dict': model.module.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'scaler_state_dict': scaler.state_dict(),
            }, checkpoint_path)

    cleanup()

if __name__ == "__main__":
    train()
```
This is the primary execution script that implements the ResNet-50 architecture, distributed training logic, mixed-precision scaling, and the checkpoint loading mechanism for the restart.

**checkpoint.pth**
(Runtime-generated binary file)
This file is produced during the previous interrupted run and contains the saved model weights, optimizer state, scaler state, and the last completed epoch number.
````
