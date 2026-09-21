# gpt-oss-120b — pytorch@sophia, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**Step (a) – Choose a legal queue**

| Queue (from the table) | Node‑range limit | Max wall‑time limit | Does the request fit? |
|------------------------|------------------|---------------------|-----------------------|
| **by‑gpu**             | 1 – 1 nodes      | 24 h                | **PASS** – we ask for 1 node, ≤ 24 h |
| **by‑node**            | 1 – 8 nodes      | 24 h                | **PASS** – we ask for 1 node, ≤ 24 h |
| **bigmem**             | 1 – 1 nodes      | 24 h                | **PASS** – we ask for 1 node, ≤ 24 h |

All three queues could technically accept the request, but we must pick **one**.  
Because we want to use the whole node (8 GPUs) and the code is built for one MPI rank per GPU, the *by‑node* queue is the most appropriate (it is intended for whole‑node allocations and allows up to 8 nodes, giving us flexibility for future scaling).

**Step 1 – Size the work & derive a realistic wall‑time**

* Workload: 100 000 images, batch‑size = 256 per GPU, 10 epochs.  
* Reference throughput (mixed‑precision ResNet‑50 on an A100, FP16) ≈ **18 000 images · s⁻¹ per GPU** (≈ 10 % slower than peak due to NCCL communication).  

For **one GPU**  

\[
\text{steps per epoch}= \frac{100\,000}{256}\approx 391
\]
\[
\text{time per step}= \frac{256}{18\,000}\;s \approx 0.0142\;s
\]
\[
\text{epoch time (1 GPU)}\approx 391\times0.0142\;s \approx 5.6\;s
\]

With **8 GPUs** (one node, 1 rank = 1 GPU) we assume near‑linear scaling (≈ 8 × speed‑up) → epoch ≈ 0.7 s.  
10 epochs ⇒ ≈ 7 s of pure compute.

Add a safety margin for:
* start‑up / data‑loading overhead,
* possible NCCL latency on the first iteration,
* scheduler and I/O jitter.

**Chosen wall‑time = 5 minutes (00:05:00)** – far below the 24 h queue limit, yet generous enough to cover all start‑up costs.

**Step 2 – Eliminate queues that cannot satisfy the limits**

* **by‑gpu** – node range 1‑1 (OK), max‑time 24 h (OK) → *remains*  
* **by‑node** – node range 1‑8 (OK), max‑time 24 h (OK) → *remains*  
* **bigmem** – node range 1‑1 (OK), max‑time 24 h (OK) → *remains*  

All survive; we finally select **by‑node** because it is the canonical whole‑node queue.

**Step 3 – Verify each of the three limits for the chosen queue (by‑node)**  

| Limit | Requested value | Queue limit | Result |
|-------|----------------|------------|--------|
| Minimum nodes | **1** | ≥ 1 (by‑node allows 1) | **PASS** |
| Maximum nodes | **1** | ≤ 8 (by‑node allows up to 8) | **PASS** |
| Maximum wall‑time | **00:05:00** | ≤ 24 h | **PASS** |

All three checks pass, so the request is legal.



**Step (b) – Ranks‑per‑node and GPUs‑per‑rank**

The application defaults (MPI‑NCCL build) use **one MPI rank per GPU**.

* **GPUs per node:** 8 (the hardware configuration of a Sophia node)  
* **Ranks per node:** 8 (one rank for each GPU)  
* **GPUs per rank:** 1



**Step (c) – Timing assumption**

No empirical timing was supplied, therefore we **assumed** a per‑GPU mixed‑precision throughput of 18 k images · s⁻¹ (≈ 10 % below the published peak for an A100 on ResNet‑50).  
From this we derived a raw compute time of ≈ 7 s for the whole job and then added a generous 5‑minute wall‑time margin.



**Step (d) – Scaling guidance**

The only scaling guidance available is the “one‑rank‑per‑GPU” rule, which we honoured.  No further scaling model was provided, so the linear‑speed‑up assumption used for the wall‑time estimate is the simplest, conservative approach.



**Step (e) – Restatement of the final resource specification**

| Item | Value |
|------|-------|
| **Queue** | `by-node` |
| **Nodes** | **1** |
| **GPUs per node** | **8** |
| **Ranks per node** | **8** |
| **Total ranks** | **1 × 8 = 8** |
| **Wall‑time** | **00:05:00** (5 minutes) |

**Result:**  

A legal request for a single Sophia node, using all 8 A100 GPUs, with 8 MPI ranks (one per GPU), a total of 8 ranks, and a wall‑time of five minutes submitted to the **by‑node** queue.
````
