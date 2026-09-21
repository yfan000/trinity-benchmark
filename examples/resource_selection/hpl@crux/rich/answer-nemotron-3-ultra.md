# nemotron-3-ultra — hpl@crux, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**Resource Specification for HPL LINPACK on Crux**

---

### (a) Queue Selection — Step-by-Step

#### 1. Size the work and derive required walltime
- **Problem**: HPL LINPACK, N=50 000 → ~83 TFLOP (2/3·N³) of FP64 work.  
- **System**: Crux node = 128 CPU cores, ~5 TFLOP/s peak (conservative).  
- **Scaling guidance**: “Maximize performance by using all 128 cores per node.”  
  → Use **128 ranks/node** (build default).  
- **Node count choice**: For fastest turnaround on this small problem, strong-scale to **2 nodes** (256 ranks, 16×16 process grid).  
  - Single-node estimate: 83 TFLOP / (5 TFLOP/s × 0.75 eff.) ≈ 22 s.  
  - Two-node estimate: 83 TFLOP / (10 TFLOP/s × 0.60 eff.) ≈ 14 s.  
  - Communication/startup overhead adds variability.  
- **Assumed compute time**: 20–40 s.  
- **Margin**: 10× for scheduler delay, I/O, load imbalance → 3–7 min.  
- **Requested walltime**: **30 minutes (0.5 h)** — generous, well under any 1 h cap.

#### 2. Eliminate queues that cannot admit the request
| Queue | Max walltime | Node range | Walltime check (0.5 h ≤ max?) | Node check (2 ∈ range?) | Verdict |
|-------|--------------|------------|-------------------------------|--------------------------|---------|
| debug | 1 h | 1–8 | 0.5 ≤ 1 ✓ | 2 ∈ [1,8] ✓ | **Survives** |
| workq-route | 24 h | 1–184 | 0.5 ≤ 24 ✓ | 2 ∈ [1,184] ✓ | Survives |
| preemptable | 72 h | 1–10 | 0.5 ≤ 72 ✓ | 2 ∈ [1,10] ✓ | Survives |
| demand | 1 h | 1–64 | 0.5 ≤ 1 ✓ | 2 ∈ [1,64] ✓ | Survives |

All four queues technically admit the request. None is eliminated by hard limits.

#### 3. Choose the best surviving queue and verify all three limits
**Selection**: **debug** — designed for short, high-priority turnaround; 1 h cap matches our 0.5 h request; 2 nodes fits 1–8 range; no preemption risk.

| Limit | Requested | Queue Limit | Pass/Fail |
|-------|-----------|-------------|-----------|
| Node minimum | 2 | 1 | **PASS** (2 ≥ 1) |
| Node maximum | 2 | 8 | **PASS** (2 ≤ 8) |
| Maximum walltime | 0.5 h | 1 h | **PASS** (0.5 ≤ 1) |

All three checks read **PASS**.

---

### (b) Ranks and GPUs from application defaults
- **Ranks per node**: 128 (build default — “CPU-only benchmark. Maximize performance by using all 128 cores per node”).  
- **GPUs per node**: 0 (Crux has 0 GPUs/node; HPL is CPU-only).  
- **GPUs per rank**: 0.  
- **Total ranks** = nodes × ranks-per-node = 2 × 128 = **256**.  
  → HPL.dat will be retuned to a 16×16 process grid (P=16, Q=16) per scaling guidance.

---

### (c) Timing assumption and margin
- **No measured timing supplied**.  
- **Assumed**: 2-node strong-scale efficiency ~60% of aggregate peak (10 TFLOP/s) → ~14 s compute.  
- **Margin added**: 10× (→ ~2.5 min) to cover scheduler latency, MPI startup, I/O, and communication variability.  
- **Requested walltime**: 30 min (0.5 h) — 12× the margined estimate, safely under the 1 h queue cap.

---

### (d) Scaling guidance adherence
- **Guidance**: “Maximize performance by using all 128 cores per node. Tune N, NB, P, Q parameters in HPL.dat for Crux node memory (512 GB/node).”  
- **Action**:  
  - Ranks/node set to 128 (uses all cores).  
  - Process grid changed from 2×2 to 16×16 (P=16, Q=16) to match 256 total ranks.  
  - N=50 000, NB=232 kept as given; note that per-rank block size becomes small (~156 MB/rank), but memory (512 GB/node) is not a constraint.  
  - Guidance fully honored; the original 2×2 grid in HPL.dat is a tunable parameter, not a fixed problem constraint.

---

### (e) Final resource specification

| Parameter | Value |
|-----------|-------|
| **Nodes** | 2 |
| **Ranks per node** | 128 |
| **Total ranks** | 256 (= 2 × 128) |
| **GPUs per node** | 0 |
| **Walltime** | 30 minutes (0.5 h) |
| **Queue** | debug |

**Verification**: Total ranks = nodes × ranks per node = 2 × 128 = 256 ✓
````
