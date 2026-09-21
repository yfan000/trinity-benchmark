# nemotron-3-ultra — nwchem@polaris, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
### (a) Queue Selection and Legality Check

#### 1. Work Sizing and Walltime Derivation
- **Reference measurement**: The prompt states a single-node run of this exact calculation completed in **5 s** wall time.  
- **Scaling behaviour**: This is a strong‑scaling benchmark on a *fixed, tiny* problem (one water molecule). As node count increases, the compute time per rank drops, but communication/startup overhead grows. For a 10‑node run (the upper end of the “small range” requested) we conservatively assume the wall time will not exceed **30 s** (6× the single‑node time, allowing for MPI/GA overhead).  
- **Safety margin**: Add a generous margin for scheduler dispatch, module loads, and potential contention → **5 minutes (00:05:00)** requested walltime.  
- **Assumption**: No measured data for multi‑node runs exists; the 5 s single‑node figure is the only timing supplied. The 30 s estimate and 5 min request are purely assumptions with a large margin.

#### 2. Queue Elimination
| Queue           | Node Range | Max Walltime | Node Count (10) | Walltime (5 min) | Verdict                     |
|-----------------|------------|--------------|-----------------|------------------|-----------------------------|
| debug           | 1–2        | 1 h          | **FAIL** (max 2) | PASS             | Excluded – node max too low |
| **debug‑scaling** | **1–10**   | **1 h**      | **PASS**        | **PASS**         | **Survives**                |
| prod            | 10–496     | 24 h         | PASS            | PASS             | Survives                    |
| demand          | 1–56       | 1 h          | PASS            | PASS             | Survives                    |
| preemptable     | 1–10       | 72 h         | PASS            | PASS             | Survives                    |
| capacity        | 1–4        | 168 h        | **FAIL** (max 4) | PASS             | Excluded – node max too low |

#### 3. Final Queue Choice: `debug-scaling`
| Limit               | Requested | Limit   | Pass? |
|---------------------|-----------|---------|-------|
| Node minimum        | 10        | 1       | PASS  |
| Node maximum        | 10        | 10      | PASS  |
| Maximum walltime    | 00:05:00  | 01:00:00| PASS  |

*Reason for choosing `debug-scaling`*: It is explicitly named for scaling studies, covers the desired 1–10 node range, and its 1 h walltime cap comfortably admits the 5 min request. The `prod` queue would also work but is intended for production runs; `demand` and `preemptable` are less targeted for this purpose.

---

### (b) Ranks and GPUs from Build Defaults
- **Ranks per node**: 4 (build default, CPU‑only MPI ranks).  
- **GPUs per node**: 0 (NWChem build is CPU‑only; GPU support is experimental and not used).

---

### (c) Timing Assumptions and Margin
- **Measured data**: Only the single‑node time of 5 s is provided.  
- **Assumed multi‑node time**: ≤30 s for 10 nodes (strong scaling of a tiny problem).  
- **Requested walltime**: 00:05:00 (5 min), giving a **10× margin** over the assumed worst case to cover startup, queue delays, and load imbalance.

---

### (d) Scaling Guidance Compliance
- **Ranks per node**: Set to 4, exactly as the build default directs.  
- **“Scale nodes for larger molecular systems”**: The workload explicitly asks for a scaling benchmark on a *single water molecule* (a very small system). This contradicts the guidance’s intent, but the exercise requires the benchmark anyway. We honour the ranks‑per‑node directive and note that strong scaling on this problem will likely saturate quickly due to communication overhead.  
- **Memory settings**: The input file (`run.nw`) must set `memory stack/heap/global` appropriately to avoid OOM errors, as advised.

---

### (e) Final Resource Specification
| Parameter          | Value |
|--------------------|-------|
| **Nodes**          | 10    |
| **Ranks per node** | 4     |
| **Total ranks**    | 40    |
| **GPUs per node**  | 0     |
| **Walltime**       | 00:05:00 |
| **Queue**          | debug-scaling |

**Verification**: Total ranks = nodes × ranks per node = 10 × 4 = 40.
````
