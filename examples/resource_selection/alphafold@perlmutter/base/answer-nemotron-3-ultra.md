# nemotron-3-ultra — alphafold@perlmutter, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**1. Size the work and derive the walltime**  
The workload is a single AlphaFold prediction for a 76‑residue monomer (human ubiquitin) with a full database search and 5 models including relaxation.  
- MSA search (CPU‑bound, can use all 64 cores on a node): ~20 min for a small protein with full databases.  
- Structure prediction on one A100 GPU (5 models × relaxation): ~40 min.  
- Sequential total ≈ 60 min. Adding a 50 % safety margin for database load variability and queue delays gives **90 min**. Rounding up to a clean scheduler limit yields a **requested walltime of 2 hours (2:00:00)**.  

**2. Eliminate queues that cannot accommodate the request**  
We plan to run one job per prediction, requiring **1 node** (1 GPU). The table below checks each queue against the two hard limits: maximum walltime and allowed node range (where specified).  

| Queue          | Max walltime | Node range (if given) | Walltime ≥ 2 h? | 1 node in range? | Verdict |
|----------------|--------------|-----------------------|-----------------|------------------|---------|
| express_amsc   | 6 h          | –                     | PASS            | assumed PASS     | survives |
| debug          | 30 min       | 1‑8 nodes             | **FAIL** (30 min < 2 h) | PASS         | **rejected** |
| regular        | 48 h         | –                     | PASS            | assumed PASS     | survives |
| premium        | 48 h         | –                     | PASS            | assumed PASS     | survives |
| shared         | 48 h         | –                     | PASS            | assumed PASS     | survives |
| preempt        | 48 h         | 1‑128 nodes           | PASS            | PASS             | survives |
| interactive    | 4 h          | 1‑4 nodes             | PASS            | PASS             | survives |
| jupyter        | 6 h          | 1‑4 nodes             | PASS            | PASS             | survives |
| overrun        | 48 h         | –                     | PASS            | assumed PASS     | survives |

Only **debug** is eliminated because its 30‑minute walltime cap is below the 2‑hour requirement. All other queues satisfy both limits for a 1‑node, 2‑hour job.

**3. Choose a queue and verify the three limits explicitly**  
For a production‑style parameter sweep the **regular** queue is the standard choice. Its limits are checked below:

| Limit                | Requested value | Queue limit | Pass/Fail |
|----------------------|-----------------|-------------|-----------|
| Node minimum         | 1               | (none stated, 1 assumed allowed) | **PASS** |
| Node maximum         | 1               | (none stated, no upper bound)    | **PASS** |
| Maximum walltime     | 2 h             | 48 h        | **PASS** |

All three checks pass.

**4. Ranks‑per‑node and GPUs‑per‑rank from Build Defaults**  
The Build Defaults state:  
- “Single GPU per run typical.”  
- “Scaling notes: Single GPU per prediction job. Parallelize by submitting multiple jobs with different FASTA inputs.”  

This means each independent prediction (each job in the sweep) is a **single‑rank, single‑GPU** task. Therefore:  
- **GPUs per rank = 1**  
- **Ranks per node = 1** (we allocate one node for one job; the other three GPUs on the node would be available for other jobs, but this specification describes one job).  

**5. Scaling guidance**  
The guidance explicitly advises against multi‑GPU or multi‑node parallelism for a single prediction and recommends submitting many independent jobs. This run follows that guidance exactly: one job = one prediction = one rank = one GPU.

**6. Final resource specification**  

| Parameter          | Value |
|--------------------|-------|
| Nodes              | 1     |
| Ranks per node     | 1     |
| Total ranks        | 1 (= 1 × 1) |
| GPUs per node      | 1     |
| Walltime           | 2:00:00 |
| Queue              | regular |

This specification obeys all queue limits, matches the application’s single‑GPU execution model, and provides a safe walltime margin for the described workload.
````
