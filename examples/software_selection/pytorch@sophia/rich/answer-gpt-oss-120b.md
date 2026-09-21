# gpt-oss-120b — pytorch@sophia, rich arm

Software selection. **FAIL** (correctness 1/2, completeness 2/2, usability 2/2; 1 of 4 requirements violated).

````
**Selected application:** **PyTorch (MPI) – PyTorch 2.5.0a0 built with MPI + NCCL back‑ends**

**Why it fits**

| Requirement | Matching feature of PyTorch (MPI) |
|-------------|------------------------------------|
| **Distributed training of ResNet‑50** | Native `torch.nn.parallel.DistributedDataParallel` works out‑of‑the‑box for image‑classification models such as ResNet‑50. |
| **All GPUs on a single node (data‑parallel)** | The MPI‑enabled build can launch a process per GPU (`torchrun --nnodes=1 --nproc_per_node=$GPU_COUNT …`). |
| **Multi‑GPU collective communication via NCCL** | The installation explicitly provides both MPI and NCCL back‑ends, allowing NCCL‑accelerated gradient all‑reduce across the node’s GPUs. |
| **Production run respecting queue limits** | The MPI‑capable PyTorch integrates cleanly with the ALCF job scheduler (SLURM on Sophia); you can request the exact GPU count and wall‑time, and the job will be scheduled within the defined queue limits. |
| **Software availability on Sophia A100 nodes** | The version is compiled from source on the A100 nodes, guaranteeing compatibility with the CUDA toolkit and the underlying hardware. |
| **Ease of use within the provided working directory** | The default Conda‑based Python environment on Sophia already includes this PyTorch build, so scripts placed under `/eagle/CombustionSim/jmartinez/run_current` can be run without additional installs. |

*Alternative options:* TensorFlow also supports NCCL but the installed PyTorch build is specifically compiled with MPI+NCCL and is the most common choice for ResNet‑50 training. DeepSpeed is oriented toward very large LLM workloads and would add unnecessary complexity for a standard ResNet‑50 job.
````
