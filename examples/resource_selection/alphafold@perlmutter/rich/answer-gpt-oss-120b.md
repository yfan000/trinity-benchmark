# gpt-oss-120b — alphafold@perlmutter, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**1.  Estimate the wall‑time needed for a *single* AlphaFold prediction**

* Human ubiquitin (76 aa) – small protein  
* AlphaFold on a single A100 usually finishes the MSA + 5‑model + relaxation pipeline in **≈ 2 h**.  
* Because the MSA step is CPU‑intensive we add a safety margin of 30 % → **≈ 2 h 40 min**.  

We therefore request **2 h 45 min (02:45:00)** – well below any queue limit that allows a “few‑hour” job.

---

**2.  Eliminate queues that cannot satisfy the request**

| Queue                | Max wall‑time | Node range | Reason it is **removed** |
|----------------------|---------------|------------|--------------------------|
| **debug**            | 30 min        | 1‑8        | max wall‑time < 02:45:00 |
| (all other queues)   | ≥ 4 h         | include 1  | **remain**               |

All remaining queues (express_amsc, regular, premium, shared, preempt, interactive, jupyter, overrun) allow a wall‑time ≥ 02:45 and accept a single node.

---

**3.  Check the three limits for the surviving queues**  

We will use the **express_amsc** queue because it has the shortest turnaround time while still satisfying every limit.

| Limit                | Requested value | Queue limit (express_amsc) | PASS/FAIL |
|----------------------|-----------------|----------------------------|----------|
| Minimum nodes        | 1               | no minimum (any ≥1)        | PASS |
| Maximum nodes        | 1               | no explicit maximum (system‑wide 3072) | PASS |
| Maximum wall‑time    | 02:45:00        | 06:00:00                   | PASS |

All three checks pass, so the request is legal.

---

**4.  Ranks‑per‑node and GPUs‑per‑rank (from the build defaults)**  

* **Ranks per node** – one MPI rank per GPU.  
* **GPUs per rank** – 1 GPU per rank.  

Because we only need a single GPU for a single AlphaFold run, we request **1 rank on the node** and **1 GPU on that node** (the other three A100s on the node remain idle – this is the minimal, safest allocation for a single‑run sweep).

---

**5.  Final resource specification**

| Item                | Value |
|---------------------|-------|
| **Queue**           | `express_amsc` |
| **Wall‑time**       | `02:45:00` |
| **Node count**      | `1` |
| **Ranks per node**  | `1` |
| **Total ranks**     | `1 × 1 = 1` |
| **GPUs per node**   | `1` (1 GPU assigned to the single rank) |

**Restatement**

- **Nodes:** 1  
- **Ranks per node:** 1 (total ranks = 1 × 1 = 1)  
- **GPUs per node:** 1 (1 GPU = 1 GPU per rank)  
- **Wall‑time:** 02:45:00 (≈ 2 h 45 min, based on a 2 h run plus 30 % margin)  
- **Queue:** express_amsc  

This specification conforms to the Perlmutter queue policies, respects the AlphaFold scaling guidance (single‑GPU per prediction), and provides a realistic, safely padded runtime for the ubiquitin prediction job.
````
