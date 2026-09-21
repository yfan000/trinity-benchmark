# Reference answer — nekrs@polaris

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
Step 1 — Size the work and estimate walltime.

Measured: 1 node, 4 GPUs, 1,000 timesteps → ~8 minutes (kernels already cached, so no precompilation overhead).

Base cost for 20,000 timesteps on 1 node = 8 × (20,000/1,000) = 160 minutes wall time at 1 node.

Scaling up to 16 nodes (a clean power-of-2 that gives 64 MPI ranks and maps evenly onto 32,000 elements):
- Ideal strong-scaling speedup: 16×, giving 160/16 = 10 minutes compute.
- NekRS scales well on A100s but not perfectly; assume 70 % parallel efficiency → effective time ≈ 10/0.70 ≈ 14 minutes compute.
- Add 30 % scheduling/I/O margin → ~18–19 minutes. Round up conservatively to 30 minutes (1800 s). This is a stated assumption, not a measured figure.

Step 2 — Eliminate queues.

| Queue | Max walltime | Max nodes | Reason eliminated |
|---|---|---|---|
| debug | 1 h | 2 nodes | Node max 2 < 16 — ruled out |
| debug-scaling | 1 h | 10 nodes | Node max 10 < 16 — ruled out |
| demand | 1 h | 56 nodes | By-request-only access; not available by default — ruled out |
| preemptable | 72 h | 10 nodes | Node max 10 < 16 — ruled out |
| capacity | 168 h | 4 nodes | Node max 4 < 16 — ruled out |
| prod | 24 h | 496 nodes (min 10) | Survives — check below |

Step 3 — Verify prod queue against all three limits.

| Limit | Requested | Queue limit | Verdict |
|---|---|---|---|
| Node minimum | 16 nodes | 10 nodes minimum | PASS |
| Node maximum | 16 nodes | 496 nodes maximum | PASS |
| Maximum walltime | 30 min (1800 s) | 24 h (86400 s) | PASS |

All three lines read PASS. No adjustment needed.

Scaling guidance honoured: The application scaling notes state 'nekRS uses 1 MPI rank per GPU (4 per node on Polaris). Scale by increasing node count.' The build default of 4 ranks per node is used unchanged. Node count is the only free parameter chosen here.

GPU/rank mapping (from build defaults): 4 ranks per node, 1 GPU per rank → 4 GPUs per node, matching Polaris hardware.

Kernel precompilation: The scaling notes warn to precompile kernels with --build-only on first run to avoid timeout. The prior 1-node run has already cached the kernels; the walltime estimate excludes precompilation overhead.

Final specification:
- Nodes: 16
- Ranks per node: 4 (build default; not agent's choice to change)
- Total ranks: 16 × 4 = 64
- GPUs per node: 4 (1 per rank, per build default)
- Total GPUs: 64
- Walltime: 30 minutes (1800 s) — assumed, with 30 % margin over a scaled-efficiency estimate; no measured throughput was available beyond the 1-node timing
- Queue: prod

Total ranks = nodes × ranks per node = 16 × 4 = 64 ✓
````
