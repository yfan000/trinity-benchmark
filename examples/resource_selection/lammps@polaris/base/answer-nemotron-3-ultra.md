# nemotron-3-ultra — lammps@polaris, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**Resource specification and reasoning**

---

### (a) Queue selection – step by step

**1. Size the work and derive the walltime actually needed**  
- Problem: 500 000 atoms, 100 000 timesteps, Lennard‑Jones (cutoff 2.5 σ), NVE.  
- Hardware: 1 node = 4 × A100 GPUs, 4 MPI ranks/node (1 GPU/rank) via Kokkos.  
- No prior runs on Polaris; performance must be estimated.  

*Assumed performance* (conservative, based on published LAMMPS/Kokkos LJ benchmarks on A100):  
- ~150 M atom‑steps/s per GPU for a domain of ~125 k atoms (500 k / 4).  
- 4 GPUs → ~600 M atom‑steps/s aggregate.  
- Total atom‑steps = 500 000 × 100 000 = 5 × 10¹⁰.  
- Pure compute time ≈ 5 × 10¹⁰ / 6 × 10⁸ ≈ 83 s.  
- Add neighbour‑list rebuilds, communication, I/O, and scheduler variability → **~2 min typical run**.  

*Margin*: multiply by 10× for safety → **20 min**.  
*Requested walltime*: **0.5 h (30 min)** – comfortably above the estimate, well below any queue cap.

**2. Eliminate queues that cannot accept the request**  
Request: **nodes = 1**, **walltime = 0.5 h**.

| Queue           | Node range | Max walltime | Node min? | Node max? | Walltime? | Verdict |
|-----------------|------------|--------------|-----------|-----------|-----------|---------|
| debug           | 1–2        | 1 h          | 1 ≥ 1 ✓   | 1 ≤ 2 ✓   | 0.5 ≤ 1 ✓ | **PASS** |
| debug‑scaling   | 1–10       | 1 h          | 1 ≥ 1 ✓   | 1 ≤ 10 ✓  | 0.5 ≤ 1 ✓ | PASS    |
| prod            | 10–496     | 24 h         | 1 ≥ 10 ✗  | –         | –         | **FAIL** (node minimum) |
| demand          | 1–56       | 1 h          | 1 ≥ 1 ✓   | 1 ≤ 56 ✓  | 0.5 ≤ 1 ✓ | PASS    |
| preemptable     | 1–10       | 72 h         | 1 ≥ 1 ✓   | 1 ≤ 10 ✓  | 0.5 ≤ 72 ✓| PASS    |
| capacity        | 1–4        | 168 h        | 1 ≥ 1 ✓   | 1 ≤ 4 ✓   | 0.5 ≤ 168 ✓| PASS   |

**3. Choose a surviving queue**  
The **debug** queue is the natural choice for a first, short, single‑node run.  
*Verdict for debug queue* (all three limits must read PASS):

| Limit            | Requested | Queue limit | Pass/Fail |
|------------------|-----------|-------------|-----------|
| Node minimum     | 1         | 1           | PASS      |
| Node maximum     | 1         | 2           | PASS      |
| Maximum walltime | 0.5 h     | 1 h         | PASS      |

---

### (b) Ranks and GPUs from build defaults
- Build default: **4 MPI ranks per node**.  
- GPU note: “4 MPI ranks per node with 1 GPU each” → **4 GPUs per node** (matches the 4 × A100 hardware).  
- Node count is the only free parameter; we choose **nodes = 1**.

---

### (c) Assumptions and margin
- No measured timing exists for this workload on Polaris.  
- Performance assumed from typical LAMMPS/Kokkos LJ benchmarks on A100 (~150 M atom‑steps/s/GPU).  
- A 10× safety margin was added to the raw compute estimate (2 min → 20 min) and rounded to **0.5 h** for the walltime request.

---

### (d) Scaling guidance
The supplied note: *“Scale nodes for large systems (>1M atoms).”*  
This system has **500 000 atoms** (<1 M), so the guidance does **not** require multi‑node scaling. Running on a single node with 4 ranks (1 per GPU) follows the default configuration and is appropriate.

---

### (e) Final resource specification

| Parameter           | Value |
|---------------------|-------|
| **Nodes**           | 1     |
| **Ranks per node**  | 4     |
| **Total ranks**     | 4 ( = 1 × 4 ) |
| **GPUs per node**   | 4     |
| **Walltime**        | 0.5 h (30 min) |
| **Queue**           | debug |

All limits of the debug queue are satisfied, and the total ranks equal nodes × ranks per node.
````
