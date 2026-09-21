# nemotron-3-ultra — alphafold@perlmutter, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**Resource specification for a single AlphaFold prediction job in the parameter sweep**

---

### (a) Queue selection and wall‑time derivation  

**1. Work sizing and required wall‑time**  
- **Target:** human ubiquitin (76 residues, monomer)  
- **Task:** full database search (MSA generation on CPUs) + 5 model predictions with relaxation (on GPU)  
- **Hardware:** 1× NVIDIA A100 (40 GB) + 64 CPU cores (single Perlmutter node)  
- **Typical runtime breakdown (literature / experience for small proteins on A100):**  
  - MSA generation (CPU, 64 cores): 30–60 min  
  - Structure prediction + relaxation for 5 models (GPU): 30–60 min  
  - **Total baseline:** ~1–2 h  
- **Margin:** 2× to account for database I/O variability, queue wait, and potential longer relaxation → **requested wall‑time = 4 hours**  

**2. Queue elimination**  

| Queue          | Max wall‑time | Node range (given) | Eliminates? | Reason |
|----------------|---------------|--------------------|-------------|--------|
| express_amsc   | 6 h           | not specified      | No          | 4 h ≤ 6 h; 1 node allowed |
| debug          | 30 min        | 1–8                | **Yes**     | 4 h > 30 min (wall‑time) |
| regular        | 48 h          | not specified      | No          | 4 h ≤ 48 h; 1 node allowed |
| premium        | 48 h          | not specified      | No          | 4 h ≤ 48 h; 1 node allowed |
| shared         | 48 h          | not specified      | No          | 4 h ≤ 48 h; 1 node allowed |
| preempt        | 48 h          | 1–128              | No          | 4 h ≤ 48 h; 1 node in range |
| interactive    | 4 h           | 1–4                | No          | 4 h ≤ 4 h; 1 node in range |
| jupyter        | 6 h           | 1–4                | No          | 4 h ≤ 6 h; 1 node in range |
| overrun        | 48 h          | not specified      | No          | 4 h ≤ 48 h; 1 node allowed |

**3. Chosen queue: `regular`** (standard batch queue for production runs)  

| Limit               | Requested | Queue limit | Pass/Fail |
|---------------------|-----------|-------------|-----------|
| Node minimum        | 1         | 1 (implicit) | PASS      |
| Node maximum        | 1         | 3072 (system) | PASS      |
| Maximum wall‑time   | 4 h       | 48 h        | PASS      |

All three checks pass.

---

### (b) Ranks per node and GPUs per rank (from Build Defaults)  
- **Scaling guidance:** “Single GPU per run typical. Parallelize by submitting multiple jobs with different FASTA inputs.”  
- **Interpretation:** Each independent prediction run uses **one GPU** and is executed as a **single rank** (no intra‑job MPI parallelism).  
- Therefore: **ranks‑per‑node = 1**, **GPUs‑per‑rank = 1**.  
- Node count is the only free parameter; we choose **1 node** to match the single‑run-per-job model.

---

### (c) Assumptions and margins  
- No measured timings were supplied. The 4 h wall‑time is an **estimate** based on typical AlphaFold performance for a 76‑residue protein on an A100 with full databases, plus a 2× safety margin.  
- MSA generation is assumed to use all 64 CPU cores of the allocated node; structure prediction uses one GPU.  
- If the actual run exceeds 4 h, the job will be terminated by the scheduler; the margin is intended to make that unlikely.

---

### (d) Scaling guidance adherence  
The Build Defaults explicitly recommend **one GPU per prediction job** and parallelising across jobs, not within a job. This run follows that guidance exactly: one job = one prediction = one GPU = one rank.

---

### Final resource specification  

| Parameter          | Value |
|--------------------|-------|
| **Nodes**          | 1     |
| **Ranks per node** | 1     |
| **Total ranks**    | 1 (= 1 × 1) |
| **GPUs per node**  | 1     |
| **Wall‑time**      | 4 hours |
| **Queue**          | regular |

*Total ranks = nodes × ranks per node = 1 × 1 = 1 ✓*
````
