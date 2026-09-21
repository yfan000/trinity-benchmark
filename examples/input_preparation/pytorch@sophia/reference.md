# Reference answer — pytorch@sophia

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
Required files for restart of ResNet-50 training on Sophia using PyTorch (MPI):

1. `train.py` — the main training script. Must include:
   - Environment setup: `init_process_group(backend='nccl')` for GPU collectives (NCCL is the correct backend for A100s on Sophia; MPI/Gloo not used for GPU tensors)
   - Model: `torchvision.models.resnet50()` wrapped in `DistributedDataParallel`
   - Dataset: a custom or standard `ImageFolder`-style dataset pointing to 100,000 images, with `DistributedSampler`
   - DataLoader: `batch_size=256` per GPU
   - Mixed precision: `torch.cuda.amp.GradScaler` and `torch.cuda.amp.autocast()`
   - Total epochs: 10
   - Checkpoint resume logic: accept a `--resume` argument or detect a checkpoint file (e.g., `checkpoint.pt`) in `/eagle/MatGenome/bkowalski/pytorch_run`; call `model.load_state_dict`, `optimizer.load_state_dict`, and restore `start_epoch` from the saved dict so training resumes from the interrupted epoch rather than epoch 0
   - Checkpoint saving: save model state dict, optimizer state dict, scaler state dict, and current epoch at end of each epoch

2. `checkpoint.pt` — binary PyTorch checkpoint; produced at runtime by a prior run, NOT written by the agent. The agent should note it must exist in `/eagle/MatGenome/bkowalski/pytorch_run` before the restart job is submitted.

Launch command (for reference, not part of input files):
```
torchrun --nproc_per_node=8 train.py --resume /eagle/MatGenome/bkowalski/pytorch_run/checkpoint.pt
```
This uses all 8 A100 GPUs on one Sophia node, consistent with the `by-gpu` queue defaults and the PyTorch (MPI) catalog entry.

Environment activation (in job script, not input file):
```
source /home/hzheng/clearml/miniconda3/etc/profile.d/conda.sh
conda activate /eagle/datascience/hzheng/software/sophia/pytorch-mpi/conda_env
export LD_LIBRARY_PATH=/usr/lib64:/usr/local/cuda/lib64:${LD_LIBRARY_PATH}
```

No additional config files are required; all parameters are expressed as Python code and command-line arguments within `train.py`.
````
