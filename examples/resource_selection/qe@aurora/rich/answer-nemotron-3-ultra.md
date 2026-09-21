# nemotron-3-ultra — qe@aurora, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**Resource Specification for Production DFT Campaign on Aurora**

---

### (a) Queue Selection — Step-by-Step

#### 1. Size the work and derive required walltime

**Problem size analysis**  
- 64-atom 3C-SiC (2×2×2 zinc-blende supercell)  
- Ultrasoft pseudopotentials, 60 Ry wave-function cutoff (480 Ry charge density)  
- 4×4×4 Monkhorst-Pack grid → **64 k-points**  
- ~35 000 plane-waves / k-point, ~250 bands  

**Parallelisation strategy (QE, CPU-only MKL+ScaLAPACK build)**  
- Natural k-point parallelism: 64 k-point pools  
- With 104 ranks/node (all cores), 16 nodes = 1 664 ranks → **26 ranks per k-point pool**  
- 26 ranks/k-point gives ~10 bands/rank and good FFT parallelisation — well within strong-scaling range for this problem size  

**Walltime estimate**  
- Measured/observed timing: *none supplied*  
- Assumption: ~45–60 min for SCF convergence (10–15 iterations) on 16 nodes based on published QE scaling for similar 64-atom/64-k-point systems on Intel Xeon/Sapphire Rapids class CPUs  
- Margin added: **100 %** (to cover SCF variability, I/O, queue wait)  
- **Requested walltime = 2 hours (02:00:00)**

---

#### 2. Eliminate queues that cannot accommodate the request

| Queue            | Node range   | Max walltime | Eliminated because…                                                                 |
|------------------|--------------|--------------|-------------------------------------------------------------------------------------|
| **debug**        | 1–2          | 1 h          | **Node maximum (2) < requested (16)**                                               |
| **debug-scaling**| 2–256        | 1 h          | **Max walltime (1 h) < requested (2 h)**                                            |
| **prod**         | 256–10 624   | 24 h         | **Node minimum (256) > requested (16)**                                             |
| **visualization**| 1–32         | 8 h          | Technically passes all three limits, but **purpose mismatch** (dedicated to interactive visualization, not batch production compute) |
| **capacity**     | 1–16         | 168 h        | **Survives all limits**                                                             |

---

#### 3. Verdict for the surviving queue (**capacity**)

| Limit               | Requested | Limit   | Pass/Fail |
|---------------------|-----------|---------|-----------|
| Node minimum        | 16        | 1       | **PASS**  |
| Node maximum        | 16        | 16      | **PASS**  |
| Maximum walltime    | 2 h       | 168 h   | **PASS**  |

**Chosen queue: `capacity`**

---

### (b) Ranks and GPUs from build defaults

- **Ranks per node** = 104 (CPU-only MPI build, uses all 104 cores; Intel MKL FFT + ScaLAPACK)  
- **GPUs per node** = 6 (hardware present: 6× Intel Data Center GPU Max Series), but **0 used by application** — build is CPU-only; `pw_gpu` requires NVIDIA GPUs and is not enabled for Aurora’s Intel GPUs  
- **Total ranks** = nodes × ranks per node = 16 × 104 = **1 664**

---

### (c) Timing assumption statement

> No measured timing was supplied. I assumed ~45–60 min for the SCF on 16 nodes based on typical QE strong-scaling for a 64-atom/64-k-point ultrasoft-PP system on comparable Intel CPU hardware, and added a 100 % margin to obtain the 2 h request.

---

### (d) Scaling guidance adherence

The application build defaults to 104 ranks/node (full node). The 64 k-points provide ample k-point parallelism; 16 nodes (1 664 ranks) yields 26 ranks/k-point, which respects the CPU-only MKL+ScaLAPACK scaling model — no GPU offload is available or used. The node count is chosen to saturate k-point parallelism without over-subscribing bands/plane-waves.

---

### Final Resource Specification

| Parameter          | Value |
|--------------------|-------|
| **Nodes**          | 16 |
| **Ranks per node** | 104 |
| **Total ranks**    | 1 664 (= 16 × 104) |
| **GPUs per node**  | 6 (hardware) / 0 (used) |
| **Walltime**       | 02:00:00 |
| **Queue**          | capacity |

All queue limits satisfied; total ranks = nodes × ranks per node verified.
````
