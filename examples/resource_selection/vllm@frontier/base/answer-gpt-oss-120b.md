# gpt-oss-120b — vllm@frontier, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**Step‑by‑step reasoning**

| Step | What we do | Result |
|------|------------|--------|
| 1️⃣  | **Estimate the run time**  <br>• Server start‑up (observed) = 165 s  <br>• Offline inference of 50 prompts × 50 tokens is tiny. Even with a conservative per‑token cost of 0.1 s the whole generation would be ≤ 5 s. <br>• Add a generous safety margin (≈ 20 %). <br>→ **Estimated wall‑clock time** ≈ 165 s + 5 s ≈ 170 s → *≈ 3 min*.  <br>Round down to a safe value that **does not exceed** any queue limit: **00:05:00** (5 min). |
| 2️⃣  | **Pick a node count**  <br>Frontier node = 8 MI250X cards = 8 GCD devices. The application defaults are **ranks‑per‑node = 8** (one rank per GCD, i.e. 1 GPU per rank).  <br>Tensor‑parallel size = 4 only requires ≥ 4 GPUs, which a single node already provides (8 GPUs).  <br>→ **Node count = 1** (the smallest legal value). |
| 3️⃣  | **Check every queue** against the two numbers we now have (walltime = 00:05:00, nodes = 1).  <br>For each queue we list the rule that would reject the request, then note whether it applies. |
|      | **batch** – nodes 1‑9280, wall‑time ≤ 24 h | Node min = 1 ✓, Node max = 9280 ✓, Wall‑time max = 24 h ✓ |
|      | **debug** – (no explicit node range given, but typically ≥ 1), wall‑time ≤ 2 h | Node min ≥ 1 ✓, Node max – (unlimited) ✓, Wall‑time max = 2 h ✓ |
|      | **extended** – nodes 1‑64, wall‑time ≤ 24 h | Node min = 1 ✓, Node max = 64 ✓, Wall‑time max = 24 h ✓ |
|      | **g1** – nodes 1‑2, wall‑time ≤ 2 h | Node min = 1 ✓, Node max = 2 ✓, Wall‑time max = 2 h ✓ |
|      | **service** – node = 1 only, wall‑time ≤ 24 h | Node min = 1 ✓, Node max = 1 ✓, Wall‑time max = 24 h ✓ |
| 4️⃣  | **Choose a queue**  <br>All queues satisfy the three limits.  For a short, single‑node test job the conventional choice on Frontier is the **debug** partition (short‑run, low‑latency allocation).  It meets every limit and is intended for exactly this class of workload. |
| 5️⃣  | **Copy the application defaults**  <br>‑ *ranks‑per‑node* = **8** (one rank per GCD). <br>‑ *GPUs‑per‑rank* = **1** (implicit from the “one per GCD” default).  <br>Only the node count is free to decide – we have set it to 1. |

---

### Final resource specification

| Quantity | Value |
|----------|-------|
| **Node count** | **1** |
| **Ranks per node** | **8** |
| **Total ranks** | **1 × 8 = 8** |
| **GPUs per node** | **8** (the 8 GCD devices on a Frontier node) |
| **Wall‑time** | **00:05:00** (5 minutes) |
| **Queue / Partition** | **debug** |

All three checks **PASS**:

| Limit | Requested | Limit | Pass/Fail |
|-------|-----------|-------|-----------|
| Node minimum | 1 | ≥ 1 (debug) | PASS |
| Node maximum | 1 | ≤ unlimited (debug) | PASS |
| Max wall‑time | 00:05:00 | ≤ 02:00:00 (debug) | PASS |

**Restatement**

- **Nodes:** 1  
- **Ranks per node:** 8 (default)  
- **Total ranks:** 8 (= 1 × 8)  
- **GPUs per node:** 8 (the 8 GCD devices)  
- **Wall‑time:** 00:05:00  
- **Queue:** debug  

This specification respects the Frontier queue policies, uses the application‑provided defaults for ranks‑per‑node and GPUs‑per‑rank, and includes a reasonable safety margin on the runtime. No PBS directives are used – all terms correspond to Slurm (e.g., *partition=debug*).
````
