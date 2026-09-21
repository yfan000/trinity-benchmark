# gpt-oss-120b — nwchem@polaris, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**1. Size the work and derive a realistic wall‑time**

* Single‑node timing (water‑molecule B3LYP/6‑31G*): **≈ 5 s**.  
* Even on 8 nodes the calculation will finish in a few seconds; however a scheduler needs a non‑zero wall‑time.  
* I add a safety margin of **5 minutes** (0 h 5 min 0 s) – well above the measured run, comfortably below any queue’s wall‑time cap, and large enough to absorb start‑up / I/O overhead.

**Requested wall‑time:** **00:05:00**  

---

**2. Eliminate queues that cannot satisfy the request**

| Queue            | Node range (min‑max) | Max wall‑time | Reason for elimination |
|------------------|----------------------|---------------|------------------------|
| **debug**        | 1‑2                  | 1 h           | **FAIL** – node count 8 > 2 |
| **debug‑scaling**| 1‑10                 | 1 h           | PASS |
| **prod**         | 10‑496               | 24 h          | **FAIL** – node count 8 < 10 |
| **demand**       | 1‑56                 | 1 h           | PASS |
| **preemptable**  | 1‑10                 | 72 h          | PASS |
| **capacity**     | 1‑4                  | 168 h         | **FAIL** – node count 8 > 4 |

The surviving queues are **debug‑scaling, demand, preemptable**.

---

**3. Verify the three limits for the chosen queue (debug‑scaling)**  

| Limit                | Requested value | Queue limit (debug‑scaling) | PASS/FAIL |
|----------------------|-----------------|-----------------------------|----------|
| Node‑minimum         | 8 nodes         | ≥ 1                         | **PASS** |
| Node‑maximum         | 8 nodes         | ≤ 10                        | **PASS** |
| Maximum wall‑time    | 00:05:00        | ≤ 1 h (60 min)               | **PASS** |

All three checks are PASS, so **debug‑scaling** is the legal queue to use.

---

**4. Application defaults → ranks‑per‑node and GPUs**

* Build default supplied: **4 MPI ranks per node**.  
* The NWChem build is **CPU‑only** (GPU support is experimental and not part of the community release).  
* Therefore **GPUs per node = 0**.

---

**5. Scaling guidance**

The application’s scaling note states “4 MPI ranks per node”.  
I honour this by requesting exactly 4 ranks on each node; no other scaling constraints apply to this tiny benchmark.

---

### Final resource specification

| Item                     | Value |
|--------------------------|-------|
| **Queue**                | debug‑scaling |
| **Node count**           | 8 |
| **MPI ranks per node**   | 4 |
| **Total MPI ranks**      | 8 × 4 = 32 |
| **GPUs per node**        | 0 (CPU‑only build) |
| **Requested wall‑time**  | 00:05:00 (5 min) |

**Restatement:**  
Run the job on **8 nodes** in the **debug‑scaling** queue, using **4 MPI ranks per node** (total **32 ranks**) and **no GPUs**, with a wall‑time of **5 minutes**. This request satisfies all node‑range and wall‑time limits of the chosen queue.
````
