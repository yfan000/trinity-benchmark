# gpt-oss-120b — qmcpack@aurora, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**Step (a) – Choose a legal queue**

| Requirement | Requested value | Queue limit | Pass/Fail | Reason |
|-------------|----------------|------------|-----------|--------|
| **Node count** (minimum) | **4 nodes** | capacity queue: 1 ≤ nodes ≤ 16 | **PASS** | 4 ≥ 1 |
| **Node count** (maximum) | **4 nodes** | capacity queue: 1 ≤ nodes ≤ 16 | **PASS** | 4 ≤ 16 |
| **Wall‑time** | **4 h 00 m** | capacity queue: max = 168 h | **PASS** | 4 h ≤ 168 h |

All three checks pass, therefore the **capacity** queue is the only queue that can satisfy the request.  
(Other queues are eliminated:  

* `debug` – max 1 h (wall‑time too short).  
* `debug‑scaling` – max 1 h (wall‑time too short).  
* `prod` – node minimum 256 (our 4 nodes far below).  
* `visualization` – max 8 h (wall‑time would pass) but the queue is intended for short‑lived visualisation jobs; the standard production‑type run is placed in the `capacity` queue.)

---

**Step (b) – Ranks‑per‑node and GPUs‑per‑node**

* Build‑time default for QMCPACK on Aurora: **6 ranks / node** (one MPI rank per GPU).  
* Each node houses **6 Intel Data Center GPU Max Series** tiles, so **6 GPUs / node**.  
* The user only chooses the **node count**; ranks‑per‑node and GPUs‑per‑node follow the defaults.

---

**Step (c) – Wall‑time estimate**

No measured timing is supplied, so a simple scaling model is used:

1. **Reference assumption** – a single Aurora node (6 GPUs, 6 MPI ranks) can complete the 64‑atom DMC job (4096 walkers, 200 blocks, 0.005 Ha⁻¹) in roughly **12 h**.  
   *This is a conservative “single‑node worst‑case” estimate taken from typical DMC workloads of comparable size on GPU‑accelerated systems.*

2. **Strong‑scaling** – QMCPACK’s SYCL build scales close to linear with the number of GPUs for this problem size (the walkers can be evenly divided among ranks).  

3. **Four‑node run** – with 4 nodes ⇒ 24 GPUs, the ideal time would be 12 h / 4 ≈ 3 h.  

4. **Safety margin** – add 20 % to guard against non‑ideal scaling, I/O overhead and queue‑startup cost:  
   3 h × 1.20 = 3.6 h ≈ **3 h 30 m**.  

5. **Rounded request** – round up to a clean hour value that still respects the queue limit → **4 h**.

Thus the requested wall‑time is **4 hours** (the scheduler will enforce the exact value we specify).

---

**Step (d) – Scaling guidance**

The supplied QMCPACK build notes state: *“6 Intel GPU tiles per node; QMCPACK SYCL build targets spir64 for Intel GPUs.”*  
No further scaling constraints are given, so the simple linear‑scaling assumption above is appropriate for a 4‑node run. No additional restriction applies.

---

**Step (e) – Restatement of the full resource specification**

| Item | Value |
|------|-------|
| **Nodes** | **4** |
| **Ranks per node** | **6** (default) |
| **Total MPI ranks** | **4 × 6 = 24** |
| **GPUs per node** | **6** (one per rank) |
| **Total GPUs** | **4 × 6 = 24** |
| **Wall‑time** | **4 h 00 m** |
| **Queue** | **capacity** |

**Check:** total ranks = nodes × ranks per node → 4 × 6 = 24 (as listed).

These numbers satisfy all queue limits, follow the application’s default mapping of ranks to GPUs, and incorporate a conservative timing estimate with an appropriate safety margin. The job can now be submitted to the **capacity** queue on Aurora with the above resource request.
````
