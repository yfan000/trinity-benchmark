# nemotron-3-ultra — qmcpack@aurora, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**Resource Specification and Reasoning for QMCPACK DMC Run on Aurora**

---

### (a) Queue Selection and Limit Verification

#### 1. Size the work and derive the required walltime

**Workload parameters**  
- System: 64‑atom Si (2×2×2 diamond supercell)  
- Algorithm: DMC with Slater‑Jastrow trial wavefunction  
- Walkers: 4096  
- DMC blocks: 200  
- Timestep: 0.005 Ha⁻¹  

**Assumptions (no prior timing data available)**  
- Steps per DMC block: 20 (typical QMCPACK default; not specified in input)  
- Total DMC steps = 200 blocks × 20 steps/block = 4000 steps  
- Total walker‑steps = 4096 walkers × 4000 steps = 16,384,000 walker‑steps  
- Performance on one Intel Data Center GPU Max Series tile (SYCL/spir64): ~1000 walker‑steps/s (conservative estimate for this system size)  
- Build default: 6 ranks/node → 1 rank per GPU tile → 6 tiles/node  
- Node‑level throughput = 6 tiles × 1000 walker‑steps/s/tile = 6000 walker‑steps/s  
- Parallel efficiency / overhead (initialization, I/O, load imbalance): +30%  
- Safety margin (no measured baseline): ×2  

**Walltime estimate for 2 nodes (12 tiles)**  
- Ideal compute time = 16,384,000 / (12 × 1000) = 1365 s ≈ 22.8 min  
- With 30% overhead = 22.8 × 1.3 ≈ 29.6 min  
- With 2× safety margin = 29.6 × 2 ≈ 59 min ≈ **1 hour**  

**Requested walltime** = 2 hours (120 min) to provide a comfortable buffer above the 1‑hour estimate.

#### 2. Eliminate queues that cannot accommodate the request

| Queue           | Node range | Max walltime | Node min (2) | Node max (2) | Walltime max (2 h) | Verdict |
|-----------------|------------|--------------|--------------|--------------|--------------------|---------|
| debug           | 1–2        | 1 h          | PASS (2≥1)   | PASS (2≤2)   | **FAIL** (2 h > 1 h) | Reject |
| debug‑scaling   | 2–256      | 1 h          | PASS (2≥2)   | PASS (2≤256) | **FAIL** (2 h > 1 h) | Reject |
| prod            | 256–10624  | 24 h         | **FAIL** (2<256) | PASS       | PASS               | Reject |
| **capacity**    | **1–16**   | **168 h**    | **PASS**     | **PASS**     | **PASS**           | **Keep** |
| visualization   | 1–32       | 8 h          | PASS         | PASS         | PASS               | Keep   |

#### 3. Choose the surviving queue and verify all three limits

Both **capacity** and **visualization** queues pass all limits. The **capacity** queue is selected because it is intended for production‑style compute jobs (the visualization queue targets interactive visualization sessions).

**Limit check for capacity queue with requested values:**

| Limit            | Requested | Queue Limit | Pass/Fail |
|------------------|-----------|-------------|-----------|
| Node minimum     | 2         | 1           | **PASS**  |
| Node maximum     | 2         | 16          | **PASS**  |
| Maximum walltime | 2 h       | 168 h       | **PASS**  |

All three checks read **PASS**.

---

### (b) Ranks and GPUs from Build Defaults

- **Ranks per node (build default)**: 6 (one per GPU tile)  
- **GPUs per rank**: 1 (each rank offloads to a single tile)  
- **GPUs per node**: 6 (fixed by hardware)  
- **Total MPI ranks** = nodes × ranks per node = 2 × 6 = **12**

---

### (c) Timing Assumptions and Margins

- **Assumed steps per block**: 20 (not provided in workload)  
- **Assumed single‑tile throughput**: 1000 walker‑steps/s (no measured data; conservative for 64‑atom Si on PVC)  
- **Overhead factor**: 1.3× (initialization, I/O, load imbalance)  
- **Safety margin**: 2× (standard practice when no prior timing exists)  
- **No measured timing or throughput figures are claimed**; all numbers are explicitly assumed.

---

### (d) Scaling Guidance

- The only scaling guidance supplied is the build‑time default of **6 ranks per node** (matching the 6 GPU tiles).  
- This default is honoured: the run uses exactly 6 ranks/node.  
- With 4096 walkers and 12 total ranks, each rank handles ~341 walkers, well above the typical minimum (~50–100) for good load balance in QMCPACK’s walker‑parallel DMC. No further scaling constraints apply.

---

### (e) Final Resource Specification

| Parameter          | Value |
|--------------------|-------|
| **Nodes**          | 2 |
| **Ranks per node** | 6 |
| **Total MPI ranks**| 12 ( = 2 × 6 ) |
| **GPUs per node**  | 6 |
| **Walltime**       | 2 hours (120 minutes) |
| **Queue**          | capacity |

**Verification**: Total ranks (12) = Nodes (2) × Ranks per node (6). All queue limits satisfied.
````
