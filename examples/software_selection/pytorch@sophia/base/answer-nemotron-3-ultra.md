# nemotron-3-ultra — pytorch@sophia, base arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
**Selected Application: PyTorch (MPI)**

**Why it fits:**
- **Native NCCL Support**: The installed PyTorch 2.5.0a0 build explicitly includes MPI and NCCL distributed backends, enabling efficient multi-GPU gradient synchronization via `torch.distributed` with the NCCL backend—exactly as required for data-parallel ResNet‑50 training.
- **Data‑Parallelism Ready**: PyTorch’s `DistributedDataParallel` (DDP) module is the standard, production‑grade way to perform single‑node, multi‑GPU data‑parallel training with NCCL collectives.
- **Optimized for Sophia**: Built from source on the ALCF Sophia system, ensuring compatibility with the A100 GPUs, CUDA 12.x stack, and the system’s MPI/NCCL libraries.
- **Framework Alignment**: ResNet‑50 image classification is a canonical PyTorch workload; the framework provides torchvision models, mixed‑precision (AMP), and profiling tools that simplify production runs while respecting queue limits.
````
