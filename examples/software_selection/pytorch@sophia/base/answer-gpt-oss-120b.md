# gpt-oss-120b — pytorch@sophia, base arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
**Selected application:** **PyTorch (MPI)** – the PyTorch 2.5.0a0 build that includes the MPI + NCCL distributed back‑ends.

**Why it fits the workload**

| Requirement | How PyTorch (MPI) satisfies it |
|-------------|--------------------------------|
| **Distributed ResNet‑50 training** | PyTorch natively supports training ResNet‑50 (and any other torchvision models) and provides the standard `torch.nn.DataParallel` / `torch.nn.parallel.DistributedDataParallel` APIs for data‑parallel scaling. |
| **All GPUs on a single node** | The MPI launch (`mpirun -np <num_gpus>`) can allocate one rank per GPU; each rank uses its local GPU, giving full‑node utilization on the A100 (or V100) nodes. |
| **Multi‑GPU collective communication via NCCL** | The PyTorch build was compiled with both MPI and NCCL back‑ends, so `DistributedDataParallel` will automatically employ NCCL for gradient all‑reduce, delivering the highest‑throughput intra‑node communication. |
| **Production‑run queue limits** | PyTorch is a lightweight, pre‑installed module; launching with `srun`/`sbatch` and the appropriate `--gpus-per-node`/`--ntasks-per-node` directives respects the queue policies without needing extra licences or special resource managers. |
| **Compatibility with existing environment** | The default scientific Python/Conda environment on Sophia A100 nodes already loads the correct CUDA (12.x) libraries, matching the system’s driver and GPU stack. No extra container or build steps are required. |

**Alternative note** – DeepSpeed is also installed and built on top of the same PyTorch MPI+NCCL stack, so it could be used if you want extra optimizer/zero‑redundancy features. However for a straightforward ResNet‑50 image‑classification benchmark, the vanilla PyTorch MPI distribution is the most direct, well‑documented, and queue‑friendly choice.
````
