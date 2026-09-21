# nemotron-3-ultra — nekrs@polaris, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**Resource Specification and Reasoning**

---

### (a) Queue Selection and Walltime Derivation

#### 1. Sizing the Work and Required Walltime
- **Baseline measurement**: 1 node × 1,000 timesteps = 8 minutes (kernels cached).  
  → 0.008 min/timestep on 1 node.
- **Production run**: 20,000 timesteps.  
  → 1‑node extrapolation: 20,000 × 0.008 = **160 minutes (2.67 h)**.
- **Node count chosen**: 20 nodes (see scaling rationale in §d).  
  Total MPI ranks = 20 nodes × 4 ranks/node = 80 ranks.
- **Strong‑scaling assumption**: NekRS scales well but not perfectly; assume **70 % parallel efficiency** when going from 1 to 20 nodes (i.e., effective speed‑up = 20 × 0.7 = 14×).  
  Estimated runtime = 160 min / 14 ≈ **11.4 minutes**.
- **Safety margin**: Add 100 % margin to cover load imbalance, statistics‑collection overhead, and system variability.  
  → 11.4 min × 2 = **22.8 minutes**.
- **Requested walltime**: **30 minutes (0.5 hours)** – comfortably above the margined estimate and well within queue limits.

#### 2. Queue Elimination Table

| Queue            | Node Range | Max Walltime | Node Minimum | Node Maximum | Walltime Limit | Verdict |
|------------------|------------|--------------|--------------|--------------|----------------|---------|
| debug            | 1–2        | 1 h          | 1 (PASS)     | 2 (FAIL: 20 > 2) | 1 h (PASS)     | **REJECT** – node maximum exceeded |
| debug‑scaling    | 1–10       | 1 h          | 1 (PASS)     | 10 (FAIL: 20 > 10) | 1 h (PASS)     | **REJECT** – node maximum exceeded |
| **prod**         | **10–496** | **24 h**     | **10 (PASS: 20 ≥ 10)** | **496 (PASS: 20 ≤ 496)** | **24 h (PASS: 0.5 h ≤ 24 h)** | **ACCEPT** |
| demand           | 1–56       | 1 h          | 1 (PASS)     | 56 (PASS)    | 1 h (PASS)     | Acceptable, but *prod* is the designated production queue |
| preemptable      | 1–10       | 72 h         | 1 (PASS)     | 10 (FAIL: 20 > 10) | 72 h (PASS)    | **REJECT** – node maximum exceeded |
| capacity         | 1–4        | 168 h        | 1 (PASS)     | 4 (FAIL: 20 > 4)   | 168 h (PASS)   | **REJECT** – node maximum exceeded |

#### 3. Final Queue Choice – **prod**
- **Node minimum**: requested 20, limit 10 → **PASS**
- **Node maximum**: requested 20, limit 496 → **PASS**
- **Maximum walltime**: requested 0.5 h, limit 24 h → **PASS**

---

### (b) Ranks and GPUs from Application Defaults
- **Ranks per node (build default)**: 4 (1 MPI rank per GPU).
- **GPUs per node**: 4 (A100, one per rank).
- **GPUs per rank**: 1.

---

### (c) Assumptions and Margins
- **Strong‑scaling efficiency**: Assumed 70 % when scaling from 1 to 20 nodes (no multi‑node timing data provided).
- **Runtime margin**: 100 % added to the estimated 11.4 minutes to obtain the requested 30 minutes.
- No measured throughput for multi‑node runs is claimed; the above are explicit assumptions.

---

### (d) Scaling Guidance Compliance
The supplied guidance states: *“nekRS uses 1 MPI rank per GPU (4 per node on Polaris). Scale by increasing node count.”*  
We follow this exactly: we increase the node count to 20 while keeping 4 ranks (and 4 GPUs) per node. The problem size (32,000 elements) yields ~400 elements per rank at 20 nodes, which is within the typical range for good spectral‑element efficiency.

---

### (e) Final Resource Specification

| Parameter            | Value |
|----------------------|-------|
| **Nodes**            | 20 |
| **Ranks per node**   | 4 |
| **Total ranks**      | 80 ( = 20 × 4 ) |
| **GPUs per node**    | 4 |
| **Walltime**         | 30 minutes (0.5 hours) |
| **Queue**            | prod |

All scheduler limits are satisfied, and the configuration adheres to the application’s scaling model.
````
