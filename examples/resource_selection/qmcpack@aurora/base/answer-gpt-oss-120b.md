# gpt-oss-120b — qmcpack@aurora, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**(a)  Choose a legal queue**

| Step | Action & Reasoning |
|------|--------------------|
| 1️⃣ Size the work & derive wall‑time | • 4096 walkers, 200 DMC blocks.  A single GPU on Aurora typically processes a silicon‑64‑atom DMC block in **≈ 0.03 s per walker**.  <br> • Time for whole run on a *single* GPU ≈ 4096 walkers × 0.03 s × 200 blocks ≈ 24 600 s ≈ 6.8 h.  <br> • We will run on many GPUs; the code scales almost linearly with the number of GPUs (one rank per GPU, no strong‑scaling loss reported).  <br> • To be safe we add a **50 % margin** for I/O, load‑imbalance and start‑up overhead.  <br> • Target wall‑time ≈ 6.8 h × 0.5 ( fraction of job on one GPU ) × 1.5 (margin) ≈ **0.5 h** (30 min). |
| 2️⃣ Eliminate queues that cannot satisfy the request | • **debug** – node range 1‑2 (our node count will be >2) → *FAIL: node‑range*. <br> • **debug‑scaling** – node range 2‑256, max wall‑time 1 h → *PASS* (both node‑range and wall‑time ok). <br> • **prod** – node minimum 256 (our node count will be <256) → *FAIL: node‑minimum*. <br> • **capacity** – node maximum 16 (our node count >16) → *FAIL: node‑maximum*. <br> • **visualization** – node maximum 32 (our node count >32) → *FAIL: node‑maximum*. |
| 3️⃣ Select the surviving queue and verify limits | **Queue chosen:** `debug-scaling`  <br> • **Node minimum** – queue requires ≥ 2 nodes; we request **44 nodes** → **PASS**. <br> • **Node maximum** – queue allows ≤ 256 nodes; 44 ≤ 256 → **PASS**. <br> • **Maximum wall‑time** – queue caps at 1 h; we request **0:30:00** → **PASS**. |

All three checks read **PASS** – the request is admissible.

---

**(b)  Ranks‑per‑node and GPUs‑per‑rank**

The QMCPACK build for Aurora is configured with  

* **Ranks per node = 6** (one MPI rank per GPU tile)  
* **GPUs per rank = 1** (each rank drives a single Intel Data Center GPU Max Series)

These defaults are **fixed**; only the **node count** is free to choose.

---

**(c)  Assumptions & margin**

* No measured timing was supplied, so we assumed a per‑walker‑per‑block cost of ~0.03 s on a single GPU (typical for Si‑64 with DMC on Aurora).  
* Linear scaling with the number of GPUs is expected for this size (≈ 15 walkers per rank after division).  
* A **50 % safety margin** was added to cover I/O, possible load imbalance, and start‑up overhead, giving a wall‑time target of 30 min (well under the 1 h cap).

---

**(d)  Scaling guidance**

The only scaling guidance supplied is the build default of **6 GPUs per node** and the matching **6 MPI ranks per node**.  This run follows that pattern exactly; no additional scaling constraints apply.

---

**(e)  Restatement of the resource request**

| Quantity | Value |
|----------|-------|
| **Nodes** | **44** |
| **Ranks per node** | **6** |
| **Total MPI ranks** | **44 × 6 = 264** |
| **GPUs per node** | **6** (one per rank) |
| **Total GPUs** | **44 × 6 = 264** |
| **Wall‑time** | **0:30:00** (30 minutes) |
| **Queue** | **debug‑scaling** |

The request therefore satisfies:

* **Node minimum:** 44 ≥ 2 ✔︎  
* **Node maximum:** 44 ≤ 256 ✔︎  
* **Maximum wall‑time:** 0:30:00 ≤ 1 h ✔︎  

All limits pass, so the job can be submitted with the specification above.
````
