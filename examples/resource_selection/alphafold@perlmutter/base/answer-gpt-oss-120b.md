# gpt-oss-120b — alphafold@perlmutter, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**Step‑by‑step reasoning**

| Step | What we did | Result |
|------|-------------|--------|
| 1️⃣  | Estimate the run time needed for a **single AlphaFold prediction** (full DB search, 5 models + relaxation) on an A100.  For a 76‑residue protein this is typically **≈ 2 h** on one GPU.  To be safe we add a 20 % safety margin → **2 h 30 min**. | **Wall‑time needed = 2 h 30 min** |
| 2️⃣  | Compare this wall‑time against the maximum wall‑time of each queue and eliminate those that cannot satisfy it. | <ul><li>**debug** – max 30 min → **eliminated** (wall‑time too short)</li><li>All other queues have max ≥ 4 h → **remain**</li></ul> |
| 2️⃣  | Check the node‑range limits for the remaining queues (the only explicit ranges are for *debug* and *preempt*). Our request is **1 node**.<br>• *preempt* allows 1‑128 nodes → OK. <br>• All other queues have no node‑range restriction → OK. | **All remaining queues accept 1 node** |
| 3️⃣  | Choose a queue that passes every limit. The **express_amsc** queue offers a generous 6 h wall‑time limit and no node‑range restriction, making it the natural choice for a short, single‑GPU job. | **Queue = express_amsc** |
| 4️⃣  | Verify the three concrete limits for the chosen queue: | |
| ‑ Node minimum | No minimum listed → **PASS** | |
| ‑ Node maximum | No maximum listed → **PASS** | |
| ‑ Maximum wall‑time | Queue limit = 6 h  > 2 h 30 min → **PASS** | |

All three checks read **PASS**, so the request is legal.

**Build‑defaults for AlphaFold**

* **Ranks per node** – one rank per GPU (AlphaFold is built for a single GPU per prediction).  
* **GPUs per rank** – 1 GPU.  

Thus on each node we will run **1 rank** using **1 GPU**.

---

### Final resource specification

| Item | Value |
|------|-------|
| **Number of nodes** | **1** |
| **Ranks per node** | **1** |
| **Total ranks** | **1 × 1 = 1** |
| **GPUs per node** | **1** (1 GPU per rank) |
| **Wall‑time** | **02:30:00** (2 h 30 min; derived from a ~2 h run + 20 % safety margin) |
| **Queue** | **express_amsc** |

**Statement of the request**

> **Request:** 1 node, 1 rank per node (total 1 rank), 1 GPU per node, wall‑time 02:30:00, queue *express_amsc*.  This satisfies all queue limits (node ≥ 0, node ≤ ∞, wall‑time ≤ 6 h).  The job will use a single A100 GPU, which is the scaling guideline for AlphaFold predictions of this size.
````
