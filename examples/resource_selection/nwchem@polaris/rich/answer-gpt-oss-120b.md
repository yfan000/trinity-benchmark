# gpt-oss-120b — nwchem@polaris, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**(a) Choose a legal queue**

| Step | Action                                                                                                                                        | Result |
|------|-----------------------------------------------------------------------------------------------------------------------------------------------|--------|
| 1. Size the work & derive wall‑time | • A single‑node NWChem run of the water‑molecule test finishes in **≈ 5 s**. <br>• For a scaling benchmark we will run the same calculation on several node counts (1 → 4 → 8 → 16 …). <br>• To give the scheduler a realistic request we add a generous safety margin (≈ 2 min) so the job is not rejected for being “too short”. <br>• **Requested wall‑time = 00:10:00 (10 min).** | – |
| 2. Eliminate queues that cannot satisfy the request | • **debug** – max wall‑time 1 h (OK) but node range 1‑2 → *fails* because we want to try ≥ 4 nodes. <br>• **debug‑scaling** – node range 1‑10, max wall‑time 1 h → *passes* . <br>• **prod** – node range 10‑496 → *fails* (our test set starts at 4 nodes). <br>• **demand** – node range 1‑56, max wall‑time 1 h → *passes*. <br>• **preemptable** – node range 1‑10, max wall‑time 72 h → *passes*. <br>• **capacity** – node range 1‑4, max wall‑time 168 h → *passes* (but only up to 4 nodes). | Queues that survive: **debug‑scaling, demand, preemptable, capacity** |
| 3. Verify the surviving queues against each limit | <br>**Queue: debug‑scaling**  <br>‑ Node minimum: request 4 ≥ 1 → **PASS**  <br>‑ Node maximum: request 4 ≤ 10 → **PASS**  <br>‑ Wall‑time max: request 10 min ≤ 1 h → **PASS** <br><br>**Queue: demand**  <br>‑ Node min 1 → PASS  <br>‑ Node max 56 → PASS  <br>‑ Wall‑time ≤ 1 h → PASS  <br><br>**Queue: preemptable**  <br>‑ Node min 1 → PASS  <br>‑ Node max 10 → PASS  <br>‑ Wall‑time ≤ 72 h → PASS  <br><br>**Queue: capacity**  <br>‑ Node min 1 → PASS  <br>‑ Node max 4 → PASS  <br>‑ Wall‑time ≤ 168 h → PASS |

All three limit checks read **PASS** for each of the four candidate queues.  
To keep the job short and to stay within the “debug‑style” allocation that is intended for quick scaling studies, we select **debug‑scaling**.

---

**(b) Ranks‑per‑node and GPUs‑per‑node**

* The NWChem build that will be used is the **CPU‑only** build.  
* The supplied build default is **4 MPI ranks per node**.  
* Because the build does not include standard GPU support, we request **0 GPUs per node** (the GPU resources are unnecessary and would be wasted).

---

**(c) Timing assumption**

The only timing information given is the 5 s wall‑time observed for a single‑node run of the exact calculation.  
We assume that the same amount of work will be distributed over the selected nodes, so the *actual* run time will be ≤ 5 s (ideal speed‑up would give 5 s / 4 ≈ 1.25 s).  
The **10‑minute wall‑time request** therefore includes a very large safety margin (≈ 600× the expected run time) but does **not** claim that the job will actually run that long.

---

**(d) Scaling guidance**

The application documentation advises **4 MPI ranks per node** for good load balance on Polaris.  
No other scaling constraints (e.g., GA memory settings) conflict with this benchmark; the input file already sets the needed global/heap/stack sizes, so we follow the default.

---

**(e) Restatement of the resource specification**

| Item                     | Value |
|--------------------------|-------|
| Nodes requested          | **4** |
| MPI ranks per node       | **4** |
| Total MPI ranks          | **4 × 4 = 16** |
| GPUs per node            | **0** |
| Wall‑time                | **00:10:00** |
| Queue                    | **debug‑scaling** |

**Thus the job will be submitted to the `debug-scaling` queue with 4 nodes, each node running 4 MPI ranks (total 16 ranks), no GPUs, and a wall‑time limit of 10 minutes.**
````
