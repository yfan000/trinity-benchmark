# gpt-oss-120b — pytorch@sophia, base arm

Input preparation. **FAIL** (correctness 0/2, completeness 0/2, usability 0/2, fatal; 5 of 9 requirements violated).

````
**File 1 – `train_config.yaml`**  
Configuration that the training script reads at start‑up. It contains every hyper‑parameter the job needs, plus the flag telling the script to load the previous checkpoint and continue training.

```yaml
# ------------------------------------------------------------------
# Distributed mixed‑precision ResNet‑50 training configuration
# ------------------------------------------------------------------
model:
  name: resnet50
  pretrained: false                # start from random weights (unless a checkpoint is loaded)

training:
  epochs: 10                       # total number of epochs to run
  start_epoch: 0                   # will be overwritten when a checkpoint is loaded
  batch_size_per_gpu: 256          # number of images each GPU processes per step
  learning_rate: 0.1
  momentum: 0.9
  weight_decay: 1e-4
  optimizer: sgd
  mixed_precision: true           # enable AMP (automatic mixed precision)

data:
  root_dir: /eagle/MatGenome/datasets/imagenet_subset   # where the 100 000‑image subset lives
  train_file: train.txt          # text file that lists the training image paths (one per line)
  num_classes: 1000

distributed:
  backend: nccl
  master_addr: 127.0.0.1
  master_port: 12355
  world_size: 8                  # total number of MPI ranks / GPUs
  rank: 0                        # will be set by the launcher for each process

checkpoint:
  directory: ./checkpoints       # where checkpoints are written
  filename: checkpoint_last.pth  # name of the most‑recent checkpoint file
  resume: true                   # tells the script to load the checkpoint if it exists
  load_optimizer_state: true
  load_scaler_state: true        # for AMP

logging:
  output_dir: ./logs
  log_interval: 10
  save_every_n_epochs: 1
```

*Why it’s needed:* The training program reads this YAML at start‑up to know the model, dataset location, batch size, mixed‑precision flag, distributed settings, and—critically—the checkpoint file to load (`resume: true`). Without it the script would start a fresh run instead of restarting.

---

**File 2 – `mpi_hosts.txt`**  
Host file used by `mpirun` (or `srun`) to launch the eight GPU‑aware MPI processes on the Sophia nodes. Each line gives a node name and the number of GPU slots to use on that node.

```text
# mpi_hosts.txt – host list for the distributed run on Sophia
node001 slots=4
node002 slots=4
```

*Why it’s needed:* `mpirun -np 8 --hostfile mpi_hosts.txt ...` reads this file to know on which compute nodes to place the eight processes (one per GPU). The training script itself does not create it; it must exist before the restart launch.

---

**File 3 – `resume.info`**  
A tiny text file that can be passed as a command‑line argument (e.g., `--resume-info resume.info`). It records the exact checkpoint file name that should be loaded. This is useful when the training script allows a separate “resume‑info” argument rather than reading the path from the main config.

```text
# resume.info – tells the trainer which checkpoint to restore
checkpoint_path=./checkpoints/checkpoint_last.pth
```

*Why it’s needed:* Some PyTorch training wrappers separate the resume metadata from the main YAML. Providing this file guarantees the script can locate the existing checkpoint (`checkpoint_last.pth`) that was written by the previous (interrupted) run.

---

### Runtime‑generated / existing binary files (not written here)

- `./checkpoints/checkpoint_last.pth` – the binary PyTorch checkpoint produced by the earlier part of the run; it contains model weights, optimizer state, AMP scaler state, and the last completed epoch. The restart process will read this file.

- `./logs/…` – log files created during the resumed run.

These files are **produced at runtime** (or already exist) and therefore are listed only as expected outputs, not as input contents.
````
