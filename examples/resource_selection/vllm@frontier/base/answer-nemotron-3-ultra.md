# nemotron-3-ultra — vllm@frontier, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**Resource Specification for Frontier Batch Job**

---

### (a) Queue Selection — Step-by-Step

#### 1. Size the work and derive required walltime

| Component | Basis | Time |
|-----------|-------|------|
| vLLM server startup | Prior measurement (Slurm job 4567519) | 165 s |
| Inference (50 prompts × 50 tokens = 2 500 tokens) | Llama-3.1-8B at TP=4 on MI250X GCDs; validated TP=8 throughput on 1 node implies ~400–600 tok/s aggregate at TP=4 → 2 500 tokens ≈ 4–6 s. Conservative estimate: 60 s | 60 s |
| **Subtotal** | | **225 s (≈ 3.8 min)** |
| Safety margin (5×) | Covers queue wait, filesystem latency, ROCm initialization variance | **~19 min** |
| **Requested walltime** | Rounded to scheduler granularity | **30 min (0.5 h)** |

*No measured throughput for TP=4 is supplied; the 5× margin is an assumption.*

#### 2. Eliminate queues that cannot accept the request

| Queue | Node range | Max walltime | Node-min check (req=1) | Node-max check (req=1) | Walltime check (req=0.5 h) | Verdict |
|-------|------------|--------------|------------------------|------------------------|----------------------------|---------|
| **batch** | 1–9 280 | 24 h | 1 ≤ 1 ✓ | 9 280 ≥ 1 ✓ | 24 ≥ 0.5 ✓ | **Survives** |
| **debug** | (not stated) | 2 h | ? | ? | 2 ≥ 0.5 ✓ | Survives (but node range unknown; debug queues are for interactive/short tests) |
| **extended** | 1–64 | 24 h | 1 ≤ 1 ✓ | 64 ≥ 1 ✓ | 24 ≥ 0.5 ✓ | **Survives** |
| **g1** | 1–2 | 2 h | 1 ≤ 1 ✓ | 2 ≥ 1 ✓ | 2 ≥ 0.5 ✓ | **Survives** |
| **service** | 1–1 | 24 h | 1 ≤ 1 ✓ | 1 ≥ 1 ✓ | 24 ≥ 0.5 ✓ | **Survives** |

#### 3. Choose the surviving queue that best matches the workload

The build defaults explicitly state: `nodes=1, partition=g1, ranks-per-node=8`.  
The prior validation (job 4567519) ran on 1–2 nodes in the `g1` queue.  
Our request (1 node, 0.5 h) fits `g1`’s 1–2 node / 2 h envelope exactly.

**Final limit verification for `g1`:**

| Limit | Requested | Queue limit | Pass/Fail |
|-------|-----------|-------------|-----------|
| Node minimum | 1 | 1 | **PASS** |
| Node maximum | 1 | 2 | **PASS** |
| Maximum walltime | 0.5 h | 2 h | **PASS** |

**Chosen queue: `g1`**

---

### (b) Ranks-per-node and GPUs-per-rank (from build defaults)

- **Ranks-per-node = 8** (one per GCD; each MI250X exposes 2 GCDs, 4 MI250X/node → 8 GCDs)  
- **GPUs-per-rank = 1** (each rank binds to one GCD)  
- **GPUs-per-node = 8** (fixed by hardware)

*Only node count is chosen by the agent; the above are properties of the built container/application.*

---

### (c) Timing assumptions stated plainly

- Server startup: **measured** at 165 s (job 4567519).  
- Inference throughput at TP=4: **not measured**; assumed 400–600 tok/s aggregate based on TP=8 validation on same hardware.  
- Margin: **5×** the subtotal (225 s → ~19 min), rounded to **30 min** walltime request.  
- No other overheads (data loading, checkpointing) are included because the workload is pure offline inference with 50 tiny prompts.

---

### (d) Scaling guidance

- The application was **validated at TP=8 on 1 node** (8 GCDs).  
- This run uses **TP=4**; with 8 ranks/node we can launch **2 concurrent TP=4 workers** (2 × 4 GCDs = 8 GCDs), fully utilizing the node.  
- Strong scaling beyond 1 node is unnecessary for 50 prompts; the problem fits in one node.  
- Therefore **node count = 1** is correct and matches the build default.

---

### (e) Final Resource Specification

| Parameter | Value |
|-----------|-------|
| **Nodes** | 1 |
| **Ranks per node** | 8 |
| **Total ranks** | 8 (= 1 × 8) |
| **GPUs per node** | 8 (8 GCDs) |
| **Walltime** | 30 minutes (0.5 h) |
| **Queue / Partition** | `g1` |

**Consistency check:** `total ranks = nodes × ranks-per-node → 8 = 1 × 8` ✓

---

**Slurm directive summary (for reference only — not a job script):**
```bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --gpus-per-node=8
#SBATCH --time=00:30:00
#SBATCH --partition=g1
#SBATCH --account=AstroLENS
```
````
