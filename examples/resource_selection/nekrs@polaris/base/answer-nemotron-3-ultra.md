# nemotron-3-ultra — nekrs@polaris, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**1. Size the work and derive the walltime**

*Reference measurement*: 1 node (4 GPUs) ran 1,000 timesteps in 8 min (kernels cached).  
*Problem size*: 32,000 spectral elements, polynomial order 7, 20,000 timesteps.  
The test run is assumed to use the same 32,000‑element mesh (the only size mentioned).  
Time per timestep on 1 node = 8 min / 1,000 = 0.48 s.  
1‑node time for 20,000 steps = 20,000 × 0.48 s = 9,600 s = **160 min (2.67 h)**.

*Strong‑scaling assumption*: NekRS scales by adding nodes (1 MPI rank/GPU, 4 GPUs/node).  
With *N* nodes (4*N* GPUs) we assume 80 % parallel efficiency relative to perfect scaling (typical for spectral‑element codes at this element‑per‑GPU count).  
Estimated time on *N* nodes = 160 min / (0.8 × *N*) = 200 / *N* minutes.

*Safety margin*: Add 20 % for I/O, statistics collection, and run‑to‑run variability.  
**Requested walltime** = 1.2 × 200 / *N* = **240 / *N* minutes**.

*Node‑count choice*: We want ≥10 nodes to use the production queue and keep elements/GPU ≥500 (32,000 elements / (4 GPUs × *N*)).  
*N* = 16 gives 500 elements/GPU, estimated walltime = 240/16 = **15 min**.  
Request **30 min (0:30:00)** to provide a comfortable cushion without exceeding any queue cap.

---

**2. Queue elimination table**

| Queue          | Node range | Max walltime | Node min (16) | Node max (16) | Walltime (0.5 h) | Verdict |
|----------------|------------|--------------|---------------|---------------|------------------|---------|
| debug          | 1–2        | 1 h          | PASS (1≤16)   | **FAIL** (2<16) | PASS (0.5≤1)     | **REJECT** |
| debug‑scaling  | 1–10       | 1 h          | PASS          | **FAIL** (10<16) | PASS             | **REJECT** |
| **prod**       | **10–496** | **24 h**     | **PASS** (10≤16) | **PASS** (496≥16) | **PASS** (0.5≤24) | **ACCEPT** |
| demand         | 1–56       | 1 h          | PASS          | PASS (56≥16)  | PASS (0.5≤1)     | ACCEPT (but not production‑oriented) |
| preemptable    | 1–10       | 72 h         | PASS          | **FAIL** (10<16) | PASS             | **REJECT** |
| capacity       | 1–4        | 168 h        | PASS          | **FAIL** (4<16)  | PASS             | **REJECT** |

Only **prod** and **demand** survive all three limits. The **prod** queue is designed for production runs (10–496 nodes, 24 h) and is the natural choice for a production NekRS job.

---

**3. Final resource specification (prod queue)**

| Parameter          | Value | Source / Reasoning |
|--------------------|-------|---------------------|
| **Nodes**          | 16    | Chosen for ≥500 elements/GPU and ≥10 nodes (prod minimum) |
| **GPUs per node**  | 4     | Polaris hardware (4 × A100); NekRS uses 1 rank/GPU |
| **Ranks per node** | 4     | Build default: 1 MPI rank per GPU → 4 ranks/node |
| **Total ranks**    | 64    | 16 nodes × 4 ranks/node |
| **Walltime**       | 0:30:00 (30 min) | 240/16 min = 15 min estimate + 20 % margin = 18 min; rounded to 30 min, well under 24 h cap |
| **Queue**          | prod  | Only production queue that admits 16 nodes and 30 min walltime |

**Checks**  
- Total ranks = nodes × ranks per node = 16 × 4 = 64 ✓  
- Node count 16 ∈ [10, 496] ✓  
- Walltime 0.5 h ≤ 24 h ✓  

**Assumptions stated**  
- Test run used the full 32,000‑element mesh.  
- Strong‑scaling efficiency = 80 % (no scaling data provided).  
- 20 % safety margin added to scaled estimate.  
- Kernels already precompiled (cached from prior run), so no --build‑only needed.
````
