# gpt-oss-120b — pytorch@sophia, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**1.  Size the work & derive a wall‑time**

| What we have | How we reason | Result |
|--------------|--------------|--------|
| **Dataset** – 100 000 images (≈ 1/13 of ImageNet) | 10 epochs → 1 000 000 image‑passes | 1 000 000 images |
| **Model / precision** – ResNet‑50, mixed‑precision (FP16) | On a single A100 the published FP16 throughput for ResNet‑50 is ≈ 10 000 images · s⁻¹ (batch = 256). | 100 000 images / 10 000 img · s⁻¹ ≈ 10 s per epoch on **one** GPU |
| **Multi‑GPU scaling** – 1 rank = 1 GPU, NCCL‑enabled → near‑linear scaling for this size | 8 GPUs per node → 8 × 10 000 = 80 000 img · s⁻¹ → 100 000 / 80 000 ≈ 1.25 s per epoch | 10 epochs ≈ 12.5 s on a *full* node |
| **Safety margin** – I add a 2 × factor to cover I/O, MPI start‑up and any non‑perfect scaling. | 12.5 s × 2 ≈ 25 s. I round up to the next convenient scheduler unit (minutes). | **Wall‑time request: 0 h 10 min (0:10:00)** – well above the estimated need, still far below any queue limit. |

*No measured timing exists, so the above is a reasoned estimate based on published A100 ResNet‑50 FP16 throughput, with a conservative 2 × safety margin.*

---

**2.  Eliminate queues that cannot satisfy the request**

| Queue | Node range (min‑max) | Max wall‑time | Verdict for our request (1 node, 0:10:00) |
|-------|----------------------|--------------|-------------------------------------------|
| **by‑gpu** | 1–1 nodes | 24 h | **PASS** – 1 node ≥ 1 min and ≤ 1 max; 0:10:00 ≤ 24 h |
| **by‑node** | 1–8 nodes | 24 h | **PASS** – 1 node within 1‑8; wall‑time OK |
| **bigmem** | 1–1 nodes | 24 h | **PASS** – same as by‑gpu |

All three queues meet the three limits (node‑minimum, node‑maximum, wall‑time).  
I choose the *by‑gpu* queue because it is the smallest‑granularity queue for a single‑node, GPU‑focused job and therefore the most appropriate for a pure multi‑GPU training run.

---

**3.  Ranks‑per‑node & GPUs‑per‑rank (application defaults)**  

* The PyTorch‑MPI build ships with the “one‑rank‑per‑GPU” default.  
* Therefore: **ranks‑per‑node = 8** (one rank for each of the 8 A100 GPUs).  
* **GPUs‑per‑rank = 1** (each rank owns exactly one GPU).  

The only freedom left to the user is the **node count**, already fixed to 1.

---

**4.  Final resource specification**

| Item | Value |
|------|-------|
| **Queue** | `by-gpu` |
| **Node count** | **1** |
| **GPUs per node** | 8 (the full A100 set on a Sophia node) |
| **Ranks per node** | 8 (1 rank = 1 GPU) |
| **Total ranks** | **1 node × 8 ranks = 8** |
| **Wall‑time** | **0:10:00** (10 minutes) |
| **Working directory** | `/eagle/MatGenome/nsvensson/pytorch_run` (not part of the spec, just noted) |

**Check:**  

*Node minimum* – queue requires ≥ 1 node → **PASS** (requested = 1).  
*Node maximum* – queue allows ≤ 1 node (by‑gpu) → **PASS** (requested = 1).  
*Maximum wall‑time* – queue limit = 24 h → **PASS** (requested = 0:10:00).

All three limits are satisfied, so the request would be accepted by the PBS‑Pro scheduler on Sophia.
````
