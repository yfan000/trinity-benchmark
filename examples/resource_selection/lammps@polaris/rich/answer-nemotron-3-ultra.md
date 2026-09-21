# nemotron-3-ultra — lammps@polaris, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**Resource Specification and Reasoning**

---

### (a) Choose a Legal Queue

#### 1. Size the work and derive the walltime needed
- **Problem**: 500,000 atoms, 100,000 timesteps → 5×10¹⁰ atom‑steps.
- **Hardware**: 1 node = 4× A100 GPUs. With the Kokkos backend each MPI rank uses 1 GPU (build default: 4 ranks/node).
- **Performance assumption**: No prior runs on Polaris exist. A conservative estimate for LAMMPS LJ on A100 with Kokkos is **~100 million atom‑steps/s per GPU** (≈4×10⁸ atom‑steps/s per node).  
  Compute time ≈ 5×10¹⁰ / 4×10⁸ = **125 seconds (≈2 minutes)**.
- **Overhead & uncertainty**: Neighbor‑list rebuilds, communication, I/O, startup, and the fact that this is a first run on the system justify a large safety margin. Apply a **10× margin** → 1250 s (≈21 min), then add **50% extra margin** → **≈31 minutes**.  
  **Requested walltime = 45 minutes (0:45:00)** – comfortably below the 1‑hour cap of the debug queues.

#### 2. Eliminate queues that cannot accept the request
| Queue            | Node range | Max walltime | Node min (1) | Node max (1) | Walltime (45 min) | Verdict |
|------------------|------------|--------------|--------------|--------------|-------------------|---------|
| **debug**        | 1–2        | 1 h (60 min) | PASS (1≥1)   | PASS (1≤2)   | PASS (45≤60)      | **Survives** |
| debug‑scaling    | 1–10       | 1 h          | PASS         | PASS         | PASS              | Survives |
| prod             | 10–496     | 24 h         | **FAIL** (min 10 > 1) | – | – | Eliminated |
| demand           | 1–56       | 1 h          | PASS         | PASS         | PASS              | Survives |
| preemptable      | 1–10       | 72 h         | PASS         | PASS         | PASS              | Survives |
| capacity         | 1–4        | 168 h        | PASS         | PASS         | PASS              | Survives |

#### 3. Choose the surviving queue and verify all three limits
**Selected queue: `debug`** (standard queue for short test/debug runs; this is the first run of the workload on Polaris).

| Limit            | Requested | Limit   | Pass? |
|------------------|-----------|---------|-------|
| Node minimum     | 1         | 1       | PASS  |
| Node maximum     | 1         | 2       | PASS  |
| Maximum walltime | 45 min    | 60 min  | PASS  |

All three checks pass.

---

### (b) Ranks per node and GPUs per rank (from build defaults)
- **Ranks per node** = 4 (build default)  
- **GPUs per rank** = 1 (each rank binds to one A100; 4 GPUs/node → 4 ranks/node)  
- **GPUs per node** = 4  

---

### (c) Assumptions and margins
- **Performance assumption**: 100 M atom‑steps/s/GPU (conservative, based on typical LAMMPS/Kokkos LJ numbers for A100).  
- **Margin**: 10× for overhead/uncertainty + 50% extra → total ~15× margin over raw compute estimate.  
- No measured timing exists; the walltime is a conservative upper bound.

---

### (d) Scaling guidance
The supplied note: *“Scale nodes for large systems (>1M atoms).”*  
This system has **500,000 atoms (<1M)**, so **no multi‑node scaling is required**. Running on a single node follows the guidance.

---

### (e) Final resource specification

| Parameter          | Value |
|--------------------|-------|
| **Nodes**          | 1 |
| **GPUs per node**  | 4 |
| **MPI ranks per node** | 4 |
| **Total MPI ranks** | 1 × 4 = **4** |
| **Walltime**       | 0:45:00 (45 minutes) |
| **Queue**          | debug |

**Consistency check**: Total ranks = nodes × ranks per node = 1 × 4 = 4 ✓
````
