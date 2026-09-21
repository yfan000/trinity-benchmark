# gpt-oss-120b — vllm@frontier, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**(a)  Choose a legal queue**

| Step | What we check | Queue | Limit that applies | Pass / Fail |
|------|---------------|-------|--------------------|-------------|
| 1.  | Required wall‑time | – | – | **≈ 10 min** (see reasoning below) |
| 2.  | Queue wall‑time caps | **batch** | 24 h | PASS |
|      |                | **debug** | 2 h | PASS |
|      |                | **extended** | 24 h | PASS |
|      |                | **g1** | 2 h | PASS |
|      |                | **service** | 24 h | PASS |
| 3.  | Node‑range limits (we will request 1 node) | **batch** | 1 – 9280 | PASS |
|      |                | **debug** | (implicit 1‑node min, no max shown) – acceptable | PASS |
|      |                | **extended** | 1 – 64 | PASS |
|      |                | **g1** | 1 – 2 | PASS |
|      |                | **service** | 1 – 1 | PASS |

All three criteria (minimum nodes, maximum nodes, maximum wall‑time) are satisfied for every queue.  
Because the job is very short (≈ 10 min) and uses only one node, the **debug** queue is the most appropriate – it is intended for quick test runs and guarantees fast start‑up.

**(b)  Ranks‑per‑node and GPUs‑per‑rank**

The application build defaults (see “sizing defaults”) prescribe  

* **ranks‑per‑node = 8** – one MPI rank for each GCD device on a Frontier node.  

Frontier nodes have **8 GCD devices** (4 × MI250X, each MI250X exposes 2 GCDs), so we will launch **8 ranks** on the node, each rank using **1 GPU** (1 GCD).  

Tensor‑parallel size = 4 means the 8 ranks are naturally split into two independent TP‑4 groups; each group will collectively hold the model across its 4 GPUs.

**(c)  Timing assumption**

* Server / model‑loading start‑up (measured on the same code base) ≈ 165 s ≈ 2 min 45 s.  
* Inference for 50 prompts × 50 tokens is tiny compared with the start‑up cost.  Even if the actual token generation took another ≈ 1 min, the total run time would be ≈ 4 min.  
* To be safe we add a 150 % safety margin (≈ 6 min) and round up to a *nice* wall‑time value of **10 minutes** (00:10:00).  

No other measured throughput is available, so the estimate is deliberately conservative.

**(d)  Scaling guidance**

The application has been **validated at TP = 8 on a single Frontier node** (see “VALIDATED 2026‑05‑11”).  
Our run uses TP = 4 (half the GPU count) on the same node, well within the validated regime.  
Thus the provided scaling guidance applies – the code is known to run correctly with up to 8 ranks per node, so using 8 ranks (TP = 4) is safe.

**(e)  Final resource specification**

| Item                | Value |
|---------------------|-------|
| **Node count**      | 1 |
| **Ranks per node**  | 8 |
| **Total ranks**     | 1 × 8 = **8** |
| **GPUs per node**   | 8 (8 GCD devices) |
| **GPUs per rank**   | 1 |
| **Tensor‑parallel size** | 4 (two independent TP‑4 groups) |
| **Wall‑time**       | 00:10:00 (10 minutes) |
| **Queue (partition)**| **debug** |

**Summary (ready for a Slurm submission)**  

- **Nodes:** 1  
- **Ranks per node:** 8  
- **Total ranks:** 8 (= 1 × 8)  
- **GPUs per node:** 8 (one per rank)  
- **Wall‑time:** 00:10:00  
- **Queue:** debug  

All limits (minimum nodes = 1, maximum nodes = 1, maximum wall‑time = 2 h) are satisfied, so the job will be accepted by the Frontier scheduler.
````
