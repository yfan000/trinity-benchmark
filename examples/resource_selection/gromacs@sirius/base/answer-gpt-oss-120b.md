# gpt-oss-120b — gromacs@sirius, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 1 of 10 requirements violated).

````
**1.  Size the work and estimate a realistic wall‑time**

*System size* – ~34 000 atoms (lysozyme + TIP3P + 0.15 M NaCl).  
*Typical GROMACS performance on an A100* – for a system of this size GROMACS usually achieves **≈ 150–200 ns day⁻¹ per GPU** when the non‑bonded and PME kernels are off‑loaded to the GPU.

*Target work*: 5 ns of production (restart)  

\[
\text{Time per GPU} \approx \frac{5\;\text{ns}}{200\;\text{ns day}^{-1}} = 0.025\;\text{day} \approx 36\text{ min}
\]

Because we will run the job on a whole node (4 GPUs) the ideal wall‑time would be ~ 36 min.  
To be safe we add a **3× safety margin** to cover I/O, checkpoint writing, and any slightly poorer scaling:

\[
\boxed{\text{Requested wall‑time } = 2\;\text{h} = 02:00:00}
\]

No measured throughput is available, so the above estimate and the 3× margin are explicitly stated.

---

**2.  Choose a legal queue (workq) – eliminate queues that do not satisfy the limits**

| Queue | Node‑range | Max wall‑time | Reason for elimination (if any) |
|-------|------------|---------------|----------------------------------|
| **workq** | 1 – 4 nodes | 24 h | **Fits** all limits – keep |
| other queues (if any) | – | – | (none listed in the prompt) |

Result: *workq* is the only queue that satisfies the request.

---

**3.  Verify the request against the three limits of the chosen queue**

| Limit | Queue limit (workq) | Our request | PASS / FAIL |
|-------|----------------------|-------------|--------------|
| Minimum nodes | 1 | **1 node** | **PASS** |
| Maximum nodes | 4 | **1 ≤ 4** | **PASS** |
| Maximum wall‑time | 24:00:00 | **02:00:00 ≤ 24:00:00** | **PASS** |

All three checks pass, therefore the request is admissible.

---

**4.  Application defaults that must be honoured**

* Build default supplied for GROMACS on Sirius: **ranks‑per‑node = 8**.  
* GPU hardware on a Sirius node: **4 × A100‑SXM4‑40GB**.  

We therefore launch **8 MPI ranks on each allocated node** and map them to the 4 GPUs (two ranks per GPU) using the `-gpu_id 0123` option; this follows the “‑gpu_id” guidance and respects the build‑time defaults.

---

**5.  Resource specification**

| Item | Value |
|------|-------|
| **Queue** | `workq` |
| **Nodes** | **1** |
| **GPUs per node** | **4** (the hardware present) |
| **Ranks per node** | **8** (application default) |
| **Total ranks** | **1 × 8 = 8** |
| **Wall‑time** | **02:00:00** (2 h, includes safety margin) |
| **CPU cores per node** | 64 (available; GROMACS will use the remaining cores for OpenMP threads) |

**Summary (restated as required)**  

- **Nodes:** 1  
- **Ranks per node:** 8  
- **Total ranks:** 8 (1 × 8)  
- **GPUs per node:** 4  
- **Wall‑time:** 02:00:00  
- **Queue:** workq  

This specification satisfies all queue constraints, uses the application‑provided MPI rank layout, and includes a conservative wall‑time estimate for the 5 ns restart run on Sirius.
````
