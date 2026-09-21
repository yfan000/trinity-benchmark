# gpt-oss-120b — nekrs@polaris, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**Step‑by‑step reasoning**

| Step | What we did | Result |
|------|--------------|--------|
| 1.  Estimate time needed for the full run (20 000 timesteps) on a *single* node | 1 000 timesteps → 8 min  ⇒ 0.48 s per timestep. <br>20 000 timesteps × 0.48 s = 9 600 s = **160 min** (≈ 2 h 40 min).<br>Add a 25 % safety margin (common practice for production runs) → **200 min** (≈ 3 h 20 min) of “baseline” work. | Baseline wall‑time = 200 min on 1 node. |
| 2.  Choose a node count that gives the desired wall‑time | NekRS uses one MPI rank per GPU; on Polaris that is **4 ranks / node** (one rank per A100). <br>Strong‑scaling on this problem is close to linear up to the tens‑of‑nodes regime. <br>Target wall‑time ≈ 30 min (well within most queues). <br>Needed speed‑up ≈ 200 min / 30 min ≈ 7 ×. <br>Using **10 nodes** (40 GPUs, 40 MPI ranks) gives a theoretical ≈ 10× speed‑up, giving an expected wall‑time ≈ 20 min; with safety margin we request **30 min**. | Decision – **10 nodes** (40 GPUs, 40 ranks). |
| 3.  Compare the request with every queue and discard those that cannot satisfy at least one limit | • **debug** – node range 1‑2 → *FAIL* (needs 10 nodes). <br>• **debug‑scaling** – node range 1‑10, max wall‑time 1 h → *PASS*. <br>• **prod** – node range 10‑496, max wall‑time 24 h → *PASS*. <br>• **demand** – node range 1‑56, max wall‑time 1 h → *PASS* (but node max 56, fine). <br>• **preemptable** – node range 1‑10, max wall‑time 72 h → *PASS*. <br>• **capacity** – node range 1‑4 → *FAIL* (needs 10 nodes). | Surviving queues: debug‑scaling, prod, demand, preemptable. |
| 4.  Pick the *best* surviving queue and verify each individual limit | Chosen queue: **debug‑scaling** (the shortest turnaround queue that still meets the limits). <br>‑ Node minimum: 1 ≤ 10 → **PASS**. <br>‑ Node maximum: 10 ≥ 10 → **PASS**. <br>‑ Wall‑time limit: 1 h ≥ 30 min → **PASS**. | All three checks PASS. |

**Scaling guidance** – NekRS is built with the default *4 ranks / node* (one MPI rank per GPU). No other scaling constraints were supplied, so we keep that default.

---

### (a) Queue choice summary

| Queue          | Node range | Wall‑time limit | Requested nodes | Requested wall‑time | Verdict (min nodes) | Verdict (max nodes) | Verdict (wall‑time) |
|----------------|------------|-----------------|-----------------|---------------------|---------------------|---------------------|---------------------|
| debug‑scaling  | 1 – 10     | 1 h             | **10**          | **00:30:00**        | PASS (1 ≤ 10)       | PASS (10 ≤ 10)      | PASS (30 min ≤ 1 h) |
| prod           | 10 – 496   | 24 h            | 10              | 00:30:00            | PASS                | PASS                | PASS |
| demand         | 1 – 56     | 1 h             | 10              | 00:30:00            | PASS                | PASS                | PASS |
| preemptable    | 1 – 10     | 72 h            | 10              | 00:30:00            | PASS                | PASS                | PASS |

The **debug‑scaling** queue is selected because it meets all limits and offers the shortest turnaround.

---

### (b) Ranks‑per‑node & GPUs‑per‑node

* Build default for NekRS on Polaris: **4 ranks / node** (one rank per A100 GPU).  
* Therefore each node supplies **4 GPUs** and **4 MPI ranks**.

---

### (c) Timing assumption & margin

* Measured 1 000 timesteps = 8 min ⇒ 0.48 s per timestep.  
* Extrapolated to 20 000 timesteps → 160 min on 1 node.  
* Added a 25 % safety margin → 200 min baseline.  
* Expected speed‑up with 10 nodes ≈ 10× → ~20 min.  
* Requested wall‑time 30 min gives a further 50 % cushion.

No other measured throughput figures are used.

---

### (d) Application‑specific scaling note

NekRS uses **one MPI rank per GPU**; the code was built with the default of 4 ranks per node on Polaris.  Scaling is achieved simply by adding more nodes (hence more GPUs).  No special “ranks‑per‑node” or “GPU‑per‑rank” tuning is required for this problem.

---

## (e) Final resource specification

| Item                     | Value |
|--------------------------|-------|
| **Nodes**                | **10** |
| **GPUs per node**        | **4** (A100) |
| **Ranks per node**       | **4** |
| **Total ranks**          | **10 × 4 = 40** |
| **Wall‑time**            | **00:30:00** (30 minutes) |
| **Queue**                | **debug‑scaling** |
| **Working directory**    | `/eagle/PlasmaEdge/mrossi/nekrs_run` |
| **Input files**          | `case.par`, `case.re2`, `case.udf` |

**Check:** 40 total ranks = 10 nodes × 4 ranks per node → **consistent**.

This specification satisfies all queue limits, respects the application’s defaults, and includes a reasonable safety margin based on the measured single‑node performance.
````
