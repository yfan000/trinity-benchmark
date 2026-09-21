# nemotron-3-ultra — pytorch@sophia, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**1. Work sizing and walltime derivation**

*Assumptions (no measured data exists for this configuration on Sophia):*
- A100 40/80 GB mixed-precision ResNet-50 throughput: **1 500 images/s/GPU** (conservative literature value for CUDA 12 / sm_80).
- Global batch size = 256 × *N*<sub>GPU</sub>.
- 100 000 images × 10 epochs = 1 000 000 images total.
- Compute batches = 1 000 000 / 256 = 3 906 batches.
- Compute time = (3 906 / *N*<sub>GPU</sub>) × (1/5.86 batches/s) ≈ **668 / *N*<sub>GPU</sub> seconds**.
- Add 20 % for NCCL all-reduce, data-loading, epoch transitions → **802 / *N*<sub>GPU</sub> seconds**.
- Add **60 s** MPI/NCCL initialisation, model load, DataLoader warm-up.

*Node count choice:* 2 nodes (16 GPUs) — small enough for a quick scaling test, large enough to exercise multi-node NCCL over IB.
- Estimated run time = 60 + 802/16 ≈ **110 s (1 min 50 s)**.
- Safety margin: **3×** (covers input variance, queue wait, scheduler jitter) → **330 s ≈ 5.5 min**.
- **Requested walltime: 00:10:00** (10 min, well under 24 h cap).

---

**2. Queue elimination**

| Queue      | Node range | Max walltime | Node-min check (req=2) | Node-max check (req=2) | Walltime check (req=0:10) | Verdict |
|------------|------------|--------------|------------------------|------------------------|---------------------------|---------|
| by-gpu     | 1–1        | 24 h         | **FAIL** (min=1, need≥2) | FAIL (max=1)           | PASS                      | ❌ Excluded |
| bigmem     | 1–1        | 24 h         | **FAIL** (min=1, need≥2) | FAIL (max=1)           | PASS                      | ❌ Excluded |
| **by-node**| **1–8**    | **24 h**     | **PASS** (1 ≤ 2)       | **PASS** (2 ≤ 8)       | **PASS** (0:10 ≤ 24:00)   | ✅ **Chosen** |

*All three limits for **by-node** read PASS.*

---

**3. Ranks-per-node and GPUs-per-rank (application defaults)**

The build defaults specify *MPI + NCCL + Gloo* with *NCCL for GPU collectives*. Standard PyTorch DDP practice (and the only way to saturate 8 A100s/node) is **1 rank per GPU**.
- **Ranks per node = 8** (fixed by code build)
- **GPUs per rank = 1** (fixed by code build)

---

**4. Scaling guidance**

No explicit scaling guidance was supplied. The chosen 2-node (16-GPU) run gives a global batch size of 4 096, which is within the known strong-scaling envelope for ResNet-50 with linear LR scaling (not configured here, but 10-epoch test runs are standard at this scale). No deviation from defaults is needed.

---

**5. Final resource specification**

| Parameter          | Value |
|--------------------|-------|
| **Nodes**          | 2 |
| **GPUs per node**  | 8 |
| **Ranks per node** | 8 |
| **Total ranks**    | 16 (= 2 × 8) |
| **Walltime**       | 00:10:00 |
| **Queue**          | by-node |

*Verification:* total ranks = nodes × ranks per node = 2 × 8 = 16 ✅
````
