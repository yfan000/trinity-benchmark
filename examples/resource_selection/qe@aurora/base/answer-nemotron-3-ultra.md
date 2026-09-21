# nemotron-3-ultra — qe@aurora, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**Resource Specification and Reasoning for Aurora Production DFT Campaign**

---

### (a) Queue Selection — Step-by-Step

#### 1. Size the Work and Derive Required Walltime

**Problem size:**
- 64-atom supercell (3C-SiC, zinc-blende, 2×2×2 conventional)
- Plane-wave cutoff: 60 Ry → ~50,000–80,000 plane waves per k-point (typical for SiC at this cutoff)
- Charge-density cutoff: 480 Ry (8× wavefunction cutoff, standard for ultrasoft PP)
- k-grid: 4×4×4 Monkhorst-Pack = 64 k-points; symmetry reduces to ~10–15 irreducible k-points
- SCF iteration count: 12–20 typical for PBE/ultrasoft SiC to convergence
- Software: Quantum ESPRESSO `pw.x`, CPU-only MPI build (Intel MKL FFT + ScaLAPACK), **no GPU offload** (Intel GPUs not supported by this build)

**Performance assumption (no measured data supplied):**
- On Aurora’s 104-core Intel Xeon CPU Max Series (Sapphire Rapids) per node, a 64-atom/60 Ry SCF with ~12 irreducible k-points runs at roughly **20–35 minutes** for a converged SCF cycle when using 104 MPI ranks (1 rank/core).
- **Assumed base time:** 30 minutes (conservative mid-range).
- **Safety margin:** 2× (covers SCF variability, I/O, queue startup, load imbalance) → **60 minutes = 1 hour**.
- **Requested walltime:** **1:00:00** (1 hour).  
  *No timing is claimed as measured; this is an assumption with explicit 2× margin.*

#### 2. Eliminate Queues That Cannot Accept the Request

| Queue | Node Range | Max Walltime | Node Count Requested (1) | Walltime Requested (1 h) | Ruling Limit | Eliminated? |
|-------|------------|--------------|--------------------------|--------------------------|--------------|-------------|
| debug | 1–2 | 1 h | 1 ∈ [1,2] ✓ | 1 h ≤ 1 h ✓ | — | **No** |
| debug-scaling | 2–256 | 1 h | 1 < 2 ✗ | — | **Node minimum (2)** | **Yes** |
| prod | 256–10624 | 24 h | 1 < 256 ✗ | — | **Node minimum (256)** | **Yes** |
| capacity | 1–16 | 168 h | 1 ∈ [1,16] ✓ | 1 h ≤ 168 h ✓ | — | **No** |
| visualization | 1–32 | 8 h | 1 ∈ [1,32] ✓ | 1 h ≤ 8 h ✓ | — | **No** |

**Surviving queues:** `debug`, `capacity`, `visualization`.

#### 3. Choose the Appropriate Production Queue and Verify All Three Limits

Campaign requirement: **“production DFT campaign”** → `debug` (debugging only) and `visualization` (interactive/rendering) are semantically wrong.  
**Chosen queue:** `capacity` (designed for production runs ≤ 16 nodes, up to 7 days).

**Limit-by-limit verification for `capacity` queue with 1 node, 1 h walltime:**

| Limit | Requested | Queue Limit | Pass/Fail |
|-------|-----------|-------------|-----------|
| Node minimum | 1 | 1 | **PASS** |
| Node maximum | 1 | 16 | **PASS** |
| Maximum walltime | 1:00:00 | 168:00:00 | **PASS** |

All three checks read **PASS**. The request is scheduler-legal.

---

### (b) Ranks per Node and GPUs per Rank — From Build Defaults

- **Ranks per node (build default):** 104 (1 rank per CPU core, CPU-only MPI build with Intel MKL + ScaLAPACK).  
  *Only node count is chosen by the agent; ranks-per-node is fixed by the build.*
- **GPUs per rank:** 0. The supplied build notes state: “CPU-only MPI build (Intel MKL FFT). GPU offload via pw_gpu requires NVIDIA; Aurora uses Intel GPUs.” → **No GPU offload is used or available for this executable.**
- **GPUs per node (physical):** 6 (Intel Data Center GPU Max Series), but **0 used by this workload**.

---

### (c) Timing Assumptions Stated Plainly

- **Base estimate:** 30 minutes for SCF convergence (64 atoms, 60 Ry, 4×4×4 k-grid, ultrasoft PP, 104 ranks).
- **Margin added:** 2× (100 %) → **1 hour requested**.
- **No measurement or observation is claimed**; the figure is a conservative assumption for a production allocation.

---

### (d) Scaling Guidance Honoured

- **Strong-scaling ceiling:** Plane-wave DFT with ~60k plane waves and ~12 irreducible k-points typically scales well to ~64–128 cores. 104 ranks (1 node) sits at the upper end of efficient scaling for this problem size; adding a second node (208 ranks) would increase communication overhead (ScaLAPACK redistributions, FFT transposes) and **degrade time-to-solution**.
- **Weak scaling not applicable** (single SCF job, not a campaign of increasing systems).
- **Therefore:** 1 node is the correct choice; larger node counts violate the application’s scaling guidance and waste allocation.

---

### Final Resource Specification

| Parameter | Value | Derivation |
|-----------|-------|------------|
| **Nodes** | 1 | Chosen to match problem scaling; passes `capacity` queue limits |
| **Ranks per node** | 104 | Build default (1 rank/core, CPU-only MPI) |
| **Total ranks** | 104 | 1 node × 104 ranks/node = **104** |
| **GPUs per node (used)** | 0 | CPU-only build; Intel GPUs not supported by `pw_gpu` |
| **Walltime** | 1:00:00 | 30 min base × 2× safety margin; ≤ 168 h `capacity` limit |
| **Queue** | `capacity` | Only production-eligible queue admitting 1 node, 1 h |

**Verification:**  
Total ranks (104) = Nodes (1) × Ranks per node (104) ✓  
All queue limits satisfied ✓  
Scaling guidance respected ✓
````
