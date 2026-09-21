# nemotron-3-ultra — gromacs@sirius, rich arm

Resource selection. **FAIL** (correctness 1/2, completeness 2/2, usability 2/2; 1 of 10 requirements violated).

````
**Resource Specification for GROMACS Restart on Sirius**

---

### (a) Queue Selection and Limit Verification

#### 1. Work Sizing and Walltime Derivation

| Parameter | Value / Assumption |
|-----------|-------------------|
| System size | ~34,000 atoms (lysozyme + TIP3P water + 0.15 M NaCl) |
| Simulation length remaining | Up to 5 ns (restart; worst case = full 5 ns) |
| Timestep | 2 fs → 2.5×10⁶ steps |
| Hardware | 4× A100-SXM4-40GB per node |
| **Throughput assumption (no measurement supplied)** | **50 ns/day per GPU** — conservative for a 34k-atom PME system on A100; literature reports 100–200+ ns/day for similar sizes, so 50 ns/day provides a wide safety margin. |
| Parallel efficiency assumption | 75 % on 4 GPUs (1 node) — typical for small-system strong scaling with PME. |
| Aggregate throughput (1 node, 4 GPUs) | 4 × 50 × 0.75 = **150 ns/day** |
| Raw compute time for 5 ns | 5 / 150 = 0.0333 day = **48 minutes** |
| Safety margin | **4×** (covers restart overhead, checkpoint I/O, queue variability, load imbalance) |
| **Requested walltime** | 48 min × 4 = **3.2 h → rounded up to 04:00:00 (4 hours)** |

*Even a single-GPU run (50 ns/day → 2.4 h raw → 9.6 h with margin) fits within the 24 h queue cap.*

#### 2. Queue Table Elimination

| Queue | Node Range | Max Walltime | Node-Min Check | Node-Max Check | Walltime Check | Verdict |
|-------|------------|--------------|----------------|----------------|----------------|---------|
| **workq** | 1–4 | 24 h | Request 1 ≥ 1 ✓ | Request 1 ≤ 4 ✓ | Request 4 h ≤ 24 h ✓ | **PASS** |

Only `workq` exists; it passes all three limits.

#### 3. Final Queue Verdict

| Limit | Requested | Limit | Pass/Fail |
|-------|-----------|-------|-----------|
| Node minimum | 1 | 1 | **PASS** |
| Node maximum | 1 | 4 | **PASS** |
| Maximum walltime | 4 h | 24 h | **PASS** |

**Chosen queue: `workq`**

---

### (b) Ranks-per-Node and GPUs-per-Rank from Application Defaults

- **Scaling guidance supplied**: “One MPI rank per GPU is recommended (−ntmpi 8 for 8 GPUs per node). −gpu_id 01234567 maps ranks 0–7 to GPUs 0–7.”
- **Sirius hardware**: 4× A100 GPUs per node.
- **Build default listed (8 ranks/node)** targets an 8-GPU node; the *scaling guidance* overrides this for the actual hardware.
- **Therefore**: **4 ranks per node** (1 rank per GPU), **1 GPU per rank**.
- `-gpu_id 0123` will map the 4 local ranks to the 4 GPUs.

---

### (c) Timing Assumptions Stated Plainly

- No measured throughput was supplied.
- Assumed **50 ns/day/GPU** (conservative for 34k atoms on A100).
- Assumed **75 % strong-scaling efficiency** on 4 GPUs.
- Applied **4× safety margin** to raw compute time.
- Resulting request: **4 hours** — well below the 24 h ceiling.

---

### (d) Scaling Guidance Honored

- Guidance: “One MPI rank per GPU is recommended.” → **Applied directly** (4 GPUs → 4 ranks/node).
- Guidance: “Multi-node: combine with thread-MPI or standard MPI; set −ntomp for OpenMP threading.” → **Not used** — system size (34k atoms) is too small to benefit from multi-node scaling; 1 node (4 GPUs) provides ample throughput and better parallel efficiency.
- Guidance: “For CPU-only PME: use −pme cpu −npme 1 with fewer GPU ranks.” → **Not used** — GPU-resident PME is preferred on A100.

---

### (e) Final Resource Specification

| Resource | Value | Derivation |
|----------|-------|------------|
| **Nodes** | **1** | Sufficient for 34k-atom system; fits queue 1–4 node range. |
| **Ranks per node** | **4** | 1 rank per GPU (scaling guidance); 4 GPUs/node on Sirius. |
| **Total ranks** | **4** | 1 node × 4 ranks/node = **4**. |
| **GPUs per node** | **4** | All A100s on the node utilized. |
| **GPUs per rank** | **1** | Direct 1:1 mapping via `−gpu_id 0123`. |
| **Walltime** | **04:00:00** | 4× margin on conservative 48-minute raw estimate. |
| **Queue** | **workq** | Only queue; passes node-min, node-max, and walltime limits. |

**Verification**: Total ranks = Nodes × Ranks per node = 1 × 4 = **4** ✓
````
