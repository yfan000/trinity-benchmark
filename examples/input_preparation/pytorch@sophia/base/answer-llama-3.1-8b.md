# llama-3.1-8b — pytorch@sophia, base arm

Input preparation. **FAIL** (correctness 2/2, completeness 1/2, usability 2/2; 2 of 9 requirements violated).

````
Based on the provided example and the requirements of the workload, the following input files are necessary to restart a distributed mixed-precision ResNet-50 training job from an existing checkpoint:

### `config.py`
```python
# config.py
# Configuration file for the application

# System parameters
num_gpus = 8
num_nodes = 1
world_size = num_gpus * num_nodes
node_rank = 0
gpu_rank = 0
save_every = 2  # Save the model every 2 epochs

# Model parameters
model_name = "resnet50"
num_epochs = 10

# Data parameters
batch_size = 256
train_dataset_name = "imagenet_subset"

# Mixed precision training parameters
use_mixed_precision = True
```

### `datautils.py`
```python
# datautils.py
# Utility functions for data loading and processing

import os
import torch
from torch.utils.data import Dataset

class MyTrainDataset(Dataset):
    def __init__(self, data_dir, image_size):
        self.data_dir = data_dir
        self.image_size = image_size
        self.data_list = os.listdir(data_dir)

    def __len__(self):
        return len(self.data_list)

    def __getitem__(self, idx):
        image_path = os.path.join(self.data_dir, self.data_list[idx])
        image = ...  # Load the image from file
        return image
```

### `train.py`
```python
# train.py
# Main training script

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.nn.parallel import DistributedDataParallel as DDP
from datautils import MyTrainDataset
from config import model_name, num_epochs, batch_size, train_dataset_name, save_every
from ddp_setup import ddp_setup

class Trainer:
    def __init__(
        self,
        model: torch.nn.Module,
        train_data: DataLoader,
        optimizer: torch.optim.Optimizer,
        gpu_id: int,
        save_every: int,
    ) -> None:
        self.gpu_id = gpu_id
        self.model = model.to(gpu_id)
        self.train_data = train_data
        self.optimizer = optimizer
        self.save_every = save_every
        self.model = DDP(model, device_ids=[gpu_id])

    def _run_batch(self, source, targets):
        self.optimizer.zero_grad()
        # ... (rest of the function remains the same)

def main():
    # Load the model from checkpoint
    checkpoint_file = "checkpoint.pth"
    model = torch.load(checkpoint_file)

    # Set up the data loader
    data_dir = "/eagle/MatGenome/bkowalski/pytorch_run/data"
    image_size = 224
    train_dataset = MyTrainDataset(data_dir, image_size)
    train_sampler = torch.utils.data.distributed.DistributedSampler(
        train_dataset, num_replicas=num_gpus, rank=gpu_rank
    )
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        sampler=train_sampler,
        num_workers=4,
        pin_memory=True,
    )

    # Set up the optimizer and scheduler
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=2, gamma=0.1)

    # Set up the trainer
    trainer = Trainer(model, train_loader, optimizer, gpu_rank, save_every)

    # Run the training loop
    for epoch in range(num_epochs):
        trainer.train_one_epoch()
        if (epoch + 1) % save_every == 0:
            torch.save(trainer.model.state_dict(), f"checkpoint_{epoch+1}.pth")

if __name__ == "__main__":
    ddp_setup(gpu_rank, num_gpus)
    main()
```

### `ddp_setup.py`
```python
# ddp_setup.py
# Function to set up the distributed data parallelism

import os
import torch
from torch.distributed import init_process_group, destroy_process_group

def ddp_setup(rank, world_size):
    os.environ["MASTER_ADDR"] = "localhost"
    os.environ["MASTER_PORT"] = "12355"
    torch.cuda.set_device(rank)
    init_process_group(backend="nccl", rank=rank, world_size=world_size)
```

### `checkpoint.pth`
*Produced at runtime*

### `config.json`
*Produced at runtime*

Note that the `config.json` file is not explicitly mentioned in the example code, but it is often used to store the configuration parameters in a JSON format. The `config.py` file can be used to generate this file at runtime.

The `checkpoint.pth` file is not explicitly mentioned in the example code, but it is often used to store the model weights and other training parameters. The `train.py` script can be used to load this file and resume training from the last checkpoint.

The `ddp_setup.py` file is used to set up the distributed data parallelism, and the `train.py` script uses this function to initialize the process group and set up the distributed data loader.
````
