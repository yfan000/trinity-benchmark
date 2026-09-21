# gpt-oss-120b — pytorch@sophia, rich arm

Input preparation. **FAIL** (correctness 0/2, completeness 0/2, usability 0/2, fatal; 6 of 9 requirements violated).

````
**File 1 – `config.yaml`**  
Configuration that the PyTorch training script reads at start‑up. It tells the DDP runtime how many processes to launch, the hardware layout on Sophia, the training hyper‑parameters, the location of the data manifest, and the checkpoint that must be loaded to resume the run.

```yaml
# -------------------------------------------------
# Distributed mixed‑precision ResNet‑50 training
# Restart configuration – Sophia (ALCF)
# -------------------------------------------------

# --------------------  System  --------------------
world_size: 64                # total # of GPU processes (8 nodes × 8 GPUs)
nodes: 8                      # physical nodes allocated
gpus_per_node: 8
master_addr: "node001"        # first node in the allocation
master_port: 29500            # NCCL port (any free port can be used)

# --------------------  Training  --------------------
model: "resnet50"
precision: "amp"              # automatic mixed‑precision (torch.cuda.amp)
batch_size_per_gpu: 256
total_batch_size: 2048        # 256 × 8 GPUs per node × 8 nodes
epochs: 10
resume:
  checkpoint_path: "checkpoints/resnet50_epoch_03.pt"
  # The script will load the epoch/iteration info stored inside the checkpoint.
  load_optimizer_state: true
  load_scaler_state: true
learning_rate: 0.1
momentum: 0.9
weight_decay: 1e-4
lr_scheduler:
  type: "step"
  step_size: 3
  gamma: 0.1

# --------------------  Data  --------------------
dataset:
  manifest: "data/imagenet_subset_manifest.txt"
  root_dir: "/eagle/MatGenome/bkowalski/datasets/imagenet_subset"
  num_classes: 1000
  num_workers: 8
  pin_memory: true
  shuffle: true
  augmentations:
    - random_resized_crop
    - horizontal_flip
    - color_jitter

# --------------------  Logging  --------------------
log_dir: "logs"
save_checkpoint_every: 1      # save a checkpoint at the end of each epoch
```

*Why it is needed:* The training script parses this file to know the distributed topology, the mixed‑precision flag, batch‑size layout, optimizer settings, where to find the data, and which checkpoint (`checkpoints/resnet50_epoch_03.pt`) must be loaded to continue training from the point where it stopped.


---

**File 2 – `data/imagenet_subset_manifest.txt`**  
Plain‑text manifest that enumerates every image in the 100 000‑image subset together with its integer class label. The `Dataset` implementation used by the script reads this file to build the `torch.utils.data.Dataset` instance.

```text
# image_path  label
eagle/MatGenome/bkowalski/datasets/imagenet_subset/n01440764/n01440764_10026.JPEG 0
eagle/MatGenome/bkowalski/datasets/imagenet_subset/n01440764/n01440764_10027.JPEG 0
eagle/MatGenome/bkowalski/datasets/imagenet_subset/n01440764/n01440764_10028.JPEG 0
eagle/MatGenome/bkowalski/datasets/imagenet_subset/n01440764/n01440764_10029.JPEG 0
eagle/MatGenome/bkowalski/datasets/imagenet_subset/n01440764/n01440764_10030.JPEG 0
# …
# (total 100 000 lines, each with absolute path and integer label)
```

*Why it is needed:* The DDP training process must know exactly which files belong to the training set and their corresponding class IDs. The manifest supplies this information to the `MyTrainDataset` (or equivalent) that the script constructs.


---

**File 3 – `checkpoints/resnet50_epoch_03.pt`** *(binary – *produced at runtime*)*  
*Not written here.* This is the checkpoint file that was written by the previous run after epoch 3. It contains the model state dict, optimizer state, AMP scaler state, and the epoch/iteration counters. The `resume.checkpoint_path` entry in `config.yaml` points to this file so that the training script can load it and continue from epoch 3 onward.

*Why it is needed:* Without this file the restart cannot restore the model weights, optimizer momentum, and mixed‑precision scaling factors, meaning training would have to start from scratch. The presence of the checkpoint enables true continuation of the interrupted job.
````
