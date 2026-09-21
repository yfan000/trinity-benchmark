# gemma-4-31b — pytorch@sophia, rich arm

Input preparation. **FAIL** (correctness 0/2, completeness 2/2, usability 0/2, fatal; 2 of 9 requirements violated).

````
`train_resnet50.py`
```python
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Subset
from torch.utils.data.distributed import DistributedSampler
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.distributed import init_process_group, destroy_process_group
from torchvision import datasets, transforms, models
from torch.cuda.amp import GradScaler, autocast

def setup(rank, world_size):
    # MPI provides these environment variables on Sophia/ALCF
    os.environ["MASTER_ADDR"] = os.environ["MASTER_ADDR"] 
    os.environ["MASTER_PORT"] = os.environ["MASTER_PORT"]
    torch.cuda.set_device(rank)
    init_process_group(backend="nccl", rank=rank, world_size=world_size)

def main():
    # Distributed environment setup
    rank = int(os.environ["RANK"])
    local_rank = int(os.environ["LOCAL_RANK"])
    world_size = int(os.environ["WORLD_SIZE"])
    setup(local_rank, world_size)

    # Hyperparameters
    batch_size = 256
    epochs = 10
    checkpoint_path = "/eagle/MatGenome/bkowalski/pytorch_run/checkpoint.pth"
    
    # Data pipeline
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    
    # Load subset of 100,000 images
    full_dataset = datasets.ImageFolder(root="/eagle/MatGenome/bkowalski/pytorch_run/data", transform=transform)
    indices = list(range(100000))
    train_dataset = Subset(full_dataset, indices)
    
    sampler = DistributedSampler(train_dataset, num_replicas=world_size, rank=rank)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, sampler=sampler, num_workers=16)

    # Model, Optimizer, and Mixed Precision Scaler
    model = models.resnet50(weights=None).cuda(local_rank)
    model = DDP(model, device_ids=[local_rank])
    optimizer = optim.SGD(model.parameters(), lr=0.1, momentum=0.9)
    scaler = GradScaler()
    start_epoch = 0

    # Restart logic: Load existing checkpoint
    if os.path.exists(checkpoint_path):
        map_location = {"cuda:%d" % 0: "cuda:%d" % local_rank}
        checkpoint = torch.load(checkpoint_path, map_location=map_location)
        model.module.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        scaler.load_state_dict(checkpoint['scaler_state_dict'])
        start_epoch = checkpoint['epoch']
        print(f"Rank {rank} resumed from epoch {start_epoch}")

    # Training loop
    model.train()
    for epoch in range(start_epoch, epochs):
        sampler.set_epoch(epoch)
        for i, (images, targets) in enumerate(train_loader):
            images, targets = images.cuda(local_rank), targets.cuda(local_rank)
            
            optimizer.zero_grad()
            with autocast():
                outputs = model(images)
                loss = nn.CrossEntropyLoss()(outputs, targets)
            
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

        # Save checkpoint at end of epoch
        if rank == 0:
            torch.save({
                'epoch': epoch + 1,
                'model_state_dict': model.module.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'scaler_state_dict': scaler.state_dict(),
            }, checkpoint_path)

    destroy_process_group()

if __name__ == "__main__":
    main()
```
The main execution script defining the distributed mixed-precision training logic and the checkpoint loading mechanism.

`checkpoint.pth`
```
[Binary data produced at runtime]
```
The existing state file containing the model weights, optimizer state, and epoch count required to resume training.
````
