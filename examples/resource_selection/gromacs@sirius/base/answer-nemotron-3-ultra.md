# nemotron-3-ultra — gromacs@sirius, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 1 of 10 requirements violated).

````
**Resource Specification & Reasoning**

---

### (a) Queue Eligibility Check

Only one queue is defined for Sirius:

| Queue | Node Range | Max Walltime |
|-------|------------|--------------|
| workq | 1–4 nodes  | 24 h         |

**Step 1 – Size the work and derive required walltime**  
- System: ~34 000 atoms (HEWL in TIP3P/NaCl), 5 ns production, 2 fs step → 2.5 M steps.  
- No measured throughput supplied.  
- **Assumption:** On a single Sirius node (4×A100, 8 MPI ranks) a 34 k-atom PME system typically achieves **≈100 ns/day** (conservative; multi-GPU scaling is poor at this atom count).  
  - 5 ns ÷ 100 ns/day = 0.05 day ≈ **1.2 h**.  
- **Margin:** +50 % for restart overhead, I/O, and variability → **1.8 h**.  
- **Requested walltime:** **02:00:00** (2 h, rounded up to clean boundary).

**Step 2 – Eliminate queues that cannot satisfy the request**  
Only `workq` exists; it survives because:
- Node minimum (1) ≤ requested nodes (1) ≤ node maximum (4) → **PASS**
- Requested walltime (2 h) ≤ queue maximum (24 h) → **PASS**

**Step 3 – Final verdict per limit**

| Limit               | Requested | Queue Limit | Pass/Fail |
|---------------------|-----------|-------------|-----------|
| Node minimum        | 1         | 1           | PASS      |
| Node maximum        | 1         | 4           | PASS      |
| Maximum walltime    | 2 h       | 24 h        | PASS      |

All three checks pass. **Chosen queue: `workq`.**

---

### (b) Ranks & GPUs from Build Defaults
- **Ranks per node (build default):** 8 (fixed by how GROMACS was compiled).  
- **GPUs per node (hardware):** 4 (4×A100-SXM4-40GB).  
- The code’s scaling notes recommend one MPI rank per GPU, but the build default is 8 ranks/node; we honour the build default. At run time GROMACS will map the 8 ranks to the 4 GPUs via `-gpu_id` (e.g., two ranks per GPU or CPU-offloaded PME).

---

### (c) Walltime Assumption Statement
No timing measurement was supplied. The 2 h walltime is derived from an **assumed 100 ns/day on 1 node (8 ranks, 4 GPUs)** for this 34 k-atom system, plus a **50 % safety margin**. Actual throughput may differ; the margin is intended to absorb restart costs and queue variability.

---

### (d) Scaling Guidance Compliance
- Guidance: “One MPI rank per GPU is recommended.”  
- Constraint: Build default fixes ranks/node = 8 while hardware provides 4 GPUs/node.  
- Decision: **Use 1 node** (8 ranks, 4 GPUs). Going to 2–4 nodes would over-decompose the 34 k-atom system (≤2 125 atoms/rank), degrading performance. The single-node choice respects the hardware’s GPU count and the code’s build configuration.

---

### (e) Final Resource Specification

| Parameter          | Value          |
|--------------------|----------------|
| **Nodes**          | 1              |
| **Ranks per node** | 8 (build default) |
| **Total ranks**    | 8 (1 × 8)      |
| **GPUs per node**  | 4 (system)     |
| **Walltime**       | 02:00:00       |
| **Queue**          | workq          |

**Verification:** Total ranks = nodes × ranks per node = 1 × 8 = 8 ✓  
All queue limits satisfied ✓
````
