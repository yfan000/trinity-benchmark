# gpt-oss-120b — lammps@polaris, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**Step‑by‑step reasoning**

---

### 1️⃣  Size the work and derive a realistic wall‑time  

*System:* 500 000 Ar atoms, Lennard‑Jones, 100 000 steps.  
*Code:* LAMMPS on Polaris using the Kokkos GPU backend (`‑k <ngpus> -sf kk -pk kokkos`).  
*Build defaults:* 4 MPI ranks / node → each rank drives **1 GPU** (4 GPUs per node).

**Performance assumption** – a single A100 can sustain roughly **10 × 10⁶ atom‑steps · s⁻¹** for this simple LJ kernel (typical published numbers for LAMMPS‑Kokkos on A100).  

\[
\text{Time per step on one GPU}= \frac{N_{\text{atoms}}}{10^{7}}=
\frac{5\times10^{5}}{10^{7}}=0.05\;\text{s}
\]

With *R* GPUs the step time scales (strong‑scaling) as 1⁄R, assuming ≈80 % parallel efficiency across GPUs on the same node (the loss is small for a single node).  

| # nodes (N) | # GPUs = 4 × N | Step time (s) | Total time for 100 k steps (h) |
|-------------|----------------|--------------|--------------------------------|
| 1 | 4 | 0.05 / 4 ≈ 0.0125 | 0.347 h  ≈ 20.8 min |
| 2 | 8 | 0.05 / 8 ≈ 0.00625| 0.174 h ≈ 10.5 min |
| 4 |16| 0.05 / 16≈0.00312| 0.087 h ≈ 5.2 min |

Even the *worst‑case* (one node) finishes well under 1 h.  
To be safe we add a **20 % timing margin** for I/O, neighbour‑list rebuilds, and any load‑imbalance:

\[
\text{Wall‑time (with margin)} = 0.174\;\text{h} \times 1.20 \approx 0.21\;\text{h}
\approx 12.5\;\text{min}
\]

Thus a **2‑node** job comfortably fits inside a **1‑hour** limit with a generous safety buffer.  
We round the requested wall‑time up to a clean value of **00:50:00** (50 min) – still well below the 1 h cap and gives extra head‑room.

---

### 2️⃣  Eliminate queues that cannot satisfy the request  

| Queue            | Node range            | Max wall‑time | Reason for elimination (if any) |
|------------------|-----------------------|---------------|-----------------------------------|
| **debug**        | 1‑2 nodes             | 1 h           | **PASS** – node count OK, wall‑time OK |
| **debug‑scaling**| 1‑10 nodes            | 1 h           | **PASS** – node count OK, wall‑time OK |
| **prod**         | 10‑496 nodes          | 24 h          | **FAIL** – node count too low (needs ≥10) |
| **demand**       | 1‑56 nodes            | 1 h           | **PASS** – node count OK, wall‑time OK |
| **preemptable**  | 1‑10 nodes            | 72 h          | **PASS** – node count OK, wall‑time OK |
| **capacity**     | 1‑4 nodes             | 168 h         | **PASS** – node count OK, wall‑time OK |

All queues except **prod** survive the wall‑time test; **prod** fails because it requires at least 10 nodes, which would be wasteful for our modest problem size.

---

### 3️⃣  Choose a legal queue and show PASS for each limit  

We pick the **debug‑scaling** queue because it matches our small node request, has the shortest turnaround, and meets all limits.

| Limit                        | Requested value | Queue limit | PASS/FAIL |
|------------------------------|-----------------|------------|-----------|
| Minimum nodes                | 2               | ≥ 1        | PASS |
| Maximum nodes                | 2               | ≤ 10       | PASS |
| Maximum wall‑time (hh:mm:ss) | 00:50:00        | ≤ 01:00:00 | PASS |

All three checks PASS → the request is admissible.

---

### 4️⃣  Apply build‑default MPI‑rank / GPU mapping  

*Ranks per node* = **4** (provided by the build).  
*GPUs per node* = **4** (one GPU per rank).  

Thus each node runs 4 MPI ranks, each rank bound to its own A100.

---

### 5️⃣  Summary (no measured timings claimed)

- **Assumption:** 10 M atom‑steps · s⁻¹ per A100 for the LJ kernel; 20 % safety margin added.  
- **Scaling guidance:** The application notes advise “4 MPI ranks per node with 1 GPU each” – we follow it exactly. No other scaling advice applies because the problem size (<1 M atoms) is well within the strong‑scaling regime; using more than 2 nodes would only shrink the run time further but is unnecessary for a 1‑hour wall‑time budget.

---

## Final resource specification  

| Item                | Value |
|---------------------|-------|
| **Queue**           | debug‑scaling |
| **Node count**      | 2 |
| **GPUs per node**   | 4 |
| **MPI ranks per node** | 4 |
| **Total MPI ranks** | 8 (= 2 × 4) |
| **Wall‑time**       | 00:50:00 |

**Check:** Total ranks = nodes × ranks‑per‑node = 2 × 4 = **8** – satisfied.  

This specification respects all Polaris queue policies, uses the recommended Kokkos GPU configuration, and includes a conservative timing margin while staying well within the 1‑hour limit of the selected queue.
````
