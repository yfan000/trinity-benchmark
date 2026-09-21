# nemotron-3-ultra — qmcpack@aurora, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**Resource Specification**

| Parameter | Value |
|-----------|-------|
| Nodes | 2 |
| Ranks per node | 6 (build default) |
| Total MPI ranks | 12 |
| GPUs per node | 6 (one per rank / GPU tile) |
| Walltime | 45 minutes (0:45:00) |
| Queue | capacity |

**Reasoning**

**(a) Queue selection — step by step**

1. **Size the work and derive walltime**  
   - Problem: 64-atom Si (2×2×2 diamond supercell), Slater–Jastrow DMC, 4096 walkers, 200 blocks, τ = 0.005 Ha⁻¹.  
   - No prior timing exists. Assumptions:  
     * QMCPACK on Intel PVC (Aurora) processes ~300–350 walkers/rank/block in ~2–4 s for a system this size.  
     * With 2 nodes × 6 ranks = 12 ranks → 4096/12 ≈ 341 walkers/rank.  
     * 200 blocks × 3 s/block ≈ 600 s (10 min) pure propagate; add VMC equilibration, I/O, startup, load imbalance → ~25–30 min.  
     * **Margin**: +50 % (15 min) for variability → **45 min requested**.  
   - *No measured throughput is claimed; the figure is an assumption with explicit margin.*

2. **Eliminate queues that cannot accept 2 nodes / 45 min**  

   | Queue | Node min | Node max | Walltime max | Node range | Walltime |
   |-------|----------|----------|--------------|------------|----------|
   | debug | 1 | 2 | 1 h | 2 ∈ [1,2] **PASS** | 45 min < 60 min **PASS** |
   | debug-scaling | 2 | 256 | 1 h | 2 ∈ [2,256] **PASS** | 45 min < 60 min **PASS** |
   | prod | 256 | 10624 | 24 h | 2 < 256 **FAIL** (node min) | — |
   | capacity | 1 | 16 | 168 h | 2 ∈ [1,16] **PASS** | 45 min ≪ 168 h **PASS** |
   | visualization | 1 | 32 | 8 h | 2 ∈ [1,32] **PASS** | 45 min < 8 h **PASS** |

   Queues **prod** is eliminated (node minimum 256 > 2). The other four survive.

3. **Choose surviving queue**  
   - *debug* / *debug-scaling*: 1 h walltime cap leaves only 15 min margin; intended for interactive debugging/scaling tests, not production reproduction.  
   - *visualization*: dedicated to rendering workloads.  
   - **capacity**: designed for production runs up to 168 h; 45 min is well within limit, 2 nodes within 1–16 range. **Selected.**

   **Final limit check for capacity queue**  
   - Node minimum: 1 ≤ 2 **PASS**  
   - Node maximum: 16 ≥ 2 **PASS**  
   - Maximum walltime: 168 h ≥ 0.75 h **PASS**

**(b) Ranks per node & GPUs per rank**  
Taken from build defaults: **6 ranks/node** (one per GPU tile), **1 GPU/rank**. Only node count (2) is chosen.

**(c) Timing assumption statement**  
No timing measurement was supplied. The 45 min request assumes ~3 s/block/rank at 341 walkers/rank on PVC, plus 50 % margin for overhead and variability.

**(d) Scaling guidance**  
QMCPACK’s SYCL build targets 1 rank per GPU tile (6/node). With 4096 walkers, strong scaling remains efficient down to ~150 walkers/rank (≈4–5 nodes). Two nodes (341 walkers/rank) sits comfortably in the strong-scaling regime; no scaling limitation applies.

**(e) Closure**  
- Nodes: 2  
- Ranks per node: 6  
- Total ranks: 2 × 6 = 12  
- GPUs per node: 6  
- Walltime: 45 minutes  
- Queue: capacity
````
