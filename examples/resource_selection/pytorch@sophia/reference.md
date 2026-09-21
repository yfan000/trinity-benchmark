# Reference answer — pytorch@sophia

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
**Ranks per node and GPUs per rank (from build defaults):**
The PyTorch (MPI) build on Sophia uses `torchrun --nproc_per_node=8` as its recommended GPU distributed launch, meaning 8 ranks per node, 1 GPU per rank, consuming all 8 A100s on each node. These are fixed by how the code was built; only the node count is the agent's to choose.

**Node count:**
A single node (8 GPUs) is sufficient for this workload. ResNet-50 on 100,000 images with batch 256 per GPU is a moderately sized training run. One full node maximises GPU utilisation without incurring multi-node communication overhead and fits within the by-gpu queue.

**Walltime estimation (assumed, no measurement available):**
A100 throughput for ResNet-50 in mixed precision is typically ~1,000–2,000 images/sec per GPU (literature/community baseline). With 8 GPUs and batch 256 per GPU (global batch 2,048), at ~1,200 img/s per GPU (conservative assumption):
- Steps per epoch: ceil(100,000 / 2,048) ≈ 49 steps
- 10 epochs → ~490 steps
- Time per step ≈ 2,048 / (8 × 1,200) ≈ 0.21 s → ~103 s of compute
Adding overhead (data loading, checkpointing, startup) and a generous 10× safety margin for an unfamiliar environment: walltime estimate ≈ 30 minutes. Rounded up to 1 hour (3,600 s) to be safe, well within any queue's 24 h cap.

**Queue elimination:**
- by-gpu: nodes 1–1, max 24 h. Requested 1 node → node range OK. 1 h walltime < 24 h → OK. Survives.
- by-node: nodes 1–8, max 24 h. Requested 1 node → node range OK. Survives, but by-gpu is the default and correct queue for a single-node GPU job.
- bigmem: nodes 1–1, max 24 h. Would survive on limits, but bigmem is reserved for 80 GB GPU nodes; this workload fits in 40 GB A100 memory and should not consume scarce bigmem resources. Eliminated on policy grounds.

**Chosen queue: by-gpu**

**Limit check for by-gpu with 1 node, 1 h walltime:**
| Criterion         | Requested | Limit | Verdict |
|-------------------|-----------|-------|---------|
| Node minimum      | 1         | 1     | PASS    |
| Node maximum      | 1         | 1     | PASS    |
| Maximum walltime  | 1 h       | 24 h  | PASS    |

**Scaling guidance:**
The build recommends NCCL for GPU collectives and notes that conda OpenMPI is not CUDA-aware. For a single-node run, NCCL intra-node communication applies with no cross-node fabric concern. Guidance is honoured.

**Final specification:**
- Nodes: 1
- Ranks per node: 8 (fixed by build: torchrun --nproc_per_node=8)
- Total ranks: 1 × 8 = 8
- GPUs per rank: 1
- GPUs requested: 8
- Walltime: 1 hour (3,600 s)
- Queue: by-gpu
````
