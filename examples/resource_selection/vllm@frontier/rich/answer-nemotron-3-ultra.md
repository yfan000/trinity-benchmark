# nemotron-3-ultra — vllm@frontier, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**Resource Specification and Reasoning for Llama-3.1-8B Offline Inference on Frontier**

---

### (a) Queue Selection and Limit Verification

#### 1. Work Sizing and Walltime Derivation
- **Measured startup**: ~165 s (from prior Slurm job 4567519 on 1 node, TP=8).  
- **Inference workload**: 50 prompts × 50 max_new_tokens = 2,500 generated tokens total.  
- **Throughput assumption**: No TP=4 measurement provided. The validated TP=8 run on 1 node (8 GCDs) serves as the only reference. With TP=4 we use 4 GCDs per model replica; on a full node (8 GCDs) we can run **2 concurrent replicas** (ranks-per-node=8 ÷ TP=4 = 2). Aggregate throughput should be comparable to the TP=8 run. Conservatively estimate **< 30 s** for the full batch.  
- **Total expected runtime**: 165 s (startup) + 30 s (inference) ≈ 195 s.  
- **Margin**: 3× safety factor → 585 s.  
- **Requested walltime**: **10 minutes (00:10:00)** — well under the 2-hour cap of the candidate queues.

#### 2. Queue Elimination Table
| Queue      | Node Range | Max Walltime | Node Count Requested (1) | Walltime Requested (0.167 h) | Disqualifying Limit (if any) |
|------------|------------|--------------|--------------------------|------------------------------|------------------------------|
| **batch**  | 1–9280     | 24 h         | PASS                     | PASS                         | —                            |
| **debug**  | (unspec.)  | 2 h          | PASS*                    | PASS                         | —                            |
| **extended**| 1–64      | 24 h         | PASS                     | PASS                         | —                            |
| **g1**     | 1–2        | 2 h          | PASS                     | PASS                         | —                            |
| **service**| 1–1        | 24 h         | PASS                     | PASS                         | —                            |

\* *debug queue node range not explicitly given; assumed to include 1 node.*

All five queues technically accept the request. The **build defaults explicitly state `partition=g1`** for this application profile (1 node, ranks-per-node=8), so **g1** is the natural choice.

#### 3. Final Limit Check for Chosen Queue (g1)
| Limit               | Requested | Queue Limit | Verdict |
|---------------------|-----------|-------------|---------|
| Node minimum        | 1         | 1           | **PASS** |
| Node maximum        | 1         | 2           | **PASS** |
| Maximum walltime    | 0.167 h   | 2 h         | **PASS** |

All three limits pass.

---

### (b) Ranks-per-Node and GPUs-per-Rank (Fixed by Build Defaults)
- **Ranks-per-node**: 8 (one per GCD, as validated in job 4567519).  
- **GPUs-per-rank**: 1 (each rank binds to one MI250X GCD).  
- **Tensor-parallel size**: 4 → each model replica consumes 4 ranks (4 GCDs).  
- With 8 ranks/node, **2 concurrent replicas** fit on a single node.

---

### (c) Timing Assumptions and Margin
- **Measured**: Server startup = 165 s (TP=8, 1 node).  
- **Assumed**: Inference throughput at TP=4 with 2 replicas ≈ TP=8 throughput (same total GCDs).  
- **Estimated inference time**: < 30 s for 2,500 tokens.  
- **Margin applied**: 3× on total measured+estimated time (195 s → 585 s).  
- **Requested walltime**: 600 s (00:10:00) — **not** rounded up to the queue cap.

---

### (d) Scaling Guidance
The application defaults (ranks-per-node=8, partition=g1, nodes=1) are designed for single-node tensor-parallel inference. The workload (50 prompts) is tiny; **multi-node scaling is unnecessary and would add communication overhead without benefit**. The TP=4 setting uses half the GCDs per replica, so running two replicas on the 8-GCD node fully utilizes the hardware, matching the validated TP=8 configuration’s aggregate compute capacity.

---

### (e) Final Restatement

| Parameter          | Value |
|--------------------|-------|
| **Nodes**          | 1 |
| **Ranks per node** | 8 |
| **Total ranks**    | 8 (= 1 × 8) |
| **GPUs per node**  | 8 (GCDs) |
| **Walltime**       | 00:10:00 (10 minutes) |
| **Queue (partition)** | g1 |

**Verification**: Total ranks (8) = Nodes (1) × Ranks per node (8) ✓  
All queue limits satisfied ✓
````
