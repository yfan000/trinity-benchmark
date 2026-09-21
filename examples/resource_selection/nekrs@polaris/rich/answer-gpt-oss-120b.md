# gpt-oss-120b — nekrs@polaris, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**Step 1 – Estimate the wall‑time needed for the full production run**

* Measured on 1 node (4 GPUs, 4 MPI ranks):  
  1 000 timesteps → ≈ 8 min  

* Timesteps required for the production case: 20 000  

* Assuming the same per‑timestep cost and that the kernels are already cached  

\[
\text{time}_{1\;node}=8\;\text{min}\times\frac{20\,000}{1\,000}=160\;\text{min}=2\;h\,40\;min .
\]

*Add a safety margin* (I/O, slight loss of strong‑scaling efficiency, scheduler‑overhead):  
\(160\;\text{min}\times1.20 = 192\;\text{min}\).

If the job is run on **N nodes**, NekRS scales (≈ 1 rank / GPU) with almost perfect strong‑scaling, so the wall‑time is divided by N.

\[
t(N)=\frac{192\;\text{min}}{N}.
\]

**Step 2 – Queue inspection**

| Queue            | Node range | Max wall‑time | Can the job fit? (reason) |
|------------------|------------|---------------|---------------------------|
| **debug**        | 1‑2        | 1 h (60 min)  | *FAIL* – even on 2 nodes  t ≈ 96 min > 60 min |
| **debug‑scaling**| 1‑10       | 1 h (60 min)  | *FAIL* – 1‑2 nodes too slow; 3+ nodes would fit but we prefer a production queue |
| **demand**       | 1‑56       | 1 h (60 min)  | *FAIL* – same reason as debug‑scaling |
| **preemptable**  | 1‑10       | 72 h          | *PASS* – 1 node gives ≈ 3 h < 72 h, but this is a pre‑emptible queue |
| **capacity**     | 1‑4        | 168 h         | *PASS* – 1‑4 nodes allowed, wall‑time well below limit |
| **prod** (chosen) | **10‑496** | **24 h (1440 min)** | *PASS* – meets both node‑range and wall‑time limits |

**Why “prod” is the best legal queue**

* It is the regular production queue (non‑pre‑emptible).  
* Minimum node count (10) is modest and keeps the job short.  
* Wall‑time request will be far below the 24 h ceiling, avoiding any unnecessary booking of longer queues.

**Step 3 – Pick the concrete resources**

* **Node count:** 10  (minimum that satisfies the *prod* queue)  
* **Ranks per node:** 4  (build default, one MPI rank per GPU)  
* **GPUs per node:** 4  (A100 GPUs, one per rank)  
* **Total MPI ranks:** 10 nodes × 4 ranks = 40  
* **Estimated wall‑time on 10 nodes:**  

\[
t(10)=\frac{192\;\text{min}}{10}=19.2\;\text{min}\;\approx\;20\;\text{min (rounded up for safety, still \< 24 h)}.
\]

The 20 min request is comfortably within the 24 h limit; we do **not** round beyond the cap.

---

### Resource specification (the answer)

| Item                     | Value |
|--------------------------|-------|
| **Queue**                | `prod` |
| **Nodes**                | 10 |
| **GPUs per node**        | 4 |
| **Ranks per node**       | 4 |
| **Total MPI ranks**      | 40 (= 10 × 4) |
| **Wall‑time**            | 20 minutes |

**Verification**

*Node‑minimum:* 10 ≥ 10 → **PASS**  
*Node‑maximum:* 10 ≤ 496 → **PASS**  
*Wall‑time‑maximum:* 20 min ≤ 1440 min → **PASS**

All limits are satisfied, the job can be submitted to the `prod` queue on Polaris.
````
