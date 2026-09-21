# nemotron-3-ultra — pytorch@sophia, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**Step 1 – Size the work and derive the walltime needed**

| Parameter | Value | Note |
|-----------|-------|------|
| Training images | 100,000 | Subset |
| Batch size / GPU | 256 | Fixed by workload |
| GPUs / node | 8 | Sophia: 8 × A100 |
| Nodes chosen | 2 | See reasoning below |
| Global batch size | 256 × 8 × 2 = 4,096 | |
| Iterations / epoch | 100,000 / 4,096 ≈ 24.4 → 25 | Ceil to full batches |
| Total iterations (10 epochs) | 250 | |
| Est. time / iteration | 0.4–0.6 s | Mixed-precision ResNet-50 on A100: compute ~0.25 s, NCCL all-reduce (2 nodes, InfiniBand) ~0.15 s, DataLoader overhead ~0.1–0.2 s (no DALI, standard PyTorch). Conservative upper bound 0.6 s. |
| Base compute time | 250 × 0.6 s = 150 s ≈ 2.5 min | |
| Safety margin | 12× | No prior measurements on this system; covers DataLoader variance, MPI/NCCL init, checkpoint writes, queue-to-start delay. |
| **Requested walltime** | **00:30:00** (30 min) | 2.5 min × 12 = 30 min. Well under 24 h cap. |

*Why 2 nodes?*  
- 1 node = not “distributed” (by-gpu/bigmem only allow 1 node anyway).  
- 2 nodes (16 GPUs) → 25 iters/epoch, a count comparable to large-scale ImageNet runs (e.g., 256 GPUs ≈ 20 iters/epoch).  
- 4+ nodes → ≤12 iters/epoch; communication dominates, scaling efficiency collapses for this problem size.  
- by-node queue permits 1–8 nodes; 2 nodes is the smallest *multi-node* choice that exercises NCCL cross-node collectives.

---

**Step 2 – Eliminate queues that cannot accept the request**

| Queue | Node range | Max walltime | Node-min check (req=2) | Node-max check (req=2) | Walltime check (req=0.5 h) | Verdict |
|-------|------------|--------------|------------------------|------------------------|----------------------------|---------|
| by-gpu | 1–1 | 24 h | **FAIL** (min=1, but max=1 < 2) | — | — | **REJECTED** – node maximum exceeded |
| bigmem | 1–1 | 24 h | **FAIL** (max=1 < 2) | — | — | **REJECTED** – node maximum exceeded |
| by-node | 1–8 | 24 h | PASS (2 ≥ 1) | PASS (2 ≤ 8) | PASS (0.5 h ≤ 24 h) | **ACCEPTED** |

Only **by-node** survives all three limits.

---

**Step 3 – Verify the chosen queue against each limit (by-node)**

| Limit | Requested | Queue limit | Pass/Fail |
|-------|-----------|-------------|-----------|
| Node minimum | 2 | 1 | **PASS** |
| Node maximum | 2 | 8 | **PASS** |
| Maximum walltime | 00:30:00 | 24:00:00 | **PASS** |

All three read **PASS**.

---

**Ranks-per-node & GPUs-per-rank (from application defaults)**

- Build defaults specify: “MPI + NCCL + Gloo backends. Use NCCL for GPU collectives”.  
- Standard PyTorch DistributedDataParallel (DDP) pattern: **1 rank per GPU**, NCCL backend for gradient all-reduce.  
- Sophia node has **8 A100 GPUs** → **8 ranks per node**, **1 GPU per rank**.  
- *Only the node count (2) was chosen by the agent; ranks-per-node and GPUs-per-rank are fixed by the code build.*

---

**Scaling guidance**

No explicit scaling guidance was supplied with the workload. The implicit guidance from the framework choice (PyTorch MPI/DDP + NCCL) and hardware (8 GPUs/node, NVLink intra-node, InfiniBand inter-node) is honoured by using 1 rank/GPU and NCCL collectives. For a 100 k-image / 10-epoch run, 2 nodes (16 GPUs) keeps iterations/epoch ≈ 25, which is in the range where NCCL multi-node scaling remains efficient (≥80 %); larger node counts would drop iterations/epoch too low and are therefore not used.

---

**Final resource specification**

| Parameter | Value |
|-----------|-------|
| **Nodes** | 2 |
| **Ranks per node** | 8 |
| **Total ranks** | 16 ( = 2 × 8 ) |
| **GPUs per node** | 8 |
| **GPUs per rank** | 1 |
| **Walltime** | 00:30:00 |
| **Queue** | by-node |

*Verification:* total ranks = nodes × ranks per node = 2 × 8 = 16 ✓
````
