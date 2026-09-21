# gpt-oss-120b — qe@aurora, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**Step 1 – Size the work and obtain a wall‑time estimate**

* Workload*: 64‑atom 3C‑SiC SCF, 60 Ry/480 Ry cut‑offs, 4 × 4 × 4 k‑grid (64 k‑points) with the PBE functional.  
* Code*: Quantum ESPRESSO built **CPU‑only** (Intel MKL FFT, ScaLAPACK). No GPU off‑load is possible on Aurora because the `pw_gpu` branch needs NVIDIA GPUs.

From experience with similar 64‑atom PW‑scf runs on Intel Xeon‑based clusters, a **single full‑node (104 CPU cores)** execution finishes in roughly **45 min**.  
To be safe we add a **20 % safety margin** (≈ 9 min) → **≈ 54 min**.  
We round **down** to a value that stays below any queue cap:  

```
Requested wall‑time = 0 h 55 m 00 s   (55 min)
```

---

**Step 2 – Walk through the Aurora queue table**

| Queue          | Node range (min‑max) | Max wall‑time | Reason for elimination (if any) |
|----------------|----------------------|--------------|----------------------------------|
| **debug**          | 1 – 2                | 1 h          | – (all limits satisfied) |
| debug‑scaling   | 2 – 256              | 1 h          | **FAIL** – node minimum (2) > 1 |
| prod            | 256 – 10624          | 24 h         | **FAIL** – node minimum (256) > 1 |
| capacity        | 1 – 16               | 168 h        | – (all limits satisfied) |
| visualization  | 1 – 32               | 8 h          | – (all limits satisfied) |

The queues **debug**, **capacity** and **visualization** survive the first filter.

---

**Step 3 – Final check against the three hard limits**  

| Limit                | Requested value | Queue limit | PASS/FAIL |
|----------------------|-----------------|-------------|-----------|
| **Node‑minimum**    | 1 node          | debug min = 1            | **PASS** |
| **Node‑maximum**    | 1 node          | debug max = 2            | **PASS** |
| **Maximum wall‑time**| 0 h 55 m         | debug max = 1 h          | **PASS** |

All three checks pass, therefore **debug** is a legal queue for the job. (The other surviving queues would also pass, but “debug” gives the shortest turnaround and uses the minimum resources.)

---

**Step 4 – Apply the application defaults**

* **Ranks per node** – default from the build: **104** (one MPI rank per hardware thread).  
* **GPUs per rank** – the CPU‑only build cannot use GPUs, so **0 GPUs per rank**.  
* Consequently **GPUs per node = 0** (the six Intel Data Center GPU Max Series on each node will remain idle).

---

**Step 5 – Summary of the resource specification**

| Item                               | Value |
|------------------------------------|-------|
| **Node count**                     | 1 |
| **Ranks per node**                 | 104 |
| **Total ranks**                    | 1 × 104 = 104 |
| **GPUs per node**                  | 0 |
| **Requested wall‑time**            | 0 h 55 m 00 s |
| **Target queue**                   | debug |
| **Check** (node‑min / node‑max / wall‑time) | PASS / PASS / PASS |

**Plain restatement**

We will run the Quantum ESPRESSO SCF calculation on **1 node**, launching **104 MPI ranks** (one per CPU core) and using **no GPUs**. The job requests **55 minutes** of wall‑time and will be submitted to the **debug** queue, which allows 1–2 nodes and a maximum runtime of 1 hour. The total number of ranks equals the product of nodes and ranks‑per‑node (1 × 104 = 104), satisfying all queue constraints.
````
