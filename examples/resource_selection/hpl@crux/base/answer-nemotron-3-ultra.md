# nemotron-3-ultra — hpl@crux, base arm

Resource selection. **FAIL** (correctness 1/2, completeness 2/2, usability 2/2; 2 of 10 requirements violated).

````
**Resource Specification and Reasoning for HPL LINPACK on Crux**

---

### (a) Queue Selection and Walltime Derivation

**1. Work Sizing and Required Walltime**  
The HPL run uses a 2×2 process grid (4 MPI ranks total) with problem size \(N=50{,}000\).  
Theoretical FLOP count: \(\frac{2}{3}N^3 \approx 8.33 \times 10^{13}\) FLOP.  
Assuming a modest per‑core HPL performance of 50 GFLOP/s (typical for modern CPUs with optimised BLAS), 4 cores deliver ≈200 GFLOP/s.  
Estimated compute time: \(8.33\times10^{13} / 2\times10^{11} \approx 416\) s ≈ 7 minutes.  
Adding a 2× safety margin for overhead, data distribution, and variability gives **≈15 minutes**.  
**Requested walltime = 0.5 hours (30 minutes)** – well within the 1‑hour cap of the short queues.

**2. Queue Elimination**  

| Queue          | Max Walltime | Node Range | Walltime Check (0.5 h ≤ Max?) | Node Check (1 ∈ Range?) | Verdict |
|----------------|--------------|------------|-------------------------------|-------------------------|---------|
| debug          | 1 h          | 1–8        | 0.5 ≤ 1 → **PASS**            | 1 ∈ [1,8] → **PASS**    | Survives |
| workq‑route    | 24 h         | 1–184      | 0.5 ≤ 24 → **PASS**           | 1 ∈ [1,184] → **PASS**  | Survives |
| preemptable    | 72 h         | 1–10       | 0.5 ≤ 72 → **PASS**           | 1 ∈ [1,10] → **PASS**   | Survives |
| demand         | 1 h          | 1–64       | 0.5 ≤ 1 → **PASS**            | 1 ∈ [1,64] → **PASS**   | Survives |

All four queues accept a 1‑node, 0.5‑hour request.

**3. Final Queue Choice**  
Turnaround is the priority. The **debug** queue is designed for short, small‑scale jobs (max 1 h, 1–8 nodes) and typically offers the fastest scheduling for such workloads.  
**Selected queue: debug**

**Verification against debug limits**  

| Limit               | Requested | Limit | Pass/Fail |
|---------------------|-----------|-------|-----------|
| Node minimum        | 1         | 1     | PASS      |
| Node maximum        | 1         | 8     | PASS      |
| Maximum walltime    | 0.5 h     | 1 h   | PASS      |

All three checks pass.

---

### (b) Ranks per Node and GPUs per Rank

The workload explicitly states a **2×2 process grid** → **total MPI ranks = 4**.  
The build default (128 ranks/node) reflects the code’s capability to use all 128 cores, but the HPL.dat input file fixes the process grid at 2×2, so only 4 ranks are launched.  
With **1 node** chosen, **ranks per node = 4**.  
The application is CPU‑only → **GPUs per node = 0**, **GPUs per rank = 0**.

---

### (c) Timing Assumptions and Margin

No measured performance data was supplied. The walltime estimate assumes:
- 50 GFLOP/s per core (conservative for HPL on current CPUs).
- 4 cores active (2×2 grid).
- 2× safety margin on the raw compute time.
The requested 0.5 h provides ample headroom.

---

### (d) Scaling Guidance

The build notes recommend using all 128 cores per node (128 ranks/node) and tuning \(P, Q\) accordingly.  
**This guidance does not apply** because the workload explicitly fixes the process grid at 2×2 (4 ranks total) via the provided HPL.dat. The run is a small‑scale, deadline‑sensitive test, not a full‑scale benchmark.

---

### (e) Final Resource Specification

| Parameter           | Value |
|---------------------|-------|
| **Nodes**           | 1     |
| **Ranks per node**  | 4     |
| **Total ranks**     | 4 (= 1 × 4) |
| **GPUs per node**   | 0     |
| **Walltime**        | 0.5 hours (30 minutes) |
| **Queue**           | debug |

All constraints satisfied; the request is legal and optimised for fastest turnaround.
````
