# nemotron-3-ultra — nwchem@polaris, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**Resource Specification**

| Parameter | Value |
|-----------|-------|
| Nodes | 4 |
| GPUs per node | 0 |
| MPI ranks per node | 4 |
| Total MPI ranks | 16 |
| Walltime | 0:10:00 (10 minutes) |
| Queue | debug-scaling |

**Reasoning**

---

### (a) Queue selection — step-by-step

#### 1. Size the work and derive required walltime
- **Measured baseline**: 1 node, 4 ranks, 5 s wall time (given).
- **Scaling behaviour**: This is a *strong-scaling* benchmark of a tiny problem (single H₂O, B3LYP/6-31G*). Communication overhead will dominate beyond a few nodes; elapsed time per run will not drop below ~5 s and may rise slightly. A conservative per-run upper bound is **30 s**.
- **Margin**: To accommodate scheduler overhead, possible re-queues, and multiple iterations per node count, apply a **20× margin** → 30 s × 20 = 600 s = **10 minutes**.
- **Requested walltime**: **0:10:00** (well under any queue’s cap).

#### 2. Eliminate queues that violate limits

| Queue | Node minimum (req. 4) | Node maximum (req. 4) | Max walltime (req. 0:10:00) | Verdict |
|-------|------------------------|------------------------|-----------------------------|---------|
| debug | 1 ≤ 4 **PASS** | 2 ≥ 4 **FAIL** | 1 h ≥ 0:10 **PASS** | **REJECT** (node max) |
| **debug-scaling** | **1 ≤ 4 PASS** | **10 ≥ 4 PASS** | **1 h ≥ 0:10 PASS** | **ACCEPT** |
| prod | 10 ≤ 4 **FAIL** | 496 ≥ 4 PASS | 24 h ≥ 0:10 PASS | **REJECT** (node min) |
| demand | 1 ≤ 4 PASS | 56 ≥ 4 PASS | 1 h ≥ 0:10 PASS | ACCEPT (but less targeted) |
| preemptable | 1 ≤ 4 PASS | 10 ≥ 4 PASS | 72 h ≥ 0:10 PASS | ACCEPT (preemptable not needed) |
| capacity | 1 ≤ 4 PASS | 4 ≥ 4 PASS | 168 h ≥ 0:10 PASS | ACCEPT (but 4-node max limits scaling range) |

#### 3. Final queue choice: **debug-scaling**
- Purpose-built for scaling benchmarks (name, 1–10 node range, 1 h walltime).
- All three limits **PASS** for the requested 4 nodes and 0:10:00 walltime.

---

### (b) Ranks per node & GPUs per rank — from build defaults
- **Ranks per node**: 4 (explicitly stated as build default; GA library expects this).
- **GPUs per node**: 0 — NWChem build is **CPU-only**; “GPU support is experimental and not standard in community releases.” No GPU resources are requested or used.

---

### (c) Timing assumptions & margin
- **Assumed**: Single-node time = 5 s (given). Strong scaling of this microscopic problem will not reduce time further; 30 s is a safe upper bound for any node count in the test range.
- **Margin**: 20× (600 s → 0:10:00). No measured throughput data exists; margin covers variability, GA initialization, and multiple repetitions per node count.

---

### (d) Scaling guidance adherence
- Guidance: “4 MPI ranks per node. Scale nodes for larger molecular systems.”
- **This run**: Problem is *not* a larger molecular system (single H₂O). The guidance therefore advises *against* expecting good scaling efficiency — but the **goal is a scaling benchmark**, i.e., to *characterise* where scaling breaks down. Running at 1, 2, 4, (and optionally 8) nodes fulfills that goal while honouring the 4-ranks-per-node directive.

---

### (e) Final verification
- **Total ranks** = nodes × ranks per node = 4 × 4 = **16** ✓
- All queue limits satisfied ✓
- GPU request matches build (0) ✓
- Walltime (0:10:00) < queue cap (1 h) ✓
````
