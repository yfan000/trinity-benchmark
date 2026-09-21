# gpt-oss-120b — hpl@crux, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**Resource specification (what will be submitted to PBS Pro)**  

| Item                      | Value                           |
|---------------------------|---------------------------------|
| Nodes                     | **8**                           |
| GPUs per node             | **0** (CPU‑only)                |
| Ranks per node (built‑in) | **128**                         |
| Total MPI ranks           | **8 × 128 = 1024**               |
| Wall‑time (hh:mm:ss)      | **00:15:00** (15 minutes)       |
| Queue                     | **debug**                       |
| Working directory         | /eagle/CosmoSurvey/dokafor/hpl_run |
| HPL process grid (P × Q)  | 32 × 32 (fits 1024 ranks)       |
| HPL problem size N        | 50000 (as given)                |
| HPL block size NB         | 232 (as given)                  |

---

### Reasoning

#### (a) Choose a legal queue  

1. **Estimate the wall‑time needed**  
   * HPL FLOP count ≈ \( \frac{2}{3}N^{3} = \frac{2}{3}(5\times10^{4})^{3}=8.33\times10^{13}\) flops.  
   * Crux node: 128 CPU cores, each ≈ 10 GFLOP s⁻¹ → peak per node ≈ 1.28 TFLOP s⁻¹.  
   * With 8 nodes the theoretical peak ≈ 10.2 TFLOP s⁻¹.  
   * Assuming 80 % of peak for HPL (typical for a well‑tuned run) → ≈ 8.2 TFLOP s⁻¹.  
   * Expected run time = \(8.33\times10^{13}\) flops ÷ \(8.2\times10^{12}\) flops s⁻¹ ≈ 10 s.  
   * To be safe we add a generous 5‑minute margin for I/O, startup, possible slower scaling and for the scheduler’s bookkeeping → **15 minutes** wall‑time.

2. **Eliminate queues whose limits are too low**  

| Queue            | Node‑range   | Max wall‑time | Reason for elimination (if any) |
|------------------|--------------|---------------|----------------------------------|
| debug            | 1‑8          | 1 h           | **Keeps** – 8 nodes ⟶ inside range, 15 min ⟶ ≤ 1 h |
| workq‑route      | 1‑184        | 24 h          | **Keeps** – permissive, but longer wait times than debug |
| preemptable      | 1‑10         | 72 h          | **Keeps** – permissive, but pre‑emptable jobs may be paused |
| demand           | 1‑64         | 1 h           | **Keeps** – meets limits, but typically higher queue time than debug |

3. **Select the best surviving queue** – The **debug** queue has the smallest expected queue‐time (it is meant for short, interactive or turnaround‑sensitive jobs) and its limits are all satisfied:

| Limit                | Requested value | Queue limit | PASS/FAIL |
|----------------------|-----------------|------------|-----------|
| Minimum nodes        | 8 ≥ 1           | 1          | PASS |
| Maximum nodes        | 8 ≤ 8           | 8          | PASS |
| Maximum wall‑time    | 00:15:00 ≤ 01:00:00 | 1 h   | PASS |

All three checks pass, so **debug** is the chosen queue.

#### (b) Ranks‑per‑node and GPUs‑per‑node  

* The HPL build reports **128 ranks per node**; this is taken as‑is.  
* No GPUs are present on Crux, so **0 GPUs per node**.

Consequently the total number of MPI ranks is **nodes × ranks‑per‑node = 8 × 128 = 1024**.  
To use all ranks the HPL input file must be edited so that **P × Q = 1024**. The square‑root gives a balanced grid **P = Q = 32**, which is consistent with the scaling note *“maximize performance by using all 128 cores per node.”*

#### (c) Timing assumption  

No measured runtime was supplied, so we **assumed** peak node performance based on core count (≈10 GFLOP s⁻¹ per core) and used a **5‑minute safety margin** on top of the theoretical 10 second runtime. The final wall‑time request (15 min) is therefore a conservative estimate well within the queue’s 1‑hour ceiling.

#### (d) Scaling guidance  

The supplied guidance states that the benchmark is **CPU‑only** and should **use all 128 cores per node**. By allocating the full 128 ranks per node and a 32 × 32 process grid we honour this recommendation. No GPU scaling is required.

#### (e) Restatement  

- **Nodes:** 8  
- **Ranks per node:** 128 (from build default)  
- **Total ranks:** 8 × 128 = 1024  
- **GPUs per node:** 0  
- **Wall‑time:** 00:15:00 (15 min) – ≤ 1 h limit, includes margin  
- **Queue:** debug  

This specification satisfies all PBS Pro limits, follows the provided scaling guidance, and targets the queue with the quickest expected turnaround for a deadline‑sensitive HPL run on Crux.
````
