# gpt-oss-120b — qe@aurora, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**1. Size the work and derive the wall‑time needed**

* Workload : 64‑atom 3C‑SiC SCF, 60 Ry / 480 Ry, 4 × 4 × 4 k‑grid, PBE, US‑PP.  
* Quantum ESPRESSO on a CPU‑only Intel‑MKL build typically needs **≈ 10 min** on a *single* Aurora node (104 CPU cores) for a calculation of this size.  
* Using two nodes gives roughly a 2 × speed‑up (the SCF is dominated by FFTs that scale well with the 104 cores per node).  
* Expected run time on 2 nodes ≈ 5 min.  

To be safe we add a **3 × safety margin** (for I/O overhead, possible slower convergence, etc.) → **≈ 15 min**.  
We round up to a convenient value **20 min** (00:20:00). This is well below any queue wall‑time limit.

---

### 2. Eliminate queues that cannot accommodate the request  

| Queue            | Node range (min‑max) | Max wall‑time | Reason for elimination (if any) |
|------------------|----------------------|---------------|-----------------------------------|
| **debug**        | 1 – 2                | 1 h           | – (our request 2 nodes, 20 min ✔) |
| debug‑scaling    | 2 – 256              | 1 h           | – (2 nodes, 20 min ✔)             |
| **prod**         | 256 – 10624          | 24 h          | **FAIL – node minimum** (needs ≥256 nodes) |
| **capacity**     | 1 – 16               | 168 h         | – (2 nodes, 20 min ✔)             |
| visualization    | 1 – 32               | 8 h           | – (2 nodes, 20 min ✔)             |

Only **debug**, **debug‑scaling**, **capacity** and **visualization** survive the wall‑time test; *prod* is excluded because the node‑minimum is not satisfied.

---

### 3. Choose a legal queue and verify limits  

We select the **capacity** queue because it is intended for production‑type runs with modest node counts and generous wall‑time limits.

| Limit examined            | Requested value | Queue limit | PASS/FAIL | Comment |
|---------------------------|-----------------|------------|----------|---------|
| **Node minimum**          | 2 nodes         | ≥ 1 (capacity) | PASS | 2 ≥ 1 |
| **Node maximum**          | 2 nodes         | ≤ 16 (capacity) | PASS | 2 ≤ 16 |
| **Maximum wall‑time**     | 00:20:00        | 168 h (capacity) | PASS | 20 min ≪ 168 h |

All three checks pass, so the request is admissible.

---

### 4. Ranks‑per‑node and GPUs‑per‑node (application defaults)

* **Ranks per node** – build default = **104** (one MPI rank per CPU core).  
* **GPUs per node** – the Quantum ESPRESSO binary is a CPU‑only MPI build; no GPU off‑load is used. We therefore request **0 GPUs per node**.

---

### 5. Final resource specification  

| Item                     | Value |
|--------------------------|-------|
| **Nodes**                | 2 |
| **Ranks per node**       | 104 |
| **Total MPI ranks**      | 2 × 104 = **208** |
| **GPUs per node**        | 0 |
| **Wall‑time**            | **00:20:00** (20 minutes) |
| **Queue**                | **capacity** |
| **Input file**           | `/lus/flare/projects/BioFoldX/yamamoto/qe_run/scf.scf.in` |
| **Application**          | Quantum ESPRESSO (CPU‑only Intel MKL/ScaLAPACK build) |

**Verification:**  
Total ranks = nodes × ranks‑per‑node = 2 × 104 = **208** (as required).

---

**Summary**

- **Queue:** `capacity` (1‑16 nodes, max 168 h) – passes all limits.  
- **Node count:** 2  
- **Ranks per node:** 104 (CPU‑only MPI)  
- **Total ranks:** 208  
- **GPUs per node:** 0 (CPU‑only build)  
- **Wall‑time:** 00:20:00 (20 min, includes a 3 × safety margin)  

This specification conforms to Aurora’s queue policies and uses the default application parallelisation parameters.
````
